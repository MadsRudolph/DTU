# 🎯 62743 DSP — Mock Exam (Claude Edition)

**Course:** 62743 Digital Signal Processing (DTU)  
**Time:** 4 hours (no aids except formula sheet)  
**Total Points:** 100  
**Date:** Practice Exam — December 2025

---

## 📋 Exam Overview

| Problem | Topic | Points | Key Skills |
|---------|-------|--------|------------|
| 1 | LTI System Analysis | 25 | Step→Impulse, H(z), Cascade, Inverse |
| 2 | IIR Butterworth Highpass via BLT | 25 | Prewarping, Order calc, bilinear |
| 3 | Sampling & Min-Phase Decomposition | 25 | Aliasing, All-Pass factorization |
| 4 | FIR Bandstop via Window Method | 25 | Ideal h[n], Linear phase, Symmetry |

---

# Problem 1 — LTI System Analysis (25 points)

An LTI system $\mathcal{S}$ has the following **step response** (output when input is the unit step $u[n]$):

$$
y_{step}[n] = 2\delta[n] + 3\delta[n-1] - 3\delta[n-2] - 2\delta[n-3]
$$

The system is known to be a cascade of two FIR filters:
$$
H(z) = H_1(z) \cdot H_2(z)
$$
where $H_1(z) = 1 + z^{-1}$.

---

## 1-1) Find the impulse response $h[n]$ (5 points)

Determine the impulse response $h[n]$ of the system from the given step response.

> [!hint]- Hint 1-1
> Use the fundamental LTI relationship:
> $$\delta[n] = u[n] - u[n-1]$$
> Therefore: $h[n] = y_{step}[n] - y_{step}[n-1]$
> 
> Compute sample by sample for $n = 0, 1, 2, 3, 4$.

**Your answer:**

$$h[n] = \underline{\hspace{8cm}}$$

![[Images/Mock_Exam_1_ImpulseResponse.png]]

---

## 1-2) Find the system function $H(z)$ (5 points)

From your impulse response, write the system function $H(z)$.

> [!hint]- Hint 1-2
> For a causal FIR filter:
> $$H(z) = \sum_{n=0}^{N-1} h[n] z^{-n}$$
> 
> Simply read off the coefficients from $h[n]$.

**Your answer:**

$$H(z) = \underline{\hspace{8cm}}$$

---

## 1-3) Find the magnitude and phase response using symmetry (5 points)

Determine $|H(\omega)|$ and $\angle H(\omega)$.

> [!hint]- Hint 1-3
> **The Symmetry Trick:**
> 1. Check if $h[n]$ is symmetric around its center
> 2. Factor out $e^{-j\omega K}$ where $K = (N-1)/2$
> 3. Group remaining terms into cosines using Euler: $e^{j\theta} + e^{-j\theta} = 2\cos\theta$
> 4. **CRITICAL:** Verify the amplitude function $A(\omega) \geq 0$ before claiming linear phase!

**Your answer:**

$$|H(\omega)| = \underline{\hspace{6cm}}$$

$$\angle H(\omega) = \underline{\hspace{6cm}}$$

![[Images/Mock_Exam_1_MagPhase.png]]

---

## 1-4) Find $H_2(z)$ in the cascade (5 points)

Given that $H(z) = H_1(z) \cdot H_2(z)$ with $H_1(z) = 1 + z^{-1}$, find $H_2(z)$.

> [!hint]- Hint 1-4
> Use polynomial division (deconvolution):
> $$H_2(z) = \frac{H(z)}{H_1(z)}$$
> 
> In MATLAB: `[H2, rem] = deconv(H_coeffs, H1_coeffs);`
> 
> The remainder should be zero (or near-zero).

**Your answer:**

$$H_2(z) = \underline{\hspace{8cm}}$$

![[Images/Mock_Exam_1_H2_PZ.png]]

---

## 1-5) Inverse system stability (5 points)

Consider the inverse system $H_{inv}(z) = 1/H(z)$.

- Can $H_{inv}(z)$ be both **causal** and **stable**?
- Justify your answer using the pole-zero plot.

> [!hint]- Hint 1-5
> For the inverse system:
> - Poles of $H_{inv}(z)$ = Zeros of $H(z)$
> - Zeros of $H_{inv}(z)$ = Poles of $H(z)$
> 
> **Stability criterion:** All poles must be inside the unit circle.
> 
> Check: Are all zeros of $H(z)$ inside $|z| < 1$?

