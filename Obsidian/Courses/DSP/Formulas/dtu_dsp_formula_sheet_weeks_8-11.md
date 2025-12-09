# DTU 62743 DSP Formula Sheet: Weeks 8-11 (Lars)
**Filter Structures & Design - Strict adherence to DTU course materials (E19-F25)**

---

## **Weeks 8-9 - Digital Filter Structures**

### **Overview**
Digital filters can be implemented in different structural forms. The choice affects:
- Memory requirements (number of delays)
- Numerical precision (quantization effects)
- Computational efficiency
- Hardware/software complexity

**Course schedule:**
- **Week 8** (Lars): Digital Filter Structures (Parts 1-2/3)
- **Week 9** (Lars): Digital Filter Structures (Part 3/3)

These weeks cover the fundamental realization structures tested heavily in exams [E21, E22, F25].

---

## **8.1 Basic Concepts**

**Transfer Function:**
$$H(z) = \frac{Y(z)}{X(z)} = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + a_2 z^{-2} + \cdots + a_N z^{-N}}$$

**Difference Equation:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**Key distinction:**
- **FIR (Finite Impulse Response):** No feedback ($a_k = 0$ for all $k > 0$)
- **IIR (Infinite Impulse Response):** Has feedback ($a_k \neq 0$ for some $k > 0$)

---

## **8.2 Direct Form I** [E22, F25, E21]

### **9.1 Direct Form I** [E22, F25]

**Block diagram:**
```
x[n] → [FIR Section] → + → y[n]
              ↓         ↑
          [Delay]   [IIR Feedback]
```

**Structure:**
- **Two separate delay lines**
- FIR (feedforward) section: $\sum b_k x[n-k]$
- IIR (feedback) section: $-\sum a_k y[n-k]$

**Characteristics:**
- Total delays: $M + N$ (where $M$ = numerator order, $N$ = denominator order)
- Easy to implement from difference equation
- More memory usage than Direct Form II

**Transfer function:**
$$H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

**Difference equation:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**Example from E22 exam:**
- Filter with $M=3, N=3$
- Requires 6 delay elements total
- FIR path: $b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] + b_3 x[n-3]$
- IIR path: $-a_1 y[n-1] - a_2 y[n-2] - a_3 y[n-3]$

### **8.3 Extracting Transfer Function from Block Diagram** [CRITICAL - E22, F25, E21]

**This is heavily tested! You MUST know how to:**

**Step 1: Identify the structure**
- Look for feedback loops → IIR (Direct Form I or II)
- No feedback → FIR
- Count delay blocks

**Step 2: Read coefficients from diagram**
- Multiplier blocks (triangles/gains) → filter coefficients
- Feedforward path (x[n] to output) → $b_k$ coefficients
- Feedback path (y[n] back to input) → $-a_k$ coefficients
  - **IMPORTANT:** Signs in diagram are usually negated!

**Step 3: Write transfer function**
$$H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

**Example from E22 (Filter 3):**
```
Given diagram shows:
- Feedforward: 0.7772, -2.3317, 2.3317, -0.7772
- Feedback: 2.4986, -2.1153, 0.6041
```

**Extract coefficients:**
- $b_0 = 0.7772$, $b_1 = -2.3317$, $b_2 = 2.3317$, $b_3 = -0.7772$
- $a_1 = -2.4986$, $a_2 = 2.1153$, $a_3 = -0.6041$ (note sign flip!)

**Transfer function:**
$$H(z) = \frac{0.7772 - 2.3317z^{-1} + 2.3317z^{-2} - 0.7772z^{-3}}{1 - 2.4986z^{-1} + 2.1153z^{-2} - 0.6041z^{-3}}$$

### **8.4 Direct Form II (Canonical)** [E22, F25]

**Block diagram:**
```
x[n] → [IIR Section] → w[n] → [FIR Section] → y[n]
```

**Structure:**
- **Single shared delay line** (canonical form)
- IIR section processes first: $w[n] = x[n] - \sum a_k w[n-k]$
- FIR section processes second: $y[n] = \sum b_k w[n-k]$

