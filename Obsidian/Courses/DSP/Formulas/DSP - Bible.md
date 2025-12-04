# 📘 MATLAB DSP — Master Reference Sheet (Part 1)
**Course:** 62743 Digital Signal Processing (DTU)  
**Purpose:** Deep theoretical explanations + MATLAB code for every DSP concept used in the course.  
**Style:** Long-form theory + collapsible code blocks + exam-oriented examples.

---

## 📋 Table of Contents

1. [[#1. MATLAB Basics]]
    - [[#1.1 Workspace Management]]
    - [[#1.2 Vectors & Indexing]]
    - [[#1.3 Element-Wise Math]]
    - [[#1.4 Preallocation & Efficiency]]

2. [[#2. Signals & Sampling]]
    - [[#2.1 Discrete-Time Signals]]
    - [[#2.2 Sampling Theory]]
    - [[#2.3 Time Vectors & Sampling Period]]
    - [[#2.4 Constructing Common DSP Signals]]

3. [[#3. Plotting & Visualization]]
    - [[#3.1 plot() — continuous-like signals]]
    - [[#3.2 stem() — Discrete-time sequences]]
    - [[#3.3 stairs() — Zero-Order Hold (ZOH) visualization]]
    - [[#3.4 scatter() — Plotting discrete points]]
    - [[#3.5 subplot() & hold on]]
    - [[#3.6 Annotating Plots]]

4. [[#4. Frequency Domain Foundations]]
    - [[#4.1 DTFT (Theory + MATLAB Implementation)]]
    - [[#4.2 DFT / FFT — Relationship]]
    - [[#4.3 FFTSHIFT — Spectrum Centering]]
    - [[#4.4 Building the Frequency Axis Correctly]]
    - [[#4.5 FFT Amplitude Scaling]]

5. [[#5. Analog Filters]]
    - [[#5.1 Transfer Functions tf()]]
    - [[#5.2 Prototype Filters (Butterworth)]]
    - [[#5.3 Frequency Transformations (LP → HP/BP/BS)]]
    - [[#5.4 freqs() — Analog Frequency Response]]

6. [[#6. Digital Filters]]
    - [[#6.1 Digital Transfer Functions H(z)]]
    - [[#6.2 freqz() — Digital Frequency Response]]
    - [[#6.3 filter() — Apply an LTI system]]
    - [[#6.4 tf2zpk() and zplane()]]
    - [[#6.5 bilinear() — analog → digital transformation]]

7. [[#7. LTI Systems & Difference Equations]]
    - [[#7.1 Impulse Response]]
    - [[#7.2 Step Response]]
    - [[#7.3 Convolution]]

8. [[#8. Z-Transform Fundamentals]]
    - [[#8.1 What is the Z-transform?]]
    - [[#8.2 Basic Z-Transform Pairs (Must Know)]]
    - [[#8.3 Symbolic Z-transform in MATLAB]]
    - [[#8.4 Poles, Zeros, and H(z)]]
    - [[#8.5 Stability & Causality Conditions]]
    - [[#8.6 Inverse Z-transform (Methods)]]
    - [[#8.7 Frequency Response from H(z)]]
    - [[#8.8 Practical Z-transform Workflow (Exam-Ready)]]
    - [[#8.9 MATLAB Z-domain Toolbox Summary]]

9. [[#9. Region of Convergence (ROC)]]
    - [[#ROC: What It Actually Represents]]
    - [[#ROC Rules (Must Know for Exam)]]
    - [[#ROC Examples (DTU Exam Style)]]
    - [[#MATLAB Workflow for ROC Analysis]]
    - [[#Determining ROC Step-by-Step (Exam-Ready)]]
    - [[#ROC Visual Intuition]]

10. [[#10. Time-Domain ↔ Z-Domain Relationships]]
    - [[#10.1 Difference Equation ↔ Z-Transform]]
    - [[#10.2 Convolution ↔ Multiplication]]
    - [[#10.3 Impulse Response ↔ H(z)]]
    - [[#10.4 Poles ↔ Time-Domain Behavior]]
    - [[#10.5 Zeros ↔ Spectral Nulls]]
    - [[#10.6 Stability ↔ Impulse Response Convergence]]
    - [[#10.7 Frequency Response ↔ Z-domain Evaluation]]
    - [[#10.8 System Interpretation Cheat Sheet]]

11. [[#11. DFT and IDFT]]
    - [[#11.1 What the DFT Actually Does]]
    - [[#11.2 IDFT — Reconstructing the Time Signal]]
    - [[#11.3 FFT — the Fast Algorithm]]
    - [[#11.4 Frequency Axis Construction (Most Common Exam Error)]]
    - [[#11.5 FFT Output Interpretation]]
    - [[#11.6 Energy & Parseval’s Relation]]
    - [[#11.7 Windowing, Leakage & Resolution]]
    - [[#11.8 The Full FFT Workflow (DTU Exam Template)]]
    - [[#11.9 Manual DFT Calculation (DTU LOVES THIS)]]
    - [[#11.10 IDFT Derivation & Practical Use]]
    - [[#11.11 Circular Convolution Relationship]]

12. [[#12. Circular Convolution and Circular Shift]]
    - [[#12.1 Why Circular Convolution Exists]]
    - [[#12.2 Circular Convolution Definition]]
    - [[#12.3 Manual Circular Convolution (Exam Style)]]
    - [[#12.4 Circular vs Linear Convolution]]
    - [[#12.5 Circular Shift]]
    - [[#12.6 DFT Properties Involving Circular Shift]]
    - [[#12.7 Circular Convolution via FFT (Fast Method)]]
    - [[#12.8 Linear Convolution via FFT (Correct Method)]]
    - [[#12.9 Circular Convolution Interpretation Cheat Sheet]]
    - [[#12.10 MATLAB Toolbox Summary]]

13. [[#13. FFT Frameworks]]
    - [[#13.1 What the FFT Actually Computes]]
    - [[#13.2 Proper Frequency Axis — The DTU Standard]]
    - [[#13.3 Full 9-Step FFT Workflow (DTU Exam Template)]]
    - [[#13.4 Understanding FFT Peaks (Bin Location)]]
    - [[#13.5 Amplitude Scaling — Avoid the #1 Exam Error]]
    - [[#13.6 Leakage, Windowing, and Resolution]]
    - [[#13.7 FFT-Based Filtering (Fast Convolution)]]
    - [[#13.8 Extracting Phase Information]]
    - [[#13.9 FFT Toolbox Summary (Memory Section)]]

14. [[#14. Filter Design Workflows]]
    - [[#14.1 Overview of the Filter Design Pipeline]]
    - [[#14.2 Prewarping (Critical Step)]]
    - [[#14.3 Designing the Analog Low-Pass Prototype]]
    - [[#14.4 Frequency Transformations (LP → HP/BP/BS)]]
    - [[#14.5 Bilinear Transform (BLT)]]
    - [[#14.6 Digital Filter Validation]]
    - [[#14.7 Full End-to-End Design Template (Copy This for Exam)]]
    - [[#14.8 Filter Type Cheat Sheet]]
    - [[#14.9 Exam Strategy for Filter Design]]

15. [[#15. Difference Equations]]
    - [[#15.1 General Form]]
    - [[#15.2 Z-Transform Solution (Core Exam Skill)]]
    - [[#15.3 Impulse Response Solution]]
    - [[#15.4 Step Response]]
    - [[#15.5 Solving Difference Equations by Hand (Exam Workflow)]]
    - [[#15.6 FIR vs IIR from Difference Equation]]
    - [[#15.7 Convolution Interpretation]]
    - [[#15.8 Stability Verification via Difference Equation]]
    - [[#15.9 Solving Systems with MATLAB]]
    - [[#15.10 Difference Equation Cheat Sheet]]

16. [[#16. Advanced DSP Techniques]]
    - [[#16.1 Signal Energy and Power]]
    - [[#16.2 Parseval’s Theorem]]
    - [[#16.3 Multi-Tone Signals (Exam Classic)]]
    - [[#16.4 Modulation and Frequency Shifting]]
    - [[#16.5 Windowing & Leakage Control]]
    - [[#16.6 DTFT via freqz (The Hidden Trick)]]
    - [[#16.7 Magnitude & Phase Interpretation (Advanced)]]
    - [[#16.8 Real vs Complex Signals]]
    - [[#16.9 Analytic Signals & Hilbert Transform (Optional but Powerful)]]
    - [[#16.10 Spectral Power Density Estimates (Welch’s Method)]]
    - [[#16.11 Advanced DSP Cheat Sheet]]

17. [[#17. Quick Reference Tables]]
    - [[#17.1 Time-Domain ↔ Frequency-Domain]]
    - [[#17.2 FFT Essentials]]
    - [[#17.3 Z-Transform & System Analysis]]
    - [[#17.4 Filter Design Pipeline]]
    - [[#17.5 Analog Filter Transformations]]
    - [[#17.6 Circular Convolution Tools]]
    - [[#17.7 Difference Equation Toolbox]]
    - [[#17.8 Windowing Cheat Sheet]]
    - [[#17.9 Signal Energy & Power]]
    - [[#17.10 Most Important MATLAB Commands (DSP Master List)]]

18. [[#18. Spectrum Sketching & Visualization]]
       - [[#18.1 Why Spectrum Sketching Matters]]
       - [[#18.2 Installation & Setup]]
       - ... (etc)

# 1. MATLAB Basics

This section builds the **MATLAB muscle memory** you will use in every single DSP exercise and exam scenario.

In 62743 DSP, _every script_ you write follows the same structure:

1. **Clean environment** (fresh workspace, clean figures)
2. **Define sampling setup** ($F_s$, $T_s$, $N$)
3. **Build index vectors** ($n$, $t$)
4. **Construct signals** ($x[n]$, impulses, steps, test tones)
5. **Process signals** (filtering, convolution, FFT, z-domain tools)
6. **Visualize results** (time plots, spectra, pole-zero diagrams)

This section gives you all the "MATLAB fundamentals" that support the rest of the DSP workflows.

---

## 1.1 Workspace Management

MATLAB keeps variables alive between runs — a dangerous trap during DSP work.

Leftover variables cause:

- wrong vector sizes
- mismatched FFT lengths
- incorrect frequency axis
- confusing plots that look "correct" but actually use old data 😭

So every DSP script **must** begin with a clean environment.

### Clean MATLAB Script Start (Exam Template)

> [!example]- Click to view code
> 
> ```matlab
> clear all      % remove all variables from workspace
> close all      % close all open figure windows
> clc            % clear the command window
> 
> format long    % helpful for debugging filter coeffs / poles
> % format short % switch back if you want a cleaner display
> ```

### Extra Tips (Exam-Proof)

- **Never** put `clear` inside loops.
- If MATLAB behaves strangely → **rerun the whole script**, not individual lines.
- `format long` makes numerical comparisons MUCH clearer (important for filter designs + root magnitudes).

---

## 1.2 Vectors & Indexing

DSP = vector manipulation.

Everything you do — time, frequency, signals, FIR kernels, index sets — comes from well-constructed vectors.

### Core Vector Patterns (Must Know)

**Index vector:**
```matlab
 n = 0:N-1;
```

**Symmetric index:**
 ```matlab
 n = -N:N;
 ```

**Even spacing:**
 ```matlab
 v = linspace(start, stop, N);
 ```

### Basic Vector Ops & Logical Indexing

> [!example]- Click to view code
> 
> ```matlab
> n = 0:20;          % sample index vector
> x = n.^2;          % x[n] = n^2 element-wise
> pos = (x >= 0);    % logical mask (1 where condition true)
> spike = (n == 3);  % impulse-like indicator at n=3
> 
> % Extract part of a sequence
> x_sub = x(n >= 10);   % keep samples with n >= 10
> ```

### Why This Matters in DSP

- **Impulses:** `(n == 0)`
- **Steps:** `(n >= 0)`
- **Rectangular windows:** `(n >= n1 & n <= n2)`
- **Piecewise signals:** use masks
- **DFT bin selection:** logical masks on f

Vector logic is DSP signal construction.

---

## 1.3 Element-Wise Math

MATLAB has two worlds:

| World           | Operator         | Meaning                   |
| --------------- | ---------------- | ------------------------- |
| Matrix algebra  | `*`, `/`, `^`    | Linear algebra operations |
| DSP signal math | `.*`, `./`, `.^` | Element-wise operations   |

In DSP, you almost always want **element-wise operations**.

If you forget the dot, MATLAB will try matrix math — and absolutely ruin your day.

### MUST-Use Cases

- **Sinusoids:** `cos(2*pi*f0*n*Ts)`
- **Exponentials:** `a.^n`
- **Modulation:** `x .* w`
- **Windowing:** `x .* hann(N).'`

### Element-wise vs Matrix Math

> [!example]- Click to view code
> 
> ```matlab
> n = 0:10;
> a = 2*n;          % row vector
> b = 3*n + 1;      % row vector
> 
> y1 = a .* b;      % correct DSP multiplication
> % y2 = a * b;     % WRONG: matrix multiply -> dimension error
> 
> c = n.^2;         % element-wise power
> d = n./(n+1);     % element-wise division
> ```

**If you see size mismatch errors → 99% chance you forgot the dot.**

---

## 1.4 Preallocation & Efficiency

Signals in DSP often use large lengths:

- Powers of 2: $N = 2^{10}, 2^{12}, 2^{14}$
- Long sequences for filtering / convolution
- Long time vectors for FFT resolution

If you build vectors inside loops without preallocating, MATLAB repeatedly resizes memory → painfully slow.

### Good Pattern
 ```matlab
 N = 5000;
 x = zeros(1, N);     % allocate memory once
 for n = 1:N
     x(n) = sin(2*pi*0.01*n);
 end
 ```

### Bad Pattern (Never Use)
 ```matlab
 x = [];
 for n = 1:N
     x(n) = sin(2*pi*0.01*n);   % slow & unsafe
 end
 ```

**Preallocation = speed + cleaner debugging + fewer mistakes.**

---
# 2. Signals & Sampling
Digital Signal Processing begins with one fundamental step:

👉 **Taking a continuous-time signal $x(t)$ and turning it into a discrete-time sequence $x[n]$**  
where  
$$x[n] = x(nT_s)$$  
and $T_s = 1/F_s$ is the sampling period.

This section builds the foundation for everything that follows: FFTs, filtering, reconstruction, aliasing, and frequency-domain interpretation.

---

## 2.1 Discrete-Time Signals
A **discrete-time (DT) signal** is simply a sequence of numbers indexed by an integer $n$.

Common definitions:

- **Continuous time:** variable $t$ (real number)
- **Discrete time:** index $n$ (integer)
- **Sampling relation:**  
  $$x[n] = x(nT_s)$$
- **Time vector:**  
  $$t_n = nT_s$$

### Why this matters
Every FFT, every filter, every plot in this course is based on constructing vectors correctly:

- $n$ is used for **discrete math** (stem plots, sequences, convolution)
- $t$ is used for *continuous-looking* plots (plot() commands)
- Filtering & transforms always take **discrete sequences** as input

> [!example]- Making a discrete-time cosine (standard DSP pattern)
> ```matlab
> Fs = 100;              % sampling frequency
> Ts = 1/Fs;             % sampling period
> N = 1000;             
>
> n = 0:N-1;             % discrete-time index vector
> x = 4*cos(2*pi*10*n*Ts);
>
> figure
> stem(n, x, 'filled')
> title('Discrete-Time Cosine, f_0 = 10 Hz')
> ```

---

## 2.2 Sampling Theory
Sampling is the process of observing $x(t)$ at discrete instants $nT_s$.

### Shannon–Nyquist Sampling Theorem
To recover a continuous-time signal from its samples, the sampling frequency must satisfy:
$$F_s > 2 f_{\max}$$

Where $f_{\max}$ is the highest frequency present in $x(t)$.

### Aliasing
If the sampling condition is violated:
- High-frequency components **fold back** into lower frequencies  
- The sampled signal **cannot** be reconstructed  
- In FFT, the peaks appear at the wrong frequencies

### Practical MATLAB guidance
- For clean visual demonstrations, choose $F_s$ at least **5× above** the max signal frequency  
- For FFT analysis, pick $N$ as a power of two for faster computation

> [!example]- Aliasing demonstration setup
> ```matlab
> Fs = 200;       % try lowering this to 60 or 40 to observe aliasing
> Ts = 1/Fs;
> N = 1000;
>
> n = 0:N-1;
> f0 = 120;       % higher than Fs/2 → aliasing happens
>
> x = cos(2*pi*f0*n*Ts);
> stem(n(1:50), x(1:50))
> title('Aliased Discrete-Time Signal')
> ```

---

## 2.3 Time Vectors & Sampling Period  
In MATLAB, you will often create both:

### 1. **Discrete index vector** (for stem plots)

$n = 0:N-1$
### 2. **Time vector** (for continuous-looking plots)
$t = n * Ts$

These two representations are crucial:

- Use **plot(t, x)** for smooth curves  
- Use **stem(n, x)** for theoretical DT signals  

You will switch between these constantly in DSP.

> [!example]- G enerating both domains
> ```matlab
> Fs = 200;
> Ts = 1/Fs;
> N = 1000;
>
> n = 0:N-1;       % discrete time index
> t = n*Ts;        % corresponding time instants
>
> x = sin(2*pi*30*t);
>
> subplot(2,1,1)
> plot(t, x)
> title('Continuous-Time Style Plot')
>
> subplot(2,1,2)
> stem(n(1:50), x(1:50))
> title('Discrete-Time Sequence Representation')
> ```

---

## 2.4 Constructing Common DSP Signals
Many exam questions begin with:  
*“Construct the signal …”* or *“Plot the sequence …”*

Here are the must-know building blocks.

---

### Unit Impulse $\delta[n]$  
Defined as:
$$
\delta[n] = \begin{cases}
1, & n = 0 \\
0, & n \neq 0
\end{cases}
$$

> [!example]- δ[n]
> ```matlab
> n = -10:10;
> d = (n == 0);     % logical impulse
>
> stem(n, d, 'filled')
> title('Unit Impulse \delta[n]')
> ```

---

### Unit Step $u[n]$  
Defined as:
$$
u[n] = \begin{cases}
1, & n \ge 0 \\
0, & n < 0
\end{cases}
$$

> [!example]- u[n]
> ```matlab
> u = (n >= 0);
> ```

---

### Exponential $a^n u[n]$
Right-sided exponential:
$$
x[n] = a^n u[n]
$$

Used heavily in:
- stability analysis  
- z-transform computations  
- difference equation solutions  

> [!example]- aⁿu[n]
> ```matlab
> a = 0.9;
> x = (a.^n) .* (n >= 0);
> ```

---

### Sinusoid $A\cos(2\pi f_0 nT_s)$

> [!example]- DT sinusoid
> ```matlab
> Fs = 500;
> f0 = 50;
> x = cos(2*pi*f0*n/Fs);
> ```

### IMPORTANT  
A discrete-time sinusoid’s **digital angular frequency** is:
$$
\omega_0 = \frac{2\pi f_0}{F_s}
$$

This angle determines:
- periodicity  
- sampling artifacts  
- aliasing properties  

---

# 3. Plotting & Visualization
In DSP, visualisation is EVERYTHING — because signals, spectra, frequency responses, and poles/zeros all carry essential information that would be impossible to interpret from raw numbers alone.

This section teaches you:

- **Which plot type to use for each signal class**  
- How to graph discrete vs continuous-time signals correctly  
- How to annotate plots with important values  
- How to create readable, exam-friendly visualizations  
- MATLAB functions that appear constantly in exercises, weekly assignments, and the exam  

---

## 3.1 plot() — continuous-like signals
`plot()` is used for signals that you want to **appear smooth**.  
This is commonly used for:

- Sampled continuous-time signals (dense $t$ vector)
- Analog waveforms
- FFT magnitude/phase spectra
- Frequency responses
- Envelope curves

### When NOT to use plot()
- For discrete-time sequences (use `stem()`)
- For frequency bin plots (use `stem()` or `plot()` depending on desired look)

### Theory
If you choose $N$ samples and sampling frequency $F_s$, the time vector is:
$$t = n T_s = \frac{n}{F_s}.$$

The finer the time resolution (larger $F_s$ or smaller step size), the smoother the plot.

> [!example]- Smooth continuous-time style plot
> ```matlab
> t = 0:0.0001:0.1;         % very fine resolution
> x = 2*sin(2*pi*50*t);     % 50 Hz sine wave
>
> figure
> plot(t, x, 'LineWidth', 2)
> xlabel('t (s)')
> ylabel('x(t)')
> title('50 Hz Sine Wave')
> grid on
> ```

---

## 3.2 stem() — Discrete-time sequences
A discrete-time signal $x[n]$ should **always** be plotted using `stem()`, because it visually encodes:

- The sample index $n$
- The fact that the signal is not continuous
- The concept of impulse/sequences used in LTI analysis

Perfect for:

- $x[n], h[n], y[n]$  
- Outputs of difference equations  
- Impulse & step responses  
- DFT/FFT magnitudes per bin  
- Piecewise-defined sequences  

> [!example]- Typical DSP DT signal plot
> ```matlab
> n = 0:30;
> x = cos(0.2*pi*n);
>
> figure
> stem(n, x, 'filled', 'LineWidth', 1.5)
> xlabel('n'); ylabel('x[n]')
> title('Discrete-Time Cosine: x[n] = cos(0.2\pi n)')
> grid on
> ```

---

## 3.3 stairs() — Zero-Order Hold (ZOH) visualization
The `stairs()` function shows samples held constant between sampling instants — just like a DAC with zero-order hold.

Use this to illustrate:

- Sample-and-hold reconstruction  
- Piecewise-constant approximations  
- Quantized steps  

> [!example]- Zero-order hold style
> ```matlab
> n = 0:20;
> x = sin(0.3*pi*n);
>
> stairs(n, x, 'LineWidth', 1.5)
> title('Zero-Order Hold Visualization')
> grid on
> ```

---

## 3.4 scatter() — Plotting discrete points
`scatter()` is useful when you want discrete points **without stems**.  
This is often seen in:

- Evaluating FFT peak values  
- Highlighting roots/poles on custom plots  
- Visualizing sample positions  

> [!example]- Scatter demo
> ```matlab
> t = 0:0.01:1;
> y = sin(2*pi*5*t);
>
> scatter(t, y, 'filled')
> title('Scatter Plot of 5 Hz Sine Samples')
> ```

---

## 3.5 subplot() & hold on
### subplot()
Lets you create **multiple figures in one window** — extremely useful in examinations where you want:

- Time-domain and frequency-domain in one figure  
- Magnitude and phase in one figure  
- Input vs output comparison  
- Discrete vs continuous visualization  

### hold on
Lets you **overlay multiple plots** on top of each other.

> [!example]- Multi-view visualization
> ```matlab
> t = 0:0.001:1;
> x1 = sin(2*pi*5*t);
> x2 = cos(2*pi*5*t);
>
> figure
> subplot(2,2,1)
> plot(t, x1); hold on; plot(t, x2)
> title('plot() overlay')
>
> subplot(2,2,2)
> stem(t(1:50), x1(1:50))
> title('stem()')
>
> subplot(2,2,3)
> stairs(t(1:50), x1(1:50))
> title('stairs()')
>
> subplot(2,2,4)
> scatter(t(1:50), x1(1:50))
> title('scatter()')
> ```

---

## 3.6 Annotating Plots
Annotations let you **mark important values** or **show exact coordinate positions**.

In DSP, annotation is especially useful for:

- Marking cutoff frequencies  
- Indicating Nyquist frequency  
- Highlighting FFT peaks  
- Labeling poles/zeros  
- Showing maxima/minima  

---

### xline() and yline()
Vertical/horizontal reference lines.

> [!example]- Marking a sampling frequency
> ```matlab
> xline(50, 'r--', 'LineWidth', 2);  % Mark f = 50 Hz
> yline(0.75, 'b--', 'LineWidth', 2);
> ```

---

### text() — manual labels

> [!example]- Labeling points
> ```matlab
> text(0.02, 0.5, '(0.02, 0.5)', 'FontSize', 14)
> ```

---

### dsearchn() — find nearest point  
This is **insanely powerful** for finding the closest FFT bin or time sample to a chosen value.

> [!example]- FFT peak detection
> ```matlab
> idx = dsearchn(f.', 120);         % closest index to f = 120 Hz
> f_peak = f(idx);
> X_peak = magX(idx);
>
> hold on
> plot(f_peak, X_peak, 'ro', 'MarkerSize', 10)
> text(f_peak, X_peak, sprintf('Peak @ %.1f Hz', f_peak))
> ```

---

# 4. Frequency Domain Foundations
The frequency domain is where **DSP becomes powerful**.

Most of the DSP exam revolves around:

- DTFT: the “true” frequency transform  
- DFT & FFT: sampled, discrete frequency analysis  
- Frequency response of LTI systems  
- Magnitude & phase plots  
- Understanding aliasing and periodicity  
- Interpreting spectra and filter behavior  

This section builds the foundation for **all spectral analysis**, filtering, and system characterization.

---

## 4.1 DTFT (Theory + MATLAB Implementation)
The **Discrete-Time Fourier Transform (DTFT)** is defined as:

$$
X(\omega) = \sum_{n=-\infty}^{\infty} x[n] e^{-j \omega n}
$$

Key characteristics:

- $\omega$ is **continuous** (analogous to $2\pi f$)
- Periodic with period $2\pi$
- Produces a **continuous spectrum**
- Not computable by FFT directly unless approximated

### When to use DTFT?
- Theoretical analysis  
- Proving properties (modulation, shifting, convolution)  
- Analysing ideal filters (rectangular low-pass, etc.)  
- Understanding $H(e^{j\omega})$ for LTI systems  

### MATLAB DTFT approximation  
MATLAB uses `freqz()` to compute the DTFT efficiently:

- `freqz(x,1,…)` → DTFT of $x[n]$  
- `freqz(b,a,…)` → frequency response $H(e^{j\omega})$  

> [!example]- DTFT approximation with freqz()
> ```matlab
> x = [1 2 3 2 1];
> [X, w] = freqz(x, 1, 2048, 'whole');    % 0 → 2π
>
> figure
> plot(w/pi, abs(X), 'LineWidth', 1.5)
> xlabel('\omega / \pi')
> ylabel('|X(e^{j\omega})|')
> title('DTFT Magnitude via freqz()')
> grid on
> ```

---

## 4.2 DFT / FFT — Relationship
The **DFT** samples the DTFT at $N$ equally spaced frequencies:

$$
X[k] = X(e^{j\omega})\Big|_{\omega = 2\pi k/N}, \quad k = 0,\dots,N-1
$$

Meaning:

- DTFT → continuous, infinite  
- DFT → *sampled*, finite  

FFT is simply a **fast algorithm** to compute the DFT.

### Interpretation  
- More samples $N$ → higher frequency resolution  
- Higher $F_s$ → wider frequency range  
- DFT is ALWAYS periodic with period $N$

> [!example]- Manual DFT vs FFT
> ```matlab
> x = [1 2 3 4].';
> N = length(x);
> n = 0:N-1;
> k = n.';
>
> % Manual DFT matrix
> W = exp(-1i*2*pi*(k*n)/N);
> X_dft = W*x;
>
> % FFT result
> X_fft = fft(x);
> ```

---

## 4.3 FFTSHIFT — Spectrum Centering
By default, MATLAB’s FFT output is “wrapped”:

- DC component at index 1  
- Positive frequencies  
- Then negative frequencies  

But humans think in centered spectra:

$$
[-F_s/2, \dots, 0, \dots, F_s/2]
$$

### fftshift() moves negative frequencies to the left

> [!example]- Centering the spectrum
> ```matlab
> X = fft(x);         % unshifted (wrapped)
> Xc = fftshift(X);   % centered (zero at middle)
> ```

This is **mandatory** for frequency plotting.

---

## 4.4 Building the Frequency Axis Correctly
This is the #1 place students make mistakes.

Given:

- $F_s$ sampling frequency  
- $N$ FFT size  

Then:

$$
\Delta f = \frac{F_s}{N}
$$

Frequency vector:

$$
f_k = -\frac{F_s}{2} : \Delta f : \frac{F_s}{2} - \Delta f
$$

> [!example]- Correct frequency axis (always use this)
> ```matlab
> df = Fs/N;
> f = -Fs/2 : df : Fs/2 - df;
> ```

### Why is the last value $F_s/2 - \Delta f$?
Because MATLAB vectors must match the FFT length exactly:  
`length(f) = N`

---

## 4.5 FFT Amplitude Scaling
The raw FFT is unscaled:

$$|X[k]| \propto N$$

You **must scale** for correct magnitude:

$$
|X[k]|_\text{scaled} = \frac{|X[k]|}{N}
$$

This ensures:

- A 4 V amplitude cosine gives a 2 V spike  
- Total energy is preserved  
- Parseval’s relation holds  

> [!example]- Proper FFT magnitude scaling
> ```matlab
> X = fftshift(fft(x));
> magX = abs(X)/N;
> ```

### Common Mistakes
❌ forgetting `/N`  
❌ mixing up one-sided and two-sided spectra  
❌ forgetting `fftshift()`  
✔️ Always use the standard 9-step FFT framework (Section 13)

---
# 5. Analog Filters
Analog filters form the *starting point* for digital filter design in this course.  
Almost every digital filter in the exam comes from:

1. A **prototype analog filter**  
2. A **frequency transformation** (LP→HP/BP/BS)  
3. **Bilinear transform (BLT)** into the $z$-domain  

This section builds the intuition and tools required to transform, analyze, and visualize analog filters before converting them.

---

## 5.1 Transfer Functions tf()
In analog filter theory, the system is described by:

$$
H(s) = \frac{B(s)}{A(s)}
     = \frac{b_0 s^M + b_1 s^{M-1} + \dots + b_M}{a_0 s^N + a_1 s^{N-1} + \dots + a_N}
$$

The $s$-domain represents continuous-time behavior.  
MATLAB uses `tf()` to create such systems.

### Why do we need $H(s)$ in DSP?
Before we design a digital filter with frequency specifications (passband, stopband), we:

- define an **analog prototype**  
- scale or warp it to match cutoff frequencies  
- convert into digital form using BLT  

> [!example]- Analog transfer function
> ```matlab
> num = [2 5 7];                 % numerator coefficients
> den = [6 8 3];                 % denominator coefficients
>
> Hs = tf(num, den);             % analog filter H(s)
> ```

---

## 5.2 Prototype Filters (Butterworth)
The **Butterworth prototype** is emphasized at DTU because:

- It’s maximally flat in the passband  
- Has monotonic magnitude response  
- Has simple pole placement on a semicircle  

### Analog low-pass prototype

$$
|H(j\Omega)|^2 = \frac{1}{1 + \left( \frac{\Omega}{\Omega_c} \right)^{2n}}
$$

Characteristics:

- $n$ = filter order  
- $\Omega_c$ = -3 dB cutoff  
- Poles uniformly distributed on a semicircle  

### Choosing the order  
Given specs:

- passband attenuation $A_p$  
- stopband attenuation $A_s$  
- passband frequency $\Omega_p$  
- stopband frequency $\Omega_s$

Order $n$ satisfies:

$$
n \ge \frac{
\log_{10}(10^{A_s/10} - 1) - \log_{10}(10^{A_p/10} - 1)
}{
2\log_{10}(\Omega_s/\Omega_p)
}
$$

DTU expects you to *compute this manually* in the exam.

---

## 5.3 Frequency Transformations (LP → HP/BP/BS)
We use prototype filters because ANY analog filter can be built from a low-pass core:

### LP → LP  
$$
s \longrightarrow \frac{s}{\Omega_c}
$$

### LP → HP
$$
s \longrightarrow \frac{\Omega_c}{s}
$$

### LP → BP  
$$
s \longrightarrow \frac{s^2 + \Omega_0^2}{B s}
$$

### LP → BS  
$$
s \longrightarrow \frac{B s}{s^2 + \Omega_0^2}
$$

MATLAB implementations:

> [!example]- LP to HP / BP / BS
> ```matlab
> [b_hp, a_hp] = lp2hp(b_lp, a_lp, Omegac);
> [b_bp, a_bp] = lp2bp(b_lp, a_lp, Omega0, B);
> [b_bs, a_bs] = lp2bs(b_lp, a_lp, Omega0, B);
> ```

---

## 5.4 freqs() — Analog Frequency Response
The analog frequency response:

$$H(j\Omega) = H(s)\big|_{s=j\Omega}$$

> [!example]- Plot analog frequency response
> ```matlab
> Omega = linspace(0, 2000, 5000);
> H = freqs(num, den, Omega);
>
> figure
> plot(Omega, abs(H), 'LineWidth', 1.5)
> xlabel('\Omega (rad/s)')
> ylabel('|H(j\Omega)|')
> grid on
> ```

This is used to:

- Inspect analog prototypes  
- Verify cutoff frequencies  
- Compare analog vs digital frequency responses  

---

# 6. Digital Filters
Digital filters operate directly on **samples** $x[n]$ and are represented by:

$$
H(z) = \frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}
          {1 + a_1 z^{-1} + \dots + a_N z^{-N}}
$$

MATLAB interacts with digital filters via:

- `tf()` (H(z) structural representation)  
- `freqz()` (frequency response analysis)  
- `filter()` (apply LTI system)  
- `impz()`, `stepz()` (responses)  
- `zplane()` (poles/zeros)

---

## 6.1 Digital Transfer Functions H(z)
Create a digital filter with:

> [!example]- Digital tf()
> ```matlab
> b = [0.3 0.3];
> a = [1 -0.4];
>
> Fs = 1000;
> Hd = tf(b, a, 1/Fs, 'variable', 'z^-1');
> ```

### Why the `'z^-1'`?
Because the course uses:

$$H(z) = b_0 + b_1 z^{-1} + \dots$$

Matching the mathematical form avoids confusion in poles/zeros and ROC.

---

## 6.2 freqz() — Digital Frequency Response
Compute:

- Magnitude response $|H(e^{j\omega})|$  
- Phase response $\angle H(e^{j\omega})$  

Over $[0, F_s/2]$ or $[-F_s/2, F_s/2]$ depending on your plot.

> [!example]- freqz()
> ```matlab
> Nfft = 4096;
> [H, f] = freqz(b, a, Nfft, Fs);
>
> figure
> subplot(2,1,1)
> plot(f, abs(H))
> title('Magnitude Response')
>
> subplot(2,1,2)
> plot(f, angle(H))
> title('Phase Response')
> ```

---

## 6.3 filter() — Apply an LTI system
The difference equation:

$$
y[n] = \sum_{k=0}^{M} b_k x[n-k]
     - \sum_{k=1}^{N} a_k y[n-k]
$$

MATLAB applies this:

> [!example]- filter()
> ```matlab
> y = filter(b, a, x);
> ```

This simulates:

- IIR/FIR filters  
- System response to arbitrary input  
- Difference equation outputs  

---

## 6.4 tf2zpk() and zplane()
For any system:

- **Zeros** = roots of numerator  
- **Poles** = roots of denominator  
- Stability: all poles inside unit circle  

> [!example]- poles and zeros
> ```matlab
> [z, p, k] = tf2zpk(b, a);
>
> figure
> zplane(b, a)
> title('Pole-Zero Plot')
> ```

Interpretation:

- Poles close to unit circle → long memory, narrow filters  
- Zeros near unit circle → deep notches  
- Zeros/poles at $z = -1$ → high-pass behavior  
- Zeros at $z = 1$ → DC cancelation  

---

## 6.5 bilinear() — analog → digital transformation
The bilinear transform (BLT) maps the $s$-plane onto the $z$-plane:

$$
s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}}
$$

This transformation:

- Avoids aliasing  
- Maps stable analog filters to stable digital filters  
- Warps frequencies (requiring prewarping)  

### Prewarping  
Given analog critical frequency $\Omega_c$:

$$
\omega_c = 2 \tan^{-1}\left(\frac{\Omega_c T_s}{2}\right)
$$

> [!example]- bilinear()
> ```matlab
> [bz, az] = bilinear(b_analog, a_analog, Fs);
> ```

---

# 7. LTI Systems & Difference Equations
Every linear time-invariant (LTI) discrete-time system is described by:

### 1. Impulse response $h[n]$  
### 2. System function $H(z)$  
### 3. Difference equation  
### 4. Convolution  
### 5. Frequency response  

MATLAB supports all viewpoints.

---

## 7.1 Impulse Response
The impulse response completely characterizes the LTI system:

$$
h[n] = \mathcal{Z}^{-1}\{H(z)\}
$$

MATLAB:

> [!example]- impz()
> ```matlab
> [h, n] = impz(b, a, 40);
> stem(n, h, 'filled')
> title('Impulse Response h[n]')
> ```

Interpretation:

- FIR → finite length $h[n]$  
- IIR → infinite length (decays over time)  
- Resonant peaks correspond to poles near unit circle  

---

## 7.2 Step Response
The step response is cumulative:

$$
s[n] = \sum_{k=0}^{n} h[k]
$$

Useful for:

- Stability visualization  
- System settling behavior  
- Detecting oscillatory or exponential responses  

> [!example]- Step response
> ```matlab
> u = ones(1,100);
> y = filter(b,a,u);
>
> plot(y)
> title('Step Response')
> ```

---

## 7.3 Convolution
For input $x[n]$ and impulse response $h[n]$:

$$
y[n] = (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k]h[n-k]
$$

MATLAB:

> [!example]- Convolution
> ```matlab
> y = conv(x, h);
>
> figure
> stem(y)
> title('Linear Convolution Output')
> ```

### When convolution matters
- Solving difference equations manually  
- Understanding LTI system mechanics  
- Designing FIR filters via convolution kernels  
- Relating time-domain filtering ↔ multiplication in frequency domain

---
# 8. Z-Transform Fundamentals

The **z-transform** is one of the most important mathematical tools in DSP.  
It unifies:

- difference equations  
- impulse responses  
- frequency response  
- poles and zeros  
- causality  
- stability  
- convolution  

Every serious LTI analysis problem is secretly a z-transform problem.

---

## 8.1 What is the Z-transform?

For a discrete-time sequence \( x[n] \):

$$
X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}
$$

### Key ideas
- The variable \( z = re^{j\omega} \) is **complex** (magnitude + angle)
- Time shift → multiplication by \( z^{-1} \)
- Convergence depends on \( |z| \) → the **Region of Convergence (ROC)**
- Frequency response comes from evaluating on the **unit circle**:

$$
H(e^{j\omega}) = H(z)\big|_{z=e^{j\omega}}
$$

### Analogy  
The z-transform is the **discrete-time version** of the Laplace transform.

---

Here's the reformatted table using `$` for inline math:

## 8.2 Basic Z-Transform Pairs (Must Know)

These appear constantly in exams and weekly exercises:

|Time Signal $x[n]$|Z-transform $X(z)$|ROC Condition|
|---|---|---|
|$\delta[n]$|$1$|entire $z$-plane|
|$u[n]$|$\frac{1}{1 - z^{-1}}$|$\|z\| > 1$|
|$a^n u[n]$|$\frac{1}{1 - a z^{-1}}$|$\|z\| > \|a\|$|
|$-a^n u[-n-1]$|$\frac{1}{1 - a z^{-1}}$|$\|z\| < \|a\|$|
|$n, a^n u[n]$|$\frac{z^{-1}}{(1 - a z^{-1})^2}$|$\|z\| > \|a\|$|
|$u[n-N]$|$\frac{z^{-N}}{1 - z^{-1}}$|$\|z\| > 1$|
### Important  
Two signals with the **same algebraic expression** for \(X(z)\) may represent **different time-domain signals** depending on their ROC.

---

## 8.3 Symbolic Z-transform in MATLAB

> [!example]- Using `ztrans()`  
> ```matlab
> syms n z a
> x = a^n * (n >= 0);
> X = ztrans(x, n, z)
> ```

---

## 8.4 Poles, Zeros, and H(z)

Given a rational z-transform:

$$
H(z) = \frac{B(z)}{A(z)}
$$

- **Poles** → roots of \(A(z)\)  
- **Zeros** → roots of \(B(z)\)  
- Behavior of the impulse response is determined by pole locations  
- Stability depends on pole magnitudes  
- Causality depends on ROC location  

---

## 8.5 Stability & Causality Conditions

### Stability
A system is stable if:

- the unit circle lies inside the ROC  
- all poles satisfy:  
  $$
  |p_k| < 1
  $$

### Causality
A system is causal if:

- ROC lies **outside** the outermost pole  
  $$
  |z| > \max |p_k|
  $$

---

## 8.6 Inverse Z-transform (Methods)

### Method 1 — Partial Fractions  
Most common:

$$
X(z) = \sum_k \frac{A_k}{1 - p_k z^{-1}}
$$

Each term corresponds to:

- \( A_k p_k^n u[n] \)

> [!example]- residue()  
> ```matlab
> [r, p, k] = residue(num, den);
> ```

---

### Method 2 — Power Series Expansion  
Expand:

$$
X(z) = \sum_n x[n] z^{-n}
$$

Useful for non-rational functions.

---

### Method 3 — Symbolic  
> [!example]- iztrans()  
> ```matlab
> syms z
> X = z/(z - 0.5);
> x = iztrans(X, z)
> ```

---

## 8.7 Frequency Response from H(z)

Evaluate on the unit circle:

$$
H(e^{j\omega}) = H(z)\big|_{z=e^{j\omega}}
$$

> [!example]- freqz()  
> ```matlab
> [H,w] = freqz(b, a, 4096);
> plot(w/pi, abs(H))
> ```

This is the **DTFT of the impulse response** \(h[n]\).

---

## 8.8 Practical Z-transform Workflow (Exam-Ready)

Given a difference equation:

### Step-by-step
1. **Z-transform both sides**  
2. Solve for  
   $$
   H(z) = \frac{Y(z)}{X(z)}
   $$
3. **Find poles/zeros**  
4. **Check ROC** (causal? stable?)  
5. **Inverse Z-transform** via partial fractions  
6. **Plot h[n]** using `impz()`  
7. **Plot frequency response** via `freqz()`  

---

## 8.9 MATLAB Z-domain Toolbox Summary

> [!example]- Z-domain essentials  
> ```matlab
> tf(b, a, 1/Fs, 'variable','z^-1')  % digital transfer function
> zplane(b, a)                       % poles & zeros
> [z,p,k] = tf2zpk(b, a)             % factorization
> [h,n] = impz(b, a, 40)             % impulse response
> [H,w] = freqz(b, a, 4096)          % frequency response
> [r,p,k] = residue(b, a)            % partial fraction expansion
> syms z; iztrans(X,z)               % symbolic inverse Z-transform
> ```

---

# 9. Region of Convergence (ROC)

The **Region of Convergence (ROC)** is one of the most important — and most misunderstood — concepts in the z-transform chapter.  
It determines:

- **whether a given $X(z)$ corresponds to a causal or anti-causal sequence**  
- **whether the system is stable or unstable**  
- **the shape of the time-domain signal**  
- **which inverse Z-transform expression is correct**

Two different signals can have **the same** algebraic Z-transform expression but **different** ROCs → therefore different time-domain signals.

This section exists to make ROC intuitive and exam-proof.

---

## ROC: What It Actually Represents
Given

$$
X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}
$$

the sum converges only for values of $z$ where:

- the powers $z^{-n}$ don't blow up  
- the amplitude of $x[n]$ decays sufficiently fast  
- the infinite series is absolutely summable  

**The ROC is the set of $z$ values where the infinite sum converges.**

### Geometry  
If:

- $z = re^{j\omega}$  

Then ROC is a set of radii $r$ where convergence happens.

This means:

👉 **The ROC is always a ring (annulus) in the complex plane.**  
Could be:

- outside a circle  
- inside a circle  
- between two circles  
- whole plane except poles  

---

## ROC Rules (Must Know for Exam)

### 1. **ROC is always a ring** in the $z$-plane  
Because it's defined by $|z|$ conditions.

---

### 2. **ROC never contains poles**  
Poles are singularities where $X(z)$ blows up.

---

### 3. **Right-sided sequences** (causal)

If  
$$x[n] = 0 \text{ for } n < n_0,$$

then ROC is:

$$|z| > \text{largest pole magnitude}$$

Causal systems always have **outer ROC**.

---

### 4. **Left-sided sequences** (anti-causal)

ROC is:

$$|z| < \text{smallest pole magnitude}$$

---

### 5. **Two-sided sequences**

If a signal has both $n<0$ and $n>0$ components, ROC is a **ring between poles**:

$$r_1 < |z| < r_2.$$

---

### 6. **Stability condition**

A system is stable if and only if:

$$\sum_{n=-\infty}^\infty |h[n]| < \infty$$  

Equivalent to:

👉 **ROC must include the unit circle**  
$$|z| = 1.$$

---

### 7. **Causal + stable ⇒ all poles inside unit circle**

This is the standard IIR stability condition:

$$|p_k| < 1 \quad \forall k$$

---

## ROC Examples (DTU Exam Style)

### **Example 1 — $a^n u[n]$**

Signal:

$$x[n] = a^n u[n]$$

Z-transform:

$$X(z) = \frac{1}{1 - a z^{-1}}$$

Pole at $z = a$  
Right-sided → ROC:

$$|z| > |a|$$

✔ causal  
✔ stable if $|a| < 1$

---

### **Example 2 — $-a^n u[-n-1]$**

Left-sided exponential.

ROC:

$$|z| < |a|$$

Same transform, different ROC ⇒ **different time-domain sequence**.

---

### **Example 3 — Two-sided exponential**

Suppose:

$$
x[n] = 
\begin{cases}
a_1^n, & n < 0 \\
a_2^n, & n \ge 0 
\end{cases}
$$

Poles at $a_1$ and $a_2$

ROC:

$$|a_1| < |z| < |a_2|$$

---

### **Example 4 — LTI System with transfer function**

Given:

$$
H(z) = \frac{1}{1 - 0.9 z^{-1}}
$$

Pole at $0.9$.

**Case A — causal system**  
ROC: $|z| > 0.9$  
Stable? Yes, unit circle is inside ROC.

**Case B — anti-causal system**  
ROC: $|z| < 0.9$  
Stable? No.

---

## MATLAB Workflow for ROC Analysis

> [!example]- Extract poles  
> ```matlab
> b = [1];
> a = [1 -0.9];
> p = roots(a)
> ```

> [!example]- Visualize ROC radius  
> ```matlab
> abs(p)       % gives boundary of ROC for causal case
> ```

> [!example]- Plot poles/zeros  
> ```matlab
> zplane(b, a)
> title('Pole-Zero Plot with ROC Consideration')
> ```

---

## Determining ROC Step-by-Step (Exam-Ready)

### Step 1 — Find poles  
Use denominator of $X(z)$.

### Step 2 — Determine if sequence is left/right/two-sided  
From problem statement or from $x[n]$ expression.

### Step 3 — Apply ROC rule  
Right-sided → outside biggest pole  
Left-sided → inside smallest pole  
Two-sided → between poles

### Step 4 — Check stability (if asked)  
Unit circle must lie inside ROC.

### Step 5 — Include ROC in final answer  
Always write:

- **Z-transform expression**  
- **ROC condition**  
- **Sequence type (causal, anti-causal, two-sided)**

This is a common requirement on the exam.

---

## ROC Visual Intuition
Many students fail ROC because they think in equations — instead, think **geometrically**.

Poles = circles in the complex plane  
ROC = region that excludes those circles

Examples:

- One pole at $|p|=0.5$ → ROC either inside or outside that circle  
- Two poles at radii $0.4$ and $0.9$ → ROC is annulus  
- Poles outside unit circle → unstable causal system  

---
# 10. Time-Domain ↔ Z-Domain Relationships

The **z-transform** is more than a mathematical tool — it is the *bridge* between the time-domain description of a system and its frequency-domain behavior.

This section shows how:

- difference equations  
- convolution  
- system responses  
- poles/zeros  
- stability  
- frequency response  

…are all just different *faces* of the same object.

This is often where exam questions get tricky, so mastering these relationships gives you a huge advantage.

---

## 10.1 Difference Equation ↔ Z-Transform
A general LTI system is described by a **difference equation**:

$$
\sum_{k=0}^{N} a_k\,y[n-k]
=
\sum_{k=0}^{M} b_k\,x[n-k]
$$

Take the z-transform of both sides and use the shift property:

$$
\mathcal{Z}\{x[n-k]\} = z^{-k}X(z)
$$

We obtain:

$$
Y(z)\left(a_0 + a_1 z^{-1} + \cdots + a_N z^{-N}\right)
=
X(z)\left(b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}\right)
$$

Thus, the **system function** is:

$$
H(z) = \frac{Y(z)}{X(z)}
     = \frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}
            {a_0 + a_1 z^{-1} + \dots + a_N z^{-N}}
$$

This connects:

- the **difference equation**  
- the **impulse response**  
- the **frequency response**  
- the **pole-zero plot**  

as different representations of the same system.

---

> [!example]- From difference equation to H(z)
> ```matlab
> % y[n] - 0.3y[n-1] + 0.1y[n-2] = x[n]
>
> b = [1 0 0];              % numerator: x[n] term
> a = [1 -0.3 0.1];         % denominator: y[n] relationship
>
> tf(b, a, 1/Fs, 'variable','z^-1')
> ```

---

## 10.2 Convolution ↔ Multiplication
Time-domain convolution:

$$
y[n] = (x * h)[n]
$$

becomes simple multiplication in the z-domain:

$$
Y(z) = X(z)H(z)
$$

This is why:

- filtering is easy in the z-domain  
- cascade of systems is multiplication of transfer functions  
- convolution is expensive in the time-domain but cheap via FFT  

---

> [!example]- Compare time-domain vs z-domain convolution
> ```matlab
> x = [1 2 3];
> h = [1 -1];
>
> y_time = conv(x, h);
>
> X = fft(x, 4);
> H = fft(h, 4);
> y_freq = ifft(X .* H);
> ```

---

## 10.3 Impulse Response ↔ H(z)
Impulse response:

$$h[n] = \mathcal{Z}^{-1}\{H(z)\}$$

This means:

- the impulse response **is the system**
- H(z) contains all time-domain behavior encoded in pole/zero form

### FIR vs IIR from h[n]
- **FIR** → finite impulse response → numerator-only structure  
- **IIR** → infinite response → poles present → feedback in difference equation  

---

> [!example]- Extract impulse response
> ```matlab
> [h,n] = impz(b, a, 40);
> stem(n, h)
> ```

---

## 10.4 Poles ↔ Time-Domain Behavior
Poles determine the **shape** of the impulse response.

For example, if $H(z)$ has a pole at $p$:

- Time-domain response contains a term $p^n u[n]$  
- Magnitude of $p$ controls growth/decay  
- Angle of $p$ controls oscillation frequency  

### Pole-Time Relationship
| Pole $p$                 | Time-domain effect                         |
|--------------------------|---------------------------------------------|
| $p = r$                  | Exponential growth/decay $r^n$              |
| $p = r e^{j\omega_0}$    | Damped sinusoid $r^n \cos(\omega_0 n)$      |
| $\lvert p \rvert < 1$    | Stable — impulse response decays to 0       |
| $\lvert p \rvert > 1$    | Unstable — impulse response grows           |
| $\lvert p \rvert = 1$    | Marginally stable — sustained oscillation   |

---

> [!example]- Visualize pole → time-domain mapping
> ```matlab
> p = 0.9*exp(1i*pi/4);   % pole
> n = 0:50;
> h = abs(p).^n .* cos(angle(p)*n);
> stem(n, h)
> ```

---

## 10.5 Zeros ↔ Spectral Nulls
A zero at $z=z_0$ creates:

- frequency attenuation  
- phase changes  
- deep notches if $z_0$ lies on the unit circle  

For example:

- zero at $z=1$ → cancels DC  
- zero at $z=-1$ → cancels Nyquist frequency (high-pass behavior)  

---

> [!example]- Explore zero behavior
> ```matlab
> b = [1 -1];   % zero at z = 1
> a = 1;
> freqz(b, a, 512, Fs)
> ```

---

## 10.6 Stability ↔ Impulse Response Convergence
A system is stable if:

$$
\sum_{n=-\infty}^{\infty} |h[n]| < \infty
$$

Z-domain equivalent:

- **unit circle must lie inside the ROC**
- all poles must satisfy $|p_k| < 1$

Time-domain equivalent:

- impulse response must decay  

---

> [!example]- Stability check
> ```matlab
> p = roots(a);
> isStable = all(abs(p) < 1)
> ```

---

## 10.7 Frequency Response ↔ Z-domain Evaluation
Frequency response is:

$$
H(e^{j\omega}) = H(z)\big|_{z=e^{j\omega}}
$$

Meaning:

- magnitude response = how system scales sinusoids  
- phase response = how system shifts sinusoids  

MATLAB:

> [!example]- freqz()
> ```matlab
> [H, w] = freqz(b, a, 4096);
> plot(w/pi, abs(H))
> ```

---

## 10.8 System Interpretation Cheat Sheet

### If you know **difference equation**  
→ You can write **H(z)** immediately.

### If you know **H(z)**  
→ You can get poles/zeros, ROC, stability.

### If you know **poles**  
→ You can draw time-domain response shape.

### If you know **time-domain response**  
→ You can identify pole radii & angles.

### If you know **impulse response**  
→ You can detect FIR/IIR, stability, and frequency selectivity.

### If you know **frequency response**  
→ You can sketch pole-zero patterns.

---
# 11. DFT and IDFT

The **Discrete Fourier Transform (DFT)** is the most important computational tool in DSP.  
It converts finite-length signals into a finite number of frequency samples.

Where DTFT is continuous and theoretical, the **DFT is discrete and computable**.

---

## 11.1 What the DFT Actually Does

Given a length-$N$ signal $x[n]$ with $n=0,\dots,N\!-\!1$:

$$
X[k] = \sum_{n=0}^{N-1} x[n]\; e^{-j 2\pi kn/N}, \quad k=0,\dots,N-1
$$

Interpretation:

- Output is **periodic** with period $N$  
- Contains **N equally spaced frequency samples**  
- Resolution is  
  $$
  \Delta f = \frac{F_s}{N}
  $$  
- Frequencies are  
  $$
  f_k = \frac{k}{N} F_s
  $$

The DFT is literally the DTFT **sampled** at $N$ points.

---

## 11.2 IDFT — Reconstructing the Time Signal

Inverse DFT:

$$
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k]\; e^{j2\pi kn/N}
$$

Meaning:

- DFT + IDFT is a reversible pair  
- If you take FFT then IFFT, you get exact reconstruction  

> [!example]- DFT & IDFT via matrix form
> ```matlab
> x = [1 2 3 4].';
> N = length(x);
> n = 0:N-1;
> k = n.';
>
> W = exp(-1j * 2*pi/N);
> DFT = W .^ (k*n);   % Vandermonde matrix
>
> X = DFT * x;        % manual DFT
> x_rec = (1/N) * DFT' * X;   % manual IDFT
> ```

---

## 11.3 FFT — the Fast Algorithm  
The FFT computes the same $X[k]$ but with complexity:

- DFT: $\mathcal{O}(N^2)$  
- FFT: $\mathcal{O}(N \log N)$  

In the exam, ALWAYS use:

> [!example]- FFT + FFTSHIFT + scaling
> ```matlab
> X = fftshift(fft(x));
> magX = abs(X)/N;
> ```

---

## 11.4 Frequency Axis Construction (Most Common Exam Error)

Given:

- sampling frequency $F_s$  
- FFT length $N$  

Step 1: resolution  
$$
\Delta f = \frac{F_s}{N}
$$

Step 2: frequency vector  
$$
f = -\frac{F_s}{2} : \Delta f : \frac{F_s}{2}-\Delta f
$$

> [!example]- Frequency axis
> ```matlab
> df = Fs/N;
> f = -Fs/2 : df : Fs/2 - df;
> ```

### Why the last point is `Fs/2 - df`  
To ensure `length(f) = N`.

---

## 11.5 FFT Output Interpretation

FFT returns complex samples:

- **Magnitude** → amplitude  
  $$
  |X[k]| = \text{“strength of frequency component at } f_k \text{”}
  $$
- **Phase** → shift / time offset  
  $$
  \arg\{X[k]\}
  $$

> [!example]- Magnitude & phase
> ```matlab
> X = fftshift(fft(x));
> magX = abs(X)/N;
> phaseX = angle(X);
> ```

---

## 11.6 Energy & Parseval’s Relation  
Energy in time-domain equals energy in frequency-domain:

$$
\sum_{n=0}^{N-1} |x[n]|^2
=
\frac{1}{N}\sum_{k=0}^{N-1} |X[k]|^2
$$

> [!example]- Parseval check
> ```matlab
> Et = sum(abs(x).^2);
> Ef = (1/N) * sum(abs(X).^2);
> ```

---

## 11.7 Windowing, Leakage & Resolution  
When the signal is **not periodic within N samples**, you get:

### Spectral Leakage  
Energy “spreads” into neighboring bins.

### Frequency Resolution  
Better resolution requires:

- higher $N$  
- OR lower first-lobe width (choice of windowing)

### Rule of thumb  
To clearly identify a sinusoid at $f_0$:

$$
N \gg \frac{F_s}{f_0}
$$

---

## 11.8 The Full FFT Workflow (DTU Exam Template)

> [!example]- Full Spectral Analysis Template  
> ```matlab
> clear all; close all; clc;
>
> Fs = 1000;              % sampling frequency
> N  = 4096;              % FFT length
> Ts = 1/Fs;
>
> n = 0:N-1;
> t = n*Ts;
>
> % Example signal
> x = 3*cos(2*pi*50*t) + 2*sin(2*pi*120*t);
>
> % FFT
> X = fftshift(fft(x));
> magX = abs(X)/N;
> phaseX = angle(X);
>
> % Frequency axis
> df = Fs/N;
> f = -Fs/2 : df : Fs/2 - df;
>
> % Plot
> figure
> subplot(2,1,1)
> plot(f, magX)
> title('Magnitude Spectrum')
> grid on
>
> subplot(2,1,2)
> plot(f, phaseX)
> title('Phase Spectrum')
> grid on
> ```

---

## 11.9 Manual DFT Calculation (DTU LOVES THIS)

Given a signal:

$$x = [\,1,\ 2,\ 3,\ 4\,]$$

Manually compute:

### Step 1 — Define n & k  
### Step 2 — Build DFT matrix  
### Step 3 — Multiply  
### Step 4 — Compare with fft(x)

> [!example]- Manual DFT (exam-ready)
> ```matlab
> x = [1 2 3 4].';
> N = length(x);
> n = 0:N-1;
> k = n.';
>
> WN = exp(-1j*2*pi/N);
> D = WN .^ (k*n);
>
> X_manual = D*x;
> X_fft = fft(x);
>
> disp([X_manual, X_fft])
> ```

---

## 11.10 IDFT Derivation & Practical Use

IDFT reconstructs time-domain signals:

$$
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] e^{j2\pi kn/N}
$$

Important exam application:

- reconstruct signals from spectra  
- design FIR filters via frequency sampling  
- building inverse transforms of piecewise-defined $X[k]$

> [!example]- Reconstruct x[n] from X[k]
> ```matlab
> x_rec = ifft(ifftshift(X))*N;   % scale back
> ```

---

## 11.11 Circular Convolution Relationship

Time-domain circular convolution:

$$
y[n] = (x \circledast h)[n]
$$

Frequency-domain:

$$
Y[k] = X[k]H[k]
$$

Used in overlap-add, overlap-save, and FFT-based filtering.

> [!example]- FFT convolution
> ```matlab
> Y = ifft( fft(x).*fft(h) );
> ```

---
# 12. Circular Convolution and Circular Shift

Circular (modulo-$N$) operations appear in:

- FFT-based filtering  
- DFT definitions  
- DFT properties (shift/modulation)  
- Block convolution (overlap-add, overlap-save)  
- Periodic extension of signals  

This section shows you how to think about circular convolution in both theory and MATLAB.

---

## 12.1 Why Circular Convolution Exists

The DFT implicitly assumes the signal $x[n]$ is **periodic with period $N$**.

Meaning:

$$
x[n + N] = x[n]
$$

When you multiply spectra:

$$
Y[k] = X[k] H[k]
$$

you are convolving **periodic versions** of $x[n]$ and $h[n]$.

Thus, the natural time-domain result is **circular convolution**:

$$
y[n] = (x \circledast h)[n]
$$

NOT linear convolution.

This is why when you FFT two signals and IFFT them, you get circular convolution unless you zero-pad.

---

## 12.2 Circular Convolution Definition

For length-$N$ sequences:

$$
y[n] = \sum_{k=0}^{N-1} x[k] \; h[(n-k) \bmod N]
$$

This is the **linear convolution**, but the index is wrapped:

$$
(n-k) \bmod N
$$

Meaning if the index goes negative or beyond $N-1$, it wraps around like a clock.

---

## 12.3 Manual Circular Convolution (Exam Style)

> [!example]- Manual circular convolution (DTU workflow)
> ```matlab
> N = 8;
> x = [1 2 3 4 0 0 0 0];
> h = [1 -1 1 -1 1 -1 1 -1];
>
> y = zeros(1,N);
> for n = 0:N-1
>     for k = 0:N-1
>         y(n+1) = y(n+1) + x(k+1) * h(mod(n-k, N) + 1);
>     end
> end
>
> disp(y)
> ```
This directly implements:
$$y[n] = \sum_k x[k]h[(n-k)\bmod N]$$

---

## 12.4 Circular vs Linear Convolution

Linear convolution of lengths $L$ and $M$ has length:

$$
L + M - 1
$$

Circular convolution **always** has length:

$$
N
$$

Circular convolution = linear convolution **with time-aliasing**.

To avoid time-aliasing when using FFT:

### Rule
If performing FFT-based convolution:

**Zero-pad both signals to length at least**
$$
N \ge L + M - 1
$$

---

## 12.5 Circular Shift

Circular shift rotates a signal **modulo $N$**.

Definition:

$$
x[(n-m) \bmod N]
$$

MATLAB equivalent:

> [!example]- Circular shift  
> ```matlab
> x = 1:8;
> m = 2;
> y = circshift(x, m)   % shifts RIGHT by m
> ```

### Important exam note:
Right shift in MATLAB:
$circshift(x, +m)$

corresponds to:

$$
x[(n-m) \bmod N]
$$

because MATLAB indexes forward while DSP index math shifts backward.

---

## 12.6 DFT Properties Involving Circular Shift

The DFT has beautiful symmetry:

### Time shift ↔ modulation:

$$
x[(n-n_0) \bmod N]
\quad \Longleftrightarrow \quad
X[k] e^{-j2\pi k n_0/N}
$$

### Modulation ↔ shift:

$$
x[n] \, e^{j\,2\pi k_0 n / N}
\;\Longleftrightarrow\;
X[(k - k_0) \bmod N]
$$


These properties are used heavily in:

- frequency shifting  
- spectral analysis  
- OFDM / communications  
- understanding FFT bin alignment  

---

## 12.7 Circular Convolution via FFT (Fast Method)

Circular convolution:

$$
y[n] = (x \circledast h)[n]
$$

### FFT method:

> [!example]- FFT circular convolution
> ```matlab
> X = fft(x);
> H = fft(h);
> y_fft = ifft(X .* H);
> ```

If `x` and `h` are length-$N$, this computes **circular** convolution.

---

## 12.8 Linear Convolution via FFT (Correct Method)

Zero-pad to length:

$$
N_{\min} = L + M - 1
$$

> [!example]- FFT linear convolution (zero-padding)
> ```matlab
> L = length(x);
> M = length(h);
> Nmin = L + M - 1;
>
> X = fft(x, Nmin);
> H = fft(h, Nmin);
>
> y = ifft(X .* H);
> ```

This yields the **same result** as MATLAB’s `conv(x,h)`.

---

## 12.9 Circular Convolution Interpretation Cheat Sheet

### If you see **modulo indexing**:  
→ circular convolution

### If the result has length N  
→ circular convolution

### If an FFT-based filtering question appears  
→ circular convolution unless $N \ge L+M-1$

### If a signal “wraps around”  
→ circular shift or circular conv

---

## 12.10 MATLAB Toolbox Summary

> [!example]- Circular ops toolbox  
> ```matlab
> circshift(x, m)         % circular shift
> cconv(x, h, N)          % circular convolution
>
> fft(x).*fft(h)          % spectrum multiplication
> ifft(fft(x).*fft(h))    % circular convolution
>
> % Zero-padded FFT for linear convolution
> ifft(fft(x,Nmin).*fft(h,Nmin))
> ```

---
# 13. FFT Frameworks

The FFT (Fast Fourier Transform) is the **workhorse** of modern DSP.  
Every DTU DSP exam question involving:

- spectrum estimation  
- identifying frequencies  
- amplitude/phase extraction  
- filtering  
- convolution  
- system identification  
- aliasing  

…will use the FFT somewhere.

This section gives you PERFECT workflows you can apply blindly and instantly.

---

## 13.1 What the FFT Actually Computes

Given a sequence $x[n]$, $n=0,\dots,N-1$:

- `fft(x)` computes the **DFT**
- Output is in **wrap-around order** (0 … positive freqs … negative freqs)
- You almost always apply `fftshift()` to center it

Mathematically:

$$
X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-j 2\pi kn/N}
$$

---

## 13.2 Proper Frequency Axis — The DTU Standard

Given:

- sampling frequency $F_s$  
- FFT length $N$

You must compute:

### Step 1 — Frequency resolution

$$
\Delta f = \frac{F_s}{N}
$$

### Step 2 — Frequency vector (centered)

$$
f = -\frac{F_s}{2} : \Delta f : \frac{F_s}{2}-\Delta f
$$

> [!example]- Frequency axis (always correct)
> ```matlab
> df = Fs/N;
> f = -Fs/2 : df : Fs/2 - df;
> ```

### Why centered?

Because after `fftshift()`:

- the **0 Hz** bin sits at the center  
- negative frequencies are on the left  
- positive frequencies on the right  

---

## 13.3 Full 9-Step FFT Workflow (DTU Exam Template)

This is the **canonical** FFT procedure.  
Memorize this. Use this. Never deviate. 😘

> [!example]- 9-Step FFT workflow  
> ```matlab
> clear all; close all; clc;
>
> % 1) Sampling specs
> Fs = 2000;
> Ts = 1/Fs;
> N  = 4096;
>
> % 2) Time vector
> n = 0:N-1;
> t = n*Ts;
>
> % 3) Construct signal
> x = 2*cos(2*pi*50*t) + 3*cos(2*pi*120*t);
>
> % 4) FFT
> X = fft(x);
>
> % 5) Center spectrum
> Xc = fftshift(X);
>
> % 6) Scaling
> magX = abs(Xc)/N;
> phaseX = angle(Xc);
>
> % 7) Frequency axis
> df = Fs/N;
> f = -Fs/2 : df : Fs/2-df;
>
> % 8) Plot
> figure
> subplot(2,1,1)
> plot(f, magX, 'LineWidth', 1.5)
> title('Magnitude Spectrum')
> grid on
>
> subplot(2,1,2)
> plot(f, phaseX)
> title('Phase Spectrum')
> grid on
> ```

---

## 13.4 Understanding FFT Peaks (Bin Location)

A tone at frequency $f_0$ should appear at:

$$
k_0 = \frac{f_0}{F_s} N
$$

But after centering, the true bin index is:

$$
k_0^{(c)} = k_0 - \frac{N}{2}
$$

### Practical peak detection

> [!example]- Finding closest FFT bin to f₀  
> ```matlab
> target = 120;
> idx = dsearchn(f.', target);
> peak_mag = magX(idx);
> ```

This is **extremely useful** for identifying frequencies in the exam.

---

## 13.5 Amplitude Scaling — Avoid the #1 Exam Error

Students forget that FFT amplitude depends on $N$.

Correct scaling:

$$
|X[k]|_\text{scaled} = \frac{1}{N} |X[k]|
$$

If you want *one-sided* amplitude (0 to Fs/2):

- multiply non-DC & non-Nyquist bins by 2  

Two-sided (DTU standard) uses **no factor of 2**.

> [!example]- Two-sided amplitude
> ```matlab
> magX = abs(Xc)/N;
> ```

---

## 13.6 Leakage, Windowing, and Resolution

### Leakage occurs when:
- The signal is **not periodic** in the analysis window  
- The tone frequency is **not exactly an integer bin**  

### Symptoms:
- Peak spreads into neighbors  
- Amplitude underestimation  
- Phase ambiguity  

### Resolution:
$$
\Delta f = \frac{F_s}{N}
$$

Increasing $N$ improves frequency resolution.  
Increasing $F_s$ does NOT improve resolution.

### Windows reduce leakage but widen the main lobe.

Window trade-off:

| Window | Leakage | Resolution |
|--------|---------|------------|
| Rectangular | worst | best |
| Hamming | low | moderate |
| Hann | moderate | moderate |
| Blackman | very low | poor |

---

## 13.7 FFT-Based Filtering (Fast Convolution)

Convolution in time ↔ multiplication in frequency:

$$
Y[k] = X[k] H[k]
$$

But **this is circular convolution** unless you zero-pad.

### Correct linear convolution via FFT:

> [!example]- FFT convolution (proper)
> ```matlab
> L = length(x);
> M = length(h);
> Nmin = L + M - 1;
>
> X = fft(x, Nmin);
> H = fft(h, Nmin);
> y = ifft(X .* H);
> ```

### Circular convolution via FFT:

> [!example]- Circular convolution
> ```matlab
> y = ifft( fft(x).*fft(h) );
> ```

---

## 13.8 Extracting Phase Information

Phase is:

$$
\phi[k] = \arg\{X[k]\}
$$

Be careful:

- If amplitude is near zero, phase is meaningless  
- Phase jumps occur (unwrap with `unwrap()`)

> [!example]- Clean phase plot  
> ```matlab
> phaseX = unwrap(angle(Xc));
> plot(f, phaseX)
> ```

---

## 13.9 FFT Toolbox Summary (Memory Section)

> [!example]- FFT cheat commands  
> ```matlab
> fft(x)                      % DFT
> fftshift(X)                 % center spectrum
> abs(X)                      % magnitude
> angle(X)                    % phase
> unwrap(angle(X))            % continuous phase
>
> ifft(X)                     % time-domain reconstruction
> ifftshift(X)                % undo fftshift
>
> dsearchn(f.', f0)           % find closest frequency bin
> ```


---

# 14. Filter Design Workflows

Filter design in DSP follows a strict, structured workflow.  
Unlike “Press butter()” MATLAB functions, DTU expects you to **manually**:

1. Interpret filter specifications  
2. Prewarp digital frequencies  
3. Transform them into analog prototype specs  
4. Build a Butterworth analog prototype  
5. Transform prototype (LP→HP/BP/BS)  
6. Apply bilinear transform  
7. Plot & validate the digital filter  

This section gives you the **exact full pipeline** for designing digital filters from scratch.

---

## 14.1 Overview of the Filter Design Pipeline

### Step 1 — Digital specs (given in the exam)
You’re given frequencies in Hz:

- Passband edge: $f_p$  
- Stopband edge: $f_s$  
- Passband ripple: $A_p$  
- Stopband attenuation: $A_s$  
- Sampling frequency: $F_s$  

### Step 2 — Convert to digital angular frequencies

$$
\omega = 2\pi \frac{f}{F_s}
$$

### Step 3 — Prewarp frequencies (BLT distortion correction)

BLT warps frequency because it maps:

$$
s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}}
$$

To preserve exact cutoff locations:

$$
\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right)
$$

### Step 4 — Use analog specs to determine Butterworth order

$$
n =
\frac{
\log_{10}\left(10^{A_s/10} - 1\right)
-
\log_{10}\left(10^{A_p/10} - 1\right)
}
{2 \log_{10}\left( \Omega_s / \Omega_p \right)}
$$

Take **ceiling**.

### Step 5 — Construct analog prototype

Butterworth poles:

$$
p_k = e^{j\frac{\pi}{2n}(2k+n-1)}, \quad k = 1,\dots,n
$$

### Step 6 — Apply frequency transformation (LP → HP/BP/BS)

Depends on filter type (covered below).

### Step 7 — Apply bilinear transform to obtain digital filter

### Step 8 — Validate using `freqz()`

---

## 14.2 Prewarping (Critical Step)

Digital frequency:

$$\omega_p = 2\pi \frac{f_p}{F_s}$$

Prewarped analog frequency:

$$
\Omega_p = \frac{2}{T_s} \tan\left(\frac{\omega_p}{2}\right)
$$

> [!example]- Prewarp both passband & stopband  
> ```matlab
> Ts = 1/Fs;
> Omega_p = (2/Ts)*tan(wp/2);
> Omega_s = (2/Ts)*tan(ws/2);
> ```

---

## 14.3 Designing the Analog Low-Pass Prototype

### Analog Butterworth LP prototype:

Magnitude:

$$
|H(j\Omega)|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2n}}
$$

Filter order \(n\):

$$
n = \left\lceil 
\frac{
\log_{10}(10^{A_s/10}-1) - \log_{10}(10^{A_p/10}-1)
}{2 \log_{10}(\Omega_s / \Omega_p)}
\right\rceil
$$

Cutoff frequency:

$$
\Omega_c = \Omega_p / (10^{A_p/10} - 1)^{1/(2n)}
$$

> [!example]- Butterworth prototype generation  
> ```matlab
> % Compute analog LP prototype
> n = ceil( ( log10(10^(As/10)-1) - log10(10^(Ap/10)-1) ) ...
>          / (2 * log10(Omega_s/Omega_p)) );
>
> Omega_c = Omega_p / ( (10^(Ap/10)-1)^(1/(2*n)) );
>
> [b_lp, a_lp] = butter(n, Omega_c, 's');
> ```

---

## 14.4 Frequency Transformations (LP → HP/BP/BS)

### LP → HP
$$
s \rightarrow \frac{\Omega_c}{s}
$$

> [!example]- LP → HP  
> ```matlab
> [b_hp, a_hp] = lp2hp(b_lp, a_lp, Omega_c);
> ```

---

### LP → Band-Pass (BP)

Center frequency:

$$\Omega_0 = \sqrt{\Omega_1 \Omega_2}$$

Bandwidth:

$$B = \Omega_2 - \Omega_1$$

Transformation:

$$
s \rightarrow \frac{s^2 + \Omega_0^2}{B s}
$$

> [!example]- LP → BP  
> ```matlab
> [b_bp, a_bp] = lp2bp(b_lp, a_lp, Omega_0, B);
> ```

---

### LP → Band-Stop (BS)

Transformation:

$$
s \rightarrow \frac{B s}{s^2 + \Omega_0^2}
$$

> [!example]- LP → BS  
> ```matlab
> [b_bs, a_bs] = lp2bs(b_lp, a_lp, Omega_0, B);
> ```

---

## 14.5 Bilinear Transform (BLT)

Maps analog transfer function to digital:

$$
s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}}
$$

### Why BLT?
- Maps entire LHP to inside unit circle  
- Guarantees stability  
- No aliasing  
- Frequency warping (prewarp fixes this)

### MATLAB:

> [!example]- Bilinear transform  
> ```matlab
> [bz, az] = bilinear(b_analog, a_analog, Fs);
> ```

---

## 14.6 Digital Filter Validation

Once you have \(b_z\), \(a_z\):

> [!example]- freqz() analysis  
> ```matlab
> [H,f] = freqz(bz, az, 4096, Fs);
> figure
> subplot(2,1,1)
> plot(f, abs(H))
> title('Magnitude Response')
> grid on
>
> subplot(2,1,2)
> plot(f, angle(H))
> title('Phase Response')
> grid on
> ```

Check:

- cutoff frequencies  
- attenuation criteria  
- ripple bounds  
- system stability (poles inside unit circle)

---

## 14.7 Full End-to-End Design Template (Copy This for Exam)

> [!example]- LP/HP/BP/BS Digital Filter Design Template  
> ```matlab
> %%%% 1. DIGITAL SPECS %%%%
> Fs = 2000;
> fp = 150; fs = 300;
> Ap = 1;  As = 40;   % dB
>
> %%%% 2. CONVERT TO DIGITAL ANGULAR FREQ %%%%
> wp = 2*pi*fp/Fs;
> ws = 2*pi*fs/Fs;
>
> %%%% 3. PREWARP %%%%
> Ts = 1/Fs;
> Omega_p = (2/Ts)*tan(wp/2);
> Omega_s = (2/Ts)*tan(ws/2);
>
> %%%% 4. BUTTERWORTH PROTOTYPE ORDER %%%%
> n = ceil( ( log10(10^(As/10)-1) - log10(10^(Ap/10)-1) ) ...
>          / (2 * log10(Omega_s/Omega_p)) );
>
> %%%% 5. PROTOTYPE CUTOFF %%%%
> Omega_c = Omega_p / ( (10^(Ap/10)-1)^(1/(2*n)) );
>
> %%%% 6. ANALOG LP PROTOTYPE %%%%
> [b_lp, a_lp] = butter(n, Omega_c, 's');
>
> %%%% 7. TRANSFORM (LP->DESIRED) %%%%
> % HP example:
> [b_analog, a_analog] = lp2hp(b_lp, a_lp, Omega_c);
>
> %%%% 8. BILINEAR TRANSFORM %%%%
> [bz, az] = bilinear(b_analog, a_analog, Fs);
>
> %%%% 9. VALIDATION %%%%
> freqz(bz, az, 4096, Fs);
> ```

---

## 14.8 Filter Type Cheat Sheet

| Analog/Digital Operation | Characteristic |
|--------------------------|----------------|
| LP → HP                  | Zero at $z=1$ → removes DC |
| LP → BP                  | Two poles + two zeros → bandpass behavior |
| LP → BS                  | Two zeros → notch at center freq |
| Pole radius              | Controls bandwidth / decay speed |
| Zero location            | Controls attenuation characteristics |

---

## 14.9 Exam Strategy for Filter Design

1. Draw timeline: Digital specs → Analog specs → Prototype → Transform → BLT  
2. Always prewarp  
3. Calculate order early  
4. Label all critical frequencies (Hz → rad/s → prewarped)  
5. For each transformation, draw a quick block diagram  
6. Use freqz() to verify — exam expects a plot  
7. Include stability reasoning (poles inside unit circle)  
8. Write final answer with:  
   - $H(z)$  
   - \(b_z, a_z\) coefficients  
   - Magnitude plot  
   - Order  
   - Filter type  

---
# 15. Difference Equations

Difference equations describe **all discrete-time LTI systems** in the time domain.  
They are the *time-domain counterpart* of the system function \( H(z) \).

You will encounter them in:

- system analysis  
- filtering  
- transient/steady-state response  
- z-transform problems  
- stability checks  
- convolution tasks  

This section explains the theory and gives you the complete exam workflow.

---

## 15.1 General Form

A general causal LTI system is:

$$
a_0 y[n] + a_1 y[n-1] + \dots + a_N y[n-N]
=
b_0 x[n] + b_1 x[n-1] + \dots + b_M x[n-M]
$$

Common normalization:

$$
y[n] = -\sum_{k=1}^{N} a_k\, y[n-k] + \sum_{k=0}^{M} b_k\, x[n-k]
$$

### Interpretation  
- **$b_k$** → feedforward (FIR part)  
- **$a_k$** → feedback (IIR part)  
- **Presence of $a_k$** → infinite impulse response  

---

## 15.2 Z-Transform Solution (Core Exam Skill)

Take the Z-transform of both sides — using:

$$
\mathcal{Z}\{x[n-k]\} = z^{-k} X(z)
$$

We get:

$$
Y(z)(a_0 + a_1 z^{-1} + \dots + a_N z^{-N})
=
X(z)(b_0 + b_1 z^{-1} + \dots + b_M z^{-M})
$$

Therefore:

$$
H(z) = \frac{Y(z)}{X(z)} 
     = \frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}
            {a_0 + a_1 z^{-1} + \dots + a_N z^{-N}}
$$

This connects:

- **difference equation**  
- **system function**  
- **poles/zeros**  
- **impulse response**  
- **frequency response**  

All representations are the same system.

---

> [!example]- From difference equation → H(z)
> ```matlab
> % Example: y[n] - 0.3y[n-1] + 0.04y[n-2] = x[n]
>
> b = [1 0 0];
> a = [1 -0.3 0.04];
>
> H = tf(b, a, 1/Fs, 'variable','z^-1');
> zplane(b, a)
> ```

---

## 15.3 Impulse Response Solution

Impulse response:

$$
h[n] = \mathcal{Z}^{-1}\{H(z)\}
$$

If the poles are at:

- $p_1, p_2, \dots, p_N$

Then:

$$
h[n] = \sum_k C_k p_k^n u[n]
$$

Where the coefficients \( C_k \) come from **partial fractions**.

---

> [!example]- Compute impulse response in MATLAB
> ```matlab
> [h, n] = impz(b, a, 40);
> stem(n, h)
> ```

---

## 15.4 Step Response

The step response highlights:

- stability  
- transient vs steady-state  
- cumulative behavior  

Step response:

$$
s[n] = \sum_{k=0}^n h[k]
$$

> [!example]- Step response with filter()
> ```matlab
> u = ones(1,200);
> y = filter(b, a, u);
> plot(y)
> ```

---

## 15.5 Solving Difference Equations by Hand (Exam Workflow)

Given:

$$
y[n] - 0.6y[n-1] + 0.1y[n-2] = x[n]
$$

### Step 1 — Z-transform both sides

### Step 2 — Solve for Y(z)

### Step 3 — Decompose partial fractions  
Find inverse terms like:

- \( C_1 p_1^n u[n] \)  
- \( C_2 p_2^n u[n] \)  

### Step 4 — Find homogeneous solution  
Solve roots of denominator:

$$
r_1, r_2 = \text{roots of }(1 - 0.6z^{-1} + 0.1z^{-2})
$$

### Step 5 — Find particular solution  
Depending on input:

- constant  
- exponential  
- sinusoid  

### Step 6 — Apply initial conditions (if required)

---

> [!example]- Partial fraction expansion in MATLAB  
> ```matlab
> [r, p, k] = residue(b, a);
> r       % residues C_k
> p       % poles
> k       % direct polynomial term
> ```

---

## 15.6 FIR vs IIR from Difference Equation

### FIR (Finite Impulse Response)
- denominator is **1**  
- no feedback  
- impulse response finite  
- always stable  

### IIR (Infinite Impulse Response)
- denominator has poles  
- feedback present  
- impulse response infinite  
- stability requires $|p_k| < 1$

---

## 15.7 Convolution Interpretation

Difference equation is equivalent to:

$$
y[n] = (x * h)[n]
$$

Where:

- convolution in time  
- multiplication in frequency  
- product in z-domain  

---

> [!example]- Linear convolution  
> ```matlab
> y = conv(x, h);
> ```

---

## 15.8 Stability Verification via Difference Equation

A causal system is stable if:

$$
\sum_{n=0}^{\infty} |h[n]| < \infty
$$

Time-domain interpretation:

- exponential decay → stable  
- sustained oscillation → marginal  
- growth → unstable  

Z-domain interpretation:

- all poles strictly inside unit circle  

---

> [!example]- Stability check  
> ```matlab
> poles = roots(a);
> isStable = all(abs(poles) < 1)
> ```

---

## 15.9 Solving Systems with MATLAB

### Direct simulation (difference equation)

> [!example]- filter()
> ```matlab
> y = filter(b, a, x);
> ```

### Impulse response

> [!example]- impz()
> ```matlab
> [h, n] = impz(b, a, 60);
> ```

### Step response

> [!example]- Step response
> ```matlab
> stepz(b, a)   % or filter(b,a,u)
> ```

### Frequency response

> [!example]- freqz()
> ```matlab
> freqz(b, a, 4096, Fs)
> ```

---

## 15.10 Difference Equation Cheat Sheet

| Representation | Meaning |
|----------------|---------|
| Difference equation | Time-domain description |
| $H(z)$ | System function |
| Poles/zeros | System behavior + stability |
| $h[n]$ | Impulse response |
| $s[n]$ | Step response |
| $y[n] = x[n] * h[n]$ | LTI convolution |
| $Y(z) = X(z)H(z)$ | z-domain multiplication |
| $Y[k] = X[k]H[k]$ | DFT multiplication |

---
# 16. Advanced DSP Techniques

This section contains the *higher-level DSP concepts* that appear throughout assignments, exams, and practical MATLAB problems.  
They extend the basic tools of FFT, $H(z)$, and difference equations into more powerful analysis and processing workflows.

These are the “exam extras” that give you a huge edge.

---

## 16.1 Signal Energy and Power

### Energy Signals
A signal is **energy type** if:

$$
E = \sum_{n=-\infty}^{\infty} |x[n]|^2 < \infty
$$

These include:

- finite-length sequences  
- decaying exponentials ($|a| < 1$)  

> [!example]- Compute energy  
> ```matlab
> E = sum(abs(x).^2);
> ```

---

### Power Signals
A signal is **power type** if energy is infinite, but average power is finite:

$$
P = \lim_{N\to\infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^2
$$

Examples:

- sinusoids  
- periodic signals  

> [!example]- Numerical power estimate  
> ```matlab
> P = mean(abs(x).^2);
> ```

---

## 16.2 Parseval’s Theorem

Time-domain ↔ Frequency-domain energy equality:

$$
\sum_{n=0}^{N-1} |x[n]|^2
=
\frac{1}{N} \sum_{k=0}^{N-1} |X[k]|^2
$$

This confirms correct FFT scaling.

> [!example]- Parseval check  
> ```matlab
> Et = sum(abs(x).^2);
> Ef = (1/N)*sum(abs(X).^2);   % X = fft(x)
> ```

---

## 16.3 Multi-Tone Signals (Exam Classic)

A multi-tone signal:

$$
x[n] = \sum_k A_k \cos(2\pi f_k n T_s)
$$

Spectrum shows multiple symmetrical peaks.

> [!example]- Multi-tone spectrum  
> ```matlab
> x = 1.5*cos(2*pi*100*t) + 4.5*cos(2*pi*400*t);
> X = fftshift(fft(x));
> magX = abs(X)/N;
> ```

Interpreting multi-tone spectra is a MUST for the exam.

---

## 16.4 Modulation and Frequency Shifting

### Time-domain modulation → frequency shift
If:

$$
y[n] = x[n] e^{j 2\pi k_0 n / N}
$$

Then:

$$
Y[(k - k_0) \bmod N]
= X[k]
$$

This is used for:

- shifting spectra  
- analytic signal creation  
- OFDM concepts  
- spectral alignment  

> [!example]- Modulate & shift in MATLAB  
> ```matlab
> k0 = 50;                       % shift index
> y = x .* exp(1j*2*pi*k0*n/N);  % time-domain modulation
> Y = fftshift(fft(y));
> ```

---

## 16.5 Windowing & Leakage Control

Windowing reduces spectral leakage at the cost of resolution.

| Window | Leakage | Resolution | Notes |
|--------|---------|------------|-------|
| Rectangular | worst | best | exam standard |
| Hann/Hanning | medium | medium | smooth decay |
| Hamming | low | moderate | popular for PSD |
| Blackman | very low | poor | high dynamic range |

> [!example]- Apply window  
> ```matlab
> w = hann(N).';
> xw = x .* w;
>
> Xw = fftshift(fft(xw));
> ```

Use windows when:

- the signal is not periodic in the measurement window  
- leakage must be minimized  
- identifying closely spaced tones  

---

## 16.6 DTFT via freqz (The Hidden Trick)

`freqz(x,1,…)` computes the DTFT of the signal $x[n]$:

- continuous frequency samples  
- higher resolution than FFT  
- no wrap-around issues  

> [!example]- DTFT using freqz  
> ```matlab
> [X,w] = freqz(x, 1, 4096, 'whole');
> plot(w/pi, abs(X))
> ```

This is extremely useful for:

- studying ideal sequences  
- theoretical spectrum comparisons  
- debugging FFT behavior  

---

## 16.7 Magnitude & Phase Interpretation (Advanced)

The FFT gives you:

- **Magnitude spectrum** → amplitude  
- **Phase spectrum** → time shift & symmetry  

### Time shift ↔ linear phase  
If:

$$
y[n] = x[n - n_0]
$$

Then:

$$
Y[k] = X[k] e^{-j 2\pi k n_0 / N}
$$

A linear phase slope corresponds to a delay in time.

> [!example]- Measuring delay via phase  
> ```matlab
> phaseX = unwrap(angle(X));
> plot(f, phaseX)
> ```

---

## 16.8 Real vs Complex Signals

### Real signals  
Have conjugate symmetric spectra:

$$
X[k] = X^*[(-k) \bmod N]
$$

### Complex signals  
Spectrum has no symmetry.

Used for:

- modulation  
- analytic signal  
- Hilbert transform  

---

## 16.9 Analytic Signals & Hilbert Transform (Optional but Powerful)

Analytic signal:

$$
x_a[n] = x[n] + j \,\hat{x}[n]
$$

Where $\hat{x}[n]$ is the Hilbert transform.

Properties:

- no negative frequencies  
- used in envelope detection  
- used in modulation systems  

> [!example]- Analytic signal  
> ```matlab
> xa = hilbert(x);
> env = abs(xa);
> ```

This is extremely useful for reading AM envelopes.

---

## 16.10 Spectral Power Density Estimates (Welch’s Method)

If the exam ever asks for PSD:

> [!example]- Welch PSD  
> ```matlab
> pwelch(x, hamming(512), 256, 1024, Fs)
> ```

---

## 16.11 Advanced DSP Cheat Sheet

| Concept         | Key Result                                      |
|-----------------|-------------------------------------------------|
| Time shift      | Linear phase slope in $H(e^{j\omega})$          |
| Frequency shift | Multiply by $e^{j\omega_0 n}$                   |
| Energy          | $E = \sum\limits_{n} \lvert x[n] \rvert^2$      |
| Parseval        | $E = \dfrac{1}{N} \sum\limits_{k} \lvert X[k]\rvert^2$ |
| Modulation      | Shifts spectrum in frequency domain             |
| Windowing       | Trade-off: leakage $\leftrightarrow$ resolution |
| Real signal     | Conjugate-symmetric spectrum                    |
| Complex signal  | No conjugate symmetry                           |
| DTFT via freqz  | High-resolution $X(e^{j\omega})$ estimate       |

---
# 17. Quick Reference Tables

This section collects the most essential DSP relationships into fast, compact tables.  
Use it for **exam lookup**, **mental refreshers**, and **workflow reminders**.

---

## 17.1 Time-Domain ↔ Frequency-Domain

| Concept              | Relationship                                                           |
|----------------------|------------------------------------------------------------------------|
| Convolution          | $y[n] = (x * h)[n]$                                                    |
| z-domain             | $Y(z) = X(z)\,H(z)$                                                    |
| DFT                  | $X[k] = \sum\limits_{n=0}^{N-1} x[n]\;e^{-j2\pi kn/N}$                 |
| IDFT                 | $x[n] = \dfrac{1}{N}\sum\limits_{k=0}^{N-1} X[k]\;e^{j2\pi kn/N}$      |
| DTFT                 | $X(e^{j\omega}) = \sum\limits_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$ |

---

## 17.2 FFT Essentials

| Task                    | MATLAB One-Liner                                      |
|-------------------------|--------------------------------------------------------|
| Compute FFT             | `X = fft(x);`                                         |
| Centered spectrum       | `Xc = fftshift(X);`                                   |
| Magnitude (two-sided)   | `magX = abs(Xc)/N;`                                   |
| Phase                   | `phaseX = angle(Xc);`                                 |
| Unwrapped phase         | `phaseX = unwrap(angle(Xc));`                         |
| Frequency axis (center) | `f = -Fs/2 : Fs/N : Fs/2 - Fs/N;`                     |
| Nearest bin to $f_0$    | `idx = dsearchn(f.', f0);`                            |

---

## 17.3 Z-Transform & System Analysis

| Concept             | Formula / Condition                                          |
|---------------------|--------------------------------------------------------------|
| Z-transform         | $X(z) = \sum\limits_{n=-\infty}^{\infty} x[n] z^{-n}$        |
| Freq. response      | $H(e^{j\omega}) = H(z)\big\rvert_{z=e^{j\omega}}$            |
| Stability           | all poles satisfy $\lvert p_k\rvert < 1$                    |
| Causal ROC          | $\lvert z\rvert > \max_k \lvert p_k\rvert$                  |
| Impulse response    | $h[n] = \mathcal{Z}^{-1}\{H(z)\}$                            |
| Convolution (z-dom) | $Y(z) = X(z) H(z)$                                           |
| Partial fractions   | `[r,p,k] = residue(b,a)`                                     |

---

## 17.4 Filter Design Pipeline

| Stage                               | Operation                                                                 |
|-------------------------------------|---------------------------------------------------------------------------|
| Digital specs → digital $\omega$    | $\omega = 2\pi f / F_s$                                                  |
| Prewarp                             | $\Omega = \dfrac{2}{T_s}\tan\big(\omega/2\big)$                          |
| Order (Butterworth)                 | $n = \left\lceil \dfrac{\log_{10}(10^{A_s/10}-1) - \log_{10}(10^{A_p/10}-1)}{2\log_{10}(\Omega_s/\Omega_p)} \right\rceil$ |
| Analog LP prototype                 | Compute Butterworth poles, form $H(s)$                                   |
| Transform to HP/BP/BS               | Use LP→HP/BP/BS substitutions                                            |
| Bilinear transform                  | `[bz, az] = bilinear(b_analog, a_analog, Fs);`                           |
| Validate digital filter             | `freqz(bz, az, 4096, Fs);`                                               |

---

## 17.5 Analog Filter Transformations

| Transform | Substitution                                      |
|-----------|---------------------------------------------------|
| LP → LP   | $s \rightarrow s / \Omega_c$                      |
| LP → HP   | $s \rightarrow \Omega_c / s$                      |
| LP → BP   | $s \rightarrow \dfrac{s^2 + \Omega_0^2}{B s}$     |
| LP → BS   | $s \rightarrow \dfrac{B s}{s^2 + \Omega_0^2}$     |

---

## 17.6 Circular Convolution Tools

| Task                      | MATLAB Command                                 |
|---------------------------|-----------------------------------------------|
| Circular shift            | `y = circshift(x, m);`                        |
| Circular convolution      | `y = cconv(x, h, N);`                         |
| FFT circular convolution  | `y = ifft( fft(x).*fft(h) );`                 |
| Linear conv via FFT       | `y = ifft( fft(x,N).*fft(h,N) );`             |

---

## 17.7 Difference Equation Toolbox

| Task               | MATLAB Command                                      |
|--------------------|-----------------------------------------------------|
| Apply system       | `y = filter(b, a, x);`                              |
| Impulse response   | `[h, n] = impz(b, a, N);`                          |
| Step response      | `y = filter(b, a, ones(1,N));`                     |
| Poles/zeros plot   | `zplane(b, a);`                                    |
| Get poles/zeros    | `[z, p, k] = tf2zpk(b, a);`                        |
| Partial fractions  | `[r, p, k] = residue(b, a);`                       |

---

## 17.8 Windowing Cheat Sheet

| Window      | Pros                         | Cons                    |
|-------------|------------------------------|-------------------------|
| Rectangular | Best resolution              | Worst leakage           |
| Hann        | Good leakage reduction       | Moderate resolution     |
| Hamming     | Low sidelobes (low leakage)  | Slightly wider mainlobe |
| Blackman    | Excellent sidelobe suppression | Poor resolution       |

---

## 17.9 Signal Energy & Power

| Concept  | Formula                                                   |
|----------|-----------------------------------------------------------|
| Energy   | $E = \sum\limits_{n=-\infty}^{\infty} \lvert x[n]\rvert^2$ |
| Power    | $P = \lim\limits_{N\to\infty} \dfrac{1}{2N+1} \sum\limits_{n=-N}^{N} \lvert x[n]\rvert^2$ |
| Parseval | $E = \dfrac{1}{N}\sum\limits_{k=0}^{N-1} \lvert X[k]\rvert^2$ |

---

## 17.10 Most Important MATLAB Commands (DSP Master List)

> [!example]- Copy/Paste DSP Toolbox  
> ```matlab
> % FFT & spectra
> X  = fft(x);
> Xc = fftshift(X);
> magX   = abs(Xc)/N;
> phaseX = angle(Xc);
> phaseX = unwrap(angle(Xc));
>
> % Frequency responses
> freqz(b, a, 4096, Fs);
> freqs(num, den);
>
> % Time-domain LTI behavior
> y  = filter(b, a, x);
> yC = conv(x, h);
> [h_imp, n_imp] = impz(b, a, 60);
>
> % Z-domain & poles/zeros
> Hz = tf(b, a, 1/Fs, 'variable', 'z^-1');
> zplane(b, a);
> [z, p, k] = tf2zpk(b, a);
> [r, p_res, k_res] = residue(b, a);
>
> % Windowing & PSD
> w_hann    = hann(N).';
> w_hamming = hamming(N).';
> w_black   = blackman(N).';
> pwelch(x);
>
> % Circular ops
> x_shift = circshift(x, m);
> y_circ  = cconv(x, h, N);
> ```

---
# 18. Spectrum Sketching & Visualization

**Purpose:** Quick, publication-quality theoretical spectrum plots for reports, assignments, and conceptual understanding.

The `plot_spectrum()` function provides a professional way to sketch **theoretical spectra** with arrow notation (Dirac deltas) — the standard representation for discrete spectral components in DSP.

---

## 18.1 Why Spectrum Sketching Matters

In DSP, you constantly switch between:

1. **Theoretical/analytical spectra** → what you expect mathematically  
2. **Computed FFT spectra** → what you actually measure  

**Theoretical spectra** use **arrows (impulses)** to represent discrete frequency components:

- AM sidebands  
- Sampling replicas  
- Modulation products  
- Aliasing effects  
- Filter specifications  

The `plot_spectrum()` function creates these theoretical plots instantly.

---

## 18.2 Basic Usage Patterns

### Pattern 1: Simplest Possible

> [!code]- MATLAB
> ```matlab
> % Just frequencies and amplitudes
> plot_spectrum([1, 3, 5], [0.5, 1, 0.3]);
> ```
Everything else (axis ranges, labels, colors) is auto-calculated.

---

### Pattern 2: Symmetric Signal (Common in DSP)

> [!code]- MATLAB
> ```matlab
> % Baseband signal with ±f components
> freqs = [-5, -2, 0, 2, 5];  % kHz
> amps  = [0.3, 0.8, 1, 0.8, 0.3];
> 
> plot_spectrum(freqs, amps, ...
>     'XLabel', 'Frequency (kHz)', ...
>     'Title', 'Baseband Spectrum');
> ```

---

### Pattern 3: AM Signal Spectrum

> [!code]- MATLAB
> ```matlab
> % cos(2π·f_m·t) · cos(2π·f_c·t)
> % Components at ±(f_c ± f_m)
> fc = 16;  % carrier [kHz]
> fm = 1;   % modulation [kHz]
> 
> freqs = [-(fc+fm), -(fc-fm), fc-fm, fc+fm];
> amps  = [0.25, 0.25, 0.25, 0.25];
> 
> plot_spectrum(freqs, amps, ...
>     'XRange', [-20, 20], ...
>     'XLabel', 'Frequency (kHz)', ...
>     'Title', 'AM Spectrum', ...
>     'Colors', {{'red'}, {'red'}, {'blue'}, {'blue'}});
> ```

---

### Pattern 4: Sampling & Aliasing

> [!code]- MATLAB
> ```matlab
> % Original signal + aliased replicas
> f0 = 1;   % signal frequency
> Fs = 8;   % sampling frequency
> 
> % Show original and first few aliases
> freqs = [-Fs-f0, -Fs+f0, -f0, f0, Fs-f0, Fs+f0];
> amps  = [1, 1, 1, 1, 1, 1];
> 
> plot_spectrum(freqs, amps, ...
>     'XRange', [-12, 12], ...
>     'Title', sprintf('Aliasing: f_0 = %d kHz, F_s = %d kHz', f0, Fs));
> ```

---

## 18.3 Complete Parameter Reference

### Required Parameters

- `frequencies` — vector of frequency values  
- `amplitudes` — vector of amplitude values (same length)  

### Optional Parameters (Name-Value Pairs)

| Parameter      | Default            | Purpose                              |
|----------------|--------------------|--------------------------------------|
| `'XRange'`     | auto               | `[xmin, xmax]` for x-axis            |
| `'YMax'`       | auto               | Maximum y-axis value                 |
| `'XStep'`      | auto               | Spacing between x-axis ticks         |
| `'YStep'`      | `0.5`             | Spacing between y-axis ticks         |
| `'XLabel'`     | `'Frequency (Hz)'` | X-axis label text                    |
| `'YLabel'`     | `'Amplitude (A.U.)'` | Y-axis label text                  |
| `'Title'`      | none               | Plot title                           |
| `'Colors'`     | auto               | Cell array of colors for each arrow |
| `'LineWidth'`  | `2`               | Width of arrows                      |
| `'FigNum'`     | new figure         | Reuse/update existing figure         |
| `'MaxXLabels'` | `15`              | Max number of x-axis labels shown    |
| `'MaxYLabels'` | `10`              | Max number of y-axis labels shown    |

---

## 18.4 Advanced Examples

### Example 1: Highlighting Nyquist Zones

> [!code]- MATLAB
> ```matlab
> % Under-sampled bandpass signal showing multiple Nyquist zones
> B  = 4;   % bandwidth
> Fs = 2*B; % sampling at 2B
> 
> % All aliases within visualization range
> freqs = [-17, -15, -9, -7, -1, 1, 7, 9, 15, 17];
> amps  = 0.5 * ones(size(freqs));
> 
> % Different colors for different zones
> colors = {{'w'},{'w'}, {'g'},{'g'}, {'m'},{'m'}, ...
>           {'g'},{'g'}, {'w'},{'w'}};
> 
> fig = plot_spectrum(freqs, amps, ...
>     'XRange', [-20, 20], ...
>     'YMax', 0.75, ...
>     'XLabel', 'Frequency (kHz)', ...
>     'Title', 'Under-Sampling: Multiple Nyquist Zones', ...
>     'Colors', colors);
> 
> % Add reference lines at Nyquist zone boundaries
> figure(fig); hold on;
> xline(0,   '--', 'LineWidth', 1.5, 'Color', [0.8 0.8 0.8]);
> xline(Fs/2, '--', 'LineWidth', 1.5, 'Color', [0.8 0.8 0.8]);
> xline(-Fs/2,'--', 'LineWidth', 1.5, 'Color', [0.8 0.8 0.8]);
> hold off;
> ```

---

### Example 2: Comparing Theoretical vs FFT Results

> [!code]- MATLAB
> ```matlab
> % Theoretical prediction
> freqs_theory = [-17, -15, 15, 17];
> amps_theory  = [0.25, 0.25, 0.25, 0.25];
> 
> figure('Position', [100, 100, 1200, 400]);
> 
> subplot(1,2,1);
> plot_spectrum(freqs_theory, amps_theory, ...
>     'XRange', [-20, 20], ...
>     'Title', 'Theoretical Spectrum', ...
>     'FigNum', gcf);
> 
> subplot(1,2,2);
> % Your FFT code here
> stem(f_fft, mag_fft, 'filled');
> title('Computed FFT Spectrum');
> xlim([-20 20]);
> grid on;
> ```

---

### Example 3: Filter Specifications

> [!code]- MATLAB
> ```matlab
> % Ideal bandpass filter specification
> fp1 = 2;   % passband start
> fp2 = 8;   % passband end
> 
> % Show passband with unit gain, stopband with zero
> freqs = [fp1, fp2];
> amps  = [1, 1];
> 
> plot_spectrum(freqs, amps, ...
>     'XRange', [0, 12], ...
>     'YMax', 1.2, ...
>     'Title', 'Ideal Bandpass Filter Specification', ...
>     'XLabel', 'Frequency (kHz)', ...
>     'Colors', {{'green'}, {'green'}});
> ```

---

## 18.5 Quick Spectrum Templates

Helper file `spectrum_templates.m`:

> [!code]- MATLAB
> ```matlab
> function fig = spectrum_templates(type, varargin)
> %SPECTRUM_TEMPLATES Quick theoretical spectrum patterns
> %   spectrum_templates('AM', fc, fm)        - AM signal
> %   spectrum_templates('baseband', f0)      - Symmetric baseband
> %   spectrum_templates('harmonics', f0, n)  - Harmonic series
> %   spectrum_templates('aliased', f0, Fs)   - Aliasing demonstration
> 
> switch lower(type)
>     case 'am'
>         fc = varargin{1};  % carrier frequency (kHz)
>         fm = varargin{2};  % modulation frequency (kHz)
>         
>         freqs = [-(fc+fm), -(fc-fm), fc-fm, fc+fm];
>         amps  = [0.25, 0.25, 0.25, 0.25];
>         
>         fig = plot_spectrum(freqs, amps, ...
>             'XLabel', 'Frequency (kHz)', ...
>             'Title', sprintf('AM: f_c = %d kHz, f_m = %d kHz', fc, fm), ...
>             'Colors', {{'red'}, {'red'}, {'blue'}, {'blue'}});
>     
>     case 'baseband'
>         f0 = varargin{1};
>         
>         freqs = [-f0, f0];
>         amps  = [0.5, 0.5];
>         
>         fig = plot_spectrum(freqs, amps, ...
>             'XLabel', 'Frequency (kHz)', ...
>             'Title', sprintf('Baseband Signal: ±%d kHz', f0), ...
>             'Colors', {{'cyan'}, {'cyan'}});
>     
>     case 'harmonics'
>         f0 = varargin{1};
>         n  = varargin{2};  % number of harmonics
>         
>         freqs = f0 * (1:n);
>         amps  = 1 ./ (1:n);  % decreasing amplitude
>         
>         fig = plot_spectrum(freqs, amps, ...
>             'XLabel', 'Frequency (kHz)', ...
>             'Title', sprintf('%d Harmonics of f_0 = %d kHz', n, f0));
>     
>     case 'aliased'
>         f0 = varargin{1};
>         Fs = varargin{2};
>         
>         % Original + first two aliases
>         freqs = [f0, Fs-f0, Fs+f0];
>         amps  = [1, 1, 1];
>         
>         fig = plot_spectrum(freqs, amps, ...
>             'XRange', [0, 1.5*Fs], ...
>             'XLabel', 'Frequency (kHz)', ...
>             'Title', sprintf('Aliasing: f_0 = %d kHz, F_s = %d kHz', f0, Fs));
>         
>         % Add Nyquist frequency line
>         figure(fig); hold on;
>         xline(Fs/2, 'r--', 'LineWidth', 2);
>         text(Fs/2, 0.5, 'F_s/2', 'Color', 'r', ...
>              'HorizontalAlignment','center', ...
>              'VerticalAlignment','bottom');
>         hold off;
>     
>     otherwise
>         error('Unknown template type: %s', type);
> end
> end
> ```

### Using Templates

> [!code]- MATLAB
> ```matlab
> % Quick AM spectrum
> spectrum_templates('AM', 16, 1);
> 
> % Baseband signal
> spectrum_templates('baseband', 5);
> 
> % Harmonic series
> spectrum_templates('harmonics', 1, 5);
> 
> % Aliasing demo
> spectrum_templates('aliased', 7, 10);
> ```

---

## 18.6 Generic Plot Template (Copy-Paste)

> [!code]- MATLAB
> ```matlab
> %% ===== SPECTRUM PLOT TEMPLATE =====
> 
> % 1. Define spectrum
> frequencies = [___];  % your frequency values
> amplitudes  = [___];  % your amplitude values
> 
> % 2. Plot with options
> plot_spectrum(frequencies, amplitudes, ...
>     'XRange', [___, ___], ...           % [min, max]
>     'YMax', ___, ...                    % max amplitude
>     'XLabel', '___', ...                % x-axis label
>     'YLabel', '___', ...                % y-axis label  
>     'Title', '___', ...                 % plot title
>     'Colors', {{___}, {___}, ...}, ...  % colors per arrow
>     'XStep', ___, ...                   % tick spacing
>     'YStep', ___, ...                   % y-tick spacing
>     'MaxXLabels', ___, ...              % label thinning
>     'LineWidth', ___ ...                % arrow width
> );
> 
> % 3. Optional: Add reference lines
> hold on;
> xline(0, '--', 'Color', [0.8 0.8 0.8]);
> hold off;
> 
> % 4. Optional: Save
> exportgraphics(gcf, 'spectrum.png', 'Resolution', 300);
> ```

---

## 18.7 When to Use plot_spectrum vs FFT Plots

### Use `plot_spectrum()` for:

- Theoretical predictions (before computing anything)  
- Showing expected spectrum structure  
- Explaining concepts in reports  
- Filter specifications  
- Demonstrating aliasing effects  
- Textbook-style diagrams  

### Use FFT `stem()` plots for:

- Actual measured/computed spectra  
- Validating theoretical predictions  
- Showing all frequency bins  
- Demonstrating leakage/windowing effects  
- Real-world signal analysis  

### Often Use BOTH:

Show theoretical spectrum first, then FFT result to validate.

---

## 18.8 Common DSP Spectrum Patterns

> [!code]- MATLAB
> ```matlab
> % Pattern: Single Tone
> plot_spectrum(440, 1, 'XLabel', 'Frequency (Hz)');
> 
> % Pattern: Complex Exponential
> % e^(j2πf₀t) has only positive frequency
> plot_spectrum(5, 1, 'XRange', [-10, 10]);
> 
> % Pattern: Real Cosine (Symmetric)
> % cos(2πf₀t) has both ±f₀
> plot_spectrum([-5, 5], [0.5, 0.5]);
> 
> % Pattern: DSB-SC Modulation
> fc = 10; fm = 1;
> plot_spectrum([fc-fm, fc+fm], [0.5, 0.5]);
> 
> % Pattern: Rectangular Pulse Train
> % Sinc envelope sampled at harmonics
> f0 = 1;
> n_harmonics = 5;
> freqs = f0 * (1:2:2*n_harmonics);  % odd harmonics
> amps = sinc(freqs/10);             % sinc envelope
> 
> plot_spectrum(freqs, amps);
> ```

---

## 18.9 Integration with Your DSP Workflow

### Typical Usage in Assignments

> [!code]- MATLAB
> ```matlab
> %% Exercise: AM Signal Analysis
> clear; close all; clc;
> addpath('..\Helpers');
> 
> % Parameters
> Fdata = 1000;    % 1 kHz
> Fcar  = 16000;   % 16 kHz
> 
> %% Part A: Theoretical Spectrum
> F1 = Fcar - Fdata;  % 15 kHz
> F2 = Fcar + Fdata;  % 17 kHz
> 
> freqs = [-F2, -F1, F1, F2] / 1000;  % convert to kHz
> amps  = [0.25, 0.25, 0.25, 0.25];
> 
> plot_spectrum(freqs, amps, ...
>     'XRange', [-20, 20], ...
>     'XLabel', 'Frequency (kHz)', ...
>     'Title', 'Theoretical AM Spectrum');
> 
> exportgraphics(gcf, 'theory_spectrum.png', 'Resolution', 300);
> 
> %% Part B: Compute FFT for Validation
> Fs = 100e3;
> N  = 8192;
> t  = (0:N-1)/Fs;
> 
> x = cos(2*pi*Fdata*t) .* cos(2*pi*Fcar*t);
> 
> X = fftshift(fft(x));
> f = (-N/2:N/2-1) * (Fs/N) / 1000;  % kHz
> 
> figure;
> stem(f, abs(X)/N, 'filled');
> xlim([-20, 20]);
> title('Computed FFT Spectrum');
> xlabel('Frequency (kHz)');
> grid on;
> 
> exportgraphics(gcf, 'fft_spectrum.png', 'Resolution', 300);
> ```

---

## 18.10 Spectrum Plotting Cheat Sheet

| Task              | Code                                                |
|-------------------|-----------------------------------------------------|
| Basic plot        | `plot_spectrum(freqs, amps)`                        |
| Set range         | `'XRange', [-10, 10]`                               |
| Color arrows      | `'Colors', {{'r'}, {'b'}}`                          |
| Add title         | `'Title', 'My Spectrum'`                            |
| Thick arrows      | `'LineWidth', 3`                                    |
| Limit labels      | `'MaxXLabels', 10`                                  |
| Update existing   | `'FigNum', 5`                                       |
| Save figure       | `exportgraphics(gcf, 'fig.png', 'Resolution', 300)` |

---

## 18.11 Troubleshooting

- **"Undefined function 'plot_spectrum'"**  
  → Check `plot_spectrum.m` is on the MATLAB path.

- **Arrows don't show**  
  → Make sure amplitudes > 0 and within `YMax` range.

- **Too many axis labels (cluttered)**  
  → Reduce tick spacing or use `'MaxXLabels', 8`.

- **Colors not working**  
  → Use cell-of-cells: `{{'red'}, {'blue'}}` not `{'red', 'blue'}`.

- **Frequencies and amplitudes length mismatch**  
  → Check `length(freqs) == length(amps)`.

---

## 18.12 MATLAB Toolbox Summary

> [!code]- MATLAB
> ```matlab
> % Basic usage
> plot_spectrum(frequencies, amplitudes);
> 
> % Full options
> fig = plot_spectrum(frequencies, amplitudes, ...
>     'XRange', [min, max], ...
>     'YMax', max_amp, ...
>     'XLabel', 'label', ...
>     'Title', 'title', ...
>     'Colors', {{color1}, {color2}, ...});
> 
> % Templates (if created)
> spectrum_templates('AM', fc, fm);
> spectrum_templates('baseband', f0);
> spectrum_templates('harmonics', f0, n);
> spectrum_templates('aliased', f0, Fs);
> ```
