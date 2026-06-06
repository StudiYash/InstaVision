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
            "cinematic film still of Kodak Motion Picture Film: (Sharp Detailed Image) "
            "An Oscar-winning movie for Best Cinematography a woman in a kimono standing "
            "on a subway train in Japan Kodak Motion Picture Film Style, shallow depth "
            "of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, "
            "epic, gorgeous, film grain, grainy"
        )
    }
    
    # Run the prediction
    try:
        output = replicate.run(
            "datacte/proteus-v0.2:06775cd262843edbde5abab958abdbb65a0a6b58ca301c9fd78fa55c775fc019",
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
