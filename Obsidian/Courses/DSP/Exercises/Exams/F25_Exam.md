> Exam set: [[62743_F25_Exam.pdf]]  
> Solution sheet: [[62743_F25_Exam_student_solutions.pdf]]  
> Matlab document: [Open](<file:///C:/Users/YOUR_PATH/F25_Exam_Template.mlx>)

---
# 62743 — F25 Exam (Digital Signal Processing)  
---

## 📘 Big-Picture Overview

This document contains **fully worked solutions** to the **F25 written exam** in 62743 Digital Signal Processing.  

For each exam problem, you get:

- A short **context / theory recap** in your own words.  
- Full **derivations** with all intermediate steps (not just final answers).  
- **MATLAB templates** you can re-use in the exam (copy → adapt parameters).  
- Clear tagging of key formulas and interpretations.

Structure:

1. **Problem 1 — LTI systems, impulse response, linear phase FIR**  
2. **Problem 2 — IIR Butterworth Highpass via BLT**  
3. **Problem 3 — Sampling, aliasing, pole-zero analysis, inverse systems**  
4. **Problem 4 — Filter realization, signal filtering**  

---

# Problem 1 — LTI Systems, Impulse Response, Linear Phase FIR

> **Given**
> Two discrete-time input signals
> $$
> x_1[n] = \delta[n] - 2\delta[n-1], \qquad
> x_2[n] = -\delta[n] + 3\delta[n-1]
> $$
> are applied separately to an unknown **LTI system**. The outputs $y_1[n]$ and $y_2[n]$ are:
>
> | $n$ | $<0$ | 0 | 1 | 2 | 3 | 4 | 5 | $>5$ |
> |-----|------|---|---|---|-----|-----|-----|------|
> | $y_1[n]$ | 0 | 1 | 0 | 2 | -10 | -3 | -2 | 0 |
> | $y_2[n]$ | 0 | -1 | 1 | 0 | 16 | 5 | 3 | 0 |
>
> You are asked to determine:
> 1. $x_1[n] + x_2[n]$  
> 2. $y_1[n] + y_2[n]$ and verify $h[n]$  
> 3. The **system function** $H(z)$ and frequency response $H(\omega)$  
> 4. **Analytical** magnitude and phase response  
> 5. Combined system with $T_1$, $T_2$, $T_3$

---

## 1-1) Sum of inputs

We add term-by-term:
$$
\begin{aligned}
x_1[n] + x_2[n]
&= \big(\delta[n] - 2\delta[n-1]\big) + \big(-\delta[n] + 3\delta[n-1]\big) \\
&= (1-1)\delta[n] + (-2+3)\delta[n-1] \\
&= \delta[n-1].
\end{aligned}
$$

So
$$
\boxed{x_1[n] + x_2[n] = \delta[n-1]}
$$

> [!code]- MATLAB — 1-1 quick check
> ```matlab
> % Problem 1-1: x1[n] + x2[n]
> x1 = [1, -2];       % coefficients at n=0,1
> x2 = [-1, 3];       % coefficients at n=0,1
> x_sum = x1 + x2;    % should be [0, 1] = δ[n-1]
> disp('x1 + x2 ='); disp(x_sum);
> ```

---

## 1-2a) Sum of outputs

From the table, we add $y_1[n] + y_2[n]$ for each $n$:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 |
|-----|---|---|---|-----|-----|-----|
| $y_1[n]$ | 1 | 0 | 2 | -10 | -3 | -2 |
| $y_2[n]$ | -1 | 1 | 0 | 16 | 5 | 3 |
| **Sum** | 0 | 1 | 2 | 6 | 2 | 1 |

So
$$
\boxed{y_1[n] + y_2[n] = \{0, 1, 2, 6, 2, 1\} \text{ for } n = 0,1,2,3,4,5}
$$

> [!code]- MATLAB — 1-2a
> ```matlab
> % Problem 1-2a: y1[n] + y2[n]
> y1 = [1, 0, 2, -10, -3, -2];
> y2 = [-1, 1, 0, 16, 5, 3];
> y_sum = y1 + y2;
> disp('y1 + y2 ='); disp(y_sum);
> % Result: [0, 1, 2, 6, 2, 1]
> ```

---

## 1-2b) Verify the impulse response

> **Key insight:** From 1-1, we found $x_1[n] + x_2[n] = \delta[n-1]$.
> 
> By **LTI linearity**: output to $\delta[n-1]$ is $h[n-1]$ (time-shifted impulse response).

Therefore:
$$
y_1[n] + y_2[n] = h[n-1]
$$

From 1-2a, $y_1[n] + y_2[n] = \{0, 1, 2, 6, 2, 1\}$ starting at $n=0$.

This means $h[n-1] = \{0, 1, 2, 6, 2, 1\}$, so shifting back:
$$
h[n] = \{1, 2, 6, 2, 1\} \text{ for } n = 0,1,2,3,4
$$

Writing in delta notation:
$$
\boxed{h[n] = \delta[n] + 2\delta[n-1] + 6\delta[n-2] + 2\delta[n-3] + \delta[n-4]}
$$

✓ This matches the given impulse response!

> [!info] Observation
> Notice that $h[n]$ is **symmetric**: $h[0]=h[4]=1$, $h[1]=h[3]=2$, $h[2]=6$.
> This is a **Type I linear phase FIR filter** (odd length, symmetric).

> [!code]- MATLAB — 1-2b verification
> ```matlab
> % Problem 1-2b: verify h[n]
> y_sum = [0, 1, 2, 6, 2, 1];  % y1+y2 starting at n=0
> h = y_sum(2:end);            % shift: h[n] = (y1+y2)[n+1]
> disp('h[n] ='); disp(h);
> % Result: [1, 2, 6, 2, 1] ✓
> 
> % Check symmetry
> h_expected = [1, 2, 6, 2, 1];
> disp(['Symmetric: ' num2str(isequal(h, fliplr(h)))]);
> ```

---

## 1-3a) System function $H(z)$

For a causal FIR filter, the system function is the Z-transform of $h[n]$:
$$
H(z) = \sum_{n=0}^{4} h[n] z^{-n} = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}
$$

