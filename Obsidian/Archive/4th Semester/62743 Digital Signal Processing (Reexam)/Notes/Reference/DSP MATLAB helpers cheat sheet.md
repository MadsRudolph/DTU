---
type: reference
tags: [DSP, reexam, MATLAB, helpers, cheat-sheet]
aliases:
  - DSP helpers
  - MATLAB helpers
  - Helper functions
---
# DSP MATLAB helpers -- cheat sheet

> [!info] Location
> All helpers live in `C:\Users\Mads2\DTU\3.semester\DSP\Helpers\` (added to path via `addpath(...)` at the top of every exam script).
> Authors: Bjørn Bjarnason, Tobias Nilson, Mathias Bay (DTU classmates, semester E25).

---

## ⚠️ Gotchas (read these FIRST during the exam)

### Hz → rad/s before any analog filter function

The exam gives you cutoffs in **Hz** ($F_p$, $F_s$, etc.). MATLAB's analog filter functions (`lp2lp`, `lp2hp`, `lp2bp`, `lp2bs`, `freqs`, `bilinear`) all want **angular frequency in rad/s** ($\Omega$).

Conversion is always:
$$\Omega = 2\pi F$$

In code, every time:
```matlab
Wp = 2*pi*Fp;     % BEFORE passing to lp2lp / freqs / lp2bs / bilinear
```

**Why it bites:** if you pass Hz directly into `lp2lp(b, a, Fp)` instead of `lp2lp(b, a, 2*pi*Fp)`, the filter is designed at a cutoff $2\pi$ times **too low** -- and the magnitude plot will look completely wrong. The numbers won't error out, you'll just get a silently broken filter.

**Where to apply it:** prototype → real filter (`lp2lp` etc.), frequency-response eval (`freqs`), BLT to digital (`bilinear`).

**Notation crib:**

| Symbol | Meaning | Units | MATLAB var |
|---|---|---|---|
| $F$ | analog frequency | Hz | `F`, `Fp`, `Fs_filter` |
| $\Omega$ | analog **angular** frequency | rad/s | `W`, `Wp` |
| $f$ | normalised digital frequency | $F/F_s$ | `f` |
| $\omega$ | digital **angular** frequency | rad/sample | `w` |

Conversions: $\Omega = 2\pi F$, $\omega = \Omega T = 2\pi f$.

### Multiple return values: `[b, a] = …` — never forget the brackets

Filter functions return **two arrays**: numerator coefficients (b) and denominator coefficients (a). Capture both with `[...]` on the LHS:

```matlab
[b_AA, a_AA] = lp2lp(b_proto, a_proto, Wp);
%  ^      ^
%  |      └─ second output: denominator (a, alphas)
%  └──────── first output:  numerator   (b, betas)
```

**Order is always `b` first, `a` second.** Same pattern everywhere in DSP:

| Call | Returns |
|---|---|
| `[b, a]   = lp2lp(...)`    | num, den (analog LP→LP) |
| `[b, a]   = lp2bs(...)`    | num, den (analog LP→BS, Q4) |
| `[bd, ad] = bilinear(b,a,Fs)` | digital num, den |
| `[r, p, k] = residuez(b,a)` | residues, poles, direct term |
| `[z, p, k] = tf2zpk(b,a)`   | zeros, poles, gain |
| `[bd, ad] = n_value(...)`  | helper: prototype num, den |
| `[H, W]   = freqz(...)`    | response values, freq points |

**Why it bites:** if you write `b_AA = lp2lp(...)` (missing brackets), MATLAB silently grabs **only the numerator** and discards the denominator. The next line that needs `a_AA` will error with "undefined a_AA". No syntax warning, no auto-complete hint -- just a delayed crash.

### `impz` only gives **causal** samples (n ≥ 0)

`impz(b,a,N)` returns the impulse response at `n = 0,1,…,N-1` only. It **cannot**:
- show **negative** n (it assumes the system is causal, so n<0 is just not computed),
- take a **range** like `[-10 30]` — a 2-element 3rd argument is *not* a start/end, and it silently overwrites your `n`.

So if an exercise says *"plot the impulse response for n = −10 … 30"*, `impz` is the wrong tool. Use the explicit-impulse + `filter` recipe → [[#🔄 Canonical patterns these enable|Impulse response over any n-range]].

### Don't shadow built-ins: `zeros`, `roots`, `i`, `sum`, `length`…

```matlab
zeros = roots(B2);   % ☠️ 'zeros' is now YOUR variable, not the function
imp   = [zeros(1,10) 1 zeros(1,30)];   % ERROR: zeros is not callable anymore
```
Naming a variable `zeros` (or `i`, `sum`, `length`, `filter`…) replaces the built-in for the rest of the script. The crash happens *later*, on a line that looks fine. Use descriptive names — Danish is great here: `nulpunkter`, `poler`.

---

## 🟢 Universal setup

### `time_vec(Fs, N)` -- time vector
```matlab
t = time_vec(Fs, N);    % == (0:N-1)/Fs
```
Replaces the `(0:N-1)*Ts` boilerplate.

### `frequency_vec(Fs, N)` -- centred frequency vector in Hz
```matlab
f = frequency_vec(Fs, N);    % [-Fs/2 : df : Fs/2 - df]
```
The vector you need for plotting `fftshift(fft(x))` magnitude.

---

## 🟢 IIR filter design (Q2 / Q4 type)

### `n_value(AsdB, ApdB, nu, "butter"|"cheby")` ⭐
Order + prototype coefs in **one call**.
```matlab
[b_proto, a_proto] = n_value(20, 3, nu, "butter");
% nu = Omega_s / Omega_p (always > 1)
```
Prints $\varepsilon$ and $n$, returns the prototype $b,a$ vectors from a hardcoded table (orders 1-6).

**This replaces the F24 Q4-1 sequence:** compute min order → look up prototype in appendix → write coefficients. One line instead of three steps.

### `n_cheb(AsdB, ApdB, nu)` -- legacy, prints n only
Subset of `n_value` for Chebyshev order. **Prefer `n_value`** -- it returns coefficients.

### ⚠️ Bug in `n_value.m`
Chebyshev **n=4** entry is a copy-paste of n=3 (only 4 denominator coefficients, should be 5). Butterworth orders 1-6 and Chebyshev orders 1, 2, 3, 5, 6 are fine. For Chebyshev n=4, **look up the prototype in the slide appendix manually**.

---

## 🟢 FIR filter design (window method)

### `FIR_fourier(type, n_vec, omega_H, omega_L)` -- ideal impulse response
```matlab
M = 50;  n = -M/2 : M/2;        % index vector centred on 0
h_LP = FIR_fourier("LP", n, 0.3*pi);
h_BP = FIR_fourier("BP", n, 0.5*pi, 0.2*pi);   % BP needs both cutoffs
```
- `type` $\in$ `"LP"`, `"HP"`, `"BP"`, `"BS"`
- Handles the $n=0$ singularity correctly by setting the centre sample explicitly.
- ⚠️ **Returns the ideal/truncated (= rectangular) response ONLY — no window applied.** Any non-rectangular window ⇒ you MUST do `h = FIR_fourier(...) .* FIR_window(...)`. Rectangular needs no multiply — that's the trap that dumped E25 3-5 (see [[FIR window design flow]] step 6).

### `FIR_window(type, M)` -- window coefficients (length $M+1$)
```matlab
w = FIR_window("hamming", M);    % "hanning", "hamming", "blackman"
h_designed = h_LP .* w;          % windowed FIR
```
Rectangular window is just `ones(1, M+1)` (not in this helper).

### `MK_values(N_taps)` -- solve $M = N{-}1$ and $K = M/2$
```matlab
[M, K] = MK_values(101);    % M = 100, K = 50
```
Symbolic solver for the standard linear-phase FIR sizing relations.

> [!danger] ⚠️ `MK_values` can hard-crash — don't use it in the exam
> It calls `syms`/`solve`/`double`. On a broken/Maple symbolic backend it errors:
> `Error using sym/double … maplemex … cannot handle unevaluated name 'M'`.
> The relations are trivial — **use the closed form**, no toolbox needed:
> ```matlab
> M = n_taps - 1;     % Ntaps = M + 1
> K = M / 2;          % Ntaps = 2K + 1  (n_taps must be a rounded odd integer)
> ```
> Also feed it an **integer**: `0.9/0.1` is `8.999…` in floating point →
> `n_taps = ceil(0.9/F_sharpness)` first (round up, make odd for Type-I).

---

## 🔄 Canonical patterns these enable

### IIR analog design (lp2lp / lp2bs etc.)
```matlab
[bp, ap]     = n_value(AsdB, ApdB, nu, "butter");      % step 1+2: order + prototype
[b_a, a_a]   = lp2lp(bp, ap, 2*pi*Fp);                 % step 3:   transform
W            = 2*pi*F;                                 % step 4:   freq grid
H_resp       = freqs(b_a, a_a, W);                     % step 5:   evaluate
plot(F, abs(H_resp));                                  % step 6:   plot
```

### Spectrum plot (the F24 Q2-3 pattern)
```matlab
t  = time_vec(Fs, N);
xA = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);
XA = fftshift(fft(xA)) / N;
f  = frequency_vec(Fs, N);
plot(f, abs(XA));
```

### Windowed FIR (Lars Wk 11 territory)
```matlab
M = 50;  n = -M/2 : M/2;
h = FIR_fourier("LP", n, omega_c);
w = FIR_window("hamming", M);
h_final = h .* w;
freqz(h_final, 1);    % verify
```

---

## 🔁 Impulse response over any n-range (incl. negative n)

**The idea (read this once and it clicks):** the impulse response *is* "what comes out when the input is a single unit spike `δ[n]` at n=0". So instead of asking a special function, you just **build that spike yourself** and run it through `filter`:

```matlab
% --- General recipe: works for ANY n-interval, also negative -------------
n_start = -10;                 % første sample-indeks (kan være negativt)
n_stop  =  30;                 % sidste sample-indeks
n   = n_start:n_stop;          % sample-akse til plottet
imp = double(n == 0);          % enheds-impuls: 1 præcis ved n=0, ellers 0
IR  = filter(b, a, imp);       % kør impulsen gennem filteret
figure
stem(n, IR)
xlabel('Sample number, n'); ylabel('amplitude'); grid on
```

`n == 0` is a logical vector that is `1` at the single position where the sample number is 0 and `0` everywhere else — so the spike lands correctly no matter what range you pick. `double(...)` because `filter` wants numbers, not logicals.

**Hand-built equivalent** (what the official solutions write — same thing, counted by hand):
```matlab
n   = -10:30;
imp = [zeros(1,10) 1 zeros(1,30)];   % 10 nuller (n=-10..-1), 1 (n=0), 30 nuller (n=1..30)
IR  = filter(b, a, imp);
stem(n, IR)
```
Spike position math: `pos = 0 - n_start + 1`. Here `0 - (-10) + 1 = 11`, so the `1` is the 11th element. The `(n==0)` form does this counting for you — prefer it.

> [!warning] Why not `impz`?
> `impz(b,a,N)` only ever returns **causal** samples `n = 0…N-1`. It can't show n<0, and `impz(b,a,[-10 30])` does *not* mean "from −10 to 30". For a custom/negative range, use the recipe above.

**How to read the plot (this answers the usual follow-up questions):**

| What you see | Conclusion |
|---|---|
| `IR` is exactly 0 for **all n < 0** | system is **causal** |
| `IR` becomes **exactly 0** after finitely many samples | **FIR** — no feedback, `a = [1]` |
| `IR` decays but is **never exactly 0** | **IIR** — recursive, poler ≠ 0 |

> [!note] Stability is about the **unit circle**, not the ROC
> A common phrasing trap: "stable because the poles are in the ROC" is **wrong** — poles are *never* in the ROC (the ROC is defined to exclude them). Correct:
> $$\text{kausalt + stabilt} \iff \text{alle poler strengt inden for enhedscirklen } (|p| < 1)$$
> equivalently the causal ROC $|z| > \max|p|$ then *contains* the unit circle. One-line check:
> ```matlab
> max(abs(roots(a))) < 1     % true => stabilt
> ```

Used in: [[E25 exam walkthrough]] P2-2, [[F25 exam walkthrough]] Q4-3 (the `roots`/`zplane`/`max|pol|<1` pattern).

---

## 📍 Mark specific values on a plot (data tips in a `.m` script)

When the exam says *"aflæs amplituden ved 100 / 300 / 600 Hz"*, don't read by eye and don't hardcode — drop a **data tip** on each frequency of interest so the plot itself shows the exact value, and just refer to the figure in your answer. The tip displays the **exact data-point value** (no rounding-by-eye), and it renders into the published PDF via `pretty.bat`.

> The interactive click → *"Update Code"* round-trip only exists in Live Scripts (`.mlx`). In a plain `.m` script you write the `datatip()` calls yourself — same result, fully reproducible.

```matlab
% --- General recipe: mark a set of x-values on a curve --------------------
h = plot(f, abs(X), 'LineWidth',1.5);   % MUST capture the line handle
grid on; xlabel('Frequency [Hz]'); ylabel('|X|')

