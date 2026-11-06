"""Register and tur (genre) profiles, register auto-detection, config loading."""
import json
import os
import re

from . import textutil as tu

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
_cache = {}


def load_json(name):
    if name not in _cache:
        with open(os.path.join(_DATA, name), encoding="utf-8") as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


def registers():
    return load_json("profiles.json")["registers"]


def profiles():
    return load_json("profiles.json")["profiles"]


def profile(tur):
    return profiles().get(tur)


ALIASES = {"eposta": "is-eposta", "e-posta": "is-eposta", "mail": "is-eposta",
           "twitter": "x", "tweet": "x", "abstract": "akademik-ozet", "ozet": "akademik-ozet",
           "makale": "akademik-giris", "dokuman": "teknik-dok", "dokumantasyon": "teknik-dok"}


def canonical_tur(key):
    """Tür id from an id, a P-number (P19), an alias or a register name. None when unknown."""
    if not key:
        return None
    profs = profiles()
    if key in profs:
        return key
    k = tu.tr_lower(key.strip())
    if k in profs:
        return k
    if re.fullmatch(r"p\d{1,2}", k):
        for tid, prof in profs.items():
            if prof.get("p", "").lower() == k:
                return tid
    if k in ALIASES:
        return ALIASES[k]
    reg = registers().get(k)
    if reg and reg.get("default_tur") in profs:
        return reg["default_tur"]
    return None


def unknown_tur(key):
    import difflib
    close = difflib.get_close_matches(key, list(profiles()) + list(ALIASES), n=3, cutoff=0.5)
    msg = "bilinmeyen tür: %s" % key
    if close:
        msg += " (yakın: %s)" % ", ".join(close)
    return ValueError(msg + ". Liste: yontu profiles")


def lookup(key):
    """Profile by tür id, or register data with its türler. None when unknown."""
    profs = profiles()
    regs = registers()
    if key not in profs and key not in regs and canonical_tur(key):
        key = canonical_tur(key)
    if key in profs:
        return dict(profs[key], id=key, register_data=regs.get(profs[key]["register"]))
    if key in regs:
        return dict(regs[key], id=key, turler=[k for k, v in profs.items() if v.get("register") == key])
    return None


def resolve(register=None, tur=None, text="", filename=None):
    """Return (register, tur, how). Flags win, then file context, then content."""
    regs = registers()
    if tur and tur not in profiles():
        canon = canonical_tur(tur)
        if not canon:
            raise unknown_tur(tur)
        tur = canon
    if register and register not in regs:
        raise ValueError("bilinmeyen register: %s" % register)
    if tur and not register:
        return profiles()[tur]["register"], tur, "flag"
    if register:
        return register, tur or regs[register].get("default_tur"), "flag"
    reg, tur2 = detect_from_filename(filename)
    if reg:
        return reg, tur2 or regs[reg].get("default_tur"), "dosya"
    reg, conf = detect_from_content(text)
    return reg, regs[reg].get("default_tur"), "içerik %.2f" % conf


def detect_from_filename(filename):
    if not filename or filename == "-":
        return None, None
    base = os.path.basename(filename)
    up = base.upper()
    if base == "COMMIT_EDITMSG":
        return "commit", "commit"
    if up.startswith("CHANGELOG"):
        return "teknik", "changelog"
    if up.startswith("README"):
        return "teknik", "readme"
    if base.endswith(".po") or base.endswith(".pot"):
        return "ui", None
    if base.endswith(".tex"):
        return "akademik", None
    parts = filename.replace("\\", "/").split("/")
    if base.endswith(".json") and any(p in ("i18n", "locales", "locale", "lang") for p in parts):
        return "ui", None
    return None, None


_HINTS = {
    "resmi": [r"^Sayı\s*:", r"^Konu\s*:", r"^İlgi\s*:", r"arz ederim", r"rica ederim",
              r"Gereğini", r"Makamına", r"\bEk-\d", r"Müdürlüğü"],
    "akademik": [r"^Özet\b", r"Anahtar [Kk]elimeler", r"^Abstract\b",
                 r"[(;] ?[" + tu.UPPER + r"][" + tu.LOWER + r"]+,? \d{4}[;)]",
                 r"Bu (?:çalışmada|araştırmada|makalede)",
                 r"\bbulgular", r"\byöntem", r"örneklem", r"istatistiksel"],
    "haber": [r"^[" + tu.UPPER + r"]{3,} \(\w+\) [-–]", r"\bdedi\b", r"açıkladı\b",
              r"bildirdi\b", r"ifade etti\b", r"kaydetti\b"],
    "kurumsal": [r"Basın Bülteni", r"Editöre Not", r"\bHakkında\b", r"^Sayın\b"],
    "teknik": [r"^```", r"`[^`]+`", r"^#+ Kurulum", r"\bnpm\b", r"\bpip\b", r"(?<!\w)--[a-z]",
               r"\bkomut", r"\bsürüm"],
    "commit": [r"\A(?:feat|fix|docs|chore|refactor|test|perf|ci|build|style)(?:\([^)]+\))?!?: "],
    "pazarlama": [r"!", r"\ben iyi\b", r"\ben ucuz\b", r"%100", r"\d+ ?TL\b", r"\bhemen\b",
                  r"\bkaçırma"],
    "sosyal": [r"(?<!\w)#\w+", r"(?<!\w)@\w+"],
    "is-eposta": [r"^Merhaba\b", r"İyi çalışmalar", r"Saygılarımla", r"Teşekkürler"],
    "sozlu": [r"^Değerli\b", r"^Sevgili\b", r"hepinizi", r"teşekkür ederim\."],
    "edebi": [r"^— ", r"^– "],
    "sohbet": [r"\bistersen\b", r"\byapabilirsin\b", r"\bsöyle(?:yebilirim|r misin)",
               r"\bsen(?:in)?\b"],
}
_COMMIT = re.compile(_HINTS["commit"][0])
_HINTS_RE = {k: [re.compile(p, re.M) for p in v] for k, v in _HINTS.items()}


def detect_from_content(text):
    if not text.strip():
        return "notr", 0.0
    if _COMMIT.match(text) and len(text.split("\n", 1)[0]) <= 100:
        return "commit", 1.0
    scores = {}
    for reg, pats in _HINTS_RE.items():
        n = 0
        for pat in pats:
            n += min(len(pat.findall(text)), 3)
        if n:
            scores[reg] = n
    if not scores:
        return "notr", 0.0
    best = max(scores, key=scores.get)
    total = sum(scores.values())
    conf = scores[best] / total
    if scores[best] < 2 or conf < 0.6:
        return "notr", conf
    return best, conf


def _normalize(cfg):
    """A string "enable" value is a comma-separated list, not a list of characters."""
    if isinstance(cfg, dict) and isinstance(cfg.get("enable"), str):
        cfg = dict(cfg)
        cfg["enable"] = [x.strip() for x in cfg["enable"].split(",") if x.strip()]
    return cfg


def load_config(path=None, start_dir=None):
    """Load .yontu.json. Missing file gives an empty config."""
    if path:
        with open(path, encoding="utf-8") as fh:
            return _normalize(json.load(fh))
    d = os.path.abspath(start_dir or os.getcwd())
    while True:
        cand = os.path.join(d, ".yontu.json")
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8") as fh:
                return _normalize(json.load(fh))
        parent = os.path.dirname(d)
        if parent == d:
            return {}
        d = parent
