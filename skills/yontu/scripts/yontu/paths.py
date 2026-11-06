"""Locate the skill files (SKILL.md, references/) in a source checkout or an installed wheel.

Source checkout: skills/yontu/SKILL.md and skills/yontu/references/**.
Wheel: the same files are packaged as yontu/skill/SKILL.md and yontu/skill/references/**.

    from yontu import paths
    paths.references_dir()              # absolute path, or None if not shipped
    paths.reference_files()             # ["ai-oruntuleri.md", ..., "turler/blog.md", ...]
    paths.reference_path("turler/blog") # absolute path, or None (unknown or outside references/)
"""
import os

_PKG = os.path.dirname(os.path.abspath(__file__))
# Wheel layout first, then the source tree (skills/yontu/scripts/yontu -> skills/yontu).
_CANDIDATES = (os.path.join(_PKG, "skill"), os.path.dirname(os.path.dirname(_PKG)))


def skill_dir():
    """Directory that holds SKILL.md and references/. None when neither layout is present."""
    for d in _CANDIDATES:
        if os.path.isdir(os.path.join(d, "references")):
            return d
    return None


def references_dir():
    """Absolute path of the references/ directory, or None."""
    d = skill_dir()
    return os.path.join(d, "references") if d else None


def reference_files():
    """Every .md file under references/, as sorted '/'-separated paths relative to it."""
    root = references_dir()
    if not root:
        return []
    out = []
    for cur, dirs, files in os.walk(root):
        dirs.sort()
        rel = os.path.relpath(cur, root)
        for name in files:
            if name.endswith(".md"):
                path = name if rel == "." else os.path.join(rel, name)
                out.append(path.replace(os.sep, "/"))
    return sorted(out)


def reference_path(name):
    """Absolute path of one reference file ("turler/blog" or "turler/blog.md").
    None when the file does not exist or the name points outside references/."""
    root = references_dir()
    if not root or not name:
        return None
    name = name.replace("\\", "/").strip("/")
    if not name.endswith(".md"):
        name += ".md"
    path = os.path.realpath(os.path.join(root, *name.split("/")))
    real_root = os.path.realpath(root)
    if not path.startswith(real_root + os.sep) or not os.path.isfile(path):
        return None
    return path