So
$$
\boxed{H(z) = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}}
$$

> [!code]- MATLAB — 1-3a
> ```matlab
> % Problem 1-3a: H(z)
> h = [1, 2, 6, 2, 1];
> B = h;      % numerator
> A = 1;      % FIR filter
> 
> % Display as transfer function
> sys = tf(B, A, -1, 'Variable', 'z^-1');
> disp(sys);
> ```

---

## 1-3b) Frequency response $H(\omega)$

The frequency response is obtained by evaluating $H(z)$ on the unit circle, $z = e^{j\omega}$:
$$
H(\omega) = H(z)\big|_{z=e^{j\omega}} = 1 + 2e^{-j\omega} + 6e^{-j2\omega} + 2e^{-j3\omega} + e^{-j4\omega}
$$

So
$$
\boxed{H(\omega) = 1 + 2e^{-j\omega} + 6e^{-j2\omega} + 2e^{-j3\omega} + e^{-j4\omega}}
$$

---

## 1-4a) Analytical magnitude and phase

> **Strategy:** Exploit the **symmetry** of $h[n]$ to factor out a linear phase term.

For a symmetric FIR filter of length $M+1 = 5$ (so $M=4$), we can write:
$$
H(\omega) = e^{-j\omega M/2} \cdot A(\omega)
$$
where $A(\omega)$ is a **real-valued amplitude function** and $M/2 = 2$.

### Derivation

Factor out $e^{-j2\omega}$ from each term:
$$
\begin{aligned}
H(\omega) &= e^{-j2\omega}\Big[e^{j2\omega} + 2e^{j\omega} + 6 + 2e^{-j\omega} + e^{-j2\omega}\Big]
\end{aligned}
$$

Using Euler's identity $e^{jx} + e^{-jx} = 2\cos(x)$:
$$
\begin{aligned}
H(\omega) &= e^{-j2\omega}\Big[2\cos(2\omega) + 4\cos(\omega) + 6\Big]
\end{aligned}
$$

So the **amplitude function** is:
$$
\boxed{A(\omega) = 6 + 4\cos(\omega) + 2\cos(2\omega)}
$$

### Magnitude response

Since $H(\omega) = e^{-j2\omega} \cdot A(\omega)$:
$$
|H(\omega)| = |e^{-j2\omega}| \cdot |A(\omega)| = |A(\omega)|
$$

> [!warning] Trap Alert!
> The magnitude is $|A(\omega)|$, **not** $A(\omega)$!
> If $A(\omega) < 0$ for some $\omega$, then $|H(\omega)| = -A(\omega)$ in that region.

Let's check if $A(\omega) \geq 0$ for all $\omega$:
- At $\omega = 0$: $A(0) = 6 + 4(1) + 2(1) = 12$ ✓
- At $\omega = \pi$: $A(\pi) = 6 + 4(-1) + 2(1) = 4$ ✓
- At $\omega = \pi/2$: $A(\pi/2) = 6 + 4(0) + 2(-1) = 4$ ✓

Since $A(\omega) > 0$ for all $\omega$, we have:
$$
\boxed{|H(\omega)| = 6 + 4\cos(\omega) + 2\cos(2\omega)}
$$

### Phase response

Since $A(\omega) > 0$:
$$
\boxed{\angle H(\omega) = -2\omega}
$$

This is **pure linear phase** with group delay $\tau_g = 2$ samples.

> [!code]- MATLAB — 1-4a analytical check
> ```matlab
> % Problem 1-4a: verify analytical magnitude/phase
> omega = linspace(-pi, pi, 1024);
> 
> % Analytical amplitude function
> A_omega = 6 + 4*cos(omega) + 2*cos(2*omega);
> 
> % Check: A(omega) should be positive everywhere
> fprintf('Min A(omega) = %.4f\n', min(A_omega));
> 
> % Magnitude = |A(omega)|
> H_mag_analytical = abs(A_omega);
> 
> % Phase = -2*omega (when A > 0)
> H_phase_analytical = -2*omega;
> ```

---

## 1-4b) Plot magnitude and phase response

