"""Default values, schema definitions, and config key constants.

This module is the single source of truth for all user-configurable
defaults and the validation schema used by ``_validation.py``.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Config key names
# ---------------------------------------------------------------------------
KEY_LOG_LEVEL: str = "log_level"
KEY_OUTPUT_FORMAT: str = "output_format"

# ---------------------------------------------------------------------------
# Default values
# ---------------------------------------------------------------------------
DEFAULT_LOG_LEVEL: str = "info"
DEFAULT_OUTPUT_FORMAT: str = "text"

# ---------------------------------------------------------------------------
# Allowed values (used for validation)
# ---------------------------------------------------------------------------
VALID_LOG_LEVELS: frozenset[str] = frozenset(
    {
        "debug",
        "info",
        "warning",
        "error",
    }
)

VALID_OUTPUT_FORMATS: frozenset[str] = frozenset({"text", "json"})

# ---------------------------------------------------------------------------
# Validation schema: maps key → allowed value set
# ---------------------------------------------------------------------------
CONFIG_SCHEMA: dict[str, frozenset[str]] = {
    KEY_LOG_LEVEL: VALID_LOG_LEVELS,
    KEY_OUTPUT_FORMAT: VALID_OUTPUT_FORMATS,
}

# ---------------------------------------------------------------------------
# File naming
# ---------------------------------------------------------------------------
CONFIG_FILE_NAME: str = "config.toml"

# ---------------------------------------------------------------------------
# Default config template (written when creating a new config file)
# ---------------------------------------------------------------------------
DEFAULT_CONFIG_TEMPLATE: str = (
    f'{KEY_LOG_LEVEL} = "{DEFAULT_LOG_LEVEL}"\n'
    f'{KEY_OUTPUT_FORMAT} = "{DEFAULT_OUTPUT_FORMAT}"\n'
)
