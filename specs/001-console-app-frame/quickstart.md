# Quickstart: Console Application Frame

**Feature**: 001-console-app-frame
**Date**: 2026-04-18

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (for development)
- [gh](https://cli.github.com/) (for releases)
- Git

## Development Setup

```bash
# Clone the repository
git clone https://github.com/leohuber/doc_classify.git
cd doc_classify

# Install all dependencies (creates .venv automatically)
uv sync

# Verify the CLI works
uv run doc-classify --version
# Output: doc-classify, version 0.1.0

uv run doc-classify --help
# Output: Help message with available commands
```

## Common Development Commands

```bash
# Run the CLI
uv run doc-classify

# Run tests
uv run pytest

# Lint (check)
uv run ruff check src/ tests/

# Format (check)
uv run ruff format --check src/ tests/

# Lint + format (fix)
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Editable install (alternative to uv run)
uv pip install -e .
doc-classify --version
```

## Project Structure

```
pyproject.toml          # Package metadata, deps, tool config
uv.lock                 # Dependency lock (auto-generated)
install.sh              # End-user install script
release.sh              # Maintainer release script

src/doc_classify/
├── __init__.py         # Package init
└── cli.py              # Click CLI entry point

tests/
├── __init__.py
└── test_cli.py         # CLI tests
```

## Creating a Release

```bash
# Must be on main branch with clean working tree
./release.sh

# This will:
# 1. Read version from pyproject.toml
# 2. Build the Python package (uv build)
# 3. Create doc-classify-0.1.0.zip (wheel + install.sh)
# 4. Tag the repo with v0.1.0
# 5. Publish a GitHub release with the zip attached
```

## End-User Installation (from release zip)

```bash
# Download the release zip from GitHub
# Extract it
unzip doc-classify-0.1.0.zip
cd doc-classify-0.1.0/

# Install
./install.sh

# Use
doc-classify --help
doc-classify --version
```
