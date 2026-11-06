"""Level policy per register and owner decisions."""
import unittest

from ortak import engine, ids

AI_TEXT = ("Günümüzde bu konu önemli bir rol oynamaktadır. Bu bağlamda ekip önemli bir rol "
           "oynamaktadır. Bu bağlamda süreç hızlı bir şekilde ilerlemektedir.")


def all_on():
    return {"enable": [r.id for r in engine.all_rules()]}


class TestRegister(unittest.TestCase):
    def test_notr_everything_info(self):
        res = engine.lint(AI_TEXT + " Herkez geldi.", register="notr", config=all_on())
        for f in res["findings"]:
            if f["layer"] != "tdk":
                self.assertEqual(f["level"], "info", f["id"])
        self.assertIn("YZ-03", ids(res, "tdk", "error"))

    def test_edebi_and_hukuk_tdk_only(self):
        for reg in ("edebi", "hukuk"):
            res = engine.lint(AI_TEXT + " Herkez geldi.", register=reg, config=all_on())
            self.assertEqual({f["layer"] for f in res["findings"]}, {"tdk"}, reg)

    def test_yogunluk_always_info(self):
        for reg in engine.profiller.registers():
            res = engine.lint(AI_TEXT, register=reg, config=all_on())
            for f in res["findings"]:
                if f["layer"] == "yogunluk":
                    self.assertEqual(f["level"], "info", (reg, f["id"]))

    def test_non_tdk_never_error(self):
        for reg in engine.profiller.registers():
            res = engine.lint(AI_TEXT, register=reg, config=all_on())
            for f in res["findings"]:
                if f["layer"] != "tdk":
                    self.assertNotEqual(f["level"], "error", (reg, f["id"]))
                    self.assertIsNone(f.get("fix"), (reg, f["id"]))

    def test_hizli_bir_sekilde_once(self):
        res = engine.lint("Bu iş hızlı bir şekilde bitti.")
        self.assertEqual(len(res["findings"]), 1)
        self.assertEqual(res["findings"][0]["layer"], "yogunluk")

    def test_absolute_counts_for_commit_and_ui(self):
        rule = engine.rule_by_id("AI-C1")
        for reg in ("commit", "ui"):
            ctx = engine.Context("kısa metin " * 400, reg, None, {})
            self.assertEqual(ctx.need({"per300": 3, "min": 2}), 2)
            self.assertEqual(engine._run_ratio(rule, ctx), [])

    def test_short_gate(self):
        for reg in ("sosyal", "pazarlama"):
            short = engine.Context("söz " * 40, reg, None, {})
            mid = engine.Context("söz " * 100, reg, None, {})
            self.assertEqual(short.need({"per300": 3, "min": 1}), 1)
            self.assertEqual(mid.need({"per300": 3, "min": 1}), 2)
        blog = engine.Context("söz " * 100, "blog", None, {})
        self.assertEqual(blog.need({"per300": 3, "min": 1}), 1)

    def test_scaled_density(self):
        ak = engine.Context("söz " * 300, "akademik", None, {})
        bl = engine.Context("söz " * 300, "blog", None, {})
        rule = {"per300": 3, "min": 2, "scaled": True}
        self.assertGreater(ak.need(rule), bl.need(rule))


class TestSahipKararlari(unittest.TestCase):
    NEVER = [("Projeye katkı sunmak istiyoruz.", "katkı sunmak"),
             ("Bu çalışma alana katkı sunmaktadır.", "katkı sunmaktadır"),
             ("Tekrardan başladık.", "Tekrardan"), ("Bunu illaki görecek.", "illaki"),
             ("Fiyatları arttırmak doğru değil.", "arttırmak"),
             ("Ona “tamam” dedim, o da ‘peki’ dedi.", "“tamam”"),
             ("Ona “tamam” dedim, o da ‘peki’ dedi.", "‘peki’")]

    def test_never_flagged(self):
        for reg in engine.profiller.registers():
            for t, word in self.NEVER:
                s = t.index(word)
                e = s + len(word)
                res = engine.lint(t, register=reg, config=all_on())
                hits = [f["id"] for f in res["findings"]
                        if f["start"] < e and f["end"] > s and f.get("scope") != "doc"
                        and f["end"] - f["start"] < len(t) - 1]
                self.assertEqual(hits, [], (reg, t))

    def test_hipotez_stays_info(self):
        for r in engine.all_rules():
            if r.d.get("evidence") != "hipotez":
                continue
            for reg in engine.profiller.registers():
                lvl = engine.resolve_level(r, reg, None, {"enable": [r.id], "rules": {r.id: "warning"}})
                self.assertIn(lvl, (None, 0, 1), (r.id, reg))


