"""Agent hooks: one sample payload per agent, stop modes, kill switches, fail-open."""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from ortak import PKG, ROOT
from yontu import hook

# BK-01 (tdk error: "birşey").
TDK_ERR = ("Bu raporu hazırladık ve sonuçları ekte bulabilirsiniz. Herkes birşey söyledi ama "
           "kimse dinlemedi, bu yüzden toplantı uzadı.")
# AI-E6 (chatbot self-reference), a strict finding outside the tdk layer.
CHATBOT = ("Bir yapay zekâ modeli olarak bu konuda kesin bir şey söyleyemem ama size genel bir "
           "çerçeve sunabilirim, bu da işinize yarar.")
# Only info findings (AI-E1, AI-E4).
INFO_ONLY = ("Elbette, işte istediğiniz özet. Proje takvimi iki hafta kaydı ve ekip yeni bir plan "
             "hazırlıyor. Umarım yardımcı olur!")
CLEAN = ("Toplantı salı günü saat onda başlayacak. Gündemde bütçe ve yeni işe alımlar var, "
         "herkesin notlarını getirmesi yeterli.")
ENGLISH = ("The meeting starts on Tuesday at ten and the agenda covers the budget and the new "
           "hires, so please bring your notes.")

CLEAR_ENV = ("YONTU_DISABLE", "YONTU_STOP_MODE", "YONTU_HOOK_LEVEL", "CLAUDE_PROJECT_DIR",
             "GEMINI_PROJECT_DIR")
# Fields the Codex 0.142.0 Stop output schema allows (additionalProperties false).
CODEX_STOP_KEYS = {"continue", "decision", "reason", "stopReason", "suppressOutput",
                   "systemMessage"}


