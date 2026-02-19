---
course: "34315"
course-name: "Internet of Things"
type: lecture-note
week: 8
tags: [IoT, lecture]
date: 2026-02-19
---
# Lecture 3 - Basic Electronics for IoT

> [!abstract] Lecture Overview
> Lesson 3/13 — Teacher: Anas Al Shalyan
> Topics: Breadboards & PCBs, schematic symbols, reading schematics, DC vs AC voltage, batteries, voltage/current/resistance, resistors (color codes, series/parallel), Ohm's law, voltage dividers, capacitors, diodes, transistors (MOSFETs), multimeters.
> Reading: Arduino Ch. 5-6.

> [!example] Related Materials
> - Slides: [[34365- Basic-Electronics-IoT.pdf]]
> - Exercise: [[34315_Intro to Ex 8.pdf|Exercise 8 -- Basic Electronics]]
> - Simon's Game: [[34315 Simons game specifications.pdf|Simon's Game Specifications]]
> - Previous: [[Lecture 2 - WiFi Communication]]

---

## 1. Prototyping Tools

### 1.1 Breadboard

A breadboard is a reusable platform for building temporary circuits without soldering:
- **Terminal strips** (inner rows): Connected in short horizontal rows (5 holes each)
- **Bus strips** (outer rails): Connected vertically along the entire length, used for power (+) and ground (-)
- **Center gap**: Separates the two halves, sized for DIP ICs

### 1.2 Printed Circuit Boards (PCBs)

PCBs provide permanent, reliable connections for production circuits. Five main types:

| Type | Description | Use Case |
|------|-------------|----------|
| **Single-layer** | Copper on one side only | Simple circuits |
| **Double-layer** | Copper on both sides | Most common for hobby/small projects |
| **Multi-layer** | 4+ copper layers sandwiched | Complex circuits (computers, phones) |
| **Flex PCB** | Flexible substrate | Wearables, tight spaces |
| **Rigid-flex** | Combination of rigid and flex | Aerospace, medical |

---

## 2. Schematic Symbols

Schematics use standardized symbols to represent electronic components. Key symbols covered:

| Component | Symbol Description |
|-----------|--------------------|
| **Resistor** | Zigzag line (US) or rectangle (EU/IEC) |
| **Capacitor** | Two parallel lines (non-polarized) or one curved line (polarized) |
| **Inductor** | Coiled/looped line |
| **Diode** | Triangle pointing to a line (anode → cathode) |
| **LED** | Diode symbol with arrows (light emission) |
| **Potentiometer** | Resistor with an arrow (adjustable wiper) |
| **Crystal** | Rectangle between two lines |
| **Header/Connector** | Row of circles or pins |
| **Switch** | Gap with a movable contact |
| **IC** | Rectangle with labeled pins |
| **Voltage node** | Arrow pointing up with label (e.g., VCC, 5V) |
| **Ground** | Three horizontal lines decreasing in width |

> [!tip] Reading Schematics
> - Follow current from **positive** supply through components to **ground**
> - Wires that cross with a **dot** are connected; without a dot they are not
> - Component values are usually written next to the symbol (e.g., 10k$\Omega$, 100nF)

---

## 3. Voltage, Current & Resistance

### 3.1 DC vs AC Voltage

| Property | DC (Direct Current) | AC (Alternating Current) |
|----------|-------------------|------------------------|
| **Direction** | Constant (one way) | Alternates periodically |
| **Source** | Batteries, solar cells, USB | Wall outlets, generators |
| **Waveform** | Flat line | Sine wave (typically) |
| **IoT relevance** | Powers all microcontrollers | Mains power (needs conversion) |

### 3.2 Batteries

**Primary batteries** (non-rechargeable):
- Alkaline (AA, AAA: 1.5V), Lithium (CR2032: 3V)
- Use once and discard

**Rechargeable batteries**:
- Li-Ion / Li-Po (3.7V nominal) — most common for IoT
- NiMH (1.2V per cell) — AA/AAA form factor
- Lead-acid (2V per cell) — heavy, high capacity

### 3.3 Fundamental Concepts

| Quantity | Symbol | Unit | Analogy |
|----------|--------|------|---------|
| **Voltage** | $V$ | Volt (V) | Water pressure |
| **Current** | $I$ | Ampere (A) | Water flow rate |
| **Resistance** | $R$ | Ohm ($\Omega$) | Pipe narrowing |

