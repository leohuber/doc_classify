"""User-adaptable configuration stored in a TOML file.

The config file location is determined by the active mode (development
vs production).  On first access the file is created with sensible
defaults if it does not yet exist.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from doc_classify.config._defaults import (
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG_TEMPLATE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_OUTPUT_FORMAT,
    KEY_LOG_LEVEL,
    KEY_OUTPUT_FORMAT,
)
from doc_classify.config._exceptions import ConfigNotFoundError
from doc_classify.config._paths import get_config_dir
from doc_classify.config._validation import validate_config

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class UserConfig:
    """User-modifiable configuration values.

    Attributes:
        log_level: Logging verbosity (debug / info / warning / error).
        output_format: Output presentation (text / json).
    """

    log_level: str = DEFAULT_LOG_LEVEL
    output_format: str = DEFAULT_OUTPUT_FORMAT


def _config_file_path() -> Path:
    """Return the absolute path to the user config TOML file."""
    return get_config_dir() / CONFIG_FILE_NAME


def _create_default_config(path: Path) -> None:
    """Write the default config template to *path*, creating dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DEFAULT_CONFIG_TEMPLATE, encoding="utf-8")


def _ensure_config_exists(path: Path) -> None:
    """Create the default config file if it does not exist yet."""
    if not path.is_file():
        _create_default_config(path)


def load_user_config() -> UserConfig:
    """Load and validate the user-adaptable configuration.

    If the config file does not exist it is created with defaults first.

    Returns:
        A :class:`UserConfig` populated from the TOML file.

    Raises:
        ConfigNotFoundError: If the config directory cannot be resolved.
        ConfigValidationError: If any value fails validation.
    """
    path = _config_file_path()

    try:
        _ensure_config_exists(path)
    except OSError as exc:
        msg = f"Cannot create config file at {path}: {exc}"
        raise ConfigNotFoundError(msg) from exc

    raw = path.read_text(encoding="utf-8")
    data = tomllib.loads(raw)
    validated = validate_config(data)

    return UserConfig(
        log_level=validated.get(KEY_LOG_LEVEL, DEFAULT_LOG_LEVEL),
        output_format=validated.get(KEY_OUTPUT_FORMAT, DEFAULT_OUTPUT_FORMAT),
    )
