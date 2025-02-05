import sys
import nest_asyncio
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import io
import redis
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
import asyncio
from queue import Queue
import re
from PIL import Image, ImageDraw, ImageFont

# Additional authentication is required for Google Colab
if "google.colab" in sys.modules:
    # Authenticate user to Google Cloud
    from google.colab import auth
    auth.authenticate_user()

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot Constants (Replace these with your own credentials)
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your actual bot token
BOT_USERNAME = '@YOUR_BOT_USERNAME'  # Add your bot's username here
GROUP_CHAT_ID = 'YOUR_GROUP_CHAT_ID'  # Replace with your group's chat ID

# We remove the Google Cloud Imagen references; keeping placeholders if needed.
# Google Cloud project information (currently not used, so can be kept empty)
PROJECT_ID = ""  
LOCATION = ""

# -- Removed Vertex AI import and initialization, as well as the Imagen model import --

# List of banned words
BANNED_WORDS = ['word1','word2']  # Add more words if necessary

# Path to store local images
LOCAL_IMAGE_FOLDER = "/content/drive/MyDrive/YourFolderPath/"  # Replace with your actual folder path

# Function to add watermark (remains in the code, though image generation is disabled)
def add_watermark(input_image_path, output_image_path, watermark_text="InstaVision",
                  font_size=30, text_color=(255, 130, 80, 128), bg_color=(0, 0, 0, 128)):
    try:
        # Open the original image
        original = Image.open(input_image_path)

        # Get dimensions of the original image
        width, height = original.size

        # Create a new Image object to draw the watermark
        watermark = Image.new("RGBA", original.size)
        draw = ImageDraw.Draw(watermark)

        # Load the font with the specified size
        # NOTE: Update the font path if you have a TTF font file
        font = ImageFont.truetype("", font_size)  

        # Get the bounding box of the watermark text
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate the position (bottom-right corner)
        padding = 10
        position = (width - text_width - padding, height - text_height - padding)

        # Calculate the background rectangle size
        rect_position = (position[0] - padding, position[1] - padding,
                         position[0] + text_width + padding, position[1] + text_height + padding)

        # Draw the background rectangle
        draw.rectangle(rect_position, fill=bg_color)

        # Add the watermark text on top of the rectangle
        draw.text(position, watermark_text, fill=text_color, font=font)

        # Combine the original image with the watermark
        watermarked = Image.alpha_composite(original.convert("RGBA"), watermark)

        # Save the output image
        watermarked.save(output_image_path, "PNG")
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise e

