# Problem 1 - Amplifier Configurations

> [!info] Exercise Files
> - Problems: [31632-problems-intro.pdf](file:///C:/Users/Mads2/DTU/Obsidian/Courses/34655%20Integrated%20Analog%20Electronics%202/Exercises/Work/31632-problems-intro.pdf)
> - Solutions: [31632-solution-intro.pdf](file:///C:/Users/Mads2/DTU/Obsidian/Courses/34655%20Integrated%20Analog%20Electronics%202/Exercises/Solutions/31632-solution-intro.pdf)

## Overview

This exercise compares three amplifier configurations:
1. **Common Source Stage** - Single transistor amplifier
2. **Cascode (Telescopic) Amplifier** - Two transistors stacked for higher gain
3. **Two-Stage Cascade** - Two common source stages in series

We calculate for each: output resistance $r_{out}$, voltage gain $A_v$, bandwidth $f_{3dB}$, and gain-bandwidth product $GBW$.

---

## Given Parameters

> [!abstract] Transistor Parameters
> | Parameter | Value | Description |
> |-----------|-------|-------------|
> | $g_{m1}$ | 0.20 mA/V | Transconductance |
> | $r_{ds1}$ | 250 kΩ | Drain-source resistance |
> | $g_s$ | 0.04 mA/V | Source-bulk transconductance |
> | $I_A$ | 20 μA | Bias current |
> | $C_L$ | 5 pF | Load capacitance |

---

## Question 1: Common Source Stage

> [!question] Calculate $r_{out}$, $A_v$, $f_{3dB}$, and $GBW$ for the common source amplifier.

### Circuit

![[Fig.1_intro.png|300]]

The common source stage has the input signal applied to the gate, with the source grounded and output taken from the drain. The ideal current source $I_A$ provides biasing.

### Solution

> [!success] Output Resistance
> For a common source stage, the output resistance equals the transistor's drain-source resistance:
> $$r_{out} = r_{ds1} = 250\ \text{k}\Omega$$

> [!success] Voltage Gain
> The small-signal voltage gain is:
> $$A_v = -g_{m1} \cdot r_{ds1}$$
>
> Substituting values:
> $$A_v = -0.20 \times 10^{-3} \times 250 \times 10^{3} = \boxed{-50\ \text{V/V}}$$
>
> The negative sign indicates phase inversion (180° phase shift).

> [!success] -3 dB Bandwidth
> The bandwidth is determined by the RC time constant at the output:
> $$f_{3dB} = \frac{1}{2\pi r_{out} C_L} = \frac{1}{2\pi r_{ds1} C_L}$$
>
> Substituting:
> $$f_{3dB} = \frac{1}{2\pi \times 250 \times 10^{3} \times 5 \times 10^{-12}} = \boxed{127.3\ \text{kHz}}$$

> [!success] Gain-Bandwidth Product
> $$GBW = |A_v| \times f_{3dB} = \frac{g_{m1} r_{ds1}}{2\pi r_{ds1} C_L} = \frac{g_{m1}}{2\pi C_L}$$
>
> $$GBW = \frac{0.20 \times 10^{-3}}{2\pi \times 5 \times 10^{-12}} = \boxed{6.366\ \text{MHz}}$$

> [!tip] Key Insight
> Notice that $GBW = \frac{g_m}{2\pi C_L}$ depends only on $g_m$ and $C_L$, not on $r_{ds}$. This will be important later.

---

## Question 2: Cascode (Telescopic) Amplifier

> [!question] Calculate $r_{out}$, $A_v$, $f_{3dB}$, and $GBW$ for the cascode amplifier.

### Circuit

![[Fig.2_intro.png|300]]

The cascode configuration stacks a common-gate transistor ($Q_2$) on top of the common-source transistor ($Q_1$). The cascode transistor's gate is held at a fixed bias voltage $V_{BIAS}$.

### Why Cascode?

The cascode configuration dramatically increases output resistance by using the common-gate transistor to shield the drain of $Q_1$ from output voltage variations.

### Solution

> [!success] Output Resistance
> For a telescopic cascode (from Carusone, equation 3.37):
> $$r_{out} = r_{ds2}(1 + r_{ds1}(g_{m2} + g_{s2} + g_{ds2})) \approx r_{ds2} \cdot r_{ds1} \cdot (g_{m2} + g_{s2})$$
>
> With $r_{ds1} = r_{ds2} = 250\ \text{k}\Omega$, $g_{m2} = 0.20\ \text{mA/V}$, $g_{s2} = 0.04\ \text{mA/V}$:
> $$r_{out} = (250 \times 10^{3})^2 \times (0.20 + 0.04) \times 10^{-3}$$
> $$r_{out} = 62.5 \times 10^{9} \times 0.24 \times 10^{-3} = \boxed{15\ \text{M}\Omega}$$
>
> This is **60× higher** than the simple common source stage!

> [!success] Voltage Gain
> The gain is now determined by the much higher output resistance:
> $$A_v = -g_{m1} \cdot r_{out} = -0.20 \times 10^{-3} \times 15 \times 10^{6} = \boxed{-3000\ \text{V/V}}$$
>
> This is **60× higher** than the common source stage.

> [!success] -3 dB Bandwidth
> $$f_{3dB} = \frac{1}{2\pi r_{out} C_L} = \frac{1}{2\pi \times 15 \times 10^{6} \times 5 \times 10^{-12}} = \boxed{2.122\ \text{kHz}}$$
>
> The bandwidth is **60× lower** than the common source stage.

> [!success] Gain-Bandwidth Product
> $$GBW = |A_v| \times f_{3dB} = \frac{g_{m1} r_{out}}{2\pi r_{out} C_L} = \frac{g_{m1}}{2\pi C_L} = \boxed{6.366\ \text{MHz}}$$

> [!warning] Important Observation
> The GBW is **identical** to the common source stage! This is because:
> - Gain is proportional to $r_{out}$
> - Bandwidth is proportional to $1/r_{out}$
> - These cancel out: $GBW = \frac{g_m}{2\pi C_L}$
>
> The cascode trades bandwidth for gain while maintaining the same GBW.

---

## Question 3: Two-Stage Cascade Amplifier

> [!question] Calculate $r_{out}$, $A_v$, $f_{3dB}$, and $GBW$ for the cascade amplifier with $I_A/2$ per stage.

### Circuit

![[Fig.3_intro.png|350]]

Two common source stages in series. To maintain the same total current as the cascode ($I_A = 20\ \mu\text{A}$), each stage operates at $I_A/2 = 10\ \mu\text{A}$.

### Effect of Reduced Current on Parameters

> [!abstract] Scaling with Current
> When current is halved ($I_D \rightarrow I_D/2$):
>
> **Transconductance** (since $g_m = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$):
> $$g_{m,new} = \frac{g_m}{\sqrt{2}} = \frac{0.20}{\sqrt{2}} = 0.141\ \text{mA/V}$$
>
> **Output resistance** (since $r_{ds} = \frac{1}{\lambda I_D}$):
> $$r_{ds,new} = 2 \cdot r_{ds} = 2 \times 250 = 500\ \text{k}\Omega$$

### Solution

> [!success] Output Resistance
> Only the second stage's output resistance matters for the overall output:
> $$r_{out} = r_{ds,new} = \boxed{500\ \text{k}\Omega}$$

> [!success] Voltage Gain
> For two stages in cascade, gains multiply:
> $$A_v = A_{v1} \times A_{v2} = (g_{m,new} \cdot r_{ds,new})^2$$
>
> $$A_v = \left(\frac{0.20}{\sqrt{2}} \times 10^{-3} \times 500 \times 10^{3}\right)^2$$
> $$A_v = (0.141 \times 10^{-3} \times 500 \times 10^{3})^2 = (70.7)^2 = \boxed{5000\ \text{V/V}}$$
>
> This is **higher** than the cascode (5000 vs 3000) because there's no bulk effect penalty.

> [!success] -3 dB Bandwidth
> $$f_{3dB} = \frac{1}{2\pi r_{out} C_L} = \frac{1}{2\pi \times 500 \times 10^{3} \times 5 \times 10^{-12}} = \boxed{63.66\ \text{kHz}}$$

> [!success] Gain-Bandwidth Product
> $$GBW = |A_v| \times f_{3dB} = 5000 \times 63.66\ \text{kHz} = \boxed{318.3\ \text{MHz}}$$
>
> This is **50× higher** than the other configurations!

---

## Summary and Comparison

> [!tldr] Results Comparison
> | Configuration | $r_{out}$ | $|A_v|$ | $f_{3dB}$ | GBW |
> |--------------|-----------|---------|-----------|-----|
> | Common Source | 250 kΩ | 50 V/V | 127.3 kHz | 6.37 MHz |
> | Cascode | 15 MΩ | 3000 V/V | 2.12 kHz | 6.37 MHz |
> | Two-Stage Cascade | 500 kΩ | 5000 V/V | 63.66 kHz | 318.3 MHz |

### Key Takeaways

> [!note] Cascode vs Common Source
> - **Same GBW** - gain and bandwidth trade off exactly
> - Cascode gives 60× more gain but 60× less bandwidth
> - Single dominant pole - easier to stabilize

> [!note] Two-Stage Cascade Advantages
> - **50× higher GBW** than single-stage designs
> - Higher gain than cascode (no bulk effect penalty)
> - Lower output impedance than cascode → higher bandwidth

> [!warning] Two-Stage Cascade Disadvantage
> The two-stage cascade has **two high-impedance nodes** (one at each stage's output), creating **two low-frequency poles**. This makes frequency compensation more challenging and can cause stability issues when used in feedback configurations.
>
> This is why Miller compensation is often needed in two-stage opamps!

---

## Formulas Reference

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | CS Gain | $A_v = -g_m \cdot r_{ds}$ |
> | Cascode $r_{out}$ | $r_{out} \approx r_{ds1} \cdot r_{ds2} \cdot (g_{m2} + g_{s2})$ |
> | Bandwidth | $f_{3dB} = \frac{1}{2\pi r_{out} C_L}$ |
> | GBW (single stage) | $GBW = \frac{g_m}{2\pi C_L}$ |
> | $g_m$ scaling | $g_m \propto \sqrt{I_D}$ |
> | $r_{ds}$ scaling | $r_{ds} \propto \frac{1}{I_D}$ |
