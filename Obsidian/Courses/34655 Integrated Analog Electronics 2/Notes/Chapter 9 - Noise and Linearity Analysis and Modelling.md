---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: literature-note
chapter: 9
source: "T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design, 2nd ed."
pages: "363-412"
tags: [IAE2, noise, linearity, dynamic-range]
---
# Chapter 9 - Noise and Linearity Analysis and Modelling

**Source:** Carusone, Johns & Martin, *Analog Integrated Circuit Design*, Ch. 9, pp. 363-412

> [!abstract] Chapter Overview
> This chapter covers **inherent noise** (thermal, shot, flicker) in electronic components, not interference noise from external sources. Noise sets the **lower limit** on useful signal amplitude, while linearity sets the **upper limit**. Together they define the circuit's **dynamic range**.

---

## 9.1 Time-Domain Analysis

All noise signals are assumed to have a **mean value of zero**.

![[Fig_9.1.png]]
*Fig. 9.1 - Example of a voltage noise signal in the time domain.*

### 9.1.1 Root Mean Square (rms) Value

$$V_{n(\text{rms})} \equiv \left[\frac{1}{T}\int_0^T v_n^2(t)\,dt\right]^{1/2}$$

The rms value indicates the **normalized noise power** of the signal. Applied to a 1-$\Omega$ resistor:

$$P_{\text{diss}} = V_{n(\text{rms})}^2 \quad \text{[watts]}$$

> [!tip] Key Insight
> The rms value obtained by time-averaging the square provides a normalized measure of the noise signal's power, even though the instantaneous value cannot be predicted.

---

### 9.1.2 SNR (Signal-to-Noise Ratio)

$$\text{SNR} = 10\log\left[\frac{\text{signal power}}{\text{noise power}}\right] \text{dB} = 20\log\left[\frac{V_{s(\text{rms})}}{V_{n(\text{rms})}}\right] \text{dB}$$

When signal and noise mean-squared values are equal: SNR = 0 dB.

---

### 9.1.3 Units of dBm

dBm expresses power on a logarithmic scale normalized to **1 mW**:
- 1 mW $\rightarrow$ 0 dBm
- 0.1 mW $\rightarrow$ -10 dBm
- 1 $\mu$W $\rightarrow$ -30 dBm

Voltages can be referenced to dBm by assuming a load (usually 50 $\Omega$ or 75 $\Omega$).

---

### 9.1.4 Noise Summation

For two noise sources $v_{n1}(t)$ and $v_{n2}(t)$ combined:

![[Fig_9.2.png]]
*Fig. 9.2 - Combining two noise sources: (a) voltage, and (b) current.*

$$V_{no(\text{rms})}^2 = V_{n1(\text{rms})}^2 + V_{n2(\text{rms})}^2 + 2\mathbf{C}\,V_{n1(\text{rms})}V_{n2(\text{rms})}$$

where $\mathbf{C}$ is the correlation coefficient ($-1 \leq \mathbf{C} \leq 1$).

> [!important] Uncorrelated Noise Sources
> For **uncorrelated** sources ($\mathbf{C} = 0$), noise powers add directly:
> $$V_{no(\text{rms})}^2 = V_{n1(\text{rms})}^2 + V_{n2(\text{rms})}^2$$
> This means rms values add in a **root-sum-of-squares** fashion. To reduce overall noise, **focus on the largest noise contributors**.

---

## 9.2 Frequency-Domain Analysis

Units of Hz (rather than rad/s) are used throughout for spectral densities.

### 9.2.1 Noise Spectral Density

The **spectral density** $V_n^2(f)$ is the average normalized noise power measured within a 1-Hz bandwidth.
- Units: $\text{V}^2/\text{Hz}$ (spectral density) or $\text{V}/\sqrt{\text{Hz}}$ (root spectral density)
- The mean-squared value at a single precise frequency is zero

