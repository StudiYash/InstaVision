# Configuring the Folder Path for **SDXL_LIGHTNING_FOLDER**

Hello, brilliant developer! The main `InstaVision_Telegram_Bot.py` file now reads the SDXL Lightning output folder from `.env` when available and otherwise uses a repo-local runtime folder.

---

## 1. Configure `.env`
- Copy `.env.example` to `.env` in the repository root.
- Set `SDXL_LIGHTNING_OUTPUT_FOLDER` if you want a custom folder.
- Leave it unset to use `runtime_outputs/sdxl_lightning`.

---

## 2. Environment Variable
Use this variable in `.env`:
```python
SDXL_LIGHTNING_OUTPUT_FOLDER=runtime_outputs/sdxl_lightning
```
