"""Rule runner: masking, rule execution, level resolution, dedup, disables."""
import math
import re

from . import textutil as tu
from . import profiller
from . import ozel as bi

LEVELS = {"info": 1, "warning": 2, "error": 3}
LEVEL_NAMES = {1: "info", 2: "warning", 3: "error"}
EVIDENCE_CAP = {"hipotez": 1, "hakem": 2, "veri": 2, "kaynak": 3}
LAYERS = ("tdk", "ai-iz", "stil", "yogunluk")

_rules_cache = None
_whitelist_cache = None


_names_alt = None


def _pattern(p):
    """tu.expand plus %N, the proper-name list in data/ozel_adlar.json."""
    global _names_alt
    if "%N" in p:
        if _names_alt is None:
            data = profiller.load_json("ozel_adlar.json")
            names = sorted(set(data["yer"]) | set(data["kisi"]), key=lambda x: (-len(x), x))
            _names_alt = "(?:" + "|".join(re.escape(n) for n in names) + ")"
        p = p.replace("%N", _names_alt)
    return tu.expand(p)


class Rule(object):
    def __init__(self, d):
        self.d = d
        self.id = d["id"]
        self.layer = d["layer"]
        self.kind = d.get("kind", "regex")
        self.level = d.get("level", "info")
        self.evidence = d.get("evidence", "hakem")
        self.prec = d.get("prec", 0 if self.layer == "tdk" else 1)
        self.case = d.get("case", "lower")
        self.default_on = d.get("default", "on") == "on"
        self.scope = d.get("scope", "span" if self.kind in ("regex", "map") else "doc")
        self.regex = None
        if self.kind == "map":
            words = sorted(d["map"], key=len, reverse=True)
            alt = "|".join(re.escape(w) for w in words)
            tail = "([%L]*)" if d.get("suffix") else "()"
            self.regex = re.compile(tu.expand("%B(" + alt + ")" + tail + "%E"), re.M)
        elif "pattern" in d:
            self.regex = re.compile(_pattern(d["pattern"]), re.M)
        self.excl = re.compile(_pattern(d["exclude"]), re.M) if d.get("exclude") else None
        self.sent_pattern = None
        if d.get("sentence_pattern"):
            self.sent_pattern = re.compile(tu.expand(d["sentence_pattern"]))

    def get(self, key, default=None):
        return self.d.get(key, default)


def all_rules():
    global _rules_cache
    if _rules_cache is None:
        rules = []
        for name in ("rules_tdk.json", "rules_ai.json", "lexicon.json"):
            for d in profiller.load_json(name)["rules"]:
                rules.append(Rule(d))
        _rules_cache = rules
    return _rules_cache


def whitelist():
    """Compiled whitelist patterns by register ("*" applies everywhere)."""
    global _whitelist_cache
    if _whitelist_cache is None:
        raw = profiller.load_json("lexicon.json").get("whitelist", {})
        _whitelist_cache = {k: [re.compile(tu.expand(p), re.M) for p in v] for k, v in raw.items()}
    return _whitelist_cache


def rule_by_id(rid):
    for r in all_rules():
        if r.id == rid:
            return r
    return None


def rule_data(rid):
    """Rule definition by id, case-insensitive. None when unknown."""
    key = (rid or "").strip().lower()
    for r in all_rules():
        if r.id.lower() == key:
            return r.d
    return None


def check_config(cfg):
    """Raise ValueError for unknown rule ids, tags, families, layers or levels in a config."""
    rules = all_rules()
    ids = set(r.id for r in rules)
    tags = set(t for r in rules for t in (r.get("tags") or []))
    keys = ids | set("family:" + str(r.get("family")) for r in rules) | set("layer:" + l for l in LAYERS)
    enable = cfg.get("enable") or []
    if not isinstance(enable, list) or not all(isinstance(x, str) for x in enable):
        raise ValueError("ayar dosyasında \"enable\" bir metin listesi olmalı")
    bad = [x for x in enable if x not in ids and x not in tags]
    table = cfg.get("rules") or {}
    if not isinstance(table, dict):
        raise ValueError("ayar dosyasında \"rules\" bir nesne olmalı")
    bad += [k for k in table if k not in keys]
    values = ("off", "on", "info", "warning", "error")
    bad += ["%s=%s" % (k, v) for k, v in table.items() if k in keys and v not in values]
    if bad:
        raise ValueError("bilinmeyen kural, etiket ya da düzey: %s" % ", ".join(bad))


