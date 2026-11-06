# OpenCode

## Skill

OpenCode reads `.agents/skills/`, `.claude/skills/` and `.opencode/skills/` in the project, and `~/.agents/skills/`, `~/.claude/skills/` and `~/.config/opencode/skills/` globally. Installing for Codex or Claude Code covers it:

```
scripts/install.sh --codex --apply
```

## MCP

Merge `opencode.json` into the project's `opencode.json` or `~/.config/opencode/opencode.json`. Note that `command` is an array and the key is `mcp`.

## Hooks

None in v1. OpenCode hooks are JS plugins, and how a plugin returns findings to the model is not tested yet.

## Status

- MCP: `opencode mcp list` shows `yontu` as connected with this config (OpenCode, 2026-11-06).
- Skill paths: from the OpenCode docs.
