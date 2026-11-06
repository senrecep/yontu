# Hermes Agent

## Skill

Either link the skill into `~/.hermes/skills/`:

```
scripts/install.sh --hermes --apply
```

or point Hermes at a checkout with `skills.external_dirs` (see `config.yaml`). `hermes skills install` also works with the GitHub repository; the exact argument form is not tested yet.

## MCP

Merge the `mcp_servers` block of `config.yaml` into `~/.hermes/config.yaml`. Tools appear as `mcp_yontu_<tool>`. Hermes gives MCP servers only the configured `env` and a safe baseline, so `yontu` must be on that PATH. Otherwise use `command: "python3"` and `args: ["/path/to/yontu/skills/yontu/scripts/yontu", "mcp"]`.

## Hooks

None. Hermes has no hook that returns feedback after an edit or at the end of a turn (`post_tool_call` and `on_session_end` ignore their output). `yontu hook --format hermes` exists for logging and always prints `{}`.

## Status

All of the above is from the Hermes docs. Not run.
