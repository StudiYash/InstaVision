# Project Backend

The **Project Backend** folder is a core part of the **InstaVision** project, containing resources for both generating and editing images. Below are the details of its structure, requirements, and setup instructions.

---

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Image Generation Models](#image-generation-models)
- [Image Editing Models](#image-editing-models)
- [Summary](#summary)

---

## 1. Requirements

To use the models in this folder, ensure you have the following:

- **Google Colab Environment** or a local machine with **Python 3.10**.
- **Replicate API Key** for accessing the models.
- **IMGBB API Key** for uploading images. (Only required in case of Image Editing Models)
- **Internet Connection** to install dependencies and interact with APIs.

---

## 2. Setup Instructions

Follow these steps to set up your environment:

1. **Install Dependencies**  
   Run the following command to install the required package for interacting with Replicate APIs:  
   ```bash
   pip install replicate
   ```

2. **Add Your Replicate API Key**  
   Set up your Replicate API Key in the environment variable or in the code for authentication.

3. **Add Your IMGBB API Key**  
   Set up your IMGBB API Key in the environment variable or in the code for authentication. Only required in case of Image Editing Models.

4. **Access Models**  
   Navigate to the specific model (Image Generation Models Folder or Image Editing Models Folder) and follow the instructions in their respective `README.md` files.

---

## 3. Image Generation Models

The **Image Generation Models** folder contains 20 advanced models designed to create stunning, high-quality images based on user prompts. Below is the complete list:

1. `ai-forever_kandinsky-2.2`
2. `black-forest-labs_flux-1.1-pro-ultra`
3. `black-forest-labs_flux-1.1-pro`
4. `black-forest-labs_flux-dev`
5. `black-forest-labs_flux-schnell`
6. `bytedance_sdxl-lightning-4step`
7. `cjwbw_animagine-xl-3.1`
8. `datacte_proteus-v0.2`
9. `datacte_proteus-v0.3`
10. `fofr_sdxl-emoji`
11. `fofr_sticker-maker`
12. `lucataco_dreamshaper-xl-turbo`
13. `lucataco_open-dalle-v1.1`
14. `lucataco_realvisxl2-lcm`
15. `nvidia_sana`
16. `recraft-ai_recraft-v3`
17. `stability-ai_stable-diffusion-3.5-medium`
18. `stability-ai_stable-diffusion`
19. `stability-ai_sdxl`
20. `tstramer_material-diffusion`

Each model has been optimized for various use cases and offers state-of-the-art capabilities in image generation.

---

## 4. Image Editing Models

The **Image Editing Models** folder includes 8 models specifically designed to edit and enhance images. These models can perform tasks like object removal, de-oldifying images, and more. Below is the complete list:

1. `adirik_t2i-adapter-sdxl-openpose`
2. `arielreplicate_deoldify-image`
3. `black-forest-labs_flux-canny-pro`
4. `black-forest-labs_flux-depth-pro`
5. `black-forest-labs_flux-redux-dev`
6. `cjwbw_rembg`
7. `sujaykhandekar_object-removal`
8. `timothybrooks_instruct-pix2pix`

These models provide powerful tools for refining and customizing images.

---

## 5. Summary

The **Project Backend** folder is structured as follows:

- **Image Generation Models**: 20 models for creating high-quality images.
- **Image Editing Models**: 8 models for enhancing and editing images.

Explore each folder for detailed instructions on utilizing the models effectively.

---
