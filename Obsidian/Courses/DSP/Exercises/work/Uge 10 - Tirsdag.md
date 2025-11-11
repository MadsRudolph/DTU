> Quick refs: [[Digital Filter Design — IIR (Part 2)]]  
> Exercise sheet: *Uge 10 – Tirsdag* (BLT IIR design)

---

# Week 10 — Bilinear Transform (IIR Low-Pass)

---

## 📘 Concept Overview
The **Bilinear Transform (BLT)** method provides a systematic way to design a **digital IIR filter** by mapping an **analog prototype filter** into the discrete-time domain without introducing aliasing.  

It defines a non-linear relationship between analog angular frequency $\Omega$ and digital angular frequency $\omega$:

$$
\Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)
$$

This mapping introduces *frequency warping* but preserves the overall filter shape. The BLT guarantees **stability preservation** (left-half $s$-plane → inside unit circle) and **monotonic frequency mapping** (no aliasing).  

Design flow (see Slides 62 & 101):  
1️⃣ Specify digital requirements $(f_p,F_s,T_s)$  
2️⃣ Prewarp to analog domain  
3️⃣ Design analog prototype filter (e.g. Butterworth)  
4️⃣ Apply BLT → obtain $H_d(z)$  
5️⃣ Verify and derive difference equation  

---

## 1-A) Digital requirements → $\omega_p$

> **Given**  
> $T_s = 0.001~\text{s}$, $f_p = 147.58~\text{Hz}$

> **Exercise description**  
> Compute the **digital passband angular frequency** $\omega_p$ in rad/sample using the specified sampling period and passband frequency.

> [!theory] **Theory Recap** (Slides 56–58, 104)  
> In a discrete-time system, the sampling frequency is $F_s = 1/T_s$.  
> The relationship between frequency in Hz and angular frequency in rad/sample is  
> $$
> \omega = 2\pi\,\frac{f}{F_s}.
> $$  
> Expressing the passband in rad/sample allows the design to proceed fully in the digital domain, where the $z$-transform operates.

**Formula**
$$
\omega_p = 2\pi\frac{f_p}{F_s}, \qquad
F_s = \frac{1}{T_s} = 1000~\text{Hz}.
$$

**Numeric evaluation**
$$
\omega_p = 2\pi\frac{147.58}{1000}
          = 0.927272~\text{rad/sample}.
$$

> [!code]- MATLAB
> ```matlab
> % 1-A) Digital passband angular frequency (numeric)
> Ts = 1e-3;               % Sampling period [s]
> Fs = 1/Ts;               % = 1000 Hz
> fp_hz = 147.58;          % Passband frequency [Hz]
> wp = 2*pi*(fp_hz/Fs);    % = 0.927272 rad/sample
> fprintf('omega_p = %.6f rad/sample\n', wp);
> ```

---

### 🧾 **Results**
- $F_s = 1000~\text{Hz}$  
- $\omega_p = 0.9273~\text{rad/sample}$  
- This defines the **digital passband edge** for the subsequent prewarping step.

---

## 1-B) Prewarp to analog $\Omega_p, F_p$

> **Given**  
> $T_s = 0.001~\text{s}$, $\omega_p = 0.9273~\text{rad/sample}$

> **Exercise description**  
> Apply the bilinear-transform frequency-warping relation to determine the **analog passband edge** $\Omega_p$ and its corresponding **frequency in Hz**, $F_p$.

> [!theory] **Theory Recap** (Slides 58–60, 105)  
> The bilinear transform maps continuous-time and discrete-time frequencies nonlinearly.  
> To ensure the designed analog filter aligns with the desired digital cutoff, **prewarping** compensates for this distortion:  
> $$
> \Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right)
> $$
> Prewarping guarantees that the passband edge in the analog domain maps exactly to $f_p$ after applying the BLT.

**Relations**
$$
\Omega_p = \frac{2}{T_s}\tan\!\left(\frac{\omega_p}{2}\right), \qquad
F_p = \frac{\Omega_p}{2\pi}
$$

