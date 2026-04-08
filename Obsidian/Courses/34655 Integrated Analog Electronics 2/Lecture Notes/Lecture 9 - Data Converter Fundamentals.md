---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: lecture-note
lecture: 9
tags: [IAE2, lecture, data-converters, DAC, ADC, quantization, SQNR, INL, DNL, resistor-string, R2R, current-steering]
---
# Lecture 9 - Data Converter Fundamentals

**Course:** 34655 Integrated Analog Electronics 2
**Lecturer:** Per Lynggaard
**Date:** 2026-04-07

> [!abstract] Lecture Overview
> This lecture covers data converter fundamentals and DAC architectures: D/A and A/D conversion basics, quantization noise analysis (time and frequency domain), SQNR, non-ideal errors (offset, gain, INL, DNL), and DAC topologies including resistor string (tree and digital decoding, folded), binary scaled, R-2R, current steering, capacitor-based, and hybrid DACs.

**Related material:** Chapter 15 & 16 — Data Converter Fundamentals & Nyquist Rate D/A Converters (Baker)

---

## Digital-to-Analog (D/A) Conversion

A DAC takes a digital input code $B_\text{in}$ and a reference voltage $V_\text{ref}$ to produce an analog output:

$$V_\text{out} = V_\text{REF} \cdot B_n$$

Where the binary code is:

$$B_n = b_1 2^{-1} + b_2 2^{-2} + \dots + b_N 2^{-N} = \sum_i b_i 2^{-i} \quad , \; b_i \in \{0, N\}$$

Key definitions:
- **LSB** (Least Significant Bit): $\text{LSB} = \frac{1}{2^N}$, $\quad V_\text{LSB} = \frac{V_\text{REF}}{2^N}$
- **MSB** (Most Significant Bit): $\text{MSB} = \frac{1}{2}$, $\quad V_\text{MSB} = \frac{V_\text{REF}}{2}$

---

## Analog-to-Digital (A/D) Conversion

An ADC takes an analog input $V_\text{in}$ and produces a digital output code $B_\text{out}$:

$$V_\text{REF} \sum_i b_i 2^{-i} = V_\text{in} \pm V_x \quad , \; |V_x| \leq \tfrac{1}{2} V_\text{LSB}$$

A certain voltage range produces the same output code — this is **quantization**. The staircase transfer function introduces an inherent quantization error bounded by $\pm \frac{1}{2}$ LSB.

---

## Quantization Noise — Time Domain

The quantization error is defined as:

$$V_Q = V_1 - V_\text{in} \quad \Leftrightarrow \quad V_1 = V_\text{in} + V_Q$$

For a ramp input, the error is a sawtooth waveform:

$$V_Q(t) = -\frac{V_\text{LSB}}{T} t \quad , \; -\frac{T}{2} < t \leq \frac{T}{2}$$

- Mean value is zero
- RMS value of the quantization noise:

$$\boxed{V_{Q,\text{rms}} = \frac{V_\text{LSB}}{\sqrt{12}}}$$

---

## Signal-to-Quantization Noise Ratio (SQNR)

For a full-scale sinusoidal input ($V_\text{in,rms} = \frac{V_\text{REF}}{2\sqrt{2}}$):

$$\text{SNR} = 20\log_{10}\left(\frac{V_\text{in,rms}}{V_{Q,\text{rms}}}\right) = 20\log_{10}\left(\frac{2^N \sqrt{12}}{2\sqrt{2}}\right)$$

$$\boxed{\text{SQNR} = N \cdot 6.02 \;\text{dB} + 1.76 \;\text{dB}}$$

> [!tip] Key Result
> - Each additional bit adds **6 dB** of SQNR
> - The 1.76 dB offset comes from the sinusoidal signal having more power than the triangular quantization noise

---

## Quantization Noise — Frequency Domain

Quantization noise is modelled as **white noise** (like thermal noise), represented by a power spectral density $S_{n,v}$ V$^2$/Hz:

$$P_n = V_{Q,\text{rms}}^2 = \int_{-f_s/2}^{f_s/2} S_{n,v} \, df = \frac{V_\text{LSB}^2}{12}$$

> [!important] Key Insight
> The total noise power is **independent of sampling rate** $f_s$. A fixed amount of noise power ($V_\text{LSB}^2/12$) is spread between 0 Hz and $f_s$. Therefore:
> - Doubling $f_s$ halves the power spectral density $S_n$
> - This is the basis for **oversampling** techniques

---

## Non-Ideal Errors

### Offset Error

**D/A converter:** The output that occurs for the input code that should produce zero output:

$$E_\text{off,D/A} = \frac{V_\text{out}}{V_\text{LSB}}\bigg|_{0\dots0}$$

**A/D converter:** Deviation of the first transition from the ideal $\frac{1}{2}$ LSB:

$$E_\text{off,A/D} = \frac{V_{0\dots01}}{V_\text{LSB}} - \frac{1}{2}$$

