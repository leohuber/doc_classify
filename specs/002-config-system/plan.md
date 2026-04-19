# Implementation Plan: Configuration System

**Branch**: `002-config-system` | **Date**: 2026-04-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-config-system/spec.md`

## Summary

Build a `config` sub-package for `doc_classify` that provides dual-mode configuration: development mode (project-local `.tmp/config/`) and production mode (`~/.doc-classify/`). The mode is stored as a source code constant toggled by zsh scripts at release time. Two config types are supported: permanent config via `importlib.metadata` (originating from `pyproject.toml`) and user-adaptable config via TOML files at the mode-dependent path. Initial user config keys: `log_level` and `output_format`.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: Click >=8.1 (existing), tomllib (stdlib, read-only TOML parsing)
**Storage**: TOML files for user config; `importlib.metadata` for permanent config
**Testing**: pytest with Click CliRunner (existing pattern)
**Target Platform**: macOS/Linux CLI
**Project Type**: CLI application
**Performance Goals**: Config loads in <100ms (SC-006)
**Constraints**: No additional PyPI dependencies for TOML writing — use string templates for the simple 2-key config. `tomllib` (stdlib) for reading.
**Scale/Scope**: 2 initial user config keys; extensible by future features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | ✅ PASS | All functions single-purpose, Google docstrings, no magic strings (constants for mode values, config keys, paths), specific exceptions |
| II. Modularity | ✅ PASS | `config` sub-package is a distinct functional domain with SRP modules: mode resolution, path resolution, permanent config, user config, validation, exceptions |
| III. Consistency | ✅ PASS | Config loaded through single mechanism (the config sub-package). PEP 8 naming. Custom exception hierarchy rooted in `ConfigError`. Import ordering enforced by Ruff |
| IV. Readability | ✅ PASS | Type hints on all signatures. Descriptive names. Short functions (<40 lines). Max 3 nesting levels |
| V. Ruff Compliance | ✅ PASS | All code will pass `ruff check` and `ruff format` with `select = ["ALL"]` |

No violations — Complexity Tracking section not needed.

## Project Structure

### Documentation (this feature)

```text
specs/002-config-system/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/doc_classify/
├── __init__.py
├── cli.py
└── config/
    ├── __init__.py      # Public API: get_config(), get_permanent(), get_user_config()
    ├── _mode.py         # MODE constant ("development"/"production"), mode helpers
    ├── _paths.py        # Path resolution: dev (.tmp/config/) vs prod (~/.doc-classify/)
    ├── _permanent.py    # PermanentConfig: reads from importlib.metadata
    ├── _user.py         # UserConfig: reads/writes/validates TOML at mode-dependent path
    ├── _defaults.py     # Default values, schema definition, config key constants
    ├── _validation.py   # Validation logic for user config values
    └── _exceptions.py   # ConfigError hierarchy (base + specific errors)

tests/
├── __init__.py
├── test_cli.py          # Existing
└── test_config/
    ├── __init__.py
    ├── test_mode.py     # Mode constant, mode helpers
    ├── test_paths.py    # Path resolution per mode
    ├── test_permanent.py # Permanent config from metadata
    ├── test_user.py     # User config CRUD, defaults creation
    ├── test_validation.py # Validation rules
    └── test_integration.py # End-to-end config loading

set-mode-prod.zsh        # Switches MODE constant to "production"
set-mode-dev.zsh         # Reverts MODE constant to "development"
```

**Structure Decision**: Extends the existing single-project layout under `src/doc_classify/` with a `config/` sub-package. Each module has a single responsibility per Constitution Principle II. Private modules prefixed with `_` per Constitution guidance. Test directory mirrors source structure.
