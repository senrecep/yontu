---
name: yontu
description: >-
  Türkçe metni yontar: yapay zekâ ve çeviri kalıplarını işaretler ve sadeleştirir (humanizer),
  yazımı ve noktalamayı TDK kurallarına göre denetler, metni türüne (akademik, haber, blog, e-posta, hukuk,
  arayüz, sosyal medya) uydurur ve kısaltır. Türkçe metin yazarken, düzeltirken, Türkçeleştirirken ya da
  "doğallaştır", "AI kokusunu gider", "kısalt", "TDK'ye göre düzelt" istendiğinde kullan.
  Turkish humanizer: flags and simplifies AI tells and translationese, TDK spelling and
  punctuation linter, genre-aware Turkish style and concise rewriting.
license: MIT
compatibility: >-
  Works from the references alone. Optional offline linter needs Python 3.9+ (no network).
metadata:
  version: "0.2.0"  # x-release-please-version
  language: "tr"
  cli: "yontu"
---

# yontu

Make Turkish text read like a careful human wrote it for its actual reader: simplify AI and
translation tells, enforce TDK spelling, fit the genre (tür), tighten wordy phrasing. Never
change what the text says.

## Checklist (do every step, even for short texts)

1. Pick the mode and the tür id. Copy the id from the list below. Never guess one.
2. Lint the input: `Y lint IN.md --tur ID`.
3. Read `references/turler/ID.md` (one short file). For `write` mode, do this first. `review`
   stops here and reports.
4. Write the rewrite to `OUT.md` under the hard rules below.
5. Lint the new text. For each `ai-iz` id from step 2 still there, note "fixed" or "kept:
   reason". Run `Y compare IN.md OUT.md` and fix every `error`. Skip this and the run is
   unfinished.
6. Return the text of `OUT.md` only.

`Y` means `python3 "${CLAUDE_SKILL_DIR}/scripts/yontu"` (or `yontu` on `PATH`). Type it in
full each time; never set a shell variable. If none runs, use the manual gate below.
Write temp files with your file tools in the working directory (no heredoc, `sed` or `/tmp`)
and delete them at the end. `lint` exits 1 on an `error`, so do not chain it with `&&`. Add
`--format json` only for character offsets. MCP only: `lint_text`, `compare_texts`,
`get_style_guide` (topic = tür id).

| Command | Use |
|---|---|
| `Y lint FILE --tur ID` | Findings with layer, id, level, suggestion |
| `Y lint FILE --fix` | Safe `tdk` autofixes only |
| `Y compare OLD NEW` | Fidelity gate: new or lost numbers, names, negation, modality |
| `Y profiles ID` | One tür profile; `Y profiles` lists every id |

Only the `tdk` layer can be `error` or autofixed. `ai-iz` findings are `warning` or `info`;
treat evidence `hipotez` as a hint. Concision findings are always `info`.

## Mode and tür

- Input not Turkish and the user says "Türkçeleştir": translate, then run the checklist.
- `rewrite` (default) returns the improved text. `review` ("incele", "denetle") returns
  findings only. `write` authors new text. `concise` ("kısalt", "yoğunlaştır"): light by
  default, strong only on request.

Tür ids by register (`--tur` also takes `p19` or a register name):
akademik-ozet, akademik-giris, akademik-tartisma, tez · dilekce, resmi-yazi, hukuk ·
haber, kose, blog, linkedin · teknik-dok, readme, changelog, commit · ui-buton, ui-hata,
ui-bos · reklam, e-ticaret, x, instagram · resmi-eposta, is-eposta, basin-bulteni · sunum,
edebi, sohbet.

Detect, never ask: user words or flags, then file name (`COMMIT_EDITMSG` commit,
`CHANGELOG*` changelog, `README*` readme, `.po` ui, `.tex` akademik, chat reply sohbet),
then content cues. Low confidence: `--register notr`. Ask only in `write` mode when the
audience is unknown.

## Hard rules

- Fidelity: keep every proposition. Add no facts, numbers, dates, names, examples, causes
  or claims. Keep hedges and modality (`-mAlI`, `-Abil`, `muhtemelen`), negation, voice,
  person, tense, terms, markdown, links and lists. Keep evidence strength
  (`düşündürmek < işaret etmek < göstermek < kanıtlamak`). Missing info: `[yer tutucu]`.
- Masking: never edit frontmatter, code, URLs, paths or quotations. A `> **Not:**` callout
  is the author's text, not a quote: fix it.