**Your answer:**

$$\underline{\hspace{10cm}}$$

---

# Problem 2 — IIR Butterworth Highpass via BLT (25 points)

Design a **digital highpass Butterworth filter** with the following specifications:

| Parameter | Value |
|-----------|-------|
| Sampling frequency | $F_s = 8000$ Hz |
| Passband edge | $F_p = 2000$ Hz |
| Stopband edge | $F_s = 1000$ Hz |
| Passband ripple | $A_p = 1$ dB |
| Stopband attenuation | $A_s = 20$ dB |

---

## 2-1) Pre-warp the frequencies (5 points)

Calculate the pre-warped analog frequencies $\Omega_p$ and $\Omega_s$.

> [!hint]- Hint 2-1
> **Pre-warping formula:**
> $$\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2 F_s \tan\left(\frac{\pi F}{F_s}\right)$$
> 
> This compensates for the frequency warping introduced by the bilinear transform.
> 
> **NEVER** use Hz frequencies directly in analog prototype formulas!

**Your answer:**

$$\Omega_p = \underline{\hspace{4cm}} \text{ rad/s}$$

$$\Omega_s = \underline{\hspace{4cm}} \text{ rad/s}$$

---

## 2-2) Calculate the minimum filter order (5 points)

Determine the minimum Butterworth order $N$ that meets the specifications.

