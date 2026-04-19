"""Tests for the _user module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import doc_classify.config._user as user_mod
from doc_classify.config._defaults import (
    CONFIG_FILE_NAME,
    DEFAULT_CONFIG_TEMPLATE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_OUTPUT_FORMAT,
)
from doc_classify.config._exceptions import ConfigValidationError
from doc_classify.config._user import UserConfig, load_user_config

if TYPE_CHECKING:
    from pathlib import Path


def test_default_config_created_when_absent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A default config.toml should be created if missing."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config = load_user_config()
    config_file = tmp_path / CONFIG_FILE_NAME
    assert config_file.is_file()
    assert config.log_level == DEFAULT_LOG_LEVEL
    assert config.output_format == DEFAULT_OUTPUT_FORMAT


def test_default_config_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Created default file should match DEFAULT_CONFIG_TEMPLATE."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)
    load_user_config()

    content = (tmp_path / CONFIG_FILE_NAME).read_text(encoding="utf-8")
    assert content == DEFAULT_CONFIG_TEMPLATE


def test_load_existing_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """load_user_config() should read values from an existing file."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(
        'log_level = "debug"\noutput_format = "json"\n',
        encoding="utf-8",
    )

    config = load_user_config()
    assert config.log_level == "debug"
    assert config.output_format == "json"


def test_user_config_defaults() -> None:
    """UserConfig defaults should match the module constants."""
    config = UserConfig()
    assert config.log_level == DEFAULT_LOG_LEVEL
    assert config.output_format == DEFAULT_OUTPUT_FORMAT


def test_nested_directory_creation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Config file creation should handle nested non-existent dirs."""
    deep_dir = tmp_path / "a" / "b" / "c"
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: deep_dir)

    load_user_config()
    assert (deep_dir / CONFIG_FILE_NAME).is_file()


# --- US2: Modification scenarios ---


def test_edited_config_reflected_on_reload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Editing config.toml and reloading should reflect new values."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    # First load creates defaults
    config1 = load_user_config()
    assert config1.log_level == "info"

    # User edits the file
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(
        'log_level = "debug"\noutput_format = "json"\n',
        encoding="utf-8",
    )

    # Reload picks up changes
    config2 = load_user_config()
    assert config2.log_level == "debug"
    assert config2.output_format == "json"


def test_invalid_edit_raises_on_reload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Editing config.toml to an invalid value should raise on reload."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(
        'log_level = "verbose"\noutput_format = "text"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError, match="log_level"):
        load_user_config()


def test_partial_edit_preserves_defaults(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Editing only one key should preserve the default for the other."""
    monkeypatch.setattr(user_mod, "get_config_dir", lambda: tmp_path)

    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text('log_level = "warning"\n', encoding="utf-8")

    config = load_user_config()
    assert config.log_level == "warning"
    assert config.output_format == "text"  # default preserved
