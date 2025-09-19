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
CSV_PATH = os.path.join(BASE_DIR, "analysis_results.csv")

# --- Arduino Setup ---
try:
    arduino = serial.Serial(port="COM7", baudrate=9600, timeout=2)
    time.sleep(2)
    print("✅ Arduino connected on COM7")
except Exception as e:
    arduino = None
    print("⚠️ Could not connect to Arduino:", e)

# --- Load model ---
model = load_model(MODEL_PATH)

# --- Load class indices ---
with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)
idx_to_class = {v: k for k, v in class_indices.items()}

# --- Counting Function ---
def count_microbes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours), thresh, contours

# --- Classification Function ---
def classify_species(frame):
    img = cv2.resize(frame, (64, 64))
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
    cv2.setNumThreads(0)
    logging.getLogger("PIL").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=UserWarning)

    cap = cv2.VideoCapture(0)  # 0 = default camera, try 1/2 if USB microscope is not first device

    if not cap.isOpened():
        print("❌ Could not access microscope camera")
        return

    print("🎥 Microscope camera stream started. Press 's' to capture & analyze, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame")
            break

        cv2.imshow("Live Microscope Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):  # Capture and analyze
            count, thresh, contours = count_microbes(frame)
            species, conf = classify_species(frame)
            conf_percent = round(conf * 100, 2)

            print(f"[Live Frame] → Species: {species} | Count: {count} | Confidence: {conf_percent}%")
            results.append(["LiveFrame", species, count, conf_percent])
            send_to_arduino(species, count)

            # Show results with overlay
            img_color = frame.copy()
            cv2.drawContours(img_color, contours, -1, (0, 255, 0), 1)
            cv2.putText(img_color, f"{species} ({conf_percent}%) Count:{count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Detection", img_color)

        elif key == ord("q"):  # Quit
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save results
    if results:
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["FrameID", "Species", "Count", "Confidence (%)"])
            writer.writerows(results)
        print(f"✅ Results saved to {CSV_PATH}")

if __name__ == "__main__":
    main()
