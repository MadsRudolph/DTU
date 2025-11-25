> Exam set: [[62743 E23 Exam.pdf]]  
> Solution sheet: [[62743 E23 Exam student solutions.pdf]]  
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/EXAM/E23.mlx>)

---
# 62743 — E23 Exam (Digital Signal Processing)
---

## 📘 Big-Picture Overview

This note contains **fully worked solutions** to the **E23 written exam** in 62743 Digital Signal Processing.

For each exam problem:

- Short **context / theory recap**  
- Full **derivations** (not only final answers)  
- **MATLAB snippets** that match the separate Live Script  
- References to the **exported figures** from the Live Script

Structure:

1. **Problem 1 – LTI step → impulse, symmetric FIR & cascade**  
2. **Problem 2 – IIR high-pass Chebyshev design via BLT**  
3. **Problem 3 – Sampling, aliasing, and IIR ROC / inverse**  
4. **Problem 4 – FIR high-pass design from Fourier series + spectrum analysis**

---

# Problem 1 — LTI System from Step Response, Symmetry & Cascade

> A discrete-time LTI system is given by its response $y_1[n]$ to a unit step input $x_1[n]=u[n]$.  
> You must:
> 1. Derive the **impulse response** $h[n]$ and classify FIR/IIR.  
> 2. Find the **system function** $H(z)$ and **frequency response** $H(\omega)$.  
> 3. Use symmetry to derive **magnitude** $\lvert H(\omega)\rvert$ and **phase** $\angle H(\omega)$ analytically and compare with `freqz`.  
> 4. Use that the overall system is a cascade of two FIR filters to find the second system function $H_2(z)$.

The student solution gives the step response output $y_1[n]$ and the final impulse response.

---

## 1-1) Impulse response from step response (FIR/IIR?)

We are told that when the input is the step

$$
x_1[n] = u[n],
$$

the output is a finite linear combination of shifted deltas.

Key idea:  
Use the identity  

$$
\delta[n] = u[n]-u[n-1] = x_1[n]-x_1[n-1].
$$

Because the system is **LTI**,

$$
\begin{aligned}
h[n]
&= \text{output to } \delta[n]\\
&= \text{output to } \big(x_1[n]-x_1[n-1]\big)\\
&= y_1[n]-y_1[n-1].
\end{aligned}
$$

Carrying out the subtraction (using the given expression for $y_1[n]$), the impulse response becomes

$$
\boxed{
h[n] = -\delta[n] - 4\delta[n-1] + 10\delta[n-2] - 4\delta[n-3] - \delta[n-4]
}
$$

Non-zero samples:

$$
h[0]=-1,\;h[1]=-4,\;h[2]=10,\;h[3]=-4,\;h[4]=-1,\quad h[n]=0\ \text{otherwise}.
$$

Since $h[n]$ is **finite-length**, the system is a **causal FIR** filter.

> [!code]- MATLAB — 1-1 impulse response from step response
> ```matlab
> % Problem 1-1: Impulse response from step response
> 
> n = 0:10;                        % time indices (a bit larger than needed)
> delta = @(k) double(k == 0);
> u     = @(k) double(k >= 0);
> 
> % Given step response output y1[n] for x1[n] = u[n]:
> % y1[n] = -δ[n] - 5δ[n-1] + 5δ[n-2] + δ[n-3]
> y1 = -delta(n) - 5*delta(n-1) + 5*delta(n-2) + delta(n-3);
> 
> % Impulse: δ[n] = u[n] - u[n-1]; by LTI: h[n] = y1[n] - y1[n-1]
> y1_shift = [0, y1(1:end-1)];
> h = y1 - y1_shift;
> 
> fprintf('1-1) h[n] from step response:\n');
> disp([n; h].');
> 
> figure;
> stem(n,h,'filled'); grid on;
> xlabel('n'); ylabel('h[n]');
> title('E23: Problem 1-1 — Impulse response h[n]');
> print('Images/DSP_Exam_E23_1_ImpulseResponse','-dpng');
> ```

![[Images/DSP_Exam_E23_1_ImpulseResponse.png]]

---

## 1-2) System function $H(z)$ and frequency response $H(\omega)$

The impulse response is a 5-tap FIR:

