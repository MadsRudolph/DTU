---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, noise]
---
# Problem 4 - Noise

> [!info] Exercise Files
> - Problems: [[31632-problems-noise.pdf]]
> - Related notes: [[Lecture 4 - Noise]], [[Chapter 9 - Noise and Linearity Analysis and Modelling]]

## Overview

This exercise set covers noise analysis in CMOS circuits:
1. **Problem 9.23** — Current mirror output noise (white + flicker)
2. **Problem 9.24** — CS amplifier output noise (0.18 μm, white only)
3. **Problem 9.25** — CS amplifier output noise (45 nm, white only)

---

## Problem 9.23: NMOS Current Mirror Noise

> [!abstract] Problem Statement
> Consider the NMOS current mirror in Fig. P9.23. $Q_2$ is in active mode and the load connected to $I_{out}$ has much lower impedance than the mirror's output impedance. Find an expression for the current noise spectral density superimposed on $I_{out}$ in terms of $C$ and all device/small-signal model parameters for $Q_1$ and $Q_2$. Neglect all parasitic capacitors.

### Circuit

```
         I_in ↓           ↓ I_out
              |           |
              Q₁ ──┬── Q₂
              |    |    |
              └────┤    |
                   C    |
                   |    |
                  GND  GND
```

$Q_1$ is diode-connected (gate = drain). $C$ connects the shared gate node to ground.

### Noise Sources

Each MOSFET has two noise sources:

**Thermal (white) drain current noise:**

$$i_{n,w}^2(f) = 4kT\gamma g_m \quad \text{[A}^2\text{/Hz]}$$

**Flicker (1/f) noise referred to gate:**

$$V_{g,f}^2(f) = \frac{K}{WLC_{ox}f} \quad \text{[V}^2\text{/Hz]}$$

Which, converted to drain current noise:

$$i_{n,f}^2(f) = g_m^2 \cdot \frac{K}{WLC_{ox}f} \quad \text{[A}^2\text{/Hz]}$$

### Small-Signal Analysis

**Gate node impedance:**

$Q_1$ diode-connected: $Z_{Q_1} \approx 1/g_{m1}$ (since $r_{ds1} \gg 1/g_{m1}$). In parallel with capacitor $C$:

$$Z_{gate} = \frac{1/g_{m1}}{1 + j2\pi f C/g_{m1}} = \frac{1}{g_{m1} + j2\pi fC}$$

This forms a **first-order lowpass** with cutoff frequency:

$$\boxed{f_c = \frac{g_{m1}}{2\pi C}}$$

### Noise from $Q_1$ (filtered by C)

$Q_1$'s drain noise current $i_{n1}$ creates a gate voltage fluctuation through $Z_{gate}$, which then drives $Q_2$:

$$I_{out,1}^2(f) = g_{m2}^2 \cdot |Z_{gate}|^2 \cdot i_{n1}^2(f) = \frac{g_{m2}^2 \cdot i_{n1}^2(f)}{g_{m1}^2 + (2\pi fC)^2}$$

> [!tip] Key insight
> The capacitor $C$ acts as a **lowpass filter** on $Q_1$'s noise contribution. At frequencies $f \gg f_c$, $Q_1$'s noise is suppressed.

### Noise from $Q_2$ (unfiltered)

Since the load impedance $\ll$ mirror output impedance, $Q_2$'s drain noise current flows directly to the output:

$$I_{out,2}^2(f) = i_{n2}^2(f)$$

### Total Output Current Noise Spectral Density

$$\boxed{I_{out}^2(f) = \frac{g_{m2}^2}{g_{m1}^2 + (2\pi fC)^2}\left(4kT\gamma g_{m1} + \frac{g_{m1}^2 K_1}{W_1 L_1 C_{ox} f}\right) + 4kT\gamma g_{m2} + \frac{g_{m2}^2 K_2}{W_2 L_2 C_{ox} f}}$$

Separating by noise type:

**White noise only:**

$$I_{out,w}^2(f) = \frac{4kT\gamma g_{m1} g_{m2}^2}{g_{m1}^2 + (2\pi fC)^2} + 4kT\gamma g_{m2}$$

**Flicker noise only:**

