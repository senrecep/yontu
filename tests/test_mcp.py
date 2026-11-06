"""MCP server: a scripted stdio session against the real process, plus protocol edge cases."""
import io
import json
import os
import subprocess
import sys
import unittest
from unittest import mock

from ortak import PKG, ROOT
from yontu import mcp

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
ENV.pop("PYTHONPATH", None)
ENV.pop("YONTU_MCP_TOOLS", None)
TOOLS = {"lint_text", "compare_texts", "get_style_guide"}
TOOLS_FULL = TOOLS | {"fix_text", "text_stats", "explain_rule", "list_profiles", "get_profile"}
TEXT = "Herkes birşey söyledi ama kimse dinlemedi, bu yüzden toplantı uzadı."


def session(messages, argv=None, env=None):
    """Send raw lines (dicts are JSON-encoded) to a fresh server, return {id: response}."""
    lines = [m if isinstance(m, str) else json.dumps(m, ensure_ascii=False) for m in messages]
    p = subprocess.run(argv or [sys.executable, PKG, "mcp"],
                       input=("\n".join(lines) + "\n").encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env or ENV, cwd=ROOT,
                       timeout=60)
    assert p.returncode == 0, p.stderr
    out = {}
    for line in p.stdout.decode("utf-8").splitlines():
        resp = json.loads(line)
        if isinstance(resp, list):
            for r in resp:
                out[r["id"]] = r
        else:
            out[resp["id"]] = resp
    return out


def req(mid, method, params=None):
    msg = {"jsonrpc": "2.0", "id": mid, "method": method}
    if params is not None:
        msg["params"] = params
    return msg


