# 05. Türkçe bağlaç, edat ve söylem belirleyicileri envanteri

Amaç: Türkçe humanizer için (skill + deterministik linter) bağlantı öğelerinin işlevine göre gruplanmış, kayıt (register), yazım/noktalama, nüans ve doğal örnek içeren kapsamlı listesi. Her grupta LLM'lerin fazla kullandığı ve neredeyse hiç kullanmadığı öğeler işaretli.

İşaretler:
- **[LLM+]**: LLM Türkçesinde aşırı sık geçiyor (çoğu İngilizce connective'in kalkı). Linter'da yoğunluk uyarısı adayı.
- **[LLM-]**: Usta yazarda doğal, LLM'de nadir. Rewrite önerisi olarak sunulacak.
- Kayıt: **R** resmî/yazı dili, **G** gündelik/konuşma, **E** edebî, **ESK** eskimiş/Osmanlıca (ironik ya da arkaik tonda kullanılır), **N** nötr (her kayıtta).

Kaynak notu: Yazım ve noktalama kuralları TDK Yazım Kılavuzu'ndan alındı (aşağıda URL'ler). LLM sıklığına dair Türkçe için yayımlanmış ölçümlü bir korpus çalışması bulamadım (bkz. §15). [LLM+] ve [LLM-] işaretleri bu yüzden gözleme dayalı sezgisel (heuristic) işaretler. Bir eşiğe bağlamadan önce kendi örneklemimizle ölçülmeleri gerekiyor.

---

## 0. TDK'nin bağlayıcılarla ilgili kesin kuralları (linter için birincil kaynak)

### 0.1 Bağlaç olan "ki" (TDK, "Bağlaç Olan ki'nin Yazılışı")
URL: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-kinin-yazilisi/

- Bağlaç olan *ki* **ayrı** yazılır: *bilmem ki, demek ki, kaldı ki*.
  - TDK örnekleri: "Türk dili, dillerin en zenginlerindendir; yeter ki bu dil, şuurla işlensin." (Atatürk) / "Geçmiş zaman olur ki hayali cihan değer."
