"""Turkish-safe text helpers: case mapping, masking, sentence splitting."""
import re
import unicodedata

LOWER = "a-zçğıöşüâîû"
UPPER = "A-ZÇĞİÖŞÜÂÎÛ"
LETTERS = LOWER + UPPER
APOS = "['’]"
VOWELS = "aeıioöuüâîû"
BACK_VOWELS = "aıouâû"
ROUND_VOWELS = "oöuüû"
VOICELESS = "çfhkpsştx"

_TOKENS = {
    "%L": LOWER,
    "%U": UPPER,
    "%W": LETTERS,
    "%B": "(?<![" + LETTERS + "0-9])",
    "%E": "(?![" + LETTERS + "0-9])",
    "%A": APOS,
}


def expand(pattern):
    """Expand %L %U %W %B %E %A placeholders in a rule pattern."""
    for key in ("%B", "%E", "%A", "%L", "%U", "%W"):
        pattern = pattern.replace(key, _TOKENS[key])
    return pattern


def nfc(text):
    return unicodedata.normalize("NFC", text)


def tr_lower(text):
    """Lowercase with Turkish dotted/dotless i. Length is preserved."""
    out = text.replace("I", "ı").replace("İ", "i").lower()
    if len(out) == len(text):
        return out
    chars = []
    for ch in text:
        if ch == "I":
            chars.append("ı")
        elif ch == "İ":
            chars.append("i")
        else:
            low = ch.lower()
            chars.append(low if len(low) == 1 else ch)
    return "".join(chars)


def tr_upper(text):
    return text.replace("i", "İ").replace("ı", "I").upper()


def tr_capitalize(text):
    if not text:
        return text
    return tr_upper(text[0]) + text[1:]


def is_upper_initial(word):
    return bool(word) and word[0] in "ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZÂÎÛ"


# --- masking -------------------------------------------------------------

_MASK_PATTERNS = [
    re.compile(r"\A---\n.*?\n---[ \t]*(?:\n|\Z)", re.S),            # YAML frontmatter
    re.compile(r"^(?P<f>```|~~~)[^\n]*\n.*?(?:^(?P=f)[^\n]*$|\Z)", re.S | re.M),  # fences
    re.compile(r"<!--.*?-->", re.S),                                  # HTML comments
    re.compile(r"`[^`\n]+`"),                                         # inline code
    re.compile(r"^[ \t]*>[^\n]*", re.M),                              # blockquote lines
    re.compile(r"\]\([^)\s]*\)"),                                     # markdown link target
    re.compile(r"(?:https?|ftp)://[^\s<>()\"'`]+|www\.[^\s<>()\"'`]+"),  # URLs
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),                          # e-mail
    re.compile(r"</?[A-Za-z][^>\n]*>"),                               # HTML tags
    re.compile(r"(?<![\w/])(?:~|\.{1,2})?/?(?:(?:[\w.*-]|\{[^}\s]*\})+/)+(?:[\w.*-]|\{[^}\s]*\})*"),  # paths a/b/{c,d}
    re.compile(r"(?<![\w.])[\w-]+\.(?:py|js|ts|tsx|jsx|json|ya?ml|toml|md|txt|sh|go|rs|rb|java|kt|swift|c|h|cpp|cs|php|html|css|ini|cfg|lock|xml|csv|sql|env|po)(?![\w])"),
    re.compile(r"\{\{[^}\n]*\}\}|\{[0-9a-zA-Z_]+\}"),                  # template placeholders
]

_QUOTE_PATTERNS = [
    re.compile(r"\"[^\"\n]{1,400}\""),
    re.compile(r"“[^”\n]{1,400}”"),
    re.compile(r"«[^»\n]{1,400}»"),
]


def code_spans(text, inline=True):
    """Spans of fenced code (and inline code when inline=True)."""
    spans = [m.span() for m in _MASK_PATTERNS[1].finditer(text)]
    if inline:
        for m in _MASK_PATTERNS[3].finditer(text):
            if not any(a <= m.start() < b for a, b in spans):
                spans.append(m.span())
    return spans


def code_mask(text, inline=True):
    mask = [False] * len(text)
    for a, b in code_spans(text, inline):
        for i in range(a, b):
            mask[i] = True
    return mask


def build_mask(text):
    """Return a list of booleans, True where text is masked (code, URL, ...)."""
    mask = [False] * len(text)
    for pat in _MASK_PATTERNS:
        for m in pat.finditer(text):
            for i in range(m.start(), m.end()):
                mask[i] = True
    return mask


def apply_mask(text, mask):
    return "".join(" " if (m and ch != "\n") else ch for ch, m in zip(text, mask))


def quote_mask(text):
    mask = [False] * len(text)
    for pat in _QUOTE_PATTERNS:
        for m in pat.finditer(text):
            for i in range(m.start(), m.end()):
                mask[i] = True
    return mask


# --- sentences -------------------------------------------------------------