$$I_{out,f}^2(f) = \frac{g_{m2}^2 K_1}{W_1 L_1 C_{ox} f \left[1 + (2\pi fC/g_{m1})^2\right]} + \frac{g_{m2}^2 K_2}{W_2 L_2 C_{ox} f}$$

### Behaviour at Frequency Extremes

| Frequency range | $Q_1$ contribution | $Q_2$ contribution |
|---|---|---|
| $f \ll f_c$ | Full: $\frac{g_{m2}^2}{g_{m1}^2}\cdot i_{n1}^2$ | Full: $i_{n2}^2$ |
| $f \gg f_c$ | Suppressed by $C$ → 0 | Full: $i_{n2}^2$ |

> [!important] Physical Interpretation
> - At low frequencies, **both** transistors contribute noise. For matched devices ($g_{m1} = g_{m2}$), $Q_1$'s white noise contribution equals $Q_2$'s, so the total white noise is $2 \times 4kT\gamma g_m$.
> - At high frequencies, $C$ shorts the gate to ground, suppressing $Q_1$'s noise. Only $Q_2$'s noise remains: $4kT\gamma g_{m2}$.
> - Flicker noise from $Q_1$ is also filtered by $C$, but since flicker noise is dominant at low frequencies (where $C$ has less effect), the filtering is less beneficial for 1/f noise.

---

## Problem 9.24: CS Amplifier with Current Source Load (0.18 μm)

> [!abstract] Problem Statement
> In the common-source amplifier of Fig. P9.24, $I_{in} = 1$ mA and $Q_1$ is in active mode with $(W/L) = (30\,\mu\text{m}/0.2\,\mu\text{m})$. Using the 0.18-μm parameters from Table 1.5 and $\gamma = 2/3$:
> **a.** Sketch the voltage noise spectral density at $v_o$.
> **b.** Find the total rms voltage noise at $v_o$.
> *(White noise only)*

### Circuit

```
      VDD
       |
      (Io)  ← ideal current source (noiseless)
       |
       ●── vo ──┤├── C
       |              |
      Q₁ (NMOS)     GND
       |
   vi ─┤
       |
      GND
```

### Device Parameters (0.18 μm NMOS, Table 1.5)

| Parameter | Value |
|---|---|
| $\mu C_{ox}$ | 270 μA/V² |
| $V_{t0}$ | 0.45 V |
| $\lambda \cdot L$ | 0.08 μm/V |
| $C_{ox}$ | 8.5 fF/μm² |

### Step 1: DC Operating Point

$$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}V_{eff}^2 \implies V_{eff}^2 = \frac{2I_D}{\mu C_{ox}(W/L)}$$

$$V_{eff}^2 = \frac{2 \times 10^{-3}}{270 \times 10^{-6} \times 150} = \frac{2 \times 10^{-3}}{40.5 \times 10^{-3}} = 0.04938$$

$$\boxed{V_{eff} = 222\,\text{mV}}$$

### Step 2: Small-Signal Parameters

**Transconductance:**

$$g_m = \frac{2I_D}{V_{eff}} = \frac{2 \times 10^{-3}}{0.222} = \boxed{9.0\,\text{mA/V}}$$

**Channel-length modulation:**

$$\lambda = \frac{\lambda \cdot L}{L} = \frac{0.08}{0.2} = 0.4\,\text{V}^{-1}$$

**Output resistance:**

$$r_{ds} = \frac{1}{\lambda I_D} = \frac{1}{0.4 \times 10^{-3}} = \boxed{2.5\,\text{k}\Omega}$$

**Intrinsic gain:**

$$A_i = g_m r_{ds} = 9.0 \times 10^{-3} \times 2500 = \boxed{22.5\,\text{V/V}}$$

### Step 3: Output Noise Spectral Density

The only noise source is $Q_1$'s thermal drain current noise (ideal current source $I_o$ is noiseless):

$$i_{n1}^2 = 4kT\gamma g_m = 4 \times 1.38 \times 10^{-23} \times 300 \times \frac{2}{3} \times 9.0 \times 10^{-3} = 9.94 \times 10^{-23}\,\text{A}^2\text{/Hz}$$

The output impedance is $r_{ds}$ in parallel with $C$:

$$V_{no}^2(f) = i_{n1}^2 \cdot |Z_{out}|^2 = \frac{4kT\gamma g_m \cdot r_{ds}^2}{1 + (f/f_0)^2}$$