- **Voltage** is the electrical pressure (potential difference) that pushes current through a circuit
- **Current** is the flow of electric charge (electrons) through a conductor
- **Resistance** opposes the flow of current

---

## 4. Resistors

A resistor is a passive component that limits current flow. Two physical formats:

- **PTH (Through-Hole)**: Leads go through holes in the PCB. Larger, easier to prototype with.
- **SMD (Surface Mount)**: Soldered directly onto the PCB surface. Smaller, used in production.

### 4.1 Resistor Color Code

Through-hole resistors use colored bands to indicate their value.

**4-band code** (most common):

| Band | Meaning |
|------|---------|
| 1st band | First significant digit |
| 2nd band | Second significant digit |
| 3rd band | Multiplier (number of zeros) |
| 4th band | Tolerance (gold = 5%, silver = 10%) |

**Color values**: Black=0, Brown=1, Red=2, Orange=3, Yellow=4, Green=5, Blue=6, Violet=7, Grey=8, White=9

> [!example] Color Code Example
> **Brown-Black-Red-Gold** = 10 × 10² = **1 k$\Omega$** ± 5%
> **Yellow-Violet-Orange-Gold** = 47 × 10³ = **47 k$\Omega$** ± 5%

**5-band code** adds a third significant digit for precision resistors (e.g., 1% tolerance).

### 4.2 Series Connection

Resistors in **series** add directly — the total resistance increases:

$$R_{total} = R_1 + R_2 + R_3 + \cdots + R_n$$

Same current flows through all resistors. Voltage divides proportionally.

### 4.3 Parallel Connection

Resistors in **parallel** reduce the total resistance — the reciprocals add:

$$\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} + \cdots + \frac{1}{R_n}$$

**Special case — two resistors in parallel:**

$$R_{total} = \frac{R_1 \cdot R_2}{R_1 + R_2}$$

**Special case — two equal resistors:**

$$R_{total} = \frac{R}{2}$$

Same voltage across all resistors. Current divides between paths.

---

## 5. Ohm's Law

The fundamental relationship between voltage, current, and resistance:

$$V = I \times R$$

Rearranged forms:

$$I = \frac{V}{R} \qquad R = \frac{V}{I}$$

> [!example] Ohm's Law Examples
> **Example 1**: 1.5V battery, 100$\Omega$ resistor:
> $$I = \frac{1.5}{100} = 0.015\text{ A} = 15\text{ mA}$$
>
> **Example 2**: 9V battery, LED rated at 20 mA — find the resistor:
> $$R = \frac{V}{I} = \frac{9}{0.020} = 450\;\Omega$$

---

## 6. Voltage Dividers

A voltage divider uses two resistors in series to produce a lower output voltage from a higher input:

$$V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}$$

Where $R_1$ is connected to $V_{in}$ and $R_2$ is connected to ground, with $V_{out}$ taken from the junction.

> [!example] Voltage Divider Example
> Stepping down **5V to 3.3V** (e.g., for ESP8266 input):
> - $R_1 = 1.7\text{ k}\Omega$, $R_2 = 3.3\text{ k}\Omega$
> - $V_{out} = 5 \times \frac{3.3}{1.7 + 3.3} = 5 \times 0.66 = 3.3\text{ V}$

> [!warning] Voltage Divider Limitations
> Voltage dividers are not ideal voltage regulators — the output voltage drops under load (when current is drawn). For power supply applications, use a proper voltage regulator instead.

---

## 7. Capacitors

A capacitor is a two-terminal component that **stores energy** in an electric field. Each capacitor has a **capacitance** value measured in **Farads (F)**, indicating how much charge it can store.

### 7.1 Capacitance Units

| Prefix | Abbreviation | Value |
|--------|-------------|-------|
| Picofarad | pF | $10^{-12}$ F |
| Nanofarad | nF | $10^{-9}$ F |
| Microfarad | $\mu$F | $10^{-6}$ F |
| Millifarad | mF | $10^{-3}$ F |

### 7.2 Types of Capacitors

| Type | Capacitance Range | Notes |
|------|-------------------|-------|
| **Ceramic** | pF to tens of $\mu$F | Small, non-polarized, common for decoupling |
| **Aluminum electrolytic** | 1 $\mu$F to thousands of $\mu$F | Polarized, larger, bulk filtering |
| **Tantalum** | $\mu$F range | Polarized, compact, stable |
| **Supercapacitor** | Farad range | Energy storage, very high capacitance |

### 7.3 Common Uses in IoT

