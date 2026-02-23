/*
  Exercise 8 - Part A
  Read input voltage from potentiometer and write value to serial monitor with 3 decimals.
*/

const int potPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(potPin);

  // Convert 0-1023 to 0.000-5.000 V
  float voltage = float(rawValue) * 5.0 / 1023.0;

  Serial.print("Raw: ");
  Serial.print(rawValue);
  Serial.print("  Voltage: ");
  Serial.println(voltage, 3); // 3 decimal places

  delay(200);
}
