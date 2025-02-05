import os
import replicate
import requests
from PIL import Image
from io import BytesIO

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Define input parameters for the model
inputs = {
    "width": 768,  # Image width
    "height": 768,  # Image height
    "prompt": "An astronaut riding a rainbow unicorn, cinematic, dramatic",  # Customize your prompt
    "refine": "expert_ensemble_refiner",  # Refine method
    "apply_watermark": False,  # Whether to apply a watermark
    "num_inference_steps": 25  # Number of inference steps
}

# Run the prediction
try:
    output = replicate.run(
        "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
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
