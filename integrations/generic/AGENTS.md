## Turkish prose (yontu)

Apply this section whenever you write, edit, translate or review Turkish text. Do not ask which genre it is: detect it.

Tools, in this order of preference:
- MCP server `yontu`: `lint_text`, `compare_texts`, `get_style_guide` (pass a tür id such as `blog` for its profile).
- CLI: `yontu lint FILE [--tur ID]`, `yontu compare OLD NEW`, `yontu profiles ID`. Text output is enough; `--format json` adds character offsets.
- Neither available: follow the rules below by hand.

Only the `tdk` layer can be `error`. `ai-iz` and style findings are hints. `hipotez` findings are weak hints.

Genre (tür) from evidence: explicit words or flags, then the file (`COMMIT_EDITMSG` commit, `README*` teknik/readme, `CHANGELOG*` teknik/changelog, `.tex` akademik, a chat reply sohbet), then content cues. Low confidence: `notr`.

Hard rules:
- Keep every proposition. Add no facts, numbers, dates, names, examples, citations, causes or code.
- Keep hedges, modality (`-mAlI`, `-Abil`, `muhtemelen`), evidence strength, negation, voice, person, tense, terms, markdown, links and lists.
- Do not edit code, inline code, URLs, paths, frontmatter, block quotes or quotations.
- Do not add an em dash inside a sentence, semicolons in blog, e-posta, sosyal, sohbet or ui text, a rhetorical question with its answer, aphorisms, idiom showers, synonym rotation or bold-label bullets.
- Do not "humanize" with invented anecdotes, slang or deliberate errors. Clean text needs few or no edits.
- Where the text needs information the input lacks, write a placeholder such as `[ürün adı]`.

Workflow:
1. Lint with the detected tür.
2. Fix structure first (openings, closings, summary sandwich, fake lists), then sentences (`-mAktAdIr` density, `-ArAk` chains, nominalization, uniform length, `X değil, Y`, triads, calques), then surface (TDK spelling and punctuation, inflated adjectives, filler, wrappers).
3. Prefer deleting filler to replacing it, and a suffix to a wrapper phrase.
4. Re-lint, then compare the old and new text. Revert any edit that adds a number, date, URL, code or name. Revert a changed negation, modality or voice unless the meaning is unchanged.

Register notes: `akademik` allows `-mAktAdIr`, passive and semicolons. `hukuk` gets TDK and fidelity checks only, no rewrite unless asked. `edebi` gets TDK fixes only. `sohbet` answers first, with no praise opener and no "Umarım yardımcı olur" closer.

Output: for a rewrite, return only the text. For a review, list span, problem, fix and rule id, grouped by structure, sentence and surface, and say plainly when nothing needs to change.
