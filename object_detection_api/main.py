import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# Model:
import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms

# Map class indices to flower names
class_to_flower = ['pink primrose','hard-leaved pocket orchid','canterbury bells','sweet pea','english marigold','tiger lily','moon orchid','bird of paradise','monkshood','globe thistle','snapdragon',"colt's foot",'king protea','spear thistle','yellow iris','globe-flower','purple coneflower','peruvian lily','balloon flower','giant white arum lily','fire lily','pincushion flower','fritillary','red ginger','grape hyacinth','corn poppy','prince of wales feathers','stemless gentian','artichoke','sweet william','carnation','garden phlox','love in the mist','mexican aster','alpine sea holly','ruby-lipped cattleya','cape flower','great masterwort','siam tulip','lenten rose','barbeton daisy','daffodil','sword lily','poinsettia','bolero deep blue','wallflower','marigold','buttercup','oxeye daisy','common dandelion','petunia','wild pansy','primula','sunflower','pelargonium','bishop of llandaff','gaura','geranium','orange dahlia','pink-yellow dahlia?','cautleya spicata','japanese anemone','black-eyed susan','silverbush','californian poppy','osteospermum','spring crocus','bearded iris','windflower','tree poppy','gazania','azalea','water lily','rose','thorn apple','morning glory','passion flower','lotus','toad lily','anthurium','frangipani','clematis','hibiscus','columbine','desert-rose','tree mallow','magnolia','cyclamen','watercress','canna lily','hippeastrum','bee balm','ball moss','foxglove','bougainvillea','camellia','mallow','mexican petunia','bromelia','blanket flower','trumpet creeper','blackberry lily']

print("Model is loading...")
# Step 1: Define the model architecture (Must match the trained model)
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(in_features=2048, out_features=102)  # Ensure output matches 102 classes

# Step 2: Load the fine-tuned model weights
model_path = "fine_tuned_resnet50.pth"  # Ensure the file is in the correct directory
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))) #, map_location=torch.device("cpu")))

# Step 3: Set model to evaluation mode
model.eval()

print("✅ Model loaded successfully!")



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you want to limit to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv8 model
#model = YOLO("yolov8s.pt")

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
    #results = model.predict(image)
    
    # Extract relevant data from results (like bounding boxes, confidence scores, and class names)
    #detections = []
    #for result in results:
    #    for box in result.boxes:
    #        detections.append({
    #            "class": model.names[box.cls[0].item()],  # class name
    #            "confidence": box.conf[0].item(),         # confidence score
    #            "bbox": box.xyxy[0].tolist()              # bounding box in [x1, y1, x2, y2] format
    #        })
    
    #return JSONResponse(content={"detections": detections})


    # RUN the model: 
    #image_path = "cat.jpg"  # Replace with your test image
    #image = Image.open(image_path).convert("RGB")  # Ensure 3-channel format

    # Define preprocessing (same as used during training)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to match model input
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    print("1")
    # Apply transformations
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    print("2")
    image = transform(image).unsqueeze(0)  # Add batch dimension
    print("3")

    # Perform inference
    with torch.no_grad():
        output = model(image)

    # Convert output to class prediction
    predicted_class = torch.argmax(output, dim=1).item()

    print(f"✅ Predicted Flower Label: {predicted_class}, name: {class_to_flower[predicted_class]}")
    detections = []
    detections.append({
        "class":class_to_flower[predicted_class],
        "confidence": 1,         # confidence score
        "bbox": [0,0,1,1]              # bounding box in [x1, y1, x2, y2] format
        
    });
    return JSONResponse(content={"detections": detections})