### Gain Error

The difference at full-scale between the ideal and actual transfer curves **after offset error has been reduced to zero**:

**D/A:**

$$E_\text{gain,D/A} = \left(\frac{V_\text{out}}{V_\text{LSB}}\bigg|_{1\dots1} - \frac{V_\text{out}}{V_\text{LSB}}\bigg|_{0\dots0}\right) - (2^N - 1)$$

**A/D:**

$$E_\text{gain,A/D} = \left(\frac{V_{1\dots11} - V_{0\dots01}}{V_\text{LSB}}\right) - (2^N - 2)$$

---

## Definitions: Resolution vs. Accuracy

- **Resolution** is the number of bits $N$ — it does NOT have to equal accuracy (and rarely does)
- **Absolute accuracy**: maximum deviation between ideal and actual transfer curve, given in bits $N_\text{abs}$:

$$E_\text{abs\_acc} = \frac{V_\text{ref}}{2^{N_\text{abs\_acc}}}$$

- **Relative accuracy**: same as absolute accuracy but **corrected for offset and gain error** — equivalent to INL

> [!warning]
> A converter may have 12-bit resolution with only 10-bit accuracy.

---

## Integral Nonlinearity (INL)

- Ideally the transfer curve should be a straight line with normalized slope = 1
- **INL** = ideal transfer curve MINUS actual transfer curve, **corrected for offset and gain error**
- Same as relative accuracy
- Can be measured as best-fit or endpoint method

---

## Differential Nonlinearity (DNL)

- Ideally the transfer curve should increase by **1 LSB per step**
- **DNL** = (step size at code $n+1$) $-$ (step size at code $n$) $-$ 1 LSB
- Can also be calculated after compensating for offset and gain error

> [!tip] Monotonicity
> If DNL $> -1$ LSB for all codes, the converter is **monotonic** (output never decreases when input code increases).

---

## DAC Architectures

### Resistor String DAC with Tree Decoding

A string of $2^N$ equal resistors forms a voltage divider from $V_\text{ref}$ to ground. A tree of switches selects the appropriate tap:

$$V(n) = \frac{n}{2^N} V_\text{REF} = (b_1 2^{-1} + b_2 2^{-2} + b_N 2^{-N}) V_\text{REF}$$

- A buffer (opamp) prevents loading of the resistor string
- All switches change simultaneously — 1 new output per clock cycle
- **Speed limitation**: parasitic capacitance $C_p$ at each internal node creates an RC ladder with time constant:

$$\boxed{\tau_N \approx \frac{N^2}{2} R_\text{on} C_p}$$

- Only one path with $N$ switches is "on" ($R = R_\text{on}$), all others are "off" ($R = +\infty$)

### Resistor String DAC with Digital Decoding

Replaces the switch tree with a **one-hot decoder** (e.g., 3-to-1-of-8):

- Only **one switch** in the signal path (instead of $N$)
- Improved settling time compared to tree decoding
- At the expense of a large digital decoder block
- Inherently **monotonic**
- Resolution limited by resistor matching (~10 bits)
- Resistors are not identical due to **process variation**

### Folded Resistor String DAC

The resistor string is folded into a 2D array with:
- **Word lines** selected by MSB decoder (rows)
- **Bit lines** selected by LSB decoder (columns)
- Reduces layout area and improves routing

### Multiple Resistor String DAC

Uses two cascaded resistor strings with interpolation:
- MSBs select a coarse segment, LSBs interpolate within it
- Fewer resistors needed
- Inherently monotonic (if opamps are matched and offset-independent)
- Reduced settling time and higher resolution compared to single string

---

### Binary Scaled DAC — Voltage Driven

Uses binary-weighted resistors ($2R, 4R, 8R, \dots, 2^N R$) connected to an inverting summing amplifier via switches:

$$V_o = V_\text{REF} \frac{R_F}{R} \sum_{i=1}^{N} b_i \left(\frac{1}{2}\right)^i$$

Properties:
- Number of resistors/switches reduced: $N \ll 2^N$
- Total resistor area is similar to resistor string
- Large ratio between smallest and largest resistor: $2^{N-1}$
- Switches must be scaled to handle different currents ($R_\text{on}$ in series)
- **Monotonicity not guaranteed**
- Glitches when changing code

### R-2R DAC — Voltage Driven

Uses only two resistor values ($R$ and $2R$) in a ladder network:

$$V_o = V_\text{REF} \frac{R_F}{R} \sum_{i=1}^{N} b_i \left(\frac{1}{2}\right)^i$$

Advantages over binary scaled:
- Number of resistors: $2N \ll 2^N$, **and total resistor area is drastically reduced**
- Small ratio between smallest and largest resistor (only 2:1)
- **Monotonic**

Disadvantages:
- Switches still carry very different currents
- Glitches when changing code

### R-2R DAC — Current Driven

