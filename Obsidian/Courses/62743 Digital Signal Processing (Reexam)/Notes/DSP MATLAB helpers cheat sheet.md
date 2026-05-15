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
Symbolic solver for the standard linear-phase FIR sizing relations. Overkill but harmless.

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