where the pole frequency is:

$$f_0 = \frac{1}{2\pi r_{ds} C}$$

**Low-frequency (flat) spectral density:**

$$V_{no}^2(0) = 4kT\gamma g_m \cdot r_{ds}^2 = 9.94 \times 10^{-23} \times (2500)^2$$

$$\boxed{V_{no}^2(0) = 6.21 \times 10^{-16}\,\text{V}^2\text{/Hz} \quad \Leftrightarrow \quad V_{no}(0) = 24.9\,\text{nV}/\sqrt{\text{Hz}}}$$

### Part (a): Sketch

```
 V²no(f)
 [V²/Hz]
   ↑
   |  6.21×10⁻¹⁶  ┌──────────────┐
   |               │  flat region  │
   |               │               └──────  -20 dB/dec
   |               │                    ╲
   |               │                     ╲
   └───────────────┼──────────────────────╲──────→ f [Hz]
                   0                  f₀=1/(2πr_ds·C)
```

The output voltage noise PSD is a **first-order lowpass** shape:
- Flat at $V_{no}^2(0) = 6.21 \times 10^{-16}$ V²/Hz for $f < f_0$
- Rolls off at $-20$ dB/dec for $f > f_0$
- Pole at $f_0 = 1/(2\pi \cdot 2500 \cdot C)$

### Part (b): Total RMS Noise

Using the noise bandwidth of a 1st-order lowpass ($f_x = \frac{\pi}{2}f_0$):

$$V_{no,\text{rms}}^2 = V_{no}^2(0) \cdot f_x = 4kT\gamma g_m r_{ds}^2 \cdot \frac{\pi}{2} \cdot \frac{1}{2\pi r_{ds}C}$$

$$= \frac{4kT\gamma g_m r_{ds}^2}{4 r_{ds}C} = \frac{kT\gamma g_m r_{ds}}{C}$$

$$\boxed{V_{no,\text{rms}}^2 = \frac{kT \cdot \gamma g_m r_{ds}}{C} = \frac{15\,kT}{C} = \frac{6.21 \times 10^{-20}}{C}\,\text{V}^2}$$

where $\gamma g_m r_{ds} = \frac{2}{3} \times 22.5 = 15$.

$$\boxed{V_{no,\text{rms}} = \sqrt{\frac{6.21 \times 10^{-20}}{C}}\,\text{V}}$$

> [!tip] Comparison with kT/C Noise
> For a simple resistor $R$ with capacitor $C$, the total noise is $V_{rms}^2 = kT/C$.
> Here the noise is **15× larger** because the MOSFET's drain noise current ($4kT\gamma g_m$) is much larger than the Johnson noise of a resistor equal to $r_{ds}$ ($4kT/r_{ds}$). The ratio is $\gamma g_m r_{ds} = \gamma A_i = 15$.

---

## Problem 9.25: CS Amplifier with Current Source Load (45 nm)

> [!abstract] Problem Statement
> Repeat Problem 9.24 but using 45 nm technology parameters from Table 1.5 with $\gamma = 2$ and $(W/L) = (7.5\,\mu\text{m}/0.05\,\mu\text{m})$. *(White noise only)*

### Device Parameters (45 nm NMOS, Table 1.5)

| Parameter | Value |
|---|---|
| $\mu C_{ox}$ | 280 μA/V² |
| $V_{t0}$ | 0.45 V |
| $\lambda \cdot L$ | 0.10 μm/V |
| $C_{ox}$ | 25 fF/μm² |

### Step 1: DC Operating Point

$$V_{eff}^2 = \frac{2I_D}{\mu C_{ox}(W/L)} = \frac{2 \times 10^{-3}}{280 \times 10^{-6} \times 150} = \frac{2 \times 10^{-3}}{42.0 \times 10^{-3}} = 0.04762$$

$$\boxed{V_{eff} = 218\,\text{mV}}$$

### Step 2: Small-Signal Parameters

$$g_m = \frac{2I_D}{V_{eff}} = \frac{2 \times 10^{-3}}{0.218} = \boxed{9.17\,\text{mA/V}}$$

$$\lambda = \frac{0.10}{0.05} = 2.0\,\text{V}^{-1}$$

