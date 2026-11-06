# Yapay zekâ ve çeviri izleri

Ne zaman oku: Linter çalışmadığında metni elle taramak, bir bulguyu açıklamak ya da neyin
gerçekten iz olduğuna karar vermek için. Kimlikler (A1, B4, C3…) linter kural adlarıyla
eşleşir. Kalıplar kod içinde, önce örnekleri alıntı bloğunda verilir.

Bu kalıplar tek başına kanıt değildir. Bir kalıbın bir kez geçmesi doğaldır. Sorun yoğunluk
ve bir arada görülmedir. Kısa metinde (50 sözcüğün altında) tek tek say, 50-150 sözcükte en
az iki eşleşme ara, daha uzun metinde oranlara bak. Akademik ve hukuk metninde eşikler üç kat
yüksektir.

## A. Sözcük ve kalıp

A1 Önem şişirme. `kilit rol`, `kritik öneme sahip`, `hayati önem taşır`,
`vazgeçilmez bir hâle gelmiştir`, `çığır açan`, `devrim niteliğinde`. Önemi gösteren bilgi
varsa onu bırak, şişirmeyi sil. Bilgi yoksa düz "önemli" yeter.

A2 Hafif fiil. `gerçekleştirmek`, `sağlamak`, `yapmak`, `bulunmak`, `etmek` ile kurulan
adlaştırma. "Kurulum işlemini gerçekleştirmek" yerine "kurmak". Ayrıntı `yogunlastirma.md`.

A3 Boş sıfat. `kapsamlı`, `bütüncül`, `eşsiz`, `benzersiz`, `paha biçilmez`, `yenilikçi`,
`dinamik`, `sorunsuz`, `zengin bir mozaik`. Ölçülebilir bir özellik yoksa sil.

A4 Moda mecaz. `yolculuk`, `goblen`, `manzara`, `ekosistem`, `senfoni`, `sinerji`,
`yol haritası`, `X'in dinamik dünyasında`. Düz adı kullan: "yeni bir yolculuk" yerine "yeni
bir iş", ama yalnız girdi bunu söylüyorsa.

A5 Bürokratik geçiş. `Bu bağlamda`, `Bu çerçevede`, `Bu doğrultuda`, `Öte yandan`,
`Bununla birlikte`, `Bunun yanı sıra`, `Ek olarak`, `X kapsamında`, `X noktasında`.
Bkz. `baglaclar.md`.

A6 Kalıp açılış. `Günümüzde`, `Dijital çağda`, `Hepimizin bildiği gibi`,
`Bu yazıda X'i ele alacağız`, `Gelin birlikte inceleyelim`. İlk cümle doğrudan konuya girer.

A7 Kalıp kapanış. `Sonuç olarak`, `Özetle`, `Tüm bunlar göz önüne alındığında`,
`Unutmayın`. Metin zaten özetliyorsa kapanış paragrafını sil. Yeni bilgi taşıyorsa bağlacı
sil, cümleyi bırak.

A8 Dolgu. `Önemle belirtmek gerekir ki`, `Unutulmamalıdır ki`, `tam da`, `gerçekten de`,
`esasen`, `nihayetinde`. Sil. Tek bir "aslında" sorun değildir.

> Önce: Günümüzde giderek önem kazanan veri güvenliği, şirketler için kritik bir rol oynamaktadır.

Sonra: Veri güvenliğinin şirketler için önemi giderek artıyor.

## B. Çeviri kalıpları