Uses the R-2R ladder with **current sources** instead of voltage-driven switches:
- Binary weighted currents in resistors
- **Current is the same in all switches** — major advantage
- Monotonic
- Still has glitches when changing code

### Current Steering DACs

**Binary weighted current sources:**

$$V_o = -2 I_\text{REF} R_F \sum_{i=1}^{N} b_i \left(\frac{1}{2}\right)^i$$

**Equal current sources (thermometer decoded):**
- Differential pair used to steer current
- All current sources are equal value
- Output generated by dumping current into load
- Typical for **high-speed applications**

---

### Binary Scaling DAC Based on Capacitors

Uses binary-weighted capacitors ($C, 2C, 4C, 8C$) with a feedback capacitor $C_\text{fb} = 16C$ and an opamp:

**Two-phase operation** with non-overlapping clocks $\varphi_1$ and $\varphi_2$:

1. **Reset phase** ($\varphi_1 = 0$, $\varphi_2 = 1$): Reset switch ($S_6$) closes, all capacitors charge to $V_\text{OS}$
2. **Sample phase** ($\varphi_1 = 1$, $\varphi_2 = 0$): Bit pattern applied to toggle switches, charge redistribution produces output

For example, $[b_1 b_2 b_3 b_4] = [1011]$:

$$V_\text{out} = -\frac{C_1 + C_3 + C_4}{C_\text{fb}} \cdot (-V_\text{REF}) = \frac{11}{16} V_\text{REF}$$

> [!tip] Advantage
> Capacitor-based DACs are well-suited for IC implementation since capacitor matching in CMOS is typically better than resistor matching.

---

## Glitches in DACs

- Worst case occurs at **MSB transitions** (e.g., $011\dots111 \to 100\dots000$)
- Different delays in decoding and settling cause momentary wrong output
- Glitch energy $E_\text{glitch}$ should be designed to be less than $0.5 \cdot E_\text{LSB}$
- Switch time requirement: $\Delta T < \frac{T}{2^N}$

### Thermometer Decoding — Reducing Glitches

- From sample $n$ to $n+1$, only **one bit changes** at a time
- Switches are not changed simultaneously
- Eliminates worst-case MSB glitch problem
- Requires binary-to-thermometer code conversion logic

---

## Hybrid DACs

Combine multiple topologies (resistor string + capacitor, etc.) to optimize:
- Number of bits
- Sampling rate
- Current consumption
- Area

Example: a 15-bit resistor-capacitor hybrid DAC using 7-bit resistor string for MSBs and 8-bit capacitor array for LSBs with interpolation.

---

## DAC Architecture Comparison

| Architecture | Components | Monotonic | Glitches | Speed | Notes |
|---|---|---|---|---|---|
| **Resistor string (tree)** | $2^N$ resistors, $N$ switches/path | Yes | Low | Limited by RC | Simple, inherently monotonic |
| **Resistor string (digital)** | $2^N$ resistors, 1 switch/path | Yes | Low | Fast | Large digital decoder |
| **Binary scaled** | $N$ resistors | No | Yes | Fast | Large resistor ratio |
| **R-2R (voltage)** | $2N$ resistors | Yes | Yes | Fast | Small resistor ratio, small area |
| **R-2R (current)** | $2N$ resistors | Yes | Yes | Fast | Equal switch currents |
| **Current steering** | $N$ or $2^N-1$ sources | Depends | Depends | Very fast | High-speed applications |
| **Capacitor-based** | $N$ capacitors | Yes | Low | Moderate | Good IC matching |
| **Hybrid** | Mixed | Depends | Low | Optimized | Best combined performance |

---

## Key Takeaways

> [!summary] Essential Concepts
> 1. **Quantization noise** RMS value is $V_\text{LSB}/\sqrt{12}$, independent of signal
> 2. **SQNR** = $N \cdot 6.02 + 1.76$ dB — each bit adds 6 dB
> 3. Quantization noise power is **independent of sampling rate** — oversampling spreads the same power over more bandwidth
> 4. **Offset error** and **gain error** are systematic errors that can be calibrated out
> 5. **INL** (integral nonlinearity) measures deviation from ideal straight line after offset/gain correction
> 6. **DNL** (differential nonlinearity) measures step size deviation from 1 LSB
> 7. Resolution $\neq$ accuracy — a 12-bit converter may only have 10-bit accuracy
> 8. **Resistor string DACs** are inherently monotonic but require $2^N$ resistors
> 9. **R-2R DACs** reduce component count to $2N$ with only two resistor values
> 10. **Thermometer decoding** eliminates worst-case glitches by changing only one bit per step
> 11. **Capacitor-based DACs** exploit good CMOS capacitor matching
> 12. **Hybrid DACs** combine topologies to optimize multiple design parameters

---

> [!nav]
> &nbsp;
>
> [[Lecture 5 - Fabrication and Layout|← Lecture 5]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Lecture 9 - Data Converter Fundamentals|Lecture 9 →]]
