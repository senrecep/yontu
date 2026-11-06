"""Autofix: safe, correct and idempotent."""
import unittest

from ortak import engine, insan, lines, read, sadakat


class TestFix(unittest.TestCase):
    def test_wrong_forms_fixed(self):
        fixed = 0
        for row in lines("yanlis-bicimler.txt"):
            wrong, right, sentence = row.split("\t")
            out = engine.fix(sentence)
            if out == sentence:
                continue
            fixed += 1
            self.assertEqual(out, sentence.replace(wrong, right), row)
            self.assertEqual(engine.fix(out), out, row)
        self.assertGreaterEqual(fixed, 150)

    def test_correct_text_unchanged(self):
        texts = [read("tdk-ornekler.txt"), read("maskeleme.md")] + [t for _, t in insan()]
        texts += [s for _, _, _, s in sadakat()]
        for text in texts:
            self.assertEqual(engine.fix(text), text, text[:60])

    def test_idempotent(self):
        text = "Herkez geldi. Yanlız kaldık, birşey olmadı. Bu gün hiç bir şey yapmadık."
        once = engine.fix(text)
        self.assertNotEqual(once, text)
        self.assertEqual(engine.fix(once), once)

    def test_fix_only_tdk(self):
        text = "Bu iş hızlı bir şekilde bitti. Günümüzde önemli bir rol oynamaktadır."
        self.assertEqual(engine.fix(text), text)

    def test_fix_spans_match_findings(self):
        text = "Herkez yanlız geldi."
        for f in engine.lint(text)["findings"]:
            if f.get("fix") is not None:
                self.assertEqual(f["layer"], "tdk")
                self.assertEqual(text[f["start"]:f["end"]], f["match"])


if __name__ == "__main__":
    unittest.main()
