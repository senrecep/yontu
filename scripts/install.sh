#!/bin/sh
# Install the yontu skill into the skill folders of local agents.
# Dry run by default. Touches only the skill folders, never agent configs. No network.
# --profile standard|full also prints the hook and MCP config to merge by hand.
set -u

usage() {
	cat <<'EOF'
Usage: scripts/install.sh [agents] [--profile lite|standard|full] [--apply] [--copy] [--force]

Agents (one or more):
  --claude        ~/.claude/skills/yontu
  --codex         ~/.agents/skills/yontu
  --cursor        ~/.cursor/skills/yontu
  --gemini        ~/.gemini/skills/yontu
  --antigravity   ~/.gemini/config/skills/yontu
  --hermes        ~/.hermes/skills/yontu
  --all           all of the above

Profiles (what the agent loads; docs/CONTEXT.md lists the token cost):
  lite       skill only (default)
  standard   skill, plus the hook config to merge by hand
  full       skill, plus the hook and MCP server config to merge by hand

Options:
  --profile P   one of the profiles above (also --profile=P)
  --apply       make the changes (without it, only print what would happen)
  --copy        copy the skill instead of linking to this checkout
  --force       replace an existing skill folder at the target
  --help        show this text

Only the skill folder is written. Hook and MCP configs are printed, never written.
See integrations/<agent>/README.md.
EOF
}

here=$(cd "$(dirname "$0")" && pwd -P) || exit 1
root=$(dirname "$here")
src="$root/skills/yontu"

if [ ! -f "$src/SKILL.md" ]; then
	echo "error: $src/SKILL.md not found" >&2
	exit 1
fi
if [ -z "${HOME:-}" ]; then
	echo "error: HOME is not set" >&2
	exit 1
fi

apply=0 copy=0 force=0 agents="" profile=lite
add() {
	case " $agents " in
	*" $1 "*) ;;
	*) agents="$agents $1" ;;
	esac
}

set_profile() {
	case "$1" in
	lite | standard | full) profile=$1 ;;
	*) echo "error: --profile takes lite, standard or full" >&2; exit 2 ;;
	esac
}

[ $# -eq 0 ] && { usage; exit 2; }
while [ $# -gt 0 ]; do
	arg=$1
	shift
	case "$arg" in
	--claude | --codex | --cursor | --gemini | --antigravity | --hermes) add "${arg#--}" ;;
	--all) for a in claude codex cursor gemini antigravity hermes; do add "$a"; done ;;
	--profile=*) set_profile "${arg#--profile=}" ;;
	--profile)
		if [ $# -eq 0 ]; then
			echo "error: --profile needs a value" >&2
			exit 2
		fi
		set_profile "$1"
		shift
		;;
	--apply) apply=1 ;;
	--copy) copy=1 ;;
	--force) force=1 ;;
	-h | --help) usage; exit 0 ;;
	*) echo "error: unknown option $arg" >&2; usage >&2; exit 2 ;;
	esac
done
if [ -z "$agents" ]; then
	echo "error: name at least one agent, or --all" >&2
	exit 2
fi

target() {
	case "$1" in
	claude) echo "$HOME/.claude/skills/yontu" ;;
	codex) echo "$HOME/.agents/skills/yontu" ;;
	cursor) echo "$HOME/.cursor/skills/yontu" ;;
	gemini) echo "$HOME/.gemini/skills/yontu" ;;
	antigravity) echo "$HOME/.gemini/config/skills/yontu" ;;
	hermes) echo "$HOME/.hermes/skills/yontu" ;;
	esac
}

# Config to merge by hand: "<file under integrations/> -> <agent config>".
hook_config() {
	case "$1" in
	claude) echo "claude-code/README.md (hooks block) -> ~/.claude/settings.json" ;;
	codex) echo "codex/hooks.json -> ~/.codex/hooks.json" ;;
	cursor) echo "cursor/hooks.json -> ~/.cursor/hooks.json" ;;
	gemini) echo "gemini-cli/hooks.settings.json -> ~/.gemini/settings.json" ;;
	antigravity) echo "antigravity/hooks.json -> ~/.gemini/config/hooks.json (set enabled: true)" ;;
	hermes) echo "none (Hermes has no feedback hook)" ;;
	esac
}

mcp_config() {
	case "$1" in
	claude) echo "run: claude mcp add yontu -- python3 \"$src/scripts/yontu\" mcp" ;;
	codex) echo "codex/config.toml -> ~/.codex/config.toml" ;;
	cursor) echo "cursor/mcp.json -> ~/.cursor/mcp.json" ;;
	gemini) echo "gemini-cli/settings.json -> ~/.gemini/settings.json" ;;
	antigravity) echo "antigravity/mcp_config.json -> ~/.gemini/config/mcp_config.json" ;;
	hermes) echo "hermes/config.yaml (mcp_servers) -> ~/.hermes/config.yaml" ;;
	esac
}

run() {
	if [ "$apply" -eq 1 ]; then
		"$@" || exit 1
	else
		echo "  would run: $*"
	fi
}

[ "$apply" -eq 1 ] || echo "Dry run. Add --apply to make these changes."
echo "Profile: $profile"
status=0
for agent in $agents; do
	dest=$(target "$agent")
	echo "$agent: $dest"
	if [ -L "$dest" ] && [ "$copy" -eq 0 ] && [ "$(readlink "$dest")" = "$src" ]; then
		echo "  already linked"
		continue
	fi
	if [ -e "$dest" ] || [ -L "$dest" ]; then
		if [ "$force" -eq 0 ]; then
			echo "  exists, left unchanged (use --force to replace)"
			status=1
			continue
		fi
		run rm -rf "$dest"
	fi
	run mkdir -p "$(dirname "$dest")"
	if [ "$copy" -eq 1 ]; then
		run cp -R "$src" "$dest"
		if [ "$apply" -eq 1 ]; then
			find "$dest" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null
		fi
	else
		run ln -s "$src" "$dest"
	fi
done

if [ "$profile" = lite ]; then
	cat <<EOF

Profile lite: the skill only, the smallest context cost. The skill calls the linter
through the shell, so it needs no MCP server. For hooks or MCP use --profile standard
or full, or see integrations/<agent>/README.md.
EOF
	exit "$status"
fi

echo
echo "Merge by hand. This script never edits agent configs. Files: $root/integrations/"
for agent in $agents; do
	echo "$agent:"
	echo "  hook: $(hook_config "$agent")"
	if [ "$profile" = full ]; then
		echo "  mcp:  $(mcp_config "$agent")"
	fi
done
echo
echo "The configs call 'yontu'. Without a pip install, use 'python3 \"$src/scripts/yontu\"'"
echo "in its place, followed by 'hook ...' or 'mcp'."
if [ "$profile" = full ]; then
	echo "The MCP server lists 3 tools. Set YONTU_MCP_TOOLS=full in its env for all 8."
	echo "In Claude Code the plugin gives all of this: /plugin marketplace add senrecep/yontu"
fi
exit "$status"