def clean_env(**extra):
    env = {k: v for k, v in os.environ.items() if k not in CLEAR_ENV and k != "PYTHONPATH"}
    env["PYTHONIOENCODING"] = "utf-8"
    env.update(extra)
    return env


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        patcher = mock.patch.dict(os.environ, clean_env(), clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        quiet = mock.patch.object(hook, "log")
        quiet.start()
        self.addCleanup(quiet.stop)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def transcript(self, text, shape="claude"):
        if shape == "claude":
            rec = {"type": "assistant",
                   "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}
        else:
            rec = {"role": "assistant", "content": text}
        user = {"type": "user", "message": {"role": "user", "content": "soru"}}
        return self.write("t.jsonl", json.dumps(user) + "\n" + json.dumps(rec) + "\n")

    def run_hook(self, fmt, event, payload, **env):
        with mock.patch.dict(os.environ, env):
            return json.loads(hook.run(fmt, event, json.dumps(payload)))


class PostEdit(Base):
    def setUp(self):
        Base.setUp(self)
        self.doc = self.write("doc.md", TDK_ERR)

    def test_claude(self):
        out = self.run_hook("claude", "post-edit", {
            "hook_event_name": "PostToolUse", "cwd": self.tmp, "tool_name": "Write",
            "tool_input": {"file_path": self.doc, "content": TDK_ERR}})
        spec = out["hookSpecificOutput"]
        self.assertEqual(spec["hookEventName"], "PostToolUse")
        self.assertIn("BK-01", spec["additionalContext"])
        self.assertIn("yontu, doc.md:", spec["additionalContext"])
        self.assertEqual(set(out), {"hookSpecificOutput"})

    def test_codex_apply_patch(self):
        patch = "*** Begin Patch\n*** Update File: doc.md\n@@\n-eski\n+yeni\n*** End Patch\n"
        for tool_input in ({"command": patch}, patch, {"input": patch}):
            out = self.run_hook("codex", "post-edit", {
                "hook_event_name": "PostToolUse", "cwd": self.tmp, "tool_name": "apply_patch",
                "tool_input": tool_input, "tool_response": "Success"})
            self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "PostToolUse")
            self.assertIn("BK-01", out["hookSpecificOutput"]["additionalContext"])

    def test_cursor(self):
        out = self.run_hook("cursor", "post-edit", {
            "hook_event_name": "postToolUse", "workspace_roots": [self.tmp], "tool_name": "Write",
            "tool_input": {"file_path": "doc.md"}})
        self.assertIn("BK-01", out["additional_context"])
        out = self.run_hook("cursor", "post-edit", {
            "hook_event_name": "afterFileEdit", "file_path": self.doc,
            "edits": [{"old_string": "a", "new_string": "b"}]})
        self.assertEqual(out, {})

    def test_copilot_tool_args_string(self):
        out = self.run_hook("copilot", "post-edit", {
            "cwd": self.tmp, "toolName": "edit", "toolArgs": json.dumps({"path": self.doc}),
            "toolResult": {"resultType": "success"}})
        self.assertIn("BK-01", out["additionalContext"])

    def test_read_only_tools_skipped(self):
        for payload in ({"toolName": "view", "toolArgs": json.dumps({"path": self.doc})},
                        {"tool_name": "Read", "tool_input": {"file_path": self.doc}},
                        {"tool_name": "read_many_files", "tool_input": {"paths": [self.doc]}},
                        {"toolCall": {"name": "view_file", "args": {"AbsolutePath": self.doc}}}):
            payload["cwd"] = self.tmp
            self.assertEqual(self.run_hook("copilot", "post-edit", payload), {}, payload)
        for name in ("Edit", "apply_patch", "write_file", "replace", "search_replace", "create"):
            self.assertFalse(hook.read_only_tool({"tool_name": name}), name)

    def test_gemini(self):
        out = self.run_hook("gemini", "post-edit", {
            "hook_event_name": "AfterTool", "cwd": self.tmp, "tool_name": "write_file",
            "tool_input": {"file_path": self.doc, "content": TDK_ERR}})
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "AfterTool")
        self.assertIn("BK-01", out["hookSpecificOutput"]["additionalContext"])

    def test_no_feedback_channel(self):
        ag = {"conversationId": "c1", "workspacePaths": [self.tmp],
              "toolCall": {"name": "write_to_file", "args": {"TargetFile": self.doc}}}
        self.assertEqual(self.run_hook("antigravity", "post-edit", ag), {})
        hermes = {"cwd": self.tmp, "tool_name": "write_file", "args": {"path": self.doc}}
        self.assertEqual(self.run_hook("hermes", "post-edit", hermes), {})

    def test_skipped_files(self):
        cases = {"kod.py": TDK_ERR, "en.md": ENGLISH, "temiz.md": CLEAN, "bilgi.md": INFO_ONLY}
        for name, text in cases.items():
            path = self.write(name, text)
            out = self.run_hook("claude", "post-edit", {
                "cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": path}})
            self.assertEqual(out, {}, name)
        out = self.run_hook("claude", "post-edit", {
            "cwd": self.tmp, "tool_name": "Write",
            "tool_input": {"file_path": os.path.join(self.tmp, "yok.md")}})
        self.assertEqual(out, {})

    def test_level_widens(self):
        path = self.write("bilgi.md", INFO_ONLY)
        payload = {"cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": path}}
        out = self.run_hook("claude", "post-edit", payload, YONTU_HOOK_LEVEL="info")
        self.assertIn("AI-E", out["hookSpecificOutput"]["additionalContext"])

    def test_kill_switches(self):
        payload = {"cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": self.doc}}
        self.assertEqual(self.run_hook("claude", "post-edit", payload, YONTU_DISABLE="1"), {})
        sub = os.path.join(self.tmp, "a", "b")
        os.makedirs(sub)
        nested = os.path.join(sub, "doc.md")
        shutil.copy(self.doc, nested)
        self.write(".yontu-ignore", "")
        payload["tool_input"]["file_path"] = nested
        self.assertEqual(self.run_hook("claude", "post-edit", payload), {})

    def test_message_is_bounded(self):
        path = self.write("uzun.md", "\n\n".join([TDK_ERR] * 60))
        out = self.run_hook("claude", "post-edit", {
            "cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": path}})
        msg = out["hookSpecificOutput"]["additionalContext"]
        self.assertLessEqual(len(msg), hook.MAX_CONTEXT)
        self.assertIn("Gösterilmeyen", msg)


