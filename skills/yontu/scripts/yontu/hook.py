"""Agent hooks: one implementation, one JSON contract per agent.

    yontu hook --format claude|codex|cursor|gemini|antigravity|copilot|hermes
               --event stop|post-edit

Reads the agent's hook payload from stdin and prints exactly one JSON object
(`{}` when there is nothing to report). It never fails the agent: any internal
error is logged to stderr and the hook exits 0 with `{}`.

Environment:
    YONTU_DISABLE=1          turn every hook off (also: a `.yontu-ignore` file)
    YONTU_STOP_MODE          advisory (default) | context | block
    YONTU_HOOK_LEVEL         error (default) | warning | info
"""
import io
import json
import os
import re
import sys

from . import engine
from . import profiller
from . import textutil as tu

FORMATS = ("claude", "codex", "cursor", "gemini", "antigravity", "copilot", "hermes")
EVENTS = ("stop", "post-edit")
STOP_MODES = ("advisory", "context", "block")
TEXT_EXT = (".md", ".mdx", ".markdown", ".txt")
IGNORE_FILE = ".yontu-ignore"
MAX_BYTES = 512 * 1024
MAX_TRANSCRIPT = 4 * 1024 * 1024
MAX_CONTEXT = 3000
MAX_ITEMS = 10
MAX_FILES = 5
MIN_WORDS = 8
# Chat artifacts that are wrong in any delivered text. AI-E9 (placeholder) is left out:
# in a chat answer a bracketed slot is often what the user asked for.
HIGH_CONFIDENCE = ("AI-E6", "AI-E7", "AI-E8")

_TR_WORDS = set("""
ve bir bu için ile de da ki mi mı mu mü ne ama çok daha gibi olarak değil var yok şu o en
her olan sonra kadar göre ancak veya ya hem diye ise nasıl neden şimdi şey biz ben sen siz
bunu bunun şunu olur oldu olduğu yani artık önce hiç bile yine zaten sadece sonra şöyle
""".split())
_EN_WORDS = set("""
the and of to is in that it for with as this are be was you not or by an from at have
can will if we which but what all there their has would should could when then than
""".split())
_PATCH_FILE = re.compile(r"^\*\*\* (?:Update|Add) File: (.+?)\s*$", re.M)
# Hooks without a matcher (Copilot) also fire for tools that only read a file.
_READ_TOOL = re.compile(r"^(?:read|view|grep|glob|ls|list|search|fetch)"
                        r"(?:_?(?:file|files|many_files|dir|directory))?$", re.I)
_PATH_KEYS = ("file_path", "filePath", "path", "target_file", "TargetFile", "absolute_path",
              "AbsolutePath", "filename")


def log(msg):
    try:
        sys.stderr.write("yontu hook: %s\n" % msg)
    except Exception:  # pragma: no cover - stderr closed
        pass


# --- language ------------------------------------------------------------------

def prose(text):
    """Text with code, URLs, paths and markup blanked out (same mask as the linter)."""
    return tu.apply_mask(text, tu.build_mask(text))


def turkish_share(text):
    """(words, Turkish-looking words, English function words) in the prose part of text."""
    ws = [tu.tr_lower(w) for w in tu.words(prose(tu.nfc(text))) if not w[0].isdigit()]
    tr = sum(1 for w in ws if w in _TR_WORDS or any(c in "çğıöşü" for c in w))
    en = sum(1 for w in ws if w in _EN_WORDS)
    return len(ws), tr, en


def is_turkish(text):
    """True when the prose is mostly Turkish: enough words, Turkish share high, little English."""
    n, tr, en = turkish_share(text)
    return n >= MIN_WORDS and tr >= 0.3 * n and tr > 2 * en


# --- payload -------------------------------------------------------------------

def _as_obj(value):
    """Decode a JSON string (Copilot sends toolArgs as a string), keep dicts, else None."""
    for _ in range(2):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                return None
    return value if isinstance(value, dict) else None


def _first(payload, *keys):
    for k in keys:
        if payload.get(k) not in (None, ""):
            return payload[k]
    return None


