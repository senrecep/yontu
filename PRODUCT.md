# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro (latest stable, exact versions pinned, lockfile committed) in `site/` at the repository root, so the Python package is unaffected. Static output only, deployed to GitHub Pages under `https://senrecep.github.io/yontu/` (`site: 'https://senrecep.github.io'`, `base: '/yontu'`). Fonts are self-hosted; nothing loads from a font CDN at runtime. Type pairing: a serif display face for headings only, Geist for body text, Geist Mono for code and terminal output.

## Users

Developers and technical writers who use AI coding agents (Claude Code, Codex, Cursor, Gemini CLI and other MCP clients) to write or translate Turkish text: READMEs, docs, commit messages, UI strings, blog posts, emails, academic abstracts. They notice that the agent's Turkish reads like a translation and that English humanizers do nothing for it. The landing page visitor is deciding whether to install yontu into their agent.

## Product Purpose

yontu is a Turkish humanizer and TDK (Türk Dil Kurumu) spelling and punctuation linter for AI agents. It flags AI and translation patterns in Turkish, checks spelling and punctuation against TDK rules, fits wording to the genre the text is written for, and gives the agent a workflow that keeps meaning intact. Success: the agent's Turkish reads as if a careful Turkish writer wrote it, with no facts added or lost.

## Positioning

Every rule was written for Turkish, not ported from English lists. `tdk` rules name their Yazım Kılavuzu section or Güncel Türkçe Sözlük entry; `ai-iz` rules carry an evidence label (`veri`, `hakem`, `hipotez`) that caps their severity. Genre profiles (28 genres under 17 registers) decide what counts as a flaw: `-mAktAdIr` is normal in an abstract and a tell in a blog post. A fidelity gate (`yontu compare OLD NEW`) fails a rewrite that adds a number, date, name, URL or code span.

## Operating Context

Used inside an agent session, from a shell, or as an MCP tool. Delivered as an Agent Skill (`skills/yontu/`), a Claude Code plugin (`/plugin marketplace add senrecep/yontu`, `/plugin install yontu@yontu`, or `yontu-lite@yontu`), an MCP server (`yontu mcp`, stdio), a Gemini CLI extension, and post-edit or stop hooks for Claude Code, Codex, Cursor, Gemini CLI, Copilot and Antigravity. CLI: `yontu` with `lint`, `compare`, `stats`, `rules`, `explain`, `profiles`, `mcp`, `hook`.

## Capabilities and Constraints

- Python 3.9+, standard library only, no network at runtime, no dependencies.
- Four rule layers: `tdk` (error/warning/info, the only layer with autofix), `ai-iz` (at most warning, never fixed), `stil` (mostly info), `yogunluk` (always info).
- Autofix only for deterministic rules (`herşey` → "her şey", `Türkçe'de` → "Türkçede").
- MCP server lists 3 tools by default (`lint_text`, `compare_texts`, `get_style_guide`), 8 with `YONTU_MCP_TOOLS=full`.
- Install profiles: lite (skill only), standard (plus hooks), full (plus MCP server).
- Not an AI detector. Heuristic rules, uncalibrated thresholds, no dictionary. These limits are part of the product's honesty and must stay visible.
- Released: v0.1.0 is on PyPI (`pipx install yontu`, `uvx yontu`), in the MCP Registry as `io.github.senrecep/yontu`, and on GitHub Releases with `yontu-skill.zip` for claude.ai upload, the wheel, the sdist and SHA256SUMS. claude.ai MCP support is planned for v0.2.

## Brand Commitments

- Name is always lowercase: yontu. From *yontmak*, to carve or whittle: "Türkçe metni yontar: biçim verir, inceltir."
- Voice follows yontu's own rules: plain words, no hype, no em dash inside a sentence, no bold-label bullet lists, no exclamation marks, no adjective triads.
- Logo palette from the existing mark: navy #1F2A44, cream #F4EBDD, burnt orange #E8833A. Final logo not chosen; candidates are a beveled "y" with an orange shaving. The mark must stay swappable from one component.
- Author: senrecep. Repository: https://github.com/senrecep/yontu. License: MIT.

## Evidence on Hand

- Real before/after pairs in `skills/yontu/references/ornekler.md`, all passing `yontu compare`.
- Genuine CLI output from running `yontu lint`, `compare`, `explain`, `stats` on those samples.
- Per-agent status table in `integrations/README.md`, context cost measurements in `docs/CONTEXT.md`.
- Social preview image (1280x640) and placeholder logo SVG.
- No testimonials, user counts, download numbers, stars or benchmarks exist. Do not fabricate them.

## Product Principles

1. Meaning first: a rewrite never adds a fact, and the gate proves it.
2. Turkish on its own terms: rules come from TDK and Turkish usage, not from English lists.
3. Severity matches evidence: a rule cannot shout louder than its source.
4. Small and offline: no dependencies, no network, minimal context cost.
5. Say what it cannot do: not a detector, heuristics, uncalibrated.

## Accessibility & Inclusion

WCAG 2.2 AA. Turkish is the primary language (`/`), English at `/en/`; correct `lang` attributes and `hreflang` alternates. Fonts must render every Turkish glyph (ı İ ş Ş ğ Ğ ç Ç ö Ö ü Ü â î û). Respect `prefers-reduced-motion` and `prefers-color-scheme`.
