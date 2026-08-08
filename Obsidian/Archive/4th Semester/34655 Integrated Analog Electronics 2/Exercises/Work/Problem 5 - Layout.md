---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, layout, fabrication, junction-capacitance, multi-finger]
---
# Problem 5 - Layout

> [!info] Exercise Files
> - Problems: [[31632-problems-layout.pdf]]
> - Related notes: [[Lecture 5 - Fabrication and Layout]]

## Overview

This exercise set covers IC layout interpretation and circuit analysis:
1. **Problem 1** — CMOS inverting amplifier: extract dimensions from layout, bias point, small-signal analysis, frequency response
2. **Problem 2** — CMOS logic gate: identify schematic from layout, junction area/perimeter
3. **Problem 3** — CS amplifier with biasing: map layout to schematic, extract dimensions, bias current, gain, process variations

---

## Problem 1: CMOS Inverting Amplifier Stage

> [!abstract] Given Parameters
> - $\mu_n C_{ox}(W/L)_n = \mu_p C_{ox}(W/L)_p = 300\;\mu\text{A/V}^2$
> - $V_{tn} = -V_{tp} = 0.7$ V
> - $|V_A| = 10$ V (Early voltage) for both NMOS and PMOS
> - $V_{DD} = 1.5$ V, $-V_{SS} = -1.5$ V
> - $\lambda = 0.35\;\mu\text{m}$

The circuit (Fig. 1) is a CMOS inverter: $Q_1$ (NMOS, source to $-V_{SS}$) and $Q_2$ (PMOS, source to $V_{DD}$), both gates connected to $v_I$, both drains to $v_O$.

---

### Question 1.1: Channel Length and Width from Layout

From the layout (Fig. 2), the **polysilicon gate** crosses the active region with width $2\lambda$:

$$L = 2\lambda = 2 \times 0.35 = \boxed{0.70\;\mu\text{m}} \quad \text{(both transistors)}$$

Reading the active region heights from the layout:

| Transistor | Type | Active Width | $W$ | $W/L$ |
|-----------|------|-------------|-----|-------|
| $Q_1$ (NMOS) | n-diffusion | $4\lambda$ | $1.4\;\mu\text{m}$ | 2 |
| $Q_2$ (PMOS) | p-diffusion | $8\lambda$ | $2.8\;\mu\text{m}$ | 4 |

> [!tip] Why is PMOS wider?
> Since hole mobility $\mu_p < \mu_n$ (typically $\mu_n \approx 2\mu_p$), the PMOS transistor needs a **larger $W/L$ ratio** to achieve the same $\mu C_{ox}(W/L)$ product as the NMOS. With $(W/L)_p = 2 \times (W/L)_n$, we get $\mu_p C_{ox} \times 4 = \mu_n C_{ox} \times 2 = 300\;\mu\text{A/V}^2$, confirming $\mu_n/\mu_p = 2$.

---

### Question 1.2: Quiescent Current

With $V_{IN} = 0$ V and $V_{OUT} = 0$ V:

**NMOS** $Q_1$: $V_{GS1} = V_{IN} - (-V_{SS}) = 0 + 1.5 = 1.5$ V
**PMOS** $Q_2$: $V_{SG2} = V_{DD} - V_{IN} = 1.5 - 0 = 1.5$ V

Both overdrive voltages:

$$V_{eff} = V_{GS} - V_t = 1.5 - 0.7 = 0.8\;\text{V}$$

Check saturation: $V_{DS1} = 1.5$ V $> V_{eff} = 0.8$ V $\checkmark$, $V_{SD2} = 1.5$ V $> 0.8$ V $\checkmark$

$$I_Q = \frac{1}{2}\mu C_{ox}\frac{W}{L}V_{eff}^2 = \frac{1}{2} \times 300 \times 10^{-6} \times (0.8)^2$$

$$\boxed{I_Q = 96\;\mu\text{A}}$$

Both transistors carry the same current (by symmetry: identical $\mu C_{ox}(W/L)$ and $|V_{eff}|$).

---

