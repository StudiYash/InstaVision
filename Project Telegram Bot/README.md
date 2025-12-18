# Telegram Bot Introduction 🛡️ 

## 1. Abstract 🔮
**InstaVision Telegram Bot** is a powerful AI-driven Telegram Bot designed to transform your text descriptions into stunning, high-quality images using various Image Generation APIs. Perfect for creators, students, and anyone with a vivid imagination, InstaVision makes it easy to bring your ideas to life with just a few words.

---

## 2. Features 🦾
- **High-Quality Image Generation**: Generate unlimited number of  high-quality images using various Image Generation APIs.
- **Simultaneous Request Handling**: Capable of processing up to 50 simultaneous requests, ensuring fast and efficient image creation.
- **Rate Limiting**: Enforces user limits to prevent abuse, with a customizable rate-limiting system. The rate-limiting system supports unlimited users, privileged users (50 images/day), and default users (5 images/day).
- **Group Image Sharing**: Automatically shares generated images in a specified Telegram group with detailed user information.
- **Banned Words Detection**: Identifies and restricts the use of inappropriate words in prompts to maintain system integrity.
- **Banned User Management**: Implements temporary and permanent bans for users violating policies, managed via Redis.
- **Translation to English**: Automatically detects the input language and translates non-English prompts to English for processing. Supports in total 80 different languages from various countries. For a detailed list of languages [click here.](https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/InstaVision_Supported_Languages.pdf)
- **Watermarking**: Adds a customizable watermark to every generated image to preserve brand identity and discourage misuse. Also allows the use of custom fonts for watermarking, with a fallback to default fonts if unavailable.
- **Error Handling**: Includes robust error handling with email notifications for critical issues like API failures or image storage errors.
- **Feedback System**: Allows users to provide feedback directly through the bot, with automated email notifications sent to administrators.
- **Excel Metrics Tracking**: Tracks user activity, usage statistics, and model-specific metrics in an organized Excel file. Logs all bot activities, including user interactions and system errors, for monitoring and debugging.
- **User-Friendly Commands**: Offers intuitive commands for easy interaction, including `/start`, `/help`, `/feedback`, and model-specific commands.
- **Local Storage**: Saves generated and watermarked images in structured local folders for easy access and organization.

---

## 3. Prerequisites 📃

Before setting up the bot, ensure you have the following:

- **Python 3.10 or later**
- **Redis Server** (with access credentials: host, port, password)
- **Telegram Bot API Token** (from [BotFather](https://core.telegram.org/bots/tutorial))
- **Replicate API Key** (for SDXL Lightning and Flux Schnell models)
- **OpenAI API Key** (for DALL-E 3 model)
- **Yagmail Configuration** (for email notifications)

---

## 4. Comparing Telegram Bot API Outputs 😎 

| S.No | Description  | DALL·E 3                       | Flux Schnell                  | SDXL Lightning          | Imagen3                       |
|------|--------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|
| 01   | Ancient Forest Temple  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/03.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/03.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/03.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/03.png) |
| 02   | Cyberpunk Samurai Duel  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/04.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/04.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/04.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/04.png) |
| 03   | Alien Planet with Floating Islands  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/05.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/05.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/05.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/05.png) |
| 04   | Deserted Amusement Park in the Future  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/07.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/07.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/07.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/07.png) |
| 05   | Mythical Phoenix Rising from Ashes  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/08.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/08.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/08.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Telegram%20Bot/Telegram%20Bot%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/08.png) |

---

## 5. Telegram Bot Setup 🎥 

<!-- ▶️ Telegram Bot Setup Video -->
  <a href="https://drive.google.com/file/d/1UX1-N35ogm18IVjCMZFyHPCjY0cgMRzz/view?usp=sharing">
    <img src="https://img.shields.io/badge/Watch-Telegram%20Bot%20Setup-red?style=for-the-badge&logo=google-drive" alt="Telegram Bot Setup">

Below is the complete list of environment variables and file paths you need to configure for the bot to run:

### Telegram Bot Configuration
- **`TOKEN`**: Replace with your Telegram Bot Token.
- **`BOT_USERNAME`**: Set your bot's username.
- **`GROUP_CHAT_ID`**: Set the group chat ID where the bot will send updates.

