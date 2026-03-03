---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: lecture-note
lecture: 4
tags: [IAE2, lecture, noise, thermal-noise, flicker-noise, SNR, noise-models, MOSFET]
---
# Lecture 4 - Noise

**Course:** 34655 Integrated Analog Electronics 2
**Lecturer:** Per Lynggaard
**Date:** Spring 2026

> [!quote] Piet Hein
> *Great is the one who knows, but even greater is the one who knows where to ask*

> [!abstract] Lecture Overview
> This lecture covers noise analysis in analog integrated circuits: noise types (thermal, flicker, shot), time- and frequency-domain descriptions, noise spectral density, noise models for passive and active components, filtered noise and noise bandwidth, and practical noise analysis of CMOS circuits (common source stages, telescoping cascode, differential pairs).

**Related material:** [[Chapter 9 - Noise and Linearity Analysis and Modelling]]

---

## Relevant Noise Types

### Thermal Noise
- Due to **thermal excitation of charge-carriers** in a conductor
- Has a **white spectral density** (flat across frequency) and is proportional to absolute temperature
- Occurs in **all resistors** (including semiconductors) above absolute zero temperature

### Flicker Noise (1/f Noise)
- Present in all **active devices** as well as carbon resistors
- Only occurs when a **DC current is flowing**
- Arises due to **traps in the semiconductor** — carriers that would normally constitute a DC current flow are held for some time period and then released

### Shot Noise
- Not covered in this course (not relevant for CMOS)
- Occurs because DC bias current is not continuous but consists of individual carrier pulses
- Mainly present in **bipolar transistors and junction diodes**, not in CMOS devices

---

## Noise in the Time Domain

### Inherent vs. Interference Noise

| Type | Description |
|------|-------------|
| **Inherent noise** | Noise generated from within the circuit itself |
| **Interference noise** | External coupling, e.g., electromagnetic interference |

> [!important] Focus
> This lecture focuses on **inherent noise** — the fundamental, unavoidable noise from circuit components.

### Mean Value

Noise is a **random/stochastic** process. The mean value of a noise signal is zero:

$$E\{v_n(t)\} = \frac{1}{T}\int_0^T v_n(t)\,dt = 0$$

### RMS Value (Root Mean Square)

Since the mean is zero, noise is characterized by its **variance** (= rms squared):

$$V_{n,\text{rms}}^2 = E\{v_n^2(t)\} = \frac{1}{T}\int_0^T v_n^2(t)\,dt$$

$$I_{n,\text{rms}}^2 = E\{i_n^2(t)\} = \frac{1}{T}\int_0^T i_n^2(t)\,dt$$

> [!tip] Key Concept
> $\sigma^2 = V_\text{rms}^2$ = **normalized noise power**. The rms value is the standard deviation of the noise distribution, which is typically Gaussian $N(\mu=0,\sigma)$.

---

## Power and Signal-to-Noise Ratio (SNR)

### Power Dissipation

$$P_\text{diss} = V_{n,\text{rms}} \cdot I_{n,\text{rms}} = R \cdot I_{n,\text{rms}}^2 = \frac{V_{n,\text{rms}}^2}{R}$$

### SNR Definition

$$\text{SNR}_\text{dB} = 10\log\left(\frac{P_\text{signal}}{P_\text{noise}}\right) = 10\log\left(\frac{V_{x,\text{rms}}^2}{V_{n,\text{rms}}^2}\right) = 20\log\left(\frac{V_{x,\text{rms}}}{V_{n,\text{rms}}}\right)$$

---

## dBm and dBμ

### dBm — Referenced to 1 mW

$$x\;\text{dBm} = 10\log_{10}\left(\frac{P}{1\;\text{mW}}\right)$$

| dBm | Power |
|-----|-------|
| 0 dBm | 1 mW |
| −10 dBm | 0.1 mW |

### dBμ — Referenced to 1 μW