### Question 1.3: Small-Signal Model

Both transistors are in saturation. The small-signal equivalent has:
- $v_{gs1} = v_i$ (NMOS gate to input, source to AC ground $-V_{SS}$)
- $v_{sg2} = -v_i$ (PMOS: $v_{gs2} = v_i$, gate to input, source to AC ground $V_{DD}$)

**Transconductance:**

$$g_{m1} = g_{m2} = \frac{2I_D}{V_{eff}} = \frac{2 \times 96\;\mu\text{A}}{0.8\;\text{V}} = \boxed{240\;\mu\text{A/V}}$$

**Output resistance:**

$$r_{ds1} = r_{ds2} = \frac{|V_A|}{I_D} = \frac{10}{96 \times 10^{-6}} = \boxed{104.2\;\text{k}\Omega}$$

---

### Question 1.4: Voltage Gain, Input and Output Resistance

**Open-circuit voltage gain** (both transistors amplify — currents add at output):

$$A_v = -(g_{m1} + g_{m2})(r_{ds1} \| r_{ds2})$$

$$= -(240 + 240) \times 10^{-6} \times \frac{104.2 \times 10^3}{2}$$

$$\boxed{A_v = -480 \times 10^{-6} \times 52.1 \times 10^3 = -25.0\;\text{V/V} \approx 28\;\text{dB}}$$

**Input resistance** (MOSFET gates):

$$\boxed{R_{in} = \infty}$$

**Output resistance:**

$$\boxed{R_{out} = r_{ds1} \| r_{ds2} = 52.1\;\text{k}\Omega}$$

---

### Question 1.5: 3-dB Frequency

Given: $R_s = 100\;\text{k}\Omega$, $C_P = 5\;\text{pF}$ (between input and output).

The capacitor $C_P$ is subject to the **Miller effect**. At the input it appears multiplied by $(1 + |A_v|)$:

$$C_M = C_P(1 + |A_v|) = 5 \times (1 + 25) = 130\;\text{pF}$$

The dominant pole is set by $R_s$ and $C_M$:

$$f_{3\text{dB}} = \frac{1}{2\pi R_s C_M} = \frac{1}{2\pi \times 100 \times 10^3 \times 130 \times 10^{-12}}$$

$$\boxed{f_{3\text{dB}} = 12.2\;\text{kHz}}$$

> [!note] Hint from Problem
> If Q1.4 was not solved, the problem suggests using $A_v = 23$ dB $\approx 14.1$ V/V, which gives $C_M = 5 \times 15.1 = 75.5$ pF and $f_{3\text{dB}} = 21.1$ kHz.

---

## Problem 2: CMOS Logic Gate from Layout

> [!abstract] Problem Statement
> Find the transistor schematic for the CMOS logic circuit realized by the layout in Fig. P2. Give the widths of all transistors. Assume $L = 2\lambda$, where $\lambda = 0.4\;\mu\text{m}$. In tabular form, give the area and perimeter of each junction that is not connected to $V_{DD}$ or ground.

### Layout Interpretation

From Fig. P2:
- $L = 2\lambda = 0.8\;\mu\text{m}$ for all transistors
- **PMOS** (top, in N-well): active region height = $8\lambda = 3.2\;\mu\text{m}$
- **NMOS** (bottom): active region height = $6\lambda = 2.4\;\mu\text{m}$
- Three polysilicon gates labeled **A**, **B**, **C** run vertically across both active regions

| Transistor | Type | Width |
|-----------|------|-------|
| $P_A, P_B, P_C$ (PMOS) | p-channel | $W_p = 8\lambda = 3.2\;\mu\text{m}$ |
| $N_A, N_B, N_C$ (NMOS) | n-channel | $W_n = 6\lambda = 2.4\;\mu\text{m}$ |

### Schematic Identification

From the metal connections in the layout:
- **PMOS transistors** are connected in **parallel** between $V_{DD}$ and $Out$
- **NMOS transistors** are connected in **series** between $Out$ and $Gnd$

This is a **3-input NAND gate**: $Out = \overline{A \cdot B \cdot C}$