> [!code]- MATLAB — 1-4b plots
> ```matlab
> % Problem 1-4b: plot magnitude and phase
> h = [1, 2, 6, 2, 1];
> omega = linspace(-pi, pi, 1024);
> 
> [H, w] = freqz(h, 1, omega);
> 
> figure;
> subplot(2,1,1);
> plot(w/pi, abs(H), 'b', 'LineWidth', 1.5);
> xlabel('\omega / \pi'); ylabel('|H(\omega)|');
> title('Magnitude Response');
> grid on;
> 
> subplot(2,1,2);
> plot(w/pi, unwrap(angle(H)), 'r', 'LineWidth', 1.5);
> hold on;
> plot(w/pi, -2*w, 'k--', 'LineWidth', 1);  % analytical: -2ω
> xlabel('\omega / \pi'); ylabel('\angle H(\omega) [rad]');
> title('Phase Response');
> legend('Actual', 'Analytical: -2\omega');
> grid on;
> ```

![[Images/DSP_Exam_F25_1_4_MagPhase.png]]

---

## 1-5) Combined system: $T_1$, $T_2$, $T_3$

> **Given:**
> - $H_1(z) = H(z) = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}$
> - $H_2(z) = 3 - 10z^{-1} - 11z^{-2}$
> - $H_3(z) = \dfrac{1}{1 - \frac{1}{4}z^{-2}}$
>
> **Diagram:** $T_1$ and $T_2$ in **parallel**, then $T_3$ in **series**.

### Combined transfer function

$$
H_{total}(z) = \big(H_1(z) + H_2(z)\big) \cdot H_3(z)
$$

**Step 1:** Compute $H_1(z) + H_2(z)$

$$
\begin{aligned}
H_1(z) + H_2(z) &= (1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}) + (3 - 10z^{-1} - 11z^{-2}) \\
&= 4 - 8z^{-1} - 5z^{-2} + 2z^{-3} + z^{-4}
\end{aligned}
$$

**Step 2:** Multiply by $H_3(z)$

$$
H_{total}(z) = \frac{4 - 8z^{-1} - 5z^{-2} + 2z^{-3} + z^{-4}}{1 - \frac{1}{4}z^{-2}}
$$

**Step 3:** Check if this simplifies (pole-zero cancellation)

The denominator $1 - \frac{1}{4}z^{-2} = \frac{z^2 - 1/4}{z^2}$ has zeros at $z = \pm\frac{1}{2}$.

Check if numerator has factors $(1 - \frac{1}{2}z^{-1})$ or $(1 + \frac{1}{2}z^{-1})$:

**YOUR CALCULATION HERE** — Use polynomial division or MATLAB `deconv`.

> [!code]- MATLAB — 1-5 combined system
> ```matlab
> % Problem 1-5: combined system
> H1 = [1, 2, 6, 2, 1];
> H2 = [3, -10, -11];
> H3_num = 1;
> H3_den = [1, 0, -1/4];  % 1 - (1/4)z^{-2}
> 
> % H1 + H2 (pad H2 with zeros to match length)
> H2_padded = [H2, 0, 0];  % [3, -10, -11, 0, 0]
> H12 = H1 + H2_padded;    % parallel combination
> disp('H1(z) + H2(z) ='); disp(H12);
> 
> % Total: (H1 + H2) * H3 = H12 / H3_den
> % Numerator of total = conv(H12, H3_num) = H12
> % Denominator of total = H3_den
> 
> % Check for pole-zero cancellation
> [q, r] = deconv(H12, H3_den);
> disp('Quotient (if exact FIR):'); disp(q);
> disp('Remainder:'); disp(r);
> 
> % If remainder is zero → exact cancellation → FIR!
> ```

### Is it FIR?

**Argument:** If the numerator $H_1(z) + H_2(z)$ is exactly divisible by the denominator $1 - \frac{1}{4}z^{-2}$, then all poles cancel with zeros, leaving only a polynomial in $z^{-1}$ → **FIR**.

$$
\boxed{\text{YOUR FINAL ANSWER HERE}}
$$

---

# Problem 2 — IIR Butterworth Highpass Filter (BLT)

> **Given specifications:**
> - Design method: **Bilinear Transform (BLT)** with $\alpha = 2/T_s$
> - Filter type: **IIR Highpass Butterworth**
> - Sampling frequency: $F_s = 4000$ Hz
> - Stopband edge: $f_s = 450$ Hz (normalized: $f_s/F_s$)
> - Passband edge: $f_p = 1000$ Hz (normalized: $f_p/F_s$)
> - Stopband attenuation: $A_s = 30$ dB
> - Passband attenuation: $A_p = 3$ dB

---

## 2-1) Analog prototype Butterworth filter

### (a) Calculate $\varepsilon$

For a Butterworth filter with passband ripple $A_p$ dB:
$$
\varepsilon = \sqrt{10^{A_p/10} - 1}
$$

With $A_p = 3$ dB:
$$
\varepsilon = \sqrt{10^{0.3} - 1} = \sqrt{2 - 1} = \sqrt{1} = 1
$$

$$
\boxed{\varepsilon = 1}
$$

### (b) Pre-warped analog frequencies

Digital angular frequencies:
$$
\omega_s = 2\pi \frac{f_s}{F_s} = 2\pi \frac{450}{4000} = 0.225\pi \text{ rad/sample}
$$
$$
\omega_p = 2\pi \frac{f_p}{F_s} = 2\pi \frac{1000}{4000} = 0.5\pi \text{ rad/sample}
$$

