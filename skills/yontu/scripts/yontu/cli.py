"""Command line: yontu (alias trlint).

Subcommands: lint, compare, stats, rules, explain, profiles, mcp, hook.

Exit codes: 0 no error-level finding, 1 at least one error-level finding,
2 usage, file or config error.
"""
import argparse
import io
import json
import os
import sys

from . import __version__
from . import engine
from . import fidelity
from . import metrics
from . import profiller
from . import textutil as tu

LEVEL_TR = {"error": "hata", "warning": "uyarı", "info": "bilgi"}


class UsageError(Exception):
    pass


def _read(path):
    if path == "-":
        data = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read()
        return data.decode("utf-8") if isinstance(data, bytes) else data
    try:
        with io.open(path, encoding="utf-8", newline="") as fh:
            return fh.read()
    except (IOError, OSError) as exc:
        raise UsageError("dosya okunamadı: %s (%s)" % (path, exc.strerror or exc))
    except UnicodeDecodeError:
        raise UsageError("dosya UTF-8 değil: %s" % path)


def _dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1)


def _config(args, path):
    try:
        start = os.path.dirname(os.path.abspath(path)) if path and path != "-" else None
        cfg = profiller.load_config(args.config, start)
    except (IOError, OSError) as exc:
        raise UsageError("ayar dosyası okunamadı: %s" % exc)
    except ValueError as exc:
        raise UsageError("ayar dosyası geçersiz JSON: %s" % exc)
    if not isinstance(cfg, dict):
        raise UsageError("ayar dosyası bir JSON nesnesi olmalı")
    cfg = dict(cfg)
    if not isinstance(cfg.get("enable") or [], list):
        raise UsageError("ayar dosyasında \"enable\" bir metin listesi olmalı")
    enable = list(cfg.get("enable") or [])
    for item in args.enable or []:
        enable.extend(x for x in item.split(",") if x)
    cfg["enable"] = enable
    _check_keys(cfg)
    return cfg


def _check_keys(cfg):
    """Reject unknown rule ids, tags, families and layers so a typo does not pass silently."""
    try:
        engine.check_config(cfg)
    except ValueError as exc:
        raise UsageError(str(exc))


def _layers(value):
    if not value:
        return None
    out = []
    for item in value:
        for x in item.split(","):
            x = x.strip()
            if x not in engine.LAYERS:
                raise UsageError("bilinmeyen katman: %s (%s)" % (x, ", ".join(engine.LAYERS)))
            out.append(x)
    return tuple(out)


def _finding_line(name, f):
    lvl = LEVEL_TR.get(f["level"], f["level"])
    line = "%s:%d:%d: %s %s [%s] %s" % (name, f["line"], f["col"], lvl, f["id"], f["layer"], f["message"])
    if f.get("match") and f.get("scope") != "doc" and len(f["match"]) <= 60:
        line += " «%s»" % f["match"].replace("\n", " ")
    hint = f.get("fix") if f.get("fix") is not None else f.get("suggestion")
    if hint:
        line += " → %s" % hint
    return line


def _summary(findings):
    c = {"error": 0, "warning": 0, "info": 0}
    for f in findings:
        c[f["level"]] = c.get(f["level"], 0) + 1
    return c


def cmd_lint(args):
    text = _read(args.file)
    cfg = _config(args, args.file)
    layers = _layers(args.layer)
    name = "<stdin>" if args.file == "-" else args.file
    if args.write and not args.fix:
        raise UsageError("--write yalnız --fix ile kullanılır")
    if args.fix:
        if args.write and args.file == "-":
            raise UsageError("--write standart girdiyle kullanılamaz")
        fixed = engine.fix(text, args.register, args.tur, cfg)
        if args.write:
            if fixed != tu.nfc(text):
                with io.open(args.file, "w", encoding="utf-8", newline="") as fh:
                    fh.write(fixed)
            res = engine.lint(fixed, args.register, args.tur, cfg, filename=name, layers=("tdk",))
            left = _summary(res["findings"])["error"]
            sys.stderr.write("%s: düzeltildi, kalan tdk hatası %d\n" % (name, left))
            return 1 if left else 0
        sys.stdout.write(fixed)
        return 0
    res = engine.lint(text, args.register, args.tur, cfg, filename=name, layers=layers,
                      min_level=args.min_level)
    counts = _summary(res["findings"])
    if args.format == "json":
        out = dict(res)
        out["file"] = name
        out["counts"] = counts
        sys.stdout.write(_dump(out) + "\n")
    else:
        for f in res["findings"]:
            sys.stdout.write(_finding_line(name, f) + "\n")
        sys.stdout.write("%s: %d hata, %d uyarı, %d bilgi · %s/%s (%s)\n" % (
            name, counts["error"], counts["warning"], counts["info"],
            res["register"], res["tur"] or "-", res["detected_by"]))
    return 1 if counts["error"] else 0


