# InstaVision 🎨

**InstaVision** is a powerful AI-driven Telegram Bot designed to transform your text descriptions into stunning, high-quality images using various Image Generation APIs. Perfect for creators, students, and anyone with a vivid imagination, InstaVision makes it easy to bring your ideas to life with just a few words.

## 🌟 Features

- **High-Quality Image Generation**: Generate up to 5 high-quality images every 24 hours various Image Generation APIs.
- **Simultaneous Request Handling**: Capable of processing up to 50 simultaneous requests, ensuring fast and efficient image creation.
- **Rate Limiting**: Enforces user limits to prevent abuse, with a customizable rate limiting system.
- **Group Image Sharing**: Automatically shares generated images in a specified Telegram group with detailed user information.

## 🚀 Getting Started

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/StudiYash/InstaVision.git
    cd InstaVision
    ```

2. **Set Up Your Environment**:
   - Install the necessary Python packages as per your choice of Image Generation API.
   - Configure your Telegram bot token and API keys.

3. **Run the Bot**:
   ```bash
   python instavision_bot.py

## 🛠️ Technologies Used

- **Python**: The core language for bot logic and processing.
- **Image Generation APIs**: For generating high-quality images from text.
- **Redis**: To manage user limits and request tracking.
- **Telegram Bot API**: For bot interactions and image sharing.

## 📦 Image Generation APIs

- **Dall E3 API by OpenAI**: For more information, visit the [Official Dall E3 Documentation](https://help.openai.com/en/articles/8555480-dall-e-3-api).
- **Flux Schnell API by black-forest-labs**: For more information, visit the [Official Flux Schnell documentation](https://replicate.com/black-forest-labs/flux-schnell).
- **Flux Dev Controlnet API by xlabs-ai**: For more information, visit the [Official Flux Dev Controlnet documentation](https://replicate.com/xlabs-ai/flux-dev-controlnet).
- **Sdxl Lightning 4step API by bytedance**: For more information, visit the [Official Sdxl Lightning 4step documentation](https://replicate.com/bytedance/sdxl-lightning-4step/api).

## 🎉 Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

Made with ❤️ by Yash Shukla