Pre-warping formula: $\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2F_s \tan\left(\frac{\omega}{2}\right)$

$$
\Omega_s = 2 \times 4000 \times \tan\left(\frac{0.225\pi}{2}\right) = 8000 \times \tan(0.1125\pi)
$$

$$
\Omega_p = 2 \times 4000 \times \tan\left(\frac{0.5\pi}{2}\right) = 8000 \times \tan(0.25\pi) = 8000 \times 1 = 8000
$$

**YOUR NUMERICAL CALCULATION HERE**

$$
\boxed{\Omega_s = \text{???} \text{ rad/s}, \quad \Omega_p = 8000 \text{ rad/s}}
$$

### (c) Minimum filter order $n$

For **highpass**, the selectivity ratio is:
$$
\text{ratio} = \frac{\Omega_p}{\Omega_s}
$$

> [!warning] Trap Alert!
> For **highpass**, the ratio is $\Omega_p/\Omega_s$ (inverted compared to lowpass!)

The Butterworth order formula:
$$
n \geq \frac{\log_{10}\left(\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\log_{10}(\text{ratio})}
$$

**YOUR CALCULATION HERE**

$$
\boxed{n = \text{???}}
$$

### (d) Prototype transfer function

From the appendix table, for order $n$:

$$
H_{LP}(s) = \frac{1}{\text{denominator from table}}
$$

> [!code]- MATLAB — 2-1
> ```matlab
> % Problem 2-1: Analog prototype design
> Fs = 4000;
> Ts = 1/Fs;
> 
> fs_hz = 450;
> fp_hz = 1000;
> As_dB = 30;
> Ap_dB = 3;
> 
> % Digital frequencies
> omega_s = 2*pi*fs_hz/Fs;
> omega_p = 2*pi*fp_hz/Fs;
> 
> % Pre-warping
> Omega_s = 2*Fs * tan(omega_s/2);
> Omega_p = 2*Fs * tan(omega_p/2);
> 
> fprintf('Omega_s = %.2f rad/s\n', Omega_s);
> fprintf('Omega_p = %.2f rad/s\n', Omega_p);
> 
> % Epsilon
> epsilon = sqrt(10^(Ap_dB/10) - 1);
> fprintf('epsilon = %.4f\n', epsilon);
> 
> % Order (highpass: ratio = Omega_p / Omega_s)
> ratio = Omega_p / Omega_s;
> n_exact = log10((10^(As_dB/10)-1)/(10^(Ap_dB/10)-1)) / (2*log10(ratio));
> n = ceil(n_exact);
> fprintf('n_exact = %.4f, n = %d\n', n_exact, n);
> ```

---

## 2-2) LP to HP transformation

> If order not found above, assume $n = 4$.

### (a) Transformation formula

To convert lowpass prototype to highpass:
$$
s_{LP} \rightarrow \frac{\Omega_p}{s}
$$

### (b) Analog highpass $H_{HP}(s)$

**YOUR DERIVATION OR MATLAB HERE**

> [!code]- MATLAB — 2-2
> ```matlab
> % Problem 2-2: LP to HP transformation
> % Prototype (use n=4 if needed)
> n = 4;
> B_proto = 1;
> A_proto = [1, 2.6131, 3.4142, 2.6131, 1];  % n=4 from table
> 
> % Transform to highpass
> [B_hp, A_hp] = lp2hp(B_proto, A_proto, Omega_p);
> 
> % Display
> H_hp = tf(B_hp, A_hp);
> disp('H_HP(s) ='); disp(H_hp);
> ```

### (c) Plot analog magnitude response

> [!code]- MATLAB — 2-2c plot
> ```matlab
> % Problem 2-2c: Analog HP magnitude
> Omega = linspace(0, 20000, 2000);
> H_analog = freqs(B_hp, A_hp, Omega);
> 
> figure;
> plot(Omega, 20*log10(abs(H_analog)), 'LineWidth', 1.5);
> xlabel('\Omega [rad/s]'); ylabel('|H_{HP}(j\Omega)| [dB]');
> title('Analog Highpass Magnitude Response');
> grid on;
> xline(Omega_s, '--r', '\Omega_s');
> xline(Omega_p, '--g', '\Omega_p');
> ```

### (d) Does it meet analog specs?

**YOUR ARGUMENT HERE**

---

## 2-3) Bilinear transformation to digital

### (a) BLT relation

$$
s = \frac{2}{T_s} \cdot \frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_s} \cdot \frac{z - 1}{z + 1}
$$

With $\alpha = 2/T_s = 2F_s = 8000$.

### (b) Digital highpass $H_{HP}(z)$

> [!code]- MATLAB — 2-3
> ```matlab
> % Problem 2-3: BLT to digital
> [Bz, Az] = bilinear(B_hp, A_hp, Fs);
> 
> % Display as z^-1 transfer function
> H_digital = tf(Bz, Az, 1/Fs, 'Variable', 'z^-1');
> disp('H_HP(z) ='); disp(H_digital);
> 
> % Show coefficients
> fprintf('b coefficients: '); disp(Bz);
> fprintf('a coefficients: '); disp(Az);
> ```

