# Data Model: Configuration System

**Feature**: 002-config-system
**Date**: 2026-04-19

## Entities

### ConfigMode

A string literal representing the active configuration mode.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| value | `Literal["development", "production"]` | Source code constant in `_mode.py`. Default: `"development"`. Modified only by zsh scripts at release time. |

### PermanentConfig

Read-only configuration values sourced from installed package metadata (originating from `pyproject.toml`).

| Attribute | Type | Source | Mutable |
|-----------|------|--------|---------|
| version | `str` | `importlib.metadata.version("doc-classify")` | No |
| name | `str` | `importlib.metadata.metadata("doc-classify")["Name"]` | No |

**Notes**: Accessed via `importlib.metadata`. Works in both development (editable install) and production (installed wheel). Read-only by design (FR-013).

### UserConfig

User-modifiable configuration values stored in a TOML file at the mode-dependent path.

| Attribute | Type | Default | Allowed Values |
|-----------|------|---------|----------------|
| log_level | `str` | `"info"` | `"debug"`, `"info"`, `"warning"`, `"error"` |
| output_format | `str` | `"text"` | `"text"`, `"json"` |

**File location**:
- Development: `.tmp/config/config.toml` (relative to project root)
- Production: `~/.doc-classify/config.toml`

**Lifecycle**:
1. On first access, if config file does not exist → create with defaults
2. On load, parse TOML → validate each key → return UserConfig
3. On validation failure → raise `ConfigValidationError` with key + expected format
4. Unknown keys → log warning, ignore (forward compatibility)

### ConfigManager

Unified access point combining PermanentConfig and UserConfig.

| Responsibility | Details |
|----------------|---------|
| Mode resolution | Reads MODE constant from `_mode.py` |
| Path resolution | Maps mode → config directory path |
| Config loading | Loads PermanentConfig + UserConfig |
| Default creation | Creates config file with defaults if missing |
| Validation | Validates user config on load |

## Relationships

```text
ConfigManager
├── reads → ConfigMode (from _mode.py constant)
├── resolves → config directory path (via _paths.py)
├── loads → PermanentConfig (via importlib.metadata)
└── loads → UserConfig (from TOML file at resolved path)
        ├── validates against → schema in _defaults.py
        └── creates defaults if → file missing
```

## State Transitions

```text
Mode Lifecycle:
  development ──[set-mode-prod.zsh]──► production ──[set-mode-dev.zsh]──► development

UserConfig File Lifecycle:
  absent ──[first access]──► created with defaults ──[user edits]──► modified
                                                    ──[invalid edit]──► validation error on next load
```
