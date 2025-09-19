import os
import shutil
import random

RAW_DIR = r"C:\Users\msuha\Downloads\SIH\datasets\raw"
OUTPUT_DIR = r"C:\Users\msuha\Downloads\SIH\datasets"

# Create train/val/test folders
splits = ["train", "val", "test"]
for split in splits:
    split_path = os.path.join(OUTPUT_DIR, split)
    os.makedirs(split_path, exist_ok=True)

# Group images by species (from filename prefix before "_")
species_map = {}
for img_file in os.listdir(RAW_DIR):
    if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
        species = img_file.split("_")[0]
        species_map.setdefault(species, []).append(img_file)

# Split 70% train, 20% val, 10% test
for species, files in species_map.items():
    random.shuffle(files)
    n = len(files)
    train_end = int(0.7 * n)
    val_end = int(0.9 * n)

    split_data = {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:]
    }

    for split, split_files in split_data.items():
        species_dir = os.path.join(OUTPUT_DIR, split, species)
        os.makedirs(species_dir, exist_ok=True)

        for f in split_files:
            src = os.path.join(RAW_DIR, f)
            dst = os.path.join(species_dir, f)
            shutil.copy(src, dst)

print("✅ Dataset prepared and split into train/val/test")

