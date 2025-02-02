import nest_asyncio
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import io
import redis
from datetime import datetime, timedelta, timezone
import asyncio
from queue import Queue
import re
from PIL import Image, ImageDraw, ImageFont
import replicate

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot Constants (Replace these with your own credentials)
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your actual bot token
BOT_USERNAME = '@YOUR_BOT_USERNAME'  # Add your bot's username here
GROUP_CHAT_ID = 'YOUR_GROUP_CHAT_ID'  # Replace with your group's chat ID

# Set Replicate API token
os.environ['REPLICATE_API_TOKEN'] = 'YOUR_REPLICATE_API_TOKEN'  # Replace with your actual API token

# List of banned words
BANNED_WORDS = ["Word1","Word2","Word3"]  # Add the words that you dont want to the user to use.

# Path to store local images
LOCAL_IMAGE_FOLDER = "/content/drive/MyDrive/YourFolderPath/"  # Replace with your actual folder path

# Ensure the local image folder exists
if not os.path.exists(LOCAL_IMAGE_FOLDER):
    os.makedirs(LOCAL_IMAGE_FOLDER)

# Function to add watermark
def add_watermark(input_image_path, output_image_path, watermark_text="InstaVision", font_size=30,
                  text_color=(255, 130, 80, 128), bg_color=(0, 0, 0, 128)):
    try:
        # Open the original image
        original = Image.open(input_image_path).convert("RGBA")

        # Get dimensions
        width, height = original.size

        # Create watermark image
        watermark = Image.new("RGBA", original.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Load font
        try:
            font = ImageFont.truetype("/content/drive/MyDrive/HIGHSENS 400.otf", font_size)  # Update with your font path
        except IOError:
            logger.warning("Specified font not found. Using default font.")
            font = ImageFont.load_default()

        # Calculate text size
        try:
            # For newer versions of Pillow
            text_width, text_height = font.getsize(watermark_text)
        except AttributeError:
            try:
                # For older versions of Pillow
                text_width, text_height = draw.textsize(watermark_text, font=font)
            except AttributeError:
                try:
                    # For even older versions
                    mask = font.getmask(watermark_text)
                    text_width, text_height = mask.size
                except Exception as e:
                    logger.error(f"Unable to calculate text size: {e}")
                    # Fallback to approximate values
                    text_width = len(watermark_text) * font_size * 0.5
                    text_height = font_size

        # Calculate the position (bottom-right corner)
        padding = 10
        position = (width - text_width - padding, height - text_height - padding)

        # Calculate the background rectangle size
        rect_position = (
            position[0] - padding, position[1] - padding,
            position[0] + text_width + padding, position[1] + text_height + padding
        )

        # Draw the background rectangle
        draw.rectangle(rect_position, fill=bg_color)

        # Add the watermark text
        draw.text(position, watermark_text, fill=text_color, font=font)

        # Combine images
        watermarked = Image.alpha_composite(original, watermark)

        # Save image
        watermarked.convert("RGB").save(output_image_path, "PNG")
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise e

# Connect to Redis
def connect_redis():
    try:
        r = redis.Redis(
            host='YOUR_REDIS_HOST',  # Replace with your Redis Host
            port=YOUR_REDIS_PORT,  # Replace with your Redis Port
            password='YOUR_REDIS_PASSWORD',  # Replace with your Redis Password
            db=0,
            decode_responses=True
        )
        # Test connection
        r.ping()
        logger.info("Connected to Redis successfully.")
        return r
    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
        return None

r = connect_redis()

# Initialize queue
request_queue = Queue()

# Function to check and update user limits
def check_and_update_user_limit(user_id):
    try:
        if not r:
            raise redis.ConnectionError("Cannot connect to Redis")

        current_time = datetime.now()
        reset_limit_hours = 24

        # Get current request count and last request time
        request_count = r.hget(user_id, 'request_count')
        last_request_time = r.hget(user_id, 'last_request_time')

        if request_count is None or last_request_time is None:
            # Initialize them if they don't exist
            r.hset(user_id, mapping={'request_count': 1, 'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")})
            logger.info(f"User {user_id}: Initialized request count and time.")
            return True

        # Convert request_count to integer
        request_count = int(request_count)

        # Parse last_request_time
        last_request_time = datetime.strptime(last_request_time, "%Y-%m-%d %H:%M:%S")

        # Check if 24 hours have passed
        if current_time - last_request_time > timedelta(hours=reset_limit_hours):
            # Reset count and time
            r.hset(user_id, mapping={'request_count': 1, 'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")})
            logger.info(f"User {user_id}: Reset request count and time after 24 hours.")
            return True

        if request_count >= 5:
            logger.info(f"User {user_id} has reached the limit of 5 high-quality images in {reset_limit_hours} hours.")
            if request_count == 5:
                r.hincrby(user_id, 'request_count', 1)  # Prevent repeated messages
            return False

        # Increment request count
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

def generate_image_sdxl(prompt: str):
    try:
        output = replicate.run(
            "bytedance/sdxl-lightning-4step:5f24084160c9089501c1b3545d9be3c27883ae2239b6f412990e82d4a6210f8f",
            input={"prompt": prompt}
        )
        return output[0]  # Assuming the output URL is the first item in the list
    except Exception as e:
        logger.error(f"Error generating image with SDXL Lightning: {e}")
        raise Exception("There was an issue generating your image. Please try again later.")

def escape_markdown(text):
    escape_chars = r'\*_`\[\]()~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

async def send_image_to_group(image_path_or_url, user_id, username, description):
    try:
        # Convert the current time to IST
        utc_time = datetime.now(timezone.utc)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        current_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")

        # Escape markdown characters
        username = escape_markdown(username)
        description = escape_markdown(description)

        # Prepare the message with user details
        group_message = (
            f"🖼️ **Image Generated**\n"
            f"👤 **User ID**: {user_id}\n"
            f"👥 **Username**: @{username}\n"
            f"📅 **Date & Time**: {current_time} (IST)\n"
            f"📝 **Description**: {description}"
        )

        # Send the image and the details to the group chat
        await app.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=image_path_or_url, caption=group_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in send_image_to_group: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not check_network_connection():
            await update.message.reply_text('Network error. Please check your internet connection and try again.')
            return

        welcome_message = (
            "Hello! I am InstaVision Bot made for generating stunning images based on descriptions. 🤩\n"
            "You can generate 5 high-quality images every 24 hours. 💯\n"
            "Type /help to understand what type of input the bot requires. 🆘\n"
            "Have a great time generating images! 😁"
        )
        await update.message.reply_text(welcome_message)
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_message = (
            "🆘 **InstaVision Bot Help** 🆘\n\n"
            "📜 **How to Use the Bot**:\n"
            "1. Provide a detailed description of the image you want.\n"
            "2. Example: 'A serene mountain landscape during sunset.'\n\n"
            "📷 **Image Generation**:\n"
            "- Generate up to **5 high-quality images every 24 hours**.\n\n"
            "🚫 **Banned Words**:\n"
            f"{', '.join(BANNED_WORDS)}\n\n"
            "📝 **Important Notes**:\n"
            "- Avoid using inappropriate language to prevent a permanent ban.\n"
            "- Ensure your prompts are clear and detailed for the best results."
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text('An unexpected error occurred while displaying the help information.')

async def handle_text_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_chat_id = update.message.chat_id

        # Ignore messages from the group chat
        if update.message.chat.type in ["group", "supergroup"]:
            return

        user_id = update.message.from_user.id
        username = update.message.from_user.username if update.message.from_user.username else "Unknown"
        user_input = update.message.text.strip()

        # Check if the user is banned
        if is_user_banned(user_id):
            await update.message.reply_text("You are banned from using this bot.")
            return

        # Check for banned words
        if any(banned_word.lower() in user_input.lower() for banned_word in BANNED_WORDS):
            ban_user(user_id)
            await update.message.reply_text("You have used inappropriate language and are permanently banned.")
            return

        limit_check = check_and_update_user_limit(user_id)
        if limit_check is None:
            await update.message.reply_text("The bot is facing a technical issue in verifying your request limit. Please try again later.")
            return

        if not limit_check:
            await update.message.reply_text("You have reached the limit of 5 high-quality images in 24 hours.")
        else:
            await update.message.reply_text(f"Received your request: '{user_input}'. The bot is processing your request, please wait...")
            request_queue.put((user_chat_id, user_id, username, user_input))

    except Exception as e:
        logger.error(f"Error in handle_text_confirmation: {e}")
        await update.message.reply_text('An unexpected error occurred while processing your request. Please try again later.')

async def process_queue():
    while True:
        if not request_queue.empty():
            user_chat_id, user_id, username, description = request_queue.get()

            loop = asyncio.get_event_loop()
            try:
                # Generate the image using SDXL Lightning
                image_url = await loop.run_in_executor(None, generate_image_sdxl, description)

                # Download the generated image
                response = requests.get(image_url)
                image_bytes = io.BytesIO(response.content)

                # Save the generated image locally for watermarking
                input_image_path = f"generated_image_{user_id}.png"
                with open(input_image_path, 'wb') as f:
                    f.write(image_bytes.getbuffer())

                # Apply watermark
                output_image_path = f"watermarked_image_{user_id}.png"
                add_watermark(input_image_path, output_image_path, "InstaVision")

                # Save the watermarked image locally
                try:
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    local_image_copy_path = os.path.join(LOCAL_IMAGE_FOLDER, f"{user_id}_{current_time}.png")
                    watermarked_img = Image.open(output_image_path)
                    watermarked_img.save(local_image_copy_path, format="PNG")

                    logger.info(f"Watermarked image saved locally at {local_image_copy_path} for user {user_id}")
                except Exception as e:
                    logger.error(f"Error saving image locally: {e}")

                # Send the watermarked image to the user
                await app.bot.send_photo(chat_id=user_chat_id, photo=open(output_image_path, 'rb'))

                # Send the image to the group
                await send_image_to_group(output_image_path, user_id, username, description)

                # Clean up temporary files
                if os.path.exists(input_image_path):
                    os.remove(input_image_path)
                if os.path.exists(output_image_path):
                    os.remove(output_image_path)

            except Exception as e:
                logger.error(f"Error in process_queue: {e}")
                await app.bot.send_message(chat_id=user_chat_id, text=f"{str(e)}")

        await asyncio.sleep(1)  # Prevent busy waiting

async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text('This bot only accepts text inputs in English. Please provide a valid text input.')
    except Exception as e:
        logger.error(f"Error in handle_non_text: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')
    await update.message.reply_text('An unexpected error occurred. Please try again later.')

if __name__ == '__main__':
    nest_asyncio.apply()  # Ensure that nested event loops are allowed
    app = Application.builder().token(TOKEN).build()

    # Start the queue processing loop
    loop = asyncio.get_event_loop()
    loop.create_task(process_queue())

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))  # Added help command handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_confirmation))
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))  # Catch non-text inputs
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