def base_dir(payload):
    roots = (payload.get("workspace_roots") or payload.get("workspaceRoots")
             or payload.get("workspacePaths") or [])
    for cand in (_first(payload, "cwd"), roots[0] if roots else None,
                 os.environ.get("CLAUDE_PROJECT_DIR"), os.environ.get("GEMINI_PROJECT_DIR")):
        if isinstance(cand, str) and cand:
            return cand
    return os.getcwd()


def read_only_tool(payload):
    name = _first(payload, "tool_name", "toolName")
    call = _as_obj(payload.get("toolCall") or payload.get("tool_call"))
    if not isinstance(name, str) and call:
        name = call.get("name")
    return isinstance(name, str) and bool(_READ_TOOL.search(name))


def edited_paths(payload):
    """Every file path the payload names, in order, without duplicates."""
    found = []

    def add(value):
        if isinstance(value, str) and value.strip():
            found.append(value.strip())

    def scan(obj):
        if not isinstance(obj, dict):
            return
        for key in _PATH_KEYS:
            add(obj.get(key))
        for key in ("paths", "files", "file_paths"):
            for item in obj.get(key) or []:
                add(item if isinstance(item, str) else (item or {}).get("path"))
        for key in ("input", "patch", "command", "content_patch"):
            if isinstance(obj.get(key), str) and "*** " in obj[key]:
                for m in _PATCH_FILE.finditer(obj[key]):
                    add(m.group(1))

    scan(payload)
    for key in ("tool_input", "toolInput", "toolArgs", "tool_args", "args", "arguments"):
        raw = payload.get(key)
        if isinstance(raw, str) and "*** " in raw and _as_obj(raw) is None:
            for m in _PATCH_FILE.finditer(raw):
                add(m.group(1))
        scan(_as_obj(raw))
    call = _as_obj(payload.get("toolCall") or payload.get("tool_call"))
    if call:
        scan(call)
        scan(_as_obj(call.get("args") or call.get("arguments")))
    scan(_as_obj(payload.get("tool_response") or payload.get("toolResponse")))
    out = []
    for p in found:
        if p not in out:
            out.append(p)
    return out


def _message_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") in (None, "text", "output_text"):
                if isinstance(item.get("text"), str):
                    parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


def transcript_last_assistant(path):
    """Last assistant text in a JSONL transcript (Claude shape and plain role/content shape)."""
    try:
        size = os.path.getsize(path)
        with io.open(path, "rb") as fh:
            if size > MAX_TRANSCRIPT:
                fh.seek(size - MAX_TRANSCRIPT)
            data = fh.read().decode("utf-8", "replace")
    except (IOError, OSError):
        return ""
    for line in reversed(data.splitlines()):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict):
            continue
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else rec
        role = msg.get("role") or rec.get("type")
        if role == "assistant":
            text = _message_text(msg.get("content"))
            if text.strip():
                return text
    return ""


def stop_text(payload):
    text = _first(payload, "last_assistant_message", "lastAssistantMessage", "prompt_response",
                  "response", "assistant_message")
    if isinstance(text, str) and text.strip():
        return text
    path = _first(payload, "transcript_path", "transcriptPath")
    if isinstance(path, str):
        return transcript_last_assistant(path)
    return ""


def stop_active(payload):
    """True when the agent is already continuing, or stopped for a reason other than a normal end."""
    if payload.get("stop_hook_active") or payload.get("stopHookActive"):
        return True
    if payload.get("terminationReason") not in (None, "", "NO_TOOL_CALL"):  # Antigravity
        return True
    try:
        return int(payload.get("loop_count") or payload.get("loopCount") or 0) > 0
    except (TypeError, ValueError):
        return False


# --- kill switch ----------------------------------------------------------------

def disabled(dirs):
    if os.environ.get("YONTU_DISABLE", "").strip().lower() in ("1", "true", "yes", "on"):
        return True
    seen = set()
    for d in dirs:
        if not d:
            continue
        d = os.path.abspath(d)
        while d not in seen:
            seen.add(d)
            if os.path.isfile(os.path.join(d, IGNORE_FILE)):
                return True
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return False


# --- linting ----------------------------------------------------------------------

def _config(start_dir):
    try:
        cfg = profiller.load_config(None, start_dir)
        if not isinstance(cfg, dict):
            raise ValueError("not an object")
        engine.check_config(cfg)
        return cfg
    except Exception as exc:  # broken .yontu.json must not break the agent
        log("ayar dosyası yok sayıldı (%s)" % exc)
        return {}


