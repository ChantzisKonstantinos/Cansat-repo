import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms
import os
import time

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

# script_dir = os.path.dirname(__file__)
# model_path = os.path.join(script_dir, "model.pth")
# model = CNN(inChannels = 3, numClasses = 10).to("cpu")
# model.load_state_dict(torch.load(model_path, map_location="cpu"))
# model.eval()

class VisionSystem:
    def __init__(self, model_path):
        self.model = CNN(inChannels = 3, numClasses = 10).to("cpu")
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5],std=[0.5])])
    def SplitImage(self, img):
        h, w, _ = img.shape
        th = h // 4
        tw = w // 4

        tiles = []

        for i in range(4):
            for j in range(4):

                tiles.append(
                    img[i*th:(i+1)*th, j*tw:(j+1)*tw]
                )

        return tiles
    def PreprocessImage(self,imgArray):
        tiles = self.SplitImage(imgArray)
        tensorList = []
        for t in tiles:
            pil = Image.fromarray(t)
            tensor = self.transform(pil)
            tensorList.append(tensor)
        batch = torch.stack(tensorList).to("cpu")
        return batch
    def ProcessImage(self,imgArray):
        batch = self.PreprocessImage(imgArray)
        with torch.no_grad():
            outputs = self.model(batch)
            predictions = torch.argmax(outputs, dim=1)
            classes = predictions.tolist()
        return classes

