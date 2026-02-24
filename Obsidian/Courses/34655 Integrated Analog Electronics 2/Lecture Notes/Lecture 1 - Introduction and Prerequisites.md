---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: lecture-note
lecture: 1
tags: [IAE2, lecture]
---
# Lecture 1 - Introduction and Prerequisites

**Course:** 34655 Integrated Analog Electronics 2
**Lecturer:** Per B. Lynggaard
**Date:** Week 6, Spring 2026

> [!example] Related Exercises
> - [[Problem 1 - Amplifier Configurations]]

---

## Course Overview

### Course Objective

> [!abstract] Main Goal
> To enable the student to **analyze** and **design** analog circuits with an emphasis on integrated **amplifiers** and **data converters** in CMOS technology.

### Learning Objectives

After completing this course, you will be able to:

1. Analyze and design different basic types of CMOS opamps (folded cascode, current mirror, two-stage)
2. Analyze the frequency response of CMOS opamps
3. Design frequency compensation for opamps with feedback
4. Apply noise models for transistors and resistors
5. Analyze layout of simple transistor circuits
6. Describe basic types and properties of data converters (A/D and D/A)
7. Analyze different types of Nyquist D/A and A/D converters
8. Make simulations in Cadence environments

### Course Structure

| Component | Weight | Deadline |
|-----------|--------|----------|
| Report on paper design of OpAmp | ~33% | February 27, 2026 |
| Poster of OpAmp | ~33% | April 10, 2026 |
| Quizzes | ~34% | Throughout course |

### Textbooks

- **Main:** Tony Chan Carusone, David Johns and Kenneth Martin, "Analog Integrated Circuit Design"
- **Supplementary (free):** Erik Bruun, "CMOS Analog IC Design: Fundamentals" and "Problems and Solutions"

---

## Prerequisites Recap: MOSFET Fundamentals

### The MOS Transistor

Two types: **NMOS** and **PMOS** - both are 4-terminal devices (Gate, Source, Drain, Bulk)

> [!warning] Sign Convention
> Pay attention to voltage and current signs! For PMOS, $V_{GS}$ and $I_D$ are negative in normal operation.

---

### Large Signal Model (Shichman-Hodges)

#### NMOS Operating Regions

| Region | Condition | Drain Current |
|--------|-----------|---------------|
| **Off (Cutoff)** | $V_{GS} < V_t$ | $I_D = 0$ |
| **Linear (Triode)** | $V_{DS} < V_{eff}$ AND $V_{GS} > V_t$ | $I_D = \mu C_{ox}\frac{W}{L}\left[(V_{GS}-V_t)V_{DS} - \frac{1}{2}V_{DS}^2\right](1+\lambda V_{DS})$ |
| **Saturation (Active)** | $V_{DS} > V_{eff}$ AND $V_{GS} > V_t$ | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2(1+\lambda V_{DS})$ |

Where:
- $V_{eff} = V_{GS} - V_t$ is the **effective voltage** (overdrive voltage)
- $\lambda$ is the channel length modulation parameter
- $V_A = 1/\lambda$ is the Early voltage

> [!tip] Simplified Saturation Formula
> For hand calculations, we often ignore channel length modulation:
> $$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2$$

---

### Input Characteristics

The input characteristic shows $I_D$ vs $V_{GS}$:

- Below $V_t$: transistor is OFF ($I_D = 0$)
- Above $V_t$: quadratic relationship (in saturation)

$$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2$$

---

### Output Characteristics

The output characteristic shows $I_D$ vs $V_{DS}$ for different $V_{GS}$ values:

- **Linear region:** $I_D$ increases with $V_{DS}$
- **Saturation region:** $I_D$ approximately constant (slight slope due to $\lambda$)

The slope in saturation is due to **channel length modulation** - the effective channel length decreases as $V_{DS}$ increases.

---

### Other Important Effects

#### Bulk (Body) Effect

When $V_{BS} \neq 0$, the threshold voltage changes:

$$V_t = V_{t0} + \gamma\left(\sqrt{V_{SB} + |2\Phi_F|} - \sqrt{|2\Phi_F|}\right)$$

Where:
- $\Phi_F$ is the Fermi potential (~1 V)
- $\gamma$ is the body effect coefficient (process dependent)

#### Sub-threshold Operation

