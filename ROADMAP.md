# Roadmap

Work planned after 0.1.0. Order is rough priority. Nothing here has a date.

## Calibration corpus

Every style threshold in 0.1 comes from the literature or from review. None is measured against human Turkish text, so `hipotez` rules stay at `info` and no rule has the `veri` label.

- Collect at least 50 human texts per register from third parties. `tests/fixtures/insan/` holds 3 human-register reference texts per register today, written for the project, enough to catch false positives in tests but not to calibrate. Candidate sources: DergiPark abstracts from 2016 to 2021 (akademik), pre-2022 news archives (haber), Turkish documentation and blogs (teknik), Bilkent Turkish Writings (deneme), the Resmî Gazete (hukuk), open i18n files (ui), and repositories with Turkish commit history (commit).
- Acceptance: a rule may produce at most 0.5 `warning` or `error` findings per 1,000 words on that corpus. A rule above that drops to `info`.
- Counter corpus: the same 50 prompts answered by several models, to measure how well each rule separates the two sets.
- Passing calibration is the only way a rule can rise above its evidence ceiling.

## Static TDK dictionary

The linter knows a fixed list of misspellings. A word list built from the Güncel Türkçe Sözlük and the Yazım Kılavuzu index at build time would catch more.

- Built by a script that is the only part of the project allowed to use the network. Runtime stays offline.
- Versioned, with the snapshot date recorded in every rule set.
- The build script reports entries that changed since the last snapshot.

## Morphology: `--deep`

Some metrics need real morphological analysis: passive voice, `-(y)An` participles, verb-final ratio, and stem-based lexical richness (MATTR, MTLD, Yule's K).

- An optional `--deep` mode backed by a Turkish morphological analyzer.
- The default mode stays standard library only.
- The false positive rate of each analyzer is measured before any metric leaves `info`.

## Glossary consistency

Long technical texts often switch between a Turkish term and its English original, or between two Turkish terms, for the same thing.

- A project glossary in `.yontu.json`.
- Findings when one concept appears under several terms in a document, or when code-mixed terms are inflected inconsistently.

## Session template repetition

A single reply can look clean while every reply in a session opens and closes the same way.

- The stop hook keeps a short per-session record of opening and closing patterns.
- A finding when the same template repeats across replies.
- The record stays local and is deleted with the session.
