# Cline (and Roo Code)

## Skill

Cline reads `.cline/skills/`, `.clinerules/skills/`, `.claude/skills/` and `.agents/skills/` in the project, and `~/.cline/skills/` globally. Roo Code reads `.roo/skills/` and `~/.roo/skills/`.

```
scripts/install.sh --codex --apply    # links ~/.agents/skills/yontu
```

For Cline globally, or for Roo, link the folder yourself, for example `ln -s /path/to/yontu/skills/yontu ~/.cline/skills/yontu`.

## MCP

- Cline IDE: MCP Servers, Configure, "Configure MCP Servers", then merge `cline_mcp_settings.json`.
- Cline CLI: `~/.cline/data/settings/cline_mcp_settings.json` (or `CLINE_MCP_SETTINGS_PATH`).
- Roo Code: `.roo/mcp.json` in the project or the global `mcp_settings.json`, same `mcpServers` shape. Rename `autoApprove` to `alwaysAllow`.

`autoApprove` lists the 3 tools the server shows by default. None of them change anything on disk. For all 8 tools, add `"env": {"YONTU_MCP_TOOLS": "full"}` to the entry; `fix_text`, `text_stats`, `explain_rule`, `list_profiles` and `get_profile` also only return text, so you can approve them too.

## Hooks

None.

## Status

From the Cline and Roo docs. Not run.
