#!/usr/bin/env zsh
# Switch configuration mode to production before a release.
# Idempotent: running when already in production is a no-op.

set -euo pipefail

SCRIPT_DIR="${0:a:h}"
PROJECT_ROOT="${SCRIPT_DIR:h}"
MODE_FILE="${PROJECT_ROOT}/src/doc_classify/config/_mode.py"

if [[ ! -f "$MODE_FILE" ]]; then
    echo "Error: Mode file not found at ${MODE_FILE}" >&2
    exit 1
fi

if grep -q 'MODE.*=.*"production"' "$MODE_FILE"; then
    echo "Mode is already set to production — nothing to do."
    exit 0
fi

sed -i '' 's/MODE.*=.*"development"/MODE: Literal["development", "production"] = "production"/' "$MODE_FILE"

echo "Mode switched to production."
