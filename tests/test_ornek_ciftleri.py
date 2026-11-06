"""Regression tests for the before/after example pairs in profiles.json."""
import unittest

from ortak import engine, profiller

# Pairs whose "before" side no rule catches today, with the reason.
EXPECTED_ZERO = {
    ("akademik-giris", 0): "missing gap statement; a content problem, not a surface pattern",
    ("akademik-tartisma", 1): "hedged academic boilerplate reads like normal academic prose",
    ("tez", 1): "vague contribution claim; needs content judgement",
    ("ui-bos", 0): "'Kayıt bulunamadı.' is correct; the pair adds guidance, not a fix",
    ("e-ticaret", 0): "praise adjectives also appear in human product copy",
    ("basin-bulteni", 1): "no rule targets the joy-and-pride cliché, and it sits inside a quotation",
    ("edebi", 0): "telling instead of showing; literary judgement",
    ("edebi", 1): "literary rhythm and cliché; literary judgement",
}

# Rules that must keep catching a given "before" text.
EXPECTED_RULE = {
    ("dilekce", 1): "YS-A25",
    ("resmi-yazi", 0): "ST-38",
    ("haber", 1): "ST-36",
    ("readme", 1): "ST-37",
    ("changelog", 0): "ST-35",
    ("changelog", 1): "ST-34",
    ("ui-buton", 0): "ST-33",
    ("ui-hata", 0): "ST-22U",
    ("ui-bos", 1): "ST-22B",
    ("x", 0): "AI-L5",
    ("instagram", 0): "AI-L5",
    ("is-eposta", 0): "ST-32",
    ("sunum", 1): "ST-32",
    ("sohbet", 0): "AI-D20",
}


def pairs():
    for tur, prof in profiller.profiles().items():
        for i, ex in enumerate(prof.get("examples", [])):
            yield tur, i, prof.get("register"), ex.get("once") or "", ex.get("sonra") or ""


class TestPairs(unittest.TestCase):
    def test_after_has_no_errors(self):
        for tur, i, reg, _once, sonra in pairs():
            res = engine.lint(sonra, tur=tur, register=reg)
            errors = [f["id"] for f in res["findings"] if f["level"] == "error"]
            self.assertEqual(errors, [], (tur, i))

    def test_before_is_caught(self):
        zero = set()
        for tur, i, reg, once, _sonra in pairs():
            if not engine.lint(once, tur=tur, register=reg)["findings"]:
                zero.add((tur, i))
        self.assertEqual(zero - set(EXPECTED_ZERO), set())

    def test_expected_rules(self):
        for (tur, i), rid in EXPECTED_RULE.items():
            prof = profiller.profiles()[tur]
            once = prof["examples"][i]["once"]
            res = engine.lint(once, tur=tur, register=prof.get("register"))
            self.assertIn(rid, [f["id"] for f in res["findings"]], (tur, i))

    def test_new_rules_silent_on_after(self):
        new = set(EXPECTED_RULE.values())
        for tur, i, reg, _once, sonra in pairs():
            res = engine.lint(sonra, tur=tur, register=reg)
            self.assertEqual([f["id"] for f in res["findings"] if f["id"] in new], [], (tur, i))


if __name__ == "__main__":
    unittest.main()
