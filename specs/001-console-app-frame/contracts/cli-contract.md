# CLI Contract: doc-classify

**Feature**: 001-console-app-frame
**Date**: 2026-04-18

## Command: `doc-classify`

**Type**: Click Group (extensible — subcommands added in future features)

### Synopsis

```
doc-classify [OPTIONS] [COMMAND]
```

### Global Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--version` | — | flag | — | Display version and exit |
| `--help` | — | flag | — | Display help message and exit |

### Behavior Matrix

| Input | Output | Exit Code | Requirement |
|-------|--------|-----------|-------------|
| `doc-classify` (no args) | Help message with usage and available commands | 0 | FR-003 |
| `doc-classify --help` | Help message with usage and available commands | 0 | FR-003 |
| `doc-classify --version` | `doc-classify, version 0.1.0` | 0 | FR-004, FR-007 |
| `doc-classify --unknown` | Error: `No such option: --unknown` + help text | 2 | FR-005, FR-008 |
| `doc-classify badcommand` | Error: `No such command 'badcommand'` + help text | 2 | FR-005, FR-008 |

### Help Message Format

```
Usage: doc-classify [OPTIONS] COMMAND [ARGS]...

  Doc-classify command-line interface.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

### Version Output Format

```
doc-classify, version 0.1.0
```

The version string is sourced from `importlib.metadata.version("doc-classify")`, which reads from the installed package metadata (originally declared in `pyproject.toml`).

### Error Output Format

Unrecognized options:
```
Error: No such option: --foo
Try 'doc-classify --help' for help.
```

Unrecognized commands:
```
Error: No such command 'foo'.
Try 'doc-classify --help' for help.
```

### Exit Codes

| Code | Meaning | Source |
|------|---------|--------|
| 0 | Success (help displayed, version displayed, command completed) | Click default |
| 1 | Application error (`click.ClickException`) | Click default |
| 2 | Usage error (bad arguments, unknown commands) | Click `UsageError` |

## Script: `install.sh`

### Synopsis

```
./install.sh [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--help` | Display help and exit |

### Behavior Matrix

| Condition | Outcome | Exit Code |
|-----------|---------|-----------|
| Python 3.14+ available | Installs package, creates symlink | 0 |
| Python < 3.14 or missing | Error: minimum version message | 1 |
| Re-run after prior install | Upgrades existing installation | 0 |

### Installation Paths

| Artifact | Path |
|----------|------|
| Virtual environment | `~/.local/share/doc-classify/` |
| Console symlink | `~/.local/bin/doc-classify` |

## Script: `release.sh`

### Synopsis

```
./release.sh
```

### Pre-flight Checks (in order)

| Check | Failure Message | Exit Code |
|-------|----------------|-----------|
| On main branch | "Releases can only be created from the main branch" | 1 |
| Clean working tree | "Working tree has uncommitted changes" | 1 |
| `gh` CLI installed | "`gh` CLI is required but not installed" | 1 |
| `gh` authenticated | "`gh` CLI is not authenticated — run `gh auth login`" | 1 |
| Version tag doesn't exist | "Version v0.1.0 has already been released" | 1 |

### Success Output

| Step | Artifact |
|------|----------|
| Build | `dist/doc_classify-0.1.0-py3-none-any.whl` |
| Bundle | `doc-classify-0.1.0.zip` (wheel + install.sh) |
| Tag | `v0.1.0` |
| Release | GitHub release with zip attached |
