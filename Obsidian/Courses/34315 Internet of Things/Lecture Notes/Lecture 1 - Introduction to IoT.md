---
course: "34315"
course-name: "Internet of Things"
type: lecture-note
week: 6
tags: [IoT, lecture]
date: 2026-02-05
---
# Lecture 1 - Introduction to IoT

> [!abstract] Lecture Overview
> Lesson 1/13 — Teacher: Sarah Ruepp
> Topics: Course introduction, IoT definition & value chain, communication technologies, LP-WAN overview, microcontrollers (Arduino UNO & ESP8266), sensors, Arduino IDE introduction.
> Reading: LPWAN Ch. 1-2, Arduino Ch. 1-2.

> [!example] Related Materials
> - Slides: [[Course intro_iot_microcontrollers.pdf]]
> - Exercise: [[34315_Exercise 1.pdf|Exercise 1 -- Morse Code]]
> - Code: `exercise1MorseCodeSimple.ino`, `exercise1MorseCodeForLoop.ino`, `exercise1MorseCodeFunctions.ino`

---

## 1. Course Overview

The course covers IoT from concept to implementation across 13 weeks:
- **Weeks 1-7**: Lectures on IoT fundamentals, communication, electronics, security
- **Weeks 8-13**: Project work with final presentation and report
- **Assessment**: Mandatory project presentation (07 May) + report hand-in (17 May)
- **Team**: Sarah Ruepp (responsible), Henrik, Anas, Erik + TAs (Reza, Oscar, Laurits, Ahmed)

---

## 2. What is IoT?

The Internet of Things connects physical objects to the internet, enabling them to collect and exchange data. The concept extends everyday objects with computing and communication capabilities.

### 2.1 IoT Connectivity

IoT is about connecting **things** — physical devices, vehicles, appliances, sensors — to the internet. These devices can:
- **Sense** their environment (temperature, light, motion, etc.)
- **Communicate** data to other devices or cloud services
- **Act** on received data or commands (turn on/off, adjust, alert)

### 2.2 IoT Value Chain

The IoT value chain describes how data flows from the physical world to actionable insights:

1. **Sensors/Actuators** — Gather data from the environment or perform actions
2. **Connectivity** — Transmit data (WiFi, LoRa, NB-IoT, Bluetooth, etc.)
3. **Data Processing** — Edge or cloud processing of raw data
4. **Application** — User-facing services and dashboards
5. **Business Value** — Insights, automation, cost savings

### 2.3 IoT System Architecture

A typical IoT system consists of:

| Layer | Components |
|-------|-----------|
| **Perception** | Sensors, actuators, embedded devices |
| **Network** | WiFi, LoRa, NB-IoT, Sigfox, Bluetooth, Zigbee |
| **Processing** | Edge computing, cloud platforms |
| **Application** | Dashboards, alerts, automation, APIs |

---

## 3. Communication Technologies

Different IoT applications require different communication technologies, selected based on range, power consumption, data rate, and cost.

### 3.1 Short-Range Technologies

| Technology | Range | Data Rate | Use Case |
|-----------|-------|-----------|----------|
| **Bluetooth/BLE** | ~10-100 m | 1-3 Mbps | Wearables, beacons |
| **WiFi** | ~50-100 m | Up to Gbps | Smart home, cameras |
| **Zigbee** | ~10-100 m | 250 kbps | Home automation, mesh |
| **Z-Wave** | ~30 m | 100 kbps | Smart home |

### 3.2 Long-Range (LP-WAN) Technologies

LP-WAN (Low-Power Wide-Area Network) technologies are designed for IoT devices that need to send small amounts of data over long distances with minimal power consumption.

| Technology | Range | Data Rate | Spectrum |
|-----------|-------|-----------|----------|
| **LoRa/LoRaWAN** | 2-15 km | 0.3-50 kbps | Unlicensed (ISM) |
| **Sigfox** | 10-50 km | 100 bps | Unlicensed (ISM) |
| **NB-IoT** | 1-10 km | ~250 kbps | Licensed (cellular) |
| **LTE-M** | 1-10 km | ~1 Mbps | Licensed (cellular) |

> [!tip] Choosing a Technology
> The choice depends on the application requirements:
> - **High data rate, short range** → WiFi, Bluetooth
> - **Low data rate, long range, battery-powered** → LoRa, Sigfox, NB-IoT
> - **Mesh networking** → Zigbee, Thread

---

## 4. Microcontrollers

A microcontroller (MCU) is a compact integrated circuit that contains a processor, memory, and I/O peripherals on a single chip. Unlike a general-purpose PC, an MCU is designed for specific, dedicated tasks.

### 4.1 MCU vs PC

