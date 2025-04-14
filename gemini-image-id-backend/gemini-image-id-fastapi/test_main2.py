from google import genai
from google.genai import types

import PIL.Image

import os
import base64
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY_2")

client = genai.Client(api_key=GEMINI_API_KEY)

# image = PIL.Image.open('img.jpg')
image = PIL.Image.open('gemini-image-id-backend/gemini-image-id-fastapi/img.jpg')

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["What is this image?", image])

print(response.text)