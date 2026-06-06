# InstaVision Configuration Guide

This document explains known configuration items discovered in the repository.

Important: this is explanatory documentation only. Backend and Telegram components now load values from `.env` when available while preserving the original placeholder fallbacks.

Phase 4 added `.env` loading for backend model scripts, the main Telegram bot, and the individual Telegram model bots. These components now read configuration values from environment variables when present, while keeping the original placeholder values as fallbacks.

## Configuration Summary

| Item | Purpose | Required? | Used By |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Authenticates a Telegram bot created with BotFather. | Required for Telegram bots. | Main Telegram bot, individual model bots. |
| `TELEGRAM_BOT_USERNAME` | Documents or identifies the bot username. | Required for complete Telegram setup. | Main Telegram bot, individual model bots. |
| `TELEGRAM_GROUP_CHAT_ID` | Group/channel where generated image logs may be sent. | Required if group sharing is enabled. | Main Telegram bot, individual model bots. |
| `REPLICATE_API_TOKEN` | Authenticates Replicate model calls. | Required for Replicate-backed scripts. | Backend model scripts, Flux Schnell bot, SDXL Lightning bot, main Telegram bot. |
| `OPENAI_API_KEY` | Authenticates OpenAI DALL-E 3 calls. | Required for DALL-E 3. | Main Telegram bot, DALL-E 3 individual bot. |
| `IMGBB_API_KEY` | Authenticates ImgBB uploads for scripts that upload local input images before editing. | Required for backend editing scripts that upload images. | Backend image editing model scripts. |
| `REDIS_HOST` | Redis server hostname. | Required for Telegram bot rate limits/user state. | Main Telegram bot, individual model bots. |
| `REDIS_PORT` | Redis server port. | Required for Telegram bot rate limits/user state. | Main Telegram bot, individual model bots. |
| `REDIS_PASSWORD` | Redis password. | Required when Redis uses authentication. | Main Telegram bot, individual model bots. |
| `EMAIL_SENDER` | Sender email for notifications. | Required for email notifications. | Main Telegram bot. |
| `EMAIL_RECEIVER` | Receiver/admin email for notifications and feedback. | Required for email notifications. | Main Telegram bot. |
| `EMAIL_APP_PASSWORD` | App password or SMTP credential for email sending. | Required for email notifications. | Main Telegram bot. |
| `METRICS_WORKBOOK_PATH` | Excel workbook path for usage metrics. | Required for metrics tracking. | Main Telegram bot. |
| `SDXL_LIGHTNING_OUTPUT_FOLDER` | Folder for SDXL Lightning output copies. | Required when saving SDXL outputs. | Main Telegram bot. |
| `FLUX_SCHNELL_OUTPUT_FOLDER` | Folder for Flux Schnell output copies. | Required when saving Flux outputs. | Main Telegram bot. |
| `DALLE3_OUTPUT_FOLDER` | Folder for DALL-E 3 output copies. | Required when saving DALL-E outputs. | Main Telegram bot. |
| `GOOGLE_IMAGEN3_OUTPUT_FOLDER` | Folder for Google Imagen3 output copies if functionality is enabled. | Component-specific. | Google Imagen3 individual bot. |
| `LOCAL_IMAGE_OUTPUT_FOLDER` | Generic local folder for individual model bot outputs. | Required for individual bots that save images. | Individual Telegram model bots. |
| `INPUT_IMAGE_PATH` | Local input image path for backend editing scripts that upload a sample image. | Required when running those backend scripts with your own image. | Backend image editing model scripts. |
| `WATERMARK_FONT_PATH` | Font file used for watermark text. | Optional if fallback font is acceptable; required for exact project watermark styling. | Main Telegram bot, individual model bots. |

## Telegram Configuration

Telegram bot values come from BotFather and Telegram chat/group setup.

- `TELEGRAM_BOT_TOKEN`: secret token. Do not publish it.
- `TELEGRAM_BOT_USERNAME`: usually starts with `@` in user-facing contexts, though code may store it with or without `@`.
- `TELEGRAM_GROUP_CHAT_ID`: can be a negative numeric ID for groups/supergroups.

## API Configuration

Replicate-backed components require `REPLICATE_API_TOKEN`.

OpenAI DALL-E 3 components require `OPENAI_API_KEY`.

Backend model scripts now read `REPLICATE_API_TOKEN` from `.env` when available. Backend editing scripts also read `IMGBB_API_KEY` when uploading local images.

## Redis Configuration

Redis is used by Telegram bot components to store request counts, user limit state, warning state, and ban state.

Typical values:

- `REDIS_HOST`: cloud Redis hostname or local hostname.
- `REDIS_PORT`: Redis port, often `6379` for local Redis.
- `REDIS_PASSWORD`: password for hosted Redis. Local Redis may not require one.

## Email Configuration

The main Telegram bot includes email notification and feedback logic.

- Use an app password when your email provider requires it.
- Do not store real email passwords in source code.
- Email notifications are optional for exploring non-bot components, but needed for the full main bot workflow.

## Output And Metrics Paths

Telegram bot components save temporary and watermarked images. The main bot also tracks usage metrics in an Excel workbook.

Prefer paths outside showcase folders so runtime outputs do not mix with project evidence assets.

Suggested local folders:

```text
runtime_outputs/generated/
runtime_outputs/watermarked/
runtime_outputs/uploads/
runtime_outputs/sdxl_lightning/
runtime_outputs/flux_schnell/
runtime_outputs/dalle3/
runtime_outputs/google_imagen3/
runtime_outputs/local_images/
runtime_outputs/metrics/instavision_metrics.xlsx
```

Supported backend and Telegram components now use repo-local `runtime_outputs/` paths as fallbacks when matching environment variables are not set. You can override these defaults in `.env` when you want outputs elsewhere.

## Font Configuration

Some Telegram bot folders include `HIGHSENS 400.otf`. If using the exact watermark style, point `WATERMARK_FONT_PATH` to that file or another preferred font.

If the configured font is missing, some scripts may fall back to a default font while others may raise an error depending on the component.
