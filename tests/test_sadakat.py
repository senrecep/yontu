"""Fidelity gate: compare(old, new)."""
import unittest

from ortak import fidelity, sadakat


def found(old, new):
    return [f["id"] for f in fidelity.compare(old, new)["findings"]]


def items(old, new, fid):
    return [f.get("item") for f in fidelity.compare(old, new)["findings"] if f["id"] == fid]


class TestAdded(unittest.TestCase):
    def test_new_number(self):
        self.assertIn("14.00", items("Toplantı yarın.", "Toplantı yarın 14.00'te.", "SD-01"))

    def test_new_date(self):
        res = fidelity.compare("Sürüm çıktı.", "Sürüm 12 Mart 2024'te çıktı.")
        self.assertIn("SD-02", [f["id"] for f in res["findings"]])
        self.assertGreaterEqual(res["errors"], 1)

    def test_new_url(self):
        self.assertIn("https://ornek.com",
                      items("Belgeye bakın.", "Belgeye https://ornek.com adresinden bakın.", "SD-03"))

    def test_new_code(self):
        self.assertIn("npm test", items("Testleri çalıştırın.", "Testleri `npm test` ile çalıştırın.", "SD-04"))

    def test_new_name(self):
        got = items("Rapor hazırlandı.", "Rapor Ahmet Yılmaz tarafından hazırlandı.", "SD-05")
        self.assertEqual(sorted(got), ["Ahmet", "Yılmaz"])

    def test_name_is_not_negation(self):
        self.assertNotIn("SD-07", found("Rapor hazırlandı.", "Rapor Ahmet Yılmaz tarafından hazırlandı."))

    def test_added_items_are_errors(self):
        res = fidelity.compare("Rapor hazırlandı.", "Rapor Ahmet tarafından 3 günde hazırlandı.")
        self.assertEqual(res["errors"], 2)


class TestChanged(unittest.TestCase):
    def test_removed_items_warn(self):
        res = fidelity.compare("Rapor 5 sayfa, Ahmet hazırladı.", "Rapor hazır.")
        self.assertEqual(sorted(f.get("item") for f in res["findings"] if f["id"] == "SD-06"),
                         ["5", "Ahmet"])
        self.assertEqual(res["errors"], 0)

    def test_negation(self):
        self.assertIn("SD-07", found("Bu yöntem işe yarar.", "Bu yöntem işe yaramaz."))
        self.assertIn("SD-07", found("Gelir.", "Gelmez."))

    def test_modality(self):
        self.assertIn("SD-08", found("Bu yöntem işe yarayabilir.", "Bu yöntem işe yaramalı."))

    def test_evidence_ladder(self):
        self.assertIn("SD-09", found("Veriler bunu düşündürüyor.", "Veriler bunu kanıtlıyor."))

    def test_first_person(self):
        self.assertIn("SD-10", found("Rapor hazırlandı.", "Raporu ben hazırladım."))

    def test_new_cause(self):
        self.assertIn("SD-11", found("Satışlar düştü.", "Satışlar düştü, çünkü fiyatlar arttı."))

    def test_changes_are_warnings(self):
        for old, new in (("Bu yöntem işe yarar.", "Bu yöntem işe yaramaz."),
                         ("Veriler bunu düşündürüyor.", "Veriler bunu kanıtlıyor."),
                         ("Satışlar düştü.", "Satışlar düştü, çünkü fiyatlar arttı.")):
            self.assertEqual(fidelity.compare(old, new)["errors"], 0, new)


class TestEquivalent(unittest.TestCase):
    def test_identical(self):
        text = "Bu iş önemli. Çok önemli. Ahmet 3 gün sonra, 12 Mart'ta gelecek."
        self.assertEqual(fidelity.compare(text, text)["findings"], [])

    def test_number_formats(self):
        self.assertEqual(found("Ödeme 1.500 TL.", "Ödeme 1500 TL."), [])

    def test_list_markers(self):
        self.assertEqual(found("1. Adım\n2. Adım", "Adım\nAdım"), [])

    def test_apostrophe_variants(self):
        self.assertEqual(found("Şirketi'ndeki çalışanlar", "Şirketindeki çalışanlar"), [])

    def test_reported_speech(self):
        self.assertEqual(found("Dedi ki geleceğim.", "\"Geleceğim\" dedi."), [])

    def test_empty(self):
        self.assertEqual(fidelity.compare("", "")["findings"], [])


class TestFixtures(unittest.TestCase):
    def test_pairs_have_no_errors(self):
        pairs = sadakat()
        self.assertGreaterEqual(len(pairs), 40)
        for name, _reg, once, sonra in pairs:
            res = fidelity.compare(once, sonra)
            self.assertEqual(res["errors"], 0, (name, [f for f in res["findings"] if f["level"] == "error"]))


if __name__ == "__main__":
    unittest.main()
