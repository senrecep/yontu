"""Command line: both entry styles, exit codes, formats and config."""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from ortak import PKG, SCRIPTS, engine, profiller, yontu

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
ENV.pop("PYTHONPATH", None)
EMPTY = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(EMPTY, ignore_errors=True)


def run(args, stdin=None, cwd=None, style="dir"):
    if cwd is None:
        cwd = EMPTY
    if style == "dir":
        cmd = [sys.executable, PKG] + list(args)
        env = ENV
    else:
        cmd = [sys.executable, "-m", "yontu"] + list(args)
        env = dict(ENV, PYTHONPATH=SCRIPTS)
    p = subprocess.run(cmd, input=(stdin or "").encode("utf-8"), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, cwd=cwd, env=env)
    return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, name, text):
        path = os.path.join(self.tmp, name)
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path


class TestEntry(Base):
    def test_both_styles(self):
        good = self.write("iyi.md", "Bu rapor yarın gönderilecek.\n")
        bad = self.write("kotu.md", "Herkez geldi.\n")
        for style in ("dir", "module"):
            self.assertEqual(run(["lint", good], cwd=self.tmp, style=style)[0], 0, style)
            code, out, _ = run(["lint", bad], cwd=self.tmp, style=style)
            self.assertEqual(code, 1, style)
            self.assertIn("YZ-03", out)
            self.assertIn("Herkes", out)

    def test_version(self):
        code, out, _ = run(["--version"])
        self.assertEqual(code, 0)
        self.assertIn(yontu.__version__, out)


class TestLint(Base):
    def test_json_and_stdin(self):
        code, out, _ = run(["lint", "-", "--format", "json"], stdin="Herkez geldi.")
        self.assertEqual(code, 1)
        data = json.loads(out)
        self.assertEqual(data["file"], "<stdin>")
        self.assertEqual(data["counts"]["error"], 1)
        self.assertEqual(data["findings"][0]["id"], "YZ-03")

    def test_layer_and_min_level(self):
        text = "Herkez geldi. Bu iş hızlı bir şekilde bitti."
        out = json.loads(run(["lint", "-", "--format", "json", "--layer", "yogunluk"], stdin=text)[1])
        self.assertEqual({f["layer"] for f in out["findings"]}, {"yogunluk"})
        code, out, _ = run(["lint", "-", "--format", "json", "--layer", "yogunluk"], stdin=text)
        self.assertEqual(code, 0)
        out = json.loads(run(["lint", "-", "--format", "json", "--min-level", "error"], stdin=text)[1])
        self.assertEqual([f["id"] for f in out["findings"]], ["YZ-03"])

    def test_fix_stdout_and_write(self):
        code, out, _ = run(["lint", "-", "--fix"], stdin="Herkez yanlız geldi.")
        self.assertEqual((code, out), (0, "Herkes yalnız geldi."))
        path = self.write("metin.md", "Herkez geldi.\n")
        code, _, err = run(["lint", path, "--fix", "--write"])
        self.assertEqual(code, 0, err)
        with io.open(path, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "Herkes geldi.\n")

    def test_write_needs_fix(self):
        path = self.write("metin.md", "Herkez geldi.\n")
        self.assertEqual(run(["lint", path, "--write"])[0], 2)

    def test_config_file(self):
        self.write(".yontu.json", json.dumps({"rules": {"YZ-03": "off"}}))
        path = self.write("metin.md", "Herkez geldi.\n")
        self.assertEqual(run(["lint", path])[0], 0)
        cfg = self.write("ayar.json", json.dumps({"rules": {"YZ-03": "warning"}}))
        self.assertEqual(run(["lint", "-", "--config", cfg], stdin="Herkez geldi.")[0], 0)

    def test_bad_config(self):
        cfg = self.write("bozuk.json", "{bozuk")
        self.assertEqual(run(["lint", "-", "--config", cfg], stdin="Metin.")[0], 2)
        cfg = self.write("yanlis.json", json.dumps({"rules": {"YZ-3": "off"}}))
        self.assertEqual(run(["lint", "-", "--config", cfg], stdin="Metin.")[0], 2)
        cfg = self.write("duzey.json", json.dumps({"rules": {"YZ-03": "of"}}))
        self.assertEqual(run(["lint", "-", "--config", cfg], stdin="Metin.")[0], 2)
        cfg = self.write("aile.json", json.dumps({"rules": {"layer:yogunluk": "off", "family:yazim": "warning"}}))
        self.assertEqual(run(["lint", "-", "--config", cfg], stdin="Metin.")[0], 0)

    def test_directive(self):
        text = "<!-- yontu-disable-next-line YZ-03 -->\nHerkez geldi.\n"
        self.assertEqual(run(["lint", "-"], stdin=text)[0], 0)

    def test_usage_errors(self):
        self.assertEqual(run([])[0], 2)
        self.assertEqual(run(["lint", os.path.join(self.tmp, "yok.md")])[0], 2)
        self.assertEqual(run(["lint", "-", "--layer", "yok"], stdin="Metin.")[0], 2)
        self.assertEqual(run(["lint", "-", "--register", "yok"], stdin="Metin.")[0], 2)
        self.assertEqual(run(["lint", "-", "--enable", "YOK-99"], stdin="Metin.")[0], 2)
        self.assertEqual(run(["explain", "YOK-99"])[0], 2)
        self.assertEqual(run(["profiles", "yok"])[0], 2)
        self.assertEqual(run(["bilinmeyen"])[0], 2)


class TestOther(Base):
    def test_compare(self):
        old = self.write("eski.md", "Rapor hazırlandı.")
        new = self.write("yeni.md", "Rapor Ahmet tarafından hazırlandı.")
        same = self.write("ayni.md", "Rapor hazırlandı.")
        code, out, _ = run(["compare", old, new])
        self.assertEqual(code, 1)
        self.assertIn("SD-05", out)
        self.assertEqual(run(["compare", old, same])[0], 0)
        data = json.loads(run(["compare", old, new, "--format", "json"])[1])
        self.assertEqual(data["errors"], 1)

    def test_stats(self):
        path = self.write("metin.md", "Bu bir deneme metnidir. İkinci cümle biraz daha uzun olsun.\n")
        code, out, _ = run(["stats", path, "--format", "json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["sentences"], 2)
        self.assertEqual(run(["stats", path])[0], 0)

    def test_rules(self):
        code, out, _ = run(["rules", "--format", "json"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(len(data), len(engine.all_rules()))
        for layer in engine.LAYERS:
            sub = json.loads(run(["rules", "--layer", layer, "--format", "json"])[1])
            self.assertEqual({d["layer"] for d in sub}, {layer})
        self.assertIn("%d kural" % len(data), run(["rules"])[1])

    def test_explain(self):
        code, out, _ = run(["explain", "YS-A57"])
        self.assertEqual(code, 0)
        self.assertIn("yogunluk", out)
        self.assertEqual(json.loads(run(["explain", "ys-a57", "--format", "json"])[1])["id"], "YS-A57")

    def test_profiles(self):
        code, out, _ = run(["profiles"])
        self.assertEqual(code, 0)
        self.assertIn("%d tür, %d register" % (len(profiller.profiles()), len(profiller.registers())), out)
        data = json.loads(run(["profiles", "--format", "json"])[1])
        self.assertEqual(len(data["profiles"]), 28)
        self.assertEqual(len(data["registers"]), 17)
        self.assertEqual(run(["profiles", "commit"])[0], 0)
        self.assertEqual(run(["profiles", data["profiles"][0], "--format", "json"])[0], 0)


if __name__ == "__main__":
    unittest.main()
