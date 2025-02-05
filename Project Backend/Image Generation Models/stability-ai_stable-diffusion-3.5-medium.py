import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Initialize the Replicate client
client = replicate.Client()
model = client.models.get("stability-ai/stable-diffusion-3.5-medium")

# Define input parameters for the model
inputs = {
    "prompt": "a beautiful sunset over a mountain range, digital art",  # Customize your prompt
    "negative_prompt": "blurry, low quality, distorted",  # Optional
    "image_strength": 0.8,  # Controls how much the generated image is influenced by the prompt
    "num_inference_steps": 50,  # Number of denoising steps
    "guidance_scale": 7.5,  # Scale for classifier-free guidance
    "seed": 42,  # Optional: Set for reproducibility
    "width": 768,  # Width of the output image
    "height": 768,  # Height of the output image
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
                image.show()
            else:
                print(f"Failed to download the image. Status code: {response.status_code}")
        else:
            print("Prediction output is invalid or empty:", prediction.output)
    else:
        print("Prediction failed:", prediction.error)
except replicate.exceptions.ReplicateError as e:
    print("Error during prediction:", e)
