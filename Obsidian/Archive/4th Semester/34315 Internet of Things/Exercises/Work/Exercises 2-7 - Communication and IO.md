---
course: "34315"
course-name: "Internet of Things"
type: exercise
tags: [IoT, exercise, Arduino, serial, LED, button]
date: 2026-02-12
---
# Exercises 2-7 - Communication and IO

> [!abstract] Overview
> Six exercises covering serial I/O, multiple LEDs, push buttons, circuit diagrams, and RGB LED control. Topics: traffic light, digital input, Fritzing diagrams, serial monitor communication, ASCII encoding, and `Serial.parseInt()`.

> [!example] Related Materials
> - Exercise sheet: [[34315_Intro to Ex 2-7.pdf|Exercises 2-7 Introduction]]
> - Solutions: [[Ex 2_4 Solution.pdf|Solution Ex 2-4]], [[Ex 5_7 Solution.pdf|Solution Ex 5-7]]
> - Lecture: [[Lecture 2 - WiFi Communication]]
> - Reading: Arduino Book Ch. 3-4 & 5-6
> - Previous: [[Exercise 1 - Morse Code]]

---

## Exercise 2: Traffic Light

**Task**: Simulate a traffic light using 3 LEDs (red, yellow, green) with serial monitor output.

**Stages**: Red --> Red+Yellow --> Green --> Yellow --> (repeat)

**Wiring**: Red LED --> pin 8, Yellow LED --> pin 9, Green LED --> pin 10 (each with 220$\Omega$ resistor).

```cpp
const byte ledRed = 8;
const byte ledYellow = 9;
const byte ledGreen = 10;
const unsigned int tShort = 500;
const unsigned int tLong = 3 * tShort;

void setup() {
  Serial.begin(9600);
  pinMode(ledRed, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(ledGreen, OUTPUT);
}

void loop() {
  // Red
  digitalWrite(ledGreen, LOW); digitalWrite(ledYellow, LOW);
  digitalWrite(ledRed, HIGH);
  Serial.println("Red");
  delay(tLong);

  // Red + Yellow
  digitalWrite(ledYellow, HIGH);
  Serial.println("Red + Yellow");
  delay(tShort);

  // Green
  digitalWrite(ledRed, LOW); digitalWrite(ledYellow, LOW);
  digitalWrite(ledGreen, HIGH);
  Serial.println("Green");
  delay(tLong);

  // Yellow
  digitalWrite(ledGreen, LOW);
  digitalWrite(ledYellow, HIGH);
  Serial.println("Yellow");
  delay(tShort);
  digitalWrite(ledYellow, LOW);
}
```

**Questions**:
- **2a**: What does `%` (modulo) do? It returns the remainder of integer division. `42 % 5 = 2`.
- **2b**: Why use `count % 8`? It constrains values to the interval [0, 7], handling overflow.
- **2c**: Use Ohm's law to verify LED current is ~20-25 mA.

**Extra**: Make a binary counter (0-7) using the three LEDs.

---

## Exercise 3: Digital Input (Push Button)

**Task**: Use a push button to control an LED.

**Wiring**: Button between a digital pin and GND. Use `INPUT_PULLUP` so the pin reads HIGH when open, LOW when pressed.

```cpp
const byte ledPin = 13;
const byte buttonPin = 7;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // A) Button pressed = LED on
  if (digitalRead(buttonPin) == LOW) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}
```

**Part B**: Invert the logic (LED on by default, button turns it off).

**Part C**: Latching button -- toggle LED state on each press:
```cpp
bool ledState = false;
bool lastButton = HIGH;

void loop() {
  bool currentButton = digitalRead(buttonPin);
  if (currentButton == LOW && lastButton == HIGH) {
    ledState = !ledState;
    digitalWrite(ledPin, ledState);
    delay(50); // debounce
  }
  lastButton = currentButton;
}
```

**Questions**:
- **3a**: With `INPUT_PULLUP`, button connects pin to GND when pressed --> reads LOW.
- **3b**: Latency depends on loop speed. No `delay()` means very responsive.
- **3c**: `!` is the NOT operator: `!true = false`, `!LOW = HIGH`.

> [!tip] INPUT vs INPUT_PULLUP
> `INPUT_PULLUP` activates the internal pull-up resistor, so you only need a button to GND. Without it (`INPUT`), you need an external pull-up or pull-down resistor.

---

## Exercise 4: Fritzing / Draw.io Diagram

**Task**: Draw the circuit setup from Exercise 3 (button + LED) using Fritzing or Draw.io.

- Use proper component representations (not photos of messy wiring)
- Show clear connections between Arduino pins and components
- No code for this exercise