def cmd_compare(args):
    old, new = _read(args.old), _read(args.new)
    res = fidelity.compare(old, new)
    if args.format == "json":
        sys.stdout.write(_dump(res) + "\n")
    else:
        for f in res["findings"]:
            sys.stdout.write("%s %s %s\n" % (LEVEL_TR[f["level"]], f["id"], f["message"]))
        sys.stdout.write("sadakat: %d hata, %d uyarı\n" % (res["errors"], res["warnings"]))
    return 1 if res["errors"] else 0


def cmd_stats(args):
    text = _read(args.file)
    name = None if args.file == "-" else args.file
    res = metrics.stats(text, args.register, args.tur, filename=name)
    if args.format == "json":
        sys.stdout.write(_dump(res) + "\n")
        return 0
    band = res["band"]
    rows = [
        ("register/tür", "%s/%s (%s)" % (res["register"], res["tur"] or "-", res["detected_by"])),
        ("kelime", res["words"]),
        ("cümle", res["sentences"]),
        ("paragraf", res["paragraphs"]),
        ("cümle ort.", "%s (sapma %s, en uzun %s)" % (res["sentence_mean"], res["sentence_stdev"],
                                                    res["sentence_max"])),
        ("bant", "cümle %s, en çok %s, Ateşman %s" % tuple(
            "-" if band[k] is None else band[k] for k in ("sentence_words", "sentence_max", "atesman"))),
        ("uzun cümle", res["long_sentences"]),
        ("Ateşman", res["atesman"]),
    ]
    for k, v in sorted(res["per300"].items()):
        rows.append(("%s/300" % k, v))
    for k, v in rows:
        sys.stdout.write("%-14s %s\n" % (k, v))
    return 0


def _rule_dicts(layer=None):
    out = []
    for r in engine.all_rules():
        if layer and r.layer != layer:
            continue
        out.append(r.d)
    return out


def cmd_rules(args):
    layer = None
    if args.layer:
        layer = _layers([args.layer])[0]
    rules = _rule_dicts(layer)
    if args.format == "json":
        slim = [{k: d.get(k) for k in ("id", "layer", "level", "evidence", "message", "default")}
                for d in rules]
        sys.stdout.write(_dump(slim) + "\n")
        return 0
    for d in rules:
        off = " (kapalı)" if d.get("default") == "off" else ""
        sys.stdout.write("%-9s %-8s %-7s %-8s %s%s\n" % (
            d["id"], d["layer"], d.get("level", "info"), d.get("evidence", ""), d.get("message", ""), off))
    sys.stdout.write("%d kural\n" % len(rules))
    return 0


def cmd_explain(args):
    d = engine.rule_data(args.id)
    if d is None:
        raise UsageError("kural yok: %s" % args.id)
    if args.format == "json":
        sys.stdout.write(_dump(d) + "\n")
        return 0
    keys = [("kimlik", "id"), ("katman", "layer"), ("düzey", "level"), ("kanıt", "evidence"),
            ("ileti", "message"), ("öneri", "suggestion"), ("düzeltme", "fix"), ("kaynak", "source"),
            ("register", "registers"), ("kapalı register", "registers_off"), ("varsayılan", "default")]
    for label, key in keys:
        if d.get(key) not in (None, "", []):
            v = d[key]
            if isinstance(v, list):
                v = ", ".join(v)
            sys.stdout.write("%-16s %s\n" % (label, v))
    ex = d.get("examples") or {}
    for t in ex.get("pos", []):
        sys.stdout.write("%-16s %s\n" % ("yakalar", t))
    for t in ex.get("neg", []):
        sys.stdout.write("%-16s %s\n" % ("yakalamaz", t))
    return 0


