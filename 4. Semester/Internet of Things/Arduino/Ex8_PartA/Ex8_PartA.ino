/*
  Exercise 8 - Part A: Analog Read Serial
  Read potentiometer voltage on A0 and print to serial monitor with 3 decimals.
  Board: Arduino UNO (10-bit ADC, 0-5V range)
*/

const int potPin = A0;
const long baudRate = 9600; // Change to 38400 if serial monitor has issues

void setup() {
  Serial.begin(baudRate);
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