**Characteristics:**
- Total delays: $\max(M, N)$ (minimum possible)
- More memory-efficient than Direct Form I
- Standard in MATLAB `filter()` function
- Also called "Direct Form II Transposed" when reversed

**State variable:** $w[n]$ is the intermediate signal

**Example from E22:**
- Same $M=3, N=3$ filter now requires only 3 delays
- Memory saving: 50% reduction compared to Direct Form I

### **8.4 Direct Form II (Canonical)** [E22, F25]

**Block diagram:**
```
x[n] → [IIR Section] → w[n] → [FIR Section] → y[n]
```

**Structure:**
- **Single shared delay line** (canonical form)
- IIR section processes first: $w[n] = x[n] - \sum a_k w[n-k]$
- FIR section processes second: $y[n] = \sum b_k w[n-k]$

**Characteristics:**
- Total delays: $\max(M, N)$ (minimum possible)
- More memory-efficient than Direct Form I
- Standard in MATLAB `filter()` function
- Also called "Direct Form II Transposed" when signal flow reversed

**State variable:** $w[n]$ is the intermediate signal

**How to identify Direct Form II:**
- Look for **intermediate node $w[n]$** (not visible at output)
- Feedback connects to **same delay line** as feedforward
- **Single delay chain** shared by both paths

**Example from E22:**
- Same $M=3, N=3$ filter now requires only 3 delays
- Memory saving: 50% reduction compared to Direct Form I
- Delays store $w[n-1], w[n-2], w[n-3]$

### **8.5 Identifying Filter Structure from Diagram** [EXAM SKILL]

**Quick identification checklist:**

| Feature | Direct Form I | Direct Form II |
|---------|---------------|----------------|
| Delay lines | **Two separate** | **One shared** |
| Total delays | $M + N$ | $\max(M,N)$ |
| Intermediate signal | None (direct) | $w[n]$ visible |
| Signal flow | FIR then IIR sum | IIR then FIR |
| Memory | Higher | Lower (canonical) |

**Common exam question:** "Which digital filter form is used?" [E22, F25]

**Answer strategy:**
1. Count independent delay chains
2. Check for intermediate node
3. Count total delays
4. If 2 chains → Direct Form I
5. If 1 chain + intermediate → Direct Form II

### **8.6 CRITICAL: Sign Convention in Diagrams** [AVOID THIS MISTAKE!]

**⚠️ The #1 mistake students make: Getting feedback signs wrong!**

**Standard form of transfer function:**
$$H(z) = \frac{b_0 + b_1z^{-1} + \cdots}{1 + a_1z^{-1} + a_2z^{-2} + \cdots}$$

**Standard difference equation:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**KEY POINT:** Notice the **negative sign** in front of the $a_k$ sum!

**When reading from diagrams:**
- **Feedforward coefficients (FIR path):** Use values directly as $b_k$
- **Feedback coefficients (IIR path):** Sign in diagram is usually **NEGATED**!

**Example from E22:**
```
Diagram shows feedback gain: +2.4986 (from y[n-1] back to summing junction)
This means: a₁ = -2.4986 in the transfer function!

Why? Because the difference equation has -a₁y[n-1]
So if diagram shows +2.4986, then a₁ must be -2.4986
```

**Rule of thumb:**
1. If feedback arrow shows $+k$ → coefficient is $-k$ in $H(z)$
2. If feedback arrow shows $-k$ → coefficient is $+k$ in $H(z)$
3. **Or:** Just write the difference equation directly from diagram, THEN convert to $H(z)$

**Safe method (always works):**
1. Write $y[n] = \ldots$ directly from diagram (use signs as shown)
2. Take Z-transform: $Y(z) = \ldots$
3. Solve for $H(z) = Y(z)/X(z)$
4. Rearrange to standard form

### **9.6 Cascade Form** [E21, E23]

**Structure:**
$$H(z) = G \prod_{k=1}^{K} H_k(z)$$

