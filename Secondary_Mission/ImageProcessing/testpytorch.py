from Secondary_Mission.Camera import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms
import os
import time

eurosatClases = ["AnnualCrop",
"Forest",
"HerbaceousVegatation",
"Highway",
"Industrial",
"Pasture",
"PermanentCrop",
"Residential",
"River",
"SeaLake"]

class CNN(nn.Module):
  def __init__(self, inChannels, numClasses):
    super(CNN, self).__init__()
    self.conv1 = nn.Conv2d(in_channels = inChannels, out_channels= 16, kernel_size = 3, stride = 1, padding = 1)
    self.pool = nn.MaxPool2d(kernel_size = 2, stride = 2)
    self.conv2 = nn.Conv2d(in_channels = 16, out_channels = 32, kernel_size = 3, stride = 1, padding = 1)
    self.fc1 = nn.Linear(32 * 16 * 16, 128)
    self.fc2 = nn.Linear(128, numClasses)
    self.dropfc1 = nn.Dropout(p=0.2)

  def forward(self, x):
    x = F.relu(self.conv1(x))
    x = self.pool(x)
    x = F.relu(self.conv2(x))
    x = self.pool(x)
    x = x.view(-1, 32 * 16 * 16)
    x = F.relu(self.dropfc1(self.fc1(x)))
    x = self.fc2(x)
    return x

script_dir = os.path.dirname(__file__)
model_path = os.path.join(script_dir, "model.pth")
device = "cpu"
model = CNN(inChannels = 3, numClasses = 10).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

#start = time.time()
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.5],
        std=[0.5]
    )
])
#end = time.time()

def ClassifyTile(tilePath):
    img = Image.open(tilePath).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        probs = torch.softmax(output, dim=1)
        confidence, prediction = torch.max(probs, dim=1)
    return prediction, confidence





#inference = (end- start)
print("Predicted class:", eurosatClases[pred.item()])
print("Confidence:", float(conf))
#print(inference)

