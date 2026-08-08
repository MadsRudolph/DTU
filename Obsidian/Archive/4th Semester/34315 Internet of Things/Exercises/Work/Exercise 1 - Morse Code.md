---
course: "34315"
course-name: "Internet of Things"
type: exercise
tags: [IoT, exercise, Arduino, morse]
date: 2026-02-05
---
# Exercise 1 - Morse Code

> [!abstract] Overview
> First Arduino exercise. Program an ESP8266/Arduino to morse SOS and your name using an LED. Four progressive tasks: simple approach, for-loops, functions, and built-in LED.

> [!example] Related Materials
> - Exercise sheet: [[34315_Exercise 1.pdf|Exercise 1 PDF]]
> - Lecture: [[Lecture 1 - Introduction to IoT]]
> - Slides: [[Course intro_iot_microcontrollers.pdf|Lecture 1 Slides]]
> - Reading: Arduino Book Ch. 1-2
> - Code: `exercise1MorseCodeSimple.ino`, `exercise1MorseCodeForLoop.ino`, `exercise1MorseCodeFunctions.ino`

---

## Setup

**Equipment**: 1x ESP8266 (or Arduino UNO), 1x LED, 1x 560$\Omega$ resistor, wires, breadboard.

**Wiring**: Connect LED to any digital pin through the resistor. Use `pinMode(PIN, OUTPUT)` to configure the pin.

**Constants to define**:
```cpp
const byte ledPin = LED_BUILTIN; // or e.g. D6
const int timeUnit = 100;        // base timing unit in ms
```

> [!warning] ESP8266 LED Inversion
> On ESP8266, the built-in LED is **inverted**: `LOW` = ON, `HIGH` = OFF. This is opposite to Arduino UNO.

---

## Morse Code Timing

| Element | Duration |
|---------|----------|
| Dot (.) | 1 time unit |
| Dash (-) | 3 time units |
| Gap between parts of a letter | 1 time unit |
| Gap between letters | 3 time units |
| Gap between words | 7 time units |

**SOS in morse**: `... --- ...` (3 dots, 3 dashes, 3 dots)

---

## Task 1: Simple SOS

Write the morse SOS program in the most straightforward way -- explicit `digitalWrite` and `delay` calls for each dot and dash.

```cpp
const byte ledPin = LED_BUILTIN;
const int timeUnit = 100;
const int dashUnit = timeUnit * 3;
const int letterDelay = dashUnit;
const int wordDelay = timeUnit * 7;

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // S: . . .
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(letterDelay);

  // O: - - -
  digitalWrite(ledPin, LOW); delay(dashUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(dashUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(dashUnit);
  digitalWrite(ledPin, HIGH); delay(letterDelay);

  // S: . . .
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(timeUnit);
  digitalWrite(ledPin, LOW); delay(timeUnit);
  digitalWrite(ledPin, HIGH); delay(wordDelay);
}
```

> [!tip] Note on ESP8266
> This code uses `LOW` = ON for ESP8266. For Arduino UNO, swap `LOW`/`HIGH`.

---

## Task 2: SOS with For-Loops

Use `for` loops to avoid repeating the same dot/dash code:

```cpp
void loop() {
  // S: 3 dots
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW); delay(timeUnit);
    digitalWrite(ledPin, HIGH); delay(timeUnit);
  }
  delay(letterDelay - timeUnit); // already waited 1 unit after last dot

  // O: 3 dashes
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW); delay(dashUnit);
    digitalWrite(ledPin, HIGH); delay(timeUnit);
  }
  delay(letterDelay - timeUnit);

  // S: 3 dots
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW); delay(timeUnit);
    digitalWrite(ledPin, HIGH); delay(timeUnit);
  }
  delay(wordDelay);
}
```

---

## Task 3: SOS with Functions

Create reusable functions for each letter, making it easy to morse any word:

```cpp
void dot() {
  digitalWrite(ledPin, LOW);
  delay(timeUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
}

void dash() {
  digitalWrite(ledPin, LOW);
  delay(dashUnit);
  digitalWrite(ledPin, HIGH);
  delay(timeUnit);
}

void morseS() { dot(); dot(); dot(); delay(letterDelay - timeUnit); }
void morseO() { dash(); dash(); dash(); delay(letterDelay - timeUnit); }

void loop() {
  morseS(); morseO(); morseS();
  delay(wordDelay);
}
```

> [!tip] Extending to Your Name
> Add a function for each letter of your name using the morse code table, then call them in sequence in `loop()`.

---

## Task 4: Built-in LED

Change the code to use `LED_BUILTIN` instead of an external LED pin. On ESP8266, `LED_BUILTIN` is typically GPIO 2. Remember the inverted logic.

---

## Morse Code Reference

| A | .- | J | .--- | S | ... | 1 | .---- |
|---|---|---|---|---|---|---|---|
| B | -... | K | -.- | T | - | 2 | ..--- |
| C | -.-. | L | .-.. | U | ..- | 3 | ...-- |
| D | -.. | M | -- | V | ...- | 4 | ....- |
| E | . | N | -. | W | .-- | 5 | ..... |
| F | ..-. | O | --- | X | -..- | 6 | -.... |
| G | --. | P | .--. | Y | -.-- | 7 | --... |
| H | .... | Q | --.- | Z | --.. | 8 | ---.. |
| I | .. | R | .-. | 0 | ----- | 9 | ----. |

---

## Key Functions Reference

| Function | Description |
|----------|-------------|
| `pinMode(pin, OUTPUT)` | Configure pin as output |
| `digitalWrite(pin, HIGH/LOW)` | Set pin voltage level |
| `delay(ms)` | Pause execution for milliseconds |
| `LED_BUILTIN` | Built-in LED pin constant |

---

> [!nav]
> &nbsp;
>
> [[34315 Internet of Things|34315 Home]] | [[Exercises 2-7 - Communication and IO|Next: Ex 2-7 -->]]
>
> &nbsp;
