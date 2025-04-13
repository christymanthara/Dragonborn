import cv2
import numpy as np
import os

# Fix for Qt platform plugin error
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# Model:
import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

# Map class indices to flower names
class_to_flower = ['pink primrose','hard-leaved pocket orchid','canterbury bells','sweet pea','english marigold','tiger lily','moon orchid','bird of paradise','monkshood','globe thistle','snapdragon',"colt's foot",'king protea','spear thistle','yellow iris','globe-flower','purple coneflower','peruvian lily','balloon flower','giant white arum lily','fire lily','pincushion flower','fritillary','red ginger','grape hyacinth','corn poppy','prince of wales feathers','stemless gentian','artichoke','sweet william','carnation','garden phlox','love in the mist','mexican aster','alpine sea holly','ruby-lipped cattleya','cape flower','great masterwort','siam tulip','lenten rose','barbeton daisy','daffodil','sword lily','poinsettia','bolero deep blue','wallflower','marigold','buttercup','oxeye daisy','common dandelion','petunia','wild pansy','primula','sunflower','pelargonium','bishop of llandaff','gaura','geranium','orange dahlia','pink-yellow dahlia','cautleya spicata','japanese anemone','black-eyed susan','silverbush','californian poppy','osteospermum','spring crocus','bearded iris','windflower','tree poppy','gazania','azalea','water lily','rose','thorn apple','morning glory','passion flower','lotus','toad lily','anthurium','frangipani','clematis','hibiscus','columbine','desert-rose','tree mallow','magnolia','cyclamen','watercress','canna lily','hippeastrum','bee balm','ball moss','foxglove','bougainvillea','camellia','mallow','mexican petunia','bromelia','blanket flower','trumpet creeper','blackberry lily']
num_classes = len(class_to_flower)
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

def visualize_result(original_image, mask, output_path=None):    
    # Mask out the original image with the segmentation mask
    masked_image = original_image.copy()
    # Resize the mask to match the dimensions of the original image
    resized_mask = cv2.resize(mask, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)
    # Apply the mask to the image
    #for i in range(3):  # Iterate over the color channels
    #    masked_image[:, :, i] = np.where(resized_mask < 10, 0, masked_image[:, :, c])
    masked_image = Image.fromarray(cv2.cvtColor(masked_image, cv2.COLOR_RGB2RGBA))
    print(masked_image)
    print(masked_image.size)
    masked_image = np.array(masked_image)  # Convert to numpy array for manipulation
    for x in range(resized_mask.shape[0]):
        for y in range(resized_mask.shape[1]):
            if resized_mask[x, y] == resized_mask[0, 0]:  # Assuming the first class is the background
                masked_image[x, y, 3] = 0  # Set alpha channel to 0 for transparency
    #masked_image = Image.fromarray(masked_image)  # Convert back to PIL Image


    # Create a figure
    plt.figure(figsize=(12, 6))
    
    # Show original image
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title('Original Image')
    plt.axis('off')
    
    # Show segmentation mask
    plt.subplot(1, 2, 2)
    plt.imshow(masked_image)
    plt.title('Masked')
    plt.axis('off')
    
    # Save or display the result
    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"Segmentation result saved to {output_path}")
    else:
        plt.show()
    return masked_image









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

    # Apply transformations
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Perform inference
    with torch.no_grad():
        output = model(image)

    # Convert output to class prediction
    highest_confidence = torch.softmax(output, dim=1).max().item()
    print(f"🌟 Confidence: {highest_confidence}")
    if highest_confidence < 0.7:
        print("❌ Confidence too low for prediction.")
        detections = []
        detections.append({
            "class":"Please try again",
            "confidence": 0,         # dummy
            "bbox": [0,0,1,1],       # dummy
            "name": "Please try again",
            "color": "",
        })
        return JSONResponse(content={"detections": detections, "segmentation": 0})

    predicted_class = torch.argmax(output, dim=1).item()
    print(f"✅ Predicted Flower Label: {predicted_class}, name: {class_to_flower[predicted_class]}")

    """
    # SEGMENTATION
    # Load a pre-trained DeepLabV3 model for segmentation
    # Load a pre-trained DeepLabV3 model for segmentation
    segmentation_model = models.segmentation.deeplabv3_resnet50(pretrained=True)
    segmentation_model.classifier[4] = torch.nn.Conv2d(256, num_classes, kernel_size=(1, 1), stride=(1, 1))
    segmentation_model.eval()
    print("✅ Segmentation model adapted for flowers and loaded successfully!")

    # Perform segmentation
    with torch.no_grad():
        # Use the already transformed image
        segmentation_output = segmentation_model(image)['out'][0]
        segmentation_mask = segmentation_output.argmax(0).byte().cpu().numpy()
    print("✅ Segmentation mask generated successfully!")

    # Visualize the result
    masked_image = visualize_result(
        original_image=np.array(Image.open(file.file).convert("RGB")),  # Convert uploaded file to RGB
        mask=segmentation_mask,
        output_path="segmentation_result.png"  # Save the result to a file
    )
    print("✅ Visualization completed!")
    """
    
    """
    # Convert masked_image from numpy array to PIL Image
    print(masked_image.size)
    image = Image.fromarray(cv2.cvtColor(masked_image, cv2.COLOR_RGBA2RGB))
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(masked_image)

    # Convert output to class prediction
    highest_confidence = torch.softmax(output, dim=1).max().item()
    print(f"🌟 Confidence: {highest_confidence}")
    """
    
    detections = []
    detections.append({
        "class":class_to_flower[predicted_class],
        "confidence": highest_confidence,         # dummy
        "bbox": [0,0,1,1],       # dummy
        "name": class_to_flower[predicted_class],
        "color": "beautiful",
    })
    return JSONResponse(content={"detections": detections, "segmentation": 0})



@app.post("/description/")
async def describe_image(file: UploadFile):
    # Process the uploaded image for description
    input_data = await file.read()
    print("input: " + str(input_data))
    return JSONResponse(content={"description": "Image description placeholder"})