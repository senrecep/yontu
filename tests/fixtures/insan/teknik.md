# Kurulum

Paketi pip ile kurabilirsiniz:

```
pip install ornek-paket
```

Python 3.9 ve sonrası desteklenir. Windows'ta komutu PowerShell yerine normal komut isteminde çalıştırmanızı öneririz; PowerShell bazı ortam değişkenlerini farklı okuyor.

## Yapılandırma

Proje klasöründe `ayarlar.toml` adında bir dosya oluşturun. Dosya yoksa varsayılan değerler kullanılır. En sık değiştirilen iki ayar şunlar:

- `zaman_asimi`: Bir isteğin kaç saniye bekleneceği. Varsayılan değer 30.
- `deneme_sayisi`: İstek başarısız olursa kaç kez tekrarlanacağı. Varsayılan değer 3.

Zaman aşımını çok düşük tutarsanız yavaş sunucularda istekler sürekli yarıda kesilir. Bizim ölçümlerimizde 10 saniyenin altı sorun çıkardı.

## Sık karşılaşılan hatalar

Kurulumdan sonra modül bulunamadı hatası alıyorsanız büyük olasılıkla paketi başka bir sanal ortama kurdunuz. `which python` komutuyla hangi yorumlayıcının çalıştığına bakın. Sertifika hatası alanlar ise şirket ağındaki vekil sunucuyu kontrol etmeli. Bu durumda `--sertifika` seçeneğiyle kendi sertifika dosyanızı gösterebilirsiniz.

Hata kaydını açmak için komutu `--ayrintili` seçeneğiyle çalıştırın. Kayıtlar ekrana ve `kayit.txt` dosyasına yazılır.
