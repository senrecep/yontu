"""Fidelity gate: compare an input text with its rewrite.

New numbers, dates, URLs, code spans and names are errors. Removed items and
changes in negation, modality, evidence strength, person, cause and quotes are
warnings. A few over-correction signals are warnings too.
"""
import re

from . import textutil as tu

L = tu.LETTERS
LOW = tu.LOWER

MONTHS = ("ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos",
          "eylül", "ekim", "kasım", "aralık")
NUMBER_WORDS = {
    "sıfır": "0", "bir": "1", "iki": "2", "üç": "3", "dört": "4", "beş": "5", "altı": "6",
    "yedi": "7", "sekiz": "8", "dokuz": "9", "on": "10", "yirmi": "20", "otuz": "30",
    "kırk": "40", "elli": "50", "altmış": "60", "yetmiş": "70", "seksen": "80",
    "doksan": "90", "yüz": "100", "bin": "1000", "milyon": "1000000", "milyar": "1000000000",
    "trilyon": "1000000000000", "yarım": "0.5", "çeyrek": "0.25",
}
SCALES = {"bin": 1000, "milyon": 10 ** 6, "milyar": 10 ** 9, "trilyon": 10 ** 12}

_FENCE = re.compile(r"^(```|~~~)[^\n]*\n(.*?)(?:^\1[^\n]*$|\Z)", re.S | re.M)
_INLINE = re.compile(r"`([^`\n]+)`")
_FRONT = re.compile(r"\A---\n.*?\n---[ \t]*(?:\n|\Z)", re.S)
_URL = re.compile(r"(?:https?|ftp)://[^\s<>()\"'`]+[^\s<>()\"'`.,;:!?]|www\.[^\s<>()\"'`]+[^\s<>()\"'`.,;:!?]"
                  r"|[\w.+-]+@[\w-]+\.[\w.-]*\w")
_DATE = re.compile(r"(?<!\d)(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})(?!\d)"
                   r"|(?<![\w])(?:\d{1,2}\s+)?(?:" + "|".join(m.capitalize() for m in MONTHS) + r")"
                   r"(?:\s+\d{4})?(?:['’][" + LOW + r"]+)?(?![" + L + r"])")
_NUM = re.compile(r"(?<![\w.,])(?:[-−](?=\d))?%?\s?\d+(?:[.,:]\d+)*\s?%?")
_SCALED = re.compile(r"(?<![\w.,])([-−]?\d+(?:[.,]\d+)?)\s+(bin|milyon|milyar|trilyon)(?![" + L + r"])"
                     r"(?:['’][" + LOW + r"]+|[" + LOW + r"]*)")
_UP = re.compile(r"(?<![" + L + r"])(?:art(?:tı|ar|mış|acak|ıyor|ma|ış)|yüksel|çoğal|büyü(?:dü|r|müş|yecek|yor|me))[" + LOW + r"]*")
_DOWN = re.compile(r"(?<![" + L + r"])(?:azal|düş(?:tü|er|müş|ecek|üyor|üş)|gerile|küçül)[" + LOW + r"]*")
_QUOTE = re.compile(r"\"([^\"\n]{2,400})\"|“([^”\n]{2,400})”|«([^»\n]{2,400})»")
_WORD = re.compile(r"[" + L + r"0-9]+(?:['’][" + L + r"]+)?")
_ACRONYM = re.compile(r"^[" + tu.UPPER + r"0-9]{2,}$")

_NEG = re.compile(
    r"(?<![" + L + r"])(?:değil|yok|hayır|hiçbir|asla)[" + LOW + r"]*"
    r"|[" + L + r"]{2,}(?:m[ae]z(?![" + LOW + r"]*lı)|m[ae]d[ıiuü](?!r)|m[ıiuü]yor|m[ae]y[ae]c[ae]k|m[ae]y[ae]n"
    r"|m[ae]m[ıiuü]ş|m[ae]m[ae]l[ıi]|m[ae]y[ıiuü]n|m[ae]d[ae]n|m[ae]y[ıiuü]p|m[ae]s[ıi]n(?![" + LOW + r"]))"
    r"[" + LOW + r"]*", re.M)

