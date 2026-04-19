"""Integration tests for the config sub-package public API."""

from __future__ import annotations

from typing import TYPE_CHECKING

import doc_classify.config._mode as mode_mod
import doc_classify.config._user as user_mod
from doc_classify.config import (
    AppConfig,
    PermanentConfig,
    UserConfig,
    get_config,
    get_permanent,
    get_user_config,
)
from doc_classify.config._defaults import CONFIG_FILE_NAME

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_get_config_returns_app_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """get_config() should return an AppConfig with both sections."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config = get_config()
    assert isinstance(config, AppConfig)
    assert isinstance(config.permanent, PermanentConfig)
    assert isinstance(config.user, UserConfig)


def test_get_permanent_returns_permanent_config() -> None:
    """get_permanent() should return a PermanentConfig."""
    perm = get_permanent()
    assert isinstance(perm, PermanentConfig)
    assert perm.version  # non-empty string


def test_get_user_config_returns_user_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """get_user_config() should return a UserConfig."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    user = get_user_config()
    assert isinstance(user, UserConfig)


def test_fresh_directory_creates_defaults(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A clean directory should get a default config file created."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config = get_config()
    assert (tmp_path / CONFIG_FILE_NAME).is_file()
    assert config.user.log_level == "info"
    assert config.user.output_format == "text"


def test_dev_mode_reads_from_tmp_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """In dev mode the config should come from .tmp/config/."""
    dev_dir = tmp_path / ".tmp" / "config"
    dev_dir.mkdir(parents=True)
    (dev_dir / CONFIG_FILE_NAME).write_text(
        'log_level = "warning"\noutput_format = "json"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(mode_mod, "MODE", "development")
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: dev_dir)

    config = get_config()
    assert config.user.log_level == "warning"
    assert config.user.output_format == "json"


def test_prod_mode_reads_from_home_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """In prod mode the config should come from ~/.doc-classify/."""
    prod_dir = tmp_path / ".doc-classify"
    prod_dir.mkdir()
    (prod_dir / CONFIG_FILE_NAME).write_text(
        'log_level = "error"\noutput_format = "text"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(mode_mod, "MODE", "production")
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: prod_dir)

    config = get_config()
    assert config.user.log_level == "error"
