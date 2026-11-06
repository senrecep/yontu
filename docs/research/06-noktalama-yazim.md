# 06 — TDK yazım ve noktalama kuralları (linter/reviewer odaklı)

Kapsam: Türkçe "humanizer" linter'ı ve reviewer'ı için TDK yazım/noktalama kuralları. Her kural regex'e dönüştürülebilecek biçimde yazıldı. Kurallar TDK Yazım Kuralları sayfalarından özetlendi. Yazımlar TDK Güncel Türkçe Sözlük API'sinde (`https://sozluk.gov.tr/gts?ara=…`) doğrulandı. Tarih: 2026-11-05.

## 0. Kaynaklar (doğrulanmış URL'ler)

| Konu | URL |
|---|---|
| Noktalama işaretleri (tüm işaretler tek sayfada) | https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/ |
| İşaret listesi (glif tablosu) | https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-ve-diger-isaretler/ |
| Kesme işareti | https://tdk.gov.tr/icerik/yazim-kurallari/kesme-isareti/ |
| Bağlaç da/de | https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-da-denin-yazilisi/ |
| Bağlaç ki | https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-kinin-yazilisi/ |
| Soru eki mı/mi | https://tdk.gov.tr/icerik/yazim-kurallari/soru-eki-mi-mi-mu-munun-yazilisi/ |
| Bulunma eki -da/-de | https://tdk.gov.tr/icerik/yazim-kurallari/bulunma-durumu-eki-da-de-ta-tenin-yazilisi/ |
| ile | https://tdk.gov.tr/icerik/yazim-kurallari/ilenin-yazilisi/ |
| Ek fiil | https://tdk.gov.tr/icerik/yazim-kurallari/ek-fiilin-yazilisi/ |
| Büyük harfler | https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/ |
| Sayılar | https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/ |
| Kısaltmalar | https://tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar/ |
| Ayrı yazılan birleşik kelimeler | https://tdk.gov.tr/icerik/yazim-kurallari/ayri-yazilan-birlesik-kelimeler/ |
| Bitişik yazılan birleşik kelimeler | https://tdk.gov.tr/icerik/yazim-kurallari/bitisik-yazilan-birlesik-kelimeler/ |
| İkilemeler | https://tdk.gov.tr/icerik/yazim-kurallari/ikilemelerin-yazilisi/ |
| Pekiştirmeli sözler | https://tdk.gov.tr/icerik/yazim-kurallari/pekistirmeli-sozlerin-yazilisi/ |
| Düzeltme işareti | https://tdk.gov.tr/icerik/yazim-kurallari/duzeltme-isareti/ |
| Alıntı kelimeler | https://tdk.gov.tr/icerik/yazim-kurallari/alinti-kelimelerin-yazilisi/ |
| Fiil çekimi (-acak/-ecek a/e) | https://tdk.gov.tr/icerik/yazim-kurallari/fiil-cekimi-ile-ilgili-yazilislar/ |
| Simgeler | https://tdk.gov.tr/icerik/yazim-kurallari/simgeler/ |
| Sözlük API (yazım doğrulama) | https://sozluk.gov.tr/gts?ara=KELIME |

Not: Görevde geçen `.../de-da-baglaci/`, `.../ki-baglaci/` ve `.../virgul/` slug'ları **404** veriyor. Doğru slug'lar yukarıda. Noktalama için ayrı sayfa yok, hepsi `noktalama-isaretleri-aciklamalar` sayfasında. TDK ana sayfası (`/icerik/yazim-kurallari/`) da 404 döndürüyor, liste için WP API kullanılmalı.

Prior art (dikkatli kullanılmalı, bkz. §14):
- https://github.com/Denomas/Turkce-yazim-denetimi (Vale kuralları; **birkaç kuralı TDK'ya aykırı**)
- https://github.com/saidsurucu/turkce-imla-skill (Claude skill, `.skill` paketi)
- https://docs.rs/akana-core/latest/src/akana_core/grammar/orthography.rs.html (Rust; mi/de-da kontrolleri, iyi bir FP listesi var)

---

## 1. Kural şeması

Her kural şu alanlarla yazıldı: **id · seviye (error/warning/info) · TDK madde · regex · yanlış → doğru · FP riski**.

