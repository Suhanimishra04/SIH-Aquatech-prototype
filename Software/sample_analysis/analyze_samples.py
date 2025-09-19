import cv2
import os
import numpy as np

# Path to sample images
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "images")

def count_microbes(image_path):
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Preprocessing
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Thresholding (separate microbes from background)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours (each contour is one microbe candidate)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = len(contours)

    return count, thresh, contours

def main():
    for file in os.listdir(IMAGE_FOLDER):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(IMAGE_FOLDER, file)
            count, thresh, contours = count_microbes(path)

            print(f"[{file}] Microbes detected: {count}")

            # Show the result (with contours drawn)
            img = cv2.imread(path)
            cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

            cv2.imshow("Original", img)
            cv2.imshow("Processed", thresh)
            cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
