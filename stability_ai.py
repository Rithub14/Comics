import io
import os
import warnings
import random
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the STABILITY_KEY environment variable is set
if 'STABILITY_KEY' not in os.environ:
    raise KeyError("STABILITY_KEY environment variable not found. Please set it in your .env file or environment.")

# Set Stability host
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

seed = random.randint(0, 1000000000)

# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],  # API Key reference.
    verbose=True,  # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0",  # Set the engine to use for generation.
    # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
)

def text_to_image(prompt):
    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt=prompt,
        seed=seed,  # If a seed is provided, the resulting generated image will be deterministic.
        steps=30,  # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=8.0,  # Influences how strongly your generation is guided to match your prompt.
        width=1024,  # Generation width, defaults to 1024 if not included.
        height=1024,  # Generation height, defaults to 1024 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, display generated image.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img
                img = Image.open(io.BytesIO(artifact.binary))
                return img 

def edit_image(input_image_path, prompt, output_image_name):
    img = Image.open(input_image_path)

    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt=prompt,
        init_image=img,  # Assign our previously generated img as our Initial Image for transformation.
        start_schedule=0.6,  # Set the strength of our prompt in relation to our initial image.
        seed=123463446,  # If attempting to transform an image that was previously generated with our API,
        steps=50,  # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=8.0,  # Influences how strongly your generation is guided to match your prompt.
        width=512,  # Generation width, defaults to 512 if not included.
        height=512,  # Generation height, defaults to 512 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated image.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img2
                img2 = Image.open(io.BytesIO(artifact.binary))
                img2.save(output_image_name + ".png")  # Save our generated image with its seed number as the filename and the img2img suffix so that we know this is our transformed image.