where each $H_k(z)$ is typically a **second-order section (SOS)** or **biquad**:
$$H_k(z) = \frac{b_{k,0} + b_{k,1} z^{-1} + b_{k,2} z^{-2}}{1 + a_{k,1} z^{-1} + a_{k,2} z^{-2}}$$

**How to derive:**
1. Factor numerator and denominator of $H(z)$
2. Find poles and zeros (using `roots()` in MATLAB)
3. Pair complex conjugate poles and zeros
4. Group into second-order sections
5. Order sections (usually most selective first)

**Advantages:**
- **Better numerical precision** (less quantization error)
- **Easier to control individual resonances**
- Used in professional audio/communications DSP

**MATLAB:**
```matlab
[z, p, k] = tf2zpk(b, a);        % Get zeros, poles, gain
[sos, g] = zp2sos(z, p, k);      % Convert to SOS matrix
```

**SOS Matrix format:**
```
sos = [b01 b11 b21  1 a11 a21
       b02 b12 b22  1 a12 a22
       ...
       b0K b1K b2K  1 a1K a2K]
```

**Example from E21:**
- 6th-order filter → 3 second-order sections
- Each section handles 2 poles and 2 zeros
- Overall gain distributed across sections or applied once

### **9.7 Parallel Form**

**Structure:**
$$H(z) = C + \sum_{k=1}^{K} H_k(z)$$

**Derived via partial fraction expansion:**
1. Compute $H(z)$ or $\frac{H(z)}{z}$
2. Apply partial fractions to get sum of simple terms
3. Each term becomes a parallel branch
4. Combine outputs

**For second-order sections:**
$$H_k(z) = \frac{r_k}{1 - p_k z^{-1}} + \frac{r_k^*}{1 - p_k^* z^{-1}} = \frac{A_k + B_k z^{-1}}{1 + a_{k,1} z^{-1} + a_{k,2} z^{-2}}$$

**Advantages:**
- **Parallel processing possible** (DSP implementation)
- **No error accumulation** between sections

**Disadvantages:**
- Less common than cascade
- Coefficient sensitivity can be higher

**MATLAB:**
```matlab
[r, p, k] = residue(b, a);       % Partial fraction expansion
```

---

## **Week 10 - IIR Filter Design (Bilinear Transform)**

### **10.1 Bilinear Transform (BLT)** [E23, F24, F21]

**Core transformation:**
$$s = \frac{2}{T_s} \cdot \frac{z-1}{z+1}$$

**Or in terms of $z$:**
$$z = \frac{1 + \frac{T_s}{2}s}{1 - \frac{T_s}{2}s}$$

**Where:**
- $T_s$ = sampling period (seconds)
- $s$ = analog Laplace variable
- $z$ = digital z-transform variable

### **10.2 Frequency Prewarping** [CRITICAL - E23, F24, F21]

**The Problem:**
BLT introduces **frequency warping** (nonlinear frequency mapping)

**The Solution:**
**ALWAYS prewarp critical frequencies BEFORE designing the analog filter**

**Prewarping formula:**
$$\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right)$$

**Where:**
- $\Omega$ = analog angular frequency (rad/s)
- $\omega$ = digital angular frequency (rad/sample)
- $\omega = 2\pi \frac{F}{F_s}$ (convert Hz to rad/sample first)

**Convert back to Hz:**
$$F_{\text{analog}} = \frac{\Omega}{2\pi}$$

**DTU 6-Step IIR Design Workflow:**
1. **Specify digital requirements:** $F_s, f_p, f_s, A_p, A_s$
2. **Convert to digital angular frequencies:** $\omega_p = 2\pi f_p/F_s$, $\omega_s = 2\pi f_s/F_s$
3. **Prewarp to analog domain:** $\Omega_p = \frac{2}{T_s}\tan(\omega_p/2)$, $\Omega_s = \frac{2}{T_s}\tan(\omega_s/2)$
4. **Design analog prototype** (Butterworth/Chebyshev)
5. **Apply frequency transformation** (LP→HP, LP→BP if needed)
6. **Apply BLT:** substitute $s = \frac{2}{T_s}\frac{z-1}{z+1}$
7. **Extract digital coefficients** and difference equation

