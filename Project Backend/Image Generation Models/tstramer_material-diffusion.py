import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Define input parameters for the model
inputs = {
    "prompt": (
        "Mossy Runic Bricks seamless texture, trending on artstation, stone, "
        "moss, base color, albedo, 4k"
    )  # Customize your prompt
}

# Run the prediction
try:
    output = replicate.run(
        "tstramer/material-diffusion:a42692c54c0f407f803a0a8a9066160976baedb77c91171a01730f9b0d7beeff",
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
