# DTU 62743 DSP Formula Sheet: Weeks 1-4 (Iver)

**Digital Signal Processing | Technical University of Denmark**  
**Strict adherence to DTU course materials (E19-F25 exam solutions)**

---

## 📋 Table of Contents

### Fundamental Reference

- [[#🌊 Fundamental: DSP Frequency Representations]]

### Week 1: Introduction & MATLAB

- [[#1.1 Discrete-Time Signals]]
- [[#1.2 Basic Signal Types]]
- [[#1.3 MATLAB Essentials]]
- [[#1.4 Signal Energy and Power]]

### Week 2: LTI Systems (Time Domain)

- [[#2.1 Linear Time-Invariant (LTI) Systems]]
- [[#2.2 Convolution]]
- [[#2.3 Impulse Response]]
- [[#2.4 Step Response]]
- [[#2.5 System Properties]]

### Week 3: Frequency Domain

- [[#3.1 DTFT (Discrete-Time Fourier Transform)]]
- [[#3.2 DTFT Properties]]
- [[#3.3 Frequency Response]]
- [[#3.4 Ideal Filters]]

### Week 4: Z-Transform

- [[#4.1 Z-Transform Definition]]
- [[#4.2 Common Z-Transform Pairs]]
- [[#4.3 Z-Transform Properties]]
- [[#4.4 Inverse Z-Transform Methods]]
- [[#4.5 Transfer Function H(z)]]
- [[#4.6 Poles, Zeros, and Stability]]
- [[#4.7 Combined Systems and Pole-Zero Cancellation]]

---

## 🌊 Fundamental: DSP Frequency Representations

**The Four Ways to Represent Frequency in DSP**

### Frequency Conversion Diagram

```
                    Adding "angular" multiply by 2π
                              ↓
        F                                    Ω = 2πF
    "Frequency"                      "Angular frequency"
    [Hz] = [1/s]  ←─────────────→    [rad/s] = [1/s]
        ↓                                    ↓
  To "normalize"                      Multiply by 2π/Fs
   divide by Fs                              ↓
        ↓                                    ↓
     f = F/Fs                           ω = 2πF/Fs
  "Normalized frequency"      "Normalized angular frequency"
    [unit-less]                      [rad] = [unit-less]
```

### The Four Frequency Types

|Type|Symbol|Formula|Units|Range|Used For|
|---|---|---|---|---|---|
|**Physical**|$F$|Given|Hz (1/s)|$0$ to $\infty$|Real-world specifications|
|**Angular**|$\Omega$|$2\pi F$|rad/s|$0$ to $\infty$|Analog filters (s-domain)|
|**Normalized**|$f$|$F/F_s$|dimensionless|$0$ to $1$|Relative to sampling rate|
|**Digital Angular**|$\omega$|$2\pi F/F_s = 2\pi f$|rad/sample|$0$ to $2\pi$|**Z-domain DSP**|

### Quick Conversions

**From Physical Frequency F (Hz):** $$f = \frac{F}{F_s} \quad \text{(normalized)}$$

$$\omega = \frac{2\pi F}{F_s} = 2\pi f \quad \text{(digital angular, rad/sample)}$$

$$\Omega = 2\pi F \quad \text{(analog angular, rad/s)}$$

**Key Landmarks:**

- **Nyquist frequency:**
    - Physical: $F_{Nyquist} = F_s/2$ Hz
    - Normalized: $f_{Nyquist} = 0.5$
    - Digital angular: $\omega_{Nyquist} = \pi$ rad/sample

### Example (F25 Problem 3)

Given: $F_1 = 1500$ Hz, $F_s = 8000$ Hz

|Representation|Calculation|Result|
|---|---|---|
|Physical|$F_1$|1500 Hz|
|Normalized|$1500/8000$|$f_1 = 0.1875$|
|Digital angular|$2\pi \times 0.1875$|$\omega_1 = 0.375\pi$ rad/sample|
|Analog angular|$2\pi \times 1500$|$\Omega_1 = 9424.8$ rad/s|

### When to Use Each

**Physical F (Hz):**

- Problem specifications
- Real-world measurements
- Communication with non-DSP engineers

**Normalized f (dimensionless):**

- Filter design specifications
- Platform-independent descriptions
- Range: [0, 0.5] for valid frequencies

**Digital Angular ω (rad/sample):**

- **Z-domain analysis** (most common in DSP!)
- DTFT calculations: $H(e^{j\omega})$
- Filter frequency response
- Range: [0, π] for valid frequencies

**Analog Angular Ω (rad/s):**

- Analog prototype design
- Bilinear transform (BLT) calculations
- Pre-warping: $\Omega = \frac{2}{T_s}\tan(\omega/2)$

### Critical Notes

> [!warning] Common Mistakes
> 
> - Don't confuse $\omega$ (digital, rad/sample) with $\Omega$ (analog, rad/s)
> - Digital angular frequency $\omega$ is **unit-less** despite "rad" notation
> - Always specify which representation you're using!
> - In z-domain, we use $\omega$ (digital angular frequency)

> [!tip] Quick Check For valid digital frequencies:
> 
> - $0 \leq f \leq 0.5$ (normalized)
> - $0 \leq \omega \leq \pi$ (digital angular)
> - Above these → **aliasing!**

### Application in Course

**Sampling & Aliasing (Week 5-7):**

- Use $F$ for specifications
- Convert to $\omega$ to check if $\omega > \pi$ (aliasing)

**IIR Filter Design (Week 8-11):**

- Specify filter in $F$ (Hz)
- Pre-warp to analog $\Omega$ for prototype
- Design analog filter in s-domain
- Convert back to z-domain using BLT

**FIR Filter Design (Week 12-13):**

- Specify cutoff in $\omega$ directly
- Use $\omega_c$ in design equations

---

## Week 1: Introduction & MATLAB Programming

### 1.1 Discrete-Time Signals

**Discrete-Time (DT) Signals** are sequences indexed by integers, written as $x[n]$ where $n \in \mathbb{Z}$.

### 1.2 Basic Signal Types

#### Unit Impulse (Delta Function)

$$ \delta[n] = \begin{cases} 1, & n = 0 \ 0, & n \neq 0 \end{cases} $$

**Example Problem:**  
Q: What is $3\delta[n] + 2\delta[n-1]$ for $n = 0, 1, 2$?

A:

- $n=0$: $3\delta[0] + 2\delta[-1] = 3 \cdot 1 + 2 \cdot 0 = 3$
- $n=1$: $3\delta[1] + 2\delta[0] = 3 \cdot 0 + 2 \cdot 1 = 2$
- $n=2$: $3\delta[2] + 2\delta[1] = 0$

#### Unit Step Function

$$ u[n] = \begin{cases} 1, & n \geq 0 \ 0, & n < 0 \end{cases} $$

**Relationship:** $$ \boxed{\delta[n] = u[n] - u[n-1]} $$

**Example Problem:**  
Q: Express $x[n] = u[n] - u[n-5]$ in words.

A: This is a "rectangular pulse" that equals 1 for $0 \leq n < 5$ and 0 elsewhere.

#### Exponential Sequence

$$ x[n] = a^n u[n], \quad a \in \mathbb{R} $$

- If $|a| < 1$: **decaying** exponential
- If $|a| > 1$: **growing** exponential
- If $a < 0$: **alternating** sign

**Example Problem:**  
Q: Sketch $x[n] = (0.5)^n u[n]$ for $n = 0, 1, 2, 3, 4$.

A: Values: $1, 0.5, 0.25, 0.125, 0.0625$ (decaying exponential)

### 1.3 MATLAB Essentials

#### Geometric Series (Critical for Exams)

**Critical for Energy Calculations** [[F24 Exam]]: $$ \boxed{\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}, \quad |r| < 1} $$

**Example:** $\sum_{n=0}^{\infty} (0.5)^n = \frac{1}{1-0.5} = 2$

This formula is used extensively for:

- Signal energy: $E = \sum |x[n]|^2$
- System stability checks
- Convolution calculations

#### Basic Signal Generation

```matlab
% Discrete time axis
n = 0:10;  % n = [0, 1, 2, ..., 10]

% Unit impulse
delta = (n == 0);  % or: delta = @(k) double(k == 0);

% Unit step
u = (n >= 0);  % or: u = @(k) double(k >= 0);

% Exponential
a = 0.5;
x = a.^n .* u;  % Element-wise operations with "."

% Plotting
stem(n, x);  % Discrete-time plot
xlabel('n'); ylabel('x[n]');
title('Exponential Sequence');
grid on;
```

### 1.4 Signal Energy and Power

**Energy of a signal:** $$ E = \sum_{n=-\infty}^{\infty} |x[n]|^2 $$

**Power of a signal:** $$ P = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^2 $$

**Classifications:**

- **Energy signal:** $E < \infty$, $P = 0$
- **Power signal:** $E = \infty$, $P$ finite
- Neither: $E = \infty$, $P = \infty$

**Example from** [[Uge 01 - Tirsdag]]:

Signal: $x[n] = (0.8)^n u[n]$

Energy: $$ E = \sum_{n=0}^{\infty} |(0.8)^n|^2 = \sum_{n=0}^{\infty} (0.64)^n = \frac{1}{1-0.64} = \frac{25}{9} < \infty $$

This is an **energy signal** (finite energy, zero power).

---

## Week 2: LTI Systems (Time Domain)

### 2.1 Linear Time-Invariant (LTI) Systems

**Linearity:** If $x_1[n] \to y_1[n]$ and $x_2[n] \to y_2[n]$, then: $$ ax_1[n] + bx_2[n] \to ay_1[n] + by_2[n] $$

**Time Invariance:** If $x[n] \to y[n]$, then: $$ x[n-n_0] \to y[n-n_0] $$

### 2.2 Convolution

**Convolution sum:** $$ y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k]h[n-k] $$

**Properties:**

- **Commutative:** $x * h = h * x$
- **Associative:** $(x * h_1) * h_2 = x * (h_1 * h_2)$
- **Distributive:** $x * (h_1 + h_2) = x * h_1 + x * h_2$

**MATLAB:**

```matlab
y = conv(x, h);  % Linear convolution
```

**Manual Convolution Steps** [[Uge 02 - Tirsdag]]:

1. Flip $h[k]$ to get $h[-k]$
2. Shift by $n$ to get $h[n-k]$
3. Multiply point-wise: $x[k] \cdot h[n-k]$
4. Sum over all $k$

**Example:** $x[n] = {1, 2, 3}$ (at $n = 0, 1, 2$)  
$h[n] = {1, 1}$ (at $n = 0, 1$)

Result: $y[n] = {1, 3, 5, 3}$ (at $n = 0, 1, 2, 3$)

### 2.3 Impulse Response

**Definition:** The output when input is $\delta[n]$: $$ h[n] = T{\delta[n]} $$

**Why it matters:**

- **Completely characterizes** an LTI system
- Any output: $y[n] = x[n] * h[n]$

**Example from** [[Uge 02 - Tirsdag]]:

System: $y[n] = 0.5y[n-1] + x[n]$

Find impulse response:

- Input: $x[n] = \delta[n]$
- $h[0] = 0.5h[-1] + \delta[0] = 0 + 1 = 1$
- $h[1] = 0.5h[0] + \delta[1] = 0.5(1) + 0 = 0.5$
- $h[2] = 0.5h[1] + \delta[2] = 0.5(0.5) + 0 = 0.25$

Pattern: $h[n] = (0.5)^n u[n]$

### 2.3.1 Finding h[n] from Delayed Impulse Response [[F25 Exam]]

**Problem Type:** Given the system's response to a delayed impulse $\delta[n-k]$, find $h[n]$.

**Method:** Use **time-invariance** property

**Key Principle:**

- If input is $\delta[n-k]$ (delayed by $k$ samples)
- Output is $h[n-k]$ (impulse response delayed by $k$ samples)
- To get $h[n]$: shift the output **left by $k$ samples**

**Example from** [[F25 Exam]]:

**Given:**

- $x_1[n] + x_2[n] = \delta[n-1]$ (delayed impulse)
- $y_1[n] + y_2[n] = \delta[n-1] + 2\delta[n-2] + 6\delta[n-3] + 2\delta[n-4] + \delta[n-5]$

**Find:** $h[n]$

**Solution:**

1. By linearity: $y_1[n] + y_2[n]$ = response to $\delta[n-1]$
2. By time-invariance: response to $\delta[n-1]$ is $h[n-1]$
3. Therefore: $y_1[n] + y_2[n] = h[n-1]$
4. Shift indices left by 1 (replace each $n$ with $n+1$):

$$h[n] = \delta[n] + 2\delta[n-1] + 6\delta[n-2] + 2\delta[n-3] + \delta[n-4]$$

**MATLAB Pattern:**

```matlab
% Given: response to δ[n-1] is y_sum[n]
% By time-invariance: y_sum[n] = h[n-1]
% To find h[n], shift left by 1:
%   Each δ[n-k] becomes δ[n-(k-1)]
```

**⚠️ Common Mistake:**

- **DON'T** use $h[n] = y[n] - y[n-1]$ (that's only for step response!)
- This problem uses **time-invariance**, not step-to-impulse conversion

**When to use each method:**

|**Method**|**When to Use**|**Formula**|
|---|---|---|
|**Step → Impulse**|Input is $u[n]$|$h[n] = y_{\text{step}}[n] - y_{\text{step}}[n-1]$ [[E23 Exam]]|
|**Time-invariance shift**|Input is $\delta[n-k]$|$h[n]$ = shift $y[n]$ left by $k$ [[F25 Exam]]|

### 2.4 Step Response

**Definition:** The output when input is $u[n]$: $$ s[n] = T{u[n]} = u[n] * h[n] $$

**Relationship to impulse response:** $$ \boxed{h[n] = s[n] - s[n-1]} $$ $$ \boxed{s[n] = \sum_{k=-\infty}^{n} h[k]} $$

**Example from** [[E23 Exam]]:

Given step response, find impulse response using first difference: $$ h[n] = y_{\text{step}}[n] - y_{\text{step}}[n-1] $$

### 2.5 System Properties

**BIBO Stability:** $$ \sum_{n=-\infty}^{\infty} |h[n]| < \infty $$

If impulse response is **absolutely summable**, the system is stable.

**Causality:** $$ h[n] = 0 \quad \text{for } n < 0 $$

System output depends only on past/present inputs.

**Example** [[Uge_02__to_løsninger.pdf]]:

System: $h[n] = (0.9)^n u[n]$

Stability check: $$ \sum_{n=0}^{\infty} |(0.9)^n| = \frac{1}{1-0.9} = 10 < \infty $$ ✓ Stable

Causality: $h[n] = 0$ for $n < 0$ ✓ Causal

---

## Week 3: Frequency Domain

### 3.1 DTFT (Discrete-Time Fourier Transform)

**Forward DTFT:** $$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$

**Inverse DTFT:** $$ x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega $$

**Notation:**

- $\omega$ = digital angular frequency (rad/sample)
- $\omega \in [-\pi, \pi]$ or $[0, 2\pi]$

**Periodicity:** $$ X(e^{j(\omega + 2\pi)}) = X(e^{j\omega}) $$

### 3.2 DTFT Properties

**Linearity:** $$ ax_1[n] + bx_2[n] \xleftrightarrow{\text{DTFT}} aX_1(e^{j\omega}) + bX_2(e^{j\omega}) $$

**Time Shifting:** $$ x[n-n_0] \xleftrightarrow{\text{DTFT}} e^{-j\omega n_0} X(e^{j\omega}) $$

**Frequency Shifting (Modulation):** $$ e^{j\omega_0 n} x[n] \xleftrightarrow{\text{DTFT}} X(e^{j(\omega - \omega_0)}) $$

**Convolution Theorem:** $$ x[n] * h[n] \xleftrightarrow{\text{DTFT}} X(e^{j\omega}) \cdot H(e^{j\omega}) $$

This is **THE KEY** to frequency domain analysis!

**Multiplication (Modulation):** $$ x[n] \cdot w[n] \xleftrightarrow{\text{DTFT}} \frac{1}{2\pi} X(e^{j\omega}) \circledast W(e^{j\omega}) $$

where $\circledast$ denotes periodic convolution.

### 3.3 Frequency Response

**Definition:** For an LTI system with impulse response $h[n]$: $$ H(e^{j\omega}) = \sum_{n=-\infty}^{\infty} h[n] e^{-j\omega n} $$

**Magnitude and Phase:** $$ H(e^{j\omega}) = |H(e^{j\omega})| e^{j\angle H(e^{j\omega})} $$

**Physical meaning:**

- $|H(e^{j\omega})|$ = gain at frequency $\omega$
- $\angle H(e^{j\omega})$ = phase shift at frequency $\omega$

### 3.3.1 Converting H(z) to H(ω) [[F25 Exam]]

**Relationship between Z-transform and Frequency Response:**

The frequency response $H(\omega)$ is obtained by evaluating the transfer function $H(z)$ on the unit circle:

$$\boxed{H(\omega) = H(e^{j\omega}) = H(z)\bigg|_{z=e^{j\omega}}}$$

**Step-by-step procedure:**

1. **Start with H(z)** (transfer function in z-domain)
2. **Substitute** $z = e^{j\omega}$ everywhere
3. **Simplify** using $(e^{j\omega})^{-k} = e^{-j\omega k}$

**Example from** [[F25 Exam]]:

**Given:** $$H(z) = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}$$

**Find:** $H(\omega)$

**Solution:**

Substitute $z = e^{j\omega}$: $$H(\omega) = 1 + 2(e^{j\omega})^{-1} + 6(e^{j\omega})^{-2} + 2(e^{j\omega})^{-3} + (e^{j\omega})^{-4}$$

Simplify using $(e^{j\omega})^{-k} = e^{-j\omega k}$: $$\boxed{H(\omega) = 1 + 2e^{-j\omega} + 6e^{-2j\omega} + 2e^{-3j\omega} + e^{-4j\omega}}$$

**MATLAB Pattern:**

```matlab
% Given H(z) coefficients
b = [1, 2, 6, 2, 1];  % Numerator
a = [1];              % Denominator

% Method 1: Direct substitution
% H(ω) = 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)

% Method 2: Using freqz (evaluates at many ω points)
[H, w] = freqz(b, a, 1024);  % 1024 frequency points
% H contains H(ω) values, w contains ω values
```

**Key insight:**

- This is why $z = e^{j\omega}$ is called the **unit circle**
- $|z| = |e^{j\omega}| = 1$ (unit magnitude)
- $\arg(z) = \omega$ (angle is the frequency)

**MATLAB:**

```matlab
[H, w] = freqz(b, a, N);  % N frequency points
mag = abs(H);             % Magnitude
phase = angle(H);         % Phase (radians)
mag_dB = 20*log10(mag);   % Magnitude in dB
```

**Example from** [[Uge 03 - Tirsdag]]:

Simple system: $h[n] = \delta[n] + \delta[n-1]$

DTFT: $$ H(e^{j\omega}) = 1 + e^{-j\omega} = e^{-j\omega/2}(e^{j\omega/2} + e^{-j\omega/2}) = 2e^{-j\omega/2}\cos(\omega/2) $$

Magnitude: $|H(e^{j\omega})| = 2|\cos(\omega/2)|$  
Phase: $\angle H(e^{j\omega}) = -\omega/2$ (linear phase)

### 3.3.2 Analytical Magnitude Computation for Symmetric FIR [[F25 Exam]], [[E23 Exam]]

**When to use this method:**

- Filter has **symmetric** impulse response: $h[n] = h[M-n]$
- Example: $h[n] = [1, 2, 6, 2, 1]$ (symmetric around center)
- Results in **linear phase** FIR filter

**General Procedure:**

**Step 1: Identify the center**

- Filter order: $M$ (number of coefficients minus 1)
- Center index: $M/2$
- Example: $h[n] = [1, 2, 6, 2, 1]$ has $M = 4$, center at $n = 2$

**Step 2: Factor out center phase term**

From $H(\omega)$, factor out $e^{-j\omega(M/2)}$:

$$H(\omega) = e^{-j\omega(M/2)} \cdot A(\omega)$$

where $A(\omega)$ will be **real-valued** (because of symmetry).

**Step 3: Group symmetric terms**

Pair up symmetric exponentials:

- $e^{jk\omega}$ pairs with $e^{-jk\omega}$

**Step 4: Apply Euler's identity**

Use: $e^{jk\omega} + e^{-jk\omega} = 2\cos(k\omega)$

This converts all complex exponentials to real cosines.

**Step 5: Extract magnitude and phase**

Once in form $H(\omega) = e^{-j\omega(M/2)} \cdot A(\omega)$ where $A(\omega)$ is real:

$$\boxed{|H(\omega)| = |A(\omega)|}$$ $$\boxed{\angle H(\omega) = -\omega(M/2)}$$

**Key insight:** $|e^{-j\theta}| = 1$ always, so magnitude only depends on the real part $A(\omega)$.

---

**Complete Example from** [[F25 Exam]]:

**Given:** $$H(\omega) = 1 + 2e^{-j\omega} + 6e^{-2j\omega} + 2e^{-3j\omega} + e^{-4j\omega}$$

Coefficients: $h[n] = [1, 2, 6, 2, 1]$ (symmetric!) with $M = 4$

**Solution:**

**Step 1:** Center is at $M/2 = 2$

**Step 2:** Factor out $e^{-j2\omega}$:

$$H(\omega) = e^{-j2\omega} \left[e^{j2\omega} + 2e^{j\omega} + 6 + 2e^{-j\omega} + e^{-j2\omega}\right]$$

**Step 3:** Group symmetric terms:

$$= e^{-j2\omega} \left[(e^{j2\omega} + e^{-j2\omega}) + 2(e^{j\omega} + e^{-j\omega}) + 6\right]$$

**Step 4:** Apply Euler's identity:

$$= e^{-j2\omega} \left[2\cos(2\omega) + 4\cos(\omega) + 6\right]$$

**Step 5:** Extract magnitude and phase:

$$A(\omega) = 2\cos(2\omega) + 4\cos(\omega) + 6$$

Since $-1 \leq \cos(\theta) \leq 1$, we have: $$A(\omega) \geq 2(-1) + 4(-1) + 6 = 0$$

Therefore $A(\omega) \geq 0$ for all $\omega$, so:

$$\boxed{|H(\omega)| = 2\cos(2\omega) + 4\cos(\omega) + 6}$$ $$\boxed{\angle H(\omega) = -2\omega}$$

**MATLAB Verification:**

```matlab
% Coefficients
b = [1, 2, 6, 2, 1];
a = [1];
M = length(b) - 1;  % Order = 4

% Frequency range
omega = linspace(-pi, pi, 1024);

% Analytical magnitude
mag_analytical = 2*cos(2*omega) + 4*cos(omega) + 6;

% Analytical phase
phase_analytical = -2*omega;

% Verify with freqz
[H, w] = freqz(b, a, omega);
mag_freqz = abs(H);
phase_freqz = angle(H);

% Plot comparison
figure;
subplot(2,1,1);
plot(omega, mag_analytical, 'b-', 'LineWidth', 2); hold on;
plot(w, mag_freqz, 'r--', 'LineWidth', 1);
xlabel('\omega (rad/sample)'); ylabel('|H(\omega)|');
title('Magnitude Response');
legend('Analytical', 'freqz');
grid on;

subplot(2,1,2);
plot(omega, phase_analytical, 'b-', 'LineWidth', 2); hold on;
plot(w, phase_freqz, 'r--', 'LineWidth', 1);
xlabel('\omega (rad/sample)'); ylabel('\angle H(\omega)');
title('Phase Response');
legend('Analytical', 'freqz');
grid on;
```

---

**Why This Method Works:**

For symmetric FIR filters:

1. Symmetry forces all imaginary parts to cancel out
2. Only real cosine terms remain after factoring
3. Phase is purely linear: $-\omega(M/2)$
4. This is why they're called "**Linear Phase FIR**" filters

**Critical Exam Tip:**

- Always check if coefficients are symmetric first!
- If symmetric, use this analytical method (much faster than direct computation)
- The official solution in [[E23 Exam]] and [[F25 Exam]] expects this approach

### 3.4 Ideal Filters

**Ideal Low-Pass:** $$ H_{\text{LP}}(e^{j\omega}) = \begin{cases} 1, & |\omega| \leq \omega_c \ 0, & \omega_c < |\omega| \leq \pi \end{cases} $$

Impulse response: $$ h_{\text{LP}}[n] = \frac{\sin(\omega_c n)}{\pi n}, \quad h_{\text{LP}}[0] = \frac{\omega_c}{\pi} $$

**Ideal High-Pass:** $$ h_{\text{HP}}[n] = \delta[n] - h_{\text{LP}}[n] $$

**Ideal Band-Pass:** $$ h_{\text{BP}}[n] = h_{\text{LP2}}[n] - h_{\text{LP1}}[n] $$

where $\omega_{c1} < \omega_{c2}$ are the lower and upper cutoffs.

**Problem:** Ideal filters are **non-causal** and have **infinite length** → Cannot be implemented exactly

**Solution:** Truncate and shift to make causal (covered in [[62743 E25 Digital filter design IIR part1.pdf]])

---

## Week 4: Z-Transform

### 4.1 Z-Transform Definition

**Forward Z-Transform:** $$ X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n} $$

**Inverse Z-Transform:** $$ x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz $$

**Relationship to DTFT:** $$ X(e^{j\omega}) = X(z)\bigg|_{z = e^{j\omega}} $$

The DTFT is the Z-transform evaluated on the unit circle.

### 4.2 Common Z-Transform Pairs

|Signal $x[n]$|Z-Transform $X(z)$|ROC|
|---|---|---|
|$\delta[n]$|$1$|All $z$|
|$u[n]$|$\frac{1}{1-z^{-1}} = \frac{z}{z-1}$|$\|z\| > 1$|
|$a^n u[n]$|$\frac{1}{1-az^{-1}} = \frac{z}{z-a}$|$\|z\| > \|a\|$|
|$-a^n u[-n-1]$|$\frac{1}{1-az^{-1}}$|$\|z\| < \|a\|$|
|$na^n u[n]$|$\frac{az^{-1}}{(1-az^{-1})^2}$|$\|z\| > \|a\|$|

**Example from** [[Uge 04 - Tirsdag]]:

Find Z-transform of $x[n] = (0.5)^n u[n]$:

$$ X(z) = \sum_{n=0}^{\infty} (0.5)^n z^{-n} = \sum_{n=0}^{\infty} (0.5z^{-1})^n = \frac{1}{1 - 0.5z^{-1}} = \frac{z}{z - 0.5} $$

ROC: $|z| > 0.5$ (outside the pole)

### 4.3 Z-Transform Properties

**Linearity:** $$ ax_1[n] + bx_2[n] \xleftrightarrow{Z} aX_1(z) + bX_2(z) $$

**Time Shifting:** $$ x[n-n_0] \xleftrightarrow{Z} z^{-n_0} X(z) $$

**Scaling in Z-domain:** $$ a^n x[n] \xleftrightarrow{Z} X(a^{-1}z) $$

**Convolution:** $$ x[n] * h[n] \xleftrightarrow{Z} X(z) \cdot H(z) $$

**Initial Value Theorem:** If $x[n]$ is causal: $$ x[0] = \lim_{z \to \infty} X(z) $$

**Final Value Theorem:** If $x[n]$ converges: $$ \lim_{n \to \infty} x[n] = \lim_{z \to 1} (z-1)X(z) $$

### 4.4 Inverse Z-Transform Methods

#### Method 1: Partial Fraction Expansion

**For rational functions:** $$ X(z) = \frac{N(z)}{D(z)} = \frac{b_0 + b_1 z^{-1} + \cdots}{1 + a_1 z^{-1} + \cdots} $$

**MATLAB:**

```matlab
[r, p, k] = residue(b, a);
% r = residues
% p = poles
% k = direct term
```

**Then use:** $$ \frac{A}{1 - pz^{-1}} \xleftrightarrow{Z} A \cdot p^n u[n] \quad \text{(if causal)} $$

#### Method 2: Long Division

Divide numerator by denominator to get sequence directly.

#### Method 3: Table Lookup

Match $X(z)$ to known transform pairs.

### 4.5 Transfer Function H(z)

**Definition:** $$ H(z) = \frac{Y(z)}{X(z)} = \mathcal{Z}{h[n]} $$

**Rational form:** $$ H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}} $$

Or: $$ H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}} $$

**Corresponds to difference equation:** $$ y[n] = -\sum_{k=1}^{N} a_k y[n-k] + \sum_{k=0}^{M} b_k x[n-k] $$

### 4.6 Poles, Zeros, and Stability

**Zeros:** Values of $z$ where $H(z) = 0$  
**Poles:** Values of $z$ where $H(z) = \infty$

**From rational form:** $$ H(z) = G \frac{(z - z_1)(z - z_2)\cdots(z - z_M)}{(z - p_1)(z - p_2)\cdots(z - p_N)} $$

**MATLAB:**

```matlab
zeros_H = roots(b);  % Find zeros
poles_H = roots(a);  % Find poles

% Pole-zero plot
figure;
zplane(b, a);
```

**Stability Criterion:**

For a **causal** system to be **BIBO stable**: $$ \boxed{\text{All poles must be inside the unit circle: } |p_k| < 1} $$

**Example from** [[Uge 04 - Torsdag]]:

$$ H(z) = \frac{1 + 0.5z^{-1}}{1 - 0.8z^{-1}} $$

- Zero at $z = -0.5$ (inside unit circle)
- Pole at $z = 0.8$ (inside unit circle)
- Since $|0.8| < 1$, system is **stable**

**For inverse system stability:** All **zeros** of $H(z)$ must be inside unit circle (minimum phase condition) [[Week 5]].

### 4.7 Combined Systems and Pole-Zero Cancellation

#### System Interconnections

**Three basic configurations:**

1. **Parallel Connection:** $$H_{\text{total}}(z) = H_1(z) + H_2(z)$$
    
    - Outputs add: $y[n] = y_1[n] + y_2[n]$
    - Just add numerators if same denominator
2. **Series (Cascade) Connection:** $$H_{\text{total}}(z) = H_1(z) \cdot H_2(z)$$
    
    - Output of first is input to second
    - Multiply transfer functions
3. **Feedback Connection:** $$H_{\text{total}}(z) = \frac{H_1(z)}{1 + H_1(z)H_2(z)}$$
    
    - Negative feedback: subtract output

**Combination example** (F25 Problem 1-5): $$ H_{\text{total}}(z) = \big(H_1(z) + H_2(z)\big) \cdot H_3(z) $$ (Parallel systems T1, T2 followed by series system T3)

---

#### Pole-Zero Cancellation Method

**When combining systems, poles from one system may cancel with zeros from another!**

**Recognition pattern:**

- System looks like IIR (has denominator with poles)
- But after simplification → becomes FIR (denominator = 1)

**Example:** From F25 Problem 1-5: $$ H(z) = \frac{4 - 8z^{-1} - 5z^{-2} + 2z^{-3} + z^{-4}}{1 - \frac{1}{4}z^{-2}} $$

Initial appearance: **IIR** (has feedback term $-\frac{1}{4}z^{-2}$ in denominator)

**But!** The denominator factor might divide evenly into numerator → **cancellation**

---

#### MATLAB Approach: Polynomial Division

**Step-by-step methodology:**

1. **Convert to positive powers** (multiply by $z^M$)
    
    - Numerator: $4z^4 - 8z^3 - 5z^2 + 2z + 1$
    - Denominator factor: $z^2 - \frac{1}{4}$
2. **Use `deconv()` for polynomial division:**
    
    ```matlab
    num = [4, -8, -5, 2, 1];      % Coefficients [z^4, z^3, z^2, z^1, z^0]
    den = [1, 0, -1/4];            % z^2 - 1/4
    
    [quotient, remainder] = deconv(num, den);
    ```
    
3. **Check remainder:**
    
    - `remainder = [0, 0, 0]` → **Perfect cancellation!**
    - Quotient: `[4, -8, -4]` represents $4z^2 - 8z - 4$
4. **Convert back to $z^{-n}$ form:** $$H(z) = 4 - 8z^{-1} - 4z^{-2} \quad \text{(FIR!)}$$
    

---

#### Verification: FIR vs IIR After Cancellation

**Three checks to confirm FIR:**

|Check|FIR Criterion|Example Result|
|---|---|---|
|1. Denominator|Must equal `[1]`|✓ After cancellation: `[1]`|
|2. Remainder|Must be zero|✓ `deconv` gives `[0, 0, 0]`|
|3. Impulse response|Finite length|✓ Only 3 samples: `[4, -8, -4]`|

**Complete MATLAB verification:**

```matlab
% After deconv
fprintf('Quotient: '); disp(quotient);
fprintf('Remainder: '); disp(remainder);

if all(abs(remainder) < 1e-10)  % Check for numerical zeros
    fprintf('✓ Perfect cancellation → FIR system\n');
    fprintf('Impulse response length: %d samples\n', length(quotient));
else
    fprintf('✗ No cancellation → IIR system\n');
end
```

---

#### Why Cancellation Happens

**Mathematical reason:**

- Denominator has poles at $z = \pm\frac{1}{2}$ (from $z^2 - \frac{1}{4} = 0$)
- Numerator must have zeros at **exactly the same locations**
- These zeros "fill in" the poles → stable cancellation
- Result: transfer function simplifies to pure polynomial

**Physical interpretation:**

- The feedback (IIR) component is exactly compensated by feedforward zeros
- Net effect: finite impulse response

---

#### Exam Strategy for Combined Systems

**When you see:**

- Multiple systems in series/parallel
- An IIR system in the combination
- Question asks "Is it FIR?"

**Do this:**

1. Write combined transfer function formula
2. Add/multiply as needed (MATLAB: `conv()` for multiply)
3. **Don't assume IIR!** Try polynomial division
4. Use `deconv()` to check for cancellation
5. If remainder ≈ 0 → argue it's FIR after cancellation

> [!warning] **Exam Note** The exam explicitly allows MATLAB for polynomial operations! From F25: _"Det er tilladt at benytte Matlab til, at udføre beregninger med polynomier"_
> 
> Don't waste time on manual polynomial division - use `deconv()`!

**Reference:** See [[F25 Exam]] Problem 1-5 for complete worked example

---

## Exam Strategy for Weeks 1-4

### Most Common Question Types

**Week 1:**

1. Basic signal operations with $\delta[n]$ and $u[n]$
2. Energy/power calculations using geometric series
3. Signal classification (energy vs power)

**Week 2:**

1. Convolution calculations (manual or MATLAB)
2. Finding impulse response from difference equation
3. Step response → impulse response conversion
4. Stability checks (absolute summability)

**Week 3:**

1. Computing DTFT of simple sequences
2. Magnitude/phase plots
3. Frequency response interpretation
4. Ideal filter impulse responses

**Week 4:**

1. Z-transform from definition or table
2. ROC identification (critical!)
3. Pole-zero plots and stability
4. Transfer function ↔ difference equation
5. Inverse Z-transform (partial fractions)
6. **Combined systems with pole-zero cancellation** (F25)

### Critical Formulas to Memorize

1. **Geometric series:** $$\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}, \quad |r| < 1$$
    
2. **Step ↔ impulse:** $$h[n] = s[n] - s[n-1]$$
    
3. **Convolution theorem (Z-domain):** $$y[n] = x[n] * h[n] \Leftrightarrow Y(z) = X(z)H(z)$$
    
4. **Stability criterion:** $$\text{All poles: } |p_k| < 1$$
    
5. **Basic Z-transforms:** $$u[n] \xleftrightarrow{Z} \frac{1}{1-z^{-1}}, \quad a^n u[n] \xleftrightarrow{Z} \frac{1}{1-az^{-1}}$$
    

### Common Mistakes to Avoid

1. **Forgetting ROC** when writing Z-transforms
2. **Wrong convolution limits** (start from $k=0$ for causal signals)
3. **Sign errors** in difference equations ($-a_k$ terms!)
4. **Confusing poles and zeros** for stability vs inverse stability
5. **DTFT periodicity** - always $2\pi$ periodic
6. **Unit circle evaluation** $z = e^{j\omega}$ to get frequency response

---

## Quick Reference: MATLAB Commands

```matlab
% Week 1-2: Basic operations
n = 0:10;                    % Time index
delta = (n == 0);            % Unit impulse
u = (n >= 0);                % Unit step
y = conv(x, h);              % Convolution
E = sum(abs(x).^2);          % Energy

% Week 3: Frequency domain
[H, w] = freqz(b, a, N);     % Frequency response
mag = abs(H);                % Magnitude
phase = angle(H);            % Phase
mag_dB = 20*log10(mag);      % Magnitude in dB

% Week 4: Z-domain
[r, p, k] = residue(b, a);   % Partial fractions
zplane(b, a);                % Pole-zero plot
zeros_H = roots(b);          % Find zeros
poles_H = roots(a);          % Find poles
stable = all(abs(poles_H)<1);% Check stability
[q, r] = deconv(num, den);   % Polynomial division (cancellation check)
```

---

**See also:**

- [[Week 5-7]]
- [[Week 8-11]]
- [[Week 12-13]]
- [[DSP-Bible]] (Complete MATLAB reference)
- [[E23 Exam]], [[F24 Exam]], [[E24 Exam]]

---

## Praktisk Anvendelse

| Projekt | Link | Anvendelse |
|---------|------|------------|
| VLF Metaldetektor (34621) | [DFT Algoritme](obsidian://open?vault=34621-Metal-Detector&file=Docs%2FTheory%2FDFT%20Algorithm) | Sampling ved 8 kHz, DFT ved 2 kHz, kompleks faseberegning |