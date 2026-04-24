"""Tests for the _validation module."""

from __future__ import annotations

import logging

import pytest

from doc_classify.config._defaults import VALID_LOG_LEVELS, VALID_OUTPUT_FORMATS
from doc_classify.config._exceptions import ConfigValidationError
from doc_classify.config._validation import validate_config


class TestValidLogLevels:
    """All valid log_level values should pass validation."""

    @pytest.mark.parametrize("level", sorted(VALID_LOG_LEVELS))
    def test_valid_log_level_passes(self, level: str) -> None:
        """Each allowed log_level value should be accepted."""
        result = validate_config({"log_level": level})
        assert result["log_level"] == level


class TestValidOutputFormats:
    """All valid output_format values should pass validation."""

    @pytest.mark.parametrize("fmt", sorted(VALID_OUTPUT_FORMATS))
    def test_valid_output_format_passes(self, fmt: str) -> None:
        """Each allowed output_format value should be accepted."""
        result = validate_config({"output_format": fmt})
        assert result["output_format"] == fmt


class TestInvalidValues:
    """Invalid values should raise ConfigValidationError."""

    def test_invalid_log_level_raises(self) -> None:
        """Invalid log_level should raise with key name in message."""
        with pytest.raises(ConfigValidationError, match="log_level") as exc_info:
            validate_config({"log_level": "verbose"})
        assert exc_info.value.key == "log_level"
        assert exc_info.value.value == "verbose"

    def test_invalid_output_format_raises(self) -> None:
        """Invalid output_format should raise with key name in message."""
        with pytest.raises(
            ConfigValidationError,
            match="output_format",
        ) as exc_info:
            validate_config({"output_format": "xml"})
        assert exc_info.value.key == "output_format"
        assert exc_info.value.value == "xml"

    def test_error_message_contains_allowed_values(self) -> None:
        """Error message should list the allowed values."""
        with pytest.raises(ConfigValidationError) as exc_info:
            validate_config({"log_level": "bad"})
        msg = str(exc_info.value)
        assert "debug" in msg
        assert "info" in msg
        assert "warning" in msg
        assert "error" in msg


class TestUnknownKeys:
    """Unknown keys should be warned about and ignored."""

    def test_unknown_key_produces_warning(self, caplog: object) -> None:
        """Unknown keys should emit a warning log message."""
        with caplog.at_level(logging.WARNING):
            result = validate_config({"unknown_key": "value"})
        assert "unknown_key" in caplog.text
        assert "unknown_key" not in result

    def test_unknown_key_does_not_fail(self) -> None:
        """Unknown keys should not cause validation to fail."""
        result = validate_config(
            {
                "log_level": "info",
                "future_key": "something",
            }
        )
        assert result["log_level"] == "info"
        assert "future_key" not in result