$$
h[0]=-1,\ h[1]=-4,\ h[2]=10,\ h[3]=-4,\ h[4]=-1.
$$

The **system function** is the $z$-transform:

$$
\begin{aligned}
H(z)
&= \sum_{n=0}^4 h[n]z^{-n}\\
&= -1 - 4z^{-1} + 10z^{-2} - 4z^{-3} - z^{-4}.
\end{aligned}
$$

Thus

$$
\boxed{H(z) = -1 - 4z^{-1} + 10z^{-2} - 4z^{-3} - z^{-4}}
$$

The **frequency response** is obtained by evaluating on the unit circle:

$$
\boxed{
H(\omega) = H(z)\big|_{z=e^{j\omega}}
= -1 - 4e^{-j\omega} + 10e^{-j2\omega} - 4 e^{-j3\omega} - e^{-j4\omega}
}
$$

> [!code]- MATLAB — 1-2 system function and freq response handle
> ```matlab
> % Problem 1-2: System function H(z) and H(omega)
> 
> h = [-1 -4 10 -4 -1];   % h[0]..h[4]
> B = h;                  % FIR numerator
> A = 1;                  % denominator
> 
> fprintf('1-2) H(z) coefficients (numerator):\n');
> disp(B);
> 
> % Frequency response via freqz for comparison later
> Nw = 2048;
> [H_omega, w] = freqz(B, A, Nw, 'whole');  % 0..2pi
> ```

---

## 1-3) Magnitude and phase from symmetry + MATLAB check

The impulse response is **symmetric** around the middle tap $n=2$:

$$
h[0]=h[4] = -1,\quad h[1]=h[3]=-4,\quad h[2]=10.
$$

For an FIR of odd length $N=5$ with symmetry about $(N-1)/2=2$, we can factor out a pure delay:

$$
\begin{aligned}
H(\omega)
&= \sum_{n=0}^4 h[n]e^{-j\omega n}\\
&= e^{-j2\omega}\Big(h[2] + 2h[1]\cos\omega + 2h[0]\cos 2\omega\Big).
\end{aligned}
$$

Insert values:

$$
\begin{aligned}
H(\omega)
&= e^{-j2\omega}\Big(10 + 2(-4)\cos\omega + 2(-1)\cos 2\omega\Big)\\
&= e^{-j2\omega}\big(10 - 8\cos\omega - 2\cos 2\omega\big).
\end{aligned}
$$

Hence

$$
\boxed{
\lvert H(\omega)\rvert = 10 - 8\cos\omega - 2\cos 2\omega
}
$$

(the bracket is non-negative for $-\pi\le\omega\le\pi$; see solution sheet),

and pure **linear phase**

$$
\boxed{\angle H(\omega) = -2\omega}
$$

apart from the usual possible $\pi$-jumps if the magnitude crosses zero.

This is exactly what we expect from an **odd-length, real-coefficient, symmetric FIR**:  

- Linear phase with slope $-\frac{N-1}{2}=-2$.  
- Magnitude given by a sum of cosines.

> [!code]- MATLAB — 1-3 analytic vs `freqz` plots
> ```matlab
> % Problem 1-3: Analytic |H(w)| and angle H(w) vs freqz
> 
> W = linspace(-pi,pi,4001);
> mag_analytic = 10 - 8*cos(W) - 2*cos(2*W);
> phase_analytic = -2*W;          % linear phase
> 
> % freqz result centered around 0
> [H_omega, w_full] = freqz(h,1,2048,'whole');    % 0..2pi
> w_shift = w_full - pi;                          % shift to [-pi,pi]
> H_shift = fftshift(H_omega);
> 
> figure;
> subplot(2,1,1);
> plot(W, mag_analytic,'LineWidth',1.5); hold on;
> plot(w_shift, abs(H_shift),'--'); grid on;
> xlabel('\omega [rad/sample]');
> ylabel('|H(\omega)|');
> legend('Analytic','freqz','Location','best');
> title('E23: Problem 1-3 — Magnitude response');
> 
> subplot(2,1,2);
> plot(W, phase_analytic,'LineWidth',1.5); hold on;
> plot(w_shift, unwrap(angle(H_shift)),'--'); grid on;
> xlabel('\omega [rad/sample]');
> ylabel('\angle H(\omega) [rad]');
> legend('Analytic','freqz','Location','best');
> title('E23: Problem 1-3 — Phase response');
> 
> print('Images/DSP_Exam_E23_1_MagPhase','-dpng');
> ```

