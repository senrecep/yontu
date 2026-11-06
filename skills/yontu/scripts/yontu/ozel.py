"""Rules that need code rather than a single regex (rule kind "builtin").

Each function takes (rule, ctx) and yields dicts with start, end and optional
message, suggestion and fix keys.
"""
import math
import re

from . import textutil as tu

# Words whose final l/t/k takes front-vowel suffixes (saate, Kemal'e).
FRONT_EXCEPTIONS = {
    "saat", "hal", "kalp", "rol", "gol", "alkol", "petrol", "sembol", "kontrol",
    "protokol", "meşgul", "mahsul", "usul", "hayal", "ihtimal", "kabul", "dikkat",
    "hakikat", "idrak", "emlak", "helak", "istiklal", "ilmühaber", "seyahat",
    "kemal", "celal", "bilal", "hilal", "meral", "cemal", "nihal", "resul", "rasul",
    "iclal", "ikbal", "sual", "kavil", "infilak", "istikbal", "harf",
    "normal", "ideal", "final", "global", "total", "lokal", "moral", "sosyal",
    "orijinal", "terminal", "festival", "metal",
    "dijital", "kristal", "meçhul", "makul", "mesul", "ihmal", "ithal", "işgal", "intikal",
    "meal", "istimlak", "kanaat", "cemaat", "ziraat", "itaat", "misal", "liberal", "general",
    "radikal", "vokal",
}

# Common English loanwords read by pronunciation, not spelling (server da, online mı).
FOREIGN_WORDS = {
    "server", "online", "offline", "feature", "update", "release", "deploy", "cache", "file",
    "page", "store", "design", "software", "hardware", "frontend", "backend", "framework",
    "pipeline", "update", "merge", "rebase", "commit", "push", "build", "debug", "docker",
    "browser", "router", "cluster", "container", "service", "base", "game", "mode", "site",
    "user", "manager", "provider", "worker", "folder", "token", "prompt", "query",
}

