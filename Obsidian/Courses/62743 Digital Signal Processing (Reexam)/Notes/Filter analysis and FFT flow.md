---
type: reference
tags: [DSP, reexam, reference, filter-analysis, FFT, sampling]
aliases:
  - Filter analysis flow
  - FFT spectrum flow
  - block diagram to Hz flow
---
# Filter analysis & FFT flow

> [!info] What this note is
> The **Q2 archetype** on the 3-question exam (E25 Q2 ≈ 30 %). One mega-question that chains: **block diagram → H(z) → freqz/zplane → sampling → FFT spectrum → filter the signal → read attenuation**. Mostly your strong MATLAB area; the only sharp edge is **FFT amplitude scaling**.

Worked: [[F25 exam walkthrough]] (filter realisering), [[E24 exam walkthrough]] (3 given H(z)), [[E25 exam walkthrough]] (full chain). Helpers: [[DSP MATLAB helpers cheat sheet]].

---

## Recognise it by

A **Direct Form I/II block diagram** with feedforward/feedback gains, *or* one or more given H(z); then "samples med Fs…", "udregn frekvensspektrummet (FFT)", "filtrer signalet med `filter`".

---

## The flow

### 1 — Block diagram → b, a
- Feedforward gains (the `x[n], x[n-1]…` branch) → **`b`** (numerator).
- Feedback gains (the `y[n-1], y[n-2]…` branch) → **`a`**, with `a(1)=1` and **feedback signs flipped** (a diagram gain of `+2.0038` on y[n-1] → `a = [1, -2.0038, …]`).
- `Hz = tf(b, a, 1/Fs, 'Variable','z^-1')` to display H(z).
- **FIR or IIR?** any non-trivial `a` (feedback) → **IIR**, infinite impulse response. State it.

### 2 — Magnitude response
```matlab
F_vec = frequency_vec(Fs, Fs/2);
[H,F] = freqz(b, a, F_vec, Fs);          % Fs as 4th arg => F in Hz
plot(F, 20*log10(abs(H)))                % dB = 20*log10(|H|)
```
Read attenuation at the asked frequencies: `freqz(b,a,[f1 f2],Fs)` then `20*log10(abs(.))`. Compare to the stated spec (e.g. "3 dB ved 400 Hz").

### 3 — Poles/zeros & stability
```matlab
zplane(b, a)
poler = roots(a)                 % no semicolon: show values
```
**Stable iff every |pole| < 1** (all inside unit circle). FIR (`a = 1`) is always stable.

### 4 — Impulse response
`h = filter(b, a, [1 zeros(1,N)]);  stem(0:N, h)` (or `impz(b,a,N)`). Asked range e.g. n = −10..30 → pad/shift accordingly.

### 5 — Sampling without aliasing
- **Nyquist:** highest frequency that can be sampled = **Fs/2**.
- Given signal with components F1, F2, F3 → no aliasing iff `max(Fi) < Fs/2`. If one exceeds it, alias appears at `|Fi − k·Fs|` folded into [0, Fs/2].
- Time vector: `t = 0:1/Fs:T;`  signal: `x = A1*cos(2*pi*F1*t) + …`

### 6 — FFT spectrum (the one sharp edge — scaling)

> [!danger] Single-sided amplitude spectrum scaling
> `X = fft(x);` is **not** the amplitude. For a length-N real signal:
> ```matlab
> N  = length(x);
> Xf = fft(x);
> P  = abs(Xf)/N;              % normalise by N
> P1 = P(1:floor(N/2)+1);      % single-sided
> P1(2:end-1) = 2*P1(2:end-1); % double interior bins (energy from neg. freqs)
> f  = (0:floor(N/2)) * Fs/N;  % Hz axis
> stem(f, P1)
> ```
> A pure `A·cos(2πF₀t)` then shows a line of height **≈ A** at F₀. If your peaks are A/2, you forgot the `*2`. If they scale with N, you forgot `/N`.

Comment: do the peak frequencies (F1,F2,F3) and heights (A1,A2,A3) match the input? They should, up to leakage.

### 7 — Filter the signal & read attenuation
```matlab
y  = filter(b, a, x);                 % apply the filter from step 1
% redo the single-sided FFT on y
```
Read amplitude at each component before vs after. Attenuation in dB:
$$\text{dæmpning}=20\log_{10}\!\frac{A_{\text{før}}}{A_{\text{efter}}}$$
**Cross-check:** this dB value should match `|H|` read off the step-2 magnitude plot at that frequency. State that it agrees.

---

## Answer style
Conclusions as `%%`-`Svar` blocks; computed values via no-semicolon or value-bearing `fprintf`; never narrate in `fprintf`. See [[62743 Digital Signal Processing (Reexam)]] §Publishing.

---

## Top traps
1. **Feedback sign** — diagram `+a_k` on y[n−k] becomes **`−a_k`** in the `a` vector.
2. **FFT not scaled** — `/N`, single-sided, `×2` interior bins. Most-missed marks here.
3. **freqz units** — pass `Fs` as the 4th arg so F comes out in **Hz**, not rad/sample.
4. **dB factor** — magnitude is `20*log10`, not `10*log10`.
5. **Aliasing fold** — alias lands at `Fs − F` (for F in (Fs/2, Fs)), not at F.

---

# Links
- [[62743 Digital Signal Processing (Reexam)]] — hub
- [[LTI z-transform flow]] — if it instead asks H(z)→h[n] by hand
- [[DSP MATLAB helpers cheat sheet]] — `frequency_vec`, `time_vec`
- [[F25 exam walkthrough]], [[E24 exam walkthrough]], [[E25 exam walkthrough]] — worked
