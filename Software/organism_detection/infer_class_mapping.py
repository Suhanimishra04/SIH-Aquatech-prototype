# infer_class_mapping.py
import os, json, collections
import numpy as np
import cv2
from tensorflow.keras.models import load_model

BASE = r"C:\Users\msuha\Downloads\SIH\Software\organism_detection"
MODEL_PATH = os.path.join(BASE, "microbe_model.h5")
DATASET_TRAIN = r"C:\Users\msuha\Downloads\SIH\datasets\train"  # your prepared train folders
OUT_MAPPING = os.path.join(BASE, "class_indices.json")

def load_model_safely(path):
    print("Loading model:", path)
    m = load_model(path)
    print("Loaded. Model input shape:", m.input_shape, "output shape:", m.output_shape)
    return m

def preprocess_for_model(img_path, input_shape):
    img = cv2.imread(img_path)
    if img is None:
        return None
    # Convert BGR->RGB because Keras ImageDataGenerator uses RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = input_shape[1], input_shape[2]
    img = cv2.resize(img, (w, h))
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)

model = load_model_safely(MODEL_PATH)
input_shape = model.input_shape  # (None, H, W, C)
num_classes = model.output_shape[-1]
print("Model predicts", num_classes, "classes.")

# Walk through train dataset folders and predict
species_prediction_counts = {}  # species -> Counter(predicted_index -> count)

if not os.path.isdir(DATASET_TRAIN):
    raise SystemExit(f"Train dataset folder not found: {DATASET_TRAIN}")

species_dirs = sorted(d for d in os.listdir(DATASET_TRAIN) if os.path.isdir(os.path.join(DATASET_TRAIN, d)))
print("Found species dirs in train:", species_dirs)

for species in species_dirs:
    species_dir = os.path.join(DATASET_TRAIN, species)
    files = [f for f in os.listdir(species_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    print(f"\nProcessing species '{species}' - {len(files)} images (limiting to 200 for speed)")
    counter = collections.Counter()
    limit = min(len(files), 200)
    for f in files[:limit]:
        p = os.path.join(species_dir, f)
        x = preprocess_for_model(p, input_shape)
        if x is None:
            print("  could not read", p)
            continue
        preds = model.predict(x, verbose=0)[0]
        pred_idx = int(np.argmax(preds))
        counter[pred_idx] += 1
    species_prediction_counts[species] = counter
    print("  top predictions for", species, ":", counter.most_common(5))

# Build inferred mapping: species -> predicted_index (choose the most common predicted index per species)
inferred = {}
for species, counter in species_prediction_counts.items():
    if len(counter)==0:
        print("Warning: no predictions for", species)
        continue
    pred_idx, cnt = counter.most_common(1)[0]
    inferred[species] = pred_idx

print("\nInferred species -> index mapping (preliminary):")
print(inferred)

# Check for collisions (same index assigned to multiple species)
inv = {}
for s, idx in inferred.items():
    inv.setdefault(idx, []).append(s)

duplicates = {idx: names for idx, names in inv.items() if len(names) > 1}
if duplicates:
    print("\nWARNING: multiple species assigned same predicted index. Resolving by highest total counts per index.")
    print(duplicates)
    # Resolve by selecting the species with the highest count for that index
    resolved = {}
    # build index -> list of (species, count)
    for s, counter in species_prediction_counts.items():
        for idx, cnt in counter.items():
            resolved.setdefault(idx, []).append((s, cnt))
    final_map = {}
    for idx, lst in resolved.items():
        lst.sort(key=lambda x: x[1], reverse=True)
        chosen_species = lst[0][0]
        final_map[chosen_species] = idx
    # ensure every species has mapping; if any species missing, assign an unused index
    used_indices = set(final_map.values())
    next_idx = 0
    for s in species_dirs:
        if s not in final_map:
            while next_idx in used_indices:
                next_idx += 1
            final_map[s] = next_idx
            used_indices.add(next_idx)
    inferred = final_map
    print("\nResolved mapping (species -> index):", inferred)
else:
    print("No duplicates - mapping OK.")

# Convert to label->index mapping and save as JSON (string keys)
label_to_index = {label: int(idx) for label, idx in inferred.items()}
with open(OUT_MAPPING, "w") as f:
    json.dump(label_to_index, f, indent=4)

print("\nSaved inferred mapping to:", OUT_MAPPING)
print("Mapping:", label_to_index)
print("IMPORTANT: If mapping looks wrong, DO NOT proceed — inspect above printed counters and correct manually.")