### **10.3 Butterworth Filter Design** [E23, F21]

**Characteristics:**
- **Maximally flat** passband (no ripples)
- **Smooth monotonic** rolloff
- $|H(j\Omega_p)| = \frac{1}{\sqrt{2}} = 0.7071$ (−3 dB at cutoff)

**Analog lowpass prototype:**
$$|H_a(j\Omega)|^2 = \frac{1}{1 + \left(\frac{\Omega}{\Omega_c}\right)^{2n}}$$

**Order calculation:**
$$n \geq \frac{\log_{10}\left[\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right]}{2\log_{10}(\Omega_s/\Omega_p)}$$

**Or in dB:**
$$n \geq \frac{A_s[\text{dB}] - A_p[\text{dB}]}{20\log_{10}(\Omega_s/\Omega_p)}$$

**Where:**
- $A_p$ = passband attenuation (dB)
- $A_s$ = stopband attenuation (dB)
- $\Omega_p$ = passband edge (rad/s)
- $\Omega_s$ = stopband edge (rad/s)

**MATLAB:**
```matlab
% Step 1-3: Digital specs → Prewarp
Ts = 1/Fs;
wp = 2*pi*fp/Fs;                    % Digital passband (rad/sample)
Omega_p = (2/Ts)*tan(wp/2);         % Analog passband (rad/s)

% Step 4: Butterworth order and cutoff
[n, Wn] = buttord(Omega_p, Omega_s, Ap, As, 's');

% Design analog prototype
[b_analog, a_analog] = butter(n, Wn, 's');

% Step 6: Apply BLT
[b_digital, a_digital] = bilinear(b_analog, a_analog, Fs);
```

**Transfer function form:**
$$H_a(s) = \frac{K}{\prod_{k=1}^{n}(s - p_k)}$$

**Pole locations (for normalized $\Omega_c = 1$):**
$$p_k = e^{j\pi\frac{2k+n-1}{2n}}, \quad k = 1, 2, \ldots, n$$

All poles on unit circle in $s$-plane, in left half

### **10.4 Chebyshev Type I Filter** [E23]

**Characteristics:**
- **Equiripple in passband** (controlled ripple)
- **Sharper rolloff** than Butterworth for same order
- **Monotonic in stopband**

**Ripple parameter:**
$$\epsilon = \sqrt{10^{A_p/10} - 1}$$

**Order calculation:**
$$n \geq \frac{\text{arccosh}\left(\sqrt{\frac{10^{A_s/10}-1}{10^{A_p/10}-1}}\right)}{\text{arccosh}(\Omega_s/\Omega_p)}$$

**Advantages over Butterworth:**
- **Lower order** for same specifications
- **Steeper transition band**

**Trade-off:**
- Passband ripples (usually ≤ 1 dB acceptable)

**MATLAB:**
```matlab
% Chebyshev Type I design
[n, Wn] = cheb1ord(Omega_p, Omega_s, Ap, As, 's');
[b_analog, a_analog] = cheby1(n, Ap, Wn, 's');
[b_digital, a_digital] = bilinear(b_analog, a_analog, Fs);
```

### **10.5 Frequency Transformations** [E23, Uge 10]

All start from **analog lowpass prototype** with cutoff $\Omega_p = 1$ rad/s

#### **Lowpass → Highpass**
$$s \rightarrow \frac{\Omega_p}{s}$$

**Effect:**
- Zeros at $s=0$ → zeros at $s=\infty$
- Poles at $s=p_k$ → poles at $s=\Omega_p/p_k$
- Passband: $\Omega \geq \Omega_p$

**MATLAB:**
```matlab
[b_HP, a_HP] = lp2hp(b_LP, a_LP, Omega_p);
```

#### **Lowpass → Bandpass**
$$s \rightarrow \frac{s^2 + \Omega_L \Omega_H}{s(\Omega_H - \Omega_L)}$$

**Where:**
- $\Omega_L$ = lower passband edge
- $\Omega_H$ = upper passband edge
- $B = \Omega_H - \Omega_L$ = bandwidth
- $\Omega_0 = \sqrt{\Omega_L \Omega_H}$ = center frequency