![[Fig_9.3.png]]
*Fig. 9.3 - Example of voltage spectral density (frequency domain): (a) spectral density, (b) root spectral density.*

The total mean-squared noise is obtained by integrating:

$$V_{n(\text{rms})}^2 = \int_0^\infty V_n^2(f)\,df$$

> [!note] Wiener-Khinchin Theorem
> $V_n^2(f)$ is rigorously defined as the Fourier transform of the autocorrelation function of the time-domain signal $v_n(t)$.

---

### 9.2.2 White Noise

A noise signal with **constant spectral density** over all frequencies:

$$V_n(f) = V_{nw} = \text{constant}$$

![[Fig_9.4.png]]
*Fig. 9.4 - An example of a white noise signal (flat root spectral density).*

In practice, finite capacitance always band-limits the noise, preventing infinite total power.

---

### 9.2.3 1/f (Flicker) Noise

Spectral density inversely proportional to frequency:

$$V_n^2(f) = \frac{k_v^2}{f}$$

![[Fig_9.5.png]]
*Fig. 9.5 - A noise signal that has both 1/f and white noise, showing the 1/f noise corner.*

| Property | Value |
|----------|-------|
| Spectral density slope | $-10$ dB/decade |
| Root spectral density slope | $-10$ dB/decade for $V_n^2(f)$; $V_n(f) \propto 1/\sqrt{f}$ |
| Power per decade | Constant: $k_v^2\ln(10) \approx 2.3\,k_v^2$ |
| 1/f noise corner | Frequency where 1/f and white noise are equal |

---

### 9.2.4 Filtered Noise

When noise passes through a transfer function $A(s)$:

![[Fig_9.6.png]]
*Fig. 9.6 - Applying a transfer function (i.e. filter) to a noise signal.*

$$V_{no}^2(f) = |A(j2\pi f)|^2 \cdot V_{ni}^2(f)$$

For root spectral density:

$$V_{no}(f) = |A(j2\pi f)| \cdot V_{ni}(f)$$

![[Fig_9.7.png]]
*Fig. 9.7 - Filtered uncorrelated noise sources contributing to total output noise.*

> [!tip] Practical Rule
> A circuit's transfer function shapes the **root** spectral density by its **magnitude response**. Uncorrelated noise sources remain uncorrelated after filtering.

![[Fig_9.8.png]]
*Fig. 9.8 - (a) Spectral density for white noise input. (b) RC filter. (c) RC filter frequency response. (d) Shaped output spectral density.*

---

### 9.2.5 Noise Bandwidth

The **noise bandwidth** $f_x$ of a filter is the width of a brick-wall filter with the same rms output noise and same peak gain.

![[Fig_9.9.png]]
*Fig. 9.9 - (a) A first-order low-pass response, and (b) a brick-wall filter with the same peak gain and area.*

For a **first-order low-pass filter** with 3-dB bandwidth $f_0$:

$$f_x = \frac{\pi}{2}f_0 = \frac{1}{4R_{\text{eq}}C}$$

Total output mean-squared noise (white noise input):

$$V_{no(\text{rms})}^2 = V_{nw}^2 \cdot \frac{\pi}{2} f_0$$

---

### 9.2.6 Piecewise Integration of Noise

Approximate total noise by integrating under piecewise-linear Bode diagrams. Break the spectrum into regions where the spectral density has a simple slope, integrate each region, and sum.

![[Fig_9.10.png]]
*Fig. 9.10 - Root spectral densities and amplifier curve example. $V_{no}(f)$ is the output noise from applying input noise $V_{ni}(f)$ through amplifier $A(s)$.*

---

### 9.2.7 1/f Noise Tangent Principle

> [!abstract] 1/f Tangent Principle
> To find the dominant noise region: lower a 1/f noise line until it touches the spectral density curve. The total noise can be approximated by the noise in the vicinity of where the 1/f line touches.
>
> This works because a $1/x$ curve contributes constant power per decade, so the largest power contribution is where the spectral density is highest.

---

