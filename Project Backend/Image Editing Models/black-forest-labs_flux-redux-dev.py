import os
import replicate
import requests

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Function to upload an image to ImgBB
def upload_to_imgbb(image_path):
    imgbb_api_key = "ENTER_IMGBB_API_KEY_HERE"  # Get an API key from ImgBB (free, no account required)
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

# Provide the local path for the redux image
local_redux_image_path = "C:/Users/Desktop/TA.png"

try:
    # Upload the redux image to ImgBB
    uploaded_redux_image_url = upload_to_imgbb(local_redux_image_path)
    print("Uploaded Redux Image URL:", uploaded_redux_image_url)

    # Define input parameters for the Replicate model
    inputs = {
        "redux_image": uploaded_redux_image_url,
        "aspect_ratio": "4:3"  # Customize aspect ratio as needed
    }

    # Run the Replicate model
    output = replicate.run("black-forest-labs/flux-redux-dev", input=inputs)

    # Save each output image locally
    for index, item in enumerate(output):
        output_file_path = f"output_{index}.webp"
        with open(output_file_path, "wb") as file:
            file.write(item.read())
        print(f"Output saved as {output_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
