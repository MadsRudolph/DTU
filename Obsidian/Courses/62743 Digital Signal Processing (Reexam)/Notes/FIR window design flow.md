---
type: reference
tags: [DSP, reexam, reference, FIR, window-design]
aliases:
  - FIR design flow
  - Fourier window method
  - FIR window flow
---
# FIR window design flow — Fourier method

> [!info] What this note is
> The **Q3 archetype** on the 3-question exam (E25 Q3, E24 Q4, F23 Q4). A FIR filter (LP/HP/BP/BS) designed by the **Fourier transform method + a window**. ~30 % of the exam. Pure recipe — this is a *strong-area, guaranteed-points* question. Do it cleanly and bank the marks.

Worked examples to open beside this: [[F23 exam walkthrough]] (HP + Blackman), [[E25 exam walkthrough]] (HP, As 20→40 dB), [[E24 exam walkthrough]] (bandstop + Hanning).
Helper signatures: [[DSP MATLAB helpers cheat sheet]]. Theory depth: [[FIR_Windowing_Complete_Guide]].

---

## Recognise it by

- "Filter design metode: **Fourier transform** metoden" / "Fourier transformation design"
- gives **Fpass, Fstop, As (stopband dæmpning dB), Fs**, sometimes Ntaps directly
- asks for: cutoff Fc, ωc, ΔF sharpness, **which window**, **Ntaps**, **truncated causal impulse response**, freqz magnitude dB, phase-linearity.

---

## The flow (top to bottom)

### 1 — Cutoff frequency Fc
Midpoint of the transition band:
$$F_c=\frac{F_{pass}+F_{stop}}{2}$$
(E25: (1750+1250)/2 = **1500 Hz** ✓ matches "vis at Fc = 1500 Hz".)

Digital cutoff:
$$\omega_c=2\pi\frac{F_c}{F_s}\qquad f_c=\frac{F_c}{F_s}$$

### 2 — Transition width → sharpness
$$\Delta F=\lvert F_{pass}-F_{stop}\rvert,\qquad \Delta F_{sharpness}=\frac{\Delta F}{F_s}\ \text{(normaliseret)}$$

### 3 — Pick the window + compute Ntaps from As
The window must give **at least** the required As. **Course table** (verified against E25 answers):

| Window | Min. stopband As | **Ntaps formula** |
|---|---|---|
| Rectangular | 21 dB | $N_{taps}=0.9/\Delta F_{sharpness}$ |
| **Hanning** | 44 dB | $N_{taps}=3.1/\Delta F_{sharpness}$ |
| **Hamming** | 53 dB | $N_{taps}=3.3/\Delta F_{sharpness}$ |
| **Blackman** | 74 dB | $N_{taps}=5.5/\Delta F_{sharpness}$ |

with $\Delta F_{sharpness}=\dfrac{\lvert F_{stop}-F_{pass}\rvert}{F_s}$.

> [!tip] Pick the *cheapest* window that clears As, then round Ntaps **up to the nearest odd integer**.
> E25 check: ΔF = 500/5000 = 0.1. As = 20 dB → Rectangular (21 dB) → Ntaps = 0.9/0.1 = **9** ✓. Spec bumped to As = 40 dB → Rectangular (21) fails → **Hanning** (44) → Ntaps = 3.1/0.1 = **31** ✓. This "change As → re-pick window → recompute Ntaps" is a standard exam sub-part.

### 4 — Order M, centre K
- $M = N_{taps}-1$ (order), $K = M/2$ (linear-phase centre = group delay in samples).
- The **`MK_values`** helper returns K and M directly (signatures: [[DSP MATLAB helpers cheat sheet]]). If the exam *states* Ntaps, just use K = (Ntaps−1)/2.

### 5 — Truncated, causal (delayed) impulse response
Ideal response, then shift by K so it's causal:
- **LP:** $h_d[n]=2f_c\,\mathrm{sinc}(2f_c\,(n-K))$
- **HP:** $h_d[n]=\delta[n-K]-2f_c\,\mathrm{sinc}(2f_c\,(n-K))$
- **BP/BS:** combination of two LP responses (see [[FIR_Windowing_Complete_Guide]]).