![[Images/DSP_Exam_E23_1_MagPhase.png]]

---

## 1-4) Second FIR filter in cascade

The exam states that the overall system is a **cascade** of two FIR filters:

- First filter: $H_1(z) = 1 - z^{-1}$  
- Second filter: $H_2(z)$ (unknown)

Total system:

$$
H(z) = H_1(z)H_2(z) = (1 - z^{-1}) H_2(z).
$$

From 1-2:

$$
H(z) = -1 - 4z^{-1} + 10z^{-2} - 4z^{-3} - z^{-4}.
$$

Therefore

$$
H_2(z) = \frac{H(z)}{1 - z^{-1}}.
$$

Carrying out the polynomial division gives

$$
\boxed{
H_2(z) = -1 - 5z^{-1} + 5z^{-2} + z^{-3}
}
$$

So the second FIR filter has impulse response

$$
h_2[n] = -\delta[n] - 5\delta[n-1] + 5\delta[n-2] + \delta[n-3].
$$

> [!code]- MATLAB — 1-4 compute $H_2(z)$ numerically
> ```matlab
> % Problem 1-4: Second filter H2(z) in cascade
> 
> H  = h;                 % overall FIR numerator coefficients
> H1 = [1 -1];            % H1(z) = 1 - z^-1
> 
> % Deconvolution: H(z) = H1(z) * H2(z)
> [H2_num, rem] = deconv(H, H1);
> 
> fprintf('1-4) H2(z) numerator coefficients:\n');
> disp(H2_num);           % should be [-1 -5 5 1]
> fprintf('Deconv remainder (should be near zero):\n');
> disp(rem);
> 
> % Pole-zero plot of H2(z)
> figure;
> zplane(H2_num,1);
> title('E23: Problem 1-4 — Pole-zero plot of H_2(z)');
> print('Images/DSP_Exam_E23_1_H2_PZ','-dpng');
> ```

![[Images/DSP_Exam_E23_1_H2_PZ.png]]

---

# Problem 2 — IIR High-Pass Chebyshev Type I via BLT

> Design a **digital high-pass IIR filter (Chebyshev Type I)** using the **Bilinear Transform** with  
> $\alpha = 2/T_s$, $F_s = 4000~\text{Hz}$.  
> Specs:
> - High-pass  
> - Digital passband edge: $f_p = 700/F_s$  
> - Digital stopband edge: $f_s = 400/F_s$  
> - Passband ripple: $A_p = 3\ \text{dB}$  
> - Stopband attenuation: $A_s = 30\ \text{dB}$

Workflow:

1. Design **analog Chebyshev Type I LP prototype**.  
2. Transform to analog **high-pass**.  
3. Use **BLT** to obtain digital $H_{HP}(z)$.  
4. Plot magnitude and check specs.

---

## 2-1) Chebyshev prototype: $\varepsilon$, analog edges, order $n$, prototype $H_{LP}(s)$

### (a) Ripple parameter $\varepsilon$

For a Chebyshev Type I filter with ripple $A_p$ in dB:

$$
\varepsilon^2 = 10^{A_p/10} - 1.
$$

With $A_p = 3$ dB:

$$
\varepsilon^2 \approx 10^{0.3}-1 \approx 0.995 \approx 1,\quad \varepsilon \approx 1.
$$

### (b) Prewarped analog edge frequencies

Digital edge frequencies in Hz:

$$
F_s = 4000,\quad
F_p = 700,\quad
F_s^{(\text{stop})} = 400.
$$

Digital angular frequency:

$$
\omega = 2\pi \frac{F}{F_s}.
$$

BLT warping (with $\alpha = 2/T_s = 2F_s$):

$$
\Omega = 2F_s \tan\!\left(\frac{\omega}{2}\right)
       = 2F_s \tan\!\left(\pi \frac{F}{F_s}\right).
$$

So

$$
\Omega_p = 2F_s \tan\!\left(\pi\frac{700}{4000}\right),\qquad
\Omega_s = 2F_s \tan\!\left(\pi\frac{400}{4000}\right).
$$

