# Contributing

Issues and pull requests are welcome in English or Turkish.

## Setup

No dependencies. Python 3.9 or newer is enough.

```
git clone https://github.com/senrecep/yontu
cd yontu
python3 -m unittest discover -s tests
```

Run the suite on the oldest supported Python too (3.9) before you open a pull request. If you change a plugin or marketplace file, run `claude plugin validate . --strict` from the repository root. The root holds `.claude-plugin/`, so do not point it at `skills/yontu`. To run the tests before every commit, enable the repository hook once: `git config core.hooksPath .githooks`.

The CLI runs from the checkout without installing:

```
python3 skills/yontu/scripts/yontu lint FILE
```

## Layout

| Path | Contents |
|---|---|
| `skills/yontu/SKILL.md` | The skill: workflow, hard rules, output format |
| `skills/yontu/references/` | Reference files the agent reads on demand |
| `skills/yontu/references/turler/` | One guide per genre (tür); `turler.md` is the index |
| `skills/yontu/scripts/yontu/` | The Python package: engine, CLI, MCP server, hooks |
| `skills/yontu/scripts/yontu/data/` | `rules_tdk.json`, `rules_ai.json`, `lexicon.json` (concision), `profiles.json`, `ozel_adlar.json` (proper names for KS-03) |
| `tests/`, `tests/fixtures/` | unittest suite, human-register reference texts per genre, before and after pairs |
| `integrations/<agent>/` | Config and hook files per agent |

There is one copy of the code. `pyproject.toml` packages `skills/yontu/scripts/yontu` directly, with `SKILL.md` and `references/` inside the wheel.

## Adding or changing a rule

Each rule is a JSON object in `data/`. Before you open a pull request:

1. Give it a unique `id`, a `layer` (`tdk`, `ai-iz`, `stil` or `yogunluk`), a `level` and an `evidence` label.
2. Cite a `source`. A `tdk` rule must use `evidence: "kaynak"` and name the TDK Yazım Kılavuzu section or the Güncel Türkçe Sözlük entry. For a dictionary entry, add the date you checked it (`gts, 2026-11-05 sorgusu`).
3. Respect the level ceilings:
   - Only the `tdk` layer may use `error` or carry an autofix.
   - Autofix only where the rule is deterministic and false positives are near zero. Never autofix a dictionary redirect.
   - `hipotez` rules and every `yogunluk` rule stay at `info`. `hakem` rules go up to `warning` at most.
   - A rule moves above that ceiling only after calibration on human text (see [ROADMAP.md](ROADMAP.md)).
4. Add `examples.pos` (text the rule must catch) and `examples.neg` (text it must leave alone). Every rule needs at least one `pos` example. The suite checks both lists.
5. Run the clean human-register fixtures in `tests/fixtures/insan/` and make sure the new rule does not fire there. A rule that flags clean text needs a narrower pattern or a lower level.
6. Write the `message` and `suggestion` in Turkish that passes `yontu lint --layer tdk` with no errors.

The code stays standard library only and makes no network calls at runtime.

## Profiles and examples

Profiles live in `data/profiles.json`. A change to a threshold needs a reason: a measured source or a fixture that shows the problem.

Each genre has exactly one guide, `references/turler/<id>.md`, and a row in `turler.md`. A new genre needs both. The suite checks that every profile has its guide and that the examples in it pass the linter.

Before and after pairs (`references/ornekler.md`, `tests/fixtures/sadakat/`) must pass `yontu compare` with no errors. The "after" text may not add a fact, number, name, date, example or claim that the "before" text lacks.

## Releasing

Releases are automated with release-please. Commit messages on `main` use Conventional Commits (`feat:`, `fix:`, `perf:`; `feat!:` or a `BREAKING CHANGE:` footer for breaking changes). After each push, `.github/workflows/release.yml` opens or updates a release PR that bumps the version in every file (`scripts/check-versions.py` lists them and CI fails if they drift) and prepends the entry to `CHANGELOG.md`. Merging that PR tags `vX.Y.Z`, creates the GitHub release and publishes to PyPI and the MCP Registry, and attaches the wheel, sdist, `yontu-skill.zip` and `SHA256SUMS` to the release.

The first release is 0.1.0 through `"initial-version"` in `release-please-config.json`; later versions follow the commit types. A release PR made with the default `GITHUB_TOKEN` does not start CI; close and reopen it, or merge with admin rights. If a publish job fails, use "Re-run failed jobs"; "Re-run all jobs" skips publishing because the release already exists.

One-time setup by the repository owner:

1. PyPI: add a pending publisher at https://pypi.org/manage/account/publishing/ with project `yontu`, owner `senrecep`, repository `yontu`, workflow `release.yml`, environment `pypi`.
2. GitHub: create the environments `pypi` and `mcp-registry` (Settings > Environments). A required reviewer on `pypi` is optional and adds a manual approval before upload.
3. GitHub: turn on "Allow GitHub Actions to create and approve pull requests" (Settings > Actions > General). release-please cannot open its PR without it.

## Human text

The most useful contribution is clean Turkish text written by people, in any genre: abstracts, news, documentation, e-mails, UI strings, commit messages. Calibration needs at least 50 texts per register. Send only text you have the right to share, and say where it came from.

## Writing style for this repository

Docs, messages and commit text follow the rules yontu enforces: plain words, no hype, no em dash inside a sentence, no bold-label bullet lists. Turkish text must pass `yontu lint`.

Commit messages use Conventional Commits, for example `fix(tdk): KS-02 dil adlarında kesme`.
