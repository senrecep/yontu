"""Text statistics: sentence length, readability and a few density figures."""
import re

from . import profiller
from . import textutil as tu

_DENSITY = {
    "maktadir": r"[%L]+m[ae]kt[ae](?:d[ıi]r|l[ae]r)[%L]*",
    "arak": r"[%L]{2,}y?[ae]r[ae]k%E",
    "bir_sekilde": r"%Bbir\s+(?:şekilde|biçimde)%E",
    "noktali_virgul": r";",
    "uzun_cizgi": r"—",
}


def _mean(xs):
    return sum(xs) / float(len(xs)) if xs else 0.0


def _stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def stats(text, register=None, tur=None, filename=None):
    """Return a dict of figures for text, with the band of the resolved profile."""
    raw = tu.nfc(text).replace("\r\n", "\n")
    reg, tur, how = profiller.resolve(register, tur, raw, filename)
    masked = tu.apply_mask(raw, tu.build_mask(raw))
    low = tu.tr_lower(masked)
    sents = tu.split_sentences(masked)
    lens = [len(tu.words(masked[s:e])) for s, e in sents]
    lens = [n for n in lens if n]
    nwords = len(tu.words(masked))
    ates = tu.atesman(masked, sents)
    regd = profiller.registers().get(reg, {})
    prof = profiller.profiles().get(tur, {}) if tur else {}
    out = {
        "register": reg,
        "tur": tur,
        "detected_by": how,
        "words": nwords,
        "sentences": len(lens),
        "paragraphs": len(tu.split_paragraphs(masked)),
        "sentence_mean": round(_mean(lens), 1),
        "sentence_stdev": round(_stdev(lens), 1),
        "sentence_max": max(lens) if lens else 0,
        "atesman": round(ates, 1) if ates is not None else None,
        "per300": {},
        "band": {
            "sentence_words": prof.get("sentence_words") or regd.get("sentence_words"),
            "sentence_max": prof.get("sentence_max") or regd.get("sentence_max"),
            "atesman": prof.get("atesman") or regd.get("atesman"),
        },
    }
    limit = out["band"]["sentence_max"]
    out["long_sentences"] = sum(1 for n in lens if limit and n > limit)
    for key, pat in _DENSITY.items():
        n = len(re.findall(tu.expand(pat), low, re.M))
        out["per300"][key] = round(n * 300.0 / nwords, 2) if nwords else 0.0
    return out
