// Pin setup
const int sensorPin = A0;               // Temperatur sensor forbundet til analog pin A0
const float voltagePerDegreeC = 0.01;   // 10mV/degC
unsigned long interval = 1000;          // Logging interval i millisekunder
unsigned long previousMillis = 0;       // Stores the last time the sensor was read

void setup() {
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  unsigned long currentMillis = millis();  // Hent aktuelle tid i millisekunder
  unsigned int overTid = currentMillis / 1000;

  // Check if enough time has passed for the next reading
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Update last reading time

    // Aflæs sensoren
    int sensorValue = analogRead(sensorPin);
    
    // Konverter analog reading (0-1023) til spænding (0-5V)
    float voltage = sensorValue * (5.0 / 1023.0);
    
    // Konverter spænding til temperatur i Celsius
    float temperatureC = voltage / voltagePerDegreeC;

    Serial.print(overTid);        // X-akse: Tid i sek
    Serial.print(";");            // Delimiter / kolonne seperator
    Serial.print(temperatureC);   // Y-akse: Volt
    Serial.println();
  }
}