import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
import replicate
from PIL import Image
from io import BytesIO
import requests

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
        "steps": 17,
        "width": 1152,
        "height": 1152,
        "prompt": "a crying dog",
        "output_format": "webp",
        "output_quality": 100,
        "negative_prompt": "",
        "number_of_images": 1
    }
    
    # Run the prediction
    try:
        # Call the model with the specified inputs
        output = replicate.run(
            "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            input=inputs
        )
    
        # Debugging: Check the raw output structure
        print("Raw output from Replicate API:", output)
    
        # Process and save the output stickers
        if isinstance(output, list):  # Handle list outputs
            for index, item in enumerate(output):
                try:
                    # If output is a URL
                    if isinstance(item, str) and item.startswith("http"):
                        response = requests.get(item)
                        response.raise_for_status()
                        image = Image.open(BytesIO(response.content))
                        file_name = GENERATED_DIR / f"output_{index}.webp"
                        image.save(file_name)
                        print(f"Sticker saved: {file_name}")
                        image.show()
                    else:
                        print(f"Unexpected item type in output list: {item}")
                except Exception as sticker_error:
                    print(f"Error processing sticker {index}: {sticker_error}")
        elif isinstance(output, str) and output.startswith("http"):
            # Handle a single URL output
            try:
                response = requests.get(output)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                file_name = GENERATED_DIR / "output_0.webp"
                image.save(file_name)
                print(f"Sticker saved: {file_name}")
                image.show()
            except Exception as url_error:
                print(f"Error downloading image from URL: {url_error}")
        else:
            print(f"Unexpected output type or invalid data: {output}")
    
    except Exception as e:
        print("Error during prediction:", e)

if __name__ == "__main__":
    main()
