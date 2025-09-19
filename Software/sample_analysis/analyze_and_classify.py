import os
import cv2
import json
import numpy as np
import csv
import warnings
import logging
import serial
import time
from tensorflow.keras.models import load_model

# --- Paths ---
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "organism_detection", "microbe_model.h5")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "..", "organism_detection", "class_indices.json")
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")  # folder with test images
CSV_PATH = os.path.join(BASE_DIR, "analysis_results.csv")

# --- Arduino Setup ---
try:
    arduino = serial.Serial(port="COM7", baudrate=9600, timeout=2)  # ⚠️ change COM port if needed
    time.sleep(2)  # allow Arduino to reset
    print("✅ Arduino connected on COM7")
except Exception as e:
    arduino = None
    print("⚠️ Could not connect to Arduino:", e)

# --- Load model ---
model = load_model(MODEL_PATH)

# --- Load class indices mapping ---
with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)
idx_to_class = {v: k for k, v in class_indices.items()}  # reverse mapping

# --- Counting Function ---
def count_microbes(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours), thresh, contours

# --- Classification Function ---
def classify_species(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (64, 64))  # ✅ match your model's expected input size
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img, verbose=0)
    predicted_idx = int(np.argmax(preds))
    predicted_species = idx_to_class.get(predicted_idx, "Unknown")
    confidence = float(preds[0][predicted_idx])
    return predicted_species, confidence

# --- Send to Arduino ---
def send_to_arduino(species, count):
    if arduino:
        message = f"{species}:{count}\n"
        arduino.write(message.encode())
        print(f"📤 Sent to Arduino → {message.strip()}")
    else:
        print(f"(⚠️ Arduino not connected) {species}:{count}")


# --- Main ---
def main():
    results = []

    # Suppress warnings
    cv2.setNumThreads(0)
    logging.getLogger("PIL").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=UserWarning)

    found_any = False
    for file in os.listdir(IMAGE_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(IMAGE_FOLDER, file)

            # Count microbes
            count, thresh, contours = count_microbes(path)

            # Classify species
            species, conf = classify_species(path)
            conf_percent = round(conf * 100, 2)

            # Print result
            print(f"[{file}] → Species: {species} | Count: {count} | Confidence: {conf_percent}%")
            results.append([file, species, count, conf_percent])

            # Send to Arduino
            send_to_arduino(species, count)

            # --- Show image with contours + label ---
            img_color = cv2.imread(path)
            cv2.drawContours(img_color, contours, -1, (0, 255, 0), 1)
            cv2.putText(img_color, f"{species} ({conf_percent}%) Count:{count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Detection", img_color)

            key = cv2.waitKey(0)  # waits for key press
            if key == ord("q"):   # press q to quit early
                break
            found_any = True

    cv2.destroyAllWindows()

    # Save results to CSV
    if results:
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Filename", "Species", "Count", "Confidence (%)"])
            writer.writerows(results)
        print(f"✅ Results saved to {CSV_PATH}")

    if not found_any:
        print("⚠️ No valid images found in the folder.")

if __name__ == "__main__":
    main()
