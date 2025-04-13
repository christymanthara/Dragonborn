from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from fastapi import Form

app = FastAPI()

# Optional: Allow CORS if Unity app is on a different domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, image.filename)

    with open(file_location, "wb") as f:
        content = await image.read()
        f.write(content)

    return {"status": "success", "filename": image.filename}

# Add a route for text messages
@app.post("/message")
async def receive_message(message: str = Form(...)):
    print(f"📩 Message received from Unity: {message}")
    return {"status": "received", "message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