$$r_{ds} = \frac{1}{\lambda I_D} = \frac{1}{2.0 \times 10^{-3}} = \boxed{500\,\Omega}$$

$$A_i = g_m r_{ds} = 9.17 \times 10^{-3} \times 500 = \boxed{4.58\,\text{V/V}}$$

### Step 3: Output Noise Spectral Density

$$i_{n1}^2 = 4kT\gamma g_m = 4 \times 1.38 \times 10^{-23} \times 300 \times 2 \times 9.17 \times 10^{-3} = 3.04 \times 10^{-22}\,\text{A}^2\text{/Hz}$$

**Low-frequency spectral density:**

$$V_{no}^2(0) = i_{n1}^2 \cdot r_{ds}^2 = 3.04 \times 10^{-22} \times (500)^2$$

$$\boxed{V_{no}^2(0) = 7.59 \times 10^{-17}\,\text{V}^2\text{/Hz} \quad \Leftrightarrow \quad V_{no}(0) = 8.71\,\text{nV}/\sqrt{\text{Hz}}}$$

### Part (a): Sketch

Same first-order lowpass shape as Problem 9.24, but with:
- Lower flat level: $7.59 \times 10^{-17}$ V²/Hz (vs $6.21 \times 10^{-16}$, about 8.2× lower)
- Higher pole frequency: $f_0 = 1/(2\pi \times 500 \times C)$ (5× higher than 0.18 μm case)

### Part (b): Total RMS Noise

$$V_{no,\text{rms}}^2 = \frac{kT \cdot \gamma g_m r_{ds}}{C} = \frac{kT \times 2 \times 4.58}{C} = \frac{9.17\,kT}{C}$$

$$\boxed{V_{no,\text{rms}}^2 = \frac{9.17\,kT}{C} = \frac{3.80 \times 10^{-20}}{C}\,\text{V}^2}$$

$$\boxed{V_{no,\text{rms}} = \sqrt{\frac{3.80 \times 10^{-20}}{C}}\,\text{V}}$$

### Comparison: 0.18 μm vs 45 nm

| Parameter | 0.18 μm | 45 nm | Ratio |
|---|---|---|---|
| $g_m$ | 9.0 mA/V | 9.17 mA/V | ≈ 1.0× |
| $r_{ds}$ | 2.5 kΩ | 500 Ω | 0.2× |
| $A_i = g_m r_{ds}$ | 22.5 | 4.58 | 0.2× |
| $\gamma$ | 2/3 | 2 | 3× |
| $V_{no}(0)$ | 24.9 nV/√Hz | 8.71 nV/√Hz | 0.35× |
| $f_0$ | $1/(2\pi \cdot 2.5\text{k} \cdot C)$ | $1/(2\pi \cdot 500 \cdot C)$ | 5× |
| $\gamma g_m r_{ds}$ | 15 | 9.17 | 0.61× |
| $V_{no,\text{rms}}^2$ | $15\,kT/C$ | $9.17\,kT/C$ | 0.61× |

> [!important] Key Observations
> 1. **Same $g_m$** — Both devices have similar $W/L = 150$ and $\mu C_{ox}$, so $g_m$ is nearly identical.
> 2. **Much lower $r_{ds}$ for 45 nm** — $\lambda$ is 5× larger (0.4 vs 2.0 V⁻¹), so $r_{ds}$ drops by 5×. This dramatically reduces the intrinsic gain ($A_i$: 22.5 → 4.58).
> 3. **Lower spectral density but wider bandwidth** — The 45 nm device has 8.2× lower peak noise PSD but 5× wider noise bandwidth. The net effect on total rms noise depends on the product $\gamma g_m r_{ds}$.
> 4. **Total rms noise is lower for 45 nm** — Despite $\gamma$ being 3× higher, the $g_m r_{ds}$ product drops by 5×, so the total noise multiplier ($\gamma g_m r_{ds}$) drops from 15 to 9.17.
> 5. **Technology scaling degrades intrinsic gain** — This is a fundamental challenge: shorter channels have higher $\lambda$, reducing $r_{ds}$ and thus gain. The higher $\gamma$ in nanoscale devices further penalises noise performance relative to the gain achieved.

---

> [!nav]
> [[Problem 2 - Advanced OpAmps|← Problem 2]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Problem 5 - Layout|Problem 5 →]]
