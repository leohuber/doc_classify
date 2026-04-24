"""CLI integration tests for doc-classify."""

from importlib.metadata import version

from click.testing import CliRunner

from doc_classify.cli import main


def _runner() -> CliRunner:
    """Create a Click test runner."""
    return CliRunner()


class TestHelp:
    """Tests for --help output."""

    def test_help_exits_zero(self) -> None:
        """``--help`` exits with code 0."""
        result = _runner().invoke(main, ["--help"])
        assert result.exit_code == 0

    def test_help_contains_usage(self) -> None:
        """``--help`` output contains 'Usage'."""
        result = _runner().invoke(main, ["--help"])
        assert "Usage" in result.output


class TestVersion:
    """Tests for --version output."""

    def test_version_exits_zero(self) -> None:
        """``--version`` exits with code 0."""
        result = _runner().invoke(main, ["--version"])
        assert result.exit_code == 0

    def test_version_matches_metadata(self) -> None:
        """``--version`` output matches importlib.metadata."""
        result = _runner().invoke(main, ["--version"])
        expected = version("doc-classify")
        assert expected in result.output


class TestNoArgs:
    """Tests for invocation with no arguments."""

    def test_no_args_exits_zero(self) -> None:
        """No arguments exits with code 0 and shows help."""
        result = _runner().invoke(main, [])
        assert result.exit_code == 0

    def test_no_args_shows_help(self) -> None:
        """No arguments shows help text."""
        result = _runner().invoke(main, [])
        assert "Usage" in result.output


class TestUnknownInput:
    """Tests for unrecognized options and commands."""

    def test_unknown_option_exits_two(self) -> None:
        """Unknown option ``--foo`` exits with code 2."""
        result = _runner().invoke(main, ["--foo"])
        assert result.exit_code == 2

    def test_unknown_command_exits_two(self) -> None:
        """Unknown command ``badcommand`` exits with code 2."""
        result = _runner().invoke(main, ["badcommand"])
        assert result.exit_code == 2
