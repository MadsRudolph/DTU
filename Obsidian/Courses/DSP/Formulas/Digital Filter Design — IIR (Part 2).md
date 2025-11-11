> 🔗 [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]]  
> **Quick refs (DSP):** [[Formulas/Week 5 – Tuesday]] · [[Formulas/FIR vs IIR Filters]]

# 🧠 Digital Filter Design — IIR (Part 2)

> [!summary] **Concept**  
> IIR filters are designed by transforming **analog prototype filters** (Butterworth or Chebyshev Type I) into the **digital domain** using the **bilinear transform (BLT)**.  
> The analog prototype provides desired amplitude characteristics, which are frequency-warped and mapped to digital form.

---

## 🧩 1 – FIR vs IIR Recap

| Property | **FIR Filter** | **IIR Filter** |
|:--|:--|:--|
| **Impulse response** | Finite length → zero after M samples | Infinite length → depends on past outputs |
| **Feedback** | None – uses only $x[n]$ | Yes – depends on $y[n\!-\!k]$ |
| **Transfer function** | $H(z)=\sum_{k=0}^{M}b_kz^{-k}$ | $H(z)=\dfrac{\sum_{k=0}^{M}b_kz^{-k}}{1+\sum_{k=1}^{N}a_kz^{-k}}$ |
| **Phase** | Can be linear if $h[n]=h[M-n]$ or $-h[M-n]$ | Non-linear |
| **Stability** | Always stable | Stable iff all poles inside unit circle |
| **Design origin** | Direct from frequency specs | Analog prototype (BW, Cheb, Elliptic) → discrete |
| **Computation** | Many coeffs (no recursion) | Fewer coeffs (recursive) |
| **Numerical robustness** | High | Lower (round-off accumulation) |

**Linear phase requirement for FIR:**  
$$h[n]=\pm h[M-n]$$  
`+` → symmetric, `–` → antisymmetric.

---

## 🧭 2 – From Analog to Digital Domain

### Continuous to Discrete Transform
$$z=e^{sT}$$  
Relates Laplace domain $s$ and Z-domain $z$.

---

### Bilinear Transform (BLT)
$$
s=\frac{2}{T}\frac{z-1}{z+1},\qquad  
z=\frac{1+\tfrac{sT}{2}}{1-\tfrac{sT}{2}}
$$

**Frequency mapping**
$$
\Omega=\frac{2}{T}\tan\!\left(\frac{\omega}{2}\right),
\qquad
\omega=2\tan^{-1}\!\left(\frac{\Omega T}{2}\right)
$$

- Linear for small $\omega$  
- Non-linear → causes **frequency warping**

---

### Linear vs Bilinear Use Cases

| Purpose | Mapping | Comment |
|:--|:--|:--|
| **Sampling theorem (linear)** | $\omega=\Omega T$ | preserves frequency linearity |
| **Filter design (BLT)** | $\omega=2\tan^{-1}(\Omega T/2)$ | avoids aliasing, non-linear mapping |

---

## 💡 3 – Analog Filter Prototypes

### Low-Pass Prototype
$$H_a(s)=\frac{1}{s+1}$$  
Magnitude response:
$$|H_a(j\Omega)|=\frac{1}{\sqrt{1+\Omega^2}}$$  
Phase response:
$$\angle H_a(j\Omega)=-\tan^{-1}\!\Omega$$  
At $\Omega=1$, $|H|=1/\sqrt2 = -3\,\text{dB}$.

---

### Filter Categories (Analog Domain)

| Type | Magnitude Shape |
|:--|:--|
| Low-pass (LP) | passes below $\Omega_p$ |
| High-pass (HP) | passes above $\Omega_p$ |
| Band-pass (BP) | passes $\Omega_{pL}<\Omega<\Omega_{pH}$ |
| Band-stop (BS) | rejects $\Omega_{sL}<\Omega<\Omega_{sH}$ |

---

## 🔀 4 – Prototype Transformations

| Target Filter | Substitution | MATLAB |
|:--|:--|:--|
| **Low-pass → Low-pass** | $s\to s/\Omega_p$ | `lp2lp()` |
| **Low-pass → High-pass** | $s\to \Omega_p/s$ | `lp2hp()` |
| **Low-pass → Band-pass** | $s\to\dfrac{s^2+\Omega_0^2}{sW}$ | `lp2bp()` |
| **Low-pass → Band-stop** | $s\to\dfrac{sW}{s^2+\Omega_0^2}$ | `lp2bs()` |

with  
$W=\Omega_{pH}-\Omega_{pL}$, $\Omega_0=\sqrt{\Omega_{pH}\Omega_{pL}}$

---

## 🎚️ 5 – Butterworth Prototype

### Magnitude Response
$$|H(j\Omega)|^2=\frac{1}{1+\varepsilon^2\Omega^{2n}}$$  

- **$n$** = filter order  
- **$\varepsilon$** = ripple factor  
- **$A_p$**, **$A_s$** = pass/stop attenuation (dB)

### Relations
$$\varepsilon^2=10^{0.1A_p}-1$$  
$$n\ge\frac{\log_{10}\!\left(\frac{10^{0.1A_s}-1}{\varepsilon^2}\right)}{2\log_{10}\upsilon_s}$$  
with $\upsilon_s=\Omega_s/\Omega_p$ for LP, or $\Omega_p/\Omega_s$ for HP.

