import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
import replicate
import requests

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN", "ENTER_YOUR_TOKEN_HERE")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
RUNTIME_OUTPUTS_DIR = PROJECT_ROOT / "runtime_outputs"
UPLOADS_DIR = RUNTIME_OUTPUTS_DIR / "uploads"
GENERATED_DIR = RUNTIME_OUTPUTS_DIR / "generated"
for folder in [UPLOADS_DIR, GENERATED_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Function to upload an image to ImgBB
def upload_to_imgbb(image_path):
    imgbb_api_key = os.getenv("IMGBB_API_KEY", "ENTER_IMGBB_API_KEY_HERE")  # Get an API key from ImgBB (free, no account required)
    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": imgbb_api_key},
            files={"image": image_file}
        )
    response_data = response.json()
    if response.status_code == 200:
        return response_data["data"]["url"]  # Return the public URL
    else:
        raise Exception(f"ImgBB upload failed: {response_data}")


def main():
    # Provide the local path for the input image
    local_image_path = Path(os.getenv("INPUT_IMAGE_PATH", str(UPLOADS_DIR / "goggle.jpg"))).expanduser()
    
    try:
        # Upload the input image to ImgBB
        uploaded_image_url = upload_to_imgbb(local_image_path)
        print("Uploaded Image URL:", uploaded_image_url)
    
        # Define input parameters for the Replicate model
        inputs = {
            "image": uploaded_image_url,
            "prompt": "turn him into cyborg"  # Customize the transformation prompt
        }
    
        # Run the Replicate model
        output = replicate.run(
            "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
            input=inputs
        )
    
        # Save each output image locally
        for index, item in enumerate(output):
            output_file_path = GENERATED_DIR / f"output_{index}.png"
            with open(output_file_path, "wb") as file:
                file.write(item.read())
            print(f"Output saved as {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
