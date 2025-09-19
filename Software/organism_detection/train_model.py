# train_model.py (dummy version, no dataset needed)

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define a simple CNN model
model = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(64,64,3)),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(3, activation='softmax')  # 3 classes (e.g. bacteria, algae, protozoa)
])

# Compile it
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Save directly without training
model.save("microbe_model.h5")

print("✅ Dummy model created and saved as microbe_model.h5")
