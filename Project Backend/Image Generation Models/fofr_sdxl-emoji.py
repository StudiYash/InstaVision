import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Define input parameters for the model
inputs = {
    "prompt": "A TOK emoji of a man",  # Customize the prompt for the emoji
    "apply_watermark": False  # Disable watermark
}

# Run the prediction
try:
    output = replicate.run(
        "fofr/sdxl-emoji:dee76b5afde21b0f01ed7925f0665b7e879c50ee718c5f78a9d38e04d523cc5e",
        input=inputs
    )

    # Process and display the output images
    for index, item in enumerate(output):
        # Save the image to disk
        file_name = f"output_{index}.png"
        with open(file_name, "wb") as file:
            file.write(item.read())
        print(f"Image saved: {file_name}")

        # Display the image in Jupyter Notebook
        image = Image.open(file_name)
        image.show()
except Exception as e:
    print("Error during prediction:", e)