for F = [100 300 600]                    % x-values you want shown
    [~, idx] = min(abs(f - F));          % snap to the nearest sample/bin
    datatip(h, 'DataIndex', idx);        % pin tip to that exact data point
end
```

Why each line matters:
- `h = plot(...)` — `datatip` needs the **line handle**. `gca`/`ax.Children(1)` is fragile (index shifts if you add `xline`/more plots later).
- `min(abs(f - F))` — finds the index of the nearest point. Needed because `f == 600` rarely hits exactly (floating point); the snapped bin is exact when `F` is a true FFT bin.
- `datatip(h,'DataIndex',idx)` — pins to data point `idx`; the label shows the stored `(x,y)`, so what you "read off" *is* the computed value. Requires R2019b+.

> [!tip] In your written answer
> Cite the figure: *"Amplituderne aflæses på datatips i figuren til ca. 0.50 / 0.98 / 0.044"* — the tip values are the exact computed numbers, so this is just as defensible as printing them, and the examiner sees them on the plot.

Interactive variant (exploring only, **not** saved to code): `datacursormode on`, then click. Tips vanish on re-run — for a submittable script the `datatip()` calls must be in the source.

Used in: [[E25 exam walkthrough]] P2-5 (read filtered-spectrum amplitudes at 100/300/600 Hz).
