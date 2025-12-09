# DTU 62743 DSP Formula Sheet (Weeks 1–4)
**Digital Signal Processing | Technical University of Denmark**

---

## 📌 Table of Contents
1. [Week 1: Introduction & MATLAB](#week-1)
2. [Week 2: Discrete-Time Signals & Systems (Time Domain)](#week-2)
3. [Week 3: Discrete-Time Signals & Systems (Frequency Domain)](#week-3)
4. [Week 4: Z-Transform](#week-4)

---

<a name="week-1"></a>
# Week 1: Introduction & MATLAB Programming

## Core Concepts
**Discrete-Time (DT) Signals** are sequences indexed by integers, written as $x[n]$ where $n \in \mathbb{Z}$.

### Key Signal Types

#### 1. Unit Impulse (Delta Function)
$$
\delta[n] = \begin{cases}
1, & n = 0 \\
0, & n \neq 0
\end{cases}
$$

**Example Problem:**  
Q: What is $3\delta[n] + 2\delta[n-1]$ for $n = 0, 1, 2$?

A: 
- $n=0$: $3\delta[0] + 2\delta[-1] = 3 \cdot 1 + 2 \cdot 0 = 3$
- $n=1$: $3\delta[1] + 2\delta[0] = 3 \cdot 0 + 2 \cdot 1 = 2$
- $n=2$: $3\delta[2] + 2\delta[1] = 0$

#### 2. Unit Step Function
$$
u[n] = \begin{cases}
1, & n \geq 0 \\
0, & n < 0
\end{cases}
$$

**Relationship:**
$$
\boxed{\delta[n] = u[n] - u[n-1]}
$$

**Example Problem:**  
Q: Express $x[n] = u[n] - u[n-5]$ in words.

A: This is a "rectangular pulse" that equals 1 for $0 \leq n < 5$ and 0 elsewhere.

#### 3. Exponential Sequence
$$
x[n] = a^n u[n], \quad a \in \mathbb{R}
$$

- If $|a| < 1$: **decaying** exponential
- If $|a| > 1$: **growing** exponential  
- If $a < 0$: **alternating** sign

**Example Problem:**  
Q: Sketch $x[n] = (0.5)^n u[n]$ for $n = 0, 1, 2, 3, 4$.

A: Values: $1, 0.5, 0.25, 0.125, 0.0625$ (decaying exponential)

### MATLAB Essentials

#### Quick Math Reference: Geometric Series

**Critical for Energy Calculations** [F20 Exam]:
$$
\boxed{\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}, \quad |r| < 1}
$$

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
stem(n, x, 'filled');  % Discrete-time plot
xlabel('n'); ylabel('x[n]'); grid on;
```

---

<a name="week-2"></a>
# Week 2: Discrete-Time Systems (Time Domain)

## LTI Systems

### Definition
A **Linear Time-Invariant (LTI)** system satisfies:
1. **Linearity**: $T\{ax_1[n] + bx_2[n]\} = aT\{x_1[n]\} + bT\{x_2[n]\}$
2. **Time-Invariance**: If $y[n] = T\{x[n]\}$, then $y[n-n_0] = T\{x[n-n_0]\}$

### Impulse Response
**Definition:** The output when the input is $\delta[n]$:
$$
\boxed{h[n] = T\{\delta[n]\}}
$$

The impulse response **completely characterizes** an LTI system.

### Convolution Sum
**Key Formula:** For any input $x[n]$, the output is:
$$
\boxed{y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]}
$$

**Alternative form:**
$$
y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k]
$$

### Finding Impulse Response from Step Response

**The DTU Trick** [E23 Q1, F24 Q1]:  
Given step response $y_{step}[n]$ when input is $u[n]$, use:
$$
\boxed{h[n] = y_{step}[n] - y_{step}[n-1]}
$$

**Why?** Because $\delta[n] = u[n] - u[n-1]$ and LTI systems preserve this relationship.

**Example Problem:**  
Given: $y_{step}[n] = -\delta[n] - 5\delta[n-1] + 5\delta[n-2] + \delta[n-3]$

Q: Find the impulse response.

A:
$$
\begin{aligned}
h[n] &= y_{step}[n] - y_{step}[n-1] \\
h[0] &= y_{step}[0] - y_{step}[-1] = -1 - 0 = -1 \\
h[1] &= y_{step}[1] - y_{step}[0] = -5 - (-1) = -4 \\
h[2] &= y_{step}[2] - y_{step}[1] = 5 - (-5) = 10 \\
h[3] &= y_{step}[3] - y_{step}[2] = 1 - 5 = -4 \\
h[4] &= y_{step}[4] - y_{step}[3] = 0 - 1 = -1
\end{aligned}
$$

Result: $h[n] = -\delta[n] - 4\delta[n-1] + 10\delta[n-2] - 4\delta[n-3] - \delta[n-4]$

### FIR vs IIR Classification

**FIR (Finite Impulse Response):**
- $h[n]$ is **finite-length** (zero outside some range)
- **No feedback** in difference equation
- **Always stable**

**IIR (Infinite Impulse Response):**
- $h[n]$ extends to infinity
- **Has feedback** (output depends on past outputs)
- May be unstable

**Red Flags for IIR** [Course Standard]:
1. Difference equation has $y[n-k]$ terms on right side
2. Transfer function $H(z)$ has non-trivial denominator
3. Impulse response doesn't become zero

**Example Problem:**  
Q: Is $h[n] = (0.5)^n u[n]$ FIR or IIR?

A: **IIR** because it never becomes exactly zero (infinite length).

### Difference Equations

**General form:**
$$
\sum_{k=0}^{N} a_k y[n-k] = \sum_{k=0}^{M} b_k x[n-k]
$$

**Standard causal form:**
$$
\boxed{y[n] = -\sum_{k=1}^{N} a_k y[n-k] + \sum_{k=0}^{M} b_k x[n-k]}
$$

**Example Problem:**  
Q: Write the difference equation for $H(z) = \frac{2 + 3z^{-1}}{1 - 0.5z^{-1}}$.

A:
$$
y[n] = 0.5y[n-1] + 2x[n] + 3x[n-1]
$$

### Stability

**BIBO Stability Condition:**
$$
\boxed{\sum_{n=-\infty}^{\infty} |h[n]| < \infty}
$$

For exponential $h[n] = a^n u[n]$: stable if $|a| < 1$.

**Example Problem:**  
Q: Is $h[n] = 2^n u[n]$ stable?

A: No, because $\sum |2^n| = \infty$ (diverges).

### Signal Energy Calculation

**Energy of a signal:**
$$
E = \sum_{n=-\infty}^{\infty} |x[n]|^2
$$

**Key Tool: Geometric Series** [F20 Exam]:

For exponential signals $x[n] = a^n u[n]$:
$$
\boxed{E = \sum_{n=0}^{\infty} |a|^{2n} = \sum_{n=0}^{\infty} (a^2)^n = \frac{1}{1-a^2}, \quad |a| < 1}
$$

**Example Problem:**  
Q: Find the energy of $x[n] = (0.5)^n u[n]$.

A:
$$
E = \sum_{n=0}^{\infty} (0.5)^{2n} = \sum_{n=0}^{\infty} (0.25)^n = \frac{1}{1-0.25} = \frac{4}{3}
$$

**Finite Energy:** If $E < \infty$, the signal has finite energy.  
**Infinite Energy:** If $E = \infty$, the signal has infinite energy (e.g., $u[n]$).

### MATLAB: Convolution & Filtering

```matlab
% Define signals
x = [1 2 3 4];
h = [0.5 0.5];

% Convolution
y = conv(x, h);
% Result: [0.5 1.5 2.5 3.5 2]

% Filtering (for difference equations)
b = [1 2];     % Numerator coefficients
a = [1 -0.5];  % Denominator coefficients
x = [1 0 0 0 0];
y = filter(b, a, x);
```

---

<a name="week-3"></a>
# Week 3: Frequency Domain Analysis

## Discrete-Time Fourier Transform (DTFT)

### Definition
$$
\boxed{X(\omega) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}}
$$

where $\omega \in [-\pi, \pi]$ is the **normalized digital angular frequency** (rad/sample).

**Inverse DTFT:**
$$
\boxed{x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(\omega) e^{j\omega n} d\omega}
$$

### Relationship Between Frequencies

**Analog frequency $F$ (Hz) ↔ Digital frequency $\omega$ (rad/sample):**
$$
\boxed{\omega = 2\pi \frac{F}{F_s}}
$$

where $F_s$ is the sampling frequency (Hz).

**Example Problem:**  
Q: If $F_s = 8000$ Hz and $F = 1000$ Hz, what is $\omega$?

A:
$$
\omega = 2\pi \frac{1000}{8000} = \frac{\pi}{4} \approx 0.785 \text{ rad/sample}
$$

### Key DTFT Properties

| **Property** | **Time Domain** | **Frequency Domain** |
|---|---|---|
| Linearity | $ax_1[n] + bx_2[n]$ | $aX_1(\omega) + bX_2(\omega)$ |
| Time Shift | $x[n - n_0]$ | $e^{-j\omega n_0} X(\omega)$ |
| Frequency Shift | $e^{j\omega_0 n} x[n]$ | $X(\omega - \omega_0)$ |
| Convolution | $x[n] * h[n]$ | $X(\omega) H(\omega)$ |
| Multiplication | $x[n] h[n]$ | $\frac{1}{2\pi} X(\omega) * H(\omega)$ |

### Frequency Response of LTI Systems

**Frequency Response:**
$$
\boxed{H(\omega) = \text{DTFT}\{h[n]\} = \sum_{n=-\infty}^{\infty} h[n] e^{-j\omega n}}
$$

**Key Insight:** 
$$
\boxed{Y(\omega) = X(\omega) H(\omega)}
$$

**From Difference Equation:**  
Given $\sum a_k y[n-k] = \sum b_k x[n-k]$, take DTFT of both sides:
$$
\boxed{H(\omega) = \frac{\sum_{k=0}^{M} b_k e^{-j\omega k}}{\sum_{k=0}^{N} a_k e^{-j\omega k}}}
$$

**Example Problem:**  
Q: Find $H(\omega)$ for $y[n] - \frac{1}{2}y[n-1] = x[n]$.

A: Taking DTFT:
$$
Y(\omega) - \frac{1}{2}e^{-j\omega} Y(\omega) = X(\omega)
$$
$$
H(\omega) = \frac{Y(\omega)}{X(\omega)} = \frac{1}{1 - \frac{1}{2}e^{-j\omega}}
$$

### Magnitude and Phase

$$
H(\omega) = |H(\omega)| e^{j\angle H(\omega)}
$$

- **Magnitude:** $|H(\omega)| = \sqrt{\text{Re}^2\{H(\omega)\} + \text{Im}^2\{H(\omega)\}}$
- **Phase:** $\angle H(\omega) = \arctan\left(\frac{\text{Im}\{H(\omega)\}}{\text{Re}\{H(\omega)\}}\right)$

### Linear Phase FIR Filters

**Symmetry Condition:**  
If $h[n] = h[M - n]$ (symmetric), then:
$$
\boxed{H(\omega) = e^{-j\omega K} A(\omega)}
$$

where $K = M/2$ and $A(\omega)$ is **real-valued**.

**The DTU Phase Factorization Method** [E23 Q1-3]:  
For symmetric FIR like $h[n] = [h_0, h_1, h_2, h_1, h_0]$ (5 taps, $M=4$, $K=2$):

1. Factor out the center delay: $e^{-j2\omega}$
2. Group symmetric pairs using $e^{j\theta} + e^{-j\theta} = 2\cos\theta$:

$$
\begin{aligned}
H(\omega) &= h_0 + h_1 e^{-j\omega} + h_2 e^{-j2\omega} + h_1 e^{-j3\omega} + h_0 e^{-j4\omega} \\
&= e^{-j2\omega}\left[h_2 + 2h_1\cos\omega + 2h_0\cos 2\omega\right]
\end{aligned}
$$

**Result:**
- **Magnitude:** $|H(\omega)| = |h_2 + 2h_1\cos\omega + 2h_0\cos 2\omega|$
- **Phase:** $\angle H(\omega) = -2\omega$ (linear) when amplitude is positive

**Example Problem:**  
Given: $h[n] = [-1, -4, 10, -4, -1]$

Q: Find $|H(\omega)|$ using symmetry.

A:
$$
H(\omega) = e^{-j2\omega}[10 - 8\cos\omega - 2\cos 2\omega]
$$
$$
|H(\omega)| = |10 - 8\cos\omega - 2\cos 2\omega|
$$

### MATLAB: Frequency Response

```matlab
% Define FIR filter
b = [-1 -4 10 -4 -1];
a = 1;

% Compute frequency response
[H, w] = freqz(b, a, 2048);

% Plot magnitude (linear)
plot(w/pi, abs(H));
xlabel('\omega/\pi'); ylabel('|H(\omega)|');

% Plot magnitude (dB)
plot(w/pi, 20*log10(abs(H)));
ylabel('Magnitude (dB)');

% Plot phase
plot(w/pi, unwrap(angle(H)));
ylabel('Phase (radians)');
```

---

<a name="week-4"></a>
# Week 4: Z-Transform

## Definition

**Z-Transform:**
$$
\boxed{X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}}
$$

where $z \in \mathbb{C}$ is a complex variable.

**Region of Convergence (ROC):** Set of $z$ values for which $X(z)$ converges.

### Connection to DTFT

**Critical Relationship:**
$$
\boxed{X(\omega) = X(z)\Big|_{z = e^{j\omega}}}
$$

DTFT exists when the **unit circle is in the ROC**.

### Common Z-Transform Pairs

| **Signal $x[n]$** | **Z-Transform $X(z)$** | **ROC** |
|---|---|---|
| $\delta[n]$ | $1$ | All $z$ |
| $u[n]$ | $\frac{1}{1-z^{-1}} = \frac{z}{z-1}$ | $\|z\| > 1$ |
| $a^n u[n]$ | $\frac{1}{1-az^{-1}} = \frac{z}{z-a}$ | $\|z\| > \|a\|$ |
| $-a^n u[-n-1]$ | $\frac{1}{1-az^{-1}}$ | $\|z\| < \|a\|$ |
| $n a^n u[n]$ | $\frac{az^{-1}}{(1-az^{-1})^2}$ | $\|z\| > \|a\|$ |

**Example Problem:**  
Q: Find $X(z)$ for $x[n] = (0.5)^n u[n]$.

A:
$$
X(z) = \frac{1}{1 - 0.5z^{-1}} = \frac{z}{z - 0.5}, \quad |z| > 0.5
$$

### Transfer Function

**System Function:**
$$
\boxed{H(z) = \frac{Y(z)}{X(z)} = \sum_{n=-\infty}^{\infty} h[n] z^{-n}}
$$

**From Difference Equation:**
$$
H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{\sum_{k=0}^{N} a_k z^{-k}} = \frac{B(z)}{A(z)}
$$

**Example Problem:**  
Q: Find $H(z)$ for $y[n] - \frac{3}{4}y[n-1] + \frac{1}{8}y[n-2] = x[n]$.

A: Taking Z-transform:
$$
Y(z) - \frac{3}{4}z^{-1}Y(z) + \frac{1}{8}z^{-2}Y(z) = X(z)
$$
$$
H(z) = \frac{1}{1 - \frac{3}{4}z^{-1} + \frac{1}{8}z^{-2}}
$$

Factor denominator:
$$
H(z) = \frac{1}{(1 - \frac{1}{2}z^{-1})(1 - \frac{1}{4}z^{-1})}
$$

### Poles and Zeros

**Zeros:** Values of $z$ where $H(z) = 0$ (numerator zeros)  
**Poles:** Values of $z$ where $H(z) = \infty$ (denominator zeros)

**Example:** For $H(z) = \frac{1 + 0.3z^{-1}}{(1-0.2z^{-1})(1-0.4z^{-1})}$
- **Zero:** $z_1 = -0.3$
- **Poles:** $p_1 = 0.2$, $p_2 = 0.4$

### Stability from Poles

**Stability Condition:**  
All poles must be **inside the unit circle**:
$$
\boxed{|p_k| < 1 \text{ for all poles } p_k}
$$

**Example Problem:**  
Q: Is $H(z) = \frac{1}{(1-0.5z^{-1})(1-2z^{-1})}$ stable?

A: Poles at $z = 0.5$ and $z = 2$.  
Since $|2| > 1$, the system is **UNSTABLE**.

### Minimum Phase & Stable Inverse Systems

**Critical Exam Concept** [E20, F25]:

For a system $H(z)$ to have a **stable inverse** $H^{-1}(z)$:
$$
\boxed{\text{All ZEROS of } H(z) \text{ must be inside the unit circle: } |z_k| < 1}
$$

**Why?** When you invert $H(z) = \frac{B(z)}{A(z)}$, the inverse is $H^{-1}(z) = \frac{A(z)}{B(z)}$. The **zeros become poles** in the inverse system!

**Example Problem:**  
Q: Can $H(z) = \frac{(1 + 2z^{-1})}{(1 - 0.3z^{-1})}$ have a stable inverse?

A: 
- Zero: $z = -2$ → $|z| = 2 > 1$ (outside unit circle)
- The inverse $H^{-1}(z) = \frac{(1 - 0.3z^{-1})}{(1 + 2z^{-1})}$ has a pole at $z = -2$
- **Answer: NO**, the inverse is unstable.

**Minimum Phase Definition:**  
A system is **minimum phase** if all its poles AND zeros are inside the unit circle.

### Inverse Z-Transform Methods

#### 1. Partial Fraction Expansion

For $H(z) = \frac{B(z)}{A(z)}$ with simple poles:
$$
H(z) = \frac{A_1}{1-p_1z^{-1}} + \frac{A_2}{1-p_2z^{-1}} + \cdots
$$

Then:
$$
h[n] = A_1 p_1^n u[n] + A_2 p_2^n u[n] + \cdots
$$

**Example Problem:**  
Q: Find $h[n]$ for $H(z) = \frac{1+0.3z^{-1}}{(1-0.2z^{-1})(1-0.4z^{-1})}$.

A: Using partial fractions:
$$
H(z) = \frac{3.5}{1-0.4z^{-1}} - \frac{2.5}{1-0.2z^{-1}}
$$
$$
h[n] = 3.5(0.4)^n u[n] - 2.5(0.2)^n u[n]
$$

#### 2. Inspection / Pattern Matching

Use Z-transform tables directly.

#### 3. Long Division (for FIR)

Divide numerator by denominator to get $h[0], h[1], h[2], \ldots$

### MATLAB: Z-Domain Analysis

```matlab
% Define transfer function
b = [1 0.3];           % Numerator: 1 + 0.3z^-1
a = [1 -0.6 0.08];     % Denominator: 1 - 0.6z^-1 + 0.08z^-2

% Find poles and zeros
[z, p, k] = tf2zp(b, a);
fprintf('Zeros: '); disp(z.');
fprintf('Poles: '); disp(p.');

% Check stability
if all(abs(p) < 1)
    disp('System is STABLE');
else
    disp('System is UNSTABLE');
end

% Pole-zero plot
zplane(b, a);
title('Pole-Zero Plot');

% Partial fraction expansion
[r, p, k] = residue(b, a);
fprintf('Residues: '); disp(r.');
fprintf('Poles: '); disp(p.');

% Impulse response (first 20 samples)
[h, n] = impz(b, a, 20);
stem(n, h, 'filled');
xlabel('n'); ylabel('h[n]');
title('Impulse Response');
```

---

## 🎯 Exam Strategy Tips

### High-Priority Formulas (Based on E19-F25 Exams)

**🔥 Top 5 Most Tested Concepts:**

1. **Step → Impulse** [E23, F24]: $h[n] = y_{step}[n] - y_{step}[n-1]$
2. **Symmetric FIR Phase** [E23]: Factor $e^{-j\omega K}$ and use $2\cos\omega$ grouping
3. **Stable Inverse** [E20, F25]: Zeros must be inside unit circle ($|z_k| < 1$)
4. **Energy via Geometric Series** [F20]: $\sum (a^2)^n = \frac{1}{1-a^2}$
5. **Partial Fraction on $H(z)$** [E19, E22]: Expand directly, not $H(z)/z$

### Pattern Recognition

1. **Step → Impulse:** Use $h[n] = y_{step}[n] - y_{step}[n-1]$
2. **Symmetric FIR:** Factor out $e^{-j\omega K}$ and use cosines
3. **IIR from Difference Eq:** Convert to $H(z)$, find poles, check stability
4. **Frequency Conversion:** Always use $\omega = 2\pi F/F_s$
5. **Inverse Systems:** Check if zeros are inside unit circle!

### Red Flags

- **Missing ROC:** Always state it when computing Z-transforms
- **Unstable Poles:** Check $|p_k| < 1$ for ALL poles
- **DTFT vs Z-Transform:** Remember $z = e^{j\omega}$ connects them
- **Causality:** For causal systems, ROC is outside the outermost pole

### MATLAB Sanity Checks

Always verify analytical results:
```matlab
% Check frequency response matches
[H_matlab, w] = freqz(b, a, 512);
% Compare with your H(omega) formula

% Check impulse response
[h_matlab, n] = impz(b, a, 50);
% Compare with your h[n] formula
```

---

**End of Formula Sheet**

*Remember: The official Student Solutions PDFs (E19–F25) are your ground truth. Always cross-reference your work!*
