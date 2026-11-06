# Tür ve kayıt profilleri

Ne zaman oku: Metnin türünü seçerken. Bu dosya yalnız dizindir. Seçtiğin türün tam profilini
`references/turler/<kimlik>.md` dosyasından oku ya da `yontu profiles <kimlik>` çalıştır.
Kimliği tahmin etme. Aşağıdaki tabloda yoksa `yontu profiles` listesine bak.

Her profil dosyası okuru, cümle uzunluğunu, hitabı, kipi, yapıyı, tipik AI hatasını ve
bir önce/sonra örneği verir. İkna amaçlı türlerde (`blog`, `linkedin`, `reklam`,
`e-ticaret`, `x`, `instagram`) dosyanın sonunda "İkna gücünü koru" bölümü vardır.

Önce örnekleri alıntı bloğunda, sonra örnekleri düz metindedir. Hiçbir sonra metni önce
metninde olmayan sayı, ad, tarih ya da iddia içermez. Eksik bilgi köşeli ayraçla gösterilir.

## Türler

| Kimlik | Kod | Kayıt | Tür |
|---|---|---|---|
| `akademik-ozet` | P1 | akademik | Akademik özet (abstract) |
| `akademik-giris` | P2 | akademik | Akademik giriş |
| `akademik-tartisma` | P3 | akademik | Akademik tartışma ve sonuç |
| `tez` | P4 | akademik | Tez (lisansüstü) |
| `dilekce` | P5 | resmi | Dilekçe |
| `resmi-yazi` | P6 | resmi | Resmî yazı (Resmî Yazışma Yönetmeliği) |
| `haber` | P7 | haber | Haber (ajans, ters piramit) |
| `kose` | P8 | deneme | Köşe yazısı ve deneme |
| `blog` | P9 | blog | Blog |
| `teknik-dok` | P10 | teknik | Teknik dokümantasyon |
| `readme` | P11 | teknik | GitHub README |
| `changelog` | P12 | teknik | CHANGELOG |
| `commit` | P13 | commit | Commit mesajı |
| `ui-buton` | P14 | ui | UI mikro metin: buton ve etiket |
| `ui-hata` | P15 | ui | UI mikro metin: hata ve onay iletileri |
| `ui-bos` | P16 | ui | UI mikro metin: boş durum ve bildirim |
| `reklam` | P17 | pazarlama | Reklam metni ve slogan |
| `e-ticaret` | P18 | pazarlama | E-ticaret ürün açıklaması |
| `linkedin` | P19 | blog | LinkedIn gönderisi |
| `x` | P20 | sosyal | X (Twitter) gönderisi |
| `instagram` | P21 | sosyal | Instagram açıklaması |
| `resmi-eposta` | P22 | kurumsal | Resmî e-posta (kurum dışı, ilk temas) |
| `is-eposta` | P23 | is-eposta | İş içi e-posta ve mesaj |
| `basin-bulteni` | P24 | kurumsal | Basın bülteni |
| `sunum` | P25 | sozlu | Sunum ve konuşma metni |
| `edebi` | P26 | edebi | Edebî metin ve öykü |
| `sohbet` | P27 | sohbet | Sohbet asistanı cevabı |
| `hukuk` | P28 | hukuk | Hukuk metni (sözleşme, karar, yönetmelik, aydınlatma metni) |

## İki seviye

Kayıt (`--register`) genel tonu ve eşikleri belirler. Tür (`--tur`) kaydın içindeki profili
seçer. Tür verilmezse kaydın varsayılanı kullanılır. Linterin kabul ettiği kimlikleri
`yontu profiles` verir.

| Kayıt | Türler | Yoğunluk eşiği | Ateşman hedefi | Öz Türkçe önerileri |
|---|---|---|---|---|
| akademik | P1-P4 | ×3 | 30-60 | isteğe bağlı |
| hukuk | sözleşme, karar, aydınlatma metni, yönetmelik | ×3 | 30-60 | kapalı |
| resmi | P5, P6 | ×3 | 30-60 | kapalı |
| kurumsal | P22, P24 | ×2 | 50-80 | isteğe bağlı |
| haber | P7 | ×1 | 50-80 | isteğe bağlı |
| deneme | P8 | ×1,5 | 50-80 | kapalı |
| blog | P9, P19 | ×1 | 50-80 | isteğe bağlı |
| teknik | P10-P12 | ×1 | 50-80 | isteğe bağlı |
| commit | P13 | mutlak sayı | yok | kapalı |
| ui | P14-P16 | mutlak sayı | 70 ve üstü | kapalı |
| pazarlama | P17, P18 | ×1, kısa metin kapısı | 70 ve üstü | isteğe bağlı |
| sosyal | P20, P21 | ×1, kısa metin kapısı | 70 ve üstü | isteğe bağlı |
| is-eposta | P23 | ×1 | 50-80 | isteğe bağlı |
| sozlu | P25 | ×1,5 | 70 ve üstü | isteğe bağlı |
| edebi | P26 | yalnız `tdk` | yok | kapalı |
| sohbet | P27 | ×1 | 70 ve üstü | isteğe bağlı |
| notr | belirsiz | ×1, her şey bilgi notu | 50-80 | isteğe bağlı |

Kısa metin kapısı: 50 sözcüğün altında mutlak sayım, 50-150 sözcükte en az iki eşleşme, 150 ve
üstünde oran. Cümle bantları ortalama hedeftir, tek cümle için ceza değildir. Okunabilirlik
puanı her zaman yalnızca bilgi notudur.

## Kaydı tanıma

Kullanıcı söylediyse onu al. Yoksa dosya adına bak: `COMMIT_EDITMSG` commit, `CHANGELOG`
teknik, `README` teknik, `.po` ve çeviri JSON'u ui, `.tex` akademik. Sonra içeriğe bak:
"Sayı/Konu" ve "arz ederim" resmi, "Özet" ve "Anahtar kelimeler" akademik, "Taraflar" ve
"madde" hukuk, buton listesi ui. Emin değilsen notr. Kullanıcıya sorma.
