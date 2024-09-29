# ![InstaVision](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Logo.png)

**InstaVision** is a powerful AI-driven Telegram Bot designed to transform your text descriptions into stunning, high-quality images using various Image Generation APIs. Perfect for creators, students, and anyone with a vivid imagination, InstaVision makes it easy to bring your ideas to life with just a few words.

## 🌟 Features

- **High-Quality Image Generation**: Generate up to 5 high-quality images every 24 hours using various Image Generation APIs.
- **Simultaneous Request Handling**: Capable of processing up to 50 simultaneous requests, ensuring fast and efficient image creation.
- **Rate Limiting**: Enforces user limits to prevent abuse, with a customizable rate-limiting system.
- **Group Image Sharing**: Automatically shares generated images in a specified Telegram group with detailed user information.

## 🚀 Getting Started

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/StudiYash/InstaVision.git
    cd InstaVision
    ```

2. **Run the Bot by Choosing the Appropriate API**:
   - Visit the folder of your API Choice and follow the instructions of the `README.md` file in those individual folders.
   - Configure your Telegram bot token and API keys properly for a flawless experience.

3. **Refer to the YouTube Video for Assistance**:
    [Official InstaVision Setup Video](https://youtu.be/EOWHH2HvRpo)
   
## 🛠️ Technologies Used

- **Python**: The core language for bot logic and processing.
- **Image Generation APIs**: For generating high-quality images from text.
- **Redis**: To manage user limits and request tracking.
- **Telegram Bot API**: For bot interactions and image sharing.

## 📦 Image Generation APIs

- **DALL·E 3 API by OpenAI**: For more information, visit the [Official DALL·E 3 Documentation](https://help.openai.com/en/articles/8555480-dall-e-3-api).
- **Flux Schnell API by black-forest-labs**: For more information, visit the [Official Flux Schnell documentation](https://replicate.com/black-forest-labs/flux-schnell).
- **Sdxl Lightning 4step API by bytedance**: For more information, visit the [Official Sdxl Lightning 4step documentation](https://replicate.com/bytedance/sdxl-lightning-4step/api).

## 📑 Comparing API Outputs

| S.No | Description  | DALL·E 3                       | Flux Schnell                  | SDXL Lightning 4step          |
|------|--------------|-------------------------------|-------------------------------|-------------------------------|
| 01   | Ancient Forest Temple  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/03.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(flux-schnell%20API)/flux_schnell_examples/03.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(sdxl-lightning-4step%20API)/sdxl_lightning_4step_examples/03.jpg) |
| 02   | Cyberpunk Samurai Duel  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/04.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(flux-schnell%20API)/flux_schnell_examples/04.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(sdxl-lightning-4step%20API)/sdxl_lightning_4step_examples/04.jpg) |
| 03   | Alien Planet with Floating Islands  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/05.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(flux-schnell%20API)/flux_schnell_examples/05.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(sdxl-lightning-4step%20API)/sdxl_lightning_4step_examples/05.jpg) |
| 04   | Deserted Amusement Park in the Future  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/07.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(flux-schnell%20API)/flux_schnell_examples/07.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(sdxl-lightning-4step%20API)/sdxl_lightning_4step_examples/07.jpg) |
| 05   | Mythical Phoenix Rising from Ashes  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/08.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(flux-schnell%20API)/flux_schnell_examples/08.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Bot%20(sdxl-lightning-4step%20API)/sdxl_lightning_4step_examples/08.jpg) |

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more details, please refer to the [LICENSE](https://github.com/StudiYash/InstaVision/blob/main/LICENSE) file in the repository.

By using this project, you agree to give appropriate credit, not use the material for commercial purposes without permission, and share any adaptations under the same license.

Attribution should be given as: "InstaVision Bot by Yash Shukla (https://github.com/StudiYash/InstaVision)"

Quick Overview regarding the permissions of usage of this project can be found on [LICENSE DEED : CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

## 🎉 Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

- **Contributor License Agreement (CLA)**: By submitting a pull request, you confirm that you have read and agree to the terms of the [Contributor License Agreement (CLA)](https://github.com/StudiYash/InstaVision/blob/main/CLA.md).

- **Code of Conduct**: This project and everyone participating in it are governed by the [InstaVision Code of Conduct](https://github.com/StudiYash/InstaVision/blob/main/CODE_OF_CONDUCT.md).

- **Contributors**: See the list of contributors [here](https://github.com/StudiYash/InstaVision/blob/main/CONTRIBUTORS.md).

Made with ❤️ by [Yash Shukla](https://www.linkedin.com/in/yash-shukla-2024aiguy/)
