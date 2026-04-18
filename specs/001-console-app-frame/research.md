# Research: Console Application Frame

**Feature**: 001-console-app-frame
**Date**: 2026-04-18

## Research Task 1: Click CLI Framework for Python 3.14

**Decision**: Use Click >=8.1 as the CLI framework.

**Rationale**:
- Click is the most widely adopted Python CLI framework (mature, battle-tested, extensive docs).
- Fully supports Python 3.14 and 3.14t (free-threading) — confirmed in Click's CI matrix.
- Provides `@click.group()` for extensible command hierarchies — the app frame can grow with subcommands.
- Built-in `@click.version_option()` integrates with `importlib.metadata` for single-source version truth.
- Automatic error handling: unrecognized arguments produce informative error + help text with exit code 2.
- Exit code semantics align with spec: 0 for success, 1 for `ClickException`, 2 for `UsageError`.

**Alternatives considered**:
- **argparse** (stdlib): Viable but verbose for group-based CLIs, no built-in version-from-metadata integration, less ergonomic for growing command sets.
- **Typer**: Built on Click but adds runtime dependency on `typing-extensions`; overkill for a simple frame and adds indirection.
- **rich-click**: Cosmetic enhancement over Click; unnecessary for a frame with no subcommands yet.

**Key pattern**:
```python
import click
from importlib.metadata import version

@click.group()
@click.version_option(version=version("doc-classify"), prog_name="doc-classify")
def main() -> None:
    """Doc-classify command-line interface."""

# Entry point: "doc-classify" = "doc_classify.cli:main"
```

## Research Task 2: uv for Dependency Management and Development Workflow

**Decision**: Use uv for all development workflows (dependency management, venv, build, run). End-user installation uses standard pip (no uv required).

**Rationale**:
- uv is a fast, Rust-based Python package manager that replaces pip + venv + pip-tools.
- `uv sync` resolves and installs all dependencies from `pyproject.toml` + `uv.lock` in seconds.
- `uv build` produces standard wheels and sdists — fully compatible with pip for end-user installation.
- `uv run` executes commands in the project venv without manual activation.
- `uv.lock` provides cross-platform, reproducible dependency resolution.
- `[dependency-groups]` (PEP 735) for dev-only dependencies (ruff, pytest) — not published with the package.

**Alternatives considered**:
- **pip + venv**: Works but lacks lockfile, slower, no integrated build/run workflow.
- **Poetry**: Feature-rich but slower than uv, uses non-standard `poetry.lock`, heavier toolchain.
- **PDM**: Good PEP compliance but smaller ecosystem than uv.

**Key commands**:
```bash
uv sync                  # Install all deps (creates .venv automatically)
uv run pytest            # Run tests in project venv
uv run ruff check src/   # Lint
uv run doc-classify      # Run the CLI
uv build                 # Build wheel + sdist to dist/
```

## Research Task 3: Build Backend Selection

**Decision**: Use hatchling as the build backend.

**Rationale**:
- Modern, lightweight build backend maintained by the PyPA.
- Native support for `src/` layout without extra configuration.
- Automatic package discovery — no need for `[tool.setuptools.packages.find]`.
- Well-integrated with uv (`uv build` delegates to the configured build backend).
- No runtime dependency — only used at build time.

**Alternatives considered**:
- **setuptools**: Ubiquitous but requires extra config for `src/` layout (`[tool.setuptools.packages.find]`), heavier.
- **flit**: Simpler than setuptools but less feature-rich than hatchling.
- **maturin**: For Rust extensions — not applicable.

**Key config**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Research Task 4: Installation Script (install.sh) Strategy

**Decision**: Shell script using standard `python3 -m venv` + `pip install` (no uv required on end-user systems). Venv at `~/.local/share/doc-classify/`, symlink at `~/.local/bin/doc-classify`.

**Rationale**:
- End users should not need to install uv — the install script must work with stock Python 3.14+.
- `~/.local/share/` is XDG-compliant for application data on macOS/Linux.
- `~/.local/bin/` is a standard user-local binary path, often already on `$PATH`.
- Re-installation handled by upgrading existing venv (not deleting + recreating).
- Python version check via `python3 --version` parsing before venv creation.

**Alternatives considered**:
- **pipx**: Requires pipx to be installed — adds a prerequisite.
- **Homebrew formula**: Platform-specific, heavy distribution overhead for a small tool.
- **System-wide install**: Violates isolation principle, requires sudo.

## Research Task 5: Release Script (release.sh) Strategy

**Decision**: Shell script that uses `uv build` for package building, creates a versioned zip (`doc-classify-<version>.zip`) with wheel + `install.sh`, tags with git, and publishes with `gh release create`.

**Rationale**:
- Maintainers already have uv installed (dev dependency) — safe to use `uv build`.
- `gh` CLI is the standard tool for GitHub release automation.
- Version extracted from `pyproject.toml` using Python one-liner (reliable parsing vs regex).
- Pre-flight checks: main branch, clean working tree, tag doesn't exist, `gh` authenticated.
- Zip format chosen for universal extraction (macOS `unzip`, no extra tools).

**Alternatives considered**:
- **GitHub Actions**: Good for CI/CD but spec requires a manual `release.sh` script.
- **twine + PyPI**: Not applicable — distribution is via GitHub releases, not PyPI.
- **setuptools sdist**: `uv build` already produces standard distributions.
