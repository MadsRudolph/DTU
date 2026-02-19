/*
  Exercise 8 - Part D: 7-Segment Display
  Use potentiometer to display digits 0-9 on a 7-segment display.
  Board: Arduino UNO
  Wiring: Potentiometer wiper -> A0
          7-segment (common cathode): a-g -> pins 2-8

  Segment layout:
       a
      ---
   f |   | b
      -g-
   e |   | c
      ---
       d
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
    digitalWrite(segPins[i], digits[digit][i]);
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

  // Map 0-1023 to 0-9
  int digit = map(rawValue, 0, 1023, 0, 9);

  displayDigit(digit);

  Serial.print("Pot: ");
  Serial.print(rawValue);
  Serial.print("  Digit: ");
  Serial.println(digit);

  delay(100);
}
