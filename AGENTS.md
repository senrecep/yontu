# yontu: agent guide

Turkish humanizer and TDK linter. An agent skill, an offline Python CLI (`yontu`), a stdio MCP server and hooks. Standard library only, Python 3.9+. [CONTRIBUTING.md](CONTRIBUTING.md) has the full contributor rules; this file is the short version for coding agents.

## Layout

| Path | Contents |
|---|---|
| `skills/yontu/SKILL.md` | The skill: checklist, hard rules, output format |
| `skills/yontu/references/` | Reference files read on demand; `turler/` holds one guide per genre (tür) |
| `skills/yontu/scripts/yontu/` | The package: `engine.py`, `cli.py`, `mcp.py`, `hook.py`, `fidelity.py`, `metrics.py`, `profiller.py`, `textutil.py`, `paths.py` |
| `skills/yontu/scripts/yontu/data/` | `rules_tdk.json`, `rules_ai.json`, `lexicon.json`, `profiles.json`, `ozel_adlar.json` |
| `tests/` | unittest suite; `tests/ortak.py` holds shared paths and loaders |
| `tests/fixtures/` | `insan/` (human-register reference texts per genre), `sadakat/` (before and after pairs), plus `tdk-ornekler.txt`, `yanlis-bicimler.txt`, `maskeleme.md`, AI-style samples |
| `integrations/<agent>/` | Config and hook files per agent; status table in `integrations/README.md` |
| `.claude-plugin/`, `hooks/`, `commands/` | Claude Code plugin, hooks and slash commands |
| `docs/research/` | Dated background notes, not rule sources. Fix spelling only; keep the findings as dated |

There is one copy of the code. `pyproject.toml` packages `skills/yontu/scripts/yontu` and ships `SKILL.md` and `references/` inside the wheel.

## Commands

Run the suite on the newest and the oldest supported Python:

```
python3 -m unittest discover -s tests
/usr/bin/python3 -m unittest discover -s tests    # macOS system Python 3.9
```

Both must stay green (251 tests today). Run the CLI from the checkout without installing:

```
python3 skills/yontu/scripts/yontu lint FILE [--tur ID] [--layer tdk] [--format json]
python3 skills/yontu/scripts/yontu compare OLD NEW
```

Turkish text you write (docs, rule messages, fixtures) must pass `lint` with no errors. CI runs it on `README.tr.md` and `skills/yontu/SKILL.md`. Run `claude plugin validate . --strict` after changing `.claude-plugin/`.

## Rule layers and limits

Each rule is a JSON object with a unique `id`, a `layer`, a `level` and an `evidence` label.

| Layer | Limit |
|---|---|
| `tdk` | The only layer that may be `error` or carry an autofix. Needs `evidence: "kaynak"` and a `source` naming the Yazım Kılavuzu section or Güncel Türkçe Sözlük entry (with the date checked) |
| `ai-iz` | At most `warning`, never fixed. `hipotez` stays at `info`; `hakem` goes up to `warning` |
| `stil` | At most `warning`, mostly `info`. Never fixed |
| `yogunluk` | Always `info`. Never fixed |

Autofix only where the rule is deterministic and false positives are near zero. Never autofix a dictionary redirect. A rule rises above its ceiling only after calibration on human text (see [ROADMAP.md](ROADMAP.md)). `tests/test_kurallar.py` enforces these limits.

Every rule needs `examples.pos` (text it must catch, at least one) and `examples.neg` (text it must leave alone). After a change, check that the clean files in `tests/fixtures/insan/` stay silent.

## Rules for changes

- No new dependencies in the core package. No network calls at runtime. A build-time script may use the network only if it is kept out of the runtime path.
- Keep the diff small. Do not refactor next to the change.
- A new genre needs a profile in `profiles.json`, a guide `references/turler/<id>.md` and a row in `references/turler.md`.
- Before and after pairs (`references/ornekler.md`, `tests/fixtures/sadakat/`) must pass `yontu compare` with no errors. The "after" text may not add a fact, number, name, date, example or claim.
- Fixtures: one file per case, UTF-8, LF line endings. `insan/` holds human-register reference texts written for the project, not collected from third parties. Do not add machine-written text to it.
- When a fact changes (test count, rule count, agent status), update every doc that states it: `README.md`, `README.tr.md`, `integrations/README.md`, `CHANGELOG.md`.
- Repository prose follows yontu's own rules: plain words, no hype, no em dash inside a sentence, no bold-label bullet lists.
- Commits use Conventional Commits, for example `fix(tdk): KS-02 dil adlarında kesme`. Do not commit secrets or local agent state (`.omc/`, `.claude/settings.local.json`).
