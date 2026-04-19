"""Validation logic for user-adaptable configuration values.

Validates parsed TOML data against the schema defined in
``_defaults.py``.  Unknown keys trigger a warning but are silently
dropped to maintain forward compatibility.
"""

from __future__ import annotations

import logging
from typing import Any

from doc_classify.config._defaults import CONFIG_SCHEMA
from doc_classify.config._exceptions import ConfigValidationError

logger = logging.getLogger(__name__)


def validate_config(data: dict[str, Any]) -> dict[str, str]:
    """Validate user config data against the known schema.

    Args:
        data: Raw key/value pairs parsed from the TOML config file.

    Returns:
        A new dict containing only the recognised keys with their
        validated (string) values.

    Raises:
        ConfigValidationError: If a known key has a value outside its
            allowed set.
    """
    validated: dict[str, str] = {}

    for key, value in data.items():
        if key not in CONFIG_SCHEMA:
            logger.warning("Unknown config key %r — ignoring.", key)
            continue

        allowed = CONFIG_SCHEMA[key]
        str_value = str(value)

        if str_value not in allowed:
            sorted_allowed = ", ".join(sorted(allowed))
            raise ConfigValidationError(
                key=key,
                value=str_value,
                allowed=sorted_allowed,
            )

        validated[key] = str_value

    return validated