> [!code]- MATLAB — 2-1a: ε and prewarping
> ```matlab
> % Problem 2-1: Chebyshev Type I prototype
> 
> Fs   = 4000;
> Ts   = 1/Fs;
> Ap_dB = 3;
> As_dB = 30;
> 
> Fp = 700;                      % passband (Hz)
> Fs_stop = 400;                 % stopband (Hz)
> 
> eps2 = 10^(Ap_dB/10) - 1;
> eps  = sqrt(eps2);
> 
> prewarp = @(F) 2*Fs*tan(pi*F/Fs);
> Omegap = prewarp(Fp);
> Omegas = prewarp(Fs_stop);
> 
> fprintf('2-1) epsilon = %.4f\n', eps);
> fprintf('Omegap = %.2f rad/s, Omegas = %.2f rad/s\n', Omegap, Omegas);
> ```

### (c) Minimum prototype order

For Chebyshev Type I LP:

$$
A_s = 10\log_{10}\big(1+\varepsilon^2 T_n^2(\Omega_s/\Omega_p)\big).
$$

This gives the standard order formula (using $\lvert\Omega_s\rvert>\lvert\Omega_p\rvert$):

$$
n \ge
\frac{
\cosh^{-1}\sqrt{\frac{10^{A_s/10}-1}{10^{A_p/10}-1}}
}{
\cosh^{-1}\left(\frac{\Omega_s}{\Omega_p}\right)
}.
$$

Evaluating numerically gives $n \approx 3.3$, so we choose

$$
\boxed{n_\text{min} = 4}
$$

as in the official solution.

> [!code]- MATLAB — 2-1c: order estimation
> ```matlab
> % Chebyshev order (using cosh-1 form)
> 
> Gp = 10^(-Ap_dB/20);      % passband gain spec
> Gs = 10^(-As_dB/20);      % stopband gain spec
> 
> k1 = sqrt(1/Gs^2 - 1);
> k2 = sqrt(1/Gp^2 - 1);
> 
> n_cheb = acosh(k1/k2) / acosh(Omegas/Omegap);
> 
> fprintf('Chebyshev order estimate = %.3f -> n_min = %d\n', ...
>         n_cheb, ceil(n_cheb));
> ```

### (d) Prototype low-pass transfer function

From **Chebyshev Type I prototype table** (3 dB ripple, order $n=4$) in Appendix 2:

$$
H_{\text{proto}}(s) = 
\frac{0.1253}{s^4 + 0.5816 s^3 + 1.1691 s^2 + 0.4048 s + 0.1770}.
$$

> [!code]- MATLAB — 2-1d: prototype TF
> ```matlab
> % Chebyshev Type I LP prototype of order 4 (from appendix)
> 
> B_proto = 0.1253;
> A_proto = [1 0.5816 1.1691 0.4048 0.1770];
> 
> sys_proto = tf(B_proto, A_proto);
> disp('2-1) Chebyshev Type I LP prototype (n=4):');
> sys_proto
> ```

---

## 2-2) Analog high-pass filter $H_{HP}(s)$

We want a **high-pass** analog filter with passband edge $\Omega_p$.

The standard LP → HP transformation for prototypes is

$$
s \;\mapsto\; \frac{\Omega_p^2}{s}.
$$

Equivalently in MATLAB: `lp2hp`.

> [!code]- MATLAB — 2-2: analog HP via `lp2hp` and magnitude plot
> ```matlab
> % Problem 2-2: analog high-pass from LP prototype
> 
> [B_HP, A_HP] = lp2hp(B_proto, A_proto, Omegap);
> sys_HP = tf(B_HP, A_HP);
> disp('2-2) Analog HP Chebyshev filter H_HP(s):');
> sys_HP
> 
> % Analog magnitude in dB
> Omega = linspace(0, 2.5*Omegap, 4000);   % rad/s
> H_HP = freqs(B_HP, A_HP, Omega);
> 
> F_analog = Omega/(2*pi);                 % Hz
> Mag_HP_dB = 20*log10(abs(H_HP));
> 
> figure;
> plot(F_analog, Mag_HP_dB,'LineWidth',1.5); grid on;
> xlabel('Analog frequency F [Hz]');
> ylabel('|H_{HP}(j\Omega)| [dB]');
> title('E23: Problem 2-2 — Analog HP Chebyshev magnitude');
> xline(Fs_stop, '--r', 'F_s');
> xline(Fp,      '--g', 'F_p');
> 
> print('Images/DSP_Exam_E23_2_Analog_HP_Mag_dB','-dpng');
> ```

