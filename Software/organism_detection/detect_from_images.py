# detect_from_images.py (robust debug version)
import os, json, numpy as np, cv2
from tensorflow.keras.models import load_model

BASE = r"C:\Users\msuha\Downloads\SIH\Software\organism_detection"
MODEL_PATH = os.path.join(BASE, "microbe_model.h5")
MAPPING_PATH = os.path.join(BASE, "class_indices.json")
IMAGES_DIR = os.path.join(BASE, "images")

# Load model and mapping
model = load_model(MODEL_PATH)
print("Model loaded. input_shape:", model.input_shape, "output_shape:", model.output_shape)

with open(MAPPING_PATH, "r") as f:
    label_to_index = json.load(f)
print("Loaded label->index mapping:", label_to_index)

# Build reverse mapping index->label
idx_to_label = {int(v): k for k, v in label_to_index.items()}

# Initialize counters
final_counts = {label: 0 for label in label_to_index.keys()}

# Preprocess helper
def preprocess(path):
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = model.input_shape[1], model.input_shape[2]
    img = cv2.resize(img, (w, h))
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)

# Confirm images folder
if not os.path.isdir(IMAGES_DIR):
    raise SystemExit("Images folder not found: " + IMAGES_DIR)

files = sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
print("Found", len(files), "test images")

for fname in files:
    path = os.path.join(IMAGES_DIR, fname)
    print("\nProcessing:", fname)
    x = preprocess(path)
    if x is None:
        print("  ERROR: cannot read image")
        continue
    print("  image shape after prep:", x.shape, "min/max:", x.min(), x.max())
    preds = model.predict(x, verbose=0)[0]
    print("  raw preds:", preds)
    pred_idx = int(np.argmax(preds))
    pred_prob = float(preds[pred_idx])
    species = idx_to_label.get(pred_idx, "Unknown")
    print(f"  predicted index={pred_idx}, species={species}, prob={pred_prob:.4f}")

    if species != "Unknown":
        final_counts[species] += 1

# Final summary
print("\n===== Final Results =====")
found_any = False
for label, count in final_counts.items():
    if count > 0:
        found_any = True
        print(f"{label}: 1 (Count={count})")
if not found_any:
    print("No species detected. (Either mapping is wrong, preprocessing mismatches model, or model outputs unexpected values.)")
