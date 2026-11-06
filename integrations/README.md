# Integrations

yontu ships three things. Each agent can use any subset.

| Part | What it is | How it gets installed |
|---|---|---|
| Skill | `skills/yontu/` (SKILL.md, references, offline linter) | `scripts/install.sh`, `npx skills add`, or a copy |
| MCP server | `yontu mcp`, stdio, no dependencies | one config entry per agent, see below |
| Hooks | `yontu hook --format <agent> --event post-edit\|stop` | Claude Code plugin, or a manual hook file |

Hooks come only with the Claude Code plugin or with a hook file you add yourself. `npx skills add` copies the skill, nothing else. `install.sh` writes only the skill folder; with `--profile standard` or `full` it also prints the hook and MCP config to merge by hand.

## Context cost

Pick the smallest setup that does the job. Token figures are estimates (characters / 3.6); [docs/CONTEXT.md](../docs/CONTEXT.md) has the full table.

| Profile | What loads | Always in context | Claude Code |
|---|---|---|---|
| lite | skill only; the skill runs the linter through the shell | about 130 tokens (skill description) | `/plugin install yontu-lite@yontu`, or `install.sh --profile lite` |
| standard | lite plus the hooks | same; hooks add nothing until they report | `install.sh --profile standard` |
| full | standard plus the MCP server (3 tools) | about 150 plus 100 for the MCP instructions, and up to 785 for tool schemas if the agent loads them upfront | `/plugin install yontu@yontu` |

The MCP server lists `lint_text`, `compare_texts` and `get_style_guide`. Set `YONTU_MCP_TOOLS=full` in its env to list all 8 tools (about 1,620 tokens of schemas). The server still answers the other 5 when called, but most clients show the model only listed tools, so set the variable if you need `fix_text`, `text_stats`, `explain_rule`, `list_profiles` or `get_profile`.

## The `yontu` command

The configs here call `yontu`. Make it available in one of these ways:

- `pipx install yontu` (or `pip install --user yontu`). Puts `yontu` on PATH.
- No install: replace `yontu` with `python3 /path/to/yontu/skills/yontu/scripts/yontu`. In JSON configs that means `"command": "python3"` and the script path as the first argument.

GUI apps (Claude Desktop, some IDEs) often do not see your shell PATH. Use absolute paths there.

## Status per agent

| Agent | Skill | MCP | Hooks | Folder |
|---|---|---|---|---|
| Claude Code | verified | verified | verified (plugin) | [claude-code](claude-code/) |
| Codex CLI | documented | config parsed by `codex mcp list` | output checked against the 0.142.0 schemas, not run in a session | [codex](codex/) |
| Cursor | documented | documented | `postToolUse` documented, tool names not tested yet | [cursor](cursor/) |
| Gemini CLI | verified (extension) | verified (`gemini mcp list`) | fields read from the 0.58.0 source, not run in a session | [gemini-cli](gemini-cli/) |
| Antigravity | documented | documented | Stop only, from the reference in `agy`, not run | [antigravity](antigravity/) |
| Hermes | documented | documented | none (no feedback hook) | [hermes](hermes/) |
| OpenCode | documented | verified (`opencode mcp list`) | none | [opencode](opencode/) |
| Windsurf | documented | path not tested yet | none | [windsurf](windsurf/) |
| GitHub Copilot | documented | standard VS Code shape | `postToolUse` documented, not tested | [copilot](copilot/) |
| Cline | documented | documented | none | [cline](cline/) |
| Zed | not tested yet | documented | none | [zed](zed/) |
| claude.ai web and mobile | zip upload, code execution needed; mobile not tested yet | remote connector planned for v0.2 | none | [claude-ai](claude-ai/) |
| Claude Desktop | zip upload | documented | none | [claude-desktop](claude-desktop/) |
| Any other agent | `AGENTS.md` snippet | any stdio MCP client | none | [generic](generic/) |

"verified" means run against the installed tool on 2026-11-06 (Claude Code, Codex 0.142.0, Gemini CLI 0.58.0, OpenCode). "documented" means taken from the agent's docs, not run. The protocol side of the MCP server is covered by `tests/test_mcp.py`, and every hook format by `tests/test_hook.py`.

## Hook behavior

- `post-edit` reads the edited `.md`, `.mdx`, `.markdown` or `.txt` file from disk and reports at most 3000 characters.
- `stop` lints the last assistant reply with the `sohbet` register.
- Both skip text that is not mostly Turkish prose (code is masked first).
- By default only TDK `error` findings and clear chatbot artifacts (`AI-E6`, `AI-E7`, `AI-E8`) are reported. `YONTU_HOOK_LEVEL=warning` or `info` widens this.
- Stop is advisory by default. `YONTU_STOP_MODE=context` (Claude Code) feeds the findings back to the model, `YONTU_STOP_MODE=block` asks the agent to continue. Neither acts when the agent is already continuing from a stop hook.
- Off switch: `YONTU_DISABLE=1`, or a `.yontu-ignore` file in the project or any parent directory.
- Any internal error prints `{}` and exits 0, so a hook never breaks the agent.
