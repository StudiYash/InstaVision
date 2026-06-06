"""Lightweight local setup checker for InstaVision.

This script inspects repository structure, configuration, dependencies, and
runtime folders. It does not run project components or call external APIs.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path


RECOMMENDED_PYTHON = (3, 10)

MAJOR_FOLDERS = [
    "Project Backend",
    "Project Frontend",
    "Project Telegram Bot",
    "Project Windows Application",
    "Project Real-life Usage",
    "Project Test Inputs",
    "Certificates",
    "Support Files",
    "requirements",
]

ROOT_FILES = [
    "README.md",
    ".env.example",
    ".gitignore",
    "LOCAL_SETUP_GUIDE.md",
    "PROJECT_STRUCTURE.md",
    "CONFIGURATION.md",
    "COMPONENT_RUN_GUIDE.md",
    "TROUBLESHOOTING.md",
    "requirements.txt",
]

REQUIREMENTS_FILES = [
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

ENV_VARS = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_BOT_USERNAME",
    "TELEGRAM_GROUP_CHAT_ID",
    "REPLICATE_API_TOKEN",
    "OPENAI_API_KEY",
    "IMGBB_API_KEY",
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_PASSWORD",
    "EMAIL_SENDER",
    "EMAIL_RECEIVER",
    "EMAIL_APP_PASSWORD",
    "METRICS_WORKBOOK_PATH",
    "SDXL_LIGHTNING_OUTPUT_FOLDER",
    "FLUX_SCHNELL_OUTPUT_FOLDER",
    "DALLE3_OUTPUT_FOLDER",
    "GOOGLE_IMAGEN3_OUTPUT_FOLDER",
    "LOCAL_IMAGE_OUTPUT_FOLDER",
    "INPUT_IMAGE_PATH",
    "WATERMARK_FONT_PATH",
]

PLACEHOLDER_MARKERS = [
    "replace-with",
    "YOUR_",
    "ENTER_",
    "TOKEN",
    "PASSWORD",
    "HOST",
]

RUNTIME_DIRS = [
    "runtime_outputs",
    "runtime_outputs/generated",
    "runtime_outputs/watermarked",
    "runtime_outputs/uploads",
    "runtime_outputs/metrics",
    "runtime_outputs/sdxl_lightning",
    "runtime_outputs/flux_schnell",
    "runtime_outputs/dalle3",
    "runtime_outputs/google_imagen3",
    "runtime_outputs/local_images",
]

DEPENDENCY_GROUPS = {
    "Frontend": ["PIL", "tkinter"],
    "Backend": ["replicate", "requests", "dotenv"],
    "Telegram Main": ["telegram", "redis", "openai", "translate", "langdetect", "yagmail", "openpyxl"],
    "Optional / Environment-Specific": ["google.colab"],
}


class SetupChecker:
    def __init__(self, root: Path, check_redis: bool = False) -> None:
        self.root = root
        self.check_redis = check_redis
        self.errors = 0
        self.warnings = 0
        self.infos = 0
        self.missing_dependencies: dict[str, list[str]] = {}
        self.missing_env: set[str] = set()
        self.placeholder_env: set[str] = set()
        self.structure_errors = False
        self.windows_app_present = False

    def ok(self, message: str) -> None:
        print(f"[OK] {message}")

    def warn(self, message: str) -> None:
        self.warnings += 1
        print(f"[WARN] {message}")

    def error(self, message: str) -> None:
        self.errors += 1
        print(f"[ERROR] {message}")

    def info(self, message: str) -> None:
        self.infos += 1
        print(f"[INFO] {message}")

    def check_python_version(self) -> None:
        current = sys.version_info
        version = f"{current.major}.{current.minor}.{current.micro}"
        if (current.major, current.minor) >= RECOMMENDED_PYTHON:
            self.ok(f"Python version: {version}")
        else:
            self.warn(f"Python version is {version}; Python 3.10+ is recommended")

    def check_repository_structure(self) -> None:
        if (self.root / "README.md").exists() and (self.root / "Project Backend").is_dir():
            self.ok(f"Repository root detected: {self.root}")
        else:
            self.error(f"Repository root could not be confirmed: {self.root}")
            self.structure_errors = True

        for folder in MAJOR_FOLDERS:
            path = self.root / folder
            if path.is_dir():
                self.ok(f"Folder found: {folder}/")
            else:
                self.error(f"Missing major folder: {folder}/")
                self.structure_errors = True

        self.windows_app_present = (self.root / "Project Windows Application").is_dir()

        for file_name in ROOT_FILES:
            path = self.root / file_name
            if path.is_file():
                self.ok(f"Root file found: {file_name}")
            else:
                self.error(f"Missing root file: {file_name}")
                self.structure_errors = True

    def check_requirements_files(self) -> None:
        for file_name in REQUIREMENTS_FILES:
            path = self.root / file_name
            if path.is_file():
                self.ok(f"Requirements file found: {file_name}")
            else:
                self.warn(f"Requirements file missing: {file_name}")

    def load_env(self) -> None:
        env_example = self.root / ".env.example"
        env_file = self.root / ".env"

        if env_example.is_file():
            self.ok(".env.example found")
        else:
            self.error(".env.example missing")
            self.structure_errors = True

        if env_file.is_file():
            self.ok(".env found")
        else:
            self.warn(".env not found; copy .env.example to .env when configuring local runs")

        try:
            from dotenv import load_dotenv
        except ImportError:
            self.warn("python-dotenv is not installed; using current process environment only")
            return

        if env_file.is_file():
            load_dotenv(env_file)
            self.ok(".env loaded with python-dotenv")
        else:
            self.info("Skipped .env loading because .env is not present")

    def check_environment_variables(self) -> None:
        for name in ENV_VARS:
            value = os.getenv(name)
            if not value:
                self.missing_env.add(name)
                self.warn(f"{name} is not set")
                continue

            if self.looks_like_placeholder(value):
                self.placeholder_env.add(name)
                self.warn(f"{name} appears to contain a placeholder value")
            else:
                self.ok(f"{name} is set")

    def looks_like_placeholder(self, value: str) -> bool:
        upper = value.upper()
        lower = value.lower()
        return any(marker in upper or marker in lower for marker in PLACEHOLDER_MARKERS)

    def check_runtime_dirs(self) -> None:
        for folder in RUNTIME_DIRS:
            path = self.root / folder
            try:
                path.mkdir(parents=True, exist_ok=True)
                self.ok(f"Runtime folder available: {folder}/")
            except OSError as exc:
                self.error(f"Runtime folder cannot be created: {folder}/ ({exc})")
                self.structure_errors = True

    def check_font_availability(self) -> None:
        env_font = os.getenv("WATERMARK_FONT_PATH", "").strip().strip('"')
        fallback = self.root / "Project Telegram Bot" / "Support Files" / "HIGHSENS 400.otf"

        env_font_exists = False
        if env_font:
            env_font_path = Path(env_font)
            if not env_font_path.is_absolute():
                env_font_path = self.root / env_font_path
            env_font_exists = env_font_path.is_file()
            if env_font_exists:
                self.ok(f"WATERMARK_FONT_PATH exists: {env_font}")
            else:
                self.warn(f"WATERMARK_FONT_PATH does not exist: {env_font}")
        else:
            self.info("WATERMARK_FONT_PATH is not set")

        if fallback.is_file():
            self.ok("Fallback watermark font found: Project Telegram Bot/Support Files/HIGHSENS 400.otf")
        elif not env_font_exists:
            self.warn("No configured or fallback watermark font was found")

    def check_dependencies(self) -> None:
        for group, modules in DEPENDENCY_GROUPS.items():
            missing = []
            for module_name in modules:
                if not self.module_available(module_name):
                    missing.append(module_name)
            self.missing_dependencies[group] = missing

            if group == "Optional / Environment-Specific":
                if missing:
                    self.info("google.colab is not available; this is expected outside Google Colab")
                else:
                    self.ok("Optional module available: google.colab")
                continue

            if missing:
                self.warn(f"{group} dependencies missing: {', '.join(missing)}")
            else:
                self.ok(f"{group} dependencies available")

    def module_available(self, module_name: str) -> bool:
        try:
            return importlib.util.find_spec(module_name) is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            return False

    def check_redis_connectivity(self) -> None:
        if not self.check_redis:
            self.info("Redis connectivity check skipped; use --check-redis to enable it")
            return

        try:
            import redis
        except ImportError:
            self.warn("Redis connectivity check requested, but redis package is not installed")
            return

        host = os.getenv("REDIS_HOST")
        port = os.getenv("REDIS_PORT")
        password = os.getenv("REDIS_PASSWORD")
        if not host or not port:
            self.warn("Redis connectivity check requested, but REDIS_HOST or REDIS_PORT is missing")
            return

        try:
            client = redis.Redis(
                host=host,
                port=int(port),
                password=password or None,
                db=0,
                decode_responses=True,
                socket_connect_timeout=3,
                socket_timeout=3,
            )
            client.ping()
            self.ok("Redis connectivity check passed")
        except Exception as exc:  # Redis raises several connection/auth exceptions.
            self.warn(f"Redis connectivity check failed: {exc}")

    def readiness_status(self, *, required_files: list[str] | None = None, env_vars: list[str] | None = None, deps_group: str | None = None) -> str:
        if required_files:
            for file_name in required_files:
                if not (self.root / file_name).exists():
                    return "ERROR"

        warnings = False
        if env_vars and any(name in self.missing_env or name in self.placeholder_env for name in env_vars):
            warnings = True
        if deps_group and self.missing_dependencies.get(deps_group):
            warnings = True
        return "WARN" if warnings else "OK"

    def print_readiness_summary(self) -> None:
        print()
        print("Component Readiness Summary")

        frontend = self.readiness_status(
            required_files=["requirements/frontend.txt", "Project Frontend"],
            deps_group="Frontend",
        )
        backend = self.readiness_status(
            required_files=["requirements/backend.txt", "Project Backend"],
            env_vars=["REPLICATE_API_TOKEN", "IMGBB_API_KEY", "INPUT_IMAGE_PATH"],
            deps_group="Backend",
        )
        main_telegram = self.readiness_status(
            required_files=["requirements/telegram-main.txt", "Project Telegram Bot/InstaVision_Telegram_Bot.py"],
            env_vars=[
                "TELEGRAM_BOT_TOKEN",
                "TELEGRAM_BOT_USERNAME",
                "TELEGRAM_GROUP_CHAT_ID",
                "REDIS_HOST",
                "REDIS_PORT",
                "REDIS_PASSWORD",
                "REPLICATE_API_TOKEN",
                "OPENAI_API_KEY",
                "EMAIL_SENDER",
                "EMAIL_RECEIVER",
                "EMAIL_APP_PASSWORD",
            ],
            deps_group="Telegram Main",
        )
        individual_telegram = self.readiness_status(
            required_files=["requirements/telegram-individual.txt", "Project Telegram Bot/Telegram Bot Individual Models"],
            env_vars=[
                "TELEGRAM_BOT_TOKEN",
                "TELEGRAM_BOT_USERNAME",
                "TELEGRAM_GROUP_CHAT_ID",
                "REDIS_HOST",
                "REDIS_PORT",
                "REDIS_PASSWORD",
                "REPLICATE_API_TOKEN",
                "OPENAI_API_KEY",
            ],
            deps_group="Telegram Main",
        )

        windows_status = "PRESENT" if self.windows_app_present else "MISSING"

        print(f"Frontend readiness: {frontend}")
        print(f"Backend readiness: {backend}")
        print(f"Main Telegram bot readiness: {main_telegram}")
        print(f"Individual Telegram bots readiness: {individual_telegram}")
        print(f"Windows Application: {windows_status}")

    def run(self) -> int:
        print("InstaVision Setup Check")
        print()
        self.check_python_version()
        self.check_repository_structure()
        self.check_requirements_files()
        self.load_env()
        self.check_environment_variables()
        self.check_runtime_dirs()
        self.check_font_availability()
        self.check_dependencies()
        self.check_redis_connectivity()
        self.print_readiness_summary()
        print()
        print(f"Summary: {self.errors} error(s), {self.warnings} warning(s), {self.infos} info item(s)")
        return 1 if self.structure_errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check local InstaVision setup without running project components.")
    parser.add_argument("--check-redis", action="store_true", help="Optionally test Redis connectivity with current environment values.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    checker = SetupChecker(root=root, check_redis=args.check_redis)
    return checker.run()


if __name__ == "__main__":
    raise SystemExit(main())
