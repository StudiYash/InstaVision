# InstaVision Bot using Stable Diffusion based Sdxl Lightning 4step API

InstaVision Bot is a Telegram bot that generates high-quality images based on user-provided text descriptions using the Sdxl Lightning 4step API made by bytedance. The bot also manages user request limits and integrates with a Redis database for storing user data. The bot also allows to ban certain words and also ban the users permanantly from using the bot. The bot also adds a Watermark to every image that it generates. The bot also stores all the images to a local folder.

## Prerequisites

Before running the code, ensure you have the following prerequisites installed and set up:

- Python 3.8 or later
- [Redis](https://redis.io/) (locally installed or cloud-hosted)
- [Telegram Bot API Token](https://core.telegram.org/bots#6-botfather) (Create a bot using BotFather on Telegram)
- [Sdxl Lightning 4step API Key on Replicate Platform](https://replicate.com/account/api-tokens) (Sign up on Replicate to get an API key)

## Installation

1. **Create a Virtual Environment:**

   It is recommended to create a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install the Required Packages:**

   Use `pip` to install the necessary Python packages.

   ```bash
   pip install -r requirements_sdxl.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the root directory of your project and add the following environment variables:

   ```bash
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   BOT_USERNAME=your-bot-username
   GROUP_CHAT_ID=your-group-chat-id
   REPLICATE_API_TOKEN=your-replicate-api-key
   REDIS_HOST=your-redis-host
   REDIS_PORT=your-redis-port
   REDIS_PASSWORD=your-redis-password
   BANNED_WORDS="Word1","Word2"  # Add your desired ban Words
   font=ImageFont.truetype("location_of_font_file", font_size)  # Ensure 'highsens.otf' path is correct or replace with your desired font and path according to it.
   LOCAL_IMAGE_FOLDER = "location_of_desired_folder_to_store_images"  # # Replace with your actual folder path to store the watermarked images.
   ```

   Replace the placeholder values with your actual credentials.

4. **Ensure Redis is Running:**

   If you're using a locally installed Redis, start the Redis server. If using a cloud-hosted Redis, ensure it is properly configured.

   ```bash
   redis-server
   ```

## Running the Bot

After setting up the environment variables and ensuring Redis is running, you can start the bot using the following command:

```bash
python InstaVision_Sdxl-Lightning-4step_API.py
```

The bot should start polling, and you'll see `Polling...` in your terminal, indicating that the bot is now active and listening for messages.

## Usage

- **Start Command:**
  - Send `/start` to the bot to receive a welcome message.
  
- **Generate Image:**
  - Send a text description of the image you want to generate. The bot will respond with a high-quality image based on your description.

- **Request Limit:**
  - Each user can generate up to 5 high-quality images every 24 hours. The bot will notify you if you exceed this limit. You can also modify this limit as per your requirement.

- **Help Command:**
  - Send `/help` to the bot to receive a help message. The help command provides detailed instructions on how to use the bot, including prompt guidelines and a list of banned words.

## Error Handling
The bot includes error handling for network issues, API errors, and Redis connection failures. If an error occurs, the bot will notify you with an appropriate message.

## Banned Words
The bot contains a list of certain words that can be banned from giving as an input to the bot. If the user uses the banned word then the user gets instantly and permanantly banned from using the bot.

## Watermark
The bot also adds a Watermark on every image that it generates. The Watermark text is customizable and is by default it is set to the word "InstaVision". The Watermark Font, Watermark Color and Watermark Background Color all are customizable and by default the Watermark Font is set to Highsens 400 font.

## Storage
The bot also stores all the Watermarked images into a local folder on the device where the bot is being deployed.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to improve the bot.