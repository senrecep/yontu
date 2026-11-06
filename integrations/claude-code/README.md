# Claude Code

The repository root is a Claude Code plugin and a marketplace with two plugins: `yontu` (full) and `yontu-lite` (skill only).

```
/plugin marketplace add senrecep/yontu
/plugin install yontu@yontu
```

Local checkout: `claude --plugin-dir /path/to/yontu`.

The plugin gives you:

- the `yontu` skill
- the `yontu` MCP server (`.mcp.json`), tools appear as `mcp__plugin_yontu_yontu__<tool>`
- `/yontu:turkcelestir` and `/yontu:yontu-lint`
- two hooks (`hooks/hooks.json`): `PostToolUse` on `Write|Edit|MultiEdit` and `Stop`

## Skill only

The marketplace also lists `yontu-lite`: the skill alone, no MCP server, no hooks, no commands. It costs about 130 tokens of always-on context, against about 150 for the full plugin before its MCP server is counted (`claude plugin details`).

```
/plugin install yontu-lite@yontu
```

Install one of the two plugins, not both, or the skill is listed twice.

Without the plugin system, `scripts/install.sh --claude --apply` links `skills/yontu` to `~/.claude/skills/yontu`. No MCP, no hooks.

The two slash commands set `disable-model-invocation`, so their descriptions stay out of the model's skill listing. Run them by name.

The MCP server lists 3 tools by default. Claude Code shows the model only listed tools, so for the other 5, add `"env": {"YONTU_MCP_TOOLS": "full"}` to the server entry in a hand-written MCP config to list all 8. The plugin's own `.mcp.json` uses the default.

## Hooks without the plugin

Add to `~/.claude/settings.json` or `.claude/settings.json`, with your own path:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit|MultiEdit",
        "hooks": [{ "type": "command", "command": "python3",
                    "args": ["/path/to/yontu/skills/yontu/scripts/yontu", "hook", "--format", "claude", "--event", "post-edit"],
                    "timeout": 15 }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "python3",
                    "args": ["/path/to/yontu/skills/yontu/scripts/yontu", "hook", "--format", "claude", "--event", "stop"],
                    "timeout": 15 }] }
    ]
  }
}
```

## Stop modes

| `YONTU_STOP_MODE` | Output | Effect |
|---|---|---|
| `advisory` (default) | `systemMessage` | You see the findings. Claude does not |
| `context` | `systemMessage` plus `additionalContext` | Claude gets the findings and continues once |
| `block` | `decision: block` | Claude must continue and fix |

`context` and `block` act only on TDK errors or chatbot artifacts, and never when `stop_hook_active` is true.

## Verified

- `claude plugin validate .` and `--strict` pass (2026-11-06, Claude Code 2.1.318).
- `yontu-lite` installed from a local marketplace in a clean config. `claude plugin details` shows one skill, about 129 tokens always on and 1.6k on invoke.
- `claude --plugin-dir <copy> mcp list` shows `plugin:yontu:yontu ... Connected`.
- `tests/test_hook.py` runs the exact argv from `hooks/hooks.json` with sample payloads.

Note: `.mcp.json` sits at the root because plugins read it from there. When you open this repository itself as a project, Claude Code also offers that file as a project MCP server, where `${CLAUDE_PLUGIN_ROOT}` is not set. Decline it, or use `--plugin-dir .`.
