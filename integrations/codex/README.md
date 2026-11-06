# Codex CLI

## Skill

Codex reads `~/.agents/skills/` and `.agents/skills/` in the project.

```
scripts/install.sh --codex --apply
```

## MCP

Append `config.toml` to `~/.codex/config.toml`, or run:

```
codex mcp add yontu -- yontu mcp
```

Tools appear under the server name `yontu`.

## Hooks

Copy `hooks.json` to `~/.codex/hooks.json` (merge with an existing file) or to `<repo>/.codex/hooks.json` in a trusted project. Codex asks you to review each hook in `/hooks` before it runs, and again when the command changes.

- `PostToolUse` returns `hookSpecificOutput.additionalContext` with the findings for an edited `.md`, `.mdx` or `.txt` file.
- `Stop` returns `systemMessage` only. The Stop output schema has no `additionalContext`. `YONTU_STOP_MODE=block` switches to `decision: block`.

## Status

- MCP config: parsed by `codex mcp list` with this file as the only config.
- Output fields: checked against the JSON schemas embedded in Codex 0.142.0. `PostToolUse` allows `hookSpecificOutput.additionalContext`, Stop allows `decision`, `reason` and `systemMessage`. Input fields `last_assistant_message`, `stop_hook_active`, `tool_name`, `tool_input` come from the same schemas.
- Hook file layout: from the Codex docs. No hook has run in a Codex session.
- Edit tool name `apply_patch`: not tested yet. The matcher also lists `Write|Edit`, and the hook reads paths from `*** Update File:` lines in the patch.
- The top-level `"hooks"` key in a standalone `hooks.json`: not tested yet for the user-level file.