def cmd_profiles(args):
    profs = profiller.profiles()
    regs = profiller.registers()
    if args.id:
        data = profiller.lookup(args.id)
        if data is None:
            raise UsageError("profil yok: %s" % args.id)
        if args.format == "json":
            sys.stdout.write(_dump(data) + "\n")
            return 0
        for k, v in sorted(data.items()):
            if k in ("guidance", "examples", "register_data"):
                continue
            sys.stdout.write("%-16s %s\n" % (k, json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v))
        for k, v in sorted((data.get("guidance") or {}).items()):
            if isinstance(v, list):
                v = " / ".join(v)
            sys.stdout.write("%-16s %s\n" % (k, v))
        return 0
    if args.format == "json":
        sys.stdout.write(_dump({"registers": sorted(regs), "profiles": sorted(profs)}) + "\n")
        return 0
    for k, v in profs.items():
        sys.stdout.write("%-18s %-10s %s\n" % (k, v.get("register"), v.get("name", "")))
    sys.stdout.write("%d tür, %d register\n" % (len(profs), len(regs)))
    return 0


def cmd_mcp(args):
    from . import mcp
    return mcp.serve()


def cmd_hook(args):
    from . import hook
    data = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read()
    out = hook.run(args.format, args.event, data)
    sys.stdout.write(out + "\n")
    sys.stdout.flush()
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="yontu", description="Türkçe metin denetleyicisi (trlint).")
    p.add_argument("--version", action="version", version="yontu " + __version__)
    sub = p.add_subparsers(dest="cmd")

    lp = sub.add_parser("lint", help="metni denetle")
    lp.add_argument("file", help="dosya ya da - (standart girdi)")
    lp.add_argument("--format", choices=("text", "json"), default="text")
    lp.add_argument("--register")
    lp.add_argument("--tur")
    lp.add_argument("--layer", action="append", help="tdk, ai-iz, stil, yogunluk (virgülle birden çok)")
    lp.add_argument("--min-level", choices=("info", "warning", "error"), default="info")
    lp.add_argument("--fix", action="store_true", help="güvenli tdk düzeltmelerini uygula")
    lp.add_argument("--write", action="store_true", help="--fix sonucunu dosyaya yaz")
    lp.add_argument("--enable", action="append", help="kapalı kuralı aç (kimlik ya da etiket)")
    lp.add_argument("--config", help=".yontu.json yolu")
    lp.set_defaults(func=cmd_lint)

    cp = sub.add_parser("compare", help="sadakat kapısı: OLD ile NEW")
    cp.add_argument("old")
    cp.add_argument("new")
    cp.add_argument("--format", choices=("text", "json"), default="text")
    cp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("stats", help="cümle uzunluğu, okunabilirlik, yoğunluk")
    sp.add_argument("file")
    sp.add_argument("--format", choices=("text", "json"), default="text")
    sp.add_argument("--register")
    sp.add_argument("--tur")
    sp.set_defaults(func=cmd_stats)

    rp = sub.add_parser("rules", help="kuralları listele")
    rp.add_argument("--layer")
    rp.add_argument("--format", choices=("text", "json"), default="text")
    rp.set_defaults(func=cmd_rules)

    ep = sub.add_parser("explain", help="bir kuralı açıkla")
    ep.add_argument("id")
    ep.add_argument("--format", choices=("text", "json"), default="text")
    ep.set_defaults(func=cmd_explain)

    pp = sub.add_parser("profiles", help="tür ve register profilleri")
    pp.add_argument("id", nargs="?")
    pp.add_argument("--format", choices=("text", "json"), default="text")
    pp.set_defaults(func=cmd_profiles)

    mp = sub.add_parser("mcp", help="MCP sunucusu (stdio)")
    mp.set_defaults(func=cmd_mcp)

    hp = sub.add_parser("hook", help="ajan kancası: standart girdiden JSON okur")
    hp.add_argument("--format", required=True,
                    choices=("claude", "codex", "cursor", "gemini", "antigravity", "copilot", "hermes"))
    hp.add_argument("--event", required=True, choices=("stop", "post-edit"))
    hp.set_defaults(func=cmd_hook)
    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help(sys.stderr)
        return 2
    try:
        return args.func(args)
    except UsageError as exc:
        sys.stderr.write("yontu: %s\n" % exc)
        return 2
    except ValueError as exc:
        sys.stderr.write("yontu: %s\n" % exc)
        return 2
