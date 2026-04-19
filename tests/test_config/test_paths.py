"""Tests for the _paths module."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import doc_classify.config._mode as mode_mod
import doc_classify.config._paths as paths_mod

if TYPE_CHECKING:
    import pytest
from doc_classify.config._paths import (
    DEV_CONFIG_SUBDIR,
    PROD_CONFIG_DIR,
    _find_project_root,
    get_config_dir,
)


def test_find_project_root_locates_pyproject() -> None:
    """_find_project_root() should find the nearest pyproject.toml ancestor."""
    root = _find_project_root()
    assert (root / "pyproject.toml").is_file()


def test_dev_mode_returns_tmp_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """In development mode the config dir is under .tmp/config/."""
    monkeypatch.setattr(mode_mod, "MODE", "development")
    monkeypatch.setattr(paths_mod, "_project_root", None)

    config_dir = get_config_dir()
    assert config_dir.parts[-2:] == (".tmp", "config")
    assert str(config_dir).endswith(DEV_CONFIG_SUBDIR)


def test_prod_mode_returns_home_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    """In production mode the config dir is under ~/.doc-classify/."""
    monkeypatch.setattr(mode_mod, "MODE", "production")

    config_dir = get_config_dir()
    expected = Path(PROD_CONFIG_DIR).expanduser()
    assert config_dir == expected


def test_dev_config_dir_is_absolute(monkeypatch: pytest.MonkeyPatch) -> None:
    """Development config directory should be an absolute path."""
    monkeypatch.setattr(mode_mod, "MODE", "development")
    monkeypatch.setattr(paths_mod, "_project_root", None)

    assert get_config_dir().is_absolute()
