# P18 E-ticaret ürün açıklaması · pazarlama

Kimlik: `e-ticaret`. Kayıt: `pazarlama`. Linter: `yontu lint --tur e-ticaret`.

- Okur: karar veren alıcı. Ölçü, malzeme, kullanım ve iade arar.
- Cümle: 8-16 sözcük, kısa giriş ve madde listesi.
- Hitap: "siz", genç markada "sen", tutarlı.
- Kip ve zaman: geniş zaman.
- Bağlaçlar: az.
- Kelime katmanı: somut ad ve ölçü. `şık`, `premium`, `kaliteli` gibi boş sıfat yok.
- Noktalama: Türkçe sayı biçimi: 10.000 mAh, 2,5 kez, %100 pamuk.
- Yapı: ne ve kimin için, özellik maddeleri, bakım, kutu içeriği.
- Tipik AI hatası: özellik uydurmak, İngilizce sayı biçimi.

> Önce: Powerbank 10,000 mAh kapasitesi ile telefonunuzu 2.5 kez şarj edebilir.

Sonra: 10.000 mAh kapasiteli powerbank, telefonunuzu 2,5 kez şarj edebilir.

## İkna gücünü koru

Açıklama alıcıyı karara götürür. Boş sıfatı at, faydayı bırak.

- İlk cümle ne işe yaradığını ve kimin için olduğunu söyler.
- Boş sıfatı girdideki somut özellikle değiştir. Girdide özellik yoksa sıfatı çıkar, özellik uydurma.
- Fiyat, kampanya ve çağrı kalır.
- Kalıp cümle kanca değildir: `bir üründen fazlası, bir yaşam tarzı`, `vazgeçilmez bir parçası`. Yerine
  ürünün ölçülebilir özelliğini yaz.
