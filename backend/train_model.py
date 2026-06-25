import os
import torch
import torchvision
from torchvision import datasets, transforms
from torch import nn, optim
from torch.utils.data import DataLoader

# 🔥 Data Augmentation (improves accuracy)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
])

# Load dataset
dataset_dir = os.path.join(os.path.dirname(__file__), "dataset")
dataset = datasets.ImageFolder(dataset_dir, transform=transform)

# Print classes
print("Classes:", dataset.classes)

loader = DataLoader(dataset, batch_size=16, shuffle=True)

# 🔥 Model (Transfer Learning)
try:
    weights = torchvision.models.MobileNet_V2_Weights.DEFAULT
    model = torchvision.models.mobilenet_v2(weights=weights)
except AttributeError:
    # Older torchvision versions still support pretrained=True
    model = torchvision.models.mobilenet_v2(pretrained=True)

# Modify final layer
model.classifier[1] = nn.Linear(model.last_channel, len(dataset.classes))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Loss + optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 🚀 Training loop
epochs = 5

for epoch in range(epochs):
    print(f"\n🚀 Starting Epoch {epoch+1}/{epochs}")

    total_loss = 0

    for i, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if i % 10 == 0:
            print(f"Batch {i}, Loss: {loss.item():.4f}")

    print(f"✅ Epoch {epoch+1} Completed, Total Loss: {total_loss:.4f}")

# 💾 Save model
torch.save(model.state_dict(), "model.pth")

print("✅ Training complete. Model saved as model.pth")