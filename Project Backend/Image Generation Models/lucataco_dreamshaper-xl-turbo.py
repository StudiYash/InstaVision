import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN", "ENTER_YOUR_TOKEN_HERE")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
RUNTIME_OUTPUTS_DIR = PROJECT_ROOT / "runtime_outputs"
GENERATED_DIR = RUNTIME_OUTPUTS_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Define input parameters for the model
    inputs = {
        "prompt": (
            "In Casey Baugh's evocative style, art of a beautiful young girl cyborg with long brown hair, futuristic, "
            "scifi, intricate, elegant, highly detailed, majestic, Baugh's brushwork infuses the painting with a unique "
            "combination of realism and abstraction, greg rutkowski, surreal gold filigree, broken glass, (masterpiece, "
            "sidelighting, finely detailed beautiful eyes: 1.2), hdr, realistic painting, natural skin, textured skin, "
            "closed mouth, crystal eyes, butterfly filigree, chest armor, eye makeup, robot joints, long hair moved by "
            "the wind, window facing to another world, Baugh's distinctive style captures the essence of the girl's enigmatic "
            "nature, inviting viewers to explore the depths of her soul, award winning art"
        ),
        "negative_prompt": (
            "ugly, deformed, noisy, blurry, low contrast, text, BadDream, 3d, cgi, render, fake, anime, open mouth, "
            "big forehead, long neck"
        ),
        "num_inference_steps": 7  # Number of denoising steps
    }
    
    # Run the prediction
    try:
        output = replicate.run(
            "lucataco/dreamshaper-xl-turbo:0a1710e0187b01a255302738ca0158ff02a22f4638679533e111082f9dd1b615",
            input=inputs
        )
    
        # Process and display the output images
        for index, item in enumerate(output):
            # Save the image to disk
            file_name = GENERATED_DIR / f"output_{index}.png"
            with open(file_name, "wb") as file:
                file.write(item.read())
            print(f"Image saved: {file_name}")
    
            # Display the image in Jupyter Notebook
            image = Image.open(file_name)
            image.show()
    except Exception as e:
        print("Error during prediction:", e)

if __name__ == "__main__":
    main()
