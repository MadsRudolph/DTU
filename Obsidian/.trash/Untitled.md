
# 📄 DSP Exam Cheat Sheet (E23 & F24 Strategy)

---

## 1. LTI Systems & Z-Transform (Q1)

### **Step $\to$ Impulse Response**
If given the step response $y_{step}[n]$, the impulse response $h[n]$ is the "discrete derivative":
$$h[n] = y_{step}[n] - y_{step}[n-1]$$
* **[span_0](start_span)Why?** Because $\delta[n] = u[n] - u[n-1]$[span_0](end_span).
* **Check:** If $h[n]$ has finite length, it is **FIR**. [span_1](start_span)If it has recursion/feedback, it is **IIR**[span_1](end_span).

### **Linearity Trick (Unknown Inputs)**
If given outputs $y_1[n]$ and $y_2[n]$ for specific inputs $x_1[n]$ and $x_2[n]$:
1.  Find the linear combination of inputs that results in a delta function: $\alpha x_1[n] + \beta x_2[n] = \delta[n]$.
2.  Apply the exact same combination to the outputs to find $h[n]$:
    $$h[n] = \alpha y_1[n] + \beta y_2[n]$$

### **Analytic Frequency Response (Symmetry Trick)**
If calculating $H(\omega)$ by hand for a symmetric FIR filter (e.g., $h[n]$ is symmetric around $n=2$):
1.  Write out the sum: $H(\omega) = \sum h[n]e^{-j\omega n}$.
2.  **Factor out the center phase term** (e.g., $e^{-j2\omega}$).
3.  Group the remaining complex exponentials into cosines using Euler: $e^{jx} + e^{-jx} = 2\cos(x)$.
    $$H(\omega) = e^{-j\text{slope}\cdot\omega} \cdot \underbrace{\left[ h_{center} + 2h_1\cos(\omega) + \dots \right]}_{\text{Real Amplitude } A(\omega)}$$
    * **[span_2](start_span)Phase:** Linear phase $\angle H(\omega) = -\text{slope}\cdot\omega$ (plus $\pi$ jumps if $A(\omega)$ crosses zero)[span_2](end_span).

### **Cascade Decomposition**
If $H(z) = H_1(z) H_2(z)$ and you need to find $H_2(z)$:
$$H_2(z) = \frac{H(z)}{H_1(z)}$$
* **Analytic:** Perform polynomial long division.
* **[span_3](start_span)MATLAB:** Use deconvolution: `[h2, rem] = deconv(h_total, h1)`[span_3](end_span).

---

## 2. IIR Filter Design (Q2 - Bilinear Transform)

[attachment_0](attachment)

### **Step 1: Pre-warping (CRITICAL)**
**Never** use digital frequencies ($f$ in Hz) directly in analog design formulas. You must "warp" them first.
$$\Omega = 2F_s \tan\left(\pi \frac{f}{F_s}\right)$$
* **[span_4](start_span)[span_5](start_span)Variable Map:** $f_{pass}, f_{stop}$ (Hz) $\to$ $\Omega_p, \Omega_s$ (rad/s)[span_4](end_span)[span_5](end_span).

### **Step 2: Analog Prototype Design**
**Order Estimation ($N$):**
For Chebyshev Type I:
$$N \ge \frac{\cosh^{-1}\left(\sqrt{\frac{10^{0.1 A_s}-1}{10^{0.1 A_p}-1}}\right)}{\cosh^{-1}(\Omega_s / \Omega_p)}$$
* **[span_6](start_span)MATLAB:** `N = ceil(acosh(sqrt((10^(As/10)-1)/(10^(Ap/10)-1))) / acosh(Ws/Wp));`[span_6](end_span).

### **Step 3: Frequency Transformation (LP $\to$ HP/BS)**
Standard tables give a **Lowpass** prototype ($H_{LP}(s)$). You must transform $s$.
* **LP $\to$ Highpass:** Replace $s \to \frac{\Omega_p}{s}$.
* **[span_7](start_span)MATLAB:** `[B_hp, A_hp] = lp2hp(B_proto, A_proto, Omega_p);`[span_7](end_span).

### **Step 4: Bilinear Transform (Analog $\to$ Digital)**
Map the analog $H(s)$ to digital $H(z)$ using $s = 2F_s \frac{1-z^{-1}}{1+z^{-1}}$.
* **[span_8](start_span)[span_9](start_span)MATLAB:** `[Bz, Az] = bilinear(B_analog, A_analog, Fs);`[span_8](end_span)[span_9](end_span).

---

## 3. Sampling & Stability (Q3)

### **Nyquist Criterion**
To avoid aliasing, the sampling frequency $\Omega_s$ must be:
$$\Omega_s \ge 2\Omega_{max}$$
* **[span_10](start_span)Visual Check:** If $\Omega_s < 2\Omega_{max}$, the spectral copies $F_a(\Omega - k\Omega_s)$ will overlap[span_10](end_span).
* **Aliased Frequency:** The apparent frequency is $|F_{in} - k \cdot F_s|$ (find the one closest to 0).

### **Stability & Causality**
* **Stable:** All poles are **inside** the unit circle ($|p| < 1$).
* **Causal:** Impulse response $h[n] = 0$ for $n < 0$.
* **Inverse System:** $H_{inv}(z) = 1/H(z)$. This swaps poles and zeros.
    * *[span_11](start_span)Trap:* If $H(z)$ has a zero **outside** the unit circle, $H_{inv}(z)$ will have a pole **outside** (unstable if causal)[span_11](end_span).

### **Min-Phase / All-Pass Decomposition**
Any system can be written as $H(z) = H_{min}(z) \cdot H_{ap}(z)$.
* **Minimum Phase:** Reflect all "bad" zeros (outside unit circle) to the inside ($z_{in} = 1/z_{out}^*$).
* **All-Pass:** Compensates for the reflection. Form:
    $$H_{ap}(z) = \frac{z^{-1} - z_0^*}{1 - z_0 z^{-1}}$$

---

## 4. Essential MATLAB Templates

### **Universal Frequency Response (Mag + Phase)**
```matlab
% Defined filter coefficients B (num) and A (den)
[H, w] = freqz(B, A, 4096, Fs); % 'whole' for 0-2pi, or default for 0-pi
f = w;                          % Freq vector (if Fs included, w is in Hz)

figure;
subplot(2,1,1);
plot(f, 20*log10(abs(H))); grid on;
title('Magnitude Response'); ylabel('Magnitude (dB)'); xlabel('Frequency (Hz)');
xline([Fpass Fstop], '--r', {'Pass','Stop'}); % Mark specs

subplot(2,1,2);
plot(f, unwrap(angle(H))); grid on; % unwrapped phase
title('Phase Response'); ylabel('Phase (rad)'); xlabel('Frequency (Hz)');

Pole-Zero Plot
figure; 
zplane(B, A);
title('Pole-Zero Map');
legend('Zeros', 'Poles');
% Check: Are all 'x' inside the circle? -> Stable

Spectrum Analysis (FFT)
N = length(x);              % Signal length
X = fft(x);                 % Compute DFT
f = (-N/2 : N/2-1)*(Fs/N);  % Frequency axis centered at 0

figure;
plot(f, abs(fftshift(X))/N); % Shift 0 to center and scale
grid on; xlabel('Frequency (Hz)'); ylabel('Magnitude');
title('Signal Spectrum');