```
        VDD
      ┌──┤──┐──┐
      PA  PB  PC    (parallel PMOS)
      └──┬──┘──┘
         Out
      ┌──┘
      NA               (series NMOS)
      ├──┘
      NB
      ├──┘
      NC
      └── Gnd
```

### Junction Area and Perimeter

For junctions **not** connected to $V_{DD}$ or $Gnd$ (i.e., the internal nodes and the output node):

The output node connects to the shared drain of all three PMOS transistors and the drain of the top NMOS ($N_A$). The internal series nodes of the NMOS chain also have junctions.

For a junction with diffusion width $W$ and extension $d = 6\lambda$ from gate edge (typical minimum):

| Junction | Type | Area $A$ | Perimeter $P$ (excl. gate edge) |
|----------|------|----------|------|
| PMOS shared drain (Out) | p+ in N-well | $A = 6\lambda \times 8\lambda = 48\lambda^2$ | $P = 2 \times 6\lambda + 8\lambda = 20\lambda$ |
| NMOS $N_A$ drain (Out) | n+ in P-sub | $A = 6\lambda \times 6\lambda = 36\lambda^2$ | $P = 2 \times 6\lambda + 6\lambda = 18\lambda$ |
| NMOS $N_A$–$N_B$ junction | n+ in P-sub | $A = 6\lambda \times 6\lambda = 36\lambda^2$ | $P = 2 \times 6\lambda + 6\lambda = 18\lambda$ |
| NMOS $N_B$–$N_C$ junction | n+ in P-sub | $A = 6\lambda \times 6\lambda = 36\lambda^2$ | $P = 2 \times 6\lambda + 6\lambda = 18\lambda$ |

> [!note] Perimeter Convention
> Junction perimeter excludes the edge that borders the gate (channel), as that side does not contribute to sidewall capacitance.

With $\lambda = 0.4\;\mu\text{m}$: $\lambda^2 = 0.16\;\mu\text{m}^2$

---

## Problem 3: CS Amplifier with Biasing

> [!abstract] Setup
> A common source amplifier with biasing is shown in layout (Fig. 1) and schematic (Fig. 2).
> - Process: $2\lambda = 0.25\;\mu\text{m}$ ($\lambda = 0.125\;\mu\text{m}$)
> - $Q_3$ (PMOS, diode-connected) + $R$ generate bias current $I_B = I_R = I_{D3}$
> - $Q_1$ (NMOS) + $Q_2$ (PMOS) form the amplifier
> - Capacitor $C$ (not in layout) ensures noise from $R$/$Q_3$ doesn't reach output
> - Bulk connected to source for all transistors

### Fallback Parameters (if Q3.2 not answered)

| Parameter | Value |
|-----------|-------|
| $(W/L)_1$ (NMOS) | $3\;\mu\text{m}\;/\;0.5\;\mu\text{m} = 6$ |
| $(W/L)_2$ (PMOS) | $8\;\mu\text{m}\;/\;1\;\mu\text{m} = 8$ |
| $(W/L)_3$ (PMOS) | $4\;\mu\text{m}\;/\;1\;\mu\text{m} = 4$ |
| $R$ | $50\;\text{k}\Omega$ |

### Process Parameters (Table 1)

| Component | Parameter | Unit | Slow | Typical | Fast |
|-----------|-----------|------|------|---------|------|
| **NMOS** | $V_{tn}$ | V | 0.7 | 0.6 | 0.5 |
| | $\mu_n C_{ox}$ | $\mu$A/V² | 80 | 100 | 120 |
| | $V_A$ | V | 12 | 15 | 18 |
| **PMOS** | $\|V_{tp}\|$ | V | 0.9 | 0.8 | 0.7 |
| | $\mu_p C_{ox}$ | $\mu$A/V² | 40 | 50 | 60 |
| | $\|V_A\|$ | V | 12 | 15 | 18 |
| **POLY Res** | $R_\square$ | kΩ/□ | 2.5 | 2 | 1.5 |

