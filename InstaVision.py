import sys
import nest_asyncio
import logging
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import os
import io
import redis
from datetime import datetime, timedelta, timezone
import asyncio
import re
from PIL import Image, ImageDraw, ImageFont
import replicate
import openai
from translate import Translator
from langdetect import detect
import yagmail
import openpyxl
from openpyxl import Workbook, load_workbook
import base64
from io import BytesIO

# =============================================================
#               Logging Configuration
# =============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================
#                 Bot & API Configuration
# =============================================================
TOKEN = 'TELEGRAM BOT TOKEN'                 # Replace with actual bot token
BOT_USERNAME = 'TELEGRAM BOT USERNAME'       # e.g. "my_bot"
GROUP_CHAT_ID = 'TELEGRAM GROUP CHAT ID'     # e.g. -100123456789

openai.api_key = 'OPENAI API KEY'            # Replace with your OpenAI API key
os.environ['REPLICATE_API_TOKEN'] = 'REPLICATE API KEY'

# =============================================================
#                Global Constants & Variables
# =============================================================
BANNED_WORDS = [
    'WORD1', 'WORD2'
]

# Local folders for saving images
SDXL_LIGHTNING_FOLDER = "SDXL_LIGHTNING_FOLDER_PATH"
FLUX_SCHNELL_FOLDER = "FLUX_SCHNELL_FOLDER_PATH"
DALLE_FOLDER = "DALLE3_FOLDER_PATH"

