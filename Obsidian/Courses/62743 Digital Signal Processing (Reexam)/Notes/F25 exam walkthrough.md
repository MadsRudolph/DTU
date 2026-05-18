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
**Working script:** `3.semester/DSP/EXAMS/F25_new.m` (outside vault)

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

## P4-1 -- filter form, FIR/IIR, H(z)  ✅ verified vs F25 solution (NotebookLM grounding)

Coefficients read off the **Direct Form I** block diagram (separate delay chains for x and y):

```matlab
b  = [0.0102, 0.0305, 0.0305, 0.0102];   % feedforward (x[n..n-3])
a  = [1, -2.0038, 1.4471, -0.3618];      % feedback gains -> LHS -> sign flip
Hz = tf(b, a, Ts4, 'Variable','z^-1');
```

$$H(z)=\dfrac{0.0102+0.0305z^{-1}+0.0305z^{-2}+0.0102z^{-3}}{1-2.0038z^{-1}+1.4471z^{-2}-0.3618z^{-3}}$$

- **Form:** Direct Form I (separate `x` and `y` delay lines).
- **IIR**, because `y[n]` depends on past *outputs* `y[n-1..n-3]` (feedback, `a ≠ [1]`) → infinite impulse response.

> 🚩 **Sign-flip trap:** feedback gains are *added* in the diagram; moving them to the LHS of the difference equation flips their sign in MATLAB's `a` vector. The "two separate delay chains" fact justifies **Direct Form I**, *not* IIR — keep those two arguments separate (common lost mark; I swapped them on the first attempt).

## P4-2 -- magnitude response (dB), read 3 dB point  ✅

```matlab
[h,f] = freqz(b,a,4096,Fs4);          % Fs as 4th arg -> f in Hz (one-sided)
plot(f, 20*log10(abs(h))); yline(-3); xline(400);
```

The −3 dB crossing sits at **≈ 400 Hz**, matching the stated spec (3 dB attenuation at 400 Hz, Fs = 5000 Hz). ✅

> 🚩 `frequency_vec(Fs,N)` returns a **two-sided** vector (±Fs/2) — fine for FFT, wrong tool for a one-sided `freqz` magnitude plot. Use scalar `freqz(b,a,4096,Fs)`.

## P4-3 -- poles/zeros, stability  ✅

```matlab
nuller = roots(b)            % zeros = roots of numerator b
poler  = roots(a)            % poles = roots of denominator a
zplane(b,a)                  % unit circle + o (zeros) / x (poles)
max(abs(poler)) < 1          % stability test
```

**Stable**: all poles strictly inside the unit circle (`max|pole| < 1`). For a *causal IIR* filter, stability ⇔ all poles inside the unit circle.

> 🚩 "Find poler/nulpunkter" wants the **numeric roots** listed (`roots(b)`, `roots(a)`), not just a `zplane` picture. Justify stability with `max(abs(poler))<1`, not "as seen on the plot".

## P4-4 -- sampling xa(t), aliasing check, plot  ✅

$x_a(t)=5\cos(2\pi\cdot50\,t)+3\cos(2\pi\cdot1000\,t)$, sampled at $F_s=5000$ Hz.

```matlab
t4 = 0:1/Fs4:0.05;
xa_sampled = A1*cos(2*pi*F1*t4) + A2*cos(2*pi*F2*t4);
```

**No aliasing:** Nyquist = Fs/2 = 2500 Hz; highest signal frequency F2 = 1000 Hz < 2500 Hz. ✅

> 🚩 Phrase as "Nyquist = Fs/2 = 2500 Hz; max **signal** freq 1000 Hz < 2500" — never write "Fmax = Fs/2" (conflates the signal's max frequency with the Nyquist limit → lost point).

## P4-5 -- filter the signal with filter(), compare before/after  ✅

```matlab
xa_filt = filter(b,a,xa_sampled);
plot(t4, xa_sampled, t4, xa_filt); legend('Før','Efter')
```

LP filter (fc ≈ 400 Hz): the **50 Hz** component passes ~unchanged in amplitude; the **1000 Hz** component is heavily attenuated → output ≈ smooth 50 Hz tone. Because it's **IIR (non-linear phase)** the surviving 50 Hz is slightly phase-delayed and there is a short start-up transient.

> 🚩 "Kommentér forskellen før/efter" → plot both on one figure *and* mention the IIR phase delay + initial transient, not just "high freqs gone".

---

# Exam-day takeaways for F25

> Filter problems complete: **Q2 ✅** (IIR HP via BLT) and **Q4 ✅** (filter realization + application). Q1 and Q3-3 deferred math.

- **Patterns used:**
  - IIR highpass via BLT 5-step pipeline (prewarp → order → prototype → `lp2hp` → `bilinear` → `freqz` dB) — HP order ratio inverted `ν_s=Ω_p/Ω_s`, no order doubling.
  - Reading `b`/`a` off a **Direct Form I** block diagram; feedback-gain **sign flip** into the `a` vector.
  - FIR-vs-IIR from structure (feedback ⇒ IIR); poles/zeros via `roots`, stability via `max(abs(poler))<1`.
  - Sampling/aliasing: Nyquist = Fs/2 vs max signal frequency; `filter(b,a,x)` and before/after comparison.
- **What tripped me up:**
  - Q4-1: swapped the *Direct Form I* justification ("2 delay chains") with the *IIR* justification (feedback). They are different arguments.
  - Q4-4: wrote "Fmax = Fs/2" — mislabels max signal freq as the Nyquist limit.
  - `frequency_vec` is a two-sided FFT helper; wrong for one-sided `freqz` plots and for `freqs`.
- **Quick reference if this comes up again:**
  - HP order ratio: `ν_s = Ω_p/Ω_s` (LP is the inverse). `lp2hp`/`lp2lp` take **one** cutoff, don't double order; `lp2bp`/`lp2bs` double it.
  - `bilinear`/`freqz` use **Hz**; `freqs` uses **rad/s**.
  - Causal IIR stable ⇔ all poles strictly inside unit circle.