> [!code]- MATLAB helper  
> ```matlab
> function [n_min,n]=butterworth_order(Ap,As,vs)
> eps2=10.^(0.1*Ap)-1;
> n_min=log10((10.^(0.1*As)-1)./eps2)./(2*log10(vs));
> n=ceil(n_min);
> end
> ```

---

### Prototype Orders
| n | $H(s)$ (ε = 1) |
|:--|:--|
| 1 | $1/(s+1)$ |
| 2 | $1/(s^2+1.4142s+1)$ |
| 3 | $1/(s^3+2s^2+2s+1)$ |
| 4 | $1/(s^4+2.6131s^3+3.4142s^2+2.6131s+1)$ |
| 5 | $1/(s^5+3.2361s^4+5.2361s^3+5.2361s^2+3.2361s+1)$ |

Increasing $n$ → sharper roll-off, slower phase.

---

### Filter Order Example
For $A_p=1$ dB, $A_s=40$ dB, $\upsilon_s=2$:  
$$n=6.64\Rightarrow7$$  

---

## 🧮 6 – Chebyshev Type I Prototype

### Amplitude Response
$$|H(j\Omega)|^2=\frac{1}{1+\varepsilon^2C_n^2(\Omega)}$$

Chebyshev polynomial:
$$
C_n(\Omega)=
\begin{cases}
\cos(n\cos^{-1}\Omega), & |\Omega|\le1\\[4pt]
\cosh(n\cosh^{-1}\Omega), & |\Omega|>1
\end{cases}
$$

### Relations
$$\varepsilon=\sqrt{10^{0.1A_p}-1}$$  
$$n\ge
\frac{\operatorname{acosh}\!\left(
\sqrt{\dfrac{10^{0.1A_s}-1}{10^{0.1A_p}-1}}
\right)}
{\operatorname{acosh}\upsilon_s}
$$  

Chebyshev Type I → ripple in passband, sharper transition than Butterworth.

> [!code]- MATLAB example  
> ```matlab
> [n,Wp]=cheb1ord(Wp,Ws,Ap,As);
> [b,a]=cheby1(n,Ap,Wp,'low');
> freqz(b,a,512,Fs);
> ```

---

### Typical ε Values (0.5 dB ripple)
| n | $H(s)$ |
|:--|:--|
| 1 | $2.8628/(s+2.8628)$ |
| 2 | $1.4314/(s^2+1.4256s+1.5162)$ |
| 3 | $0.7157/(s^3+1.2529s^2+1.5349s+0.7157)$ |

---

## 🔄 7 – Normalized Filter Parameters

| Filter | $\upsilon_p$ | $\upsilon_s$ | Relation |
|:--|:--:|:--:|:--|
| LP | 1 | $\Omega_s/\Omega_p$ | — |
| HP | 1 | $\Omega_p/\Omega_s$ | — |
| BP | 1 | $\dfrac{\Omega_s^2-\Omega_0^2}{\Omega_pW}$ | $W=\Omega_{pH}-\Omega_{pL}$ |
| BS | 1 | $\dfrac{\Omega_pW}{\Omega_s^2-\Omega_0^2}$ | $W=\Omega_{pH}-\Omega_{pL}$ |

---

## ⚙️ 8 – Digital Filter Design via BLT (Steps)

1. **Specs:** $f_p,f_s,A_p,A_s,F_s$  
2. **Pre-warp:** $\Omega_p=2F_s\tan(\pi f_p/F_s)$, $\Omega_s$ similar  
3. **Select prototype:** Butterworth or Chebyshev  
4. **Compute:** $n, \varepsilon$  
5. **Apply:** LP→HP/BP/BS transform  
6. **Apply BLT:** $s=\frac{2}{T}\frac{z-1}{z+1}$  
7. **Verify:** magnitude & phase (`freqz`)

> [!code]- MATLAB pipeline  
> ```matlab
> % Example: digital low-pass Butterworth
> Ap=1; As=40; Fs=90;
> fp=15; fs=25;
> Wp=fp/(Fs/2); Ws=fs/(Fs/2);
> [n,Wn]=buttord(Wp,Ws,Ap,As);
> [b,a]=butter(n,Wn,'low');
> freqz(b,a,512,Fs);
> ```

---

## 🧮 Worked Example — 1st-Order Butterworth via BLT (Slides 104–108)

> [!summary] **Goal**  
> Design a **digital 1st-order Butterworth low-pass** with $f_p = 15~\text{Hz}$ and $F_s = 90~\text{Hz}$ using a normalized analog prototype, pre-warping, and the bilinear transform (BLT).

---

### Step 1 — Digital Filter Specifications

- Filter type: Low-pass, 1st-order (Butterworth)  
- Passband edge: $f_p = 15~\text{Hz}$  
- Sampling frequency: $F_s = 90~\text{Hz}$  

#### Digital normalized passband frequency
$$
f_{p,\mathrm{norm}} = \frac{f_p}{F_s} = \frac{15}{90} = \frac{1}{6}
$$

#### Digital passband angular frequency (not normalized)
*(Linear relation → $\omega = 2\pi f$)*
$$
\omega_p = 2\pi f_p = 2\pi \cdot 15~\text{Hz} = 94.2~\text{rad/s}
$$

