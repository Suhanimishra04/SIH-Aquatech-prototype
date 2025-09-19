import os
import json

# Path to your dataset
DATASET_PATH = r"C:\Users\msuha\Downloads\SIH\datasets\raw"

# Extract class names from folder structure OR from file names
# Since your files are like "Yeast_5.png", we'll use prefixes
classes = set()
for fname in os.listdir(DATASET_PATH):
    if fname.lower().endswith((".png", ".jpg", ".jpeg")):
        label = fname.split("_")[0]  # part before underscore
        classes.add(label)

classes = sorted(list(classes))  # sorted for consistent ordering

# Create mapping
class_indices = {cls: idx for idx, cls in enumerate(classes)}

# Save to JSON
with open(r"C:\Users\msuha\Downloads\SIH\Software\organism_detection\class_indices.json", "w") as f:
    json.dump(class_indices, f, indent=4)

print("✅ class_indices.json created with the following mapping:")
print(class_indices)
