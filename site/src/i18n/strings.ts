export type Lang = 'tr' | 'en';

const tr = {
  htmlLang: 'tr',
  ogLocale: 'tr_TR',
  title: 'yontu · Türkçe humanizer ve TDK denetleyicisi',
  description:
    'Yapay zekâ ajanları için Türkçe humanizer ve TDK yazım denetleyicisi. Skill, MCP sunucusu ve CLI olarak gelir. Bağımlılığı yok, çevrim dışı çalışır.',
  skip: 'İçeriğe geç',
  nav: {
    label: 'Sayfa içi',
    demo: 'Örnek',
    how: 'Nasıl çalışır',
    proof: 'Kanıt',
    faq: 'SSS',
    install: 'Kurulum',
  },
  menuOpen: 'Menüyü aç',
  menuClose: 'Menüyü kapat',
  switchLabel: 'English',
  switchHint: 'Read this page in English',
  home: 'yontu ana sayfa',

  heroTitle: ['Ajanınızın Türkçesini yontar.', 'Anlamına dokunmaz.'],
  heroSub:
    'Yapay zekâ ajanlarıyla Türkçe yazanlar için açık kaynak bir linter. Çeviri kalıplarını işaretler, yazımı ve noktalamayı TDK kurallarına göre denetler.',
  ctaLabel: 'Kurulum, tek komut',
  proof: ['PyPI ve MCP Registry’de', 'Python 3.9 ile 3.14 arası', 'bağımlılık yok', 'MIT lisansı'],
  heroDemoLabel: 'Gerçek bir çalıştırma',
  copy: 'Kopyala',
  copied: 'Kopyalandı',

  problemTitle: 'İngilizce için yazılmış kurallar Türkçede iz bulmaz',
  problemBody:
    'Humanizer araçlarının çoğu “delve”, “tapestry” gibi İngilizce sözcük listelerine dayanır. Türkçe yapay zekâ metni başka yerden belli olur: her cümlenin “kullanılmaktadır” diye bitmesinden, çeviri kalıplarından, “Umarım yardımcı olur” gibi sohbet artıklarından.',
  demoTitle: 'Aynı README, yontulmadan önce ve sonra',
  beforeLabel: 'Önce: README.md',
  afterLabel: 'Sonra: README.md',
  legendDrop: 'yeniden yazımda atılan',
  legendRule: 'denetleyicinin bulduğu kural',
  demoKept:
    'Korunan: aracın adı, bulduğu üç sorun, komut. Atılan: sıfat üçlüsü, ünlem, “kolayca”. Başlık cümle düzenine geçti. Metne yeni bilgi eklenmedi.',
  demoSource: 'Örnek, depodaki skills/yontu/references/ornekler.md dosyasından. Çıktılar yontu 0.1.0 ile alındı.',

  benefitsTitle: 'Neye bakar',
  benefits: [
    {
      icon: 'seal',
      tag: 'BK-01 · KS-02',
      title: 'TDK yazım ve noktalama',
      body: 'Her kural Yazım Kılavuzu’ndaki bölümünü ya da Güncel Türkçe Sözlük’teki maddesini gösterir. Otomatik düzeltme yalnız kesin kurallarda çalışır.',
    },
    {
      icon: 'fingerprint',
      tag: 'AI-E1 · AI-C18',
      title: 'Türkçeye özgü yapay zekâ izleri',
      body: 'Ek zincirleri, çeviri kalıpları, hâl ekinin yerine geçen “konusunda” ve “bir şekilde” gibi sarmalayıcılar, sohbet kapanışları.',
    },
    {
      icon: 'stack',
      tag: '--tur readme',
      title: 'Türe göre ölçü',
      body: 'Akademik özette olağan olan blog yazısında göze batar. yontu 17 register altında 28 tür tanır, her birinin kendi eşikleri var.',
    },
    {
      icon: 'shield',
      tag: 'yontu compare',
      title: 'Bilgi ekleyemeyen yeniden yazım',
      body: 'Yeni bir sayı, tarih, ad, URL ya da kod parçası eklenirse karşılaştırma hata verir. Ajan o düzenlemeyi geri alır.',
    },
  ],

  tagline: ['Fazlasını atar, özünü korur,', 'metne yeni bilgi eklemez.'],

  howTitle: 'Nasıl çalışır',
  how: [
    {
      title: 'Kurun',
      body: 'CLI ve MCP sunucusu PyPI’dan gelir. Claude Code eklentisi bunlara kancaları da ekler.',
      code: 'pipx install yontu',
    },
    {
      title: 'Denetleyin',
      body: 'Her bulgu satır, sütun, kural kimliği, düzey ve öneriyle gelir. Metnin türünü verirseniz eşikler ona göre ayarlanır.',
      code: 'yontu lint metin.md --tur readme',
    },
    {
      title: 'Kapıdan geçirin',
      body: 'Yeniden yazılmış sürüm eskisiyle karşılaştırılır. Yeni bilgi varsa komut 1 koduyla çıkar.',
      code: 'yontu compare eski.md yeni.md',
    },
  ],

  proofTitle: 'Söylediklerinin kanıtı depoda',
  proofIntro: 'Hepsi depoda. Testleri kendiniz çalıştırabilir, aşağıdaki her çıktıyı kendi makinenizde yeniden üretebilirsiniz.',
  facts: [
    ['bağımlılık', '0, yalnız Python standart kitaplığı'],
    ['MCP', 'elle yazılmış JSON-RPC, SDK yok'],
    ['test', '251 birim testi, her değişiklikte CI’da'],
    ['Python', '3.9, 3.10, 3.11, 3.12, 3.13, 3.14 ve macOS'],
    ['sürüm', '0.1.0, PyPI ve MCP Registry’de'],
    ['yayın', 'GitHub Releases, SHA256 özetleriyle'],
  ] as [string, string][],
  gateTitle: 'Kapı, eklenen tarihi yakalar',
  gateBody:
    'Ajan toplantı notunu düzeltirken tarihi değiştirip saat eklemiş. Karşılaştırma iki hata verir ve 1 koduyla çıkar.',
  gateOld: 'eski.md',
  gateNew: 'yeni.md',
  gateExit: 'çıkış kodu 1',
  explainTitle: 'Her kural kaynağını söyler',
  explainBody: 'yontu explain bir kuralın katmanını, düzeyini, kaynağını ve neyi yakalayıp neyi yakalamadığını gösterir.',
  tdkTitle: 'Güvenli düzeltme yalnız kesin kurallarda',
  tdkBody: '“Herşey” ve “Türkçe’de” düzeltilir. “Umarım yardımcı olur” işaretlenir ama silinmez. O kararı yazar verir.',

  faqTitle: 'Sık sorulanlar',
  faq: [
    ['yontu bir yapay zekâ dedektörü mü?', 'Hayır. yontu kalıpları raporlar. Bir bulgu metnin makineyle yazıldığını göstermez, temiz bir rapor da yazılmadığını göstermez. Bir dedektörü geçmek amaç değildir.'],
    ['Metnim bir sunucuya gidiyor mu?', 'Hayır. Denetleyici ağ bağlantısı kurmaz, bütün kurallar sizin makinenizde çalışır. MCP sunucusu da yerel bir süreçtir.'],
    ['Hangi ajanlarla çalışır?', 'Claude Code, Codex CLI, Cursor, Gemini CLI ve MCP destekleyen her istemciyle. claude.ai için skill zip olarak yüklenir. Öbür araçların ayar dosyaları depodaki integrations klasöründe.'],
    ['Metni kendisi düzeltir mi?', 'Yalnız tdk katmanındaki kesin kurallarda ve yalnız siz --fix verdiğinizde. Yapay zekâ izleri hiç otomatik düzeltilmez. Yeniden yazımı ajan yapar, yontu denetler.'],
    ['Yanlış pozitif verir mi?', 'Verir. ai-iz, stil ve yogunluk kuralları yüzey biçimleri üzerinde düzenli ifade ve sayımdır, biçim bilgisi çözümlemesi yapmaz. Bu yüzden çoğu bilgi düzeyinde kalır.'],
    ['Hangi metin türlerini tanır?', 'Akademik özetten commit mesajına, dilekçeden reklam metnine 17 register altında 28 tür. Tür verilmezse register içerikten tahmin edilir.'],
    ['Ne gerektirir?', 'Python 3.9 ya da üstü. Başka hiçbir paket kurulmaz.'],
    ['Ücretli mi?', 'Hayır. yontu MIT lisanslı açık kaynak bir projedir.'],
    ['Sözlüğü var mı?', 'Yok. Bilinen yanlış yazımları yakalar, her yanlış yazımı değil. Eşikler de henüz insan yazısından oluşan bir derlemle ayarlanmadı.'],
  ] as [string, string][],

  riskTitle: 'Denemek size bir şeye mal olmaz',
  riskBody:
    'Lisans ücreti, hesap ya da API anahtarı yok. Kod MIT lisanslı, her kuralın kaynağı depoda. Yalnız Python standart kitaplığını kullanır ve metniniz makinenizden çıkmaz.',
  risk: [
    ['Ücretsiz', 'Lisans ücreti, hesap ya da anahtar yok.'],
    ['Açık kaynak', 'MIT lisansı. Her kuralın kodu ve kaynağı depoda.'],
    ['Bağımlılıksız', 'Yalnız Python standart kitaplığı.'],
    ['Çevrim dışı', 'Metniniz makinenizden çıkmaz.'],
  ] as [string, string][],

  routesTitle: 'Öbür kurulum yolları',
  routes: [
    {
      name: 'Claude Code eklentisi',
      note: 'Skill, MCP sunucusu ve kancalar birlikte gelir. Komutlar: /yontu:turkcelestir, /yontu:yontu-lint.',
      code: '/plugin marketplace add senrecep/yontu\n/plugin install yontu@yontu',
    },
    {
      name: 'Skill klasörü okuyan her ajan',
      note: 'Yalnız skill’i kopyalar. MCP sunucusu ve kanca eklemez.',
      code: 'npx skills add senrecep/yontu',
    },
    {
      name: 'MCP sunucusu',
      note: 'Claude Code için tek satır. Öbür istemciler aynı komutu kendi ayar dosyalarına yazar.',
      code: 'claude mcp add yontu -- uvx yontu mcp',
    },
  ],
  zipName: 'claude.ai',
  zipNote: 'Skill’i zip olarak indirin, Customize altında Skills bölümünden yükleyin. Kod çalıştırma açık olmalı.',
  zipLink: 'yontu-skill.zip indir',

  footerLicense: 'MIT lisansı',
  footerCredit: 'Kaynaklar: Türk Dil Kurumu, Yazım Kuralları ve Güncel Türkçe Sözlük.',
  footerLinks: { repo: 'GitHub', changelog: 'Değişiklikler', readme: 'README', contributing: 'Katkı rehberi' },

  notFoundTitle: 'Bu sayfa yok',
  notFoundBody: 'Aradığınız adres taşınmış ya da hiç olmamış olabilir.',
  notFoundHome: 'Ana sayfaya dön',
};

