<p align="center">
  <a href="https://senrecep.github.io/yontu/"><img src="https://raw.githubusercontent.com/senrecep/yontu/main/site/public/mark.svg" alt="yontu" width="120" height="120"></a>
</p>

# yontu

Türkçe humanizer, TDK denetleyicisi ve tür üslubu rehberi. Türkçe metni yontar: biçim verir, inceltir.

yontu, Türkçe metindeki yapay zekâ ve çeviri kalıplarını işaretler ve sadeleştirir. Yazımı ve noktalamayı Türk Dil Kurumunun kurallarına göre denetler. Sözcük seçimini ve cümle yapısını metnin türüne uydurur. Ajan skill'i, çevrim dışı komut satırı aracı ve MCP sunucusu olarak gelir. Claude Code, Codex, Cursor, Gemini CLI ve MCP destekleyen her istemciyle çalışır. İngilizce humanizer araçları Türkçede pek işe yaramaz, bu yüzden buradaki her kural Türkçe için yazıldı.

[English README](README.md) · [Web sitesi](https://senrecep.github.io/yontu/)

## Neden

Humanizer araçlarının çoğu İngilizce için yazıldı. Kuralları Vikipedi'deki "Signs of AI writing" gibi listelerden gelir ve "delve", "tapestry" gibi İngilizce sözcüklere dayanır. Bu kurallar Türkçe metinde neredeyse hiçbir şey bulmaz. Uzun çizgi gibi birkaç kalıp Türkçede de görülür. Onu yakalamak için de Türkçe bir kural gerekir: TDK uzun çizgiyi yalnız konuşma çizgisi olarak kullanır. Türkçe yapay zekâ metninin asıl sorunları başka yerdedir:

- her cümlenin `-mAktAdIr` ile bitmesi, uzun `-ArAk` zincirleri
- `önemli bir rol oynamaktadır`, `bu bağlamda` gibi çeviri kalıpları
- hâl ekinin yerine geçen sarmalayıcılar: "konusunda", "hususunda", "bir şekilde"
- sohbet artıkları: `Umarım bu e-posta sizi iyi bulur`, `Umarım yardımcı olur`
- dikkatli bir yazarın yapmayacağı yazım ve noktalama yanlışları: `herşey`, "ve" önünde virgül, `Türkçe'de`

Türkçede doğru dil bağlama göre de değişir. Makale özeti, reklam, blog yazısı, README, commit mesajı ve dilekçe ayrı cümle uzunluğu, resmiyet, hitap ve bağlaç ister. Birinde doğru olan öbüründe kusur olur: `-mAktAdIr` akademik özette olağandır, blog yazısında göze batar. Sözcük seçimi de aynı ölçüde önemlidir. `Hızlı bir şekilde` çoğu zaman yalnızca "hızla" demektir.

yontu bunları kaynaklı kurallara, tür profillerine ve bir sözcük listesine döker. Ajana da anlamı koruyan bir çalışma düzeni verir.

## Bileşenler

| Parça | Ne işe yarar |
|---|---|
| Skill | `skills/yontu/`: `SKILL.md`, dokuz başvuru dosyası ve `references/turler/` altında her tür için bir rehber. Python olmadan da çalışır |
| Denetleyici | Python 3.9 ve üstü, yalnız standart kitaplık, ağ bağlantısı yok. Katmanlar: `tdk`, `ai-iz`, `stil`, `yogunluk` |
| Profiller | 17 register altında 28 tür. Her biri cümle uzunluğu, yoğunluk, resmiyet, hitap, kip ve zaman, bağlaç, söz varlığı, noktalama ve yapı tanımlar |
| Sadakat kapısı | `yontu compare ESKI YENI` yeni sayı, tarih, ad, URL ya da kod eklenirse hata verir. Bir öğe düşerse, olumsuzluk ya da kip değişirse uyarır |
| MCP sunucusu | `yontu mcp`, stdio, SDK'siz JSON-RPC |
| Kancalar | Ajana göre düzenleme sonrası ya da tur sonu kancası: Claude Code, Codex, Cursor, Gemini CLI, Copilot, Antigravity. Ayrıntılar `integrations/` klasöründe |

## Önce ve sonra

`skills/yontu/references/ornekler.md` dosyasından, README türü:

> yontu: Türkçe Metinler İçin Modern Ve Güçlü Bir Linter
>
> yontu, Türkçe metinlerinizi analiz ederek yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini tespit eden, modern, güçlü ve kullanıcı dostu bir araçtır. Projenin temel amacı, yazım kalitenizi bir üst seviyeye taşımaktır!
>
> Kullanım: Analiz işlemini gerçekleştirmek için aşağıdaki komutu kolayca çalıştırabilirsiniz: `yontu lint metin.md`

```text
yontu: Türkçe metinler için linter

yontu, Türkçe metindeki yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini bulan
bir linterdir.

Kullanım: `yontu lint metin.md`
```

Korunan: aracın adı, bulduğu üç sorun, komut. Atılan: sıfat üçlüsü, ünlem, "kolayca". Başlık cümle düzenine geçti. Metne yeni bilgi eklenmedi.

## Kurulum

Claude Code için skill, MCP sunucusu ve kancalar birlikte gelir:

```
/plugin marketplace add senrecep/yontu
/plugin install yontu@yontu
```

Kancaları kuran tek yol budur. Komutlar: `/yontu:turkcelestir`, `/yontu:yontu-lint`.

Skill klasörü okuyan başka ajanlar için:

```
npx skills add senrecep/yontu
```

Bu komut yalnız skill'i kopyalar. MCP sunucusu ve kancalar gelmez.

Komut satırı aracı:

```
pipx install yontu          # yontu ve trlint komutlarını PATH'e koyar
uvx yontu lint metin.md     # kurulumsuz
```

Depo kopyasından kurulum yapmadan: `python3 skills/yontu/scripts/yontu lint metin.md`.

MCP sunucusu:

```bash
claude mcp add yontu -- uvx yontu mcp
```

Diğer istemciler için `{"command": "uvx", "args": ["yontu", "mcp"]}`. Ajan başına ayar dosyaları, yollar ve hangi sürümde neyin denendiği [integrations/](integrations/README.md) klasöründe.

claude.ai web sitesinde skill, zip olarak yüklenir ve kod çalıştırma açık olmalıdır. Uzak MCP bağlayıcısı v0.2 için planlandı. Mobil uygulamalarda denenmedi. Adımlar: [integrations/claude-ai](integrations/claude-ai/README.md).

Sunucu varsayılan olarak üç araç listeler: `lint_text`, `compare_texts`, `get_style_guide`. Sekiz aracın hepsi için sunucunun ortamına `YONTU_MCP_TOOLS=full` eklenir. Diğer beş araç listelenmese de çağrılırsa yanıt verir, ama çoğu istemci modele yalnız listelenen araçları gösterir.

### Ajan başına

| Ajan | Skill | MCP | Kancalar |
|---|---|---|---|
| Claude Code | eklenti | eklenti | eklenti |
| Codex CLI | `~/.agents/skills` | `codex mcp add yontu -- yontu mcp` | `hooks.json` |
| Gemini CLI | uzantı | uzantı | ayar dosyası |
| Cursor | `~/.cursor/skills` | `mcp.json` | `hooks.json` |
| claude.ai (web, mobil) | zip yükleme, bkz. [klasör](integrations/claude-ai/README.md) | v0.2 için planlandı | yok |
| OpenCode, Hermes, Windsurf, Copilot, Cline, Zed, Claude Desktop, Antigravity | klasöre bakın | klasöre bakın | kısmen |

Ayar dosyaları, kesin yollar ve hangi sürümde neyin denendiği: [integrations/](integrations/README.md).

### Kurulum profilleri

| Profil | Ne yüklenir | Claude Code | Diğer ajanlar |
|---|---|---|---|
| `lite` | yalnız skill, denetleyiciyi kabuktan çalıştırır | `/plugin install yontu-lite@yontu` | `scripts/install.sh --<ajan> --profile lite --apply` |
| `standard` | `lite` ve kancalar | `full` kullanılır | `--profile standard` kanca ayarını da yazdırır |
| `full` | `standard` ve MCP sunucusu | `/plugin install yontu@yontu` | `--profile full` kanca ve MCP ayarlarını yazdırır |

`install.sh`, `--apply` verilmezse yalnız ne yapacağını gösterir. Diske yalnız skill klasörünü yazar, ayarları elle eklemeniz gerekir. Claude Code için iki eklentiden yalnız birini kurun.

Bağlam maliyeti: tam eklenti MCP araçları hariç sürekli yaklaşık 150, lite yaklaşık 130 token tutar. Bir blog yazısını baştan sona yeniden yazmak toplam yaklaşık 3.900 token harcar. Sayılar, yöntem ve neyin ne zaman yüklendiği: [docs/CONTEXT.md](docs/CONTEXT.md).

## Tools

| MCP aracı | Ne yapar |
|---|---|
| `lint_text` | Katman, kural kimliği, düzey, konum ve öneriyle bulguları verir (`detail: true` bütün alanları döndürür) |
| `compare_texts` | İki sürüm arasındaki sadakat kapısı |
| `get_style_guide` | Tür kimliğine göre bir türün rehberini ya da bir başvuru dosyasını verir: önce bölüm listesi, sonra tek bölüm |
| `fix_text` | Yalnız güvenli `tdk` düzeltmelerini uygular |
| `text_stats` | Cümle uzunluğu, okunabilirlik, yoğunluk |
| `explain_rule` | Bir kural kimliğinin iletisi, kaynağı ve örnekleri |
| `list_profiles` | Bütün register'lar ve türler |
| `get_profile` | Bir tür ya da register'ın eşikleri |

Sunucu varsayılan olarak ilk üç aracı listeler. Sekizinin de listelenmesi için sunucunun ortamına `YONTU_MCP_TOOLS=full` eklenir. Diğer beş araç her durumda yanıt verir, ama çoğu istemci modele yalnız listelenen araçları gösterir.

MCP istemleri: `turkcelestir` (metni Türkçeye çevirir ya da uyarlar), `yogunlastir` (metni sıkılaştırır).

## Kullanım

`yontu` ve `trlint` aynı komuttur.

```
yontu lint DOSYA [--register SLUG] [--tur KIMLIK] [--layer tdk,ai-iz] [--min-level warning] [--format json]
yontu lint DOSYA --fix [--write]    # yalnız güvenli tdk düzeltmeleri
yontu compare ESKI YENI             # sadakat kapısı
yontu stats DOSYA                   # cümle uzunluğu, Ateşman okunabilirliği, yoğunluk
yontu rules [--layer tdk]           # kural listesi
yontu explain AI-E6                 # bir kuralın kaynağı ve örnekleri
yontu profiles [KIMLIK]             # türler ve register'lar
```

`--min-level` verilen düzeyin altındaki bulguları gizler (`info`, `warning`, `error`). `DOSYA` yerine `-` yazılırsa metin standart girdiden okunur. `lint` ve `compare` hata bulursa 1, kullanım yanlışında 2 ile çıkar.

`--register` ve `--tur` verilmezse yontu register'ı içerikten tahmin eder. Emin olamazsa `notr` kullanır. Bu durumda bütün üslup kuralları `info` düzeyinde kalır.

Proje ayarları `.yontu.json` dosyasına yazılır (`register`, `tur`, `enable`, `rules`). Tek satırda bir kuralı kapatmak için `<!-- yontu-disable-next-line KS-01 -->`, bir bölüm için `<!-- yontu-disable KS-01 -->` ve `<!-- yontu-enable KS-01 -->` kullanılır.

## Türler

| Register | Türler (`--tur`) |
|---|---|
| `akademik` | `akademik-ozet`, `akademik-giris`, `akademik-tartisma`, `tez` |
| `resmi` | `dilekce`, `resmi-yazi` |
| `hukuk` | `hukuk` (sözleşme, karar, yönetmelik, aydınlatma metni) |
| `haber` | `haber` |
| `deneme` | `kose` |
| `blog` | `blog`, `linkedin` |
| `teknik` | `teknik-dok`, `readme`, `changelog` |
| `commit` | `commit` |
| `ui` | `ui-buton`, `ui-hata`, `ui-bos` |
| `pazarlama` | `reklam`, `e-ticaret` |
| `sosyal` | `x`, `instagram` |
| `kurumsal` | `resmi-eposta`, `basin-bulteni` |
| `is-eposta` | `is-eposta` |
| `sozlu` | `sunum` |
| `edebi` | `edebi` |
| `sohbet` | `sohbet` |
| `notr` | tür yok, üslup kuralları `info` |

`hukuk` ve `edebi` metinlerde yalnız `tdk` katmanı ve sadakat kapısı çalışır. Skill bu metinleri istenmedikçe yeniden yazmaz.

## Kural katmanları

| Katman | Neye bakar | Düzey |
|---|---|---|
| `tdk` | TDK Yazım Kılavuzu ve Güncel Türkçe Sözlük'e göre yazım ve noktalama | `error`, `warning`, `info`. Otomatik düzeltme yalnız bu katmanda |
| `ai-iz` | Yapay zekâ ve çeviri kalıpları | `warning` ya da `info`, düzeltilmez |
| `stil` | Tür profiline uygunluk | çoğunlukla `info` |
| `yogunluk` | Gereksiz uzunluk, destek fiiller, sarmalayıcılar | her zaman `info` |

Her `tdk` kuralı dayandığı Yazım Kılavuzu bölümünü ya da Güncel Türkçe Sözlük maddesini gösterir. Bağlantılar `skills/yontu/references/kaynaklar.md` dosyasındadır. Otomatik düzeltme yalnız yanlış alarm vermeyen kesin kurallarda çalışır: `herşey` yerine "her şey", `Türkçe'de` yerine "Türkçede". Sözlükteki yönlendirmeler hiçbir zaman otomatik düzeltilmez.

Her `ai-iz` kuralının bir kanıt etiketi vardır: `veri` (derlemde ölçüldü), `hakem` (inceleyenler onayladı), `hipotez` (gözlendi, ölçülmedi). `hipotez` kuralları `info` düzeyini, `hakem` kuralları `warning` düzeyini geçmez. 0.1 sürümünde henüz `veri` etiketli kural yok. Ayrıntı için [ROADMAP.md](ROADMAP.md).

## Sınırlar

- yontu bir yapay zekâ dedektörü değildir. Kalıp bildirir. Bir bulgu metnin makineyle yazıldığını göstermez, temiz rapor da tersini kanıtlamaz. Dedektör atlatmak bu projenin amacı değildir.
- `ai-iz`, `stil` ve `yogunluk` kuralları yüzey biçimine bakan düzenli ifadeler ve sayımlardır. Biçimbilim çözümlemesi yoktur. Yanlış alarm olur, çoğu `info` düzeyindedir.
- Cümle bantları ve yoğunluk eşikleri alan yazınından ve incelemeden gelir, insan metinleriyle kalibre edilmedi. Kalibrasyona kadar `info` ya da `warning` düzeyinde kalırlar.
- Sözlük paketi yok. Denetleyici bilinen yanlışları yakalar, her yazım yanlışını değil.

## Katkı

[CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın. Yeni kural için kaynak, kanıt etiketi ve örnek dosya gerekir. En değerli katkı, herhangi bir türde özenle yazılmış insan metnidir. Kalibrasyon bu metinlerle yapılacak.

## Teşekkür

- Türk Dil Kurumu: Yazım Kuralları ve Güncel Türkçe Sözlük.
- Oguzhan Durmaz'ın [turkish-humanify](https://github.com/durmazoguzhan/turkish-humanify) ve bushrabeg'in [turkce-humanizer](https://github.com/bushrabeg/turkce-humanizer) projeleri (ikisi de MIT). Bu projelerden alınan fikirler yeniden yazıldı ve TDK kurallarıyla denetlendi.
- Vikipedi'deki "Signs of AI writing" sayfası, kalıp kataloğunun iskeleti için.
- Bütün kaynaklar: `skills/yontu/references/kaynaklar.md`.

## Lisans

MIT. [LICENSE](LICENSE) dosyasına bakın.