## 9.3 Noise Models for Circuit Elements

Three fundamental noise mechanisms: **thermal**, **shot**, and **flicker**.

| Mechanism | Nature | Bias Dependent? | Spectrum |
|-----------|--------|-----------------|----------|
| **Thermal** | Random carrier excitation in conductors | No | White |
| **Shot** | Discrete carrier flow across junctions | Yes ($\propto I_D$) | White |
| **Flicker** | Carrier trapping/release in semiconductors | Yes (requires DC current) | 1/f |

![[Fig_9.11.png]]
*Fig. 9.11 - Circuit elements and their noise models. Note that capacitors and inductors do not generate noise.*

---

### 9.3.1 Resistors

Thermal noise modeled as a **voltage source in series** or **current source in parallel**:

| Model | Spectral Density |
|-------|-----------------|
| Thevenin (voltage) | $V_R^2(f) = 4kTR$ |
| Norton (current) | $I_R^2(f) = 4kT/R$ |

A 1-k$\Omega$ resistor at room temperature has a root spectral density of $\approx 4.06\;\text{nV}/\sqrt{\text{Hz}}$.

> [!tip] Rule of Thumb
> $V_R(f) = \sqrt{\frac{R}{1\,\text{k}\Omega}} \times 4.06\;\text{nV}/\sqrt{\text{Hz}}$ at 27 $^\circ$C

---

### 9.3.2 Diodes

Shot noise modeled as a **current source in parallel** with the small-signal resistance:

$$I_d^2(f) = 2qI_D$$

where $q = 1.6\times10^{-19}$ C and $r_d = kT/(qI_D)$.

---

### 9.3.3 Bipolar Transistors

Two equivalent noise sources at the base:

| Source | Spectral Density |
|--------|-----------------|
| Input voltage noise | $V_i^2(f) = 4kT\left(r_b + \frac{1}{2g_m}\right)$ |
| Input current noise | $I_i^2(f) = 2q\left(I_B + \frac{KI_B}{f} + \frac{I_C}{|\beta(f)|^2}\right)$ |

Dominated by **$r_b$ thermal noise** (voltage) and **base-current shot noise** (current). These two sources are typically treated as uncorrelated.

---

### 9.3.4 MOSFETs

Two noise sources - flicker and thermal:

| Source | Spectral Density |
|--------|-----------------|
| **Flicker** (gate-referred voltage) | $V_g^2(f) = \frac{K}{WLC_{ox}f}$ |
| **Thermal** (drain current) | $I_d^2(f) = 4kT\gamma g_m$ |

where $\gamma = 2/3$ for long-channel devices (higher for short-channel).

> [!important] MOSFET Noise Design Rules
> - **1/f noise** is inversely proportional to gate area $WL$ $\Rightarrow$ use **large transistors**
> - **p-channel** transistors typically have **less 1/f noise** than n-channel
> - **Thermal noise** is proportional to $g_m$ $\Rightarrow$ equivalent to a resistor of value $r_{ds}$ in triode
> - 1/f noise constant $K$ varies widely for different devices in the same process

**Simplified input-referred model** (valid at low and moderate frequencies):

$$V_i^2(f) = 4kT\left(\frac{2}{3}\right)\frac{1}{g_m} + \frac{K}{WLC_{ox}f}$$

---

### 9.3.5 Opamps

Three uncorrelated input-referred noise sources:
- $V_n(f)$: input voltage noise
- $I_{n-}(f)$: negative input current noise
- $I_{n+}(f)$: positive input current noise

![[Fig_9.12.png]]
*Fig. 9.12 - Opamp circuits showing the need for three noise sources in an opamp noise model.*

For MOSFET input stages, the current noises are often negligible at low frequencies.

---

### 9.3.6 Capacitors and Inductors

Capacitors and inductors **do not generate noise** but accumulate noise from other sources.

![[Fig_9.13.png]]
*Fig. 9.13 - (a) Capacitor $C$ in parallel with a resistor, and (b) equivalent noise model circuit.*

