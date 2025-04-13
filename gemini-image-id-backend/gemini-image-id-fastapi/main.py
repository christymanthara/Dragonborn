from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.generativeai import GenerativeModel, Part
from dotenv import load_dotenv
import os
import base64

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

model = GenerativeModel("gemini-pro-vision", api_key=GEMINI_API_KEY)

@app.post("/identify-image/")
async def identify_image(image_file: UploadFile = File(...)):
    try:
        contents = await image_file.read()
        encoded_content = base64.b64encode(contents).decode("utf-8")

        image_data = [Part.from_data(data=encoded_content, mime_type=image_file.content_type)]
        prompt = "What is in this image? Be as descriptive as possible."

        response = model.generate_content([prompt, image_data])
        response.raise_for_status()
        identification = response.text

        return {"identification": identification}
    except Exception as e:
        print(f"Error identifying image: {e}")
        return {"error": "Failed to identify image"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)