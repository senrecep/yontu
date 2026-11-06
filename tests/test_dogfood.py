"""Regression tests for false positives found by linting the project's own documents.
Each test checks that the false alarm is gone and that the real error still fires."""
import unittest

from ortak import engine, profiller  # noqa: F401
from yontu import hook
from yontu import textutil as tu

ENGLISH = ("Don't run the linter on generated files. It reads the text, finds the rule "
           "that matches and reports it. 76% of the warnings in this file were style hints, "
           "and the rest can be fixed with the --fix flag when you want.")


def hits(text, rid, **kw):
    return [f for f in engine.lint(text, **kw)["findings"] if f["id"] == rid]


def every(text, **kw):
    return engine.lint(text, **kw)["findings"]


class TestFixMentions(unittest.TestCase):
    def test_quoted_word_is_not_fixed(self):
        text = "“Herşey” ve “Türkçe’de” biçimleri yanlıştır. Herşey yolunda."
        self.assertEqual(engine.fix(text),
                         "“Herşey” ve “Türkçe’de” biçimleri yanlıştır. Her şey yolunda.")
        # the finding is still reported; only the autofix leaves the mention alone
        found = [f for f in engine.lint(text)["findings"] if f["id"] == "BK-01"]
        self.assertEqual(len(found), 2)

    def test_long_quote_is_still_fixed(self):
        text = 'O gün "herşey bitti, artık gidiyorum" dedi.'
        self.assertEqual(engine.fix(text), 'O gün "her şey bitti, artık gidiyorum" dedi.')

    def test_straight_and_guillemet_mentions(self):
        for q in ('"Herşey"', "«Herşey»"):
            text = "%s biçimi yanlıştır." % q
            self.assertEqual(engine.fix(text), text)


class TestLanguageGuard(unittest.TestCase):
    def test_english_text_is_silent(self):
        self.assertEqual(every(ENGLISH), [])
        for rid in ("KS-07", "SY-01", "ST-03", "ST-01"):
            self.assertEqual(hits(ENGLISH, rid), [], rid)
        self.assertEqual(engine.fix(ENGLISH), ENGLISH)

    def test_short_turkish_still_fires(self):
        self.assertTrue(hits("%76 oranında arttı.", "SY-01") or hits("Herşey yolunda.", "BK-01"))
        self.assertTrue(every("Herşey yolunda."))

    def test_english_paragraph_inside_turkish_text(self):
        text = ("Bu belge yontu kurallarını anlatır. Herşey burada.\n\n" + ENGLISH + "\n\n"
                "Son paragraf da Türkçe yazılmıştır ve kısa tutulmuştur.")
        ids = [f["id"] for f in every(text)]
        self.assertNotIn("KS-07", ids)
        self.assertNotIn("SY-01", ids)
        self.assertTrue(any(f["line"] == 1 for f in every(text)))

    def test_fix_leaves_english_paragraph_alone(self):
        text = ("Bu paragraf Türkçe yazıldı ve herşey yolunda gidiyor, değil mi ?\n\n"
                "This paragraph is written in English , and it keeps a stray space before the comma .")
        out = engine.fix(text)
        self.assertTrue(out.startswith("Bu paragraf Türkçe yazıldı ve her şey yolunda gidiyor, değil mi?\n\n"))
        self.assertTrue(out.endswith(text.split("\n\n")[1]))

    def test_hook_reexports(self):
        self.assertIs(hook.is_turkish, tu.is_turkish)
        self.assertTrue(hook.is_turkish("Bu metin Türkçe yazıldı ve dil denetimi bunu doğru bulmalı."))
        self.assertFalse(hook.is_turkish(ENGLISH))


class TestMetalanguage(unittest.TestCase):
    def test_cz01_table_cell_and_named_glyph(self):
        for text in ("| SP-05 çift boşluk | info | — |", "Uzun çizgi (—) kullanılmaz."):
            self.assertEqual(hits(text, "CZ-01"), [], text)
        self.assertTrue(hits("Bu kural — bence — gerekli.", "CZ-01"))
        self.assertTrue(hits("| Ad | Çeviri — notu |", "CZ-01"))

    def test_sp04_sp01_named_glyph(self):
        for text in ("## 3. Nokta ( . )", "Tırnak ( “ ” ‘ ’ ), ayraç ( ( ) [ ] )"):
            self.assertEqual(hits(text, "SP-04"), [], text)
        self.assertEqual(hits("Soru ( ? ) işareti.", "SP-01"), [])
        self.assertEqual(hits("| zarf tümcesinde ? | bilgi |", "SP-01"), [])
        self.assertTrue(hits("Bu ( örnek ) yanlış.", "SP-04"))
        self.assertTrue(hits("Geldi , gitti.", "SP-01"))
        self.assertTrue(hits("Bitti .", "SP-01"))

    def test_tr01_opening_quote(self):
        self.assertEqual(hits("Metadil (\"'ve', 'ile' gibi\") atlanır.", "TR-01"), [])
        self.assertTrue(hits("“Çalıkuşu”'nu okudum.", "TR-01"))
        self.assertTrue(hits("Kitap \"Çalıkuşu\"'nu okudum.", "TR-01"))

    def test_st11_empty_pair(self):
        self.assertEqual(hits('Ayrıca "kitap" dedi. Kıvrık tırnak (“ ”) da var.', "ST-11"), [])
        self.assertTrue(hits('"Bir" ve “iki” dedi.', "ST-11"))