> [!warning] kT/C Noise - Fundamental Limit
> For a capacitor $C$ in parallel with any resistance $R$:
> $$V_{no(\text{rms})}^2 = \frac{kT}{C}$$
> This result is **independent of $R$**! It sets a fundamental noise floor for sampled-data circuits. At 300 K, achieving 96-dB dynamic range with 1 V signals requires $C \geq 16.6$ pF.

For an inductor $L$ in parallel with any resistance:

$$I_{no(\text{rms})}^2 = \frac{kT}{L}$$

---

### 9.3.7 Sampled Signal Noise

![[Fig_9.14.png]]
*Fig. 9.14 - A sample-and-hold circuit.*

Sampling an analog voltage onto a capacitor captures both signal and noise with mean-square value $kT/C$.

- Noise is **independent of sampling rate**
- **Oversampling** (averaging $N$ samples) reduces noise by $\sqrt{N}$

---

### 9.3.8 Input-Referred Noise

> [!abstract] Definition
> The **input-referred noise** is the noise that, applied to the input of a noiseless copy of the circuit, produces the same output noise as the actual circuit. Found by dividing the output noise by the circuit's gain:
> $$v_{\text{in(rms)}} = v_{\text{on(rms)}}/A$$

![[Fig_9.15.png]]
*Fig. 9.15 - Determination of input-referred noise for voltage amplifier and transimpedance amplifier.*

**Noise factor** and **noise figure**:

$$F(f) = \frac{v_{ao}^2(f)}{4kTR_s|A(f)|^2} = 1 + \frac{v_{ai}^2(f)}{4kTR_s}$$

$$\text{NF}(f) = 10\log_{10}[F(f)] \;\text{dB}$$

> [!tip] Cascade Noise Rule
> In a cascade of amplifiers, the **first stage dominates** the overall noise performance. Place the **lowest-noise, highest-gain** amplifier first.

![[Fig_9.16.png]]
*Fig. 9.16 - Computing the input-referred noise: placing the low-noise, high-gain amplifier first yields lower total noise.*

![[Fig_9.17.png]]
*Fig. 9.17 - Separating noise contributed by the source resistance and circuit noise.*

---

## 9.4 Noise Analysis Examples

### 9.4.1 Opamp Example (Inverting Amplifier)

![[Fig_9.18.png]]
*Fig. 9.18 - (a) Low-pass filter, and (b) equivalent noise model.*

For an inverting amplifier with feedback capacitor $C_f$ and resistor $R_f$:
- Noise from resistor current sources is shaped by a low-pass with $f_0 = 1/(2\pi R_f C_f)$
- Integrated output noise due to $R_f$ alone: $kT/C_f$
- Including $R_1$ increases noise by factor $(1 + R_f/R_1)$
- Opamp noise contributes additional terms
- $R_2$ (at positive input) adds both thermal noise and amplifies opamp current noise - eliminate $R_2$ in low-noise designs

---

### 9.4.2 Bipolar Common-Emitter Example

![[Fig_9.19.png]]
*Fig. 9.19 - A bipolar common-emitter amplifier with noise sources.*

Total input-referred noise:

$$V_{i,\text{total}}^2(f) = 4kT\left[R_S + r_b + \frac{1}{2g_m} + \frac{g_m(R_S + r_b)^2}{2\beta}\right]$$

**Optimum bias current** (minimizes input noise):

$$I_{C,\text{opt}} = \frac{kT}{q}\frac{\sqrt{\beta}}{R_S + r_b}$$

$$g_{m,\text{opt}} = \frac{\sqrt{\beta}}{R_S + r_b}$$

> [!note] Design Guideline
> Even with zero source resistance, thermal noise from $r_b$ dominates. Reduce $r_b$ by using **larger transistors** or **multiple parallel transistors**.

---

### 9.4.3 CMOS Differential Pair Example

