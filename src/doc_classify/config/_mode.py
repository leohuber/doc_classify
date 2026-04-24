"""Configuration mode constant and helpers.

The ``MODE`` constant is the single indicator of whether the application
runs in development or production mode.  It is toggled by the
``set-mode-prod.zsh`` / ``set-mode-dev.zsh`` scripts via *sed* and
baked into the released wheel.
"""

from __future__ import annotations

from typing import Literal

# Named constants for mode values
DEVELOPMENT: str = "development"
PRODUCTION: str = "production"

# Active mode — toggled by zsh scripts at release time
MODE: Literal["development", "production"] = "development"


def get_mode() -> str:
    """Return the active configuration mode.

    Returns:
        The current mode string (``"development"`` or ``"production"``).
    """
    return MODE
