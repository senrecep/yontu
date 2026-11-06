# Yoğunlaştırma ve söz varlığı

Ne zaman oku: `concise` kipinde, linter `YS-` ile başlayan bir bulgu verdiğinde ya da metin
hafif fiil, `bir şekilde` zarfı, boş "olan" ve totoloji ile şiştiğinde. Bu dosya kısaltmanın
nerede durması gerektiğini de söyler. Şişkin biçimler kod içinde, önce örnekleri alıntı
bloğundadır.

## Temel ilke

Yoğunlaştırma bir yoğunluk sinyalidir. Tek eşleşme hata değildir. "karar vermek", "yardım
etmek", haberde "meydana gelmek", hukukta "söz konusu" doğal Türkçedir. Bir kalıp iki koşul
birlikte sağlanınca sorundur: aynı aile metinde sık geçer (300 sözcükte 3 ve üstü, akademik
ve hukukta 9 ve üstü) ve kalıp türe yabancıdır (blogda `gerçekleştirilmektedir`).

Kısa metin kapısı burada da geçerlidir: 50 sözcüğün altında yoğunluk kuralları kapalıdır,
yalnız mutlak sayım yapılır. 50-150 sözcükte en az iki eşleşme gerekir. 150 ve üstünde oran
kullanılır.

Kısaltmak için anlam feda edilmez. Kısa ama iddiası güçlenmiş bir cümle, uzun ve doğru bir
cümleden kötüdür.

## Katmanlar

Her satırın bir modu vardır:

| Mod | Ne olur |
|---|---|
| L | linter `info` verir, varsayılan açık |
| L0 | linter `info` verir, varsayılan kapalı (`--enable concision-extra` ya da profil açar) |
| S | linterde yoktur, yalnız bu dosyada ve yeniden yazımda kullanılır |

Özlülük kuralları hiçbir zaman `warning` olmaz, otomatik düzeltilmez. Linter bulguda kural
kimliğini (`YS-A57`), aileyi, kanıt düzeyini ve en çok üç karşılık adayını gösterir. Aday
öneridir, seçim bağlama bakılarak yapılır.

Bir satır linterde ancak üç koşulla yer alır: sabit dizgiyle ya da dar bir düzenli ifadeyle
yakalanır, eşleşme bağlamdan bağımsız aynı anlama gelir ve karşılık anlam seçimi gerektirmez.

## A. Hafif fiil ve adlaştırma

Türkçe eylemi fiille söyler. `X işlemini gerçekleştirmek`, `X'in sağlanması` İngilizce
"perform, provide, carry out" yapısının izidir. Ölçüt, zaten fiili olan bir adın genel fiille
kurulması ya da "işlem, süreç, faaliyet" sarmalayıcısıdır. Sözlükleşmiş hafif fiiller
doğaldır: karar vermek, yardım etmek, söz vermek, hata yapmak, teşekkür etmek.

L (linter):
- `kontrol işlemini gerçekleştirmek` → denetlemek, kontrol etmek (A01)
- `değerlendirme yapmak` → değerlendirmek (A03), `inceleme yapmak` → incelemek (A04)
- `güncelleme yapmak` → güncellemek (A06), `iyileştirme yapmak` → iyileştirmek (A09)
- `ödeme işlemini gerçekleştirmek` → ödemek (A10), `kayıt işlemini gerçekleştirmek` →
  kaydolmak (A11), `giriş işlemini gerçekleştirmek` → giriş yapmak, oturum açmak (A12)
- `kutlama gerçekleştirmek` → kutlamak (A14), `sohbet gerçekleştirmek` → sohbet etmek (A16)
- `test işlemini`, `kurulum işlemini`, `silme işlemini gerçekleştirmek` → test etmek, kurmak,
  silmek (A21-A23), `gönderme işlemini yapmak` → göndermek (A24)
- `-mA işlemini gerçekleştirmek` genel kalıbı (A25, öneriyi skill seçer)
- `kullanımı sağlanmaktadır` → kullanılır (A54)
- `-mAsI mümkündür` → -Abilir, `-mAsI mümkün değildir` → -AmAz,
  `-mA imkânı bulunmaktadır` → -Abilir (A57-A59)
- yalnız şu sabit liste: `belirtmek isterim`, `ifade etmek isterim`, `vurgulamak isterim`,
  `teşekkür etmek isterim` (A81). "gitmek isterim" gerçek istektir, eşleşmez.
- `bilgilendirme yapmak` → bilgilendirmek (A93), `paylaşımda bulunmak` → paylaşmak (A94)