class TestListsAndSuffixes(unittest.TestCase):
    def test_c8_exact_triads(self):
        for text in ("Rapor, tutanak, dilekçe ve mektup ayrı yazılır. Hız, güven ve kalite de önemlidir.",
                     "Odak, yani yeni ve vurgulanan bilgi yüklemin önüne gelir. Hız, güven ve kalite önemlidir.",
                     "Blog, sohbet ve e-posta gevşek yazılır. Deneme, blog ve mektupta ses serbesttir.",
                     "| Hız, güven ve kalite | Ekip, süreç ve araçlar |"):
            self.assertEqual(hits(text, "AI-C8"), [], text)
        self.assertTrue(hits("Hız, güven ve kalite sunuyoruz. Ekip, süreç ve araçlar hazır.", "AI-C8"))
        # longer series count once each, adjectives are not text kinds
        self.assertTrue(hits("Hız, güven, kalite ve hizmet sunuyoruz. Ekip, süreç, araç ve kültür hazır.", "AI-C8"))
        self.assertTrue(hits("Hukuki, sosyal ve ekonomik boyutlar önemlidir. Hız, güven ve kalite sunuyoruz.",
                             "AI-C8"))

    def test_st36_date(self):
        self.assertEqual(hits("Duruşma tarihi açıklamada yer aldı.", "ST-36", register="haber"), [])

    def test_english_gate(self):
        en = "This is an English paragraph and it is long enough for the gate in the test.\n\n"
        self.assertTrue(hits(en + en + "Herkez geldi. Sonra gittiler.", "YZ-03"))
        self.assertTrue(hits(en + "Herkez geldi ve TDK'nın kararı açıklandı.", "KY-01K"))
        self.assertTrue(hits("Hata mesajı şu oldu: the file is not in the path and it is not found. "
                             "Herkez şaşırdı.", "YZ-03"))
        self.assertEqual(hits(en + en + en, "YZ-03"), [])

    def test_ky01_other_readings(self):
        for text in ("API'nin yanıtı geldi.", "API'de hata var.", "AI'ın etkisi büyük.", "AI'a sordum.",
                     "LLM'in çıktısı uzun.", "JS'te yazdım.", "MEB'e yazdı.", "KAY'a bakın.",
                     "MOR'un rengi koyu."):
            self.assertEqual(hits(text, "KY-01"), [], text)
        for text in ("ABD'ya göre durum değişti.", "PTT'ya gitti.", "TBMM'e gitti.", "TBMM'in kararı.",
                     "THY'ın uçağı.", "AB'ın kararı."):
            self.assertTrue(hits(text, "KY-01"), text)

    def test_ks07v_english_names(self):
        for text in ("Linter'a sordum.", "Linter'da hata yok.", "Humanizer'ın çıktısı.",
                     "Unicode'u okudum.", "Unicode'da yok.", "Case'e bakın."):
            self.assertEqual(hits(text, "KS-07V"), [], text)
        for text in ("Mehmet'a sordum.", "Ayşe'ya sordum.", "Emine'ya sordum.", "Emine'i gördüm.",
                     "Berker'a sordum.", "Gencer'ın evi."):
            self.assertTrue(hits(text, "KS-07V"), text)

    def test_ks03_function_word(self):
        self.assertEqual(hits("Ki'li cümleler eskidir.", "KS-03S"), [])
        self.assertEqual(hits("Bu yapı Ki'li cümle sayılır.", "KS-03B"), [])
        self.assertTrue(hits("Göreme'li rehberle konuştum.", "KS-03S"))
        self.assertTrue(hits("Bu Bergama'lı bir halıdır.", "KS-03B"))

    def test_vr02_conjunction_lists(self):
        for text in ("Bağlaçlar: *ve, ama, fakat* gibi.", "Metin içinde **ve, veya, yahut** bağlaçları.",
                     "| Ekleme | ve, de, hem |", "U u, Ü ü, V ve, Y ye, Z ze."):
            self.assertEqual(hits(text, "VR-02"), [], text)
        self.assertTrue(hits("Geldi ve, oturdu.", "VR-02"))
        self.assertTrue(hits("Elma aldı ve, eve döndü.", "VR-02"))


