# yontu landing page plan

Working notes for the GitHub Pages site in this folder. Turkish is the primary page (`/yontu/`), English sits at `/yontu/en/`. Every claim below comes from the repository; the page carries no testimonials, user counts, stars or benchmarks.

## Page outline

1. Floating nav: brand, Örnek, Nasıl çalışır, Kanıt, SSS, Kurulum, language switch, GitHub.
2. Hero: headline, subheadline, the one install command with a copy button, proof line. A real `yontu lint` run sits beside it on desktop.
3. Problem and solution: why English humanizers miss Turkish, then the before/after README slate with genuine lint and compare output.
4. Benefits: four full width rows separated by incised grooves, each naming a real rule code or command.
5. Tagline reveal: two lines, word by word.
6. How it works: three steps.
7. Proof: a mono ledger of facts from the repo and CI (no big number row), the fidelity gate refusing an added date, `yontu explain` naming its TDK source.
8. FAQ: nine questions, with FAQPage JSON-LD.
9. Risk reversal: one serif line (free, open source, no dependencies, offline) and one supporting paragraph.
10. Final CTA: the hero command again, then the other install routes (Claude Code plugin, skill folder, claude.ai zip, MCP).
11. Footer.

## Hero copy

| | Türkçe | English |
|---|---|---|
| Headline | Ajanınızın Türkçesini yontar. Anlamına dokunmaz. | Carves your agent's Turkish. Leaves the meaning alone. |
| Subheadline | Yapay zekâ ajanlarıyla Türkçe yazanlar için açık kaynak bir linter. Çeviri kalıplarını işaretler, yazımı ve noktalamayı TDK kurallarına göre denetler. | An open source linter for anyone writing Turkish with AI agents. It flags translation patterns and checks spelling and punctuation against the TDK rules. |
| CTA | `pipx install yontu` (copy) | same |
| Proof line | PyPI ve MCP Registry'de · Python 3.9 ile 3.14 arası · bağımlılık yok · MIT | On PyPI and the MCP Registry · Python 3.9 to 3.14 · no dependencies · MIT |

## Benefits

1. TDK yazım ve noktalama: her kural Yazım Kılavuzu'ndaki bölümünü gösterir; otomatik düzeltme yalnız kesin kurallarda çalışır.
2. Türkçeye özgü yapay zekâ izleri: "kullanılmaktadır" zincirleri, çeviri kalıpları, sohbet artıkları. İngilizce sözcük listeleri değil.
3. Türe göre ölçü: 17 register altında 28 tür, her birinin kendi eşikleri.
4. Sadakat kapısı: yeniden yazım yeni sayı, tarih, ad, URL ya da kod ekleyemez.

## How it works

1. Kurun: `pipx install yontu` ya da Claude Code eklentisi.
2. Denetleyin: `yontu lint metin.md --tur readme` bulguları kural kimliği, düzey ve öneriyle verir.
3. Kapıdan geçirin: `yontu compare eski.md yeni.md` eklenen bilgide 1 koduyla çıkar; ajan düzenlemeyi geri alır.

## FAQ (TR, mirrored in EN)

1. yontu bir yapay zekâ dedektörü mü? Hayır. Kalıpları raporlar; bir bulgu metnin makineyle yazıldığını göstermez.
2. Metnim bir sunucuya gidiyor mu? Hayır. Denetleyici ağ bağlantısı kurmaz.
3. Hangi ajanlarla çalışır? Claude Code, Codex, Cursor, Gemini CLI, MCP destekleyen istemciler, zip ile claude.ai.
4. Metni kendisi düzeltir mi? Yalnız tdk katmanındaki kesin kurallarda, `--fix` ile. ai-iz bulguları hiç düzeltilmez.
5. Yanlış pozitif verir mi? Verir. Kurallar sezgiseldir, çoğu bilgi düzeyindedir.
6. Hangi metin türlerini tanır? 17 register altında 28 tür; tür verilmezse içerikten tahmin eder.
7. Ne gerektirir? Python 3.9 ve üstü. Yalnız standart kitaplık.
8. Ücretli mi? Hayır. MIT lisanslı.
9. Sözlüğü var mı? Yok. Bilinen yanlış yazımları yakalar, her yanlış yazımı değil.

## SEO and AEO

- Index both pages. `noindex` on 404, excluded from the sitemap.
- TR title: "yontu · Türkçe humanizer ve TDK denetleyicisi". EN title: "yontu · Turkish humanizer and TDK linter".
- Meta descriptions from the README's first paragraph, under 160 characters.
- `hreflang` tr, en and x-default (Turkish), absolute canonical URLs, OG and Twitter cards with the 1280×640 social preview.
- FAQPage JSON-LD per language, SoftwareApplication JSON-LD with license, OS and price 0.
- One h1 per page; headings carry the search terms (Türkçe humanizer, TDK yazım denetimi, yapay zekâ metin).

## Layout choice

Layout A, classic hero and stacked sections, with the before/after slate as the first section after the hero. The product is easiest to understand by seeing one bloated paragraph get carved, so the proof sits right below the command instead of behind a long argument. The audience is developers, who scan, so long form persuasion would slow them down; skepticism is answered by real output and the limitations in the FAQ.
