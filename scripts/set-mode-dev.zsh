#!/usr/bin/env zsh
# Revert configuration mode to development after a release.
# Idempotent: running when already in development is a no-op.

set -euo pipefail

SCRIPT_DIR="${0:a:h}"
MODE_FILE="${SCRIPT_DIR}/src/doc_classify/config/_mode.py"

if [[ ! -f "$MODE_FILE" ]]; then
    echo "Error: Mode file not found at ${MODE_FILE}" >&2
    exit 1
fi

if grep -q 'MODE.*=.*"development"' "$MODE_FILE"; then
    echo "Mode is already set to development — nothing to do."
    exit 0
fi

sed -i '' 's/MODE.*=.*"production"/MODE: Literal["development", "production"] = "development"/' "$MODE_FILE"

echo "Mode reverted to development."