**Numeric evaluation**
$$
\begin{aligned}
T_s &= 0.001~\text{s}, \quad \omega_p = 0.927272~\text{rad/sample} \\[4pt]
\Omega_p &= \frac{2}{0.001}\tan\!\Big(\frac{0.927272}{2}\Big)
          = 999.971587~\text{rad/s} \\[4pt]
F_p &= \frac{999.971587}{2\pi}
     = 159.150421~\text{Hz}
\end{aligned}
$$

> [!code]- MATLAB
> ```matlab
> % 1-B) Prewarp to analog domain (numeric)
> Ts = 1e-3;  Fs = 1/Ts;
> wp = 0.927272;                 % from 1-A
> alpha = 2/Ts;
> Op = alpha * tan(wp/2);        % = 999.971587 rad/s
> Fp = Op/(2*pi);                % = 159.150421 Hz
> fprintf('Omega_p = %.6f rad/s, Fp = %.6f Hz\n', Op, Fp);
> ```

---

### 🧾 **Results**
- $\Omega_p = 999.9716~\text{rad/s}$  
- $F_p = 159.1504~\text{Hz}$  
- The prewarped analog cutoff ensures that, after the BLT, the digital filter’s $f_p = 147.58$ Hz corresponds exactly to the –3 dB point.

---

## 1-C) Analog Butterworth filter (order 1)

> **Given**  
> $\Omega_p = 999.97~\text{rad/s}$, $F_p = 159.15~\text{Hz}$

> **Exercise description**  
> Design the analog low-pass filter.  
> Assume a first-order Butterworth prototype.  
> 1️⃣ Write the prototype filter transfer function.  
> 2️⃣ Derive analytically the transformed filter transfer function using algebra and verify with `lp2lp()`.  
> 3️⃣ Plot the magnitude response as a function of **frequency** (Hz).  
> 4️⃣ Confirm that the passband edge equals the prewarped frequency from 1-B.

> [!theory] **Theory Recap** (Slides 65–69, 106)  
> The normalized Butterworth prototype has a maximally flat passband:
> $$
> H_p(s)=\frac{1}{s+1}.
> $$
> Scaling to the desired cutoff $\Omega_c$ gives
> $$
> H_a(s)=\frac{\Omega_c}{s+\Omega_c},\qquad\Omega_c=\Omega_p.
> $$
> The pole is at $s=-\Omega_c$ and $|H_a(j\Omega_c)|=1/\sqrt2$ (−3 dB).

---

### Analytical derivation (prototype → scaled)

Starting from the prototype:
$$
H_p(s)=\frac{1}{s+1}.
$$
Using the low-pass-to-low-pass frequency scaling:
$$
H_a(s)=H_p\!\left(\frac{s}{\Omega_c}\right)
      =\frac{1}{\tfrac{s}{\Omega_c}+1}
      =\frac{\Omega_c}{s+\Omega_c}.
$$
For $\Omega_c=\Omega_p$,
$$
H_a(s)=\frac{999.97}{s+999.97}.
$$
At $\Omega=\Omega_p$:
$$
|H_a(j\Omega_p)|=\frac{999.97}{\sqrt{999.97^2+999.97^2}}
                 =0.7071
                 \Rightarrow-3.01~\text{dB}.
$$

