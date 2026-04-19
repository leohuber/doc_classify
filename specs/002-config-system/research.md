# Research: Configuration System

**Feature**: 002-config-system
**Date**: 2026-04-19

## R1: Permanent Config Access Method

**Decision**: Use `importlib.metadata` (stdlib) to read permanent config values originating from `pyproject.toml`.

**Rationale**: The app already uses `importlib.metadata.version("doc-classify")` in `cli.py`. This approach works in both development mode (editable install via `uv sync`) and production mode (installed from wheel). Parsing `pyproject.toml` directly would break in production where the file isn't at a predictable path.

**Alternatives considered**:
- Direct `pyproject.toml` parsing via `tomllib`: Only works when file is accessible (development); breaks for installed packages. Rejected.
- Embedding values at build time via `__version__` pattern: Duplicates what `importlib.metadata` already provides. Rejected.

## R2: TOML Writing Strategy (Default Config Creation)

**Decision**: Write default config as a simple string template. No additional dependency for TOML writing.

**Rationale**: The initial config has only 2 keys (`log_level`, `output_format`). A string template like `log_level = "info"\noutput_format = "text"\n` is trivially correct TOML. Adding `tomli-w` as a dependency for 2 lines of output is unnecessary overhead.

**Alternatives considered**:
- `tomli-w` PyPI package: Full TOML writer. Overkill for 2 keys; adds external dependency. Rejected for v1 but acceptable if schema grows significantly.
- JSON config format: Inconsistent with project's TOML-centric approach (`pyproject.toml`). Rejected.

## R3: Project Root Detection (Development Mode)

**Decision**: In development mode, resolve the project root by walking up from the config module's `__file__` location to find `pyproject.toml`. Cache the result.

**Rationale**: The config sub-package lives at `src/doc_classify/config/`. Walking up 3 levels from `__file__` reaches the repo root. Validating by checking for `pyproject.toml` ensures correctness. This mirrors common Python project patterns.

**Alternatives considered**:
- `os.getcwd()`: Fragile; depends on where the user runs the command. Rejected.
- Environment variable: Adds configuration burden. Rejected.
- Hardcoded relative path: Breaks if project structure changes. Rejected.

## R4: Mode Constant Location and Script Mechanism

**Decision**: Store `MODE = "development"` in `src/doc_classify/config/_mode.py`. The zsh scripts use `sed` to toggle the value in-place.

**Rationale**: A dedicated `_mode.py` file isolates the mode constant, making sed replacement safe (no risk of matching other strings). The file is small and single-purpose, aligning with Constitution Principle II (Modularity).

**Alternatives considered**:
- Constant in `__init__.py`: Risks sed matching unrelated content. Rejected.
- Constant in a separate non-Python file: Requires custom loading logic. Rejected.

## R5: User Config File Name

**Decision**: `config.toml` — placed at `.tmp/config/config.toml` (development) or `~/.doc-classify/config.toml` (production).

**Rationale**: Clear, conventional name. Consistent with TOML format. Easy to discover.

**Alternatives considered**:
- `settings.toml`: Less intuitive for a CLI tool. Rejected.
- `doc-classify.toml`: Redundant with the parent directory name. Rejected.

## R6: Validation Approach

**Decision**: Define allowed values as constants in `_defaults.py`. Validate on load using a simple schema (dict mapping key names to allowed value sets or type constraints). Raise `ConfigValidationError` with key name and expected format.

**Rationale**: For 2 keys with enumerated values, a lightweight custom validation is simpler than pulling in a schema library (pydantic, attrs). Extensible by adding entries to the schema dict.

**Alternatives considered**:
- Pydantic/attrs: Heavy dependency for 2 fields. Rejected for v1.
- No validation (trust user): Violates FR-012. Rejected.
