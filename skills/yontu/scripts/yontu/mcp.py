"""MCP stdio server: JSON-RPC 2.0, one message per line, stdlib only.

    yontu mcp

Methods: initialize, notifications/initialized, ping, tools/list, tools/call,
prompts/list, prompts/get. Every tool calls the public package API; nothing here
re-implements linting. Logs go to stderr, stdout carries only protocol messages.

tools/list shows three tools by default (lint_text, compare_texts, get_style_guide) to keep
the agent's context small. YONTU_MCP_TOOLS=full lists all eight. tools/call accepts all
eight either way, so older clients keep working.
"""
import io
import json
import os
import sys

from . import __version__
from . import engine
from . import fidelity
from . import metrics
from . import paths
from . import profiller
from . import textutil as tu

PROTOCOLS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
LEVEL_NAMES = ("info", "warning", "error")
DEFAULT_TOOLS = ("lint_text", "compare_texts", "get_style_guide")
# Findings keep these keys unless lint_text gets detail: true.
SLIM_KEYS = ("id", "layer", "level", "line", "col", "match", "message", "suggestion", "fix",
             "evidence")
MATCH_MAX = 120

INSTRUCTIONS = (
    "yontu checks Turkish text offline: TDK spelling and punctuation, AI and translation "
    "tells, genre (tür) style, wordy phrasing. Call lint_text before a rewrite and "
    "compare_texts(old, new) after it; revert any edit compare reports as error. Only tdk "
    "findings are errors. get_style_guide returns one tür profile (blog, haber, ...) or one "
    "section of a reference.")


class ToolError(Exception):
    """Reported to the client as a tool result with isError true."""


# --- tool schemas -------------------------------------------------------------------

def _s(desc, **kw):
    d = {"type": "string", "description": desc}
    d.update(kw)
    return d


_TEXT = _s("Turkish text (Markdown allowed; code, URLs and quotes are skipped).")
_REG = _s("Register slug, for example akademik, blog, teknik, hukuk. Auto-detected when omitted.")
_TUR = _s("Tür (genre profile) id, for example blog, haber, commit. See list_profiles.")
_RO = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True,
       "openWorldHint": False}


def _tool(name, title, desc, props, required=()):
    return {"name": name, "title": title, "description": desc,
            "inputSchema": {"type": "object", "properties": props, "required": list(required),
                            "additionalProperties": False},
            "annotations": dict(_RO, title=title)}


def topics():
    """(references dir, sorted topic names). Topics: 'skill', every reference path
    without .md ("ai-oruntuleri", "turler/blog") and each bare tür id ("blog")."""
    ref = paths.references_dir()
    if ref is None:
        return None, []
    names = [f[:-3] for f in paths.reference_files()]
    names += [n[len("turler/"):] for n in names if n.startswith("turler/")]
    if os.path.isfile(os.path.join(paths.skill_dir(), "SKILL.md")):
        names.append("skill")
    return ref, sorted(set(names))


def _topic_path(topic):
    """File for a topic name; a bare tür id resolves to turler/<id>.md."""
    if topic == "skill":
        return os.path.join(paths.skill_dir(), "SKILL.md")
    return paths.reference_path(topic) or paths.reference_path("turler/" + topic)


def tool_mode():
    return "full" if os.environ.get("YONTU_MCP_TOOLS", "").strip().lower() == "full" else "default"


def tools(mode=None):
    """Every tool schema, or only the default surface (see the module docstring)."""
    out = all_tools()
    if (mode or tool_mode()) != "full":
        out = [t for t in out if t["name"] in DEFAULT_TOOLS]
    return out


