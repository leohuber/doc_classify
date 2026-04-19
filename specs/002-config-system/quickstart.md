# Quickstart: Configuration System

**Feature**: 002-config-system

## Usage

### Reading Configuration (Application Code)

```python
from doc_classify.config import get_config

config = get_config()

# Permanent config (from pyproject.toml / package metadata)
print(config.permanent.version)   # e.g., "0.2.0"
print(config.permanent.name)      # "doc-classify"

# User-adaptable config (from TOML file)
print(config.user.log_level)      # "info" (default)
print(config.user.output_format)  # "text" (default)
```

### Accessing Individual Config Types

```python
from doc_classify.config import get_permanent, get_user_config

# Permanent only
perm = get_permanent()
print(perm.version)

# User config only
user = get_user_config()
print(user.log_level)
```

### Default Config File

On first access, if no config file exists, one is created automatically:

**Development mode** (`.tmp/config/config.toml`):
```toml
log_level = "info"
output_format = "text"
```

**Production mode** (`~/.doc-classify/config.toml`):
Same content, different location.

### Mode Switching (Release Workflow)

```bash
# Before release: switch to production mode
./set-mode-prod.zsh

# After release: revert to development mode
./set-mode-dev.zsh
```

## Development

### Running Tests

```bash
uv run pytest tests/test_config/
```

### Lint & Format

```bash
uv run ruff check src/doc_classify/config/ tests/test_config/
uv run ruff format --check src/doc_classify/config/ tests/test_config/
```
