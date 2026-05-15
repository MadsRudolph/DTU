---
type: walkthrough
tags: [DSP, reexam, exam, F25, walkthrough]
aliases:
  - F25 walkthrough
  - F25 exam log
---
# F25 exam -- MATLAB walkthrough

> [!info] What this note is
> Step-by-step log of how I'm solving the **F25 exam** in [[62743 F25 Exam.pdf]].
> **Filter-first**: Q2 (IIR HP via BLT) and Q4 (filter realization + application) are the priority. Q1 and Q3-3 are deferred math.
> One section per sub-question. Explains *what the MATLAB is doing* and *why*.

**Exam PDF:** [[62743 F25 Exam.pdf]]
**Solution PDF:** [[62743 F25 Exam student solutions.pdf]]
**Working script:** `3.semester/DSP/EXAMS/F25.m` (outside vault)

---

# Problem 1 -- LTI system / H(z) / mag-phase / cascade  [DEFERRED - math]

Math question (linearity extraction, H(z), analytic |H(ω)|/∠H(ω), cascade FIR proof). Deferred per filter-first strategy. Solution in [[62743 F25 Exam student solutions.pdf]] if needed.

---

# Problem 2 -- IIR højpas Butterworth via BLT  [FILTER -- priority]

**Topic:** T9 (IIR design, BLT, prewarp, Butterworth). Same pipeline as F24 Q4 but **highpass** (`lp2hp`, no order doubling).

**Spec:** BLT $\alpha=2/T_s$; IIR **highpass** Butterworth; $F_s=4000$ Hz; stopband edge $f_s=450/F_s$; passband edge $f_p=1000/F_s$; $A_{sdB}=30$ dB; $A_{pdB}=3$ dB. (HP: stopband **below** passband.)

## P2-1 -- prototype (ε, prewarp, order, TF)  ✅ verified vs solution pp.5-6

```matlab
eps_sq = 10^(0.1*ApdB) - 1;        % epsilon^2 from passband atten.
e      = sqrt(eps_sq);             % epsilon ~ 1 (since Ap = 3 dB)

omega_s = fs*2*pi;   Omega_s = (2/Ts2)*tan(omega_s/2);   % prewarp -> rad/s
omega_p = fp*2*pi;   Omega_p = (2/Ts2)*tan(omega_p/2);

vs = Omega_p/Omega_s;              % HIGHPASS ratio (LP would be Os/Op)
n  = ceil( log10((10^(0.1*AsdB)-1)/eps_sq) / (2*log10(vs)) );

proto_num = 1;
H_Proto   = tf(proto_num, proto_den{n});   % proto_den{4} from appendix
```

**Verified values** [F25 Student Solutions, 2-1]:

| Quantity | Value |
|---|---|
| ε | 0.9976 ≈ 1 |
| Ω_s | ≈ 2951 rad/s |
| Ω_p | ≈ 8000 rad/s |
| ν_s = Ω_p/Ω_s | ≈ 2.71 |
| n (unrounded 3.47) | **4** |
| Prototype | $1/(s^4+2.6131s^3+3.4142s^2+2.6131s+1)$ |

> 🚩 **The one new concept vs F24:** for a **highpass**, the order ratio is $\nu_s = \Omega_p/\Omega_s$ (passband over stopband). For a **lowpass** it's $\Omega_s/\Omega_p$. The solution states this explicitly: *"Den normaliserede frekvens ν_s er for et **højpasfilter** defineret som ν_s = Ω_p/Ω_s"*.

## P2-2 -- analog HP via lp2hp + dB plot  ✅ verified vs solution pp.7-8

**Transformation:** LP-prototype → highpass is $s \rightarrow \dfrac{\Omega_p}{s}$. Cutoff = **passband edge** Ω_p (because $A_{pdB}=3$ dB is defined there, and 3 dB *is* the Butterworth cutoff).

```matlab
[b_HP,a_HP] = lp2hp(proto_num, proto_den{n}, Omega_p);
HHP = tf(b_HP, a_HP)

[H_analog,wout] = freqs(b_HP, a_HP, 1024);   % scalar 1024 -> auto rad/s range
plot(wout, 20*log10(abs(H_analog)));         % MUST plot vs returned wout

H_chk = freqs(b_HP, a_HP, [Omega_s, Omega_p]);   % exact spec-point check
```