# --- level resolution --------------------------------------------------------

def _cap(rule):
    cap = EVIDENCE_CAP.get(rule.evidence, 2)
    if rule.layer != "tdk":
        cap = min(cap, 2)
    if rule.layer == "yogunluk":
        cap = 1
    return cap


def _override(value, rule, current, allow_off):
    """Apply one override value. Returns new level int, 0 for off, None to keep."""
    if value is None:
        return current
    if value == "off":
        return 0 if allow_off else current
    if value == "on":
        return current if current else LEVELS.get(rule.level, 1)
    return LEVELS.get(value, current)


def _lookup(table, rule):
    if not table:
        return None
    for key in (rule.id, "family:" + str(rule.get("family")), "layer:" + rule.layer):
        if key in table:
            return table[key]
    return None


def _enabled(rule, config):
    keys = set((config or {}).get("enable") or [])
    if not keys:
        return False
    tags = set(rule.get("tags") or [])
    return rule.id in keys or bool(tags & keys)


def resolve_level(rule, reg, tur, config):
    """Return level int (0 = off). Order: default, register, tur, config, cap."""
    on = rule.default_on or _enabled(rule, config)
    level = LEVELS.get(rule.level, 1) if on else 0
    regs = profiller.registers()
    rdata = regs.get(reg, {})
    tdata = profiller.profiles().get(tur, {}) if tur else {}
    allowed = rule.get("registers")
    if allowed and reg not in allowed:
        level = 0
    if reg in rule.get("registers_off", []):
        level = 0
    turs = rule.get("turs")
    if turs and tur not in turs:
        level = 0
    if turs and tur in turs and rule.get("default") == "tur":
        level = LEVELS.get(rule.level, 1)
    tdk = rule.layer == "tdk"
    if not tdk and rule.layer in rdata.get("layers_off", []):
        level = 0
    level = _override(_lookup(rdata.get("rules"), rule), rule, level, not tdk)
    level = _override(_lookup(tdata.get("rules"), rule), rule, level, not tdk)
    level = _override(_lookup((config or {}).get("rules"), rule), rule, level, True)
    if level and rdata.get("ai_info") and rule.layer in ("ai-iz", "stil"):
        level = 1
    if level:
        level = min(level, _cap(rule))
    return level


# --- running -----------------------------------------------------------------

class Context(object):
    def __init__(self, text, register, tur, config):
        self.raw = tu.nfc(text)
        self.mask = tu.build_mask(self.raw)
        self.text = tu.apply_mask(self.raw, self.mask)
        self.low = tu.tr_lower(self.text)
        assert len(self.low) == len(self.text)
        qmask = tu.quote_mask(self.text)
        self.noquote = tu.apply_mask(self.text, qmask)
        self.noquote_low = tu.tr_lower(self.noquote)
        self.register = register
        self.tur = tur
        self.config = config or {}
        self.sentences = tu.split_sentences(self.text)
        self.paragraphs = tu.split_paragraphs(self.text)
        self.words = tu.words(self.text)
        self.nwords = len(self.words)
        reg = profiller.registers().get(register, {})
        self.reg = reg
        self.prof = profiller.profiles().get(tur, {}) if tur else {}
        self.mult = reg.get("multiplier", 1.0)
        self.absolute_only = reg.get("absolute_only", False)

    def masked_near(self, start, end):
        lo = max(start - 1, 0)
        hi = min(end + 1, len(self.mask))
        return any(self.mask[lo:hi])

    def need(self, rule):
        per300 = rule.get("per300")
        minimum = rule.get("min", 2)
        short = self.reg.get("short_gate", False)
        if per300 is None or self.absolute_only or (short and self.nwords < 50):
            return minimum
        mult = self.mult if rule.get("scaled") else 1.0
        fam = rule.get("family")
        if fam and isinstance(self.reg.get("family_mult"), dict):
            mult = self.reg["family_mult"].get(fam, mult)
        need = max(minimum, int(math.ceil(per300 * mult * max(self.nwords, 1) / 300.0)))
        if short and self.nwords < 150:
            need = max(2, need)
        return need