for folder in [SDXL_LIGHTNING_FOLDER, FLUX_SCHNELL_FOLDER, DALLE_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

EXCEL_FILE_PATH = "instavision_metrics.xlsx Path"

# User role configurations
unlimited_users = ['USERNAME1', 'USERNAME2']       # e.g. admin users
fifty_per_day_users = ['USERNAME3', 'USERNAME4']   # e.g. semi-privileged
custom_banned_users = ['USERNAME5', 'USERNAME6']   # permanently banned

# Redis connection (edit host/port/password as needed)
def connect_redis():
    try:
        r = redis.Redis(
            host='REDIS HOST',
            port=9999,
            password='REDIS PASSWORD',
            db=0,
            decode_responses=True
        )
        r.ping()
        logger.info("Connected to Redis successfully.")
        return r
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
        return None

r = connect_redis()

# Asynchronous queue for requests
request_queue = asyncio.Queue()
# Dictionary to track who is awaiting feedback
awaiting_feedback = {}

# =============================================================
#                  Email Utility
# =============================================================
def send_error_email(subject, body):
    try:
        sender_email = "SENDER MAIL ADDRESS"
        receiver_email = "RECEIVER MAIL ADDRESS"
        app_password = "SENDER APP PASSWORD"

        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(to=receiver_email, subject=subject, contents=body)
        logger.info(f"Error email sent: {subject}")
    except Exception as e:
        logger.error(f"Error sending error email: {e}")

# =============================================================
#             User Limit & Ban System
# =============================================================
def check_and_update_user_limit(user_id, username):
    """
    Checks the user's daily limit. 
    - 5 images/day for default
    - 50/day for certain privileged
    - unlimited for admin
    """
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")

        if username in unlimited_users:
            return True
        elif username in fifty_per_day_users:
            limit = 50
        else:
            limit = 5

        current_time = datetime.now()
        reset_limit_hours = 24

        request_count = r.hget(user_id, 'request_count')
        last_request_time = r.hget(user_id, 'last_request_time')

        if request_count is None or last_request_time is None:
            # Initialize
            r.hset(user_id, mapping={
                'request_count': 1,
                'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return True

        request_count = int(request_count)
        last_request_time = datetime.strptime(last_request_time, "%Y-%m-%d %H:%M:%S")

        # Reset if 24 hours have passed
        if current_time - last_request_time > timedelta(hours=reset_limit_hours):
            r.hset(user_id, mapping={
                'request_count': 1,
                'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            return True

        # If limit reached
        if request_count >= limit:
            if request_count == limit:
                # increment so user can't spam
                r.hincrby(user_id, 'request_count', 1)
            return False

        # Otherwise, increment
        r.hincrby(user_id, 'request_count', 1)
        return True

    except Exception as e:
        logger.error(f"Error in check_and_update_user_limit: {e}")
        return None

def ban_user(user_id, duration_in_seconds=None):
    """Bans a user for 'duration_in_seconds' or permanently."""
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")
        if duration_in_seconds:
            ban_expiry_time = datetime.now() + timedelta(seconds=duration_in_seconds)
            r.hset(user_id, 'ban_expiry_time', ban_expiry_time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            # permanent ban
            r.hset(user_id, 'banned', 1)
        logger.info(f"User {user_id} has been banned.")
        return True
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return None

def is_user_banned(user_id, username):
    """
    Check if user is banned, including permanent ban (custom_banned_users)
    or temporary ban stored in Redis with ban_expiry_time.
    """
    try:
        if username in custom_banned_users:
            return True

        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")

        ban_expiry_time_str = r.hget(user_id, 'ban_expiry_time')
        if ban_expiry_time_str:
            ban_expiry_time = datetime.strptime(ban_expiry_time_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() >= ban_expiry_time:
                # Ban expired
                r.hdel(user_id, 'ban_expiry_time')
                r.hdel(user_id, 'warning_issued')
                logger.info(f"Ban expired for user {user_id}.")
                return False
            else:
                return True
        else:
            # check permanent ban
            banned_status = r.hget(user_id, 'banned')
            return banned_status is not None
    except Exception as e:
        logger.error(f"Error checking banned status for user {user_id}: {e}")
        return None

# =============================================================
#               Image Generation (Other Models)
# =============================================================
def generate_image_sdxl(prompt: str):
    """
    Uses Replicate's SDXL Lightning model
    """
    try:
        output = replicate.run(
            "bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637",
            input={"prompt": prompt}
        )
        file_output = output[0]
        image_data = file_output.read()
        image = Image.open(BytesIO(image_data))

        image_filename = f"generated_image_sdxl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(image_filename)
        return image_filename
    except Exception as e:
        logger.error(f"Error generating image with SDXL Lightning: {e}")
        subject = "API Failure Detected - SDXL Lightning"
        body = f"Error generating image with SDXL Lightning: {e}"
        send_error_email(subject, body)
        raise Exception("There was an issue generating your image. Please try again later.")

def generate_image_flux_schnell(prompt: str):
    """
    Uses Replicate's Flux Schnell model
    """
    try:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "png",
                "output_quality": 80
            }
        )
        file_output = output[0]
        image_data = file_output.read()
        image = Image.open(BytesIO(image_data))

        image_filename = f"generated_image_flux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(image_filename)
        return image_filename
    except Exception as e:
        logger.error(f"Error generating image with Flux Schnell: {e}")
        subject = "API Failure Detected - Flux Schnell"
        body = f"Error generating image with Flux Schnell: {e}"
        send_error_email(subject, body)
        raise Exception("There was an issue generating your image. Please try again later.")

def generate_image_dalle(prompt: str):
    """
    Uses OpenAI DALL-E 3
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except openai.error.AuthenticationError as e:
        logger.error(f"Authentication error with DALL-E: {e}")
        subject = "API Failure Detected - DALL-E Authentication"
        body = f"Authentication error with DALL-E: {e}"
        send_error_email(subject, body)
        raise Exception("Image generation system is currently facing an issue. Please try again later.")
    except Exception as e:
        logger.error(f"Error generating image with DALL-E: {e}")
        subject = "API Failure Detected - DALL-E"
        body = f"Error generating image with DALL-E: {e}"
        send_error_email(subject, body)
        raise Exception("Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed.")

# =============================================================
#                   Utility Functions
# =============================================================
def escape_markdown(text):
    escape_chars = r'\*_`\[\]()~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

def translate_to_english(text):
    """
    Detect language; if not English, translate to English.
    """
    try:
        detected_language = detect(text)
    except Exception as e:
        logger.error(f"Could not detect language: {e}")
        subject = "Error in Language Detection"
        body = f"Could not detect language for text: {text}\nError: {e}"
        send_error_email(subject, body)
        raise Exception("Your input was not understood correctly. Please reword your input and try again.")

    if detected_language != 'en':
        try:
            translator = Translator(from_lang=detected_language, to_lang='en')
            translation = translator.translate(text)
            logger.info(f"Translated prompt from {detected_language} to English.")
            return translation
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            subject = "Error in Translation"
            body = f"Failed to translate text: {text}\nError: {e}"
            send_error_email(subject, body)
            raise Exception("Your input was not understood correctly. Please reword your input and try again.")
    else:
        return text

def add_watermark(
    input_image_path, 
    output_image_path, 
    watermark_text="InstaVision", 
    font_size=30,
    text_color=(255, 130, 80, 128), 
    bg_color=(0, 0, 0, 128)
):
    """
    Add a watermark to the bottom-right corner of an image.
    """
    try:
        original = Image.open(input_image_path).convert("RGBA")
        width, height = original.size

        watermark = Image.new("RGBA", original.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        try:
            font = ImageFont.truetype("HIGHSENS 400.otf Path", font_size)
        except IOError:
            logger.warning("Specified font not found. Using default font.")
            font = ImageFont.load_default()
            subject = "Image Storage and Custom Font Fetching Issue"
            body = "The custom font for watermarking could not be found. The default font is being used."
            send_error_email(subject, body)

        try:
            text_width, text_height = font.getsize(watermark_text)
        except AttributeError:
            bbox = font.getbbox(watermark_text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

        padding = 10
        position = (width - text_width - padding, height - text_height - padding)
        rect_position = (
            position[0] - padding, position[1] - padding,
            position[0] + text_width + padding, position[1] + text_height + padding
        )

        draw.rectangle(rect_position, fill=bg_color)
        draw.text(position, watermark_text, fill=text_color, font=font)

        combined = Image.alpha_composite(original, watermark)
        combined.convert("RGB").save(output_image_path, "PNG")

    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise e

def contains_unsupported_characters(text):
    """
    Quick check for non-textual or control characters, etc.
    """
    try:
        cleaned_text = re.sub(r'[a-zA-Z0-9\s,.!?;:\'\"@#%&()\[\]{}\-_/\\]', '', text)
        return bool(cleaned_text)
    except Exception as e:
        logger.error(f"Error checking unsupported characters: {e}")
        return True

# =============================================================
#                  Excel Tracking
# =============================================================
def init_excel_file():
    """
    Ensure the Excel file has columns for Imagen3, SDXL, FluxSchnell, DALL-E3.
    """
    if not os.path.exists(EXCEL_FILE_PATH):
        wb = Workbook()
        ws_user_stats = wb.active
        ws_user_stats.title = "UserStats"

        ws_global_stats = wb.create_sheet(title="GlobalStats")
        ws_request_log = wb.create_sheet(title="RequestLog")

        # Reintroducing Imagen3 so we can log it
        ws_user_stats.append([
            "UserID", "Username", "TotalImages",
            "Imagen3", "SDXL", "FluxSchnell", "DALL-E3"
        ])
        ws_global_stats.append([
            "Month", "Year", "TotalImages",
            "Imagen3", "SDXL", "FluxSchnell", "DALL-E3"
        ])
        ws_request_log.append([
            "Timestamp", "UserID", "Username",
            "ModelUsed", "Prompt"
        ])

        wb.save(EXCEL_FILE_PATH)
        logger.info("Excel file created and initialized.")
    else:
        logger.info("Excel file already exists.")

init_excel_file()

def update_metrics(user_id, username, command, prompt):
    """
    Log usage in the Excel file. Now includes Imagen3 for /imagen3 usage.
    """
    try:
        wb = load_workbook(EXCEL_FILE_PATH)
        ws_user_stats = wb["UserStats"]
        ws_global_stats = wb["GlobalStats"]
        ws_request_log = wb["RequestLog"]

        current_time = datetime.now()
        month = current_time.month
        year = current_time.year
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Convert command to model name
        model_map = {
            '/imagen3': 'Imagen3',
            '/sdxl': 'SDXL',
            '/flux': 'FluxSchnell',
            '/dalle3': 'DALL-E3'
        }
        model_used = model_map.get(command, "Unknown")

        # Update UserStats
        user_found = False
        for row in ws_user_stats.iter_rows(min_row=2, values_only=False):
            if row[0].value == user_id:
                user_found = True
                # total images
                row[2].value = (row[2].value or 0) + 1
                # model-specific count
                for idx, cell in enumerate(row):
                    col_header = ws_user_stats.cell(row=1, column=idx+1).value
                    if col_header == model_used:
                        cell.value = (cell.value or 0) + 1
                        break
                break

        if not user_found:
            # New row for this user
            new_row = [
                user_id,
                username,
                1,  # total images
                0,  # Imagen3
                0,  # SDXL
                0,  # Flux
                0   # DALL-E3
            ]
            if model_used == 'Imagen3':
                new_row[3] = 1
            elif model_used == 'SDXL':
                new_row[4] = 1
            elif model_used == 'FluxSchnell':
                new_row[5] = 1
            elif model_used == 'DALL-E3':
                new_row[6] = 1
            ws_user_stats.append(new_row)

        # Update GlobalStats
        stats_found = False
        for row in ws_global_stats.iter_rows(min_row=2, values_only=False):
            if row[0].value == month and row[1].value == year:
                stats_found = True
                row[2].value = (row[2].value or 0) + 1
                for idx, cell in enumerate(row):
                    col_header = ws_global_stats.cell(row=1, column=idx+1).value
                    if col_header == model_used:
                        cell.value = (cell.value or 0) + 1
                        break
                break

        if not stats_found:
            new_row = [
                month,
                year,
                1,  # total
                0,  # Imagen3
                0,  # SDXL
                0,  # Flux
                0   # DALL-E3
            ]
            if model_used == 'Imagen3':
                new_row[3] = 1
            elif model_used == 'SDXL':
                new_row[4] = 1
            elif model_used == 'FluxSchnell':
                new_row[5] = 1
            elif model_used == 'DALL-E3':
                new_row[6] = 1
            ws_global_stats.append(new_row)

        # Update RequestLog
        ws_request_log.append([
            timestamp,
            user_id,
            username,
            model_used,
            prompt
        ])

        wb.save(EXCEL_FILE_PATH)
        logger.info("Metrics updated successfully.")
    except Exception as e:
        logger.error(f"Error updating metrics: {e}")

# =============================================================
#                Telegram Bot Handlers
# =============================================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        welcome_message = (
            "Hello! I am InstaVision Bot. 🤩\n"
            "You can generate images using:\n\n"
            "- `/imagen3` (Google Imagen 3*)\n"
            "- `/sdxl` (SDXL Lightning)\n"
            "- `/flux` (Flux Schnell)\n"
            "- `/dalle3` (OpenAI DALL-E 3)\n\n"
            "*Note: Google Imagen 3 is not publicly available.\n"
            "If you try `/imagen3`, you'll get the Google Form link.\n"
            "Type /help for more info!"
        )
        await update.message.reply_text(welcome_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(
            "An unexpected error occurred. Please try again later."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        banned_words_formatted = ', '.join(BANNED_WORDS)
        help_message = (
            "🆘 **InstaVision Bot Help** 🆘\n\n"
            "**Commands**:\n"
            "- `/imagen3`  (Google Imagen 3*)\n"
            "- `/sdxl`     (SDXL Lightning)\n"
            "- `/flux`     (Flux Schnell)\n"
            "- `/dalle3`   (OpenAI DALL-E 3)\n\n"
            "*Using `/imagen3` increments your usage in logs, but you won't get a real image.\n"
            "Instead, you'll get the Google Form link if you want to request access.\n\n"
            "**Daily Limits**:\n"
            "- Default users: 5 images/24h\n"
            "- Fifty/day users: 50 images/24h\n"
            "- Unlimited users: no limit\n\n"
            "**Banned Words**:\n"
            f"{banned_words_formatted}\n"
            "Using them triggers warnings or bans.\n\n"
            "**Feedback**: Use `/feedback` anytime!\n"
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text(
            "An unexpected error occurred while displaying help."
        )

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        username = update.message.from_user.username or "Unknown"

        if is_user_banned(user_id, username):
            ban_expiry_time_str = r.hget(user_id, 'ban_expiry_time')
            if ban_expiry_time_str:
                ban_expiry_time = datetime.strptime(ban_expiry_time_str, "%Y-%m-%d %H:%M:%S")
                time_left = ban_expiry_time - datetime.now()
                if time_left.total_seconds() > 0:
                    if username in fifty_per_day_users:
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_left_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        ban_message = (
                            f"You are currently banned for {time_left_str}.\n\n"
                            "If you think you are banned for no reason, please email instavision001@gmail.com"
                        )
                    else:
                        days = time_left.days
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_left_str = f"{days} days {hours:02d}:{minutes:02d}:{seconds:02d}"
                        ban_message = (
                            f"You are currently banned for {time_left_str}.\n\n"
                            "If you think you are banned for no reason, please email instavision001@gmail.com"
                        )
                else:
                    ban_message = (
                        "You are currently banned from using this bot.\n\n"
                        "If you think you are banned for no reason, please email instavision001@gmail.com"
                    )
            else:
                ban_message = (
                    "You are currently banned from using this bot.\n\n"
                    "If you think you are banned for no reason, please email instavision001@gmail.com"
                )
            await update.message.reply_text(ban_message, parse_mode="Markdown")
            return

        awaiting_feedback[user_id] = True
        await update.message.reply_text(
            "Please type your feedback. 📝\n\n"
            "If you need more than 5 images/day, mail instavision001@gmail.com.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in feedback_command: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

def send_feedback_email(user_id, username, feedback_message):
    try:
        sender_email = "SENDER MAIL ADDRESS"
        receiver_email = "RECEIVER MAIL ADDRESS"
        subject = "Feedback from InstaVision User"
        body = (
            f"User ID: {user_id}\nUsername: {username}\nFeedback:\n{feedback_message}"
        )

        yag = yagmail.SMTP(sender_email, 'SENDER APP PASSWORD')
        yag.send(to=receiver_email, subject=subject, contents=body)
        logger.info(f"Feedback email sent from user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error sending feedback email: {e}")
        return False

async def handle_text_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles text messages: checks for ban, feedback, valid commands, 
    banned words, translation, queueing, etc.
    """
    try:
        user_chat_id = update.message.chat_id

        # Skip group chats
        if update.message.chat.type in ["group", "supergroup"]:
            return

        user_id = update.message.from_user.id
        username = update.message.from_user.username or "Unknown"
        user_input = update.message.text.strip()

        # Ban check
        if is_user_banned(user_id, username):
            ban_expiry_time_str = r.hget(user_id, 'ban_expiry_time')
            if ban_expiry_time_str:
                ban_expiry_time = datetime.strptime(ban_expiry_time_str, "%Y-%m-%d %H:%M:%S")
                time_left = ban_expiry_time - datetime.now()
                if time_left.total_seconds() > 0:
                    if username in fifty_per_day_users:
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_left_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        ban_message = (
                            f"You are banned for {time_left_str}.\n\n"
                            "If you think you are banned unfairly, email instavision001@gmail.com"
                        )
                    else:
                        days = time_left.days
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_left_str = f"{days} days {hours:02d}:{minutes:02d}:{seconds:02d}"
                        ban_message = (
                            f"You are banned for {time_left_str}.\n\n"
                            "If you think you are banned unfairly, email instavision001@gmail.com"
                        )
                else:
                    ban_message = (
                        "You are currently banned.\n\n"
                        "If you think you are banned unfairly, email instavision001@gmail.com"
                    )
            else:
                ban_message = (
                    "You are currently banned.\n\n"
                    "If you think you are banned unfairly, email instavision001@gmail.com"
                )
            await update.message.reply_text(ban_message)
            return

        # If user is providing feedback
        if user_id in awaiting_feedback and awaiting_feedback[user_id]:
            feedback_message = user_input
            feedback_sent = send_feedback_email(user_id, username, feedback_message)
            if feedback_sent:
                await update.message.reply_text("Thank you for your feedback! 🙏")
            else:
                await update.message.reply_text(
                    "We had an issue sending your feedback. "
                    "Please try again or email it manually."
                )
            awaiting_feedback[user_id] = False
            return

        # Recognize the commands
        recognized_commands = r'^(/imagen3|/sdxl|/flux|/dalle3)\s+(.+)?'
        match = re.match(recognized_commands, user_input, re.IGNORECASE)
        if not match:
            await handle_invalid_command(update, context)
            return

        command = match.group(1).lower()
        prompt = match.group(2)
        if not prompt:
            await update.message.reply_text(
                "Please provide a description after the command. "
                "Example: /sdxl A beautiful sunset."
            )
            return

        # Banned words check
        if any(bad.lower() in prompt.lower() for bad in BANNED_WORDS):
            warning_issued = r.hget(user_id, 'warning_issued')
            banned_words_formatted = ', '.join(BANNED_WORDS)

            if username in unlimited_users:
                warning_message = (
                    "🚫 **Warning**: This prompt has a banned word.\n"
                    "Prompt not processed.\n"
                    f"Avoid these words: {banned_words_formatted}"
                )
                await update.message.reply_text(warning_message, parse_mode="Markdown")
                return
            else:
                # normal or fifty
                if warning_issued:
                    # second offense
                    if username in fifty_per_day_users:
                        ban_duration = 24 * 3600
                        ban_user(user_id, ban_duration)
                        await update.message.reply_text(
                            "🚫 You have been banned for 24 hours "
                            "due to repeated use of prohibited words."
                        )
                    else:
                        ban_duration = 7 * 24 * 3600
                        ban_user(user_id, ban_duration)
                        await update.message.reply_text(
                            "🚫 You have been banned for 1 week "
                            "due to repeated use of prohibited words."
                        )
                    return
                else:
                    # first offense
                    r.hset(user_id, 'warning_issued', 1)
                    warning_message = (
                        "🚫 **Warning**: Banned word found; prompt not processed.\n"
                        f"Avoid these words: {banned_words_formatted}\n"
                        "Next time, you will be banned."
                    )
                    await update.message.reply_text(warning_message, parse_mode="Markdown")
                    return

        # Translate prompt if needed
        try:
            translated_prompt = translate_to_english(prompt)
        except Exception as e:
            await update.message.reply_text(str(e))
            return

        # Rate limiting
        limit_check = check_and_update_user_limit(user_id, username)
        if limit_check is None:
            await update.message.reply_text(
                "Technical issue verifying your limit. Please try again later."
            )
            return
        if not limit_check:
            if username in unlimited_users:
                pass
            else:
                # user hit limit
                if username in fifty_per_day_users:
                    limit = 50
                else:
                    limit = 5
                await update.message.reply_text(
                    f"You have reached your limit of {limit} images in 24 hours."
                )
                feedback_text = (
                    "🤖 We hope you're enjoying InstaVision Bot!\n"
                    "We'd love any feedback or suggestions.\n"
                    "Reply to this message with your thoughts.\n\n"
                    "Need more images? Request it via email: instavision001@gmail.com"
                )
                await update.message.reply_text(feedback_text, parse_mode="Markdown")
                awaiting_feedback[user_id] = True
                return

        # All checks passed -> queue the request
        await update.message.reply_text(
            f"Received your request: '{prompt}'. Processing, please wait ~40 seconds."
        )
        await request_queue.put((user_chat_id, user_id, username, prompt, command, translated_prompt))

    except Exception as e:
        logger.error(f"Error in handle_text_confirmation: {e}")
        await update.message.reply_text(
            "An unexpected error occurred while processing your request. Please try again later."
        )

async def handle_invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if contains_unsupported_characters(update.message.text.strip()):
            await update.message.reply_text(
                "Unsupported characters or file formats detected. Provide textual input only."
            )
            return

        error_message = (
            "Invalid input. Use one of the following commands + your prompt:\n"
            "- `/imagen3`\n"
            "- `/sdxl`\n"
            "- `/flux`\n"
            "- `/dalle3`\n"
            "- `/feedback`\n\n"
            "Example: `/sdxl A beautiful sunset over the mountains.`"
        )
        await update.message.reply_text(error_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in handle_invalid_command: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Reject non-text content.
    """
    try:
        await update.message.reply_text(
            "Unsupported characters or file formats detected. Provide textual input only."
        )
    except Exception as e:
        logger.error(f"Error in handle_non_text: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

# =============================================================
#  Send generated image (or logs) to group channel
# =============================================================
async def send_image_to_group(image_path_or_url, user_id, username, description, model_name):
    """
    For /imagen3, we'll send a text-only message (no photo).
    For other commands, we attach the image if we have it.
    """
    try:
        utc_time = datetime.now(timezone.utc)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        current_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")

        username_md = escape_markdown(username)
        description_md = escape_markdown(description)
        model_name_md = escape_markdown(model_name)

        if model_name_md.lower() == '/imagen3':
            # No real image -> send text
            group_message = (
                f"🖼️ **Imagen3 Request Logged**\n"
                f"👤 **User ID**: {user_id}\n"
                f"👥 **Username**: @{username_md}\n"
                f"📅 **Date & Time**: {current_time} (IST)\n"
                f"📝 **Description**: {description_md}\n"
                f"🖥️ **Model Used**: {model_name_md}\n\n"
                "No image generated (Google Imagen 3 is not public)."
            )
            await app.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=group_message,
                parse_mode="Markdown"
            )
        else:
            group_message = (
                f"🖼️ **Image Generated**\n"
                f"👤 **User ID**: {user_id}\n"
                f"👥 **Username**: @{username_md}\n"
                f"📅 **Date & Time**: {current_time} (IST)\n"
                f"📝 **Description**: {description_md}\n"
                f"🖥️ **Model Used**: {model_name_md}"
            )

            if image_path_or_url and os.path.exists(image_path_or_url):
                await app.bot.send_photo(
                    chat_id=GROUP_CHAT_ID,
                    photo=open(image_path_or_url, 'rb'),
                    caption=group_message,
                    parse_mode="Markdown"
                )
            else:
                # fallback (no file found)
                await app.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=group_message + "\n\n(No image file found.)",
                    parse_mode="Markdown"
                )

    except Exception as e:
        logger.error(f"Error in send_image_to_group: {e}")
        subject = "Error Sending Image to Telegram Group"
        body = f"Error sending image/log for user {user_id}.\nError: {e}"
        send_error_email(subject, body)

# =============================================================
#        Process the queue in an asynchronous task
# =============================================================
async def process_queue():
    while True:
        try:
            queue_item = await request_queue.get()
            if queue_item is None:
                break

            user_chat_id, user_id, username, description, command, translated_description = queue_item
            loop = asyncio.get_event_loop()

            logger.info(f"Processing request from user {username} | Command: {command} | Desc: {description}")

            # ------------------------------------------------------------------
            # 1) If command == /imagen3 -> we do NOT generate an image,
            #    but we do everything else as if it's a valid generation.
            # ------------------------------------------------------------------
            if command == '/imagen3':
                # Update metrics
                update_metrics(user_id, username, command, description)

                # Send message to group (text only)
                await send_image_to_group(None, user_id, username, description, command)

                # Inform the user that Google Imagen is not public
                google_form_msg = (
                    "🚫 **Google Imagen 3 is not publicly available**.\n"
                    "Therefore, you cannot generate images with `/imagen3`.\n\n"
                    "If you want to request access to Imagen,\n"
                    "please fill out this form:\n"
                    "[Google Form](https://forms.gle/5nZvxutEuJYG8K6g9)"
                )
                await app.bot.send_message(
                    chat_id=user_chat_id,
                    text=google_form_msg,
                    parse_mode="Markdown"
                )

                request_queue.task_done()
                await asyncio.sleep(1)
                continue

            # ------------------------------------------------------------------
            # 2) For other commands: /sdxl, /flux, /dalle3
            # ------------------------------------------------------------------
            if command == '/sdxl':
                logger.info("Calling SDXL Lightning...")
                image_path = await asyncio.wait_for(
                    loop.run_in_executor(None, generate_image_sdxl, translated_description),
                    timeout=120
                )
                save_folder = SDXL_LIGHTNING_FOLDER

            elif command == '/flux':
                logger.info("Calling Flux Schnell...")
                image_path = await asyncio.wait_for(
                    loop.run_in_executor(None, generate_image_flux_schnell, translated_description),
                    timeout=120
                )
                save_folder = FLUX_SCHNELL_FOLDER

            elif command == '/dalle3':
                logger.info("Calling DALL-E 3...")
                image_url = await asyncio.wait_for(
                    loop.run_in_executor(None, generate_image_dalle, translated_description),
                    timeout=120
                )
                save_folder = DALLE_FOLDER

                # Download the generated image
                response = requests.get(image_url, timeout=60)
                image_bytes = io.BytesIO(response.content)
                input_image_path = f"generated_image_{user_id}.png"
                with open(input_image_path, 'wb') as f:
                    f.write(image_bytes.getbuffer())

                # Watermark
                output_image_path = f"watermarked_image_{user_id}.png"
                add_watermark(input_image_path, output_image_path, "InstaVision")

                # Save locally
                try:
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    local_image_copy_path = os.path.join(save_folder, f"{user_id}_{current_time}.png")
                    watermarked_img = Image.open(output_image_path)
                    watermarked_img.save(local_image_copy_path, format="PNG")
                    logger.info(f"Watermarked image saved locally at {local_image_copy_path}")
                except Exception as e:
                    logger.error(f"Error saving image locally: {e}")
                    send_error_email(
                        "Image Storage and Custom Font Fetching Issue",
                        f"Error saving image for user {user_id}.\nError: {e}"
                    )

                await app.bot.send_photo(chat_id=user_chat_id, photo=open(output_image_path, 'rb'))
                await send_image_to_group(output_image_path, user_id, username, description, command)
                update_metrics(user_id, username, command, description)

                # Cleanup
                if os.path.exists(input_image_path):
                    os.remove(input_image_path)
                if os.path.exists(output_image_path):
                    os.remove(output_image_path)

                request_queue.task_done()
                await asyncio.sleep(1)
                continue

            else:
                # Shouldn't happen given our command recognition
                await app.bot.send_message(
                    chat_id=user_chat_id,
                    text="Invalid command."
                )
                request_queue.task_done()
                await asyncio.sleep(1)
                continue

            # Watermark for /sdxl or /flux
            output_image_path = f"watermarked_image_{user_id}.png"
            add_watermark(image_path, output_image_path, "InstaVision")

            # Save locally
            try:
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                local_image_copy_path = os.path.join(save_folder, f"{user_id}_{current_time}.png")
                watermarked_img = Image.open(output_image_path)
                watermarked_img.save(local_image_copy_path, format="PNG")
                logger.info(f"Watermarked image saved locally at {local_image_copy_path}")
            except Exception as e:
                logger.error(f"Error saving image locally: {e}")
                send_error_email(
                    "Image Storage and Custom Font Fetching Issue",
                    f"Error saving image for user {user_id}.\nError: {e}"
                )

            # Send to user
            await app.bot.send_photo(chat_id=user_chat_id, photo=open(output_image_path, 'rb'))
            # Send to group
            await send_image_to_group(output_image_path, user_id, username, description, command)

            update_metrics(user_id, username, command, description)

            # Cleanup
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(output_image_path):
                os.remove(output_image_path)

            request_queue.task_done()
            await asyncio.sleep(1)

        except asyncio.TimeoutError:
            logger.error("Image generation timed out.")
            await app.bot.send_message(
                chat_id=user_chat_id,
                text="Sorry, your request timed out. Please try again later."
            )
            request_queue.task_done()
        except Exception as e:
            logger.error(f"Error in process_queue: {e}")
            await app.bot.send_message(
                chat_id=user_chat_id,
                text="An error occurred while generating the image. Please try again later."
            )
            request_queue.task_done()
            await asyncio.sleep(1)

# =============================================================
#                 Error Handler
# =============================================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
    try:
        if update and hasattr(update, 'effective_message') and update.effective_message:
            await update.effective_message.reply_text(
                "An unexpected error occurred. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error in error_handler while sending message: {e}")

# =============================================================
#                  Main Entrypoint
# =============================================================
if __name__ == '__main__':
    nest_asyncio.apply()
    app = Application.builder().token(TOKEN).build()

    # Start the queue processing loop
    loop = asyncio.get_event_loop()
    loop.create_task(process_queue())

    # Register handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('feedback', feedback_command))

    # Pattern for text commands (include /imagen3 now)
    command_list = ['/imagen3', '/sdxl', '/flux', '/dalle3']
    command_pattern = '(?i)^(' + '|'.join(map(re.escape, command_list)) + r')\s+'
    command_filter = filters.TEXT & filters.Regex(command_pattern)

    # If matches one of the commands above
    app.add_handler(MessageHandler(command_filter, handle_text_confirmation))

    # Otherwise, handle text as well
    app.add_handler(MessageHandler(filters.TEXT & (~command_filter), handle_text_confirmation))

    # Non-text (images, docs, etc.)
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))

    # Register error handler
    app.add_error_handler(error_handler)

    print('Polling...')
    app.run_polling(poll_interval=3)
