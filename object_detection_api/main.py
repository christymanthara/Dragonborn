import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you want to limit to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv8 model
model = YOLO("yolov8s.pt")

@app.get("/")
async def read_root():
    return {"message": "Hello, World! Yolo is running"}


@app.post("/detect/")
async def detect_objects(file: UploadFile):
    # Process the uploaded image for object detection
    image_bytes = await file.read()
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Perform object detection with YOLOv8
    results = model.predict(image)
    
    # Extract relevant data from results (like bounding boxes, confidence scores, and class names)
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": model.names[box.cls[0].item()],  # class name
                "confidence": box.conf[0].item(),         # confidence score
                "bbox": box.xyxy[0].tolist()              # bounding box in [x1, y1, x2, y2] format
            })
    
    return JSONResponse(content={"detections": detections})

