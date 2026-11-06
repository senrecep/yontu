---
description: Lint Turkish text with yontu
disable-model-invocation: true
argument-hint: "[file path] [--register SLUG] [--tur ID]"
---

Lint the Turkish text named below with yontu and report the findings.

Input: $ARGUMENTS

Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/yontu/scripts/yontu" lint <file> [--register SLUG] [--tur ID]`,
or call the yontu MCP tool `lint_text` with the file's text.

Report:
- the detected register and tür, and how they were detected
- every `tdk` error with its line, the wrong form and the fix
- warnings, grouped by rule
- a count of info findings, not the full list, unless the user asks for it.

Do not edit the file. Offer `lint --fix --write` for the safe `tdk` fixes only.