def _source_text(ctx, rule):
    if rule.get("skip_quotes"):
        return ctx.noquote if rule.case == "exact" else ctx.noquote_low
    return ctx.text if rule.case == "exact" else ctx.low


def _render(template, m, raw=None):
    """Fill $n from the match. With raw, groups are cut from the original text so a
    rule run on lowered text keeps the writer's capitals (Güzelmi -> Güzel mi)."""
    if template is None:
        return None
    if raw is None:
        try:
            return m.expand(template.replace("$", "\\"))
        except (re.error, IndexError):
            return template

    def group(x):
        g = int(x.group(1))
        if g > (m.re.groups or 0) or m.start(g) < 0:
            return ""
        return raw[m.start(g):m.end(g)]
    return re.sub(r"\$(\d)", group, template)


def _keep_case(orig, repl):
    if repl and orig and tu.is_upper_initial(orig) and not tu.is_upper_initial(repl):
        if orig.isupper() and len(orig) > 1:
            return tu.tr_upper(repl)
        return tu.tr_capitalize(repl)
    return repl


def _make(rule, ctx, start, end, **kw):
    f = {
        "id": rule.id, "layer": rule.layer, "start": start, "end": end,
        "match": ctx.raw[start:end], "message": rule.get("message", ""),
        "suggestion": rule.get("suggestion"), "fix": None,
        "evidence": rule.evidence, "source": rule.get("source"),
        "family": rule.get("family"), "prec": rule.prec, "scope": rule.scope,
    }
    f.update(kw)
    return f


def _run_regex(rule, ctx):
    out = []
    src = _source_text(ctx, rule)
    grp = rule.get("group", 0)
    for m in rule.regex.finditer(src):
        start, end = m.span(grp)
        if start == end or ctx.masked_near(start, end):
            continue
        if rule.excl is not None:
            ws = max(0, start - 80)
            if any(a < end and start < b for a, b in
                   (x.span() for x in rule.excl.finditer(src, ws, min(len(src), end + 160)))):
                continue
        if (ctx.register in (rule.get("para_start_registers") or ())
                and start > 0 and src[start - 1] != "\n"):
            continue  # this register uses it mid-paragraph; only a line-opening one counts
        if rule.get("skip_sentence_initial") and bi._sentence_initial(ctx.text, start):
            continue  # capitalized at sentence start: may be a common noun (Banner'lar)
        orig = ctx.raw[start:end]
        raw = ctx.raw if rule.case != "exact" else None
        sugg = _render(rule.get("suggestion"), m, raw) if rule.get("suggestion") else None
        fix = None
        tdk = rule.layer == "tdk"
        if tdk and rule.get("fix") is not None and rule.get("fixable", True):
            fix = _keep_case(orig, _render(rule.get("fix"), m, raw))
        if rule.get("transform") == "capitalize":
            sugg = tu.tr_capitalize(orig)
            if tdk and rule.get("fixable", True):
                fix = sugg
        if rule.kind == "map":
            key = m.group(1)
            right = rule.get("map")[key]
            suffix = m.group(2)
            repl = _keep_case(orig, right + suffix)
            sugg = repl
            if suffix and rule.get("fix_bare_only"):
                stem = _keep_case(orig, right)
                sugg = "%s (ekin uyumunu yeniden kurun)" % stem
            elif tdk and rule.get("fixable", True):
                fix = repl
        f = _make(rule, ctx, start, end, suggestion=sugg, fix=fix)
        if rule.get("multiword_cap") and bi.multiword_term(ctx.text, start, end):
            # Pull Request'ler, GitHub Action'lar: a capitalized term, not a lone proper name
            f.update(level_cap=rule.get("multiword_cap"), suggestion=None, fix=None)
        out.append(f)
    return out


def _groups(ctx, per):
    if per == "paragraph":
        return ctx.paragraphs
    if per == "sentence":
        return ctx.sentences
    return [(0, len(ctx.text))]


