// Serial command control for LED
const int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED turned ON");
    } else if (command == "OFF") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED turned OFF");
    } else if (command.startsWith("BRIGHT")) {
      Serial.println("Brightness control placeholder");
    } else {
      Serial.println("Unknown command");
    }
  }
}
