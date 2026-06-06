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
        "width": 1024,  # Width of the output image
        "height": 1024,  # Height of the output image
        "prompt": "a beautiful painting of a serene mountain landscape at sunrise",  # Customize your prompt
        "num_inference_steps": 50,  # Number of denoising steps
        "guidance_scale": 7.5  # Guidance scale for prompt adherence
    }
    
    # Run the prediction
    try:
        output = replicate.run(
            "ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a",
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
