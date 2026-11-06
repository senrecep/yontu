# Aşırı düzeltme

Ne zaman oku: Yeniden yazımı bitirdikten sonra, sonucu teslim etmeden önce. Ayrıca metin
"insanlaştırılmış" göründüğü hâlde yapay okunuyorsa ve `yontu compare` aşırı düzeltme bulgusu
verdiğinde. Kötü örnekler alıntı bloğundadır, onları taklit etme.

## Neden önemli

AI izini silmek kolaydır, yerine başka bir iz koymak daha kolaydır. Her cümleyi kısaltan,
her paragrafı soruyla açan, her yere deyim serpiştiren bir yeniden yazım yine bir makine
imzası taşır. Üstelik çoğu zaman anlamı da kaydırır. Hedef "AI gibi okunmayan" metin değil,
yazarın söylediğini daha iyi söyleyen metindir.

## Sinyaller

`yontu compare` ve `yontu lint` yeniden yazımdan sonra şunları sayar:

| Sinyal | Eşik | Düzey |
|---|---|---|
| girdide olmayan rakam, tarih, URL, kod ya da özel ad | bir tane bile | `error` (`compare`) |
| girdide olup çıktıda olmayan öğe, olumsuzluk ya da kip değişimi | bir tane bile | `warning` (`compare`) |
| üç sözcük ve altındaki vurucu cümle | cümlelerin %20'sinden fazlası | `info` |
| soru ve hemen ardından yanıt | 300 sözcükte 2 ve üstü | `info` |
| aforizma kapanışı | girdide yokken bir tane bile | `info` |
| deyim ya da ikileme | 150-250 sözcükte birden fazla | `info` |

Şunları linter saymaz, sen elle bakarsın. Temiz bir lint çıktısı bunların olmadığını
göstermez:

- girdide olmayan kişi, vaka ya da örnek (sayı ya da ad taşımıyorsa `compare` görmez)
- art arda üç paragrafın aynı bağlaçla açılması
- türün dozunu aşan devrik cümle (bkz. `cumle-turleri.md`)
- zorla eklenmiş argo ya da yapay yazım hatası
- art arda üç ve üstü eksiltili cümle

## Yapılmayacaklar

1. Kasıtlı yazım hatası ekleme. Kusursuz yazım AI kanıtı değildir, hata insan kanıtı
   değildir.
2. Girdide olmayan anı, görüş, duygu, örnek ya da kişi ekleme. "Ses katmak" yazarın bilgisini
   ister.
3. Kayıt düşürme. Resmî metne argo, akademik metne sohbet dili koyma.
4. Her `-mAktAdIr`, her edilgen, her "olarak" peşine düşme. Akademik ve hukuk metninde
   bunlar normdur.
5. Eş anlamlı döndürme. Aynı kavram için her cümlede başka sözcük kullanmak da bir izdir.
6. Terimi "sadeleştirme". Alan terimi, tanımlı terim ve hukuki kavram kalır.
7. Kesinlik derecesini değiştirme. "işaret etmektedir" ile "kanıtlamaktadır" aynı iddia
   değildir. "-ebilir" kesin bilgiye dönmez, kesin bilgi "-ebilir"e de dönmez.
8. Olumsuzluğu düşürme. `X değil, Y` kalıbını sadeleştirirken olumsuz bilgiyi koru.
9. Alıntıya dokunma. Tırnak içi söz, blok alıntı, kod, URL ve dosya yolu olduğu gibi kalır.
10. Kısa metni şişirme. Tek satırlık bir buton ya da commit başlığı öyle kalır.
11. İkna gücünü silme. Reklamda, köşe yazısında ya da LinkedIn gönderisinde vurgu ve çağrı
    kalır. Yalnız kanıtsız iddiayı çıkar. Metni düz bir bilgi notuna çevirmek de aşırı
    düzeltmedir.

## İşaretlenmeyecekler