$$
H_{HP}(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_N z^{-N}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}
$$

**YOUR NUMERICAL COEFFICIENTS HERE**

---

## 2-4) Verify digital filter

### (a) Plot magnitude response in dB vs frequency (Hz)

> [!code]- MATLAB — 2-4a
> ```matlab
> % Problem 2-4a: Digital magnitude response
> [H, f] = freqz(Bz, Az, 2048, Fs);
> 
> figure;
> plot(f, 20*log10(abs(H)), 'b', 'LineWidth', 1.5);
> xlabel('Frequency F [Hz]'); ylabel('|H_{HP}(F)| [dB]');
> title('Digital Highpass Magnitude Response');
> grid on;
> xlim([0 Fs/2]);
> 
> % Mark specifications
> xline(450, '--r', 'f_s = 450 Hz');
> xline(1000, '--g', 'f_p = 1000 Hz');
> yline(-3, ':k', '-3 dB');
> yline(-30, ':k', '-30 dB');
> ```

![[Images/DSP_Exam_F25_2_4_DigitalHP_Magnitude.png]]

### (b) Read attenuation at 450 Hz and 1000 Hz

> [!code]- MATLAB — 2-4b
> ```matlab
> % Problem 2-4b: Attenuation at specific frequencies
> f_test = [450, 1000];
> [H_test, ~] = freqz(Bz, Az, f_test, Fs);
> att_dB = 20*log10(abs(H_test));
> 
> fprintf('At 450 Hz:  %.2f dB\n', att_dB(1));
> fprintf('At 1000 Hz: %.2f dB\n', att_dB(2));
> ```

| Frequency | Attenuation | Requirement |
|-----------|-------------|-------------|
| 450 Hz (stopband) | ??? dB | ≤ -30 dB |
| 1000 Hz (passband) | ??? dB | ≥ -3 dB |

### (c) Does the filter meet specifications?

**YOUR DISCUSSION HERE**

- Stopband: At 450 Hz, attenuation should be ≤ -30 dB. Measured: ???
- Passband: At 1000 Hz, attenuation should be ≥ -3 dB. Measured: ???

$$
\boxed{\text{Filter meets/does not meet specifications because...}}
$$

---

# Problem 3 — Sampling, Aliasing, and Inverse Systems

> **Given:**
> Continuous-time signal:
> $$
> x(t) = 3\cos(2\pi \cdot 1500 \cdot t) + 2\cos(2\pi \cdot 4200 \cdot t), \quad t \geq 0
> $$
> Sampling frequency: $F_s = 8000$ Hz

---

## 3-1) Sketch amplitude spectrum from -10 kHz to 10 kHz

### Original signal frequencies
- Component 1: $F_1 = 1500$ Hz, amplitude $A_1 = 3$
- Component 2: $F_2 = 4200$ Hz, amplitude $A_2 = 2$

### Nyquist frequency
$$
F_{Nyquist} = \frac{F_s}{2} = \frac{8000}{2} = 4000 \text{ Hz}
$$

### After sampling: spectral replication
Sampling replicates the spectrum at multiples of $F_s$:
$$
F_{aliased} = F \pm k \cdot F_s, \quad k = 0, \pm 1, \pm 2, \ldots
$$

**Component 1 ($F_1 = 1500$ Hz):** $1500 < 4000$ ✓ No aliasing
- Appears at: $\pm 1500$ Hz (and replicas at $\pm 1500 \pm 8000$, etc.)

**Component 2 ($F_2 = 4200$ Hz):** $4200 > 4000$ ⚠️ **ALIASING!**
- Folds to: $F_{apparent} = F_s - F_2 = 8000 - 4200 = 3800$ Hz
- Appears at: $\pm 3800$ Hz

### Spectrum sketch

| Frequency | Amplitude | Source |
|-----------|-----------|--------|
| $\pm 1500$ Hz | 3/2 | Original $F_1$ |
| $\pm 3800$ Hz | 2/2 = 1 | Aliased $F_2$ |
| $\pm 6500$ Hz | 3/2 | Replica of $F_1$ at $8000-1500$ |
| $\pm 9500$ Hz | 3/2 | Replica of $F_1$ at $8000+1500$ |

> [!code]- MATLAB — 3-1 spectrum plot
> ```matlab
> % Problem 3-1: Amplitude spectrum after sampling
> F1 = 1500; A1 = 3;
> F2 = 4200; A2 = 2;
> Fs = 8000;
> 
> % For cosine: amplitude spectrum has spikes at ±F with height A/2
> % After sampling: replicate at ±k*Fs
> 
> % Original frequencies (before aliasing consideration)
> freqs_orig = [-F2, -F1, F1, F2];
> amps_orig = [A2/2, A1/2, A1/2, A2/2];
> 
> % F2 aliases: 4200 -> 8000-4200 = 3800
> F2_alias = Fs - F2;  % = 3800
> 
> % Build spectrum from -10kHz to 10kHz
> figure;
> hold on;
> 
> % Plot impulses at each frequency
> for k = -1:1
>     % F1 component
>     stem(F1 + k*Fs, A1/2, 'b', 'LineWidth', 2);
>     stem(-F1 + k*Fs, A1/2, 'b', 'LineWidth', 2);
>     % F2 component (aliased to 3800)
>     stem(F2_alias + k*Fs, A2/2, 'r', 'LineWidth', 2);
>     stem(-F2_alias + k*Fs, A2/2, 'r', 'LineWidth', 2);
> end
> 
> xlabel('Frequency [Hz]');
> ylabel('Amplitude');
> title('Amplitude Spectrum of Sampled Signal');
> xlim([-10000 10000]);
> grid on;
> legend('F_1 = 1500 Hz', '', 'F_2 aliased to 3800 Hz');
> ```