const en: typeof tr = {
  htmlLang: 'en',
  ogLocale: 'en_US',
  title: 'yontu · Turkish humanizer and TDK linter',
  description:
    'A Turkish humanizer and TDK spelling linter for AI agents. Ships as an agent skill, an MCP server and a CLI. No dependencies, works offline.',
  skip: 'Skip to content',
  nav: {
    label: 'On this page',
    demo: 'Example',
    how: 'How it works',
    proof: 'Proof',
    faq: 'FAQ',
    install: 'Install',
  },
  menuOpen: 'Open menu',
  menuClose: 'Close menu',
  switchLabel: 'Türkçe',
  switchHint: 'Bu sayfayı Türkçe oku',
  home: 'yontu home',

  heroTitle: ['Carves your agent’s Turkish.', 'Leaves the meaning alone.'],
  heroSub:
    'An open source linter for anyone writing Turkish with AI agents. It flags translation patterns and checks spelling and punctuation against the Türk Dil Kurumu (TDK) rules.',
  ctaLabel: 'Install, one command',
  proof: ['On PyPI and the MCP Registry', 'Python 3.9 to 3.14', 'no dependencies', 'MIT license'],
  heroDemoLabel: 'A real run',
  copy: 'Copy',
  copied: 'Copied',

  problemTitle: 'Rules written for English find little in Turkish',
  problemBody:
    'Most humanizers lean on English word lists such as “delve” and “tapestry”. Turkish AI text gives itself away elsewhere: sentence after sentence ending in “kullanılmaktadır”, calques, and chatbot leftovers like “Umarım yardımcı olur” (hope this helps).',
  demoTitle: 'One README, before and after yontu',
  beforeLabel: 'Before: README.md',
  afterLabel: 'After: README.md',
  legendDrop: 'dropped in the rewrite',
  legendRule: 'rule the linter reported',
  demoKept:
    'Kept: the name, the three things it finds, the command. Dropped: the adjective triad, the exclamation, “kolayca” (easily). The title moved to sentence case. Nothing was added.',
  demoSource:
    'The sample is from skills/yontu/references/ornekler.md in the repository, with output from yontu 0.1.0. It stays in Turkish because that is what the tool reads.',

  benefitsTitle: 'What it looks at',
  benefits: [
    {
      icon: 'seal',
      tag: 'BK-01 · KS-02',
      title: 'TDK spelling and punctuation',
      body: 'Every rule names the Yazım Kılavuzu section or Güncel Türkçe Sözlük entry it comes from. Autofix runs only on deterministic rules.',
    },
    {
      icon: 'fingerprint',
      tag: 'AI-E1 · AI-C18',
      title: 'AI tells that are Turkish',
      body: 'Suffix chains, calques, wrappers like “konusunda” and “bir şekilde” that stand in for a case ending, and chatbot sign offs.',
    },
    {
      icon: 'stack',
      tag: '--tur readme',
      title: 'Measured by genre',
      body: 'What is normal in an academic abstract is a tell in a blog post. yontu knows 28 genres under 17 registers, each with its own thresholds.',
    },
    {
      icon: 'shield',
      tag: 'yontu compare',
      title: 'Rewrites that cannot add facts',
      body: 'If a new number, date, name, URL or code span shows up, the comparison fails. The agent reverts that edit.',
    },
  ],

  tagline: ['It cuts the excess, keeps the substance,', 'and never adds a fact.'],

  howTitle: 'How it works',
  how: [
    {
      title: 'Install',
      body: 'The CLI and the MCP server come from PyPI. The Claude Code plugin adds hooks on top.',
      code: 'pipx install yontu',
    },
    {
      title: 'Lint',
      body: 'Each finding comes with line, column, rule id, level and a suggestion. Pass the genre and the thresholds follow it.',
      code: 'yontu lint metin.md --tur readme',
    },
    {
      title: 'Gate the rewrite',
      body: 'The rewritten version is compared with the original. If it carries new facts, the command exits with 1.',
      code: 'yontu compare eski.md yeni.md',
    },
  ],

  proofTitle: 'The proof is in the repository',
  proofIntro: 'It is all in the repository. Run the tests yourself and reproduce every output below on your own machine.',
  facts: [
    ['dependencies', '0, Python standard library only'],
    ['MCP', 'hand written JSON-RPC, no SDK'],
    ['tests', '251 unit tests, run in CI on every change'],
    ['Python', '3.9, 3.10, 3.11, 3.12, 3.13, 3.14 and macOS'],
    ['version', '0.1.0, on PyPI and the MCP Registry'],
    ['release', 'GitHub Releases with SHA256 checksums'],
  ] as [string, string][],
  gateTitle: 'The gate catches an added date',
  gateBody:
    'Fixing a meeting note, the agent changed the date and added a time. The comparison reports two errors and exits with 1.',
  gateOld: 'eski.md (old)',
  gateNew: 'yeni.md (new)',
  gateExit: 'exit code 1',
  explainTitle: 'Every rule names its source',
  explainBody: 'yontu explain shows a rule’s layer, level, source, and what it catches and what it leaves alone.',
  tdkTitle: 'Safe fixes only where the rule is certain',
  tdkBody: '“Herşey” and “Türkçe’de” get fixed. The closer “Umarım yardımcı olur” is flagged, not deleted. That call belongs to the writer.',

  faqTitle: 'Questions',
  faq: [
    ['Is yontu an AI detector?', 'No. yontu reports patterns. A finding does not mean a text was machine written, and a clean report does not mean it was not. Passing a detector is not a goal.'],
    ['Does my text go to a server?', 'No. The linter makes no network calls and every rule runs on your machine. The MCP server is a local process too.'],
    ['Which agents does it work with?', 'Claude Code, Codex CLI, Cursor, Gemini CLI and any MCP client. On claude.ai the skill is uploaded as a zip. Config files for other tools are in the integrations folder of the repository.'],
    ['Does it fix the text itself?', 'Only for deterministic rules in the tdk layer, and only when you pass --fix. AI patterns are never fixed automatically. The agent rewrites, yontu checks.'],
    ['Will it report false positives?', 'Yes. The ai-iz, stil and yogunluk rules are regular expressions and counts over surface forms, with no morphological analysis. That is why most of them stay at info.'],
    ['Which kinds of text does it know?', '28 genres under 17 registers, from academic abstracts to commit messages and from petitions to ad copy. Without a genre, it guesses the register from the content.'],
    ['What does it need?', 'Python 3.9 or newer. Nothing else gets installed.'],
    ['Does it cost anything?', 'No. yontu is open source under the MIT license.'],
    ['Does it have a dictionary?', 'No. It catches known misspellings, not every misspelling. The thresholds are not yet calibrated on a corpus of human writing either.'],
  ],

  riskTitle: 'Trying it costs you nothing',
  riskBody:
    'No license fee, account or API key. The code is MIT licensed and the source of every rule is in the repository. It uses only the Python standard library, and your text never leaves your machine.',
  risk: [
    ['Free', 'No license fee, account or API key.'],
    ['Open source', 'MIT license. The code and source of every rule are in the repository.'],
    ['No dependencies', 'Python standard library only.'],
    ['Offline', 'Your text never leaves your machine.'],
  ],

  routesTitle: 'Other ways to install',
  routes: [
    {
      name: 'Claude Code plugin',
      note: 'Skill, MCP server and hooks together. Commands: /yontu:turkcelestir, /yontu:yontu-lint.',
      code: '/plugin marketplace add senrecep/yontu\n/plugin install yontu@yontu',
    },
    {
      name: 'Any agent that reads skill folders',
      note: 'Copies the skill only. No MCP server, no hooks.',
      code: 'npx skills add senrecep/yontu',
    },
    {
      name: 'MCP server',
      note: 'One line for Claude Code. Other clients put the same command in their config file.',
      code: 'claude mcp add yontu -- uvx yontu mcp',
    },
  ],
  zipName: 'claude.ai',
  zipNote: 'Download the skill as a zip and upload it under Customize, then Skills. Code execution has to be on.',
  zipLink: 'Download yontu-skill.zip',

  footerLicense: 'MIT license',
  footerCredit: 'Sources: Türk Dil Kurumu, Yazım Kuralları and Güncel Türkçe Sözlük.',
  footerLinks: { repo: 'GitHub', changelog: 'Changelog', readme: 'README', contributing: 'Contributing' },

  notFoundTitle: 'This page does not exist',
  notFoundBody: 'The address may have moved, or it never existed.',
  notFoundHome: 'Back to the home page',
};

export const strings = { tr, en };
