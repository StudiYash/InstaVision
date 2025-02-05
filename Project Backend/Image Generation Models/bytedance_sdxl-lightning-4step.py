import replicate
import os
from PIL import Image
from io import BytesIO
from google.colab import files  # For downloading in Google Colab

# Set the Replicate API token
os.environ['REPLICATE_API_TOKEN'] = 'ENTER_YOUR_TOKEN_HERE'

# Test SDXL Model
try:
    output = replicate.run(
        "bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637",
        input={"prompt": "A Monkey"}
    )

    # Assuming the first output is a FileOutput object
    file_output = output[0]

    # Read the raw binary image data
    image_data = file_output.read()  # This will return the raw image bytes

    # Open the image directly using Pillow
    image = Image.open(BytesIO(image_data))

    # Save the image locally
    image_filename = "generated_image.png"  # Save as a PNG file
    image.save(image_filename)
    print(f"Image saved as {image_filename}")

    # Download the image file (if running in Google Colab)
    files.download(image_filename)

except Exception as e:
    print("Error with SDXL:", e)