Bunlar kural ihlali ya da AI izi değildir. Linter bunlar için bulgu vermez, sen de verme:

- Cümleye "Ama", "Ve", "Çünkü" ile başlamak.
- Tek bir "aslında", tek bir "Öte yandan", tek bir kalın vurgu.
- Kıvrık tırnak (“ ”).
- Kurala uygun noktalı virgül, akademik ve hukuk metninde.
- Satır başındaki konuşma çizgisi.
- Akademik `-mAktAdIr`, yöntem bölümündeki edilgen, tanımdaki `-DIr`.
- Haberde "meydana geldi", "açıklama yaptı".
- Hukukta "işbu", "mezkûr", "söz konusu", "-mAsI hâlinde", "temel esaslar", "önem arz eder".
- Sözlükte geçerli olan biçimler: illaki, tekrardan, arttırmak.
- Gerçek liste, gerçek tablo, gerçek başlık.
- Yazarın bilinçli seçtiği eski ya da yöresel sözcük.
- "açık ve net", "güç ve zor" gibi tek geçişli çiftler.

## Kontrol sırası

Yeniden yazımı teslim etmeden önce:

1. `yontu compare eski.txt yeni.txt` çalıştır. `error` varsa ilgili değişikliği geri al.
   `warning` (girdide olup çıktıda olmayan öğe) varsa öğenin bilgi taşıyıp taşımadığına bak.
   Bilgi taşıyorsa geri koy.
2. `yontu lint yeni.txt --format json --tur <tür>` çalıştır. Çıktıda yeni `—`, blog ya da e-postada yeni
   `;`, "Sonuç olarak", sohbet kalıntısı varsa düzelt.
3. Linter yoksa elle bak:
   - Sonra metnindeki her rakam, tarih ve özel ad önce metninde var mı?
   - Olumsuzluk sayısı aynı mı?
   - Kip ve kesinlik derecesi aynı mı?
   - Önce metnindeki her iddia sonra metninde bir yerde duruyor mu?
4. Sesli oku. Her cümle aynı kısalıkta mı? Her paragraf aynı biçimde mi bitiyor? Öyleyse
   bir kısmını eski hâline yaklaştır.

## Kötü örnekler

Aşağıdaki "sonra" metinleri yapılmaması gerekeni gösterir.

> Önce: Bu yöntem, verimliliğin artırılmasına yardımcı olabilir.
>
> Kötü sonra: Bu yöntem verimliliği artırır.

Kesinlik yükseldi: "yardımcı olabilir" kısmi ve olası katkıdır, "artırır" kesin nedendir.
Doğrusu: "Bu yöntem verimliliği artırmaya yardımcı olabilir."

> Önce: Toplantı ertelendi. Yeni tarih daha sonra duyurulacak.
>
> Kötü sonra: Toplantı ertelendi. Neden mi? Takvim. Yeni tarih yakında.

Soru ve yanıt eklendi, girdide olmayan bir neden uyduruldu, "daha sonra" ile "yakında" aynı
şey değil. Önce metni zaten temizdir, dokunulmaz.

> Önce: Bulgular, iki değişken arasında anlamlı bir ilişkiye işaret etmektedir.
>
> Kötü sonra: Bulgular, iki değişkenin birbirini doğrudan etkilediğini kanıtlıyor.

Basamak atlandı (işaret etmek → kanıtlamak), ilişki nedenselliğe döndü, akademik kayıt
düştü.

> Önce: Ödeme sırasında bir hata oluştu. Lütfen tekrar deneyin.
>
> Kötü sonra: Eyvah, ödeme patladı! Bir daha dene bakalım.

Kayıt düştü, hitap "siz"den "sen"e geçti, ünlem ve argo eklendi.

> Önce: Kurulum tamamlandı.
>
> Kötü sonra: Kurulum bitti. Sorunsuz. Hızlı. Hazırsınız.

Eksiltili cümle yığını ve girdide olmayan iki nitelik ("sorunsuz", "hızlı").
