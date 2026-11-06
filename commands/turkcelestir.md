---
description: Türkçeleştir, then lint and check fidelity
disable-model-invocation: true
argument-hint: "[file path or text] [--tur ID]"
---

Translate or adapt the input below into natural Turkish for its real reader, using the yontu skill.

Input: $ARGUMENTS

If the input is a file path, read the file. If it names a tür with `--tur`, use that profile;
otherwise infer the tür from the text and say which one you used.

1. Write a faithful first translation. If the input is already Turkish, this step is the input itself.
2. Lint it with the yontu MCP tool `lint_text` (or `python3 "${CLAUDE_PLUGIN_ROOT}/skills/yontu/scripts/yontu" lint --tur ID -`).
   Fix every `tdk` error. Treat `ai-iz`, `stil` and `yogunluk` findings as suggestions.
3. Improve the style for the tür. Keep every fact, number, date, name, negation and modality.
4. Run `compare_texts` with the first translation as old and your final text as new.
   Revert any edit it reports as `error`. Check each `warning` by hand.
5. Return only the final Turkish text. If the input was a file, show the text and ask before writing it back.
