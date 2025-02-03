# ![InstaVision](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Logo.png)

## Project Introduction 🛡️ 

### Abstract 
**InstaVision** is a powerful AI-driven Telegram Bot designed to transform your text descriptions into stunning, high-quality images using various Image Generation APIs. Perfect for creators, students, and anyone with a vivid imagination, InstaVision makes it easy to bring your ideas to life with just a few words.

### Features

- **High-Quality Image Generation**: Generate unlimited number of  high-quality images using various Image Generation APIs.
- **Simultaneous Request Handling**: Capable of processing up to 50 simultaneous requests, ensuring fast and efficient image creation.
- **Rate Limiting**: Enforces user limits to prevent abuse, with a customizable rate-limiting system. The rate-limiting system supports unlimited users, privileged users (50 images/day), and default users (5 images/day).
- **Group Image Sharing**: Automatically shares generated images in a specified Telegram group with detailed user information.
- **Banned Words Detection**: Identifies and restricts the use of inappropriate words in prompts to maintain system integrity.
- **Banned User Management**: Implements temporary and permanent bans for users violating policies, managed via Redis.
- **Translation to English**: Automatically detects the input language and translates non-English prompts to English for processing. Supports in total 80 different languages from various countries.
- **Watermarking**: Adds a customizable watermark to every generated image to preserve brand identity and discourage misuse. Also allows the use of custom fonts for watermarking, with a fallback to default fonts if unavailable.
- **Error Handling**: Includes robust error handling with email notifications for critical issues like API failures or image storage errors.
- **Feedback System**: Allows users to provide feedback directly through the bot, with automated email notifications sent to administrators.
- **Excel Metrics Tracking**: Tracks user activity, usage statistics, and model-specific metrics in an organized Excel file. Logs all bot activities, including user interactions and system errors, for monitoring and debugging.
- **User-Friendly Commands**: Offers intuitive commands for easy interaction, including `/start`, `/help`, `/feedback`, and model-specific commands.
- **Local Storage**: Saves generated and watermarked images in structured local folders for easy access and organization.

**Index Terms:** AI-driven Telegram Bot, High-Quality Image Generation, Image Generation APIs, Redis Database,  Watermarking, Rate Limiting, Simultaneous Request Handling, Custom Error Handling, User Feedback System, Banned Words Detection, Translation to English, Excel Metrics Tracking, Async Request Queue, Real-Time Logging.

### Project Timeline 

- **Start Date**: 22nd August 2024
- **End Date**: 6th February 2025
- **Total Time Required**: 5 Months and 16 Days

### My Introduction 

