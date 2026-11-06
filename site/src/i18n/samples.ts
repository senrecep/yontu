// Real samples and real CLI output. The before/after pair comes from
// skills/yontu/references/ornekler.md (README genre); the terminal lines were
// produced by yontu 0.1.0 on these exact files.

export type Segment = { t: string; drop?: boolean; rule?: string; code?: boolean };

export const before: Segment[][] = [
  [
    { t: 'yontu: Türkçe Metinler İçin ' },
    { t: 'Modern ', drop: true },
    { t: 'Ve', drop: true, rule: 'BH-13' },
    { t: ' Güçlü Bir ', drop: true },
    { t: 'Linter' },
  ],
  [
    { t: 'yontu, Türkçe ' },
    { t: 'metinlerinizi analiz ederek', drop: true },
    { t: ' yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini ' },
    { t: 'tespit eden, ', drop: true },
    { t: 'modern, güçlü ve kullanıcı dostu', drop: true, rule: 'AI-D15' },
    { t: ' bir ' },
    { t: 'araçtır', drop: true },
    { t: '. ' },
    { t: 'Projenin temel amacı, yazım kalitenizi ', drop: true },
    { t: 'bir üst seviyeye taşımaktır', drop: true, rule: 'AI-D13' },
    { t: '!', drop: true },
  ],
  [
    { t: 'Kullanım: ' },
    { t: 'Analiz işlemini gerçekleştirmek', drop: true, rule: 'YS-A25' },
    { t: ' için aşağıdaki komutu kolayca çalıştırabilirsiniz:', drop: true },
    { t: ' ' },
    { t: 'yontu lint metin.md', code: true },
  ],
];

export const after: Segment[][] = [
  [{ t: 'yontu: Türkçe metinler için linter' }],
  [{ t: 'yontu, Türkçe metindeki yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini bulan bir linterdir.' }],
  [{ t: 'Kullanım: ' }, { t: 'yontu lint metin.md', code: true }],
];

export const lintBefore = {
  cmd: 'yontu lint metin.md --tur readme',
  lines: [
    'metin.md:1:36: uyarı BH-13 [tdk] Başlıkta büyük yazılan sözler arasında "ve", "ile", "ya", "veya", "ki", "de", "mi" küçük yazılır. «Ve» → ve',
    'metin.md:3:49: bilgi AI-C8 [ai-iz] Aynı paragrafta birden çok üçlü sıralama var. (2 kez, eşik 2) «hatalarını, noktalama sorunlarını ve yapay»',
    'metin.md:3:119: bilgi AI-D15 [ai-iz] Pazarlama sıfatı üçlüsü. Aracın ne yaptığını yazın. «modern, güçlü ve kullanıcı dostu»',
    'metin.md:3:204: bilgi AI-D13 [ai-iz] Kalıp vaat: "bir üst seviyeye taşımak". Neyin nasıl değiştiğini yazın. «bir üst seviyeye taşımaktır»',
    'metin.md:5:11: bilgi YS-A25 [yogunluk] Hafif fiil kalıbı: "-mA işlemini gerçekleştirmek". «Analiz işlemini gerçekleştirmek» → fiilin kendisi',
  ],
  summary: 'metin.md: 0 hata, 1 uyarı, 4 bilgi · teknik/readme (flag)',
};

export const lintAfter = {
  cmd: 'yontu lint yontulmus.md --tur readme',
  lines: [] as string[],
  summary: 'yontulmus.md: 0 hata, 0 uyarı, 0 bilgi · teknik/readme (flag)',
};

export const compareOk = {
  cmd: 'yontu compare metin.md yontulmus.md',
  lines: [
    'uyarı SD-06 Çıkarılan öğe (ad): Modern',
    'uyarı SD-06 Çıkarılan öğe (ad): Güçlü',
    'uyarı SD-08 Kip belirteci değişti (olanak): 1 → 0.',
  ],
  summary: 'sadakat: 0 hata, 3 uyarı',
};

export const gate = {
  old: 'Toplantı 12 Kasım günü yapılacak.',
  new: "Toplantı 14 Kasım günü saat 10.00'da yapılacak.",
  cmd: 'yontu compare eski.md yeni.md',
  lines: [
    'hata SD-02 Yeni tarih: 14 Kasım',
    'uyarı SD-06 Çıkarılan öğe (tarih): 12 Kasım',
    'hata SD-01 Yeni sayı: 10.00',
  ],
  summary: 'sadakat: 2 hata, 1 uyarı',
  exit: 1,
};

export const tdk = {
  input: "Herşey hazır, Türkçe'de yazdığımız metni kontrol edelim ve bitirelim. Umarım yardımcı olur.",
  cmd: 'yontu lint not.md',
  lines: [
    'not.md:1:1: hata BK-01 [tdk] Bu söz ayrı yazılır. «Herşey» → Her şey',
    "not.md:1:15: hata KS-02 [tdk] Dil adlarına gelen ekler kesmeyle ayrılmaz. «Türkçe'de» → Türkçede",
    'not.md:1:71: bilgi AI-E1 [ai-iz] Sohbet kapanışı. Metinde gereksiz. «Umarım yardımcı olur»',
  ],
  summary: 'not.md: 2 hata, 0 uyarı, 1 bilgi · notr/- (içerik 0.00)',
  fixCmd: 'yontu lint not.md --fix',
  fixOut: 'Her şey hazır, Türkçede yazdığımız metni kontrol edelim ve bitirelim. Umarım yardımcı olur.',
};

export const explain = {
  cmd: 'yontu explain KS-02',
  rows: [
    ['kimlik', 'KS-02'],
    ['katman', 'tdk'],
    ['düzey', 'error'],
    ['kanıt', 'kaynak'],
    ['ileti', 'Dil adlarına gelen ekler kesmeyle ayrılmaz.'],
    ['kaynak', 'TDK Yazım Kılavuzu, Kesme İşareti'],
    ['yakalar', "Türkçe'de bu böyle."],
    ['yakalamaz', 'Türkçede bu böyle.'],
  ],
};

// From README.md, "Profiles".
export const registers: [string, string[]][] = [
  ['akademik', ['akademik-ozet', 'akademik-giris', 'akademik-tartisma', 'tez']],
  ['resmi', ['dilekce', 'resmi-yazi']],
  ['hukuk', ['hukuk']],
  ['haber', ['haber']],
  ['deneme', ['kose']],
  ['blog', ['blog', 'linkedin']],
  ['teknik', ['teknik-dok', 'readme', 'changelog']],
  ['commit', ['commit']],
  ['ui', ['ui-buton', 'ui-hata', 'ui-bos']],
  ['pazarlama', ['reklam', 'e-ticaret']],
  ['sosyal', ['x', 'instagram']],
  ['kurumsal', ['resmi-eposta', 'basin-bulteni']],
  ['is-eposta', ['is-eposta']],
  ['sozlu', ['sunum']],
  ['edebi', ['edebi']],
  ['sohbet', ['sohbet']],
  ['notr', []],
];
