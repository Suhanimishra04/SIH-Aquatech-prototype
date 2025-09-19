// DC motor control with L298N or similar motor driver
const int motorPin1 = 7;
const int motorPin2 = 8;

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
}

void loop() {
  // Move motor forward
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  delay(1000);

  // Stop motor
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  delay(500);

  // Move motor backward
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  delay(1000);

  // Stop motor
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  delay(500);
}
