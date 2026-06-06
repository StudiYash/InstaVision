import requests
import replicate
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN", "ENTER_YOUR_TOKEN_HERE")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
RUNTIME_OUTPUTS_DIR = PROJECT_ROOT / "runtime_outputs"
UPLOADS_DIR = RUNTIME_OUTPUTS_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Initialize the Replicate client
    client = replicate.Client()
    model = client.models.get("black-forest-labs/flux-depth-pro")
    
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
    
    # Function to delete the uploaded image (optional)
    def delete_from_imgbb(delete_url):
        response = requests.get(delete_url)
        if response.status_code == 200:
            print("Image successfully deleted from ImgBB.")
        else:
            print(f"Failed to delete image: {response.text}")
    
    # Provide the local path of your image
    local_image_path = Path(os.getenv("INPUT_IMAGE_PATH", str(UPLOADS_DIR / "TA.png"))).expanduser()
    
    try:
        # Upload the image to ImgBB
        uploaded_image_url = upload_to_imgbb(local_image_path)
        print("Uploaded Image URL:", uploaded_image_url)
    
        # Define input parameters for the Replicate model
        inputs = {
            "prompt": "abstract 3D render with the word \"DEPTH\"",
            "guidance": 7,
            "control_image": uploaded_image_url
        }
    
        # Create the prediction
        prediction = client.predictions.create(model=model, input=inputs)
        prediction.wait()
    
        # Check if the prediction succeeded
        if prediction.status == "succeeded":
            output_url = prediction.output
            print("Edited Image URL:", output_url)
    
            # (Optional) Delete the image from ImgBB
            # Uncomment the following line if privacy is important:
            delete_from_imgbb(response_data["data"]["delete_url"])
        else:
            print("Prediction failed:", prediction.error)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
