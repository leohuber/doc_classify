#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────────────
# release.sh — Build, tag, and publish a GitHub release for doc-classify
#
# Pre-flight checks ensure a clean, reproducible release from main.
# ──────────────────────────────────────────────────────────────────────

# ── Read version from pyproject.toml ─────────────────────────────────
VERSION="$(python3 -c "
import tomllib, pathlib
data = tomllib.loads(pathlib.Path('pyproject.toml').read_text())
print(data['project']['version'])
")"
TAG="v${VERSION}"
ZIP_NAME="doc-classify-${VERSION}.zip"

echo "Preparing release ${TAG} ..."

# ── Pre-flight checks (ordered) ─────────────────────────────────────
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "${current_branch}" != "main" ]]; then
    echo "Error: Releases can only be created from the main branch (current: ${current_branch})." >&2
    exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Error: Working tree has uncommitted changes." >&2
    exit 1
fi

if ! command -v gh &>/dev/null; then
    echo "Error: \`gh\` CLI is required but not installed." >&2
    exit 1
fi

if ! gh auth status &>/dev/null; then
    echo "Error: \`gh\` CLI is not authenticated — run \`gh auth login\`." >&2
    exit 1
fi

if git rev-parse "${TAG}" &>/dev/null; then
    echo "Error: Version ${TAG} has already been released." >&2
    exit 1
fi

echo "Pre-flight checks passed ✓"

# ── Build ────────────────────────────────────────────────────────────
echo "Building package ..."
uv build

wheel="$(find dist -name '*.whl' | head -n 1)"
if [[ -z "${wheel}" ]]; then
    echo "Error: No wheel found in dist/ after build." >&2
    exit 1
fi

# ── Bundle zip ───────────────────────────────────────────────────────
echo "Creating ${ZIP_NAME} ..."
staging="doc-classify-${VERSION}"
mkdir -p "${staging}"
cp "${wheel}" "${staging}/"
cp install.sh "${staging}/"
zip -r "${ZIP_NAME}" "${staging}"
rm -rf "${staging}"

# ── Tag and release ──────────────────────────────────────────────────
echo "Creating git tag ${TAG} ..."
git tag "${TAG}"

echo "Publishing GitHub release ..."
gh release create "${TAG}" "${ZIP_NAME}" \
    --title "doc-classify ${VERSION}" \
    --notes "Release ${VERSION}"

# ── Clean up ─────────────────────────────────────────────────────────
rm -rf dist/ "${ZIP_NAME}"

echo ""
echo "✓ Released ${TAG} successfully!"