- Kalıplaşmış şu yedi sözcük **bitişik** yazılır: **belki, çünkü, hâlbuki, mademki, meğerki, oysaki, sanki**. *Çünkü* sözcüğünde ek küçük ünlü uyumuna uyar (*çünki* değil).
- Şüphe ve pekiştirme bildiren *ki* de ayrı yazılır: "Ders bitti, zil çaldı mı ki?", "Seni öyle göreceğim geldi ki."
- Ayrı yazılan kalıplaşmış ki'ler (bitişik yazılmaz): *yeter ki, demek ki, kaldı ki, bilmem ki, öyle ki, şöyle ki, ne var ki, şu var ki, diyelim ki, farz et ki, tut ki, ola ki, olur ki, neyse ki, illa ki, hele ki (G), sanırım ki (eskice), unutma ki, inanın ki, öyle ki, o kadar ki, değil ki, ne zaman ki, nerede ki, her ne kadar … -sa da* (ki yok).
- **Ek olan -ki** (ilgi eki, *-deki, yarınki, benimki*) bitişik yazılır. Bağlaç ki ile karıştırma: ek olan *-ki* vurgulu, bağlaç ki vurgusuzdur (Türk Dili dergisi; Farsça kökenli ki üzerine: https://tdk.gov.tr/wp-content/uploads/2020/01/9_Hamza-Z%C3%BClfikar-_-FARS%C3%87A-K%C3%96KENL%C4%B0-K%C4%B0-BA%C4%9ELACINI-ADLANDIRMA-_-6.pdf).
- İstisna olarak *-ki* eki ünlü uyumuna girer: *bugünkü, dünkü, öbürkü* (ek). Bağlaç ki hiçbir zaman uyuma girmez.

**Linter regex adayları (deterministik, yüksek güven):**
| Yanlış | Doğru |
|---|---|
| `oysa ki` | `oysaki` (ya da `oysa`) |
| `halbu ki`, `hâlbu ki`, `halbuki ki` | `hâlbuki` |
| `madem ki` | `mademki` (ya da `madem`) |
| `meğer ki` (koşul anlamında) | `meğerki` *(dikkat: şaşma bildiren "meğer … -mış" ayrı bir öğe, ki almaz)* |
| `san ki`, `sanki ki` | `sanki` |
| `bel ki` | `belki` |
| `çünki`, `çün ki`, `çünkü ki` | `çünkü` |
| `demekki` | `demek ki` |
| `kaldıki` | `kaldı ki` |
| `yeterki` | `yeter ki` |
| `neyseki` | `neyse ki` |
| `illaki` | `illa ki` |
| `diyelimki` | `diyelim ki` |
| `öyleki`, `şöyleki` | `öyle ki`, `şöyle ki` |
| `ne varki` | `ne var ki` |

Not: Güncel TDK *hâlbuki* yazımında şapka kullanıyor. Linter şapkasız *halbuki* için yalnızca "info" seviyesinde uyarmalı, çünkü şapkasız yazım yaygın ve kabul görüyor.

### 0.2 Bağlaç olan "da/de" (TDK, "Bağlaç Olan da, de'nin Yazılışı")
URL: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-da-denin-yazilisi/

- Bağlaç *da/de* **ayrı** yazılır ve önceki sözcüğün son ünlüsüne uyar (*ben de, sen de, o da, onlar da*).
- Sert ünsüzden sonra bile **ta/te olmaz**: "Gidip de gelmemek var" (*gidip te* yanlış).
- **Ya da** iki ayrı sözcük (*yada* yanlış).
- Kesme işaretiyle bağlanmaz: *Ayşe de geldi* (*Ayşe'de geldi* yanlış; o yazım bulunma hâli anlamına gelir).
- Ayrım testi: *de* cümleden çıkarıldığında anlam bozulmuyorsa (yalnızca "dahi/ayrıca" anlamı kayboluyorsa) bağlaçtır, ayrı yazılır. Anlam bozuluyorsa bulunma ekidir, bitişik yazılır. Bulunma eki için TDK sayfası: https://tdk.gov.tr/icerik/yazim-kurallari/bulunma-durumu-eki-da-de-ta-tenin-yazilisi/

**Linter regex adayları (yüksek frekanslı hatalar):** `belkide→belki de`, `yinede→yine de`, `genede→gene de`, `hemde→hem de`, `bende geldim→ben de geldim` (bağlamsal), `sende→sen de` (bağlamsal), `bizde→biz de` (bağlamsal), `ama da`, `veya da` (gereksiz), `yada→ya da`, `ya-da→ya da`, `ki de`, `veyahutta→veyahut da`, `üstelikte→üstelik de`, `hattâ da` (gereksiz).

### 0.3 Virgül ve bağlaçlar (TDK Yazım Kılavuzu, Noktalama İşaretleri)
URL: https://yazim.tdk.gov.tr/content/09-noktalama-isaretleri.html (ayrıca https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/)

TDK uyarıları (birebir kurallar):
1. "Metin içinde **ve, veya, yahut, ya … ya** bağlaçlarından önce de sonra da virgül konmaz."
2. Tekrarlı bağlaçlarda virgül konmaz: **hem … hem, ya … ya, gerek … gerek, ister … ister**. TDK örnekleri: "Hem gider hem ağlar.", "Ne kız verir ne dünürü küstürür." (*ne … ne* de bu kurala uyuyor).
3. Pekiştirme ve bağlama görevindeki **da/de**'den sonra virgül konmaz.
4. "-ınca" anlamındaki **mı/mi**'den sonra virgül konmaz ("Geldi mi kimseyi dinlemez").
5. **Şart ekinden** sonra virgül konmaz.
6. Metin içinde **zarf-fiil** almış sözcüklerden sonra virgül konmaz. Ancak art arda sıralanan zarf-fiillerin arasına konur (kural 13).
7. Virgül **sıralı cümleleri** ayırır (kural 2). İç virgüllü sıralı cümleler noktalı virgülle ayrılır.
8. *Evet, hayır, peki, tamam, olur, elbette* gibi cevap ve onay sözlerinden sonra virgül konur: "Peki, gideriz."
9. Ara söz ve ara cümleler virgülle (ya da kısa çizgiyle) ayrılır.
10. Bir sözcüğün sonrakine bağlı olmadığını göstermek ve yanlış anlamayı önlemek için virgül konur. Kullanıldığı bağlama göre bu kural cümle başı bağlayıcıları da kapsayabilir.

TDK'nin **düzenlemediği** konular (linter bunlarda hata vermemeli, en fazla stil önerisi yapmalı):
- Cümle başındaki *Ama / Fakat / Ancak / Oysa / Yani / Örneğin / Kısacası / Öte yandan*'dan sonra virgül konup konmayacağı. TDK örneklerinde *Ama* ve *Fakat*'tan sonra genelde virgül yok. Çok sözcüklü söylem belirleyicilerden sonra (*Öte yandan, Bununla birlikte, Kısacası, Sözün kısası,*) yayın pratiğinde virgül yaygın.
- Bağlaç *ki*'den önce ya da sonra virgül (kılavuzda kural yok). TDK örneği "Seni öyle göreceğim geldi ki." virgülsüz.
- *Ama, fakat, ancak, lakin, çünkü* öncesinde noktalı virgül. 2000 kılavuzunda vardı, 2005'te kaldırıldı, 2012 ve sonrasında yok. Kaynak: dergipark makalesi https://dergipark.org.tr/en/download/article-file/70399. Linter `; ama` / `; çünkü` gördüğünde "eski kural, virgül yeterli" diye stil uyarısı verebilir.
- 2025 Türk Dili incelemesine göre "ikilemeler arasına virgül konmaz" ve "vb.'den önce virgül konmaz" eski kılavuzlarda vardı, güncel metinde yok: https://tdk.gov.tr/wp-content/uploads/2025/04/Belgin-Tezcan-Aksu_-E-_-Gelecege-Isik-Yazim-Sorunlarina-Gecmisten-Cozumler-_12.pdf

**Linter regex adayları (TDK-kesin):** `, ve `, ` ve, `, `, veya `, `, yahut `, `hem [^.]+?, hem`, `ne [^.]+?, ne `, `ya [^.]+?, ya `, `ister [^.]+?, ister`, `gerek [^.]+?, gerek`, `\b(de|da), ` (bağlaç sonrası virgül; uzun ara söz istisnası için düşük güvenle işaretle).

---

## 1. Ekleme ve sıralama

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **ve** | N | Öncesinde ve sonrasında virgül yok (TDK). Sıralamada yalnızca son öğeden önce. | En nötr ekleme bağlacı. Cümle başında ("Ve…") yazınsal ya da gazeteci vurgusu verir. Arka arkaya çok "ve" kullanılması çeviri kokar. | "Kapıyı kapadı, ışığı söndürdü ve uzandı." |
| **ile** | N | Bağlaç olduğunda ayrı yazılır, ek olduğunda bitişik (*kalemle*). Önceki öğe büyük harfle başlıyorsa *ve* ile değiştirilebilir. | Yalnızca isimleri bağlar, cümleleri bağlamaz. Test: "ve" konabiliyorsa bağlaçtır. | "Ali ile Veli kavga etti." |
| **de / da** | N | Ayrı yazılır, sonrasında virgül yok (§0.2). | "dahi, ayrıca" anlamı verir. Ekleme için en doğal Türkçe araç budur ve *ayrıca*'nın yerine geçer. | "Kitap da getirdim." |
| **hem … hem (de)** | N | Virgül yok. İkinci öğede *de* isteğe bağlı. | İki öğeyi eşit ağırlıkla vurgular. | "Hem yorgun hem aç." |
| **gerek … gerek(se)** | R | Virgül yok. | Resmî ve sıralayıcı ton. | "Gerek öğrenciler gerekse veliler itiraz etti." |
| **ayrıca** **[LLM+]** | R/N | Cümle başında çoğu zaman virgüllü. | İngilizcedeki *also/additionally* karşılığı. LLM'ler neredeyse her paragrafın başında kullanıyor. | "Ayrıca, sistem güncellenmiştir." → daha doğal: "Sistem de güncellendi." |
| **ek olarak / buna ek olarak** **[LLM+]** | R | Virgülle | Doğrudan *in addition* kalkı. İnsan yazısında seyrek, resmî raporda bile ağır durur. | → "…de", "üstelik", "bir de" |
| **bunun yanı sıra / -ın yanı sıra** **[LLM+]** | R | | Edat öbeği olarak meşru, ama LLM bunu sıralayıcı bağlaç gibi kullanıyor. | "Maaşın yanı sıra yol parası da veriliyor." (doğal kullanım) |
| **aynı zamanda** **[LLM+]** | N | | Gerçek anlamı "eş zamanlı". LLM bunu *also* yerine kullanıyor ("X aynı zamanda Y'dir"). | "Hem öğretmen hem yazar." ile değiştir. |
| **dahası** **[LLM+]** | R/E | Virgülle | *Moreover* kalkı. Az kullanılırsa güçlü, LLM'de ise klişe. | → "üstelik", "hatta", "kaldı ki" |
| **üstelik** **[LLM-]** | N | Cümle başında virgüllü ya da virgülsüz. | Eklenen bilgi öncekinden daha ağır. Hafif sitem ya da şaşkınlık taşır. | "Geç kaldı, üstelik özür de dilemedi." |
| **üstüne üstlük** **[LLM-]** | G | | "Bir de bu" diye yakınma tonu. | "Yağmur yağdı, üstüne üstlük otobüs kaçtı." |
| **bir de** **[LLM-]** | G/N | Ayrı. | Listeye son bir öğe ekler, çoğunlukla yakınma ya da ironi taşır. | "Bir de utanmadan hesap soruyor." |
| **bir yandan … bir yandan (da) / bir taraftan … diğer taraftan** | N | | Eş zamanlı iki eylemi anlatır. | "Bir yandan yemek yapıyor, bir yandan telefonla konuşuyordu." |
| **öncelikle, ilk olarak, ikinci olarak, son olarak** **[LLM+]** | R | | Madde madde yazma refleksinin düzyazıya taşınmış hâli. | → "Önce…, sonra…, en sonunda…" ya da sıralı cümle |
| **önce … sonra … en sonunda / derken** | N | | Doğal anlatım sırası. | "Önce bir sessizlik oldu, derken kapı çalındı." |
| **her şeyden önce** | N | | Öncelik vurgusu. LLM'de açılış klişesi olarak fazla kullanılıyor. | |
| **keza** | R/ESK | | "Aynı şekilde". Resmî yazıda ve hukuk dilinde yaşıyor. | "Keza ikinci madde de iptal edildi." |
| **-ıp / -ıp da** (zarf-fiil) **[LLM-]** | N | Ek, sonrasında virgül yok. | Türkçenin asıl sıralama aracı. İki cümleyi bağlaçsız bağlar. | "Eve gidip yattı." (LLM: "Eve gitti ve ardından yattı.") |
| **-arak / -erek** | N | | Tarz ve sıralama bildirir. LLM bunu fazla ve ağır kullanır ("…-arak … sağlanmaktadır"). | |
| **-dıktan sonra, ardından** **[LLM+ "ardından"]** | N | | | "Yemeği yedikten sonra çıktık." |
| **sıralı cümle (virgülle bağlaçsız)** **[LLM-]** | N/E | Virgül (TDK kural 2) | Bağlaçsız art arda dizilen kısa yargılar. Usta yazarın ritim aracı. | "Kalktı, giyindi, çıktı." |

---

## 2. Karşıtlık ve kısıtlama (en zengin grup, humanizer için en kritik)

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **ama** | N (G'ye yakın) | Cümle ortasında öncesinde virgül olağan. Cümle başında virgülsüz. | En nötr karşıtlık bağlacı. Pekiştirme anlamı da var: "Güzel ama çok güzel." Ayrıca koşul ya da sitem: "Ama söz verdin!" | "Yorgunum ama gelirim." |
| **fakat** | N/R | ama ile aynı | *ama*'dan biraz daha resmî ve keskin. | "Aradım, fakat açmadı." |
| **lakin** | ESK/E/G-ironik | TDK: *lakin*. | Eskice. Bugün edebî ya da şakacı tonda kullanılır. | "Lakin işler umduğu gibi gitmedi." |
| **ancak** | R | Cümle başında çoğu kez virgüllü (TDK düzenlemiyor). | Resmî karşıtlık. Ayrıca "yalnızca" ("ancak o bilir") ve "ancak -ınca" (zaman) anlamları var. LLM'de *however* karşılığı olarak sık. | "Başvurular alındı. Ancak eksik belgeler var." |
| **yalnız** **[LLM-]** | G/N | Virgülle | Yumuşak kısıtlama ("tek şu var"). | "Gelirim, yalnız biraz geç kalırım." |
| **oysa / oysaki** **[LLM-]** | N/E | *oysaki* bitişik (TDK). Cümle başında ya da virgülden sonra gelir. | Beklenen ya da önceden bilinen durumla gerçek durum arasındaki çelişki. Çoğu zaman sitem ve hayal kırıklığı taşır. *ama*'dan daha anlatıcı. | "Herkes onu suçladı. Oysa o gece evde bile değildi." |
| **hâlbuki** **[LLM-]** | N/G | Bitişik, TDK şapkalı yazar (*hâlbuki*). | *oysa* ile hemen hemen eş anlamlı. Konuşmada daha sık, sitem tonu daha güçlü. | "Hâlbuki ben sana söylemiştim." |
| **ne var ki** **[LLM-]** | E/R | Ayrı. Ardından virgül isteğe bağlı. | Anlatıda beklenmedik engel. Hikâye anlatıcı tonu. | "Plan kusursuzdu. Ne var ki kimse saati hesaba katmamıştı." |
| **ne ki** | E | Ayrı | *ne var ki*'nin kısa, edebî hâli. | "Ne ki talih yüzüne gülmedi." |
| **gelgelelim** **[LLM-]** | E/G | Bitişik | "Ne var ki" anlamı, hafif ironik ve anlatıcı. | "Her şeyi düşünmüştü. Gelgelelim yağmuru düşünmemişti." |
| **şu var ki / şu da var ki** **[LLM-]** | G/N | Ayrı | Konuşmacının kendi itirazı ya da çekincesi. | "İyi fikir. Şu var ki bütçe yetmez." |
| **mamafih / maamafih** | ESK | TDK: *mamafih* | Osmanlıca "bununla birlikte". Bugün ironik ya da arkaik tonda. | "Mamafih, kimse bir şey demedi." |
| **bununla birlikte / bununla beraber** **[LLM+]** | R | Virgülle | *However/nevertheless* kalkı. LLM Türkçesinin en belirgin işaretlerinden biri. | → "ama", "yine de", "-sa da" |
| **buna karşın / buna rağmen** | R/N | Virgülle | Somut bir olguya karşı çıkar. LLM'de orta sıklıkta. | "Uyarıldı. Buna rağmen gitti." |
| **-masına rağmen / -mesine karşın / -dığı hâlde** **[LLM- "dığı hâlde"]** | N | Ek-edat yapısı. *hâlde* ayrı yazılır. | İki cümleyi tek cümlede birleştirir. *-dığı hâlde*'de beklentinin tersine dönmesi daha güçlü. | "Bildiği hâlde söylemedi." |
| **-sa da / -se de** **[LLM-]** | N | *de* ayrı: *gelse de*. Şart ekinden sonra virgül konmaz (TDK), ama bu yapıdan sonra virgül yaygındır. | En doğal ve kısa karşıtlık aracı. | "Zor olsa da deneyeceğim." |
| **her ne kadar … -sa da** | R | | Resmî. LLM bunu ağır ve tekrar tekrar kullanıyor. | "Her ne kadar haklı olsa da üslubu sertti." |
| **gerçi** **[LLM-]** | N/G | Çoğunlukla *gerçi …, ama …* kalıbında. Tek başına sonradan gelen çekince olarak da kullanılır. | Karşı tarafa bir noktayı teslim eder (concessive). | "Gerçi pahalı, ama değer." / "Haklısın. Gerçi o da çok uğraştı." |
| **hoş** **[LLM-]** | G | Cümle başında virgülle. | Gündelik "gerçi". Konuşma dilinin sıcaklığını verir. | "Hoş, o da pek haklı sayılmaz." |
| **yine de / gene de** **[LLM- "gene de"]** | N / G | *yine de* ayrı (*yinede* yanlış). | Engele rağmen sonuç. *gene* daha gündelik. | "Çok yorgundu, yine de geldi." |
| **ise** (karşıtlık / konu değiştirme) | N/R | Ayrı ya da ek (*-se*). Öncesinde virgül. | İki öğeyi karşılaştırır. LLM'de "X ise …" diye her paragrafta konu açma olarak fazla kullanılıyor. | "Ben çay içerim, o ise kahve." |
| **-ken** (karşıtlık) **[LLM-]** | N | Bitişik (*iken*'in ek hâli). | "…durumdayken" anlamında karşıtlık. | "Herkes susarken o konuştu." |
| **aksine / tersine / bilakis** | N / N / ESK-R | Virgülle | Önceki yargıyı reddedip tersini koyar. *bilakis* resmî ve eskice. | "Kızmadı, aksine güldü." |
| **öte yandan** **[LLM+]** | R | Virgülle | Gerçek işlevi bir konunun ikinci yüzünü açmaktır. LLM ise bunu her geçişte kullanıyor. *bir yandan* olmadan tek başına geldiğinde fazla kullanımın işaretidir. | |
| **diğer taraftan / diğer yandan** **[LLM+]** | R | | *öte yandan* ile aynı | |
| **ne de olsa** | (bkz. §3) | | | |
| **değil ki / … ki değil** | G | Ayrı | Karşı çıkarak gerekçe sunar. | "Çocuk değil ki anlamasın." |

**Humanizer kuralı:** Bir metinde *bununla birlikte, öte yandan, ancak, buna rağmen* toplamı paragraf başına birden fazlaysa sırayla şunlarla değiştir: (1) *-sa da / -dığı hâlde / -ken* gibi ekle bağlanan yapı, (2) *oysa / hâlbuki / ne var ki / gelgelelim / yalnız / gerçi*, (3) bağlaçsız iki kısa cümle.

---

## 3. Neden ve gerekçe

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **çünkü** | N | Bitişik, *çünki* yanlış (TDK). Cümle ortasında öncesinde virgül yaygın. Cümle başında da kullanılabilir. | Açık gerekçe. Bu yüzden LLM'de fazla açıklayıcı bir ton yaratabilir. | "Gelmedim, çünkü hastaydım." |
| **zira** **[LLM-]** | R/ESK-E | | "Çünkü"nün resmî ya da edebî karşılığı. Hukuk ve deneme dilinde yaşıyor. | "Bu karar yerindedir; zira başka yol kalmamıştı." |
| **madem / mademki** **[LLM-]** | N/G | *mademki* bitişik (TDK). | Bilinen ve kabul edilmiş bir gerekçeden sonuç çıkarır. Sıklıkla sitem ya da ikna tonu taşır. | "Madem biliyordun, neden söylemedin?" |
| **ne de olsa** **[LLM-]** | N/G | Ayrı | Herkesin kabul ettiği bir gerekçe ("sonuçta"). | "Affet onu, ne de olsa çocuk." |
| **nasılsa** **[LLM-]** | G | Bitişik | "Zaten olacak, merak etme" anlamı. | "Acele etme, nasılsa yetişiriz." |
| **zaten** **[LLM-]** | G/N | | Önceden var olan durumu gerekçe gösterir. Hafif sitem taşır. | "Zaten geç kalmıştık, bir de yağmur başladı." |
| **sonuçta** | G | | Gündelik "ne de olsa / nihayetinde". | "Sonuçta o da insan." |
| **-dığı için** | N | | En doğal ekle bağlanan neden yapısı. | "Yağmur yağdığı için çıkmadık." |
| **-dığından (dolayı)** | R | | Resmî. *dolayı* çoğu zaman gereksiz. | "Belge eksik olduğundan başvuru reddedildi." |
| **-masından / -mesinden dolayı** | R | | Ağır ve LLM'de yaygın | → "-dığı için" |
| **yüzünden** | N | Olumsuz neden bildirir. | | "Trafik yüzünden geç kaldım." |
| **sayesinde** | N | Olumlu neden bildirir. | LLM'de *bu sayede* çok sık. | |
| **dolayısıyla** | (bkz. §4) | | | |
| **-dığına göre** **[LLM-]** | N | | Çıkarımsal neden ("madem"). | "Işıklar yandığına göre evdeler." |
| **ki** (gerekçe, sondan) **[LLM-]** | G/E | Ayrı | Gerekçe sonradan eklenir. | "Sus, ki duymasınlar." / "Çok çalış ki kazanasın." (amaç) |
| **-sın diye / -mek için / -mek üzere** | N / N / R | | Amaç bildirir | "Uyanmasın diye fısıldadı." |
| **nitekim** | (bkz. §5, açıklama ve doğrulama) | | | |
| **ister istemez** | N | | Zorunluluktan doğan sonuç | |

---

## 4. Sonuç ve çıkarım

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **bu yüzden** | N | Cümle başında virgül isteğe bağlı. | Nötr sonuç. Olumsuz ya da nötr bir nedene bağlanır. | "Otobüs kaçtı, bu yüzden yürüdük." |
| **bu nedenle / bu sebeple** **[LLM+ "bu nedenle"]** | R | | Resmî. LLM'de çok sık. | → "bu yüzden", "o yüzden", "-dığı için" |
| **o yüzden / onun için** **[LLM-]** | G | | Konuşma dili | "Param yoktu, o yüzden gelemedim." |
| **dolayısıyla** **[LLM+]** | R | Virgülle | Mantıksal sonuç. Akademik ve LLM dilinde aşırı sık. | |
| **sonuç olarak** **[LLM+]** | R | Virgülle | *As a result / in conclusion* kalkı. LLM'in kapanış klişesi. | → "kısacası", "demek ki", hiç kullanmamak |
| **böylece / bu sayede** **[LLM+ ikisi de]** | N | | Amaçlanan sonuç | |
| **demek ki** **[LLM-]** | N/G | Ayrı (TDK). *demekki* yanlış. | Konuşanın kendi çıkarımı. Doğal düşünme tonu verir. | "Kapı kilitli değil, demek ki biri gelmiş." |
| **demek (ki)** soru biçiminde | G | | "Demek gidiyorsun?" | |
| **şu hâlde** **[LLM-]** | R/E | Ayrı. TDK *hâl*'i şapkalı yazar. | Kesin mantıksal sonuç ("ergo"). Deneme dilinde etkili. | "Şu hâlde, ya kural yanlış ya uygulama." |
| **öyleyse / o hâlde / o zaman** **[LLM-]** | N / N / G | *öyleyse* bitişik, *o hâlde* ayrı. | Karşı tarafın sözünden sonuç çıkarıp önerir. | "Yorgunsan, öyleyse kalalım." / "O zaman yarın konuşuruz." |
| **binaenaleyh** | ESK | | Osmanlıca "bundan dolayı". Bugün yalnızca ironik. | |
| **netice itibarıyla / neticede** | R/ESK, G | *itibarıyla* (*itibariyle* yanlış) | | |
| **nihayetinde** **[LLM+]** | R | | LLM'de "eventually/ultimately" kalkı. | |
| **ki** (sonuç) | N/E | Ayrı | "öyle …-dı ki" kalıbı | "Öyle yoruldum ki konuşacak hâlim kalmadı." |
| **o kadar … ki** **[LLM-]** | N | | Derece ve sonuç | "O kadar güldük ki karnımız ağrıdı." |
| **haliyle / doğal olarak** | G / N | *hâliyle* | Kaçınılmaz sonuç | "Haliyle herkes kızdı." |
| **bu da … anlamına gelir** **[LLM+]** | R | | *which means* kalkı. Tipik LLM kalıbı. | → "demek ki", "yani" |

---

## 5. Açıklama, örnekleme, doğrulama

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **yani** | N/G | Ardından virgül isteğe bağlı. | Yeniden ifade eder ve açar. Konuşmada dolgu sözcüğü olarak da kullanılır. | "Yarın, yani cuma, toplantı var." |
| **başka bir deyişle / diğer bir deyişle / bir başka deyişle** **[LLM+]** | R | | *In other words* kalkı | → "yani" |
| **şöyle ki** **[LLM-]** | N | Ayrı, ardından açıklama gelir. TDK açıklama öncesi iki nokta öngörür ama "şöyle ki"yi ayrıca anmaz. | Açıklamayı duyurur. | "Durum karışık, şöyle ki iki taraf da haklı." |
| **örneğin** **[LLM+ cümle başında]** | N | Virgülle | Nötr | |
| **mesela** | G/N | TDK güncel: *mesela* | Konuşma dili | "Mesela dün ne yaptın?" |
| **sözgelimi / sözgelişi** **[LLM-]** | E/R | Bitişik | Edebî ve zarif örnekleme | "Sözgelimi bir köprü düşünün…" |
| **diyelim (ki) / tutalım ki / farz edelim ki / tut ki / say ki** **[LLM-]** | G/N | Ayrı | Varsayımsal örnek. Okuru düşünceye katar. | "Diyelim ki kazandın, sonra ne olacak?" |
| **gibi / ve benzeri / vb. / vs.** | N | *vb.* öncesinde virgül tartışmalı (§0.3) | | |
| **nitekim** **[LLM-]** | R/E | Cümle başında. Ardından virgül isteğe bağlı. | Önceki iddiayı olguyla doğrular ("nitekim öyle oldu"). LLM bunu çoğu zaman yanlış anlamda, "ayrıca" yerine kullanıyor. | "Bu işin yürümeyeceğini söylemiştim. Nitekim iki ay sonra kapandı." |
| **zaten / hakikaten / gerçekten de** | G/N | | Doğrulama | "Gerçekten de öyle çıktı." |
| **özellikle** **[LLM+]** | N | | Özelleştirme. LLM'de "özellikle de" ve "özellikle …-da" dolgusu çok sık. | → "hele", "bilhassa" (R/ESK), bazen tamamen sil |
| **hele / hele hele** **[LLM-]** | G/E | | Özelleştirme ve pekiştirme, duygusal | "Hele o sabah, hiç unutmam." |
| **bilhassa** | ESK/R | | Osmanlıca "özellikle" | |
| **ki** (açıklama, Farsça kökenli tümleç) | N/R | Ayrı | "Biliyorum ki…", "Duydum ki…". Resmî "Bilinmelidir ki…" yapısı LLM'de klişe. | "Duydum ki taşınmışsın." |
| **şunu belirtmek gerekir ki / unutulmamalıdır ki / önemle vurgulamak gerekir ki / belirtmekte fayda var** **[LLM+ yüksek]** | R | | Meta-söylem dolgusu. Bilgi taşımaz, doğrudan sil. | |
| **bu noktada / tam da bu noktada / işte tam burada** **[LLM+]** | R/G | | Sahte vurgu | |
| **bu bağlamda / bu çerçevede / bu doğrultuda / bu kapsamda** **[LLM+ yüksek]** | R | | Bürokratik ve LLM dolgusu | Sil ya da somut bağlantı kur |
| **söz konusu** **[LLM+]** | R | | "Bu" yerine kullanılan bürokratik gösterici | → "bu" |
| **açıkçası / doğrusu / aslına bakarsanız / işin aslı** | G | | Samimi açıklama. *açıkçası* LLM'de de görülüyor. | "Doğrusu, beklemiyordum." |

---

## 6. Özetleme ve kapanış

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **kısacası** **[LLM+]** | N | Virgülle | Nötr özet. LLM kapanışlarında sık. | |
| **özetle / özetlemek gerekirse / toparlarsak** **[LLM+]** | R | | Sunum ve rapor dili. LLM klişesi. | |
| **sonuç olarak / genel olarak / genel itibarıyla** **[LLM+ yüksek]** | R | | Kapanış klişesi. Humanizer kapanışta bunları silmeli. | |
| **sözün kısası** **[LLM-]** | N/E | | Konuşanın sesini taşır | "Sözün kısası, kimse kazanmadı." |
| **uzun lafın kısası** **[LLM-]** | G | | Samimi | "Uzun lafın kısası, taşındık." |
| **velhasıl / velhasılıkelam** **[LLM-]** | ESK-G/E (şakacı) | Bitişik | Osmanlıca, bugün esprili | "Velhasıl, yine biz kaybettik." |
| **hâsılı / hâsılıkelam** | ESK/E | | | |
| **ezcümle** | ESK | | "Bu arada, özetle" | |
| **kısaca** | N | | Zarf. "kısacası" ile karıştırılmamalı. | |
| **neyse / her neyse** **[LLM-]** | G | Virgülle | Konuyu kapatır ya da geçiştirir | "Neyse, uzatmayalım." |
| **neyse ki** **[LLM-]** | N/G | Ayrı | Rahatlama ("fortunately"). | "Neyse ki kimse yaralanmadı." |
| **ne yazık ki / maalesef / şükür ki / iyi ki / bereket versin ki** | N/G | Ayrı | Değerlendirme bildiren tutum belirleyicileri | |
| **en nihayetinde / nihayet** | R / N | | | |

---

## 7. Koşul

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **-sa / -se** (şart eki) | N | Ardından virgül yok (TDK uyarısı). | Temel koşul yapısı | "Gelirsen konuşuruz." |
| **eğer … -sa** | N | | *eğer* pekiştirir. Gereksiz kullanılması çeviri kokar ("if" kalkı). | Çoğu zaman *eğer*'i sil. |
| **şayet** | R/ESK | | Resmî "eğer" | |
| **madem(ki)** | (bkz. §3) | | Gerçekleşmiş koşul | |
| **yeter ki** **[LLM-]** | N | Ayrı (TDK örneği) | Tek şart | "Gel, yeter ki geç kalma." |
| **meğerki** | ESK/E | Bitişik (TDK) | "…-madıkça, ancak … şartıyla" | "Gelmez, meğerki çağırasın." |
| **ola ki / olur ki** | E/G | Ayrı | "belki de" anlamında olasılık koşulu | "Ola ki ararsa, haber ver." |
| **-dığı takdirde / aksi takdirde / aksi hâlde** | R | | Hukuk ve resmî dil | |
| **yoksa / değilse** **[LLM- "yoksa"]** | G/N | | Olumsuz koşul ("aksi hâlde"). *yoksa* ayrıca soru ve kuşku bildirir. | "Çabuk ol, yoksa kaçıracağız." |
| **-madıkça / -dığı sürece / … şartıyla / … kaydıyla** | N / N / R / R | | Süreklilik koşulu | "Sen istemedikçe gitmem." |
| **-sa bile / -sa dahi** | N / R | Ayrı | Etkisiz koşul ("even if") | "Yağmur yağsa bile gideriz." |
| **ister … ister** | (bkz. §11) | | | |
| **illa (ki)** | G | Ayrı | Mutlak koşul | "İlla ki gelecekmiş." |
| **… mı, … (soru biçimli koşul)** **[LLM-]** | G/E | | Ekle kurulan koşul | "Para mı lazım, söyle." |

---

## 8. Zaman ve eş zamanlılık

| İfade | Kayıt | Nüans | Doğal örnek |
|---|---|---|---|
| **-ınca / -ince** | N | Temel zaman bağlayıcısı | "Eve gelince ara." |
| **-dığında / -dığı zaman** | N | | |
| **-ken** | N | Eş zamanlılık ve karşıtlık | "Yürürken düşündüm." |
| **-ır -maz** **[LLM-]** | N | "…-ınca hemen" | "Kapıyı açar açmaz bağırdı." |
| **mı/mi ("-ınca" anlamı)** **[LLM-]** | G/E | TDK: ardından virgül yok | "Bir başladı mı susmaz." |
| **-dıkça** | N | Süreklilik ve orantı | "Okudukça açılıyordu." |
| **-alı / -eli (beri)** | N | Başlangıç noktası | "Taşınalı iki yıl oldu." |
| **-madan (önce)** | N | | |
| **-dıktan sonra** | N | | |
| **derken** **[LLM-]** | N/G | Anlatıda beklenmedik geçiş, "tam o sırada" | "Tam çıkacaktık, derken telefon çaldı." |
| **bir de baktım ki** **[LLM-]** | G | Şaşkınlıkla gelen keşif | "Bir de baktım ki kapı açık." |
| **meğer(se) … -mış** **[LLM-]** | N/G | Sonradan anlaşılan durum | "Meğer o da biliyormuş." |
| **o sırada / bu arada / tam o sırada** | N | *bu arada* konuşmada konu değiştirmek için de kullanılır | |
| **sonra / ardından / akabinde** | N / N / R-ESK | *akabinde* bürokratik | |
| **nihayet / sonunda / en sonunda** | N | | |
| **o zamandan beri / o günden bu yana** | N | | |
| **eskiden / bir zamanlar / vaktiyle** | N / N / E | | |

---

## 9. Kıyas ve benzerlik

| İfade | Kayıt | Nüans | Örnek |
|---|---|---|---|
| **gibi** | N | Benzetme | "Kar gibi beyaz." |
| **kadar** | N | Eşitlik ve derece | "Senin kadar uzun." |
| **-dan daha / -dan çok / -dan fazla** | N | Üstünlük. "daha" bazen gereksiz. | "Ondan uzun." |
| **göre / -a nazaran / -a nispeten** | N / R-ESK / R | | |
| **ne kadar … o kadar** **[LLM-]** | N | Orantı | "Ne kadar çalışırsan o kadar kazanırsın." |
| **-dıkça … -ır** | N | Orantı | "Büyüdükçe susuyor." |
| **aynı şekilde / benzer şekilde / buna benzer olarak** **[LLM+]** | R | *similarly* kalkı | → "de", "keza", "aynen" |
| **keza / aynen / tıpkı … gibi / sanki** | R / G / N / N | *sanki* bitişik (TDK) | "Sanki hiçbir şey olmamış gibi." |
| **adeta / âdeta** | N/E | "neredeyse, sanki" | "Adeta uçuyordu." |
| **-casına** **[LLM-]** | E | "…-mış gibi" | "Kaçarcasına çıktı." |
| **iken (karşılaştırma)** | R | | "A artarken B azalmıştır." (LLM bunu raporlarda fazla kullanıyor) |

---

## 10. Pekiştirme ve derecelendirme

| İfade | Kayıt | Yazım / noktalama | Nüans | Doğal örnek |
|---|---|---|---|---|
| **hatta** **[LLM orta]** | N | Virgülle | Bir üst basamağa çıkar | "Herkes geldi, hatta Ali bile." |
| **bile** **[LLM-]** | N | Ayrı. Öğeden sonra gelir. | Beklenmedik uç durum ("even") | "Annesi bile tanımadı." |
| **dahi** | R | Ayrı | "bile"nin resmî karşılığı | |
| **kaldı ki** **[LLM-]** | N/E | Ayrı (TDK örneği) | Ek ve daha güçlü bir argüman. "Hem de üstelik…" | "Gelemem, kaldı ki davet de edilmedim." |
| **üstelik / üstüne üstlük** | (bkz. §1) | | | |
| **… şöyle dursun, … bile** **[LLM-]** | N/E | | "Bırakın X'i, Y bile yok" | "Teşekkür etmek şöyle dursun, selam bile vermedi." |
| **bırak(ın) … -ı, … bile** **[LLM-]** | G | | Aynı yapının gündelik hâli | "Bırak yardım etmeyi, aramadı bile." |
| **… değil, … bile** | N | | | |
| **hem de** **[LLM-]** | G/N | Ayrı | Şaşkınlık ve sitem dolu pekiştirme | "Gitti, hem de kimseye haber vermeden." |
| **ki ne …** **[LLM-]** | G | Ayrı | Ünlem gibi pekiştirir | "Bir yemek yaptı ki ne yemek!" |
| **de / da** (pekiştirme) | G | Ayrı | "Güzel de bir ev." "Gel de gör." | |
| **mi** (pekiştirme) | G/E | Ayrı | "Güzel mi güzel", "uzun mu uzun" | |
| **ama** (pekiştirme) | G | | "Gelecek ama bu sefer kesin." | |
| **ya / yahu / be** | G | | Konuşma dili ünlem bağlayıcıları | "Bıktım ya!" |
| **asla / kesinlikle / mutlaka / elbette / tabii (ki)** | N | *tabii* (*tabi* "tabi olmak" ile karıştırılır). *tabii ki* ayrı. | Kesinlik. LLM'de *kesinlikle* çok sık. | |
| **özellikle / bilhassa / hele** | (bkz. §5) | | | |
| **en azından / hiç değilse / hiç olmazsa** **[LLM- son ikisi]** | N/G | | Asgari teselli | "Hiç değilse bir telefon açsaydın." |

---

## 11. Seçenek ve ayırma

| İfade | Kayıt | Yazım / noktalama | Nüans | Örnek |
|---|---|---|---|---|
| **veya** | N/R | Öncesinde ve sonrasında virgül yok (TDK) | Nötr seçenek | |
| **ya da** | N | İki sözcük. *yada* yanlış. Virgül yok. | En doğal seçenek bağlacı | "Çay ya da kahve?" |
| **yahut / veyahut** | E/R | Bitişik. Virgül yok. | Eskice ve yazınsal | |
| **ya … ya (da)** | N | Virgül yok (TDK) | Kesin iki seçenekten biri | "Ya gel ya ara." |
| **ister … ister** | N | Virgül yok | Seçim fark etmez | "İster gel ister gelme." |
| **ha … ha** **[LLM-]** | G | | "Fark etmez, ikisi bir" | "Ha bugün ha yarın, ne fark eder?" |
| **kâh … kâh** **[LLM-]** | E | Şapkalı | Dönüşümlü durum ("bazen … bazen") | "Kâh gülüyor kâh ağlıyordu." |
| **ne … ne (de)** | N | Virgül yok (TDK). Yüklem olumlu. | Çifte olumsuzluk. Olumsuz yüklemle kullanmak sık görülen hatadır. | "Ne arar ne sorar." (*ne aramaz ne sormaz* yanlış) |
| **olsun … olsun** | N | | "hem … hem" | "Genç olsun yaşlı olsun herkes geldi." |
| **gerek … gerek(se)** | R | Virgül yok | | |
| **yoksa** | N | | Soruda seçenek, kuşku | "Çay mı, yoksa kahve mi?" / "Yoksa unuttun mu?" |
| **ya** (tek başına, soru) | G | | "Peki ya sen?" | |
| **bazen … bazen** | N | | | |

---

## 12. "ki", "de/da", "mi" ve "ise"nin işlev haritası (humanizer için tek tabloda)

### 12.1 ki (bağlaç)
| İşlev | Örnek | Not |
|---|---|---|
| Açıklama, tümleç ("that") | "Biliyorum ki gelmeyecek." | Farsça kökenli yapı. Bugün çoğu zaman *-dığını* ile kurulur: "Gelmeyeceğini biliyorum." LLM'in "Bilinmelidir ki" kullanımı çeviri kokar. |
| Sonuç ("öyle … ki") | "Öyle bağırdı ki herkes döndü." | Doğal ve güçlü |
| Amaç | "Erken çık ki yetişesin." | Edebî ve gündelik |
| Gerekçe | "Sus, ki duymasınlar." | |
| Şaşkınlık ve keşif | "Bir de baktım ki…" | |
| Şüphe ve pekiştirme (cümle sonu) | "Ne bileyim ki?", "Gelir mi ki?" | Ayrı (TDK) |
| Sitem ve pekiştirme | "Öyle bir sevindim ki!" | |
| Karşıtlık ("ki" = oysa) | "Ona güvendim, ki hiç güvenmemeliydim." | Edebî |
| Kalıplar | *demek ki, kaldı ki, yeter ki, ne var ki, şu var ki, diyelim ki, neyse ki, illa ki, tabii ki, iyi ki, ne yazık ki, şükür ki, bereket ki, öyle ki, şöyle ki, o kadar ki, değil ki, ola ki, olur ki, meğer ki/meğerki, nerde (nerede) ki* | Hepsi ayrı. Bitişik olan yalnızca TDK'nin 7 sözcüğü. |

### 12.2 de / da (bağlaç)
| İşlev | Örnek |
|---|---|
| Ekleme ("dahi") | "Ben de geleceğim." |
| Pekiştirme | "Güzel de bir ev almışlar." |
| Karşıtlık ve sitem | "Çalıştın da ne oldu?" |
| Küçümseme ve yakınma | "Bir de bana akıl veriyor." |
| Sıralama ve sonuç ("ve sonra/ve bu yüzden") | "Hastalandım da gelemedim." / "Gitti de geldi." |
| Koşul ve meydan okuma | "Gel de gör!" |
| Tavsiye ve rica | "Otur da bir çay iç." |
| Tamamlama | "-sa da" (bkz. §2), "ya da", "hem de", "yine de", "belki de", "ne de olsa" |
**Humanizer notu:** *de*'nin bağlama işlevi ("Hastalandım da gelemedim") LLM'de neredeyse hiç görülmüyor, oysa konuşma Türkçesinin en doğal bağlayıcısı. Kayıt uygunsa *ve bu nedenle* yerine önerilmeli.

### 12.3 mi
- Soru: "Geldi mi?" (ayrı, kişi eki *mi*'ye bitişir: "Gelecek misin?")
- "-ınca" anlamı: "Bir başladı mı bitirmeden kalkmaz." (TDK: ardından virgül yok)
- Pekiştirme: "uzun mu uzun", "güzel mi güzel"
- Koşul gibi kullanım: "Para mı lazım, söyle."

### 12.4 ise / -se
- Karşıtlık ve konu değiştirme: "Ali geldi, Veli ise gelmedi."
- Koşul: "Gerekirse ararım."
- **LLM aşırı kullanımı:** Her paragrafa "X ise …" diye girmek ("Teknoloji ise hayatımızın…"). Linter: paragraf başında `\b\w+ ise\b` kalıbı tekrar ediyorsa uyar.

---

## 13. Söylem belirleyicileri (konuşma ve deneme dili, en "insan" kokan grup)

Çoğu, LLM çıktısında neredeyse hiç geçmiyor **[LLM-]**. Kayda uygunsa (blog, köşe yazısı, kişisel deneme) humanizer bunları seyrek kullanılacak bir palet olarak sunabilir. Her paragrafa birini koymak ters etki yapar.

| İfade | İşlev | Kayıt | Örnek |
|---|---|---|---|
| **peki** | Geçiş ve onay. Cümle başında virgül alır (TDK kural 9). | G/N | "Peki, sonra ne oldu?" *(LLM'de "Peki, X nedir?" retorik soru açılışı da klişeleşti [LLM+])* |
| **e / eh / ee** | Konuya giriş, sabırsızlık | G | "E, ne yapacaktık?" |
| **hani** | Ortak bilgiye gönderme | G | "Hani geçen yıl gittiğimiz yer var ya…" |
| **ya** (cümle sonu) | Ortak bilgi, vurgu | G | "Söylemiştim ya." |
| **işte** | Sonuca bağlama, vurgu | G/N | "İşte bu yüzden gelmedim." |
| **aslında** | Beklentiyi düzeltme | N | LLM'de orta sıklıkta, zayıf dolgu olarak kullanılıyor |
| **zaten** | Önceden bilinen | G | |
| **galiba / herhalde / sanırım / belki** | Kesinliği yumuşatma (hedging) | N/G | *belki* bitişik (TDK) |
| **doğrusu / açıkçası / laf aramızda / söz aramızda** | Samimiyet işareti | G | |
| **bu arada / yeri gelmişken / aklıma gelmişken** | Konu değiştirme | G/N | |
| **neyse** | Konuyu kapatma | G | |
| **velev ki** | "Hadi diyelim ki" (Arapça kökenli) | ESK | "Velev ki öyle olsun, ne değişir?" |
| **hadi / haydi** | Teşvik, varsayım ("hadi diyelim") | G | "Hadi diyelim kabul ettiler…" |
| **yok … yok** | Bahanelerin sıralanması (alaycı) | G | "Yok başım ağrıyor, yok işim var…" |
| **efendim** | Düzeltme, nezaket | G/R | |
| **gel gör ki** | Beklenmedik ve kötü gerçek | G/E | "Gel gör ki kimse dinlemedi." |
| **ne demişler** | Atasözü girişi | G | |
| **bakalım / bakarsın** | Belirsiz gelecek | G | "Bakarsın gelir." |
| **nerede kaldı ki** | "bırak ki" | G/E | |

---

## 14. Ekle bağlama (zarf-fiil ve isim-fiil): Türkçenin asıl bağlayıcı sistemi

İngilizce connective kalkıyla yazan LLM, iki tam cümleyi bağımsız bir bağlaç sözcüğüyle birleştirir. Usta Türkçe yazar ise aynı ilişkiyi ekle kurulan yan cümleyle verir. Humanizer'ın en verimli dönüşüm tablosu:

| LLM / çeviri kalıbı | Doğal Türkçe |
|---|---|
| "X yaptı. Bununla birlikte Y olmadı." | "X yaptıysa da Y olmadı." / "X yaptığı hâlde Y olmadı." / "X yaptı, ama Y olmadı." |
| "X oldu ve bu nedenle Y." | "X olunca Y." / "X olduğu için Y." / "X oldu da Y." |
| "Önce X yaptı, ardından Y yaptı." | "X yapıp Y yaptı." / "X yaptıktan sonra Y'ye geçti." |
| "X yaparken aynı zamanda Y yaptı." | "X yaparken Y'yi de yaptı." |
| "Eğer X olursa, o zaman Y." | "X olursa Y." |
| "X'in nedeni Y'dir." | "Y yüzünden X." / "Y olduğundan X." |
| "Bu da X anlamına gelmektedir." | "Demek ki X." / "Yani X." |
| "X olmasına rağmen Y. Ayrıca Z." | "X olsa da Y, üstelik Z." |
| "Bu bağlamda belirtmek gerekir ki X." | "X." (dolguyu sil) |
| "Öte yandan, X." (karşıtlık yokken) | Bağlacı sil ya da "Bir de X." |
| "Sonuç olarak, X." (kapanış) | Sil. Gerekiyorsa "Kısacası X." / "Sözün kısası X." |
| "X özellikle Y'de önemlidir." | "X, hele Y'de, çok önemli." / "X en çok Y'de işe yarar." |

Zarf-fiil envanteri: -ıp, -arak, -madan/-meksizin, -ınca, -dıkça, -dığında, -ken, -alı, -ır…-maz, -casına, -dıktan sonra, -mak üzere, -a…-a ("koşa koşa"), -dığı için/-dığından, -dığı hâlde, -sa da, -mekle birlikte (R, LLM+), -mesine rağmen, -dığına göre, -cesine.

---

## 15. LLM Türkçesi: aşırı kullanılan bağlayıcılar (linter sözlüğü)

**Uyarı:** Türkçe LLM çıktılarında bağlaç sıklığını ölçen yayımlanmış bir çalışma bulamadım (arama: dergipark ve genel web, 2026-11). Aşağıdaki liste gözleme ve İngilizce kalk eşleşmesine dayalı bir hipotez. *Sonuç olarak* ve *bununla birlikte* insan akademik Türkçesinde de yaygın. Bu yüzden tek bir geçiş hata sayılmamalı, linter **yoğunluk ve tekrar** üzerinden çalışmalı. Türkçe için ayrı dedektör gerekçesi: https://openaccess.izu.edu.tr/entities/publication/fbb35125-076b-4f20-90ba-c6bca9b285ca/full

### 15.1 Yüksek şüphe (İngilizce kalkı ve meta-söylem dolgusu)
`bununla birlikte` (however), `bununla beraber`, `ek olarak` / `buna ek olarak` (additionally), `dahası` (moreover), `öte yandan` (on the other hand), `diğer taraftan`, `sonuç olarak` (in conclusion), `bu bağlamda` (in this context), `bu çerçevede`, `bu doğrultuda`, `bu kapsamda`, `aynı zamanda` (also), `özellikle` (particularly), `bunun yanı sıra` (besides), `son olarak` (finally), `ilk olarak`, `bir başka deyişle` / `diğer bir deyişle` (in other words), `bu da … anlamına gelir` (which means), `nihayetinde` (ultimately), `genel olarak` (overall), `özetle` / `özetlemek gerekirse` (to summarize), `şunu belirtmek gerekir ki`, `belirtmekte fayda var`, `unutulmamalıdır ki`, `önemle vurgulamak gerekir`, `bu noktada`, `tam da bu noktada`, `söz konusu`, `-mesi açısından önem taşır/büyük önem arz eder`, `bu sayede`, `böylece`, `dolayısıyla`, `bu nedenle`, `her ne kadar … -sa da`, `-mekle birlikte`, `benzer şekilde` (similarly), `ayrıca` (paragraf başında), `peki` (retorik soruyla açılış), `gelin birlikte bakalım`, `kısacası` (kapanış).

### 15.2 Neredeyse hiç kullanılmayanlar (rewrite paleti)
Karşıtlık: `oysa(ki)`, `hâlbuki`, `ne var ki`, `ne ki`, `gelgelelim`, `yalnız`, `gerçi`, `hoş`, `şu var ki`, `gene de`, `-dığı hâlde`, `-sa da`, `-ken` (karşıtlık), `gel gör ki`.
Neden: `zira`, `madem(ki)`, `ne de olsa`, `nasılsa`, `zaten`, `-dığına göre`, `ki` (gerekçe).
Sonuç: `demek ki`, `şu hâlde`, `öyleyse`, `o hâlde`, `o yüzden`, `haliyle`, `öyle … ki`, `o kadar … ki`.
Açıklama ve örnek: `şöyle ki`, `sözgelimi`, `sözgelişi`, `diyelim ki`, `tutalım ki`, `farz edelim ki`, `nitekim` (doğrulama), `hele`.
Pekiştirme: `kaldı ki`, `üstelik`, `üstüne üstlük`, `bile`, `hem de`, `şöyle dursun`, `bırakın … -ı`, `hiç değilse`, `bir de`.
Özet: `sözün kısası`, `uzun lafın kısası`, `velhasıl`, `hâsılı`, `neyse`.
Zaman: `derken`, `-ır -maz`, `bir de baktım ki`, `meğer … -mış`, `mı` ("-ınca").
Seçenek: `ha … ha`, `kâh … kâh`, `olsun … olsun`, `ne … ne`.
Ekle bağlama: `de` (bağlayıcı), `-ıp`, `-ınca`, `-dıkça`.

### 15.3 Önerilen linter metrikleri
1. **Bağlayıcı yoğunluğu:** 15.1 listesinden 100 sözcükte >2 geçiş varsa uyar. Aynı öğe metinde 2'den fazla geçiyorsa uyar.
2. **Cümle başı tekdüzeliği:** Cümlelerin >%30'u bir söylem belirleyiciyle (*Ayrıca, Ancak, Bununla birlikte, Öte yandan, Sonuç olarak, Bu nedenle*) başlıyorsa uyar.
3. **Paragraf açılış ve kapanış kalıbı:** Son paragraf `Sonuç olarak|Özetle|Kısacası|Genel olarak` ile başlıyorsa uyar.
4. **Karşıtlık çeşitliliği:** Karşıtlık öğelerinin tamamı {ancak, ama, fakat, bununla birlikte, öte yandan} içinde kalıyorsa ve sayısı ≥4 ise rewrite önerisi ver (§15.2 paleti).
5. **Ekle bağlama oranı:** Yan cümle eklerinin (-ınca, -dığı için, -sa da, -ken, -ıp, -dıkça) bağımsız bağlaç sözcüğüne oranı düşükse "çeviri sözdizimi" uyarısı ver.
6. **Meta-dolgu:** `belirtmek gerekir ki|unutulmamalıdır ki|vurgulamak gerekir|belirtmekte fayda var|bu bağlamda|bu çerçevede|söz konusu` gördüğünde doğrudan sil önerisi.
7. **TDK kesin hataları (§0):** ki/de yazımı, ve/veya/ya…ya virgülü, hem/ne/ister/gerek tekrarlı bağlaç virgülü, *ne … ne* + olumsuz yüklem.

---

## 16. Kayıt matrisi (hızlı seçim)

| İşlev | Resmî/akademik | Nötr | Gündelik | Edebî | Eskimiş/ironik |
|---|---|---|---|---|---|
| Karşıtlık | ancak, buna karşın, -mekle birlikte | ama, fakat, oysa, -sa da | yalnız, hoş, gene de, hâlbuki | ne var ki, gelgelelim, ne ki | lakin, mamafih, bilakis |
| Neden | -dığından, zira | çünkü, -dığı için | nasılsa, zaten, sonuçta | ki (gerekçe) | zira |
| Sonuç | dolayısıyla, bu nedenle | bu yüzden, demek ki | o yüzden, haliyle | şu hâlde | binaenaleyh |
| Açıklama | başka bir deyişle | yani, şöyle ki, örneğin | mesela, diyelim | sözgelimi | ezcümle |
| Doğrulama | nitekim | gerçekten de | zaten, hakikaten | nitekim | |
| Özet | özetle, sonuç olarak | kısacası | uzun lafın kısası, neyse | sözün kısası | velhasıl, hâsılı |
| Pekiştirme | dahi, üstelik | hatta, bile | üstüne üstlük, hem de | kaldı ki, şöyle dursun | |
| Koşul | -dığı takdirde, şayet | -sa, yeter ki | yoksa, illa | ola ki | meğerki, velev ki |
| Seçenek | veya, gerek … gerekse | ya da, ya … ya | ha … ha | yahut, kâh … kâh | veyahut |
| Ekleme | ayrıca, keza | ve, de, hem … hem | bir de | | keza |

---

## Kaynaklar
- TDK, Bağlaç Olan ki'nin Yazılışı: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-kinin-yazilisi/
- TDK, Bağlaç Olan da, de'nin Yazılışı: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-da-denin-yazilisi/
- TDK, Bulunma Durumu Eki -da/-de'nin Yazılışı: https://tdk.gov.tr/icerik/yazim-kurallari/bulunma-durumu-eki-da-de-ta-tenin-yazilisi/
- TDK Yazım Kılavuzu, Noktalama İşaretleri: https://yazim.tdk.gov.tr/content/09-noktalama-isaretleri.html
- TDK, Noktalama İşaretleri (Açıklamalar): https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/
- TDK, Yazım Kuralları kategori: https://tdk.gov.tr/kategori/icerik/yazim-kurallari/
- Hamza Zülfikar, "Farsça Kökenli ki Bağlacını Adlandırma", Türk Dili: https://tdk.gov.tr/wp-content/uploads/2020/01/9_Hamza-Z%C3%BClfikar-_-FARS%C3%87A-K%C3%96KENL%C4%B0-K%C4%B0-BA%C4%9ELACINI-ADLANDIRMA-_-6.pdf
- Hamza Zülfikar, "Kuralsız Türkçe Öğretimi", Türk Dili 2022: https://www.tdk.gov.tr/wp-content/uploads/2022/06/Hamza-Z%C3%BClfikar-_-KURALSIZ-T%C3%9CRK%C3%87E-%C3%96%C4%9ERET%C4%B0M%C4%B0_-5-1.pdf
- Belgin Tezcan Aksu, Türk Dili 2025 (yazım kılavuzlarındaki kural değişimleri): https://tdk.gov.tr/wp-content/uploads/2025/04/Belgin-Tezcan-Aksu_-E-_-Gelecege-Isik-Yazim-Sorunlarina-Gecmisten-Cozumler-_12.pdf
- TDK, Şart Cümlelerinde Noktalama Tutarsızlığı: https://tdk.gov.tr/wp-content/uploads/2012/11/12.pdf
- Bağlaç öncesi noktalı virgülün kılavuzlardan kaldırılması (dergipark): https://dergipark.org.tr/en/download/article-file/70399
- Türkçede söylem belirleyicileri, temel çalışmalar: Özbek (1995, 1998). Schiffrin (1987) modeli üzerine bir Dil Dergisi incelemesi (2020); taramada çıkan dergipark makaleleri: https://dergipark.org.tr/tr/pub/mersinjll/article/1285423 , https://dergipark.org.tr/tr/pub/sutad/article/1405528
- Türkçe yapay zekâ metni tespiti (Türkçeye özgü dedektör gerekçesi): https://openaccess.izu.edu.tr/entities/publication/fbb35125-076b-4f20-90ba-c6bca9b285ca/full
- Kayıt, nüans ve örnek cümlelerin büyük kısmı dil bilgisi bilgisine dayalı derleme. Nüans tanımları için TDK Güncel Türkçe Sözlük (sozluk.gov.tr) ile tek tek doğrulanması önerilir.