def strict(f):
    return (f["layer"] == "tdk" and f["level"] == "error") or f["id"] in HIGH_CONFIDENCE


def select(findings, level):
    if level == "info":
        return [f for f in findings if f["layer"] in ("tdk", "ai-iz") or strict(f)]
    if level == "warning":
        return [f for f in findings
                if strict(f) or (f["layer"] in ("tdk", "ai-iz") and f["level"] in ("warning", "error"))]
    return [f for f in findings if strict(f)]


def hook_level():
    level = os.environ.get("YONTU_HOOK_LEVEL", "error").strip().lower()
    return level if level in ("error", "warning", "info") else "error"


def _item(f):
    match = (f.get("match") or "").replace("\n", " ")
    if len(match) > 40:
        match = match[:40] + "..."
    hint = f.get("fix") if f.get("fix") is not None else f.get("suggestion")
    line = "- satır %d: “%s” %s (%s)" % (f["line"], match, f["message"], f["id"])
    if hint:
        line += " Öneri: %s" % hint
    return line


def report(title, findings):
    """Factual Turkish summary, at most MAX_ITEMS lines and MAX_CONTEXT characters."""
    errors = sum(1 for f in findings if f["level"] == "error")
    head = "yontu, %s: %d bulgu, %d hata." % (title, len(findings), errors)
    lines = [head]
    for f in findings[:MAX_ITEMS]:
        item = _item(f)
        if sum(len(x) + 1 for x in lines) + len(item) > MAX_CONTEXT - 80:
            break
        lines.append(item)
    left = len(findings) - (len(lines) - 1)
    if left > 0:
        lines.append("Gösterilmeyen %d bulgu var." % left)
    return "\n".join(lines)[:MAX_CONTEXT]


def lint_file(path, level):
    """Findings for one prose file, or None when the file is skipped."""
    if not path.lower().endswith(TEXT_EXT) or not os.path.isfile(path):
        return None
    if os.path.getsize(path) > MAX_BYTES:
        log("çok büyük, atlandı: %s" % path)
        return None
    try:
        with io.open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (IOError, OSError, UnicodeDecodeError) as exc:
        log("okunamadı: %s (%s)" % (path, exc))
        return None
    if not is_turkish(text):
        return None
    cfg = _config(os.path.dirname(path))
    res = engine.lint(text, config=cfg, filename=path)
    return select(res["findings"], level)


_QUOTED = re.compile(r'"([^"\n]{1,80})"|“([^”\n]{1,80})”')
_ARROW_LEFT = re.compile(r"[^\n:;,()\"“”]{1,60}?(?=[ \t]*(?:->|→))")
_TR_ONLY = re.compile("[çğıöşüÇĞİÖŞÜ]")


def _mentions(text):
    """Spans a reply uses to name a form rather than to write it: the left side of
    `X -> Y`, a quoted single word ("Ankara'lı") and a quoted non-Turkish string. A reply
    that names a wrong form to correct it should not be flagged for it. Longer quoted
    Turkish phrases stay checked."""
    spans = [m.span() for m in _ARROW_LEFT.finditer(text)]
    for m in _QUOTED.finditer(text):
        inner = (m.group(1) or m.group(2) or "").strip()
        if not _TR_ONLY.search(inner) or (inner and not any(c.isspace() for c in inner)):
            spans.append(m.span())
    return spans


def _quoted_match(text, f):
    """True when the finding's match is exactly the content of a quoted span around it."""
    for m in _QUOTED.finditer(text):
        g = 1 if m.group(1) is not None else 2
        if m.start(g) <= f["start"] and f["end"] <= m.end(g) and \
                m.group(g).strip() == text[f["start"]:f["end"]].strip():
            return True
    return False


def lint_reply(text, start_dir, level):
    if len(text.encode("utf-8")) > MAX_BYTES or not is_turkish(text):
        return None
    res = engine.lint(text, register="sohbet", config=_config(start_dir))
    spans = _mentions(text)
    found = [f for f in res["findings"]
             if not any(f["start"] <= e and s <= f["end"] for s, e in spans)
             and not _quoted_match(text, f)]
    return select(found, level)


