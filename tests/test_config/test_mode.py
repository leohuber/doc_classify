"""Tests for the _mode module."""

from doc_classify.config._mode import DEVELOPMENT, MODE, PRODUCTION, get_mode


def test_mode_defaults_to_development() -> None:
    """MODE constant should default to 'development'."""
    assert MODE == "development"


def test_get_mode_returns_current_mode() -> None:
    """get_mode() should return the active MODE value."""
    assert get_mode() == MODE


def test_development_constant() -> None:
    """DEVELOPMENT constant should be 'development'."""
    assert DEVELOPMENT == "development"


def test_production_constant() -> None:
    """PRODUCTION constant should be 'production'."""
    assert PRODUCTION == "production"


def test_get_mode_returns_valid_literal() -> None:
    """get_mode() should return one of the known mode values."""
    assert get_mode() in {DEVELOPMENT, PRODUCTION}