### OpenAI Configuration
- **`openai.api_key`**: Replace with your OpenAI API key.

### Replicate Configuration
- Set the environment variable:
  ```bash
  export REPLICATE_API_TOKEN="Your_Replicate_API_Key"
  ```

### Redis Configuration
Update the Redis connection details in the script:
```python
host='REDIS HOST',
port=9999,
password='REDIS PASSWORD'
```

### Email Configuration
Update the email settings in the `send_error_email` function:
- **`sender_email`**: Your email address.
- **`app_password`**: Your email's app-specific password.
- **`receiver_email`**: Email address for receiving error notifications.

### Local Directories
Ensure the following paths are set correctly:
- **`SDXL_LIGHTNING_FOLDER`**: Path to store SDXL Lightning-generated images.
- **`FLUX_SCHNELL_FOLDER`**: Path to store Flux Schnell-generated images.
- **`DALLE_FOLDER`**: Path to store DALL-E images.
- **`EXCEL_FILE_PATH`**: Path to save the metrics Excel file.
- **`FONT_PATH`**: Path to the font file for watermarking (e.g., `HIGHSENS 400.otf`).

### Watermark Configuration
Customize watermark settings in the `add_watermark` function:
- **`watermark_text`**: Default is `InstaVision`.
- **`font_size`**: Adjust the size of the watermark text.
- **`text_color`**: Set the RGBA values for the text color.
- **`bg_color`**: Set the RGBA values for the background color.

### Watch the Setup Video
If you are still facing any issues in setting up the InstaVision Telegram bot then watch the vieo below.

<div align="center">
  <a href="https://www.youtube.com/watch?v=EOWHH2HvRpo" target="_blank">
  <img src="https://img.youtube.com/vi/EOWHH2HvRpo/0.jpg" alt="InstaVision Setup Video" width="600" height="350">
  </a>
</div>
Click the image above to watch the setup video for InstaVision!

---

## 6. How to Use ♟️

### Start the Bot
Run the bot locally:
```bash
python InstaVision_Telegram_Bot.py
```

### Commands
- `/start`: Displays a welcome message and available commands.
- `/help`: Provides detailed usage instructions.
- `/feedback`: Allows users to send feedback to the bot admin.
- `/imagen3`: Logs a request for Google Imagen 3 (no real image generation).
- `/sdxl`: Generates an image using SDXL Lightning.
- `/flux`: Generates an image using Flux Schnell.
- `/dalle3`: Generates an image using OpenAI DALL-E 3.

---

## 7. Features in Detail 📇

### Rate Limiting
The bot enforces the following limits:
- **Default Users**: 5 images/day.
- **Privileged Users**: 50 images/day.
- **Admin Users**: Unlimited images.

### Watermarking
Watermark settings can be customized in the `add_watermark` function:
- **`watermark_text`**: Default is `InstaVision`.
- **`font_size`**: Adjust the size of the watermark text.

### Feedback Collection
User feedback is emailed to the bot admin. Ensure email credentials are correctly configured.

---

## 8. Error Handling 🆘

- **Redis Connection Failure**: Logs an error and skips Redis-dependent operations.
- **API Authentication Errors**: Sends an email notification to the admin.
- **Translation Failures**: Requests users to reword their input.
- **Feedback Email Failure**: Prompts users to manually email their feedback.

---

## 9. Image Generation APIs 📦 

- **DALL·E 3 API by OpenAI**: For more information, visit the [Official DALL·E 3 Documentation](https://help.openai.com/en/articles/8555480-dall-e-3-api).
- **Flux Schnell API by black-forest-labs**: For more information, visit the [Official Flux Schnell documentation](https://replicate.com/black-forest-labs/flux-schnell).
- **Sdxl Lightning 4step API by bytedance**: For more information, visit the [Official Sdxl Lightning 4step documentation](https://replicate.com/bytedance/sdxl-lightning-4step/api).
- **Imagen3 API by Google**: For more information, visit the [Official Imagen3 Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview).

---

## 10. Contributions 🔖
Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

---