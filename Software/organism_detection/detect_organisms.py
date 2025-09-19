import cv2
import numpy as np
import tensorflow as tf

# Load the dummy model
MODEL_PATH = "microbe_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Instead of loading metadata.csv, just define dummy classes
CLASS_NAMES = ["Bacteria", "Algae", "Protozoa"]

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (64, 64))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Run prediction
    preds = model.predict(img, verbose=0)
    class_id = np.argmax(preds)
    label = CLASS_NAMES[class_id]

    # Show prediction on frame
    cv2.putText(frame, f"Detected: {label}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Microbe Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
