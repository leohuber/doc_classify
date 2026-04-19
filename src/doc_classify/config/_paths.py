"""Path resolution for mode-dependent configuration directories.

In **development** mode the user-adaptable config lives under the
project's ``.tmp/config/`` directory.  In **production** mode it lives
under ``~/.doc-classify/``.
"""

from __future__ import annotations

from pathlib import Path

from doc_classify.config._mode import DEVELOPMENT, get_mode

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------
DEV_CONFIG_SUBDIR: str = ".tmp/config"
PROD_CONFIG_DIR: str = "~/.doc-classify"

# Cached project root (computed once)
_project_root: Path | None = None


def _find_project_root() -> Path:
    """Walk up from the config package to locate the repository root.

    The root is identified by the presence of ``pyproject.toml``.

    Returns:
        Absolute path to the project root directory.

    Raises:
        FileNotFoundError: If ``pyproject.toml`` cannot be found in any
            ancestor directory.
    """
    global _project_root  # noqa: PLW0603
    if _project_root is not None:
        return _project_root

    current = Path(__file__).resolve().parent
    for ancestor in (current, *current.parents):
        if (ancestor / "pyproject.toml").is_file():
            _project_root = ancestor
            return _project_root

    msg = "Cannot locate project root (no pyproject.toml found in ancestors)"
    raise FileNotFoundError(msg)


def get_config_dir() -> Path:
    """Return the directory where user-adaptable config is stored.

    Returns:
        Absolute ``Path`` to the config directory for the active mode.
    """
    if get_mode() == DEVELOPMENT:
        return _find_project_root() / DEV_CONFIG_SUBDIR
    return Path(PROD_CONFIG_DIR).expanduser()
