import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_setup_checker_exists():
    assert (ROOT / "scripts" / "check_setup.py").is_file()


def test_setup_checker_runs_without_redis_check():
    result = subprocess.run(
        [sys.executable, "scripts/check_setup.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "InstaVision Setup Check" in result.stdout
    assert "Component Readiness Summary" in result.stdout
