import torch

from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.eval()

example_input = torch.randn(1,3,640,640)

scripted_model = torch.jit.script(model)

scripted_model.save("yolov8n_scripted.pt")