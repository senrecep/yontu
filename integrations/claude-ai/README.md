# claude.ai (web) and Claude mobile apps

The skill works in claude.ai. The MCP server does not yet: claude.ai connects only to remote servers, and yontu's server is local stdio.

## Skill

1. Build the zip from a checkout:

   ```
   scripts/package-skill.sh          # writes ./yontu-skill.zip
   ```

   Or by hand: `cd skills && zip -r ../yontu-skill.zip yontu -x '*/__pycache__/*'`.

   The zip holds one folder, `yontu/`, with `SKILL.md` directly inside it. The folder name must match the skill name in the frontmatter. Files placed at the zip root instead of inside the folder are rejected.

2. In claude.ai open Customize, then Skills, click `+`, choose Create skill, then Upload a skill, and pick `yontu-skill.zip`. Older versions of the app put the same upload under Settings, Capabilities, Skills. Turn the skill on after upload.

3. Turn on code execution: Settings, Capabilities, "Code execution and file creation" (shown as "Create and edit files" in newer layouts). On Team and Enterprise plans an owner enables it under Organization settings, Plugins & skills. The skill needs it to run the linter in `scripts/`. Without it Claude still reads `SKILL.md` and the references, but cannot run `yontu lint` or `yontu compare`, and falls back to the manual gate in `SKILL.md`.

Skills are available on Free, Pro, Max, Ultra, Team and Enterprise plans. A skill uploaded on claude.ai does not appear in Claude Code or the API; install it there separately (see the [main README](../../README.md)).

## Mobile apps (iOS, Android)

Anthropic's help pages do not say whether the iOS and Android apps run custom skills or sync them from claude.ai. Upload on the web, then ask for a Turkish text check in the mobile app to see if the skill triggers. Treat mobile as not tested until that works for you.

## MCP server

Planned for v0.2: a remote server at `https://yontu.senrecep.com/mcp`, added in claude.ai as a custom connector. It is not live yet. Until then the MCP server runs only in clients that start a local process, such as Claude Desktop ([claude-desktop](../claude-desktop/)) and Claude Code.

## Hooks

None.

## Status

Zip layout checked with `unzip -l` and by running the linter from the unpacked zip. The upload itself, and behavior on mobile, were not run. Menu names come from Anthropic's help center and can change.
