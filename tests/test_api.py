"""Public API of the package."""
import unittest

from ortak import yontu


class TestApi(unittest.TestCase):
    def test_exports(self):
        self.assertRegex(yontu.__version__, r"^\d+\.\d+\.\d+$")
        for name in ("lint", "fix", "compare", "stats", "profiles"):
            self.assertTrue(callable(getattr(yontu, name)), name)

    def test_lint(self):
        res = yontu.lint("Herkez geldi.")
        for key in ("register", "tur", "detected_by", "words", "sentences", "findings"):
            self.assertIn(key, res)
        f = res["findings"][0]
        self.assertEqual((f["id"], f["level"], f["line"], f["col"]), ("YZ-03", "error", 1, 1))
        self.assertEqual(yontu.lint("Herkez geldi.", config={"rules": {"YZ-03": "off"}})["findings"], [])

    def test_lint_register(self):
        self.assertEqual(yontu.lint("Metin.", register="akademik")["register"], "akademik")
        with self.assertRaises(ValueError):
            yontu.lint("Metin.", register="yok")

    def test_fix(self):
        self.assertEqual(yontu.fix("Herkez geldi."), "Herkes geldi.")
        self.assertEqual(yontu.fix(""), "")

    def test_compare(self):
        res = yontu.compare("Rapor hazır.", "Rapor 3 günde hazır.")
        self.assertEqual(res["errors"], 1)
        self.assertEqual(res["findings"][0]["id"], "SD-01")

    def test_stats(self):
        res = yontu.stats("Bu bir deneme. İkinci cümle biraz daha uzun olsun.")
        self.assertEqual(res["sentences"], 2)
        self.assertGreater(res["words"], 0)

    def test_profiles(self):
        profs = yontu.profiles()
        self.assertEqual(len(profs), 28)
        for data in profs.values():
            self.assertIn("register", data)

    def test_empty_text(self):
        res = yontu.lint("")
        self.assertEqual(res["findings"], [])
        self.assertEqual(res["register"], "notr")


if __name__ == "__main__":
    unittest.main()