![[Fig_9.20.png]]
*Fig. 9.20 - A CMOS input stage for a traditional opamp with MOSFET noise sources shown.*

For a differential pair (Q1, Q2) with current mirror load (Q3, Q4):

**Thermal noise** (input-referred):

$$V_{neq}^2(f) = 2\cdot 4kT\gamma\frac{1}{g_{m1}} + 2\cdot 4kT\gamma\left(\frac{g_{m3}}{g_{m1}}\right)^2\frac{1}{g_{m3}}$$

$$= \frac{8kT\gamma}{g_{m1}}\left(1 + \frac{g_{m3}}{g_{m1}}\right)$$

> [!important] Minimizing Noise in CMOS Diff Pair
> **Thermal noise:**
> - Maximize $g_{m1}$ (input pair transconductance)
> - Minimize $g_{m3}$ (load pair transconductance)
> - This implies: small $V_{\text{eff},1}$, large $V_{\text{eff},3}$ (weak inversion for input pair)
>
> **1/f noise:**
> - Make input transistors **wide** ($W_1$ large) and load transistors with **long** channels ($L_3$ large)
> - Use **p-channel input** transistors (lower $K$)

**1/f noise** (input-referred):

$$V_{ni}^2(f) = \frac{2}{C_{ox}f}\left[\frac{K_i}{W_i L_i} + \left(\frac{\mu_n}{\mu_p}\right)\frac{K_3 L_i}{W_i L_3^2}\right]$$

---

### 9.4.4 Fiber-Optic Transimpedance Amplifier Example

![[Fig_9.21.png]]
*Fig. 9.21 - A fiber-optic transresistance preamp.*

![[Fig_9.22.png]]
*Fig. 9.22 - A simplified model for a CMOS fiber-optic preamp with noise sources.*

![[Fig_9.23.png]]
*Fig. 9.23 - A simplified small-signal model used for noise analysis.*

Key design trade-offs for a CMOS fiber-optic preamp:
- $R_F$ should be as large as possible to minimize feedback resistor noise ($4kT/R_F$)
- Bandwidth constraint: $\omega_{-3\text{dB}} = (1 + A_V)/(R_F C_T)$
- Thermal noise of input transistor Q1 is amplified at high frequencies (peaking effect)
- Optimal design: choose $C_{gs} = C_{in}$ (match gate-source capacitance to detector capacitance)

---

## 9.5 Dynamic Range Performance

Noise limits the **smallest** useful signal; linearity limits the **largest**. Dynamic range is the ratio between them.

### 9.5.1 Total Harmonic Distortion (THD)

For a nonlinear system with Taylor series expansion $v_o(t) = a_1 v_{in} + a_2 v_{in}^2 + a_3 v_{in}^3 + \cdots$, applying a sinusoidal input produces harmonics.

**Third-order harmonic distortion** (dominant in differential circuits):

$$\text{HD}_3 = \left(\frac{a_3}{a_1}\right)\left(\frac{A^2}{4}\right)$$

**Total Harmonic Distortion:**

$$\text{THD} = 10\log\left(\frac{H_{D2}^2 + H_{D3}^2 + H_{D4}^2 + \cdots}{H_{D1}^2}\right) \;\text{dB}$$

> [!warning] THD Limitation
> THD works well only when the fundamental frequency is well below the circuit's passband limit. Harmonics falling outside the passband get attenuated, giving a falsely good THD reading.

---

### 9.5.2 Third-Order Intercept Point (IP3)

Uses a **two-tone intermodulation test** to characterize third-order distortion near the passband edge.

With two equal-amplitude tones at $\omega_1$ and $\omega_2$ ($\Delta\omega$ small):
- Intermodulation products appear at $\omega_1 \pm \Delta\omega$ and $\omega_2 \pm \Delta\omega$ (in-band!)
- Fundamental rises at 1 dB/dB; intermodulation rises at 3 dB/dB