> [!note] Process Corners
> Components of the **same type** track together (all NMOS share one corner, all PMOS share one corner), but **different types** are independent. Each corner is a set $\{V_t, \mu C_{ox}, V_A\}$.

---

### Question 3.1: Layout-to-Schematic Mapping

From the layout (Fig. 1):
- **Top row** ($G_A$–$G_F$): 6 PMOS gate fingers in the N-WELL region
- **Bottom** ($G_G$, $G_H$): 2 NMOS gate fingers connected to $V_{IN}$
- **Poly resistor**: long poly strip with "Resistor implant region" at bottom-left

The NMOS transistors ($G_G$, $G_H$) have their gate connected to $V_{IN}$ → these are **$Q_1$**.

The PMOS transistors form $Q_2$ (load) and $Q_3$ (bias reference). For a matched current mirror, they are laid out in **common centroid** pattern:

| Layout Gate | Schematic Transistor | Role |
|------------|---------------------|------|
| $G_A$, $G_D$, $G_E$ | **$Q_2$** (3 fingers) | PMOS current mirror output (load) |
| $G_B$, $G_C$, $G_F$ | **$Q_3$** (3 fingers) | PMOS diode-connected (bias reference) |
| $G_G$, $G_H$ | **$Q_1$** (2 fingers) | NMOS amplifier |

> [!tip] Common Centroid
> $Q_2$ and $Q_3$ are interleaved ($Q_2$-$Q_3$-$Q_3$-$Q_2$-$Q_2$-$Q_3$ or similar) so that any linear process gradient affects both equally — critical for current mirror matching.

---

### Question 3.2: Transistor Dimensions and Resistor Value

From the layout with $2\lambda = 0.25\;\mu\text{m}$, reading the gate widths (poly crossing active) and active region widths:

| Device | Fingers | $W$ per finger | $W_\text{eff}$ | $L$ | $W/L$ |
|--------|---------|---------------|----------------|-----|-------|
| $Q_1$ (NMOS) | 2 | $1.5\;\mu\text{m}$ | $3\;\mu\text{m}$ | $0.5\;\mu\text{m}$ | 6 |
| $Q_2$ (PMOS) | 3 | $\approx 2.67\;\mu\text{m}$ | $8\;\mu\text{m}$ | $1\;\mu\text{m}$ | 8 |
| $Q_3$ (PMOS) | 3 | $\approx 1.33\;\mu\text{m}$ | $4\;\mu\text{m}$ | $1\;\mu\text{m}$ | 4 |

**Resistor** (poly with resistor implant region):
- Length $L_R = 25\lambda$, Width $W_R = 1\lambda$ (from layout dimension markers)

$$R = R_\square \times \frac{L_R}{W_R} = 2\;\text{k}\Omega/\square \times 25 = \boxed{50\;\text{k}\Omega}$$

---

### Question 3.3: Typical Bias Current in $Q_3$

Using typical parameters: $\mu_p C_{ox} = 50\;\mu\text{A/V}^2$, $|V_{tp}| = 0.8$ V, $V_{DD} = 2$ V, $R = 50\;\text{k}\Omega$.

$Q_3$ is diode-connected PMOS: $V_{SG3} = V_{SD3}$. KVL from $V_{DD}$ through $R$ to $Q_3$:

$$I_R = I_{D3} = \frac{V_{DD} - V_{SG3}}{R}$$

$$I_{D3} = \frac{1}{2}\mu_p C_{ox}\left(\frac{W}{L}\right)_3(V_{SG3} - |V_{tp}|)^2$$

Let $x = V_{SG3} - |V_{tp}| = V_{SG3} - 0.8$, so $V_{SG3} = x + 0.8$:

$$\frac{2 - (x + 0.8)}{50\text{k}} = \frac{1}{2} \times 50\mu \times 4 \times x^2$$

$$\frac{1.2 - x}{50\text{k}} = 100\mu \times x^2$$

$$1.2 - x = 5x^2$$

$$5x^2 + x - 1.2 = 0$$

