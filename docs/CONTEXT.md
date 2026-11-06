# Context cost

What yontu puts in an agent's context, when, and how to keep it small.

Tokens are estimates: characters divided by 3.6, rounded up. Turkish text tokenizes worse than English, so treat every number as a floor. "Before" is the pre-0.1.0 layout; "after" is this tree. The method: count the characters an agent would receive for each item. MCP schemas and prompts are counted as `json.dumps` output with its default spacing. Tool names are counted with the `mcp__plugin_yontu_yontu__` prefix that Claude Code gives a plugin's server; after `claude mcp add yontu` the prefix is `mcp__yontu__` and the 3 names cost about 21. The "After" column was measured again on 2026-11-06.

## Layers

| Layer | Loads | Before | After |
|---|---|---|---|
| Skill name and description | always (skill listing) | 214 | 151 |
| Slash commands `/turkcelestir`, `/yontu-lint` | always (Claude Code listing) | 53 | 0 (`disable-model-invocation`) |
| MCP instructions | always, when the server is on | 115 | 100 |
| MCP tool names | always, with tool search (Claude Code) | 83 (8 tools) | 32 (3 tools) |
| MCP tool schemas | always, in agents without tool search | 1,574 (8 tools) | 785 (3 tools) |
| MCP tool schemas, `YONTU_MCP_TOOLS=full` | same | 1,574 | 1,624 (8 tools) |
| MCP prompts | only when the user picks one | 182 | 182 |
| Hooks | only when they report a finding | 0 | 0 |
| SKILL.md body | when the skill triggers | 3,119 | 2,124 |
| Tür guidance | when the tür is known | 6,881 (`turler.md`, every tür) | 155 to 552 (`turler/<id>.md`, one tür) |
| `turler.md` | id table and detection cues only | 6,881 | 1,151 |
| Other references | when SKILL.md routes to them | 1,147 to 4,421 each | unchanged |
| `get_style_guide` on a reference | MCP call | the whole file | section list (about 150 to 180), then one section |

`claude plugin details` (Claude Code's own estimate, MCP not counted; not re-run after the 2026-11-06 SKILL.md changes):

| Plugin | Always on | On invoke |
|---|---|---|
| `yontu` before | about 240 | skill about 2.8k |
| `yontu` after | about 154 | skill about 1.6k |
| `yontu-lite` | about 129 | skill about 1.6k |

## A typical task

Rewrite a short blog post, run the checklist once. "Lint the input" was measured again on 2026-11-06 on a 144-word blog post with 15 findings.

| Step | Before | After |
|---|---|---|
| Description | 214 | 151 |
| SKILL.md body | 3,119 | 2,124 |
| Tür guidance | 6,881 | 510 |
| Lint the input | 1,043 (JSON) | 476 (text) |
| Lint the rewrite | 175 (JSON) | 80 (text) |
| Compare | 170 (JSON) | 70 (text) |
| Text in and out | 502 | 502 |
| Total | 12,104 | 3,913 |

With JSON output in both columns the after total was 4,652 before the 2026-11-06 rule and SKILL.md changes; it was not measured again. The skill now asks for text output; `--format json` is there when character offsets are needed. Through MCP, `lint_text` returns trimmed findings (576 against 903 before); `detail: true` returns every field.

In a measured run, the peak context was about 21.5k tokens with the split skill. The number of turns moves the total more than the size of any one file above.

## What loads when

1. Session start: the skill description. With the MCP server, also its instructions and either the 3 tool names (tool search) or the 3 schemas.
2. The user asks for Turkish text work: the SKILL.md body.
3. The tür is known: one file under `references/turler/`.
4. Only if needed: one other reference, picked from the table at the end of SKILL.md. Through MCP, `get_style_guide` returns a section list first and one section on the second call.
5. Hooks stay silent unless they find a TDK error or a chatbot artifact.

## Choosing a profile

- lite: the skill alone. The skill runs the linter through the shell, so most agents need nothing else. Claude Code: `/plugin install yontu-lite@yontu`. Other agents: `scripts/install.sh --<agent> --profile lite --apply`.
- standard: lite plus hooks, for feedback after edits and replies. `install.sh --profile standard` prints the hook config to merge.
- full: standard plus the MCP server, for agents without a shell or when you want tool calls. Claude Code: `/plugin install yontu@yontu`. Elsewhere `install.sh --profile full` prints both configs.
- `YONTU_MCP_TOOLS=full` in the server env lists all 8 MCP tools. Without it only `lint_text`, `compare_texts` and `get_style_guide` are listed. The server still answers `fix_text`, `text_stats`, `explain_rule`, `list_profiles` and `get_profile`, but most clients show the model only listed tools, so set the variable if you need them.

Install `yontu` or `yontu-lite` in Claude Code, not both.

## Not verified

- Claude Code: the always-on figures come from `claude plugin details` and the docs. Tool search deferring MCP schemas is the documented default; it was not measured in a live session.
- Codex: probably loads every MCP tool schema at start. Not checked.
- Cursor, Antigravity, Windsurf, Copilot, Cline, Zed: how they load skills and MCP tools was not checked.
- Gemini CLI: activating a skill also adds its folder listing. The split raised that listing from 25 files (about 180 tokens) to 53 files (about 410 tokens). The net is still far smaller than reading `turler.md` whole, but the listing cost was computed, not observed.
- MCP prompts are assumed to stay out of context until picked.