class Stop(Base):
    def claude(self, text=CHATBOT, **extra):
        payload = {"hook_event_name": "Stop", "cwd": self.tmp, "stop_hook_active": False,
                   "transcript_path": self.transcript(text)}
        payload.update(extra)
        return payload

    def test_claude_modes(self):
        out = self.run_hook("claude", "stop", self.claude())
        self.assertEqual(set(out), {"systemMessage"})
        self.assertIn("AI-E6", out["systemMessage"])
        out = self.run_hook("claude", "stop", self.claude(), YONTU_STOP_MODE="context")
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "Stop")
        self.assertIn("AI-E6", out["hookSpecificOutput"]["additionalContext"])
        self.assertNotIn("\n", out["systemMessage"])
        out = self.run_hook("claude", "stop", self.claude(), YONTU_STOP_MODE="block")
        self.assertEqual(out["decision"], "block")
        self.assertIn("AI-E6", out["reason"])

    def test_already_continuing(self):
        for mode in ("context", "block"):
            out = self.run_hook("claude", "stop", self.claude(stop_hook_active=True),
                                YONTU_STOP_MODE=mode)
            self.assertEqual(set(out), {"systemMessage"}, mode)

    def test_info_findings_never_block(self):
        out = self.run_hook("claude", "stop", self.claude(INFO_ONLY), YONTU_STOP_MODE="block",
                            YONTU_HOOK_LEVEL="info")
        self.assertEqual(set(out), {"systemMessage"})
        self.assertEqual(self.run_hook("claude", "stop", self.claude(INFO_ONLY)), {})

    def test_quiet_cases(self):
        for text in (CLEAN, ENGLISH):
            self.assertEqual(self.run_hook("claude", "stop", self.claude(text)), {})
        self.assertEqual(self.run_hook("claude", "stop", {"cwd": self.tmp}), {})
        self.assertEqual(self.run_hook("claude", "stop",
                                       {"cwd": self.tmp, "transcript_path": "/yok/t.jsonl"}), {})
        self.assertEqual(self.run_hook("claude", "stop", self.claude(), YONTU_DISABLE="1"), {})
        self.write(".yontu-ignore", "")
        self.assertEqual(self.run_hook("claude", "stop", self.claude()), {})

    def test_codex(self):
        payload = {"hook_event_name": "Stop", "cwd": self.tmp, "stop_hook_active": False,
                   "last_assistant_message": TDK_ERR, "turn_id": "t1"}
        for mode in ("advisory", "context", "block"):
            out = self.run_hook("codex", "stop", payload, YONTU_STOP_MODE=mode)
            self.assertTrue(set(out) <= CODEX_STOP_KEYS, out)
        self.assertEqual(out["decision"], "block")
        self.assertIn("BK-01", out["reason"])
        payload["stop_hook_active"] = True
        out = self.run_hook("codex", "stop", payload, YONTU_STOP_MODE="block")
        self.assertEqual(set(out), {"systemMessage"})

    def test_gemini(self):
        payload = {"hook_event_name": "AfterAgent", "cwd": self.tmp, "prompt": "soru",
                   "prompt_response": CHATBOT, "stop_hook_active": False}
        self.assertEqual(set(self.run_hook("gemini", "stop", payload)), {"systemMessage"})
        out = self.run_hook("gemini", "stop", payload, YONTU_STOP_MODE="block")
        self.assertEqual(out["decision"], "deny")
        payload["stop_hook_active"] = True
        out = self.run_hook("gemini", "stop", payload, YONTU_STOP_MODE="block")
        self.assertNotIn("decision", out)

    def test_cursor(self):
        payload = {"hook_event_name": "stop", "status": "completed", "loop_count": 0,
                   "workspace_roots": [self.tmp], "transcript_path": self.transcript(CHATBOT)}
        self.assertEqual(self.run_hook("cursor", "stop", payload), {})
        out = self.run_hook("cursor", "stop", payload, YONTU_STOP_MODE="block")
        self.assertIn("AI-E6", out["followup_message"])
        payload["loop_count"] = 1
        self.assertEqual(self.run_hook("cursor", "stop", payload, YONTU_STOP_MODE="block"), {})

    def test_copilot(self):
        payload = {"cwd": self.tmp, "transcriptPath": self.transcript(CHATBOT, "plain")}
        self.assertEqual(self.run_hook("copilot", "stop", payload), {})
        out = self.run_hook("copilot", "stop", payload, YONTU_STOP_MODE="block")
        self.assertEqual(out["decision"], "block")

    def test_antigravity_always_decides(self):
        payload = {"conversationId": "c1", "workspacePaths": [self.tmp], "executionNum": 1,
                   "terminationReason": "NO_TOOL_CALL", "fullyIdle": True,
                   "transcriptPath": self.transcript(CHATBOT, "plain")}
        out = self.run_hook("antigravity", "stop", payload, YONTU_STOP_MODE="block")
        self.assertEqual(out["decision"], "continue")
        self.assertIn("AI-E6", out["reason"])
        self.assertEqual(self.run_hook("antigravity", "stop", payload), {"decision": "allow"})
        payload["terminationReason"] = "USER_CANCELED"
        self.assertEqual(self.run_hook("antigravity", "stop", payload, YONTU_STOP_MODE="block"),
                         {"decision": "allow"})
        payload["transcriptPath"] = self.transcript(CLEAN, "plain")
        payload["terminationReason"] = "NO_TOOL_CALL"
        self.assertEqual(self.run_hook("antigravity", "stop", payload, YONTU_STOP_MODE="block"),
                         {"decision": "allow"})
        self.assertEqual(self.run_hook("antigravity", "stop", payload, YONTU_DISABLE="1"),
                         {"decision": "allow"})

    def test_hermes_logs_only(self):
        payload = {"cwd": self.tmp, "last_assistant_message": CHATBOT}
        self.assertEqual(self.run_hook("hermes", "stop", payload, YONTU_STOP_MODE="block"), {})