$$x\;\text{dB}\mu = 10\log_{10}\left(\frac{P}{1\;\mu\text{W}}\right)$$

| dBμ | Power |
|-----|-------|
| 0 dBμ | 1 μW |
| 10 dBμ | 10 μW |

---

## Adding Noise Sources

> [!warning] Critical Rule
> **DO NOT ADD NOISE VOLTAGES — ONLY THEIR POWER!**

For two uncorrelated noise sources $v_{n1}(t)$ and $v_{n2}(t)$ in series:

$$V_{no,\text{rms}}^2 = \frac{1}{T}\int_0^T [v_{n1}(t) + v_{n2}(t)]^2\,dt$$

Expanding:

$$= V_{n1,\text{rms}}^2 + V_{n2,\text{rms}}^2 + \frac{2}{T}\int_0^T v_{n1}(t)\,v_{n2}(t)\,dt$$

The cross-term equals **zero** because noise sources are **uncorrelated**:

$$\boxed{V_{no,\text{rms}}^2 = V_{n1,\text{rms}}^2 + V_{n2,\text{rms}}^2}$$

The same applies for current noise sources in parallel: $I_{no}^2 = I_{n1}^2 + I_{n2}^2$

---

## Noise in the Frequency Domain

### Spectral Density and Root Spectral Density

![[Fig_9.3.png]]
*Fig. 9.3 — (a) Spectral density (power spectral density, V²/Hz) and (b) root spectral density (V/√Hz)*

**Noise spectral density (NSD):** The average normalized power within a 1-Hz bandwidth:

$$\text{NSD:} \quad V_n^2(f) \quad [\text{V}^2/\text{Hz}]$$

**Root spectral density:** The average normalized noise voltage within a 1-Hz bandwidth:

$$\text{Root SD:} \quad V_n(f) \quad [\text{V}/\sqrt{\text{Hz}}]$$

**RMS value from spectral density** (integrating over frequency range):

$$V_{n,\text{rms}}^2 = \int_{f_1}^{f_2} V_n^2(f)\,df$$

---

### Thermal Noise (White Noise) — Spectral Density

![[Fig_9.4.png]]
*Fig. 9.4 — White noise has a flat (constant) root spectral density across all frequencies.*

- The NSD of white noise is **constant for all frequencies**
- In practice, it is limited:
  - At **high frequencies**: NSD goes to zero (as $f \to \infty$)
  - At **low frequencies**: limited by device turn-on time ($f \neq 0$ Hz)

**RMS value of white noise** over bandwidth $[f_1, f_2]$:

$$V_{nw,\text{rms}}^2 = \int_{f_1}^{f_2} V_{nw}^2\,df = V_{nw}^2(f_2 - f_1)$$

---

### Flicker (1/f) Noise — Spectral Density

![[Fig_9.5.png]]
*Fig. 9.5 — Flicker noise combined with white noise, showing the 1/f noise corner frequency.*

The NSD of flicker noise drops at **−10 dB/decade**:

$$V_n^2(f) = \frac{k_v^2}{f}$$

**RMS value of 1/f noise** over $[f_1, f_2]$:

$$V_{n,1/f,\text{rms}}^2 = \int_{f_1}^{f_2}\frac{k_v^2}{f}\,df = k_v^2 \ln\left(\frac{f_2}{f_1}\right)$$

> [!tip] 1/f Noise Corner
> The **1/f noise corner frequency** is where the 1/f noise spectral density equals the white noise spectral density. Below this frequency, 1/f noise dominates; above, white noise dominates.

---

## Filtered Noise

### One Noise Source Through Filter $A(s)$

![[Fig_9.6.png]]
*Fig. 9.6 — A noise signal filtered by transfer function A(s).*

$$\boxed{V_{no}^2(f) = |A(s)|^2 \cdot V_{ni}^2(f)}$$

### Multiple Uncorrelated Sources Through Different Filters

![[Fig_9.7.png]]
*Fig. 9.7 — Multiple uncorrelated noise sources filtered through different transfer functions.*

