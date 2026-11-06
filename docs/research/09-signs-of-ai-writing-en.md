# 09: "Signs of AI writing" (en) → Türkçe eşleme

> Kaynak: İngilizce Vikipedi, ["Wikipedia:Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (CC BY-SA 4.0). Bu dosya sayfayı özetler ve Türkçeye uyarlar; metin kopyalanmadı. Amaç, her kalıbın Türkçe karşılığı olup olmadığına bakmak ve A/B/C diye sınıflamak.

---

## 1. Kaynaklar ve Türkçe karşılık bulgusu

| Kaynak | URL | Not |
|---|---|---|
| EN ana sayfa (okunan sürüm) | https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&oldid=1383697236 | revid 1383697236, 2026-11-04T06:08:39Z. Sayfa "As of October 2026" diyor ve her ay değişiyor, alıntılar bu permalink'e göre. |
| EN Style alt sayfası | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing/Style | Title case, bold, inline-header list, heading, emoji, tablo, curly quote |
| EN Markup alt sayfası (yalnızca referans) | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing/Markup | Wikitext'e özgü (B) |
| DE karşılığı (kıyas için) | https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte | EN'de olmayan iki başlık var: "Bestimmte Konjunktionen", "Falsche Erweiterung" |
| TR: VP:BDM (deneme) | https://tr.wikipedia.org/wiki/Vikipedi:B%C3%BCy%C3%BCk_dil_modelleri | Politika/deneme, **belirti listesi değil** |
| TR: VP:BDMMY (teklif) | https://tr.wikipedia.org/wiki/Vikipedi:B%C3%BCy%C3%BCk_dil_modelleriyle_madde_yazma | 2 paragraf: "BDM ile sıfırdan madde yazmayın" |
| TR: VP:YZ (bilgi sayfası) | https://tr.wikipedia.org/wiki/Vikipedi:Yapay_zek%C3%A2 | ORES vb. uygulamalar, belirti listesi yok |
| TDK büyük harf kuralları | https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/ | Başlık büyük harf kuralı (Bölüm 3.3, S1 satırı) |

**Türkçe karşılık bulgusu:** Türkçe Vikipedi'de "Signs of AI writing" sayfasının bir karşılığı **yok**. Doğrulama:
1. EN sayfanın `langlinks` listesinde yalnızca **de, fi, fr, he, pt, ru, th, zh** var, `tr` yok.
2. tr.wikipedia `Vikipedi:` (ns 4) ve `Yardım:` (ns 12) ad alanlarında "yapay zekâ" araması 30 sonuç döndürdü. İlgili olanlar yalnızca VP:BDM, VP:BDMMY ve VP:YZ. Üçü de politika ya da deneme sayfası, içlerinde dil veya üslup belirtisi listesi bulunmuyor.
3. VP:BDM'de ilgili tek ifade, yorum ve değişiklik özetlerinin şeffaf olmayan biçimde yapay zekâ araçlarıyla yazılmasının önerilmediği yönünde. Bu sayfa da büyük olasılıkla EN WP:LLM'den çevrilmiş.

Sonuç: Türkçeye özgü AI-belirti envanteri Vikipedi'de yok, bu boşluğu projenin kendisi dolduracak.

---

## 2. Sayfanın temel tezi (tasarım için bağlayıcı)

- **Ortalamaya gerileme.** Sayfaya göre model, istatistiksel olarak seyrek olan özgül ve incelikli olguları atıp yerine genel ve olumlu betimlemeler koyar. Konu hem daha belirsiz hem daha abartılı hâle gelir.
  → Humanizer yalnızca kelime değiştirmekle yetinmemeli, **somut ayrıntıyı geri koymalı** (tarih, isim, sayı, özel olgu). Kaynakta olmayan şeyi uydurmamalı. Ayrıntı yoksa şişirilmiş cümleyi silmeli.
- **Yüzeyi düzeltmek, sorunu düzeltmek değildir.** Sayfa, belirtileri yalnızca giderilecek sorun olarak görmemeyi öğütler; bu tespiti zorlaştırabilir. Bizim bağlamımızda: linter yalnızca "AI kelimesi" saymamalı. Skill her zaman içerik boşluğunu (genellik, kaynaksız yorum) da ele almalı.
- **Kelimeler literal okunmalı.** Bir sözcüğün sık kullanılması, eş anlamlılarının da sık kullanıldığını göstermez. Aşağıdaki Türkçe kelime listeleri **bu projede türetilmiş analoglardır**, Vikipedi bunları raporlamıyor. Kullanılmadan önce **corpus ile doğrulanmaları gerekir** (insan Türkçe metin ile LLM Türkçe çıktısındaki frekans kıyaslanmalı).
- **Tek başına zayıf sinyaller.** Em dash, geçiş kelimeleri ve "mükemmel dilbilgisi" ayrı ayrı zayıftır. Sinyal **yoğunluk ve birlikte görülme** ile güçlenir: bir belirti varsa yanında başkaları da vardır.
- **Dönemsel kayma.** Sık kullanılan kelimeler model nesline göre değişiyor; sayfa dönemleri ayrı ayrı sıralıyor. Son dönemde noktalama ve kısa cümle yığılması da gözleniyor (yaklaşık 8-20 kelimelik bant). Liste statik tutulmamalı, sürümlenebilir bir veri dosyası olmalı.
- **Modeller arası fark.** Sayfaya göre geniş bağlam vurgusu bazı modellerde, kısalık ve düz tırnak kullanımı başkalarında daha belirgin. Bu yüzden en olası belirtiler şunlar: yakın dönem düzeltici çerçeveler, kısa ve tekdüze cümle uzunluğu, noktalama çeşitliliğinin düşüklüğü, negatif paralellik. Promosyon dili daha az görülür.

---

## 3. Eşleme tablosu (EN başlıklar sırasıyla)

Sınıflar: **A** = doğrudan Türkçe analoğu var · **B** = İngilizceye/Vikipedi'ye özgü, atla · **C** = yapısal ya da dilden bağımsız.
Linter: **regex** = deterministik kalıp · **heur** = sayım/yoğunluk/oran sezgiseli · **LLM** = yalnızca skill/LLM değerlendirmesi.
"TR biçimleri" sütunundaki her şey **aday** listedir (doğrulanmadı).

### 3.1 Content

| # | EN kalıp (kısayol) | Sınıf | TR biçimleri ve örnek (aday) | Linter |
|---|---|---|---|---|
| C1 | Undue emphasis on significance, legacy, broader trends (WP:AILEGACY, WP:AITREND) | A | "…nın bir kanıtı/göstergesi niteliğindedir", "önemli/kritik/hayati/kilit bir rol oynar", "dönüm noktası niteliğinde", "önemli bir kırılma/dönüşümü temsil eder", "…in önemini vurgular/altını çizer", "daha geniş bir …in parçası", "kalıcı/silinmez bir iz bıraktı", "köklü", "zemin hazırladı", "değişen/gelişen manzara/peyzaj", "odak noktası", "…ı şekillendirdi", "bu ayrım önemlidir çünkü". **Örnek:** "Enstitü 1989'da kuruldu ve bölgesel istatistik tarihinde **önemli bir dönüm noktası oldu**. Kuruluşu, **daha geniş bir** yerelleşme hareketinin **parçasıydı**." → "Enstitü 1989'da kuruldu. Katalonya o tarihten beri kendi nüfus sayımını yapıyor." Alt türler: "tartışmalara yol açtı", "kamusal tartışmalarda yer aldı", "felsefi soruları gündeme getirdi". Biyoloji konularında: "ekosistemde önemli bir rol oynar", "korunması hayati önem taşır". | regex (kalıp listesi) + heur (paragraf başına yoğunluk) |
| C2 | Canned emphasis on notability, attribution, media coverage (WP:AIATTR) | A | "ulusal/yerel basında geniş yer buldu", "çeşitli medya kuruluşlarında yer aldı", "sektörel yayınlarda", "bağımsız kaynaklarca", "aktif bir sosyal medya varlığı/güçlü bir dijital varlık sürdürmektedir", "alanında önde gelen bir uzman tarafından kaleme alınan". **Örnek:** "Şirket **güçlü bir dijital varlık sürdürmekte**, Instagram'da güncel etkinliklerini **aktif olarak paylaşmaktadır**." | regex |
| C3 | Undue emphasis on identification by primary/tertiary sources (WP:AIDENTIFY), 2026'dan beri yaygın | A | "Kişisel web sitesi onu … olarak tanımlamaktadır", "kayıtlarda … olarak geçmektedir", "resmî profilinde … olarak listelenmektedir", "… tarafından … olarak tanımlanmıştır". **Örnek:** "**Kişisel web sitesi onu** 1982 kuşağı emekli bir vali **olarak tanımlamaktadır**." → "1982 kuşağından emekli validir.[kaynak]" | regex |
| C4 | Superficial analyses (WP:SUPERFICIAL): cümle sonuna eklenen "-ing" yorumu. **Söz dizimi notu:** İngilizcede katılımsı cümle sonundadır. Türkçe SOV olduğu için aynı yüzeysel yorum ya (a) **ana yüklemde** durur ("…a katkıda bulunmaktadır", "…ı yansıtmaktadır", "…ın önemini vurgulamaktadır"), ya (b) ", bu da / ki bu da" kuyruğunda yer alır, ya da (c) çeviri kokan bir **cümle sonu -arak** olarak görülür ("…, bölgenin kalkınmasına katkıda bulunarak."). (c) doğal Türkçede nadirdir, bu yüzden güçlü bir çeviri izi sayılır. (a) ise en sık görülen biçimdir. | A (güçlü) | **Türkçe karşılığı cümle sonundaki zarf-fiil kuyruğu:** "…ı vurgulayarak", "…ın altını çizerek", "…ı yansıtarak", "…ı simgeleyerek", "…a katkıda bulunarak", "…ı pekiştirerek", "…ı güçlendirerek", "…ı teşvik ederek", "…ı geliştirerek", "…ı garanti altına alarak", "…ı sağlayarak". Diğer kuyruk biçimleri: "**ki bu da** … göstermektedir/yansıtmaktadır", "…, bu da …ın önemini ortaya koymaktadır", "…, böylece … bir köprü kurmaktadır", "değerli içgörüler sunar", "…ile uyumludur / …ile örtüşür / …da yankı bulur". **Örnek:** "İstasyon 8 peronludur ve yolcu ile yük taşımacılığını kolaylaştırarak **bölgenin sosyo-ekonomik gelişimine katkıda bulunmaktadır**." → "İstasyonda 8 peron var. Darbhanga'yı Delhi, Patna ve Kalküta'ya bağlar." | heur (ana): yorum fiili sözlüğü (vurgula, yansıt, simgele, katkıda bulun, pekiştir, güçlendir, teşvik et, ortaya koy, gözler önüne ser) **cümle sonu yüklemde** (`-mAktAdIr/-Ar/-DI`) + öznenin cansız kurum/olgu olması · regex (güçlü çeviri izi): cümle sonunda `-arak/-erek` + "ki bu da"/", bu da" kuyruğu |
| C5 | Vague expression of connection or association (WP:AICONNECT); Ekim 2026'nın en yaygın 5 belirtisinden biri | A | "… ile bağlantılı olarak", "… ile ilişkilendirilmektedir", "… ile ilişkili", "… bağlamında", "… ile anılmaktadır", "… çerçevesinde", "özellikle/yaygın olarak … ile ilişkilendirilir". **Örnek:** "Profesör, üniversitedeki fen eğitimi **ile ilişkilendirilmektedir**." → "Profesör, üniversitede fen dersleri verdi." | regex + heur (doğrudan yüklem yerine "ilişkilendiril-" kullanımı) |
| C6 | Vague attributions and overgeneralization (WP:AIWEASEL) | A (güçlü) | "uzmanlara göre", "uzmanlar … olduğunu belirtiyor", "bazı eleştirmenler", "gözlemciler", "araştırmacılar ve koruma uzmanları", "akademik çevrelerde … olarak tanımlanır", "modern araştırmacılar … olarak ele alır", "sektör raporları", "çeşitli kaynaklar", "birçok yayın", "… gibi" (liste aslında tam olduğu halde), "yaygın olarak kabul edilmektedir", "genel kanı …", "… olduğu düşünülmektedir/bilinmektedir". **Örnek:** "Nehir, eşsiz özellikleri nedeniyle **araştırmacıların ve koruma uzmanlarının** ilgisini çekmektedir." | regex (kalıp) + LLM (kaynak sayısıyla tutarlılık) |
| C7 | Outline-like conclusions about challenges and future prospects (WP:FACESCHALLENGES) | A | "**…na rağmen**, X çeşitli zorluklarla karşı karşıyadır", "**Tüm bu zorluklara rağmen**", "Zorluklar ve Gelecek Perspektifleri" (başlık), "Geleceğe Bakış", "X'in geleceği, … uyum sağlama yeteneğine bağlıdır", "önümüzdeki on yıllarda", "potansiyel gelişmeler", "gelişmeye devam etmektedir", "… olmayı sürdürmektedir". **Örnek:** "Endüstriyel refahına rağmen Korattur, kentsel alanlara özgü **zorluklarla karşı karşıyadır** … stratejik konumu ve süregelen girişimleriyle **gelişmeye devam etmektedir**." | regex (çerçeve) + heur (metin sonunda yer alması) |
| C8 | "Awards and recognition" section; "X and Y" başlığı | A/C | "Ödüller ve Tanınırlık", "Miras ve Etki", "Zorluklar ve Gelecek", "Eleştiriler ve Tartışmalar" türünden **"X ve Y" başlıkları** | regex (başlıkta `^#+ .+ ve .+$`) |

### 3.2 Language and grammar

| # | EN kalıp | Sınıf | TR biçimleri ve örnek (aday) | Linter |
|---|---|---|---|---|
| L1 | High density of "AI vocabulary" (WP:AIVOCAB) | A (corpus doğrulaması şart) | Kelime kelime aday karşılıklar: Additionally → "**Ayrıca,**" / "Bunun yanı sıra," / "Buna ek olarak," (cümle başında) · crucial/pivotal/vital → "kritik", "kilit", "hayati", "son derece önemli", "belirleyici" · delve/deep dive → "derinlemesine incelemek", "…a derinlemesine dalmak" · enduring → "kalıcı", "süregelen", "köklü" · enhance → "geliştirmek", "güçlendirmek", "artırmak", "zenginleştirmek" · fostering → "teşvik etmek", "beslemek", "geliştirmek" · garner → "toplamak (ilgi/beğeni)", "kazanmak" · highlight/underscore/emphasize → "vurgulamak", "altını çizmek", "öne çıkarmak", "gözler önüne sermek" · interplay → "etkileşim", "karşılıklı etkileşim" · intricate → "karmaşık", "girift", "incelikli" · landscape (soyut) → "manzara", "ortam", "ekosistem", "alan" · meticulous → "titiz", "titizlikle", "özenle", "özenli" · robust → "sağlam", "güçlü", "gürbüz" · showcase → "sergilemek", "gözler önüne sermek" · tapestry → "**zengin dokusu**", "mozaiği", "renkli mozaik", "kilim gibi" · testament → "…nın kanıtı", "…nın canlı bir örneği", "…nın tanığı" · valuable → "değerli" · vibrant → "canlı", "hareketli", "dinamik", "renkli" · boasts → "…a sahiptir", "…ı barındırır", "…a ev sahipliği yapar" · align with → "…ile uyumlu", "…ile örtüşen" · bolstered → "güçlendirdi", "pekiştirdi" · GPT-6 dönemi → "pratik", "net/daha net", "istikrarlı", "sessizce", "öncelik vermek", "çok boyutlu", "kaldıraç olarak kullanmak", "evrensel olarak", "önemli olan …dır", "yankı buldu". | regex (sözlük) + heur (1000 kelime başına yoğunluk, birlikte görülme) |
| L2 | Avoidance of basic copulatives (WP:AINOCOPULA, WP:AIREPRESENTS) | A (en güçlü Türkçe analoglardan) | Basit ek-fiil ("-dır/-dir", "-dı", "vardır", "…dır", "var") yerine şunlar: "**… işlevi görmektedir**", "**… görevi görmektedir**", "**… konumundadır**", "**… niteliğindedir**", "… olarak hizmet vermektedir", "… olarak öne çıkmaktadır", "**… yer almaktadır**", "**… bulunmaktadır**" ("var" yerine), "… sunmaktadır" ("var/sahip" yerine), "… barındırmaktadır", "… temsil etmektedir", "… unvanına sahiptir", "… ifade etmektedir/… anlamına gelmektedir" (madde başında "refers to" karşılığı). **Örnek:** "Galeri 825, LAAA'nın sergi alanı **olarak hizmet vermektedir**. Galeri dört ayrı alan **sunmaktadır**." → "Galeri 825, LAAA'nın sergi alanıdır. Dört salonu var." Başka bir örnek: "ilk ve en eski tabloid **olma unvanına sahiptir**" → "ilk ve en eski tabloiddir". | regex (sözlük) + heur ("bulunmaktadır/yer almaktadır" oranının "var/-dır" oranına bölümü) |
| L3a | Negative parallelism: "Not just X, but also Y" (WP:AIPARALLEL) | C (Türkçe biçimiyle) | "**Sadece/Yalnızca X değil, aynı zamanda Y**", "**X'le kalmayıp Y**", "**Bu yalnızca bir X değil; bir Y'dir**", "**Mesele sadece X değil, Y**", "X olmanın ötesinde Y", "**hem X hem de Y**" (aşırı kullanıldığında). **Örnek:** "Otoportre **yalnızca bir** kendini temsil **değil**, saplantılarının görsel bir belgesi**dir**." Cümleler arası biçim: "…ünlü Duse ailesindendi. Ne var ki Eugenio'nun hayatı, kişisel hırs ile ailevi karmaşaların iç içe geçtiği bir yol izledi." (Burada tell, **beklenti kırma karşıtlık yapısıdır**, "ne var ki" bağlacı değil. "Ne var ki", projenin teşvik edeceği bağlaçlardandır ve flag listesine girmemelidir.) | regex |
| L3b | "Not X, but Y" | C | "**X değil, Y**", "**Bu bir X değil; bir Y.**", "**Ne X, ne Y, sadece Z**", "**X değil; aksine Y**", "Bu bir ayna değil, bir kapı: benliğin temsili değil, …". Tartışma yorumlarında sık: "Bu bir kaynak sorunu değil, sistemik bir önyargı." | regex: `\b\w+ değil[,;—–-]\s*\w+` + cümle sonu "değil." ardından gelen yeni cümle |
| L3c | "Y rather than X", son dönem LLM çıktısında özellikle yaygın | C | "**X yerine Y**", "**X'ten ziyade Y**", "**X'ten çok Y**", "**X olmaktan çok Y**", "**X'i değil, Y'yi önceleyerek**", "**yeni bir X sunmak yerine**". **Örnek:** "Yazılım, geleneksel disassembler'ların **yerine geçmekten ziyade** AI ajanları ile mevcut araçlar arasında **bir köprü** işlevi görür." | regex |
| L4 | Leads treating lists/broad titles as proper nouns | A (zayıf) | "**X (sağlık)**, … **ifade eder**", "**'Meksika hakkında şarkılar listesi'**, … **derlemesidir**", "X kavramı, … anlamına gelmektedir". Madde başı tanım kalıbı. | heur (ilk cümlede "ifade eder/anlamına gelir/olarak tanımlanır") |
| L5 | Rule of three (WP:RO3) | C | Üçlü sıfat ve öbekler: "zengin tarihi, manevi mirası ve doğal güzellikleri", "güvenilir, ölçeklenebilir ve sürdürülebilir", "mitolojik imgesi, büyülü silahları ve direniş ruhu". Değişiklik özeti, kısa not gibi süssüz olması beklenen bağlamda daha güçlü bir sinyal. | heur: "A, B ve C" kalıbı sayımı (`\w+, \w+ ve \w+`) + öbek uzunluk benzerliği. Paragraf başına ≥2 ise uyarı |

### 3.3 Style (Style alt sayfası dahil)

| # | EN kalıp | Sınıf | TR notu | Linter |
|---|---|---|---|---|
| S1 | Title case in headings (WP:AITITLECASE) | **C, ama Türkçede zayıf veya geçersiz** | **TDK'ya göre:** "Kitap, bildiri, makale vb.nde ana başlıktaki kelimelerin tamamı, alt başlıktaki kelimelerin ise yalnızca ilk harfleri büyük olarak yazılır." Ayrıca "ve, ile, ya, veya, yahut, ki, da, de" ile "mı/mi" küçük yazılır. Yani Türkçe resmî metinde alt başlıkta **her kelimenin büyük harfle başlaması TDK'ya uygundur** ve AI işareti sayılamaz. Web, Markdown ve sohbet bağlamında cümle düzeni ("Kurulum adımları") daha doğal olabilir. Linter'ın denetleyeceği şey: title case kullanılmışsa bağlaçların ("ve", "ile", "ki", "da/de") küçük yazılıp yazılmadığı. Tutarsızlık da denetlenmeli. | regex (bağlaç büyük harf hatası) |
| S2 | Overuse of boldface (WP:AIBOLD); asterisk ile bold (WP:AIASTERISK) | C | Düzyazı içinde kalın yazı yoğunluğu. Örnek: "**ortak çalışmanın doğası**", "**dilin zenginleşmesi değil bozulması**". | heur (100 kelime başına `**…**` sayısı; paragraf içi bold) |
| S3 | Inline-header vertical lists (WP:AILIST) | C | "- **Başlık:** açıklama" kalıbı. Satır başı madde işareti olarak •, -, –, # ya da emoji. | regex: `^\s*[-*•–]\s*\*\*[^*]+\*\*:?` |
| S4 | Heading errors (Title heading, skipping levels, overuse of level 1, headings only containing other headings) | C (Markdown'a uyarlanabilir) | Metni H1 başlıkla açmak, `# ` başlıkları birden fazla kullanmak, seviye atlamak (H2 → H4), altında metin olmayan başlık | regex/heur |
| S5 | Emoji as formatting (WP:AIEMOJI) | C | Başlık ya da madde başında emoji: "✨ Hakkımda", "🚀 İyi Düzenlemeler!" | regex (Unicode emoji, satır başında) |
| S6 | Unusual use of tables | C | Düzyazı ya da 2-3 satırla anlatılabilecek bilgiyi küçük tabloya dökmek | heur (≤3 satırlı tablo) |
| S7 | Curly quotation marks (WP:AICURLY) | **Türkçede B ya da çok zayıf** | Sayfanın kendisi, eğri tırnağın tek başına kanıt olmadığını söylüyor. Türkçe dizgide “ ” ve ’ normal sayılır (Word ve macOS akıllı tırnak). Denetlenecek olan karışıklık: aynı metinde " ve “ birlikte kullanılmışsa, ya da özel ad eki için ’ ile ' karışmışsa. | regex (tutarsızlık) |

### 3.4 Communication intended for the user

| # | EN kalıp | Sınıf | TR biçimleri (aday) | Linter |
|---|---|---|---|---|
| U1 | Collaborative communication (WP:CERTAINLY, WP:COLLABCOMM) | C (sycophancy + sohbet artığı) | "**Umarım yardımcı olur**", "**Elbette!**", "**Tabii ki!**", "**Kesinlikle haklısınız!**", "**Harika bir soru!**", "**İster misiniz…?**", "**…ister misiniz?**", "**Başka bir konuda yardımcı olabilir miyim?**", "**Bana bildirin / Haber verin**", "**İşte …:**", "**Aşağıda … bulabilirsiniz**", "**Daha ayrıntılı bir döküm**", "yayınlamadan önce kontrol etmeyi unutmayın", "Bu bölümde … ele alacağız", "Bu makalede … inceleyeceğiz". | regex (yüksek kesinlik) |
| U2 | Hedging disclaimers about source availability (WP:AIDISCLAIMER) 2023-24: didactic | C/A | "**Şunu belirtmek önemlidir ki**", "**Unutulmamalıdır ki**", "**Önemle belirtmek gerekir ki**", "**…ı ayırt etmek büyük önem taşır**", "**Göz önünde bulundurulmalıdır**", "kullanmadan önce mutlaka kontrol edin", "… farklılık gösterebilir". | regex |
| U3 | 2024-25: kaynak yokluğu | A | "**Ayrıntılı bilgi sınırlı olsa da**", "**…na ilişkin bilgiler kamuya açık kaynaklarda yer almamaktadır**", "**yaygın olarak belgelenmemiştir**", "**mevcut bilgilere göre / eldeki bilgilere dayanarak**", "**sağlanan kaynaklarda**", "**arama sonuçlarında**", "muhtemelen … desteklemektedir". | regex |
| U4 | Mid-2026-present: düzeltici çerçeveler | **A (güçlü, yakın dönem)** | "**X, Y olarak değil, Z olarak ele alınmalıdır**", "**…dan ziyade … olarak değerlendirilmelidir**", "**… tek başına … olduğunu kanıtlamaz / göstermez**", "**… olduğu sonucuna varmak için yeterli değildir**", "**… anlamına gelmez**", "**… ile karıştırılmamalıdır**". **Örnek:** "Mucizevi askıda durma iddiaları, arkeolojik bir açıklama**dan ziyade** dinî gelenek **olarak ele alınmalıdır**." Ek EN notu: Temmuz 2026'dan (GPT-5.6) önce bu kalıp neredeyse hiç görülmezdi. | regex |
| U5 | Phrasal templates and placeholder text (WP:AIPLACEHOLDER), tarih ve URL yer tutucuları | C | `[Adınız]`, `[Şirket Adı]`, `[buraya … ekleyin]`, `[Tarih]`, `XX.XX.20XX`, `example.com`, `INSERT_…` | regex (yüksek kesinlik) |
| U6 | Letter-style (mektup kalıbı) | C/A | "**Umarım bu mesaj sizi iyi bulur**" (Türkçe için birebir çeviri kokusu), "**Değerli … Ekibi,**", "**… amacıyla yazıyorum**", "**Anlayışınız için teşekkür ederim**", "**Saygılarımla, [Adınız]**" | regex |

### 3.5 Markup ve citations (çoğunlukla B; deterministik olan C maddeleri)

| # | EN kalıp | Sınıf | Not | Linter |
|---|---|---|---|---|
| M1 | Markdown in wikitext (`**`, `#`, `---`, `[text](url)`, ``` ``` ```) | B (bizim için Markdown normal) | Düz metin çıktısı istendiği yerde Markdown artığı: `**` ile kalınlaştırma, `##`, ```` ``` ````. Yalnızca hedef format düz metinse işaretle. | regex (bağlama bağlı) |
| M2 | Exposed citation internals `contentReference[oaicite:1]`, `↩` | C (kesin işaret) | `oaicite`, `contentReference`, `turn0search0`, `【…†source】` | regex |
| M3 | `utm_source=openai` / `chatgpt.com` / `copilot.com`, `referrer=grok.com` | C (kesin işaret) | URL parametresi | regex |
| M4 | Nonexistent categories/templates, broken links, invalid DOI/ISBN, unrelated DOIs, book citations without pages, unconventional reference reuse, named refs unused, outdated access-date | B | Wikitext/kaynakçaya özgü. Bizim kapsamımızda yalnızca "uydurma kaynak" uyarısı olarak skill'e taşınır. | — |

### 3.6 Comments / Edit summaries / Miscellaneous

| # | EN kalıp | Sınıf | TR notu | Linter |
|---|---|---|---|---|
| E1 | Comment-specific indicators: uydurma politika kısayolları, uzun ve başlıklı yorumlar, "insan emeği kattım" savunması, "içeriğe odaklanalım" | B (çoğu) / C | Müşteri hizmetleri tonu Türkçeye geçer: "**Olası bir rahatsızlık için özür dilerim**", "**Endişelerinizi anlıyorum**", "**Lütfen düzeltilmesi gereken belirli noktaları belirtin, gidermeye çalışayım**" | regex |
| E2 | Edit summaries (genel) | B | Vikipedi'ye özgü | — |
| E3 | Canned assurance of adherence (WP:AIASSURE). | **A (commit mesajı ve değişiklik notu bağlamında)** | "**Akıcılık ve netlik iyileştirildi**", "**okunabilirlik artırıldı**", "**anlatım sadeleştirildi/rafine edildi**", "**ton daha tarafsız hâle getirildi**", "**gereksiz tekrarlar giderildi**", "**… standartlarına uygunluk sağlandı**", "**… korunarak**", "**… bozulmadan**". Kendi işini aklama tonu. | regex |
| E4 | Specific mentions of "preserved"/"retained" information, "avoided" mistakes, procedural statements. İnsan değişiklik özetinin, değiştirilmeyen şeylerden ya da yapılmayanlardan söz etmesi alışılmadıktır. | **A (commit mesajı, PR açıklaması ve "ne değiştirdim" notu için çok alakalı)** | "**… korunarak**", "**orijinal anlam ve teknik ayrıntılar korunarak**", "**mevcut yapı korundu**", "**kaynaklar ve kategoriler korundu**", "**… değiştirilmeden bırakıldı**", "**… hatalarından kaçınıldı**", "**… sağlandı / … güvence altına alındı**", "**… amaçlandı / … hedeflendi**". **Örnek:** "Tanıtım dili kaldırıldı ve anlatım, **orijinal anlam ve teknik ayrıntılar korunarak** daha tarafsız bir tona kavuşturuldu." | regex |
| E5 | Overemphasis on presence/reliability of citations. | A (rapor ve özet bağlamında) | "**kaynaklı bilgi eklendi**", "**doğrulanmış içerik eklendi**", "**bağımsız/ikincil/hakemli kaynaklarla desteklendi**", "**atıflar iyileştirildi**". İnsan yazar içeriği söyler ("sanatçının ilk albümü eklendi"), AI kaynaklı olduğunu vurgular. | regex |
| E6 | Overemphasis on parameter/template names; Reference to AfC review | B / A (kod inceleme bağlamı) | Kod dünyasında karşılığı: "**inceleme geri bildirimleri doğrultusunda**", "**reviewer yorumları adreslendi**" türünden apaçık ve gereksiz bildirimler. Parametre adlarını gereksiz ayrıntıyla sıralamak. | regex (zayıf) |
| X1 | Pronounced shift in writing style | C (meta) | Kullanıcının kendi önceki metniyle karşılaştırma. Linter dışı, skill notu. | — |
| X2 | AfC submission statements, pre-placed maintenance templates, canned user pages | B / C | Kalıp başlıklar Türkçeye geçebilir: "**Hakkımda**", "**İlgi Alanlarım**", "**Hadi Bağlantı Kuralım!**" ve emoji | regex (emoji + başlık) |
| X3 | Permissions gaming, pro-authoritarian bias | B | Kapsam dışı | — |
| X4 | Differences between LLMs | Meta | Bkz. Bölüm 2 | — |

### 3.7 Historical indicators (azalan sinyaller; düşük ağırlıkla tutulmalı)

| # | EN kalıp | Sınıf | TR biçimleri (aday) | Linter |
|---|---|---|---|---|
| H1 | Promotional language 2023–2025 (WP:AIPUFFERY) | A | "**…nın kalbinde**", "**…nın kucağında yer alan / kucaklanmış**", "**eşsiz doğal güzellikleri**", "**nefes kesici**", "**büyüleyici**", "**zengin kültürel miras**", "**köklü geçmişi**", "**çığır açan**", "**ünlü/tanınmış/saygın**", "**geniş bir yelpaze/çeşitlilik**", "**…a olan bağlılığı/taahhüdü**", "**…ın en güzel örneklerinden**", "**ziyaretçilere büyüleyici bir deneyim sunar**", "**… ile sizi bekliyor**", "**…ın vazgeçilmez durağı**". Not: EN gözlemine göre AI metni "en iyi" türü üstünlük sıfatlarından **kaçınıyor**. | regex (sözlük) |
| H2 | Knowledge-cutoff disclaimers 2022–2023 (WP:AICUTOFF) | C | "**Son bilgi güncellememe göre**", "**Eğitim verilerimin kapsadığı tarihe kadar**", "**… itibarıyla elimdeki bilgilere göre**" | regex (kesin) |
| H3 | Section summaries (WP:CONCLUSION) | A | "**Sonuç olarak,**", "**Özetle,**", "**Kısacası,**", "**Genel olarak,**", "**Toparlamak gerekirse,**", "**Son tahlilde,**", "**Sonuç:**" (başlık), paragraf sonunda ana fikri yeniden söyleme | regex + heur (son paragrafın ilk kelimesi) |
| H4 | Prompt refusal | C | "**Bir yapay zekâ dil modeli olarak**", "**Bir yapay zekâ olarak**", "**Tıbbi tavsiye veremem ancak…**", "**Üzgünüm, ama…**" | regex (kesin) |
| H5 | Overuse of em dashes (2022–Eylül 2026) (WP:AIDASH) | C (**sönen sinyal**) | Türkçe gündelik yazıda uzun çizgi (—) nadirdir. **TDK uzun çizgi ve ara söz kuralı burada doğrulanmadı (tdk.gov.tr uzun-çizgi sayfası çekilemedi). Doğrulanmalı.** Not: TDK'nın "kısa çizgi"si `-` (hyphen) karakteridir, en dash (–) değildir. Formülsel kullanımı ("bu sadece X değil — Y") işaretlenmeli. **Önemli EN gözlemi:** Eylül 2026'dan sonra yeni modeller em dash'ten kaçınacak biçimde ayarlanmış. Bunun yan etkisi: *"the overall variety has dropped significantly in their output; commas and periods are more likely"*. → Yeni tell, **noktalama çeşitliliğinin düşük olması** (noktalı virgül, iki nokta, parantez, ünlem, soru yok) ve **tekdüze 8-20 kelimelik cümleler**. Projenin cümle çeşitliliği hedefini doğrudan destekliyor. | heur: em dash yoğunluğu (düşük ağırlık) + noktalama entropisi + cümle uzunluğu standart sapması |
| H6 | Abrupt cut offs | C | Yarım kalan son cümle | heur (son karakter noktalama değilse) |
| H7 | Outdated access-date | B | — | — |
| H8 | Lexical diversity / elegant variation (WP:AIELEVAR) | C → **Türkçede zayıf** | Aynı kavramı her geçişte farklı adlandırmak ("Sovyet sanat kısıtlamaları" / "devletin dayattığı sanatsal normlar" / "Sovyet rejiminin kısıtlamaları"). EN sayfası, bazı ülkelerde okulda sözcük tekrarından kaçınmanın öğretildiğini hatırlatıyor. Türk okul geleneği de "kelime tekrarından kaçın" öğretir. Bu yüzden Türkçe insan yazısında da sık görülür, zayıf işaret olarak tutulmalı. | LLM-only |

### 3.8 DE sürümünde olup EN'de olmayan (Türkçe için alakalı)

| # | DE kalıp | Sınıf | TR karşılığı | Linter |
|---|---|---|---|---|
| D1 | **Bestimmte Konjunktionen:** DE sayfası, "ayrıca", "bunun yanı sıra" türü bağlaçların modeller tarafından aşırı ve kalıpsal kullanıldığını söylüyor. | A | "**Ayrıca**", "**Bunun yanı sıra**", "**Buna ek olarak**", "**Bununla birlikte**", "**Öte yandan**", "**Dahası**", "**Üstelik**", "**Diğer taraftan**", "**Bu bağlamda**", "**Bu doğrultuda**", "**Nitekim**" (mekanik kullanım). Bkz. aşağıdaki EN "ineffective indicators" uyarısı: tek başına değil, **yoğunluk ve cümle başı tekrarı** ölçülmeli. | heur (cümle başı bağlaç oranı, aynı bağlacın tekrarı, çeşitlilik) |
| D2 | **Falsche Erweiterung:** "von … bis" ile sahte kapsam | A | "**…dan …a kadar**" sahte yelpaze: "**Tarihî yapılarından doğal güzelliklerine kadar**", "**kadim geleneklerden modern sanata uzanan**", "**…dan …a uzanan geniş bir yelpazede**". EN H1 örneği:"manzaralarından tarihî yapılarına kadar" türü bir yapı. | regex: `\w+(dan\|den\|tan\|ten) .{1,40} (a\|e\|ya\|ye) (kadar\|uzanan)` (mekân/zaman bağlamını hariç tutmak için heur) |

### 3.9 "Signs of human writing" ve "Ineffective indicators": **işaretlenmeyecekler** (linter false-positive koruması)

**Signs of human writing → Syntax** (EN sayfasından özetlendi): AI'da daha az, insan Vikipedi metninde daha sık görülenler:
- Basit "var/sahip" yapıları (EN: "there is a", "it has a"). → TR: "var", "-dır", "vardı", "sahipti" yerine sadece "-ı vardı". **Bu yapılar teşvik edilmeli**, L2'nin tersi.
- Süslü ya da örtmeceli eş anlamlılar yerine yalın fiiller. → TR'de AI tercihi solda, insan tercihi sağda: "**kaleme aldı** / yazdı", "**ikamet etmeye başladı, yerleşti** / taşındı", "**kullanım sağladı, istifade etti, yararlandı** / kullandı", "**girişimde bulundu** / denedi", "**hayatını kaybetti, vefat etti, aramızdan ayrıldı** / öldü". Not: "hayatını kaybetti" Türk haber dilinde de çok yaygındır, ağırlığı düşük tutulmalı.
- Üstünlük ve kesinlik bildiren ifadeler. → TR: "en iyilerinden", "tek", "ilk". AI bunlardan kaçınıyor, insan kullanıyor.
- Niteleyiciler ve pekiştirmeler. → TR: "çok", "belki", "galiba", "pek", "epey", "-mA eğiliminde".
- Dağınık hâlde geçen uzun kalıplar. → TR: "…ın bir sonucu olarak", "…mek amacıyla/için", "…ın tamamı", "…ın bir parçası", "**…dığı gerçeği**". İnsan yazısında dağınık hâlde bulunur, tek başına işaret değildir.

**Ineffective indicators** (EN'de işaret sayılmayanlar):
- Kusursuz dilbilgisi: kusursuz dilbilgisi AI kanıtı değildir.
- Gündelik ve resmî kaydın karışması: karışık üslup AI kanıtı değildir.
- "Sönük" ya da "robotik" üslup: tek başına değil.
- "Süslü", "akademik" ya da "resmî" üslup: korelasyon yalnızca **belirli kelimelerde**, genel resmî üslupta yok. → Türkçe resmî/bilimsel üslubu ("-mektedir", edilgen yapı) toptan AI işareti saymamak gerekir. Akademik Türkçe zaten "-mektedir" ağırlıklıdır.
- Geçiş sözcükleri (tek başına): yalnızca birkaçı yapay zekâda aşırı kullanılıyor ve bu örüntü insanın deneme tarzı yazısında da görülür. → **Bağlaç hedefimiz için kritik:** "Ayrıca" kelimesini tek başına işaretleme. Cümle başı oranını, tekrarı ve envanter darlığını ölç. Humanizer'ın hedefi bağlaç **çeşitliliği** (oysa, halbuki, ne var ki, zira, şu halde…), bağlaçları silmek değil.
- Kaynaksız içerik, tuhaf ya da doğru wikitext: B.

---

## 4. Türkçeye özgü uyarılar ve tasarım çıkarımları

1. **Türkçe karşılık sayfası yok.** Türkçe AI-tell envanteri ilk kez bu projede kurulacak. Yukarıdaki TR listeleri aday hipotezlerdir. Önerilen doğrulama: aynı istemlerle üretilmiş LLM Türkçe çıktıları ile 2022 öncesi Türkçe Vikipedi, köşe yazısı ve akademik özet corpus'u karşılaştırılmalı, her kalıp için 1 milyon kelime başına frekans oranı hesaplanmalı.
2. **En güçlü Türkçe analoglar (öncelik sırasıyla):**
   - (i) L2: "işlevi görmektedir / bulunmaktadır / yer almaktadır / sunmaktadır" (ek-fiilden kaçınma)
   - (ii) C4: cümle sonunda "-arak/-erek" ile yorum kuyruğu ve "ki bu da …"
   - (iii) U4: 2026 düzeltici çerçeveleri ("…dan ziyade … olarak ele alınmalıdır", "tek başına … kanıtlamaz")
   - (iv) L3: negatif paralellik ("sadece X değil, aynı zamanda Y", "X değil, Y")
   - (v) C1 ve C6: önem şişirme ve muğlak atıf ("uzmanlara göre")
   - (vi) H3 ve U1: kapanış ve sohbet artıkları
3. **"-mektedir" yoğunluğu** EN'de karşılığı olmayan, Türkçeye özgü bir eksen. EN'deki "copula avoidance" fikri Türkçede iki parçaya ayrılıyor: (a) "-dır" yerine perifrastik yüklem, (b) geniş zaman ya da "-dı" yerine "-mektedir". Linter ikisini ayrı oranlar olarak ölçmeli. Türün (akademik, haber, blog) normuna göre eşik değişmeli (Bölüm 3.9'daki "formal prose" uyarısı).
4. **Title case Türkçede AI işareti değil.** TDK alt başlıkta her kelimenin büyük harfle başlamasını öngörüyor. Yalnızca bağlaçların büyük yazılması ("Ve", "İle", "Ki") ve tutarsızlık denetlenmeli.
5. **Curly quote** Türkçe için işaret değil.
6. **Elegant variation** Türk okul kültüründe de öğretiliyor. Zayıf sinyal olarak tutulmalı ve LLM değerlendirmesine bırakılmalı.
7. **Em dash sönüyor.** Yerine şunlar ölçülmeli: (a) noktalama çeşitliliği (`;`, `:`, `(`, `?`, `!`, `…` oranları), (b) cümle uzunluğu dağılımı (standart sapma; 8-20 kelime bandında yığılma), (c) cümle tipi çeşitliliği (devrik, eksiltili, soru). Bunlar projenin "cümle çeşitliliği" hedefinin ölçüm tarafını oluşturur.
8. **Bağlaçlar:** EN "ineffective" uyarısı ile DE "Bestimmte Konjunktionen" maddesi birlikte değerlendirildiğinde kural şu: tekil bağlacı işaretleme. Şunları ölç: (a) cümle başı ek bağlaç oranı ("Ayrıca/Bunun yanı sıra/Buna ek olarak/Öte yandan/Bununla birlikte"), (b) aynı bağlacın N cümle içinde tekrarlanması, (c) envanter genişliği (kaç farklı bağlaç). Skill düzeltme yaparken bağlacı silmekle yetinmemeli, çeşitlendirmeli.
9. **Yüzey düzeltmesi yetmez.** EN sayfasının ana uyarısı bu. Skill'in akışı şöyle olmalı: tespit → içerik sorusu ("bu cümle hangi somut bilgiyi taşıyor?") → somut bilgi varsa yaz, yoksa cümleyi sil. Eş anlamlı değiştirmek tek başına yeterli değil, örneğin "kritik" → "çok önemli" yalnızca tespiti zorlaştırır.
10. **Deterministik, yüksek kesinlikli linter kuralları** (yanlış pozitifi düşük): U1, U5, U6, H2, H4, M2, M3, S5 (emoji başlık), S3 (inline-header list), C8 ("X ve Y" başlık). Sezgisel/yoğunluk kuralları: L1, L2, C1, C4, C6, L5, D1, H5. Yalnızca LLM ile değerlendirilecekler: C6'da kaynak sayısı tutarlılığı, H8, L4, genel "ortalamaya gerileme".

---

## 5. Hızlı regex taslakları (Python; smoke test sonuçları aşağıda)

**Türkçe büyük/küçük harf notu:** `re.IGNORECASE` Türkçede güvenilir değildir (`"İ".lower()` → `i̇`, I/ı ve i/İ eşleşmez). Önce Türkçe kurala göre küçült: `s.replace("İ","i").replace("I","ı").lower()`. Sonra IGNORECASE kullanmadan eşleştir. `CLOSERS` için `re.MULTILINE` gerekir ya da önce cümlelere bölünmelidir.

```python
SUPERFICIAL_PRED = r"\b(vurgul|yansıt|simgel|pekiştir|güçlendir|teşvik ed|katkıda bulun|altını çiz|ortaya koy|gözler önüne ser)\w*(maktadır|mektedir|ar|er|ır|ir|dı|di|du|dü|tı|ti)\s*[.!]"
SUPERFICIAL_TAIL = r",\s*[^.!?]{0,80}\b\w+(arak|erek)\s*[.!]"   # cümle sonu -arak: çeviri izi
KI_BU_DA        = r"\bki bu da\b"
COPULA_AVOID    = r"\b(işlevi|görevi) görmektedir\b|\b(konumunda|niteliğinde)(dır|dir)\b|\bolarak hizmet vermektedir\b|\b(bulunmaktadır|yer almaktadır)\b|\bunvanına sahiptir\b"
NEG_PARALLEL    = r"\b(sadece|yalnızca|salt)\b[^.]{1,60}\bdeğil\b[,;]?\s*(aynı zamanda|bilakis|aksine)?|\b\w+ değil[,;—–]\s*\w+|\b\w+(dan|den|tan|ten) ziyade\b|\byerine\b[^.]{1,60}\bolarak\b"
CORRECTIVE_2026 = r"\bolarak (ele alınmalı|değerlendirilmeli)\w*|\btek başına\b[^.]{0,60}\b(kanıtlamaz|göstermez|ispatlamaz)\b|\bile karıştırılmamalıdır\b|\banlamına gelmez\b"
CHALLENGES      = r"\b(rağmen)\b[^.]{0,80}\bzorluklarla karşı karşıya\w*|\btüm bu zorluklara rağmen\b|\bgeleceğe bakış\b"
WEASEL          = r"\b(uzmanlara göre|uzmanlar(a)? (göre|belirtiyor|vurguluyor)|bazı (eleştirmenler|uzmanlar|araştırmacılar)|gözlemciler|sektör raporları|çeşitli kaynaklar|yaygın olarak kabul edil\w+)\b"
CONNECT         = r"\b(ile bağlantılı olarak|ile ilişkilendiril\w+|ile anıl\w+)\b"
CLOSERS         = r"^(sonuç olarak|özetle|kısacası|genel olarak|toparlamak gerekirse|son tahlilde)[,:]"   # re.MULTILINE
CHATTY          = r"\b(umarım (bu )?yardımcı olur|elbette!|tabii ki!|kesinlikle haklısınız|harika bir soru|başka bir konuda yardımcı olabilir miyim|bana bildirin|ister misiniz\?)"
DISCLAIMER      = r"\b(şunu belirtmek önemlidir|unutulmamalıdır ki|önemle belirtmek gerekir|mevcut bilgilere göre|eldeki bilgilere dayanarak|yaygın olarak belgelenmemiştir|kamuya açık kaynaklarda yer almamaktadır)\b"
AI_SELF         = r"\b(bir yapay zek[aâ] (dil modeli )?olarak|son bilgi güncellememe göre|eğitim verilerimin)\b"
PLACEHOLDER     = r"\[(adınız|ad soyad|şirket adı|tarih|buraya[^\]]*)\]|insert_\w+|example\.com"
LEAKS           = r"contentReference\[oaicite:\d+\]|oaicite|utm_source=(openai|chatgpt\.com|copilot\.com)|referrer=grok\.com|turn\d+search\d+"
FALSE_RANGE     = r"\b\w+(dan|den|tan|ten)\b[^.]{1,50}\b\w+(a|e|ya|ye|na|ne)\s+(kadar|uzanan)\b"
PROMO           = r"\b(kalbinde|kucağında|nefes kesici|büyüleyici|eşsiz doğal güzellik\w*|zengin kültürel miras\w*|çığır açan|geniş bir yelpaze\w*)\b"
```

Tüm kalıplar **Türkçe kurala göre küçültülmüş** metne uygulanmak üzere küçük harfle yazıldı. **Smoke test (2026-11-05):** 17 kalıbın 17'si tablolardaki örnek cümleleri yakaladı. CLOSERS ilk denemede büyük harf yüzünden kaçırıyordu, düzeltildi. Yanlış pozitif testi **yapılmadı**: NEG_PARALLEL içindeki `yerine…olarak` ve FALSE_RANGE kalıpları gerçek mekân/zaman ifadelerinde patlayabilir, corpus ile kalibre edilmeli.

Her kural tek başına bir **puan** üretmeli, ikili karar vermemeli. Metin düzeyindeki karar yoğunluk ve birlikte görülme ile verilmeli.