# Connect to Redis (Replace with your credentials)
def connect_redis():
    try:
        r = redis.Redis(
            host='YOUR_REDIS_HOST',  # Replace with your Redis Host
            port=YOUR_REDIS_PORT,  # Replace with your Redis Port
            password='YOUR_REDIS_PASSWORD',  # Replace with your Redis Password
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

# Initialize request queue
request_queue = Queue()

# Function to check and update user limits
def check_and_update_user_limit(user_id):
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")

        current_time = datetime.now()
        reset_limit_hours = 24

        request_count = r.hget(user_id, 'request_count')
        last_request_time = r.hget(user_id, 'last_request_time')

        if request_count is None or last_request_time is None:
            r.hset(user_id, mapping={
                'request_count': 1,
                'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            logger.info(f"User {user_id}: Initialized request count and time.")
            return True

        request_count = int(request_count)
        last_request_time = datetime.strptime(last_request_time, "%Y-%m-%d %H:%M:%S")

        if current_time - last_request_time > timedelta(hours=reset_limit_hours):
            r.hset(user_id, mapping={
                'request_count': 1,
                'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
            logger.info(f"User {user_id}: Reset request count and time after 24 hours.")
            return True

        if request_count >= 5:
            logger.info(f"User {user_id} has reached the limit of 5 high-quality images in {reset_limit_hours} hours.")
            if request_count == 5:
                r.hincrby(user_id, 'request_count', 1)
            return False

        r.hincrby(user_id, 'request_count', 1)
        logger.info(f"User {user_id}: Incremented request count = {request_count + 1}")
        return True
    except Exception as e:
        logger.error(f"Error in check_and_update_user_limit: {e}")
        return None

# Function to ban a user
def ban_user(user_id):
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")
        r.hset(user_id, 'banned', 1)
        logger.info(f"User {user_id} has been banned.")
        return True
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return None

# Function to check if a user is banned
def is_user_banned(user_id):
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")
        banned_status = r.hget(user_id, 'banned')
        return banned_status is not None
    except Exception as e:
        logger.error(f"Error checking banned status for user {user_id}: {e}")
        return None

def check_network_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        logger.error(f"Network error: {e}")
        return False

def escape_markdown(text):
    escape_chars = r'\*_\[\]()~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

async def send_image_to_group(image_path_or_url, user_id, username, description):
    """
    In the original code, this function sends the generated image to the group.
    Since generation is disabled, this function might be unused, but we keep it here
    in case you want to re-enable it in the future.
    """
    try:
        # Convert time to IST
        utc_time = datetime.now(timezone.utc)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        current_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")

        username = escape_markdown(username)
        description = escape_markdown(description)

        group_message = (
            f"🖼️ **Image Generated**\n"
            f"👤 **User ID**: {user_id}\n"
            f"👥 **Username**: @{username}\n"
            f"📅 **Date & Time**: {current_time} (IST)\n"
            f"📝 **Description**: {description}"
        )

        await app.bot.send_photo(
            chat_id=GROUP_CHAT_ID, 
            photo=image_path_or_url, 
            caption=group_message, 
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in send_image_to_group: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not check_network_connection():
            await update.message.reply_text('Network error. Please check your internet connection and try again.')
            return

        welcome_message = (
            "Hello! I am InstaVision Bot. 🤩\n"
            "Currently, Google Imagen 3 code is not publicly available for image generation. 🚫\n"
            "Type /help for more information. 🆘\n"
            "Have a great day! 😁"
        )
        await update.message.reply_text(welcome_message)
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

# Help command providing instructions to the user
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_message = (
            "🆘 **InstaVision Bot Help** 🆘\n\n"
            "📜 **Current Status**:\n"
            "Google Imagen 3 code is not publicly released for general use.\n\n"
            "🚫 **Banned Words**:\n"
            f"{', '.join(BANNED_WORDS)}\n\n"
            "📝 **Important Notes**:\n"
            "- Using inappropriate language will lead to a permanent ban.\n"
            "- If you need access to Imagen features, please fill out the following form:\n"
            "  **https://forms.gle/5nZvxutEuJYG8K6g9**"
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text('An unexpected error occurred while displaying the help information.')

async def handle_text_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_chat_id = update.message.chat_id

        # Ignore messages from group chats in this logic
        if update.message.chat.type in ["group", "supergroup"]:
            return

        user_id = update.message.from_user.id
        username = update.message.from_user.username if update.message.from_user.username else "Unknown"
        user_input = update.message.text.strip()

        if is_user_banned(user_id):
            await update.message.reply_text("You are banned from using this bot.")
            return

        # Check for banned words
        if any(banned_word.lower() in user_input.lower() for banned_word in BANNED_WORDS):
            ban_user(user_id)
            await update.message.reply_text("You have used inappropriate language and are permanently banned.")
            return

        # Check user limit
        limit_check = check_and_update_user_limit(user_id)
        if limit_check is None:
            await update.message.reply_text("Technical issue in verifying your request limit. Try later.")
            return

        if not limit_check:
            await update.message.reply_text("You have reached the limit of 5 requests in 24 hours.")
        else:
            # Instead of generating an image, just notify about Imagen 3 unavailability
            await update.message.reply_text(
                "Thanks for your request! However, Google Imagen 3 code is not publicly available.\n"
                "If you need access, please fill out this form:\n"
                "**https://forms.gle/5nZvxutEuJYG8K6g9**",
                parse_mode="Markdown"
            )

            # We can still enqueue the request, but the queue processing will not generate images.
            request_queue.put((user_chat_id, user_id, username, user_input))

    except Exception as e:
        logger.error(f"Error in handle_text_confirmation: {e}")
        await update.message.reply_text('An unexpected error occurred while processing your request. Please try again later.')

async def process_queue():
    """ 
    This function used to generate images with Google Imagen.
    Now it only informs users that image generation is unavailable.
    """
    while True:
        if not request_queue.empty():
            user_chat_id, user_id, username, description = request_queue.get()

            try:
                # Instead of generating or watermarking an image, we just reaffirm the message.
                await app.bot.send_message(
                    chat_id=user_chat_id, 
                    text=(
                        "Reminder: Google Imagen 3 code is **not** publicly available.\n"
                        "If you wish to request access, please fill out this form:\n"
                        "**https://forms.gle/5nZvxutEuJYG8K6g9**"
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Error in process_queue: {e}")
                await app.bot.send_message(chat_id=user_chat_id, text=f"{str(e)}")

        await asyncio.sleep(1)  # Prevent busy waiting

async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "This bot only accepts text inputs in English. Please provide valid text."
        )
    except Exception as e:
        logger.error(f"Error in handle_non_text: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')
    await update.message.reply_text('An unexpected error occurred. Please try again later.')

if __name__ == '__main__':
    nest_asyncio.apply()  # Ensure nested event loops are allowed (for Jupyter or Colab environments)
    app = Application.builder().token(TOKEN).build()

    executor = ThreadPoolExecutor(max_workers=50)  # Handle 50 users simultaneously

    # Start the queue processing loop
    loop = asyncio.get_event_loop()
    loop.create_task(process_queue())

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_confirmation))
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
