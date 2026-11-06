"""Regression tests for residual false positives."""
import unittest

from ortak import engine


def hits(text, rid, **kw):
    return [f for f in engine.lint(text, **kw)["findings"] if f["id"] == rid]


class TestYanlisAlarm(unittest.TestCase):
    def test_a5b_akademik_mid_paragraph(self):
        text = ("Önceki çalışmalar bu sorunu farklı açılardan ele almıştır. Bu bağlamda, "
                "örneklem büyüklüğünün etkisi ayrıca incelenmiştir.")
        for tur in ("akademik-giris", "tez"):
            self.assertEqual(hits(text, "AI-A5B", tur=tur), [], tur)
        # a paragraph opened with it is still the tell, in akademik and elsewhere
        opener = "Bu bağlamda, konunun incelenmesi büyük önem taşımaktadır."
        self.assertTrue(hits(opener, "AI-A5B", tur="akademik-giris"))
        self.assertTrue(hits(text, "AI-A5B", tur="blog"))

    def test_a9_news_past_tense(self):
        text = "Bakanlığın verileri, ihracatın düştüğünü açıkça ortaya koydu."
        self.assertEqual(hits(text, "AI-A9"), [])
        self.assertTrue(hits("Bulgular bu etkiyi açıkça ortaya koymaktadır.", "AI-A9"))
        self.assertTrue(hits("Sonuçlar bunu kesin olarak ortaya koymuştur.", "AI-A9"))

    def test_l3b_literal_travel(self):
        for text in ("Bu yolculukta öğrendiğim en önemli şey, tren saatlerine güvenmemekti.",
                     "Ertesi gün Kars'a doğru yeni bir yolculuğa çıktık.",
                     "Bu keşif yolculuğu üç hafta sürdü."):
            for tur in (None, "blog"):
                self.assertEqual(hits(text, "AI-L3B", tur=tur), [], (text, tur))
        post = "Bugün yeni bir yolculuğa başlıyorum. Bu yolculukta öğrendiğim çok şey oldu."
        self.assertEqual(len(hits(post, "AI-L3B")), 2)
        # trend, kampanya are not travel cues
        for text in ("Bu yolculukta öğrendiğim en önemli şey trendleri takip etmekti.",
                     "Bu yolculukta öğrendiğim çok şey var, kampanya ekibimize teşekkürler."):
            self.assertTrue(hits(text, "AI-L3B"), text)

    def test_d15_legislative_pair(self):
        text = "Kamu kaynaklarının etkili, verimli ve güvenli bir şekilde kullanılması esastır."
        for reg in (None, "resmi", "hukuk"):
            self.assertEqual(hits(text, "AI-D15", register=reg), [], reg)
        self.assertTrue(hits("Uygulama modern, hızlı ve kullanıcı dostu.", "AI-D15"))
        # the pair inside a selling list still counts
        self.assertTrue(hits("Hızlı, etkili ve verimli bir çözüm sunuyoruz.", "AI-D15", tur="readme"))

    def test_c13e_event_and_menu_posts(self):
        event = ("Cumartesi akşamı sizi bekliyoruz!\n📍 Kadıköy Moda Sahnesi\n🕗 Saat 20.00\n"
                 "🎟️ Biletler kapıda\n🍷 İkram bizden\n")
        menu = "Bu haftanın menüsü\n🍕 Margarita 180 TL\n🍝 Penne 210 TL\n🥗 Sezar 150 TL\n"
        for text in (event, menu):
            for kw in ({}, {"tur": "instagram"}, {"register": "notr"}):
                self.assertEqual(hits(text, "AI-C13E", **kw), [], (text[:20], kw))
                self.assertEqual(hits(text, "ST-13", **kw), [], (text[:20], kw))
        # a selling-point list with a price inside a long line still counts
        sell = ("Neden biz?\n✅ Taze kavrum: çekirdekler siparişe özel kavrulur.\n"
                "✅ Esnek abonelik: istediğiniz zaman durdurun.\n"
                "✅ Ücretsiz kargo: 250 TL ve üzeri siparişlerde kargo bizden.\n")
        self.assertTrue(hits(sell, "AI-C13E", register="notr"))

    def test_c13e_st13_single_report(self):
        text = ("Merhaba ekip.\n🎉 Yeni sürüm çıktı.\nDetaylar aşağıda.\n✅ Hızlı kurulum\n"
                "✅ Yeni tema\n✅ Daha az bellek\n")
        ids = [f["id"] for f in engine.lint(text)["findings"]]
        self.assertIn("AI-C13E", ids)
        self.assertNotIn("ST-13", ids)
        # disabling AI-C13E brings ST-13 back
        ids = [f["id"] for f in engine.lint("<!-- yontu-disable AI-C13E -->\n" + text)["findings"]]
        self.assertIn("ST-13", ids)

    def test_st31_instructional_superlative(self):
        for text in ("En iyi sonuç için hamuru bir gece dinlendirin.",
                     "En iyi sonucu almak için fırını önceden ısıtın."):
            self.assertEqual(hits(text, "ST-31", register="pazarlama"), [], text)
        self.assertTrue(hits("Şehrin en iyi kahvesi burada.", "ST-31", register="pazarlama"))
        self.assertTrue(hits("En iyi fiyat bizde.", "ST-31", register="pazarlama"))

    def test_ky01_info_under_notr(self):
        # PR'ı (pi-ar) and CI'ın (si-ay) follow the English letter names: not flagged at all
        self.assertEqual(hits("PR'ı merge etmeden önce CI'ın geçtiğini kontrol et.", "KY-01"), [])
        text = "Paketi PTT'ya vermeden önce adresi bir kez daha kontrol et."
        res = engine.lint(text)
        self.assertEqual(res["register"], "notr")
        levels = {f["level"] for f in res["findings"] if f["id"] == "KY-01"}
        self.assertEqual(levels, {"info"})
        # a register that was detected or given keeps the warning
        self.assertEqual({f["level"] for f in hits("PTT'ya gittik.", "KY-01", register="blog")},
                         {"warning"})

    def test_ks07_french_silent_endings(self):
        text = "Renault'da çalışan arkadaşım Peugeot'dan teklif aldı. Bordeaux'dan şarap geldi."
        found = [f["id"] for f in engine.lint(text)["findings"] if f["id"].startswith("KS-07")]
        self.assertEqual(found, [])

    def test_ks03b_multiword_tech_terms(self):
        text = "Pull Request'ler incelendi ve GitHub Action'lar yeniden çalıştırıldı."
        found = hits(text, "KS-03B")
        self.assertEqual(len(found), 2)
        for f in found:
            self.assertEqual(f["level"], "warning")
            self.assertIsNone(f["fix"])
            self.assertIsNone(f["suggestion"])
        self.assertEqual(engine.fix(text), text)
        for f in hits("Bunu hangi Request'ler bozdu?", "KS-03B"):
            self.assertEqual(f["level"], "warning")
        # a lone Turkish proper name after a sentence-initial word stays an error
        found = hits("Toplantıya Akçaabat'lı iki müşteri katılacak.", "KS-03B")
        self.assertEqual([f["level"] for f in found], ["error"])

    def test_ks11_lowercase_brand_not_autofixed(self):
        text = "Siparişi yemeksepeti'nden verdim, yarım saatte geldi."
        self.assertEqual(engine.fix(text), text)
        found = [f for f in engine.lint(text)["findings"] if f["id"].startswith("KS-11")]
        self.assertTrue(found)
        for f in found:
            self.assertEqual(f["level"], "warning")
            self.assertIsNone(f["fix"])

    def test_yz02b_english_standard_not_flagged(self):
        self.assertEqual(hits("Standard library only, Python 3.9+.", "YZ-02B"), [])
        self.assertEqual(hits("Use the standard input for it.", "YZ-02B"), [])
        self.assertTrue(hits("Bu standard eski.", "YZ-02B"))


if __name__ == "__main__":
    unittest.main()