$$\boxed{V_{no}^2(f) = \sum_i |A_i(s)|^2 \cdot V_{ni,i}^2(f)}$$

---

### Example: 1st Order Lowpass Filter

![[Fig_9.8.png]]
*Fig. 9.8 — (a)–(d) White noise filtered by an RC lowpass filter.*

For a 1st order LP with $A(s) = \frac{1}{1+sRC}$ and white noise input $V_{ni}^2(f) = V_{nw}^2$:

$$V_{no}^2(f) = \left|\frac{1}{1+j\frac{f}{f_0}}\right|^2 V_{nw}^2$$

Integrating to find total output noise power:

$$V_{no,\text{rms}}^2 = \int_0^{+\infty}\frac{1}{1+\left(\frac{f}{f_0}\right)^2}V_{nw}^2\,df = \left[V_{nw}^2 f_0 \arctan\left(\frac{f}{f_0}\right)\right]_0^{+\infty} = V_{nw}^2 f_0 \frac{\pi}{2}$$

Where $f_0 = \frac{1}{2\pi RC}$ and $\omega_0 = \frac{1}{RC}$.

---

### Noise Bandwidth — Brick Wall Equivalent

![[Fig_9.9.png]]
*Fig. 9.9 — (a) First-order LP response and (b) equivalent brick-wall filter with same noise power.*

The **noise bandwidth** $f_x$ is the bandwidth of an ideal brick-wall filter that passes the same total noise power:

$$V_{no,\text{rms}}^2 = \int_0^{+\infty}|A(s)|^2 V_{nw}^2\,df = \int_0^{f_x}V_{nw}^2\,df = V_{nw}^2 f_x$$

For a **1st order LP filter**:

$$V_{nw}^2 f_x = V_{nw}^2 f_0 \frac{\pi}{2} \quad \Longrightarrow \quad \boxed{f_x = f_0\frac{\pi}{2} = \frac{1}{4RC}}$$

> [!important] Relationship
> If a real 1st order LP filter is modelled as an ideal brick-wall filter:
> $$f_0 = f_x \cdot \frac{2}{\pi}$$
> Where $f_0 = \frac{1}{2\pi R_\text{eq}C}$

---

## Noise Models for Circuit Elements

### Resistor — Thermal Noise Only

![[Fig_9.11.png]]
*Fig. 9.11 — Noise models for circuit elements (resistor, diode, BJT, MOSFET, opamp).*

| Model | Expression | Units |
|-------|-----------|-------|
| **Voltage source** (series with noiseless R) | $V_R^2(f) = 4kTR$ | V²/Hz |
| **Current source** (parallel with noiseless R) | $I_R^2(f) = \frac{4kT}{R}$ | A²/Hz |

- $k = 1.38 \times 10^{-23}$ J/K (Boltzmann constant)
- $T$ = absolute temperature in Kelvin
- NSD is $4kTB$ where $B = 1$ Hz (spectral density)
- Use **one or the other** model, but **never both simultaneously!**
- Only **white (thermal) noise** — resistors have no flicker noise

---

### Diode — Thermal Noise Only

The diode equation: $I_D = I_S\left(e^{\frac{qV_D}{nkT}}-1\right)$

| Model | Expression |
|-------|-----------|
| **Voltage source** (series with noiseless $r_d$) | $V_d^2(f) = 2kTr_d$ |
| **Current source** (parallel with noiseless $r_d$) | $I_d^2(f) = 2qI_D$ |

Where $r_d = \frac{kT}{qI_D}$ and $q = 1.6 \times 10^{-19}$ C (electron charge).

---

### MOSFET — Thermal + Flicker Noise

The MOSFET has **two** noise types:

**Individual noise sources** (gate-referred voltage + drain current):