> [!note]
> At this point the spec is still **digital** and unwarped; we convert to the analog domain next.

> [!code]- MATLAB
> ```matlab
> fp = 15; Fs = 90;
> omega_p_notnorm = 2*pi*fp        % -> 94.2478 rad/s
> ```

---

### Step 2 — Analog Filter Specifications (Pre-Warping)

The BLT introduces frequency warping, so convert the digital frequency to an analog angular frequency using  
$$
\Omega = 2F_s\tan\!\left(\frac{\pi f}{F_s}\right)
$$
Hence  
$$
\Omega_p = 2\cdot 90 \cdot \tan\!\left(\frac{\pi \cdot 15}{90}\right)
= 180 \cdot \tan\!\left(\frac{\pi}{6}\right)
= 180 \cdot \frac{\sqrt{3}}{3}
\approx 103.9~\text{rad/s}
$$

> [!tip]
> The slides’ plot multiplies the y-axis by $F_s$ to show warping:  
> the digital requirement $2\pi f_p F_s = 94.2$ maps to $\Omega_p ≈ 103.9$.

> [!code]- MATLAB
> ```matlab
> Omega_p = 2*Fs * tan(pi*fp/Fs)   % -> 103.923 rad/s
> ```

---

### Step 3 — Normalized Low-Pass Prototype

Use the 1st-order Butterworth prototype:
$$
H_P(s) = \frac{1}{s + 1}
$$

---

### Step 4 — Transform Prototype to Required Analog LP

Apply the LP → LP transform $s \to s / \Omega_p$:
$$
H_{LP}(s)
= \frac{1}{(s / \Omega_p) + 1}
= \frac{\Omega_p}{s + \Omega_p}
= \frac{103.9}{s + 103.9}
$$

> [!code]- MATLAB
> ```matlab
> b_s = [Omega_p];          % numerator Ωp
> a_s = [1 Omega_p];        % denominator s + Ωp
> ```

---

### Step 5 — Bilinear Transform → Digital $H(z)$

With $T = 1 / F_s$ and $K = 2 / T = 2F_s = 180$:
$$
s = \frac{2}{T}\frac{z - 1}{z + 1}
\quad \Longrightarrow \quad
H(z) = \frac{\Omega_p(1 + z^{-1})}{(K + \Omega_p) + (\Omega_p - K)z^{-1}}
$$

Normalize by $(K + \Omega_p)$ to get standard form:
$$
H(z) = \frac{b_0 + b_1 z^{-1}}{1 + a_1 z^{-1}}
$$
where
$$
b_0 = b_1 = \frac{\Omega_p}{K + \Omega_p}
= \frac{103.9}{283.9}
\approx 0.3660
$$
and
$$
a_1 = \frac{\Omega_p - K}{K + \Omega_p}
= \frac{-76.1}{283.9}
\approx -0.2680
$$
thus
$$
H(z) = \boxed{\frac{0.3660 + 0.3660z^{-1}}{1 - 0.2680z^{-1}}}
$$

> [!code]- MATLAB
> ```matlab
> K  = 2*Fs;
> b0 = Omega_p/(K + Omega_p);
> b  = [b0 b0];
> a  = [1 (Omega_p - K)/(K + Omega_p)];
> [b; a]
>
> % Cross-check with bilinear():
> [bz, az] = bilinear(b_s, a_s, Fs);
> [bz; az]
> ```

---

### Step 6 — Verification

For a 1st-order Butterworth, $|H(e^{j\omega_p})| = 1 / \sqrt{2}$ (≈ −3 dB) at $f_p = 15$ Hz.

> [!code]- MATLAB
> ```matlab
> % Derived filter verification
> figure; freqz(b, a, 512, Fs);
> title('1st-Order Butterworth via BLT (derived)');
>
> % Cross-check with butter()
> [b2, a2] = butter(1, fp/(Fs/2), 'low');
> figure; freqz(b2, a2, 512, Fs);
> title('butter(1, 15/(90/2)) cross-check');
> [b2 a2]   % Matches [0.3660 0.3660], [1 -0.2680]
> ```

---

### ✅ Final Result
$$
\boxed{H(z) = \frac{0.3660 + 0.3660z^{-1}}{1 - 0.2680z^{-1}}}
$$

This matches the slides (104–108):  
**Digital specs → pre-warp → prototype → analog LP → BLT → verification.**

---

## 🧠 MATLAB – Full Solution: 1st-Order Butterworth via BLT (Slides 104–108)

> [!summary] **Description**  
> Complete MATLAB Live Script implementing all steps of the Butterworth design:  
> 1️⃣ Digital specs → 2️⃣ Pre-warp → 3️⃣ Analog prototype → 4️⃣ Bilinear transform → 5️⃣ Verification and −3 dB check.  
> Designed for direct copy–paste into MATLAB or Obsidian Live Code Blocks.

---