- No new tells: a `—` inside a sentence becomes a comma or a new sentence, and the clause
  after it stays. No semicolons in blog, e-posta, sosyal, sohbet or ui text, no rhetorical
  question plus answer, no aphorisms, no synonym rotation, no new bold-label bullets (old
  labels in a real list may stay as short plain lead words).
- No over-correction: no invented anecdotes, slang or forced first person. Good text gets
  few or no edits. Read `references/asiri-duzeltme.md` before a heavy rewrite.
- Persuasive genres (`blog`, `linkedin`, `reklam`, `e-ticaret`, `x`, `instagram`): keep the
  hook, the emotion, the sign-off, the brand claim and the call to action. Reword stock
  phrases at the same strength; delete only unproven superlatives ("en iyi"), closing
  aphorisms without a fact and sentences about the text ("Umarız bu yazı …"). In `write` mode use connected prose in the tür's length band, no
  headings under about 150 words; fix ST-15 and ST-01.

## Rewrite and compare

Top down: structure, sentence, surface. Change what a sentence does, not its trigger word
("kritik rol" to "belirleyici rol" fixes nothing):

- A sentence about the text ("Bu bölümde … anlatılır") goes; a claim inside it becomes a
  plain sentence. A closer that restates an earlier claim goes. A template title becomes a topic line.
- Rhythm: mix long and short. Join short same-topic sentences with a converb (`-Ip`,
  `-IncA`) or a participle before the noun instead of splitting every long one. Outside
  definitions and formal tür, drop `-DIr`: "Varsayılan değer 3600, yani bir saat."
- Fix tells in the middle paragraphs too. Lint-clean is the floor, not the goal.

A `compare` error (new number, date, URL, code or name) reverts that edit. A warning
(dropped item or claim word, negation, modality) stays only if the meaning is unchanged.
Valid reasons to keep an `ai-iz` id: a real list, a quote, a term the tür needs. Do not
chase `stil` or `yogunluk` info into a second rewrite.

## Write mode

1. Read `references/turler/ID.md`.
2. Put the given facts in `facts.txt`, one per line.
3. Write `draft.md` in the profile's sentence band, hitap and kip.
4. `Y lint draft.md --tur ID`, fix as above. Steps 4-5 are required even for 20 words.
5. `Y compare facts.txt draft.md`. Any new number, date, name or URL: remove it or use a
   `[yer tutucu]`.

## Manual gate (no linter)

Every digit, date, percentage, URL, code span and capitalized name in the output exists in
the input. Same count of negations (`değil`, `yok`, `-mA-`). Same modality and evidence
rung. No new first person, no new cause ("çünkü", "-dığı için"). For a translation, check
source to first draft, then draft to final text.

## Registers that change behavior

- `akademik`: `-mAktAdIr`, passive, `-DIr` and semicolons are normal.
- `hukuk`: without a rewrite request, `lint`, optional `--fix`, then `compare`. "işbu", "mezkûr" stay.
- `resmi`: impersonal `-DIr`, closings "Arz ederim", "Rica ederim".
- `edebi`: `tdk` layer only; style ideas go to the author as questions.
- `sohbet`: answer first; no praise opener, no "Umarım yardımcı olur".
- `notr`: change only clear tells and TDK errors.

Do not flag: clean grammar, a real list, one bold phrase, "Ama" or "Ve" at sentence start,
one "aslında", "katkı sunmak", "tekrardan", "illaki", "arttırmak", curly quotes.

## Output

`rewrite`, `concise`, `write`: the text only, no preface or change log. Add a note only when
asked or when a placeholder needs the author. `review`: a short list of span, problem, fix
and rule id, grouped by structure, sentence and surface. Reply in the user's language.

## Read only when needed

| File | Read when |
|---|---|
| `references/turler/ID.md` | Always, once the tür is known |
| `references/turler.md` | Id table, register thresholds, tür detection cues |
| `references/asiri-duzeltme.md` | Before a heavy rewrite, or the output feels overdone |
| `references/ai-oruntuleri.md` | No linter, or you must explain an `ai-iz` finding |
| `references/noktalama-yazim.md` | A TDK spelling, apostrophe, number or punctuation question |
| `references/yogunlastirma.md` | `concise` mode |
| `references/baglaclar.md` | Connector chains, "ki" and "de" spelling |
| `references/cumle-turleri.md` | Uniform rhythm, inversion, converbs, `-ArAk` chains |
| `references/ornekler.md` | Full before and after pairs for calibration |
| `references/kaynaklar.md` | Citing a rule's source |