Below threshold, current is not zero but exponentially dependent on $V_{GS}$:

$$I_D = I_{D0}\frac{W}{L}\exp\left(\frac{V_{GS}}{nV_T}\right)$$

Where $V_T = \frac{kT}{q} \approx 25$ mV at room temperature.

---

## Small Signal Model

### Why Linearize?

The MOSFET is inherently **nonlinear**. For small signal analysis, we linearize around the DC operating point (bias point).

> [!note] Notation Convention
> - **Capital letters** (e.g., $V_{GS}$, $I_D$) = DC bias point values
> - **Lowercase letters** (e.g., $v_{gs}$, $i_d$) = small signal (AC) values

---

### Transconductance ($g_m$)

The transconductance relates small changes in $v_{gs}$ to changes in $i_d$:

$$g_m = \frac{\partial i_D}{\partial v_{GS}}\bigg|_{\text{Bias}}$$

**Three equivalent expressions for $g_m$:**

| Expression | Form |
|------------|------|
| Process/geometry | $g_m = \mu C_{ox}\frac{W}{L}(V_{GS}-V_t)$ |
| In terms of $V_{eff}$ | $g_m = \frac{2I_D}{V_{eff}}$ |
| In terms of $I_D$ | $g_m = \sqrt{2\mu C_{ox}\frac{W}{L}I_D}$ |

> [!tip] Key Insight
> $g_m$ depends on both **geometry** ($W/L$) and **bias current** ($I_D$).

---

### Output Conductance ($g_{ds}$)

Models channel length modulation - the slope in the output characteristics:

$$g_{ds} = \frac{1}{r_{ds}} = \frac{\partial i_D}{\partial v_{DS}}\bigg|_{\text{Bias}} \approx I_D\lambda$$

$$r_{ds} \approx \frac{1}{I_D\lambda} = \frac{V_A}{I_D}$$

---

### Complete Small Signal Model

The basic small signal model consists of:
- Voltage-controlled current source: $g_m v_{gs}$
- Output resistance: $r_{ds}$ (parallel to current source)

> [!important] Operating Point Dependence
> The small signal **circuit topology** is the same for all operating points, but the **parameter values** ($g_m$, $g_{ds}$, capacitances) depend on the specific bias point.

---

## Single-Stage Amplifier Configurations

### Current Mirror

| Property | Description |
|----------|-------------|
| Function | Mirrors and scales currents |
| Current ratio | $I_{out} = K \cdot I_B$ where $K = (W/L)_{out}/(W/L)_{ref}$ |
| Output impedance | $r_{out} = r_{ds}$ (can be increased with cascoding) |
| Application | Distributing bias currents throughout a circuit |

---

### Common Source Stage

| Property | Value |
|----------|-------|
| Voltage gain | $A_v = -g_m(r_{ds} \parallel R_L)$ |
| Open-circuit gain | $A_{voc} = -g_m r_{ds} = -\frac{2V_A}{V_{eff}}$ |
| Output resistance | $r_o = r_{ds}$ |
| Input resistance | $r_{in} = \infty$ |

**Characteristics:**
- Very commonly used gain stage
- **Inverting** gain (negative sign)
- Gate-drain capacitance exposed to **Miller effect**

---

### Common Drain (Source Follower)

| Property | Value |
|----------|-------|
| Gain (no bulk effect) | $A_v = \frac{g_m}{g_m + g_{ds}} \approx 1 - \frac{g_{ds}}{g_m} < 1$ |
| Gain (with bulk effect) | $A_v = \frac{g_m}{g_m + g_s + g_{ds}}$ |
| Output resistance | $r_o = \frac{1}{g_m}$ |
| Input resistance | $r_{in} = \infty$ |

**Characteristics:**
- Often used as **output stage**
- **Non-inverting** gain (positive, close to 1)
- **Low output impedance**
- Bulk effect reduces gain below 1

---

### Common Gate Stage

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = g_m r_{ds}$ |
| Output resistance | $r_o = r_{ds}(1 + R_S g_m)$ |
| Input resistance | $r_{in} = \frac{1}{g_m}\left(1 + \frac{R_L}{r_{ds}}\right)$ |

**Characteristics:**
- Same gain magnitude as common source but **non-inverting**
- **Low input impedance** (if $R_L$ not large)
- Can achieve **high output impedance**