def all_tools():
    _, tops = topics()
    topic = _s("A tür id (blog, haber, linkedin, ...), a reference name (ai-oruntuleri, "
               "noktalama-yazim, yogunlastirma, asiri-duzeltme, ...) or 'skill' for the "
               "workflow.")
    return [
        _tool("lint_text", "Lint Turkish text",
              "Lint Turkish text. Findings carry id, layer (tdk, ai-iz, stil, yogunluk), level, "
              "line, col, match, message and suggestion or fix. Only tdk findings are errors.",
              {"text": _TEXT, "register": _REG, "tur": _TUR,
               "layers": {"type": "array", "items": {"type": "string", "enum": list(engine.LAYERS)},
                          "description": "Limit to these layers."},
               "min_level": _s("Drop findings below this level.", enum=list(LEVEL_NAMES)),
               "filename": _s("File name used only for register detection, e.g. README.md."),
               "enable": {"type": "array", "items": {"type": "string"},
                          "description": "Turn on default-off rules by id or tag."},
               "detail": {"type": "boolean",
                          "description": "Return every finding field (offsets, source)."}},
              ["text"]),
        _tool("fix_text", "Apply safe TDK fixes",
              "Apply only the safe tdk-layer autofixes. Returns the fixed text and the tdk "
              "findings left over. Style and AI findings are never auto-applied.",
              {"text": _TEXT, "register": _REG, "tur": _TUR}, ["text"]),
        _tool("compare_texts", "Fidelity gate",
              "Compare an original and a rewrite. error: a number, date, URL, code or name "
              "appears that the original lacks. warning: removed item, changed negation or "
              "modality. Revert edits that cause errors.",
              {"old": _s("Original text."), "new": _s("Rewritten text.")}, ["old", "new"]),
        _tool("text_stats", "Text statistics",
              "Sentence length, Ateşman readability, paragraph count and per-300-word "
              "densities, with the band for the register or tür.",
              {"text": _TEXT, "register": _REG, "tur": _TUR}, ["text"]),
        _tool("explain_rule", "Explain a rule",
              "Full definition of one rule: message, level, evidence, source and examples.",
              {"id": _s("Rule id, for example YZ-03 or AI-E6.")}, ["id"]),
        _tool("list_profiles", "List profiles",
              "All register slugs and tür profiles with their register.", {}),
        _tool("get_profile", "Get a profile",
              "One tür profile (sentence band, formality, mood, connectives, vocabulary, "
              "punctuation, structure, typical AI errors, examples), or a register with its türler.",
              {"tur": _s("Tür id or register slug.")}, ["tur"]),
    ] + ([_tool("get_style_guide", "Get a style guide",
                "Markdown guidance. A tür id returns that profile. A reference without "
                "section returns its section list; pass section to get one.",
                {"topic": topic,
                 "section": _s("Heading text or part of it, e.g. 'Bağlaç zinciri'.")},
                ["topic"])] if tops else [])


# --- tool implementations -----------------------------------------------------------

def _str(args, key, required=False):
    value = args.get(key)
    if value is None or (value == "" and not required):
        if required:
            raise ToolError("missing argument: %s" % key)
        return None
    if not isinstance(value, str):
        raise ToolError("argument must be a string: %s" % key)
    return value


def _list(args, key):
    value = args.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ToolError("argument must be a list of strings: %s" % key)
    return value


def _counts(findings):
    c = {"error": 0, "warning": 0, "info": 0}
    for f in findings:
        c[f["level"]] += 1
    return c


def _slim(f):
    out = {}
    for k in SLIM_KEYS:
        v = f.get(k)
        if v is None:
            continue
        if k == "match" and len(v) > MATCH_MAX:
            v = v[:MATCH_MAX] + "…"
        out[k] = v
    return out


def t_lint(args):
    text = _str(args, "text", True)
    detail = args.get("detail", False)
    if not isinstance(detail, bool):
        raise ToolError("argument must be a boolean: detail")
    layers = _list(args, "layers")
    if layers:
        bad = [x for x in layers if x not in engine.LAYERS]
        if bad:
            raise ToolError("unknown layer: %s" % ", ".join(bad))
    level = _str(args, "min_level") or "info"
    if level not in LEVEL_NAMES:
        raise ToolError("unknown min_level: %s" % level)
    cfg = {"enable": _list(args, "enable") or []}
    engine.check_config(cfg)
    res = engine.lint(text, _str(args, "register"), _str(args, "tur"), cfg,
                      filename=_str(args, "filename"), layers=tuple(layers) if layers else None,
                      min_level=level)
    res["counts"] = _counts(res["findings"])
    if not detail:
        res["findings"] = [_slim(f) for f in res["findings"]]
    return res


