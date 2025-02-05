import replicate
import os
from PIL import Image
from io import BytesIO
from google.colab import files  # For downloading in Google Colab

# Set the Replicate API token
os.environ['REPLICATE_API_TOKEN'] = 'ENTER_YOUR_TOKEN_HERE'

# Test Flux Schnell Model
try:
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": "A Lion",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "png",
            "output_quality": 80
        }
    )

    # Assuming the first output is a FileOutput object
    file_output = output[0]

    # Read the raw binary image data
    image_data = file_output.read()  # This will return the raw image bytes

    # Open the image directly using Pillow
    image = Image.open(BytesIO(image_data))

    # Save the image locally
    image_filename = "flux_schnell_generated_image.png"  # Save as a PNG file
    image.save(image_filename)
    print(f"Image saved as {image_filename}")

    # Download the image file (if running in Google Colab)
    files.download(image_filename)

except Exception as e:
    print("Error with Flux Schnell:", e)