$$x = \frac{-1 + \sqrt{1 + 24}}{10} = \frac{-1 + 5}{10} = 0.4\;\text{V}$$

Therefore: $V_{SG3} = 0.4 + 0.8 = 1.2$ V

$$\boxed{I_{D3} = \frac{1}{2} \times 50\mu \times 4 \times 0.4^2 = 16\;\mu\text{A}}$$

**Verify:** $I_R = (2 - 1.2)/50\text{k} = 0.8/50\text{k} = 16\;\mu\text{A}$ $\checkmark$

---

### Question 3.4: Input DC Voltage for $V_{OUT} = V_{DD}/2$

The current mirror ratio: $(W/L)_2 / (W/L)_3 = 8/4 = 2$

$$I_{D2} = 2 \times I_{D3} = 2 \times 16 = 32\;\mu\text{A}$$

At DC, capacitor $C$ is open, so $V_{G2} = V_{G3} = V_{DD} - V_{SG3} = 2 - 1.2 = 0.8$ V.

KCL at output: $I_{D1} = I_{D2} = 32\;\mu\text{A}$

For $Q_1$ (NMOS) with typical parameters ($\mu_n C_{ox} = 100\;\mu\text{A/V}^2$, $V_{tn} = 0.6$ V):

$$I_{D1} = \frac{1}{2}\mu_n C_{ox}\left(\frac{W}{L}\right)_1(V_{IN} - V_{tn})^2$$

$$32\mu = \frac{1}{2} \times 100\mu \times 6 \times (V_{IN} - 0.6)^2$$

$$(V_{IN} - 0.6)^2 = \frac{32}{300} = 0.1067$$

$$V_{IN} - 0.6 = 0.327\;\text{V}$$

$$\boxed{V_{IN} = 0.93\;\text{V}}$$

Check saturation: $V_{DS1} = V_{OUT} = 1.0$ V $> V_{eff1} = 0.33$ V $\checkmark$
$V_{SD2} = V_{DD} - V_{OUT} = 1.0$ V $> V_{eff2} = 0.4$ V $\checkmark$

---

### Question 3.5: Output Amplitude for 1 mV AC Input

Small-signal parameters (using $V_{IN} = 0.92$ V as given fallback):

$$V_{eff1} = V_{IN} - V_{tn} = 0.92 - 0.6 = 0.32\;\text{V}$$

$$g_{m1} = \frac{2I_{D1}}{V_{eff1}} = \frac{2 \times 32\;\mu\text{A}}{0.32\;\text{V}} = 200\;\mu\text{A/V}$$

$$r_{ds1} = \frac{V_{A,n}}{I_{D1}} = \frac{15}{32\;\mu} = 468.8\;\text{k}\Omega$$

$$r_{ds2} = \frac{|V_{A,p}|}{I_{D2}} = \frac{15}{32\;\mu} = 468.8\;\text{k}\Omega$$

**Voltage gain** (capacitor $C$ makes $v_{gs2} = 0$ at signal frequencies, so $Q_2$ acts as a current source — only $Q_1$ amplifies):

$$A_v = -g_{m1}(r_{ds1} \| r_{ds2}) = -200\;\mu \times 234.4\;\text{k} = -46.9\;\text{V/V}$$

**Output amplitude:**

$$\boxed{v_{out} = |A_v| \times v_{in} = 46.9 \times 1\;\text{mV} = 46.9\;\text{mV}}$$

