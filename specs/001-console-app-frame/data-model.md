# Data Model: Console Application Frame

**Feature**: 001-console-app-frame
**Date**: 2026-04-18

## Overview

The console application frame has no persistent data storage or complex domain entities. The "data model" consists of configuration metadata and runtime artifacts that flow through the build → release → install → run pipeline.

## Entities

### 1. Package Metadata

**Source**: `pyproject.toml` (single source of truth)

| Field | Type | Value | Description |
|-------|------|-------|-------------|
| `name` | string | `"doc-classify"` | PyPI-style package name (hyphenated) |
| `version` | string | `"0.1.0"` | SemVer version — initial development |
| `requires-python` | string | `">=3.14"` | Minimum Python version constraint |
| `description` | string | `"..."` | One-line project description |
| `dependencies` | list[string] | `["click>=8.1"]` | Runtime dependencies |

**Relationships**:
- Read by `release.sh` to determine release version and zip filename.
- Read at runtime via `importlib.metadata.version("doc-classify")` for `--version` output.
- Read by `install.sh` indirectly (the wheel embeds this metadata).

### 2. CLI Command

**Source**: `src/doc_classify/cli.py`

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string | `"doc-classify"` — the console command name |
| `type` | enum | `click.Group` — extensible command group |
| `options` | list | `--version`, `--help` (built-in) |
| `subcommands` | list | Empty (frame only — future commands attach here) |

**State transitions**: None — the CLI is stateless in the frame. Each invocation is independent.

### 3. Release Artifact

**Source**: Built by `release.sh`

| Attribute | Type | Description |
|-----------|------|-------------|
| `zip_name` | string | `doc-classify-<version>.zip` |
| `contents` | list | Wheel file (`.whl`) + `install.sh` |
| `git_tag` | string | `v<version>` (e.g., `v0.1.0`) |
| `github_release` | string | Created via `gh release create` |

### 4. Installation

**Source**: Created by `install.sh`

| Attribute | Type | Description |
|-----------|------|-------------|
| `venv_path` | path | `~/.local/share/doc-classify/` |
| `symlink_path` | path | `~/.local/bin/doc-classify` |
| `python_min` | string | `3.14` — checked before installation |

## Validation Rules

| Rule | Source | Enforcement |
|------|--------|-------------|
| Version matches SemVer pattern | FR-007 | `pyproject.toml` declaration |
| Python >= 3.14 at install time | FR-010 | `install.sh` version check |
| On main branch for release | FR-017 | `release.sh` branch check |
| Clean working tree for release | FR-017 | `release.sh` git status check |
| Tag does not already exist | FR-018 | `release.sh` tag existence check |
| `gh` CLI authenticated | FR-019 | `release.sh` auth check |

## Entity Relationship Diagram

```text
pyproject.toml
    │
    ├──→ uv build ──→ wheel (.whl)
    │                      │
    │                      ├──→ release.sh ──→ zip + git tag + GitHub release
    │                      │
    │                      └──→ install.sh ──→ venv + symlink
    │
    └──→ importlib.metadata ──→ cli.py --version
```
