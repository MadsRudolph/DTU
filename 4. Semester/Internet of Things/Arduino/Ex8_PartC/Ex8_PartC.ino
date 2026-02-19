/*
  Exercise 8 - Part C: RGB LED Rainbow
  Use potentiometer to fade an RGB LED through the rainbow.
  0V = violet/purple, 5V = red.
  Board: Arduino UNO
  Wiring: Potentiometer wiper -> A0
          RGB LED: R -> pin 9, G -> pin 10, B -> pin 11 (all PWM, with resistors)
          Common cathode RGB LED assumed (HIGH = on)
*/

const int potPin = A0;
const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(potPin);

  // Map potentiometer to 6 rainbow segments (0-1023 -> 0-1529)
  // Rainbow: violet -> blue -> cyan -> green -> yellow -> orange -> red
  // We split into 6 equal segments of ~170 ADC values each
  int r, g, b;
  int segment = rawValue / 171; // 0-5 (6 segments)
  int offset = rawValue % 171;
  int rise = map(offset, 0, 170, 0, 255);
  int fall = 255 - rise;

  switch (segment) {
    case 0: // Violet -> Blue (R falls, B stays high)
      r = fall;  g = 0;    b = 255;
      break;
    case 1: // Blue -> Cyan (G rises, B stays high)
      r = 0;     g = rise; b = 255;
      break;
    case 2: // Cyan -> Green (B falls, G stays high)
      r = 0;     g = 255;  b = fall;
      break;
    case 3: // Green -> Yellow (R rises, G stays high)
      r = rise;  g = 255;  b = 0;
      break;
    case 4: // Yellow -> Orange/Red (G falls, R stays high)
      r = 255;   g = fall; b = 0;
      break;
    default: // Red (fully turned)
      r = 255;   g = 0;    b = 0;
      break;
  }

  analogWrite(redPin, r);
  analogWrite(greenPin, g);
  analogWrite(bluePin, b);

  Serial.print("Pot: ");
  Serial.print(rawValue);
  Serial.print("  R: ");
  Serial.print(r);
  Serial.print(" G: ");
  Serial.print(g);
  Serial.print(" B: ");
  Serial.println(b);

  delay(50);
}