LETTER_READING = {
    "A": "a", "B": "be", "C": "ce", "Ç": "çe", "D": "de", "E": "e", "F": "fe",
    "G": "ge", "Ğ": "ge", "H": "he", "I": "ı", "İ": "i", "J": "je", "K": "ke",
    "L": "le", "M": "me", "N": "ne", "O": "o", "Ö": "ö", "P": "pe", "R": "re",
    "S": "se", "Ş": "şe", "T": "te", "U": "u", "Ü": "ü", "V": "ve", "Y": "ye", "Z": "ze",
}

ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def number_last_word(numtext):
    """Last word of the Turkish reading of a number written with digits."""
    s = numtext.strip()
    if re.match(r"^\d{1,3}(?:\.\d{3})+$", s):
        n = int(s.replace(".", ""))
    else:
        parts = re.split(r"[.,:]", s)
        part = parts[-1]
        if len(parts) == 2 and re.match(r"^\d{1,2}[.:]00$", s) and int(parts[0]) <= 24:
            part = parts[-2]  # 09.00, 13:00 are read as the hour
        elif len(parts) > 1 and part.isdigit() and int(part) == 0:
            return "sıfır"  # 1.0, 2,0: "bir nokta sıfır"
        if not part.isdigit():
            return None
        n = int(part)
    if n == 0:
        return "sıfır"
    for scale, word in ((10 ** 9, "milyar"), (10 ** 6, "milyon"), (10 ** 3, "bin")):
        if n % scale == 0:
            return word
    r = n % 1000
    if r % 100 == 0:
        return "yüz"
    if r % 10 == 0:
        return TENS[(r % 100) // 10]
    return ONES[r % 10]


def base_info(word, front_override=False):
    low = tu.tr_lower(word)
    lv = tu.last_vowel(low)
    if not lv:
        return None
    back = lv in tu.BACK_VOWELS

    if front_override or low in FRONT_EXCEPTIONS:
        back = False
    return {
        "back": back,
        "round": lv in tu.ROUND_VOWELS,
        "vowel_end": low[-1] in tu.VOWELS,
        "voiceless": low[-1] in tu.VOICELESS,
    }


def _v2(info):
    return "a" if info["back"] else "e"


def _v4(info):
    if info["back"]:
        return "u" if info["round"] else "ı"
    return "ü" if info["round"] else "i"


def expected_suffix(info, suffix):
    """Return the correct form of the first suffix morpheme, or None if unknown."""
    s = suffix
    m = re.match(r"^([dt])([ae])(n?)(.*)$", s)
    if m:
        c = "t" if info["voiceless"] else "d"
        return c + _v2(info) + m.group(3) + m.group(4), m.group(1) != c
    m = re.match(r"^([dt])([ıiuü])r(lar|ler)?$", s)
    if m:
        c = "t" if info["voiceless"] else "d"
        return c + _v4(info) + "r" + (m.group(3) or ""), m.group(1) != c
    m = re.match(r"^(y?)([ae])$", s)
    if m:
        y = "y" if info["vowel_end"] else ""
        return y + _v2(info), m.group(1) != y
    m = re.match(r"^(y?)([ıiuü])$", s)
    if m:
        y = "y" if info["vowel_end"] else ""
        return y + _v4(info), m.group(1) != y
    m = re.match(r"^(n?)([ıiuü])n$", s)
    if m:
        n = "n" if info["vowel_end"] else ""
        return n + _v4(info) + "n", m.group(1) != n
    m = re.match(r"^(n?)([ıiuü]?)nc([ıiuü])$", s)
    if m:
        if info["vowel_end"]:
            return "nc" + _v4(info), m.group(2) != ""
        return _v4(info) + "nc" + _v4(info), m.group(2) == ""
    m = re.match(r"^l([ae])r(.*)$", s)
    if m:
        return "l" + _v2(info) + "r" + m.group(2), False
    m = re.match(r"^(y?)l([ae])$", s)  # (y)lA
    if m:
        y = "y" if info["vowel_end"] else ""
        return y + "l" + _v2(info), m.group(1) != y
    m = re.match(r"^l([ıiuü])(k?)$", s)
    if m:
        return "l" + _v4(info) + m.group(2), False
    return None


_NUM_SUFFIX = re.compile(r"(?<![\w.,$€£₺¥~])(\d+(?:[.,:]\d+)*)(['’])([" + tu.LOWER + r"]+)")
_ACRO_SUFFIX = re.compile(r"(?<![\w])([" + tu.UPPER + r"]{2,6})(['’])([" + tu.LOWER + r"]+)")
_NAME_SUFFIX = re.compile(r"(?<![\w'’])([" + tu.UPPER + r"][" + tu.LOWER + r"]+)(['’])([" + tu.LOWER + r"]+)")


# Spellings Turkish does not use, so the name is likely read the foreign way. Final
# clusters such as sk, mp, nd and double consonants do not end Turkish words (Musk'ın).
_FOREIGN = re.compile(r"[wqx]|th|sh|ch|gh|ph|ck|oo|ee|ou|ea|au|eu|y$|([bcdfgkpt])\1le$|[gkpbt]le$"
                      r"|(?:sk|sp|mp|mb|nk|ng|nd|ld|lk|rd|rn)$|([bcdfgklmnprstvz])\2$")
_HARD = set(tu.VOICELESS)
# French names whose spelled final consonant is silent (Renault "reno", Bordeaux "bordo"):
# the suffix follows the spoken vowel, so KS-07 cannot judge it from the spelling.
_SILENT_END = re.compile(r"(?:ault|eaux?|aux|oux|oix|ois|ais|ot)$")
_SILENT_NAMES = {"dumas", "degas", "camus", "debussy"}


def apostrophe_suffix(rule, ctx):
    """Check the suffix after an apostrophe against its base (number, acronym, name)."""
    target = rule.get("target")
    params_word = {k.upper(): v for k, v in (rule.get("word_acronyms") or {}).items()}
    skip = set(rule.get("skip_acronyms") or [])
    pat = {"number": _NUM_SUFFIX, "acronym": _ACRO_SUFFIX, "name": _NAME_SUFFIX}[target]
    for m in pat.finditer(ctx.text):
        base, apo, suf = m.group(1), m.group(2), m.group(3)
        if ctx.masked_near(m.start(), m.end()):
            continue
        if target == "number":
            if base.count(".") >= 2 or re.search(r"[$€£₺¥]\s?$", ctx.text[max(0, m.start() - 2):m.start()]):
                continue  # version 4.17.0, currency $4
            reading = number_last_word(base)
            info = base_info(reading) if reading else None
        elif target == "acronym":
            if base in skip:
                continue
            reading = params_word.get(base)
            if reading is None:
                if rule.get("mode") == "word":
                    continue
                if len(base) >= 4 and re.search("[AEIİOÖUÜ]", base[1:-1]):
                    continue  # probably read as a word (TÜSİAD, ASELSAN)
                last = base[-1]
                if last in "KH" and rule.get("mode") != "kh":
                    continue
                if last not in "KH" and rule.get("mode") == "kh":
                    continue
                reading = LETTER_READING.get(last)
            elif rule.get("mode") != "word":
                continue
            info = base_info(reading) if reading else None
        else:
            low = tu.tr_lower(base)
            if rule.get("check") == "consonant":
                # voicing follows the spelled final consonant (Facebook'ta, Linux'ta);
                # c is read differently across languages, so it is skipped (Mac).
                if suf[0] not in "dt" or low[-1] == "c" or low.endswith("es"):
                    continue
                if _SILENT_END.search(low) or low in _SILENT_NAMES:
                    continue
                want = "t" if (low[-1] in _HARD or low.endswith("ck")) else "d"
                if low[-1] in tu.VOWELS:
                    continue  # silent final e (Claude) hides the spoken consonant
                if suf[0] != want:
                    yield {"start": m.start(), "end": m.end(),
                           "suggestion": base + apo + want + suf[1:], "fix": None}
                continue
            if _FOREIGN.search(low):
                continue
            info = base_info(base)
        if not info:
            continue
        exp = expected_suffix(info, suf)
        if not exp:
            continue
        good, consonant_diff = exp
        if good == suf:
            continue
        if target == "name" and suf[0] in "dt" and good[0] in "dt" and good[0] != suf[0]:
            continue  # voicing is KS-07's job
        yield {"start": m.start(), "end": m.end(),
               "suggestion": base + apo + good,
               "fix": (base + apo + good) if rule.get("fixable") else None}


def title_case_small(rule, ctx):
    small = set(rule.get("small_words"))
    pos = 0
    for line in ctx.text.split("\n"):
        ws = list(re.finditer(r"[" + tu.LETTERS + r"]+", line))
        letters = "".join(w.group() for w in ws)
        stripped = line.strip()
        heading = stripped.startswith("#") or (
            stripped and stripped[-1] not in ".,;:!?…" and len(ws) <= 12)
        if heading and len(ws) >= 3 and letters != tu.tr_upper(letters):
            rest = ws[1:]
            caps = [w for w in rest if tu.is_upper_initial(w.group())]
            if len(caps) >= 0.6 * len(rest):
                for w in rest:
                    if w.group() in small:
                        st = pos + w.start()
                        yield {"start": st, "end": st + len(w.group()),
                               "suggestion": tu.tr_lower(w.group()),
                               "fix": tu.tr_lower(w.group())}
        pos += len(line) + 1


_PARTICLE = re.compile(r"(?<![" + tu.LETTERS + r"0-9'’-])([" + tu.LETTERS + r"]+) (de|da|mı|mi|mu|mü)(?![" + tu.LETTERS + r"0-9'’])")


_PRONOUNS = {"o", "bu", "şu", "ben", "sen", "biz", "siz", "onlar", "bunlar", "şunlar"}


def _sentence_initial(text, pos):
    j = pos - 1
    while j >= 0 and text[j] in " \t\"'“(*_-#|>":
        j -= 1
    return j < 0 or text[j] in ".!?…:\n"


def particle_harmony(rule, ctx):
    kind = rule.get("particle")
    skip = set(rule.get("skip_words") or [])
    for m in _PARTICLE.finditer(ctx.low):
        word, part = m.group(1), m.group(2)
        if (kind == "de") != (part in ("de", "da")):
            continue
        if word in skip or len(word) < 2 or word in FOREIGN_WORDS or _FOREIGN.search(word):
            continue
        orig = ctx.text[m.start(1):m.end(1)]
        if orig.isupper() or (tu.is_upper_initial(orig) and word not in _PRONOUNS
                              and not _sentence_initial(ctx.text, m.start(1))):
            continue
        if ctx.masked_near(m.start(), m.end()):
            continue
        info = base_info(word)
        if not info:
            continue
        good = ("d" + _v2(info)) if kind == "de" else ("m" + _v4(info))
        if good != part:
            yield {"start": m.start(2), "end": m.end(2), "suggestion": good}


def _sent_words(ctx, span):
    return tu.words(ctx.text[span[0]:span[1]])


def _prose_sentences(ctx):
    out = []
    for s, e in ctx.sentences:
        line_start = ctx.text.rfind("\n", 0, s) + 1
        prefix = ctx.text[line_start:s + 4]
        if re.match(r"^\s*(?:#|[-*+•]\s|\d+[.)]\s|\|)", prefix):
            continue
        n = len(_sent_words(ctx, (s, e)))
        if n:
            out.append((s, e, n))
    return out


def _band(ctx, key):
    if ctx.prof.get(key) is not None:
        return ctx.prof.get(key)
    return ctx.reg.get(key)


def sentence_band(rule, ctx):
    band = _band(ctx, "sentence_words")
    sents = _prose_sentences(ctx)
    if not band or len(sents) < rule.get("min_sentences", 5) or ctx.nwords < 50:
        return
    avg = sum(n for _, _, n in sents) / float(len(sents))
    lo, hi = band
    if avg > hi * rule.get("tolerance", 1.15) or avg < lo / rule.get("tolerance", 1.15):
        yield {"start": sents[0][0], "end": min(sents[0][1], sents[0][0] + 60),
               "message": "Ortalama cümle %.1f kelime; bu tür için hedef %d-%d." % (avg, lo, hi)}


def sentence_max(rule, ctx):
    limit = _band(ctx, "sentence_max")
    if not limit:
        return
    sents = _prose_sentences(ctx)
    long_ = [(s, e, n) for s, e, n in sents if n > limit]
    if len(long_) >= rule.get("min", 2):
        s, e, n = long_[0]
        yield {"start": s, "end": min(e, s + 60),
               "message": "%d cümle %d kelimeyi aşıyor (en uzunu %d)." % (
                   len(long_), limit, max(x[2] for x in long_))}


def readability(rule, ctx):
    band = _band(ctx, "atesman")
    if not band or ctx.nwords < rule.get("min_words", 100):
        return
    sents = _prose_sentences(ctx)
    if len(sents) < 3:
        return
    text = " ".join(ctx.text[s:e] for s, e, _ in sents)
    score = tu.atesman(text, [(0, 1)] * len(sents))
    if score is None:
        return
    lo, hi = band
    if score < lo - rule.get("margin", 10) or score > hi + rule.get("margin", 10):
        yield {"start": sents[0][0], "end": min(sents[0][1], sents[0][0] + 60),
               "message": "Ateşman okunabilirlik puanı %.0f; bu tür için bant %d-%d." % (score, lo, hi)}


def commit_title(rule, ctx):
    first = ctx.raw.split("\n", 1)[0]
    if not first.strip() or first.startswith("#"):
        return
    check = rule.get("check")
    n = len(first)
    if check == "length":
        lo, hi = rule.get("limits", [60, 72])
        if (rule.get("level") == "warning" and n > hi) or (rule.get("level") == "info" and lo < n <= hi):
            yield {"start": 0, "end": n, "message": "Commit başlığı %d karakter (sınır %d)." % (
                n, hi if n > hi else lo)}
    elif check == "format":
        if not re.match(r"^(?:feat|fix|docs|chore|refactor|test|perf|ci|build|style|revert)(?:\([^)]+\))?!?: \S", first) \
                and not first.startswith("Merge "):
            yield {"start": 0, "end": n}
    elif check == "period":
        if first.rstrip().endswith("."):
            yield {"start": n - 1, "end": n, "fix": None}


def word_count(rule, ctx):
    words = ctx.prof.get("words") or [None, None]
    lo = rule.get("min_words", words[0])
    hi = rule.get("max_words", words[1])
    n = ctx.nwords
    if (lo and 0 < n < lo) or (hi and n > hi):
        yield {"start": 0, "end": min(len(ctx.text), 40),
               "message": "%s (%d kelime)" % (rule.get("message", ""), n)}


def max_sentences(rule, ctx):
    limit = rule.get("max") or ctx.prof.get("max_sentences")
    if not limit:
        return
    if len(ctx.sentences) > limit:
        s, e = ctx.sentences[limit]
        yield {"start": s, "end": e, "message": "%s (%d cümle)" % (rule.get("message", ""), len(ctx.sentences))}


def line_words(rule, ctx):
    """Short-line registers (buttons, slide bullets): a line longer than max words."""
    limit = rule.get("max") or ctx.prof.get("line_words")
    if not limit:
        return
    pos = 0
    for line in ctx.text.split("\n"):
        body = re.sub(r"^\s*(?:[-*+•]|\d+[.)])\s+", "", line)
        n = len(tu.words(body))
        if n > limit and (not rule.get("bullets_only") or body != line):
            yield {"start": pos, "end": pos + len(line),
                   "message": "%s (%d kelime)" % (rule.get("message", ""), n)}
        pos += len(line) + 1


def burstiness(rule, ctx):
    sents = _prose_sentences(ctx)
    if len(sents) < rule.get("min_sentences", 10):
        return
    lens = [n for _, _, n in sents]
    mean = sum(lens) / float(len(lens))
    var = sum((x - mean) ** 2 for x in lens) / len(lens)
    cv = math.sqrt(var) / mean if mean else 0
    if mean < rule.get("min_mean", 0):
        return
    if cv < rule.get("threshold", 0.25):
        yield {"start": sents[0][0], "end": min(sents[0][1], sents[0][0] + 60),
               "message": "Cümle uzunlukları çok tekdüze (değişkenlik katsayısı %.2f)." % cv}


def mixed_quotes(rule, ctx):
    t = ctx.text
    straight = re.search(r"\"[^\"\n]+\"", t)
    curly = re.search(r"“[^”\n]+”", t)
    apo_s = re.search(r"[" + tu.LETTERS + r"0-9]'[" + tu.LOWER + r"]", t)
    apo_c = re.search(r"[" + tu.LETTERS + r"0-9]’[" + tu.LOWER + r"]", t)
    hit = None
    if straight and curly:
        hit = curly
    elif apo_s and apo_c:
        hit = apo_c
    if hit:
        yield {"start": hit.start(), "end": hit.end()}


def paragraph_initial(rule, ctx):
    words = rule.get("words")
    pat = re.compile(r"^\s*(?:" + "|".join(words) + r")\b")
    paras = [p for p in ctx.paragraphs if not re.match(r"\s*(?:#|[-*+•]\s|\d+[.)]\s|```)", ctx.text[p[0]:p[1]])]
    if len(paras) < rule.get("min_paragraphs", 3):
        return
    hits = [p for p in paras if pat.match(ctx.low[p[0]:p[1]])]
    if len(hits) / float(len(paras)) > rule.get("threshold", 0.5):
        s = hits[0][0]
        yield {"start": s, "end": min(hits[0][1], s + 30),
               "message": "%s (%d/%d paragraf)" % (rule.get("message", ""), len(hits), len(paras))}


_SING = re.compile(r"(?<![" + tu.LETTERS + r"])(?:sen|seni|sana|senin|sende|senden|seninle)(?![" + tu.LETTERS + r"])"
                   r"|[" + tu.LOWER + r"]+(?:r|yor|cak|cek|malı|meli|mış|miş|muş|müş)(?:sın|sin|sun|sün)(?=[.!?])")
_PLUR = re.compile(r"(?<![" + tu.LETTERS + r"])(?:siz|sizi|size|sizin|sizde|sizden|sizinle)(?![" + tu.LETTERS + r"])"
                   r"|[" + tu.LOWER + r"]{2,}(?:sınız|siniz|sunuz|sünüz|nız|niz|nuz|nüz)(?=[.!?])")


def sen_siz(rule, ctx):
    src = ctx.noquote_low
    a = list(_SING.finditer(src))
    b = list(_PLUR.finditer(src))
    if a and b:
        minority = a if len(a) <= len(b) else b
        m = minority[0]
        yield {"start": m.start(), "end": m.end()}


def _outside_fences(ctx):
    """ctx.raw with fenced code blanked (inline code stays visible)."""
    return tu.apply_mask(ctx.raw, tu.code_mask(ctx.raw, inline=False))


def code_apostrophe(rule, ctx):
    for m in re.finditer(r"`[^`\n]+`['’][" + tu.LOWER + r"]+", _outside_fences(ctx)):
        yield {"start": m.start(), "end": m.end()}


_EMOJI = re.compile("(?:[\U0001F300-\U0001FAFF☀-➿⭐✅❌]|\\d\uFE0F?\u20E3)")


# Emoji used as a field label (📍 place, 🕗 time, 🎟️ ticket, 📞 phone) or a priced menu line:
# the post's form, not a decorative bullet.
_LABEL_EMOJI = re.compile("^\\s*(?:[-*+]\\s*)?(?:[\U0001F4CD\U0001F4CC\U0001F4C5\U0001F4C6\U0001F5D3"
                          "\U0001F550-\U0001F567⏰⌚\U0001F39F\U0001F3AB\U0001F4DE☎"
                          "\U0001F4E7✉\U0001F310\U0001F517\U0001F4B0\U0001F4B3\U0001F3F7])")
_PRICE_TIME = re.compile(r"\d+(?:[.,]\d+)?\s*(?:TL|₺)|(?<!\d)\d{1,2}[.:]\d{2}(?!\d)")


def _label_line(line):
    # a priced or timed line counts only when short (🍕 Margarita 180 TL), not a selling point
    return bool(_LABEL_EMOJI.match(line)
                or (_PRICE_TIME.search(line) and len(line.split()) <= 6))


def multiword_term(text, start, end):
    """Capitalized word after an apostrophe-bearing match that belongs to a multiword or
    foreign term (Pull Request'ler, GitHub Action'lar), not a lone Turkish proper name."""
    stem = re.match(r"[\w]+", text[start:end]).group(0)
    if _FOREIGN.search(tu.tr_lower(stem)):
        return True  # English spelling: Request'ler, Workflow'lar
    m = re.search(r"([" + tu.UPPER + r"][\w]*)[ \t]+$", text[:start])
    if not m:
        return False
    if re.search(r"[" + tu.UPPER + r"]", m.group(1)[1:]):
        return True  # inner capital: GitHub Action'lar
    return not _sentence_initial(text, m.start(1))  # Pull Request'ler mid-sentence


def emoji_lines(rule, ctx):
    mode = rule.get("mode", "line_start")
    raw = _outside_fences(ctx)
    lines = [l for l in raw.split("\n") if l.strip()]
    if rule.get("skip_labels"):
        lines = ["\u00b7" if _label_line(l) else l for l in lines]  # counts as a plain line
    if not lines:
        return
    if mode == "heading":
        hits = [l for l in lines if l.lstrip().startswith("#") and _EMOJI.search(l)]
        hits += [l for l in lines if re.match(r"^\s*[-*+]\s*" + _EMOJI.pattern, l)]
        need = rule.get("min", 3)
        ok = len(hits) >= need
    elif mode == "list":
        # Longest run of consecutive lines that use an emoji as the bullet ("✅ ...", "- 1️⃣ ...").
        run, best = [], []
        for l in lines:
            if re.match(r"^\s*(?:[-*+]\s*)?" + _EMOJI.pattern, l):
                run.append(l)
                if len(run) > len(best):
                    best = list(run)
            else:
                run = []
        hits = best
        ok = len(hits) >= rule.get("min", 3)
    else:
        hits = [l for l in lines if _EMOJI.match(l.lstrip())]
        ok = len(lines) >= 3 and len(hits) / float(len(lines)) > rule.get("threshold", 0.3)
    if ok:
        off = raw.find(hits[0])
        yield {"start": off, "end": off + len(hits[0]),
               "message": "%s (%d satır)" % (rule.get("message", ""), len(hits))}


def short_sentence_share(rule, ctx):
    sents = _prose_sentences(ctx)
    if len(sents) < rule.get("min_sentences", 5):
        return
    short = [x for x in sents if x[2] <= rule.get("max_words", 3)]
    share = len(short) / float(len(sents))
    if share > rule.get("threshold", 0.2):
        s, e, _ = short[0]
        yield {"start": s, "end": e,
               "message": "%s (%%%d)" % (rule.get("message", ""), round(share * 100))}


def qa_pairs(rule, ctx):
    hits = []
    sents = ctx.sentences
    for i in range(len(sents) - 1):
        s, e = sents[i]
        if ctx.noquote[s:e].rstrip().endswith("?"):
            ns, ne = sents[i + 1]
            same_para = "\n\n" not in ctx.text[e:ns]
            if same_para and len(tu.words(ctx.text[ns:ne])) <= rule.get("answer_words", 8):
                hits.append((s, ne))
    need = max(rule.get("min", 2), int(math.ceil(rule.get("per300", 2) * ctx.nwords / 300.0)))
    if len(hits) >= need:
        yield {"start": hits[0][0], "end": hits[0][1],
               "message": "%s (%d çift)" % (rule.get("message", ""), len(hits))}


def synonym_rotation(rule, ctx):
    for cluster in rule.get("clusters"):
        found = []
        for w in cluster:
            m = re.search(r"(?<![" + tu.LETTERS + r"])" + w + r"[" + tu.LOWER + r"]*", ctx.low)
            if m:
                found.append(m)
        if len(found) >= rule.get("min", 3):
            m = sorted(found, key=lambda x: x.start())[0]
            yield {"start": m.start(), "end": m.end(),
                   "message": "%s (%s)" % (rule.get("message", ""), ", ".join(x.group() for x in found))}


def first_sentence(rule, ctx):
    """Pattern that matters only in the first prose sentence of the text."""
    sents = _prose_sentences(ctx)
    if not sents:
        return
    s, e, _ = sents[0]
    pat = re.compile(tu.expand(rule.get("first_pattern")))
    m = pat.search(ctx.low, s, e)
    if m:
        yield {"start": m.start(), "end": m.end()}