def t_fix(args):
    text = _str(args, "text", True)
    reg, tur = _str(args, "register"), _str(args, "tur")
    fixed = engine.fix(text, reg, tur)
    left = engine.lint(fixed, reg, tur, layers=("tdk",))["findings"]
    return {"text": fixed, "changed": fixed != text, "remaining": left,
            "counts": _counts(left)}


def t_compare(args):
    return fidelity.compare(_str(args, "old", True), _str(args, "new", True))


def t_stats(args):
    return metrics.stats(_str(args, "text", True), _str(args, "register"), _str(args, "tur"))


def t_explain(args):
    d = engine.rule_data(_str(args, "id", True))
    if d is None:
        raise ToolError("unknown rule: %s" % args.get("id"))
    return d


def t_list(args):
    regs = profiller.registers()
    profs = profiller.profiles()
    return {"registers": [{"id": k, "name": v.get("name"), "default_tur": v.get("default_tur")}
                          for k, v in sorted(regs.items())],
            "profiles": [{"id": k, "p": v.get("p"), "name": v.get("name"),
                          "register": v.get("register")} for k, v in profs.items()]}


def t_profile(args):
    key = _str(args, "tur", True)
    data = profiller.lookup(key)
    if data is None:
        raise ToolError("unknown tür or register: %s (see list_profiles)" % key)
    return data


def _heading(row):
    """(level, title) for a Markdown heading row outside code, else None."""
    if not row.startswith("#"):
        return None
    level = len(row) - len(row.lstrip("#"))
    if level > 6 or row[level:level + 1] != " ":
        return None
    return level, row[level + 1:].strip()


def _outline(text, topic):
    rows, intro, heads, fence = text.split("\n"), [], [], False
    for row in rows:
        if row.startswith("```"):
            fence = not fence
        h = None if fence else _heading(row)
        if h and h[0] >= 2:
            heads.append("  " * (h[0] - 2) + "- " + h[1])
        elif not heads:
            intro.append(row)
    return ("\n".join(intro).strip() + "\n\nSections of %s (call again with section):\n%s\n"
            % (topic, "\n".join(heads)))


def _section(text, want):
    """The first heading that equals, starts with or contains want, with its body."""
    rows, key, fence, heads = text.split("\n"), tu.tr_lower(want).strip(" #"), False, []
    for i, row in enumerate(rows):
        if row.startswith("```"):
            fence = not fence
        h = None if fence else _heading(row)
        if h is not None:
            heads.append((i, h[0], tu.tr_lower(h[1]).strip("`\"' ")))
    if not key:
        return None
    for test in (lambda s: s == key, lambda s: s.startswith(key), lambda s: key in s):
        hit = [x for x in heads if test(x[2])]
        if hit:
            i, level, _ = hit[0]
            end = next((j for j, lv, _ in heads if j > i and lv <= level), len(rows))
            return "\n".join(rows[i:end]).strip() + "\n"
    return None


def t_guide(args):
    topic = _str(args, "topic", True)
    section = _str(args, "section")
    ref, tops = topics()
    if ref is None:
        raise ToolError("style guides are not installed with this package; "
                        "use the skill directory or the repository")
    note = ""
    name = topic[:-3] if topic.endswith(".md") else topic
    if name not in tops:
        tur = profiller.canonical_tur(name)
        if tur and tur in tops:
            if tur != name:
                note = "Topic %r maps to the tür %r.\n\n" % (topic, tur)
            name = tur
    if name not in tops:
        refs = sorted(t for t in tops if "/" not in t and t not in profiller.profiles())
        raise ToolError("unknown topic: %s. Use a tür id (blog, haber, ...; list_profiles), "
                        "'skill' or a reference: %s" % (topic, ", ".join(refs)))
    topic = name
    path = _topic_path(topic)
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    if section:
        part = _section(text, section)
        if part is None:
            raise ToolError("no section matching %r in %s\n\n%s" % (section, topic,
                                                                    _outline(text, topic)))
        return note + part
    if topic == "skill" or os.path.dirname(path) != ref or topic == "turler":
        return note + text  # the workflow, one tür profile, or the tür index: small and whole
    return note + _outline(text, topic)