> [!note] Bulk Effect
> To include bulk effect, replace $g_m$ with $(g_m + g_{mb})$ in the equations.

---

### Differential Stage

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = g_{m1}(r_{ds1} \parallel r_{ds4})$ |
| Output resistance | $r_o = r_{ds1} \parallel r_{ds4}$ |
| Matching requirement | $(W/L)_1 = (W/L)_2$ and $(W/L)_3 = (W/L)_4$ |

**Characteristics:**
- **High differential gain**
- **Low common mode gain** (ideally zero) → high CMRR
- **Transistor pairs must be matched!**

---

### Cascode Stage (Telescopic)

Common Source followed by Common Gate:

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = -A_{i1}A_{i2} = -g_{m1}r_{ds1}g_{m2}r_{ds2}$ |
| Output resistance | $r_o = r_{ds1}A_{i2} = r_{ds1}g_{m2}r_{ds2}$ |

Where $A_i = g_m r_{ds}$ is the **intrinsic gain** of a transistor.

**Characteristics:**
- **Very high gain** (~square of single-stage gain)
- **Very high output resistance**
- Gate-drain capacitance of M1 **not exposed to Miller effect** (source of M2 has low impedance)

---

### Cascade Stages (Two CS in Series)

| Property | Value |
|----------|-------|
| Stage 1 gain | $A_1 = -g_{m1}r_{ds1}$ |
| Stage 2 gain | $A_2 = -g_{m2}r_{ds2}$ |
| Total gain | $A_v = A_1 A_2 = g_{m1}r_{ds1}g_{m2}r_{ds2}$ |
| Output resistance | $r_o = r_{ds2}$ |

**Comparison with Cascode:**
- Same gain magnitude but **opposite sign**
- **Lower output impedance** than cascode

---

## Frequency Response Fundamentals

### Single Pole (Low-Pass RC)

$$H(s) = \frac{1}{1 + s/\omega_0}, \quad \omega_0 = \frac{1}{RC}$$

| Frequency | Magnitude | Phase |
|-----------|-----------|-------|
| $\omega \ll \omega_0$ | $|H| \approx 1$ (0 dB) | $\angle H \approx 0°$ |
| $\omega = \omega_0$ | $|H| = 1/\sqrt{2}$ (-3 dB) | $\angle H = -45°$ |
| $\omega \gg \omega_0$ | $|H| \approx \omega_0/\omega$ (-20 dB/decade) | $\angle H \approx -90°$ |

---

### Single Pole with Zero (High-Pass CR)

$$H(s) = \frac{s/\omega_0}{1 + s/\omega_0}, \quad \omega_0 = \frac{1}{RC}$$

| Frequency | Magnitude | Phase |
|-----------|-----------|-------|
| $\omega \ll \omega_0$ | $|H| \approx \omega/\omega_0$ (+20 dB/decade) | $\angle H \approx +90°$ |
| $\omega = \omega_0$ | $|H| = 1/\sqrt{2}$ (-3 dB) | $\angle H = +45°$ |
| $\omega \gg \omega_0$ | $|H| \approx 1$ (0 dB) | $\angle H \approx 0°$ |

---

### General Transfer Function

For circuits with multiple poles and zeros:

$$H(s) = A_0 \frac{\prod_n(1 + s/\omega_{z,n})}{\prod_k(1 + s/\omega_{p,k})}$$

**Magnitude:** $|H(\omega)| = A_0 \frac{\prod_n\sqrt{1 + (\omega/\omega_{z,n})^2}}{\prod_k\sqrt{1 + (\omega/\omega_{p,k})^2}}$

**Phase:** $\angle H(\omega) = \sum_n \arctan(\omega/\omega_{z,n}) - \sum_k \arctan(\omega/\omega_{p,k})$

---

## Feedback Systems

### Basic Feedback Equations

$$A_{CL}(s) = \frac{A(s)}{1 + \beta(s)A(s)}$$

$$L(s) = \beta(s)A(s) \quad \text{(Loop Gain)}$$

**Key properties:**
- For low frequencies (high $A$): $A_{CL} \approx 1/\beta$
- For high frequencies (low $A$): $A_{CL} \approx A$

---

### First-Order System with Feedback

For an amplifier with a single dominant pole:

$$A(s) = \frac{A_0}{1 + s/\omega_{p1}}$$