class TestAyar(unittest.TestCase):
    def test_profiles_cannot_turn_tdk_off(self):
        for reg in engine.profiller.registers():
            self.assertIn("YZ-03", ids(engine.lint("Herkez geldi.", register=reg)), reg)

    def test_user_config_can_turn_tdk_off(self):
        res = engine.lint("Herkez geldi.", config={"rules": {"YZ-03": "off"}})
        self.assertNotIn("YZ-03", ids(res))

    def test_turn_off_and_downgrade(self):
        t = "Bu iş hızlı bir şekilde bitti."
        self.assertNotIn("YS-B01", ids(engine.lint(t, config={"rules": {"YS-B01": "off"}})))
        self.assertEqual(ids(engine.lint(t, config={"rules": {"layer:yogunluk": "off"}})), [])
        res = engine.lint("Kapı açıktı — içeri girdik.", config={"rules": {"CZ-01": "info"}})
        self.assertEqual([f["level"] for f in res["findings"] if f["id"] == "CZ-01"], ["info"])

    def test_enable_default_off(self):
        off = [r for r in engine.all_rules() if r.d.get("default") == "off"
               and r.layer == "yogunluk" and (r.d.get("examples") or {}).get("pos")]
        self.assertTrue(off)
        r = off[0]
        t = r.d["examples"]["pos"][0]
        reg = r.d.get("test_register") or (r.d.get("registers") or ["notr"])[0]
        tur = r.d.get("test_tur")
        self.assertNotIn(r.id, ids(engine.lint(t, register=reg, tur=tur)))
        self.assertIn(r.id, ids(engine.lint(t, register=reg, tur=tur, config={"enable": [r.id]})))

    def test_layers_and_min_level(self):
        t = "Herkez geldi. Bu iş hızlı bir şekilde bitti."
        self.assertEqual({f["layer"] for f in engine.lint(t, layers=("tdk",))["findings"]}, {"tdk"})
        self.assertEqual(ids(engine.lint(t, min_level="error")), ["YZ-03"])

    def test_register_from_config(self):
        res = engine.lint("Kısa bir not.", config={"register": "haber"})
        self.assertEqual(res["register"], "haber")


class TestYonerge(unittest.TestCase):
    def test_next_line(self):
        t = "<!-- yontu-disable-next-line YZ-03 -->\nherkez geldi.\nherkez gitti."
        res = engine.lint(t)
        self.assertEqual([f["line"] for f in res["findings"] if f["id"] == "YZ-03"], [3])

    def test_block_with_trlint_prefix(self):
        t = "herkez\n<!-- trlint-disable -->\nherkez\nherkez\n<!-- trlint-enable -->\nherkez"
        res = engine.lint(t)
        self.assertEqual([f["line"] for f in res["findings"] if f["id"] == "YZ-03"], [1, 6])

    def test_block_for_one_id(self):
        t = "<!-- yontu-disable YZ-03 -->\nherkez hızlı bir şekilde geldi."
        res = engine.lint(t)
        self.assertNotIn("YZ-03", ids(res))
        self.assertIn("YS-B01", ids(res))

    def test_wrong_id_does_not_hide(self):
        t = "<!-- yontu-disable-next-line YZ-01 -->\nherkez geldi."
        self.assertIn("YZ-03", ids(engine.lint(t)))


if __name__ == "__main__":
    unittest.main()
