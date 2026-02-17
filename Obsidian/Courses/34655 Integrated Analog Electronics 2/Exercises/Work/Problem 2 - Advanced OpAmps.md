---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise]
---
# Problem 2 - Advanced OpAmps

> [!info] Exercise Files
> - Problems: [[31632-problems-avd-opamp.pdf]]
> - Related notes: [[Advanced OpAmps - Lecture Notes]]

## Overview

This exercise set covers:
1. **Wide-swing current mirror** - Input impedance analysis
2. **Enhanced output impedance current mirror** - Output impedance with amplifier feedback
3. **OTA with capacitive load** - Output impedance and dominant pole
4. **Feedback amplifier design** - Using folded cascode and current mirror OTAs

---

## Problem 1: Wide-Swing Current Mirror

> [!abstract] Context
> One important property of the folded cascode OTA is that all internal nodes have low impedance and the dominant pole occurs at the output (the only high impedance node). For this to be true, the input impedance of the wide-swing current mirror must be low.
>
> See: [[Advanced OpAmps - Lecture Notes#4.2 Wide-Swing Cascode Current Mirror]]

### Circuit

![[figure 1.png|400]]

---

### Question 1.1: Input Impedance

> [!question] Show that the input impedance of the wide-swing current mirror is low and approximately $1/g_{m1}$.

#### Small Signal Analysis

To find the input impedance, we apply a test voltage $v_x$ at the input node and calculate the resulting current $i_x$.

> [!note] Key Insight
> The gate of M1 is connected to its drain (diode-connected), so $v_{gs1} = v_x$.

**For the diode-connected transistor M1:**

The small-signal current through M1 is:
$$i_{ds1} = g_{m1}v_{gs1} + g_{ds1}v_{ds1}$$

Since $v_{gs1} = v_{ds1} = v_x$ (diode-connected):
$$i_{ds1} = g_{m1}v_x + g_{ds1}v_x = (g_{m1} + g_{ds1})v_x$$

**For the cascode transistor M2:**

M2 is in common-gate configuration. Its gate is at AC ground (fixed bias $V_B$).

The source of M2 sees the drain of M1, and since M2 acts as a current buffer, most of the input current flows through this path.

**Total input impedance:**

Looking into the input node, we see:
- The impedance looking into M1: $\frac{1}{g_{m1} + g_{ds1}}$
- This is in parallel with the impedance looking into the source of M2

For M2 in common-gate, the impedance looking into the source is approximately $\frac{1}{g_{m2}}$ (when loaded by a high impedance).

The parallel combination is dominated by the smaller impedance:

$$r_{in} = \frac{1}{g_{m1} + g_{ds1}} \parallel \frac{1}{g_{m2}}$$

> [!success] Result
> Using the approximation $g_m \gg g_{ds}$ (equivalently $g_m r_{ds} \gg 1$):
> $$r_{in} \approx \frac{1}{g_{m1}} \parallel \frac{1}{g_{m2}} \approx \frac{1}{g_{m1}}$$
>
> assuming $g_{m1} \approx g_{m2}$.
>
> **The input impedance is low**, approximately $\boxed{r_{in} \approx \frac{1}{g_{m1}}}$

> [!tip] Physical Interpretation
> The low input impedance is due to the diode-connected M1. In a diode-connected MOSFET, the negative feedback from drain to gate linearizes the device and creates a low impedance of $1/g_m$.

---

### Question 1.2: Bias Voltage Range for $V_B$

> [!question] Given Parameters
> - All transistors M1-M4 have the same size
> - $V_{eff} = 200$ mV for all transistors
> - $V_t = 0.5$ V
>
> Find the minimum and maximum gate voltage $V_B$ for M2 and M4 that ensures all transistors remain saturated.

#### Saturation Conditions

For a MOSFET to be saturated: $V_{DS} \geq V_{eff}$ (i.e., $V_{DS} \geq V_{GS} - V_t$)
 
#### Analyzing the Input Side (M1 and M2)

**Voltage at node between M1 and M2:**

The drain of M1 (source of M2) is at voltage:
$$V_{D1} = V_{GS1} = V_t + V_{eff} = 0.5 + 0.2 = 0.7\ \text{V}$$

**For M1 to be saturated:**
$$V_{DS1} \geq V_{eff1}$$
$$V_{D1} - 0 \geq V_{eff}$$
$$0.7\ \text{V} \geq 0.2\ \text{V} \quad \checkmark \text{ (always satisfied)}$$

**For M2 to be saturated:**
$$V_{DS2} \geq V_{eff2}$$
$$V_{D2} - V_{D1} \geq V_{eff}$$

The drain of M2 connects to the input current source. For M2:
$$V_{GS2} = V_B - V_{D1} = V_B - 0.7\ \text{V}$$

For M2 to be ON: $V_{GS2} \geq V_t + V_{eff} = 0.7$ V
$$V_B - 0.7 \geq 0.7 \Rightarrow V_B \geq 1.4\ \text{V}$$

> [!success] Minimum $V_B$
> $$V_{B,min} = V_{GS1} + V_{GS2} = 2(V_t + V_{eff}) = 2 \times 0.7 = \boxed{1.4\ \text{V}}$$

#### Analyzing the Output Side (M3 and M4)

**For M3 to be saturated:**
$$V_{DS3} \geq V_{eff3}$$

The source of M3 is at ground, so:
$$V_{D3} \geq V_{eff} = 0.2\ \text{V}$$

The drain of M3 is the source of M4:
$$V_{S4} = V_{D3}$$

**For M4 to be saturated:**
$$V_{DS4} \geq V_{eff4}$$
$$V_{D4} - V_{S4} \geq V_{eff}$$

**Finding the constraint on $V_B$:**

For M3: $V_{GS3} = V_t + V_{eff} = 0.7$ V (same bias as M1)

The gate of M3 is at $V_{GS1} = 0.7$ V, so:
$$V_{D3} = V_{G3} - V_{GS3} + V_{DS3} = 0.7 - 0.7 + V_{DS3} = V_{DS3}$$

For M3 just at the edge of saturation: $V_{D3} = V_{eff} = 0.2$ V

For M4: $V_{GS4} = V_B - V_{D3} = V_B - V_{DS3}$

At minimum $V_{DS3} = V_{eff} = 0.2$ V:
$$V_{GS4} = V_B - 0.2$$

For M4 to have $V_{DS4} \geq V_{eff}$, the output voltage must satisfy:
$$V_{out} \geq V_{D3} + V_{eff} = V_{eff} + V_{eff} = 2V_{eff} = 0.4\ \text{V}$$

**Maximum $V_B$ constraint:**

The maximum $V_B$ is limited by M2 staying in saturation on the input side. The drain of M2 must be high enough:
$$V_{D2} \geq V_{GS2} - V_t + V_{D1} = V_{eff2} + V_{D1}$$

This depends on the current source compliance. However, for the current mirror to work properly with all same-sized transistors:

> [!success] Maximum $V_B$
> For the wide-swing configuration with equal transistor sizes, to ensure M3 stays in saturation:
> $$V_{GS4} = V_t + V_{eff} = 0.7\ \text{V}$$
> $$V_B = V_{GS4} + V_{DS3,min} = 0.7 + 0.2 = 0.9\ \text{V}$$
>
> But this conflicts with the minimum requirement. For equal-sized transistors in a **standard** wide-swing mirror, we need $V_{eff5} = 2V_{eff}$ (from the design equations in lecture).
>
> **For the given equal-sized configuration:**
> $$V_{B,min} = V_t + 2V_{eff} = 0.5 + 0.4 = \boxed{0.9\ \text{V}}$$
> $$V_{B,max} = 2V_t + 2V_{eff} = 1.0 + 0.4 = \boxed{1.4\ \text{V}}$$

> [!warning] Note
> In practice, for a proper wide-swing cascode with equal $V_{eff}$ on all transistors, the bias transistor needs $(W/L)_{bias} = (W/L)_{mirror}/4$ to achieve $V_{eff,bias} = 2V_{eff}$. With all transistors the same size as given here, the operating range is more constrained.

---

## Problem 2: Enhanced Output Impedance Current Mirror

> See: [[Advanced OpAmps - Lecture Notes#4.3 Self-Regulating Current Mirror (Enhanced Output Impedance)]]

### Circuit

![[figure 2.png|350]]

---

### Question 2.1: Output Impedance

> [!question] Find the output impedance and show that it can be approximated by:
> $$r_{out} \approx A \cdot g_{m2} \cdot r_{ds1} \cdot r_{ds2}$$
> assuming $A \gg 1$

#### Analysis

The enhanced current mirror uses an amplifier with gain $-A$ to regulate the drain voltage of M1.

**Feedback mechanism:**
- If $V_{out}$ increases, the source of M2 (drain of M1) tries to increase
- The amplifier senses this and decreases its output
- This reduces $V_{GS2}$, reducing the current through M2
- The negative feedback stabilizes the operating point and increases output impedance

**Small-signal analysis:**

Apply a test voltage $v_x$ at the output and find current $i_x$.

Let $v_s$ be the voltage at the source of M2 (drain of M1).

**For M2 (cascode transistor):**
$$i_x = g_{m2}v_{gs2} + \frac{v_x - v_s}{r_{ds2}}$$

The gate voltage of M2 is controlled by the amplifier:
$$v_{g2} = -A \cdot v_s$$

So:
$$v_{gs2} = v_{g2} - v_s = -Av_s - v_s = -(1+A)v_s$$

**For M1 (input transistor):**

M1 has its gate at AC ground ($V_{B1}$ is a DC bias), so $v_{gs1} = 0$.
$$i_1 = \frac{v_s}{r_{ds1}}$$

**Current continuity:**

At the node between M1 and M2:
$$i_x = i_1 = \frac{v_s}{r_{ds1}}$$

**Substituting into M2 equation:**
$$\frac{v_s}{r_{ds1}} = g_{m2}(-(1+A)v_s) + \frac{v_x - v_s}{r_{ds2}}$$

$$\frac{v_s}{r_{ds1}} = -g_{m2}(1+A)v_s + \frac{v_x}{r_{ds2}} - \frac{v_s}{r_{ds2}}$$

$$v_s\left(\frac{1}{r_{ds1}} + \frac{1}{r_{ds2}} + g_{m2}(1+A)\right) = \frac{v_x}{r_{ds2}}$$

Since $g_{m2}(1+A) \gg \frac{1}{r_{ds1}} + \frac{1}{r_{ds2}}$ (assuming $g_m r_{ds} \gg 1$ and $A \gg 1$):

$$v_s \approx \frac{v_x}{r_{ds2} \cdot g_{m2}(1+A)} \approx \frac{v_x}{r_{ds2} \cdot g_{m2} \cdot A}$$

**Output impedance:**
$$r_{out} = \frac{v_x}{i_x} = \frac{v_x}{v_s/r_{ds1}} = \frac{v_x \cdot r_{ds1}}{v_s}$$

$$r_{out} = \frac{v_x \cdot r_{ds1}}{\frac{v_x}{r_{ds2} \cdot g_{m2} \cdot A}} = r_{ds1} \cdot r_{ds2} \cdot g_{m2} \cdot A$$

> [!success] Result
> $$\boxed{r_{out} \approx A \cdot g_{m2} \cdot r_{ds1} \cdot r_{ds2}}$$
>
> This is the standard cascode output impedance ($g_{m2} r_{ds1} r_{ds2}$) multiplied by the amplifier gain $A$.

> [!tip] Physical Interpretation
> The amplifier creates a feedback loop that actively regulates the drain of M1, making it appear as a much better current source. The enhancement factor is equal to the amplifier gain $A$.

---

## Problem 3: OTA with Capacitive Load

### Circuit

![[figure 3.png|400]]

The OTA has transconductance $G_{ma}$ and output impedance $r_{out}$.

---

### Question 3.1: Output Impedance from DC Gain

> [!question] Given Parameters
> - $G_{ma} = 5$ mA/V
> - DC gain = 50 dB
>
> Find the output impedance $r_{out}$.

#### Solution

**DC gain of an OTA:**

The voltage gain at DC (with open-circuit output or very high load impedance) is:
$$A_0 = G_{ma} \cdot r_{out}$$

**Converting dB to linear:**
$$50\ \text{dB} = 20 \log_{10}(A_0)$$
$$A_0 = 10^{50/20} = 10^{2.5} = 316.2\ \text{V/V}$$

**Solving for $r_{out}$:**
$$r_{out} = \frac{A_0}{G_{ma}} = \frac{316.2}{5 \times 10^{-3}}$$

> [!success] Result
> $$r_{out} = \frac{316.2}{0.005} = \boxed{63.25\ \text{k}\Omega}$$

---

### Question 3.2: Dominant Pole Location

> [!question] Given Parameters
> - Unity gain frequency $f_{ta} = 50$ MHz
> - Only the dominant pole matters
>
> Find the location of the dominant pole.

#### Solution

**For a single-pole system:**

The transfer function is:
$$A(s) = \frac{A_0}{1 + s/\omega_p} = \frac{G_{ma} \cdot r_{out}}{1 + s \cdot r_{out} \cdot C_L}$$

where $\omega_p = \frac{1}{r_{out} C_L}$ is the dominant pole.

**Gain-bandwidth relationship:**

For a single-pole system, the unity-gain frequency (where $|A(j\omega)| = 1$) is:
$$\omega_{ta} = A_0 \cdot \omega_p = G_{ma} \cdot r_{out} \cdot \frac{1}{r_{out} C_L} = \frac{G_{ma}}{C_L}$$

This shows that $\omega_{ta}$ is independent of $r_{out}$ - a key property!

**Finding the dominant pole:**

From $\omega_{ta} = A_0 \cdot \omega_p$:
$$\omega_p = \frac{\omega_{ta}}{A_0}$$

$$f_p = \frac{f_{ta}}{A_0} = \frac{50 \times 10^6}{316.2}$$

> [!success] Result
> $$f_p = \boxed{158.1\ \text{kHz}}$$
>
> Or in radians: $\omega_p = 2\pi \times 158.1 \times 10^3 = 993.5$ krad/s

> [!note] Verification
> We can verify: $GBW = A_0 \times f_p = 316.2 \times 158.1\ \text{kHz} = 50\ \text{MHz}$ ✓

---

## Problem 4: Feedback Amplifier Design

### Circuit

![[figure 4.png|400]]

> [!abstract] Given Parameters
> - $C_1 = 4$ pF
> - $C_2 = 2$ pF
> - The dotted resistor sets DC bias and can be ignored for AC analysis

---

### Question 4.1: Loop Gain and Effective Load Capacitance

> [!question] Find the loop gain $L(s)$ and the effective capacitive load at the output, assuming the amplifier gain is $A(s)$.

#### Breaking the Loop

We break the loop at the minus terminal of the amplifier.

![[figure 4.png|300]]

**Feedback network analysis:**

The capacitors $C_1$ and $C_2$ form a capacitive voltage divider.

When the output changes by $v_{out}$, the voltage fed back to the input is:
$$v_{fb} = v_{out} \cdot \frac{C_2}{C_1 + C_2}$$

**Feedback factor:**
$$\beta = \frac{C_2}{C_1 + C_2} = \frac{2}{4 + 2} = \frac{2}{6} = \frac{1}{3}$$

**Loop gain:**

Breaking at the inverting input and injecting a test signal:
$$L(s) = A(s) \cdot \beta = A(s) \cdot \frac{C_2}{C_1 + C_2}$$

> [!success] Loop Gain
> $$\boxed{L(s) = A(s) \cdot \frac{C_2}{C_1 + C_2} = \frac{A(s)}{3}}$$

**Effective load capacitance:**

The output sees:
- $C_2$ connected to the virtual ground (inverting input)
- Plus any additional load capacitance

Since the inverting input is a virtual ground in the feedback configuration, $C_2$ appears directly across the output.

Additionally, due to Miller effect on $C_2$, the effective capacitance at the output is:
$$C_{L,eff} = C_2 \cdot \left(1 + \frac{1}{A_{CL}}\right) \approx C_2$$

where $A_{CL}$ is the closed-loop gain.

For the OTA output node, the total capacitance is approximately:
$$C_{L,eff} = C_2 + C_1 \cdot \frac{C_2}{C_1 + C_2} = C_2\left(1 + \frac{C_1}{C_1 + C_2}\right) = \frac{C_2(C_1 + C_2) + C_1 C_2}{C_1 + C_2}$$

Actually, more precisely, looking from the OTA output:
$$C_{L,eff} = C_2 \cdot \frac{C_1}{C_1 + C_2} + C_2 = C_1 \parallel C_2 + \text{stray capacitance}$$

> [!success] Effective Load Capacitance
> For the feedback configuration with ideal OTA (infinite input impedance):
> $$\boxed{C_{L,eff} = C_1 \parallel C_2 = \frac{C_1 \cdot C_2}{C_1 + C_2} = \frac{4 \times 2}{4 + 2} = \frac{8}{6} = 1.33\ \text{pF}}$$

---

### Question 4.2: Folded Cascode OTA Current Consumption

> [!question] Given Parameters
> - Folded cascode OTA (Figure 5)
> - Input differential pair uses 80% of total current
> - $V_{eff1} = V_{eff2} = 150$ mV
> - Target: $f_{3dB} = 60$ MHz
>
> Find the total current consumption.
>
> See: [[Advanced OpAmps - Lecture Notes#7. Folded Cascode Differential Pair (OpAmp)]]

### Circuit

![[figure 5.png|500]]

#### Analysis

**Closed-loop bandwidth:**

For the feedback amplifier with loop gain $L(s) = A(s)\beta$:

The closed-loop transfer function is:
$$A_{CL}(s) = \frac{A(s)}{1 + A(s)\beta}$$

For a single-pole OTA with $A(s) = \frac{A_0}{1 + s/\omega_p}$:

$$A_{CL}(s) = \frac{A_0/(1 + s/\omega_p)}{1 + A_0\beta/(1 + s/\omega_p)} = \frac{A_0}{1 + A_0\beta + s/\omega_p}$$

The closed-loop pole is at:
$$\omega_{3dB} = \omega_p(1 + A_0\beta) \approx A_0\beta\omega_p = \beta \cdot \omega_{ta}$$

where $\omega_{ta} = A_0 \omega_p$ is the unity-gain bandwidth.

**Required unity-gain bandwidth:**
$$\omega_{ta} = \frac{\omega_{3dB}}{\beta} = \frac{2\pi \times 60 \times 10^6}{1/3} = 3 \times 2\pi \times 60 \times 10^6$$
$$f_{ta} = 3 \times 60\ \text{MHz} = 180\ \text{MHz}$$

**Transconductance requirement:**

For an OTA: $\omega_{ta} = \frac{G_m}{C_{L,eff}}$

$$G_m = \omega_{ta} \cdot C_{L,eff} = 2\pi \times 180 \times 10^6 \times 1.33 \times 10^{-12}$$
$$G_m = 1.131 \times 10^9 \times 1.33 \times 10^{-12} = 1.50\ \text{mA/V}$$

**Relating $G_m$ to bias current:**

For the differential pair: $G_m = g_{m1} = g_{m2}$

Using $g_m = \frac{2I_D}{V_{eff}}$ for each transistor in the differential pair:

Each input transistor carries $I_{D1} = I_{tail}/2$, where $I_{tail}$ is the tail current.

$$g_{m1} = \frac{2 \cdot (I_{tail}/2)}{V_{eff}} = \frac{I_{tail}}{V_{eff}}$$

Solving for tail current:
$$I_{tail} = G_m \cdot V_{eff} = 1.50 \times 10^{-3} \times 0.15 = 225\ \mu\text{A}$$

**Total current:**

The differential pair uses 80% of total current:
$$I_{tail} = 0.8 \times I_{total}$$
$$I_{total} = \frac{I_{tail}}{0.8} = \frac{225\ \mu\text{A}}{0.8}$$

> [!success] Result
> $$I_{total} = \boxed{281.25\ \mu\text{A}}$$

---

### Question 4.3: Current Mirror OTA Current Consumption

> [!question] Given Parameters
> - Current mirror amplifier (Figure 6)
> - Current scaling factor $K = 3$
> - $V_{eff} = 150$ mV for input transistors
> - Target: $f_{3dB} = 60$ MHz
>
> Find the total current consumption.
>
> See: [[Advanced OpAmps - Lecture Notes#8. Current Mirror OpAmp]]

### Circuit

![[figure 6_a.png|400]]

![[figure 6_b.png|500]]

#### Analysis

**Key difference from folded cascode:**

The current mirror OTA has an effective transconductance of:
$$G_{m,eff} = K \cdot g_{m1}$$

where $K$ is the current mirror ratio and $g_{m1}$ is the transconductance of the input transistors.

**Required transconductance:**

Same as before:
$$G_{m,eff} = 1.50\ \text{mA/V}$$

**Input stage transconductance:**
$$g_{m1} = \frac{G_{m,eff}}{K} = \frac{1.50\ \text{mA/V}}{3} = 0.5\ \text{mA/V}$$

**Tail current for differential pair:**
$$g_{m1} = \frac{I_{tail}}{V_{eff}}$$
$$I_{tail} = g_{m1} \cdot V_{eff} = 0.5 \times 10^{-3} \times 0.15 = 75\ \mu\text{A}$$

**Current in output stage:**

Each side of the differential pair carries $I_{D1} = I_{tail}/2 = 37.5\ \mu$A

After the current mirror with ratio K=3:
$$I_{out,stage} = K \cdot I_{D1} = 3 \times 37.5 = 112.5\ \mu\text{A}$$

**Total current calculation:**

Looking at Figure 6b:
- Tail current source: $I_b = I_{tail} = 75\ \mu$A
- The PMOS current mirror (Q5-Q6, Q7-Q8) mirrors with 1:1, so each branch has the same current
- The NMOS output mirror (Q13-Q14) scales by K=3

Total current from supply:
- Input stage: $I_{tail} = 75\ \mu$A (through Q13)
- Output PMOS branches: The 1:1 mirror from Q5/Q6 to Q7/Q8 copies the input current
- Output NMOS stage: $I_{D14} = K \cdot I_{D1} = 3 \times 37.5 = 112.5\ \mu$A per side

From the schematic, the bias current for the output mirrors:
$$I_{D14} = K \cdot I_{D1} = K \cdot \frac{I_b}{2} = \frac{K \cdot I_b}{2}$$

Total current:
$$I_{total} = I_b + 2 \times I_{D14} = I_b + 2 \times \frac{K \cdot I_b}{2} = I_b(1 + K) = 75(1 + 3) = 300\ \mu\text{A}$$

Actually, looking more carefully at the topology:
- $I_b = I_{tail}$ for the differential pair
- Each output branch carries $K \cdot I_{D1} = K \cdot I_b/2$
- Two output branches: $2 \times K \cdot I_b/2 = K \cdot I_b$

$$I_{total} = I_b + K \cdot I_b = I_b(1 + K) = 75\ \mu\text{A} \times 4$$

> [!success] Result
> $$I_{total} = \boxed{300\ \mu\text{A}}$$

> [!note] Comparison
> | OTA Type | Total Current | Advantage |
> |----------|---------------|-----------|
> | Folded Cascode | 281.25 μA | Higher output swing |
> | Current Mirror (K=3) | 300 μA | Higher gain for same $g_m$ |
>
> The current mirror OTA uses slightly more current but provides $K$ times more transconductance from the same input stage, effectively trading current for gain.

---

## Summary

> [!tldr] Key Results
>
> **Problem 1:** Wide-swing current mirror input impedance
> - $r_{in} \approx 1/g_{m1}$ (low impedance)
> - $V_B$ range: 0.9 V to 1.4 V
>
> **Problem 2:** Enhanced output impedance
> - $r_{out} = A \cdot g_{m2} \cdot r_{ds1} \cdot r_{ds2}$
>
> **Problem 3:** OTA parameters
> - $r_{out} = 63.25$ kΩ
> - $f_p = 158.1$ kHz
>
> **Problem 4:** Feedback amplifier design
> - Loop gain: $L(s) = A(s)/3$
> - Effective load: $C_{L,eff} = 1.33$ pF
> - Folded cascode: $I_{total} = 281.25$ μA
> - Current mirror: $I_{total} = 300$ μA

---

## Formulas Reference

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | Diode-connected MOSFET $r_{in}$ | $r_{in} \approx 1/g_m$ |
> | Cascode $r_{out}$ | $r_{out} = g_m r_{ds1} r_{ds2}$ |
> | Enhanced cascode $r_{out}$ | $r_{out} = A \cdot g_m r_{ds1} r_{ds2}$ |
> | OTA gain | $A_0 = G_m \cdot r_{out}$ |
> | Unity-gain frequency | $\omega_{ta} = G_m / C_L$ |
> | Feedback bandwidth | $\omega_{3dB} = \beta \cdot \omega_{ta}$ |
> | Transconductance | $g_m = 2I_D/V_{eff} = I_{tail}/V_{eff}$ |
> | Current mirror OTA $G_m$ | $G_{m,eff} = K \cdot g_{m1}$ |

---

> [!nav]
> [[Problem 1 - Amplifier Configurations|← Problem 1]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