> [!code]- MATLAB (Live Script)
> ```matlab
> %% ✅ Full solution — 1st-Order Butterworth via BLT (Slides 104–108)
> clear;
> % ---- Step 1: Digital specs -------------------------------------------------
> fp = 15;                  % passband edge [Hz]
> Fs = 90;                  % sampling frequency [Hz]
> T  = 1/Fs;
> 
> f_p_norm   = fp/Fs;                     % normalized (cycles/sample)
> omega_p    = 2*pi*fp;                   % digital passband angular freq (NOT normalized) [rad/s]
> omega_samp = 2*pi*fp/Fs;                % digital angular freq ON unit circle [rad/sample]
> 
> disp('--- Step 1: Digital specs ---');
> fprintf('f_p / F_s = %g\n', f_p_norm);
> fprintf('omega_p (not normalized) = %.4f rad/s\n', omega_p);
> fprintf('omega on unit circle = %.4f rad/sample\n', omega_samp);
> 
> % ---- Step 2: Pre-warp digital to analog -----------------------------------
> Omega_p = 2*Fs * tan(pi*fp/Fs);         % [rad/s]  (Ω = 2Fs tan(pi f / Fs))
> 
> disp('--- Step 2: Pre-warp ---');
> fprintf('Omega_p = %.4f rad/s\n', Omega_p);
> 
> % ---- Step 3: Normalized analog prototype ----------------------------------
> % Butterworth, 1st order: H_P(s) = 1/(s+1)
> % ---- Step 4: LP -> LP scaling to place cutoff at Omega_p -------------------
> % H_LP(s) = Omega_p / (s + Omega_p)
> b_s = [Omega_p];
> a_s = [1 Omega_p];
> 
> disp('--- Step 3-4: Analog LP prototype at Omega_p ---');
> fprintf('H_LP(s) = %g / (s + %g)\n', Omega_p, Omega_p);
> 
> % ---- Step 5: Bilinear Transform to digital H(z) ----------------------------
> K  = 2/T;                              % = 2*Fs
> b0 = Omega_p/(K + Omega_p);
> b  = [b0 b0];
> a1 = (Omega_p - K)/(K + Omega_p);
> a  = [1 a1];
> 
> % Cross-check with MATLAB's bilinear()
> [bz, az] = bilinear(b_s, a_s, Fs);
> 
> disp('--- Step 5: Digital coefficients ---');
> fprintf('Derived  b = [%.4f  %.4f]\n', b(1), b(2));
> fprintf('Derived  a = [1      %.4f]\n', a1);
> fprintf('bilinear b = [%.4f  %.4f]\n', bz(1), bz(2));
> fprintf('bilinear a = [1      %.4f]\n', az(2));
> 
> % ---- Step 6: Verification --------------------------------------------------
> % A) Magnitude/phase plots
> figure; freqz(b, a, 512, Fs);
> title('1st-Order Butterworth via BLT (derived coefficients)');
> 
> % B) Cross-check with butter()
> [b2, a2] = butter(1, fp/(Fs/2), 'low');
> figure; freqz(b2, a2, 512, Fs);
> title('butter(1, 15/(90/2)) cross-check');
> 
> % C) -3 dB check at fp = 15 Hz (manual evaluation of H(e^jω))
> fp = 15;
> w  = 2*pi*fp/Fs;                % rad/sample
> z1 = exp(-1j*w);                % z^{-1}
> H_at_fp = (b(1) + b(2)*z1) / (1 + a(2)*z1);
> mag_db  = 20*log10(abs(H_at_fp));
> 
> fprintf('At fp = %.1f Hz -> |H(e^(j*w))| = %.6f  (%.2f dB)\n', ...
>         fp, abs(H_at_fp), mag_db);
> 
> fgrid = linspace(0, Fs/2, 1000);
> Hgrid = freqz(b, a, fgrid, Fs);       % vector -> frequency list mode
> plot(fgrid, 20*log10(abs(Hgrid))); grid on;
> xlabel('Frequency (Hz)'); ylabel('Mag (dB)');
> xline(fp, '--r'); yline(-3, '--r');
> title('Magnitude Response with -3 dB at f_p');
> 
> % D) Show final H(z) nicely
> disp('--- Final H(z) ---');
> fprintf('H(z) = (%.4f + %.4f z^{-1}) / (1 %+.4f z^{-1})\n', b(1), b(2), a(2));
> ```

---

## 🧠 10 – Key Formula Recap

| Concept | Formula |
|:--|:--|
| Bilinear mapping | $s=\tfrac{2}{T}\tfrac{z-1}{z+1}$ |
| Frequency warping | $\Omega=\tfrac{2}{T}\tan(\omega/2)$ |
| Pre-warp | $\Omega_p=2F_s\tan(\pi f_p/F_s)$ |
| Butterworth order | $n=\dfrac{\log_{10}\!\left((10^{0.1A_s}-1)/(10^{0.1A_p}-1)\right)}{2\log_{10}\upsilon_s}$ |
| Chebyshev I order | $n=\dfrac{\operatorname{acosh}\!\sqrt{(10^{0.1A_s}-1)/(10^{0.1A_p}-1)}}{\operatorname{acosh}\upsilon_s}$ |
| Ripple factor | $\varepsilon=\sqrt{10^{0.1A_p}-1}$ |
| Analog prototype | $H_P(s)=\dfrac{1}{s+1}$ |
| Digital mapping | $z=e^{sT}$ |

---

# 🧮 MATLAB Helpers — Digital Filter Design (IIR)

