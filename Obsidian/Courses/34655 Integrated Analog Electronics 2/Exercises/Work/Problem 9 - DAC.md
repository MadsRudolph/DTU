---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, DAC, R2R, current-steering, data-converters]
---
# Problem 9 - DAC

> [!info] Exercise Files
> - Problems: [[31632-problems-dac.pdf]]
> - Related notes: [[Lecture 9 - Data Converter Fundamentals]]

## Overview

This exercise set covers DAC circuit analysis:
1. **Problem 16.12** — R-2R current-driven DAC: verify operation and estimate speed
2. **Problem 16.13** — R-2R current-driven DAC with offset and gain errors
3. **Problem 16.17** — Dynamically matched current source: W/L sizing and charge injection
4. **Problem 16.18** — Repeat 16.17 without the 0.9$I_\text{ref}$ source

---

## Problem 16.12: R-2R Current-Driven DAC

> [!abstract] Problem Statement
> Show that the D/A converter circuit in Fig. 16.11 operates correctly. Estimate the speed if the opamp has infinite bandwidth, $R = 10\;\text{k}\Omega$, and all nodes have a capacitance of 0.5 pF to ground.

### Circuit Description

The R-2R current-driven DAC (Fig. 16.11) has 4 identical current sources of value $I$. The nodes from left to right are labelled A, B, C, D:

- **Node A** (leftmost): $R$ shunt to ground, current source $b_4$
- **Node B**: $2R$ shunt to ground, current source $b_3$
- **Node C**: $2R$ shunt to ground, current source $b_2$
- **Node D** (rightmost): connects to opamp (−) terminal through $R_f$, current source $b_1$ (MSB)

Horizontal connections: A—$R$—B—$R$—C—$R$—D. The opamp (−) is a virtual ground ($V = 0$).

### Part 1: Verify Correct Operation

**Strategy:** Use superposition. For each bit $b_i = 1$ (all others off), find the current reaching the virtual ground at node D.

#### Equivalent resistance looking left from each node

Since the opamp (−) is at virtual ground (0 V), and all shunts also go to ground (0 V):

| From node | Looking left | Calculation |
|---|---|---|
| A | $R$ to ground | $Z_A = R$ |
| B | $R + Z_A = 2R$, in parallel with $2R$ shunt | $2R \| 2R = R \Rightarrow Z_B = R$ |
| C | $R + Z_B = 2R$, in parallel with $2R$ shunt | $2R \| 2R = R \Rightarrow Z_C = R$ |
| D | $R + Z_C = 2R$ | $Z_{\text{left from D}} = 2R$ |

#### Current from $b_1$ (node D, MSB)

Current $I$ enters D. Since D is at virtual ground (0 V) and the left-side equivalent resistance terminates at ground, no current flows left. **All** current goes to the opamp:

$$I_{b_1} = I$$

#### Current from $b_2$ (node C)

Current $I$ enters C. Three paths to ground: left ($2R$), right ($R$ to D at 0 V), shunt ($2R$):

$$V_C = \frac{I}{\frac{1}{2R} + \frac{1}{R} + \frac{1}{2R}} = \frac{I}{\frac{2}{R}} = \frac{IR}{2}$$

Current to opamp (through $R$ to D):

$$I_{b_2} = \frac{V_C}{R} = \frac{I}{2}$$

#### Current from $b_3$ (node B)

Current $I$ enters B. Three paths: left ($2R$), shunt ($2R$), right to the rest of the network.

Looking right from B: $R$ to C, and at C the parallel combination $2R \| R = 2R/3$. So $Z_\text{right} = R + 2R/3 = 5R/3$.

$$V_B = \frac{I}{\frac{1}{2R} + \frac{1}{2R} + \frac{3}{5R}} = \frac{I}{\frac{5+5+6}{10R}} = \frac{10IR}{16} = \frac{5IR}{8}$$

Current flowing right from B into C:

$$I_\text{right} = \frac{V_B}{5R/3} = \frac{5IR/8}{5R/3} = \frac{3I}{8}$$

At C, this current splits between $2R$ (down) and $R$ (right to D):