> [!code]- MATLAB — analytical + `lp2lp` verification and linear plot
> ```matlab
> % 1-C) Analog Butterworth (order 1) — analytical derivation + lp2lp check
> syms s Oc real positive
> Hp = 1/(s + 1);
> Ha_sym = subs(Hp, s, s/Oc);              % analytical scaling
> Ha_simplified = simplify(Ha_sym);
> pretty(Ha_simplified)                    % shows Oc/(s+Oc)
>
> % Numeric verification with MATLAB lp2lp()
> Oc_num = Op;                             % from 1-B (~999.97 rad/s)
> Bproto = 1; Aproto = [1 1];
> [B_lp2lp, A_lp2lp] = lp2lp(Bproto, Aproto, Oc_num);
> fprintf('Analytical:  B=[%.4f], A=[1 %.4f]\n', Oc_num, Oc_num);
> fprintf('lp2lp:       B=[%.4f], A=[1 %.4f]\n', B_lp2lp, A_lp2lp(2));
> assert(abs(B_lp2lp - Oc_num) < 1e-10 && abs(A_lp2lp(2) - Oc_num) < 1e-10, ...
>        'lp2lp verification failed');
>
> % Magnitude check at Fp
> Ban = [Oc_num]; Aan = [1 Oc_num];
> wFp = 2*pi*Fp;
> H_Fp = freqs(Ban, Aan, wFp);
> fprintf('|H(jw_p)| = %.6f (%.4f dB)\n', abs(H_Fp), 20*log10(abs(H_Fp)));
>
> % --- Linear magnitude plot (dark theme, dashed blue guide box) ---
> f  = linspace(0, 10*Fp, 5000);                 % long tail up to ~1600 Hz
> H  = freqs(Ban, Aan, 2*pi*f);
> mag = abs(H);
>
> % exact |H| at Fp (=1/sqrt(2))
> H_Fp_exact = polyval(Ban, 1j*2*pi*Fp) / polyval(Aan, 1j*2*pi*Fp);
> mag_fp     = abs(H_Fp_exact);
>
> fig = figure('Name','Analog LP magnitude (linear)','Color','k');
> ax  = axes('Parent',fig);
> ax.Color = 'k';  ax.XColor = [1 0 0];  ax.YColor = [1 0 0];
> ax.GridColor = [0.4 0.4 0.4];  ax.LineWidth = 1.0;
> plot(f, mag, 'Color', [1 0.5 0], 'LineWidth', 1.8); hold on; grid on;
>
> % dashed blue guide box at (Fp, 1/sqrt(2))
> blue = [0 0.447 0.741];
> plot([0, Fp],  [mag_fp, mag_fp], 'Color', blue, 'LineWidth', 1.4, 'LineStyle','--');
> plot([Fp, Fp], [0, mag_fp],      'Color', blue, 'LineWidth', 1.4, 'LineStyle','--');
>
> xlabel('Analog frequency (Hz)', 'Color', 'w');
> ylabel('Magnitude Frequency Response', 'Color', 'w');   % linear
> title('Analog LP (1st-order)', 'Color', 'w');
> xlim([0, 10*Fp]);  ylim([0, 1.02]);
> xticks(0:100:round(10*Fp, -2));                         % fine ticks
>
> exportgraphics(gcf, 'C:/Users/Mads2/DTU/Obsidian/Courses/DSP/Images/Week10_AnalogLP_mag.png', 'Resolution', 300);
> ```

---

**Verification**  
![[Courses/DSP/Images/Week10_AnalogLP_mag.png]]

---

### 🧾 **Results**
- Analytical: $H_a(s)=\dfrac{999.97}{s+999.97}$  
- `lp2lp()` check: identical numerator and denominator coefficients ✅  
- Pole: $s=-999.97~\text{rad/s}$ Time constant $\tau=1/\Omega_p=1.00$ ms  
- $|H_a(j\Omega_p)|=0.7071$ → −3.01 dB $\angle H_a(j\Omega_p)≈−45°$  
- The analog Butterworth filter fulfills the design criterion with cutoff at $F_p=159.15$ Hz.

---

## 1-D) Bilinear Transform → digital $H_d(z)$

> **Given**  
> $T_s = 0.001~\text{s}$ (thus $\alpha=\dfrac{2}{T_s}=2000$),  
> $H_a(s)=\dfrac{\Omega_p}{s+\Omega_p}$ with $\Omega_p \approx 999.9716~\text{rad/s}$

> **Exercise description**  
> Apply the **bilinear transform (BLT)** to map the analog prototype $H_a(s)$ into the digital domain and obtain $H_d(z)$ in the form
> $$
> H_d(z)=\frac{b_0+b_1 z^{-1}}{1+a_1 z^{-1}}.
> $$
> Verify the coefficients using `bilinear()`.

