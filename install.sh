#!/usr/bin/env bash
set -euo pipefail

# Install doc-classify from a .whl file in the same directory.
# If a previous installation exists it is removed first.

# ── Variables ────────────────────────────────────────────────────────

INSTALL_DIR="${HOME}/.local/share/doc-classify"
BIN_DIR="${HOME}/.local/bin"
SYMLINK="${BIN_DIR}/doc-classify"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Preflight checks ─────────────────────────────────────────────────

# Require Python >= 3.14
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found on PATH." >&2; exit 1
fi

py_version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
py_major="${py_version%%.*}"; py_minor="${py_version##*.}"

if [[ "${py_major}" -lt 3 ]] || { [[ "${py_major}" -eq 3 ]] && [[ "${py_minor}" -lt 14 ]]; }; then
    echo "Error: Python >= 3.14 required (found ${py_version})." >&2; exit 1
fi

# Locate the wheel in the same directory as this script
wheel="$(find "${SCRIPT_DIR}" -maxdepth 1 -name '*.whl' | head -n 1)"
if [[ -z "${wheel}" ]]; then
    echo "Error: No .whl file found in ${SCRIPT_DIR}." >&2; exit 1
fi

# ── Uninstall previous version ───────────────────────────────────────

if [[ -e "${SYMLINK}" ]] || [[ -d "${INSTALL_DIR}" ]]; then
    echo "Removing existing installation..."
    rm -f "${SYMLINK}"
    rm -rf "${INSTALL_DIR}"
fi

# ── Install new version ──────────────────────────────────────────────

echo "Installing $(basename "${wheel}")..."

mkdir -p "${INSTALL_DIR}" "${BIN_DIR}"
python3 -m venv "${INSTALL_DIR}"
"${INSTALL_DIR}/bin/pip" install --quiet "${wheel}"
ln -s "${INSTALL_DIR}/bin/doc-classify" "${SYMLINK}"

echo "doc-classify installed → ${SYMLINK}"

if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo "Note: add ${BIN_DIR} to your PATH:  export PATH=\"${BIN_DIR}:\${PATH}\""
fi