**Result:** −34.64 dB @ Ω_s (spec ≥30 dB ✅), −3.01 dB @ Ω_p (spec ≈3 dB ✅). Filter meets analog requirements.

> 🚩 `freqs` with a **scalar** (1024) auto-picks the rad/s range and returns it as `wout` — you must capture and plot against `wout`, not a hand-made vector. `frequency_vec` is an **FFT helper** (Hz, ±Fs/2) and is the *wrong* tool for `freqs`.

## P2-3 -- BLT to digital HP  ✅

**s↔z relation** (α = 2/Ts): $s = \dfrac{2}{T_s}\cdot\dfrac{z-1}{z+1}$

```matlab
[bz, az] = bilinear(b_HP, a_HP, Fs2);   % Fs2 in Hz (NOT rad/s)
HHP_z    = tf(bz, az, Ts2)
```

> 🚩 `bilinear` takes **Fs in Hz**; `freqs` takes rad/s. Different conventions — see [[DSP MATLAB helpers cheat sheet]] gotchas.

## P2-4 -- verify digital filter  ✅

```matlab
[h,f] = freqz(bz, az, 4096, Fs2);   % Fs2 as 4th arg -> f in Hz
plot(f, 20*log10(abs(h)));          % abs(h) = response, NOT abs(f)

H_chk2 = freqz(bz, az, [450, 1000], Fs2);   % exact attenuation read-off
dB2 = 20*log10(abs(H_chk2));
```

**Expected:** ≈ −34.6 dB @ 450 Hz, ≈ −3.0 dB @ 1000 Hz — matches the 2-2 analog values because **the BLT preserves the response exactly at the prewarped edge frequencies**. Spec met (≥30 dB stopband, ≈3 dB passband).

> 🚩 Two recurring slips fixed here: (1) `freqz(b,a,n)` with scalar `n` returns `f` in *normalized* rad/sample — pass `Fs` as the **4th** arg to get Hz; (2) plot `abs(h)` (response), not `abs(f)` (frequency axis).

### 🚩 Pattern: IIR highpass via BLT (vs F24 bandstop)

Same 5-step pipeline as F24 Q4. Differences for **highpass**:
- Order ratio: $\nu_s = \Omega_p/\Omega_s$ (inverted vs lowpass).
- Transform: `lp2hp(b, a, Omega_p)` — **one** cutoff param (the passband edge), no order doubling (unlike `lp2bs`/`lp2bp` which double).
- Everything else (prewarp → order → prototype → bilinear → freqz/dB) is identical.

---

# Problem 3 -- Sampling (3-1/3-2) + ROC/stability (3-3 deferred math)

**Setup:** $x(t)=3\cos(2\pi\cdot1500\,t)+2\cos(2\pi\cdot4200\,t)$, $F_s=8000$ Hz.

## P3-1 -- sketch amplitude spectrum (-10..10 kHz)

<!-- fill in -->

## P3-2 -- aliasing in -4..4 kHz, at what frequency

<!-- fill in -->

## P3-3 -- DEFERRED (ROC / stability / inverse filter -- math)

---

# Problem 4 -- Digital LP filter: realization + application  [FILTER -- priority]

**Topic:** T7 (filter structures), T6 (sampling), filtering with `filter()`. Filter has 3 dB attenuation at 400 Hz, $F_s=5000$ Hz. Coefficients read from a Direct-Form block diagram.

## P4-1 -- filter form, FIR/IIR, H(z)

<!-- fill in -->

## P4-2 -- magnitude response (dB), read 3 dB point

<!-- fill in -->

## P4-3 -- poles/zeros, stability

<!-- fill in -->

## P4-4 -- sampling xa(t), aliasing check, plot

<!-- fill in -->

## P4-5 -- filter the signal with filter(), compare before/after

<!-- fill in -->

---

# Exam-day takeaways for F25

> Filled in after we finish the filter problems.

- **Patterns used:**
- **What tripped me up:**
- **Quick reference if this comes up again:**