![[Images/DSP_Exam_F25_3_1_Spectrum.png]]

---

## 3-2) Is there aliasing in [-4 kHz, 4 kHz]?

**Analysis:**

The Nyquist frequency is $F_{Nyquist} = F_s/2 = 4000$ Hz.

- $F_1 = 1500$ Hz: Since $1500 < 4000$, this component is **not aliased**.
- $F_2 = 4200$ Hz: Since $4200 > 4000$, this component **IS aliased**.

**Aliased frequency of $F_2$:**
$$
F_{2,aliased} = F_s - F_2 = 8000 - 4200 = 3800 \text{ Hz}
$$

$$
\boxed{\text{Yes, aliasing occurs. } F_2 = 4200 \text{ Hz aliases to } 3800 \text{ Hz}}
$$

> [!warning] Key Point
> The 4200 Hz component appears at 3800 Hz after sampling. This is **indistinguishable** from a true 3800 Hz signal — information is lost!

---

## 3-3) Digital filter $H_1(z)$ analysis

> **Given difference equation:**
> $$
> y[n] - 0.7y[n-1] + 0.1y[n-2] = x[n] + x[n-1]
> $$

### System function $H_1(z)$

Taking the Z-transform:
$$
Y(z) - 0.7z^{-1}Y(z) + 0.1z^{-2}Y(z) = X(z) + z^{-1}X(z)
$$

$$
Y(z)\big(1 - 0.7z^{-1} + 0.1z^{-2}\big) = X(z)\big(1 + z^{-1}\big)
$$

$$
H_1(z) = \frac{Y(z)}{X(z)} = \frac{1 + z^{-1}}{1 - 0.7z^{-1} + 0.1z^{-2}}
$$

### Poles and zeros

**Numerator:** $B(z) = 1 + z^{-1}$
- Zero: $1 + z^{-1} = 0 \Rightarrow z = -1$

**Denominator:** $A(z) = 1 - 0.7z^{-1} + 0.1z^{-2}$

Multiply by $z^2$: $z^2 - 0.7z + 0.1 = 0$

Using quadratic formula:
$$
z = \frac{0.7 \pm \sqrt{0.49 - 0.4}}{2} = \frac{0.7 \pm \sqrt{0.09}}{2} = \frac{0.7 \pm 0.3}{2}
$$

- Pole 1: $z_1 = \frac{0.7 + 0.3}{2} = 0.5$
- Pole 2: $z_2 = \frac{0.7 - 0.3}{2} = 0.2$

### Pole-zero summary

| Type | Location | $|z|$ |
|------|----------|-------|
| Zero | $z = -1$ | 1 (on unit circle) |
| Pole | $z = 0.5$ | 0.5 (inside UC) |
| Pole | $z = 0.2$ | 0.2 (inside UC) |

### ROC and stability

For a **causal** system, ROC is outside the outermost pole:
$$
\text{ROC: } |z| > 0.5
$$

Since all poles are **inside the unit circle** ($|z| < 1$), and the ROC includes the unit circle:

$$
\boxed{H_1(z) \text{ is stable (all poles inside UC, } |p| < 1\text{)}}
$$

> [!code]- MATLAB — 3-3 pole-zero plot
> ```matlab
> % Problem 3-3: H1(z) pole-zero analysis
> B = [1, 1];           % 1 + z^{-1}
> A = [1, -0.7, 0.1];   % 1 - 0.7z^{-1} + 0.1z^{-2}
> 
> zeros_H1 = roots(B);
> poles_H1 = roots(A);
> 
> fprintf('Zeros: '); disp(zeros_H1.');
> fprintf('Poles: '); disp(poles_H1.');
> fprintf('|poles| = '); disp(abs(poles_H1).');
> 
> figure;
> zplane(B, A);
> title('H_1(z) Pole-Zero Diagram');
> grid on;
> ```

![[Images/DSP_Exam_F25_3_3_PoleZero.png]]

### Inverse system $H_2(z) = 1/H_1(z)$

The inverse system is:
$$
H_2(z) = \frac{1}{H_1(z)} = \frac{1 - 0.7z^{-1} + 0.1z^{-2}}{1 + z^{-1}}
$$

**Poles and zeros swap:**
- **Poles of $H_2$:** zeros of $H_1$ → $z = -1$
- **Zeros of $H_2$:** poles of $H_1$ → $z = 0.5, 0.2$

**Stability of $H_2(z)$:**

$H_2(z)$ has a pole at $z = -1$, which is **on the unit circle** ($|z| = 1$).

$$
\boxed{H_2(z) = 1/H_1(z) \text{ is marginally stable (pole on unit circle at } z = -1\text{)}}
$$