**Effect:**
- Order doubles: $n \rightarrow 2n$
- Each pole/zero splits into complex conjugate pair

**MATLAB:**
```matlab
[b_BP, a_BP] = lp2bp(b_LP, a_LP, Omega_0, B);
```

#### **Lowpass → Bandstop**
$$s \rightarrow \frac{s(\Omega_H - \Omega_L)}{s^2 + \Omega_L \Omega_H}$$

**MATLAB:**
```matlab
[b_BS, a_BS] = lp2bs(b_LP, a_LP, Omega_0, B);
```

### **10.6 Complete Design Example** [Week 10 Tuesday]

**Given:**
- Lowpass IIR filter
- $F_s = 1000$ Hz → $T_s = 0.001$ s
- Passband: $f_p = 147.58$ Hz
- Stopband: $f_s = 200$ Hz
- $A_p = 3$ dB
- $A_s = 30$ dB

**Solution:**

**Step 1: Digital frequencies**
$$\omega_p = 2\pi \frac{147.58}{1000} = 0.9273 \text{ rad/sample}$$
$$\omega_s = 2\pi \frac{200}{1000} = 1.2566 \text{ rad/sample}$$

**Step 2: Prewarp**
$$\Omega_p = \frac{2}{0.001}\tan(0.9273/2) = 999.97 \text{ rad/s}$$
$$\Omega_s = \frac{2}{0.001}\tan(1.2566/2) = 1414.2 \text{ rad/s}$$

**Step 3: Butterworth order**
$$n \geq \frac{30 - 3}{20\log_{10}(1414.2/999.97)} = \frac{27}{3.01} = 8.97 \rightarrow n = 9$$

**Step 4: Design analog filter**
$$H_a(s) = \frac{\Omega_p^n}{\prod_{k=1}^{n}(s - p_k)}$$

**Step 5: Apply BLT**
$$s = \frac{2}{T_s}\frac{z-1}{z+1} = 2000\frac{z-1}{z+1}$$

**Step 6: Extract coefficients**
$$H_d(z) = \frac{b_0 + b_1 z^{-1} + \cdots}{1 + a_1 z^{-1} + \cdots}$$

---

## **Week 11 - FIR Filter Design**

### **11.1 Ideal Filter Impulse Responses** [Uge 11, E19, E20]

**Ideal Lowpass:**
$$h_{\text{LP,ideal}}[n] = \begin{cases}
\dfrac{\sin(\omega_c n)}{\pi n}, & n \neq 0 \\
\dfrac{\omega_c}{\pi}, & n = 0
\end{cases}$$

**Ideal Highpass (spectral inversion):**
$$h_{\text{HP,ideal}}[n] = \delta[n] - h_{\text{LP,ideal}}[n]$$

Specifically:
$$h_{\text{HP,ideal}}[n] = \begin{cases}
-\dfrac{\sin(\omega_c n)}{\pi n}, & n \neq 0 \\
1 - \dfrac{\omega_c}{\pi}, & n = 0
\end{cases}$$

**Ideal Bandpass:**
$$h_{\text{BP,ideal}}[n] = \begin{cases}
\dfrac{\sin(\omega_H n) - \sin(\omega_L n)}{\pi n}, & n \neq 0 \\
\dfrac{\omega_H - \omega_L}{\pi}, & n = 0
\end{cases}$$

**Ideal Bandstop:**
$$h_{\text{BS,ideal}}[n] = \delta[n] - h_{\text{BP,ideal}}[n]$$

### **11.2 FIR Design Process** [Week 11]

**Step 1: Frequency specs**
$$\omega_c = 2\pi \frac{F_c}{F_s}$$

**Step 2: Compute ideal impulse response**
Use formulas above (infinite length, non-causal)

**Step 3: Choose filter length**
$$N_{\text{taps}} = 2K + 1 \text{ (odd number)}$$

**Step 4: Truncate symmetrically**
Keep samples: $n = -K, -K+1, \ldots, 0, \ldots, K-1, K$