L0: `önem arz etmek` → önemli olmak (A89). Hukukta kapalıdır, orada terimdir.

S (yeniden yazımda, bağlama bakarak):
- `katkı sağlamak`, `katkıda bulunmak` → katkı sunmak. "katkı sunmak" yerleşiktir, işaretlenmez.
- `yardımcı olmak` → yardım etmek, kolaylaştırmak, katkı sunmak. "hızlandırır" gibi tam neden
  bildiren fiile çevirme, iddia güçlenir.
- `olanak sağlamak`, `imkân sunmak` → -Abilmek: "X sayesinde Y yapabilirsiniz".
- `artış göstermek` → artmak, `gelişme göstermek` → gelişmek. Akademikte kalabilir.
- `sahip olmak` (soyut iyelik) → -lI, var: `geniş bir deneyime sahip` → "deneyimli".
- `-mAsI gerekmektedir` → -mAlI(dIr). Kip korunur: zorunluluk öneriye dönmez.
- `-mAsI durumunda` → -sA. Hukukta "-mAsI hâlinde" terimdir, dokunma.
- `-mAsInI sağlamak` → ettirgen: "çalışmasını sağlar" → "çalıştırır", yalnız fail açıksa.
- `yer vermek` → "bulunur, yer alır". "eklendi" demek anlamı değiştirir.
- `ortaya koymak` → göstermek. Akademikte "ortaya koymaktadır" terimdir, dokunma.
- `meydana gelmek` haberde terimdir. `açıklama yapmak` haberde kalır.

Kaldırılan: `-mAsInA neden olmak` → `öldürdü` türü dönüşüm failliği değiştirir. "Ölümüne
neden oldu" dolaylı nedendir, "öldürdü" doğrudan faildir. Bu dönüşüm yapılmaz.

## B. `bir şekilde` zarfı

`-lI bir şekilde` ve `-lI bir biçimde` çoğu zaman yalın zarf ya da `-cA` ekiyle kısalır. Bir
eşleşme tek bulgu üretir. Genel düzenli ifade ile tablo satırı aynı yeri yakalarsa bir kez
sayılır.

L:
- `hızlı bir şekilde` → hızla, hızlıca (B01), `dikkatli bir şekilde` → dikkatle (B02)
- `kolay bir şekilde` → kolayca (B03), `açık bir şekilde` → açıkça (B04)
- `etkili bir şekilde` → etkili (B05), `verimli bir şekilde` → verimli (B06)
- `başarılı bir şekilde` → başarıyla (B07), `sorunsuz bir şekilde` → sorunsuz (B08)
- `sürekli bir şekilde` → sürekli (B10), `detaylı bir şekilde`, `ayrıntılı bir şekilde` →
  ayrıntılı (B11), `kapsamlı bir şekilde` → kapsamlı (B12)
- `doğru bir şekilde` → doğru (B13), `güvenli bir şekilde` → güvenle (B14)
- `sessiz bir şekilde` → sessizce, `yavaş bir şekilde` → yavaşça, `sakin bir şekilde` →
  sakince, `rahat bir şekilde` → rahatça (B16-B19)
- `özenli bir şekilde` → özenle, `titiz bir şekilde` → titizlikle, `acil bir şekilde` →
  acilen, `sabırlı bir şekilde` → sabırla, `net bir şekilde` → net (B22-B26)
- `tam bir şekilde` → eksiksiz, `sistematik bir şekilde` → sistemli, `yoğun bir şekilde` →
  yoğun (B30-B32)
- `kesin bir şekilde` → kesinlikle, `sıkı bir şekilde` → sıkıca, `derin bir şekilde` →
  derinden (B44-B47)
- `kalıcı bir şekilde` → kalıcı olarak, temelli (B49), `bilimsel bir şekilde` → bilimsel
  olarak (B51)
- teknik metinde `otomatik bir şekilde` → otomatik, `manuel bir şekilde` → elle (B52, B53)
- `doğrudan bir şekilde` → doğrudan (B54)

L0: `doğal bir şekilde` (B33). İki anlamı vardır: "doğaya uygun biçimde" ve cümle zarfı olarak
"elbette". Seçim bağlam ister.