![[Images/DSP_Exam_E23_2_Analog_HP_Mag_dB.png]]

---

## 2-3) Digital high-pass filter $H_{HP}(z)$ via BLT

Using the Bilinear Transform

$$
s = \frac{2}{T_s}\frac{1-z^{-1}}{1+z^{-1}} = 2F_s \frac{1-z^{-1}}{1+z^{-1}},
$$

we map the analog $H_{HP}(s)$ to a digital IIR:

> [!code]- MATLAB — 2-3: BLT to get $H_{HP}(z)$
> ```matlab
> % Problem 2-3: Bilinear transform to digital HP IIR
> 
> [Bz_HP, Az_HP] = bilinear(B_HP, A_HP, Fs);
> 
> Ts = 1/Fs;
> sys_HP_z = tf(Bz_HP, Az_HP, Ts, 'Variable','z^-1');
> disp('2-3) Digital HP Chebyshev H_HP(z):');
> sys_HP_z
> ```

From the student solution we know the digital transfer function can be written as

$$
\boxed{
H_{HP}(z) =
\frac{
0.11 - 0.4401z^{-1} + 0.6601z^{-2} - 0.4401z^{-3} + 0.11 z^{-4}
}{
1 - 0.3269z^{-1} + 0.9044z^{-2} + 0.0742 z^{-3} + 0.3294 z^{-4}
}.
}
$$

---

## 2-4) Digital magnitude response and spec check

We now examine the **digital** magnitude in dB versus frequency $F$ in Hz:

> [!code]- MATLAB — 2-4: digital magnitude and attenuation at key edges
> ```matlab
> % Problem 2-4: Digital HP magnitude & specs
> 
> F = linspace(0, Fs/2, 4000);    % 0..Nyquist (Hz)
> [Hdig_HP, F_resp] = freqz(Bz_HP, Az_HP, F, Fs);
> Magdig_HP_dB = 20*log10(abs(Hdig_HP));
> 
> figure;
> plot(F_resp, Magdig_HP_dB,'LineWidth',1.5); grid on;
> xlabel('f [Hz]');
> ylabel('|H_{HP}(e^{j\omega})| [dB]');
> title('E23: Problem 2-4 — Digital HP Chebyshev magnitude');
> xline(Fs_stop,'--r','F_s = 400 Hz');
> xline(Fp,     '--g','F_p = 700 Hz');
> 
> print('Images/DSP_Exam_E23_2_Digital_HP_Mag_dB','-dpng');
> 
> % Attenuation at the spec edges
> F_edges = [Fs_stop, Fp];
> [H_edges, ~] = freqz(Bz_HP, Az_HP, F_edges, Fs);
> Att_edges_dB = 20*log10(abs(H_edges));
> 
> fprintf('Digital HP attenuation:\n');
> fprintf('  At 400 Hz (stopband): %.2f dB\n', Att_edges_dB(1));
> fprintf('  At 700 Hz (passband): %.2f dB\n', Att_edges_dB(2));
> ```

![[Images/DSP_Exam_E23_2_Digital_HP_Mag_dB.png]]

From the solution sheet:   

- At $400$ Hz: about $-37.3$ dB (better than $30$ dB spec).  
- At $700$ Hz: about $-3.0$ dB (meets the $3$ dB passband spec).

So the designed digital HP Chebyshev filter satisfies the requirements.

---

# Problem 3 — Sampling & IIR ROC / Inverse Filter

> Problem 3 first considers an **analog spectrum** $F_a(\Omega)$ and sampling with different angular sampling frequencies $\Omega_s$. Then it gives a **causal IIR filter** with poles and zeros and asks about ROC, stability, and the inverse filter.

---

## 3-1) Sampling criterion from spectral plots

The figure in the exam shows the analog spectrum $F_a(\Omega)$ band-limited to some $\Omega_{\max}$, and below it the replicated spectra $F_a(\Omega - k\Omega_s)$ for three choices of $\Omega_s$.   

