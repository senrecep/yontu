"""Shipped integration files: valid JSON, consistent versions, install.sh dry run."""
import glob
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest

from ortak import ROOT, yontu

INSTALL = os.path.join(ROOT, "scripts", "install.sh")


def load(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def shipped_json():
    files = glob.glob(os.path.join(ROOT, "integrations", "*", "*.json"))
    files += [os.path.join(ROOT, p) for p in (
        "gemini-extension.json", "server.json", ".mcp.json", os.path.join("hooks", "hooks.json"),
        os.path.join(".claude-plugin", "plugin.json"),
        os.path.join(".claude-plugin", "marketplace.json"))]
    return sorted(files)


class Files(unittest.TestCase):
    def test_json_valid(self):
        files = shipped_json()
        self.assertGreater(len(files), 15)
        for path in files:
            with self.subTest(path=os.path.relpath(path, ROOT)):
                self.assertIsInstance(load(path), dict)

    def test_versions_match(self):
        v = yontu.__version__
        self.assertEqual(load(os.path.join(ROOT, ".claude-plugin", "plugin.json"))["version"], v)
        self.assertEqual(load(os.path.join(ROOT, "gemini-extension.json"))["version"], v)
        server = load(os.path.join(ROOT, "server.json"))
        self.assertEqual(server["version"], v)
        self.assertEqual(server["packages"][0]["version"], v)

    def test_server_json(self):
        server = load(os.path.join(ROOT, "server.json"))
        self.assertLessEqual(len(server["description"]), 100)
        self.assertRegex(server["name"], r"^io\.github\.[^/]+/yontu$")
        pkg = server["packages"][0]
        self.assertEqual((pkg["registryType"], pkg["identifier"]), ("pypi", "yontu"))
        self.assertEqual(pkg["transport"], {"type": "stdio"})
        self.assertEqual([a["value"] for a in pkg["packageArguments"]], ["mcp"])

    def test_mcp_configs_start_the_server(self):
        found = 0
        for path in shipped_json():
            data = load(path)
            for key in ("mcpServers", "servers", "context_servers", "mcp"):
                entry = (data.get(key) or {}).get("yontu")
                if entry:
                    found += 1
                    flat = json.dumps(entry)
                    self.assertIn('"mcp"', flat, path)
                    self.assertIn("yontu", flat, path)
        self.assertGreaterEqual(found, 10)

    def test_no_em_dash(self):
        for path in shipped_json() + glob.glob(os.path.join(ROOT, "integrations", "*", "*.md")):
            with io.open(path, encoding="utf-8") as fh:
                self.assertNotIn("\u2014", fh.read(), path)


@unittest.skipIf(os.name == "nt" or not shutil.which("sh"), "POSIX shell")
class Install(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()
        self.env = dict(os.environ, HOME=self.home)

    def tearDown(self):
        shutil.rmtree(self.home, ignore_errors=True)

    def sh(self, *args, **kw):
        p = subprocess.run([kw.get("shell", "sh"), INSTALL] + list(args), env=self.env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8")

    def test_syntax(self):
        for shell in ("sh", "dash"):
            if shutil.which(shell):
                p = subprocess.run([shell, "-n", INSTALL])
                self.assertEqual(p.returncode, 0, shell)

    def test_dry_run_changes_nothing(self):
        shells = ["sh"] + (["dash"] if shutil.which("dash") else [])
        for shell in shells:
            code, out, _ = self.sh("--all", "--copy", "--force", shell=shell)
            self.assertEqual(code, 0, out)
            self.assertIn("Dry run", out)
            for part in (".claude/skills/yontu", ".agents/skills/yontu", ".cursor/skills/yontu",
                         ".gemini/skills/yontu", ".gemini/config/skills/yontu",
                         ".hermes/skills/yontu"):
                self.assertIn(os.path.join(self.home, part), out)
            self.assertEqual(os.listdir(self.home), [])

    def test_existing_target_is_kept(self):
        dest = os.path.join(self.home, ".claude", "skills", "yontu")
        os.makedirs(dest)
        code, out, _ = self.sh("--claude", "--claude")
        self.assertEqual(code, 1)
        self.assertEqual(out.count("claude:"), 1)
        self.assertIn("--force", out)
        self.assertTrue(os.path.isdir(dest))

    def test_usage_errors(self):
        self.assertEqual(self.sh()[0], 2)
        self.assertEqual(self.sh("--apply")[0], 2)
        self.assertEqual(self.sh("--bogus")[0], 2)
        code, out, _ = self.sh("--help")
        self.assertEqual(code, 0)
        self.assertIn("--antigravity", out)
        self.assertIn("--profile", out)
        self.assertEqual(self.sh("--claude", "--profile")[0], 2)
        self.assertEqual(self.sh("--claude", "--profile", "huge")[0], 2)
        self.assertEqual(self.sh("--claude", "--profile=")[0], 2)

    def test_profiles(self):
        code, out, _ = self.sh("--codex")
        self.assertEqual(code, 0)
        self.assertIn("Profile: lite", out)
        self.assertNotIn("mcp:", out)
        code, out, _ = self.sh("--codex", "--profile", "standard")
        self.assertEqual(code, 0)
        self.assertIn("hook: codex/hooks.json", out)
        self.assertNotIn("mcp:", out)
        code, out, _ = self.sh("--all", "--profile=full")
        self.assertEqual(code, 0)
        self.assertEqual(out.count("  mcp:  "), 6)
        for name in ("codex/config.toml", "cursor/mcp.json", "gemini-cli/settings.json",
                     "antigravity/mcp_config.json", "hermes/config.yaml",
                     "codex/hooks.json", "cursor/hooks.json", "gemini-cli/hooks.settings.json",
                     "antigravity/hooks.json"):
            self.assertIn(name, out)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "integrations", name)), name)
        self.assertEqual(os.listdir(self.home), [])


if __name__ == "__main__":
    unittest.main()
