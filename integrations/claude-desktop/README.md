# Claude Desktop and claude.ai

## MCP

Settings, Developer, Edit Config, then merge `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Use absolute paths. The app does not read your shell PATH. If you installed with pipx, `command` can be the absolute path of `yontu` (for example `/Users/YOU/.local/bin/yontu`) with `args: ["mcp"]`. On Windows use `python` and a Windows path. Restart the app fully after editing.

Logs: `~/Library/Logs/Claude/mcp*.log`.

## Skill

Zip the `skills/yontu` folder (the zip must contain `yontu/SKILL.md`) and upload it under Settings, Capabilities, Skills. The frontmatter uses only spec fields, which the upload requires.

## Hooks

None.

## Status

Config shape from the MCP docs. The server itself is the same one verified in Claude Code. Not run in Claude Desktop.
