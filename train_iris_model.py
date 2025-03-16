import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision import models
from torch.utils.data import DataLoader, Dataset
import numpy as np
import os
import cv2
from tqdm import tqdm

# Define IrisNet Model
class IrisNet(nn.Module):
    def __init__(self):
        super(IrisNet, self).__init__()
        self.model = models.resnet18(pretrained=True)  # Use ResNet18
        self.model.fc = nn.Linear(self.model.fc.in_features, 128)  # Output 128-dimensional vector

    def forward(self, x):
        return self.model(x)

# Custom Dataset for Iris Images
class IrisDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]
        self.transform = transform

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # Convert grayscale to 3-channel

        if self.transform:
            image = self.transform(image)

        label = idx  # Dummy labels (just for training)
        return image, label

# Define Transformations
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load Dataset
image_dir = "static/iris_images"  # Make sure you have iris images here
dataset = IrisDataset(image_dir, transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Train the Model
def train_model():
    model = IrisNet()
    model.train()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 5  # You can increase this
    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")

        for images, labels in tqdm(dataloader):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f"Loss: {loss.item()}")

    # Save the trained model
    torch.save(model.state_dict(), "models/iris_net.pth")
    print("✅ Model saved as 'models/iris_net.pth'")

if __name__ == "__main__":
    train_model()
