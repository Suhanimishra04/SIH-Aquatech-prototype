// Basic LED control - toggles the built-in LED on and off every second
const int ledPin = 13; // Built-in LED

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH); // Turn LED on
  delay(1000);                // Wait 1 second
  digitalWrite(ledPin, LOW);  // Turn LED off
  delay(1000);                // Wait 1 second
}
