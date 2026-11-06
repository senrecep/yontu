"""Regressions for review findings: offsets, directives, config, MCP, splitter,
apostrophe checks, fidelity and the style guide's own examples."""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from ortak import PKG, ROOT, engine, fidelity, profiller, ids, lines
from yontu import hook
from yontu import textutil as tu

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
ENV.pop("PYTHONPATH", None)
GUIDE_DIR = os.path.join(ROOT, "skills", "yontu", "references", "turler")


def lint_ids(text, **kw):
    return ids(engine.lint(text, **kw))


class TestDirektif(unittest.TestCase):
    def test_directive_in_code_is_ignored(self):
        fenced = "```\n<!-- yontu-disable -->\n```\n\nHerkez geldi."
        inline = "Bunu `<!-- yontu-disable -->` ile kapatırsın. Herkez geldi."
        self.assertIn("YZ-03", lint_ids(fenced))
        self.assertIn("YZ-03", lint_ids(inline))

    def test_directive_outside_code_still_works(self):
        self.assertNotIn("YZ-03", lint_ids("<!-- yontu-disable -->\nHerkez geldi."))


class TestCRLF(unittest.TestCase):
    def test_offsets_point_into_original(self):
        text = "Satır bir.\r\nHerkez geldi.\r\n"
        f = [x for x in engine.lint(text)["findings"] if x["id"] == "YZ-03"][0]
        self.assertEqual(text[f["start"]:f["end"]], "Herkez")

    def test_fix_keeps_crlf(self):
        out = engine.fix("Satır bir.\r\nHerkez geldi.\r\n")
        self.assertEqual(out, "Satır bir.\r\nHerkes geldi.\r\n")

    def test_cli_write_keeps_crlf(self):
        d = tempfile.mkdtemp()
        try:
            path = os.path.join(d, "a.md")
            with io.open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("Satır bir.\r\nHerkez geldi.\r\n")
            subprocess.run([sys.executable, PKG, "lint", path, "--fix", "--write"], env=ENV, cwd=d,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            with io.open(path, encoding="utf-8", newline="") as fh:
                self.assertEqual(fh.read(), "Satır bir.\r\nHerkes geldi.\r\n")
        finally:
            shutil.rmtree(d, ignore_errors=True)


class TestVeriTemizligi(unittest.TestCase):
    def test_no_combining_dot(self):
        for r in engine.all_rules():
            blob = json.dumps(r.d, ensure_ascii=False)
            self.assertNotIn("̇", blob, r.id)

    def test_map_is_case_insensitive(self):
        self.assertIn("YZ-06", lint_ids("Yinede geldi."))
        self.assertIn("YZ-06", lint_ids("yinede geldi."))


class TestAyar(unittest.TestCase):
    def test_string_enable(self):
        cfg = profiller._normalize({"enable": "ST-18, ST-15"})
        self.assertEqual(cfg["enable"], ["ST-18", "ST-15"])

    def test_bad_enable_type(self):
        with self.assertRaises(ValueError):
            engine.check_config({"enable": 5})

    def test_tur_aliases(self):
        self.assertEqual(profiller.canonical_tur("P19"), "linkedin")
        self.assertEqual(profiller.canonical_tur("eposta"), "is-eposta")
        self.assertIn("linkedin", str(profiller.unknown_tur("linkdin")))


class TestMCP(unittest.TestCase):
    def run_lines(self, msgs):
        init = [{"jsonrpc": "2.0", "id": 0, "method": "initialize",
                 "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                            "clientInfo": {"name": "t", "version": "1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"}]
        data = "\n".join(json.dumps(m, ensure_ascii=False) for m in init + msgs) + "\n"
        p = subprocess.run([sys.executable, PKG, "mcp"], input=data.encode("utf-8"), env=ENV,
                           cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        return [json.loads(l) for l in p.stdout.decode("utf-8").splitlines()]

    def test_bad_ids_and_args(self):
        out = self.run_lines([
            {"jsonrpc": "2.0", "id": {"a": 1}, "method": "ping"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": 5}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "text_stats", "arguments": {"text": "", "extra": 1}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "text_stats", "arguments": {"text": ""}}},
        ])
        by = {json.dumps(r.get("id")): r for r in out}
        self.assertEqual(by["null"]["error"]["code"], -32600)
        self.assertEqual(by["2"]["error"]["code"], -32602)
        self.assertTrue(by["3"]["result"].get("isError"))
        self.assertFalse(by["4"]["result"].get("isError"))


class TestCumleBolme(unittest.TestCase):
    def count(self, text):
        return len(tu.split_sentences(text))

    def test_ambiguous_abbreviations(self):
        self.assertEqual(self.count("Gel ve gör. Sonra konuşuruz."), 2)
        self.assertEqual(self.count("Öğr. Gör. Ali geldi."), 1)
        self.assertEqual(self.count("Bunu sen de gör. Ben gidiyorum."), 2)


class TestKesme(unittest.TestCase):
    def test_number_suffix_negatives(self):
        for t in ("Sürüm 4.17.0'daki hata.", "1.0'a geçtik.", "3.10'a yükselttik.",
                  "Maliyet $4'a indi.", "Saat 09.00'da başlar."):
            self.assertNotIn("KS-07N", lint_ids(t), t)

    def test_foreign_names(self):
        for t in ("Facebook'da gördüm.", "Linux'da çalışır.", "Ahmet'de kaldı."):
            self.assertIn("KS-07", lint_ids(t), t)
        for t in ("Apple'ın ürünü.", "Mac'te çalışır.", "Netflix'te izledim."):
            self.assertNotIn("KS-07", lint_ids(t), t)
            self.assertNotIn("KS-07V", lint_ids(t), t)

    def test_sentence_initial_common_noun(self):
        for t in ("Banner'lar güncellendi.", "Diff'leri inceledim."):
            self.assertEqual({"KS-03", "KS-03B"} & set(lint_ids(t)), set(), t)
        self.assertIn("KS-03", lint_ids("Bu Ankara'lı bir öğrenci."))

    def test_known_names_are_error_everywhere(self):
        # Known place and person names: error in every register, at sentence start too.
        for t in ("Bu Ankara'lı bir öğrenci.", "Ankara'lı öğrenciler geldi.", "İstanbul'lu yazar.",
                  "Türkiye'li sporcular kazandı.", "Ahmet'ler geldi."):
            for reg in ("sohbet", "teknik", None):
                res = engine.lint(t, register=reg)
                got = [(f["id"], f["level"]) for f in res["findings"] if f["id"].startswith("KS-03")]
                self.assertEqual(got, [("KS-03", "error")], (t, reg))

    def test_common_noun_apostrophe(self):
        # KS-11: possessive common noun + apostrophe + n-case. Capitalized names and quotes stay out.
        res = engine.lint("Kiracı, sözleşmenin 5. maddesi'nde belirtilen yükümlülükleri yerine getirir.", tur="hukuk")
        got = [(f["id"], f["level"], f.get("fix")) for f in res["findings"] if f["id"] == "KS-11"]
        self.assertEqual(got, [("KS-11", "error", "maddesinde")])
        for t in ("Avrupa Birliği'ne katıldı.", "Türk Dil Kurumu Başkanı'na yazdı.", "Bu Kanun'un 17. maddesi uygulanır.",
                  "Kurtuluş Savaşı'nda kazanıldı.", "Paket 3 kg'dan ağır.", "Ayar 'Gelişmiş menüsü'nde bulunur.",
                  "yontu'nun kurulumu kolay."):
            self.assertNotIn("KS-11", lint_ids(t), t)

    def test_chat_register_softens_ks03b(self):
        res = engine.lint("Bu Modal'lar açıldı.", register="sohbet")
        got = [(f["id"], f["level"]) for f in res["findings"] if f["id"].startswith("KS-03")]
        self.assertEqual(got, [("KS-03B", "warning")])
        self.assertIn("KS-03B", lint_ids("Bu Modal'lar açıldı."))


class TestSadakatEk(unittest.TestCase):
    def fids(self, a, b):
        return [f["id"] for f in fidelity.compare(a, b)["findings"]]

    def test_scale_words(self):
        self.assertIn("SD-01", self.fids("Bütçe 5 milyon lira.", "Bütçe 5 milyar lira."))
        self.assertEqual(self.fids("Bütçe 5 milyon lira.", "Bütçe 5.000.000 lira."), [])

    def test_number_words(self):
        self.assertEqual(self.fids("Süre on iki ay.", "Süre 12 ay."), [])
        self.assertEqual(self.fids("İki yüz bin kişi geldi.", "200.000 kişi geldi."), [])

    def test_sign_and_direction(self):
        self.assertIn("SD-01", self.fids("Sıcaklık -5 derece.", "Sıcaklık 5 derece."))
        self.assertIn("SD-15", self.fids("Satışlar %5 arttı.", "Satışlar %5 azaldı."))

    def test_dropped_claim_word(self):
        self.assertIn("SD-16", self.fids("Kahve 72 saat içinde size ulaşıyor, tazelik garantisiyle!",
                                         "Kahve 72 saat içinde size ulaşıyor."))
        self.assertNotIn("SD-16", self.fids("Kargo ücretsiz.", "Kargo ücretsizdir."))

    def test_month(self):
        self.assertIn("SD-02", self.fids("Toplantı Mart ayında.", "Toplantı Nisan ayında."))


class TestHookMaskeleme(unittest.TestCase):
    def test_mentions_are_not_flagged(self):
        t = "Düzeltmeler:\n- Yinede -> Yine de\n- \"pekala\" yerine pekâlâ yaz.\n"
        got = [f["id"] for f in hook.lint_reply(t, ROOT, "info") or []]
        self.assertNotIn("YZ-06", got)
        self.assertNotIn("DZ-07", got)

    def test_quoted_wrong_form_in_correction(self):
        for t in ("Metninde \"Ankara'lı\" yazmışsın, TDK kurallarına göre bunun doğru yazımı Ankaralı olmalı, düzelttim.",
                  "Sözleşmede “maddesi'nde” yazıyordu, bunu kurala göre maddesinde olarak düzelttim ve kaydettim."):
            self.assertEqual(hook.lint_reply(t, ROOT, "error"), [], t)
        got = [f["id"] for f in hook.lint_reply("Dün Ankara'lı bir tedarikçiyle konuştum, fiyatı yüzde on "
                                                   "düşürdüler ve teslimatı hızlandırdılar.", ROOT, "error") or []]
        self.assertIn("KS-03", got)
        self.assertTrue(hook.is_turkish("İzmir'li tedarikçiyle konuştum, fiyatı yüzde on düşürdüler, iyi oldu."))

    def test_plain_errors_still_flagged(self):
        got = [f["id"] for f in hook.lint_reply("Bugün toplantıya herkez geldi ve iş planını birlikte gözden geçirdik. "
                                                   "Sonra yarınki adımları konuştuk.", ROOT, "info") or []]
        self.assertIn("YZ-03", got)


def guide_examples():
    """(tur, kind, text) for every "> Önce:" and "Sonra:" pair in references/turler/<tur>.md."""
    out = []
    for name in sorted(os.listdir(GUIDE_DIR)):
        if not name.endswith(".md"):
            continue
        tur = name[:-3]
        with io.open(os.path.join(GUIDE_DIR, name), encoding="utf-8") as fh:
            rows = fh.read().split("\n")
        m = re.match(r"# (P\d+|Hukuk) ", rows[0])
        assert m and profiller.canonical_tur(m.group(1).lower()) == tur, name
        i = 0
        while i < len(rows):
            row = rows[i]
            if row.startswith("> Önce: "):
                out.append((tur, "once", row[8:]))
            elif row.startswith("Sonra: "):
                buf = [row[7:]]
                i += 1
                while i < len(rows) and rows[i].strip():
                    buf.append(rows[i])
                    i += 1
                out.append((tur, "sonra", " ".join(buf)))
            i += 1
    return out


class TestRehberOrnekleri(unittest.TestCase):
    # Önce examples whose AI trace the rules are expected to catch.
    CAUGHT = {"akademik-ozet", "akademik-giris", "akademik-tartisma", "haber", "kose", "blog",
              "readme", "ui-bos", "linkedin", "x", "sunum", "sohbet", "resmi-eposta"}
    # Rule IDs each Önce example must trigger under its tür (any layer) and its Sonra must not.
    # edebi is tdk only by design, so it has no entry.
    EXPECT = {
        "akademik-giris": {"AI-A5B"},
        "akademik-tartisma": {"AI-A9"},
        "tez": {"ST-25"},
        "hukuk": {"KS-11"},
        "resmi-yazi": {"ST-26", "ST-27"},
        "teknik-dok": {"ST-28"},
        "readme": {"AI-D13", "AI-D15"},
        "ui-buton": {"ST-29"},
        "ui-hata": {"ST-30"},
        "reklam": {"ST-31"},
        "e-ticaret": {"NK-04", "NK-05B"},
    }

    def test_one_file_per_profile(self):
        names = {n[:-3] for n in os.listdir(GUIDE_DIR) if n.endswith(".md")}
        self.assertEqual(names, set(profiller.profiles()))

    def test_examples(self):
        rows = guide_examples()
        self.assertGreater(len(rows), 50)
        bad = []
        for tur, kind, text in rows:
            res = engine.lint(text, tur=tur)
            if kind == "sonra":
                hit = [f["id"] for f in res["findings"] if f["layer"] == "ai-iz"
                       or (f["layer"] == "tdk" and f["level"] != "info")]
                if hit:
                    bad.append((tur, kind, hit))
            elif tur in self.CAUGHT and not ids(res, layer="ai-iz"):
                bad.append((tur, kind, text[:40]))
        self.assertEqual(bad, [])

    def test_expected_ids(self):
        once, sonra = {}, {}
        for tur, kind, text in guide_examples():
            got = set(ids(engine.lint(text, tur=tur)))
            (once if kind == "once" else sonra).setdefault(tur, set()).update(got)
        bad = []
        for tur, want in sorted(self.EXPECT.items()):
            if want - once.get(tur, set()):
                bad.append((tur, "once", sorted(want - once.get(tur, set()))))
            if want & sonra.get(tur, set()):
                bad.append((tur, "sonra", sorted(want & sonra.get(tur, set()))))
        self.assertEqual(bad, [])

    def test_edebi_is_tdk_only(self):
        text = ("Bu bağlamda yeni bir yolculuğa başladı. Bulgular bunu açıkça kanıtlamaktadır.\n"
                "✅ Bir\n✅ İki\n✅ Üç\nEşsiz bir deneyim yaşadı ve herkez sustu.")
        for kw in ({"register": "edebi"}, {"tur": "edebi"}):
            res = engine.lint(text, **kw)
            self.assertEqual({f["layer"] for f in res["findings"]}, {"tdk"}, kw)
        self.assertTrue(ids(engine.lint(text), layer="ai-iz"))


if __name__ == "__main__":
    unittest.main()
