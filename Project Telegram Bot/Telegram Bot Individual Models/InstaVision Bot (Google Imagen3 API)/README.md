# InstaVision Bot using Google Imagen 3 API

InstaVision Bot is a Telegram bot designed to generate high-quality images based on user-provided text descriptions. However, as of now, Google Imagen 3's API is not publicly available, and users are unable to generate images using this bot. If you wish to request access to Imagen 3, please fill out this Google Form: **[https://forms.gle/5nZvxutEuJYG8K6g9]**. The bot still manages user request limits, bans certain words, and integrates with a Redis database for storing user data.

## Prerequisites

Before running the code, ensure you have the following prerequisites installed and set up:

- Python 3.8 or later
- [Redis](https://redis.io/) (locally installed or cloud-hosted)
- [Telegram Bot API Token](https://core.telegram.org/bots#6-botfather) (Create a bot using BotFather on Telegram)

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
   pip install -r requirements_imagen3.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the root directory of your project and add the following environment variables:

   ```bash
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   BOT_USERNAME=your-bot-username
   GROUP_CHAT_ID=your-group-chat-id
   REDIS_HOST=your-redis-host
   REDIS_PORT=your-redis-port
   REDIS_PASSWORD=your-redis-password
   BANNED_WORDS="Word1","Word2"  # Add your desired ban words
   LOCAL_IMAGE_FOLDER="location_of_desired_folder_to_store_images"  # Replace with the folder path to store images
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
python InstaVision_Imagen3_API.py
```

The bot should start polling, and you'll see `Polling...` in your terminal, indicating that the bot is now active and listening for messages.

## Usage

- **Start Command:**
  - Send `/start` to the bot to receive a welcome message.
  - The bot will inform you that Google Imagen 3 is currently not publicly available and will provide a link to the Google Form where you can request access.

- **Generate Image Request:**
  - If you send a text description requesting image generation, the bot will reply with a message informing you that image generation is not currently supported due to Google Imagen 3's API restrictions.
  - It will also provide a link to the Google Form where you can request access to Imagen 3.

- **Help Command:**
  - Send `/help` to the bot to receive a help message, which will include information on why Google Imagen 3 is not available and how to request access.

## Error Handling

The bot includes error handling for network issues, Redis connection failures, and improper user inputs. If an error occurs, the bot will notify you with an appropriate message.

## Banned Words

The bot contains a list of certain words that can be banned from being given as input to the bot. If a user uses a banned word, they are instantly and permanently banned from using the bot.

## Storage

Although image generation is currently unavailable, the bot is designed to store all generated images in a local folder when functionality is restored.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to improve the bot.

---

If you are interested in gaining access to Google Imagen 3, please fill out this Google Form: **[https://forms.gle/5nZvxutEuJYG8K6g9]**.