$$V_C = I_\text{right} \times (2R \| R) = \frac{3I}{8} \times \frac{2R}{3} = \frac{IR}{4}$$

$$I_{b_3} = \frac{V_C}{R} = \frac{I}{4}$$

#### Current from $b_4$ (node A)

Current $I$ enters A. Two paths: $R$ shunt (up) and $R$ to B (right).

Looking right from A: $R$ to B, at B: $2R \| Z_\text{right from B} = 2R \| 5R/3 = 10R/11$. So $Z_\text{right from A} = R + 10R/11 = 21R/11$.

$$V_A = \frac{I}{\frac{1}{R} + \frac{11}{21R}} = \frac{I}{\frac{21+11}{21R}} = \frac{21IR}{32}$$

Current flowing right from A:

$$I_\text{right} = \frac{V_A}{21R/11} = \frac{21IR}{32} \times \frac{11}{21R} = \frac{11I}{32}$$

Tracing through B → C → D (repeating the splitting at each node):

At B: $V_B = I_\text{right} \times (2R \| 5R/3) = \frac{11I}{32} \times \frac{10R}{11} = \frac{10IR}{32} = \frac{5IR}{16}$

Current right from B: $V_B/(5R/3) = \frac{5IR}{16} \times \frac{3}{5R} = \frac{3I}{16}$

At C: $V_C = \frac{3I}{16} \times \frac{2R}{3} = \frac{IR}{8}$

$$I_{b_4} = \frac{V_C}{R} = \frac{I}{8}$$

#### Summary

| Bit | Current to opamp |
|---|---|
| $b_1$ (MSB) | $I$ |
| $b_2$ | $I/2$ |
| $b_3$ | $I/4$ |
| $b_4$ (LSB) | $I/8$ |

The currents are **binary weighted** (each successive bit contributes half). The output voltage:

$$\boxed{V_o = -R_f \left(b_1 I + b_2 \frac{I}{2} + b_3 \frac{I}{4} + b_4 \frac{I}{8}\right) = -2R_f I \sum_{i=1}^{4} b_i \left(\frac{1}{2}\right)^i}$$

This confirms the D/A converter operates correctly as a 4-bit DAC.

### Part 2: Speed Estimate

With $R = 10\;\text{k}\Omega$ and $C = 0.5\;\text{pF}$ at each node, the speed is limited by the RC settling of the ladder network.

**Single-stage time constant:**

$$\tau = RC = 10\;\text{k}\Omega \times 0.5\;\text{pF} = 5\;\text{ns}$$

**Worst case:** a code change at node A must propagate through 3 RC stages to reach the output at D. Using the Elmore delay approximation for the cascaded RC network:

$$\tau_D \approx RC + 2RC + 3RC = 6RC = 30\;\text{ns}$$

For settling to 4-bit accuracy (within $\frac{1}{2}$ LSB = 1/32 of full scale):

$$e^{-t/\tau_D} < \frac{1}{32} \implies t > \ln(32) \times \tau_D \approx 3.47 \times 30 = 104\;\text{ns}$$

> [!tip] Result
> Maximum conversion rate $\approx 1/104\;\text{ns} \approx 10\;\text{MHz}$
>
> A rough estimate gives a bandwidth of $f_{-3\text{dB}} \approx \frac{1}{2\pi \times 6RC} \approx 5.3\;\text{MHz}$

---

## Problem 16.13: R-2R DAC with Offset and Gain Error

> [!abstract] Problem Statement
> Consider the R-2R current-driven DAC in Fig. 16.11 with $I = 1\;\text{mA}$, $R_f = 2\;\text{k}\Omega$, and $R = 10\;\text{k}\Omega$. The converter is perfectly linear but has an offset error of 0.15 LSB and a gain error of 0.2 LSB. Find the output levels for codes 0000, 1000, and 1111.

### Ideal Analysis

From Problem 16.12, the output voltage is:

$$V_o = -R_f\left(b_1 I + b_2 \frac{I}{2} + b_3 \frac{I}{4} + b_4 \frac{I}{8}\right)$$

