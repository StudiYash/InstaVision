# Configuring the Folder Path for **FLUX_SCHNELL_FOLDER**

Hello, brilliant developer! The main `InstaVision_Telegram_Bot.py` file now reads the Flux Schnell output folder from `.env` when available and otherwise uses a repo-local runtime folder.

---

## 1. Configure `.env`
- Copy `.env.example` to `.env` in the repository root.
- Set `FLUX_SCHNELL_OUTPUT_FOLDER` if you want a custom folder.
- Leave it unset to use `runtime_outputs/flux_schnell`.

---

## 2. Environment Variable
Use this variable in `.env`:
```python
FLUX_SCHNELL_OUTPUT_FOLDER=runtime_outputs/flux_schnell
```
