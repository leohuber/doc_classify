#!/usr/bin/env zsh
set -euo pipefail

# ──────────────────────────────────────────────────────────────────────
# release.zsh — Build, tag, and publish a GitHub release for doc-classify
#
# Pre-flight checks ensure a clean, reproducible release from main.
# ──────────────────────────────────────────────────────────────────────

SCRIPT_DIR="${0:a:h}"
PROJECT_ROOT="${SCRIPT_DIR:h}"

# ── Helpers ───────────────────────────────────────────────────────────
read_version() {
    python3 -c "
import tomllib, pathlib
data = tomllib.loads(pathlib.Path('${PROJECT_ROOT}/pyproject.toml').read_text())
print(data['project']['version'])
"
}

run_mode_script() {
    local name="$1"
    if [[ -f "${PROJECT_ROOT}/scripts/${name}" ]]; then
        zsh "${PROJECT_ROOT}/scripts/${name}"
    else
        echo "Warning: ${name} not found, skipping." >&2
    fi
}

# ── Pre-flight checks ────────────────────────────────────────────────
if [[ "$(git rev-parse --abbrev-ref HEAD)" != "main" ]]; then
    echo "Error: Releases can only be created from the main branch." >&2
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

# ── Select bump type ──────────────────────────────────────────────────
echo ""
echo "Select version bump type:"
echo "  1) major"
echo "  2) minor"
echo "  3) patch"
print -n "Enter choice (1-3): "
read bump_choice

case "${bump_choice}" in
    1) bump_type="major" ;;
    2) bump_type="minor" ;;
    3) bump_type="patch" ;;
    *)
        echo "Error: Invalid choice. Please select 1, 2, or 3." >&2
        exit 1
        ;;
esac

# ── Bump version in pyproject.toml ────────────────────────────────────
echo "Bumping ${bump_type} version ..."
python3 -c "
import re, pathlib
path = pathlib.Path('${PROJECT_ROOT}/pyproject.toml')
content = path.read_text()
match = re.search(r'version\s*=\s*[\"\'](.*?)[\"\']', content)
if not match:
    exit(1)
major, minor, patch = (int(x) for x in match.group(1).split('.'))
if '${bump_type}' == 'major':   major += 1; minor = 0; patch = 0
elif '${bump_type}' == 'minor': minor += 1; patch = 0
else:                           patch += 1
new_version = f'{major}.{minor}.{patch}'
path.write_text(re.sub(r'version\s*=\s*[\"\'](.*?)[\"\']', f'version = \"{new_version}\"', content, count=1))
print(f'Version bumped: {match.group(1)} → {new_version}')
"

VERSION="$(read_version)"
TAG="v${VERSION}"
ZIP_NAME="doc-classify-${VERSION}.zip"
echo "Preparing release ${TAG} ..."

# ── Set production mode and commit ────────────────────────────────────
run_mode_script "set-mode-prod.zsh"
git add -A
git commit -m "chore: bump version to ${VERSION}"

# ── Build ─────────────────────────────────────────────────────────────
echo "Building package ..."
(cd "${PROJECT_ROOT}" && uv build)

wheel="$(find "${PROJECT_ROOT}/dist" -name '*.whl' | head -n 1)"
if [[ -z "${wheel}" ]]; then
    echo "Error: No wheel found in dist/ after build." >&2
    exit 1
fi

# ── Bundle zip ────────────────────────────────────────────────────────
echo "Creating ${ZIP_NAME} ..."
staging="${PROJECT_ROOT}/.tmp/doc-classify-${VERSION}"
mkdir -p "${staging}"
cp "${wheel}" "${PROJECT_ROOT}/install.sh" "${staging}/"
(cd "${PROJECT_ROOT}/.tmp" && zip -r "${ZIP_NAME}" "doc-classify-${VERSION}")
rm -rf "${staging}"

# ── Tag and publish release ───────────────────────────────────────────
echo "Creating git tag ${TAG} ..."
git tag "${TAG}"
git push origin "${TAG}"

echo "Publishing GitHub release ..."
gh release create "${TAG}" "${PROJECT_ROOT}/.tmp/${ZIP_NAME}" \
    --title "doc-classify ${VERSION}" \
    --notes "Release ${VERSION}"

# ── Clean up ──────────────────────────────────────────────────────────
rm -rf "${PROJECT_ROOT}/dist/" "${PROJECT_ROOT}/.tmp/"

# ── Set development mode and commit ───────────────────────────────────
run_mode_script "set-mode-dev.zsh"
git add -A
git commit -m "chore: revert to development mode"

echo ""
echo "✓ Released ${TAG} successfully!"
