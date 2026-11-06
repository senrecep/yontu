# Windsurf (Devin Local)

## Skill

Windsurf reads `.windsurf/skills/`, `.devin/skills/` and `.agents/skills/` in the workspace, and `~/.agents/skills/` globally.

```
scripts/install.sh --codex --apply    # links ~/.agents/skills/yontu
```

`AGENTS.md` at the project root is always on. The snippet in `../generic/AGENTS.md` works there.

## MCP

Merge `mcp_config.json` into `~/.codeium/windsurf/mcp_config.json` (classic Windsurf) or `.devin/mcp_config.json` / `~/.config/devin/mcp_config.json` (Devin Local).

## Hooks

None in v1. The hook format is changing during the move to Devin Local.

## Status

Windsurf's docs now live at docs.devin.ai and are moving. The classic MCP path and the stdio shape for Devin are not tested yet. Nothing here was run.
