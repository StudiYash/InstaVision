import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ENV_VARS = [
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


def env_template_text():
    return (ROOT / ".env.example").read_text(encoding="utf-8")


def test_env_example_contains_expected_variables():
    text = env_template_text()
    missing = [name for name in EXPECTED_ENV_VARS if not re.search(rf"^{name}=", text, re.MULTILINE)]
    assert not missing


def test_env_example_uses_placeholders_or_safe_local_paths():
    suspicious_assignments = []
    for line in env_template_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        safe = (
            value.startswith("replace-with")
            or value.startswith("runtime_outputs/")
            or value.startswith("Project Telegram Bot/")
        )
        if key and value and not safe:
            suspicious_assignments.append(line)

    assert not suspicious_assignments


def test_env_example_does_not_contain_obvious_real_secrets():
    text = env_template_text()
    secret_like_patterns = [
        r"\bsk-[A-Za-z0-9_-]{20,}",
        r"\br8_[A-Za-z0-9]{20,}",
        r"\b\d{6,}:[A-Za-z0-9_-]{20,}",
        r"BEGIN (RSA |OPENSSH )?PRIVATE KEY",
    ]
    matches = [pattern for pattern in secret_like_patterns if re.search(pattern, text)]
    assert not matches
