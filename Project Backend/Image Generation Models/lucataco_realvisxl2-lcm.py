import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Define input parameters for the model
inputs = {
    "seed": 34694,  # Set a seed for reproducibility
    "prompt": (
        "dark shot, front shot, photo of a 25 y.o latino man, perfect eyes, "
        "natural skin, skin moles, looks at viewer, cinematic shot"
    )  # Customize your prompt
}

# Run the prediction
try:
    output = replicate.run(
        "lucataco/realvisxl2-lcm:479633443fc6588e1e8ae764b79cdb3702d0c196e0cb2de6db39ce577383be77",
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
