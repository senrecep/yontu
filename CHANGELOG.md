# Changelog

## Unreleased

### Removed

* **cli:** drop the `trlint` console script and the `trlint-disable` comment prefix; use `yontu` and `yontu-disable`.

## 0.1.0 (2026-11-06)


### Added

* **linter:** add stdlib Turkish linter, fidelity check, MCP server and hooks ([f3948bd](https://github.com/senrecep/yontu/commit/f3948bdf4a8b7f80b14672b19c8b60f037e36f4e))
* **plugin:** add Claude plugin, commands and agent integrations ([a097943](https://github.com/senrecep/yontu/commit/a097943a6c87a30cd586ff35ffa6ba7cc41218b1))
* **skill:** add yontu skill, style references and genre guides ([fdda655](https://github.com/senrecep/yontu/commit/fdda65539b7f5030000c58926144133a6deb084e))

## Initial feature set

Notes written by hand before the first release (0.1.0). release-please prepends every release entry above this section from conventional commits and adds the `# Changelog` title. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

### Added

- Agent skill `yontu`: `SKILL.md` with rewrite, review, write and concise modes, nine reference files (AI patterns, genres, TDK spelling and punctuation, connectives, sentence types, concision, over-correction, examples, sources) and one guide per genre under `references/turler/`. `SKILL.md` opens with a fixed checklist and a table that says which file to read when; `turler.md` is an index, so the agent reads only the guide for its genre.
- Linter with four layers: `tdk` (spelling and punctuation, each rule citing its TDK source), `ai-iz` (AI and translation patterns with `hakem` or `hipotez` evidence labels), `stil` (genre fit) and `yogunluk` (concision, always `info`).
- Safe autofix for deterministic `tdk` rules only (`lint --fix`, `--write`).
- 28 genre profiles under 17 registers, including `hukuk`. Selected with `--register` and `--tur`, or detected from the file name and content.
- Fidelity gate `yontu compare OLD NEW`: new numbers, dates, names, URLs or code are errors; dropped items, dropped claim words (garanti, ücretsiz, indirim, iade and similar), changes in negation, modality or evidence strength, and new first person or cause are warnings.
- Commands `stats`, `rules`, `explain` and `profiles`.
- Project config `.yontu.json` and inline `yontu-disable` / `yontu-enable` comments.
- Two console scripts, `yontu` and `trlint`, for the same CLI. Python 3.9+, standard library only, no network at runtime.
- MCP server `yontu mcp` (stdio) with 8 tools and 2 prompts. It lists `lint_text`, `compare_texts` and `get_style_guide` by default; `YONTU_MCP_TOOLS=full` lists all 8. `get_style_guide` takes a genre id or a reference name and returns a reference as a section list, then one section. `lint_text` returns trimmed findings unless `detail: true`.
- The wheel ships `SKILL.md` and every reference file, so `get_style_guide` works after `pip install`.
- Hooks (`yontu hook`) for post-edit or stop events, depending on the agent: Claude Code, Codex, Cursor, Gemini CLI, Copilot and Antigravity. See `integrations/README.md` for which event each agent gets. Off switches `YONTU_DISABLE=1` and `.yontu-ignore`.
- Claude Code marketplace with two plugins: `yontu` (skill, MCP server, hooks, commands) and `yontu-lite` (skill only). The slash commands set `disable-model-invocation`, so they stay out of the model's listing.
- Gemini CLI extension, MCP Registry `server.json`, and config files for 13 agents plus a generic `AGENTS.md` snippet under `integrations/`.
- `scripts/install.sh`: links or copies the skill into local agent folders. Dry run unless `--apply`. `--profile standard` also prints the hook config to merge by hand, `--profile full` the hook and MCP configs.
- `docs/CONTEXT.md`: what yontu adds to an agent's context and when.

### Known issues

- Register detection without `--register` or `--tur` falls back to `notr` for most texts. Pass the genre when you know it.
- KS-03 (apostrophe before `-lI`, `-cI`, `-sIz`) is an `error` only for the names in `ozel_adlar.json`. Other capitalized words go to KS-03B, an `error` without autofix that is lowered to `warning` in `sohbet`, `teknik` and `commit`. The Stop hook lints replies as `sohbet`, so a misspelled unlisted Turkish name in mid-sentence passes it. KS-03S catches the sentence-initial case as a `warning`.
- KS-11 is an `error` only on document nouns (madde, fıkra, bent, ek, bölüm, sayfa and similar). Other lowercase nouns go to KS-11B, a `warning` without autofix, because a brand written in lowercase keeps its apostrophe (yemeksepeti'nden).
- The Stop hook skips replies under 8 words and replies that are not mostly Turkish.
- AI-A5B ("Bu bağlamda,") and AI-A9 still run in `akademik`, where human writers use them too. They are `info` and wait for calibration.
- AI-L3B flags "bu yolculukta öğrendiğim" even when the journey is literal.
- ST-31 flags superlatives that are not claims ("En iyi sonuç için", "en taze hâliyle"). It is `info`.
- The rules added last (AI-A11, AI-D16, AI-D17, AI-D18, AI-L4, the second form of AI-B13) are `hipotez` and `info`. They were checked on test samples only.
- No `ai-iz` rule has the `veri` evidence label yet. Thresholds are not calibrated against a human corpus: the test fixtures hold 3 human-register reference texts per register, written for the project, far below the 50 that calibration needs.
