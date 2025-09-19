import serial
import time

class ArduinoController:
    def __init__(self, port='COM3', baudrate=9600):
        self.arduino = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # allow Arduino to reset

    def send_command(self, cmd: str):
        """Send a single character command to Arduino"""
        self.arduino.write(cmd.encode())

    def close(self):
        self.arduino.close()
