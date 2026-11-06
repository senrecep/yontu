#!/usr/bin/env python3
"""Assert that every version string in the repository is the same.

Usage: scripts/check-versions.py [--tag vX.Y.Z]

Exit 0 when all locations agree (and match --tag if given), exit 1 with a table otherwise.
Stdlib only; reads the files as text, so it works on Python 3.9+ without tomllib.
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def _json(rel):
    return json.loads(_read(rel))


def _regex(rel, pattern):
    m = re.search(pattern, _read(rel), re.M)
    if not m:
        raise ValueError("no version found in %s" % rel)
    return m.group(1)


def collect():
    """Return [(location, version)] for every place a version is written."""
    plugin = _json(".claude-plugin/plugin.json")
    market = _json(".claude-plugin/marketplace.json")
    server = _json("server.json")
    found = [
        ("pyproject.toml [project].version", _regex("pyproject.toml", r'^version\s*=\s*"([^"]+)"')),
        ("skills/yontu/scripts/yontu/__init__.py __version__",
         _regex("skills/yontu/scripts/yontu/__init__.py", r'^__version__\s*=\s*"([^"]+)"')),
        (".claude-plugin/plugin.json version", plugin.get("version")),
    ]
    if "version" in market.get("metadata", {}):
        found.append((".claude-plugin/marketplace.json metadata.version", market["metadata"]["version"]))
    for i, p in enumerate(market.get("plugins", [])):
        found.append((".claude-plugin/marketplace.json plugins[%d] (%s)" % (i, p.get("name")), p.get("version")))
    found.append(("server.json version", server.get("version")))
    for i, p in enumerate(server.get("packages", [])):
        found.append(("server.json packages[%d].version" % i, p.get("version")))
    found.append(("gemini-extension.json version", _json("gemini-extension.json").get("version")))
    found.append(("skills/yontu/SKILL.md metadata.version",
                  _regex("skills/yontu/SKILL.md", r'^  version:\s*"([^"]+)"')))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tag", help="release tag (vX.Y.Z) that every version must equal")
    args = ap.parse_args(argv)
    found = collect()
    expected = args.tag[1:] if args.tag and args.tag.startswith("v") else args.tag
    if expected is None:
        expected = found[0][1]
    bad = [(loc, v) for loc, v in found if v != expected]
    if not bad:
        print("all %d versions are %s" % (len(found), expected))
        return 0
    width = max(len(loc) for loc, _ in found)
    print("version mismatch (expected %s):" % expected, file=sys.stderr)
    for loc, v in found:
        print("  %-*s  %s%s" % (width, loc, v, "" if v == expected else "   <-- differs"), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