**Step 5: Make causal**
Shift right by $K$ samples:
$$b[n] = h_{\text{ideal}}[n - K], \quad n = 0, 1, \ldots, M$$

where $M = N_{\text{taps}} - 1 = 2K$

**Result:**
- **Symmetric coefficients:** $b[n] = b[M-n]$
- **Linear phase:** $\angle H(e^{j\omega}) = -\omega K$
- **Group delay:** $\tau_g = K$ samples (constant)

### **11.3 Window Functions** [Uge 11, E19, E20]

**Purpose:**
Reduce **Gibbs oscillations** (ripples) caused by truncation

**Rectangular window (no window):**
$$w[n] = 1, \quad n = 0, 1, \ldots, M$$

- **Narrowest main lobe** (sharpest transition)
- **Highest sidelobes** (~−13 dB)
- **~9% overshoot** (Gibbs phenomenon)

**Hamming window:**
$$w[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{M}\right)$$

- **Wider main lobe**
- **Lower sidelobes** (~−43 dB)
- **Reduced overshoot**
- Standard textbook window, appears in Mock Exam solutions

**Hanning window:**
$$w[n] = 0.5 - 0.5\cos\left(\frac{2\pi n}{M}\right)$$

- **Sidelobes:** ~−32 dB
- **Smoother than Hamming**
- **⚠️ THE DTU FAVORITE - MOST COMMON in exams:** Used in **E20 Q4, E22 Q4, F24** [AUDIT CONFIRMED]
- **If unsure which window, check for Hanning first!**

**Blackman window:**
$$w[n] = 0.42 - 0.5\cos\left(\frac{2\pi n}{M}\right) + 0.08\cos\left(\frac{4\pi n}{M}\right)$$

- **Widest main lobe**
- **Lowest sidelobes** (~−58 dB)
- **Best stopband attenuation**
- Used in **E19 Q2** [AUDIT CONFIRMED]

**🚨 CRITICAL EXAM WARNING 🚨**
**DO NOT assume which window to use!** Different exams specify different windows:
- **E20 Q4, E22 Q4, F24:** Hanning ($0.5 - 0.5\cos$) ← **MOST FREQUENT!**
- **E19 Q2:** Blackman (3-term formula)
- **Mock Exam/Textbook:** Hamming ($0.54 - 0.46\cos$) - Know it but don't default to it!

**Always check the exam question carefully!** Using the wrong window coefficients will give incorrect filter coefficients and fail the question.

**Quick coefficient check:**
- Hanning starts with **0.5** ← **Check for this FIRST in recent exams!**
- Hamming starts with **0.54** (textbook standard)
- Blackman has **three terms** (0.42, 0.5, 0.08)

**Exam pattern observed:** Recent official exams (E20, E22, F24) all use **Hanning**!

**Trade-off summary:**
| Window      | Main Lobe Width | Stopband Atten. | Transition Width |
|-------------|-----------------|-----------------|------------------|
| Rectangular | Narrowest       | ~13 dB (worst)  | Sharpest         |
| Hanning     | Medium          | ~32 dB          | Medium           |
| Hamming     | Medium          | ~43 dB          | Medium           |
| Blackman    | Widest          | ~58 dB (best)   | Widest           |

**Application:**
$$b_{\text{windowed}}[n] = b[n] \cdot w[n]$$

**MATLAB:**
```matlab
% Manual windowing
M = Ntaps - 1;
w_hamming = 0.54 - 0.46*cos(2*pi*(0:M)/M);
b_windowed = b .* w_hamming;

% Or use built-in
w_hamming = hamming(Ntaps);
b_windowed = b .* w_hamming';
```

### **11.4 Gibbs Phenomenon**

**Cause:**
Abrupt truncation of infinite ideal impulse response

**Effect:**
- **~9% overshoot** near discontinuities (rectangular window)
- **Ringing** in frequency response
- **Cannot be eliminated**, only reduced

**Solutions:**
1. Use window functions (Hamming, Blackman)
2. Increase filter order (more taps)
3. Accept trade-off between transition width and ripple

