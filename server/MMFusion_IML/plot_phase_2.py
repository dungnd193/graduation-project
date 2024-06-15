import matplotlib.pyplot as plt
import pandas as pd
import re

# Read data from file
with open(r'D:\dungnd\GraduationProject\MMFusion-IML\USB_5_6_20_22_25_training_process_phase2.txt', 'r') as file:
    data = file.readlines()

# Initialize lists to store data
epochs = []
val_loss = []
val_auc = []
val_bacc = []

# Parse data
for line in data:
    if 'Val Loss' in line:
        match = re.search(r'Val Loss: ([\d.]+) epoch: (\d+)', line)
        if match:
            val_loss.append(float(match.group(1)))
            epoch = int(match.group(2))
            epochs.append(epoch)
    elif 'Val AUC' in line:
        match = re.search(r'Val AUC: ([\d.]+) epoch: (\d+)', line)
        if match:
            val_auc.append(float(match.group(1)))
    elif 'Val bACC' in line:
        match = re.search(r'Val bACC: ([\d.]+) epoch: (\d+)', line)
        if match:
            val_bacc.append(float(match.group(1)))

# Create a DataFrame
df = pd.DataFrame({
    'Epoch': epochs,
    'Validation Loss': val_loss,
    'Validation AUC': val_auc,
    'Validation bACC': val_bacc
})

# Plot the data
plt.figure(figsize=(12, 8))

# Plot Validation Loss
plt.subplot(3, 1, 1)
plt.plot(df['Epoch'], df['Validation Loss'], label='Validation Loss', color='blue')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Validation Loss')
plt.legend()

# Plot Validation AUC
plt.subplot(3, 1, 2)
plt.plot(df['Epoch'], df['Validation AUC'], label='Validation AUC', color='orange')
plt.xlabel('Epoch')
plt.ylabel('AUC')
plt.title('Validation AUC')
plt.legend()

# Plot Validation bACC
plt.subplot(3, 1, 3)
plt.plot(df['Epoch'], df['Validation bACC'], label='Validation bACC', color='green')
plt.xlabel('Epoch')
plt.ylabel('Balanced Accuracy')
plt.title('Validation bACC')
plt.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
