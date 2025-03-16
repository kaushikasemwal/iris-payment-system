import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import cv2
import numpy as np

class IrisNet(nn.Module):
    def __init__(self):
        super(IrisNet, self).__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 128)  # Output 128-d vector

    def forward(self, x):
        return self.model(x)

def extract_iris_vector(image_path):
    """Extracts 128-dimensional iris vector from an image."""
    model = IrisNet()
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # Convert grayscale to 3-channel
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        iris_vector = model(image).numpy()
    
    return iris_vector.flatten()