> [!summary] **Purpose**  
> These compact examples implement formulas from *Digital Filter Design — IIR (Part 2)*.  
> Each section introduces the **theory**, **formula**, and a **tiny MATLAB demo** with its helper defined inside the same code block.  
> Designed for direct copy–paste into MATLAB Live Script (no external `.m` files needed).

---

## 🧩 1 — Butterworth Order Helper

> [!summary] **Concept**
> The **Butterworth prototype** magnitude response is:
> $$
> |H(j\Omega)|^2 = \frac{1}{1+\varepsilon^2\Omega^{2n}}
> $$
> with $\varepsilon^2 = 10^{0.1A_p}-1$.  
>  
> To meet a stopband attenuation $A_s$ at $\upsilon_s=\Omega_s/\Omega_p$:
> $$
> n \ge \frac{\log_{10}\!\left(\frac{10^{0.1A_s}-1}{10^{0.1A_p}-1}\right)}{2\log_{10}\upsilon_s}
> $$
>  
> This helper computes $n_{\min}$ and the rounded integer order $n$.  
> Useful when designing analog or digital Butterworth filters before calling `butter()`.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% Butterworth order helper — self-contained example
> Ap = 1; As = 40;
> vs = 2;                         % normalized stop edge (Ωs/Ωp)
> [n_min, n_bw] = butterworth_order(Ap, As, vs)
>
> % Compare with MATLAB's buttord for digital specs:
> Wp = 0.3; Ws = 0.6;
> [n_builtin, Wn] = buttord(Wp, Ws, Ap, As)
>
> % Quick plot
> [b, a] = butter(n_bw, Wp, 'low');
> figure; freqz(b, a, 512); title(sprintf('Butterworth (n=%d via helper)', n_bw));
>
> %% --- Local function ---
> function [n_min, n] = butterworth_order(Ap_dB, As_dB, v_s)
>     eps2  = 10.^(0.1*Ap_dB) - 1;
>     n_min = log10((10.^(0.1*As_dB) - 1)./eps2) ./ (2*log10(v_s));
>     n     = ceil(n_min);
> end
> ```

---

## 🧮 2 — Chebyshev Type I Order Helper

> [!summary] **Concept**
> Chebyshev Type I filters have **equiripple passbands**, characterized by:
> $$
> |H(j\Omega)|^2 = \frac{1}{1+\varepsilon^2C_n^2(\Omega)},\qquad
> \varepsilon=\sqrt{10^{0.1A_p}-1}
> $$
> The minimum order that satisfies $(A_p,A_s,\upsilon_s)$ is:
> $$
> n = \frac{\operatorname{acosh}\!\left(\sqrt{\dfrac{10^{0.1A_s}-1}{10^{0.1A_p}-1}}\right)}{\operatorname{acosh}\upsilon_s}
> $$
>  
> This function implements that closed-form equation.  
> Compare its result to MATLAB’s `cheb1ord()` output.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% Chebyshev I order formula — self-contained example
> Ap = 1; As = 40; vs = 2;
> n_cheb = cheby1_order_formula(Ap, As, vs)
>
> % Compare to MATLAB's estimator:
> Wp = 0.30; Ws = 0.60;
> [n_est, Wp_c] = cheb1ord(Wp, Ws, Ap, As)
> [b, a] = cheby1(n_est, Ap, Wp_c, 'low');
> figure; freqz(b, a, 512);
> title(sprintf('Chebyshev I (n=%d, ripple=%.1f dB)', n_est, Ap));
>
> %% --- Local function ---
> function n = cheby1_order_formula(Ap_dB, As_dB, v_s)
>     num = sqrt((10^(0.1*As_dB)-1)/(10^(0.1*Ap_dB)-1));
>     n_real = acosh(num)/acosh(v_s);
>     n = ceil(n_real);
> end
> ```

---

## 🧭 3 — Pre-Warping Frequencies

> [!summary] **Concept**
> The **Bilinear Transform** compresses higher frequencies (frequency warping).  
> To design an analog prototype matching digital specs, edge frequencies must be **pre-warped**:
> $$
> \Omega = 2F_s\tan\!\left(\frac{\pi f}{F_s}\right)
> $$
> This converts digital cutoff frequencies $(f_p,f_s)$ to analog $(\Omega_p,\Omega_s)$ before design.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% Pre-warp digital edge freqs — self-contained example
> Fs = 90; fp = 15; fs = 25;
> [Om_p, Om_s] = prewarp(fp, fs, Fs)
>
> % Design 1st-order analog LP and BLT it:
> [b_s, a_s] = butter(1, Om_p, 's');
> [bz, az]   = bilinear(b_s, a_s, Fs);
> figure; freqz(bz, az, 512, Fs); title('1st-order LP via pre-warp + BLT');
>
> %% --- Local function ---
> function [Om_p, Om_s] = prewarp(fp, fs, Fs)
>     Om_p = 2*Fs * tan(pi*fp/Fs);
>     Om_s = 2*Fs * tan(pi*fs/Fs);
> end
> ```

---

## 🔁 4 — Bilinear Transform Wrapper

> [!summary] **Concept**
> Implements $s=\frac{2}{T}\frac{z-1}{z+1}$ for a first-order analog LP prototype:
> $$
> H(s)=\frac{\Omega_c}{s+\Omega_c}
> $$
> Converts to digital domain $H(z)$ maintaining low-frequency behavior.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% Bilinear transform wrapper — self-contained example
> Oc = 100; b_s = [Oc]; a_s = [1 Oc];
> Fs = 200; [bz, az] = blt(b_s, a_s, Fs)
> figure; freqz(bz, az, 512, Fs); title('BLT wrapper: 1st-order LP');
>
> %% --- Local function ---
> function [bz, az] = blt(b_s, a_s, Fs)
>     [bz, az] = bilinear(b_s, a_s, Fs);
> end
> ```

