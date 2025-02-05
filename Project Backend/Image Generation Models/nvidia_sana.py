import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
import os
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Initialize the Replicate client
client = replicate.Client()
model = client.models.get("nvidia/sana")
version = model.versions.get("c6b5d2b7459910fec94432e9e1203c3cdce92d6db20f714f1355747990b52fa6")

# Define input parameters for the model
inputs = {
    'prompt': 'a cyberpunk cat with a neon sign that says "Sana"',  # Update as per your needs
    'negative_prompt': '',
    'width': 1024,
    'height': 1024,
    'num_inference_steps': 18,
    'guidance_scale': 5,
    'pag_guidance_scale': 2,
    'seed': 42  # Replace with an integer for reproducibility
}

# Create the prediction
prediction = client.predictions.create(version=version, input=inputs)

# Wait for the prediction to complete
prediction.wait()

# Check if the prediction succeeded
if prediction.status == "failed":
    print("Prediction failed with error:", prediction.error)
    exit()

# Debugging: Print the full prediction output
print("Full Prediction Output:", prediction.output)

# Extract the output URL safely
output_url = prediction.output  # Directly use the string value
if not output_url or not isinstance(output_url, str):
    print("Prediction output is invalid or empty.")
    exit()

print("Output URL:", output_url)

# Validate the output URL
if not output_url.startswith("http"):
    print("Invalid URL received:", output_url)
    exit()

# Fetch and display the image
response = requests.get(output_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.show()
else:
    print(f"Failed to download the image. Status code: {response.status_code}")
