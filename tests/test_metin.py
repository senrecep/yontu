"""Turkish-aware text helpers."""
import unittest

from ortak import yontu  # noqa: F401
from yontu import textutil as tu


class TestHarf(unittest.TestCase):
    def test_lower_upper(self):
        self.assertEqual(tu.tr_lower("İSTANBUL IŞIK"), "istanbul ışık")
        self.assertEqual(tu.tr_upper("istanbul ılık"), "İSTANBUL ILIK")
        self.assertEqual(tu.tr_capitalize("istanbul"), "İstanbul")

    def test_lower_keeps_length(self):
        for t in ("İİİ", "i̇stanbul", "ÂÎÛ ŞĞÇ", "Iı İi"):
            self.assertEqual(len(tu.tr_lower(t)), len(t), t)

    def test_upper_initial(self):
        self.assertTrue(tu.is_upper_initial("İzmir"))
        self.assertFalse(tu.is_upper_initial("ılık"))


class TestCumle(unittest.TestCase):
    def test_abbreviation_and_time(self):
        t = "Dr. Ali geldi. Saat 17.30'da çıktı! Sonra ne oldu?"
        self.assertEqual(len(tu.split_sentences(t)), 3)

    def test_paragraphs(self):
        self.assertEqual(len(tu.split_paragraphs("a\n\nb\nc\n\n\nd")), 3)

    def test_words(self):
        self.assertEqual(tu.words("Ali'nin 1.500 lirası var."), ["Ali'nin", "1.500", "lirası", "var"])

    def test_syllables_and_vowel(self):
        self.assertEqual(tu.syllables("kelebek"), 3)
        self.assertEqual(tu.last_vowel("kitap"), "a")

    def test_atesman_range(self):
        self.assertGreater(tu.atesman("Ali geldi. Ayşe gitti."), 90)


class TestMaske(unittest.TestCase):
    def test_masks_code_url_mail(self):
        t = "a `kod` b https://x.com/y c ali@x.com d"
        out = tu.apply_mask(t, tu.build_mask(t))
        self.assertEqual(len(out), len(t))
        for s in ("kod", "x.com", "ali@"):
            self.assertNotIn(s, out)
        self.assertIn("a ", out)
        self.assertIn(" d", out)

    def test_frontmatter_and_fence(self):
        t = "---\nbaslik: herşey\n---\nmetin\n```\nherkez\n```\nson"
        out = tu.apply_mask(t, tu.build_mask(t))
        self.assertNotIn("herşey", out)
        self.assertNotIn("herkez", out)
        self.assertIn("metin", out)
        self.assertIn("son", out)


if __name__ == "__main__":
    unittest.main()
