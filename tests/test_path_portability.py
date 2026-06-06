from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

UNSAFE_PATTERNS = [
    "/content/drive/MyDrive/YourFolderPath",
    "C:/Users",
    "C:\\Users",
    "SDXL_LIGHTNING_FOLDER_PATH",
    "FLUX_SCHNELL_FOLDER_PATH",
    "DALLE3_FOLDER_PATH",
    "instavision_metrics.xlsx Path",
    "HIGHSENS 400.otf Path",
]


def python_files_to_scan():
    for folder in ["Project Backend", "Project Telegram Bot"]:
        yield from (ROOT / folder).rglob("*.py")


def test_no_old_path_placeholders_in_python_files():
    violations = []
    for path in python_files_to_scan():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in UNSAFE_PATTERNS:
            if pattern in text:
                violations.append(f"{path.relative_to(ROOT)} contains {pattern}")

    assert not violations


def test_gitignore_ignores_runtime_outputs():
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "runtime_outputs/" in text