class TestSentenceUnits(unittest.TestCase):
    def test_c10q_question_lists(self):
        listed = ("Örnek sorular şunlardır. Kaldı mı? Sen de mi geldin? Olur mu? "
                  "İnsanlık öldü mü? Verecek misin? Okuyor muyuz?")
        self.assertEqual(hits(listed, "AI-C10Q"), [])
        self.assertTrue(hits("Neden mi? Çünkü hızlı. Peki ya fiyat? Gayet uygun.", "AI-C10Q"))

    def test_not_prose_units(self):
        from yontu import ozel

        class Ctx(object):
            pass
        self.assertTrue(ozel._not_prose("Sayın Müdürlüğe,", ["Sayın", "Müdürlüğe"]))
        self.assertTrue(ozel._not_prose("Konu : Staj başvurusu", ["Konu", "Staj", "başvurusu"]))
        self.assertTrue(ozel._not_prose("Kimlik: blog.", ["Kimlik", "blog"]))
        self.assertTrue(ozel._not_prose("a · b · c", ["a", "b", "c"]))
        self.assertFalse(ozel._not_prose("Bugün toplantı yapıldı.", ["Bugün", "toplantı", "yapıldı"]))

    def test_one_line_text_is_still_prose(self):
        # a short line without a period is a heading only when real sentences follow it
        line = "Günümüzde dijital okuryazarlık önem kazanmıştır"
        self.assertTrue(hits(line, "ST-17", register="akademik"))
        self.assertTrue(hits(line + "\nBu çalışma lise öğrencilerini incelemektedir.",
                             "ST-17", register="akademik"))
        self.assertFalse(hits("Giriş\n\nBu çalışma lise öğrencilerini incelemektedir. "
                              "Günümüzde dijital okuryazarlık önem kazanmıştır.",
                              "ST-17", register="akademik"))

    def test_st02_id_list(self):
        ids = " · ".join("tur%d" % i for i in range(40))
        text = ("Bu dosya tür kimliklerini listeler ve her biri ayrı bir rehbere bağlanır. "
                "Rehberler kısa tutulur. " + ids + ". Liste burada biter. Sonra örnekler gelir.")
        self.assertEqual(hits(text, "ST-02", register="haber"), [])

    def test_c18_labels_and_quotes(self):
        text = ("A1 Önem şişirme. A2 Boş geçiş. A3 Sahte derinlik. A4 Klişe kapanış. "
                "\"Siz\". \"Sen\". Bu liste yapay metinlerde sık görülen kalıpları sayar ve "
                "her birine kısa bir örnek ekler. Örnekler gerçek metinlerden alınmıştır.")
        self.assertEqual(hits(text, "AI-C18", register="blog"), [])
        clipped = ("Hızlı. Net. Etkili. Güvenli. Bu ürün işinizi kolaylaştırır. Hemen deneyin. "
                   "Pişman olmazsınız. Fark yaratır. Ekibimiz her zaman yanınızda ve sorularınızı "
                   "yanıtlamaya hazır bekliyor.")
        self.assertTrue(hits(clipped, "AI-C18", register="blog"))
        self.assertEqual(hits(clipped, "AI-C18", register="ui"), [])

    def test_c14_table_and_arrow(self):
        table = ("| Kalıp | Öneri |\n|---|---|\n| önemli | kritik |\n| hayati | elzem |\n\n"
                 "Bu tablo yalnız öneri verir.")
        self.assertEqual(hits(table, "AI-C14"), [])
        self.assertEqual(hits("Bu adım önemli. Sözcük seçimi: hayati → kritik, elzem.", "AI-C14"), [])
        self.assertTrue(hits("Bu adım önemli. Sonraki adım kritik. Son adım ise hayati.", "AI-C14"))

    def test_st09_named_forms(self):
        self.assertEqual(hits("Hitapta sen ve siz karışmamalı.", "ST-09"), [])
        example = "Bu bölüm hitabı anlatır.\n\nÖnce: Siz bunu bilirsin.\n\nSonra: Sen bunu bilirsin."
        self.assertEqual(hits(example, "ST-09"), [])
        self.assertEqual(hits("| ben de | sen de | siz de |", "ST-09"), [])
        self.assertTrue(hits("Sen bunu bilirsin. Siz de gelirsiniz.", "ST-09"))

    def test_st16_prose_lines(self):
        speech = "Elbette her şey yolunda gitmedi. Kırsal mahallelerde ulaşım zor oldu."
        self.assertEqual(hits(speech, "ST-16", tur="sunum"), [])
        # a single long sentence on a slide is still long, with or without a bullet
        self.assertTrue(hits("Bugün size geçen yıl başlattığımız evde bakım programının sonuçlarını anlatacağım.",
                             "ST-16", tur="sunum"))
        self.assertTrue(hits("- Gelirler geçen yıla göre belirgin biçimde arttı ve yüzde on ikiye ulaştı",
                             "ST-16", tur="sunum"))
        self.assertTrue(hits("Kaydet ve sonraki adıma geç ya da vazgeç", "ST-16", tur="ui-buton"))

    def test_st16s_per_block_in_ui(self):
        blocks = "Dosya yüklenemedi. Yeniden deneyin.\n\nBağlantı koptu. Ağınızı kontrol edin."
        self.assertEqual(hits(blocks, "ST-16S", tur="ui-hata"), [])
        long_ = "Dosya yüklenemedi. Boyut çok büyük. Sınır 10 MB. Yeniden deneyin."
        self.assertTrue(hits(long_, "ST-16S", tur="ui-hata"))