For each of the given $\Omega_s\in\{200,400,150\}\,\text{rad/s}$, you must decide whether the replicas overlap (aliasing) or not.

**Nyquist criterion (angular):**

$$
\Omega_s \ge 2\Omega_{\max}.
$$

Looking at the provided solutions and plots, we see:

- For $\Omega_s = 200$: replicas overlap ⇒ sampling criterion **not satisfied**.  
- For $\Omega_s = 400$: just fits ⇒ criterion **satisfied (critical)**.  
- For $\Omega_s = 150$: strong overlap ⇒ **not satisfied**.

(Here $\Omega_{\max}$ is read from the original $F_a(\Omega)$ plot.)

No MATLAB is needed; this is purely geometric in the frequency domain.

---

## 3-2) New band-limited signal with different $\Omega_{\max}$

A second analog signal $g_a(t)$ has a **larger** bandwidth (larger $\Omega_{\max}$). You are asked which of the same sampling angular frequencies now satisfy Nyquist.  

Using the new $\Omega_{\max}$ given in the exam and again checking $\Omega_s \ge 2\Omega_{\max}$ you conclude, consistent with the solution sheet, that **only one** of the three $\Omega_s$ values fulfills the criterion (the one at or above $2\Omega_{\max}$).

---

## 3-3) IIR filter: ROC, stability and inverse

The exam then defines a **causal IIR filter** via a pole-zero plot (or system function) and asks:

1. Determine the **ROC** and whether the system is **BIBO stable**.  
2. Derive the **inverse system** $H^{-1}(z)$ and discuss its ROC/stability.

The concrete system is (from the solution sheet) a simple rational function with all poles strictly **inside** the unit circle, and the ROC selected as the **outer** region (since the system is causal).  

So:

- ROC: $\lvert z\rvert > r_\text{max}$ (outermost pole radius).  
- Since this ROC includes $\lvert z\rvert=1$, the system is **BIBO stable**.

The **inverse system** has transfer function

$$
H^{-1}(z) = \frac{1}{H(z)},
$$

which **swaps poles and zeros**. That is:

- Poles of the inverse $=$ zeros of $H(z)$.  
- Zeros of the inverse $=$ poles of $H(z)$.

At least one original zero lies **outside** the unit circle, so the inverse system would have a pole outside $\lvert z\rvert=1$. That means:

- You *cannot* choose an ROC for the inverse that includes the unit circle and still be causal → the **inverse is not simultaneously causal and BIBO stable**.

> [!code]- MATLAB — 3-3 generic ROC / pole-zero illustration
> ```matlab
> % Problem 3-3: Generic example with poles inside UC
> 
> % Example system H(z) with two complex-conjugate poles inside UC
> B_ex = [1 0];              % simple zero at z = 0 (example)
> A_ex = [1 -0.8 0.64];      % poles at 0.4±j*sqrt(0.64-0.16) etc
> 
> figure;
> zplane(B_ex, A_ex);
> title('E23: Problem 3-3 — Example pole-zero plot & ROC idea');
> print('Images/DSP_Exam_E23_3_PZ_ROC','-dpng');
> ```

![[Images/DSP_Exam_E23_3_PZ_ROC.png]]

The ROC for the **causal** example would be $\lvert z\rvert > \lvert p_{\max}\rvert$; since $\lvert p_{\max}\rvert<1$, the unit circle lies in the ROC → stable. For the inverse, the ROC would need to exclude the original zero outside the unit circle, leading to a non-causal / unstable configuration.

---

# Problem 4 — FIR High-Pass from Fourier Series + Spectrum

> Design a **linear-phase high-pass FIR filter** by truncating the Fourier series of the ideal HP response.  
> Then:
> - Implement the FIR filter with the found coefficients.  
> - Compute the spectrum of a noisy 2-tone signal $x[n]$.  
> - Find amplitudes before and after filtering at given frequencies.

---

## 4-1) High-pass FIR design via Fourier series

The exam gives sampling frequency $F_s$, desired **cutoff** $F_c = 240$ Hz, and a **desired transition sharpness** (difference between stopband and passband edges). Using the standard formula for a **truncated, delayed high-pass FIR** (see solution):

