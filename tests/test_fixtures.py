"""Corpus checks: TDK-correct text, wrong forms, masking, human and AI texts."""
import unittest

from ortak import engine, ids, insan, lines, profiller, read, sadakat


class TestTdk(unittest.TestCase):
    def test_correct_examples_clean(self):
        text = read("tdk-ornekler.txt")
        self.assertEqual(ids(engine.lint(text), "tdk"), [])
        for line in lines("tdk-ornekler.txt"):
            self.assertEqual(ids(engine.lint(line), "tdk"), [], line)

    def test_wrong_forms_recall(self):
        rows = lines("yanlis-bicimler.txt")
        self.assertGreaterEqual(len(rows), 150)
        missed = []
        for row in rows:
            wrong, _right, sentence = row.split("\t")
            hit = [f for f in engine.lint(sentence)["findings"] if f["layer"] == "tdk"
                   and sentence.find(wrong) < f["end"] and f["start"] < sentence.find(wrong) + len(wrong)]
            if not hit:
                missed.append(wrong)
        self.assertEqual(missed, [])


class TestMasking(unittest.TestCase):
    def test_masked_regions_silent(self):
        res = engine.lint(read("maskeleme.md"), config={"enable": [r.id for r in engine.all_rules()]})
        self.assertEqual(res["findings"], [])


class TestHuman(unittest.TestCase):
    def check(self, reg, text, register):
        res = engine.lint(text, register=register)
        self.assertEqual(ids(res, "tdk"), [], (reg, register))
        self.assertEqual(ids(res, "ai-iz", "warning"), [], (reg, register))
        self.assertLessEqual(len(ids(res, "ai-iz")), max(1, res["words"] // 300), (reg, register))

    def test_budget(self):
        texts = insan()
        self.assertGreaterEqual(len(texts), 48)
        for reg, text in texts:
            self.check(reg, text, reg)
            self.check(reg, text, None)

    def test_every_register_has_three_texts(self):
        count = {}
        for reg, _ in insan():
            count[reg] = count.get(reg, 0) + 1
        regs = set(profiller.registers()) - {"notr"}
        self.assertEqual({r for r in regs if count.get(r, 0) < 3}, set())

    def test_every_tur(self):
        # tür-scoped rules only run under their tür, so each text is checked under every
        # tür of its register.
        for reg, text in insan():
            for tur, prof in profiller.profiles().items():
                if prof["register"] != reg:
                    continue
                res = engine.lint(text, tur=tur)
                self.assertEqual(ids(res, "tdk"), [], (reg, tur))
                self.assertEqual(ids(res, "ai-iz", "warning"), [], (reg, tur))
                self.assertLessEqual(len(ids(res, "ai-iz")), max(1, res["words"] // 300), (reg, tur))

    def test_detection(self):
        # Only the first text of each register is a detection target; the others may fall
        # back to notr, which keeps ai-iz at info.
        for name, reg, text in insan(names=True):
            if name in ("akademik", "haber", "teknik", "resmi", "is-eposta", "sohbet"):
                self.assertEqual(engine.lint(text)["register"], reg)


class TestAi(unittest.TestCase):
    def test_ai_texts_flagged_more_than_human(self):
        human = {reg: len(ids(engine.lint(text, register=reg), "ai-iz")) for reg, text in insan()}
        for name, reg in (("ai-metin-blog.md", "blog"), ("ai-metin-akademik.md", "akademik")):
            text = read(name)
            in_reg = len(ids(engine.lint(text, register=reg), "ai-iz"))
            default = len(ids(engine.lint(text), "ai-iz"))
            self.assertGreaterEqual(in_reg, 3, name)
            self.assertGreaterEqual(default, 4, name)
            self.assertGreater(in_reg, human[reg], name)

    def test_ai_findings_not_errors(self):
        for name in ("ai-metin-blog.md", "ai-metin-akademik.md"):
            # The blog sample keeps one em dash on purpose: it is one of the tells under test.
            self.assertLessEqual(set(ids(engine.lint(read(name)), "tdk")), {"CZ-01"}, name)
            for f in engine.lint(read(name), register="blog")["findings"]:
                if f["layer"] == "ai-iz":
                    self.assertIn(f["level"], ("info", "warning"), f["id"])


class TestSadakatTexts(unittest.TestCase):
    def test_sonra_clean(self):
        for name, reg, _once, sonra in sadakat():
            self.assertEqual(ids(engine.lint(sonra, register=reg), "tdk"), [], name)


if __name__ == "__main__":
    unittest.main()
