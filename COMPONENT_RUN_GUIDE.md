# InstaVision Component Run Guide

This guide lists available runtime components and how they appear to be run from the current repository.

Commands are shown for PowerShell on Windows. On macOS/Linux, use `/` path separators and `python3` if needed.

## Pre-Run Setup Check

From the repository root, run the local checker before launching a component:

```powershell
python scripts/check_setup.py
```

For an optional Redis connectivity check:

```powershell
python scripts/check_setup.py --check-redis
```

To run the lightweight validation suite:

```powershell
pip install -r requirements/dev.txt
pytest tests/
```

## Frontend Project Interfaces

The current frontend scripts are Tkinter desktop UI scripts.

### Main Page

- Entry point: `Project Frontend\Main Page\Main Page.py`
- Dependencies: Python, Tkinter, Pillow.
- Credentials: none.
- Basic command:

```powershell
pip install -r requirements/frontend.txt
cd "Project Frontend\Main Page"
python "Main Page.py"
```

- Notes and limitations:
  - Run from its folder so `InstaVision_Logo.png` can be found.
  - Opens a desktop window.

### Image Generation UI

- Entry point: `Project Frontend\Image Generation\Image Generation.py`
- Dependencies: Python, Tkinter, Pillow.
- Credentials: none for the current frontend-only placeholder behavior.
- Basic command:

```powershell
pip install -r requirements/frontend.txt
cd "Project Frontend\Image Generation"
python "Image Generation.py"
```

- Notes and limitations:
  - Current UI simulates generation with placeholder output.
  - Settings fields document token-style values but do not represent complete backend integration.

### Image Editing UI

- Entry point: `Project Frontend\Image Editing\Image Editing.py`
- Dependencies: Python, Tkinter, Pillow.
- Credentials: none for the current frontend-only placeholder behavior.
- Basic command:

```powershell
pip install -r requirements/frontend.txt
cd "Project Frontend\Image Editing"
python "Image Editing.py"
```

- Notes and limitations:
  - Current UI provides frontend behavior and simulated editing flow.
  - Run from its folder so local assets resolve correctly.

## Backend Model Scripts

### Image Generation Models

- Entry points: Python files in `Project Backend\Image Generation Models\`.
- Dependencies: `replicate`, `requests`, `Pillow`; some scripts import `google.colab`.
- Credentials: Replicate API token for Replicate-backed models.
- Basic setup:

```powershell
pip install -r requirements/backend.txt
cd "Project Backend\Image Generation Models"
python "black-forest-labs_flux-schnell.py"
```

- Notes and limitations:
  - Each script is a standalone model experiment.
  - Many scripts contain placeholder token assignment lines.
  - Optional Colab download behavior is guarded for local imports.
  - Model workflows execute when scripts are run directly through their entry point.
  - Prompts may be defined inside the script; supported saved outputs use `runtime_outputs/generated`.

### Image Editing Models

- Entry points: Python files in `Project Backend\Image Editing Models\`.
- Dependencies: `replicate`, `requests`, and possibly image upload support depending on the script.
- Credentials: Replicate API token; ImgBB API key may be needed for editing flows described by README files.
- Environment variables loaded: `REPLICATE_API_TOKEN`, `IMGBB_API_KEY`, `INPUT_IMAGE_PATH`.
- Basic setup:

```powershell
pip install -r requirements/backend.txt
cd "Project Backend\Image Editing Models"
python "cjwbw_rembg.py"
```

- Notes and limitations:
  - Each script targets one editing model.
  - Model workflows execute when scripts are run directly through their entry point.
  - Inputs such as image URLs, masks, or prompts may need to be set inside each script.
  - Scripts that upload local sample images use `INPUT_IMAGE_PATH` when set, otherwise `runtime_outputs/uploads`.

## Main Telegram Bot

- Entry point: `Project Telegram Bot\InstaVision_Telegram_Bot.py`
- Dependencies: `Project Telegram Bot\requirements.txt`
- Required credentials/services:
  - Telegram bot token, username, and group chat ID.
  - Redis host, port, and password.
  - Replicate API token.
  - OpenAI API key for DALL-E 3.
  - Email sender, receiver, and app password for notifications.
  - Output folders, metrics workbook path, and watermark font path.
- Environment variables loaded: values from `.env.example`, including Telegram, Redis, API, email, metrics, output folder, and font settings.
- Basic setup:

```powershell
pip install -r requirements/telegram-main.txt
cd "Project Telegram Bot"
python "InstaVision_Telegram_Bot.py"
```

- Notes and limitations:
  - The current script contains inline placeholder values that must be configured before full operation.
  - Redis must be reachable before rate limiting and ban logic can work.
  - The bot starts polling when run directly.
  - Importing the file does not start polling.
  - Runtime images and metrics use `runtime_outputs/` fallbacks unless overridden in `.env`.

## Individual Telegram Model Bots

Each individual model bot is an available runtime component with its own folder, README, and requirements file.

### DALL-E 3 Bot

- Entry point: `Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Dall E3 API)\InstaVision_DallE3_API.py`
- Dependencies: `requirements_dalle3.txt`
- Required credentials/services: Telegram, OpenAI API key, Redis, local output folder, watermark font.
- Environment variables loaded: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_BOT_USERNAME`, `TELEGRAM_GROUP_CHAT_ID`, `OPENAI_API_KEY`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `DALLE3_OUTPUT_FOLDER`, `LOCAL_IMAGE_OUTPUT_FOLDER`, `WATERMARK_FONT_PATH`.
- Basic command:

```powershell
cd "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Dall E3 API)"
pip install -r requirements_dalle3.txt
python "InstaVision_DallE3_API.py"
```

Alternative from the repository root:

```powershell
pip install -r requirements/telegram-individual.txt
```

- Notes and limitations:
  - Contains placeholder credentials that must be configured before full operation.
  - Output and font paths use portable fallbacks unless overridden in `.env`.

### Flux Schnell Bot

- Entry point: `Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Flux Schnell API)\InstaVision_Flux-Schnell_API.py`
- Dependencies: `requirements_schnell.txt`
- Required credentials/services: Telegram, Replicate API token, Redis, local output folder, watermark font.
- Environment variables loaded: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_BOT_USERNAME`, `TELEGRAM_GROUP_CHAT_ID`, `REPLICATE_API_TOKEN`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `FLUX_SCHNELL_OUTPUT_FOLDER`, `LOCAL_IMAGE_OUTPUT_FOLDER`, `WATERMARK_FONT_PATH`.
- Basic command:

```powershell
cd "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Flux Schnell API)"
pip install -r requirements_schnell.txt
python "InstaVision_Flux-Schnell_API.py"
```

Alternative from the repository root:

```powershell
pip install -r requirements/telegram-individual.txt
```

- Notes and limitations:
  - Contains placeholder credentials that must be configured before full operation.
  - Output and font paths use portable fallbacks unless overridden in `.env`.

### Imagen3 Bot

- Entry point: `Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Google Imagen3 API)\InstaVision_Imagen3_API.py`
- Dependencies: `requirements_imagen.txt`
- Required credentials/services: Telegram, Redis, local output folder. Google Imagen3 availability is explained by the component README and bot messages.
- Environment variables loaded: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_BOT_USERNAME`, `TELEGRAM_GROUP_CHAT_ID`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `GOOGLE_IMAGEN3_OUTPUT_FOLDER`, `LOCAL_IMAGE_OUTPUT_FOLDER`, `WATERMARK_FONT_PATH`.
- Basic command:

```powershell
cd "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Google Imagen3 API)"
pip install -r requirements_imagen.txt
python "InstaVision_Imagen3_API.py"
```

Alternative from the repository root:

```powershell
pip install -r requirements/telegram-individual.txt
```

- Notes and limitations:
  - The script includes Colab authentication behavior when run inside Google Colab.
  - Importing the file does not authenticate Colab or start polling.
  - Repository documentation states Google Imagen 3 code/API availability limitations for general users.

### SDXL Lightning Bot

- Entry point: `Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Sdxl Lightning 4Step API)\InstaVision_Sdxl-Lightning-4step_API.py`
- Dependencies: `requirements_sdxl.txt`
- Required credentials/services: Telegram, Replicate API token, Redis, local output folder, watermark font.
- Environment variables loaded: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_BOT_USERNAME`, `TELEGRAM_GROUP_CHAT_ID`, `REPLICATE_API_TOKEN`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `SDXL_LIGHTNING_OUTPUT_FOLDER`, `LOCAL_IMAGE_OUTPUT_FOLDER`, `WATERMARK_FONT_PATH`.
- Basic command:

```powershell
cd "Project Telegram Bot\Telegram Bot Individual Models\InstaVision Bot (Sdxl Lightning 4Step API)"
pip install -r requirements_sdxl.txt
python "InstaVision_Sdxl-Lightning-4step_API.py"
```

Alternative from the repository root:

```powershell
pip install -r requirements/telegram-individual.txt
```

- Notes and limitations:
  - Contains placeholder credentials that must be configured before full operation.
  - Output and font paths use portable fallbacks unless overridden in `.env`.

## Windows Application

- Entry point: `Project Windows Application\InstaVision.exe`
- Dependencies: packaged executable for Windows.
- Credentials: any required runtime settings depend on the packaged application behavior.
- Basic run:

```powershell
cd "Project Windows Application"
.\InstaVision.exe
```

- Notes and limitations:
  - This is an available project interface.
  - See `Project Windows Application\README.md` for installer screenshots and usage overview.
  - Windows Defender or security tools may warn about downloaded executables; review and decide according to your local security policy.