> [!info] Marginal stability
> A system with poles **on** (not inside) the unit circle is called **marginally stable**. 
> - Bounded input may produce unbounded output
> - Impulse response neither decays nor grows exponentially — it oscillates

---

# Problem 4 — Filter Realization and Signal Filtering

> **Given:**
> A digital lowpass filter with 3 dB attenuation at 400 Hz, realized as shown in the block diagram.
> 
> **Coefficients from diagram:**
> - Feedforward (numerator): $b_0 = 0.0102$, $b_1 = 0.0305$, $b_2 = 0.0305$, $b_3 = 0.0102$
> - Feedback (denominator): $a_1 = -2.0038$, $a_2 = 1.4471$, $a_3 = -0.3618$
> 
> Sampling frequency: $F_s = 5000$ Hz

---

## 4-1) Identify filter structure

### (a) Filter form

Looking at the block diagram structure:
- Left side: input $x[n]$ with feedforward coefficients ($b$ values)
- Right side: output $y[n]$ with feedback from delayed outputs ($a$ values)
- Delays ($z^{-1}$) are shared between input and output paths

$$
\boxed{\text{Direct Form II (Transposed or Canonical)}}
$$

### (b) FIR or IIR?

**IIR** because:
- There are **feedback terms** (output $y[n]$ depends on past outputs $y[n-1], y[n-2], y[n-3]$)
- Denominator is not just 1
- The filter has **poles** (not just zeros)

$$
\boxed{\text{IIR filter — has feedback (recursive structure)}}
$$

### (c) Transfer function $H(z)$

From the coefficients:
$$
H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + b_3 z^{-3}}{1 + a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3}}
$$

$$
\boxed{H(z) = \frac{0.0102 + 0.0305z^{-1} + 0.0305z^{-2} + 0.0102z^{-3}}{1 - 2.0038z^{-1} + 1.4471z^{-2} - 0.3618z^{-3}}}
$$

> [!code]- MATLAB — 4-1
> ```matlab
> % Problem 4-1: Filter coefficients
> b = [0.0102, 0.0305, 0.0305, 0.0102];
> a = [1, -2.0038, 1.4471, -0.3618];
> Fs = 5000;
> 
> % Display transfer function
> H = tf(b, a, 1/Fs, 'Variable', 'z^-1');
> disp('H(z) ='); disp(H);
> ```

---

## 4-2) Magnitude response and -3 dB frequency

### (a) Plot magnitude response in dB

> [!code]- MATLAB — 4-2a
> ```matlab
> % Problem 4-2a: Magnitude response
> [H_freq, f] = freqz(b, a, 2048, Fs);
> 
> figure;
> plot(f, 20*log10(abs(H_freq)), 'b', 'LineWidth', 1.5);
> xlabel('Frequency F [Hz]');
> ylabel('|H(F)| [dB]');
> title('Lowpass Filter Magnitude Response');
> grid on;
> xlim([0 Fs/2]);
> yline(-3, '--r', '-3 dB');
> xline(400, '--g', '400 Hz');
> ```

![[Images/DSP_Exam_F25_4_2_Magnitude.png]]

### (b) Read -3 dB frequency

> [!code]- MATLAB — 4-2b
> ```matlab
> % Problem 4-2b: Find -3 dB frequency
> mag_dB = 20*log10(abs(H_freq));
> idx_3dB = find(mag_dB <= -3, 1, 'first');
> f_3dB = f(idx_3dB);
> fprintf('-3 dB frequency: %.1f Hz\n', f_3dB);
> 
> % Or evaluate at exactly 400 Hz
> [H_400, ~] = freqz(b, a, [400], Fs);
> fprintf('Attenuation at 400 Hz: %.2f dB\n', 20*log10(abs(H_400)));
> ```

**Expected:** The -3 dB frequency should be approximately 400 Hz as stated in the problem.

$$
\boxed{f_{-3dB} \approx 400 \text{ Hz — matches specification}}
$$

---

## 4-3) Pole-zero analysis and stability

### (a) Find and plot poles and zeros

> [!code]- MATLAB — 4-3a
> ```matlab
> % Problem 4-3: Poles and zeros
> zeros_H = roots(b);
> poles_H = roots(a);
> 
> fprintf('Zeros:\n'); disp(zeros_H);
> fprintf('Poles:\n'); disp(poles_H);
> fprintf('|poles| = '); disp(abs(poles_H).');
> 
> figure;
> zplane(b, a);
> title('Filter Pole-Zero Diagram');
> grid on;
> ```

![[Images/DSP_Exam_F25_4_3_PoleZero.png]]

### (b) Is the filter stable?

**Stability criterion:** All poles must be **strictly inside** the unit circle ($|p| < 1$).

**YOUR ANALYSIS HERE** — Check $|p_i|$ for each pole.

If all $|p_i| < 1$:
$$
\boxed{\text{Filter is stable — all poles inside unit circle}}
$$

---

## 4-4) Sampling an analog signal

> **Given analog signal:**
> $$
> x_a(t) = 5\cos(2\pi \cdot 50 \cdot t) + 3\cos(2\pi \cdot 1000 \cdot t)
> $$
> - $A_1 = 5$, $F_1 = 50$ Hz
> - $A_2 = 3$, $F_2 = 1000$ Hz
> - Sampling: $F_s = 5000$ Hz