### **11.5 Linear Phase FIR**

**Symmetric coefficients:**
$$b[n] = b[M-n]$$

**Phase response:**
$$\angle H(e^{j\omega}) = -\omega K$$

where $K = M/2$ (perfect linear phase)

**Magnitude response factorization:**
$$H(e^{j\omega}) = e^{-j\omega K} \cdot A(\omega)$$

where $A(\omega)$ is real-valued amplitude function

**Advantages:**
- **No phase distortion**
- **Constant group delay:** $\tau_g = K$ samples
- **Preserve waveform shape** (important for audio, communications)

### **11.6 MATLAB FIR Design**

**Manual method:**
```matlab
% Specs
Fc = 800;                      % Cutoff frequency (Hz)
Fs = 8000;                     % Sampling frequency (Hz)
Ntaps = 23;                    % Number of taps (odd)

% Normalized cutoff
wc = 2*pi*Fc/Fs;               % rad/sample

% Design
M = Ntaps - 1;
K = M/2;
n_ideal = -K:K;                % Symmetric around 0

% Ideal lowpass impulse response
h_ideal = sin(wc*n_ideal)./(pi*n_ideal);
h_ideal(K+1) = wc/pi;          % Handle n=0 case

% Make causal
b = h_ideal;                   % Already centered at n=K

% Apply Hamming window
w = hamming(Ntaps);
b_windowed = b .* w';

% Frequency response
[H, f] = freqz(b_windowed, 1, 2048, Fs);
```

**Built-in method:**
```matlab
% fir1 designs FIR filters using windowing
Wn = Fc/(Fs/2);                % Normalized frequency (0 to 1)
b = fir1(M, Wn, 'low', hamming(Ntaps));

% For highpass
b = fir1(M, Wn, 'high', hamming(Ntaps));

% For bandpass
b = fir1(M, [Fc1 Fc2]/(Fs/2), 'bandpass', hamming(Ntaps));
```

### **11.7 FIR vs IIR Comparison**

| Feature           | FIR                          | IIR                          |
|-------------------|------------------------------|------------------------------|
| Phase             | Exactly linear (if symmetric)| Nonlinear                    |
| Stability         | Always stable                | Can be unstable              |
| Order             | Higher for sharp filters     | Lower order                  |
| Delay             | High (K samples)             | Lower                        |
| Computation       | More multiplies              | Fewer multiplies             |
| Design            | Straightforward              | More complex                 |
| Applications      | Audio, communications        | Control, real-time           |

---

## **Exam Strategy for Weeks 8-11**

### **Most Common Question Types**

**Weeks 8-9 (Filter Structures):**
1. **Identify structure from block diagram** [E22, F25] ← MOST COMMON!
2. **Extract transfer function $H(z)$ from diagram** [E22, F25, E21]
3. **Write difference equation from structure** [E21]
4. **Count delay elements** (Direct Form I: $M+N$, Direct Form II: $\max(M,N)$)
5. **Convert H(z) to cascade SOS format** [E21]
6. **Draw filter structure from difference equation**
7. **Identify FIR vs IIR** from diagram (look for feedback!)

**Week 10 (IIR Design):**
1. **ALWAYS PREWARP FIRST** - most common mistake is skipping this! [E23, F24]
2. Calculate Butterworth/Chebyshev order
3. Apply frequency transformations (LP→HP, LP→BP)
4. Extract coefficients after BLT
5. Verify specs with freqz plots

**Week 11 (FIR Design):**
1. Compute ideal impulse response [E19, E20]
2. Make causal by shifting
3. **CHECK WHICH WINDOW THE EXAM SPECIFIES!** (Hanning≠Hamming≠Blackman)
   - E20, E22: Hanning
   - E23, F24: Hamming  
   - E19: Blackman
4. Calculate linear phase and group delay
5. Compare window trade-offs

**🚨 WINDOW QUICK REFERENCE CARD 🚨**
**Memorize these for the exam - they test this every year!**

