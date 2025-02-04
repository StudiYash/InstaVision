# Image Generation Models

The **Image Generation Models** folder contains 20 advanced models specifically designed to create stunning, high-quality images based on text prompts. These models leverage state-of-the-art technologies to deliver exceptional results for various use cases, from artistic creations to realistic imagery.

---

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Model Directory](#model-directory)
- [How To Use](#how-to-use)
- [Recommendations](#recommendations)
- [Summary](#summary)

---

## 1. Requirements

Before using these models, ensure you meet the following requirements:

- **Python 3.10 or later**.
- **Replicate API Key** for accessing the models.
- **Stable Internet Connection** to fetch model data and dependencies.
- **Google Colab Environment** (recommended) or a compatible local setup.

---

## 2. Setup Instructions

Follow these steps to get started with the image generation models:

1. **Install the Required Library**  
   Use the following command to install the `replicate` library:
   ```bash
   pip install replicate
   ```

2. **Configure Your API Key**  
   Add your Replicate API Key to your environment or directly in the script.
   ```python
   import replicate
   replicate.Client(api_token="YOUR_API_KEY")
   ```

3. **Select the Model**  
   Navigate to the specific model and insert the Replicate API Key in the code in the appropriate spot.

4. **Run The Code**
   Enter your desired prompt inside the code and then run the cell.

---

## 3. Model Directory

Below is a list of the 20 image generation models available in this folder:

### Kandinsky Models
1. `ai-forever_kandinsky-2.2`

### Flux Models
2. `black-forest-labs_flux-1.1-pro-ultra`
3. `black-forest-labs_flux-1.1-pro`
4. `black-forest-labs_flux-dev`
5. `black-forest-labs_flux-schnell`

### ByteDance and Animagine
6. `bytedance_sdxl-lightning-4step`
7. `cjwbw_animagine-xl-3.1`

### Datacte Proteus Series
8. `datacte_proteus-v0.2`
9. `datacte_proteus-v0.3`

### Fofr Series
10. `fofr_sdxl-emoji`
11. `fofr_sticker-maker`

### Lucataco Models
12. `lucataco_dreamshaper-xl-turbo`
13. `lucataco_open-dalle-v1.1`
14. `lucataco_realvisxl2-lcm`

### NVIDIA and Recraft
15. `nvidia_sana`
16. `recraft-ai_recraft-v3`

### Stability AI Models
17. `stability-ai_stable-diffusion-3.5-medium`
18. `stability-ai_stable-diffusion`
19. `stability-ai_sdxl`

### Material Diffusion
20. `tstramer_material-diffusion`

---

## 4. How to Use

1. **Explore the Models**: Navigate to the individual subfolders for model-specific documentation and examples.
2. **Input Prompts**: Provide a detailed and descriptive text prompt to achieve the best results.
3. **Customization**: Modify parameters like resolution, styles, and more (refer to the model's documentation).
4. **Output**: Save or further process the generated images as needed.

---

## 5. Recommendations

- Use **Google Colab** for better resource management and free GPU usage.
- Experiment with different prompts to unlock the full potential of each model.
- Refer to the individual model README files for advanced settings and usage tips.

---

## 6. Summary

The **Image Generation Models** folder empowers creators, researchers, and developers to transform their ideas into visually compelling images. Whether you are looking to generate artistic visuals or realistic renders, these 20 models provide unparalleled flexibility and power.

Feel free to explore and unleash your creativity!
