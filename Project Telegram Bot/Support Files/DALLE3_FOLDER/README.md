# Configuring the Folder Path for **DALLE3_FOLDER**

Hello, brilliant developer! The main `InstaVision_Telegram_Bot.py` file now reads the DALL-E 3 output folder from `.env` when available and otherwise uses a repo-local runtime folder.

---

## 1. Configure `.env`
- Copy `.env.example` to `.env` in the repository root.
- Set `DALLE3_OUTPUT_FOLDER` if you want a custom folder.
- Leave it unset to use `runtime_outputs/dalle3`.

---

## 2. Environment Variable
Use this variable in `.env`:
```python
DALLE3_OUTPUT_FOLDER=runtime_outputs/dalle3
```