# --- output contracts ---------------------------------------------------------------

def post_edit_output(fmt, payload, msg):
    if msg is None:
        return {}
    if fmt in ("claude", "codex"):
        return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}
    if fmt == "cursor":
        if (payload.get("hook_event_name") or payload.get("hookEventName")) == "afterFileEdit":
            log(msg)  # afterFileEdit has no feedback field
            return {}
        return {"additional_context": msg}
    if fmt == "copilot":
        return {"additionalContext": msg}
    if fmt == "gemini":
        return {"hookSpecificOutput": {"hookEventName": "AfterTool", "additionalContext": msg}}
    log(msg)  # antigravity PostToolUse and hermes post_tool_call have no feedback channel
    return {}


def stop_output(fmt, msg, trigger, active, mode):
    """trigger: the reply has strict findings. active: the agent is already continuing."""
    if msg is None:
        return {}
    act = trigger and not active
    if fmt == "claude":
        if mode == "block" and act:
            return {"decision": "block", "reason": msg}
        if mode == "context" and act:
            return {"systemMessage": msg.split("\n", 1)[0],
                    "hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": msg}}
        return {"systemMessage": msg}
    if fmt == "codex":
        if mode == "block" and act:
            return {"decision": "block", "reason": msg}
        return {"systemMessage": msg}
    if fmt == "gemini":
        if mode == "block" and act:
            return {"decision": "deny", "reason": msg}
        return {"systemMessage": msg}
    if fmt == "copilot":
        if mode == "block" and act:
            return {"decision": "block", "reason": msg}
        log(msg)
        return {}
    if fmt == "cursor":
        if mode == "block" and act:
            return {"followup_message": msg}
        log(msg)
        return {}
    if fmt == "antigravity":
        if mode == "block" and act:
            return {"decision": "continue", "reason": msg}
        log(msg)
        return {}
    log(msg)
    return {}


def stop_mode():
    mode = os.environ.get("YONTU_STOP_MODE", "advisory").strip().lower()
    return mode if mode in STOP_MODES else "advisory"


def _display(path, base):
    try:
        rel = os.path.relpath(path, base)
    except ValueError:
        return path
    return path if rel.startswith("..") else rel


def handle(fmt, event, payload):
    """Pure function: payload dict in, output dict out."""
    out = _handle(fmt, event, payload)
    if fmt == "antigravity" and event == "stop" and "decision" not in out:
        out = {"decision": "allow"}  # Antigravity requires a decision; anything but "continue" stops
    return out


def _handle(fmt, event, payload):
    if not isinstance(payload, dict):
        return {}
    base = base_dir(payload)
    level = hook_level()
    if event == "post-edit":
        if read_only_tool(payload):
            return {}
        paths = []
        for p in edited_paths(payload):
            full = p if os.path.isabs(p) else os.path.join(base, p)
            if full.lower().endswith(TEXT_EXT):
                paths.append(os.path.normpath(full))
        paths = paths[:MAX_FILES]
        if not paths or disabled([base, os.environ.get("CLAUDE_PROJECT_DIR")] +
                                 [os.path.dirname(p) for p in paths]):
            return {}
        parts = []
        for p in paths:
            found = lint_file(p, level)
            if found:
                parts.append(report(_display(p, base), found))
        msg = "\n".join(parts)[:MAX_CONTEXT] if parts else None
        return post_edit_output(fmt, payload, msg)
    if disabled([base, os.environ.get("CLAUDE_PROJECT_DIR")]):
        return {}
    found = lint_reply(stop_text(payload), base, level)
    if not found:
        return {}
    msg = report("son yanıt", found)
    return stop_output(fmt, msg, any(strict(f) for f in found), stop_active(payload), stop_mode())


def run(fmt, event, data):
    """Bytes or str from stdin in, one JSON line out. Never raises."""
    try:
        if isinstance(data, bytes):
            data = data.decode("utf-8", "replace")
        payload = json.loads(data) if data.strip() else {}
        out = handle(fmt, event, payload)
    except Exception as exc:  # fail open
        log("iç hata, atlandı: %r" % (exc,))
        out = {"decision": "allow"} if (fmt, event) == ("antigravity", "stop") else {}
    return json.dumps(out, ensure_ascii=False)