class FailOpen(Base):
    def test_garbage(self):
        for data in ("", "not json", "[1, 2]", "null", "\xff\xfe", '{"cwd": 5}',
                     '{"tool_input": {"file_path": 7}, "transcript_path": ["x"]}'):
            for fmt in hook.FORMATS:
                for event in hook.EVENTS:
                    out = json.loads(hook.run(fmt, event, data))
                    want = {"decision": "allow"} if (fmt, event) == ("antigravity", "stop") else {}
                    self.assertEqual(out, want, (fmt, event, data))

    def test_internal_error(self):
        with mock.patch.object(hook, "_handle", side_effect=RuntimeError("x")):
            self.assertEqual(hook.run("claude", "stop", "{}"), "{}")
            self.assertEqual(json.loads(hook.run("antigravity", "stop", "{}")),
                             {"decision": "allow"})

    def test_broken_config_ignored(self):
        doc = self.write("doc.md", TDK_ERR)
        self.write(".yontu.json", "{bozuk")
        out = self.run_hook("claude", "post-edit", {
            "cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": doc}})
        self.assertIn("BK-01", out["hookSpecificOutput"]["additionalContext"])


class Shipped(Base):
    """The exact commands in the shipped hook files, run as the agent would."""

    def proc(self, argv, payload, env=None, shell=False):
        p = subprocess.run(argv, input=json.dumps(payload).encode("utf-8"), shell=shell,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.tmp,
                           env=env or clean_env(), timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        lines = p.stdout.decode("utf-8").splitlines()
        self.assertEqual(len(lines), 1, lines)
        return json.loads(lines[0])

    def test_plugin_hooks_json(self):
        with io.open(os.path.join(ROOT, "hooks", "hooks.json"), encoding="utf-8") as fh:
            spec = json.load(fh)
        doc = self.write("doc.md", TDK_ERR)
        payloads = {"PostToolUse": {"cwd": self.tmp, "tool_name": "Write",
                                    "tool_input": {"file_path": doc}},
                    "Stop": {"cwd": self.tmp, "stop_hook_active": False,
                             "transcript_path": self.transcript(CHATBOT)}}
        keys = {"PostToolUse": "hookSpecificOutput", "Stop": "systemMessage"}
        for event, groups in spec["hooks"].items():
            for h in groups[0]["hooks"]:
                self.assertEqual(h["command"], "python3")
                argv = [sys.executable] + [a.replace("${CLAUDE_PLUGIN_ROOT}", ROOT)
                                           for a in h["args"]]
                out = self.proc(argv, payloads[event])
                self.assertIn(keys[event], out)

    @unittest.skipIf(os.name == "nt", "POSIX shell commands")
    def test_integration_hook_commands(self):
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        shim = os.path.join(bindir, "yontu")
        with io.open(shim, "w", encoding="utf-8") as fh:
            fh.write('#!/bin/sh\nexec "%s" "%s" "$@"\n' % (sys.executable, PKG))
        os.chmod(shim, 0o755)
        env = clean_env(PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
        doc = self.write("doc.md", TDK_ERR)
        edit = {"cwd": self.tmp, "tool_name": "Write", "tool_input": {"file_path": doc},
                "toolName": "edit", "toolArgs": json.dumps({"path": doc})}
        stop = {"cwd": self.tmp, "last_assistant_message": CHATBOT, "prompt_response": CHATBOT,
                "workspacePaths": [self.tmp], "terminationReason": "NO_TOOL_CALL"}
        commands = []
        for rel in ("codex/hooks.json", "cursor/hooks.json", "gemini-cli/hooks.settings.json",
                    "copilot/hooks.json", "antigravity/hooks.json"):
            with io.open(os.path.join(ROOT, "integrations", rel), encoding="utf-8") as fh:
                commands += list(_commands(json.load(fh)))
        self.assertGreaterEqual(len(commands), 7)
        for cmd in commands:
            out = self.proc(cmd, stop if "--event stop" in cmd else edit, env=env, shell=True)
            self.assertNotEqual(out, {}, cmd)


def _commands(obj):
    """Every shell command string in a hook config, whatever its nesting."""
    if isinstance(obj, dict):
        for key in ("command", "bash"):
            if isinstance(obj.get(key), str) and "yontu hook" in obj[key]:
                yield obj[key]
        for value in obj.values():
            for cmd in _commands(value):
                yield cmd
    elif isinstance(obj, list):
        for value in obj:
            for cmd in _commands(value):
                yield cmd


if __name__ == "__main__":
    unittest.main()
