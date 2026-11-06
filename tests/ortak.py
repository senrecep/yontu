"""Shared paths and fixture loaders for the test suite."""
import glob
import io
import os
import re
import sys

TESTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TESTS)
SCRIPTS = os.path.join(ROOT, "skills", "yontu", "scripts")
PKG = os.path.join(SCRIPTS, "yontu")
FIX = os.path.join(TESTS, "fixtures")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import yontu  # noqa: E402
from yontu import engine, fidelity, profiller  # noqa: E402,F401


def read(*parts):
    with io.open(os.path.join(FIX, *parts), encoding="utf-8") as fh:
        return fh.read()


def lines(name):
    """Non-empty, non-comment lines of a fixture."""
    return [l.strip() for l in read(name).split("\n") if l.strip() and not l.startswith("#")]


def sadakat():
    """(name, register, once, sonra) for every fidelity pair."""
    regs = profiller.registers()
    out = []
    for path in sorted(glob.glob(os.path.join(FIX, "sadakat", "*.txt"))):
        with io.open(path, encoding="utf-8") as fh:
            head, rest = fh.read().split("\n", 1)
        once = rest.split("=== önce\n", 1)[1].split("=== sonra\n", 1)[0].strip()
        sonra = rest.split("=== sonra\n", 1)[1].strip()
        reg = head.rsplit("·", 1)[1].strip() if "·" in head else None
        out.append((os.path.basename(path), reg if reg in regs else None, once, sonra))
    return out


def insan(names=False):
    """(register, text) for every human-written fixture. <register>-<n>.md files add more
    texts to the same register. names=True gives (file name, register, text)."""
    out = []
    for path in sorted(glob.glob(os.path.join(FIX, "insan", "*.md"))):
        name = os.path.basename(path)[:-3]
        reg = re.sub(r"-\d+$", "", name)
        with io.open(path, encoding="utf-8") as fh:
            text = fh.read()
        out.append((name, reg, text) if names else (reg, text))
    return out


def ids(res, layer=None, level=None):
    return [f["id"] for f in res["findings"]
            if (layer is None or f["layer"] == layer) and (level is None or f["level"] == level)]


def rule_files():
    return ("rules_tdk.json", "rules_ai.json", "lexicon.json")
