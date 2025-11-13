> Quick refs: [[Courses/DSP/Formulas/Bilinear Transform & Prewarping]] · [[Courses/DSP/Formulas/Butterworth & High-Pass Prototypes]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 10 Torsdag.pdf]]  
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 10 Torsdag solutions.pdf]]  
> Slides: [[62743 E25 Digital filter design IIR part3.pdf]]
---

> Quick refs: [[Digital Filter Design — IIR (Part 3)]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 10 Torsdag.pdf]]

---

# Week 10 — IIR Highpass + Bandpass (Bilinear Transform)

---

## 📘 Concept Overview
This exercise continues the IIR filter design workflow using the **bilinear transform (BLT)**, this time for:

- **Highpass** filter design (Exercises 1-A → 1-F)  
- **Bandpass** filter design (Exercises 2-A → 2-F)  

The same BLT identity applies (Slides 113–130 in Part 3 slides):

$$
s = \frac{2}{T_s}\,\frac{z-1}{z+1}
$$

Frequency warping remains nonlinear:

$$
\Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)
$$

Both highpass and bandpass designs require:

1️⃣ Convert digital specs → **normalized digital angular frequencies**  
2️⃣ Prewarp → **analog passband/stopband edges**  
3️⃣ Choose a **prototype** (Butterworth or Chebyshev)  
4️⃣ Apply the correct **frequency transformation** (LP→HP or LP→BP)  
5️⃣ Apply the **bilinear transform**  
6️⃣ Verify with magnitude plots  
7️⃣ Extract the **difference equation**

---

# 🟦 **Exercise 1 — Highpass filter**

---

## 1-A) Digital requirements → $T_s$, $\omega_p$, $\omega_s$

> **Given**  
> - IIR highpass filter  
> - Sampling frequency: $F_s = 200~\mathrm{Hz}$  
> - Normalized digital passband: $f_p = 30\;\mathrm{Hz}\cdot T_s$  
> - Normalized digital stopband: $f_s = 20\;\mathrm{Hz}\cdot T_s$  
> - Passband attenuation: $A_p = 1/\sqrt{2}$  
> - Stopband attenuation: $A_s = 0.3$

> **Task**  
> - Determine the sampling time $T_s$  
> - Determine $\omega_p$  
> - Determine $\omega_s$

> [!theory] **Theory (Slides 113–115)**  
> $T_s = 1/F_s$  
> Normalized digital frequency (cycles/sample):  
> $f_\text{norm} = f\cdot T_s$  
> Angular frequency (rad/sample):  
> $\omega = 2\pi f_\text{norm}$

**Your calculations**
- $T_s =$ …  
- $f_p =$ …  
- $f_s =$ …  
- $\omega_p =$ …  
- $\omega_s =$ …

> [!code]- MATLAB
> ```matlab
> % 1-A placeholder
> Fs = 200;
> Ts = 1/Fs;
> fp_norm = 30*Ts;
> fs_norm = 20*Ts;
> wp = 2*pi*fp_norm;
> ws = 2*pi*fs_norm;
> fprintf('Ts=%.6f, wp=%.6f, ws=%.6f\n', Ts, wp, ws);
> ```

---

## 1-B) Analog requirements → $\Omega_p,\;F_p,\;\Omega_s,\;F_s$

> **Task**  
> Prewarp the digital frequencies to obtain analog passband/stopband edges.

> [!theory] **Theory (Slides 115–117)**  
> $$
> \Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)
> $$

**Your calculations**
- $\Omega_p =$ …  
- $\Omega_s =$ …  
- $F_p = \Omega_p/(2\pi)$  
- $F_s = \Omega_s/(2\pi)$

> [!code]- MATLAB
> ```matlab
> % 1-B placeholder
> alpha = 2/Ts;
> Op = alpha * tan(wp/2);
> Os = alpha * tan(ws/2);
> Fp = Op/(2*pi);
> Fs_analog = Os/(2*pi);
> ```

---

## 1-C) Analog Butterworth HP (3rd order)

> **Given**  
> 3rd-order Butterworth prototype (ε=1), from appendix:  
> $$
> H_p(s) = \frac{1}{s^3 + 2s^2 + 2s + 1}
> $$