---

## 🎚️ 5 — Prototype Transformations (LP → LP/HP/BP/BS)

> [!summary] **Concept**
> Transform the normalized prototype $H_P(s)=1/(s^2+1.4142s+1)$ to other types using:
> - LP: $s\!\to\!s/\Omega_p$  
> - HP: $s\!\to\!\Omega_p/s$  
> - BP: $s\!\to\!(s^2+\Omega_0^2)/(sW)$  
> - BS: $s\!\to\!sW/(s^2+\Omega_0^2)$  
> where $W=\Omega_{pH}-\Omega_{pL}$, $\Omega_0=\sqrt{\Omega_{pH}\Omega_{pL}}$.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% Prototype transforms — self-contained example
> bP = 1; aP = [1 1.4142 1];
> OpL = 150; OpH = 250; W = OpH - OpL; O0 = sqrt(OpL*OpH);
> Fs = 1000;
>
> [blp, alp] = lp2lp(bP, aP, OpH);
> [bhp, ahp] = lp2hp(bP, aP, OpH);
> [bbp, abp] = lp2bp(bP, aP, O0, W);
> [bbs, abs_] = lp2bs(bP, aP, O0, W);
>
> [blp_z, alp_z] = bilinear(blp, alp, Fs); figure; freqz(blp_z, alp_z, 512, Fs); title('LP→LP');
> [bhp_z, ahp_z] = bilinear(bhp, ahp, Fs); figure; freqz(bhp_z, ahp_z, 512, Fs); title('LP→HP');
> [bbp_z, abp_z] = bilinear(bbp, abp, Fs); figure; freqz(bbp_z, abp_z, 512, Fs); title('LP→BP');
> [bbs_z, abs_z] = bilinear(bbs, abs_, Fs); figure; freqz(bbs_z, abs_z, 512, Fs); title('LP→BS');
> ```

---

## ⚙️ 6 — Full Digital Butterworth Design

> [!summary] **Concept**
> Design a low-pass digital Butterworth filter directly from specs.  
> MATLAB handles normalization, order selection, and coefficient generation.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% One-shot Butterworth design — self-contained example
> Ap = 1; As = 40; Fs = 200; 
> fp = 30; fs = 60;
> Wp = fp/(Fs/2); Ws = fs/(Fs/2);
> [n, Wn] = buttord(Wp, Ws, Ap, As)
> [b, a]  = butter(n, Wn, 'low');
> figure; freqz(b, a, 512, Fs);
> title(sprintf('Butterworth LP (n=%d)', n));
> ```

---

## ⚙️ 7 — Full Digital Chebyshev I Design

> [!summary] **Concept**
> Similar to Butterworth, but with a specified passband ripple $A_p$.  
> Produces a steeper roll-off at the cost of passband ripples.

> [!code]- MATLAB (Live Script)
> ```matlab
> %% One-shot Chebyshev I design — self-contained example
> Ap = 1; As = 40; Fs = 200; 
> fp = 30; fs = 60;
> Wp = fp/(Fs/2); Ws = fs/(Fs/2);
> [n, WpCheb] = cheb1ord(Wp, Ws, Ap, As)
> [bc, ac]    = cheby1(n, Ap, WpCheb, 'low');
> figure; freqz(bc, ac, 512, Fs);
> title(sprintf('Chebyshev I LP (n=%d, ripple=%.1f dB)', n, Ap));
> ```


# 🧩 MATLAB Template — General IIR Filter Design via Pre-Warp + Bilinear Transform

> [!summary] **Overview**  
> A complete and numerically stable MATLAB Live Script for designing analog-prototype-based IIR filters (Butterworth or Chebyshev Type I) via **pre-warping**, **analog prototype transformation**, and **bilinear transform**.  
> Supports **LP**, **HP**, **BP**, and **BS** filters with automatic or manual order selection.

---

