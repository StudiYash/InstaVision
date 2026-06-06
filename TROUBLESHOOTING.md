# InstaVision Troubleshooting Guide

This guide covers common setup problems for the available InstaVision project components.

## Setup Checker

Run the local checker from the repository root:

```powershell
python scripts/check_setup.py
```

Warnings about missing API keys or optional packages are expected until you configure the component you want to run. Use `python scripts/check_setup.py --check-redis` only when you want to test Redis connectivity with your current environment values.

## Validation Tests

Run the smoke tests from the repository root:

```powershell
pip install -r requirements/dev.txt
pytest tests/
```

The tests use stubs for external services and should not call APIs, start bots, connect Redis, generate images, or open GUI windows.

## Missing API Keys

Symptoms:

- Authentication errors from Replicate or OpenAI.
- Telegram bot starts but image generation fails.
- Scripts still show placeholder values like `ENTER_YOUR_TOKEN_HERE`.

What to check:

- Confirm which component you are running.
- Fill the matching values in `.env` based on `.env.example`.
- Backend model scripts, the main Telegram bot, and individual Telegram model bots now load `.env` values automatically.
- If a value is missing from `.env`, the scripts keep their original placeholder fallback values. Seeing placeholders usually means the matching environment variable was not set.
- Never commit real API keys.

## Telegram Bot Startup Issues

Symptoms:

- Bot does not respond in Telegram.
- Terminal does not show `Polling...`.
- Telegram token errors.

What to check:

- Bot token is valid and copied from BotFather.
- The bot has not been revoked or regenerated.
- You installed the correct requirements file.
- You are running the correct entry point from the correct folder.
- Network access is available.
- The bot is not already running elsewhere with the same token.

## Redis Connection Failures

Symptoms:

- Logs mention Redis connection failure.
- Rate limiting or ban checks fail.
- Bot replies with a technical issue verifying limits.

What to check:

- `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD` are correct.
- Redis is running if you use a local server.
- Hosted Redis allows connections from your network.
- Port values are numeric.
- Password is omitted only when your Redis server truly has no password.

## Missing Fonts

Symptoms:

- Watermarking fails.
- Logs mention missing `HIGHSENS 400.otf`.
- Watermark falls back to a default font.

What to check:

- The individual bot folders include `HIGHSENS 400.otf`.
- Use a valid `WATERMARK_FONT_PATH`.
- Backend and Telegram components now use repo-local font fallbacks where available.
- If you override `WATERMARK_FONT_PATH`, make sure the configured file exists.

## Missing Output Folders

Symptoms:

- Errors when saving generated or watermarked images.
- Errors around `LOCAL_IMAGE_FOLDER`.
- Paths containing placeholders such as `YourFolderPath` fail.

What to check:

- Supported backend and Telegram components create their needed `runtime_outputs/...` folders automatically.
- If you override an output path in `.env`, make sure your user account can write to that location.
- Ensure your user account has write permission.
- Avoid saving runtime outputs inside showcase folders.

## Replicate Authentication Failures

Symptoms:

- Replicate API returns authentication or unauthorized errors.
- Backend model script fails immediately.

What to check:

- Replicate API token is active.
- Token has been copied without extra spaces.
- The script is not still using `ENTER_YOUR_TOKEN_HERE`.
- Your account has access to the requested model.
- Network access is available.

## OpenAI Authentication Failures

Symptoms:

- DALL-E 3 bot fails with authentication errors.
- Main Telegram bot fails only for DALL-E 3 generation.

What to check:

- OpenAI API key is valid.
- The code path uses the expected OpenAI SDK version. Current requirements use `openai==0.28.0`.
- The script is not still using a placeholder key.
- Your account/project has access to the image generation model being used.

## Tkinter Launch Issues

Symptoms:

- Frontend UI does not open.
- Error says Tkinter cannot be imported.
- Window opens but logo is missing.

What to check:

- Python installation includes Tkinter.
- Run the script from its own folder so local logo files can be found.
- Install Pillow with `pip install Pillow`.
- Desktop UI scripts need a graphical environment and will not run properly in headless terminals.

## Pillow Installation Issues

Symptoms:

- `ModuleNotFoundError: No module named PIL`.
- Image loading, resizing, or watermarking fails.

What to check:

- Install Pillow in the active virtual environment:

```powershell
pip install Pillow
```

- Confirm your virtual environment is activated.
- Re-run `python -c "from PIL import Image; print('Pillow OK')"` to verify.

## Colab-Specific Issues

Symptoms:

- Local Python cannot import `google.colab`.
- Code calls `files.download(...)`.

What to check:

- Some backend scripts were written for Google Colab workflows.
- Colab-only imports and downloads are guarded for local execution.
- Run Colab-oriented scripts inside Google Colab when you want notebook download behavior.
- Supported output and font fallbacks are now local filesystem paths under `runtime_outputs/` or bundled font files.

## General Dependency Problems

Symptoms:

- `ModuleNotFoundError` for `telegram`, `redis`, `replicate`, `openai`, `translate`, `langdetect`, `yagmail`, or `openpyxl`.

What to check:

- You installed the requirements file for the component you are running.
- Prefer the top-level files when possible:
  - `requirements/frontend.txt`
  - `requirements/backend.txt`
  - `requirements/telegram-main.txt`
  - `requirements/telegram-individual.txt`
  - `requirements.txt` for all Python components.
- Your virtual environment is active.
- You are using a supported Python version.

## When To Use Each Guide

- Use `PROJECT_STRUCTURE.md` to understand where files live.
- Use `LOCAL_SETUP_GUIDE.md` to prepare your machine.
- Use `CONFIGURATION.md` to understand required keys and paths.
- Use `COMPONENT_RUN_GUIDE.md` to start a specific component.