MODALITY = {
    "zorunluluk": r"[" + L + r"]{2,}m[ae]l[ıi](?:[ydt][ıi]r|y[ıi]z|s[ıi]n|y[ıi]m|d[ıi]|ydı)?(?![" + LOW + r"])"
                  r"|(?<![" + L + r"])gerek(?:ir|mektedir|iyor|li|lidir|meli)?(?![" + LOW + r"])"
                  r"|(?<![" + L + r"])zorunlu[" + LOW + r"]*|(?<![" + L + r"])şart(?:tır)?(?![" + LOW + r"])",
    "olanak": r"[" + L + r"]{2,}[ae]bil[" + LOW + r"]*|[" + L + r"]{2,}[ae]m[ae](?:z|d[ıi]|y[ae]c[ae]k|m[ıi]ş)[" + LOW + r"]*"
              r"|(?<![" + L + r"])(?:mümkün|imk[aâ]n|olanak)[" + LOW + r"]*",
    "olasılık": r"(?<![" + L + r"])(?:muhtemelen|belki|galiba|sanırım|herhalde|olasılıkla|büyük\s+ihtimalle|olası)(?![" + LOW + r"])"
                r"|[" + L + r"]{2,}m[ıiuü]ş\s+ol[ae]bilir",
    "kesinlik": r"(?<![" + L + r"])(?:kesinlikle|mutlaka|elbette|şüphesiz|kuşkusuz|tartışmasız|açıkça)(?![" + LOW + r"])",
}
EVIDENCE_LADDER = [
    ("düşündürmek", r"(?<![" + L + r"])düşündür[" + LOW + r"]*"),
    ("işaret etmek", r"(?<![" + L + r"])işaret\s+e[dt][" + LOW + r"]*"),
    ("göstermek", r"(?<![" + L + r"])göster(?!ge)[" + LOW + r"]*"),
    ("kanıtlamak", r"(?<![" + L + r"])(?:kanıtl|ispatl|ispat\s+e[dt])[" + LOW + r"]*"),
]
_FIRST_PERSON = re.compile(
    r"(?<![" + L + r"])(?:ben|biz|bana|bize|beni|bizi|benim|bizim|bende|bizde|benden|bizden|bence|bizce)(?![" + LOW + r"])"
    r"|(?<![" + L + r"])(?!artık)[" + L + r"]{2,}(?:[ıiuü]yor(?:um|uz)|[dt][ıiuü][mk]|[ae]c[ae]ğ[ıi][mz]|[ae]c[ae]ğ[ıi]z)(?![" + LOW + r"])")
_CAUSE = re.compile(
    r"(?<![" + L + r"])(?:çünkü|zira|bu\s+yüzden|bu\s+nedenle|bu\s+sebeple|dolayısıyla|bundan\s+dolayı)(?![" + LOW + r"])"
    r"|[" + L + r"]{2,}[dt][ıiuü]ğ[ıiuü](?:\s+için|nd[ae]n)(?![" + LOW + r"])"
    r"|(?<![" + L + r"])(?:sayesinde|yüzünden|nedeniyle|sebebiyle)(?![" + LOW + r"])")


# Claim words a rewrite tends to drop with the clause around them ("— tazelik garantisiyle!").
CLAIM_WORDS = ("garanti", "ücretsiz", "bedava", "indirim", "iade", "iptal", "hediye", "taksit",
               "kampanya", "tazelik", "sınırsız", "ömür boyu")
_CLAIM = {w: re.compile(r"(?<![" + L + r"])" + re.escape(w).replace(r"\ ", r"\s+"))
          for w in CLAIM_WORDS}
_SENT_START = re.compile(r"(?:^|[.!?:;\n]\s*|[\"'(]\s*)$")