> [!theory] **Theory Recap** (Slides 57, 60, 107–108)  
> The BLT substitutes
> $$
> s = \alpha\,\frac{z-1}{z+1},\qquad \alpha=\frac{2}{T_s},
> $$
> which maps the **LHP** (stable analog) into the **unit disk** (stable digital) and is **frequency–monotone** (no aliasing).  
> Prewarping (1-B) ensures the passband edge maps correctly after BLT.

**Algebra (symbolic derivation)**  
Start with  
$$
H_a(s)=\frac{\Omega_p}{s+\Omega_p},\qquad s=\alpha\frac{z-1}{z+1}.
$$
Substitute and simplify:
$$
H_d(z)=\frac{\Omega_p}{\alpha\frac{z-1}{z+1}+\Omega_p}
      = \frac{\Omega_p(z+1)}{(\alpha+\Omega_p)z + (\Omega_p-\alpha)}.
$$
Divide numerator/denominator by $z$ to get powers of $z^{-1}$:
$$
H_d(z)=\frac{\Omega_p(1+z^{-1})}{(\alpha+\Omega_p) + (\Omega_p-\alpha)z^{-1}}.
$$
Normalize by $(\alpha+\Omega_p)$:
$$
\boxed{
H_d(z)=\frac{\tfrac{\Omega_p}{\alpha+\Omega_p}\bigl(1+z^{-1}\bigr)}
{1+\tfrac{\Omega_p-\alpha}{\alpha+\Omega_p}\,z^{-1}}
}
\;\Rightarrow\;
\begin{aligned}
b_0 &= \frac{\Omega_p}{\alpha+\Omega_p},\\
b_1 &= \frac{\Omega_p}{\alpha+\Omega_p},\\
a_1 &= \frac{\Omega_p-\alpha}{\alpha+\Omega_p}.
\end{aligned}
$$

**Numeric evaluation**  
With $\alpha=2000$ and $\Omega_p=999.9716$:
$$
\begin{aligned}
b_0 &= b_1 = \frac{999.9716}{2000+999.9716}
          \approx 0.333323,\\[4pt]
a_1 &= \frac{999.9716-2000}{2000+999.9716}
          \approx -0.333354.
\end{aligned}
$$
So
$$
\boxed{H_d(z)=\frac{0.333323 + 0.333323\,z^{-1}}{1 - 0.333354\,z^{-1}}.}
$$

**Sanity checks (quick)**
- **DC gain:** $H_d(1)=\dfrac{b_0+b_1}{1+a_1}\approx \dfrac{0.666646}{0.666646}=1$ ✅  
- **Pole:** denominator $1+a_1 z^{-1}=0 \Rightarrow z=-a_1\approx 0.333354$ (inside unit circle) ✅  
- **Zeros:** $z=-1$ (from the $(1+z^{-1})$ factor) as expected for BLT of 1st-order LP ✅

> [!code]- MATLAB — verify with `bilinear()`
> ```matlab
> % 1-D) Bilinear transform to digital H(z)
> % Uses: Ban=[Oc], Aan=[1 Oc], Fs, Ts, Op, Fp already defined earlier
> [Bz, Az] = bilinear(Ban, Aan, Fs);
> b0 = Bz(1); b1 = Bz(2); a1 = Az(2);
> fprintf('[1-D] Digital H(z):  B=[%.6f %.6f],  A=[1 %.6f]\n', b0, b1, a1);
>
> % Quick sanity checks
> Hdc  = (b0+b1)/(1+a1);
> pole = -a1;     % from 1 + a1 z^-1 = 0
> fprintf('       H(1)=%.6f (expect ~1),  pole=%.6f (|pole|<1 stable)\n', Hdc, pole);
> ```

---

### 🧾 **Results**
- Coefficients: $b_0=b_1=\dfrac{\Omega_p}{\alpha+\Omega_p}\approx 0.33332$,  
  $a_1=\dfrac{\Omega_p-\alpha}{\alpha+\Omega_p}\approx -0.33335$.  
