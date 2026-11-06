# Gemini CLI

## Extension (skill and MCP in one step)

The repository root is a Gemini CLI extension (`gemini-extension.json`).

```
gemini extensions install https://github.com/senrecep/yontu
```

Local checkout: `gemini extensions link /path/to/yontu`. The extension loads `skills/yontu` and starts the MCP server with `python3`, so nothing else needs to be on PATH.

The extension also contains the Claude Code `hooks/hooks.json`. Gemini CLI skips its `PostToolUse` and `Stop` entries as unknown event names, so the extension adds no hooks. The install prompt still says the extension has hooks.

## Skill only

```
scripts/install.sh --gemini --apply
```

Or `gemini skills install https://github.com/senrecep/yontu --path skills/yontu`.

## MCP only

Merge `settings.json` into `~/.gemini/settings.json` or `.gemini/settings.json`, or run `gemini mcp add -s user yontu yontu mcp`.

Gemini CLI starts no MCP server, user-level ones included, in a folder you have not trusted. `gemini mcp list` then shows the server as `Disabled`.

## Hooks (opt-in)

Merge `hooks.settings.json` into the same settings file.

- `AfterTool` on `write_file|replace` returns `hookSpecificOutput.additionalContext`. Gemini appends it to the tool result inside `<hook_context>`.
- `AfterAgent` returns `systemMessage` by default, shown to you only. With `YONTU_STOP_MODE=block` it returns `decision: deny`, which makes Gemini send the reason as a new request. It stays quiet when `stop_hook_active` is true.
- Gemini fingerprints project hooks and asks before running a changed one.

## Status

- `settings.json`: `gemini mcp list` shows `yontu ... Connected` in a trusted folder.
- Extension: `gemini extensions validate` passes, and `gemini mcp list` shows `yontu ... Connected` with the extension linked (Gemini CLI 0.58.0, 2026-11-06).
- Hook field names (`tool_input`, `prompt_response`, `stop_hook_active`, `hookSpecificOutput.additionalContext`, `decision: deny`) and tool names `write_file`, `replace`: read from the Gemini CLI 0.58.0 source. Not run in a live session.