> [!code]- MATLAB (Live Script)
> ```matlab
> %% =========================
> %% USER PARAMETERS (EDIT ME)
> %% =========================
> clear; clc; close all;
> 
> % Sampling
> Fs = 480;                 % Hz
> 
> % Filter type: 'lp' | 'hp' | 'bp' | 'bs'
> ftype = 'lp';
> 
> % Analog prototype: 'butter' | 'cheby1'
> proto = 'butter';
> 
> % Specs (digital, in Hz and dB)
> % For LP/HP: scalars fp, fs. For BP/BS: 1x2 vectors [fL fH].
> Ap = 1;                   % passband ripple (dB) — used by Chebyshev I
> As = 40;                  % stopband attenuation (dB)
> 
> switch ftype
>   case {'lp','hp'}
>     fp = 60;              % passband edge [Hz]
>     fs = 100;             % stopband edge [Hz]
>   case {'bp','bs'}
>     fp = [120 180];       % passband edges [Hz]
>     fs = [ 90 210];       % stopband edges [Hz]
>   otherwise
>     error('Unknown ftype');
> end
> 
> % Order selection mode:
> %   'auto_formula' : closed-form (LP/HP only; Butter/Cheby1)
> %   'auto_ord'     : use buttord/cheb1ord on digital specs (any type)
> %   'manual'       : use n_manual
> order_mode = 'auto_formula';
> n_manual   = 4;
> 
> % Plot toggles
> do_plots    = true;       % show freqz
> show_markers = true;      % overlay fp, fs markers (LP/HP)
> 
> 
> %% =============================
> %% 1) PRE-WARP DIGITAL -> ANALOG
> %% =============================
> % Omega = 2*Fs*tan(pi*f/Fs)
> [Om_p, Om_s] = prewarp_edges(fp, fs, Fs);
> 
> fprintf('--- Prewarp ---\n');
> if isscalar(Om_p)
>     fprintf('Omega_p = %.6f rad/s,  Omega_s = %.6f rad/s\n', Om_p, Om_s);
> else
>     fprintf('Omega_p = [%.6f  %.6f] rad/s\n', Om_p(1), Om_p(2));
>     fprintf('Omega_s = [%.6f  %.6f] rad/s\n', Om_s(1), Om_s(2));
> end
> 
> 
> %% =============================
> %% 2) DETERMINE ORDER n
> %% =============================
> use_auto_ord = false;
> 
> switch order_mode
>   case 'manual'
>     n = n_manual;
> 
>   case 'auto_formula'
>     switch lower(proto)
>       case 'butter'
>         if strcmpi(ftype,'lp')
>             vs = Om_s/Om_p;                 % LP: vs = Os/Op
>             n  = butter_order_formula(Ap, As, vs);
>         elseif strcmpi(ftype,'hp')
>             vs = Om_p/Om_s;                 % HP: vs = Op/Os
>             n  = butter_order_formula(Ap, As, vs);
>         else
>             warning('Formula mode not implemented for BP/BS. Falling back to auto_ord.');
>             use_auto_ord = true;
>         end
>       case 'cheby1'
>         if strcmpi(ftype,'lp')
>             vs = Om_s/Om_p;                 % LP: vs = Os/Op
>             n  = cheby1_order_formula(Ap, As, vs);
>         elseif strcmpi(ftype,'hp')
>             vs = Om_p/Om_s;                 % HP: vs = Op/Os
>             n  = cheby1_order_formula(Ap, As, vs);
>         else
>             warning('Formula mode not implemented for BP/BS. Falling back to auto_ord.');
>             use_auto_ord = true;
>         end
>       otherwise
>         error('Unknown proto');
>     end
> 
>   case 'auto_ord'
>     use_auto_ord = true;
> 
>   otherwise
>     error('Unknown order_mode');
> end
> 
> if use_auto_ord
>     switch ftype
>       case {'lp','hp'}
>         Wp = fp/(Fs/2); Ws = fs/(Fs/2);
>       case {'bp','bs'}
>         Wp = fp/(Fs/2); Ws = fs/(Fs/2);  % 1x2 vectors
>     end
>     switch lower(proto)
>       case 'butter'
>         [n, ~] = buttord(Wp, Ws, Ap, As);
>       case 'cheby1'
>         [n, ~] = cheb1ord(Wp, Ws, Ap, As);
>       otherwise
>         error('Unknown proto');
>     end
> end
> fprintf('--- Order selection ---\n');
> fprintf('Chosen order n = %d\n', n);
> 
> 
> %% =====================================
> %% 3) NORMALIZED ANALOG PROTOTYPE (LP)
> %% =====================================
> switch lower(proto)
>   case 'butter'
>     [bP, aP] = butter(n, 1, 's');
>   case 'cheby1'
>     [bP, aP] = cheby1(n, Ap, 1, 's');
>   otherwise
>     error('Unknown proto');
> end
> 
> 
> %% 4) ANALOG FILTER (zpk) AT WARPED EDGES
> switch lower(proto)
>   case 'butter'
>     switch lower(ftype)
>       case 'lp', [zA,pA,kA] = butter(n, Om_p, 's');
>       case 'hp', [zA,pA,kA] = butter(n, Om_p, 'high', 's');
>       case 'bp', [zA,pA,kA] = butter(n, sort(Om_p), 'bandpass', 's');
>       case 'bs', [zA,pA,kA] = butter(n, sort(Om_p), 'stop', 's');
>     end
>   case 'cheby1'
>     switch lower(ftype)
>       case 'lp', [zA,pA,kA] = cheby1(n, Ap, Om_p, 's');
>       case 'hp', [zA,pA,kA] = cheby1(n, Ap, Om_p, 'high', 's');
>       case 'bp', [zA,pA,kA] = cheby1(n, Ap, sort(Om_p), 'bandpass', 's');
>       case 'bs', [zA,pA,kA] = cheby1(n, Ap, sort(Om_p), 'stop', 's');
>     end
> end
> 
> % Analog zpk -> SOS (stable scaling)
> [sosA, gA] = zp2sos(zA, pA, kA);
> 
> %% 5) BILINEAR TRANSFORM SECTION-BY-SECTION
> sosZ = zeros(size(sosA));
> for s = 1:size(sosA,1)
>     b_s = sosA(s,1:3) * gA^(s==1);
>     a_s = sosA(s,4:6);
>     [bz, az] = bilinear(b_s, a_s, Fs);
>     sosZ(s,:) = [bz az];
> end
> [bZ,aZ] = sos2tf(sosZ);     % numerically safe composition
> 
> %% =================
> %% 6) VERIFICATION
> %% =================
> if do_plots
>   figure; freqz(bZ, aZ, 2048, Fs);
>   title(sprintf('%s-%s via Prewarp+BLT (n=%d)', upper(proto), upper(ftype), n));
> end
> 
> switch lower(ftype)
>   case {'lp','hp'}
>     Hfp = freqz(bZ, aZ, [fp fp+1e-9], Fs); Hfp = Hfp(1);
>     mdB = 20*log10(abs(Hfp));
>     fprintf('At fp = %.2f Hz: |H| = %.6f (%.2f dB)\n', fp, abs(Hfp), mdB);
>   case {'bp','bs'}
>     Hfp1 = freqz(bZ, aZ, [fp(1) fp(1)+1e-9], Fs); Hfp1 = Hfp1(1);
>     Hfp2 = freqz(bZ, aZ, [fp(2) fp(2)+1e-9], Fs); Hfp2 = Hfp2(1);
>     mdB1 = 20*log10(abs(Hfp1));
>     mdB2 = 20*log10(abs(Hfp2));
>     fprintf('At fpL = %.2f Hz: |H| = %.6f (%.2f dB)\n', fp(1), abs(Hfp1), mdB1);
>     fprintf('At fpH = %.2f Hz: |H| = %.6f (%.2f dB)\n', fp(2), abs(Hfp2), mdB2);
> end
> 
> if do_plots && show_markers && isscalar(fp) && isscalar(fs)
>   fgrid = linspace(0, Fs/2, 2000);
>   Hgrid = freqz(bZ, aZ, fgrid, Fs);
>   figure; plot(fgrid, 20*log10(abs(Hgrid))); grid on;
>   xlabel('Frequency (Hz)'); ylabel('Magnitude (dB)');
>   title('Magnitude Response with Markers');
>   xline(fp, '--r', 'fp'); 
>   xline(fs, '--k', 'fs');
> end
> 
> %% =====================
> %% LOCAL HELPER FUNCS
> %% =====================
> function [Om_p, Om_s] = prewarp_edges(fp, fs, Fs)
>   Om_p = 2*Fs*tan(pi*fp/Fs);
>   Om_s = 2*Fs*tan(pi*fs/Fs);
> end
> 
> function n = butter_order_formula(Ap_dB, As_dB, vs)
>   eps2  = 10^(0.1*Ap_dB) - 1;
>   n_min = log10( (10^(0.1*As_dB) - 1)/eps2 ) / (2*log10(vs));
>   n     = ceil(n_min);
> end
> 
> function n = cheby1_order_formula(Ap_dB, As_dB, vs)
>   num   = sqrt( (10^(0.1*As_dB)-1) / (10^(0.1*Ap_dB)-1) );
>   n_min = acosh(num) / acosh(vs);
>   n     = ceil(n_min);
> end
> ```

