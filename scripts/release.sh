#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────────────
# release.sh — Build, tag, and publish a GitHub release for doc-classify
#
# Pre-flight checks ensure a clean, reproducible release from main.
# ──────────────────────────────────────────────────────────────────────

# ── Resolve project root (parent of this script's directory) ─────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

# ── Read version from pyproject.toml ─────────────────────────────────
VERSION="$(python3 -c "
import tomllib, pathlib
data = tomllib.loads(pathlib.Path('${PROJECT_ROOT}/pyproject.toml').read_text())
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
(cd "${PROJECT_ROOT}" && uv build)

wheel="$(find "${PROJECT_ROOT}/dist" -name '*.whl' | head -n 1)"
if [[ -z "${wheel}" ]]; then
    echo "Error: No wheel found in dist/ after build." >&2
    exit 1
fi

# ── Bundle zip ───────────────────────────────────────────────────────
echo "Creating ${ZIP_NAME} ..."
mkdir -p "${PROJECT_ROOT}/.tmp"
staging="${PROJECT_ROOT}/.tmp/doc-classify-${VERSION}"
mkdir -p "${staging}"
cp "${wheel}" "${staging}/"
cp "${PROJECT_ROOT}/install.sh" "${staging}/"
(cd "${PROJECT_ROOT}/.tmp" && zip -r "${ZIP_NAME}" "doc-classify-${VERSION}")
rm -rf "${staging}"

# ── Tag and release ──────────────────────────────────────────────────
echo "Creating git tag ${TAG} ..."
git tag "${TAG}"
git push origin "${TAG}"

echo "Publishing GitHub release ..."
gh release create "${TAG}" "${PROJECT_ROOT}/.tmp/${ZIP_NAME}" \
    --title "doc-classify ${VERSION}" \
    --notes "Release ${VERSION}"

# ── Clean up ─────────────────────────────────────────────────────────
rm -rf "${PROJECT_ROOT}/dist/" "${PROJECT_ROOT}/.tmp/"

echo ""
echo "✓ Released ${TAG} successfully!"