$$\text{ID}_3 = \left(\frac{a_3}{a_1}\right)\left(\frac{3A^2}{4}\right)$$

![[Fig_9.24.png]]
*Fig. 9.24 - Graphical illustration of the third-order intercept point. $\text{IIP}_3$ and $\text{OIP}_3$ are the input and output third-order intercept points.*

**Relationship between OIP3, signal level, and intermodulation:**

$$\text{OIP}_3 = I_{D1} - \frac{\text{ID}_3}{2} \quad \text{(all in dB)}$$

> [!note] HD3 vs ID3
> $\text{ID}_3 = 3\,\text{HD}_3$ (i.e., 9.5 dB worse). The intermodulation test is more conservative.

---

### 9.5.3 Spurious-Free Dynamic Range (SFDR)

![[Fig_9.25.png]]
*Fig. 9.25 - Graphical illustration of spurious-free dynamic range (SFDR).*

SFDR is the SNR when the distortion power equals the noise power:

$$\text{SFDR} = \frac{2}{3}(\text{OIP}_3 - N_o) \quad \text{[dB]}$$

where $N_o$ is the output noise power in dBm.

---

### 9.5.4 Signal-to-Noise and Distortion Ratio (SNDR)

$$\text{SNDR} = 10\log\left(\frac{V_1^2}{N_o + V_{h2}^2 + V_{h3}^2 + V_{h4}^2 + \cdots}\right)$$

- At **low signal levels**: SNDR $\approx$ SNR (noise dominates)
- At **high signal levels**: SNDR $\approx$ 1/THD (distortion dominates)
- $\text{SNDR}_{\text{max}}$ occurs at an optimal signal amplitude

![[Fig_9.26.png]]
*Fig. 9.26 - Variation of SNDR with signal amplitude in an analog circuit.*

---

## Summary of Noise Models

| Element              | Noise Model                | Spectral Density                            |
| -------------------- | -------------------------- | ------------------------------------------- |
| **Resistor** ($R$)   | Voltage source in series   | $V_R^2(f) = 4kTR$                           |
| **Resistor** ($R$)   | Current source in parallel | $I_R^2(f) = 4kT/R$                          |
| **Diode**            | Current source in parallel | $I_d^2(f) = 2qI_D$                          |
| **BJT** (voltage)    | Voltage at base            | $V_i^2(f) = 4kT(r_b + 1/2g_m)$              |
| **BJT** (current)    | Current at base            | $I_i^2(f) = 2q(I_B + KI_B/f + I_C/\beta^2)$ |
| **MOSFET** (flicker) | Voltage at gate            | $V_g^2(f) = K/(WLC_{ox}f)$                  |
| **MOSFET** (thermal) | Current drain-source       | $I_d^2(f) = 4kT\gamma g_m$                  |
| **Capacitor** ($C$)  | rms voltage                | $V_{no}^2 = kT/C$                           |
| **Inductor** ($L$)   | rms current                | $I_{no}^2 = kT/L$                           |


---

## Key Design Guidelines

> [!abstract] Noise Reduction Strategies
> 1. **Focus on the largest noise contributor** - reducing smaller sources has minimal effect (root-sum-of-squares)
> 2. **Maximize first-stage gain** - subsequent stage noise is divided by the first-stage gain
> 3. **Use large gate areas** ($WL$) for MOSFETs to minimize 1/f noise
> 4. **Prefer p-channel input transistors** for lower 1/f noise
> 5. **Maximize input pair $g_m$** in differential amplifiers (low $V_{\text{eff}}$, high $W/L$)
> 6. **Don't over-design bandwidth** - excess bandwidth admits more noise
> 7. **Noise bandwidth** of a first-order filter is $\pi/2$ times the -3 dB bandwidth
> 8. **kT/C** sets a fundamental noise floor for sampled-data circuits

---

> [!nav]
> &nbsp;
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Lecture 1 - Introduction and Prerequisites|Lecture 1 - Prerequisites]]
