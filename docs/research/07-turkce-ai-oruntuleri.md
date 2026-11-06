# 07 - Türkçeye özgü yapay zekâ metin izleri ve çeviri kokusu (translationese)

Kapsam: AI ajanları için Türkçe humanizer (skill + deterministik linter + hook). Bu dosya bir katalog. Her iz için: neden iz, regex ipucu, yanlış pozitif (FP) riski, önce/sonra örneği.
Tarih: 2026-11-05. Örnekler Türkçe, açıklamalar karışık.

---

## 0. Kanıt tabanı ve korpus istatistikleri

### 0.1 Ampirik çalışmalar (Türkçe)

| Kaynak | Bulgu | Linter için anlamı |
|---|---|---|
| Kocagül 2026, *Detecting the Human in the Machine* (Çankaya Univ. JHSS), 336 tartışmacı metin, 56 katılımcı, 61 özellik. https://doi.org/10.47777/cankujhss.1957142 | Cümle başında "Sonuç": AI %83.9, insan %7.2. **Noktalı virgül: AI %76.8, insan %15.2.** Yüksek virgül yoğunluğu: %82.1 / %20.5. Tırnak işareti: %42.9 / %8.9. Cümle başı söylem belirleyicileri (öncelikle, ayrıca, sonuç olarak): %83.9 / %25.9. **-ArAk zarf-fiil zinciri: %82.1 / %32.2.** Çok paragraflı yapı: %53.6 / %2.7. İnsan tarafı: cümle başı "aslında/ama/çünkü/bence" %31.3 / AI %23.2. Yüklem düşürme (eksiltili cümle): insan %20.5 / AI %3.6. Editörlü hibrit metinlerde 61 özelliğin 41'i (%67) AI profilinde kalıyor. | En güçlü tekil sinyaller bunlar. Noktalı virgül, Pangram'ın "AI noktalı virgül kullanmaz" iddiasının tersine, **Türkçede AI sinyali**. -ArAk ve cümle başı bağlaç sayımı birinci sınıf özellik olmalı. |
| Bergin & Atasoy 2026, UTOAD, 147 ChatGPT-4o-mini + 147 öğrenci metni. https://dergipark.org.tr/tr/pub/utoad/article/1805843 | AI: 34.235 token / 2.365 tür (TTR %6.9). Öğrenci: 23.306 / 3.800 (TTR %16.3). Deyim: AI 1.038 kullanım ama 107 tür; öğrenci 559 kullanım, 205 tür. İkileme: AI 68 kullanım / 10 tür, öğrenci 53 / 29. Atasözü: AI 0. | AI deyim ve ikilemeyi **çok ama tekdüze** kullanıyor. Linter: aynı deyim/ikileme tekrarı ve düşük tür/kullanım oranı. "Deyim ekle" tavsiyesi dikkatli verilmeli. |
| Uzun 2024, IntechOpen, ChatGPT-4 Türkçe akademik + duygusal metin. https://doi.org/10.5772/intechopen.1007724 | AI ortalama cümle 15-20 kelime, paragraf 5-7. Akademik metinde insanla fark küçük (Cohen d≈0.3). Duygusal metinde belirgin fark. | Akademik registerda sözcük düzeyi tespit zayıf. Duygusal/kişisel registerda ton ve somutluk daha ayırt edici. |
| Şimşek & Özdemir 2026, JLERE. https://dergipark.org.tr/en/pub/jlere/article/1858803 | ChatGPT daha yüksek karmaşık (birleşik) cümle oranı, daha az hata. | Hatasızlık + birleşik cümle yoğunluğu birlikte iz. |
| "Söz dizimi açısından ChatGPT'nin Türkçesi", UÜFEFSBD. https://dergipark.org.tr/en/download/article-file/4293409 | GPT-4 yazım/noktalama hatası nadir; tüm cümle türlerini kurabiliyor. Tipik örnek: "Değişim, kimi zaman korkutucu olsa da, aslında ... göstergesidir." | "-sa da ... aslında ... göstergesidir" ödünleme kalıbı. |
| TÜBİTAK Bilim Genç 2023 (arXiv özetine dayanır). https://bilimgenc.tubitak.gov.tr/makale/bir-metni-chatgptnin-hazirladigi-anlasilabilir-mi | İnsan metninde ünlem, üç nokta ve parantez içi açıklama daha sık; AI daha nesnel ve konu odaklı. | Duygu noktalaması yokluğu zayıf sinyal (blog registerı için). |
| Özdemir 2026, arXiv 2602.13504 | BERTurk ile Türk haber metinlerinde AI yeniden yazımı tespiti F1 0.971; 2023-2026 haberlerinin ~%2.5'i LLM ile yeniden yazılmış. | Sınıflandırıcı mümkün ama bu proje deterministik; yüzey sinyalleri yeterli değil, yoğunluk skoru şart. |
| Diğer tespit çalışmaları: Kayabaş vd. 2025 (MDPI Appl. Sci. 15/10/5541, LSTM %97.28); MDPI 2026 Appl. Sci. 16/14/7249 (DistilBERT+GCN, TR %98; veri: hf `aycabostancioglu/Arabic-English-Turkish-AI-Human-Text`); TUM neural-news benchmark (hf `tum-nlp/neural-news-benchmark`); Karabulut 2026 tezi (tezara 1018532, 9.5M cümle, BERTurk %98.98) | Model tabanlı yüksek doğruluk. | Linter test seti için hazır etiketli veri kaynağı. |

### 0.2 İnsan Türkçesi normları (baz çizgisi)

