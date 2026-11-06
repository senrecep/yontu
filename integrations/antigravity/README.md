# Google Antigravity (app, IDE, CLI)

## Skill

Antigravity reads `.agents/skills/<name>/` in the workspace and `~/.gemini/config/skills/<name>/` globally.

```
scripts/install.sh --antigravity --apply
```

## Rule (optional)

Copy `yontu-rule.md` to `.agents/rules/yontu.md`. A rule without a valid `trigger` is dropped silently, and a `model_decision` rule needs a `description`.

## MCP

Merge `mcp_config.json` into `~/.gemini/config/mcp_config.json` (global) or `<workspace>/.agents/mcp_config.json`.

## Hooks (opt-in)

Antigravity's `PostToolUse` hook has no feedback channel: it must return `{}`. yontu therefore ships no edit hook for it.

`hooks.json` holds one disabled Stop hook. Copy it to `.agents/hooks.json` or `~/.gemini/config/hooks.json` and set `"enabled": true` to use it. It runs in block mode: when the last reply has a TDK error or a chatbot artifact, it returns `decision: continue` with the findings as the reason. Otherwise it returns `decision: allow`. It never continues when `terminationReason` is anything other than `NO_TOOL_CALL`. Without `YONTU_STOP_MODE=block` (the default advisory mode) the hook only logs to stderr and returns `decision: allow`.

The hook command runs through `sh -c` in the directory that holds `hooks.json`.

## Status

- Hook file layout, `PostToolUse` returning `{}`, Stop `decision`/`reason` and camelCase payloads: from the hooks reference embedded in the `agy` CLI, read on 2026-11-06. Not run in a session.
- How yontu finds the last reply: Antigravity's Stop payload has no reply field, so yontu reads the last assistant message from `transcriptPath`. The transcript format is not tested yet, and when yontu cannot read it the hook stays quiet.
- Antigravity has no `stop_hook_active` flag. Repeated continues end at Antigravity's own forced-continuation limit.
- MCP config path and shape: from the Antigravity docs, not run.
