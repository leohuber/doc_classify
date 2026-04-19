"""Configuration sub-package for doc-classify.

Provides a unified API for reading both permanent (package metadata)
and user-adaptable (TOML file) configuration values.

Usage::

    from doc_classify.config import get_config

    config = get_config()
    print(config.permanent.version)
    print(config.user.log_level)
"""

from __future__ import annotations

from dataclasses import dataclass

from doc_classify.config._permanent import PermanentConfig, load_permanent_config
from doc_classify.config._user import UserConfig, load_user_config

__all__ = [
    "AppConfig",
    "PermanentConfig",
    "UserConfig",
    "get_config",
    "get_permanent",
    "get_user_config",
]


@dataclass(frozen=True)
class AppConfig:
    """Combined application configuration.

    Attributes:
        permanent: Read-only values from package metadata.
        user: User-modifiable values from the TOML config file.
    """

    permanent: PermanentConfig
    user: UserConfig


def get_permanent() -> PermanentConfig:
    """Load and return permanent (read-only) configuration.

    Returns:
        A frozen :class:`PermanentConfig` instance.
    """
    return load_permanent_config()


def get_user_config() -> UserConfig:
    """Load, validate, and return user-adaptable configuration.

    Creates the config file with defaults if it does not exist.

    Returns:
        A :class:`UserConfig` instance.
    """
    return load_user_config()


def get_config() -> AppConfig:
    """Load the full application configuration.

    Combines permanent (package metadata) and user-adaptable (TOML file)
    configuration into a single :class:`AppConfig` object.

    Returns:
        An :class:`AppConfig` instance.
    """
    return AppConfig(
        permanent=get_permanent(),
        user=get_user_config(),
    )
