# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
| < 0.1   | No        |

Fixes ship as patch releases.

## Scope

yontu is an offline linter. It reads the text you give it and never sends it anywhere: the core package uses the Python standard library and makes no network calls at runtime. The MCP server runs over local stdio and opens no port. Hooks read files on your machine and print findings.

Reports that matter most: code execution or file access beyond the path you passed, a crafted input that hangs the linter (regular expression backtracking), unsafe handling in `install.sh` or the hook commands, and anything that makes the package reach the network.

A wrong finding or a missed misspelling is not a vulnerability. Use the false positive issue template for those.

## Reporting a vulnerability

Preferred: open a private advisory at https://github.com/senrecep/yontu/security/advisories and choose "Report a vulnerability". Include the affected version, steps to reproduce and a suggested fix if you have one.

Fallback: email **me@senrecep.com** with the subject `[SECURITY] yontu`.

I aim to reply within 72 hours. Please do not disclose the issue publicly until a fix is released. The advisory is published after the release.
