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
    model = client.models.get("black-forest-labs/flux-1.1-pro")
    
    # Define input parameters for the model
    inputs = {
        'prompt': 'a majestic waterfall in a dense forest during sunset',  # Customize your prompt
        'guidance': 3.5,  # Adjust guidance scale as needed
        'num_outputs': 1,  # Number of images to generate
        'aspect_ratio': '16:9',  # Options: '1:1', '4:3', '16:9', etc.
        'output_format': 'png',  # Options: 'jpeg', 'png', 'webp'
        'output_quality': 80,  # Quality of the output image
        'prompt_strength': 0.8,  # Strength of the prompt influence
        'num_inference_steps': 30,  # Number of inference steps
        'seed': 42  # Optional: Set for reproducibility
    }
    
    # Create the prediction
    try:
        prediction = client.predictions.create(model=model, input=inputs)
        print("Prediction started. Waiting for it to complete...")
        prediction.wait()
    
        # Check if the prediction succeeded
        if prediction.status == "succeeded":
            # Ensure output is a valid URL
            if prediction.output and isinstance(prediction.output, list) and len(prediction.output) > 0:
                output_url = prediction.output[0]
                print("Generated Image URL:", output_url)
    
                # Fetch and display the image
                response = requests.get(output_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    output_file_path = GENERATED_DIR / "flux_1_1_pro_output.png"
                    image.save(output_file_path)
                    print(f"Image saved: {output_file_path}")
                    image.show()
                else:
                    print(f"Failed to download the image. Status code: {response.status_code}")
            else:
                print("Prediction output is invalid or empty:", prediction.output)
        else:
            print("Prediction failed:", prediction.error)
    except replicate.exceptions.ReplicateError as e:
        print("Error during prediction:", e)

if __name__ == "__main__":
    main()
