import nest_asyncio
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import io
import redis
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import openai
import asyncio
from queue import Queue

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot Constants
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Add your bot token in the environment variables
BOT_USERNAME = os.getenv('BOT_USERNAME')  # Add your bot's username in the environment variables
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')  # Replace with your group's chat ID stored in the environment variables

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Add your OpenAI API key in the environment variables

# Connect to Redis
def connect_redis():
    try:
        r = redis.Redis(
            host=os.getenv('REDIS_HOST'),   # Replace with your Redis server's hostname or IP address, retrieved from environment variables.
            port=os.getenv('REDIS_PORT'),   # Replace with your Redis server's port number, retrieved from environment variables.
            password=os.getenv('REDIS_PASSWORD'),   # Replace with your Redis server's password, retrieved from environment variables.
            db=0    # The Redis database number to connect to (default is 0).
        )
        # Test connection
        r.ping()
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
            # If either value is missing, initialize them
            r.hset(user_id, mapping={'request_count': 1, 'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")})
            logger.info(f"User {user_id}: Initialized Request Count and Time.")
            return True

        # Convert request_count to an integer
        request_count = int(request_count)

        # Decode last_request_time from bytes to string and then parse to datetime
        last_request_time = datetime.strptime(last_request_time.decode('utf-8'), "%Y-%m-%d %H:%M:%S")

        # Check if 24 hours have passed
        if current_time - last_request_time > timedelta(hours=reset_limit_hours):
            # Reset the count and time if more than 24 hours have passed
            r.hset(user_id, mapping={'request_count': 1, 'last_request_time': current_time.strftime("%Y-%m-%d %H:%M:%S")})
            logger.info(f"User {user_id}: Reset Request Count and Time after 24 hours.")
            return True

        if request_count >= 5:
            logger.info(f"User {user_id} has reached the limit of 5 high-quality images in {reset_limit_hours} hours.")
            if request_count == 5:
                r.hincrby(user_id, 'request_count', 1)  # Increment to prevent repeated messages
            return False

        # Increment the request count
        r.hincrby(user_id, 'request_count', 1)
        logger.info(f"User {user_id}: Incremented Request Count = {request_count + 1}")
        return True
    except Exception as e:
        logger.error(f"Error in check_and_update_user_limit: {e}")
        return None

def check_network_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        logger.error(f"Network error: {e}")
        return False

def generate_image_dalle(prompt: str):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except openai.error.AuthenticationError:
        raise Exception("Image generation system is currently facing an issue. Please try again later.")
    except Exception as e:
        logger.error(f"Error generating image with DALL-E: {e}")
        raise Exception("Your request was rejected as a result of our safety system. Your prompt may contain text that is not allowed by our safety system.")

async def send_image_to_group(image_path_or_url, user_id, username, description):
    try:
        # Convert the current time to IST
        utc_time = datetime.now(timezone.utc)
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        current_time = ist_time.strftime("%Y-%m-%d %H:%M:%S")

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
            "Hello! I am a InstaVision Bot specially made for generating stunning images just using the description of the image. \n"
            " \n"
            "You can provide the description of the image in the textual format in English language.\n"
            " \n"
            "You can generate 5 high quality images in every 24 hours.\n"
            " \n"
            "Have a happy time generating Images 😊😊"
        )
        await update.message.reply_text(welcome_message)
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text('An unexpected error occurred. Please try again later.')

async def handle_text_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_chat_id = update.message.chat_id

        # Ignore messages from the group chat
        if update.message.chat.type in ["group", "supergroup"]:
            return

        user_id = update.message.from_user.id
        username = update.message.from_user.username if update.message.from_user.username else "Unknown"
        user_input = update.message.text.strip()

        limit_check = check_and_update_user_limit(user_id)
        if limit_check is None:
            await update.message.reply_text("The bot is facing a technical issue in verifying your request limit. Please try again later.")
            return

        if not limit_check:
            await update.message.reply_text("You have reached the limit of 10 high-quality images in 24 hours.")
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

            # Ensure that we're running in the correct event loop
            loop = asyncio.get_event_loop()
            try:
                # Generate high-quality image using DALL-E
                image_url = await loop.run_in_executor(None, generate_image_dalle, description)
                await app.bot.send_photo(chat_id=user_chat_id, photo=image_url)
                await send_image_to_group(image_url, user_id, username, description)
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
    nest_asyncio.apply()  # Ensure that nested event loops are allowed (for Jupyter or Colab environments)
    app = Application.builder().token(TOKEN).build()

    executor = ThreadPoolExecutor(max_workers=50)  # Handle 50 users simultaneously

    # Start the queue processing loop
    loop = asyncio.get_event_loop()
    loop.create_task(process_queue())

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_confirmation))
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))  # Catch non-text inputs
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
