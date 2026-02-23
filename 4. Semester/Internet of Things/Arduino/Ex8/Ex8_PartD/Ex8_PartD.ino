/*
  Exercise 8 - Part D
  Add the 7-segment display. Use the potentiometer to count up values from 0 to 9.
*/

const int potPin = A0;

// Segment pins: a, b, c, d, e, f, g
const int segPins[] = {2, 3, 4, 5, 6, 7, 8};
const int numSegments = 7;

// Segment patterns for digits 0-9 (1 = on, 0 = off)
//                          a  b  c  d  e  f  g
const byte digits[10][7] = {
  {1, 1, 1, 1, 1, 1, 0},  // 0
  {0, 1, 1, 0, 0, 0, 0},  // 1
  {1, 1, 0, 1, 1, 0, 1},  // 2
  {1, 1, 1, 1, 0, 0, 1},  // 3
  {0, 1, 1, 0, 0, 1, 1},  // 4
  {1, 0, 1, 1, 0, 1, 1},  // 5
  {1, 0, 1, 1, 1, 1, 1},  // 6
  {1, 1, 1, 0, 0, 0, 0},  // 7
  {1, 1, 1, 1, 1, 1, 1},  // 8
  {1, 1, 1, 1, 0, 1, 1}   // 9
};

void displayDigit(int digit) {
  for (int i = 0; i < numSegments; i++) {
    digitalWrite(segPins[i], !digits[digit][i]); // Invert for common anode
  }
}

void setup() {
  for (int i = 0; i < numSegments; i++) {
    pinMode(segPins[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(potPin);

  // Map 0-1023 to 0-9 (divide into 10 equal bands)
  int digit = rawValue / 103;  // 0-102=0, 103-205=1, ... , 927-1023=9
  if (digit > 9) digit = 9;

  displayDigit(digit);

  Serial.print("Pot: ");
  Serial.print(rawValue);
  Serial.print("  Digit: ");
  Serial.println(digit);

  delay(100);
}
