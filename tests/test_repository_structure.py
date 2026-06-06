from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_major_folders_exist():
    folders = [
        "Project Backend",
        "Project Frontend",
        "Project Telegram Bot",
        "Project Windows Application",
        "Project Real-life Usage",
        "Project Test Inputs",
        "Certificates",
        "Support Files",
        "requirements",
        "scripts",
    ]

    missing = [folder for folder in folders if not (ROOT / folder).is_dir()]
    assert not missing


def test_major_docs_and_root_files_exist():
    files = [
        "README.md",
        "LOCAL_SETUP_GUIDE.md",
        "PROJECT_STRUCTURE.md",
        "CONFIGURATION.md",
        "COMPONENT_RUN_GUIDE.md",
        "TROUBLESHOOTING.md",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "scripts/check_setup.py",
    ]

    missing = [file_name for file_name in files if not (ROOT / file_name).is_file()]
    assert not missing