| Window       | Formula                                         | First Coefficient  | Exam Appearances                   |
| ------------ | ----------------------------------------------- | ------------------ | ---------------------------------- |
| **Hanning**  | $0.5 - 0.5\cos(2\pi n/M)$                       | **0.5**            | **E20, E22, F24** ← Most Frequent! |
| **Blackman** | $0.42 - 0.5\cos(2\pi n/M) + 0.08\cos(4\pi n/M)$ | **0.42** (3 terms) | E19                                |
| **Hamming**  | $0.54 - 0.46\cos(2\pi n/M)$                     | **0.54**           | Mock Exam / Textbook               |

**Memory trick:** 
- **Hanning = Half** (0.5) ← **DEFAULT CHECK for recent exams!**
- **Hamming = Half + a bit** (0.54) ← Textbook standard
- **Blackman = Three terms** (0.42 + two more)

**Exam Strategy:** Recent official exams (E20, E22, F24) ALL use Hanning. Always verify in exam text!

### **Critical Formulas to Memorize**

1. **BLT and Prewarping:**
   $$\Omega = \frac{2}{T_s}\tan\left(\frac{\omega}{2}\right)$$

2. **Ideal Lowpass:**
   $$h_{\text{LP}}[n] = \frac{\sin(\omega_c n)}{\pi n}, \quad h_{\text{LP}}[0] = \frac{\omega_c}{\pi}$$

3. **Butterworth Order:**
   $$n \geq \frac{A_s[\text{dB}] - A_p[\text{dB}]}{20\log_{10}(\Omega_s/\Omega_p)}$$

4. **LP→HP Transformation:**
   $$s \rightarrow \frac{\Omega_p}{s}$$

5. **Windows (CHECK EXAM!):**
   - **Hanning (E20, E22, F24):** $w[n] = 0.5 - 0.5\cos(2\pi n/M)$ ← **Most frequent!**
   - **Blackman (E19):** $w[n] = 0.42 - 0.5\cos(2\pi n/M) + 0.08\cos(4\pi n/M)$
   - **Hamming (Mock/Textbook):** $w[n] = 0.54 - 0.46\cos(2\pi n/M)$

### **Common Mistakes to Avoid**

1. **Forgetting to prewarp** before analog filter design (CRITICAL for Week 10!)
2. **Getting feedback signs wrong** when extracting H(z) from diagrams (Week 8!)
3. **Using wrong window formula** - CHECK THE EXAM CAREFULLY!
   - Hanning (0.5 - 0.5cos): **E20 Q4, E22 Q4, F24** ← Most frequent!
   - Blackman (3-term): E19 Q2
   - Hamming (0.54 - 0.46cos): Mock Exam / Textbook
   - **Mixing these up = wrong filter = zero points!**
4. **Not making FIR causal** (forgetting to shift by K)
5. **Wrong delay count** in Direct Form I (should be M+N) vs Direct Form II (max(M,N))
6. **Confusing analog $\Omega$ (rad/s) with digital $\omega$ (rad/sample)**
7. **Not identifying intermediate node w[n]** in Direct Form II

### **MATLAB Quick Reference**

```matlab
% IIR Design (Week 10)
Omega_p = (2/Ts)*tan(wp/2);              % PREWARP FIRST!
[n, Wn] = buttord(Omega_p, Omega_s, Ap, As, 's');
[b_a, a_a] = butter(n, Wn, 's');
[b, a] = bilinear(b_a, a_a, Fs);

% LP→HP transformation
[b_HP, a_HP] = lp2hp(b_LP, a_LP, Omega_p);

% FIR Design (Week 11)
h_ideal = sin(wc*n)./(pi*n);             % Ideal impulse
w = hamming(Ntaps);                      % Window
b = h_ideal .* w';                       % Apply window

% Or use fir1
b = fir1(M, Wn, 'low', hamming(Ntaps));

% Filter Structures (Week 9)
[z, p, k] = tf2zpk(b, a);                % Poles and zeros
[sos, g] = zp2sos(z, p, k);              % Cascade (SOS)
[r, p, k] = residue(b, a);               % Parallel
```

---

