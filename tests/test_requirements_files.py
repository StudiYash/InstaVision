from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIREMENTS_FILES = [
    "requirements.txt",
    "requirements/frontend.txt",
    "requirements/backend.txt",
    "requirements/telegram-main.txt",
    "requirements/telegram-individual.txt",
    "requirements/dev.txt",
    "requirements/all-components.txt",
    "Project Telegram Bot/requirements.txt",
    "Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Dall E3 API)/requirements_dalle3.txt",
    "Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Flux Schnell API)/requirements_schnell.txt",
    "Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Google Imagen3 API)/requirements_imagen.txt",
    "Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Sdxl Lightning 4Step API)/requirements_sdxl.txt",
]


def read_req(path):
    return (ROOT / path).read_text(encoding="utf-8").lower()


def assert_contains(path, package):
    assert package.lower() in read_req(path), f"{package} missing from {path}"


def test_requirements_files_exist():
    missing = [path for path in REQUIREMENTS_FILES if not (ROOT / path).is_file()]
    assert not missing


def test_frontend_and_backend_core_packages():
    assert_contains("requirements/frontend.txt", "Pillow")
    assert_contains("requirements/backend.txt", "Pillow")
    assert_contains("requirements/backend.txt", "replicate")
    assert_contains("requirements/backend.txt", "requests")
    assert_contains("requirements/backend.txt", "python-dotenv")


def test_dev_requirements_include_pytest():
    assert_contains("requirements/dev.txt", "pytest")


def test_telegram_requirements_include_core_packages():
    telegram_files = [
        "requirements/telegram-main.txt",
        "requirements/telegram-individual.txt",
        "Project Telegram Bot/requirements.txt",
    ]
    for path in telegram_files:
        assert_contains(path, "redis")
        assert_contains(path, "python-dotenv")


def test_model_specific_requirements():
    assert_contains("requirements/telegram-main.txt", "openai==0.28.0")
    assert_contains("Project Telegram Bot/requirements.txt", "openai==0.28.0")
    assert_contains("Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Dall E3 API)/requirements_dalle3.txt", "openai==0.28.0")

    assert_contains("Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Flux Schnell API)/requirements_schnell.txt", "replicate")
    assert_contains("Project Telegram Bot/Telegram Bot Individual Models/InstaVision Bot (Sdxl Lightning 4Step API)/requirements_sdxl.txt", "replicate")