| Noise Source | Expression | Type |
|-------------|-----------|------|
| Flicker (gate voltage) | $V_g^2(f) = \frac{K}{WLC_{ox}f}$ | 1/f |
| Thermal (drain current) | $I_d^2(f) = 4kT\left(\frac{2}{3}\right)g_m$ | White |

**Combined input-referred model** (both referred to gate):

$$\boxed{V_i^2(f) = 4kT\left(\frac{2}{3}\right)\frac{1}{g_m} + \frac{K}{WLC_{ox}f}}$$

- Dominant noise sources for active MOSFETs are **flicker (1/f)** and **thermal** noise
- Valid in the **active (saturation) region**
- Simplified model, valid for **low and moderate frequencies**

> [!tip] Reducing MOSFET Noise
> - **Lower white noise:** Increase $I_D$ and/or $W/L$ (decrease $V_\text{eff}$)
> - **Lower 1/f noise:** Increase $WL$ (larger gate area)

---

## Example: Common Source Stage with Current Load

$$G = -g_m r_{out} = -g_m r_{ds}$$

**Output noise spectral density:**

$$V_{no}^2(f) = I_{no}^2(f) \cdot r_o^2$$

**Input-referred noise spectral density:**

$$V_{ni}^2(f) = \frac{V_{no}^2(f)}{G^2} = \frac{I_{no}^2(f) \cdot r_o^2}{g_m^2 \cdot r_o^2} = \frac{I_{no}^2(f)}{g_m^2}$$

**White noise (input-referred):**

$$V_{ni,w}^2(f) = \frac{\frac{8}{3}kT g_m}{g_m^2} = \frac{8}{3}\frac{kT}{g_m} = \frac{8}{3}\frac{kT}{\sqrt{2\mu_n C_{ox}\frac{W}{L}I_D}} = \frac{8}{3}\frac{kT}{2I_D}V_\text{eff}$$

**1/f noise (input-referred):**

$$V_{ni,1/f}^2(f) = \frac{K_f}{WLC_{ox}f}$$

---

## Example: Common Source Stage with R Load

Output noise current (MOSFET noise + resistor noise):

$$I_{no}^2(f) = I_{n1}^2(f) + I_{nR}^2(f)$$

Using simplified notation: $I_{no}^2 = I_{n1}^2 + I_{nR}^2$

Output noise voltage:

$$V_{no}^2(f) = I_{no}^2(f) \cdot r_o^2 = I_{no}^2(f)(r_{ds}\|R)^2$$

Input-referred noise:

$$V_{ni}^2(f) = \frac{V_{no}^2(f)}{A_v^2} = \frac{I_{no}^2(f) \cdot r_o}{g_{m1}^2 \cdot r_o^2}$$

$$\boxed{V_{ni}^2(f) = \frac{I_{n1}^2 + I_{nR}^2}{g_{m1}^2}}$$

---

## Example: RC Lowpass Filter — kT/C Noise

![[Fig_9.13.png]]
*Fig. 9.13 — (a) Capacitor in parallel with resistor and (b) equivalent noise model circuit.*

Using the 1st order LP result:

$$V_{no,\text{rms}}^2 = V_{nw}^2 f_0 \frac{\pi}{2}$$

Substituting $V_{nw}^2 = 4kTR$ and $f_0 = \frac{1}{2\pi RC}$:

$$V_{no,\text{rms}}^2 = 4kTR \cdot \frac{1}{2\pi RC} \cdot \frac{\pi}{2} = \frac{kT}{C}$$

> [!important] kT/C Noise — Fundamental Result
> $$\boxed{V_{no,\text{rms}}^2 = \frac{kT}{C}}$$
> - Noise power is **INDEPENDENT of R** when integrated over all frequencies!
> - Only depends on **temperature** and **capacitance**
> - Capacitors themselves are **noiseless** — the noise comes from the resistor, but the result only depends on C
> - This sets a **fundamental lower limit** on noise for capacitor-based circuits (e.g., sample-and-hold)

---

## Input-Referred Noise — Two Gain Stages