---

## Exercise 5: Serial Monitor (Read/Write)

**Task**: Understand serial communication -- read bytes from the serial monitor and echo them back.

```cpp
int incomingByte = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
}
```

**Questions**:
- **5a**: Why does typing 'G' show 71? Because `Serial.read()` returns the **ASCII decimal value**. 'A'=65, 'G'=71.
- **5b**: Sending a line ending transmits ASCII 10 (Line Feed / `\n`).
- **5c**: Changing `Serial.print(incomingByte, DEC)` to `Serial.print((char)incomingByte)` casts the byte back to a character, so 'G' displays as 'G' instead of 71.

> [!tip] Serial Monitor Settings
> Set baud rate to match code (9600). Set line ending to **"No line ending"** to avoid extra bytes.

---

## Exercise 6: Read from Serial Monitor (LED Control)

**Task**: Control 5 LEDs from serial input. Typing 'a'-'e' turns on the corresponding LED; any other character turns all off.

**Wiring**: 5 LEDs on pins 2-6 (each with 220$\Omega$ resistor).

```cpp
void setup() {
  Serial.begin(9600);
  for (int pin = 2; pin < 7; pin++) {
    pinMode(pin, OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'a': digitalWrite(2, HIGH); break;
      case 'b': digitalWrite(3, HIGH); break;
      case 'c': digitalWrite(4, HIGH); break;
      case 'd': digitalWrite(5, HIGH); break;
      case 'e': digitalWrite(6, HIGH); break;
      default:
        for (int pin = 2; pin < 7; pin++)
          digitalWrite(pin, LOW);
    }
  }
}
```

**Questions**:
- **6a**: `char` is a character data type, typically 8 bits (1 byte), representing one ASCII character.
- **6b**: Given `char mychar = '4'; int val = mychar - '0'; mychar = (char)(val + 'A' - 1);` --> val = 4, mychar = 'D' (4th letter).

**Extra**: Input a number via serial and display it in binary on the LEDs.

---

## Exercise 7: RGB LED via Serial (ASCII String Parsing)

**Task**: Parse comma-separated RGB values from serial input and use them to control an RGB LED.

**Wiring**: RGB LED (common cathode): R --> pin 3, G --> pin 5, B --> pin 6 (PWM pins, each with 220$\Omega$ resistor).

**Input format**: `200,100,40` followed by newline.

```cpp
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  while (Serial.available() > 0) {
    int red = Serial.parseInt();
    int green = Serial.parseInt();
    int blue = Serial.parseInt();

    if (Serial.read() == '\n') {
      red = constrain(red, 0, 255);
      green = constrain(green, 0, 255);
      blue = constrain(blue, 0, 255);

      analogWrite(redPin, red);
      analogWrite(greenPin, green);
      analogWrite(bluePin, blue);

      Serial.print("R:"); Serial.print(red);
      Serial.print(" G:"); Serial.print(green);
      Serial.print(" B:"); Serial.println(blue);
    }
  }
}
```

> [!warning] Common Anode vs Common Cathode
> The solution PDF uses `255 - constrain(val, 0, 255)` which is for **common anode** LEDs. For **common cathode**, just use `constrain(val, 0, 255)` directly.

**Questions**:
- **7a**: RGB = three values (Red, Green, Blue), each 0-255 because one byte = 8 bits = $2^8 = 256$ values.
- **7b**: `Serial.parseInt()` reads characters from the serial buffer and parses them as an integer, stopping at the first non-numeric character.

**Extra**: Use `random()` and a button to generate random colors on press.

---

## Key Functions Reference

| Function | Description | Exercise |
|----------|-------------|----------|
| `Serial.begin(baud)` | Initialize serial at given baud rate | All |
| `Serial.print()` / `println()` | Write to serial monitor | 2, 5, 6, 7 |
| `Serial.available()` | Check if bytes waiting to read | 5, 6, 7 |
| `Serial.read()` | Read one byte from serial buffer | 5, 6, 7 |
| `Serial.parseInt()` | Parse integer from serial string | 7 |
| `digitalRead(pin)` | Read digital pin (HIGH/LOW) | 3 |
| `analogWrite(pin, val)` | PWM output (0-255) | 7 |
| `constrain(val, min, max)` | Clamp value to range | 7 |
| `switch/case` | Branch on discrete values | 6 |

---

> [!nav]
> &nbsp;
>
> [[Exercise 1 - Morse Code|<-- Ex 1]] | [[34315 Internet of Things|34315 Home]] | [[Exercise 8 - Analog Input|Next: Ex 8 -->]]
>
> &nbsp;