def _neg_count(text, low):
    """Count negations; skip capitalized words inside a sentence (likely names such as Yılmaz)."""
    n = 0
    for m in _NEG.finditer(low):
        i = m.start()
        if text[i] != low[i] and not _SENT_START.search(text[max(0, i - 3):i]):
            continue
        n += 1
    return n


def _count(pattern, low):
    return len(re.findall(pattern, low, re.M))


def _blank(text, spans):
    chars = list(text)
    for s, e in spans:
        for i in range(s, e):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def number_keys(raw):
    """All plausible readings of a number: 1.500 and 1,500 can both mean 1500."""
    s = raw.strip().strip("%").strip().replace("−", "-")
    sign = "-" if s.startswith("-") else ""
    s = s.lstrip("-")
    keys = {s, s.replace(":", ".")}
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", s):
        keys.add(s.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", s):
        keys.add(s.replace(",", ""))
    if re.fullmatch(r"\d+,\d+", s):
        keys.add(s.replace(",", "."))
    out = set()
    for k in keys:
        if re.fullmatch(r"\d+\.0+", k):
            k = k.split(".")[0]
        out.add(sign + (k.lstrip("0") or "0"))
    return out


def _scaled_key(num, scale):
    """5 milyon -> 5000000, 2,5 milyar -> 2500000000."""
    from fractions import Fraction
    num = num.replace("−", "-").replace(",", ".")
    try:
        v = Fraction(num) * SCALES[scale]
    except (ValueError, ZeroDivisionError):
        return None
    return str(v.numerator) if v.denominator == 1 else str(float(v))


def _name_stem(word):
    return tu.tr_lower(re.split(r"['’]", word)[0])


def extract(text):
    """Pull comparable items out of a text. Returns {kind: {key: shown}}."""
    text = tu.nfc(text).replace("\r\n", "\n")
    items = {"kod": {}, "url": {}, "tarih": {}, "sayı": {}, "ad": {}, "alıntı": {}}
    spans = []
    m = _FRONT.match(text)
    if m:
        spans.append(m.span())
    for m in _FENCE.finditer(text):
        body = m.group(2).strip()
        if body:
            items["kod"][body] = body.splitlines()[0][:60]
        spans.append(m.span())
    work = _blank(text, spans)
    spans = []
    for m in _INLINE.finditer(work):
        items["kod"][m.group(1)] = m.group(1)
        spans.append(m.span())
    work = _blank(work, spans)
    spans = []
    for m in _URL.finditer(work):
        items["url"][m.group(0).rstrip("/")] = m.group(0)
        spans.append(m.span())
    work = _blank(work, spans)
    for m in _QUOTE.finditer(work):
        q = next(g for g in m.groups() if g)
        items["alıntı"][tu.tr_lower(q.strip())] = q.strip()
    spans = []
    for m in _DATE.finditer(work):
        raw = m.group(0)
        key = re.sub(r"['’][" + LOW + r"]+$", "", tu.tr_lower(raw))
        key = re.sub(r"\s+", " ", key)
        items["tarih"][key] = raw
        spans.append(m.span())
    work = _blank(work, spans)
    spans = []
    for m in _SCALED.finditer(work):
        key = _scaled_key(m.group(1), m.group(2))
        if key:
            items["sayı"][key] = m.group(0)
            spans.append(m.span())
    work = _blank(work, spans)
    work = re.sub(r"(?m)^(\s*)\d+([.)]\s)", lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1)) - 1) + m.group(2)[-1:], work)
    for m in _NUM.finditer(work):
        raw = m.group(0).strip()
        if not re.search(r"\d", raw):
            continue
        items["sayı"][raw.strip("%").strip()] = raw
    for key, shown in _names(work):
        items["ad"].setdefault(key, shown)
    return items