- Final form: $H_d(z)=\dfrac{b_0+b_1 z^{-1}}{1+a_1 z^{-1}}$ with $H_d(1)=1$.  
- Pole at $z\approx 0.333$ (stable), zero at $z=-1$.  
- **Verification:** `bilinear(Ban,Aan,Fs)` returns identical coefficients.

---

## 1-E) Verify digital passband with $H_d(e^{j\omega})$

> **Given**  
> $T_s = 0.001~\text{s}$ ($F_s = 1000~\text{Hz}$), $f_p = 147.58~\text{Hz}$, and  
> $H_d(z) = \dfrac{b_0 + b_1 z^{-1}}{1 + a_1 z^{-1}}$ from 1-D (with $b_0 = b_1 \approx 0.33332$, $a_1 \approx -0.33335$).

> **Exercise description**  
> Evaluate the **digital frequency response** and verify that the attenuation at $f_p$ is approximately **−3 dB**.  
> Display the **linear magnitude** response and highlight $f_p$ and the −3 dB (0.707) point.

> [!theory] **Theory Recap** (Slides 58–59, 108)  
> The discrete-time frequency response is obtained by evaluating $H_d(z)$ on the unit circle:
> $$
> H_d(e^{j\omega}) = H_d(z)\Big|_{z=e^{j\omega}}, \qquad \omega = 2\pi \frac{f}{F_s}.
> $$
> MATLAB’s `freqz` efficiently samples this, returning both magnitude and frequency vectors for verification.

---

**Procedure**
1. Compute $H_d(e^{j\omega_p})$ at $\omega_p = 2\pi f_p/F_s$.  
2. Confirm $|H_d(e^{j\omega_p})| \approx 0.707$.  
3. Plot the **linear magnitude** vs. frequency and draw guide lines at $f_p$ and 0.707.

> [!code]- MATLAB
> ```matlab
> %% 1-E) Verify digital passband with freqz (linear magnitude style)
> n = 4096;                                 % dense grid for smooth curve
> [Hdz, fHz] = freqz(Bz, Az, n, Fs);        % Bz,Az from 1-D
>
> % Value at f_p (closest bin)
> [~, k] = min(abs(fHz - fp_hz));
> H_at_fp = Hdz(k);
> fprintf('[1-E] |H_d(e^{jω_p})| = %.6f  (%.4f dB) at f_p = %.5f Hz\n', ...
>         abs(H_at_fp), 20*log10(abs(H_at_fp)), fHz(k));
>
> % Exact evaluation at f_p (no grid error)
> wp_exact = 2*pi*fp_hz/Fs;
> z = exp(1j*wp_exact);
> H_exact = (b0 + b1*z.^-1) / (1 + a1*z.^-1);
>
> % ---- Linear magnitude plot (dark theme, orange curve, red axes, white text) ----
> mag = abs(Hdz);
> mag_fp = abs(H_exact);   % |H| at f_p for the guide box
>
> fig = figure('Name','Digital LP magnitude','Color','k');
> ax = axes('Parent',fig);
> ax.Color = 'k';  ax.XColor = [1 0 0];  ax.YColor = [1 0 0];
> ax.GridColor = [0.4 0.4 0.4];  ax.LineWidth = 1.0;
>
> % main curve
> plot(fHz, mag, 'Color', [1 0.5 0], 'LineWidth', 1.8); hold on; grid on;
>
> % guide box at (f_p, |H|)
> plot([0, fp_hz], [mag_fp, mag_fp], 'Color', [1 0.5 0.5], 'LineWidth', 1.2);
> plot([fp_hz, fp_hz], [0, mag_fp], 'Color', [1 0.5 0.5], 'LineWidth', 1.2);
>
> xlabel('Frequency [Hz]', 'Color', 'w');
> ylabel('Magnitude Frequency Response', 'Color', 'w');
> title('Digital LP magnitude (linear)', 'Color', 'w');
> xlim([0 Fs/2]); ylim([0 1.02]);
>
> export('Week10_DigitalLP_mag.png');
> ```