| Kimlik | Kalıp | Ne yap |
|---|---|---|
| B1 | `günün sonunda` | "sonuçta" ya da sil |
| B2 | `masaya getirmek` | "önermek", "sunmak" |
| B4 | `-e sahip olmak` | "-lI", "var": "üç odası var" |
| B5 | gereksiz `tarafından` | etken çatı, özne biliniyorsa |
| B6 | `bir X olarak` | "X olarak" ya da "-ken", çoğu zaman sil |
| B8 | `bir güncelleme yaptık` | "güncelledik" |
| B9 | her cümlede `-Abilir` | kesin bilgi kesin söylenir, ama girdideki çekinceyi koru |
| B10 | `ve` zinciri | ekle bağla, cümleyi böl |
| B11 | üçten uzun tamlama zinciri | fiil cümlesine çevir |
| B12 | `bu, … anlamına gelir` | "demek ki", "yani" |
| B13 | `Sadece X değil, aynı zamanda Y` | "X olduğu kadar Y", "hem X hem Y" |
| B14 | `sizi iyi bulur` | sil |
| B15 | `çekinmeyin`, `çekinmeden` | "yazabilirsiniz", "sorabilirsiniz" |
| B16 | `dört gözle bekliyorum` | "bekliyorum" ya da sil |
| B17 | `X'in bir kanıtıdır` | "X'i gösterir", kanıt basamağını koru |
| B18 | `emin olun` | "kontrol edin", "denetleyin" |
| B19 | `önemini vurgular` | ne vurguladığını yaz ya da sil |
| B28 | gereksiz zamir (`ben`, `biz`, `siz`) | kişi eki yeter |
| B29 | gereksiz `bir` | `önemli bir şekilde` → "önemli ölçüde" |
| B30 | pleonazm | bkz. `yogunlastirma.md` D ailesi |

> Önce: Bu uygulama, kullanıcıların verilerine erişim sağlayabilmesi için birçok özelliğe sahiptir.

Sonra: Uygulamanın, kullanıcıların verilerine erişebilmesi için birçok özelliği var.

## C. Söz dizimi ve biçim

C1 `-mAktAdIr` yoğunluğu. Blog ve e-postada %15'in üstü, akademik metinde %45'in üstü
yapay okunur. Geniş ya da şimdiki zamana çevir. Akademik ve hukuk metninde tek tek
dokunma.

C2 `-mIştIr` ve `-DIr` sonu. Tanım cümlesinde `-DIr` doğaldır. Her cümle `-DIr` ile bitiyorsa
(%40 ve üstü) bir kısmını çıkar: "Bu yöntem hızlıdır." → "Bu yöntem hızlı."

C3 `-ArAk` zinciri. AI metinlerinde çok sık. Bir cümlede bir kez kullan. Bkz.
`cumle-turleri.md` zarf-fiil paleti.

C4 Tekdüze cümle uzunluğu. Uzunlukları türün bandı içinde değiştir. Yalnız bilgi notudur.

C5 Adlaştırma. `-mAsI`, `-mA` zinciri. Fiili geri getir.

C6 `olarak` yığını. `etkili olarak`, `sonuç olarak`, `bir araç olarak`. Çoğu silinir.

C7 Öznesiz edilgen gereklilik. `yapılması gerekmektedir`. Kipi koruyarak "-mAlI" ya da emir:
"yapılmalıdır", teknik metinde "yapın".

C8 Üçlemeler. Her listede üç öge, her cümlede üç sıfat. Gerçek öge sayısını koru, süs
sıfatı sil.

C9 `X değil, Y` karşıtlığı. Metinde bir kez geçmesi doğaldır. Her paragrafta geçiyorsa bir
kısmını düz bildirime çevir, ama olumsuzluğun taşıdığı bilgiyi silme.

C10 Retorik soru ve hemen ardından yanıt. `Peki neden? Çünkü…`, `Cevap basit:`. Bildirme
cümlesine çevir.

C11 Noktalı virgül ve virgül yoğunluğu. Kocagül (2026): noktalı virgül AI metinlerinin
%76,8'inde, insan metinlerinin %15,2'sinde. Akademikte dokunma, diğer türlerde yeniden
yazarken üretme.

C12 Cümle içi uzun çizgi ve aralıklı kısa çizgi. Virgül, ayraç ya da bitişik kısa çizgi
kullan.

