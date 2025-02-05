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
        "Anime mugshot of a tough woman. She is holding a prison sign that reads \"Proteus\". "
        "Her face is censored. Anime key visual (best quality, HD, ~+~aesthetic~+~:1.2)"
    ),
    "negative_prompt": (
        "nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, blur, "
        "blurry, ugly, wrong proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, deformed, noisy image"
    ),
    "num_inference_steps": 30  # Number of inference steps for generating the image
}

# Run the prediction
try:
    output = replicate.run(
        "datacte/proteus-v0.3:b28b79d725c8548b173b6a19ff9bffd16b9b80df5b18b8dc5cb9e1ee471bfa48",
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
