# GitHub Copilot (CLI, VS Code agent mode, cloud agent)

## Skill

Copilot reads `.github/skills/`, `.claude/skills/` and `.agents/skills/` in the project, and `~/.copilot/skills/` and `~/.agents/skills/` globally.

```
scripts/install.sh --codex --apply    # links ~/.agents/skills/yontu
```

## MCP

- VS Code: copy `mcp.json` to `.vscode/mcp.json`. The key is `servers`, not `mcpServers`.
- Copilot CLI: merge `mcp-config.json` into `~/.copilot/mcp-config.json`.

## Hooks

Copy `hooks.json` to `.github/hooks/yontu.json` (the cloud agent reads it from the default branch) or to `~/.copilot/hooks/yontu.json` for the CLI.

- `postToolUse` returns `{"additionalContext": ...}` with findings for an edited prose file. Copilot sends `toolArgs` as a JSON string, and yontu decodes it.
- The hook has no matcher, so it runs after every tool. yontu returns `{}` for read-only tools and for files that are not `.md`, `.mdx`, `.markdown` or `.txt`.
- No `agentStop` hook is shipped. Copilot's only stop output that reaches the model is `decision: block`, which forces another turn. With `YONTU_STOP_MODE=block`, `yontu hook --format copilot --event stop` returns it, and stays quiet when `stop_hook_active` is true. In the default advisory mode the stop hook only logs to stderr, and the model sees nothing.

## Status

- Hook file shape, event names, `toolArgs` as a string and `additionalContext`: from the GitHub docs. Not run.
- Copilot's edit tool names and the fields inside `.vscode/mcp.json` and `~/.copilot/mcp-config.json`: not tested yet.