S (bağlama bakarak):
- `düzenli bir şekilde` → düzenli olarak. "sık sık" değil, düzenlilik sıklık demek değildir.
- `iyi bir şekilde` → iyi. "iyice" tamamen anlamı da taşır, yalnız bağlam uygunsa.
- `şeffaf bir şekilde` → açıkça.
- `geçici bir şekilde` → geçici olarak. Yalnız zarf kullanımında "şimdilik".
- `eşit bir şekilde` → eşit olarak. "adil biçimde" değil.
- `önemli bir şekilde` → büyük ölçüde. Akademikte `anlamlı bir şekilde` istatistik terimi
  olabilir: "anlamlı düzeyde".
- `kolayca ve hızlıca ve güvenlice` gibi zarf yığını → tek zarf ve fiil.

Kaldırılan: `olumsuz bir şekilde` → `kötü` ("olumsuz etki" kötü etki değildir) ve
`tutarlı bir şekilde` → `hep` (tutarlılık süreklilik değildir). Bu iki satır önerilmez.

## C. Boş "olan" ve bağlantı şişmesi

L:
- `-dA yer alan` → -dAki: `tabloda yer alan değerler` → tablodaki değerler (C03)
- `ile ilgili olan` → ile ilgili (C07), `-A yönelik olan` → -A yönelik (C08)
- iç içe `olan … olan` zinciri: birini sıfata çevir ya da cümleyi böl (C23)

L0: `mevcut olan` yalnız ardından ad gelince (C17). "mevcut olanı korumak" adlaşmıştır.

S:
- `önemli olan konu` → önemli konu. "Önemli olan, …" kalıbı ayrıdır, dokunma.
- `-dA bulunan` → -dAki, `-A ait olan` → -In, `-mAkta olan` → -An.
- `konusunda`, `noktasında`, `açısından` sarmalayıcıları çoğu zaman hâl ekine iner.
- `sahip olduğu bilgi` → bildiği.
- Akademikte `yapılan çalışmalar`, `elde edilen bulgular` → çalışmalar, bulgular.
- `ki bu da` → yeni cümle ya da `-dIğIndan`.
- `üç bölümden oluşan rapor` → üç bölümlü rapor.

## D. Totoloji ve gereksiz söz

L:
- `geri iade` → iade (D01), `en optimum` → optimum, en uygun (D02), `en ideal` → ideal (D03)
- `en maksimum`, `en minimum` → en çok, en az (D05)
- `en son olarak` → son olarak (D09)
- `sebebi … -den dolayıdır` → nedeni …-dır (D10), `amacı … -mak içindir` → amacı …-mak(tır)
  (D11)
- `yeniden tekrar`, `tekrar yeniden` → biri (D13, D14)
- `birlikte iş birliği yapmak` → iş birliği yapmak (D32), `birbirleriyle karşılıklı` →
  biri (D16)
- `sonuç olarak sonuçta`, `ama fakat`, `ve ayrıca`, `bunun yanı sıra ayrıca` → biri (D21-D24)
- `vb. gibi` → biri (D26)
- `tahminen yaklaşık`, `hemen hemen neredeyse`, `kesinlikle mutlaka`, `olası ihtimal` →
  biri (D28-D31)
- `ortak paylaşım` → paylaşım, `tüm … hepsi`, `bütün herkes` → biri (D33-D35)
- `yeni yenilikler` → yenilikler, `şu anki mevcut` → biri (D37, D38)
- `eş zamanlı olarak aynı anda`, `her zaman daima` → biri (D40, D41)
- `son derece çok` → biri, `X'in kendisi bizzat` → biri (D44, D45)
- `kısaca özetlemek gerekirse` → kısaca (D47), `zaten hâlihazırda` → biri (D50)

L0: `en mükemmel` (D04), `karşılıklı iş birliği` (D15), `asla hiçbir zaman` (D42),
`örneğin … gibi` (D25, tek cümle içinde ve en çok 8 sözcük arayla), `yaklaşık N kadar` (D27,
yalnız sayıdan sonra).

S:
- `temel esas`, `baş başlıca` → biri. Hukukta "temel esaslar" terimdir, dokunma (D43).
- `kısa bir özet`, `ilk önce`, `ön hazırlık`, `geçmiş deneyim`: vurgu taşıyabilir. Yalnız
  yinelenirse öner.
- `şunu belirtmek gerekir ki` → sil. `önemli olduğunu belirtmek gerekir` → X önemlidir.
- `sorunsuz ve hatasız` gibi çift: anlamlar örtüşüyorsa biri.