> [!note] Role of Capacitor $C$
> $C$ is AC-coupled between the gates of $Q_2$ and $Q_3$. At signal frequencies, $C$ shorts the gate of $Q_2$ to AC ground (since $Q_3$'s diode connection has low impedance $\approx 1/g_{m3}$). This means $Q_2$ acts as a pure current source — it does not amplify the signal, only $Q_1$ does.

---

### Question 3.6: Process Variation — Min/Max Bias Current

The bias current $I_{D3}$ depends on the PMOS corner and the resistor corner. Since PMOS and POLY resistor are **independent** types, all combinations must be considered.

#### Maximum Bias Current (Fast PMOS + Fast Resistor)

Parameters: $\mu_p C_{ox} = 60\;\mu\text{A/V}^2$, $|V_{tp}| = 0.7$ V, $R_\square = 1.5\;\text{k}\Omega/\square$

$$R = 50\text{k} \times \frac{1.5}{2} = 37.5\;\text{k}\Omega$$

$$\frac{1.3 - x}{37.5\text{k}} = \frac{1}{2} \times 60\mu \times 4 \times x^2 = 120\mu \cdot x^2$$

$$1.3 - x = 4.5x^2 \quad \Rightarrow \quad 4.5x^2 + x - 1.3 = 0$$

$$x = \frac{-1 + \sqrt{1 + 23.4}}{9} = \frac{-1 + 4.94}{9} = 0.438\;\text{V}$$

$$\boxed{I_{D3,\max} = 120\mu \times 0.438^2 = 23.0\;\mu\text{A}}$$

#### Minimum Bias Current (Slow PMOS + Slow Resistor)

Parameters: $\mu_p C_{ox} = 40\;\mu\text{A/V}^2$, $|V_{tp}| = 0.9$ V, $R_\square = 2.5\;\text{k}\Omega/\square$

$$R = 50\text{k} \times \frac{2.5}{2} = 62.5\;\text{k}\Omega$$

$$\frac{1.1 - x}{62.5\text{k}} = \frac{1}{2} \times 40\mu \times 4 \times x^2 = 80\mu \cdot x^2$$

$$1.1 - x = 5x^2 \quad \Rightarrow \quad 5x^2 + x - 1.1 = 0$$

$$x = \frac{-1 + \sqrt{1 + 22}}{10} = \frac{-1 + 4.796}{10} = 0.380\;\text{V}$$

$$\boxed{I_{D3,\min} = 80\mu \times 0.380^2 = 11.5\;\mu\text{A}}$$

### Bias Current Summary

| Corner | $\mu_p C_{ox}$ | $\|V_{tp}\|$ | $R_\square$ | $R$ | $V_{eff3}$ | $I_{D3}$ |
|--------|-------------|----------|-----------|-----|---------|---------|
| **Fast** | 60 μA/V² | 0.7 V | 1.5 kΩ/□ | 37.5 kΩ | 0.438 V | **23.0 μA** |
| **Typical** | 50 μA/V² | 0.8 V | 2.0 kΩ/□ | 50 kΩ | 0.400 V | **16.0 μA** |
| **Slow** | 40 μA/V² | 0.9 V | 2.5 kΩ/□ | 62.5 kΩ | 0.380 V | **11.5 μA** |

> [!important] Key Observations
> - The bias current varies by **±44%** from typical across process corners
> - **Maximum** current comes from **fast PMOS** (low $|V_{tp}|$, high $\mu_p C_{ox}$) combined with **low $R_\square$** (fast resistor → smaller $R$)
> - **Minimum** current comes from **slow PMOS** (high $|V_{tp}|$, low $\mu_p C_{ox}$) combined with **high $R_\square$** (slow resistor → larger $R$)
> - The resistor helps reduce variation: without $R$, the current would depend only on PMOS parameters. With $R$, the voltage drop across the resistor provides negative feedback that partially stabilizes the current

---

## Formulas Reference

| Quantity | Formula |
|----------|---------|
| Sheet resistance | $R = R_\square \cdot L/W$ |
| Capacitance | $C = C_\square \cdot L \cdot W$ |
| MOSFET saturation current | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS} - V_t)^2$ |
| Transconductance | $g_m = 2I_D / V_{eff}$ |
| Output resistance | $r_{ds} = V_A / I_D$ |
| CS stage gain | $A_v = -g_m(r_{ds1} \| r_{ds2})$ |
| Miller capacitance | $C_M = C_P(1 + |A_v|)$ |
| Junction area (single) | $A = d \times W$ where $d$ is diffusion extension |
| Junction perimeter | $P = 2d + W$ (excluding gate edge) |

---

> [!nav]
> [[Problem 4 - Noise|← Problem 4]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