def _run_count(rule, ctx):
    """count/density: aggregate matches, emit one finding at the first match."""
    out = []
    src = _source_text(ctx, rule)
    per = rule.get("per", "doc")
    if rule.kind == "density" and ctx.nwords < 1:
        return out
    for gs, ge in _groups(ctx, per):
        hits = [m for m in rule.regex.finditer(src, gs, ge)
                if not ctx.masked_near(m.start(), m.end())]
        if rule.get("distinct"):
            seen, uniq = set(), []
            for m in hits:
                key = m.group(rule.get("distinct_group", 0))
                if key not in seen:
                    seen.add(key)
                    uniq.append(m)
            hits = uniq
        if rule.get("same"):
            byk = {}
            for m in hits:
                byk.setdefault(m.group(rule.get("same_group", 0)), []).append(m)
            hits = max(byk.values(), key=len) if byk else []
        need = ctx.need(rule) if rule.kind == "density" else rule.get("min", 2)
        if len(hits) >= need:
            m0 = hits[0]
            msg = "%s (%d kez, eşik %d)" % (rule.get("message", ""), len(hits), need)
            out.append(_make(rule, ctx, m0.start(), m0.end(), message=msg,
                             suggestion=rule.get("suggestion"), count=len(hits)))
    return out


def _sentence_text(ctx, span):
    s, e = span
    return ctx.text[s:e]


def _run_ratio(rule, ctx):
    sents = ctx.sentences
    if ctx.absolute_only:
        return []
    if len(sents) < rule.get("min_sentences", 5) or ctx.nwords < 50:
        return []
    pat = rule.sent_pattern
    hits = []
    for s, e in sents:
        body = tu.tr_lower(ctx.text[s:e]).rstrip(" .!?…\"'”’)")
        if not tu.words(body):
            continue
        ok = bool(pat.search(body))
        if ok != bool(rule.get("invert")):
            hits.append((s, e))
    share = len(hits) / float(len(sents))
    if share >= rule.get("threshold", 0.4) and hits:
        s, e = hits[0]
        msg = "%s (%%%d cümle, eşik %%%d)" % (rule.get("message", ""), round(share * 100),
                                              round(rule.get("threshold", 0.4) * 100))
        return [_make(rule, ctx, s, min(e, s + 80), message=msg)]
    return []


def _run_rule(rule, ctx):
    if rule.kind in ("regex", "map"):
        return _run_regex(rule, ctx)
    if rule.kind in ("count", "density"):
        return _run_count(rule, ctx)
    if rule.kind == "ratio":
        return _run_ratio(rule, ctx)
    if rule.kind == "builtin":
        fn = getattr(bi, rule.get("builtin"))
        res = []
        for item in fn(rule, ctx):
            start, end = item.pop("start"), item.pop("end")
            res.append(_make(rule, ctx, start, end, **item))
        return res
    raise ValueError("bilinmeyen kural türü: %s" % rule.kind)


def _dedup(findings):
    span = [f for f in findings if f["scope"] == "span"]
    other = [f for f in findings if f["scope"] != "span"]
    span.sort(key=lambda f: (f["prec"], -(f["end"] - f["start"]), f["start"]))
    kept = []
    for f in span:
        # a lower-level finding never hides a higher-level one (DZ-02 info vs AI-E6)
        if any(f["start"] < k["end"] and k["start"] < f["end"]
               and LEVELS.get(k.get("level"), 3) >= LEVELS.get(f.get("level"), 3) for k in kept):
            continue
        kept.append(f)
    return kept + other


def _whitelisted(findings, ctx):
    """Drop non-tdk span findings that fall inside a whitelisted phrase."""
    pats = list(whitelist().get("*", [])) + list(whitelist().get(ctx.register, []))
    if not pats:
        return findings
    spans = [m.span() for p in pats for m in p.finditer(ctx.low)]
    if not spans:
        return findings
    out = []
    for f in findings:
        if f["layer"] != "tdk" and f["scope"] == "span" and any(
                a <= f["start"] and f["end"] <= b for a, b in spans):
            continue
        out.append(f)
    return out


_DIRECTIVE = re.compile(r"<!--\s*(?:yontu|trlint)-(disable-next-line|disable|enable)\b([^>]*?)-->")