Akboğa (2026) Türkçe Ulusal Derlem verisiyle şunu gösterir: "gereksiz sözcük" sayılan eş ya
da yakın anlamlı çiftler (arzu-istek, güç-zor, düşünce-fikir, seçenek-alternatif) anlama
ayrı katkı yapar ve mutlak gereksiz değildir. "açık ve net", "güç ve zor" gibi çiftlere tek
geçişte dokunma. Yalnız metinde üç ve üstü kez yineleniyorsa öner.

## E. Çeviri kalıbı öbekler

Linter bu aileyi tek tek işaretlemez, yalnız yoğunluğu sayar (300 sözcükte 3 ve üstü).
Satırları yeniden yazarken sen ele alırsın.

- `önemli bir rol oynamak` → önemlidir, belirleyicidir, payı büyük
- `kilit rol oynamak` → belirleyici olmak
- `günün sonunda` → sonuçta
- `fark yaratmak` → öne çıkmak, katkı sunmak
- `bir yolculuk` (mecaz) → süreç, ya da sil. Yalnız blog ve e-postada.
- `derinlemesine dalmak` → ayrıntısıyla incelemek
- `-In altını çizmek` → vurgulamak
- `kapı açmak` → yol açmak, `köprü kurmak` → birleştirmek, yakınlaştırmak
- `büyük resmi görmek` → bütünü görmek, `aynı sayfada olmak` → aynı fikirde olmak
- `-mAktAn çekinmeyin` → -Abilirsiniz
- `herhangi bir sorunuz olursa` → sorunuz olursa
- `-In bir parçası olmak` → -A katılmak
- `emin olun` (teknik) → kontrol edin
- `gerçek zamanlı olarak` → anlık
- `giderek artan bir şekilde` → giderek, gitgide
- `-In bir sonucu olarak` → -In sonucunda, -den dolayı
- `-mAk adına` ("için" anlamında) → -mAk için
- `geri dönüş` (feedback) → geri bildirim
- `-A değer katmak` → zenginleştirmek, güçlendirmek
- `-In kalbinde` → -In özünde

Kaldırılan: "masaya yatırmak", "göz ardı etmek" ve "ışık tutmak" yerleşik Türkçe deyimlerdir.
Çeviri kalıbı sayılmaz, önerilmez. "yeni bir sayfa açmak" da Türkçe deyimdir, dokunma.

## F. Genel fiil ve sıfat tekrarı

AI metni çok farklı kavramı tek genel fiille söyler: sağlamak, yapmak, artırmak, önemli.
Linter yalnız tekrar yoğunluğunu sayar (aynı genel fiil 300 sözcükte 4 ve üstü). Karşılık
seçimi sende, nesneye bakarak:

| Genel sözcük | Nesneye göre seçenek |
|---|---|
| artırmak | çoğaltmak (sayı), büyütmek (boyut), yükseltmek (oran) |
| azaltmak | düşürmek (oran, fiyat), kısmak (ses, harcama) |
| sağlamak | vermek, sunmak, getirmek, kazandırmak |
| kullanmak | yararlanmak (kaynak), başvurmak (yöntem), uygulamak |
| göstermek | belgelemek, sergilemek. Akademikte kanıt basamağını koru. |
| oluşturmak | kurmak (yapı), yazmak (metin), çizmek (plan) |
| önemli | belirleyici, can alıcı, kayda değer |
| sorun | güçlük, engel, aksaklık, pürüz |

"arttırmak" bir yazım çeşidi değildir, ayrı ve ettirgen bir maddedir. "artırmak" için
karşılık olarak önerilmez, yazım hatası da sayılmaz.

Eş anlamlı döndürme yasaktır. Aynı kavram aynı terimle sürer. Zenginlik, farklı kavramlara
farklı ve isabetli fiil demektir.

Deyim ve ikileme önerileri (`kolları sıvamak`, `didik didik etmek`, `ter dökmek`,
`adım adım`, `boş yere`, `yığınla`, `uzun lafın kısası`, `yavaş yavaş`) yalnız blog, sohbet ve
e-postada yapılır. Metin başına en çok bir iki tane. Her paragrafa bir deyim koymak da bir
izdir. Akademik, resmî, hukuk ve teknik metinde deyim önerme.

## G. Arapça ve Farsça kökenli sözcükler

Bu ailenin linterdeki satırları varsayılan kapalıdır (L0). Kullanıcı ya da profil açarsa
`info` verir. Öneri yönlendirmedir, hata bildirmez.