def _names(work):
    """Capitalized words that are not sentence-initial, words with an apostrophe
    suffix after a capital, and acronyms."""
    out = []
    for line in work.split("\n"):
        body = re.sub(r"^\s*(?:#{1,6}\s+|[-*+•]\s+|\d+[.)]\s+|>\s*|\|)", "", line)
        start_of_sentence = True
        for m in _WORD.finditer(body):
            w = m.group(0)
            before = body[:m.start()].rstrip()
            if before and before[-1] in ".!?:…|(\"“«'‘-–·/•;":
                start_of_sentence = True
            is_cap = tu.is_upper_initial(w) and not w[0].isdigit()
            if is_cap:
                stem = re.split(r"['’]", w)[0]
                if _ACRONYM.match(stem) and not stem.isdigit():
                    out.append((_name_stem(w), stem))
                elif "'" in w or "’" in w or not start_of_sentence:
                    out.append((_name_stem(w), stem))
            start_of_sentence = False
    return out


def _word_set(low):
    return set(_WORD.findall(re.sub(r"['’]", "", low)))


def _present_name(key, words):
    """True when some word of the other text is the same name with other suffixes."""
    key = re.sub(r"['’]", "", key)
    for w in words:
        if w.startswith(key) or key.startswith(w) and len(w) >= 4:
            return True
        n = 0
        for a, b in zip(w, key):
            if a != b:
                break
            n += 1
        if n >= max(4, min(len(w), len(key)) - 3):
            return True
    return False


def _number_words(low):
    """Single number words and the values of runs such as "on iki" or "iki yüz bin"."""
    found = set()
    total = cur = 0
    run = 0

    def close():
        if run > 1 and total + cur:
            found.add(str(total + cur))

    for m in re.finditer(r"[" + LOW + r"]+|[^" + LOW + r"]+", low):
        w = m.group(0)
        if not w.strip():
            continue
        v = NUMBER_WORDS.get(w)
        if v is None or "." in v:
            close()
            total = cur = run = 0
            if v is not None:
                found.add(v)
            continue
        found.add(v)
        v = int(v)
        if v == 100:
            cur = (cur or 1) * 100
        elif v >= 1000:
            total += (cur or 1) * v
            cur = 0
        else:
            cur += v
        run += 1
    close()
    return found


def _sentences(text):
    return [text[s:e] for s, e in tu.split_sentences(text)]


def _overcorrection(old, new):
    out = []
    so, sn = _sentences(old), _sentences(new)
    short = lambda ss: sum(1 for s in ss if 0 < len(tu.words(s)) <= 3)
    if len(sn) >= 5:
        rn = short(sn) / float(len(sn))
        ro = short(so) / float(len(so)) if so else 0.0
        if rn > 0.2 and rn > ro + 0.05:
            out.append(("SD-12", "Kısa vurucu cümle oranı arttı: %%%d." % round(rn * 100)))
    qa = lambda ss: sum(1 for i, s in enumerate(ss[:-1]) if s.rstrip().endswith("?")
                        and not ss[i + 1].rstrip().endswith("?"))
    words_new = max(len(tu.words(new)), 1)
    qn, qo = qa(sn), qa(so)
    if qn > qo and qn >= max(2, 2 * words_new / 300.0):
        out.append(("SD-13", "Soru-cevap çifti eklendi: %d." % (qn - qo)))
    return out


MESSAGES = {
    "kod": ("SD-04", "Yeni kod parçası"),
    "url": ("SD-03", "Yeni URL veya e-posta"),
    "tarih": ("SD-02", "Yeni tarih"),
    "sayı": ("SD-01", "Yeni sayı"),
    "ad": ("SD-05", "Yeni özel ad"),
}


class _Side(object):
    """One text's items, with lookups that tolerate suffixes and number formats."""

    def __init__(self, items, low):
        self.items = items
        self.low = low
        self.words = _word_set(low)
        self.numkeys = set(_number_words(low))
        for raw in items["sayı"]:
            self.numkeys |= number_keys(raw)
        for d in items["tarih"]:
            for part in re.findall(r"\d+", d):
                self.numkeys |= number_keys(part)

    def has(self, kind, key):
        if key in self.items[kind]:
            return True
        if kind == "ad":
            return _present_name(key, self.words)
        if kind == "sayı":
            return bool(number_keys(key) & self.numkeys)
        if kind == "tarih":
            return all(p in self.low for p in key.split())
        if kind == "kod":
            return tu.tr_lower(key) in self.low
        return False