> [!hint]- Hint 2-2
> **Butterworth order formula:**
> $$N \geq \frac{\log_{10}\left(\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\log_{10}(\Omega_s/\Omega_p)}$$
> 
> **For highpass:** The ratio is $\Omega_p/\Omega_s$ (inverted!) because $\Omega_p > \Omega_s$.
> 
> Round UP to the nearest integer.

**Your answer:**

$$N = \underline{\hspace{3cm}}$$

---

## 2-3) Design the analog lowpass prototype (5 points)

Write the transfer function of the normalized Butterworth lowpass prototype $H_{LP}(s)$ of order $N$.

> [!hint]- Hint 2-3
> Use the Butterworth pole formula or the appendix tables.
> 
> For order $N$, poles are at:
> $$s_k = e^{j\pi(2k+N-1)/(2N)}, \quad k = 1, 2, \ldots, N$$
> 
> The normalized prototype has $\Omega_c = 1$ rad/s.

**Your answer:**

$$H_{LP}(s) = \underline{\hspace{8cm}}$$

---

## 2-4) Transform to analog highpass (5 points)

Apply the LP→HP transformation to get $H_{HP}(s)$.

> [!hint]- Hint 2-4
> **LP → HP transformation:**
> $$s \rightarrow \frac{\Omega_p}{s}$$
> 
> In MATLAB: `[B_HP, A_HP] = lp2hp(B_proto, A_proto, Omega_p);`

**Your answer:**

$$H_{HP}(s) = \underline{\hspace{8cm}}$$

![[Images/Mock_Exam_2_Analog_HP.png]]

---

## 2-5) Apply bilinear transform and verify (5 points)

Apply the bilinear transform to get the digital filter $H_{HP}(z)$.

Verify that the filter meets specifications at the passband and stopband edges.

> [!hint]- Hint 2-5
> **Bilinear transform:**
> $$s = \frac{2}{T_s} \cdot \frac{z-1}{z+1}$$
> 
> In MATLAB: `[Bz, Az] = bilinear(B_HP, A_HP, Fs);`
> 
> Check attenuation at $F_p$ and $F_s$ using `freqz`.

**Your answer:**

| Frequency | Spec | Achieved |
|-----------|------|----------|
| $F_p = 2000$ Hz | $\geq -1$ dB | ___ dB |
| $F_s = 1000$ Hz | $\leq -20$ dB | ___ dB |

![[Images/Mock_Exam_2_Digital_HP.png]]

---

# Problem 3 — Sampling & Min-Phase Decomposition (25 points)

Consider the continuous-time signal:

$$
x_a(t) = 4\cos(2\pi \cdot 500 \cdot t) + 2\cos(2\pi \cdot 1200 \cdot t) + \cos(2\pi \cdot 1800 \cdot t)
$$

---

## 3-1) Determine the Nyquist rate (3 points)

What is the minimum sampling frequency required to avoid aliasing?

> [!hint]- Hint 3-1
> **Nyquist criterion:** $F_s > 2 F_{max}$
> 
> Find the highest frequency component in $x_a(t)$.

**Your answer:**

$$F_{Nyquist} = \underline{\hspace{4cm}} \text{ Hz}$$

---

## 3-2) Sample at $F_s = 3000$ Hz — Sketch spectrum (7 points)

The signal is sampled at $F_s = 3000$ Hz.

- Does aliasing occur?
- Sketch the spectrum $X(e^{j\omega})$ for $\omega \in [-\pi, \pi]$.
- Mark all frequency components with their amplitudes.

> [!hint]- Hint 3-2
> **Digital frequency:** $\omega = 2\pi \frac{F}{F_s}$
> 
> Convert each analog frequency to digital:
> - 500 Hz → $\omega = ?$
> - 1200 Hz → $\omega = ?$
> - 1800 Hz → $\omega = ?$ (check for aliasing!)
> 
> **Aliasing formula:** If $F > F_s/2$, the aliased frequency is $F_{alias} = F_s - F$

**Your answer:**

![[Images/Mock_Exam_3_Spectrum.png]]

---

## 3-3) Sample at $F_s = 2500$ Hz — Identify aliased components (5 points)

Now the signal is sampled at $F_s = 2500$ Hz.

- Which components alias?
- What are their apparent frequencies after sampling?

> [!hint]- Hint 3-3
> $F_s/2 = 1250$ Hz is the Nyquist frequency.
> 
> Any component $F > 1250$ Hz will fold back:
> $$F_{apparent} = |F - k \cdot F_s|$$
> where $k$ is chosen to bring the result into $[0, F_s/2]$.

**Your answer:**

| Original $F$ | Aliased? | Apparent $F$ |
|--------------|----------|--------------|
| 500 Hz | | |
| 1200 Hz | | |
| 1800 Hz | | |

---

## 3-4) Min-Phase / All-Pass Decomposition (10 points)

Consider the system:

$$
H(z) = \frac{(z - 2)(z - 0.5)}{z^2}
$$

Decompose $H(z)$ into:
$$H(z) = H_{min}(z) \cdot H_{ap}(z)$$

where $H_{min}(z)$ is minimum-phase and $H_{ap}(z)$ is all-pass.

> [!hint]- Hint 3-4
> **Minimum-phase:** All zeros inside unit circle.
> **All-pass:** $|H_{ap}(e^{j\omega})| = 1$ for all $\omega$.
> 
> **The trick:** For each zero $z_0$ outside the unit circle:
> 1. Replace it with its "reflection" $1/z_0^*$ in $H_{min}(z)$
> 2. Add an all-pass factor $H_{ap}(z) = \frac{z^{-1} - z_0^*}{1 - z_0 z^{-1}}$ to compensate
> 
> Here: $z_0 = 2$ is outside. Its reflection is $1/2^* = 0.5$.

**Your answer:**

$$H_{min}(z) = \underline{\hspace{6cm}}$$

$$H_{ap}(z) = \underline{\hspace{6cm}}$$

![[Images/Mock_Exam_3_MinPhase_PZ.png]]

---

# Problem 4 — FIR Bandstop via Window Method (25 points)

Design a **linear-phase FIR bandstop filter** with the following specifications:

| Parameter | Value |
|-----------|-------|
| Sampling frequency | $F_s = 4000$ Hz |
| Lower stopband edge | $F_{s1} = 600$ Hz |
| Upper stopband edge | $F_{s2} = 1000$ Hz |
| Filter length | $N = 21$ taps |
| Window | Hamming |

---

## 4-1) Calculate the digital cutoff frequencies (4 points)

Convert the stopband edges to digital angular frequencies $\omega_{c1}$ and $\omega_{c2}$.

> [!hint]- Hint 4-1
> $$\omega = 2\pi \frac{F}{F_s}$$

**Your answer:**

$$\omega_{c1} = \underline{\hspace{4cm}} \text{ rad/sample}$$

$$\omega_{c2} = \underline{\hspace{4cm}} \text{ rad/sample}$$

---

## 4-2) Write the ideal bandstop impulse response (6 points)

Determine the ideal (infinite-length) impulse response $h_{BS,ideal}[n]$ for a bandstop filter.

> [!hint]- Hint 4-2
> **Bandstop = Allpass − Bandpass**
> 
> $$h_{BS}[n] = \delta[n] - h_{BP}[n]$$
> 
> where the bandpass impulse response is:
> $$h_{BP}[n] = \frac{\sin(\omega_{c2} n) - \sin(\omega_{c1} n)}{\pi n}, \quad n \neq 0$$
> 
> At $n = 0$: $h_{BP}[0] = \frac{\omega_{c2} - \omega_{c1}}{\pi}$
> 
> So: $h_{BS}[0] = 1 - \frac{\omega_{c2} - \omega_{c1}}{\pi}$

**Your answer:**

$$h_{BS,ideal}[n] = \underline{\hspace{8cm}}$$

---

## 4-3) Apply truncation and windowing (5 points)

Truncate the ideal response to $N = 21$ taps and apply a Hamming window.

Give the **center coefficient** $h_{BS}[10]$ and the formula for the causal filter coefficients.

> [!hint]- Hint 4-3
> **Shift for causality:** $K = (N-1)/2 = 10$
> 
> The causal coefficients are:
> $$b[n] = h_{BS,ideal}[n - K] \cdot w[n], \quad n = 0, 1, \ldots, N-1$$
> 
> **Hamming window:** $w[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{N-1}\right)$

**Your answer:**

$$h_{BS}[10] = \underline{\hspace{4cm}}$$

![[Images/Mock_Exam_4_Impulse.png]]

---

## 4-4) Verify linear phase using symmetry (5 points)

Show that the filter has linear phase by demonstrating the symmetry property.

Write the magnitude response $|H(\omega)|$ in terms of cosines.

> [!hint]- Hint 4-4
> For Type I FIR (odd length, symmetric):
> $$H(\omega) = e^{-j\omega K} \cdot A(\omega)$$
> 
> where $A(\omega) = h[K] + 2\sum_{m=1}^{K} h[K-m]\cos(m\omega)$
> 
> **Remember:** Verify $A(\omega) \geq 0$ before claiming $\angle H(\omega) = -K\omega$!

**Your answer:**

$$|H(\omega)| = \underline{\hspace{8cm}}$$

$$\angle H(\omega) = \underline{\hspace{4cm}}$$

---

## 4-5) Plot and verify stopband attenuation (5 points)

Plot the magnitude response in dB.

Measure the attenuation at the center of the stopband ($F = 800$ Hz).

> [!hint]- Hint 4-5
> Use `freqz(b, 1, N_fft, Fs)` to compute the frequency response.
> 
> Convert to dB: $|H|_{dB} = 20\log_{10}|H|$
> 
> The Hamming window provides approximately **40-50 dB** stopband attenuation.

**Your answer:**

Attenuation at 800 Hz: $\underline{\hspace{3cm}}$ dB

![[Images/Mock_Exam_4_Magnitude.png]]

---

# 📊 Answer Summary Sheet

| Problem | Sub | Answer |
|---------|-----|--------|
| 1-1 | $h[n]$ | |
| 1-2 | $H(z)$ | |
| 1-3 | $\|H(\omega)\|$ | |
| 1-4 | $H_2(z)$ | |
| 1-5 | Stable? | |
| 2-1 | $\Omega_p, \Omega_s$ | |
| 2-2 | Order $N$ | |
| 2-5 | Specs met? | |
| 3-1 | $F_{Nyquist}$ | |
| 3-4 | $H_{min}, H_{ap}$ | |
| 4-3 | $h_{BS}[10]$ | |
| 4-5 | Atten @ 800 Hz | |

---

# ✅ Self-Check Before Submission

- [ ] Problem 1: Did you verify $A(\omega) \geq 0$ for linear phase?
- [ ] Problem 2: Did you use **pre-warped** frequencies for analog design?
- [ ] Problem 2: Did you use **LP→HP transform** before BLT?
- [ ] Problem 3: Did you correctly identify aliased frequencies?
- [ ] Problem 4: Is your filter **symmetric** (linear phase)?
- [ ] All figures exported and embedded?

---

**Good luck! 🍀**