**Open-loop GBW:** $\text{GBW}_A = A_0 \cdot \omega_{p1} = \omega_{ta}$

**Closed-loop:**
- Gain: $A_{CL,0} = \frac{A_0}{1 + \beta A_0} \approx \frac{1}{\beta}$
- Bandwidth: $\omega_{CL} = \omega_{p1}(1 + \beta A_0) \approx \beta \cdot \omega_{ta}$
- **GBW is conserved:** $\text{GBW}_{CL} = A_{CL,0} \cdot \omega_{CL} = \omega_{ta}$

---

### Second-Order System and Stability

For a second-order system, the closed-loop transfer function can be written as:

$$A_{CL}(s) = \frac{A_{CL,0}}{1 + s\frac{1}{Q\omega_0} + \frac{s^2}{\omega_0^2}}$$

Where:
- $\omega_0 = \sqrt{(1+L_0)\omega_{p1}\omega_{p2}}$ is the natural frequency
- $Q = \frac{\omega_0}{\omega_{p1} + \omega_{p2}}$ is the quality factor

**Stability criteria:**
- Peaking in frequency response occurs if $Q > \frac{\sqrt{2}}{2} \approx 0.707$
- Ringing in step response occurs if $Q > \frac{1}{2}$

---

### Phase Margin

**Definition:** $PM = 180° + \angle L(j\omega_t)$ where $|L(j\omega_t)| = 1$

| Phase Margin | Q | Behavior |
|--------------|---|----------|
| 90° | 0.5 | No peaking, no ringing |
| 76° | 0.707 | Onset of peaking |
| 60° | 1 | Moderate peaking/ringing |
| 45° | 1.4 | Significant peaking/ringing |

> [!tip] Design Target
> For good stability, aim for **PM ≥ 60°** (Q ≤ 1).

---

## The Two-Stage OpAmp

This is the OpAmp you will design in the computer exercise.

### Structure

1. **First stage:** Differential pair with current mirror load
2. **Second stage:** Common source amplifier
3. **Compensation:** Miller capacitor $C_C$ (with optional $R_C$)

### Transfer Function

$$A(s) = \frac{A_0(1 - s/\omega_z)}{(1 + s/\omega_{p1})(1 + s/\omega_{p2})}$$

### Miller Effect

A capacitor $C$ across a gain stage with gain $-A$ appears as:
- **At input:** $C_1 = (1+A)C$ (Miller multiplication)
- **At output:** $C_2 = (1 + 1/A)C \approx C$

This is used to control the dominant pole in opamps - a small compensation capacitor $C_C$ appears as a much larger capacitance at the first stage output.

---

## Summary: Key Formulas

> [!abstract] Essential Equations to Remember
>
> | Quantity | Formula |
> |----------|---------|
> | Saturation current | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2$ |
> | Transconductance | $g_m = \frac{2I_D}{V_{eff}} = \sqrt{2\mu C_{ox}\frac{W}{L}I_D}$ |
> | Output resistance | $r_{ds} = \frac{V_A}{I_D} = \frac{1}{\lambda I_D}$ |
> | Intrinsic gain | $A_i = g_m r_{ds} = \frac{2V_A}{V_{eff}}$ |
> | CS gain | $A_v = -g_m(r_{ds} \parallel R_L)$ |
> | Cascode gain | $A_v = -g_{m1}r_{ds1}g_{m2}r_{ds2}$ |
> | Cascode $r_{out}$ | $r_o = r_{ds1}g_{m2}r_{ds2}$ |
> | Pole frequency | $\omega_p = \frac{1}{RC}$ |
> | Closed-loop gain | $A_{CL} = \frac{A}{1+\beta A} \approx \frac{1}{\beta}$ |
> | Phase margin | $PM = 180° + \angle L(\omega_t)$ |

---

## IC Design Flow

```
Theory (Hand calculations)          Simulations (Cadence)
        ↓                                    ↓
Understanding of circuit            Accurate frequency response
        ↓                                    ↓
Initial W/L estimates         →     Optimized W/L values
        ↓                                    ↓
        ←──── Iterate until specs met ────→
```

**This course:** Theory + Simulations in Cadence
**Next course (34656):** Layout, DRC, LVS, Parasitic extraction, Fabrication

---

> [!nav]
> &nbsp;
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Lecture 2 - Advanced OpAmps|Lecture 2 →]]