### (a) Is there aliasing?

Nyquist frequency: $F_{Nyquist} = F_s/2 = 2500$ Hz

- $F_1 = 50$ Hz: $50 < 2500$ ✓ **No aliasing**
- $F_2 = 1000$ Hz: $1000 < 2500$ ✓ **No aliasing**

$$
\boxed{\text{No aliasing — both frequencies are below Nyquist (2500 Hz)}}
$$

### (b) Plot sampled signal from 0 to 0.05 seconds

> [!code]- MATLAB — 4-4b
> ```matlab
> % Problem 4-4b: Sample and plot signal
> Fs = 5000;
> t = 0 : 1/Fs : 0.05;    % 0 to 50 ms
> 
> A1 = 5; F1 = 50;
> A2 = 3; F2 = 1000;
> 
> x_sampled = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);
> 
> figure;
> plot(t, x_sampled, 'b', 'LineWidth', 1);
> xlabel('Time [s]');
> ylabel('x[n]');
> title('Sampled Signal');
> grid on;
> xlim([0 0.05]);
> ```

![[Images/DSP_Exam_F25_4_4_SampledSignal.png]]

---

## 4-5) Filter the sampled signal

### (a) What does the filter do to each component?

The filter is a **lowpass** with $f_{-3dB} = 400$ Hz.

| Component | Frequency | Relative to cutoff | Effect |
|-----------|-----------|-------------------|--------|
| $F_1 = 50$ Hz | In passband | $50 \ll 400$ | **Passes through** (minimal attenuation) |
| $F_2 = 1000$ Hz | In stopband | $1000 > 400$ | **Attenuated** (significant reduction) |

$$
\boxed{\text{50 Hz component passes; 1000 Hz component is attenuated}}
$$

### (b) Filter using MATLAB

> [!code]- MATLAB — 4-5b
> ```matlab
> % Problem 4-5b: Filter the signal
> y_filtered = filter(b, a, x_sampled);
> 
> figure;
> subplot(2,1,1);
> plot(t, x_sampled, 'b', 'LineWidth', 1);
> xlabel('Time [s]'); ylabel('Amplitude');
> title('Input Signal x[n]');
> grid on;
> 
> subplot(2,1,2);
> plot(t, y_filtered, 'r', 'LineWidth', 1);
> xlabel('Time [s]'); ylabel('Amplitude');
> title('Filtered Signal y[n]');
> grid on;
> ```

![[Images/DSP_Exam_F25_4_5_FilteredSignal.png]]

### (c) Compare input and output

**Observations:**

1. **Input signal:** Shows both the slow 50 Hz oscillation AND the fast 1000 Hz ripple superimposed.

2. **Output signal:** 
   - The slow 50 Hz oscillation **remains** (approximately same amplitude)
   - The fast 1000 Hz ripple is **removed/attenuated**
   - Signal is "smoother"

3. **Transient:** There may be a short startup transient at the beginning due to filter initial conditions.

$$
\boxed{\text{The lowpass filter removes the 1000 Hz component, leaving only the 50 Hz signal}}
$$

---

# Appendix — Butterworth Lowpass Prototype (ε = 1, 3 dB)

| Order $n$ | Denominator polynomial |
|:---------:|:-----------------------|
| 1 | $s + 1$ |
| 2 | $s^2 + 1.4142s + 1$ |
| 3 | $s^3 + 2s^2 + 2s + 1$ |
| 4 | $s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1$ |
| 5 | $s^5 + 3.2361s^4 + 5.2361s^3 + 5.2361s^2 + 3.2361s + 1$ |
| 6 | $s^6 + 3.8637s^5 + 7.4641s^4 + 9.1416s^3 + 7.4641s^2 + 3.8637s + 1$ |

All have numerator = 1.

---

# Quick Reference — Key Formulas

## Sampling & Aliasing
$$
F_{Nyquist} = \frac{F_s}{2}, \qquad F_{alias} = |F - k \cdot F_s| \text{ (folded into } [0, F_s/2])
$$

## Pre-warping (BLT)
$$
\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2F_s \tan\left(\pi \frac{F}{F_s}\right)
$$

## Butterworth Order
$$
n \geq \frac{\log_{10}\left(\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\log_{10}(\text{ratio})}
$$
- **Lowpass:** ratio = $\Omega_s / \Omega_p$
- **Highpass:** ratio = $\Omega_p / \Omega_s$

## Bilinear Transform
$$
s = \frac{2}{T_s} \cdot \frac{1 - z^{-1}}{1 + z^{-1}}
$$

## Linear Phase FIR (Symmetric)
$$
H(\omega) = e^{-j\omega M/2} \cdot A(\omega), \qquad |H(\omega)| = |A(\omega)|, \qquad \angle H(\omega) = -\frac{M}{2}\omega
$$

## Stability
- **Stable:** All poles strictly inside unit circle ($|p| < 1$)
- **Marginally stable:** At least one pole ON unit circle ($|p| = 1$)
- **Unstable:** At least one pole outside unit circle ($|p| > 1$)