# Kimlik doğrulama

API'ya yapılan her istekte `Authorization` başlığında bir erişim anahtarı gönderilmelidir. Anahtarı yönetim panelindeki Ayarlar sayfasından oluşturabilirsiniz.

```
curl -H "Authorization: Bearer ANAHTAR" https://api.ornek.com/v1/siparisler
```

Anahtarlar 90 gün geçerlidir. Süresi dolan anahtarla yapılan istekler 401 koduyla reddedilir. Süre dolmadan yeni bir anahtar oluşturup eskisini silmenizi öneririz; iki anahtar aynı anda geçerli olabilir.

## Hız sınırı

Her anahtar dakikada en çok 120 istek gönderebilir. Sınır aşıldığında sunucu 429 kodunu döndürür ve `Retry-After` başlığında kaç saniye beklemeniz gerektiğini bildirir. İstemcinizin bu başlığı okuyup beklemesi gerekir. Sürekli sınıra takılıyorsanız istekleri toplu uç noktalarla birleştirmeyi deneyin.