def _SCHEMA_KEYS():
    return {t["name"]: set(t["inputSchema"]["properties"]) for t in all_tools()}


HANDLERS = {"lint_text": t_lint, "fix_text": t_fix, "compare_texts": t_compare,
            "text_stats": t_stats, "explain_rule": t_explain, "list_profiles": t_list,
            "get_profile": t_profile, "get_style_guide": t_guide}


# --- prompts --------------------------------------------------------------------------

_GUIDE_KEYS = (("amac", "Purpose"), ("uzunluk", "Length"), ("resmiyet", "Formality"),
               ("kip", "Mood and tense"), ("baglaclar", "Connectives"), ("sozcuk", "Vocabulary"),
               ("noktalama", "Punctuation"), ("yapi", "Structure"))

PROMPTS = [
    {"name": "turkcelestir", "title": "Türkçeleştir",
     "description": "Translate or adapt a text into natural Turkish for its genre, "
                    "then check it with yontu.",
     "arguments": [{"name": "text", "description": "Source text (any language).", "required": True},
                   {"name": "tur", "description": "Target tür id, e.g. blog, haber, teknik-dok.",
                    "required": False}]},
    {"name": "yogunlastir", "title": "Yoğunlaştır",
     "description": "Make a Turkish text shorter and plainer without losing content.",
     "arguments": [{"name": "text", "description": "Turkish text.", "required": True},
                   {"name": "tur", "description": "Tür id, e.g. blog, akademik-ozet.",
                    "required": False}]},
]


def _profile_lines(tur):
    if not tur:
        return []
    tur = profiller.canonical_tur(tur) or tur
    prof = profiller.profiles().get(tur)
    if prof is None:
        raise ValueError("unknown tür: %s" % tur)
    g = prof.get("guidance") or {}
    lines = ["", "Target genre: %s (%s, register %s)." % (prof.get("name"), tur, prof.get("register"))]
    for key, label in _GUIDE_KEYS:
        if g.get(key):
            lines.append("- %s: %s" % (label, g[key]))
    if g.get("ai_hatalari"):
        lines.append("- Typical AI errors to avoid: " + " / ".join(g["ai_hatalari"]))
    return lines


def prompt_text(name, args):
    text = args.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("missing argument: text")
    tur = args.get("tur") or None
    if name == "turkcelestir":
        head = [
            "Translate or adapt the text below into natural Turkish written for its real reader.",
            "If it is already Turkish, rewrite only what reads as translation or AI output.",
            "Keep every fact, number, date, name, negation, modality and hedge. Add nothing.",
            "Follow TDK spelling and punctuation. No em dash, no chatbot opener or closer.",
            "Workflow: write a faithful first translation, then call lint_text on your draft and "
            "fix tdk errors, then improve the style, then call compare_texts with the first "
            "translation as old and the final text as new and revert any edit it reports as error.",
            "Return only the final Turkish text.",
        ]
    elif name == "yogunlastir":
        head = [
            "Make the Turkish text below shorter and plainer without dropping any content.",
            "Cut light verbs, wrappers and tautology (\"bir şekilde\", \"yapılmaktadır\", "
            "\"olarak\" chains). Near-synonym pairs are not automatically redundant; "
            "\"katkı sunmak\" is acceptable.",
            "Call lint_text with layers [\"yogunluk\", \"tdk\"] for candidates. They are "
            "suggestions, not orders.",
            "Then call compare_texts with the original as old and your version as new; revert "
            "any edit it reports as error and check every warning.",
            "Return only the final text.",
        ]
    else:
        raise KeyError(name)
    lines = head + _profile_lines(tur) + ["", "Text:", "", text]
    return "\n".join(lines)


# --- JSON-RPC ------------------------------------------------------------------------

class RpcError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
        self.message = message