| Name                   | GitHub Profile | LinkedIn Profile |
|--------------------------------|----------------|------------------|
| **Yash Suhas Shukla**          | [GitHub](https://github.com/StudiYash) | [LinkedIn](https://www.linkedin.com/in/yash-shukla-2024aiguy/) |

<div align="center">
  <img src="https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/About%20Me.png" alt="Introduction Image" width="800" height="450">
</div>

---

## Project Setup 🎥 

### Watch the Setup Video

<div align="center">
  <a href="https://www.youtube.com/watch?v=EOWHH2HvRpo" target="_blank">
  <img src="https://img.youtube.com/vi/EOWHH2HvRpo/0.jpg" alt="InstaVision Setup Video" width="600" height="350">
  </a>
</div>

Click the image above to watch the setup video for InstaVision!


---
## Image Generation APIs 📦 

- **DALL·E 3 API by OpenAI**: For more information, visit the [Official DALL·E 3 Documentation](https://help.openai.com/en/articles/8555480-dall-e-3-api).
- **Flux Schnell API by black-forest-labs**: For more information, visit the [Official Flux Schnell documentation](https://replicate.com/black-forest-labs/flux-schnell).
- **Sdxl Lightning 4step API by bytedance**: For more information, visit the [Official Sdxl Lightning 4step documentation](https://replicate.com/bytedance/sdxl-lightning-4step/api).
- **Imagen3 API by Google**: For more information, visit the [Official Imagen3 Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview).

## Comparing API Outputs 📑 

| S.No | Description  | DALL·E 3                       | Flux Schnell                  | SDXL Lightning          | Imagen3                       |
|------|--------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|
| 01   | Ancient Forest Temple  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/03.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/03.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/03.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/03.png) |
| 02   | Cyberpunk Samurai Duel  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/04.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/04.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/04.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/04.png) |
| 03   | Alien Planet with Floating Islands  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/05.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/05.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/05.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/05.png) |
| 04   | Deserted Amusement Park in the Future  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/07.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/07.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/07.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/07.png) |
| 05   | Mythical Phoenix Rising from Ashes  | ![Image1](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Dall%20E3%20API)/dalle3_examples/08.jpg) | ![Image2](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Flux%20Schnell%20API)/flux_schnell_examples/08.jpg) | ![Image3](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Sdxl%20Lightning%204Step%20API)/sdxl_lightning_4step_examples/08.jpg) | ![Image4](https://github.com/StudiYash/InstaVision/blob/main/Project%20Individual%20Models/InstaVision%20Bot%20(Google%20Imagen3%20API)/google_imagen3_examples/08.png) |

---

## Project Representation 🎉

1. **Innovation Fest 2024 at Vishwakarma University Pune**

    The **InstaVision** project was proudly showcased at the **Innovation Fest 2024** on **24th October 2024**. Held at the **Vishwakarma University, Pune**, this prestigious event was sponsored by the **Binghamton University** and **Thomas J. Watson College of Engineering and Applied Science**.

    The project secured a **Consolation prize of ₹1000**. Below are the Consolation certificate awarded to me for presenting InstaVision at Innovation Fest 2024.

    <p align="center">
    <img src="https://github.com/StudiYash/InstaVision/blob/main/Certificates/Project%20Representation/Vishwakarma%20University%20Innovation%20Fest%202024/Yash.jpg" alt="Innovation Fest 2024 Certificate" width="60%" />
    </p>

2. **Techmanthan 2025 at JSPM College Pune**

    The **InstaVision** project was proudly showcased at the **Techmanthan 2025** which was a **National Level Technical Fest** and which was organized on **28th - 29th January 2025**. Held at the **JSPM College, Pune**. This Competition offered me a valuable platform for knowledge exchange, constructive feedback, and networking with other innovators, researchers, and industry experts.

    Below is the participation certificate awarded to me for presenting InstaVision at Techmanthan 2025.

    <p align="center">
    <img src="https://github.com/StudiYash/InstaVision/blob/main/Certificates/Project%20Representation/JSPM%20TechManthan%202025/Yash.jpg" alt="Techmanthan 2025 Certificate" width="60%" />
    </p>

---

## Project Copyright ©️

Securing copyright for this project marked an important milestone in safeguarding my innovation and intellectual property. Copyrighting my project not only protects the unique aspects of my Image Generation system but also reinforces my commitment to creating responsible AI products. By copyrighting this idea, I have ensured that the methods, models, and technological advances developed through this project remain attributed to me.

### Copyright Publication Date: 22nd November 2024

### Certificate of Copyright 
<p align="center">
  <img src="https://github.com/StudiYash/InstaVision/blob/main/Certificates/Project%20Copyright/Copyright%20Certificate.png" alt="Copyright Certificate" width="60%" />
</p>

> *Establishing copyright protection is a proactive step towards fostering innovation, ensuring recognition, and laying a foundation for future advancements in image generation.*

---

## Real-Life Usage 🌍 

InstaVision has been successfully utilized in various real-world events, showcasing its versatility and impact. Here are some notable instances:

### 01) Alampata 2024 - VPKBIET's Ganeshotsav Celebration

- **Event:** Alampata 2024, an annual Ganeshotsav festival at VPKBIET
- **Date:** August 7, 2024 - August 17, 2024
- **Theme:** Technology and AI Integration
- **InstaVision's Role:** Used for **Telegram Bot Image Generative Competition**
- **Images Generated:** **702** Images.
  
  [![Alampata 2024 Images](https://img.shields.io/badge/VISIT-Alampata%202024%20Images-gold?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Real-life%20Usage/Alampata%202024)

- **Alampata 2024 Report:** 
  
  [![Alampata 2024 Report](https://img.shields.io/badge/VISIT-Alampata%202024%20Report-indigo?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/blob/main/Project%20Real-life%20Usage/Alampata%202024/Alampata_Ganeshotsav_2024_Report.pdf)

--- 

## License 📄 

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more details, please refer to the [LICENSE](https://github.com/StudiYash/InstaVision/blob/main/LICENSE) file in the repository.

By using this project, you agree to give appropriate credit, not use the material for commercial purposes without permission, and share any adaptations under the same license.

Attribution should be given as: "InstaVision Bot by Yash Shukla (https://github.com/StudiYash/InstaVision)"

Quick Overview regarding the permissions of usage of this project can be found on [LICENSE DEED : CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

## Contributions 🎉 
Contributions are welcome! Feel free to open an issue or submit a pull request.

- **Contributor License Agreement (CLA)**: By submitting a pull request, you confirm that you have read and agree to the terms of the [Contributor License Agreement (CLA)](https://github.com/StudiYash/InstaVision/blob/main/CLA.md).

- **Code of Conduct**: This project and everyone participating in it are governed by the [InstaVision Code of Conduct](https://github.com/StudiYash/InstaVision/blob/main/CODE_OF_CONDUCT.md).

- **Contributors**: See the list of contributors [here](https://github.com/StudiYash/InstaVision/blob/main/CONTRIBUTORS.md).

Made with ❤️ by [Yash Shukla](https://www.linkedin.com/in/yash-shukla-2024aiguy/)