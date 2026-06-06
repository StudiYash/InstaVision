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
    # Initialize the Replicate client
    client = replicate.Client()
    model = client.models.get("recraft-ai/recraft-v3")
    
    # Define input parameters for the model
    inputs = {
        'prompt': 'a wildlife photography photo of a red panda using a laptop in a snowy forest',  # Customize your prompt
        'size': '1024x1024',  # Options: '512x512', '768x768', '1024x1024', etc.
        'style': 'realistic_image',  # Options: 'realistic_image', 'digital_illustration', 'vector_illustration', etc.
        'seed': 42  # Optional: Set for reproducibility
    }
    
    # Create the prediction
    prediction = client.predictions.create(model=model, input=inputs)
    
    # Wait for the prediction to complete
    prediction.wait()
    
    # Check if the prediction succeeded
    if prediction.status == "succeeded":
        output_url = prediction.output
        print("Generated Image URL:", output_url)
    
        # Fetch and display the image
        response = requests.get(output_url)
        image = Image.open(BytesIO(response.content))
        output_file_path = GENERATED_DIR / "recraft_v3_output.png"
        image.save(output_file_path)
        print(f"Image saved: {output_file_path}")
        image.show()
    else:
        print("Prediction failed:", prediction.error)

if __name__ == "__main__":
    main()
