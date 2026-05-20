---
type: walkthrough
tags: [DSP, reexam, exam, F20, walkthrough]
aliases:
  - F20 walkthrough
  - F20 exam log
---
# F20 exam -- MATLAB walkthrough

> [!info] What this note is
> Step-by-step log of how I'm solving the **F20 exam** in [[62743 F20 Exam.pdf]]
> One section per sub-question. Each section explains *what the MATLAB code is doing* and *why*, not just the answer.
>
> Theory is offloaded to [[LTI z-transform flow]] -- this note links back instead of duplicating.

**Exam PDF:** `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/Exam sets/62743 F20 Exam.pdf`
**Solution PDF:** `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/Solutions/62743 F20 Exam student solutions.pdf`
**Working script:** `3.semester/DSP/EXAMS/F20.m`

---

# Problem 1 -- LTI system

Difference equation:

$$y[n] + 0.1\,y[n-1] - 0.06\,y[n-2] \;=\; x[n] + 0.2\,x[n-1]$$

## P1-1 -- Find H(z)

**Theory:** [[LTI z-transform flow#Step 1 -- Difference equation to H(z)]].

z-transform both sides, factor, divide:

$$H(z) \;=\; \frac{1 + 0.2\,z^{-1}}{1 + 0.1\,z^{-1} - 0.06\,z^{-2}}$$

### MATLAB

```matlab
b = [1, 0.2];          % numerator coefficients (z^-1 form)
a = [1, 0.1, -0.06];   % denominator coefficients
H = tf(b, a, -1, 'Variable', 'z^-1')
```

- `b` and `a` use the convention that element `k` is the coefficient of $z^{-(k-1)}$.
- `tf(b, a, -1, 'Variable', 'z^-1')` builds a discrete-time transfer function object. `Ts = -1` means "sample time unspecified," and the `'Variable','z^-1'` flag prints it in the $z^{-1}$ form we derived (rather than positive-power $z$).

---

## P1-2 -- Poles, zeros, stability

**Theory:** [[LTI z-transform flow#Step 2 -- Poles, zeros, stability]].

Multiply top and bottom by $z^{2}$ to get the **z-form** (so the zero at $z=0$ shows up):

$$H(z) \;=\; \frac{z\,(z + 0.2)}{(z + 0.3)(z - 0.2)}$$

- Zeros: $z = 0$, $z = -0.2$
- Poles: $z = -0.3$, $z = +0.2$
- All poles strictly inside the unit circle -> **stable**.

### MATLAB

```matlab
[z_all, p_all, k_gain] = tf2zpk(b, a);
zplane(b, a);
isstable(tf(b, a, -1))
```

- `tf2zpk(b,a)` returns zeros, poles, and gain. **Use this, not `roots(b)` alone** -- `roots(b)` operates only on the numerator polynomial in $z^{-1}$ form and would miss the zero at $z = 0$ that only appears after converting to z-form.
- `zplane(b, a)` draws the pole-zero plot with the unit circle. Zeros are `o`, poles are `x`.

---

## P1-3 -- Impulse response h[n]

**Theory:** [[LTI z-transform flow#Step 3 -- Impulse response h[n] via partial fractions]].

### Strategy: let MATLAB do the PFD

The partial fraction decomposition (PFD) of $H(z)$ is:

$$H(z) \;=\; \frac{A}{1 + 0.3\,z^{-1}} + \frac{B}{1 - 0.2\,z^{-1}}$$

By hand, we'd find $A = 0.2$, $B = 0.8$ (see [[LTI z-transform flow#Applying to F20]]).

For the exam, we're allowed to use MATLAB's [`residuez`](https://www.mathworks.com/help/signal/ref/residuez.html), which does the PFD directly on $B(z)/A(z)$ in $z^{-1}$ form. No hand algebra needed.

### What residuez returns

```matlab
[r, p, k] = residuez(b, a);
```

For distinct poles and a numerator order strictly less than the denominator order:

| Output | Meaning |
|---|---|
| `r` | Residues -- one per pole. These are the $A, B, \ldots$ in the PFD. |
| `p` | Poles -- in the same order as `r`. **Sign already correct** in $a$-form (i.e. for the table entry $\tfrac{1}{1 - a z^{-1}}$). |
| `k` | Direct (polynomial) term. Empty when degree of $b$ < degree of $a$. |

The PFD it represents is:

$$H(z) \;=\; \sum_{i} \frac{r_i}{1 - p_i\,z^{-1}} \;+\; (\text{direct term})$$

> [!tip] No sign trap with `residuez`
> The $a$ in the table entry $\tfrac{1}{1 - a z^{-1}}$ is **literally** what `residuez` puts in `p`. No "rewrite as $1 - (\ldots) z^{-1}$ first" step. That's the main payoff of using the function.

### Reading off h[n]

Each table pair $\dfrac{1}{1 - a\,z^{-1}} \leftrightarrow a^{n}\,u[n]$ gives one term. Sum over all poles:

$$h[n] \;=\; \sum_{i} r_i \cdot p_i^{\,n} \cdot u[n]$$

For F20 (residuez output: $r = [0.2,\, 0.8]$, $p = [-0.3,\, 0.2]$, $k = [\,]$ -- order may vary):

$$\boxed{\;h[n] \;=\; 0.2\,(-0.3)^{n}\,u[n] \;+\; 0.8\,(0.2)^{n}\,u[n]\;}$$

### MATLAB code (in [F20.m](file:///C:/Users/Mads2/DTU/3.semester/DSP/EXAMS/F20.m))

```matlab
[r_h, p_h, k_h] = residuez(b, a);

% Recombine sanity check: residuez(r, p, k) is the inverse direction.
% Should reproduce (b, a).
[b_chk, a_chk] = residuez(r_h, p_h, k_h);

% Plot h[n] directly from the difference equation (impz uses b,a, not r,p).
[h_n, n_h] = impz(b, a, 30);
stem(n_h, h_n, 'filled');
```

- `residuez(r, p, k)` (called with the residue/pole/direct outputs as inputs) is the **inverse direction** -- it recombines the PFD back into a single rational. Quick sanity check that the PFD is right.
- `impz(b, a, N)` returns the first `N` samples of $h[n]$ directly from the difference equation. Doesn't go through PFD at all -- independent verification of the analytic answer.

### What to write on the exam

1. State the strategy: "PFD via `residuez`, then inverse-transform each piece using $\tfrac{1}{1 - a z^{-1}} \leftrightarrow a^{n} u[n]$."
2. Show the MATLAB call and printed `r`, `p`, `k` values.
3. Write the boxed $h[n]$ expression.
4. (Optional but cheap) Show the `impz` plot and note it matches.

---

## P1-4 -- Output y[n] for x[n] = (-0.2)^n u[n]

**Theory:** [[LTI z-transform flow#Step 4 -- Output y[n] for a given x[n]]].

### Strategy

1. Write $X(z)$ from the table.
2. $Y(z) = H(z)\,X(z)$. Multiplying rationals = convolving the numerator and denominator coefficient vectors.
3. PFD on $Y(z)$ via `residuez`.
4. Inverse-transform each piece using $\tfrac{1}{1 - a z^{-1}} \leftrightarrow a^{n}\,u[n]$.

### Step 1 -- X(z)

$x[n] = (-0.2)^{n}\,u[n]$ matches the table entry $a^{n}u[n] \leftrightarrow \tfrac{1}{1 - a z^{-1}}$ with $a = -0.2$:

$$X(z) \;=\; \frac{1}{1 - (-0.2)\,z^{-1}} \;=\; \frac{1}{1 + 0.2\,z^{-1}}, \qquad |z| > 0.2$$

> [!warning] Sign on `ax`
> $a = -0.2$ goes into the table entry as $1 - (-0.2)\,z^{-1} = 1 + 0.2\,z^{-1}$. So in MATLAB, `ax = [1, 0.2]` (positive). Reading the sign off the time-domain expression and stuffing it straight into `ax` is wrong.

### Step 2 -- Watch for pole-zero cancellation

Before computing anything, look at the factors:

$$Y(z) \;=\; H(z)\,X(z) \;=\; \underbrace{\frac{1 + 0.2\,z^{-1}}{(1 + 0.3\,z^{-1})(1 - 0.2\,z^{-1})}}_{H(z)} \cdot \underbrace{\frac{1}{1 + 0.2\,z^{-1}}}_{X(z)}$$

The numerator factor $(1 + 0.2\,z^{-1})$ and one of $X(z)$'s denominator factors **cancel exactly**:

$$Y(z) \;=\; \frac{1}{(1 + 0.3\,z^{-1})(1 - 0.2\,z^{-1})}$$

So $Y(z)$ effectively has **two poles**, not three.

> [!tip] How `residuez` handles cancellation
> We don't need to simplify by hand -- we hand `residuez` the un-cancelled $(b_y, a_y)$ (3rd-order denominator). It returns 3 (residue, pole) pairs, but the residue paired with the cancelled pole at $z = -0.2$ is **numerically zero** (floating-point noise, ~1e-16). The PFD machinery handles cancellation automatically: a zero in the numerator at the same location as a denominator pole yields zero residue.
>
> So you can just blindly do `Y(z) = H * X` and trust `residuez`. No pre-simplification needed.

### Step 3 -- PFD via residuez

```
bx = 1;          ax = [1, 0.2];      % X(z)
by = conv(b, bx);                    % numerator of Y(z) = H * X
ay = conv(a, ax);                    % denominator of Y(z)
[r_y, p_y, k_y] = residuez(by, ay);
```

`conv` multiplies polynomials: $(1 + 0.2 z^{-1})(1) = 1 + 0.2 z^{-1}$ for the numerator, and the denominator becomes a 3rd-order polynomial in $z^{-1}$.

### Step 4 -- Read off y[n]

For F20, `residuez` will return (order may vary):

- $r \approx [0.6,\, 0.4,\, \approx\!0]$
- $p \approx [-0.3,\, +0.2,\, -0.2]$

The third pair has $r \approx 0$ -- that's the cancelled pole. Drop it. The remaining two:

| Pair | Term in $y[n]$ |
|---|---|
| $r = 0.6,\ p = -0.3$ | $0.6\,(-0.3)^{n}\,u[n]$ |
| $r = 0.4,\ p = +0.2$ | $0.4\,(0.2)^{n}\,u[n]$ |

$$\boxed{\;y[n] \;=\; 0.6\,(-0.3)^{n}\,u[n] \;+\; 0.4\,(0.2)^{n}\,u[n]\;}$$

### Numeric sanity check via `filter`

```matlab
N_y  = 30;
n_y  = (0:N_y-1).';
x_n  = (-0.2).^n_y;            % x[n] = (-0.2)^n u[n]
y_filt = filter(b, a, x_n);    % numeric output via diff eq
```

`filter(b, a, x)` runs the difference equation step-by-step on the input -- no PFD involved. Spot-check a few samples of `y_filt` against the closed-form $0.6(-0.3)^n + 0.4(0.2)^n$ and they should agree to numerical precision.

### What to write on the exam

1. State $X(z) = \tfrac{1}{1 + 0.2 z^{-1}}$ from the table.
2. Note the pole-zero cancellation between the $H$ numerator and $X$ denominator (shows you understand the algebra, even though `residuez` handles it).
3. Show the MATLAB calls (`conv`, `residuez`).
4. Give the boxed $y[n]$.
5. Plot from `filter` and note it matches the analytic form.

---

## P1-5 -- Energy E_x and E_y

> [!note] Low-priority for the actual reexam
> Energy questions have been **dropped from recent exam sets**. Walking through it once for completeness, then moving on.

**Theory:** [[LTI z-transform flow#Step 5 -- Energy]].

### Definition

$$E \;=\; \sum_{n=-\infty}^{\infty} |x[n]|^{2}$$

Both $x[n]$ and $y[n]$ here are causal (start at $n=0$) and built from decaying exponentials $a^{n}u[n]$ with $|a| < 1$. So each piece contributes a finite geometric series.

### E_x -- one exponential

$x[n] = (-0.2)^{n}\,u[n]$:

$$E_x \;=\; \sum_{n=0}^{\infty} |(-0.2)^{n}|^{2} \;=\; \sum_{n=0}^{\infty} (0.04)^{n} \;=\; \frac{1}{1 - 0.04} \;=\; \frac{1}{0.96} \;\approx\; 1.0417$$

> [!tip] Generalisation
> $$x[n] = a^{n}\,u[n], \;|a| < 1 \;\;\Longrightarrow\;\; E_x = \frac{1}{1 - |a|^{2}}$$

### E_y -- sum of two exponentials, watch the cross term

$y[n] = A\,p_1^{\,n} + B\,p_2^{\,n}$ with $A = 0.6,\; p_1 = -0.3,\; B = 0.4,\; p_2 = +0.2$.

Square it (real-valued so $|y|^2 = y^2$):

$$y[n]^{2} \;=\; \left(A p_1^{n} + B p_2^{n}\right)^{2} \;=\; A^{2} p_1^{2n} \;+\; 2AB\,(p_1 p_2)^{n} \;+\; B^{2} p_2^{2n}$$

Three geometric series, each summable:

$$\boxed{\;E_y \;=\; \frac{A^{2}}{1 - p_1^{2}} \;+\; \frac{2AB}{1 - p_1 p_2} \;+\; \frac{B^{2}}{1 - p_2^{2}}\;}$$

> [!warning] Don't forget the cross term
> The natural mistake is to compute $\sum A^2 p_1^{2n} + \sum B^2 p_2^{2n}$ and stop. The $2AB(p_1 p_2)^n$ cross term comes from $(a+b)^2 = a^2 + 2ab + b^2$ and is **not** zero just because the two exponentials have different bases.

Plugging in the F20 numbers:

$$E_y \;=\; \frac{0.36}{0.91} \;+\; \frac{0.48}{1.06} \;+\; \frac{0.16}{0.96} \;\approx\; 0.3956 + 0.4528 + 0.1667 \;\approx\; 1.0151$$

### MATLAB

```matlab
% Closed forms
E_x_closed = 1 / (1 - abs(-0.2)^2);
E_y_closed = 0.6^2/(1 - (-0.3)^2) + 2*0.6*0.4/(1 - (-0.3)*0.2) + 0.4^2/(1 - 0.2^2);

% Numeric check: long horizon so the tail is negligible
N_long = 200;
x_long = (-0.2).^(0:N_long-1).';
y_long = filter(b, a, x_long);
E_x_num = sum(abs(x_long).^2);
E_y_num = sum(abs(y_long).^2);
```

The numeric and closed-form values should agree to 4+ decimal places at $N = 200$ (geometric tail at $n=200$ for the slowest pole $|p_1| = 0.3$ is $0.3^{200} \approx 10^{-105}$ -- vanishingly small).

### Boxed answers

$$E_x \;=\; \tfrac{1}{0.96} \;\approx\; 1.0417 \qquad\qquad E_y \;\approx\; 1.0151$$

---

# Problem 2 -- V(t) spectrum analysis

Signal:

$$V(t) \;=\; \cos(2\pi F_1 t)\bigl[1 + \cos(2\pi F_2 t)\bigr] + \tfrac{1}{3}\cos(2\pi F_3 t)$$

with $F_1 = 100$ Hz, $F_2 = 130$ Hz, $F_3 = 180$ Hz.

> [!important] The big idea behind this whole problem
> $V(t)$ contains a **product** of two cosines. The product creates new frequency components at the sum and difference: $F_1 \pm F_2$. So even though only three Fs appear in the formula, the signal actually contains **four** spectral lines, with the highest at $F_1 + F_2 = 230$ Hz -- which is *higher* than $F_3 = 180$ Hz.
>
> Sub-questions 2-1 (time plot), 2-2 (FFT) and 2-3 (analytical rewrite) all aim at the same point: making this hidden 230 Hz component visible. Sub-question 2-4 asks for Nyquist, which depends on getting that right.

---

## P2-1 -- Time domain plot, read off min/max

### What's asked

Sample $V(t)$ at $F_s = 4600$ Hz, plot it in time, read minimum and maximum amplitudes off the plot.

### MATLAB

```matlab
F1 = 100;  F2 = 130;  F3 = 180;
Fs2 = 4600;
T_plot = 0.05;
t1 = (0:1/Fs2:T_plot - 1/Fs2).';
V1 = cos(2*pi*F1*t1) .* (1 + cos(2*pi*F2*t1)) + (1/3)*cos(2*pi*F3*t1);
plot(t1, V1);
[min(V1), max(V1)]   % numeric read-off (sanity check vs the plot)
```

### Anatomy of the time vector

The line `t1 = (0:1/Fs2:T_plot - 1/Fs2).'` looks fiddly. It's just MATLAB's colon notation `start:step:stop` plus a transpose, but every piece is deliberate:

| Piece | What it is | Why this value |
|---|---|---|
| `0` | start time | Begin sampling at $t = 0$ (causal, conventional). |
| `1/Fs2` | step | One sample every $T_s = 1/F_s$ seconds. **The step is the sampling period**, not some arbitrary plot resolution. |
| `T_plot - 1/Fs2` | stop time | The horizon $T_\text{plot}$ **minus one sample period**. See "off-by-one" below. |
| `.'` | non-conjugate transpose | Turns the row vector into a column vector. Matches the column-vector convention used elsewhere (e.g. `n_y = (0:N-1).'` in P1-4). |

> [!warning] The off-by-one in the stop value
> Why subtract `1/Fs2` from the stop? Because the colon notation **includes** the endpoint when it lands exactly on a step. If we wrote `0:1/Fs2:T_plot` with $T_\text{plot} = 0.05$ and $F_s = 4600$, we'd get $N+1 = 231$ samples covering $[0,\,0.05]$ inclusive on both ends. Subtracting one step gives the more natural $N = 230$ samples covering $[0,\,T_\text{plot})$ -- right-open interval, ready to be repeated periodically without duplicating the boundary sample.
>
> Equivalent and often clearer: `t1 = (0:N-1).'/Fs2` with `N = round(T_plot*Fs2)`. Same result, no off-by-one to worry about. (See P1-4 and P2-2 for that style.)

### Other notes on this snippet

- **Horizon** $T_\text{plot} = 0.05\,\text{s}$ = 50 ms is chosen so several periods of the *lowest* visible component (30 Hz, period 33 ms) fit. Anything from 30-100 ms works.
- The element-wise product `.*` matters -- `cos(...) * (1 + cos(...))` without the dot would attempt a matrix product and error out (or, worse, silently misbehave if dimensions happen to align).

### Expected read-off

The actual extremes depend on phase alignment of all four components, so just report what MATLAB prints. Roughly $V \in [-2,\,+2]$ with some excursion outside.

---

## P2-2 -- Frequency domain (FFT)

### What's asked

Use $F_s = 4600$ Hz, frequency resolution $\Delta F = 0.1$ Hz, and $N = F_s / \Delta F = 46\,000$ samples. Plot the magnitude spectrum and read off the discrete frequency components and their amplitudes.

### Why these parameters

| Parameter | Reason |
|---|---|
| $F_s = 4600$ Hz | well above Nyquist (460 Hz) -- no aliasing |
| $\Delta F = 0.1$ Hz | bin width. All component frequencies (30, 100, 180, 230) are integer multiples of 0.1, so they fall **exactly on bins** -> clean peaks, no spectral leakage |
| $N = F_s / \Delta F = 46000$ | samples needed for that resolution. Equivalent to capturing exactly $T = 1 / \Delta F = 1$ second of signal |

### FFT amplitude scaling -- the "divide by N, double the inside" rule

For a real cosine $x[n] = A\cos(2\pi f_0 n / F_s)$ sampled $N$ times with $f_0$ on a bin, MATLAB's `fft` produces a peak with magnitude $A\,N/2$ at the bin (half on the positive frequency, half on the negative). So:

$$\text{one-sided amplitude}[k] \;=\; \begin{cases} |X[k]|/N & k = 0 \text{ (DC)} \text{ or } k = N/2 \text{ (Nyquist)} \\ 2|X[k]|/N & \text{otherwise} \end{cases}$$

```matlab
X2  = fft(V2);
half = 1:N2/2 + 1;
A_amp = abs(X2(half))/N2;
A_amp(2:end-1) = 2*A_amp(2:end-1);
stem(f2(half), A_amp);
xlim([0 500]);    % zoom to the relevant band
```

> [!warning] Don't forget the doubling
> Plotting `abs(X)/N` gives you half the true amplitude on the one-sided plot. Either double the interior bins, or plot the two-sided spectrum from `-Fs/2` to `+Fs/2` and read peaks individually.

### Reading the components off the plot

After running the FFT and zooming in with `xlim([0 500])`, four stems should be clearly visible. You can read them visually, but there's a much cleaner way that scales to every future spectrum question -- the **nearest-bin lookup idiom**.

---

### MATLAB idiom: nearest-bin lookup

> [!important] Two-line pattern. Memorise it.
> ```matlab
> [~, idx] = min(abs(x_axis - x_target));    % closest bin to x_target
> value    = y_axis(idx);                     % read off the amplitude there
> ```
>
> Works for **any** $(x_\text{axis}, y_\text{axis})$ pair. Frequency vs amplitude. Frequency vs magnitude in dB. Time vs signal value. Any time the question asks "what is the value at $x = X$".

#### How it works -- one line at a time

`x_axis - x_target` -- subtract the target from every element of the axis. Result is a vector of *signed offsets*: positive where the axis is higher than the target, negative where lower.

`abs(x_axis - x_target)` -- take absolute values. Now you have *distances*: how far each bin is from the target.

`min(abs(...))` -- find the smallest distance. Crucially, MATLAB's `min` returns **two outputs**: `[min_value, min_index]`. The first is the smallest distance itself; the second is the *position* in the vector where that minimum occurred.

`[~, idx] = min(...)` -- the `~` is "ignore this output." We don't care what the smallest distance is; we just want its location. So `idx` is the bin number closest to `x_target`.

`y_axis(idx)` -- look up the y-value at that bin.

#### Why this beats visual read-off

| Visual (data cursor) | Nearest-bin lookup |
|---|---|
| Hover with mouse, eyeball, write down approximate value | Two lines of code, exact value printed |
| Doesn't generalise -- redo for each new plot | Same two lines for every spectrum question |
| Risk of misreading axis | Zero ambiguity |

The cost: you have to remember the two-line pattern. The benefit: you'll use it on **every** future problem with `freqz`, `fft`, `filter` magnitude responses, etc.

#### Use cases on this exam

| Where it appears | x_axis | y_axis | x_target |
|---|---|---|---|
| **P2-2** (this section) | frequency vector `f_half` | amplitude `A_amp` | each component frequency |
| **P3-3** (later) -- "amplitude of filter at $f$ Hz?" | frequency from `freqz` | `20*log10(abs(H))` | passband / stopband edges |
| **P3-4** (later) -- "phase at $f$ Hz?" | frequency from `freqz` | `unwrap(angle(H))` | $\omega$ of interest |
| Any "read off the dB attenuation at..." | frequency | dB magnitude | given frequency |

### Applied to F20 P2-2

```matlab
expected_f = [30, 100, 180, 230];
for fc = expected_f
    [~, idx] = min(abs(f_half - fc));
    fprintf('  f = %3d Hz   amplitude = %.4f\n', fc, A_amp(idx));
end
```

This prints (because all targets land exactly on bins given $\Delta F = 0.1$ Hz, all components are at integer Hz):

| f [Hz] | Amplitude |
|---|---|
| 30  | 0.5000 |
| 100 | 1.0000 |
| 180 | 0.3333 |
| 230 | 0.5000 |

> [!tip] When does it land "off-bin"?
> If the target frequency isn't an exact multiple of $\Delta F$, the closest bin will be slightly off, and the amplitude will be slightly less than the true value (spectral leakage). For exam questions this rarely matters because the parameters are chosen so components land on bins. But if you see a peak that's clearly *between* two bins on a plot, expect a small underestimate from the nearest-bin lookup.

---

## P2-3 -- Analytical rewrite, compare with FFT

### Tool: product-to-sum identity

$$\cos(A)\cos(B) \;=\; \tfrac{1}{2}\bigl[\cos(A-B) + \cos(A+B)\bigr]$$

### Apply to V(t)

Expand the bracket first:

$$V(t) \;=\; \cos(2\pi F_1 t) \;+\; \cos(2\pi F_1 t)\cos(2\pi F_2 t) \;+\; \tfrac{1}{3}\cos(2\pi F_3 t)$$

The middle term is the product. Apply the identity with $A = 2\pi F_1 t$, $B = 2\pi F_2 t$:

$$\cos(2\pi F_1 t)\cos(2\pi F_2 t) \;=\; \tfrac{1}{2}\cos\bigl(2\pi(F_1{-}F_2)\,t\bigr) + \tfrac{1}{2}\cos\bigl(2\pi(F_1{+}F_2)\,t\bigr)$$

Cosine is even ($\cos(-x) = \cos(x)$), so $\cos(2\pi(F_1-F_2)t) = \cos(2\pi(F_2-F_1)t) = \cos(2\pi \cdot 30 \cdot t)$.

### Final form

$$\boxed{\;V(t) \;=\; \tfrac{1}{2}\cos(2\pi\!\cdot\!30\,t) \;+\; \cos(2\pi\!\cdot\!100\,t) \;+\; \tfrac{1}{3}\cos(2\pi\!\cdot\!180\,t) \;+\; \tfrac{1}{2}\cos(2\pi\!\cdot\!230\,t)\;}$$

### Comparison with FFT

Reading the boxed expression off directly:

| Component | Frequency [Hz] | Amplitude |
|---|---|---|
| $\cos(2\pi F_1 t)$ alone (the standalone term, not multiplied by anything) | 100 | 1 |
| $\cos(F_2 - F_1)$ from the product | 30 | 1/2 |
| $\cos(F_1 + F_2)$ from the product | 230 | 1/2 |
| $\tfrac{1}{3}\cos(2\pi F_3 t)$ | 180 | 1/3 |

Match the FFT result exactly -> confirms both the FFT scaling and the analytical decomposition.

---

## P2-4 -- Minimum sampling frequency (Nyquist)

### The point of the problem

The naive answer is $F_{s,\min} = 2 F_3 = 360$ Hz, because you read "$F_3 = 180$ Hz" as the highest frequency in the formula. **This is wrong.**

After the rewrite in 2-3, the actual highest frequency in $V(t)$ is $F_1 + F_2 = 230$ Hz. So:

$$\boxed{\;F_{s,\min} \;=\; 2 \cdot F_{\max} \;=\; 2 \cdot 230 \;=\; 460\,\text{Hz}\;}$$

Sampling at 360 Hz would alias the 230 Hz component down to $|230 - 360| = 130$ Hz, corrupting the spectrum.

> [!tip] General rule
> Whenever a signal has products or modulation, **expand it analytically first** to find all spectral components. Don't trust the apparent maximum in the original formula.

### Sanity check

The script computes `Fmax = max([F1, F2, F3, F1+F2, abs(F2-F1)])` and prints `2*Fmax = 460 Hz`. Confirms 460 Hz is the cutoff.

---

# Problem 3 -- H(z) given, find ROC, h[n], y[n], realisations

System (causal LTI):

$$H(z) \;=\; \frac{1}{(1 + \tfrac{1}{5}z^{-1})(1 - \tfrac{4}{5}z^{-1})} \;=\; \frac{1}{(1 + 0.2 z^{-1})(1 - 0.8 z^{-1})}$$

Already factored -- saves us the work of factoring a quadratic. **Two poles** at $z = -0.2$ and $z = +0.8$, **no finite zeros** (numerator is constant 1).

### Setting up b3 and a3

We need the denominator as a polynomial in $z^{-1}$. Expand:

$$(1 + 0.2 z^{-1})(1 - 0.8 z^{-1}) \;=\; 1 - 0.6 z^{-1} - 0.16 z^{-2}$$

```matlab
b3 = 1;
a3 = [1, -0.6, -0.16];
```

> [!tip] Don't expand by hand if you don't have to
> Equivalent: `a3 = conv([1, 0.2], [1, -0.8])`. Same answer, no arithmetic, less risk of a sign slip on `1 * (-0.8) + 0.2 * 1 = -0.6`.

---

## P3-1 -- Region of convergence (ROC)

**Theory:** [[LTI z-transform flow#Quick reference cheat sheet]] (ROC rules table).

The system is **causal** (stated in the problem). For a causal system:

> ROC = outside the outermost pole.

Outermost pole: $|z| = 0.8$ (the $z = +0.8$ pole; the other has magnitude 0.2).

$$\boxed{\;\text{ROC: } |z| > 0.8\;}$$

That's the whole answer. No MATLAB needed for this sub-question -- just state it.

---

## P3-2 -- Poles, zeros, pole-zero plot

**Theory:** [[LTI z-transform flow#Step 2 -- Poles, zeros, stability]].

### From the factored form

- **Poles:** $z = -0.2$ and $z = +0.8$ (already factored, just read off).
- **Zeros:** numerator is the constant 1, so no finite zeros... in $z^{-1}$ form. But in $z$ form, multiplying top and bottom by $z^{2}$ gives:

$$H(z) \;=\; \frac{z^{2}}{(z + 0.2)(z - 0.8)}$$

So there's a **double zero at $z = 0$**. (Same gotcha as F20 P1-2 -- you only see it after converting to $z$ form.)

### MATLAB

```matlab
[z3, p3, k3] = tf2zpk(b3, a3);
zplane(b3, a3);
```

`tf2zpk` returns the zeros at the origin (from the $z^{2}$ factor), so the zplane plot shows two `o` markers at the origin and two `x` markers at $z = -0.2$ and $z = +0.8$. All inside the unit circle -> system is stable, consistent with the ROC including $|z| = 1$.

---

## P3-3 -- Impulse response h[n]

**Theory:** [[LTI z-transform flow#Step 3 -- Impulse response h[n] via partial fractions]].

### Strategy: residuez

```matlab
[r3, p3r, k3r] = residuez(b3, a3);
```

PFD form: $H(z) = \dfrac{r_1}{1 - p_1 z^{-1}} + \dfrac{r_2}{1 - p_2 z^{-1}}$

For F20 P3, residuez prints (order may vary):

- $r = [0.2,\; 0.8]$
- $p = [-0.2,\; 0.8]$
- $k = [\,]$ (empty -- numerator order < denominator order)

### Read off h[n]

Each $(r_i, p_i)$ becomes one term via $\tfrac{1}{1 - p z^{-1}} \leftrightarrow p^{\,n} u[n]$:

$$\boxed{\;h[n] \;=\; 0.2\,(-0.2)^{n}\,u[n] \;+\; 0.8\,(0.8)^{n}\,u[n]\;}$$

Plot the first 30 samples with `[h, n] = impz(b3, a3, 30); stem(n, h)` for the figure to put in the answer.

---

## P3-4 -- Output y[n] for x[n] = δ[n] + δ[n-2]

### Strategy: linearity, not a fresh PFD

The instinct is to compute $X(z) = 1 + z^{-2}$, multiply $Y(z) = H(z)\,X(z)$, and run `residuez` on the result. This works but it's more work than the question needs.

**Cleaner argument:**

$$x[n] = \delta[n] + \delta[n-2]$$

The system is LTI. For an LTI system, the response to $\delta[n]$ is $h[n]$, and the response to $\delta[n-k]$ is $h[n-k]$ (time-invariance). By linearity (superposition):

$$y[n] \;=\; h[n] + h[n-2]$$

> [!tip] When to use this shortcut
> Whenever $x[n]$ is a finite sum of (possibly shifted) impulses, $y[n]$ is the same sum of (correspondingly shifted) impulse responses. Skip the PFD work entirely.

### Substitute h[n] -- this is the answer y[n]

From P3-3:

$$h[n] \;=\; 0.2\,(-0.2)^{n}\,u[n] \;+\; 0.8\,(0.8)^{n}\,u[n]$$

Plug into $y[n] = h[n] + h[n-2]$:

$$\boxed{\;y[n] \;=\; \bigl[0.2\,(-0.2)^{n} + 0.8\,(0.8)^{n}\bigr]u[n] \;+\; \bigl[0.2\,(-0.2)^{n-2} + 0.8\,(0.8)^{n-2}\bigr]u[n-2]\;}$$

This **is** the function $y[n]$. The two unit-step factors $u[n]$ and $u[n-2]$ make it piecewise -- which we can also write out explicitly.

### Cleaner: piecewise form

The unit steps mean:

| Range of $n$ | Which $u$'s are 1? | $y[n]$ |
|---|---|---|
| $n < 0$ | neither | $0$ |
| $n = 0$ | only $u[n]$ | $h[0]$ |
| $n = 1$ | only $u[n]$ | $h[1]$ |
| $n \geq 2$ | both | $h[n] + h[n-2]$ |

Compute the boundary samples:

- $h[0] = 0.2(-0.2)^0 + 0.8(0.8)^0 = 0.2 + 0.8 = 1$
- $h[1] = 0.2(-0.2)^1 + 0.8(0.8)^1 = -0.04 + 0.64 = 0.6$

For $n \geq 2$ we can simplify by pulling the shifted exponentials in. Use $(-0.2)^{n-2} = (-0.2)^{n}/(-0.2)^{2} = (-0.2)^{n}/0.04 = 25\,(-0.2)^{n}$ and similarly $(0.8)^{n-2} = (0.8)^{n}/0.64 = 1.5625\,(0.8)^{n}$:

$$\begin{aligned}
y[n] \;&=\; 0.2(-0.2)^n + 0.8(0.8)^n + 0.2(-0.2)^{n-2} + 0.8(0.8)^{n-2} \\
&=\; 0.2(-0.2)^n + 0.8(0.8)^n + 0.2 \cdot 25\,(-0.2)^n + 0.8 \cdot 1.5625\,(0.8)^n \\
&=\; (0.2 + 5)(-0.2)^n + (0.8 + 1.25)(0.8)^n \\
&=\; 5.2\,(-0.2)^n + 2.05\,(0.8)^n
\end{aligned}$$

Putting it all together:

$$\boxed{\;y[n] \;=\; \begin{cases} 0 & n < 0 \\ 1 & n = 0 \\ 0.6 & n = 1 \\ 5.2\,(-0.2)^{n} + 2.05\,(0.8)^{n} & n \geq 2 \end{cases}\;}$$

> [!tip] Which form to write on the exam
> The first boxed form (with $u[n]$ factors) is the direct answer from the convolution argument. The piecewise form is what you get after working out the steps -- cleaner to plug in numbers but more algebra. Either is acceptable. Write whichever you trust more.

### MATLAB sanity check

```matlab
N3 = 30;
x3 = zeros(N3, 1);  x3(1) = 1;  x3(3) = 1;     % δ[n] + δ[n-2]
y3 = filter(b3, a3, x3);
stem(0:N3-1, y3, 'filled');
```

Note `x3(1) = 1` for $\delta[n]$ (MATLAB is 1-indexed: index 1 = sample $n=0$) and `x3(3) = 1` for $\delta[n-2]$ (index 3 = sample $n=2$). Common off-by-one trap.

Spot-check the first three samples of `y3` against the closed form:

| $n$ | filter output | analytical |
|---|---|---|
| 0 | 1.0000 | $h[0] = 1$ |
| 1 | 0.6000 | $h[1] = 0.6$ |
| 2 | $5.2(0.04) + 2.05(0.64) = 0.208 + 1.312 = 1.52$ | 1.52 |

---

## P3-5 -- Cascade and parallel realisations

This question is purely structural: rewrite $H(z)$ as either a cascade (multiplication) or a sum (parallel) of two first-order systems.

### Cascade: factor → multiply

The given $H(z)$ is **already** factored into two first-order pieces. Just label them:

$$H(z) \;=\; H_1(z) \cdot H_2(z) \qquad\text{with}\qquad H_1(z) = \frac{1}{1 + 0.2\,z^{-1}}, \quad H_2(z) = \frac{1}{1 - 0.8\,z^{-1}}$$

**Block diagram:** $x[n] \to [H_1] \to [H_2] \to y[n]$ (or $H_2$ first then $H_1$ -- order doesn't matter for LTI cascades).

Each block is a first-order recursive filter:
- $H_1$: $y_1[n] = -0.2\,y_1[n-1] + x[n]$
- $H_2$: $y_2[n] = +0.8\,y_2[n-1] + y_1[n]$

### Parallel: PFD → sum

The PFD from P3-3 **is** the parallel form. Each term is one branch:

$$H(z) \;=\; H_1'(z) + H_2'(z) \qquad\text{with}\qquad H_1'(z) = \frac{0.2}{1 + 0.2\,z^{-1}}, \quad H_2'(z) = \frac{0.8}{1 - 0.8\,z^{-1}}$$

**Block diagram:** $x[n]$ feeds both $H_1'$ and $H_2'$ in parallel, their outputs sum to $y[n]$.

> [!important] The link to PFD
> Every PFD you compute (via `residuez` or by hand) **is** the parallel realisation. The residues are the gain on each branch; the poles are the recursion coefficients. Free realisation diagram on every PFD problem.

### What to write on the exam

1. State both decompositions in equation form (boxed expressions above).
2. Optional: sketch the two block diagrams (one cascade, one parallel sum).
3. Note that the cascade comes from the factored $H(z)$ and the parallel comes from the PFD.

---

# Problem 4 -- IIR Butterworth highpass via BLT

### The full design pipeline

This problem walks through the **standard IIR design recipe** end-to-end. Five sub-questions, one per pipeline stage:

```
digital specs (in Hz)
       |
       v
[4-1] PRE-WARP   :  digital ω -> analog Ω   via   Ω = (2/Ts)·tan(ω/2)
       |
       v
[4-2] ORDER + LP :  pick Butterworth order n; get H_LP(s) prototype
       |          (normalized so LP cutoff is 1 rad/s)
       v
[4-3] LP -> HP   :  substitute s_lp -> Wo / s_hp   ->   H_HP(s)
       |          (Wo = the desired HP cutoff)
       v
[4-4] BLT        :  substitute s = (2/Ts)·(1-z^-1)/(1+z^-1)   ->   H_HP(z)
       |
       v
[4-5] VERIFY     :  freqz, plot |H| in dB, check it meets the specs
```

Every IIR design via BLT follows this exact pipeline. Memorise the box.

### Specs

| Param | Value |
|---|---|
| Filter | IIR Butterworth highpass |
| $F_s$ | 5000 Hz |
| Stopband edge $F_\text{stop}$ | 100 Hz |
| Passband edge $F_\text{pass}$ | 180 Hz |
| Stopband attenuation $A_s$ | 20 dB |
| Passband attenuation $A_p$ | 3 dB |
| BLT $\alpha$ | $2/T_s$ |

> [!note] Highpass means stopband **below** passband
> $F_\text{stop} = 100\,\text{Hz} < F_\text{pass} = 180\,\text{Hz}$. For a lowpass it'd be the other way around. Watch this when applying generic order formulas -- the "ratio" you plug in differs.

---

## P4-1 -- Pre-warping (digital → analog frequencies)

### The formula

The bilinear transform maps the entire analog frequency axis $\Omega \in (-\infty, \infty)$ onto the digital frequency interval $\omega \in (-\pi, \pi)$ via:

$$\Omega \;=\; \alpha \tan(\omega/2) \qquad \text{with}\;\alpha = 2/T_s$$

Equivalently, in Hz:

$$\Omega \;=\; \frac{2}{T_s}\,\tan\!\left(\frac{\pi F}{F_s}\right)$$

Pre-warping is just applying this formula to each spec frequency *before* designing the analog filter, so that after the BLT the digital edges land exactly where we want them.

### Why pre-warp at all

The BLT is non-linear in frequency: high analog frequencies get squeezed toward the Nyquist boundary. If we designed an analog filter at the un-warped frequencies and then applied the BLT, the resulting digital edges would be at the **wrong** Hz values. Pre-warping cancels the squeeze.

### MATLAB

```matlab
Fs4 = 5000;  Ts4 = 1/Fs4;
omega_s = 2*pi*100/Fs4;     % digital angular freq for stopband edge
omega_p = 2*pi*180/Fs4;     % digital angular freq for passband edge
Omega_s = (2/Ts4) * tan(omega_s/2);
Omega_p = (2/Ts4) * tan(omega_p/2);
```

### Numbers

$$\Omega_s = \frac{2}{T_s}\tan\!\left(\frac{\pi \cdot 100}{5000}\right) \approx 628.7\,\text{rad/s}$$

$$\Omega_p = \frac{2}{T_s}\tan\!\left(\frac{\pi \cdot 180}{5000}\right) \approx 1135\,\text{rad/s}$$

---

## P4-2 -- Filter order n, lowpass prototype H(s)

### Map HP specs onto an LP prototype

The classical analog Butterworth design tables are for **lowpass** filters, normalized to cutoff = 1 rad/s. For our HP problem, we use the LP→HP frequency mapping in reverse:

| HP edge | mapped to LP prototype edge |
|---|---|
| $\Omega_p^\text{HP}$ (passband, 3 dB cutoff) | $1$ rad/s (LP cutoff) |
| $\Omega_s^\text{HP}$ (stopband) | $\Omega_p / \Omega_s$ rad/s (LP stopband) |

So in the LP prototype, the "stopband to passband ratio" is:

$$r \;=\; \frac{\Omega_p}{\Omega_s} \;=\; \frac{1135}{628.7} \;\approx\; 1.804$$

### Butterworth order formula

$$n \;\geq\; \frac{\log_{10}\!\left(\dfrac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\,\log_{10}(r)}$$

The numerator: $\log_{10}((100-1)/(2-1)) = \log_{10}(99) \approx 1.9956$.
The denominator: $2 \log_{10}(1.804) \approx 0.5125$.

$$n \;\geq\; 1.9956 \,/\, 0.5125 \;\approx\; 3.894 \;\Rightarrow\; \boxed{n = 4}$$

### Normalized LP prototype H(s) for n = 4

Standard 4th-order Butterworth (cutoff = 1 rad/s):

$$H_\text{LP}(s) \;=\; \frac{1}{s^4 + 2.6131\,s^3 + 3.4142\,s^2 + 2.6131\,s + 1}$$

The denominator coefficients come from the four Butterworth poles on the unit circle in the left half plane.

### MATLAB

```matlab
[z_lp, p_lp, k_lp] = buttap(n_order);          % poles of LP prototype, cutoff 1
[b_lp, a_lp]       = zp2tf(z_lp, p_lp, k_lp);  % to (b, a) form
```

`buttap(4)` returns the four normalized Butterworth poles directly. `zp2tf` converts to polynomial coefficients. Output `a_lp` should be `[1, 2.6131, 3.4142, 2.6131, 1]` matching the boxed expression.

---

## P4-3 -- Lowpass-to-Highpass transformation

### The substitution

$$s_\text{lp} \;\longrightarrow\; \frac{W_o}{s_\text{hp}}$$

where $W_o$ is the desired HP cutoff (3-dB point). For our Butterworth design, $A_p = 3$ dB *is* the cutoff, so:

$$W_o \;=\; \Omega_p \;\approx\; 1135\,\text{rad/s}$$

This substitution maps the LP prototype's cutoff at 1 to the HP's cutoff at $W_o$, and inverts the band (LP passband → HP stopband and vice versa).

### MATLAB

```matlab
Wo = Omega_p;
[b_hp_a, a_hp_a] = lp2hp(b_lp, a_lp, Wo);
```

`lp2hp` does the substitution analytically and returns the new analog $H_\text{HP}(s)$ as polynomial coefficients in $s$.

The output is in the form:

$$H_\text{HP}(s) \;=\; \frac{\beta_M s^M + \beta_{M-1}s^{M-1} + \cdots + \beta_0}{\alpha_N s^N + \alpha_{N-1}s^{N-1} + \cdots + \alpha_0}$$

Just print the coefficient vectors `b_hp_a` (the $\beta$'s) and `a_hp_a` (the $\alpha$'s). For a 4th-order HP, both are length 5 with $\beta_4 = 1$, $\beta_3 = \beta_2 = \beta_1 = \beta_0 = 0$ (numerator is $s^4$ alone) and a 4th-order denominator.

---

## P4-4 -- Bilinear transform to digital H(z)

### The substitution

$$s \;\longrightarrow\; \frac{2}{T_s}\,\frac{1 - z^{-1}}{1 + z^{-1}}$$

This is the BLT relation that motivated the pre-warp in P4-1. Applying it to $H_\text{HP}(s)$ gives a rational in $z^{-1}$.

### MATLAB

```matlab
[b_hp_d, a_hp_d] = bilinear(b_hp_a, a_hp_a, Fs4);
```

> [!warning] No extra prewarping flag
> MATLAB's `bilinear` accepts an optional pre-warp frequency: `bilinear(b, a, fs, fp)`. **Do not pass `fp` here** -- we already prewarped manually in P4-1. Passing it would prewarp twice and the digital edges would be wrong.

The output is:

$$H_\text{HP}(z) \;=\; \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + b_3 z^{-3} + b_4 z^{-4}}{1 + a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3} + a_4 z^{-4}}$$

Both numerator and denominator are 4th-order. Print `b_hp_d` and `a_hp_d` as the answer.

---

## P4-5 -- Magnitude response and spec verification

### Plot |H(f)| in dB

```matlab
[H4, F4] = freqz(b_hp_d, a_hp_d, 4096, Fs4);
H4_dB    = 20*log10(abs(H4));
plot(F4, H4_dB);
```

`freqz(b, a, N, Fs)` returns `H` evaluated at `N` frequency points in $[0, F_s/2]$, with the frequency axis `F4` already in Hz. Convenient -- no manual scaling.

### Mark the spec lines

```matlab
xline(100, '--r', '100 Hz (Fstop)');
xline(180, '--g', '180 Hz (Fpass)');
yline(-As4, '--r', '-20 dB');
yline(-Ap4, '--g', '-3 dB');
```

The spec is met when the magnitude curve:
- is **at or below** $-A_s = -20$ dB to the **left** of $F_\text{stop} = 100$ Hz (stopband)
- is **at or above** $-A_p = -3$ dB to the **right** of $F_\text{pass} = 180$ Hz (passband)

### Numerical spec check (using the nearest-bin lookup idiom)

```matlab
[~, idx_stop] = min(abs(F4 - 100));
[~, idx_pass] = min(abs(F4 - 180));
H4_dB(idx_stop)    % attenuation at the stopband edge
H4_dB(idx_pass)    % attenuation at the passband edge
```

For a 4th-order Butterworth designed to exactly $A_s = 20$ dB at $F_\text{stop}$ and $A_p = 3$ dB at $F_\text{pass}$, the script should print roughly:

| Frequency | Attenuation | Spec | Pass? |
|---|---|---|---|
| 100 Hz | $\approx -23$ to $-25$ dB | $\le -20$ dB | yes (over-design from `ceil`) |
| 180 Hz | $\approx -3.0$ dB | $\ge -3$ dB | yes (lands on the boundary) |

Because we rounded $n$ from 3.89 up to 4, the stopband attenuation is somewhat better than the spec required. The passband attenuation lands exactly on $A_p$ since $W_o = \Omega_p$ was chosen as the 3-dB cutoff.

### Discussion

Briefly note in the answer:
- The filter meets both specs.
- The over-design at the stopband is the consequence of `n = ceil(3.894) = 4`. Using `n = 3` would not meet the 20 dB stopband requirement.
- The plot should look like a clean monotonic Butterworth highpass: deep null near DC, smooth rise, asymptotic to 0 dB beyond the cutoff.

---

# Links

- [[LTI z-transform flow]] -- theory reference for Problem 1
- [[Partial fraction practice]] -- hand-calc PFD drills (deprecated for exam since `residuez` is allowed)
- [[62743 Digital Signal Processing (Reexam)]] -- course hub
