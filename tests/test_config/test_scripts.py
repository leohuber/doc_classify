"""Tests for the mode-switching zsh scripts."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROD_SCRIPT = REPO_ROOT / "set-mode-prod.zsh"
DEV_SCRIPT = REPO_ROOT / "set-mode-dev.zsh"
MODE_FILE_REL = Path("src") / "doc_classify" / "config" / "_mode.py"


@pytest.fixture
def sandbox(tmp_path: Path) -> Path:
    """Create a temporary copy of the mode file for safe testing."""
    dest_dir = tmp_path / MODE_FILE_REL.parent
    dest_dir.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / MODE_FILE_REL, dest_dir / "_mode.py")

    # Copy scripts into sandbox so SCRIPT_DIR resolves correctly
    for script in (PROD_SCRIPT, DEV_SCRIPT):
        dest = tmp_path / script.name
        shutil.copy2(script, dest)
        dest.chmod(0o755)

    return tmp_path


def _read_mode(sandbox: Path) -> str:
    """Extract the MODE value from the sandboxed _mode.py."""
    content = (sandbox / MODE_FILE_REL).read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.startswith("MODE") and "=" in line:
            # Get the assignment value (right of the last '=')
            rhs = line.rsplit("=", maxsplit=1)[1].strip()
            if rhs == '"production"':
                return "production"
            if rhs == '"development"':
                return "development"
    msg = "MODE assignment not found"
    raise ValueError(msg)


def _run_script(sandbox: Path, script_name: str) -> subprocess.CompletedProcess[str]:
    """Run a zsh script inside the sandbox."""
    return subprocess.run(
        ["zsh", str(sandbox / script_name)],
        capture_output=True,
        text=True,
        check=False,
        cwd=sandbox,
    )


class TestSetModeProd:
    """Tests for set-mode-prod.zsh."""

    def test_switches_to_production(self, sandbox: Path) -> None:
        """Script should change MODE to 'production'."""
        result = _run_script(sandbox, "set-mode-prod.zsh")
        assert result.returncode == 0
        assert _read_mode(sandbox) == "production"

    def test_idempotent_when_already_production(self, sandbox: Path) -> None:
        """Running twice should succeed without error."""
        _run_script(sandbox, "set-mode-prod.zsh")
        result = _run_script(sandbox, "set-mode-prod.zsh")
        assert result.returncode == 0
        assert "already" in result.stdout.lower()
        assert _read_mode(sandbox) == "production"


class TestSetModeDev:
    """Tests for set-mode-dev.zsh."""

    def test_reverts_to_development(self, sandbox: Path) -> None:
        """Script should change MODE back to 'development'."""
        # First switch to production
        _run_script(sandbox, "set-mode-prod.zsh")
        assert _read_mode(sandbox) == "production"

        # Then revert
        result = _run_script(sandbox, "set-mode-dev.zsh")
        assert result.returncode == 0
        assert _read_mode(sandbox) == "development"

    def test_idempotent_when_already_development(self, sandbox: Path) -> None:
        """Running when already development should succeed without error."""
        result = _run_script(sandbox, "set-mode-dev.zsh")
        assert result.returncode == 0
        assert "already" in result.stdout.lower()
        assert _read_mode(sandbox) == "development"


class TestRoundTrip:
    """Test full prod→dev→prod cycle."""

    def test_round_trip_succeeds(self, sandbox: Path) -> None:
        """prod→dev→prod should all succeed."""
        _run_script(sandbox, "set-mode-prod.zsh")
        assert _read_mode(sandbox) == "production"

        _run_script(sandbox, "set-mode-dev.zsh")
        assert _read_mode(sandbox) == "development"

        _run_script(sandbox, "set-mode-prod.zsh")
        assert _read_mode(sandbox) == "production"
