#!/bin/sh
# Build yontu-skill.zip for upload to claude.ai (Customize > Skills, or Settings > Capabilities).
# The zip holds one folder, yontu/, with SKILL.md directly inside it.
# Usage: scripts/package-skill.sh [OUTPUT.zip]   (default: ./yontu-skill.zip)
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
out=${1:-yontu-skill.zip}
case $out in /*) ;; *) out=$(pwd)/$out ;; esac

command -v zip >/dev/null 2>&1 || { echo "zip not found" >&2; exit 1; }
rm -f "$out"
cd "$root/skills"
zip -rq "$out" yontu -x '*/__pycache__/*' '*.pyc' '*.DS_Store'
echo "wrote $out"