ABBREVIATIONS = {
    "dr", "prof", "doç", "yrd", "vb", "vs", "no", "s", "sf", "alb", "cad", "sok",
    "mah", "ltd", "şti", "a.ş", "t.c", "alm", "ar", "ing", "bkz", "örn", "yy",
    "av", "müh", "bşk", "gn", "md", "c", "sy", "st", "apt", "tel", "nu", "is",
    "hz", "ord", "uzm", "öğr", "gör", "arş", "op", "fr", "lat", "fars", "yun", "s.a",
}
# real words too: an abbreviation only when capitalized or followed by a digit or lowercase
_AMBIGUOUS = {"gör", "sok", "tel", "no", "is", "ar", "av", "op", "nu", "st", "fr", "lat", "c", "s"}
_ROMAN = re.compile(r"^[IVXLC]+$")
_SENT_END = re.compile(r"[.!?…]+[\"'”’»)]*(?=\s+|$)")
_BLOCK_LINE = re.compile(r"^\s*(?:#{1,6}\s|[-*+•]\s|\d+[.)]\s|\|)")


def _is_abbrev(text, dot_pos):
    j = dot_pos
    while j > 0 and (text[j - 1].isalnum() or text[j - 1] == "."):
        j -= 1
    token = text[j:dot_pos]
    low = tr_lower(token)
    rest = text[dot_pos + 1:dot_pos + 4].lstrip()
    soft = bool(rest) and (rest[0].isdigit() or rest[0].islower())
    if low in _AMBIGUOUS:
        return is_upper_initial(token) or soft  # "Öğr. Gör. Ali" but "gel, gör. Sonra"
    if low in ABBREVIATIONS or low.rstrip(".") in ABBREVIATIONS:
        return True
    if _ROMAN.match(token):
        return True
    if len(token) == 1 and token.isalpha():
        return token.isupper() or soft  # initials: A. Yılmaz
    return False


def split_paragraphs(text):
    """Yield (start, end) of paragraphs separated by blank lines."""
    out = []
    for m in re.finditer(r"(?:[^\n]|\n(?![ \t]*\n))+", text):
        if m.group().strip():
            out.append((m.start(), m.end()))
    return out


def split_sentences(text):
    """Return a list of (start, end) spans. Headings and list items are own units."""
    spans = []
    for pstart, pend in split_paragraphs(text):
        # split paragraph into blocks: list items / headings start a new block
        blocks = []
        cur = pstart
        pos = pstart
        for line in text[pstart:pend].split("\n"):
            if pos != pstart and _BLOCK_LINE.match(line):
                blocks.append((cur, pos - 1))
                cur = pos
            if _BLOCK_LINE.match(line) and line.lstrip().startswith("#"):
                blocks.append((cur, pos + len(line)))
                cur = pos + len(line) + 1
            pos += len(line) + 1
        if cur < pend:
            blocks.append((cur, pend))
        for bstart, bend in blocks:
            if bstart >= bend:
                continue
            start = bstart
            for m in _SENT_END.finditer(text, bstart, bend):
                end = m.end()
                nxt = text[end:end + 40].lstrip()
                if m.group()[0] == "." and len(m.group().rstrip("\"'”’»)")) == 1:
                    if _is_abbrev(text, m.start()):
                        continue
                    if nxt and (nxt[0].islower() or nxt[0] in ",;:"):
                        continue
                    before = text[max(bstart, m.start() - 4):m.start()]
                    if re.search(r"\d$", before) and nxt[:1].isdigit():
                        continue
                if nxt and nxt[0].islower() and m.group()[0] in "?!":
                    continue
                if text[start:end].strip():
                    spans.append(_trim(text, start, end))
                start = end
            if text[start:bend].strip():
                spans.append(_trim(text, start, bend))
    return spans


def _trim(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return (start, end)


WORD_RE = re.compile(r"[" + LETTERS + r"0-9]+(?:" + APOS + r"[" + LETTERS + r"]+)?(?:[.,:][0-9]+)*")


def words(text):
    return [m.group() for m in WORD_RE.finditer(text)]


def syllables(word):
    n = sum(1 for ch in tr_lower(word) if ch in VOWELS)
    return max(n, 1)


def last_vowel(word):
    for ch in reversed(tr_lower(word)):
        if ch in VOWELS:
            return ch
    return ""


def atesman(text, sents=None):
    ws = [w for w in words(text) if not w[0].isdigit()]
    if not ws:
        return None
    sents = sents or split_sentences(text)
    nsent = max(len(sents), 1)
    syl = sum(syllables(w) for w in ws)
    return 198.825 - 40.175 * (syl / len(ws)) - 2.610 * (len(ws) / nsent)


class LineIndex:
    def __init__(self, text):
        self.starts = [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                self.starts.append(i + 1)

    def pos(self, offset):
        lo, hi = 0, len(self.starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, offset - self.starts[lo] + 1
