"""Tests for the _permanent module."""

from __future__ import annotations

import importlib.metadata

import pytest

from doc_classify.config._permanent import load_permanent_config


def test_version_matches_metadata() -> None:
    """PermanentConfig.version should match importlib.metadata."""
    config = load_permanent_config()
    expected = importlib.metadata.version("doc-classify")
    assert config.version == expected


def test_name_is_doc_classify() -> None:
    """PermanentConfig.name should be 'doc-classify'."""
    config = load_permanent_config()
    assert config.name == "doc-classify"


def test_permanent_config_is_frozen() -> None:
    """PermanentConfig should be immutable (frozen dataclass)."""
    config = load_permanent_config()
    with pytest.raises(AttributeError):
        config.version = "99.0.0"  # type: ignore[misc]
