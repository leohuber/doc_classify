#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────────────────────────────
# install.sh — Install doc-classify from a release zip
#
# Creates an isolated virtual environment and a symlink so the user
# can invoke `doc-classify` without activating anything.
# ──────────────────────────────────────────────────────────────────────

INSTALL_DIR="${HOME}/.local/share/doc-classify"
BIN_DIR="${HOME}/.local/bin"
SYMLINK="${BIN_DIR}/doc-classify"
MIN_MAJOR=3
MIN_MINOR=14

usage() {
    cat <<EOF
Usage: ./install.sh [OPTIONS]

Install doc-classify into ~/.local/share/doc-classify and create a
symlink at ~/.local/bin/doc-classify.

Options:
  --help    Show this help message and exit
EOF
}

# ── Parse arguments ──────────────────────────────────────────────────
for arg in "$@"; do
    case "${arg}" in
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option '${arg}'" >&2
            usage >&2
            exit 1
            ;;
    esac
done

# ── Check Python version ────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required but not found on PATH." >&2
    exit 1
fi

py_version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
py_major="${py_version%%.*}"
py_minor="${py_version##*.}"

if [[ "${py_major}" -lt "${MIN_MAJOR}" ]] ||
   { [[ "${py_major}" -eq "${MIN_MAJOR}" ]] && [[ "${py_minor}" -lt "${MIN_MINOR}" ]]; }; then
    echo "Error: Python >= ${MIN_MAJOR}.${MIN_MINOR} is required (found ${py_version})." >&2
    exit 1
fi

echo "Found Python ${py_version} ✓"

# ── Locate the wheel ────────────────────────────────────────────────
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
wheel="$(find "${script_dir}" -maxdepth 1 -name '*.whl' | head -n 1)"

if [[ -z "${wheel}" ]]; then
    echo "Error: No .whl file found in ${script_dir}." >&2
    exit 1
fi

echo "Installing from $(basename "${wheel}")"

# ── Create or upgrade virtual environment ────────────────────────────
if [[ -d "${INSTALL_DIR}" ]]; then
    echo "Upgrading existing installation at ${INSTALL_DIR}"
    python3 -m venv --upgrade "${INSTALL_DIR}"
else
    echo "Creating virtual environment at ${INSTALL_DIR}"
    mkdir -p "${INSTALL_DIR}"
    python3 -m venv "${INSTALL_DIR}"
fi

# ── Install the wheel ───────────────────────────────────────────────
"${INSTALL_DIR}/bin/pip" install --quiet --force-reinstall "${wheel}"

# ── Create symlink ──────────────────────────────────────────────────
mkdir -p "${BIN_DIR}"

if [[ -L "${SYMLINK}" ]] || [[ -e "${SYMLINK}" ]]; then
    rm -f "${SYMLINK}"
fi

ln -s "${INSTALL_DIR}/bin/doc-classify" "${SYMLINK}"

echo ""
echo "✓ doc-classify installed successfully!"
echo "  Executable: ${SYMLINK}"

# ── PATH hint ────────────────────────────────────────────────────────
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo ""
    echo "⚠ ${BIN_DIR} is not on your PATH."
    echo "  Add it by appending to your shell profile:"
    echo "    export PATH=\"${BIN_DIR}:\${PATH}\""
fi