- `müracaat` → başvuru, `husus` → konu, `netice` → sonuç, `ispat etmek` → kanıtlamak
- `binaenaleyh` → bu yüzden, `mütemadiyen` → sürekli, `ekseriyetle` → çoğunlukla
- `tatbik etmek` → uygulamak, `istifade etmek` → yararlanmak, `münasebet` → ilişki
- `nazaran` → -A göre, `bilhassa` → özellikle, `akabinde` → ardından
- `teferruat` → ayrıntı, `lüzum` → gerek, `malumat` → bilgi, `kifayet etmek` → yetmek

Kapsam:
- Akademik ve hukuk metninde bu sözcükler terim olabilir. Orada öneri yapma.
- Hukukta "müracaat", "mütalaa", "teşkil eder", "işbu", "mezkûr" yerleşiktir.
- Resmî yazıda kurum dili sürer.
- Deneme ve edebî metinde eski sözcük bilinçli seçim olabilir. G ailesi kapalıdır.
- Öz Türkçe karşılık her zaman doğal değildir. Önerilen karşılıkların bir kısmı kullanıma
  girmemiştir. Okurun tanımadığı bir sözcüğü önerme.

## Dokunulmayacaklar

1. Sözlükleşmiş hafif fiiller: karar vermek, yardım etmek, söz vermek, hata yapmak, ziyaret
   etmek, teşekkür etmek, kabul etmek, dikkat etmek, merak etmek, kontrol etmek.
2. Türün yerleşik terimleri:
   - haber: "meydana geldi", "açıklama yaptı", "artış gösterdi"
   - hukuk: "söz konusu", "-e ilişkin", "hâlinde", "talepte bulunmak", "yerine getirmek"
   - akademik: "ortaya koymaktadır", "analiz edilmiştir", "amaçlanmıştır",
     "anlamlı farklılık", "gelişmekte olan ülkeler"
3. Vurgu ve ritim taşıyan çiftler: "açık ve net", "güç ve zor".
4. Deneme ve edebî metinde bilerek seçilmiş eski sözcük.
5. Kısaltma anlamı değiştiriyorsa:
   - `başarıyla tamamlandı` → "tamamlandı" yalnız başarısızlık seçeneği yoksa.
   - `-mAsI gerekmektedir` → "-mAlI" dönüşümünde zorunluluk korunur.
   - Kanıt fiilleri basamaklıdır: düşündürmek < işaret etmek < göstermek < kanıtlamak.
     Akademikte bir basamaktan ötekine geçilmez.
6. Tek sözcük her zaman daha iyi değildir. "göz önünde bulundurmak" ile "gözetmek" eş
   değildir, "gözetmek" korumak anlamı da taşır.
7. Öneri ilk geçişte değil, aile yoğunluk eşiğini aşınca yapılır.

## Örnekler

> Önce: Kurulum işlemini gerçekleştirdikten sonra, yapılandırma dosyasında gerekli olan değişikliklerin yapılması gerekmektedir.

Sonra: Kurulumdan sonra yapılandırma dosyasında gerekli değişiklikleri yapın.

"gerekli" belirli bir değişiklik kümesini gösterdiği için kaldı. Teknik metinde gereklilik
emirle verilir.

> Önce: Bu yöntem, verimliliğin artırılması konusunda önemli bir rol oynamakta ve kullanıcılara zaman tasarrufu sağlama imkânı sunmaktadır.

Sonra: Bu yöntem verimliliği artırmaya önemli katkı sunar ve kullanıcıya zaman
kazandırabilir.

Derece korundu: "önemli rol" tek neden değildir, bu yüzden "artırır" yazılmadı. "imkânı
sunar" kipi "-Abilir" oldu.

> Önce: Herhangi bir sorunuz olması durumunda benimle iletişime geçmekten çekinmeyin.

Sonra: Sorunuz olursa bana ulaşabilirsiniz.

> Önce: Çalışmada elde edilen bulgular, söz konusu değişkenler arasında anlamlı bir ilişkinin var olduğunu ortaya koymaktadır.

Sonra: Çalışmanın bulguları, bu değişkenler arasında anlamlı bir ilişki olduğunu ortaya
koymaktadır.

Akademik kayıt ve `-mAktAdIr` korundu. Yalnız `elde edilen` ve `var olduğunu` kısaldı.

> Önce: Ürünü geri iade etmenin sebebi, kargoda hasar görmesinden dolayıdır.

Sonra: Ürünün iade nedeni, kargoda hasar görmesidir.

Kaynakta iade olmuş bir olay olarak söylenmiyor. "iade edildi" ya da "iade ettik" yazmak
olay ve özne ekler.

Haber metninde "Deprem saat 04.30'da meydana geldi." cümlesine dokunulmaz.
