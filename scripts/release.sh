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

echo "Pre-flight checks passed ✓"

# ── Version bump ─────────────────────────────────────────────────────
echo ""
echo "Select version bump type:"
echo "  1) major"
echo "  2) minor"
echo "  3) patch"
read -p "Enter choice (1-3): " bump_choice

case "${bump_choice}" in
    1)
        bump_type="major"
        ;;
    2)
        bump_type="minor"
        ;;
    3)
        bump_type="patch"
        ;;
    *)
        echo "Error: Invalid choice. Please select 1, 2, or 3." >&2
        exit 1
        ;;
esac

echo "Bumping ${bump_type} version ..."
python3 -c "
import re, pathlib
path = pathlib.Path('${PROJECT_ROOT}/pyproject.toml')
content = path.read_text()
match = re.search(r'version\s*=\s*[\"\'](.*?)[\"\']', content)
if not match:
    exit(1)
version = match.group(1)
parts = version.split('.')
major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

if '${bump_type}' == 'major':
    major += 1
    minor = 0
    patch = 0
elif '${bump_type}' == 'minor':
    minor += 1
    patch = 0
else:
    patch += 1

new_version = f'{major}.{minor}.{patch}'
new_content = re.sub(
    r'version\s*=\s*[\"\'](.*?)[\"\']',
    f'version = \"{new_version}\"',
    content,
    count=1
)
path.write_text(new_content)
print(f'Version bumped: {version} → {new_version}')
"

# ── Set production mode ──────────────────────────────────────────────
echo "Running set-mode-prod.zsh ..."
if [[ -f "${PROJECT_ROOT}/../set-mode-prod.zsh" ]]; then
    bash "${PROJECT_ROOT}/../set-mode-prod.zsh"
elif [[ -f "${PROJECT_ROOT}/scripts/set-mode-prod.zsh" ]]; then
    bash "${PROJECT_ROOT}/scripts/set-mode-prod.zsh"
else
    echo "Warning: set-mode-prod.zsh not found, skipping." >&2
fi

# ── Commit version bump ──────────────────────────────────────────────
echo "Committing version bump ..."
git add "${PROJECT_ROOT}/pyproject.toml"
git commit -m "chore: bump version to ${bump_type}"

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

# ── Set development mode and commit ──────────────────────────────────
echo "Running set-mode-dev.zsh ..."
if [[ -f "${PROJECT_ROOT}/../set-mode-dev.zsh" ]]; then
    bash "${PROJECT_ROOT}/../set-mode-dev.zsh"
elif [[ -f "${PROJECT_ROOT}/scripts/set-mode-dev.zsh" ]]; then
    bash "${PROJECT_ROOT}/scripts/set-mode-dev.zsh"
else
    echo "Warning: set-mode-dev.zsh not found, skipping." >&2
fi

echo "Committing development mode changes ..."
git add -A
git commit -m "chore: revert to development mode"

echo ""
echo "✓ Released ${TAG} successfully!"
