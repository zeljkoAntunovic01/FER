import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torchvision.models import resnet18, resnet34
from torch.optim import lr_scheduler
import matplotlib.pyplot as plt
import sys
import time
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/cifar10")
if torch.cuda.is_available():
    print("using cuba")
else:
    print(":(")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
num_epochs = 20
learning_rate = 0.001

DATA_DIR = './datasets'

# CIFAR-10 dataset

train_dataset = torchvision.datasets.CIFAR10(root=DATA_DIR, train=True, transform=transforms.Compose([
    transforms.Pad(4),
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32),
    transforms.ToTensor()]))

test_dataset = torchvision.datasets.CIFAR10(root=DATA_DIR, train=False, transform=transforms.Compose([
    transforms.ToTensor()]))

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=100, shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=100, shuffle=False)
# TensorBoard data examples
examples = iter(test_loader)
example_data, example_targets = next(examples)
example_data, example_targets = example_data.to(device), example_targets.to(device)
img_grid = torchvision.utils.make_grid(example_data)
writer.add_image('cifar10_images', img_grid)
writer.close()
#sys.exit()

# Model
model = resnet18(pretrained=False, progress=True).to(device)


# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

#sys.exit()
# Train the model
test_accs1 = []
total_step = len(train_loader)
curr_lr = learning_rate
training_accs = []
running_loss = 0
running_correct_predictions = 0
since = time.time()
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        running_correct_predictions += (predicted == labels).sum().item()

        if (i+1) % 100 == 0:
            cur_acc = running_correct_predictions / 100
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}] Loss: {loss.item()} Acc: {cur_acc}%")
            writer.add_scalar('Randomly Assigned Params Resnet18 Training Loss', running_loss/100, epoch * total_step + i)
            writer.add_scalar('Randomly Assigned Params Resnet18 Training Accuracy', cur_acc, epoch * total_step + i)
            training_accs.append(cur_acc)

            running_loss = 0.0
            running_correct_predictions = 0
    scheduler.step()
    # Test the model
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        test_acc = 100 * correct / total
        test_accs1.append(test_acc)

    model.train()
    print(f"Test acc: {test_acc}%")

print(f'Accuracy of the non-pretrained Resnet18 model on the test images: {test_acc} %')
time_elapsed = time.time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(
    time_elapsed // 60, time_elapsed % 60))
print("\n"*10)







# Pretrained Model
model = resnet18(pretrained=True, progress=True).to(device)

num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10) #10 CIFAR klasa

model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
test_accs = []
total_step = len(train_loader)
curr_lr = learning_rate

running_loss = 0
running_correct_predictions = 0
since = time.time()
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        running_correct_predictions += (predicted == labels).sum().item()

        if (i+1) % 100 == 0:
            cur_acc = running_correct_predictions / 100
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}] Loss: {loss.item()} Acc: {cur_acc}%")
            writer.add_scalar('Pretrained Params Resnet18 Training Loss', running_loss/100, epoch * total_step + i)
            writer.add_scalar('Pretrained Params Resnet18 Training Accuracy', cur_acc, epoch * total_step + i)

            running_loss = 0.0
            running_correct_predictions = 0
    # Test the model
    scheduler.step()
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        pretrained_test_acc = 100 * correct / total
        test_accs.append(pretrained_test_acc)

    model.train()
    print(f"Test acc: {pretrained_test_acc}%")

print(f'Accuracy of the pretrained Resnet18 model on the test images: {pretrained_test_acc} %')
time_elapsed = time.time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(
    time_elapsed // 60, time_elapsed % 60))
print("\n"*10)












# Model
model = resnet34(pretrained=False, progress=True).to(device)


# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

#sys.exit()
# Train the model
test_accs = []
total_step = len(train_loader)
curr_lr = learning_rate

running_loss = 0
running_correct_predictions = 0
since = time.time()
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        running_correct_predictions += (predicted == labels).sum().item()

        if (i+1) % 100 == 0:
            cur_acc = running_correct_predictions / 100
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}] Loss: {loss.item()} Acc: {cur_acc}%")
            writer.add_scalar('Randomly Assigned Params Resnet34 Training Loss', running_loss/100, epoch * total_step + i)
            writer.add_scalar('Randomly Assigned Params Resnet34 Training Accuracy', cur_acc, epoch * total_step + i)
            running_loss = 0.0
            running_correct_predictions = 0
    scheduler.step()
    # Test the model
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        test_acc = 100 * correct / total
        test_accs.append(test_acc)

    model.train()
    print(f"Test acc: {test_acc}%")

print(f'Accuracy of the non-pretrained Resnet34 model on the test images: {test_acc} %')
time_elapsed = time.time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(
    time_elapsed // 60, time_elapsed % 60))
print("\n"*10)







# Pretrained Model
model = resnet34(pretrained=True, progress=True).to(device)

num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10) #10 CIFAR klasa

model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
test_accs = []
total_step = len(train_loader)
curr_lr = learning_rate

running_loss = 0
running_correct_predictions = 0
since = time.time()
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        running_correct_predictions += (predicted == labels).sum().item()

        if (i+1) % 100 == 0:
            cur_acc = running_correct_predictions / 100
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}] Loss: {loss.item()} Acc: {cur_acc}%")
            writer.add_scalar('Pretrained Params Resnet34 Training Loss', running_loss/100, epoch * total_step + i)
            writer.add_scalar('Pretrained Params Resnet34 Training Accuracy', cur_acc, epoch * total_step + i)
            running_loss = 0.0
            running_correct_predictions = 0
    scheduler.step()
    # Test the model
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        pretrained_test_acc = 100 * correct / total
        test_accs.append(pretrained_test_acc)

    model.train()
    print(f"Test acc: {pretrained_test_acc}%")

print(f'Accuracy of the pretrained Resnet34 model on the test images: {pretrained_test_acc} %')
time_elapsed = time.time() - since
print('Training complete in {:.0f}m {:.0f}s'.format(
    time_elapsed // 60, time_elapsed % 60))


