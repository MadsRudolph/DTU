---
course: "34315"
course-name: "Internet of Things"
type: exercise
tags: [IoT, exercise, Arduino, analog]
date: 2026-02-19
---
# Exercise 8 - Analog Input

> [!abstract] Overview
> Analog input exercises using a potentiometer on Arduino UNO. Four parts: reading voltage, LED brightness control, RGB rainbow, and 7-segment display. Individual hand-in with code + video for each part.

> [!info] Hand-in
> - **Deadline**: Wednesday 25 Feb @ 23:59
> - **Where**: Assignment "Exercise 8" on DTU LEARN
> - **Format**: All code in 1 `.zip` (files named `Ex8_PartX_studentnr`), 4 separate video files (NOT zipped)
> - **Individual** — you may discuss, but hand in your own code/video

> [!example] Related Materials
> - Introduction: [[34315_Intro to Ex 8.pdf|Exercise 8 Introduction Slides]]
> - Lecture: [[Lecture 3 - Basic Electronics for IoT]]
> - Slides: [[34365- Basic-Electronics-IoT.pdf|Basic Electronics Slides]]
> - Reading: Arduino Book Ch. 5-6

---

## Background: Analog Input on Arduino UNO

The Arduino UNO has **6 analog input channels** (A0-A5) with a **10-bit ADC**:
- Input range: **0-5V**
- Digital output: **0-1023** (10 bits → $2^{10} = 1024$ levels)
- Resolution: $5\text{V} / 1024 = 4.88\text{ mV}$ per step

A **potentiometer** acts as a variable voltage divider: turning the knob sweeps the wiper voltage from 0V to 5V (or vice versa). Connect the three pins as:
- One outer pin → **5V**
- Other outer pin → **GND**
- Middle pin (wiper) → **A0**

---

## Part A: Read Voltage to Serial Monitor

**Task**: Read the potentiometer voltage on A0 and print it to the serial monitor with 3 decimal places.

**Key concepts**: `analogRead()` returns 0-1023. Convert to voltage using `float()`:

$$V = \frac{\texttt{analogRead(A0)}}{1023} \times 5.0$$

```cpp
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
```

> [!tip] float() Cast
> Without `float()`, the division `rawValue * 5 / 1023` would use integer arithmetic and always return 0. Casting to `float` first ensures decimal precision.

---

## Part B: LED Brightness Control

**Task**: Control a single-color LED's brightness by turning the potentiometer.

**Key concepts**: `analogWrite()` outputs a PWM signal (0-255). Use `map()` to convert the 10-bit ADC range to 8-bit PWM.

**Wiring**: Potentiometer wiper → A0, LED anode → pin 9 (PWM) through a 220$\Omega$ resistor → GND.

```cpp
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
```

> [!tip] PWM Pins on Arduino UNO
> Only pins marked with **~** support `analogWrite()`: **3, 5, 6, 9, 10, 11**. Using a non-PWM pin will only give HIGH/LOW, not dimming.

---

## Part C: RGB LED Rainbow

**Task**: Fade an RGB LED through the rainbow colors based on potentiometer position. 0V = violet/purple, 5V = red.

**Key concepts**: Divide the ADC range into 6 segments corresponding to the rainbow spectrum, and interpolate RGB values within each segment.

**Wiring**: Potentiometer → A0, RGB LED (common cathode): R → pin 9, G → pin 10, B → pin 11 (each through a 220$\Omega$ resistor).

**Rainbow mapping** (0V → 5V):

| Segment | Color Transition | R | G | B |
|---------|-----------------|---|---|---|
| 0 | Violet → Blue | 255→0 | 0 | 255 |
| 1 | Blue → Cyan | 0 | 0→255 | 255 |
| 2 | Cyan → Green | 0 | 255 | 255→0 |
| 3 | Green → Yellow | 0→255 | 255 | 0 |
| 4 | Yellow → Red | 255 | 255→0 | 0 |
| 5 | Red | 255 | 0 | 0 |

```cpp
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

  int r, g, b;
  int segment = rawValue / 171; // 0-5 (6 segments)
  int offset = rawValue % 171;
  int rise = map(offset, 0, 170, 0, 255);
  int fall = 255 - rise;

  switch (segment) {
    case 0: // Violet -> Blue
      r = fall;  g = 0;    b = 255;
      break;
    case 1: // Blue -> Cyan
      r = 0;     g = rise; b = 255;
      break;
    case 2: // Cyan -> Green
      r = 0;     g = 255;  b = fall;
      break;
    case 3: // Green -> Yellow
      r = rise;  g = 255;  b = 0;
      break;
    case 4: // Yellow -> Red
      r = 255;   g = fall; b = 0;
      break;
    default: // Red
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
```

> [!warning] Common Cathode vs Common Anode
> This code assumes a **common cathode** RGB LED (shared GND pin, HIGH = on). If you have a **common anode** LED (shared VCC pin), invert the values: replace `r` with `255 - r`, etc.

---

## Part D: 7-Segment Display

**Task**: Display digits 0-9 on a 7-segment display controlled by the potentiometer.

**Key concepts**: A 7-segment display has 7 LEDs (a-g) that form digits. Map the ADC range to digits 0-9 and drive the corresponding segments.

**Wiring**: Potentiometer → A0, 7-segment (common cathode): segments a-g → pins 2-8 (each through a 220$\Omega$ resistor).

**Segment layout and digit patterns**:

```
     a
    ---
 f |   | b
    -g-
 e |   | c
    ---
     d
```

| Digit | a | b | c | d | e | f | g |
|-------|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| 4 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 6 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| 7 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 8 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |

```cpp
const int potPin = A0;

// Segment pins: a, b, c, d, e, f, g
const int segPins[] = {2, 3, 4, 5, 6, 7, 8};
const int numSegments = 7;

// Segment patterns for digits 0-9 (1 = on, 0 = off)
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
```

> [!tip] Pin Mapping
> If your 7-segment display has different pin assignments, update the `segPins[]` array to match. Check the datasheet for which physical pin maps to which segment (a-g).

---

## Wiring Summary

| Part | A0 | Other Pins | Components |
|------|-----|-----------|------------|
| A | Pot wiper | — | Potentiometer |
| B | Pot wiper | 9: LED | Potentiometer, LED, 220$\Omega$ |
| C | Pot wiper | 9: R, 10: G, 11: B | Potentiometer, RGB LED, 3x 220$\Omega$ |
| D | Pot wiper | 2-8: segments a-g | Potentiometer, 7-seg display, 7x 220$\Omega$ |

All parts share the same potentiometer wiring (5V → outer pin, GND → outer pin, wiper → A0).

---

## Key Functions Reference

| Function | Description |
|----------|-------------|
| `analogRead(pin)` | Read 10-bit ADC value (0-1023) |
| `analogWrite(pin, val)` | Output 8-bit PWM (0-255), pin must be PWM-capable |
| `map(val, fromLow, fromHigh, toLow, toHigh)` | Linear interpolation between ranges |
| `float(x)` | Cast integer to floating point for decimal arithmetic |
| `Serial.println(val, decimals)` | Print value with specified decimal places |

---

> [!nav]
> &nbsp;
>
> [[34315 Internet of Things|34315 Home]]
>
> &nbsp;
