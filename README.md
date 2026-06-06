# ![InstaVision](https://github.com/StudiYash/InstaVision/blob/main/InstaVision%20Logo.png)

<p align="center">

  <!-- ⭐ GitHub Stars -->
  <a href="https://github.com/StudiYash/InstaVision/stargazers">
    <img src="https://img.shields.io/github/stars/StudiYash/InstaVision?style=for-the-badge&logo=github&color=yellow" alt="GitHub Stars">
  </a>

  <!-- ▶️ Official YouTube Video -->
  <a href="https://youtu.be/HhnD14Yw-Y0">
    <img src="https://img.shields.io/badge/Watch-Project%20Walkthrough-red?style=for-the-badge&logo=youtube" alt="Project Walkthrough">
  </a>

</p>

## Project Introduction 🛡️

### Abstract 
**InstaVision** is a powerful AI-driven Image Generation and Image Editing project designed to transform your text descriptions into stunning, high-quality images using various Image Generation APIs. Perfect for creators, students, and anyone with a vivid imagination, InstaVision makes it easy to bring your ideas to life with just a few words.

### Project Timeline 

- **Start Date**: 22nd August 2024  
- **End Date**: 14th February 2025 
- **Total Time Required**: 5 months and 24 days 

### My Introduction  

| Name                   | GitHub Profile | LinkedIn Profile |
|------------------------|----------------|------------------|
| **Yash Suhas Shukla**  | [GitHub](https://github.com/StudiYash) | [LinkedIn](https://www.linkedin.com/in/yash-shukla-2024aiguy/) |

<div align="center">
  <img src="https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/About%20Me.gif" alt="Introduction GIF" width="800" height="450">
</div>

---

## Run InstaVision Locally 🚀

You can explore InstaVision locally after cloning the repository. The project includes multiple runnable components, including Tkinter frontend interfaces, backend model scripts, the main Telegram bot, individual Telegram model bots, and the packaged Windows application.

The local setup guide is the best starting point for installation, configuration, validation, and component-specific run instructions.

[![Local Setup Guide](https://img.shields.io/badge/View-Local%20Setup%20Guide-gold?style=for-the-badge&logo=markdown)](https://github.com/StudiYash/InstaVision/blob/main/LOCAL_SETUP_GUIDE.md)

---

## Methodology ✨

<p align="center">
<img src="https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/System%20Methodology.png" style="border: 2px solid black; width: 600px; height: 400px;" alt="Project Methodology">
</p>

The **Methodology of InstaVision** is designed to efficiently process text-based inputs to generate visually stunning, AI-powered images. Below is an in-depth breakdown of each component and its functionality:

### 1. **Text Input**
   - **Source**: Inputs are received through multiple platforms, including:
     - **Telegram Bot**: Users can interact with the bot by sending text prompts directly via Telegram.
     - **Windows Application**: Desktop users can input their prompts through the standalone InstaVision application.
   - **Purpose**: This serves as the starting point of the entire workflow, where users provide their creative ideas or descriptions for image generation.

### 2. **Prompt Preprocessing**
   This stage ensures that the text input is validated and optimized for the image generation process. It includes two key components:

   #### a) **Banned Words Check**
   - **Objective**: Ensures that inputs adhere to ethical and usage guidelines by filtering out inappropriate or offensive language.
   - **Process**:
     - Scans the text prompt for words or phrases that are flagged as inappropriate.
     - Prompts the user to revise their input if any banned words are detected.
   - **Impact**: Maintains the integrity and professionalism of the generated content.

   #### b) **Rate Limiting via Redis** (Only for Telegram Bot)
   - **Objective**: Prevents system overload and abuse by enforcing user-specific rate limits.
   - **Features**:
     - Default users can generate up to **5 images per day**.
     - Privileged users can generate up to **50 images per day**.
     - Admin users have no restrictions.
   - **Technology Used**: 
     - Redis Cloud Database for maintaining real-time user quota information.
     - Reset logic to refresh limits every 24 hours.
   - **Impact**: Ensures fair usage and system scalability for multiple users simultaneously.

### 3. **Image Processing**
   This stage leverages advanced AI models to generate and enhance images based on the processed input. It comprises two critical submodules:

   #### a) **Image Generation**
   - **Objective**: Transforms text-based prompts into visually stunning images using state-of-the-art AI models.
   - **Supported Models**:
     - **Replicate APIs** for SDXL Lightning and Flux Schnell.
     - **Google Imagen API** for generating highly detailed and realistic images.
     - **OpenAI DALL-E 3 API** for a creative and versatile image generation approach.
   - **Process**:
     - Receives processed text input and sends it to the selected image generation API.
     - Produces a high-quality image as output.
   - **Impact**: Offers users diverse styles and capabilities for image generation, catering to various creative needs.

   #### b) **Watermarking**
   - **Objective**: Adds a customizable watermark to the generated image for branding and intellectual property protection.
   - **Features**:
     - Supports both default and custom watermark text.
     - Uses fonts specified by the user, with fallbacks to default fonts if unavailable.
     - Ensures that the watermark is visually appealing and non-intrusive.
   - **Impact**: Protects generated images from unauthorized use and establishes a unique identity for InstaVision.

### 4. **Image Output**
   - **Objective**: Delivers the final, watermarked image to the user.
   - **Delivery Channels**:
     - **Telegram Bot**: Sends the image to the user and/or a designated group.
     - **Windows Application**: Displays the image directly within the application and allows users to save it locally.
   - **Impact**: Ensures a seamless user experience by making the final output readily accessible.

### Key Advantages of the Methodology:
- **Scalability**: Efficiently handles simultaneous requests from multiple users through robust backend integration.
- **Ethical Compliance**: Ensures content appropriateness through banned words detection.
- **Flexibility**: Supports a variety of input methods and image generation models.
- **User Protection**: Implements rate limiting and watermarking to ensure fair use and intellectual property security.

This methodology highlights the seamless integration of user-friendly interfaces, ethical controls, and advanced AI technologies to deliver a reliable and creative experience with InstaVision.

---

## Backend Preparation 🔧

### Mark Models Index

The backend development was an intricate journey, involving months of rigorous research, experimentation, and iterative coding. Each phase contributed to refining the system’s ability to generate and edit images over various prompts of input and in various languages. 

Our **Mark Model Index Document** provides a comprehensive overview of this journey, showcasing each model’s evolution, from early concepts to the final optimized versions. Dive into the document to see how each model was crafted, tested, and fine-tuned to tackle the challenges of multilingual, multimodal hate speech detection.

[![Mark Model Index Document](https://img.shields.io/badge/View-Mark%20Model%20Index%20Document-blue?style=for-the-badge&logo=Github)](https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/Mark%20Model%20Index.pdf)

---

## Project Backend 🖥️

The **Project Backend** contains resources for both generating and editing images, supporting state-of-the-art models to deliver exceptional results.

### Image Generation Models:

A collection of **20 advanced models** for creating high-quality images:
1. `ai-forever_kandinsky-2.2`
2. `black-forest-labs_flux-1.1-pro-ultra`
3. `bytedance_sdxl-lightning-4step`
4. `lucataco_dreamshaper-xl-turbo`
... *(see the full list in the [Backend README](https://github.com/StudiYash/InstaVision/tree/main/Project%20Backend/Image%20Generation%20Models))*

### Image Editing Models:

A set of **8 powerful tools** for enhancing images, such as object removal, de-oldifying, and more:
1. `adirik_t2i-adapter-sdxl-openpose`
2. `arielreplicate_deoldify-image`
3. `black-forest-labs_flux-canny-pro`
... *(complete list in the [Backend README](https://github.com/StudiYash/InstaVision/blob/main/Project%20Backend/Image%20Editing%20Models))*

For detailed instructions, visit the

[![Explore Project Backend](https://img.shields.io/badge/View-Project%20Backend-white?style=for-the-badge&logo=github)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Backend)

---

## Project Frontend 🎨

The **Project Frontend** focuses on delivering a user-friendly and aesthetically pleasing interface for InstaVision.  

### Main Page Features:
- 🌟 Maximized window view.
- 🎨 Dark-themed interface with dynamic logo resizing.
- ✨ Hover-responsive buttons.

### Image Generation UI:
- 🖥 Fully responsive design.
- 🎨 Dark theme with real-time image preview.
- 📂 Save generated images with a single click.

### Image Editing UI:
- 🖼 Real-time preview of uploaded and edited images.
- 🛠 AI-powered tools for object removal, enhancements, and more.

For detailed instructions, visit the 

[![Explore Project Frontend](https://img.shields.io/badge/View-Project%20Frontend-pink?style=for-the-badge&logo=github)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Frontend)

---

## Project Windows Application ✨

### Installer Steps:
1. **Language Selection**: Choose preferred language.
2. **License Agreement**: Accept terms.
3. **Installation Progress**: Relax while the app installs.

### Main Features:
- **Main Page**: Central hub for navigation.
- **Image Generation**: Advanced UI for AI-powered image creation.
- **Image Editing**: Tools for refining and enhancing images.

**📥 Download InstaVision**
> Click the button below to download the latest version of InstaVision.

[![InstaVision Windows Application](https://img.shields.io/badge/View-Download%20InstaVision%20Windows%20Application-gold?style=for-the-badge&logo=GitHub)](https://github.com/StudiYash/InstaVision/blob/main/Project%20Windows%20Application/InstaVision.exe)

For more information about Project Windows Application, visit the 

<p align="center">

  <!-- ⭐ Project Windows Application Code-->
  <a href="https://github.com/StudiYash/InstaVision/tree/main/Project%20Windows%20Application">
    <img src="https://img.shields.io/badge/View-Project%20Windows%20Application-indigo?style=for-the-badge&logo=github">
  </a>

  <!-- ▶️ Project Windows Application Setup Video -->
  <a href="https://drive.google.com/file/d/1TJRBYDH2MOK6q8VmP2o2Ouu9TNKL7r5J/view?usp=sharing">
    <img src="https://img.shields.io/badge/Watch-Project%20Windows%20Application%20Setup-red?style=for-the-badge&logo=google-drive" alt="Project Windows Application">
  </a>

</p>

---

## Project Telegram Bot 🤖

### Key Features:
- **Simultaneous Request Handling**: Handles up to 50 requests simultaneously.
- **Rate Limiting**: Enforces user limits (default: 5/day; privileged: 50/day).
- **Translation**: Supports input in **80+ languages** ([Language List](https://github.com/StudiYash/InstaVision/blob/main/Support%20Files/InstaVision_Supported_Languages.pdf)).
- **Watermarking**: Customizable watermark with fallback fonts.

For more details, refer to

<p align="center">

  <!-- ⭐ Telegram Bot Code -->
  <a href="https://github.com/StudiYash/InstaVision/tree/main/Project%20Telegram%20Bot">
    <img src="https://img.shields.io/badge/View-Telegram%20Bot%20Code-teal?style=for-the-badge&logo=github">
  </a>

  <!-- ▶️ Telegram Bot Setup Video -->
  <a href="https://drive.google.com/file/d/1UX1-N35ogm18IVjCMZFyHPCjY0cgMRzz/view?usp=sharing">
    <img src="https://img.shields.io/badge/Watch-Telegram%20Bot%20Setup-red?style=for-the-badge&logo=google-drive" alt="Telegram Bot Setup">
  </a>

</p>

---

## Project Representation 🎉

1. **Innovation Fest 2024 at Vishwakarma University Pune**

    The **InstaVision** project was proudly showcased at the **Innovation Fest 2024** on **24th October 2024**. Held at the **Vishwakarma University, Pune**, this prestigious event was sponsored by the **Binghamton University** and **Thomas J. Watson College of Engineering and Applied Science**.

    The project secured a **Consolation prize of ₹1000**. Below are the Consolation certificate awarded to me for presenting InstaVision at Innovation Fest 2024.

    <p align="center">
    <img src="https://github.com/StudiYash/InstaVision/blob/main/Certificates/Project%20Representation/Vishwakarma%20University%20Innovation%20Fest%202024/Yash.jpg" alt="Innovation Fest 2024 Certificate" width="80%" />
    </p>

2. **Techmanthan 2025 at JSPM College Pune**

    The **InstaVision** project was proudly showcased at the **Techmanthan 2025** which was a **National Level Technical Fest** and which was organized on **28th - 29th January 2025**. Held at the **JSPM College, Pune**. This Competition offered me a valuable platform for knowledge exchange, constructive feedback, and networking with other innovators, researchers, and industry experts.

    Below is the participation certificate awarded to me for presenting InstaVision at Techmanthan 2025.

    <p align="center">
    <img src="https://github.com/StudiYash/InstaVision/blob/main/Certificates/Project%20Representation/JSPM%20TechManthan%202025/Yash.jpg" alt="Techmanthan 2025 Certificate" width="80%" />
    </p>

---

## Real-Life Usage 🌍 

InstaVision has been successfully utilized in various real-world events, showcasing its versatility and impact. Here are some notable instances:

### 01) Alampata 2024 - VPKBIET's Ganeshotsav Celebration

- **Event:** Alampata 2024, an annual Ganeshotsav festival at VPKBIET
- **Date:** August 7, 2024 - August 17, 2024
- **Theme:** Technology and AI Integration
- **InstaVision's Role:** Used for **Telegram Bot Image Generative Competition**
- **Images Generated:** **702** Images.
  
  [![Alampata 2024 Images](https://img.shields.io/badge/VISIT-Alampata%202024%20Images-purple?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Real-life%20Usage/Alampata%202024/Images)

- **Alampata 2024 Report:** 
  
  [![Alampata 2024 Report](https://img.shields.io/badge/VISIT-Alampata%202024%20Report-tan?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/blob/main/Project%20Real-life%20Usage/Alampata%202024/Alampata_Ganeshotsav_2024_Report.pdf)


### 02) VoltzFest 2025 - VPKBIET's AI Art Gallery

- **Event:** VoltzFest 2025, a platform for artists for uplifting their skills using AI
- **Date:** February 10, 2025 - February 11, 2025
- **Theme:** AI Art Generation
- **InstaVision's Role:** Used for **Telegram Bot Image Generative Competition**
- **Images Generated:** **264** Images.
  
  [![VoltzFest 2025 Images](https://img.shields.io/badge/VISIT-VoltzFest%202025%20Images-purple?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Real-life%20Usage/VoltzFest%202025/Images)

- **VoltzFest 2025 Report:** 
  
  [![VoltzFest 2025 Report](https://img.shields.io/badge/VISIT-VoltzFest%202025%20Report-tan?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/blob/main/Project%20Real-life%20Usage/VoltzFest%202025/Voltzfest_AI_Art_Gallery_2025_Report.pdf)

---

## Project Testing Prompts 📝

The **Project Test Inputs** folder includes curated prompts for evaluating InstaVision across all models. Prompts are designed for versatility and optimized for showcasing API strengths.  

Explore test prompts and examples in the Project Test Inputs Folder.

[![Project Test Inputs](https://img.shields.io/badge/VISIT-Project%20Test%20Inputs-olive?style=for-the-badge&logo=Files)](https://github.com/StudiYash/InstaVision/tree/main/Project%20Test%20Inputs)

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
