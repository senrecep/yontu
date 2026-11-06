"""yontu.paths finds SKILL.md and references/** and pyproject ships all of them."""
import fnmatch
import os
import re
import unittest

from ortak import ROOT
from yontu import paths

SKILL = os.path.join(ROOT, "skills", "yontu")


class TestPaths(unittest.TestCase):
    def test_source_layout(self):
        self.assertEqual(paths.skill_dir(), SKILL)
        self.assertEqual(paths.references_dir(), os.path.join(SKILL, "references"))

    def test_files_are_recursive(self):
        files = paths.reference_files()
        on_disk = []
        for cur, _, names in os.walk(paths.references_dir()):
            for n in names:
                if n.endswith(".md"):
                    on_disk.append(os.path.relpath(os.path.join(cur, n), paths.references_dir()).replace(os.sep, "/"))
        self.assertEqual(files, sorted(on_disk))
        self.assertIn("turler/blog.md", files)

    def test_reference_path(self):
        self.assertTrue(paths.reference_path("turler/blog").endswith(os.path.join("turler", "blog.md")))
        self.assertEqual(paths.reference_path("turler/blog.md"), paths.reference_path("turler/blog"))
        for bad in ("../SKILL", "../../yontu/paths.py", "yok", "", None):
            self.assertIsNone(paths.reference_path(bad), bad)

    def test_pyproject_ships_every_reference(self):
        with open(os.path.join(ROOT, "pyproject.toml"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r'^"yontu\.skill" = \[(.*)\]$', text, re.M)
        self.assertTrue(m)
        globs = re.findall(r'"([^"]+)"', m.group(1))
        self.assertIn("SKILL.md", globs)
        for f in paths.reference_files():
            rel = "references/" + f
            # setuptools "**" matches any depth; "*" stays within one directory.
            ok = any(fnmatch.fnmatch(rel, g.replace("**/", "*/")) if "**" in g
                     else (fnmatch.fnmatch(rel, g) and rel.count("/") == g.count("/")) for g in globs)
            self.assertTrue(ok, rel)


if __name__ == "__main__":
    unittest.main()
