# InstaVision Bot using Dall E3 API

InstaVision Bot is a Telegram bot that generates high-quality images based on user-provided text descriptions using the OpenAI DALL-E API. The bot also manages user request limits and integrates with a Redis database for storing user data.

## Prerequisites

Before running the code, ensure you have the following prerequisites installed and set up:

- Python 3.8 or later
- [Redis](https://redis.io/) (locally installed or cloud-hosted)
- [Telegram Bot API Token](https://core.telegram.org/bots#6-botfather) (Create a bot using BotFather on Telegram)
- [OpenAI API Key](https://platform.openai.com/account/api-keys) (Sign up on OpenAI to get an API key)

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
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the root directory of your project and add the following environment variables:

   ```bash
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   BOT_USERNAME=your-bot-username
   GROUP_CHAT_ID=your-group-chat-id
   OPENAI_API_KEY=your-openai-api-key
   REDIS_HOST=your-redis-host
   REDIS_PORT=your-redis-port
   REDIS_PASSWORD=your-redis-password
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
python insta_vision_bot.py
```

The bot should start polling, and you'll see `Polling...` in your terminal, indicating that the bot is now active and listening for messages.

## Usage

- **Start Command:**
  - Send `/start` to the bot to receive a welcome message.
  
- **Generate Image:**
  - Send a text description of the image you want to generate. The bot will respond with a high-quality image based on your description.

- **Request Limit:**
  - Each user can generate up to 5 high-quality images every 24 hours. The bot will notify you if you exceed this limit. You can also modigy this limit as per your requirement.

## Error Handling

The bot includes error handling for network issues, API errors, and Redis connection failures. If an error occurs, the bot will notify you with an appropriate message.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to improve the bot.