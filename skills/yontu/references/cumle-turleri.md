# Cümle yapısı ve ritim

Ne zaman oku: Cümleler aynı uzunlukta ve aynı kalıpta ilerlediğinde, `-ArAk` zinciri ya da
adlaştırma yoğunlaştığında, devrik veya eksiltili cümleyi kullanıp kullanmamaya karar
verirken. Önce örnekleri alıntı bloğunda, sonra örnekleri düz metinde verilir.

## Öge dizilişi ve odak

- Türkçede yüklem sondadır. Vurgulanan öge yüklemin hemen önüne gelir.
  - "Raporu Ayşe yazdı." Kim yazdı? Ayşe.
  - "Ayşe raporu dün yazdı." Ne zaman? Dün.
- Vurguyu sıfatla değil, sırayla ver. "çok önemli bir nokta" demek yerine önemli ögeyi
  yüklemin önüne al.
- Çeviri kokusu çoğu zaman sıradan gelir: özne başta, ardından uzun bir tümleç zinciri,
  sonda "yapılmaktadır".

## Devrik cümle

- Devrik cümlede yüklemden sonra yalnız bilinen bilgi gelir: "Gördüm onu." "Geldi mi
  mektup?"
- Uygun doz türe göre değişir: deneme, blog ve mektupta cümlelerin yaklaşık %10-25'i,
  teknik metinde %0-5. Akademik, resmî ve hukuk metninde kullanma.
- Her cümleyi devirmek aşırı düzeltmedir.

## Eksiltili cümle

- Yüklemi düşmüş cümle meşrudur. İnsan metinlerinde AI metinlerine göre çok daha sık görülür.
- Uygun yerleri: betimleme, yargı, paragraf sonu. "Yöntemin sınırları var."
- Üç nokta paragraf başına en çok bir kez.
- Art arda eksiltili cümleler (`Hata yok. Uyarı yok. Sorun yok.`) kesik kesik okunur. Bu bir
  aşırı düzeltme işaretidir.

## Soru cümlesi

- İnsan yazar retorik soruyu çoğu zaman yanıtsız bırakır.
- AI kalıbı soruyu sorup hemen yanıtlar: `Peki bu ne anlama geliyor? Cevap basit:`. Bunu
  düz bildirme cümlesine çevir.
- Denemede 300 sözcükte 0-2 retorik soru yeter. Teknik, akademik ve resmî metinde kullanma.

## Uzunluk ve ritim

- Art arda üç cümle aynı uzunluk bandında olmasın. Bu bir öneridir, kural değil.
- Türe uygun bantlar `turler/<kimlik>.md` içindedir. Bant ortalama hedeftir, tek cümle için ceza
  değildir.
- Uzun bir cümleyi bölerken öznesi değişen yerden böl. Kısa cümleleri birleştirirken ortak
  özneyi kullan.
- Kısa cümle vurgu içindir. Her paragrafı kısa bir vurucu cümleyle bitirmek kalıptır.

## Zarf-fiil paleti

`-ArAk` AI metinlerinde çok sık geçer. Bir cümlede en çok bir kez kullan. Seçenekler:

| Ek | İşlev | Örnek |
|---|---|---|
| -ip | ardışık eylem, aynı özne | Dosyayı açıp okudu. |
| -ınca | zaman, koşul | Kapı açılınca içeri girdi. |
| -dıkça | süreklilik, oran | Okudukça anladı. |
| -ken | eş zaman, özne değişebilir | Ben yazarken o okudu. |
| -madan | önce, olumsuz | Kaydetmeden kapattı. |
| -e -e | süreklilik, tekrar | Koşa koşa geldi. |
| -r -maz | hemen ardından | Gelir gelmez aradı. |
| -dığında | zaman, özne değişebilir | Sunucu çöktüğünde ekip uyardı. |

Dikkat:
- "-ip" ve "-ArAk" aynı özne ister. Özne değişiyorsa "-ınca", "-ken" ya da "-dığında" kullan.
- "-ip" olumsuzluğu belirsiz paylaşır. "Gelip görmedi" iki türlü okunabilir. Anlam
  önemliyse iki fiili ayrı çekimle.
- mı'lı yapı konuşma diline yakın bir koşul kurar: "Veri bir kez düzgün okundu mu gerisi
  kolay." Sohbet ve blogda kullanılabilir, akademik metinde değil.

## Adlaştırma ve boş "olan"

- `-mAsI` zinciri çeviri kokusudur. Fiili geri getir.
- Boş "olan" kalıpları: `sahip olan`, `yer alan`, `bulunan`, `mevcut olan`. Çoğu zaman sıfat
  ya da "-lI", "-dAki" yeter.
- Terimleşmiş yapılara dokunma: "gelişmekte olan ülkeler", "Önemli olan, …".

> Önce: Eğitim, kişisel gelişim açısından çok önemli olan bir süreçtir.

Sonra: Eğitim, kişisel gelişim için çok önemli bir süreç.

> Önce: Yöntemin sahip olduğu bazı sınırlılıklar bulunmaktadır.

Sonra: Yöntemin sınırları var.

> Önce: Bu durum önemlidir. Bunun sebebi, verilerin X'i göstermesidir.

Sonra: Bu durum önemli, çünkü veriler X'i gösteriyor.

## Dönüşüm kuralları

1. Dönüşüm önermeyi korur. Biçim değişir, iddia değişmez.
2. Yüklem kipini koru: gereklilik gereklilik, olasılık olasılık kalır.
3. Öznesiz edilgeni etkene çevirirken özne uydurma. Özne metinde yoksa edilgen kalsın.
4. Akademik ve hukuk metninde `-mAktAdIr` ve edilgen doğaldır.
5. "Ses katmak" yazarın bilgisini ister. Girdide olmayan anı, görüş ya da duygu ekleme.
6. Cümle sayısını keyfe göre değiştirme. Bölmek ve birleştirmek okunurluk içindir.