![[Fig_9.16.png]]
*Fig. 9.16 — Cascaded gain stages: order matters for noise performance.*

For two cascaded stages with gains $G_1$ and $G_2$:

**Output noise power:**

$$V_{no,\text{rms}}^2 = (G_1 \cdot G_2)^2 V_{n1,\text{rms}}^2 + G_2^2 V_{n2,\text{rms}}^2$$

**Input-referred noise power:**

$$V_{ni,\text{rms}}^2 = \frac{V_{no,\text{rms}}^2}{(G_1 \cdot G_2)^2} = V_{n1,\text{rms}}^2 + \frac{1}{G_1^2}V_{n2,\text{rms}}^2$$

> [!warning] Design Rule
> **ALWAYS AS MUCH GAIN AS EARLY AS POSSIBLE!**
>
> Only the second stage noise $V_{n2}$ is divided by $G_1^2$ when referred to the input. A larger first-stage gain suppresses the noise contribution of later stages.

---

## Example: Two CS Stage Amplifier

Two common source stages connected in series (with current loads $I_B$):

**Moving $i_{n1}$ to input of M1:**

$$v_{ni}^2 = \frac{(i_{n1} \cdot r_{ds1})^2}{(g_{m1} \cdot r_{ds1})^2} = \frac{i_{n1}^2}{g_{m1}^2}$$

**Moving $i_{n2}$ to input of M1:**

$$v_{ni}^2 = \frac{(i_{n2} \cdot r_{ds2})^2}{(g_{m1} \cdot r_{ds1})^2 (g_{m2} \cdot r_{ds2})^2} = \frac{i_{n2}^2}{(g_{m1} \cdot g_{m2} \cdot r_{ds1})^2}$$

**Combined input-referred noise:**

$$v_{ni,tot}^2 = \frac{i_{n1}^2}{g_{m1}^2} + \frac{i_{n2}^2}{(g_{m1} \cdot g_{m2} \cdot r_{ds1})^2} \approx \frac{i_{n1}^2}{g_{m1}^2}$$

> [!tip] As expected, **input stage noise dominates** — the second stage contribution is suppressed by the first stage gain.

---

## Telescoping Cascode — Noise Analysis

### Hybrid-Pi Small Signal Model

The telescoping cascode (M1 input transistor + M2 cascode transistor) is analyzed using superposition on the hybrid-pi model with noise sources $i_{n1}$ and $i_{n2}$.

### Superposition — Noise from $M_1$ ($i_{n1}$)

$$v_{no,1}^2 = (i_{n1} \cdot r_{ds1})^2 + g_{m2}^2(i_{n1} \cdot r_{ds1})^2 \cdot r_{ds2}$$
$$v_{no,1}^2 \approx g_{m2}^2(i_{n1} \cdot r_{ds1})^2 \cdot r_{ds2}$$

### Superposition — Noise from $M_2$ ($i_{n2}$)