def compare(old, new):
    """Return {"findings": [...], "errors": n, "warnings": n}."""
    old, new = tu.nfc(old).replace("\r\n", "\n"), tu.nfc(new).replace("\r\n", "\n")
    a, b = extract(old), extract(new)
    low_old, low_new = tu.tr_lower(old), tu.tr_lower(new)
    findings = []

    def add(fid, level, message, item=None):
        f = {"id": fid, "level": level, "message": message}
        if item is not None:
            f["item"] = item
        findings.append(f)

    side_old = _Side(a, low_old)
    side_new = _Side(b, low_new)
    for kind in ("kod", "url", "tarih", "sayı", "ad"):
        fid, msg = MESSAGES[kind]
        for key, shown in b[kind].items():
            if not side_old.has(kind, key):
                add(fid, "error", "%s: %s" % (msg, shown), shown)
        for key, shown in a[kind].items():
            if not side_new.has(kind, key):
                add("SD-06", "warning", "Çıkarılan öğe (%s): %s" % (kind, shown), shown)
    for key, shown in b["alıntı"].items():
        if key not in a["alıntı"] and key not in low_old:
            add("SD-14", "warning", "Yeni alıntı: \"%s\"" % shown[:60], shown)
    for key, shown in a["alıntı"].items():
        if key not in b["alıntı"] and key not in low_new:
            add("SD-06", "warning", "Çıkarılan alıntı: \"%s\"" % shown[:60], shown)

    no, nn = _neg_count(old, low_old), _neg_count(new, low_new)
    if no != nn:
        add("SD-07", "warning", "Olumsuzluk sayısı değişti: %d → %d." % (no, nn))
    for name, pat in MODALITY.items():
        co, cn = _count(pat, low_old), _count(pat, low_new)
        if co != cn:
            add("SD-08", "warning", "Kip belirteci değişti (%s): %d → %d." % (name, co, cn))
    ladder_old = [_count(p, low_old) for _, p in EVIDENCE_LADDER]
    ladder_new = [_count(p, low_new) for _, p in EVIDENCE_LADDER]
    if ladder_old != ladder_new:
        moved = ", ".join("%s %d → %d" % (EVIDENCE_LADDER[i][0], o, n)
                          for i, (o, n) in enumerate(zip(ladder_old, ladder_new)) if o != n)
        add("SD-09", "warning", "Kanıt basamağı değişti: %s." % moved)
    uo, do_ = len(_UP.findall(low_old)), len(_DOWN.findall(low_old))
    un, dn = len(_UP.findall(low_new)), len(_DOWN.findall(low_new))
    if (un < uo and dn > do_) or (un > uo and dn < do_):
        add("SD-15", "warning", "Yön değişti: artış %d → %d, azalış %d → %d." % (uo, un, do_, dn))
    fo, fn = len(_FIRST_PERSON.findall(low_old)), len(_FIRST_PERSON.findall(low_new))
    if fn > fo:
        add("SD-10", "warning", "Birinci şahıs eklendi: %d → %d." % (fo, fn))
    co, cn = len(_CAUSE.findall(low_old)), len(_CAUSE.findall(low_new))
    if cn > co:
        add("SD-11", "warning", "Yeni neden bağı eklendi: %d → %d." % (co, cn))
    for word, pat in _CLAIM.items():
        co, cn = len(pat.findall(low_old)), len(pat.findall(low_new))
        if cn < co:
            add("SD-16", "warning", "İddia sözcüğü çıkarıldı (%s): %d → %d." % (word, co, cn), word)
    for fid, msg in _overcorrection(old, new):
        add(fid, "warning", msg)
    errors = sum(1 for f in findings if f["level"] == "error")
    return {"findings": findings, "errors": errors, "warnings": len(findings) - errors}