The **LSB voltage** corresponds to the smallest step (bit $b_4$ only):

$$V_\text{LSB} = R_f \times \frac{I}{8} = 2\;\text{k}\Omega \times \frac{1\;\text{mA}}{8} = 0.25\;\text{V}$$

**Ideal output levels** (magnitudes):

| Code $b_1 b_2 b_3 b_4$ | Decimal | Ideal $V_o$               |
| ---------------------- | ------- | ------------------------- |
| 0000                   | 0       | 0 V                       |
| 1000                   | 8       | $8 \times 0.25 = 2.0$ V   |
| 1111                   | 15      | $15 \times 0.25 = 3.75$ V |

### Applying Offset and Gain Errors

**Offset error definition** (D/A):

$$E_\text{off} = \frac{V_\text{out}|_{0\dots0}}{V_\text{LSB}} = 0.15\;\text{LSB}$$

$$|V_\text{out}(0000)| = 0.15 \times 0.25\;\text{V} = 0.0375\;\text{V}$$

**Gain error definition** (D/A):

$$E_\text{gain} = \left(\frac{|V_\text{out}|_{1\dots1}|}{V_\text{LSB}} - \frac{|V_\text{out}|_{0\dots0}|}{V_\text{LSB}}\right) - (2^N - 1) = 0.2\;\text{LSB}$$

$$\frac{|V_\text{out}(1111)| - |V_\text{out}(0000)|}{V_\text{LSB}} = 15 + 0.2 = 15.2$$

$$|V_\text{out}(1111)| - |V_\text{out}(0000)| = 15.2 \times 0.25 = 3.80\;\text{V}$$

$$|V_\text{out}(1111)| = 3.80 + 0.0375 = 3.8375\;\text{V}$$

**For code 1000** (linear converter, step size is uniform):

$$V_\text{step,actual} = \frac{|V_\text{out}(1111)| - |V_\text{out}(0000)|}{15} = \frac{3.80}{15} = 0.2533\;\text{V}$$

$$|V_\text{out}(1000)| = |V_\text{out}(0000)| + 8 \times V_\text{step,actual} = 0.0375 + 8 \times 0.2533 = 2.064\;\text{V}$$

### Results

> [!tip] Output Levels (magnitude, circuit output is negative)
>
> | Code | Ideal $V_o$ | Actual $V_o$ |
> |---|---|---|
> | 0000 | 0 V | **0.0375 V** |
> | 1000 | 2.000 V | **2.064 V** |
> | 1111 | 3.750 V | **3.838 V** |

---

## Problem 16.17: Dynamically Matched Current Source

> [!abstract] Problem Statement
> A D/A converter uses dynamically matched current sources (Fig. 16.20). Assuming ideal transistors, find $W/L$ for $Q_1$ to set $V_{GS} = 3\;\text{V}$ when $I_\text{ref} = 50\;\mu\text{A}$, $V_t = 1\;\text{V}$, $\mu_n C_{ox} = 92\;\mu\text{A/V}^2$. If switch $S_1$ causes a random charge injection voltage of 1 mV, what is the expected percentage of random variation of the current being held on $Q_1$?

### Circuit Operation (Fig. 16.20)

The dynamically matched current source uses:
- $Q_1$ with gate capacitor $C_{gs}$ — a small adjustable transistor
- A fixed $0.9 I_\text{ref}$ current source providing the bulk of the output current
- $S_1$ — calibration switch (stores $V_{GS}$ on $C_{gs}$)
- $S_2$ — output steering switch

**Calibration phase:** $S_1$ closes. The reference current $I_\text{ref}$ is forced through the branch. The $0.9 I_\text{ref}$ source provides 45 $\mu$A, so $Q_1$ adjusts to provide the remaining:

$$I_{D1} = I_\text{ref} - 0.9 I_\text{ref} = 0.1 I_\text{ref} = 5\;\mu\text{A}$$

When $S_1$ opens, $V_{GS} = 3\;\text{V}$ is stored on $C_{gs}$.

### Finding W/L

MOSFET saturation current:

