# doc-classify

Document classification CLI tool.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (for development)
- [gh](https://cli.github.com/) (for releases)

## Development Setup

```bash
# Install all dependencies (creates .venv automatically)
uv sync

# Verify the CLI works
uv run doc-classify --version
uv run doc-classify --help
```

## Common Commands

```bash
uv run doc-classify              # Run the CLI
uv run pytest                    # Run tests
uv run ruff check src/ tests/    # Lint
uv run ruff format --check src/ tests/  # Check formatting
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
└── test_cli.py         # CLI integration tests
```

## Creating a Release

```bash
# Must be on main branch with clean working tree
./release.sh
```

## End-User Installation

```bash
# Download and extract the release zip from GitHub, then:
./install.sh
doc-classify --help
```

For more integration scenarios, see [quickstart.md](specs/001-console-app-frame/quickstart.md).