Since $v_s = 0$ (the controlled source $g_{m2}v_s$ is zero when no input signal drives M2's gate from $i_{n1}$):

$$v_{no,2}^2 = i_{n2}^2 \cdot r_{ds2}^2$$

### Combined Input-Referred Noise

$$v_{ni}^2 = \frac{v_{no,1}^2 + v_{no,2}^2}{(G_\text{total})^2}$$

$$v_{ni}^2 = \frac{i_{n1}^2}{g_{m1}^2} + \frac{i_{n2}^2}{g_{m2}^2 \cdot g_{m1}^2 \cdot r_{ds1}^2} \approx \frac{i_{n1}^2}{g_{m1}^2}$$

> [!important] Key Result
> The cascode transistor M2 contributes negligible noise when referred to the input — the result is the **same as a simple CS stage**. The cascode provides higher gain and output impedance without significantly increasing noise.

---

## Noise in a CMOS Differential Pair

![[Fig_9.20.png]]
*Fig. 9.20 — A CMOS input stage with MOSFET noise sources shown (Q1–Q5).*

### Noise Gain Factors

- $V_{n1}$ and $V_{n2}$ (input pair): noise gain = signal gain = $g_{m1}R_o$
- $V_{n3}$ and $V_{n4}$ (current mirror load): $\left|\frac{V_{no}}{V_{n3}}\right| = \left|\frac{V_{no}}{V_{n4}}\right| = g_{m3}R_o$
- $V_{n5}$ (tail current source): contribution is very small and can be **ignored**

> [!note] Why $V_{n5}$ is Negligible
> The tail current source noise appears as common-mode, which is rejected by the differential pair.

### White Noise Analysis

Output noise:

$$V_{no}^2(f) = 2(g_{m1}R_o)^2 V_{n1}^2(f) + 2(g_{m3}R_o)^2 V_{n3}^2(f)$$

Input-referred (dividing by gain $(g_{m1}R_o)^2$):

$$V_{neq}^2(f) = 2V_{n1}^2(f) + 2V_{n3}^2(f)\left(\frac{g_{m3}}{g_{m1}}\right)^2$$

Substituting $V_{ni}^2(f) = 4kT\gamma\left(\frac{1}{g_{mi}}\right)$:

$$\boxed{V_{neq}^2(f) = 2 \cdot 4kT\gamma\left(\frac{1}{g_{m1}}\right) + 2 \cdot 4kT\gamma\left(\frac{g_{m3}}{g_{m1}}\right)^2\left(\frac{1}{g_{m3}}\right)}$$

Where $\gamma = 2/3$ for long-channel devices (process- and device-dependent).

> [!tip] Minimizing White Noise
> - Maximize $g_{m1}$ of input pair (increase $W/L$ or $I_D$)
> - Minimize $g_{m3}/g_{m1}$ ratio (make load transistors weaker relative to input pair)

### Flicker Noise Analysis

Using the output noise expression and substituting $g_{mi} = \sqrt{2\mu_i C_{ox}\frac{W_i}{L_i}I_{Di}}$ and $V_{ni}^2(f) = \frac{K_i}{W_iL_iC_{ox}f}$:

$$\boxed{V_{ni}^2(f) = \frac{2}{C_{ox}f}\left[\frac{K_1}{W_1L_1} + \left(\frac{\mu_n}{\mu_p}\right)\frac{K_3 L_1}{W_1 L_3^2}\right]}$$

> [!tip] Minimizing Flicker Noise
> - Increase $W_1 L_1$ (input pair gate area)
> - Increase $L_3$ (load transistor length) — this reduces the load pair's 1/f contribution
> - Use PMOS input pair if $K_p < K_n$ (PMOS typically has lower flicker noise)

---

## Key Takeaways

> [!summary] Essential Design Rules
> 1. **Never add noise voltages** — always add noise **powers** (mean-squared values)
> 2. **White noise** (thermal) has flat spectral density: $V_n^2(f) = 4kTR$
> 3. **Flicker noise** has $1/f$ spectral density: $V_n^2(f) = K/(WLC_{ox}f)$
> 4. **Noise bandwidth** of a 1st order LP: $f_x = \frac{\pi}{2}f_0 = \frac{1}{4RC}$
> 5. **kT/C noise** is a fundamental limit: $V_{n,\text{rms}}^2 = kT/C$ (independent of R)
> 6. **Maximize first-stage gain** to suppress noise from subsequent stages
> 7. **Cascode** does not add significant noise compared to a simple CS stage
> 8. In **differential pairs**: input transistor noise dominates; minimize $g_{m3}/g_{m1}$ ratio for lower noise
> 9. **Lower white noise**: increase $g_m$ (via $I_D$ or $W/L$)
> 10. **Lower flicker noise**: increase gate area $WL$

---

> [!nav]
> &nbsp;
>
> [[Lecture 2 - Advanced OpAmps|← Lecture 2]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Lecture 5 - Fabrication and Layout|Lecture 5 →]]