class TestDensityRules(unittest.TestCase):
    def test_yz04_both_spellings(self):
        for text in ("Şirketin unvanı değişti.", "Şirketin ünvanı değişti."):
            self.assertEqual(every(text), [], text)

    def test_c5_calisma(self):
        text = ("Bu çalışmada örneklem seçildi. Çalışmanın amacı açıktır. Çalışmaları inceledik. "
                "Çalışmamızda ölçek kullanıldı. Çalışmalarımız sürüyor.")
        self.assertEqual(hits(text, "AI-C5"), [])
        nominal = ("Sürecin iyileştirilmesi, verimin artırılması ve maliyetlerin düşürülmesi "
                   "hedeflenmektedir. Ekibin güçlendirilmesi ve eğitimlerin yapılması gerekir.")
        self.assertTrue(hits(nominal, "AI-C5"))

    def test_c6_format_and_role(self):
        text = ("Dosyayı JSON olarak kaydet. Çıktıyı metin olarak al. Varsayılan olarak açık gelir. "
                "Yönetici olarak gir.")
        self.assertEqual(hits(text, "AI-C6"), [])
        self.assertTrue(hits("Ekip olarak hızlı olarak ve düzenli olarak çalıştık.", "AI-C6"))

    def test_c7_kurumsal_threshold(self):
        rule = engine.rule_data("AI-C7")
        self.assertGreater(rule["register_threshold"]["kurumsal"], rule["threshold"])
        text = ("Yeni bina geçen ay hizmete açılmıştır. Proje bütçesi yönetim kurulunca onaylanmıştır. "
                "Çalışanlar için yeni bir eğitim programı hazırlanmıştır. Kampüste otopark alanı "
                "genişletildi ve girişler düzenlendi. Ekipler yeni ofislere taşındı ve masalar yerleşti. "
                "Önümüzdeki dönemde iki yeni şube açmayı planlıyoruz ve hazırlıklar sürüyor. "
                "Müşterilerimizden gelen öneriler de bu planlara yön veriyor.")
        self.assertEqual(hits(text, "AI-C7", register="kurumsal"), [])
        self.assertTrue(hits(text, "AI-C7", register="blog"))

    def test_c11_comma_clause(self):
        self.assertEqual(hits("Kurulum, bence, kolay; ayarlar sade.", "AI-C11", register="blog"), [])
        self.assertTrue(hits("Kurulum kolay; ayarlar sade.", "AI-C11", register="blog"))

    def test_c13_commit(self):
        text = ("Sürüm notları\n\n- **linter:** kural eklendi\n- **cli:** bayrak düzeldi\n"
                "- **hook:** hata giderildi\n")
        self.assertEqual(hits(text, "AI-C13", register="commit"), [])
        self.assertTrue(hits(text, "AI-C13", register="blog"))

    def test_st31_quoted(self):
        self.assertEqual(hits('Bu menü "en iyi" etiketini kullanmaz.', "ST-31", register="pazarlama"), [])
        self.assertTrue(hits("Şehrin en iyi kahvesi burada.", "ST-31", register="pazarlama"))


if __name__ == "__main__":
    unittest.main()