- **Ateşman okunabilirlik:** `198.825 - 40.175*(hece/kelime) - 2.610*(kelime/cümle)`. 70-89 kolay, 50-69 orta, 30-49 zor, <30 çok zor. (researchgate 380156427)
- **Ortalama cümle uzunluğu** Türkçe genel metinde 9-11 kelime, kelime başına ~2.6 hece (Bezirci & Yılmaz, YOD; https://dergipark.org.tr/tr/pub/deumffmd/issue/40831/492667). AI akademik/blog çıktısı 15-22 kelimede yoğunlaşıyor ve sapması düşük.
- **Bağlaç dağılımı** (Keklik & Yılmaz 2013, https://dergipark.org.tr/tr/download/article-file/202242): karşıtlık bağlaçları (ama/ancak) eklemeli bağlaçların (ve, de/da) kabaca 1/5'i; "yani" tüm bağlaçların %1-2'si.
- **Sıklık listeleri** (Vikisözlük Türkçe sıklık listesi, TS Corpus 1.8B token, TNC 50M kelime): "ama" ilk 25'te (Vikisözlük'te 20.). "öte yandan", "bununla birlikte", "bu bağlamda" ilk 50'nin hiçbirinde yok. Yani bunların sık görülmesi doğal dağılımdan sapma.
- **İnsan hatası insan sinyalidir:** RTÜK 2019 Doğru Türkçe raporu 4.598 hata saymış (de/da, ki, büyük harf, gereksiz "olan"). Hatasız ama ritimsiz metin AI'a işaret eder. Humanizer hata **eklememeli** ama hatasızlığı tek başına kanıt saymamalı.

### 0.3 Önceki çalışmalar (prior art)

- `bushrabeg/turkce-humanizer` (SKILL.md v3.2): 5 mutlak yasak, eşikli sinyaller, 100 kelime başına rapor.
- `tahiryildiz/insanca` (48 örüntü + `references/kaynaklar.md`): en kapsamlı Türkçe örüntü listesi. Küme (cluster) tespiti öneriyor; sert iz ile yumuşak iz arasında ~20 kat güven farkı.
- Web rehberleri: hidengpt.com/tr/rehber/chatgpt-yazisi-nasil-anlasilir (300 kelimede 6-7 örüntü + somut detay yok = şüpheli), pangram.com/tr (çeviri listeler), assistin.ai, tezmakale.com, yapaytu.com, hub.chatday.ai.
- Çeviri kokusu: Attila Aşut, BirGün 2024 "Çeviri söylemler" (https://www.birgun.net/makale/ceviri-soylemler-558960); Milliyet Blog "Türkçe'nin yaraları"; DergiPark TV çevirisi hataları (article-file/424284); Necmiye Alpay, *Türkçe Sorunları Kılavuzu*; AA "Türkçeyi Doğru Kullan"; Dragoman editör rehberi.

---

## A. Sözcüksel klişeler (170 madde, sade karşılıklarıyla)

Genel FP kuralı: tek eşleşme ceza değil. Skor = ağırlıklı eşleşme / 100 kelime. Akademik ve hukuki registerda A2/A5'in eşiği 2 kat yüksek tutulmalı.

Regex notları (tüm bölüm için):
- Python `re` Unicode'da `\w` Türkçe harfleri kapsar; `\b` çalışır. **Büyük/küçük harf için `re.I` kullanma**: `I/ı` ve `İ/i` yanlış eşleşir. Önce Türkçeye özel küçültme yap: `s.replace("I","ı").replace("İ","i").lower()`.
- Ünlü uyumu ve kaynaştırma için çekim eki grubu: `(?:\w*)` kuyruk yeterli. Örnek: `\bkilit (?:bir )?rol oyna\w*`.
- Şapka varyantı: `hâl|hal`, `imkân|imkan`, `kâr|kar` için `[aâ]`.

### A1. Önem şişirme (significance inflation)
Neden iz: Her konuyu "kritik/hayati" seviyesine çıkarma, RLHF ödül eğilimi. Türkçede "-maktadır" ile birleşip kalıp cümle üretir.
Regex: `\b(?:kilit|kritik|hayati|önemli|büyük|merkezi) (?:bir )?(?:rol|önem|yer|işlev)\w* (?:oyna|taşı|üstlen|arz et|sahip)\w*`
FP: Orta. Bilimsel metinde "kritik sıcaklık", "kritik yol" terimdir. Terim listesi muafiyeti gerekir.

| # | Klişe | Sade alternatif |
|---|---|---|
| 1 | kilit bir rol oynamaktadır | X'i belirler / X olmadan Y olmaz |
| 2 | kritik bir rol oynar | etkiler, belirler |
| 3 | hayati bir önem taşımaktadır | çok önemli / (somut sonuç yaz) |
| 4 | büyük önem arz etmektedir | önemlidir |
| 5 | önemli bir yere sahiptir | önemlidir / çok kullanılır |
| 6 | önemli bir rol üstlenmektedir | ... yapar (eylemi yaz) |
| 7 | vazgeçilmez bir hale gelmiştir | artık herkes kullanıyor |
| 8 | hayatımızın ayrılmaz bir parçası haline geldi | (sil, ya da somut sayı ver) |
| 9 | dönüm noktası | önemli an / (tarih ve olay) |
| 10 | çığır açan | yeni, ilk |
| 11 | devrim niteliğinde | büyük bir değişiklik |
| 12 | oyunun kurallarını değiştiren | işleri değiştiren / (neyi değiştirdiğini yaz) |
| 13 | ezber bozan | alışılmışın dışında |
| 14 | kalıcı bir iz bırakmak | etkisi sürdü |
| 15 | köklü bir geçmişe sahip | eski, X yıldır var |
| 16 | zemin hazırlamak | yol açmak |
| 17 | ... habercisi | ... işareti / ... olacağını gösteriyor |
| 18 | giderek daha önemli hale gelmektedir | önemi artıyor |
| 19 | son yıllarda giderek önem kazanmaktadır | son yıllarda öne çıktı |
| 20 | yeni bir çağın kapılarını aralamak | yeni bir dönem başlatmak |
| 21 | paradigma değişimi | yaklaşım değişti |
| 22 | X'in DNA'sında var | X'in temel özelliği |
| 23 | altın standart | en iyi bilinen yöntem |
| 24 | göz ardı edilemez bir gerçek | açık |
| 25 | tartışmasız bir şekilde | açıkça / (sil) |

### A2. Hafif fiil ve fiil kalıpları (bürokratik ağırlaştırma)
Neden iz: İngilizce "perform/conduct/provide" karşılıkları ile isim+gerçekleştirmek yapısı. Türkçe tek fiille söyler. Çeviri metinlerden ve kurumsal korpustan geçmiş.
Regex: `\b\w+(?:ma|me|ım|im|um|üm|ış|iş|uş|üş)\w* (?:gerçekleştir|sağla|olanak tanı|imkan sun|imkân sun|katkı sağla|hayata geçir)\w*`
FP: Orta-yüksek. "sağlamak" asıl anlamıyla (provide) yaygın. Yoğunluk eşiği: 100 kelimede ≥2.

| # | Klişe | Sade alternatif |
|---|---|---|
| 26 | toplantı gerçekleştirmek | toplanmak |
| 27 | kutlama gerçekleştirmek | kutlamak |
| 28 | ziyaret gerçekleştirmek | ziyaret etmek |
| 29 | sohbet gerçekleştirmek | sohbet etmek, konuşmak |
| 30 | analiz gerçekleştirmek | incelemek |
| 31 | değerlendirme yapmak | değerlendirmek |
| 32 | açıklama yapmak | açıklamak |
| 33 | katkı sağlamak / katkıda bulunmak | katkısı olmak, yardım etmek |
| 34 | olanak tanımak | -ebilmek / sağlamak |
| 35 | imkan sunmak | -ebilmek |
| 36 | yapma imkanına sahiptir | yapabilir |
| 37 | fayda sağlamak | işe yaramak |
| 38 | hayata geçirmek | başlatmak, uygulamak |
| 39 | önem arz etmek | önemli olmak |
| 40 | göz önünde bulundurmak | düşünmek, hesaba katmak |
| 41 | dikkate almak | düşünmek |
| 42 | ele almak | incelemek, anlatmak |
| 43 | değinmek (zincirleme) | söylemek |
| 44 | altını çizmek | vurgulamak / (sil) |
| 45 | vurgulamak (her paragrafta) | demek, söylemek |
| 46 | ışık tutmak | açıklamak, göstermek |
| 47 | gözler önüne sermek | göstermek |
| 48 | ortaya koymak | göstermek |
| 49 | potansiyelini ortaya çıkarmak | iyi kullanmak |
| 50 | değer katmak | işe yaramak, iyileştirmek |
| 51 | fark yaratmak | işe yaramak / (farkı yaz) |
| 52 | zenginleştirmek | geliştirmek, çeşitlendirmek |
| 53 | şekillendirmek | belirlemek, etkilemek |
| 54 | yön vermek | belirlemek |
| 55 | dönüştürmek (soyut) | değiştirmek |
| 56 | optimize etmek (genel metinde) | iyileştirmek |
| 57 | beraberinde getirmek | yol açmak, getirmek |
| 58 | ön plana çıkmak | öne çıkmak |
| 59 | kendini göstermek | görülmek |
| 60 | dikkat çekmektedir | (sil) / görülüyor |
| 61 | söz konusu olmak | olmak, var olmak |
| 62 | yer almaktadır | var, bulunuyor |
| 63 | bulunmaktadır | var |
| 64 | mevcuttur | var |
| 65 | barındırmaktadır | içerir, vardır |
| 66 | olma özelliğine sahiptir | -dır |
| 67 | işlevi görmektedir | -dır, iş görür |
| 68 | olarak hizmet vermektedir | -dır |
| 69 | olarak öne çıkmaktadır | -dır |
| 70 | niteliği taşımaktadır | -dır |
| 71 | konumundadır | -dır |
| 72 | keşfetmek (her şey için) | bakmak, öğrenmek, denemek |

### A3. Boş değerlendirici sıfat ve zarflar
Neden iz: Somut bilgi yerine onay sıfatı. Bergin & Atasoy'un düşük TTR bulgusuyla tutarlı: aynı 20-30 sıfat dönüp duruyor.
Regex: `\b(?:kapsamlı|bütüncül|derinlemesine|eşsiz|benzersiz|paha biçilmez|yenilikçi|dönüştürücü|dinamik|etkileyici|büyüleyici|vazgeçilmez|sürdürülebilir|kusursuz|sorunsuz|güçlü|sağlam)\b`
FP: Orta. "sürdürülebilir kalkınma", "dinamik programlama" terimdir. Eşik: paragrafta ≥2 veya 100 kelimede ≥3.

| # | Klişe | Sade alternatif |
|---|---|---|
| 73 | kapsamlı bir rehber | rehber / (kaç madde olduğunu yaz) |
| 74 | derinlemesine bir inceleme | inceleme |
| 75 | bütüncül bir yaklaşım | her yönüyle ele alan / (yönleri say) |
| 76 | eşsiz bir deneyim | (deneyimi anlat) |
| 77 | benzersiz | farklı / (farkı yaz) |
| 78 | paha biçilmez | çok değerli |
| 79 | yenilikçi | yeni |
| 80 | dönüştürücü | büyük değişiklik getiren |
| 81 | dinamik (genel sıfat) | hızlı değişen / canlı |
| 82 | etkileyici | iyi / (neden etkilediğini yaz) |
| 83 | büyüleyici | güzel, ilginç |
| 84 | göz kamaştıran | parlak, gösterişli |
| 85 | son derece | çok |
| 86 | oldukça (her cümlede) | (sil) |
| 87 | etkili bir şekilde | iyi / (sil) |
| 88 | etkin bir biçimde | (sil) |
| 89 | sorunsuz bir şekilde | sorunsuz |
| 90 | kusursuz | iyi, hatasız |
| 91 | zengin bir mozaik | çeşitli |
| 92 | çok boyutlu | birçok yönü olan |
| 93 | çok yönlü | işe yarayan / (alanları say) |
| 94 | değerli içgörüler | bilgi, fikir |
| 95 | anlamlı (her yerde) | (sil) |
| 96 | adeta bir zaman kapsülü | (sil, somut tarih) |
| 97 | unutulmaz bir deneyim | (ne olduğunu anlat) |
| 98 | her damak tadına hitap eden | çeşitli |
| 99 | doğayla iç içe | ağaçlık, kırsal |
| 100 | tarihin ve modernin buluştuğu | eski ve yeni yapılar yan yana |

### A4. Moda mecazlar ve isimler
Neden iz: İngilizce LLM jargonu (journey, tapestry, landscape, ecosystem, delve, symphony) doğrudan çevriliyor. Türkçede bu kullanımlar korpusta seyrek.
Regex: `\b(?:yolculu[kğ]\w*|goblen\w*|manzara\w*|ekosistem\w*|senfoni\w*|dokunuş\w*|sinerji\w*|mozaik\w*|labirent\w*|pusula\w*)\b`
FP: Düşük-orta. Gerçek yolculuk, gerçek manzara, biyolojik ekosistem. Bağlam: soyut isimle tamlama (`\w+ yolculuğu`, `\w+ ekosistemi`) ise iz.

| # | Klişe | Sade alternatif |
|---|---|---|
| 101 | öğrenme yolculuğu | öğrenme süreci, öğrenirken |
| 102 | kariyer yolculuğunuz | kariyeriniz |
| 103 | karmaşık bir goblen | karışık bir yapı |
| 104 | sürekli değişen manzara | hızla değişen alan |
| 105 | X'in dinamik dünyasında | X'te |
| 106 | dijital ekosistem | dijital araçlar / (araçları say) |
| 107 | bir senfoni gibi | uyumlu |
| 108 | son dokunuş | son ayar |
| 109 | sinerji yaratmak | birlikte daha iyi çalışmak |
| 110 | vizyon (her metinde) | hedef, plan |
| 111 | X'in derinliklerine dalmak | X'i ayrıntılı incelemek |
| 112 | kapılarını aralamak | başlatmak |
| 113 | köprü kurmak (soyut) | bağlamak |
| 114 | yol haritası | plan |
| 115 | pusula görevi görmek | yol göstermek |
| 116 | anahtarı (başarının anahtarı) | için gerekli |
| 117 | X'in kalbinde | X'in merkezinde / (sil) |
| 118 | bir sonraki seviyeye taşımak | geliştirmek, ilerletmek |
| 119 | konfor alanından çıkmak | alışmadığın şeyi denemek |
| 120 | dengeyi bulmak | ikisini de idare etmek |
| 121 | bir hatırlatma niteliğinde | hatırlatıyor |
| 122 | insan ruhu | insan |
| 123 | mirası | bıraktıkları |
| 124 | söylenmemişlerin ağırlığı | (sil) |
| 125 | arasındaki sınırı bulanıklaştırmak | ayrımı zorlaştırmak |

### A5. Bürokratik bağlaç ve edat öbekleri
Neden iz: Kocagül 2026: cümle başı söylem belirleyicisi AI'da %83.9, insanda %25.9. Bu öbekler sıklık listelerinin ilk 50'sinde yok.
Regex (cümle başı): `(?:^|[.!?]\s+)(?:Bu bağlamda|Bu çerçevede|Bu doğrultuda|Öte yandan|Bununla birlikte|Bunun yanı sıra|Ayrıca|Ek olarak|Dolayısıyla|Öncelikle|Sonuç olarak|Bu noktada|Söz konusu)\b`
Regex (ek öbek): `\b\w+(?:kapsamında|çerçevesinde|doğrultusunda|bağlamında|noktasında|sürecinde)\b` ve `\b\w+[ae] (?:yönelik|ilişkin|dair)\b`
FP: Orta. Hukuki-idari metinde normal. Eşik: metin başına ≥3 farklı öbek, ya da cümle başı oranı > %20.

| # | Klişe | Sade alternatif |
|---|---|---|
| 126 | Bu bağlamda | Bu yüzden / (sil) |
| 127 | Bu çerçevede | Bu yüzden / Burada |
| 128 | Bu doğrultuda | Buna göre |
| 129 | Öte yandan | Ama / Oysa |
| 130 | Bununla birlikte | Yine de / Ama |
| 131 | Bunun yanı sıra | Ayrıca / -de |
| 132 | Ek olarak | Bir de |
| 133 | Dolayısıyla (her paragraf) | Bu yüzden / (sil) |
| 134 | Söz konusu X | Bu X |
| 135 | X kapsamında | X'te, X için |
| 136 | X çerçevesinde | X'e göre |
| 137 | X doğrultusunda | X'e göre |
| 138 | X noktasında | X'te, X konusunda |
| 139 | X'e yönelik olarak | X için |
| 140 | X'e ilişkin | X ile ilgili, X'in |
| 141 | X sürecinde | X'te, X sırasında |
| 142 | neticesinde | sonunda, sonucunda |
| 143 | itibarıyla | -den beri, itibaren |
| 144 | Bu noktada şunu belirtmek gerekir ki | (sil) |
| 145 | Genel olarak bakıldığında | Genelde |

### A6. Açılış kalıpları
Neden iz: Konu ne olursa olsun çağ/dünya tespitiyle girme.
Regex: `^(?:Günümüzde|Günümüz dünyasında|Dijital çağda|Dijitalleşen dünyada|Teknolojinin hızla geliştiği|Hızla değişen|Son yıllarda|Hepimizin bildiği gibi|Bilindiği üzere)\b` (ilk cümle; `re.M` ile paragraf başı da)
FP: Düşük (ilk cümlede). Haber metninde "Son yıllarda" + somut sayı normaldir.

| # | Klişe | Sade alternatif |
|---|---|---|
| 146 | Günümüzde ... | (sil, doğrudan konuya gir) |
| 147 | Günümüzün hızla değişen dünyasında | (sil) |
| 148 | Teknolojinin baş döndürücü hızla geliştiği çağımızda | (sil) |
| 149 | Dijitalleşen dünyada | İnternette / (sil) |
| 150 | Hepimizin bildiği gibi | (sil) |
| 151 | Bilindiği üzere | (sil) |
| 152 | Bu yazıda X'i ele alacağız | (sil, X'i anlatmaya başla) |
| 153 | Gelin birlikte inceleyelim | (sil) |
| 154 | X'in derinliklerine dalalım | (sil) |
| 155 | İşte bilmeniz gereken her şey | (sil) |
| 156 | Lafı uzatmadan | (sil) |
| 157 | Hadi başlayalım / Hadi konuya girelim | (sil) |

### A7. Kapanış kalıpları
Neden iz: Kocagül: cümle başı "Sonuç" AI %83.9 / insan %7.2. Özet tekrarı ve motivasyon cümlesi.
Regex (son paragraf): `(?:^|[.!?]\s+)(?:Sonuç olarak|Sonuçta|Özetle|Kısacası|Uzun lafın kısası|Velhasıl|Netice itibarıyla|Tüm bunlar göz önüne alındığında)\b`
FP: Orta. Akademik makalenin "Sonuç" başlığı muaf; başlık satırlarını hariç tut.

| # | Klişe | Sade alternatif |
|---|---|---|
| 158 | Sonuç olarak, ... | (son cümleyi yeni bilgiyle bitir) |
| 159 | Özetle | (özeti sil) |
| 160 | Tüm bunlar göz önüne alındığında | Bu yüzden |
| 161 | Gelecek parlak görünüyor | (sil, ya da somut beklenti) |
| 162 | Siz de bu dönüşümün bir parçası olun | (sil) |
| 163 | Unutmayın, başarı bir gecede gelmez | (sil) |
| 164 | Her yolculuk tek bir adımla başlar | (sil) |
| 165 | Belki de asıl mesele ... | (sil) |
| 166 | Peki ya siz? / Siz ne düşünüyorsunuz? | (blog'da kalabilir, değilse sil) |

### A8. Dolgu ve vurgu kalıpları
Neden iz: Cümleye bilgi eklemeyen vurgu. bushrabeg eşik: ≥2.
Regex: `\b(?:Önemle belirtmek gerekir ki|Şunu belirtmek önemlidir|Unutulmamalıdır ki|Unutmayın ki|Belirtmek gerekir ki|Dikkat edilmesi gereken bir diğer husus|tam da|tam anlamıyla|gerçek anlamda|gerçekten de|esasen|nihayetinde|bir bakıma|işte tam da bu yüzden)\b`
FP: Orta. Konuşma dilinde "gerçekten de" doğal; tek kullanım cezalandırılmamalı.

| # | Klişe | Sade alternatif |
|---|---|---|
| 167 | Önemle belirtmek gerekir ki | (sil) |
| 168 | Unutulmamalıdır ki | (sil) |
| 169 | İşte tam da bu yüzden | Bu yüzden |
| 170 | gerçek anlamda / tam anlamıyla | (sil) |
| 171 | esasen / nihayetinde | (sil) / sonunda |
| 172 | Bu noktada şunu söylemek mümkün | (sil) |
| 173 | Kesin olan tek şey şudur: | (sil, cümleyi doğrudan kur) |

---

## B. Çeviri kalıpları (calque) ve çeviri kokusu

Her biri İngilizce bir kaynaktan doğrudan geçmiş. Hem çeviri metinlerde hem LLM çıktısında yaygın. Ağırlık: yüksek (sert iz), çünkü doğal Türkçe korpusta seyrek.

| # | Kalıp | Kaynak | Neden iz | Regex | FP | Önce → Sonra |
|---|---|---|---|---|---|---|
| B1 | günün sonunda | at the end of the day | Aşut 2024 (BirGün) çeviri söylem olarak listeliyor | `\bgünün sonunda\b` | Orta: gerçek "akşam" anlamı. Fiil zamanı/saat bağlamı varsa muaf. | "Günün sonunda önemli olan müşteri memnuniyeti." → "Sonuçta önemli olan müşterinin memnun kalması." |
| B2 | masaya getirmek | bring to the table | Türkçede "katkı", "getirmek" yeter | `\bmasaya (?:getir|koy)\w*` | Düşük | "Ekibe masaya getirdiği deneyim" → "Ekibe kattığı deneyim" |
| B3 | oyunun kurallarını değiştiren | game-changer | A1 | `\boyunun kurallarını değiştir\w*` | Düşük (spor haberi hariç) | "Oyunun kurallarını değiştiren bir özellik" → "Ödeme süresini yarıya indiren bir özellik" |
| B4 | -e sahip olmak | have / possess | "Ev sahibi" dışında Türkçe "-li/-sı var" der | `\b\w+[ae] sahip(?:tir|tır|tirler| olan| olmak\w*| olduğu\w*)\b` | Orta: hukukta "hakka sahip" yerleşik. | "Şirket 200 çalışana sahiptir." → "Şirketin 200 çalışanı var." |
| B5 | tarafından edilgen | by-passive | Türkçe failli edilgeni seyrek kullanır; özne etken olur | `\btarafından\b` (sayım; 100 kelimede ≥1.5) | Orta: haber ve hukuk normal | "Rapor ekip tarafından hazırlandı." → "Raporu ekip hazırladı." |
| B6 | bir X olarak | as a X | "Bir yazılımcı olarak düşünüyorum ki" | `\b(?:bir )?\w+ olarak,? (?:ben|biz|düşünüyorum|söyleyebilirim)` ve genel `\bolarak\b` yoğunluğu | Orta: "olarak" Türkçede doğal; yoğunluk >1.5/100 kelime iz | "Bir uzman olarak şunu söyleyebilirim" → "Yıllardır bu işi yapıyorum, şunu gördüm" |
| B7 | için aşırı kullanımı | for / in order to | "-mek için" her amacı taşıyor; Türkçe "-e", "-meye", "diye" de kullanır | `\biçin\b` (100 kelimede ≥3) | Yüksek; sadece yoğunluk | "Hızlı olmak için önbellek kullanıyoruz" → "Önbellek kullanıyoruz, hızlansın diye" |
| B8 | hafif fiil yapmak/etmek | make/do + N | "karar yapmak", "hata yapmak" doğal; "bir değişiklik yapmak" yerine "değiştirmek" | `\bbir \w+ (?:yap|gerçekleştir)\w*` | Orta | "Kodda bir güncelleme yaptık" → "Kodu güncelledik" |
| B9 | -ebilmek kaçamağı | can/may hedging | Her yargıyı olasılığa çevirme | `\b\w+(?:abil|ebil)\w*(?:ir|ır|ur|ür)\b` yoğunluğu, `olabilir` ≥3/paragraf | Orta | "Bu durum sorunlara yol açabilir ve performansı etkileyebilir." → "Bu, sayfayı yavaşlatıyor." |
| B10 | ve zinciri | A, B, and C / and-chaining | Türkçe virgül ve zarf-fiille bağlar; "ve" cümlede 2+ kez iz | `(?:\bve\b.*?){3,}` (cümle içi) | Orta | "Hızlı ve güvenli ve ölçeklenebilir ve kolay" → "Hızlı, güvenli, büyüyebilir; kurması da kolay" |
| B11 | tamlama zinciri | of-of-of | 3+ isim tamlaması: "projenin geliştirme sürecinin yönetiminin" | `\b\w+(?:nın|nin|nun|nün|ın|in|un|ün) \w+(?:nın|nin|nun|nün|ın|in|un|ün|sı|si|su|sü|ı|i|u|ü)\w* \w+(?:nın|nin|nun|nün|ın|in|un|ün)\b` | Orta-yüksek (morfolojik regex kaba) | "Sistemin performansının iyileştirilmesinin önemi" → "Sistemi hızlandırmak önemli" |
| B12 | bu, ... anlamına gelir | this means | İngilizce "This means that" | `\b(?:Bu|bu),? (?:da )?\w+.{0,40}anlamına gel\w*` | Düşük-orta | "Bu, maliyetlerin düşeceği anlamına gelir." → "Böylece maliyet düşer." |
| B13 | Sadece X değil, aynı zamanda Y | not only... but also | bushrabeg: tek kullanımda bayrak | `\b(?:sadece|yalnızca|salt|yalnız)\b.{0,60}\bdeğil\w*,?.{0,40}\b(?:aynı zamanda|de|da)\b` | Düşük | "Sadece hızlı değil, aynı zamanda güvenli." → "Hızlı, üstelik güvenli." |
| B14 | Umarım bu e-posta sizi iyi bulur | I hope this email finds you well | hidengpt | `\bsizi iyi bul\w*` | Çok düşük | → "Merhaba Ayşe Hanım," |
| B15 | ... çekinmeyin | don't hesitate to | hidengpt | `\bçekinmeyin\b` | Düşük | "Sorularınız için benimle iletişime geçmekten çekinmeyin." → "Sorunuz olursa yazın." |
| B16 | dört gözle bekliyorum | I look forward to | Türkçe deyim ama e-posta kapanışında çeviri kokar | `\bdört gözle bekl\w*` | Orta | → "Görüşmek üzere." |
| B17 | X'in bir kanıtıdır | is a testament to | Pangram TR | `\bbir kanıtı(?:dır)?\b` | Düşük | "Bu başarı ekibin özverisinin bir kanıtıdır." → "Ekip haftalarca hafta sonu çalıştı." |
| B18 | -den emin olun | make sure | | `\b\w+(?:dan|den|tan|ten) emin olun\b` | Orta | "Kaydettiğinizden emin olun." → "Kaydetmeyi unutmayın." |
| B19 | X'in önemini vurgular | underscores the importance | | `\bönemini (?:vurgula|ortaya koy)\w*` | Düşük | → (sil) |
| B20 | hissetmeden edemem / merak etmeden edemem | can't help but | Pangram TR | `\b\w+madan edeme\w*` | Düşük | → "Merak ediyorum" |
| B21 | Nasıl gidiyor? / Üzgünüm (sorry) | how's it going / I'm sorry | Milliyet Blog | `\bÜzgünüm\b` (özür bağlamı) | Orta | "Üzgünüm, bunu yapamam." → "Kusura bakmayın, bunu yapamıyorum." |
| B22 | Sıkıntı yok | no problem | Aşut 2024 | `\bsıkıntı yok\b` | Yüksek (konuşma dilinde yerleşti) | bilgi amaçlı, düşük ağırlık |
| B23 | karşılaşmak (encounter) her bağlamda | encounter | | yoğunluk | Yüksek | — |
| B24 | X ya da Y olsan da | whether you're X or Y | Pangram TR | `\b\w+ (?:ya da|veya) \w+ ol(?:sanız|san) da\b` | Düşük | "İster yeni başlayan ister uzman olun" → (hedef kitleyi tek cümlede söyle) |
| B25 | Kendinize şu soruyu sorun | ask yourself | insanca §16 | `\bkendinize (?:şu )?soru\w* sor\w*` | Düşük | → (soruyu doğrudan yaz) |
| B26 | işte bu kadar | that's it | insanca §16 | `\bişte bu kadar\b` | Orta | → (sil) |
| B27 | daha fazlası için | for more | | `\bdaha fazlası için\b` | Orta | → "Ayrıntı: [link]" |
| B28 | gereksiz özne zamiri | pro-drop ihlali | Türkçe öznesiz cümle kurar; "Ben düşünüyorum ki", "Biz inanıyoruz ki" | `(?:^|[.!?]\s+)(?:Ben|Biz|Sen|Siz|O) \w+(?:um|üm|ım|im|uz|üz|ız|iz)\b` | Orta: vurgu amaçlı zamir doğal | "Biz bu konuda çok çalıştık. Biz inanıyoruz ki..." → "Bu konuda çok çalıştık. İnanıyoruz ki..." |
| B29 | gereksiz "bir" (a/an) | indefinite article | İngilizce a/an'ın birebir aktarımı | `\bbir (?:şekilde|biçimde|hale|durumda)\b` + `bir` yoğunluğu >4/100 kelime | Orta | "Bu, önemli bir konudur." → "Bu konu önemli." |
| B30 | pleonazm | çeviri hataları | DergiPark TV çevirisi | `\b(?:sahil kıyısı|defalarca kez|birlikte paylaş\w*|geri iade\w*|en optimum|ruhsat evrakı|tekrar yeniden)\b` | Çok düşük | "Birlikte paylaştık" → "Paylaştık" |

---

## C. Biçimbilimsel ve sözdizimsel izler

### C1. -mAktAdIr yığılması
Neden iz: Haber/akademik dilin şimdiki zaman + kesinlik eki. LLM bunu blog, e-posta ve sohbet metnine de taşıyor. Satır sonu kafiyesi oluşuyor (insanca §13).
Regex: `\b\w+(?:makta|mekte)(?:dır|dir|dırlar|dirler)\b`. Oran = eşleşen cümle / toplam cümle.
Eşik: Blog/e-posta'da >%15; akademikte >%45 (bushrabeg: doğal akademik ~%20-25). Paragrafta ≥4 ise sert.
FP: Yüksek akademik/hukukta. Register tespiti olmadan ağır ceza verme.
Önce: "Yapay zeka sağlık alanında yaygınlaşmaktadır. Doktorlar teşhis için kullanmaktadır. Hastalar da faydalanmaktadır."
Sonra: "Yapay zekâ hastanelere hızla girdi. Doktorlar teşhiste kullanıyor, hastalar da sonuçlarını daha erken alıyor."

### C2. -mIştIr yığılması ve kesinlik -DIr
Neden iz: "-mıştır" (geçmiş + kesinlik) ve isim cümlesinde "-dır" her cümlede. Konuşma ve blogda "-dı/-dır"sız hal doğal.
Regex: `\b\w+(?:mış|miş|muş|müş)(?:tır|tir|tur|tür)\b`; `\b\w+(?:dır|dir|dur|dür|tır|tir|tur|tür)[.!?]` (cümle sonu).
Eşik: Cümle sonlarının >%50'si -DIr ise ve register blog/e-posta ise.
FP: Yüksek akademik registerda.
Önce: "Bu yöntem etkilidir. Uygulaması kolaydır. Maliyeti düşüktür."
Sonra: "Yöntem işe yarıyor, uygulaması kolay ve ucuz."

### C3. -ArAk zarf-fiil zinciri ("yüzeysel -arak kuyruğu")
Neden iz: Kocagül: AI %82.1 / insan %32.2. Cümle sonuna "...katkıda bulunarak", "...ortaya koyarak" eklemek anlam katmadan cümleyi uzatır (insanca §3).
Regex: `\b\w+(?:arak|erek)\b`; özel: `\b(?:katkıda bulunarak|ortaya koyarak|gözler önüne serere?k|yansıtarak|altını çizerek|ışık tutarak|pekiştirerek|vurgulayarak)\b`
Eşik: Cümlelerin >%15'inde -ArAk; özel listede tek eşleşme bile orta ağırlık.
FP: Orta. "Koşarak geldi" gibi somut eylemler doğal; soyut fiil + -ArAk iz.
Önce: "Belediye yeni parkı açarak şehrin yeşil alanlarına katkıda bulunmuştur."
Sonra: "Belediye yeni bir park açtı. Şehrin yeşil alanı 3 dönüm arttı."

### C4. Tekdüze cümle uzunluğu ve SOV düzeni (burstiness)
Neden iz: AI cümleleri 15-22 kelimede kümelenir (Uzun 2024: 15-20), sapma düşük. Türkçe insan normu 9-11 ama sapma yüksek. Devrik cümle hiç yok; yüklem hep sonda.
Ölçüm: Cümle uzunlukları (kelime) için ortalama μ ve standart sapma σ. CV=σ/μ.
Eşik: CV < 0.30 ve μ ≥ 18 → iz (bushrabeg: SD <%30 ve ort. 22+, ya da hiç <8 kelimelik cümle yok). En kısa cümle ≥8 kelime ise ek puan.
Devrik cümle tespiti (kaba): cümle sonu çekimli fiil değilse ve sonrası tek isim öbeği (`\b\w+(?:dı|di|du|dü|yor|acak|ecek)\w*,? \w+(?:ı|i|u|ü|ım|im)?[.!?]$`). Yokluk zayıf sinyal.
FP: Hukuki metin tekdüzedir. Kısa metinde (<5 cümle) ölçme.
Önce: Beş cümle, her biri 18-21 kelime.
Sonra: "Kurulum on dakika sürdü. Sorun yapılandırmadaydı: ortam değişkeni eksikti, uygulama da sessizce varsayılana dönüyordu. Ekledik. Çalıştı."

### C5. Adlaştırma (nominalization)
Neden iz: Fiil yerine "-mA/-mAk/-Iş + sı + gerçekleştirilmesi". "Kararın verilmesinin ardından" yerine "Karar verilince".
Regex: `\b\w+(?:ılması|ilmesi|ulması|ülmesi|nması|nmesi)(?:nın|nin|na|ne|nı|ni)?\b` yoğunluğu (100 kelimede >3).
FP: Akademik/hukukta yüksek.
Önce: "Verilerin analiz edilmesinin ardından sonuçların raporlanması gerçekleştirilecektir."
Sonra: "Verileri inceledikten sonra sonuçları raporlayacağız."

### C6. "olarak" aşırı kullanımı
Neden iz: "as" ve "-ly" karşılığı ("hızlı olarak", "genel olarak", "sonuç olarak", "X olarak hizmet").
Regex: `\bolarak\b` yoğunluğu (>1.5/100 kelime); özel: `\b(?:genel|sonuç|temel|ilk|aktif|etkin) olarak\b`.
FP: Orta.
Önce: "Sistem aktif olarak kullanılmakta olup temel olarak üç modülden oluşmaktadır."
Sonra: "Sistem kullanımda, üç modülden oluşuyor."

### C7. Gereksiz faceless edilgen
Neden iz: "gerekmektedir, söylenebilir, düşünülmektedir, değerlendirilmektedir, göz ardı edilmemelidir". Özneyi gizler (insanca §18).
Regex: `\b\w+(?:ıl|il|ul|ül|ın|in|un|ün)(?:makta|mekte|abil|ebil|ma|me)\w*(?:dır|dir|ir|ır)\b` + `\bgerekmektedir\b`.
FP: Akademik yöntem bölümü.
Önce: "Bu konunun dikkatle değerlendirilmesi gerekmektedir."
Sonra: "Bu konuya dikkatle bakmalıyız."

### C8. Üçlüler (triads)
Neden iz: Her sayıma üç öğe: "hızlı, güvenli ve ölçeklenebilir". Üçleme kuralı (rule of three) RLHF eğilimi.
Regex: `\b\w+, \w+ ve \w+\b` (sıfat/isim üçlüsü); paragraf başına sayım, ≥2 üçlü → iz.
FP: Orta-yüksek; doğal sayımlar da üçlü olabilir. Yalnızca yoğunluk.
Önce: "Ekibimiz yaratıcı, dinamik ve çözüm odaklıdır."
Sonra: "Ekip, müşteri şikayetlerini ortalama iki saatte çözüyor."

### C9. "X değil, Y" ve türevleri
Neden iz: insanca §9 "Mesele X değil Y". Karşıtlık iskeleti. Varyantlar: "...den öte, bir ...", "Bu bir X değil, bir Y", üçlü ret "Ne hız. Ne fiyat. Sadece güven."
Regex: `\b(?:Mesele|Sorun|Konu|Asıl mesele|Bu)\b.{0,50}\bdeğil\w*,.{0,50}` ; `\b\w+(?:dan|den|tan|ten) öte,? bir\b` ; `(?:^|[.]\s+)Ne \w+\. Ne \w+\.`
Eşik: Metinde "değil" >3 ve bunların ≥2'si karşıtlık kalıbında → iz. Tek kullanım düşük ağırlık.
FP: Orta; gerçek düzeltme cümleleri.
Önce: "Bu bir yazılım değil, bir yaşam biçimi."
Sonra: "Bu yazılımı her gün kullanıyoruz; yerine koyacak bir şey bulamadık."

### C10. Retorik soru + cevap ve iki nokta ifşası
Neden iz: "Peki bu ne anlama geliyor?", "Peki neden?", "Sonuç mu?", "Cevap basit:", "Sorun şu:" (insanca §27, §46).
Regex: `(?:^|[.!?]\s+)Peki(?:,)? [^?]{0,60}\?` ; `\b(?:Cevap|Sorun|Mesele|Gerçek|İşin aslı|Sır|Formül) (?:basit|şu|şudur)\s*:` ; `\b\w+ mi\?\s+[A-ZÇĞİÖŞÜ]` (soru → hemen cevap)
Eşik: İki nokta ifşası 1000 kelimede >1-2; retorik soru 500 kelimede >1.
FP: Düşük-orta; konuşma dilinde doğal ama tekrar iz.
Önce: "Peki bu ne anlama geliyor? Cevap basit: maliyet düşüyor."
Sonra: "Kısacası maliyet düşüyor." ya da daha iyisi: "Aylık fatura 40 bin liradan 28 bine indi."

### C11. Noktalı virgül ve virgül yoğunluğu (Türkçeye özgü)
Neden iz: Kocagül: noktalı virgül AI %76.8 / insan %15.2; yüksek virgül yoğunluğu %82.1 / %20.5. Pangram'ın İngilizce gözlemi ("AI noktalı virgül kullanmaz") Türkçe için **ters**.
Regex: `;` sayısı; virgül/cümle oranı.
Eşik: Blog/e-posta'da 300 kelimede ≥1 noktalı virgül → orta ağırlık. Virgül/cümle > 2.5 → zayıf.
FP: Akademik/hukuki metinde noktalı virgül doğal. bushrabeg'in "mutlak yasak"ı abartılı; TDK noktalı virgülü yasaklamıyor. **Yasak değil, yoğunluk.**
Önce: "Sistem hızlı; ancak pahalı; üstelik bakımı zor."
Sonra: "Sistem hızlı ama pahalı. Bakımı da zor."

### C12. Uzun tire (em dash) ve kısa tire (en dash)
Neden iz: Türkçe yazımda uzun tire nadirdir (TDK'de konuşma çizgisi/ara söz için var ama gündelik metinde yok). İngilizce LLM alışkanlığı.
Regex: `[—–]` ; ayrıca ` - ` (boşluklu kısa çizgi ara söz olarak).
Eşik: Herhangi bir uzun tire → orta-yüksek ağırlık (insanca: sıfır tolerans).
FP: Edebi metinde diyalog çizgisi (`^—`) muaf. Sayı aralığı `\d–\d` muaf.
Önce: "Bu araç — ki çok popüler — her şeyi değiştirdi."
Sonra: "Bu araç çok popüler ve birçok şeyi değiştirdi."

### C13. Biçimlendirme izleri
| İz | Regex | FP | Not |
|---|---|---|---|
| Kalın etiketli madde: `- **Başlık:** açıklama` | `^\s*[-*•]\s+\*\*[^*]+\*\*\s*[:：]` | Teknik dokümanda normal | Düzyazı istenen yerde sert iz |
| Kalın vurgu yoğunluğu | `\*\*[^*]+\*\*` 100 kelimede >1 | Doküman | WhatsApp/e-postaya yapışmış `**` sert iz (hidengpt) |
| Başlıkta Title Case | `^#{1,6} (?:\S+ ){1,}` içinde ≥2 büyük harfle başlayan ve "ve/ile/için/de/da/ki" dahil büyük | Özel isimler | TDK: başlıkta bağlaçlar küçük ("Ve" yanlış). Regex: `^#{1,6} .*\b(?:Ve|İle|İçin|Veya|Ya Da)\b` |
| Emoji başlık/madde | `^#{1,6}\s*[\U0001F300-\U0001FAFF☀-➿]` ve `^\s*[-*]\s*[\U0001F300-\U0001FAFF]` | Sosyal medya | Kurumsal metinde sert |
| Gereksiz başlık bölme | kısa metinde (<300 kelime) ≥3 başlık | — | Kocagül: çok paragraf AI %53.6 / insan %2.7 |
| Eğik/slash ayırıcı | `\b\w+/\w+\b` (tarih ve URL hariç) ≥2 | Teknik | "kullanıcı/müşteri" (bushrabeg) |
| Parantez içi açıklama takıntısı | `\([^)]{3,40}\)` 100 kelimede >2 | Akademik | insanca §31 |
| Tırnak yoğunluğu | `["“”«»]` | Alıntı yapan metin | Kocagül: AI %42.9 / insan %8.9 |

### C14. Eş anlamlı döndürme ve tersi
Neden iz: Aynı varlığa paragrafta 3+ farklı ad ("şirket, firma, kuruluş, marka"). Tersi: aynı sözcüğün takıntılı tekrarı (insanca §12).
Ölçüm: Önceden tanımlı eş anlam kümeleri (şirket/firma/kuruluş/işletme; kullanıcı/müşteri/tüketici; yöntem/yaklaşım/strateji/metot). Paragrafta kümeden ≥3 farklı üye → iz.
FP: Orta.

### C15. Ödünleme kalıbı "-sA dA ... aslında ... göstergesidir"
Neden iz: UÜFEFSBD makalesindeki GPT-4 örneği. Klişe denge cümlesi.
Regex: `\b\w+(?:sa|se) da\b.{0,60}\baslında\b.{0,60}\b(?:göstergesi|işareti|fırsatı)\w*`
FP: Düşük.
Önce: "Değişim, kimi zaman korkutucu olsa da, aslında büyümenin bir göstergesidir."
Sonra: "Değişim korkutuyor. Ama geçen yıl ekibi değiştirmesek bu projeyi bitiremezdik."

### C16. Sahte aralık "X'ten Y'ye"
Neden iz: "Sağlıktan eğitime, finanstan ulaşıma" gibi gerçek bir ölçek belirtmeyen sayım (insanca §11, chatday).
Regex: `\b\w+(?:dan|den|tan|ten) \w+(?:a|e|ya|ye)(?:,| kadar)` iki kez art arda.
FP: Gerçek aralıklar (tarih, sayı, coğrafya). Rakam içeriyorsa muaf.
Önce: "Sağlıktan eğitime, finanstan ulaşıma kadar pek çok alanda kullanılıyor."
Sonra: "Hastanelerde randevu planlamasında ve bankalarda dolandırıcılık tespitinde kullanılıyor."

### C17. Tekdüze deyim/ikileme (Bergin & Atasoy)
Neden iz: AI deyimi çok kullanıyor ama hep aynılarını (1.038 kullanım / 107 tür). İkileme 68 kullanım / 10 tür.
Ölçüm: Bilinen deyim ve ikileme listesi (ör. "göz ardı etmek", "yer almak", "ön plana çıkmak", "adım atmak", "el ele vermek", "ilk adım", "yavaş yavaş", "adım adım", "gün geçtikçe"). Aynı deyim/ikileme metinde ≥2 → iz.
FP: Düşük.

---

## D. Ton izleri

| # | İz | Neden | Regex | FP | Önce → Sonra |
|---|---|---|---|---|---|
| D1 | Dalkavukluk | RLHF onay eğilimi | `\b(?:Harika|Mükemmel|Çok güzel|Ne güzel) bir (?:soru|nokta|fikir|gözlem)\b`, `\bKesinlikle haklısınız\b`, `\bÇok yerinde bir\b` | Çok düşük (metin başında) | "Harika bir soru! Bu konu..." → "Bu konu..." |
| D2 | Terapist modu | Güvenlik ayarı empati şablonu | `\bYalnız değilsiniz\b`, `\bBunu hissetmeniz (?:çok )?normal\b`, `\bKendinize (?:karşı )?nazik olun\b`, `\bduygularınız geçerli\b` | Gerçek destek metni | → (somut öneriye geç) |
| D3 | Aşırı kaçamak (hedging) | Sorumluluktan kaçış | `\b(?:muhtemelen|büyük olasılıkla|bir ölçüde|belli ölçüde|kısmen|genellikle|çoğu zaman)\b` + `-ebilir` yoğunluğu; cümlede ≥2 kaçamak | Bilimsel temkin | "Bu yaklaşım bazı durumlarda belli ölçüde faydalı olabilir." → "Bu yaklaşım küçük veri setlerinde işe yarıyor." |
| D4 | Bilgi sınırı ifadeleri | Model belirsizliği | `\beldeki bilgilere göre\b`, `\bkamuya açık kaynaklarda\b`, `\bbilgi kesme tarihim\b`, `\bolduğu düşünülmektedir\b` | Düşük | → (kaynak ver ya da sil) |
| D5 | Belirsiz otorite | Kaynaksız iddia | `\b(?:Uzmanlar|Araştırmalar|Bilim insanları|Kimi çevreler)\b.{0,30}\b(?:belirtiyor|gösteriyor|vurguluyor|göstermektedir)\b`, `\bgenel kanı\b` | Kaynak/atıf varsa muaf (yakında `\(\w+,? \d{4}\)` veya link) | "Araştırmalar, uykunun önemli olduğunu gösteriyor." → "Walker'ın 2017 kitabına göre 6 saatin altında uyuyanlarda..." |
| D6 | Motivasyonlu kapanış | Pazarlama şablonu | `\b(?:Unutmayın|Hatırlayın)\b,?`, `\bsiz de .{0,30}(?:olun|başlayın|katılın)\b`, `\bhayallerinizin peşinden\b` | Reklam metni | → (sil) |
| D7 | Sahte derinlik / aforizma | Boş genel geçer | `\b\w+,? \w+(?:nın|nin|nun|nün|ın|in) dilidir\b`, `\bbir yaşam biçimidir\b`, `\bbaşarının anahtarı\b`, `\bher şey \w+ ile başlar\b`, `\bbazen en büyük\b` | Edebi | "Sabır, başarının dilidir." → (sil) |
| D8 | Sahte samimiyet | Doğallık taklidi | `\b(?:Dürüst olmak gerekirse|Açık konuşalım|İşin aslı şu|Gerçek şu ki|Açıkçası)\b` | Konuşma dilinde doğal; tekrar iz | → (sil) |
| D9 | Boş doğrular | Herkesin bildiği | `\b(?:güven zamanla inşa edilir|iletişim her ilişkinin temelidir|başarı bir gecede gelmez|her yolculuk .{0,20}adımla başlar)\b` | Çok düşük | → (sil) |
| D10 | Uydurma vaka | Sahte örnek kişi | `\b(?:Ayşe|Mehmet|Ahmet|Zeynep) (?:Hanım|Bey)\b.{0,80}\b\d+ (?:günde|ayda|haftada)\b` | Gerçek vaka | Uyarı: humanizer sahte isim/sayı **eklememeli** |
| D11 | Register kayması | Zorla argo + -maktadır | `\b(?:kanka|valla|yani abi|resmen)\b` ile aynı paragrafta `-maktadır` | Düşük | → tek registerda kal |
| D12 | Broşür dili | Turizm/pazarlama şablonu | `\b(?:keşfetmeye hazır olun|sizi bekliyor|kendinizi .{0,20} bırakın|dünyasına adım atın)\b` | Reklam | "Eşsiz manzarasıyla sizi bekliyor" → "Tepeden körfez görünüyor." |

---

## E. Sohbet botu artıkları (chatbot artifacts)

En yüksek ağırlık (sert iz). Tek eşleşme yeterli. FP neredeyse yok (yalnızca AI'dan alıntı yapan metinler).

| # | Artık | Regex |
|---|---|---|
| E1 | Umarım yardımcı olur / Umarım faydalı olmuştur | `\bUmarım (?:bu )?(?:yardımcı|faydalı|işinize yarar)\w*` |
| E2 | Başka sorunuz olursa çekinmeyin | `\b(?:Başka|Ek) (?:bir )?soru\w* (?:olursa|varsa)\b` |
| E3 | Dilerseniz ... açıklayabilirim / Devam edeyim mi? | `\bDilerseniz\b.{0,60}\b\w+(?:abilirim|ebilirim)\b`, `\b(?:Devam edeyim mi|İster misiniz|Size .{0,20} hazırlayabilirim)\b` |
| E4 | Elbette! / Tabii ki! / Kesinlikle! (metin başında) | `^(?:Elbette|Tabii ki|Tabii|Kesinlikle|Memnuniyetle)[!,.]` |
| E5 | İşte X hakkında bilgiler / İşte size ... | `^İşte\b.{0,60}(?::|\.)$` |
| E6 | Bir yapay zeka (dil modeli) olarak | `\bbir yapay zek[aâ] (?:dil modeli |asistanı )?olarak\b` |
| E7 | Bilgi kesme tarihi | `\b(?:bilgi kesme|eğitim verilerim|son güncellemem)\b` |
| E8 | Regenerate response / Yanıtı yeniden oluştur | `\b(?:Regenerate response|Yanıtı yeniden oluştur|Copy code|Kodu kopyala)\b` |
| E9 | Yer tutucular | `\[(?:Adınız|Şirket Adı|İsim|Tarih|X)\]`, `\{\{?\w+\}?\}` |
| E10 | Markdown kalıntısı düz metinde | `\*\*[^*]+\*\*`, `^#{1,6} ` (e-posta/mesaj registerında) |
| E11 | Bu yazıda / Bu yanıtta ... ele alacağız | `\bBu (?:yazıda|yanıtta|makalede)\b.{0,40}\b(?:ele alacağız|inceleyeceğiz|değineceğiz)\b` |
| E12 | Özet sandviçi | Giriş paragrafı ve son paragraf arasında yüksek sözcük örtüşmesi (Jaccard >0.4) |
| E13 | "Not:" ya da "Önemli:" ile başlayan kalın uyarı | `^\s*\*\*(?:Not|Önemli|Uyarı)\*\*\s*:` |
| E14 | Aşağıda ... bulabilirsiniz | `\bAşağıda\b.{0,40}\bbulabilirsiniz\b` |

Önce: "Elbette! İşte Türkiye'nin en güzel 5 şehri hakkında bilgiler: ... Umarım yardımcı olur! Başka sorunuz olursa çekinmeyin."
Sonra: "Beş şehir öneriyorum: ..." (açılış ve kapanış silinir)

---

## F. Yanlış pozitif yönetimi ve register muafiyetleri

1. **Register tespiti önce.** Beş register: hukuki-idari, akademik-kurumsal, analitik-gazetecilik, deneme-blog, edebi-yaratıcı. Basit sezgi: -mAktAdIr oranı, atıf deseni `\(\w+,? \d{4}\)`, madde numarası `^\d+\.`, diyalog çizgisi, birinci tekil şahıs oranı.
2. **Muafiyet tablosu:**
   - Hukuki-idari: C1, C2, C5, C7, A5, B4 ("hakka sahip"), B5 eşikleri ×3.
   - Akademik: C1, C5, C7, C11 (noktalı virgül), A2 eşikleri ×2. D3 hedging normal.
   - Gazetecilik: B5 (tarafından) ×2, "Son yıllarda" + sayı muaf.
   - Edebi: C12'de diyalog çizgisi muaf, A4 mecazlar düşük ağırlık, devrik cümle beklenir.
   - Blog/e-posta: en sıkı eşikler.
3. **Tek eşleşme ceza değil.** E grubu hariç. Skor = Σ(ağırlık × eşleşme) / (kelime/100).
4. **Hatasızlık AI kanıtı değil**, hata eklemek humanizasyon değil. Humanizer yazım hatası üretmemeli.
5. **Tartışmalı kurallar** (bushrabeg'de mutlak, burada değil):
   - "ama/ancak" öncesi virgül: TDK yasaklamaz. Yalnızca yoğunluk.
   - Noktalı virgül: TDK'de geçerli. Ama Türkçe AI sinyali olarak güçlü (Kocagül). Yasak değil, blog'da yumuşat.
   - Bağlaçla başlayan cümle ("Ama", "Ve"): insanda daha sık (Kocagül: insan %31.3). Tersine humanizasyon tekniği olarak kullanılabilir.
   - Şapka (â, î, û) kaldırma: üslup tercihi, iz değil. Tutarsızlık (aynı metinde hem "hâlâ" hem "hala") zayıf iz.
6. **Aşırı düzeltme kokusu** (insanca §45): Humanizer çıktısında her paragrafta "Ama" ile başlayan cümle, zorla argo, yapay yazım hatası, her cümlede devrik yapı yeni bir iz olur. Linter kendi çıktısını da tarar.
7. **Turkish lowercasing**: `I→ı`, `İ→i`. Aksi halde "İşte" ve "Ilık" eşleşmeleri bozulur.

---

## G. Linter tasarım notları

### G1. Ağırlıklar (öneri)
| Seviye | Ağırlık | Gruplar |
|---|---|---|
| Sert (tek eşleşme yeter) | 5 | E1-E14, D1, B14, B15, B13, C12 (uzun tire, blog registerı) |
| Güçlü | 3 | A6, A7 cümle başı "Sonuç olarak", C3 özel -ArAk listesi, C9, C10, C15, B1-B3, B17, B19, B20, D7, D9 |
| Orta | 2 | A1, A3, A4, A5 cümle başı, C11 noktalı virgül, C13, D3, D5, D8 |
| Zayıf (yalnız yoğunlukla) | 1 | A2, B4-B11, B28, B29, C1, C2, C5, C6, C7, C8, C14, C17 |

### G2. Eşikler
- **Skor/100 kelime:** <2 temiz, 2-5 dikkat, >5 yeniden yaz. (hidengpt: 300 kelimede 6-7 örüntü + somut detay yok = şüpheli ≈ 2/100 kelime ham sayım.)
- **İstatistikler:** CV(cümle uzunluğu) < 0.30, μ ≥ 18; -mAktAdIr oranı > register eşiği; cümle başı bağlaç oranı > %20; -ArAk cümle oranı > %15; TTR (ilk 300 token) < register normu.
- **Somutluk çapası (negatif sinyal):** rakam `\d`, özel isim (cümle ortası büyük harf), tarih, birim. 100 kelimede 0 somut çapa ise skor ×1.3.
- **Ateşman:** Blog registerında < 40 ise uyarı.

### G3. Regex uygulama ipuçları
```python
import re
def tr_lower(s): return s.replace("I", "ı").replace("İ", "i").lower()
MEKTEDIR = re.compile(r"\b\w+(?:makta|mekte)d[ıi]r(?:lar|ler)?\b")
MISTIR   = re.compile(r"\b\w+m[ıiuü]şt[ıiuü]r\b")
ARAK     = re.compile(r"\b\w{2,}(?:arak|erek)\b")
DASH     = re.compile(r"[—–]")
NOTONLY  = re.compile(r"\b(?:sadece|yalnızca|salt)\b.{0,60}\bdeğil\w*,?.{0,40}\b(?:aynı zamanda|de|da)\b")
TITLECASE_CONJ = re.compile(r"^#{1,6} .*\b(?:Ve|İle|İçin|Veya)\b", re.M)
SENT_START_CONN = re.compile(r"(?:^|(?<=[.!?])\s+)(?:Bu bağlamda|Öte yandan|Bununla birlikte|Bunun yanı sıra|Ayrıca|Ek olarak|Dolayısıyla|Öncelikle|Sonuç olarak)\b", re.M)
```
- Cümle bölme: `(?<=[.!?…])\s+(?=[A-ZÇĞİÖŞÜ"“])` ; kısaltmalar (vb., vs., Dr., Prof., örn., bkz.) için istisna listesi şart.
- Kelime sayımı: `re.findall(r"\b[\wçğıöşüâîû'’]+\b", text)` ; kesme işaretiyle ayrılan ekleri ("İstanbul'da") tek kelime say.
- Kod blokları (```...```), satır içi kod, URL ve alıntı (`> `) tarama dışı.
- Hook için: PostToolUse (Write/Edit) sonrası yalnızca `.md`/`.txt` ve Türkçe oranı yüksek dosyalarda çalıştır (Türkçe tespiti: `[çğışöü]` karakter oranı > %3).

### G4. Yeniden yazım ilkeleri (skill için)
- Klişeyi silmek çoğu zaman eş anlamlısıyla değiştirmekten iyidir.
- Somut bilgi yoksa uydurma; kullanıcıdan iste ya da cümleyi kısalt.
- İnsan ritmi: kısa-uzun karışımı, ara sıra devrik cümle, yüklem düşürme (Kocagül: insan %20.5), virgülle bağlanan fiil zinciri, cümle başında "Ama/Çünkü/Aslında/Bence" (ölçülü), birinci çoğul şahıs.
- Deyim ve ikileme: sayıyı artırma, **çeşitliliği** artır (Bergin & Atasoy). 150-250 kelimede ≤1 deyim (insanca).
- Atıf merdiveni: isim → zamir → öznesiz cümle.

---

## H. Açık sorular

1. Kocagül 2026'nın Supplementary Table S1 (61 özelliğin tamamı) erişilebilirse eşikler kalibre edilmeli.
2. Claude'a özgü Türkçe izler (GPT'den farklı) için korpus yok. Öneri: aynı 50 istemle Claude/GPT/Gemini Türkçe çıktısı toplayıp n-gram farkı çıkarmak. Claude'un İngilizcedeki "genuinely", "I'd be happy to", em dash eğilimlerinin Türkçe karşılıkları ("gerçekten", "memnuniyetle", uzun tire) bu katalogda var ama Claude'a özgü frekans ölçülmedi.
3. Register sınıflandırıcısının deterministik doğruluğu bilinmiyor; küçük bir etiketli set (Bilkent Turkish Writings 9.119 AI öncesi deneme + hf `tum-nlp/neural-news-benchmark`) ile test edilmeli.
4. Noktalı virgül: Kocagül tartışmacı deneme korpusunda güçlü sinyal; teknik dokümantasyonda geçerliliği test edilmeli.

---

## Kaynaklar

- Kocagül, H. (2026). Detecting the Human in the Machine. https://doi.org/10.47777/cankujhss.1957142
- Bergin, B. & Atasoy, A. (2026). Söz Varlığı Unsurları Bağlamında Yapay Zekâ ve Öğrenci Metinleri. https://dergipark.org.tr/tr/pub/utoad/article/1805843
- Uzun, C. (2024). Some Determinations as to Whether or Not Academic Texts Are Produced by AI. https://doi.org/10.5772/intechopen.1007724
- Şimşek, P. H. & Özdemir, S. (2026). JLERE. https://dergipark.org.tr/en/pub/jlere/article/1858803
- Söz dizimi açısından ChatGPT'nin Türkçesine bir bakış. https://dergipark.org.tr/en/download/article-file/4293409
- Özdemir, O. (2026). arXiv:2602.13504. https://arxiv.org/abs/2602.13504
- TÜBİTAK Bilim Genç (2023). https://bilimgenc.tubitak.gov.tr/makale/bir-metni-chatgptnin-hazirladigi-anlasilabilir-mi
- Bezirci & Yılmaz, YOD okunabilirlik. https://dergipark.org.tr/tr/pub/deumffmd/issue/40831/492667
- Keklik & Yılmaz (2013), bağlaç sıklığı. https://dergipark.org.tr/tr/download/article-file/202242
- Ateşman okunabilirlik formülü (researchgate 380156427)
- Vikisözlük Türkçe sıklık listesi; TS Corpus; TNC
- hidengpt: https://hidengpt.com/tr/rehber/chatgpt-yazisi-nasil-anlasilir
- Pangram TR: https://www.pangram.com/tr/blog/comprehensive-guide-to-spotting-ai-writing-patterns , https://www.pangram.com/tr/signs-of-ai-writing
- assistin.ai AI yazım kalıpları rehberi; tezmakale.com ChatGPT ile yazılan tez; yapaytu.com ChatGPT Türkçe; hub.chatday.ai
- Aşut, A. (2024). Çeviri söylemler. https://www.birgun.net/makale/ceviri-soylemler-558960
- Milliyet Blog, Türkçe'nin yaraları; DergiPark TV çevirisi hataları (article-file/424284)
- RTÜK (2019) Doğru Türkçe raporu; Necmiye Alpay, Türkçe Sorunları Kılavuzu; AA Türkçeyi Doğru Kullan; Dragoman editör rehberi
- Prior art: github.com/bushrabeg/turkce-humanizer (SKILL.md v3.2), github.com/tahiryildiz/insanca (SKILL.md, references/kaynaklar.md)
- Wikipedia: Signs of AI writing (İngilizce; Türkçe Vikipedi'de karşılığı yok); EQ-Bench slop score; DAMAGE arXiv 2501.03437; tropes.fyi