> [!danger] MATLAB `sinc` is normalised: `sinc(x) = sin(πx)/(πx)`.
> So `2*fc*sinc(2*fc*(n-K))` — do **not** add an extra π. Index `n = 0:Ntaps-1`, centre `K`.

Then **multiply by the window**: `h = hd .* w(:)'` where `w = hanning(Ntaps)` etc. The **`FIR_fourier`** / **`FIR_window`** helpers do steps 5+6 in one call — use them, then `stem(0:Ntaps-1, h)`.

### 6 — Transfer function & verify
- `H(z)`: numerator = `h`, denominator = `1` (FIR → all zeros, no poles → always stable).
- `[H,F] = freqz(h, 1, F_vec, Fs);` plot `20*log10(abs(H))` vs F in Hz.
- Mark **Fc, Fpass, Fstop, As** with `xline`/`yline`. Comment: does it clear As at Fstop and ~0 dB at Fpass?

### 7 — Phase
- `plot(F, unwrap(angle(H)))` → **linear** in the passband (straight line).
- Why: symmetric truncated `h` (type-I/II linear phase) → constant group delay = K samples. Always say *"linear phase, fordi h[n] er symmetrisk om n = K"*.

---

## MATLAB skeleton

```matlab
Fs = 5000;  Fpass = 1750;  Fstop = 1250;  AsdB = 20;

Fc = (Fpass + Fstop)/2;          % 1500 Hz
fc = Fc/Fs;       wc = 2*pi*fc;
dF = abs(Fpass - Fstop)/Fs;      % normaliseret transition width

% K, M, Ntaps for valgt vindue (se MK_values-signatur i cheat sheet)
[K, M] = MK_values(...);         % -> Ntaps = M+1
n  = 0:M;

% trunkeret + forsinket impulsrespons (HP-eksempel) + vindue
h  = FIR_fourier(...);           % eller FIR_window(...) — se cheat sheet

F_vec = frequency_vec(Fs, Fs/2);
[H,F] = freqz(h, 1, F_vec, Fs);

figure; plot(F, 20*log10(abs(H))); grid on
xline(Fc,'--g','Fc'); xline(Fpass,'--b'); xline(Fstop,'--b');
yline(-AsdB,'--r','As'); title('FIR magnituderespons')

%%
% *Svar:* Vinduet er <Hanning/...> da kravet til stopbåndsdæmpning er
% <As> dB. Ntaps = <N>, K = <K>. Filteret opfylder kravet (≥ <As> dB
% dæmpning ved Fstop, ~0 dB i pasbåndet). Fasen er lineær i pasbåndet,
% hvilket er forventet for et symmetrisk FIR-filter.
```

(Write answers as `%%`-`Svar` blocks — see [[62743 Digital Signal Processing (Reexam)]] §Publishing.)

---

## Top traps

1. **Wrong Fc** — it's the *midpoint* of Fpass/Fstop, not Fpass.
2. **`sinc` double-π** — MATLAB `sinc` already has π baked in.
3. **Window too weak** — Rectangular only gives ~21 dB; if As > 21 you *must* go Hanning+.
4. **Forgot the K-shift** — un-delayed `h` is non-causal; centre at K = M/2.
5. **Ntaps vs order** — `Ntaps = M + 1`. The exam sometimes states Ntaps, sometimes M.

---

# Links
- [[62743 Digital Signal Processing (Reexam)]] — hub
- [[FIR_Windowing_Complete_Guide]] — full theory
- [[DSP MATLAB helpers cheat sheet]] — `MK_values`, `FIR_fourier`, `FIR_window`, `frequency_vec`
- [[F23 exam walkthrough]], [[E25 exam walkthrough]], [[E24 exam walkthrough]] — worked
