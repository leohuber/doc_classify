"""Permanent (read-only) configuration from installed package metadata.

Values originate from ``pyproject.toml`` and are accessed at runtime
through :mod:`importlib.metadata`, which works for both editable
installs and production wheels.
"""

from __future__ import annotations

import importlib.metadata
from dataclasses import dataclass

_PACKAGE_NAME: str = "doc-classify"


@dataclass(frozen=True)
class PermanentConfig:
    """Read-only configuration sourced from package metadata.

    Attributes:
        version: The installed package version (e.g. ``"0.2.0"``).
        name: The distribution name (``"doc-classify"``).
    """

    version: str
    name: str


def load_permanent_config() -> PermanentConfig:
    """Load permanent configuration from installed package metadata.

    Returns:
        A frozen :class:`PermanentConfig` instance.
    """
    return PermanentConfig(
        version=importlib.metadata.version(_PACKAGE_NAME),
        name=importlib.metadata.metadata(_PACKAGE_NAME)["Name"],
    )
