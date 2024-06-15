import matplotlib.pyplot as plt
import pandas as pd
import re

# Read data from file
with open(r'D:\dungnd\GraduationProject\MMFusion-IML\USB_5_6_20_22_25_training_process_phase1.txt', 'r') as file:
    data = file.readlines()

# Initialize lists to store data
epochs = []
training_loss = []
val_loss = []
val_f1_best = []
val_f1_fixed = []

# Parse data
for line in data:
    if 'Training Loss' in line:
        match = re.search(r'Training Loss:(\d+\.\d+) epoch: (\d+)', line)
        if match:
            training_loss.append(float(match.group(1)))
            epochs.append(int(match.group(2)))
    elif 'Val Loss' in line:
        match = re.search(r'Val Loss: (\d+\.\d+) epoch: (\d+)', line)
        if match:
            val_loss.append(float(match.group(1)))
    elif 'Val F1 best' in line:
        match = re.search(r'Val F1 best: (\d+\.\d+) epoch: (\d+)', line)
        if match:
            val_f1_best.append(float(match.group(1)))
    elif 'Val F1 fixed' in line:
        match = re.search(r'Val F1 fixed: (\d+\.\d+) epoch: (\d+)', line)
        if match:
            val_f1_fixed.append(float(match.group(1)))

# Create a DataFrame
df = pd.DataFrame({
    'Epoch': epochs,
    'Training Loss': training_loss,
    'Validation Loss': val_loss,
    'Validation F1 Best': val_f1_best,
    'Validation F1 Fixed': val_f1_fixed
})

# Plot the data
plt.figure(figsize=(12, 8))

# Plot Training Loss
plt.subplot(2, 2, 1)
plt.plot(df['Epoch'], df['Training Loss'], label='Training Loss', color='blue')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.legend()

# Plot Validation Loss
plt.subplot(2, 2, 2)
plt.plot(df['Epoch'], df['Validation Loss'], label='Validation Loss', color='orange')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Validation Loss')
plt.legend()

# Plot Validation F1 Best
plt.subplot(2, 2, 3)
plt.plot(df['Epoch'], df['Validation F1 Best'], label='Validation F1 Best', color='green')
plt.xlabel('Epoch')
plt.ylabel('F1 Score')
plt.title('Validation F1 Best')
plt.legend()

# Plot Validation F1 Fixed
plt.subplot(2, 2, 4)
plt.plot(df['Epoch'], df['Validation F1 Fixed'], label='Validation F1 Fixed', color='red')
plt.xlabel('Epoch')
plt.ylabel('F1 Score')
plt.title('Validation F1 Fixed')
plt.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