| Feature | Microcontroller | PC |
|---------|----------------|-----|
| **Processor** | Simple (8/16/32-bit) | Complex (64-bit, multi-core) |
| **Clock speed** | MHz range | GHz range |
| **Memory** | KB of RAM | GB of RAM |
| **Storage** | KB-MB flash | GB-TB SSD/HDD |
| **Power** | mW range | 50-500 W |
| **OS** | None / RTOS | Full OS |
| **Cost** | $1-10 | $100-1000+ |
| **Purpose** | Dedicated task | General purpose |

### 4.2 Arduino UNO

The Arduino UNO is a popular development board based on the ATmega328P microcontroller:

| Specification | Value |
|---------------|-------|
| **MCU** | ATmega328P |
| **Architecture** | 8-bit AVR |
| **Clock** | 16 MHz |
| **Flash** | 32 KB |
| **SRAM** | 2 KB |
| **EEPROM** | 1 KB |
| **Digital I/O** | 14 pins (6 PWM) |
| **Analog inputs** | 6 pins |
| **Operating voltage** | 5 V |

### 4.3 ESP8266 / NodeMCU

The ESP8266 is a low-cost WiFi-enabled microcontroller, often used on the NodeMCU development board:

| Specification | Value |
|---------------|-------|
| **MCU** | ESP8266 (Tensilica L106) |
| **Architecture** | 32-bit RISC |
| **Clock** | 80/160 MHz |
| **Flash** | 4 MB (external) |
| **RAM** | 80 KB usable |
| **WiFi** | 802.11 b/g/n |
| **Digital I/O** | 17 GPIO pins |
| **Analog input** | 1 pin (10-bit ADC) |
| **Operating voltage** | 3.3 V |

> [!warning] ESP8266 LED Logic
> The ESP8266 built-in LED is **inverted**: `digitalWrite(LED_BUILTIN, HIGH)` turns it **OFF** and `LOW` turns it **ON**. This is opposite to the Arduino UNO.

### 4.4 Sensors

Sensors convert physical quantities into electrical signals that the MCU can read:
- **Temperature** — Thermistors, DHT11/22, DS18B20
- **Light** — LDR (photoresistor), phototransistors
- **Motion** — PIR sensors, accelerometers
- **Distance** — Ultrasonic (HC-SR04), infrared
- **Humidity** — DHT11/22, BME280

---

## 5. Arduino IDE & Programming

The Arduino IDE provides a simple environment for writing and uploading code to Arduino-compatible boards.

### 5.1 Program Structure

Every Arduino program (sketch) has two required functions:

```cpp
void setup() {
    // Runs once at startup
    // Initialize pins, serial, libraries
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    // Runs repeatedly after setup
    // Main program logic
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
```

### 5.2 Key Functions

| Function | Purpose |
|----------|---------|
| `pinMode(pin, mode)` | Set pin as INPUT or OUTPUT |
| `digitalWrite(pin, val)` | Set digital pin HIGH or LOW |
| `digitalRead(pin)` | Read digital pin state |
| `analogRead(pin)` | Read analog value (0-1023) |
| `delay(ms)` | Pause for milliseconds |
| `Serial.begin(baud)` | Start serial communication |
| `Serial.println(data)` | Print to serial monitor |

---

## 6. Exercise 1 — Morse Code

The first exercise introduces Arduino programming by implementing Morse code with an LED:
- **Task 1**: Morse SOS in the simplest way
- **Task 2**: Morse SOS using `for` loops
- **Task 3**: Morse SOS using functions for each letter
- **Task 4**: Use the built-in LED instead of an external one

Equipment: ESP8266/Arduino, LED, 560$\Omega$ resistor, wires, breadboard.

> [!tip] Morse Code Timing
> International standard: dot = 1 unit, dash = 3 units, gap between parts of a letter = 1 unit, gap between letters = 3 units, gap between words = 7 units.

---

## Key Takeaways

1. **IoT** connects physical devices to the internet for sensing, communicating, and acting
2. **LP-WAN** technologies (LoRa, Sigfox, NB-IoT) enable long-range, low-power IoT communication
3. **Microcontrollers** are dedicated, low-power processors designed for embedded tasks — very different from PCs
4. **Arduino UNO** (5V, 8-bit, no WiFi) and **ESP8266** (3.3V, 32-bit, built-in WiFi) are popular IoT development boards
5. Arduino programs have `setup()` (runs once) and `loop()` (runs forever) as their core structure
6. The IoT value chain spans from physical sensors to business applications

---

> [!nav]
> &nbsp;
>
> [[34315 Internet of Things|34315 Home]] | [[Lecture 2 - WiFi Communication|Next →]]
>
> &nbsp;