def _error(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


class Server(object):
    def __init__(self):
        self.protocol = PROTOCOLS[0]

    def initialize(self, params):
        asked = params.get("protocolVersion")
        self.protocol = asked if asked in PROTOCOLS else PROTOCOLS[0]
        return {"protocolVersion": self.protocol,
                "capabilities": {"tools": {"listChanged": False},
                                 "prompts": {"listChanged": False}},
                "serverInfo": {"name": "yontu", "title": "yontu", "version": __version__},
                "instructions": INSTRUCTIONS}

    def call_tool(self, params):
        name = params.get("name")
        if not isinstance(name, str) or name not in HANDLERS:
            raise RpcError(-32602, "unknown tool: %s" % (name,))
        args = params.get("arguments") or {}
        if not isinstance(args, dict):
            raise RpcError(-32602, "arguments must be an object")
        try:
            known = _SCHEMA_KEYS().get(name)
            extra = sorted(k for k in args if known is not None and k not in known)
            if extra:  # inputSchema says additionalProperties: false
                raise ToolError("unknown argument: %s" % ", ".join(extra))
            data = HANDLERS[name](args)
        except (ToolError, ValueError) as exc:
            return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
        if isinstance(data, str):
            return {"content": [{"type": "text", "text": data}], "isError": False}
        out = {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}],
               "isError": False}
        if self.protocol >= "2025-06-18":
            out["structuredContent"] = data
        return out

    def get_prompt(self, params):
        name = params.get("name")
        spec = [p for p in PROMPTS if p["name"] == name]
        if not spec:
            raise RpcError(-32602, "unknown prompt: %s" % name)
        args = params.get("arguments") or {}
        try:
            text = prompt_text(name, args if isinstance(args, dict) else {})
        except ValueError as exc:
            raise RpcError(-32602, str(exc))
        return {"description": spec[0]["description"],
                "messages": [{"role": "user", "content": {"type": "text", "text": text}}]}

    def dispatch(self, method, params):
        if method == "initialize":
            return self.initialize(params)
        if method == "ping":
            return {}
        if method == "tools/list":
            return {"tools": tools()}
        if method == "tools/call":
            return self.call_tool(params)
        if method == "prompts/list":
            return {"prompts": PROMPTS}
        if method == "prompts/get":
            return self.get_prompt(params)
        raise RpcError(-32601, "method not found: %s" % method)

    def handle(self, msg):
        """One decoded message in, response dict out, or None for notifications."""
        if isinstance(msg, list):
            if not msg:
                return _error(None, -32600, "empty batch")
            out = [r for r in (self.handle(m) for m in msg) if r is not None]
            return out or None
        if not isinstance(msg, dict):
            return _error(None, -32600, "invalid request")
        if "method" not in msg and ("result" in msg or "error" in msg):
            return None  # a response from the client; this server sends no requests
        mid = msg.get("id")
        if "method" not in msg or msg.get("jsonrpc") != "2.0":
            if "id" not in msg:
                return None  # malformed notification: JSON-RPC sends no reply
            ok_id = not isinstance(mid, bool) and isinstance(mid, (str, int, float, type(None)))
            return _error(mid if ok_id else None, -32600, "invalid request")
        notify = "id" not in msg
        if not notify and (isinstance(mid, bool) or not isinstance(mid, (str, int, float, type(None)))):
            return _error(None, -32600, "invalid request: id must be a string or number")
        method = msg.get("method")
        params = msg.get("params") or {}
        if not isinstance(method, str) or not isinstance(params, dict):
            return None if notify else _error(mid, -32600, "invalid request")
        if notify:
            return None  # notifications/initialized, notifications/cancelled, ...
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": self.dispatch(method, params)}
        except RpcError as exc:
            return _error(mid, exc.code, exc.message)
        except Exception as exc:
            sys.stderr.write("yontu mcp: %s failed: %r\n" % (method, exc))
            return _error(mid, -32603, "internal error")


def serve(inp=None, out=None):
    """Read newline-delimited JSON-RPC from inp (bytes), write responses to out (bytes)."""
    inp = inp or sys.stdin.buffer
    out = out or sys.stdout.buffer
    server = Server()
    while True:
        raw = inp.readline()
        if not raw:
            return 0
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            resp = _error(None, -32700, "parse error")
        else:
            resp = server.handle(msg)
        if resp is not None:
            out.write(json.dumps(resp, ensure_ascii=False).encode("utf-8") + b"\n")
            out.flush()