---

## 🎯 **Try These Test Questions**

Use them to verify that your script behaves correctly for all prototypes and filter types:

|#|Test|Set these EXACT params|
|---|---|---|
|1|LP Butterworth|`proto='butter'`, `ftype='lp'`, `fp=60`, `fs=100`, `Fs=480`|
|2|HP Butterworth|`proto='butter'`, `ftype='hp'`, `fp=80`, `fs=50`, `Fs=480`|
|3|LP Chebyshev I|`proto='cheby1'`, `ftype='lp'`, `Ap=1`, `As=40`, `fp=60`, `fs=100`, `Fs=480`|
|4|BP Butterworth|`proto='butter'`, `ftype='bp'`, `fp=[120 180]`, `fs=[90 210]`, `Fs=480`|
|5|BS Chebyshev I|`proto='cheby1'`, `ftype='bs'`, `Ap=1`, `As=40`, `fp=[120 180]`, `fs=[90 210]`, `Fs=480`|
|6|Auto vs Manual|pick any of the above; compare `order_mode='auto_formula'` vs `'manual'` (e.g., `n_manual=4`)|
|7|Auto_ord sanity (BP)|`proto='butter'`, `ftype='bp'`, `fp=[120 180]`, `fs=[90 210]`, `order_mode='auto_ord'`|
|8|Pre-warp check|print Ω values; they should increase with `f`|
|9|Gain at fp|printed ≈ −3 dB (LP/HP)|
|10|High-order stability|bump `n_manual≥8`; no warnings thanks to SOS|

---

> 💡 *Pro tip:* After each run, verify visually that  
> - The cutoff aligns with `fp`,  
> - The stopband attenuation ≈ `As`,  
> - The passband meets the ripple spec `Ap`.

---
🔗 **References**  
- Lecture Slides (50–108) → *Digital Filter Design IIR Part 2*  
- MATLAB Docs: `buttord`, `butter`, `cheby1`, `bilinear`, `freqz`  

---

**Recent in same folder**
```dataview
LIST FROM "Courses/DSP"
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.mtime desc
LIMIT 5
```
