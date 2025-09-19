import cv2
import time
from organism_detection.detect_organisms import detect
from serial_communication.send_commands import ArduinoController

def main():
    cap = cv2.VideoCapture(0)
    arduino = ArduinoController(port='COM7')

    last_detection_time = 0
    cooldown = 2  # seconds between LED blinks

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        organisms_detected = detect(frame)

        if organisms_detected > 0 and (time.time() - last_detection_time > cooldown):
            print(f"Detected {organisms_detected} organisms!")
            arduino.send_command('1')  # Blink LED once
            last_detection_time = time.time()

        cv2.imshow("Microscope Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