- **Decoupling/bypass**: Place near IC power pins to filter high-frequency noise (typically 100 nF ceramic)
- **Bulk filtering**: Smooth power supply ripple (typically 10-100 $\mu$F electrolytic)
- **Timing**: RC circuits for delays and oscillators
- **Energy storage**: Brief backup power during supply interruptions

---

## 8. Diodes

A **diode** is a semiconductor device that allows current to flow in **only one direction** — from the **anode** (+) to the **cathode** (-).

### 8.1 Diode Behavior

| Condition | Behavior |
|-----------|----------|
| **Forward bias** (anode > cathode) | Conducts — acts as a short circuit (with ~0.7V drop for silicon) |
| **Reverse bias** (cathode > anode) | Blocks — acts as an open circuit |

### 8.2 Applications

- **Reverse polarity protection**: Prevents damage if a battery is inserted backwards
- **Rectification**: Converting AC to DC
- **LEDs**: Light-emitting diodes produce light when forward biased (specific forward voltage per color)
- **Flyback protection**: Protect circuits from voltage spikes (e.g., when switching inductive loads like motors)

---

## 9. Transistors & MOSFETs

A **transistor** is a semiconductor device used for **switching** and **amplification**. In IoT, transistors are primarily used as electronically controlled switches — allowing a low-power MCU pin to control a high-power load.

### 9.1 MOSFET (Metal Oxide Semiconductor Field Effect Transistor)

MOSFETs are voltage-controlled switches with three terminals:

| Terminal | Function |
|----------|----------|
| **Gate (G)** | Controls ON/OFF (voltage-driven, no current needed) |
| **Drain (D)** | Connects to the load |
| **Source (S)** | Connects to ground (N-MOSFET) or VCC (P-MOSFET) |

### 9.2 N-MOSFET vs P-MOSFET

| Type | Gate HIGH | Gate LOW | Typical Use |
|------|-----------|----------|-------------|
| **N-MOSFET** | ON (conducts drain→source) | OFF (blocks) | Low-side switching |
| **P-MOSFET** | OFF (blocks) | ON (conducts source→drain) | High-side switching |

> [!tip] MOSFET for Motor Control
> An Arduino digital pin (3.3V or 5V) can drive the gate of an N-MOSFET to switch a motor powered by a separate 9V battery. The MCU controls the gate; the MOSFET handles the high-current path. A 1k$\Omega$ pull-down resistor on the gate ensures the MOSFET stays OFF when the MCU pin is floating.

---

## 10. Multimeters

A multimeter is an essential measurement tool for electronics. It can measure:

| Function | What it Measures | Tips |
|----------|------------------|------|
| **Voltage (V)** | Potential difference between two points | Measure in **parallel** (across the component) |
| **Current (A)** | Flow of charge through a point | Measure in **series** (break the circuit and insert meter) |
| **Resistance ($\Omega$)** | Opposition to current flow | Measure with **power off** (component removed from circuit) |
| **Continuity** | Whether a path conducts | Beeps if resistance is near zero — useful for checking wires and traces |

> [!warning] Current Measurement
> Always ensure the multimeter is in **current mode** with the correct terminal (mA or 10A) before measuring current in series. Measuring current with the meter in voltage mode (parallel) can blow the fuse or damage the meter.

---

## Key Takeaways

1. **Breadboards** are for prototyping; **PCBs** are for production — know the connection patterns
2. **Resistor color codes**: memorize the digit-color mapping (Black=0 through White=9) and the band structure
3. **Ohm's law** ($V = IR$) is the most fundamental circuit equation — use it to calculate current-limiting resistors for LEDs
4. **Series resistors add**, **parallel resistors** combine as reciprocals — parallel always gives a lower total resistance
5. **Voltage dividers** ($V_{out} = V_{in} \cdot \frac{R_2}{R_1+R_2}$) are essential for level shifting (e.g., 5V → 3.3V for ESP8266)
6. **Capacitors** store energy — use ceramic for decoupling and electrolytic for bulk filtering
7. **Diodes** conduct in one direction only — use for polarity protection and as LEDs
8. **N-MOSFETs** let a low-power MCU pin switch high-power loads (motors, solenoids, LED strips)
9. **Multimeters** measure V, I, R, and continuity — voltage in parallel, current in series, resistance with power off

---

> [!nav]
> &nbsp;
>
> [[Lecture 2 - WiFi Communication|← Previous]] | [[34315 Internet of Things|34315 Home]]
>
> &nbsp;