C13 Biçim kalıpları. `**Kalın etiket:**` ile başlayan maddeler, başlıklarda Title Case
(`Ve`, `İle` büyük), her başlıkta emoji, eğik çizgili seçenek yığını, her terime tırnak.
Düz metne istenmediyse markdown koyma. Tek bir kalın vurgu sorun değildir.

C14 Eş anlamlı döndürme. Aynı kavram için her cümlede başka sözcük. Terimi koru, tekrar
doğaldır.

C15 `-sA dA … aslında … göstergesidir` kalıbı. Düz yargıya çevir.

C16 Sahte aralık. `Küçük işletmelerden dev holdinglere kadar` gibi iki uç arası boş kapsam.
Somut kapsam yoksa sil.

C17 Tekdüze deyim. Her paragrafta bir deyim. Metin başına bir iki deyim yeter.

## D. Ton

| Kimlik | Ad | Örnek kalıp |
|---|---|---|
| D1 | Dalkavukluk | `Harika bir soru!`, `Çok haklısınız` |
| D2 | Terapist dili | `Bu duyguların çok normal`, `Kendine nazik ol` |
| D3 | Aşırı çekince | `bir ölçüde`, `belli bir düzeyde`, `olabileceği düşünülebilir` |
| D4 | Bilgi sınırı notu | `Bilgilerim şu tarihe kadar` |
| D5 | Belirsiz otorite | `Uzmanlar diyor ki`, `Araştırmalar gösteriyor ki` (kaynaksız) |
| D6 | Motivasyon kapanışı | `Unutma, başarı bir yolculuktur!` |
| D7 | Aforizma | `Kitaplar bizi biz yapar.` türü genel yargı, girdide yoksa |
| D8 | Sahte samimiyet | `Açık konuşayım`, `Sana bir sır vereyim` |
| D9 | Boş doğrular | `Her şeyin bir dengesi vardır` |
| D10 | Uydurma vaka | `Geçen yıl bir müşterimiz…` (girdide yoksa) |
| D11 | Kayıt kayması | resmî metinde argo, sohbette resmî yazı dili |
| D12 | Broşür dili | `hayalinizdeki`, `bir tık uzağınızda` |

D3 için dikkat: Girdideki gerçek çekince korunur. Yalnız üst üste binmiş çekinceleri
(`muhtemelen … olabileceği düşünülebilir`) tek çekinceye indir.

D5 ve D10 için: Kaynağı ya da vakayı sen ekleme. Silmek ya da yazara sormak gerekir.

## E. Sohbet botu kalıntısı

`Umarım yardımcı olur`, `Başka sorunuz olursa`, `Dilerseniz…`, `Elbette!`, `İşte…`,
`Bir yapay zekâ olarak`, `[Adınız]` gibi doldurulmamış yer tutucular, düz metinde markdown,
`Bu yazıda…`, baştaki ve sondaki özet (özet sandviçi), `**Not:**`,
`Aşağıda … bulabilirsiniz`.

Hepsi silinir. Yer tutucuyu silme, yazara bırak.

> Önce: Elbette! İşte istediğiniz e-posta taslağı. Umarım işinize yarar!

Sonra: (yalnızca taslağın kendisi)

## Kanıt düzeyi

Linter her `ai-iz` kuralına bir etiket koyar:
- `veri`: Türkçe derlem çalışmasıyla ölçülmüş (örneğin noktalı virgül, `-ArAk`).
- `hakem`: stil rehberlerinde ya da uzman değerlendirmesinde geçen.
- `hipotez`: gözleme dayanan, henüz ölçülmemiş. En çok `info` düzeyindedir.

## İz sayılmayanlar

- Kusursuz yazım tek başına AI kanıtı değildir.
- Cümleye "Ama" ya da "Ve" ile başlamak. İnsan yazılarında sık görülür.
- Eksiltili cümle. İnsan metinlerinde AI metinlerinden çok daha sık geçer.
- Akademik `-mAktAdIr`, yöntem bölümünde edilgen, tanımda `-DIr`.
- Resmî kayıtta resmî sözcük.
- Gerçek liste.
