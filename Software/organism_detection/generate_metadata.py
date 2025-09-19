import os
import csv

# 🔹 Change this to the folder where your images are stored
image_folder = r"C:\Users\msuha\Downloads\SIH\datasets\raw"

# 🔹 Output CSV file (will be created in the same folder as the script)
output_csv = "labels.csv"

with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "species"])  # header row

    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".bmp")):
            # Extract species name from filename (before first underscore or dot)
            species = filename.split("_")[0]
            writer.writerow([filename, species])

print(f"✅ CSV file created: {output_csv}")