$$I_D = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS} - V_t)^2$$

$$5\;\mu\text{A} = \frac{1}{2} \times 92\;\mu\text{A/V}^2 \times \frac{W}{L} \times (3 - 1)^2$$

$$5 = \frac{1}{2} \times 92 \times \frac{W}{L} \times 4 = 184 \times \frac{W}{L}$$

$$\boxed{\frac{W}{L} = \frac{5}{184} \approx 0.027}$$

### Charge Injection Analysis

The transconductance of $Q_1$:

$$g_m = \frac{2I_D}{V_{GS} - V_t} = \frac{2 \times 5\;\mu\text{A}}{3 - 1} = 5\;\mu\text{A/V}$$

Charge injection causes $\Delta V_{GS} = 1\;\text{mV}$, giving:

$$\Delta I_D = g_m \times \Delta V_{GS} = 5\;\mu\text{A/V} \times 1\;\text{mV} = 5\;\text{nA}$$

**Percentage variation of $Q_1$'s current:**

$$\frac{\Delta I_D}{I_{D1}} = \frac{5\;\text{nA}}{5\;\mu\text{A}} = \boxed{0.1\%}$$

**Impact on total output current** ($I_\text{ref}$):

$$\frac{\Delta I_D}{I_\text{ref}} = \frac{5\;\text{nA}}{50\;\mu\text{A}} = 0.01\%$$

> [!tip] Key Advantage
> The $0.9 I_\text{ref}$ fixed source means $Q_1$'s charge injection error (5 nA) only affects 10% of the total current. The **output current variation is only 0.01%** of $I_\text{ref}$.

---

## Problem 16.18: Without the $0.9 I_\text{ref}$ Source

> [!abstract] Problem Statement
> Repeat Problem 16.17 if the design does not incorporate the $0.9 I_\text{ref}$ extra current source (i.e., $Q_1$ must be the source for all of $I_\text{ref}$).

### Finding W/L

Now $Q_1$ must carry the full $I_\text{ref} = 50\;\mu\text{A}$ at $V_{GS} = 3\;\text{V}$:

$$50\;\mu\text{A} = \frac{1}{2} \times 92\;\mu\text{A/V}^2 \times \frac{W}{L} \times (3 - 1)^2 = 184 \times \frac{W}{L}$$

$$\boxed{\frac{W}{L} = \frac{50}{184} = \frac{25}{92} \approx 0.272}$$

### Charge Injection Analysis

$$g_m = \frac{2 \times 50\;\mu\text{A}}{3 - 1} = 50\;\mu\text{A/V}$$

$$\Delta I_D = 50\;\mu\text{A/V} \times 1\;\text{mV} = 50\;\text{nA}$$

**Percentage variation of $Q_1$'s current (which IS the output):**

$$\frac{\Delta I_D}{I_\text{ref}} = \frac{50\;\text{nA}}{50\;\mu\text{A}} = \boxed{0.1\%}$$

### Comparison: 16.17 vs 16.18

| Parameter | With $0.9I_\text{ref}$ source (16.17) | Without (16.18) |
|---|---|---|
| $W/L$ | 0.027 | 0.272 |
| $Q_1$ current | 5 $\mu$A | 50 $\mu$A |
| $g_m$ | 5 $\mu$A/V | 50 $\mu$A/V |
| $\Delta I_D$ (absolute) | 5 nA | 50 nA |
| $\Delta I_D / I_{D1}$ | 0.1% | 0.1% |
| $\Delta I_D / I_\text{ref}$ | **0.01%** | **0.1%** |

> [!important] Key Takeaway
> The percentage variation of $Q_1$'s own current is **the same** in both cases (0.1%) because $\Delta I/I = 2\Delta V/(V_{GS} - V_t)$ depends only on the overdrive voltage and charge injection, not on the current level.
>
> However, the $0.9 I_\text{ref}$ source provides a **10× improvement** in the output current accuracy (0.01% vs 0.1% of $I_\text{ref}$) because $Q_1$'s error only affects 10% of the total current. This is the advantage of dynamic element matching with a fixed bias source.
