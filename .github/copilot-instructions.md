# doc_classify Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-19

## Active Technologies
- Python 3.14+ + Click >=8.1 (existing), tomllib (stdlib, read-only TOML parsing) (002-config-system)
- TOML files for user config; `importlib.metadata` for permanent config (002-config-system)

- Python 3.14+ + Click >=8.1 (CLI framework) (001-console-app-frame)

## Project Structure

```text
src/
tests/
```

## Commands

cd src && pytest && ruff check .

## Code Style

Python 3.14+: Follow standard conventions

## Recent Changes
- 002-config-system: Added Python 3.14+ + Click >=8.1 (existing), tomllib (stdlib, read-only TOML parsing)

- 001-console-app-frame: Added Python 3.14+ + Click >=8.1 (CLI framework)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
