"""Profiles, registers and register detection."""
import unittest

from ortak import engine, ids, insan, profiller


class TestVeri(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(profiller.profiles()), 28)
        self.assertEqual(len(profiller.registers()), 17)

    def test_links(self):
        regs = profiller.registers()
        for tid, p in profiller.profiles().items():
            self.assertIn(p["register"], regs, tid)
        for slug, r in regs.items():
            dt = r.get("default_tur")
            self.assertTrue(dt is None or dt in profiller.profiles(), slug)

    def test_hukuk_and_edebi_layers(self):
        regs = profiller.registers()
        for slug in ("hukuk", "edebi"):
            self.assertEqual(sorted(regs[slug]["layers_off"]), ["ai-iz", "stil", "yogunluk"])

    def test_guidance_has_no_tdk_errors(self):
        bad = []
        for tid, p in profiller.profiles().items():
            for key, val in (p.get("guidance") or {}).items():
                if key == "ai_hatalari":
                    continue
                for t in (val if isinstance(val, list) else [val]):
                    res = engine.lint(t, register="notr", layers=("tdk",))
                    errs = [(f["id"], f["match"]) for f in res["findings"] if f["level"] == "error"]
                    if errs:
                        bad.append((tid, key, errs))
            for ex in p.get("examples", []):
                res = engine.lint(ex.get("sonra") or "", register="notr", layers=("tdk",))
                errs = [(f["id"], f["match"]) for f in res["findings"] if f["level"] == "error"]
                if errs:
                    bad.append((tid, "sonra", errs))
        self.assertEqual(bad, [])


class TestSecim(unittest.TestCase):
    def test_flags_win(self):
        self.assertEqual(profiller.resolve("haber", None, "Özet", None)[:2], ("haber", "haber"))
        self.assertEqual(profiller.resolve(None, "readme", "", None)[:3], ("teknik", "readme", "flag"))

    def test_unknown(self):
        with self.assertRaises(ValueError):
            profiller.resolve("yok-boyle", None, "", None)
        with self.assertRaises(ValueError):
            profiller.resolve(None, "yok-boyle", "", None)

    def test_filename(self):
        self.assertEqual(profiller.resolve(text="x", filename=".git/COMMIT_EDITMSG")[:2], ("commit", "commit"))
        self.assertEqual(profiller.resolve(text="x", filename="README.md")[:2], ("teknik", "readme"))
        self.assertEqual(profiller.resolve(text="x", filename="CHANGELOG.md")[:2], ("teknik", "changelog"))
        self.assertEqual(profiller.resolve(text="x", filename="locales/tr.json")[0], "ui")

    def test_content(self):
        found = {}
        for name, reg, text in insan(names=True):
            if name == reg:
                found[reg] = profiller.resolve(text=text)[0]
        for reg in ("akademik", "haber", "teknik", "resmi", "is-eposta", "sohbet"):
            self.assertEqual(found[reg], reg)

    def test_commit_content(self):
        self.assertEqual(profiller.resolve(text="fix(api): boş yanıtı yakala\n")[0], "commit")

    def test_empty_is_notr(self):
        self.assertEqual(profiller.resolve(text="")[0], "notr")
        res = engine.lint("")
        self.assertEqual((res["register"], res["findings"]), ("notr", []))

    def test_lint_reports_detection(self):
        res = engine.lint("Kısa bir not.", register="haber")
        self.assertEqual(res["detected_by"], "flag")
        self.assertEqual(ids(res), [])


if __name__ == "__main__":
    unittest.main()
