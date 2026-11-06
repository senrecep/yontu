"""Rule data: invariants and each rule's own examples."""
import json
import os
import unittest

from ortak import PKG, engine, rule_files, ids

LAYERS = set(engine.LAYERS)
EVIDENCE = {"kaynak", "veri", "hakem", "hipotez"}


def load(name):
    with open(os.path.join(PKG, "data", name), encoding="utf-8") as fh:
        return json.load(fh)["rules"]


class TestVeri(unittest.TestCase):
    def setUp(self):
        self.rules = engine.all_rules()

    def test_ids_unique(self):
        seen = [r.id for r in self.rules]
        self.assertEqual(len(seen), len(set(seen)))

    def test_layers_and_evidence(self):
        for r in self.rules:
            self.assertIn(r.layer, LAYERS, r.id)
            self.assertIn(r.d.get("evidence"), EVIDENCE, r.id)
            self.assertTrue(r.d.get("message"), r.id)

    def test_only_tdk_has_error_or_fix(self):
        for r in self.rules:
            if r.layer == "tdk":
                continue
            self.assertNotEqual(r.d.get("level"), "error", r.id)
            self.assertFalse(r.d.get("fix"), r.id)
            self.assertFalse(r.d.get("fixable"), r.id)
            for v in (r.d.get("registers_level") or {}).values():
                self.assertNotEqual(v, "error", r.id)

    def test_tdk_rules_cite_source(self):
        for r in self.rules:
            if r.layer == "tdk":
                self.assertEqual(r.d.get("evidence"), "kaynak", r.id)
                self.assertTrue(r.d.get("source"), r.id)

    def test_caps(self):
        regs = list(engine.profiller.registers())
        for r in self.rules:
            for reg in regs:
                lvl = engine.resolve_level(r, reg, None, {"enable": [r.id]})
                if not lvl:
                    continue
                if r.d.get("evidence") == "hipotez" or r.layer == "yogunluk":
                    self.assertEqual(lvl, 1, (r.id, reg))
                if r.layer != "tdk":
                    self.assertLessEqual(lvl, 2, (r.id, reg))

    def test_ys_a57_exists(self):
        self.assertIsNotNone(engine.rule_by_id("YS-A57"))

    def test_counts(self):
        by = {}
        for r in self.rules:
            by[r.layer] = by.get(r.layer, 0) + 1
        self.assertEqual(set(by), LAYERS)
        self.assertGreaterEqual(by["tdk"], 70)
        self.assertGreaterEqual(by["yogunluk"], 100)

    def test_rule_text_has_no_tdk_errors(self):
        for r in self.rules:
            for key in ("message", "suggestion"):
                t = r.d.get(key)
                if not t or "$" in t:
                    continue
                res = engine.lint(t, register="notr", layers=("tdk",))
                self.assertEqual(ids(res, level="error"), [], (r.id, key, t))


class TestOrnekler(unittest.TestCase):
    """Every rule must hit its pos examples and miss its neg examples."""

    def test_examples(self):
        bad = []
        n = 0
        for name in rule_files():
            for d in load(name):
                ex = d.get("examples") or {}
                cfg = {"enable": [d["id"]], "rules": {d["id"]: "on"}}
                reg = d.get("test_register") or (d.get("registers") or ["notr"])[0]
                for kind in ("pos", "neg"):
                    for t in ex.get(kind, []):
                        n += 1
                        res = engine.lint(t, register=reg, tur=d.get("test_tur"), config=cfg)
                        hit = d["id"] in ids(res)
                        if hit != (kind == "pos"):
                            bad.append((d["id"], kind, t))
        self.assertGreater(n, 500)
        self.assertEqual(bad, [])

    def test_every_rule_has_positive_example(self):
        missing = []
        for name in rule_files():
            for d in load(name):
                if not (d.get("examples") or {}).get("pos"):
                    missing.append(d["id"])
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
