# Cursor

## Skill

Cursor reads `~/.cursor/skills/`, `~/.agents/skills/`, `.agents/skills/`, and for compatibility `~/.claude/skills/`. If the Claude Code skill is installed, Cursor already sees it.

```
scripts/install.sh --cursor --apply
```

## Rule (optional)

Copy `yontu.mdc` to `.cursor/rules/yontu.mdc`. The extension must be `.mdc`. It points the agent at the skill when it edits prose files.

## MCP

Copy `mcp.json` to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global), or merge its `mcpServers` entry.

## Hooks

Copy `hooks.json` to `.cursor/hooks.json` or `~/.cursor/hooks.json`.

- `postToolUse` returns `additional_context` with findings for an edited prose file.
- `afterFileEdit` has no documented feedback field. If you wire it, yontu only logs to stderr.
- No `stop` hook is shipped. Cursor's `followup_message` sends a new user message, so it is never passive. With `YONTU_STOP_MODE=block` the stop hook would use it, and it stays quiet when `loop_count` is above 0. In the default advisory mode the stop hook only logs to stderr, and the model sees nothing.

## Status

- Paths, `version: 1`, `postToolUse` and `additional_context`: from the Cursor docs, not run.
- Matcher `Write`: Cursor's edit tool names are not tested yet. yontu ignores read-only tools and non-prose files, so a wider matcher only costs time.