---
**Verification**  
![[Courses/DSP/Images/Week10_DigitalLP_mag.png]]

---
### 🧾 **Results**
- $|H_d(e^{j\omega_p})| = 0.7074$ → −3.01 dB ✅  
- The linear magnitude at $f_p$ confirms correct prewarping and bilinear transform behavior.  

---

## 1-F) Difference equation

> **Given**  
> $H_d(z)=\dfrac{b_0+b_1 z^{-1}}{1+a_1 z^{-1}}$ with  
> $b_0=b_1\approx 0.333323,\quad a_1\approx -0.333354$ (from 1-D).

> **Exercise description**  
> Write the **time-domain difference equation** corresponding to $H_d(z)$, and print it numerically.

> [!theory] **Theory Recap** (Slides 54–55, 107–108)  
> For 
> $$
> H(z)=\frac{\sum_{k=0}^{M} b_k z^{-k}}{1+\sum_{k=1}^{N} a_k z^{-k}},
> $$
> the causal LTI difference equation is
> $$
> y[n]=-\sum_{k=1}^{N} a_k\,y[n-k]+\sum_{k=0}^{M} b_k\,x[n-k].
> $$
> For first-order $N=M=1$:
> $$
> y[n] = -a_1\,y[n-1] + b_0\,x[n] + b_1\,x[n-1].
> $$

**Numeric form**  
With your coefficients:
$$
\boxed{
y[n] \;=\; 0.333323\,x[n] \;+\; 0.333323\,x[n-1] \;+\; 0.333354\,y[n-1].
}
$$

> [!code]- MATLAB
> ```matlab
> %% 1-F) Difference equation (print nicely)
> fprintf('[1-F] Difference equation coefficients:\n');
> fprintf('      b0 = %.10f\n', b0);
> fprintf('      b1 = %.10f\n', b1);
> fprintf('      a1 = %.10f\n', a1);
>
> % Pretty ASCII equation
> fprintf('\ny[n] = %.6f*x[n] + %.6f*x[n-1] + (%.6f)*y[n-1]\n\n', b0, b1, -a1);
>
> % (Optional) impulse response quick check
> L = 32; x = [1; zeros(L-1,1)];
> y_imp = filter([b0 b1], [1 a1], x);
> fprintf('[1-F] First five h[n]: '); fprintf('%.6f ', y_imp(1:5)); fprintf('\n');
> ```
---

### 🧾 **Results**
- Difference equation: $y[n]= -a_1\,y[n-1] + b_0\,x[n] + b_1\,x[n-1]$  
- Numerically: $y[n]= 0.333323\,x[n] + 0.333323\,x[n-1] + 0.333354\,y[n-1]$  
- (Optional) impulse response printed for sanity.

---

## Optional — Step response and DC behavior

> **Exercise description**  
> Evaluate $H(1)$ and $H(-1)$ to check DC and Nyquist gains, and plot the unit-step response to observe stability and transient behavior.

> [!theory] **Theory Recap** (Slides 55, 107)  
> $H(1)$ represents steady-state gain (DC), $H(-1)$ represents Nyquist frequency gain. A bounded step response confirms stability.

> [!code]- MATLAB
> ```matlab
> H_dc = polyval(Bz,1)/polyval(Az,1);
> H_nyq = polyval(Bz,-1)/polyval(Az,-1);
> L=400; u=ones(L,1); y=filter(Bz,Az,u);
> figure; plot(y,'LineWidth',1.4); grid on;
> xlabel('n'); ylabel('y[n]'); title('Step response');
> exportgraphics(gcf,'C:/Users/Mads2/DTU/Obsidian/Courses/DSP/Images/Week10_DigitalLP_step.png');
> ```

**Verification**  
![[Courses/DSP/Images/Week10_DigitalLP_step.png]]

---

**References**  
- Lecture Slides: [[62743 E25 Digital filter design IIR part2.pdf]] (Slides 54–66, 101–108)  
- A. Clausen et al., [[62743 E25 Digital Signal Processing Uge 10 Tirsdag solutions.pdf]] (2025)