- Transition width:
  $$
  \Delta F_\text{sharpness} = \frac{F_{\text{stop}}-F_{\text{pass}}}{F_s}
  $$
- Estimated number of taps:
  $$
  N_{\text{taps}} \approx \frac{0.9}{\Delta F_\text{sharpness}}
  $$
- With exam values you obtain:
  $$
  N_{\text{taps}} = 15,\quad M=N_{\text{taps}}-1=14,\quad
  K=M/2=7.
  $$

The (truncated, delayed) high-pass impulse response is expressed from a **low-pass prototype** via spectral inversion and a time shift $K$. The solution provides the final set of coefficients $b_k$ (for $k=0,\dots,14$):

$$
\begin{aligned}
b[0] &= 0.038394,\quad
b[1] &= 0.052112,\quad
b[2] &= 0.037420,\\
b[3] &= -0.0099737,\quad
b[4] &= -0.081754,\quad
b[5] &= -0.15884,\\
b[6] &= -0.21790,\quad
b[7] &= 0.76000,\\
b[8] &= -0.21790,\quad
b[9] &= -0.15884,\\
b[10]&= -0.081754,\quad
b[11]&= -0.0099737,\\
b[12]&= 0.037420,\quad
b[13]&= 0.052112,\quad
b[14]&= 0.038394.
\end{aligned}
$$

Impulse response is symmetric → linear-phase.

> [!code]- MATLAB — 4-1 HP FIR coefficients and magnitude
> ```matlab
> % Problem 4-1: High-pass FIR design via Fourier coefficients
> 
> Fs = 2000;                  % (use exam value here if different)
> Fc = 240;                   % cutoff
> 
> b_hp = [ ...
>   0.038394  0.052112  0.037420  -0.0099737  -0.081754 ...
>  -0.15884  -0.21790   0.76000   -0.21790    -0.15884  ...
>  -0.081754 -0.0099737 0.037420  0.052112    0.038394 ];
> 
> a_hp = 1;
> 
> % Impulse response (not required, but illustrative)
> n = 0:length(b_hp)-1;
> figure;
> stem(n, b_hp,'filled'); grid on;
> xlabel('n'); ylabel('h_{HP}[n]');
> title('E23: Problem 4-1 — High-pass FIR impulse response');
> print('Images/DSP_Exam_E23_4_HP_Impulse','-dpng');
> 
> % Magnitude response
> [H_hp, F_hp] = freqz(b_hp, a_hp, 4096, Fs);
> Mag_hp_dB = 20*log10(abs(H_hp));
> 
> figure;
> plot(F_hp, Mag_hp_dB,'LineWidth',1.5); grid on;
> xlabel('f [Hz]');
> ylabel('|H_{HP}(e^{j\omega})| [dB]');
> title('E23: Problem 4-1 — High-pass FIR magnitude (dB)');
> xline(100,'--r','100 Hz');
> xline(350,'--g','350 Hz');
> 
> print('Images/DSP_Exam_E23_4_HP_FIR_Mag_dB','-dpng');
> ```

![[Images/DSP_Exam_E23_4_HP_Impulse.png]]  
![[Images/DSP_Exam_E23_4_HP_FIR_Mag_dB.png]]

From the solution: attenuation at $100$ Hz is about $-20.8$ dB; gain at $350$ Hz about $+0.67$ dB.   

---

## 4-2) Spectrum of the sampled 2-tone signal $x[n]$

Analog signal:

$$
x_a(t) = A_1\sin(2\pi F_1 t) + A_2\cos(2\pi F_2 t),
$$

with

$$
F_1 = 100~\text{Hz},\quad F_2 = 350~\text{Hz},\quad
A_1 = 6,\quad A_2 = 2.
$$

Sample with sampling frequency $F_s$ (from first part of problem) and $N$ samples.

Discrete signal:

$$
x[n] = x_a(nT_s).
$$

You are asked to:

1. Compute and plot $\lvert X[k]\rvert$ vs **physical frequency** $F = f\,F_s$.  
2. Read off magnitudes at $\pm 100$ Hz and $\pm 350$ Hz.

From the theoretical spectrum of sin/cos terms (or from FFT), we expect:

- Peaks at $\pm 100$ Hz with amplitude $\approx 3$.  
- Peaks at $\pm 350$ Hz with amplitude $\approx 1$.   

> [!code]- MATLAB — 4-2: spectrum of x[n]
> ```matlab
> % Problem 4-2: Spectrum of sampled 2-tone signal x[n]
> 
> Fs = 2000;           % or the exam's Fs value
> N  = 4096;           % use exam's N if specified
> Ts = 1/Fs;
> 
> n = 0:N-1;
> t = n*Ts;
> 
> F1 = 100;  A1 = 6;
> F2 = 350;  A2 = 2;
> 
> xa = A1*sin(2*pi*F1*t) + A2*cos(2*pi*F2*t);
> x  = xa;              % discrete-time samples
> 
> X = fft(x);
> Xs = fftshift(X)/N;
> 
> f = (-N/2:N/2-1)*(Fs/N);
> 
> figure;
> plot(f, abs(Xs),'LineWidth',1); grid on;
> xlabel('F [Hz]');
> ylabel('|X(F)| (scaled)');
> title('E23: Problem 4-2 — Spectrum of x[n]');
> xlim([-500 500]);
> 
> print('Images/DSP_Exam_E23_4_InputSpectrum','-dpng');
> 
> % Locate magnitudes near ±100 and ±350 Hz
> targetFreqs = [100 350];
> for F0 = targetFreqs
>     [~, idx_pos] = min(abs(f - F0));
>     [~, idx_neg] = min(abs(f + F0));
>     fprintf('Approx |X| at ±%d Hz: %.3f (pos), %.3f (neg)\n', ...
>             F0, abs(Xs(idx_pos)), abs(Xs(idx_neg)));
> end
> ```

![[Images/DSP_Exam_E23_4_InputSpectrum.png]]

The solution confirms:

- Magnitude at $\pm 100$ Hz ≈ $3$.  
- Magnitude at $\pm 350$ Hz ≈ $1$.   

---

## 4-3) Output amplitudes after filtering

Finally, we pass $x[n]$ through the designed high-pass FIR filter:

$$
y[n] = (h_{HP} * x)[n].
$$

We are asked to:

1. Determine the **attenuation in dB** at $\pm 100$ Hz and $\pm 350$ Hz from the filter magnitude.  
2. Use these to compute the **output amplitudes** at those frequencies.

From the solution:

- Filter attenuation:  
  $$
  A_{100} \approx -20.81\ \text{dB} \quad(\text{linear} \approx 0.0911),
  $$
  $$
  A_{350} \approx +0.673\ \text{dB} \quad(\text{linear} \approx 1.0806).
  $$   

So output amplitudes become:

$$
\begin{aligned}
\text{At }100~\text{Hz}:&\quad
A_{1,\text{out}} \approx 3 \cdot 0.0911 \approx 0.273,\\
\text{At }350~\text{Hz}:&\quad
A_{2,\text{out}} \approx 1 \cdot 1.0806 \approx 1.081.
\end{aligned}
$$

> [!code]- MATLAB — 4-3: filtering and output spectrum
> ```matlab
> % Problem 4-3: Filter x[n] and inspect spectrum
> 
> y = filter(b_hp, a_hp, x);
> 
> Y = fft(y);
> Ys = fftshift(Y)/N;
> 
> figure;
> plot(f, abs(Ys),'LineWidth',1); grid on;
> xlabel('F [Hz]');
> ylabel('|Y(F)| (scaled)');
> title('E23: Problem 4-3 — Spectrum after HP filtering');
> xlim([-500 500]);
> 
> print('Images/DSP_Exam_E23_4_OutputSpectrum','-dpng');
> 
> % Read amplitudes at ±100 and ±350 Hz
> for F0 = targetFreqs
>     [~, idx_pos] = min(abs(f - F0));
>     [~, idx_neg] = min(abs(f + F0));
>     fprintf('Approx |Y| at ±%d Hz: %.4f (pos), %.4f (neg)\n', ...
>             F0, abs(Ys(idx_pos)), abs(Ys(idx_neg)));
> end
> ```

![[Images/DSP_Exam_E23_4_OutputSpectrum.png]]

These numerical results line up with the analytical attenuation values from the magnitude response and the official solution.

---
