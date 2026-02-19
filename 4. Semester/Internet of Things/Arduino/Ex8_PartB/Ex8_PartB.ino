/*
  Exercise 8 - Part B: LED Brightness Control
  Control a single-color LED brightness with a potentiometer using PWM.
  Board: Arduino UNO
  Wiring: Potentiometer wiper -> A0, LED (with resistor) -> pin 9 (PWM)
*/

const int potPin = A0;
const int ledPin = 9; // Must be a PWM pin (~)

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(potPin);

  // Map 10-bit ADC (0-1023) to 8-bit PWM (0-255)
  int brightness = map(rawValue, 0, 1023, 0, 255);

  analogWrite(ledPin, brightness);

  Serial.print("Pot: ");
  Serial.print(rawValue);
  Serial.print("  Brightness: ");
  Serial.println(brightness);

  delay(50);
}
