# InstaVision Local Setup Guide

This guide helps a first-time user clone, inspect, configure, and run the available InstaVision project components.

InstaVision is a completed AI image generation and editing showcase project. It includes multiple project interfaces and runtime options: frontend UI scripts, backend model scripts, a main Telegram bot, individual Telegram model bots, a Windows application, test prompts, and showcase material from real usage events.

Different components have different requirements. You do not need to configure every service unless you plan to run the component that uses it.

## Documentation Map

Use this guide as the starting point. If you need more detail, open the focused documents below.

| Need | Open |
|---|---|
| Understand the full repository layout | [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) |
| Configure API keys, paths, Redis, email, and output folders | [`CONFIGURATION.md`](CONFIGURATION.md) |
| Run a specific component | [`COMPONENT_RUN_GUIDE.md`](COMPONENT_RUN_GUIDE.md) |
| Fix common setup/runtime problems | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |
| Validate local setup before running components | `python scripts/check_setup.py` |
| Run lightweight repository smoke tests | `pip install -r requirements/dev.txt` then `pytest tests/` |

## 1. Install Python

Use Python 3.10 or later for the Python-based components.

Check your Python version:

```powershell
python --version
```

If `python` is not available, install Python from the official Python website or through your system package manager. On Windows, enable "Add Python to PATH" during installation.

## 2. Clone The Repository

```powershell
git clone https://github.com/StudiYash/InstaVision.git
cd InstaVision
```

## 3. Create A Virtual Environment

Create one virtual environment for the component you want to run:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies

This repository now includes top-level dependency targets in the `requirements/` folder.

To install dependencies for all Python-based components:

```powershell
pip install -r requirements.txt
```

For a smaller component-specific install, use one of these files:

```powershell
pip install -r requirements/frontend.txt
pip install -r requirements/backend.txt
pip install -r requirements/telegram-main.txt
pip install -r requirements/telegram-individual.txt
```

The original Telegram requirement files are also preserved:

```powershell
pip install -r "Project Telegram Bot\requirements.txt"
```

For individual Telegram model bots, install the matching file from that bot folder:

```powershell
pip install -r "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Dall E3 API)\requirements_dalle3.txt"
pip install -r "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Flux Schnell API)\requirements_schnell.txt"
pip install -r "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Google Imagen3 API)\requirements_imagen.txt"
pip install -r "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Sdxl Lightning 4Step API)\requirements_sdxl.txt"
```

For frontend Tkinter UI scripts, the only pip dependency currently needed is Pillow:

```powershell
pip install Pillow
```

For backend model scripts, install the common model dependencies:

```powershell
pip install -r requirements/backend.txt
```

Some backend scripts include optional Google Colab download behavior. Colab-only imports and downloads are guarded, and backend workflows run through script entry points instead of executing during import.

## 5. Prepare Environment Variables

Copy the environment template:

```powershell
copy .env.example .env
```

Fill in only the values needed by the component you plan to run. Backend and Telegram components load `.env` values when available while preserving their original placeholder fallbacks.

Backend model scripts, the main Telegram bot, and individual Telegram model bots now load `.env` values automatically. If a variable is missing, the scripts keep their original placeholder fallback values so the setup behavior remains recognizable.

Important values include:

- Telegram bot token, username, and group chat ID.
- Replicate API token.
- OpenAI API key.
- ImgBB API key for backend image editing scripts that upload local images.
- Redis host, port, and password.
- Email sender, receiver, and app password.
- Output folder paths. If unset, supported components use `runtime_outputs/...`.
- Metrics workbook path. If unset, the main bot uses `runtime_outputs/metrics/instavision_metrics.xlsx`.
- Watermark font path. If unset, supported Telegram components use bundled `HIGHSENS 400.otf` files where available.
- Backend sample input image path for editing scripts, via `INPUT_IMAGE_PATH`.

Do not commit `.env`.

## 6. External Services Overview

- Telegram Bot API: required for the main Telegram bot and individual Telegram model bots.
- Redis: required for request limits and ban/user state in Telegram bots.
- Replicate: required by most backend model scripts, Flux Schnell, and SDXL Lightning flows.
- OpenAI: required for DALL-E 3 flows.
- ImgBB: required by backend image editing scripts that upload local input images before calling editing models.
- Email SMTP/app password: used by the main Telegram bot for error and feedback notifications.
- Google Imagen3: represented by an individual bot component; repository text notes Google Imagen 3 code/API availability constraints.

## 7. Suggested Setup Order

1. Read `PROJECT_STRUCTURE.md`.
2. Decide which component you want to run.
3. Install only that component's dependencies.
4. Copy `.env.example` to `.env` and fill only needed values.
5. Run the setup checker.
6. Read `COMPONENT_RUN_GUIDE.md` for the entry point and run command.
7. Use `TROUBLESHOOTING.md` if startup fails.

## 8. Setup Checker

From the repository root, run:

```powershell
python scripts/check_setup.py
```

Missing API keys are reported as warnings, not fatal errors. To optionally test Redis connectivity with your current `.env` values:

```powershell
python scripts/check_setup.py --check-redis
```

## 9. Validation Tests

For contributor validation, install development helpers and run the smoke suite:

```powershell
pip install -r requirements/dev.txt
pytest tests/
```

## 10. Component-Specific Notes

- Frontend UI scripts are Tkinter-based desktop interfaces, not Streamlit scripts in the current repository.
- Backend model scripts are individual examples for model experimentation.
- Main Telegram bot combines multiple generation options, Redis rate limiting, watermarking, metrics, and email notifications.
- Individual Telegram model bots are separate runnable components for specific model/API choices.
- Windows Application is a packaged project interface and should be treated as an available runtime component.