Regex'ler Python `re` sözdizimindedir. Uygulama notları için §15'e bakın (Türkçe I/İ sorunu, `\b`, kod bloklarını atlama). `'` aşağıda **hem `'` (U+0027) hem `’` (U+2019)** anlamına gelir; regex'te `['’]` yazıldı.

Sınıf kısaltmaları:
```
L  = [a-zçğıöşüâîû]           # küçük harf
U  = [A-ZÇĞİÖŞÜÂÎÛ]           # büyük harf
W  = [A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû]
AP = ['’]
```

---

## 2. Genel boşluk ve işaret kuralları

TDK: "nokta, virgül, noktalı virgül, iki nokta, üç nokta, soru, ünlem, tırnak, ayraç ve kesme işaretleri ait oldukları kelimelere bitişik olarak yazılır ve kesme dışındaki işaretlerden sonra bir harf boşluğu ara verilir."

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| SP-01 işaretten önce boşluk | error | `\s+([.,;:!?…])` | `geldi .` → `geldi.` | Fransızca metin; `: ` ile başlayan kod; Markdown tablo hücreleri; `?` bağımsız kullanımı (`(?)` hariç tut) |
| SP-02 işaretten sonra boşluk yok | warning | `([,;])(?=[A-Za-zÇĞİÖŞÜçğıöşü])` | `elma,armut` → `elma, armut` | Sayılar `3,5` (rakamla devam ediyorsa eşleşmez); kod |
| SP-03 nokta/soru/ünlemden sonra boşluk yok | warning | `([.!?])(?=[A-ZÇĞİÖŞÜ][a-zçğıöşü])` | `geldi.Sonra` → `geldi. Sonra` | URL, dosya adı (`Dosya.Txt`), kısaltma `T.C.`; kod |
| SP-04 ayraç içi boşluk | warning | `\(\s+|\s+\)` | `( örnek )` → `(örnek)` | yok denecek kadar az |
| SP-05 çift boşluk | info | `(?<=\S)  +(?=\S)` | — | hizalanmış tablo/kod |
| SP-06 kesmeden sonra boşluk | error | `\w['’]\s+(?:[ıiuü]n|[ae]|d[ae]|t[ae]|d[ae]n|t[ae]n|y[ae]|[ıiuü])\b` | `Ankara' da` → `Ankara'da` | düz tırnak `'…'` ile alıntı |

---

## 3. Nokta ( . )

TDK maddeleri (tam metin özetleri, örnekler TDK'dan):
1. Cümle sonuna konur.
2. Bazı kısaltmaların sonuna: Alb., Dr., Yrd. Doç., Prof., Cad., Sok., s., sf., vb., Alm., Ar., İng.
3. Sıra bildirmek için sayıdan sonra: 3. (üçüncü), 15.; II. Mehmet, XIV. Louis, XV. yüzyıl; 2. Cadde.
4. Art arda sıralanan rakamlarda **yalnızca sonuncudan sonra**: "3, 4 ve 7. maddeler; XII – XIV. yüzyıllar".
5. Madde numaralarından sonra: I. 1. A. a.
6. Tarihte gün/ay/yıl ayırıcı: 29.5.1453, 29.X.1923. UYARI: Ay adı yazıyla yazılırsa nokta yok: **29 Mayıs 1453**.
7. Saat ve dakika ayırıcı: **09.15'te, 13.00'te, 17.30'da**.
8. Künye sonuna.
9. 4+ basamaklı sayılarda üçlü gruplama: **1.000, 326.197, 49.750.812**.
10. Genel ağ adresleri; 11. matematikte çarpma.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| NK-01 sıra noktası + ek | error | `\b(\d+)\.\s?['’]?(?:inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü|ci|cı|cu|cü)\b` | `8.'inci`, `2.nci` → `8'inci`, `2'nci` | yok |
| NK-02 ay adlı tarihte nokta | error | `\b\d{1,2}\.\s?(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\b` | `29. Ekim 1923` → `29 Ekim 1923` | "29. Ekim" sıra sayısı olarak çok nadir |
| NK-03 saat iki nokta ile | info | `\b([01]?\d|2[0-3]):([0-5]\d)\b` | `13:00'te` → `13.00'te` | Saat:dakika:saniye, kod, oran "3:1", maç skoru; **yalnızca info** (yaygın kullanım) |
| NK-04 İngilizce ondalık nokta | warning | `\b\d+\.\d{1,2}\s?(?:milyon|milyar|bin|trilyon|kat|puan|saat|yıl|dakika|metre|km|kg|TL|dolar|avro|°C)\b` | `3.5 milyon` → `3,5 milyon` | Sürüm `v3.5`, IP, bölüm no `2.3`, saat `09.15` (birimsiz olduğundan eşleşmez) |
| NK-05 İngilizce binlik virgül | warning | `\b\d{1,3}(?:,\d{3})+(?!,?\d)\b` | `1,500,000` → `1.500.000` | `0,125` gibi üç ondalıklı sayı; `1,250` (bir virgül iki yüz elli) belirsiz → yalnızca **iki+ grup** veya bağlamda "kişi/lira" varsa error |
| NK-06 4+ basamakta gruplama yok | info | `(?<![\d.,])\d{5,}(?![\d.,])` | `1500000 kişi` → `1.500.000 kişi` | Yıllar (4 hane, eşleşmez), posta kodu, telefon, ID, kod; yalnızca info |
| NK-07 sıralı rakamlarda her birine nokta | warning | `\b\d+\.,\s*\d+\.(?:\s*ve\s*\d+\.)` | `3., 4. ve 7. maddeler` → `3, 4 ve 7. maddeler` | düşük |

---

## 4. Virgül ( , )

TDK kullanım yerleri (1–15): eş görevli kelimeler; sıralı cümleler; yüklemden uzak düşmüş özne; ara söz; tekrar; tırnaksız alıntıdan sonra ("Adana'ya yarın gideceğim, dedi."); konuşma çizgisinden sonra; **hayır, yok, evet, peki, pekâlâ, tamam, olur, hayhay, başüstüne, öyle, haydi, elbette** sonrası; anlam karışıklığını önleme ("Bu, tek gözlü…"); hitaplardan sonra; ondalık; art arda zarf-fiiller; **özne olan bu/şu/o'dan sonra** ("Bu, benim gibi yazarlar için…"); künyeler.

**Virgül KONMAZ uyarıları (linter için en değerli kısım):**
- **ve, veya, yahut, ya … ya** bağlaçlarından önce ve sonra virgül konmaz.
- Tekrarlı bağlaçlarda (hem … hem, ya … ya, gerek … gerek, ister … ister, ne … ne, … da … da) virgül konmaz.
- Pekiştirme ve bağlama görevindeki **da/de bağlacından sonra** virgül konmaz.
- "-ınca" anlamlı **mı/mi** zarf-fiilinden sonra ("Ben aç yattım mı kötü rüyalar görürüm") virgül konmaz.
- **Şart ekinden sonra** virgül konmaz ("…biri gelecek olursa hemen susuyorlardı").
- Zarf-fiil ekli tek kelimeden sonra virgül konmaz ("buluştukça kıza…").

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| VR-01 Oxford/İngilizce virgül (ve öncesi) | **error** | `,\s+(ve|veya|yahut|ya da|ile)\s` | `elma, armut, ve kiraz` → `elma, armut ve kiraz` | Ara söz bitişi: "Ahmet, bence, ve…" (çok nadir); "ile" bağlaç değil edat olabilir → ile için warning |
| VR-02 ve sonrası virgül | error | `\b(ve|veya|yahut)\s*,` | `ve, sonra` → `ve sonra` | Metadil ("'ve', 'ile' gibi") → tırnak içini atla |
| VR-03 tekrarlı bağlaçta virgül | warning | `\b(hem|ne|ya|gerek|ister)\s+[^,.;!?]{1,40},\s+\1\s` | `hem gider, hem ağlar` → `hem gider hem ağlar` | Uzun cümlede ara söz |
| VR-04 da/de bağlacından sonra virgül | warning | `\s(da|de)\s*,` | `Ben de, gittim` → `Ben de gittim` | Cümle sonundaki "de," (ör. "o da, bu da") sıralamalarda ara virgül; warning |
| VR-05 şart ekinden sonra virgül | info | `\b\w+(?:sa|se)(?:m|n|k|nız|niz|lar|ler)?,\s` | `gelirse, gideriz` → `gelirse gideriz` | Çok yaygın ve uzun şart cümlelerinde okunurluk için konuyor; TDK uyarısı var ama "humanizer" için yalnızca info. "Ayrıca, hatta, yine de" hariç tutulmalı. "-se" ile biten isimler (ör. "kese", "masa"…) FP → bir fiil kök/çekim kontrolü gerekir |
| VR-06 hitap/evet/peki sonrası virgül eksik | info | `^(Evet|Hayır|Peki|Tamam|Olur|Haydi|Elbette|Pekâlâ)\s+(?=\w)` | `Evet bu doğru` → `Evet, bu doğru` | Elbette tek başına zarf olarak kullanılabilir |
| VR-07 özne "bu/şu/o" sonrası virgül | info | yalnızca reviewer | `Bu benim için zor.` → `Bu, benim için zor.` | Sıfat olarak "bu kitap" → regexle ayrılamaz |
| VR-08 İngilizce bağlaç-başı virgülü | warning (stil) | `^(Ancak|Fakat|Ayrıca|Dahası|Üstelik|Sonuç olarak|Özetle|Kısacası|Bu nedenle|Dolayısıyla|Öte yandan|Bununla birlikte),` | AI kalıbı; TDK'da zorunlu değil. Sık tekrar sayılmalı (bkz. dosya 05/07) | Tek başına hata değil; **yoğunluk** metriği olarak kullan |

---

## 5. Noktalı virgül ( ; )

TDK: (1) virgüllerle ayrılmış tür/takımları ayırır: "Erkek çocuklara Doğan, Tuğrul, Aslan, Orhan; kız çocuklara ise İnci, Çiçek…"; (2) ögelerinde virgül olan sıralı cümleleri ayırır: "At ölür, meydan kalır; yiğit ölür, şan kalır."; (3) ikiden fazla eş değer ögede virgül varsa özneden sonra: "Yeni usul şiirimiz; zevksiz, köksüz, acemice görünüyordu."

| id | seviye | kontrol | not |
|---|---|---|---|
| NV-01 noktalı virgülden sonra büyük harf | warning | `;\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]` (özel ad sözlüğü dışında) | "Gittik; Sonra…" → küçük. FP: özel ad |
| NV-02 aşırı noktalı virgül | info (stil) | paragraf başına `;` sayısı > 2 | AI metinlerinde İngilizce semicolon alışkanlığı; insan Türkçesinde nadir |

---

## 6. İki nokta ( : )

TDK: (1) örnek verilecek cümle sonuna; (2) açıklama verilecek cümle sonuna; (3) ses bilgisinde uzun ünlü (a:ile); (4) konuşmalarda konuşanı belirten sözden sonra; (5) edebî eserde konuşmadan önceki ifade sonuna; (6) genel ağ adresi; (7) bölme.

**Büyük harf kuralı (Büyük Harfler A):** "İki noktadan sonra gelen **cümleler** büyük harfle başlar: Menfaat sandalyeye benzer: Başında taşırsan…" **UYARI:** "İki noktadan sonra cümle ve özel ad niteliğinde olmayan örnekler sıralandığında bunlar **büyük harfle başlamaz**: …çok evde görmüşsünüzdür: duvarlarda çiviler, çivi yerleri, lekeler…"

→ Görevdeki "colon then capital = İngilizce sızıntısı" varsayımı **TDK'ya göre yanlış**. İki noktadan sonra tam cümle varsa büyük harf **doğrudur**. Kontrol edilebilir olan, büyük harfle başlayan **sıralama** (fiilsiz liste) ve İngilizce "Title: Subtitle" kalıbıdır.

| id | seviye | regex / mantık | yanlış → doğru | FP riski |
|---|---|---|---|---|
| IN-01 iki noktadan sonra liste büyük harfle | warning | `:\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)(,\s+[a-zçğıöşü]\w*){1,}` ve segmentte çekimli fiil yok | `şunlar: Elma, armut, kiraz` → `şunlar: elma, armut, kiraz` | İlk öge özel ad ise doğru; özel ad sözlüğü gerekir |
| IN-02 iki noktadan sonra tam cümle küçük harfle | warning | `:\s+[a-zçğıöşü][^.!?]*\b\w+(?:dı|di|du|dü|tı|ti|tu|tü|yor|acak|ecek|mış|miş|muş|müş|r|maz|mez|dır|dir|dur|dür|tır|tir|tur|tür)[.!?]` | `Sebep basit: herkes yorgundu.` → `Sebep basit: Herkes yorgundu.` | Fiil eki sezgisi kaba; info'ya düşürülebilir |
| IN-03 iki noktadan önce boşluk | error | `\s+:` (URL/zaman hariç) | `Not : ` → `Not: ` | Fransızca tipografi |
| IN-04 "X: Y" başlık kalıbı (İngilizce subtitle) | info (stil) | Markdown başlıkta `^#+\s.+:\s.+$` | AI başlık kalıbı ("Yapay Zekâ: Geleceğin Anahtarı") | İnsan yazısında da var; yoğunluk metriği |
| IN-05 iki nokta + kesme ile saat | info | `\d{1,2}:\d{2}['’]` | `13:00'te` → `13.00'te` | NK-03 ile aynı |

---

## 7. Üç nokta ( … ), soru ( ? ), ünlem ( ! )

**Üç nokta (TDK):** tamamlanmamış cümle; açık yazılmak istenmeyen kelime (b…tan); alıntıda alınmayan bölüm; sözü okuyucuya bırakma; ünlem/seslenmede pekiştirme; eksik cevap. **UYARI:** "Ünlem ve soru işaretinden sonra üç nokta yerine **iki nokta** konulması yeterlidir: Gök ekini biçer gibi!.. Nasıl da akşam oldu?.." **UYARI:** "Üç nokta yerine iki veya daha çok nokta kullanılmaz."

**Soru (TDK):** soru eki/sözü içeren cümle sonu; soru eki içermeyen soru ("Adınız?"); şüpheli bilgi "(?)" "1496 (?)". **UYARI:** zarf tümleci olan mı'lı yan cümlede soru işareti yok: "Akşam oldu mu sürüler döner." **UYARI:** sıralı/bağlı soru cümlelerinde soru işareti **en sona**: "Çok yakından mı bu sesler, çok uzaklardan mı?"

**Ünlem (TDK):** duygu cümleleri; seslenme/hitap/uyarı; alay/küçümseme için ayraç içinde "(!)".

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| UN-01 dört+ nokta | error | `\.{4,}` | `bekledik....` → `bekledik…` | ASCII art, içindekiler noktalı çizgi |
| UN-02 iki nokta (?!/! sonrası değil) | error | `(?<![.?!])\.\.(?!\.)` | `tamam..` → `tamam…` | `..` dosya yolu (`../src`), sürüm aralığı `1..5`, kod → kod/URL'yi atla |
| UN-03 soru/ünlemden sonra üç nokta | warning | `([?!])(\.\.\.|…)` | `Neden?...` → `Neden?..` | yok |
| UN-04 "..." yerine "…" | info (tipografi) | `(?<!\.)\.\.\.(?!\.)` | `ama...` → `ama…` | İkisi de kabul görür. TDK metni `…` kullanır. Yalnızca normalizasyon tercihi |
| UN-05 üç noktadan önce boşluk | warning | `\s+…|\s+\.\.\.(?!\s*$)` | `ama …` → `ama…` | Alıntı başı "… derken" geçerli (cümle başında) → satır/cümle başını hariç tut |
| UN-06 soru işareti tekrarı / ?! | info | `\?{2,}|!{2,}|\?!|!\?` | `Ne?!` | Edebî/sohbet dilinde kabul görür; resmî metinde info |
| UN-07 mı/mi'li zarf tümcesinde ? | info (reviewer) | yalnızca reviewer | `Akşam oldu mu? sürüler döner` | regexle ayrılamaz |
| UN-08 soru eki var, ? yok | warning | `\b(mı|mi|mu|mü)(?:sın|sin|sun|sün|yım|yim|yum|yüm|yız|yiz|yuz|yüz|sınız|siniz|sunuz|sünüz|dır|dir|dur|dür)?\s*\.(\s|$)` | `Geldin mi.` → `Geldin mi?` | "Güzel mi güzel." (pekiştirme), "yağdı mı çıkamayız" (zarf; nokta ile bitmez); dolaylı soru "gelip gelmediğini sordu mu bilmem." nadir |
| UN-09 ünlem enflasyonu | info (stil) | paragraf başına `!` > 1 (diyalog dışı) | AI pazarlama tonu | — |

---

## 8. Kısa çizgi ( - / – ), uzun çizgi ( — ), eğik çizgi ( / )

**Kısa çizgi (TDK):**
1. Satır sonu bölme.
2. **Ara söz/ara cümle**: başına ve sonuna konur, **bitişik yazılır**: "Küçük bir sürü **-dört inekle birkaç koyun-** köye giren geniş yolun ağzında durmuştu." Büyük Harfler UYARI: "İki çizgi arasındaki açıklama cümleleri büyük harfle başlamaz: Bir zamanlar -bu zamanlar çok da uzak değildir…- Türk saltanatının…"
3–6. Dil bilgisi: kök/ek ayırma (al-ış), fiil kökü (gör-), ek gösterimi (-lık), hece (a-raş-tır-ma).
7. "arasında, ve, ile, ila, -den -e" anlamı: Aydın-İzmir yolu, Türk-Alman ilişkileri, 09.30-10.30, 1914-1918. **UYARI:** "Cümle içinde sayı adlarının yinelenmesinde araya kısa çizgi konmaz: On on beş yıl. Üç beş kişi geldi."
8–9. Çıkarma, eksi (-2 °C).

**Uzun çizgi (TDK):** "Yazıda **satır başına alınan konuşmaları** göstermek için kullanılır. Buna konuşma çizgisi de denir." Oyunlarda konuşanın adından sonra da konabilir ("Sıtkı Bey — Kaleyi…"). **UYARI:** "Konuşmalar tırnak içinde verildiğinde uzun çizgi kullanılmaz."

→ TDK'da uzun çizginin **cümle içi ara söz / vurgu / açıklama** kullanımı **yoktur**. Bu kullanım İngilizce em-dash alışkanlığıdır ve AI metninin en güçlü işaretlerinden biridir. TDK'nın ara söz için önerdiği karşılıklar: virgül (Virgül 4), bitişik kısa çizgi (Kısa Çizgi 2), yay ayraç (Yay Ayraç 1).

Not: TDK sayfası başlıkta kısa çizgiyi `–` (en dash) glifiyle gösteriyor ama örneklerde `-` (hyphen) kullanıyor; "XII – XIV. yüzyıllar" örneğinde aralıklı en dash da var. Aralık gösteriminde `-` ve `–` ikisi de kabul edilmeli.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| CZ-01 cümle içi em dash | **error** (humanizer için en güçlü sinyal) | `(?<=\S)\s*—\s*(?=\S)` (satır başı hariç: `(?m)^(?!\s*—)`) | `Bu karar — bence yanlış — ertelendi.` → `Bu karar, bence yanlış, ertelendi.` / `-bence yanlış-` / `(bence yanlış)` | Oyun metni "Ad — replik" kalıbı (`^[A-ZÇĞİÖŞÜ][\w ]{1,30} — `) hariç tutulmalı |
| CZ-02 aralıklı en dash ara söz | warning | `(?<=[a-zçğıöşü])\s+–\s+(?=[a-zçğıöşü])` | `karar – bence yanlış – ertelendi` → virgül/ayraç | Sayı/yer aralığı `Aydın – İzmir` (büyük harf ya da rakam yanında → atla) |
| CZ-03 aralıklı hyphen ara söz | warning | `(?<=[a-zçğıöşü])\s+-\s+(?=[a-zçğıöşü])` | `sürü - dört inek - köye` → `sürü -dört inek- köye` veya virgül | Madde işareti `- ` (satır başı) hariç tutulmalı |
| CZ-04 satır başı konuşma çizgisi | OK | `(?m)^\s*—\s` | geçerli; dokunma | — |
| CZ-05 tırnaklı konuşma + uzun çizgi | warning | `(?m)^\s*—\s*[“"]` | `— "Gel," dedi.` → biri kaldırılmalı | — |
| CZ-06 sayı yinelemede çizgi | warning | `\b(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on)-(iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|on beş|yirmi)\s+(kişi|gün|yıl|saat|dakika|kez|defa)\b` | `üç-beş kişi` → `üç beş kişi` | yok |
| CZ-07 em dash yoğunluğu | metrik | 1000 kelime başına `—` sayısı (diyalog dışı) | İnsan Türkçe denemede ≈0 | — |

**Eğik çizgi (TDK):** yan yana dizeler; adres (21/6, Kurtuluş / ANKARA); tarih (18/11/1969); ek biçimleri (-a /-e); URL; bölme; birim oranı (g/sn, **boşluksuz**).

| id | seviye | regex | not |
|---|---|---|---|
| EC-01 "ve/veya" | info (stil, çeviri kokusu) | `\bve/veya\b` | İngilizce "and/or" kalıbı. Önerilen: "veya", "ya da", "ve ya da" yerine cümleyi yeniden kur |
| EC-02 eğik çizgili seçenek yığını | info | `\b\w+/\w+/\w+\b` (URL hariç) | "kullanıcı/müşteri/üye" → sözlü anlatım |

---

## 9. Tırnak ( “ ” ‘ ’ ), kesme ( ’ ), ayraç ( ( ) [ ] )

**Tırnak (TDK):** (1) olduğu gibi aktarılan söz; UYARI: alıntının sonundaki işaret **tırnak içinde kalır**: “İzmir üzerine dünyada bir şehir daha yoktur!” diyorlar. (2) Özel olarak vurgulanmak istenen söz: Yeni bir “barış taarruzu” başladı. (3) Eser, yazı ve bölüm adları. UYARI: Bunlar eğik yazıyla da gösterilebilir. **UYARI: Tırnak içine alınan sözlerden sonra gelen ekleri ayırmak için kesme işareti kullanılmaz: Elif Şafak'ın “Bit Palas”ını okudunuz mu?** (4) Makale adları. **Tek tırnak:** tırnak içinde tırnak.

TDK'nın kendi glifleri: “ ” (çift), ‘ ’ (tek), ’ (kesme). Yani **kıvrık tırnaklar TDK biçimidir, işaretlenmemeli.** Düz `"` ve `'` dijitalde kabul edilir. Linter ikisini de kabul etmeli, yalnızca **aynı metinde karışık kullanımı** info olarak bildirmeli. Alman/Fransız tırnağı (`„ “`, `« »`) Türkçe standardında yok.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| TR-01 tırnak sonrası kesme | error | `[”"]['’](?:[a-zçğıöşü]+)` | `“Bit Palas”'ını` → `“Bit Palas”ını` | yok |
| TR-02 noktalama tırnak dışında (alıntı cümlesi) | info | `[“"][A-ZÇĞİÖŞÜ][^”"]{10,}[^.!?…][”"][.!?]` | `“…yoktur”!` → `“…yoktur!”` | Alıntı cümle değil söz parçasıysa nokta dışarıda kalabilir → info |
| TR-03 vurgu tırnağı enflasyonu | info (stil) | paragraf başına vurgu amaçlı tırnaklı tek/çift kelime > 2 | AI "scare quotes" alışkanlığı | — |
| TR-04 karışık tırnak stili | info | aynı belgede hem `"` hem `“` | tutarlılık | — |
| TR-05 « » / „ “ | warning | `[«»„]` | → “ ” | Yabancı dilde alıntı |

**Ayraç (TDK):** ek bilgi; **özel ada ait ek ayraçtan önce yazılır: Yunus Emre'nin (1240?-1320)…**; tiyatro yönergeleri; kaynak; alıntıda (…); alay "(!)"; şüphe "(?)"; madde 1) a). Köşeli ayraç: ayraç içinde ayraç; alıntıya eklenen söz: "fark[ın]".

| id | seviye | regex | yanlış → doğru |
|---|---|---|---|
| AY-01 ek ayraçtan sonra | error | `\b([A-ZÇĞİÖŞÜ]\w+)\s*\([^)]*\)['’]?(n?[ıiuü]n|[ıiuü]|y?[ae]|d[ae]n|t[ae]n|d[ae]|t[ae])\b` | `Yunus Emre (1240-1320)'nin` → `Yunus Emre'nin (1240-1320)` |
| AY-02 kısaltma açılımı + ek | warning | `\b([A-ZÇĞİÖŞÜ]{2,})\s*\(([^)]+)\)['’]` | `TDK (Türk Dil Kurumu)'nun` → `Türk Dil Kurumunun (TDK)` ya da `TDK'nin` |

---

## 10. Kesme işareti — ayrıntılı kurallar

### 10.1 Konur (TDK madde 1–7)
1. Özel adlara getirilen **iyelik, durum ve bildirme (ek fiil)** ekleri: Kurtuluş Savaşı'nı, Atatürk'üm, Türkiye'mizin, Ziya Gökalp'tan, Refik Halit Karay'mış, Ahmet Cevat Emre'dir, Namık Kemal'se, Şinasi'yle, Alman'sınız, Kırgız'ım, Osmanlı Devleti'ndeki, Çanakkale Boğazı'nın, Resmî Gazete'de, Millî Eğitim Temel Kanunu'na, Eski Çağ'ın, Yükselme Dönemi'nin.
   - Kısaltmalı yer söyleyişi: Hisar'dan, Boğaz'dan.
   - Belirli bir kanun/yönetmelik kastedilip büyük yazıldığında: **Bu Kanun'un 17. maddesi… Yönetmelik'in 2'nci maddesi**.
   - **Avrupa Birliği'ne** (açık istisna).
2. Saygı/unvan sözlerine gelen ekler: Nihat Bey'e, Ayşe Hanım'dan, Enver Paşa'ya, **Türk Dil Kurumu Başkanı'na**.
3. Kısaltmalara: TBMM'nin, TDK'nin, BM'de, ABD'de, TV'ye.
4. Sayılara: 1985'te, 8'inci, 2'nci, 7,65'lik, 657'yle.
5. Belirli tarih bildiren ay/gün adlarına: 17 Aralık'a kadar, 12 Temmuz 2010 Pazartesi'nin.
6. Ölçü/söyleyiş gereği ses düşmesi: n'eyleyim, m'ola.
7. Ek veya harften sonra: a'dan z'ye, -lık'la.

### 10.2 Konmaz (UYARI'lar)
- **Kurum, kuruluş, kurul, birleşim, oturum ve iş yeri adlarına gelen ekler kesmeyle ayrılmaz:** Türkiye Büyük Millet Meclisine, Türk Dil Kurumundan, Türkiye Petrolleri Anonim Ortaklığına, Bakanlar Kurulunun, Danışma Kurulundan, Mavi Köşe Bakkaliyesinden.
- Başbakanlık, Rektörlük + ünlü → Başbakanlığa, Rektörlüğe.
- Sonu 3. tekil iyelikli özel ada başka iyelik gelirse: Boğaz Köprümüzün, Amik Ovamızın.
- **Yapım ekleri, çokluk eki ve bunlardan sonraki ekler:** Türklük, Türkçe, **Türkçenin**, Avrupalı, Konyalı, **Ahmetler, Türklerin**, Müslümanlıkta, Atatürkçülüğün.
- "o" zamiri (özel ad yerine) küçük yazılır, kesme almaz.
- Tırnaktan sonraki ekler (§9).
- Noktalı kısaltmalar ve üslü birimler: **vb.leri, Alm.dan, İng.yi; cm³e, m²ye**.
- **Bağlaç da/de** kesmeyle ayrılmaz: Ayşe de geldi (Ayşe'de geldi değil).
- Simgelere ek getirilmez, ada getirilir: Fe'ye değil demire.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| KS-01 kurum adı + kesme | **error** | `\b(Kurumu|Kurulu|Bakanlığı|Başkanlığı|Müdürlüğü|Genel Müdürlüğü|Üniversitesi|Fakültesi|Enstitüsü|Yüksekokulu|Meclisi|Derneği|Vakfı|Belediyesi|Valiliği|Kaymakamlığı|Lisesi|Okulu|Hastanesi|Bankası|Şirketi|Ortaklığı|Holdingi|Merkezi|Ajansı|Odası|Borsası|Konseyi|Komisyonu|Mahkemesi|Savcılığı|Bakkaliyesi|Kulübü|Partisi|Sendikası|Federasyonu|Birleşimi|Oturumu)['’]` | `Türk Dil Kurumu'nun` → `Türk Dil Kurumunun`; `İstanbul Üniversitesi'nde` → `İstanbul Üniversitesinde` | **Avrupa Birliği'ne** (istisna; listede "Birliği" yok); makam "Başkanı'na" (listede yok, doğru); spor kulübü/ parti adları basında kesmeyle yazılıyor ama TDK'ya göre yine kesmesiz |
| KS-02 dil adı + kesme | **error** | `\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:ça|çe|ca|ce))['’]\w+` | `Türkçe'de`, `İngilizce'ye` → `Türkçede`, `İngilizceye` | Özel ad "Ece'nin", "Bilge'nin", "Hatice'yi", "Nice'te", "Seyrekçe" vb. → kişi adı listesiyle hariç tut (ör. Ece, Gonca, Hatice, Nevin…); `-ca/-ce` ile biten il/ilçe (Gölcük değil; "Karaca" soyadı, "Çatalca") FP |
| KS-03 çokluk/yapım eki öncesi kesme | **error** | `\b[A-ZÇĞİÖŞÜ]\w*['’](lar|ler|lı|li|lu|lü|lık|lik|luk|lük|cı|ci|cu|cü|çı|çi|çu|çü|laş|leş|ca|ce|ça|çe|sız|siz|suz|süz|ız|iz)\w*` | `Türk'ler`, `Avrupa'lı`, `Ankara'lı`, `Atatürk'çü` → `Türkler`, `Avrupalı`, `Ankaralı`, `Atatürkçü` | `'ler` kısaltmadan sonra geçerli (`STK'ler`, `AVM'ler`) → büyük harf kısaltmaları hariç tut (`[A-ZÇĞİÖŞÜ]{2,}['’]ler` OK). Sayıdan sonra `1990'lı` geçerli → rakamı hariç tut |
| KS-04 noktalı kısaltma + kesme | error | `\b(vb|vs|Dr|Prof|Doç|Av|Alb|Gen|Mah|Cad|Sok|No|Alm|İng|Fr|Ar|Far)\.['’]` | `vb.'leri`, `Dr.'a`, `No.'lu` → `vb.leri`, `Dr.a`, `No.lu` | Cümle sonu noktası + tırnak (`vb.'`) |
| KS-05 bağlaç de/da kesmeyle | warning (reviewer) | `\b[A-ZÇĞİÖŞÜ]\w*['’](da|de)\s+(geldi|gitti|var|yok|olur|oldu|bil|çok|mi|mı)` | `Ayşe'de geldi` → `Ayşe de geldi` | Bulunma eki ile karışır ("Ankara'da var"); regex yalnızca sezgi, kararı reviewer verir |
| KS-06 özel ada ek, kesme yok (gazetteer) | warning | `\b(Türkiye|İstanbul|Ankara|İzmir|Avrupa|Asya|Amerika|Almanya|Fransa|İngiltere|Rusya|Çin|Japonya|Google|Microsoft|Apple|OpenAI)(nin|nın|de|da|den|dan|te|ta|ten|tan|ye|ya|yi|yı|e|a|i|ı|in|ın|un|ün|le|la|yle|yla|dir|dır|dur|dür)\b` | `İstanbulda` → `İstanbul'da` | `-li/-lı`, `-ce`, `-ler` dahil edilmemeli (yapım/çokluk). Marka adlarının "iş yeri adı" sayılıp sayılmayacağı TDK'da belirsiz; basın kesmeli yazıyor (Google'ın). **Tek kelimelik marka: kesme kabul; çok kelimeli "X Şirketi": kesmesiz** |
| KS-07 kesmeli ekin ses uyumu (özel ad) | error | §10.3 algoritması | `Ahmet'de` → `Ahmet'te`; `Kemal'dan` → `Kemal'den`; `Paris'ye` → `Paris'e` | Yabancı adların okunuşu (Bordeaux'ya: "bordo"); okunuş sözlüğü gerekir → yabancı ad listesini warning'e düşür |
| KS-08 "o" zamiri büyük/kesmeli | warning | `(?<![.!?]\s)\bO['’](nun|na|nu|nda|ndan)\b` | `O'nun (Atatürk) için` → `onun` | Cümle başı "O'nun" bile yanlış (kesme gereksiz) → kesme kısmı her zaman error |
| KS-09 ek fiil/ek ile özel ad, kesme eksik sayı | error | `\b(\d+)(de|da|te|ta|den|dan|ten|tan|e|a|ye|ya|i|ı|u|ü|yi|yı|in|ın|un|ün|nin|nın|nun|nün|inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü|lik|lık|luk|lük|li|lı|lu|lü)\b` | `2023te`, `5inci` → `2023'te`, `5'inci` | `3D`, `4K`, `5G`, `2FA` (harfle biten kodlar) — listedeki ekler değil ama `5G`'yi atlamak için harfli tek-karakter son eki dışla |

### 10.3 Ses uyumu algoritması (KS-07, KS-09, KY-01 için)

TDK: kesmeye rağmen ek, **okunuşa** göre gelir (Kısaltmalar: "Büyük harflerle yapılan kısaltmalara getirilen eklerde ise kısaltmanın son harfinin okunuşu esas alınır: BDT'ye, TDK'den, THY'de, TRT'den, TL'nin"; "kelime gibi okunan kısaltmalarda kısaltmanın okunuşu esas alınır: ASELSAN'da, BOTAŞ'ın, NATO'dan, UNESCO'ya").

```
son_ünlü ∈ {a, ı}  → a/ı ekleri   (da, ın, ı, a, dan, la)
son_ünlü ∈ {o, u}  → a/u          (da, un, u, a)
son_ünlü ∈ {e, i}  → e/i          (de, in, i, e)
son_ünlü ∈ {ö, ü}  → e/ü          (de, ün, ü, e)
son_ses ∈ {f,s,t,k,ç,ş,h,p} → d→t (te/ta, ten/tan)      ("fıstıkçı şahap")
son_ses ünlü → kaynaştırma: 'ye/'ya, 'yi/'yı, 'nin/'nın, 'yle/'yla
```
Yabancı kökenli ince-l'li adlar (Kemal, Hilal, Celal, Bilal, Lale…) **ince** ek alır: Kemal'e, Hilal'in, Lale'yi. Sözlükle istisna listesi tutulmalı.

**Sayıların okunuş tablosu (son okunan kelimeye göre):**

| Son basamak / okunuş | -de | -e (yönelme) | -in (ilgi) | -inci |
|---|---|---|---|---|
| 1 bir | 1'de | 1'e | 1'in | 1'inci |
| 2 iki | 2'de | 2'ye | 2'nin | 2'nci |
| 3 üç | 3'te | 3'e | 3'ün | 3'üncü |
| 4 dört | 4'te | 4'e | 4'ün | 4'üncü |
| 5 beş | 5'te | 5'e | 5'in | 5'inci |
| 6 altı | 6'da | 6'ya | 6'nın | 6'ncı |
| 7 yedi | 7'de | 7'ye | 7'nin | 7'nci |
| 8 sekiz | 8'de | 8'e | 8'in | 8'inci |
| 9 dokuz | 9'da | 9'a | 9'un | 9'uncu |
| 10 on | 10'da | 10'a | 10'un | 10'uncu |
| 20 yirmi | 20'de | 20'ye | 20'nin | 20'nci |
| 30 otuz | 30'da | 30'a | 30'un | 30'uncu |
| 40 kırk | 40'ta | 40'a | 40'ın | 40'ıncı |
| 50 elli | 50'de | 50'ye | 50'nin | 50'nci |
| 60 altmış | 60'ta | 60'a | 60'ın | 60'ıncı |
| 70 yetmiş | 70'te | 70'e | 70'in | 70'inci |
| 80 seksen | 80'de | 80'e | 80'in | 80'inci |
| 90 doksan | 90'da | 90'a | 90'ın | 90'ıncı |
| 100 yüz | 100'de | 100'e | 100'ün | 100'üncü |
| 1000 bin | 1000'de | 1000'e | 1000'in | 1000'inci |
| milyon | …'da | …'a | …'un | …'uncu |
| milyar | …'da | …'a | …'ın | …'ıncı |

Algoritma: sağdan ilk sıfır olmayan basamak grubunu bul. Son basamak 0 değilse birler tablosu; birler 0, onlar ≠ 0 ise onlar (10…90); ikisi de 0 ise yüz; 000 ise bin/milyon/milyar. Örnekler: **2023'te** (üç), **2020'de** (yirmi), **2000'de** (bin), **1990'da** (doksan), **2024'te** (dört), **2025'te** (beş), **2026'da** (altı). AI metinlerinde "2024'de", "2023'de", "1990'larda" (doğru), "2010'larda" (doğru: on → 'larda) hataları çok sık. Ondalıklı sayıda son okunan kesir kısmıdır: "7,65'lik" (altmış beş → 'lik).

**Kısaltma harf okunuşları (Türk alfabesi):** A a, B be, C ce, Ç çe, D de, E e, F fe, G ge, Ğ yumuşak ge, H he, I ı, İ i, J je, K **ke**, L le, M me, N ne, O o, Ö ö, P pe, R re, S se, Ş şe, T te, U u, Ü ü, V ve, Y ye, Z ze. → Ünsüzle biten her harf adı **e** ile biter. Bu yüzden harf harf okunan, ünsüz harfle biten kısaltmalar **ince ünlülü ek** alır: **TDK'ye, TDK'nin, TDK'den; TBMM'ye/'nin; ABD'ye/'de; THY'de; AKP'nin; CHP'ye; TL'nin; TV'ye**. Ünlü harfle bitenler kendi harfine göre: ODTÜ'ye (kelime okunuşu), AB'ye (be), BM'de (me), İTÜ'de.

→ Görevde geçen "**TDK'ya**" biçimi **TDK'ya göre yanlıştır**. Doğrusu **TDK'ye**. TDK'nın kendi örnekleri: "TDK'nin, TDK'den" (Kesme 3, Kısaltmalar). Ayrıca TDK yazarken "TDK'nın" değil "TDK'nin" kullanıyor.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| KY-01 ünsüzle biten kısaltmaya kalın ek | warning | `\b([A-ZÇĞİÖŞÜ]{2,6})['’](ya|yı|nın|dan|da|tan|ta|a|ı|ın|la|yla|lar|lık|dır|ydı)\b` + son harf ∉ {A, I, O, U} + kısaltma ∉ KELİME_OKUNAN | `TDK'ya`, `ABD'ye`ok, `TBMM'nın` → `TDK'ye`, `TBMM'nin` | **KELİME_OKUNAN** listesi: NATO, UNESCO, UNICEF, NASA, BOTAŞ, ASELSAN, TÜBİTAK, RTÜK, TÖMER, İLESAM, OYAK, TOKİ, SGK? (harf: SGK'ye ✓), ÖSYM (harf), HAVELSAN, ROKETSAN, TUSAŞ, İSKİ, ASKİ, BİM?, TEKEL, NATO, FIFA, UEFA, OPEC, AFAD, KOSGEB, YÖK (kelime: YÖK'e), ÖSYM, MEB (harf: MEB'e? okunuş "meb" → MEB'e de yaygın). İngilizce okunan kısaltmalar (AI "ey-ay", API, CEO, PDF) için okunuş belirsiz → **warning ve öneri**, error değil |
| KY-02 küçük harf kısaltma | info | `\b(cm|mm|km|kg|mg|ml|gr|lt)['’](\w+)` | `kg'dan` ✓ (okunuş: kilogram) | Okunuşa göre — "km'ye" (kilometre) ✓ |
| KY-03 noktalı/kesmesiz | bkz. KS-04 | | | |
| KY-04 büyük harfli kısaltmada nokta | warning | `\b(?:[A-ZÇĞİÖŞÜ]\.){2,}(?![A-ZÇĞİÖŞÜ])` hariç `T\.C\.` | `A.B.D.` → `ABD` | T.C. ve T. (Türkçe) gelenekleşmiş istisna; kişi adı baş harfleri "M. K. Atatürk" |
| KY-05 sert ünsüz yumuşatma | error | `\b(TÜBİTAĞ|RTÜĞ|CMUĞ|AGİĞ)['’]` | `TÜBİTAĞ'ın` → `TÜBİTAK'ın` | yok |

---

## 11. Bağlaçlar ve ekler: de/da, ki, mi, ile, ek fiil

### 11.1 Bağlaç da/de (TDK)
"Bağlaç olan da / de ayrı yazılır ve kendisinden önceki kelimenin son ünlüsüne bağlı olarak büyük ünlü uyumuna uyar: Kızı da geldi gelini de." UYARI: "Ayrı yazılan da / de **hiçbir zaman ta / te** biçiminde yazılmaz: Gidip de gelmemek var (Gidip te değil)." UYARI: "ya da" ayrı. UYARI: kesmeyle ayırmak yanlış: "Ayşe de geldi (Ayşe'de geldi değil)". Bulunma eki -da/-de/-ta/-te **bitişik**: devede kulak, yolda kalmak, ayakta durmak.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| DD-01 bağlaç te/ta | error | `\b(\w+[pçtkfsşh])\s+(te|ta)\b(?!\s+ki\b)` | `gidip te` → `gidip de`; `kitap ta` → `kitap da` | "ta" zarfı: "ta kendisi, ta oraya, ta ki, ta başından, ta ezelden" → `(?!\s+(ki|kendisi|oraya|buraya|başından|ezelden|baştan|uzaktan))` |
| DD-02 sık bitişik yazım | error | `\b(yada|hemde|dahada|pekde|hiçde|bilede|sonrada|hatta da)\b` → `ya da, hem de, daha da, pek de, hiç de…`; `\b([Yy]a|[Hh]em|[Dd]aha|[Pp]ek|[Hh]iç)['’]?(da|de)\b` | `yada` → `ya da` | **"yada"** TDK'de ayrı bir kelime (sihirli taş) → yalnızca bağlaç bağlamında error; pratikte FP ≈ 0 |
| DD-03 çekimli fiile bitişik de | warning | `\b\w+(dı|di|du|dü|tı|ti|tu|tü|yor|acak|ecek|mış|miş|muş|müş|sa|se)(da|de)\b` | `geldide` → `geldi de`; `bilsede` → `bilse de` | İsim + bulunma eki çok (ör. "kadıda", "ödüde"?) → morfoloji olmadan warning |
| DD-04 bölünmüş bulunma eki | error | `\b(hakkın|arasın|konusun|tarafın|sayesin|karşısın|içerisin|üzerin|altın|üstün|önün|sonun|başın|yanın|durumun|zamanın|ortasın)\s+(da|de)\b` | `hakkın da` → `hakkında`, `arasın da` → `arasında` | "altın da" (altın + bağlaç) "altın da gümüş de" → altın/başın için warning |
| DD-05 zamir + de belirsizliği | **reviewer** | `\b(bende|sende|onda|bizde|sizde|onlarda|bunda|şunda)\b` | `Bende geldim` → `Ben de geldim` | **Bulunma hâli olarak doğru**: "Kitap bende." → regexle karar verilemez. Ancak sezgi: ardından yüklem fiil (geldim/gittim/düşünüyorum/istiyorum) ve kişi eki zamirle uyumluysa yüksek olasılıkla bağlaç: `\b(Ben|Sen|Biz|Siz)de\s+\w+(m|n|k|z|yim|sin|iz|siniz|ım|ın|ız|sınız)\b` → warning |
| DD-06 de/da'dan sonra virgül | warning | VR-04 | | |
| DD-07 ünlü uyumu (ayrı yazılmış de) | warning | önceki kelimenin son ünlüsü kalın ise `de`, ince ise `da` → hata | `kitap de` → `kitap da` | Yabancı kelime/özel ad (Kemal da?) → ince-l istisnası |

### 11.2 Bağlaç ki (TDK)
"Bağlaç olan ki ayrı yazılır: bilmem ki, demek ki, kaldı ki vb." "Birkaç örnekte ki bağlacı kalıplaşmış olduğu için bitişik yazılır: **belki, çünkü, hâlbuki, mademki, meğerki, oysaki, sanki**." Şüphe/pekiştirme "ki" de ayrı: "zil çaldı mı ki? Seni öyle göreceğim geldi ki."

Ek olan -ki (ilgi/aitlik) **bitişik**: evdeki, yarınki, akşamki, benimki, seninki, onunki; ünlü uyumuna girmez ama **bugünkü, dünkü, öbürkü** istisnadır.

Sözlükte ayrı madde olarak doğrulananlar: **nasıl ki, şöyle ki, kaldı ki, yeter ki** (ayrı), **mademki, meğerki, oysaki, hâlbuki, sanki, çünkü** (bitişik). "oysa ki" sözlükte yok; ki sayfası **oysaki** diyor.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| KI-01 bağlaç ki bitişik | error | `\b(demek|kaldı|yeter|bilmem|öyle|şöyle|nasıl|sanırım|görüyorum|biliyorum|anlaşılan|madem|meğer|tabii|hatta|şu var|o kadar|öyle bir|ne var|varsay|yok|var|halbu)ki\b` hariç `(mademki|meğerki|halbuki|hâlbuki|oysaki|sanki|belki|çünkü)` | `demekki` → `demek ki`; `yokki` → `yok ki` | "yokki"/"varki" az; "nasılki" vb. FP ≈ 0 |
| KI-02 kalıplaşmışları ayırma | error | `\b(oysa|hâlbu|halbu|madem|meğer|san|bel)\s+ki\b` | `oysa ki`, `madem ki`, `hâlbu ki` → `oysaki`, `mademki`, `hâlbuki` | "madem ki" halk ağzında yaygın; TDK bitişik → error. "bel ki" yok denecek kadar az |
| KI-03 sıfat -ki'yi ayırma | error | `\b(\w+(?:da|de|ta|te|nda|nde))\s+ki\s+(\w+)` + sonraki kelime isim | `evde ki kitap` → `evdeki kitap` | "Evde ki kimse yoktu" → ki bağlaç olabilir mi? Çok nadir. Asıl FP: "Ben de ki…" yok. Warning olarak tut |
| KI-04 -ki zaman | error | `\b(yarın|akşam|sabah|dün|bugün|öbür|geçen yıl|şimdi)\s+ki\b` | `bugün ki` → `bugünkü`; `dün ki` → `dünkü`; `şimdi ki` → `şimdiki` | "Yarın ki gelirse…" (bağlaç) çok nadir |
| KI-05 kesmeli ki | error | `\w['’]ki\b` | `Ali'ki` → ? (`Ali'ninki`) | yok |

### 11.3 Soru eki mı/mi/mu/mü (TDK)
"Bu ek gelenekleşmiş olarak **ayrı yazılır** ve … ünlü uyumlarına uyar: Kaldı mı? Sen de mi geldin? Olur mu? İnsanlık öldü mü?" "Soru ekinden sonra gelen ekler **bu eke bitişik** yazılır: Verecek misin? Okuyor muyuz? Gelecek miydi?" Sorudan başka görevde de ayrı: "Güzel mi güzel! Yağmur yağdı mı dışarı çıkamayız." "Vaz mı geçtin?"

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| MI-01 fiile bitişik soru eki | error | `\b(\w+(?:dı|di|du|dü|tı|ti|tu|tü|yor|acak|ecek|mış|miş|muş|müş|ır|ir|ur|ür|ar|er|r|maz|mez|sa|se|malı|meli))(mı|mi|mu|mü)(sın|sin|sun|sün|yım|yim|yum|yüm|yız|yiz|yuz|yüz|sınız|siniz|sunuz|sünüz|ydı|ydi|ydu|ydü|ymış|ymiş|dır|dir|dur|dür)?\b` | `geliyormusun` → `geliyor musun`; `yaptınmı` → `yaptın mı` | İsimler: "hazırmı"? → zaten hata. Gerçek kelimeler: "kimi, simi, tümü, ümü, dünyamı (dünyamı = dünyam-ı!)", "-mı" iyelik+belirtme: "kitabımı, arabamı, işimi, evimi" (**çok yüksek FP**) → yalnızca **fiil çekimi** önekli kalıp tutulmalı; isim gövdesi için uygulanmamalı |
| MI-02 soru eki ünlü uyumu | error | önceki kelimenin son ünlüsü → beklenen `mı/mi/mu/mü` | `geldi mı` → `geldi mi`; `okul mi` → `okul mu` | Yabancı kelime (Kemal mi ✓) |
| MI-03 soru ekinin sonrasını ayırma | error | `\b(mı|mi|mu|mü)\s+(sın|sin|sun|sün|yım|yim|yız|yiz|sınız|siniz|ydı|ydi|ymış|ymiş)\b` | `gelecek mi sin` → `gelecek misin` | yok |
| MI-04 sıralı soruda ara soru işareti | info | `\b(mı|mi|mu|mü)\?\s*[a-zçğıöşü][^?]{0,40}\b(mı|mi|mu|mü)\?` | `Yakından mı? uzaktan mı?` → `Yakından mı, uzaktan mı?` | Ayrı soru cümleleri de olabilir |

### 11.4 ile, ek fiil
- **ile** ayrı ya da bitişik yazılabilir; bitişikte i düşer, ünlü uyumu: bulutla, çiçekle, arkadaşıyla, çevreyle. Kontrol: `\b\w+[aıou]\w*['’]?(le)\b` → uyum hatası (`arabayle`). Ayrıca "ile" bağlacından önce virgül yok (VR-01).
- **Ek fiil** (idi, imiş, ise, iken) ayrı veya bitişik; bitişikte uyum: yorgundu, güzelmiş, gelirse; sonuncuydu, yabancıymış, neyse. **-ken uyuma girmez**: başlayacakken, okurken, okuldayken. Kontrol: `\w+(kan)\b` → `-ken` (`okurkan` hatası; nadir).
- **Fiil çekimi (TDK):** -acak/-ecek, -ayım/-eyim, -alım/-elim, -an/-en eklerinden önceki ünlü söyleyişe bakılmaksızın a/e yazılır: başlayacağım (başlıyacağım değil), gelmeyeceksin, başlayayım. Regex: `\b\w+(ıyacak|iyecek|uyacak|üyecek|ıyayım|iyeyim)\w*` → `ayacak/eyecek`. Örn. `başlıyacak` → `başlayacak`, `gidiyecek`… (FP: `-iyor` + ek? "diyecek", "yiyecek" **doğru** — de-/ye- fiilleri istisna: `(?<!\bd)(?<!\by)iyecek`).
- **Mastar + y:** okumaya, görmeyi (okumağa eski).

---

## 12. Büyük harf

TDK maddelerinden linter'a uygun olanlar:

| id | seviye | kural (TDK) | regex | FP riski |
|---|---|---|---|---|
| BH-01 cümle başı | error | A: Cümle büyük harfle başlar | `(?:^|[.!?…]\s+)([a-zçğıöşü])` | Kısaltma sonrası (`vb. gibi`), `?..` sonrası, liste, kod; "iPhone", "e-posta" cümle başı → info |
| BH-02 rakamla başlayan cümlede sonraki kelime | warning | UYARI: Rakamla başlayan cümlede rakamdan sonraki kelime özel ad değilse küçük | `(?:^|[.!?]\s+)\d+['’]?\w*\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)` | Özel ad sonrası (2007 Türkiye…) |
| BH-03 cümle rakamla başlamaz | info | Sayılar 12: "Bir zorunluluk olmadıkça cümle rakamla başlamaz." | `(?:^|[.!?]\s+)\d` (liste/başlık hariç) | Tarih ile başlayan haber cümlesi |
| BH-04 dil adları | error | C.7 Dil adları büyük | `\b(türkçe|ingilizce|almanca|fransızca|arapça|rusça|ispanyolca|italyanca|japonca|çince|farsça|korece|yunanca|latince|kürtçe)\w*` | Hiçbiri (Turkish-aware case gerekir) |
| BH-05 millet adları | error | C.6 | `\b(türk|alman|ingiliz|fransız|rus|arap|japon|amerikalı|yunan)(ler|lar|lerin|ların)?\b` küçük | "türk kahvesi" → **Türk kahvesi** (C.26: yalnız özel ad büyük) |
| BH-06 belirli tarihte ay/gün | error | Ç: belirli tarih → büyük | `\b\d{1,2}\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\b` | yok denecek kadar az |
| BH-07 belirsiz ay/gün büyük | warning | Ç: "eylülün ikinci haftasında", "perşembe günleri" | `(?<!\d\s)(?<!\d)\b(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık|Pazartesi|Salı|Çarşamba|Perşembe|Cuma|Cumartesi|Pazar)\b(?!\s+\d)` cümle başı değilse | `Ekim ayında` → `ekim ayında`; `Cuma günleri` → `cuma günleri` | "Mayıs 2024'te" (ay+yıl): TDK örnekleri gün içeriyor; ay+yıl belirli dönem sayılır → hariç tut. Kişi adı "Cuma", "Mart", "Pazar"(soyadı), "Ekim" (nadir) |
| BH-08 para birimi | warning | UYARI: para birimleri küçük | `\b(Lira|Dolar|Avro|Euro|Kuruş|Sterlin|Yen)\b` cümle içi | "Türk Lirası" resmî adı ("Türk lirası" TDK'ye göre küçük; TL kısaltması büyük) |
| BH-09 dünya/güneş/ay | info | 11. UYARI: gezegen anlamı dışında küçük | `\bDünya\b` cümle içi | Gezegen anlamında doğru → info |
| BH-10 yön vs. Doğu/Batı kavramı | info | 12 | reviewer | — |
| BH-11 akrabalık adı | warning | UYARI: "Tülay ablama" | `\b[A-ZÇĞİÖŞÜ]\w+\s+(Abla|Ağabey|Abi|Teyze|Amca|Dayı|Hala|Yenge)(m|n|sı|si|mız|nız)?\b` | Lakap/unvan olarak (Dayı Kemal, Gül Baba) → isimden **önce** gelir; sonra gelenler küçük |
| BH-12 unvan + ad | info | 2: Kaymakam Erol Bey, Dr. Alâaddin | `\b(doktor|profesör|bakan|vali|başkan|cumhurbaşkanı|kaymakam|general)\s+[A-ZÇĞİÖŞÜ]` | "bakan ... (fiil)" yanlış eşleşme |
| BH-13 ve/ile/de/mi başlıkta | **warning** | C.21 UYARI: özel ad/başlıkta büyük yazılan kelimelerde **ve, ile, ya, veya, yahut, ki, da, de, mı/mi/mu/mü küçük yazılır** (tamamı büyükse büyük) | Başlık satırında `\s(Ve|İle|Ya|Veya|Yahut|Ki|Da|De|Mı|Mi|Mu|Mü)\s` | Satırın tamamı büyükse doğru |
| BH-14 İngilizce Title Case | info (stil) | **Dikkat:** TDK E: "ana başlıktaki kelimelerin tamamı, alt başlıktaki kelimelerin ise yalnızca ilk harfleri büyük" → kitap/makale alt başlıklarında Title Case **TDK'ye uygundur**. Görevdeki "Title Case = İngilizce sızıntı" varsayımı kural olarak doğru değil. Yalnızca **gövde metnindeki** (başlık olmayan) kalıplar ve aynı belgede tutarsız başlık stili işaretlenmeli | Markdown `^#{2,}\s` başlıklarda büyük harfle başlayan kelime oranı ≥ %80 ve ≥4 kelime → info | Belge bazlı tercih; web/blog'da cümle düzeni yaygın |
| BH-15 kurum adı tam ve asıl kastedilen | info | 18, 20: "Bu yıl ise Meclis…", "Kurumun…" | reviewer | — |
| BH-16 özel addan türeyen | error | 25: Türklük, Avrupalı, Konyalı büyük | `\b(türklük|avrupalı|asyalı|istanbullu|ankaralı|izmirli|müslüman|hristiyan)\w*` | Turkish-aware case |
| BH-17 "o" zamiri büyük | warning | UYARI | `(?<=[a-zçğıöşü,]\s)O\s` (cümle içi) | "O" harfi/kan grubu "0 Rh+" |
| BH-18 yer + tür adı | warning | 14: Ağrı Dağı, Van Gölü, Ege Denizi büyük; 14 UYARI: "Konya ili, Etimesgut ilçesi" küçük | `\b[A-ZÇĞİÖŞÜ]\w+\s+(dağı|gölü|denizi|nehri|ırmağı|boğazı|körfezi|adası|ovası|kanalı)\b` → büyük; `\b[A-ZÇĞİÖŞÜ]\w+\s+(İli|İlçesi|Köyü|Beldesi)\b` → küçük | "deniz kenarı" vb. |

Ek not, **İ/I dönüşümü**: AI çıktısında "Istanbul", "Izmir", "INGILIZCE" gibi noktasız I hataları görülebilir: `\b(Istanbul|Izmir|Ingiliz\w*|Iran|Isveç|Ispanya|Italya|Isviçre|Ilk|Için|Ise)\b` → error (Türkçe "Ilık, Irak, Isparta, Iğdır" doğru → listeyle sınırla).

---

## 13. Sayılar (TDK Sayıların Yazılışı)

Özet kurallar:
1. Sayılar harfle yazılabilir. Ama **saat, para, ölçü, istatistik** → rakam: 17.30'da, 1.500.000 lira, 25 kilogram.
2. Çok kelimeli sayılar **ayrı**: iki yüz, üç yüz altmış beş, bin iki yüz elli bir. (Bitişik yalnızca çek/senette ve iskambil oyun adlarında: altmışaltı, ellibir.)
3. **%25, ‰50**: işaret ile sayı arasında boşluk yok, işaret **önde**.
4. Romen rakamı: II. Dünya Savaşı, XX. yüzyıl, III. Selim.
5. Binlik nokta, ondalık virgül.
6. Sıra sayısı: "15." veya "15'inci"; ikisi birden değil.
7. **Üleştirme sayıları yazıyla**: 2'şer değil ikişer, 9'ar değil dokuzar, 100'er değil yüzer.
8. Bayağı kesir eki paydaya göre: 1/2'si, 4/8'i.
9. Bir zorunluluk olmadıkça cümle rakamla başlamaz.

| id | seviye | regex | yanlış → doğru | FP riski |
|---|---|---|---|---|
| SY-01 yüzde sonda | error | `\b(\d+(?:[.,]\d+)?)\s?%` | `25%`, `25 %` → `%25` | Kod, CSS (`width: 50%`) → kod bloklarını atla |
| SY-02 yüzde + boşluk | error | `%\s+\d` | `% 25` → `%25` | yok |
| SY-03 üleştirme rakamla | error | `\b\d+['’](şer|şar|er|ar)\b` | `2'şer`, `10'ar` → `ikişer`, `onar` | `4'er` (dörder); kısaltmada `MR'ar`? yok |
| SY-04 bitişik sayı | error | `\b(on|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan|yüz|bin|iki|üç|dört|beş|altı|yedi|sekiz|dokuz)(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|yüz|bin|milyon|milyar)\b` | `onbeş`, `ikiyüz`, `üçbin` → `on beş`, `iki yüz`, `üç bin` | iskambil "ellibir/altmışaltı/yirmibir" (oyun adı); "dokuzbin"? yok. Kelime içi eşleşmeyi `\b` engeller ama "Onbir" ad? Sınırlı |
| SY-05 sıra ekinde nokta+kesme | error | NK-01 | | |
| SY-06 sıra eki yanlış | error | `\b\d+['’](inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü)\b` → §10.3 tablosuyla karşılaştır | `2'inci` → `2'nci`; `3'ncü` → `3'üncü`; `6'ıncı` → `6'ncı` | yok |
| SY-07 "1." ve "birinci" karışık | info | — | — | — |
| SY-08 binlik nokta ve ondalık virgül | NK-04, NK-05 | | | |
| SY-09 rakam + yazı tekrarı | info | `\b\d+\s*\((?:bir|iki|üç|…)\w*\)` | Hukuki metin dışında gereksiz | — |
| SY-10 "x" çarpı | info | `\b\d+x\b` | `3x daha hızlı` → `3 kat daha hızlı` (çeviri kokusu) | Teknik notasyon (`1920x1080`, `4x4`) → yalnızca "daha/kat" bağlamında |

**Tarih ve saat:**
- TDK: `29.5.1453`, `29.X.1923`, `18/11/1969`, `29 Mayıs 1453`, `29 Ekim 1923 Salı`. Ay adı yazıyla yazılınca nokta yok.
- ISO `2024-05-29` teknik bağlamda kabul; düz metinde info.
- **İngilizce tarih sırası**: `(Ocak|…|Aralık)\s+\d{1,2},\s+\d{4}` → error: `Ekim 29, 1923` → `29 Ekim 1923`.
- `\b\d{1,2}(st|nd|rd|th)\b` → error (İngilizce sıra eki sızıntısı).
- Saat: TDK `09.15`, `13.00'te`, yazıyla "saat dokuzu beş geçe". `13:00` → info.
- Yüzyıl: `XX. yüzyıl` / `20. yüzyıl`; `20'nci yüzyıl` da doğru. `20.yy` → `20. yy.`.

---

## 14. Birleşik kelimeler, ayrı/bitişik yazım

### 14.1 TDK kuralı (özet)
**Bitişik:** ses düşmesi/türemesi olanlar (kaybolmak, affetmek, hissetmek, reddetmek, emretmek, sabretmek, şükretmek, zannetmek, seyretmek); anlam kayması (aslanağzı, hanımeli…); tasvirî fiiller (-ebilmek, -ivermek, -akalmak, -adurmak, -agelmek, -ayazmak: gelebilmek, alıvermek, uyuyakalmak); emir kalıpları (albeni, ateşkes, yapboz, kapkaç, örtbas); sıfat-fiil kalıpları (gökdelen, barışsever, hacıyatmaz, çokbilmiş); -dı kalıpları (gecekondu, imambayıldı); dedikodu, okuryazar, biçerdöver; **soyut alt/üst/üzeri**: bilinçaltı, gözaltı, olağanüstü, akşamüstü, suçüstü; başbakan, başkent, başrol; binbaşı, yüzbaşı; ağabey, hanımefendi; **biraz, birçok, birçoğu, birkaç, birkaçı, birtakım, herhangi, hiçbir, hiçbiri**; -ev: yayınevi, huzurevi; -hane/-name/-zade; -zede (depremzede); Farsça/Arapça kalıplar (gayrimenkul, suikast, fevkalade, inşallah, maşallah, velhasıl); İçişleri, Dışişleri, Genelkurmay, Yükseköğretim Kurulu.

**Ayrı:** etmek/olmak'lı ses değişmeyenler (**fark etmek, kabul etmek, terk etmek, hak etmek, yok olmak, var olmak, dans etmek, not etmek, yardım etmek**); hayvan/bitki türleri (köpek balığı, ateş böceği, çörek otu); renkler (açık mavi, gece mavisi); -r/-maz/-an sıfat-fiil tamlamaları (çalar saat, tükenmez kalem, uçan daire); yön sözleri yer adında (Orta Doğu, Uzak Doğu, Güneydoğu Anadolu); **dış, iç, sıra**: yasa dışı, olağan dışı, hafta içi, yurt içi, yanı sıra, peşi sıra; somut alt/üst: yer altı (yüzey), deri altı, su altı; **alt, üst, ana, ön, art, arka, yan, karşı, iç, dış, orta, büyük, küçük, sağ, sol, peşin, bir, iki, tek, çok, çift** + isim: alt kurul, ön söz, **ön yargı**, art niyet, arka plan, yan etki, karşı görüş, iç savaş, dış borç; durum/olay: **iş birliği, iş bölümü, baş ağrısı, yer çekimi, ana dili**; bilim/bilgi: **dil bilimi, dil bilgisi, ruh bilimi, toplum bilimi**; zaman: **hafta sonu, gece yarısı, hafta başı**; ikilemeler (yavaş yavaş, el ele, iç içe, baş başa, bire bir); deyimler (göz atmak, kulak asmak).

Not: "yeraltı" sözlükte ayrı anlamla var ("gizli ve yasa dışı": yeraltı dünyası); somut yüzey anlamında "yer altı". "bilinçaltı, gözaltı" (gözetim) bitişik.

### 14.2 Doğrulanmış ayrı/bitişik tablosu (sözlük API, 2026-11-05)

Ayrı yazılır (sözlükte madde, bitişik biçim yok): **her şey, her zaman, her biri, hiç kimse, pek çok, ya da, ara sıra, art arda, yanı sıra, bir an, bir an önce, bir arada, hafta sonu, iş birliği, ön yargı, ön söz, ön koşul, ön ek, son ek, öz geçmiş, dil bilgisi, eş zamanlı, eş anlamlı, olağan dışı, yasa dışı, son derece, söz konusu, fark etmek, hak etmek (hakketmek = kakmak, başka kelime), var olmak, ilgi çekici, arka plan, çevrim içi, yüksek lisans, ön lisans, ilk önce, bilim insanı, bakış açısı, öte yandan, ister istemez, kimi zaman, zaman zaman, şu hâlde, ne var ki, kaldı ki, yeter ki, nasıl ki, şöyle ki, belki de, hem de, her hâlde (= kesinlikle)**.

Bitişik: **birçok, birçoğu, birkaç, birtakım, biraz, birdenbire, birden, birbiri, herhangi, hiçbir, hiçbiri, herhâlde (= büyük ihtimalle), hâlihazırda, olağanüstü, altyapı, üstyapı, öngörü, öngörmek, vazgeçmek, seyretmek, sabretmek, şükretmek, zannetmek, öncelikle, dolayısıyla, yalnızca, kısacası, sonuçta, şimdilik, mademki, oysaki, hâlbuki, meğerki, sanki, çünkü, e-posta, e-ticaret**.

Sözlükte madde olarak bulunmayan ama TDK kuralına göre doğru olanlar: **bir şey, hiçbir şey, bir gün, demek ki, öyle ki, bir araya** (ayrı). API'nin "sonuç yok" demesi yanlış yazım anlamına gelmez.

| id | seviye | regex (yanlış) | doğru | FP riski |
|---|---|---|---|---|
| BK-01 | error | `\b([Hh])erşey\w*` | her şey | yok |
| BK-02 | error | `\b([Bb])irşey\w*`, `\bbişey\b`, `\bbişi\b` | bir şey | yok |
| BK-03 | error | `\b([Hh])içbirşey\w*` | hiçbir şey | yok |
| BK-04 | error | `\b([Hh])erzaman\b` | her zaman | yok |
| BK-05 | error | `\b([Hh])erbiri\w*`, `\bherbir\b` | her biri, her bir | yok |
| BK-06 | error | `\b([Hh])içkimse\w*` | hiç kimse | yok |
| BK-07 | error | `\b([Pp])ekçok\b` | pek çok | yok |
| BK-08 | error | `\b([Bb])ir\s+(çok|kaç|takım)\b` | birçok, birkaç, birtakım | "bir takım" = bir spor takımı ("bir takım kurduk") → **warning**; "bir çok" FP ≈ 0 |
| BK-09 | error | `\b([Hh])iç\s+bir(i|ini|inde|şey)?\b` | hiçbir, hiçbiri | yok |
| BK-10 | error | `\b([Hh])er\s+hangi\b` | herhangi | yok |
| BK-11 | error | `\b([Hh])erhangibir\b` | herhangi bir | yok |
| BK-12 | error | `\b([Ff])ark\s?ed(?=[eiaıdmyst])` bitişik: `\bfarket\w*`, `\bfarkın[dt]a\b` hariç | fark etmek, fark ettim | yok |
| BK-13 | error | `\b(terket|kabulet|yardımet|dansed|notet|sözet|ilanet|yokol|varol)\w*` | ayrı: terk etmek, kabul etmek… | "Varol" kişi adı (büyük harf → hariç), "varoluş" bitişik TDK? ("varoluş" sözlükte bitişik) → `varol(?!uş)` |
| BK-14 | error | `\b(kayıp\s+ol|affet|hisset|redd)` ayrı yazımı: `\b(kayıp olmak|af etmek|his etmek|red etmek|emir etmek|sabır etmek|şükür etmek|zan etmek|seyir etmek)\b` | kaybolmak, affetmek, hissetmek, reddetmek, emretmek, sabretmek, şükretmek, zannetmek, seyretmek | "kayıp olmak" ≈ "kaybolmuş durumda olmak" → warning |
| BK-15 | error | `\b(önyargı|işbirliği|haftasonu|özgeçmiş|dilbilgisi|eşzamanlı|eşanlamlı|olağandışı|yasadışı|yanısıra|arasıra|biraraya|önkoşul|önek|sonek|sonderece|çevrimiçi|ilgiçekici|bilimi?nsanı|öngörmek?)\w*` (öngör- hariç: doğru) | ayrı biçimler | "önek" (ön ek), "sonek" (son ek); "öngörü/öngörmek" **bitişik doğru**, listeden çıkar. "yasadışı" basında çok yaygın, TDK ayrı → error. "eşzamanlı" teknik metinde yaygın, TDK ayrı → error |
| BK-16 | error | `\b(alt yapı|üst yapı|olağan üstü|bilinç altı|göz altı(?:na|nda|ndan|ya)|akşam üstü|suç üstü)\b` | altyapı, üstyapı, olağanüstü, bilinçaltı, gözaltı, akşamüstü, suçüstü | "göz altı" (gözün altı, somut: "göz altı torbaları") → **warning** |
| BK-17 | error | `\b(bir\s+biri|bir\s+birine|bir\s+birini|bir\s+birlerine)\b` | birbiri, birbirine | yok |
| BK-18 | error | `\b(vaz\s+geç)\w*` | vazgeç- (soru ekli "vaz mı geçtin" hariç) | yok |
| BK-19 | warning | `\b(baş\s+bakan|baş\s+kent|baş\s+rol|baş\s+öğretmen)\b` | başbakan, başkent, başrol | yok |
| BK-20 | error | `\b(yayın\s+evi|huzur\s+evi|bakım\s+evi|basım\s+evi|kahve\s+hane|ders\s+hane|deprem\s+zede|kaza\s+zede)\b` | bitişik | "Yayın Evi" özel ad olarak tescilli olabilir |
| BK-21 ikileme bitişik/çizgili | error | `\b(\w{2,})-\1\b`, `\b(\w{3,})\1\b` (sözlük kontrolüyle) | `yavaş-yavaş`, `yavaşyavaş` → `yavaş yavaş` | Pekiştirmeli bitişikler (apaçık, masmavi, kapkara, büsbütün, paramparça, yemyeşil) ikileme değil → farklı desen; "çekiçekiç"? yok. `\1\1` deseninde "dede, nine, baba, kuku" gibi kökler → uzunluk ≥3 ve sözlükte yoksa |
| BK-22 pekiştirmeli ayrı | error | `\b(ap\s+açık|mas\s+mavi|kap\s+kara|yem\s+yeşil|sap\s+sarı|düm\s+düz|bom\s+boş|tam\s+tamam|para\s+parça)\b` | apaçık, masmavi, kapkara… | yok |
| BK-23 tasvirî fiil ayrı | error | `\b\w+(a|e|ı|i|u|ü|ya|ye|yı|yi|yu|yü)\s+(bil|ver|kal|dur|gel|yaz)(?:ir|di|miş|ecek|acak|iyor|ıyor|dı|mek|mak|meli|malı)\w*` | `gelebilir` ✓; `gele bilir` → `gelebilir` | "bile bile", "gide gide" ikileme; "ya bilir" → düşük; warning |
| BK-24 hâl/hal birleşikleri | info | `\bher\s?halde\b` | Bağlama göre: herhâlde (muhtemelen) / her hâlde (kesinlikle) | Anlam bağlamı → reviewer |

---

## 15. Düzeltme işareti (^)

TDK: (1) yazılışı aynı anlamı farklı kelimeleri ayırt etmek için: **âdet/adet, âlem/alem, âşık/aşık, hâl/hal, hâlâ/hala, şûra/şura**. (2) Arapça/Farsça kökenli kelimelerde ince g, k'den sonraki a, u: **dergâh, gâvur, karargâh, tezgâh, yadigâr, dükkân, hikâye, kâfir, kâğıt, Hakkâri, Kâzım, mahkûm, mezkûr, sükûn, sükût**; ince l sonrası özel adlarda: Halûk, Lâle, Elâzığ, Lâdik. (3) **Nispet î**: askerî, dinî, ilmî, resmî, millî; ek alınca da korunur: millîleştirmek, resmîlik.

Sözlük API'sinde düzeltme işareti göz ardı edilir (`zeka` → `zekâ`, `halbuki` → `hâlbuki`, `reklâm` → `reklam`). Bu yüzden API düzeltme işaretini doğrulamaz. Madde başı (`madde`) alanı ise TDK'nın tercih ettiği biçimi verir: **zekâ, yapay zekâ, hükûmet, hâlbuki, hâlihazırda, herhâlde, pekâlâ, reklam (şapkasız), mülakat (şapkasız), mesela (şapkasız)**.

| id | seviye | regex | doğru | FP riski |
|---|---|---|---|---|
| DZ-01 hâlâ | warning | `\bhala\b` + bağlam: zarf ("hala devam ediyor", "hala yok") | hâlâ | **hala** (babanın kız kardeşi) geçerli. Sezgi: ardından fiil/olumsuzluk → hâlâ; önünde iyelik ("halam", "Ayşe hala") → hala |
| DZ-02 zekâ | info | `\bzeka\w*` | zekâ, yapay zekâ | Gündelik yazımda şapkasız çok yaygın; **humanizer'da info** (fazla zorlamak da yapay kokar) |
| DZ-03 kâğıt/hikâye/dükkân/rüzgâr/kâr | info | `\b(kağıt|hikaye|dükkan|rüzgar|yadigar|tezgah|karargah|dergah|mahkum|sükut|sükun)\w*` | kâğıt, hikâye, dükkân, rüzgâr… | Aynı |
| DZ-04 nispet î | info | `\b(resmi|milli|dini|askeri|ilmi|siyasi|tarihi|edebi|ekonomi?ki|insani|fiili|kanuni|manevi|maddi|sanayi)\s+(kurum|bayram|tören|eğitim|bilgi|okul|görev|yazışma|tatil)` | resmî tatil, millî bayram | "resmi" = onun resmi; **bağlam: ardından isim gelirse sıfat → î** |
| DZ-05 hükûmet | info | `\bhükümet\w*` | hükûmet | Sözlükte madde hükûmet; "hükümet" yaygın; info |
| DZ-06 yanlış şapka | warning | `\b(reklâm|mülâkat|kâtil|hâyat|kâlp)\b` | reklam, mülakat, katil… | TDK güncel sözlük reklam/mülakat şapkasız |

Humanizer notu: Düzeltme işaretini **tutarlı** kullanmak, hiç kullanmamaktan daha "yazar" gibi görünür. Ama metinde bir yerde "hâlâ" diğer yerde "hala" (zarf anlamında) kullanmak tutarsızlık sinyalidir. Linter belge düzeyinde tutarlılık kontrolü yapmalı.

---

## 16. Sık yanlış yazılan kelimeler (sözlük API ile doğrulandı)

Format: `yanlış → doğru`. Doğru biçimin TDK sözlüğünde madde olduğu, yanlış biçimin madde olmadığı API ile doğrulandı (aksi not edildi). Regex: `\b(?:YANLIŞ)\w*\b` (Türkçe-duyarlı büyük/küçük harf; ek alabilir: `yanlızca`, `herkeze`).

### 16.1 error (sözlükte yok, kesin yanlış)
```
yanlız → yalnız            yalnış → yanlış           herkez → herkes
şöför → şoför              kirbik, kiprik → kirpik   süpriz, supriz → sürpriz
orjinal → orijinal         eşortman → eşofman        egsoz, eksoz → egzoz
meyva → meyve              traş → tıraş              entellektüel → entelektüel
kollej → kolej             profesyönel → profesyonel proğram → program
fotograf → fotoğraf        kontor → kontör           mötör → motor
tirbüşon → tirbuşon        yımırta → yumurta         kıravat → kravat
labaratuvar, laboratuar → laboratuvar               konservatuar → konservatuvar
antreman → antrenman       antreör → antrenör        eşkiya → eşkıya
klavuz → kılavuz           herhangibir → herhangi bir   yada → ya da*
şarz → şarj                mağazin → magazin         pantalon → pantolon
istifrağ → istifra         eczahane → eczane         mahsüs → mahsus
espiri → espri             inşaallah → inşallah      maşşallah → maşallah
sağol → sağ ol             kurdela → kurdele         tiren → tren
kıral → kral               pilaj → plaj              pisikoloji → psikoloji
sandoviç → sandviç         bisküvit → bisküvi        kilasör → klasör
çukulata → çikolata        eşarb → eşarp             dinazor → dinozor
fermuvar → fermuar         kuafor → kuaför           reportaj → röportaj
rotuş → rötuş              sezeryan → sezaryen       şovalye → şövalye
tellevizyon → televizyon   yogurt, yoğrut → yoğurt   mozayik → mozaik
mataryal → materyal        metod → metot             aksesuvar → aksesuar
akvaryüm → akvaryum        ambülans → ambulans       apartıman → apartman
anfi → amfi                ayakabı → ayakkabı        bilhasa → bilhassa
pekçok → pek çok           herbiri → her biri        kopye → kopya
mayanez → mayonez          mösyü → mösyö             nufüs → nüfus
otobus → otobüs            pardesü → pardösü         pogaça, poaça → poğaça
prezentabl → prezantabl    rasgele → rastgele        restorant → restoran
sörvis → servis            tasaruf → tasarruf        teferruvat → teferruat
tıraktör → traktör         zatürree → zatürre        pilaket → plaket
ünversite → üniversite     annons → anons            bilakiz → bilakis
deklanşor → deklanşör      ekspress → ekspres        eksersiz → egzersiz
egzema, ekzema → egzama    ekzotik → egzotik         enterasan → enteresan
fasülye → fasulye          feslegen → fesleğen       gardrop → gardırop
heycan → heyecan           hierarşi → hiyerarşi      kampanye → kampanya
katalok → katalog          kayısi → kayısı           kordinat → koordinat
kordinasyon → koordinasyon kordinatör → koordinatör  konsensus → konsensüs
kontejan → kontenjan       lahmacün → lahmacun       lökemi → lösemi
mitink → miting            müsvette → müsvedde       mütala → mütalaa
ofsait → ofsayt            parelel → paralel         parfum → parfüm
prespektif → perspektif    pisuar → pisuvar          prosedur → prosedür
radyotör → radyatör        rezarvasyon → rezervasyon sentral → santral
sempozium → sempozyum      siluet → silüet           spageti → spagetti
stad → stat                standard → standart       şampuvan → şampuan
teklonoji → teknoloji      tiatro → tiyatro          tualet → tuvalet
vantilator → vantilatör    vejeteryan → vejetaryen   zaafiyet → zafiyet
farketmek → fark etmek     varolmak → var olmak      biraraya → bir araya
önyargı → ön yargı         işbirliği → iş birliği    haftasonu → hafta sonu
özgeçmiş → öz geçmiş       dilbilgisi → dil bilgisi  eşzamanlı → eş zamanlı
olağandışı → olağan dışı   yasadışı → yasa dışı      yanısıra → yanı sıra
arasıra → ara sıra         önkoşul → ön koşul        çevrimiçi → çevrim içi
ilgiçekici → ilgi çekici   herşey → her şey          birşey → bir şey
diğil, deyil → değil       teşekürler → teşekkürler  insiyatif → inisiyatif
dolayısı ile → dolayısıyla  ard arda → art arda      oysa ki → oysaki
```
`*` "yada" sözlükte ayrı bir kelime (yağmur yağdırdığına inanılan taş). Bağlam neredeyse hep "ya da" olduğu için pratikte error.

Ek yaygın hatalar (TDK kuralından türetilmiş, API'de tek tek doğrulanmadı ama kural metniyle uyumlu): `yalnızlık` ✓, `kendiside` → `kendisi de`, `birtek` → `bir tek`, `hiçbirzaman` → `hiçbir zaman`, `okadar/bukadar/nekadar` → `o kadar/bu kadar/ne kadar`, `herkesde` → `herkeste`, `yanlızca` → `yalnızca`, `tabiki` → `tabii ki`, `tabi ki` → `tabii ki`.

### 16.2 warning (sözlükte var ama yönlendirme / tercih edilmeyen biçim)
API bu biçimleri "► / bkz." ile tercih edilen maddeye yönlendiriyor. Yanlış değil, ama TDK'nın tercih ettiği biçim öneriliyor:
```
makina → makine        mönü → menü           ahçı → aşçı
sarmısak → sarımsak    tekrardan → tekrar (sözlükte "tekrar tekrar" anlamına yönlendirilmiş; "yeniden" anlamında üslup hatası sayılır)
halbuki → hâlbuki      herhalde → herhâlde   halihazırda → hâlihazırda
pekala → pekâlâ        meselâ → mesela       reklâm → reklam
mülâkat → mülakat      hükümet → hükûmet (madde başı hükûmet)
zeka / yapay zeka → zekâ / yapay zekâ
bilim adamı ↔ bilim insanı (ikisi de madde; bilim insanı → bilim adamı'na yönlendiriyor; tercih meselesi)
rağmen ↔ karşın (rağmen → karşın'a yönlendirilmiş; ikisi de doğru)
```

### 16.3 Eş yazımlı / anlam ayrımı (FP riski yüksek, yalnızca reviewer veya bağlam kuralı)
| biçim | anlam | karışan | not |
|---|---|---|---|
| **tabi** | bağımlı ("kanuna tabi") | **tabii** (doğal, elbette) | "Tabi ki" → **Tabii ki** (error: `\b[Tt]abi\s+ki\b`) |
| **gurup** | güneşin batması | **grup** | `gurup` + (üye|toplantı|olarak|çalışması) → grup |
| **direk** | sütun | **direkt** (doğrudan) | `\bdirek\s+(olarak|bağlantı|etki|iletişim)\b` → direkt / doğrudan |
| **mütevazi** | paralel | **mütevazı** (alçakgönüllü) | insan sıfatı bağlamında → mütevazı |
| **hala** | babanın kız kardeşi | **hâlâ** | DZ-01 |
| **hal** | çözme; meyve hâli | **hâl** (durum) | info |
| **kar** | yağış | **kâr** (kazanç) | `\bkar\s+(marjı|payı|oranı|elde|amacı)` → kâr |
| **adet** | sayı | **âdet** (gelenek) | info |
| **yeraltı** | gizli, yasa dışı | **yer altı** (yüzey altı) | anlam |
| **her hâlde** | kesinlikle | **herhâlde** (muhtemelen) | anlam |
| **akordeon → akordiyon** | akordeon sözlükte akordiyon'a yönlendiriliyor | — | warning (§16.2 türü) |
| **hakketmek** | kakmak (oymak) | **hak etmek** | "hakkettin" → "hak ettin" (error; anlam bağlamı kesin) |
| **bende/sende/onda** | bulunma | ben de / sen de | DD-05 |
| **birde** | saat birde | bir de | warning |

---

## 17. AI / İngilizce kaynaklı noktalama sızıntıları (humanizer'a özel)

TDK kuralına dayananlar **error**. Üslup tercihi olup AI'yı ele verenler **info/metrik**.

| id | sinyal | TDK dayanağı | seviye | tespit |
|---|---|---|---|---|
| AI-01 | Cümle içi em dash `—` | Uzun çizgi yalnız satır başı konuşma | error | CZ-01 |
| AI-02 | Oxford comma `, ve` | Virgül UYARI: ve/veya/yahut öncesi virgül yok | error | VR-01 |
| AI-03 | `25%`, `3.5 milyon`, `1,000` | Sayılar 4, 7, 8 | error/warning | SY-01, NK-04, NK-05 |
| AI-04 | `Ekim 29, 2024`, `1st`, `2nd` | Tarih/sayı kuralları | error | §13 |
| AI-05 | `Türkçe'de`, `Türk'ler`, `Microsoft Şirketi'nin`, `Üniversitesi'nde` | Kesme UYARI'ları | error | KS-01..03 |
| AI-06 | `2024'de`, `TDK'ya` | Okunuş esaslı ek | error/warning | §10.3 |
| AI-07 | Başlıkta `Ve`, `İle`, `İçin`? | C.21: ve/ile/ki/da/de/mi küçük | warning | BH-13 ("İçin" kuralda yok; Title Case başlıkta "için" büyük yazılabilir) |
| AI-08 | Title Case gövde dışı başlık enflasyonu | E maddesi alt başlıkta Title Case'e izin veriyor | info | BH-14 |
| AI-09 | `"..."` ile her ikinci terimi tırnaklama (scare quotes) | Tırnak 2: "özel olarak vurgulanmak istenen" söz → seyrek olmalı | info (yoğunluk) | TR-03 |
| AI-10 | Noktalı virgül enflasyonu | Noktalı virgül yalnız 3 durumda | info | NV-02 |
| AI-11 | İki nokta ile "Sonuç: …", "Not: …" kalıpları, `**Kalın:**` madde başları | İki nokta 1–2 kullanımlarına uygun ama sıklık yapay | info (metrik) | `(?m)^\**[A-ZÇĞİÖŞÜ][\w ]{1,25}\**:` sayısı |
| AI-12 | `ve/veya` | — (çeviri) | info | EC-01 |
| AI-13 | Paragraf başı bağlaç + virgül (`Ancak,`, `Ayrıca,`, `Sonuç olarak,`) | TDK zorunlu kılmıyor | info (yoğunluk) | VR-08 |
| AI-14 | `"` düz tırnak + `’` kıvrık kesme karışık | — | info | TR-04 |
| AI-15 | Ünlem enflasyonu, `!` pazarlama | Ünlem: duygu/seslenme | info | UN-09 |
| AI-16 | `…` yerine `...` | Ikisi de olur | yok (normalizasyon) | UN-04 |
| AI-17 | `İ`/`I` hataları (`Istanbul`, `INGILIZCE`) | Alfabe | error | §12 notu |
| AI-18 | Liste maddelerinin sonunda tutarsız nokta | F: "Açıklayıcı yazı cümle niteliğinde değilse sonuna nokta konmaz" (görsel açıklamaları için; listeye uyarlanabilir) | info | Madde fiilsizse nokta yok, cümleyse nokta |
| AI-19 | Ara söz için `—…—` yerine `(…)` aşırı kullanımı | Yay ayraç 1 | info | paragraf başına ayraç > 2 |
| AI-20 | `x2`, `3x` | — (İngilizce notasyon) | info | SY-10 |

**Kıvrık tırnaklar (smart quotes) AI sinyali değildir**: TDK kendi metninde “ ” ‘ ’ ve ’ kullanıyor. İngilizce humanizer'lardaki "smart quote → straight quote" kuralı Türkçeye **taşınmamalı**.

---

## 18. Prior art: bilinen hatalı üçüncü taraf kuralları

`Denomas/Turkce-yazim-denetimi` (Vale) kurallarında TDK'ya **aykırı** maddeler var. Bunlar kopyalanmamalı:

| dosya | hatalı kural | TDK |
|---|---|---|
| `KiEki.yml` | `mademki → madem ki`, `meğerki → meğer ki`, `sanki → san ki` | **mademki, meğerki, sanki bitişik** (ki sayfası) |
| `BitisikYazim.yml` | `nasıl ki → nasılki`, `öyle ki → öyleki`, `şöyle ki → şöyleki` | **ayrı** (ki bağlacı ayrı; sözlükte "nasıl ki", "şöyle ki" ayrı madde) |
| `DeDABaglaci.yml` | `bende[^n]`, `sende[^n]`, `onda[^n]`, `bizde[^n]`… | Bulunma hâli olarak doğru biçimler → çok yüksek FP |
| `*.yml` | `ignorecase: true` | Go/Vale büyük/küçük harf katlaması Türkçe I/ı/İ/i'yi yanlış eşler |
| link alanları | `/de-da-baglaci/`, `/ki-baglaci/`, `/noktalama-isaretleri/` | 404; doğru slug'lar §0'da |

İşe yarar kısımlar: `YanlisTurkce.yml` swap listesi (yanlız, yalnış, süpriz, şarz, espiri, insiyatif, diğil/deyil, teşekürler), Plaza/Akademik sadeleştirme listeleri (bunlar dosya 07'nin alanı).

`akana-core` (Rust) iyi bir fikir veriyor: bulunma ekinin yanlışlıkla ayrılması için kök listesi (`hakkın, arasın, konusun, tarafın, sayesin, karşısın…` + `da/de`) → DD-04'e alındı. Ama `bende/sende/birde` birleşmelerini koşulsuz düzeltmesi aynı FP sorununu taşıyor.

---

## 19. Uygulama notları (linter yazarı için)

1. **Türkçe büyük/küçük harf**: Python `str.lower()` "I" → "i" yapar (Türkçede "ı" olmalı), "İ".lower() → "i̇" (birleşik nokta). JS `toLowerCase()` locale'siz aynı sorunu taşır, `toLocaleLowerCase('tr-TR')` kullanın. Regex'te `re.IGNORECASE` kullanmayın. Açık sınıflar yazın: `[Iı]`, `[İi]`, ya da önce Türkçe kurallarla katlayın: `s.replace('I','ı').replace('İ','i').lower()`.
2. **`\b` sınırı**: Python 3 `re` Unicode'da `ç, ğ, ı, ö, ş, ü` harflerini `\w` sayar. JS'de **`u` bayrağı olmadan** `\b` ve `\w` ASCII'dir, `/\bçok\b/` başarısız olur. JS'de `(?<![\p{L}])…(?![\p{L}])` + `u` bayrağı kullanın.
3. **Kesme işareti**: Her kuralda `['’]` (U+0027 ve U+2019). Ayrıca `‘` (U+2018) ve `´` (U+00B4) yanlış kesme olarak normalize edilebilir.
4. **Atlanacak bölgeler**: kod blokları (```` ``` ````), satır içi kod, URL, e-posta, dosya yolları, Markdown link hedefleri, HTML etiketleri, YAML front matter. Aksi hâlde SP-*, NK-*, SY-01, UN-02 sürekli tetiklenir.
5. **Cümle bölme**: kısaltma listesi gerekir (Dr., Prof., vb., vs., No., s., sf., Alb., Cad., Sok., Mah., T.C., A.Ş., Ltd. Şti.) ve sıra noktası (`15. yüzyıl`). Bunlar olmadan BH-01 ve BH-02 FP üretir.
6. **Özel ad sözlüğü**: KS-06/KS-07/BH-* için il/ilçe, ülke, yaygın kişi adları ve marka listesi (örn. 81 il + 200 ülke + ilk 500 ad). İnce-l istisnaları (Kemal, Hilal, Celal, Bilal, Lale, Meral, Jale…) ayrı liste.
7. **Seviye politikası (humanizer bağlamı)**: error → otomatik düzeltilebilir (yalnız deterministik ve FP≈0 olanlar: VR-01, CZ-01, UN-01, SY-01/02/03, NK-01, KS-01..04, BK-01..11, MI-03, KI-02, DD-01/02, §16.1 listesi). warning → reviewer'a öneri. info → metrik/yoğunluk (AI-*).
8. **Morfoloji**: MI-01, DD-03, DD-05, VR-05 için Zemberek (Java) veya `zeyrek` (Python) gibi bir çözümleyici FP'yi ciddi düşürür. Deterministik linter'da bu kurallar warning kalmalı.
9. **Sözlük API**: `https://sozluk.gov.tr/gts?ara=` yanıtı başında `\n` olabilir, `strip()` gerekli. Bulunamayınca `{"error":"Sonuç bulunamadı"}` döner. Düzeltme işaretini yok sayar. Çok kelimeli kalıpların bir kısmı madde değildir (bir şey, demek ki). Rate limit belirsiz, 8 paralel istekte sorun çıkmadı. Tek seferde timeout yaşanabiliyor. **Çalışma anında değil, build sırasında** bir kez çekilip statik liste olarak gömülmeli.
10. **Test korpusu**: TDK sayfalarındaki örnek cümleler (bu dosyada alıntılananlar) "doğru" pozitif test seti olarak kullanılmalı. Linter TDK'nın kendi örneklerinde **sıfır** uyarı vermeli. Ham metinler scratchpad'de `tdk/*.txt` olarak indirildi; WP API ile yeniden üretilebilir: `curl 'https://tdk.gov.tr/wp-json/wp/v2/posts?categories=27&per_page=50&_fields=slug,link,content'`.

---

## 20. Hızlı başvuru: en yüksek değerli 25 deterministik kural

| # | id | regex (kısaltılmış) | düzeltme |
|---|---|---|---|
| 1 | CZ-01 | `(?<=\S)\s*—\s*(?=\S)` (satır başı değil) | `, ` / `(…)` / `-…-` |
| 2 | VR-01 | `,\s+(ve|veya|yahut|ya da)\s` | virgülü sil |
| 3 | UN-01 | `\.{4,}` | `…` |
| 4 | UN-02 | `(?<![.?!])\.\.(?!\.)` | `…` |
| 5 | UN-03 | `([?!])(\.\.\.|…)` | `\1..` |
| 6 | SY-01 | `(\d+(?:,\d+)?)\s?%` | `%\1` |
| 7 | SY-03 | `\d+['’](şer|şar|er|ar)\b` | yazıyla üleştirme |
| 8 | NK-01 | `\d+\.['’]?(inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü)` | noktayı sil |
| 9 | KS-01 | `(Kurumu|Bakanlığı|Üniversitesi|…)['’]` | kesmeyi sil, ünlü uyumu |
| 10 | KS-02 | `[A-ZÇĞİÖŞÜ]\w+(ça|çe|ca|ce)['’]` (ad listesi hariç) | kesmeyi sil |
| 11 | KS-03 | `[A-ZÇĞİÖŞÜ]\w*['’](lar|ler|lı|li|lu|lü|lık|lik|cı|ci|çı|çi)` | kesmeyi sil |
| 12 | KS-04 | `(vb|Dr|Prof|No)\.['’]` | kesmeyi sil |
| 13 | §10.3 | `\d+['’](de|da|te|ta|…)` uyum tablosu | doğru ek |
| 14 | KY-01 | `[A-Z]{2,}['’](ya|nın|da|…)` + son harf ünsüz + harf okunan | ince ek |
| 15 | DD-01 | `\b\w+[pçtkfsşh]\s+(te|ta)\b` (ta-zarfı hariç) | de/da |
| 16 | DD-02 | `\b(yada|hemde|dahada|pekde|hiçde)\b` | ayır |
| 17 | DD-04 | `\b(hakkın|arasın|konusun|…)\s+(da|de)\b` | birleştir |
| 18 | KI-01 | `\b(demek|kaldı|yeter|nasıl|öyle|şöyle)ki\b` | ayır |
| 19 | KI-02 | `\b(oysa|hâlbu|halbu|madem|meğer)\s+ki\b` | birleştir |
| 20 | KI-04 | `\b(bugün|dün|yarın|akşam|şimdi)\s+ki\b` | bugünkü/dünkü/şimdiki |
| 21 | MI-01 | çekimli fiil + `(mı|mi|mu|mü)(sın|…)?` bitişik | ayır |
| 22 | BK-01..11 | herşey, birşey, hiçbirşey, herzaman, pekçok, bir çok, hiç bir, herhangibir | §14.2 |
| 23 | BH-04 | küçük harfle dil adları | büyük harf |
| 24 | BH-06 | `\d{1,2}\s+(ocak|…|aralık)` | ay adı büyük |
| 25 | `\b[Tt]abi\s+ki\b` | | tabii ki |