def _directives(raw):
    """Return (blocks, nextline) where blocks is a list of (start_line, end_line, ids).

    Directives shown inside fenced or inline code are examples, not directives.
    """
    idx = tu.LineIndex(raw)
    code = tu.code_spans(raw)
    blocks, nextline, open_ = [], {}, {}
    for m in _DIRECTIVE.finditer(raw):
        if any(a <= m.start() < b for a, b in code):
            continue
        kind = m.group(1)
        ids = frozenset(x for x in re.split(r"[\s,]+", m.group(2).strip()) if x) or frozenset(["*"])
        line, _ = idx.pos(m.start())
        if kind == "disable-next-line":
            nextline.setdefault(line + 1, set()).update(ids)
        elif kind == "disable":
            for i in ids:
                open_.setdefault(i, line)
        else:
            for i in ids:
                keys = list(open_) if i == "*" else [i]
                for k in keys:
                    if k in open_:
                        blocks.append((open_.pop(k), line, k))
    for k, start in open_.items():
        blocks.append((start, 10 ** 9, k))
    return blocks, nextline


def _disabled(f, blocks, nextline):
    line = f["line"]
    ids = nextline.get(line, ())
    if "*" in ids or f["id"] in ids:
        return True
    for s, e, k in blocks:
        if s <= line <= e and (k == "*" or k == f["id"]):
            return True
    return False


def lint(text, register=None, tur=None, config=None, filename=None, layers=None,
         min_level="info"):
    """Lint text. Returns a dict with register, tur, words and findings."""
    config = config or {}
    register = register or config.get("register")
    tur = tur or config.get("tur")
    text = tu.nfc(text)
    crs = None
    if "\r" in text:  # work on LF text, report offsets in the original
        crs = [i for i, ch in enumerate(text) if ch == "\r" and text[i + 1:i + 2] == "\n"]
        text = text.replace("\r\n", "\n")
    reg, tur, how = profiller.resolve(register, tur, text, filename)
    ctx = Context(text, reg, tur, config)
    findings = []
    for rule in all_rules():
        if layers and rule.layer not in layers:
            continue
        lvl = resolve_level(rule, reg, tur, config)
        if not lvl:
            continue
        for f in _run_rule(rule, ctx):
            cap = LEVELS.get(f.pop("level_cap", None), lvl)
            f["level"] = LEVEL_NAMES[min(lvl, cap)]
            findings.append(f)
    findings = _whitelisted(_dedup(findings), ctx)
    idx = tu.LineIndex(ctx.raw)
    blocks, nextline = _directives(ctx.raw)
    out = []
    floor = LEVELS.get(min_level, 1)
    for f in findings:
        f["line"], f["col"] = idx.pos(f["start"])
        if _disabled(f, blocks, nextline):
            continue
        if LEVELS[f["level"]] < floor:
            continue
        out.append(f)
    # a rule that yields_to another drops when that one is reported too (ST-13 under AI-C13E)
    fired = set(f["id"] for f in out)
    yields = dict((r.id, r.get("yields_to")) for r in all_rules() if r.get("yields_to"))
    out = [f for f in out if not fired.intersection(yields.get(f["id"]) or ())]
    out.sort(key=lambda f: (f["start"], f["id"]))
    for f in out:
        f.pop("prec", None)
        f.pop("scope", None)
        if crs:
            f["start"] = _orig_offset(f["start"], crs)
            f["end"] = _orig_offset(f["end"], crs)
    return {"register": reg, "tur": tur, "detected_by": how, "words": ctx.nwords,
            "sentences": len(ctx.sentences), "findings": out}


def _orig_offset(pos, crs):
    """Map an offset in CRLF-normalized text back to the original text."""
    n = 0
    for k, i in enumerate(crs):
        if i - k < pos:
            n += 1
        else:
            break
    return pos + n


def fix(text, register=None, tur=None, config=None):
    """Apply safe tdk autofixes until stable. Returns the fixed text."""
    text = tu.nfc(text)
    if "\r\n" in text:
        return fix(text.replace("\r\n", "\n"), register, tur, config).replace("\n", "\r\n")
    for _ in range(5):
        res = lint(text, register, tur, config, layers=("tdk",))
        edits = [f for f in res["findings"] if f.get("fix") is not None]
        if not edits:
            break
        edits.sort(key=lambda f: f["start"], reverse=True)
        last = len(text) + 1
        changed = False
        for f in edits:
            if f["end"] > last:
                continue
            if text[f["start"]:f["end"]] != f["fix"]:
                text = text[:f["start"]] + f["fix"] + text[f["end"]:]
                changed = True
            last = f["start"]
        if not changed:
            break
    return text