def init(version="2025-11-25"):
    return [req(0, "initialize", {"protocolVersion": version, "capabilities": {},
                                  "clientInfo": {"name": "test", "version": "1"}}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"}]


def call(mid, name, args=None):
    params = {"name": name}
    if args is not None:
        params["arguments"] = args
    return req(mid, "tools/call", params)


class Session(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = session(init() + [
            req(1, "ping"),
            req(2, "tools/list"),
            req(3, "prompts/list"),
            call(10, "lint_text", {"text": TEXT, "register": "sohbet"}),
            call(11, "fix_text", {"text": TEXT}),
            call(12, "compare_texts", {"old": "Toplantı 3 Mart'ta.", "new": "Toplantı 5 Mart'ta."}),
            call(13, "text_stats", {"text": TEXT}),
            call(14, "explain_rule", {"id": "BK-01"}),
            call(15, "list_profiles", {}),
            call(16, "get_profile", {"tur": "blog"}),
            call(17, "get_style_guide", {"topic": "skill"}),
            call(18, "lint_text", {}),
            call(19, "explain_rule", {"id": "YOK-99"}),
            call(20, "get_profile", {"tur": "yok"}),
            call(21, "get_style_guide", {"topic": "yok"}),
            call(22, "lint_text", {"text": 5}),
            call(23, "nope", {}),
            call(25, "get_style_guide", {"topic": "linkedin"}),
            call(26, "get_style_guide", {"topic": "yogunlastirma"}),
            call(27, "get_style_guide", {"topic": "baglaclar", "section": "ki"}),
            call(28, "get_style_guide", {"topic": "baglaclar", "section": "yok-boyle"}),
            call(29, "lint_text", {"text": TEXT, "register": "sohbet", "detail": True}),
            req(24, "tools/call", {"name": "lint_text", "arguments": "metin"}),
            req(30, "prompts/get", {"name": "turkcelestir",
                                    "arguments": {"text": "Hello world.", "tur": "blog"}}),
            req(31, "prompts/get", {"name": "yogunlastir", "arguments": {"text": TEXT}}),
            req(32, "prompts/get", {"name": "yogunlastir", "arguments": {}}),
            req(33, "prompts/get", {"name": "yok", "arguments": {"text": "x"}}),
            req(34, "prompts/get", {"name": "turkcelestir",
                                    "arguments": {"text": "x", "tur": "yok"}}),
            req(40, "resources/list"),
            "{bozuk",
            [req(50, "ping"), {"jsonrpc": "2.0", "method": "notifications/cancelled"}],
            req(51, "ping"),
        ])

    def result(self, mid):
        self.assertIn("result", self.r[mid], self.r[mid])
        return self.r[mid]["result"]

    def error(self, mid):
        self.assertIn("error", self.r[mid], self.r[mid])
        return self.r[mid]["error"]["code"]

    def data(self, mid):
        res = self.result(mid)
        self.assertFalse(res["isError"])
        self.assertEqual(json.loads(res["content"][0]["text"]), res["structuredContent"])
        return res["structuredContent"]

    def test_initialize(self):
        res = self.result(0)
        self.assertEqual(res["protocolVersion"], "2025-11-25")
        self.assertEqual(res["serverInfo"]["name"], "yontu")
        self.assertIn("tools", res["capabilities"])
        self.assertIn("prompts", res["capabilities"])
        self.assertTrue(res["instructions"])

    def test_ping(self):
        self.assertEqual(self.result(1), {})
        self.assertEqual(self.result(51), {})

    def test_tools_list(self):
        tools = self.result(2)["tools"]
        self.assertEqual({t["name"] for t in tools}, TOOLS)
        self.assertLess(len(json.dumps(tools, ensure_ascii=False)), 3500)
        for t in tools:
            self.assertEqual(t["inputSchema"]["type"], "object")
            self.assertTrue(t["description"])

    def test_prompts_list(self):
        names = {p["name"] for p in self.result(3)["prompts"]}
        self.assertEqual(names, {"turkcelestir", "yogunlastir"})

    def test_tools(self):
        self.assertIn("BK-01", [f["id"] for f in self.data(10)["findings"]])
        fixed = self.data(11)
        self.assertTrue(fixed["changed"])
        self.assertIn("bir şey", fixed["text"])
        self.assertTrue(self.data(12))
        self.assertTrue(self.data(13))
        self.assertEqual(self.data(14)["id"], "BK-01")
        self.assertTrue(self.data(15)["profiles"])
        self.assertTrue(self.data(16))
        guide = self.result(17)
        self.assertFalse(guide["isError"])
        self.assertIn("# yontu", guide["content"][0]["text"])
        self.assertNotIn("structuredContent", guide)

    def test_slim_and_detail(self):
        slim = self.data(10)["findings"][0]
        self.assertNotIn("start", slim)
        self.assertNotIn("source", slim)
        self.assertTrue(all(v is not None for v in slim.values()))
        full = self.data(29)["findings"][0]
        self.assertIn("start", full)

    def test_style_guide_sections(self):
        text = lambda mid: self.result(mid)["content"][0]["text"]
        self.assertTrue(text(25).startswith("# P19 LinkedIn"))
        self.assertIn("İkna gücünü koru", text(25))
        outline = text(26)
        self.assertIn("call again with section", outline)
        self.assertLess(len(outline), 2000)
        self.assertTrue(text(27).startswith('## "ki" yazımı'))
        self.assertNotIn("## ", text(27)[3:])
        self.assertTrue(self.result(28)["isError"])

    def test_tool_errors(self):
        for mid in (18, 19, 20, 21, 22):
            res = self.result(mid)
            self.assertTrue(res["isError"], mid)
            self.assertNotIn("structuredContent", res)
        self.assertEqual(self.error(23), -32602)
        self.assertEqual(self.error(24), -32602)

    def test_prompts(self):
        msg = self.result(30)["messages"][0]
        self.assertEqual(msg["role"], "user")
        self.assertIn("Hello world.", msg["content"]["text"])
        self.assertIn("Target genre:", msg["content"]["text"])
        self.assertIn(TEXT, self.result(31)["messages"][0]["content"]["text"])
        for mid in (32, 33, 34):
            self.assertEqual(self.error(mid), -32602, mid)

    def test_protocol_errors(self):
        self.assertEqual(self.error(40), -32601)
        self.assertEqual(self.r[None]["error"]["code"], -32700)
        self.assertEqual(self.result(50), {})


class Versions(unittest.TestCase):
    def test_old_protocol_has_no_structured_content(self):
        r = session(init("2025-03-26") + [call(1, "list_profiles", {})])
        self.assertEqual(r[0]["result"]["protocolVersion"], "2025-03-26")
        self.assertNotIn("structuredContent", r[1]["result"])
        json.loads(r[1]["result"]["content"][0]["text"])

    def test_unknown_version_gets_latest(self):
        r = session(init("1999-01-01"))
        self.assertEqual(r[0]["result"]["protocolVersion"], mcp.PROTOCOLS[0])

    def test_plugin_mcp_json(self):
        with io.open(os.path.join(ROOT, ".mcp.json"), encoding="utf-8") as fh:
            spec = json.load(fh)["mcpServers"]["yontu"]
        self.assertEqual(spec["command"], "python3")
        argv = [sys.executable] + [a.replace("${CLAUDE_PLUGIN_ROOT}", ROOT) for a in spec["args"]]
        r = session(init() + [req(1, "tools/list")], argv=argv)
        self.assertEqual({t["name"] for t in r[1]["result"]["tools"]}, TOOLS)

    def test_full_surface(self):
        env = dict(ENV, YONTU_MCP_TOOLS="full")
        r = session(init() + [req(1, "tools/list")], env=env)
        self.assertEqual({t["name"] for t in r[1]["result"]["tools"]}, TOOLS_FULL)

    def test_hidden_tools_still_callable(self):
        r = session(init() + [call(1, "text_stats", {"text": TEXT}),
                              call(2, "get_profile", {"tur": "blog"})])
        self.assertFalse(r[1]["result"]["isError"])
        self.assertFalse(r[2]["result"]["isError"])


class InProcess(unittest.TestCase):
    def test_notifications_and_responses_get_no_reply(self):
        s = mcp.Server()
        self.assertIsNone(s.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        self.assertIsNone(s.handle({"jsonrpc": "2.0", "id": 9, "result": {}}))
        self.assertEqual(s.handle([])["error"]["code"], -32600)
        self.assertEqual(s.handle(5)["error"]["code"], -32600)
        self.assertEqual(s.handle({"jsonrpc": "2.0", "id": 1, "method": 3})["error"]["code"],
                         -32600)

    def test_request_without_method_is_invalid(self):
        s = mcp.Server()
        out = s.handle({"jsonrpc": "2.0", "id": 1})
        self.assertEqual((out["id"], out["error"]["code"]), (1, -32600))
        self.assertEqual(s.handle({"id": 2, "method": "ping"})["error"]["code"], -32600)
        self.assertIsNone(s.handle({"jsonrpc": "2.0"}))

    def test_style_guide_names(self):
        for topic in ("blog", "turler/blog", "turler/blog.md"):
            self.assertTrue(mcp.t_guide({"topic": topic}).startswith("# P9 Blog"), topic)
        text = mcp.t_guide({"topic": "akademik"})
        self.assertTrue(text.startswith("Topic 'akademik' maps to the tür 'akademik-giris'."), text[:80])
        self.assertIn("# P2 Akademik", text)
        with self.assertRaises(mcp.ToolError) as cm:
            mcp.t_guide({"topic": "yok"})
        self.assertIn("ai-oruntuleri", str(cm.exception))
        self.assertNotIn("turler/", str(cm.exception))

    def test_internal_error(self):
        s = mcp.Server()
        with mock.patch.object(s, "dispatch", side_effect=RuntimeError("x")), \
                mock.patch.object(sys, "stderr", io.StringIO()):
            out = s.handle({"jsonrpc": "2.0", "id": 1, "method": "ping"})
        self.assertEqual(out["error"]["code"], -32603)


if __name__ == "__main__":
    unittest.main()
