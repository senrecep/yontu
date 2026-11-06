<p align="center">
  <a href="https://senrecep.github.io/yontu/en/"><img src="https://raw.githubusercontent.com/senrecep/yontu/main/site/public/mark.svg" alt="yontu" width="120" height="120"></a>
</p>

# yontu

<!-- mcp-name: io.github.senrecep/yontu -->

**Turkish humanizer, TDK linter and style guide for AI agents. Türkçe metni yontar: biçim verir, inceltir.**

yontu is a Turkish humanizer (Türkçe humanizer) and TDK spelling and punctuation linter, shipped as an agent skill, an offline CLI and an MCP server. It flags AI and translation patterns in Turkish text, checks spelling and punctuation against the Türk Dil Kurumu (TDK) rules, and fits wording to the genre the text is written for. It works with Claude Code, Codex, Cursor, Gemini CLI and any MCP client. English humanizers do little for Turkish, so every rule here was written for Turkish.

[Türkçe README](README.tr.md) · [Website](https://senrecep.github.io/yontu/en/)

## Why

Most humanizers target English. Their rules come from lists such as Wikipedia's "Signs of AI writing", built on English words like "delve" and "tapestry". Run them on Turkish and they find almost nothing. A few patterns, such as the em dash, carry over, but only with a Turkish rule behind them (TDK allows the dash for dialogue only). Most Turkish AI text fails in other ways:

- `-mAktAdIr` at the end of every sentence, and long `-ArAk` chains
- calques such as `önemli bir rol oynamaktadır` and `bu bağlamda`
- wrappers that replace a case suffix: "konusunda", "hususunda", "bir şekilde"
- chatbot leftovers: `Umarım bu e-posta sizi iyi bulur`, `Umarım yardımcı olur`
- spelling and punctuation errors that a careful Turkish writer would not make: `herşey`, a comma before "ve", `Türkçe'de`

Turkish also changes shape with context. An academic abstract, an ad, a blog post, a README, a commit message and a court petition each have their own sentence length, formality, pronouns and connectives. A rule that fixes one breaks another: `-mAktAdIr` is normal in an abstract and a tell in a blog post. Word choice matters as much: `hızlı bir şekilde` is usually just "hızla".

yontu encodes these as rules with sources, per-genre profiles and a word list, and gives the agent a workflow that keeps the meaning intact.

## What's in the box

| Part | What it is |
|---|---|
| Skill | `skills/yontu/`: `SKILL.md`, nine reference files and one guide per genre in `references/turler/`. Works without Python |
| Linter | Python 3.9+, standard library only, no network. Layers `tdk`, `ai-iz`, `stil`, `yogunluk` |
| Profiles | 28 genres (tür) under 17 registers: sentence length, density, formality, pronouns, mood and tense, connectives, vocabulary, punctuation, structure |
| Fidelity gate | `yontu compare OLD NEW` fails when a rewrite adds a number, date, name, URL or code span, and warns when it drops one or changes negation or modality |
| MCP server | `yontu mcp`, stdio, hand-written JSON-RPC, no SDK |
| Hooks | Post-edit or stop hooks, depending on the agent: Claude Code, Codex, Cursor, Gemini CLI, Copilot, Antigravity. Details in `integrations/` |

## Before and after

From `skills/yontu/references/ornekler.md` (README genre):

> yontu: Türkçe Metinler İçin Modern Ve Güçlü Bir Linter
>
> yontu, Türkçe metinlerinizi analiz ederek yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini tespit eden, modern, güçlü ve kullanıcı dostu bir araçtır. Projenin temel amacı, yazım kalitenizi bir üst seviyeye taşımaktır!
>
> Kullanım: Analiz işlemini gerçekleştirmek için aşağıdaki komutu kolayca çalıştırabilirsiniz: `yontu lint metin.md`

```text
yontu: Türkçe metinler için linter

yontu, Türkçe metindeki yazım hatalarını, noktalama sorunlarını ve yapay zekâ izlerini bulan
bir linterdir.

Kullanım: `yontu lint metin.md`
```

Kept: the name, the three things it finds, the command. Dropped: the adjective triad, the exclamation, "kolayca". The title moved to sentence case. Nothing was added.

## Quick start

### Claude Code (skill, MCP server, hooks)

```
/plugin marketplace add senrecep/yontu
/plugin install yontu@yontu
```

This is the only install path that also adds hooks. Commands: `/yontu:turkcelestir`, `/yontu:yontu-lint`.

### Any agent that reads skill folders

```
npx skills add senrecep/yontu
```

This copies the skill only: no MCP server, no hooks.

### CLI

```
pipx install yontu          # puts yontu on PATH
uvx yontu lint metin.md     # no install
```

From a checkout, without installing: `python3 skills/yontu/scripts/yontu lint metin.md`.

### MCP server

```bash
claude mcp add yontu -- uvx yontu mcp
```

Other clients:

```json
{
  "mcpServers": {
    "yontu": { "command": "uvx", "args": ["yontu", "mcp"] }
  }
}
```

### Per agent

| Agent | Skill | MCP | Hooks |
|---|---|---|---|
| Claude Code | plugin | plugin | plugin |
| Codex CLI | `~/.agents/skills` | `codex mcp add yontu -- yontu mcp` | `hooks.json` |
| Gemini CLI | extension | extension | settings file |
| Cursor | `~/.cursor/skills` | `mcp.json` | `hooks.json` |
| claude.ai (web, mobile) | zip upload, see [folder](integrations/claude-ai/README.md) | planned for v0.2 | none |
| OpenCode, Hermes, Windsurf, Copilot, Cline, Zed, Claude Desktop, Antigravity | see folder | see folder | partial |

Config files, exact paths and what was tested on which version: [integrations/](integrations/README.md).

### Install profiles

| Profile | What loads | Claude Code | Other agents |
|---|---|---|---|
| `lite` | the skill; it runs the linter through the shell | `/plugin install yontu-lite@yontu` | `scripts/install.sh --<agent> --profile lite --apply` |
| `standard` | `lite` plus hooks | use `full` | `--profile standard` also prints the hook config to merge |
| `full` | `standard` plus the MCP server | `/plugin install yontu@yontu` | `--profile full` prints the hook and MCP configs |

`install.sh` is a dry run without `--apply` and writes only the skill folder. In Claude Code, install one of the two plugins, not both.

Context cost: about 150 tokens always on for the full plugin before its MCP tools, about 130 for lite, and about 3,900 tokens for a whole blog rewrite. Numbers, method and what loads when: [docs/CONTEXT.md](docs/CONTEXT.md).

## Tools

| MCP tool | What it does |
|---|---|
| `lint_text` | Findings with layer, rule id, level, span and suggestion (`detail: true` returns every field) |
| `compare_texts` | Fidelity gate between two versions |
| `get_style_guide` | Guidance for one genre by tür id, or a reference file: its section list first, then one section |
| `fix_text` | Applies safe `tdk` fixes only |
| `text_stats` | Sentence length, readability, density |
| `explain_rule` | Message, source and examples for a rule id |
| `list_profiles` | All registers and genres |
| `get_profile` | Thresholds for one genre or register |

The server lists the first three tools by default. Set `YONTU_MCP_TOOLS=full` in its env to list all eight. It answers the other five either way, but most clients show the model only listed tools.

Prompts: `turkcelestir` (translate or adapt into Turkish), `yogunlastir` (tighten a text).

## CLI

```
yontu lint FILE [--register SLUG] [--tur ID] [--layer tdk,ai-iz] [--min-level warning] [--format json]
yontu lint FILE --fix [--write]     # safe tdk fixes only; --write saves the file
yontu compare OLD NEW               # fidelity gate
yontu stats FILE                    # sentence length, Ateşman readability, density
yontu rules [--layer tdk]           # list rules
yontu explain AI-E6                 # one rule with source and examples
yontu profiles [ID]                 # genres and registers
```

`FILE` can be `-` for standard input. `lint` and `compare` exit with 1 when they report an `error`, and with 2 on a usage error.

Without `--register` or `--tur`, yontu guesses the register from the content and falls back to `notr`, where every style rule is `info`.

Project settings go in `.yontu.json` (keys `register`, `tur`, `enable`, `rules`). Silence a rule in place with `<!-- yontu-disable-next-line KS-01 -->`, or a range with `<!-- yontu-disable KS-01 -->` and `<!-- yontu-enable KS-01 -->`.

## Profiles

`--register` picks the register, `--tur` the genre. A genre implies its register.

| Register | Genres (`--tur`) |
|---|---|
| `akademik` | `akademik-ozet`, `akademik-giris`, `akademik-tartisma`, `tez` |
| `resmi` | `dilekce`, `resmi-yazi` |
| `hukuk` | `hukuk` (contract, ruling, regulation, privacy notice) |
| `haber` | `haber` |
| `deneme` | `kose` |
| `blog` | `blog`, `linkedin` |
| `teknik` | `teknik-dok`, `readme`, `changelog` |
| `commit` | `commit` |
| `ui` | `ui-buton`, `ui-hata`, `ui-bos` |
| `pazarlama` | `reklam`, `e-ticaret` |
| `sosyal` | `x`, `instagram` |
| `kurumsal` | `resmi-eposta`, `basin-bulteni` |
| `is-eposta` | `is-eposta` |
| `sozlu` | `sunum` |
| `edebi` | `edebi` |
| `sohbet` | `sohbet` |
| `notr` | none: all style rules at `info` |

`hukuk` and `edebi` get the `tdk` layer and the fidelity gate only. The skill does not rewrite them unless asked.

## Rule layers

| Layer | What it checks | Levels |
|---|---|---|
| `tdk` | Spelling and punctuation from the TDK Yazım Kılavuzu and Güncel Türkçe Sözlük | `error`, `warning`, `info`. The only layer with autofix |
| `ai-iz` | AI and translation patterns | `warning` or `info`, never fixed |
| `stil` | Fit to the genre profile | mostly `info` |
| `yogunluk` | Wordy phrasing, light verbs, wrappers | always `info` |

Every `tdk` rule names the TDK Yazım Kılavuzu section or Güncel Türkçe Sözlük entry it comes from. The links are in `skills/yontu/references/kaynaklar.md`. Autofix runs only on deterministic rules with near-zero false positives (`herşey` → "her şey", `Türkçe'de` → "Türkçede"). Dictionary redirects are never autofixed.

Every `ai-iz` rule carries an evidence label: `veri` (measured on a corpus), `hakem` (agreed by reviewers) or `hipotez` (observed, not measured). A `hipotez` rule never goes above `info`, and a `hakem` rule never goes above `warning`. The v0.1 rule set has no `veri` rules yet; see [ROADMAP.md](ROADMAP.md).

Run `yontu rules` for the full list and `yontu explain ID` for any rule.

## Limitations

- Not an AI detector. yontu reports patterns. A finding does not mean a text was machine-written, and a clean report does not mean it was not. Passing a detector is not a goal.
- Heuristics. The `ai-iz`, `stil` and `yogunluk` rules are regular expressions and counts over surface forms, with no morphological analysis. Expect false positives, mostly at `info`.
- Uncalibrated thresholds. Sentence bands and density thresholds come from the literature and from review, not from a human baseline corpus. Until calibration they stay at `info` or `warning`.
- No dictionary. The linter catches known misspellings, not every misspelling.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New rules need a source, an evidence label and fixtures. Turkish examples of clean human writing in any genre are the most useful contribution: they are what calibration needs.

## Credits

- Türk Dil Kurumu: Yazım Kuralları and Güncel Türkçe Sözlük.
- [turkish-humanify](https://github.com/durmazoguzhan/turkish-humanify) by Oguzhan Durmaz (MIT) and [turkce-humanizer](https://github.com/bushrabeg/turkce-humanizer) by bushrabeg (MIT), whose ideas were rewritten and checked against TDK.
- Wikipedia's "Signs of AI writing", for the structure of the pattern catalog.
- Full source list: `skills/yontu/references/kaynaklar.md`.

## License

MIT. See [LICENSE](LICENSE).
