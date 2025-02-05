import os
import replicate
from PIL import Image
from io import BytesIO
import requests

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "ENTER_YOUR_TOKEN_HERE"

# Run the prediction
try:
    # Call the model with the given inputs
    output = replicate.run(
        "cjwbw/animagine-xl-3.1:6afe2e6b27dad2d6f480b59195c221884b6acc589ff4d05ff0e5fc058690fbb9",
        input={
            "width": 896,
            "height": 1152,
            "prompt": (
                "1girl, cagliostro, granblue fantasy, violet eyes, standing, hand on own chin, "
                "looking at object, smile, closed mouth, table, beaker, glass tube, experiment apparatus, "
                "dark room, laboratory, upper body"
            ),
            "guidance_scale": 7,
            "style_selector": "(None)",
            "negative_prompt": (
                "nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, "
                "low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, "
                "extra digits, artistic error, username, scan, [abstract]"
            ),
            "quality_selector": "Standard v3.1",
            "num_inference_steps": 28
        }
    )

    # Debugging: Check the raw output structure
    print("Raw output from Replicate API:", output)

    # Process and save the output images
    if isinstance(output, str) and output.startswith("http"):
        # If it's a URL, download the image
        try:
            response = requests.get(output)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            file_name = "output.png"
            image.save(file_name)
            print(f"Image saved: {file_name}")
            image.show()
        except Exception as url_error:
            print(f"Error downloading image from URL: {url_error}")
    else:
        print(f"Unexpected output type or invalid data: {output}")

except Exception as e:
    print("Error during prediction:", e)