> **Tasks**  
> - Confirm that order 3 satisfies the attenuation requirements  
> - Write the prototype  
> - Apply LP→HP transform  
> - Compute the transformed transfer function  
> - Plot the **linear** magnitude vs analog frequency  
> - Verify cutoff and stopband frequencies

> [!theory] **Theory (Slides 117–120)**  
> HP transform:  
> $$
> s \leftarrow \frac{\Omega_c}{s}
> $$  
> Then substitute into $H_p(s)$ and simplify.

**Derivations**
- $H_p(s) =$ …  
- LP→HP: $H_\text{HP}(s) =$ …

> [!code]- MATLAB
> ```matlab
> % 1-C placeholder for LP→HP
> Bp = 1;
> Ap = [1 2 2 1];
> Wc = Op;
> [B_HP, A_HP] = lp2hp(Bp, Ap, Wc);
>
> f = linspace(0, ???, ???);
> w = 2*pi*f;
> H = freqs(B_HP, A_HP, w);
> % dark-theme plot here (same style as Tuesday)
> ```

---

## 1-D) Bilinear transform → digital HP $H_d(z)$

> **Task**  
> Apply BLT and compute  
> $$
> H_d(z)=\frac{b_0+b_1z^{-1}+b_2z^{-2}+b_3z^{-3}}
> {1+a_1z^{-1}+a_2z^{-2}+a_3z^{-3}}
> $$

> [!theory] **Theory (Slides 122–125)**  
> $$
> s=\frac{2}{T_s}\frac{z-1}{z+1}
> $$  
> Must be able to derive coefficients **manually**.

> [!code]- MATLAB
> ```matlab
> % 1-D placeholder
> [Bz, Az] = bilinear(B_HP, A_HP, Fs);
> ```

---

## 1-E) Verify digital HP response

> Plot magnitude using `freqz`  
> Confirm passband and stopband behavior.

> [!code]- MATLAB
> ```matlab
> % 1-E placeholder
> [Hd,fHz] = freqz(Bz,Az,4096,Fs);
> % dark plot
> ```

---

## 1-F) Difference equation

> Extract the time-domain equation:
> $$
> y[n] = -a_1y[n-1] - a_2y[n-2] - a_3y[n-3]
>       + b_0x[n] + b_1x[n-1] + b_2x[n-2] + b_3x[n-3]
> $$

> [!code]- MATLAB
> ```matlab
> % 1-F placeholder
> fprintf("y[n] = ...\n");
> ```

---

# 🟩 **Exercise 2 — Bandpass filter**

---

## 2-A) Digital BP specs → $\omega_{pL},\omega_{pH}$

> **Given**  
> $F_s = 120~\text{Hz}$  
> $f_{pL} = 15\,\text{Hz}\cdot T_s$  
> $f_{pH} = 25\,\text{Hz}\cdot T_s$

> **Task**  
> Compute the lower and upper normalized angular passband frequencies.

> [!code]- MATLAB
> ```matlab
> % 2-A placeholder
> Fs2 = 120;
> Ts2 = 1/Fs2;
> fpL = 15*Ts2;
> fpH = 25*Ts2;
> wpL = 2*pi*fpL;
> wpH = 2*pi*fpH;
> ```

---

## 2-B) Prewarp lower/upper analog edges

> [!code]- MATLAB
> ```matlab
> % 2-B placeholder
> alpha2 = 2/Ts2;
> OpL = alpha2*tan(wpL/2);
> OpH = alpha2*tan(wpH/2);
> ```

---

## 2-C) Chebyshev type-1 (order 1) → Analog BP

> **Given**  
> Chebyshev (ε=0.5088) prototype:  
> $$
> H_p(s)=\frac{1.9652}{s+1.9652}
> $$

> **Tasks**  
> - Write the prototype  
> - Perform LP→BP transform  
> - Plot magnitude using `freqs`  
> - Verify passband edges

---

## 2-D) Bilinear transform → digital BP

---

## 2-E) Verify digital BP response

---

## 2-F) Difference equation

---

# References
- Lecture slides: *Digital Filter Design — IIR Part 3*  
- Exercise sheet: *Uge 10 Torsdag*  
