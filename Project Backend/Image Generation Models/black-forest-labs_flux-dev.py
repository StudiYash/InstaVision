import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Initialize the Replicate client
client = replicate.Client()
model = client.models.get("black-forest-labs/flux-dev")

# Define input parameters for the model
inputs = {
    'prompt': 'a futuristic cityscape at sunset',  # Customize your prompt
    'guidance': 3.5,  # Adjust guidance scale as needed
    'num_outputs': 1,  # Number of images to generate
    'aspect_ratio': '16:9',  # Options: '1:1', '4:3', '16:9', etc.
    'output_format': 'webp',  # Options: 'jpeg', 'png', 'webp'
    'output_quality': 80,  # Quality of the output image
    'prompt_strength': 0.8,  # Strength of the prompt influence
    'num_inference_steps': 28,  # Number of inference steps
    'seed': 42  # Optional: Set for reproducibility
}

# Create the prediction
prediction = client.predictions.create(model=model, input=inputs)

# Wait for the prediction to complete
prediction.wait()

# Check if the prediction succeeded
if prediction.status == "succeeded":
    output_url = prediction.output[0]  # Access the first image URL
    print("Generated Image URL:", output_url)

    # Fetch and display the image
    response = requests.get(output_url)
    image = Image.open(BytesIO(response.content))
    image.show()
else:
    print("Prediction failed:", prediction.error)
