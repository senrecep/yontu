"""scripts/check-versions.py: every version location agrees, and a mismatch exits 1."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ortak import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "check-versions.py")


def run(*args):
    return subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True, encoding="utf-8")


class TestSurum(unittest.TestCase):
    def test_repository_is_consistent(self):
        r = run()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_tag_mismatch_fails(self):
        r = run("--tag", "v99.0.0")
        self.assertEqual(r.returncode, 1)
        self.assertIn("differs", r.stderr)

    def test_drift_is_reported(self):
        tmp = tempfile.mkdtemp()
        try:
            for rel in ("scripts", ".claude-plugin", "skills", "pyproject.toml", "server.json", "gemini-extension.json"):
                src = os.path.join(ROOT, rel)
                dst = os.path.join(tmp, rel)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("references", "__pycache__", "data"))
                else:
                    shutil.copy(src, dst)
            path = os.path.join(tmp, "server.json")
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            data["packages"][0]["version"] = "0.0.1"
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            r = subprocess.run([sys.executable, os.path.join(tmp, "scripts", "check-versions.py")],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(r.returncode, 1)
            self.assertIn("server.json packages[0].version", r.stderr)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
