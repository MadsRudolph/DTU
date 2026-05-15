---
type: walkthrough
tags: [DSP, reexam, exam, F24, walkthrough]
aliases:
  - F24 walkthrough
  - F24 exam log
---
# F24 exam -- MATLAB walkthrough

> [!info] What this note is
> Step-by-step log of how I'm solving the **F24 exam** in [[62743 F24 Exam.pdf]].
> One section per sub-question. Each section explains *what the MATLAB code is doing* and *why*, not just the answer.
>
> Theory is offloaded to [[LTI z-transform flow]] and other topic notes -- this note links back instead of duplicating.

**Exam PDF:** [[62743 F24 Exam.pdf]] (alt: [[62743 F24 Exam-1.pdf]] -- the two are essentially identical)
**Solution PDF:** [[62743 F24 Exam student solutions1.pdf]]
**Working script:** `3.semester/DSP/EXAMS/F24.m` (outside vault)

---

# Problem 1 -- LTI system identification from input/output pairs, then cascade

**Topic mix:** T1 (LTI properties, linearity), T3 (Z-transform, ROC, stability), T4 (cascade).

**Setup from exam:**
- $x_1[n] = 3\delta[n] + 2\delta[n-1]$, $x_2[n] = \delta[n] + 2\delta[n-1]$
- $y_1[n], y_2[n]$ given in a table for $n = 0\ldots 4$, both zero outside.
- System is LTI.

---

## P1-1 -- Compute $x_1[n] - x_2[n]$

**Theory:** just arithmetic on weighted impulses.

$$
x_1[n] - x_2[n] = (3-1)\delta[n] + (2-2)\delta[n-1] = \mathbf{2\,\delta[n]}
$$

**Why we care:** we've now constructed a clean (scaled) impulse on the input side. This is the setup for 1-2.

---

## P1-2 -- Verify $h[n] = 4\delta[n] - 12\delta[n-1] + \delta[n-2] - 3\delta[n-3]$

**Theory:** LTI linearity. The impulse response $h[n]$ is the system's output for input $\delta[n]$.

**The trick (DTU canonical pattern -- memorise):**

From 1-1: $\delta[n] = \tfrac{1}{2}(x_1[n] - x_2[n])$. By **linearity** of the system, the same combination applies to outputs:

$$
h[n] = \tfrac{1}{2}\big(y_1[n] - y_2[n]\big)
$$

Plug in the table:

| $n$ | $y_1-y_2$ | $h[n]$ |
|---|---|---|
| 0 | 8 | **4** |
| 1 | -24 | **-12** |
| 2 | 2 | **1** |
| 3 | -6 | **-3** |
| 4 | 0 | 0 |

$$\Rightarrow \mathbf{h[n] = 4\delta[n] - 12\delta[n-1] + \delta[n-2] - 3\delta[n-3]} \quad \checkmark$$

### 🚩 Pattern: linearity extraction

Any time an exam gives **two input/output pairs** and asks for $h[n]$:
1. Find a linear combo of inputs that equals $\delta[n]$ (possibly scaled).
2. Apply the **same** combo to outputs.
3. That's $h[n]$ (divided by the scale factor).

No difference equation needed. No z-transform yet.

### 📘 Where this is in the slides (verified with NotebookLM)

**Primary:** Iver, Uge 2 Tirsdag — [[Uge_02_ti.pdf]]:
- **Slide 11/25** — Linearity definition: $T(\alpha_1 x_1 + \alpha_2 x_2) = \alpha_1 T(x_1) + \alpha_2 T(x_2)$.
- **Slide 12/25** — "Lineære systemer er linearkombinations-respekterende": if $Tx_1 = y_1$ and $Tx_2 = y_2$, then $\alpha_1 x_1 + \alpha_2 x_2 \xrightarrow{T} \alpha_1 y_1 + \alpha_2 y_2$. **This is the slide that justifies the trick.**
- **Slide 15/25** — Impulse response definition: $h = T\delta$.

**Reinforcement:** Iver, Uge 2 Torsdag — [[Uge_02_to.pdf]] — links linearity to **linear difference equations**: a linear diff eq with **trivial initial conditions** defines a linear system; with **initial rest** ("initialt i hvile") defines an LTI system. Useful framing for 1-4.

**Textbook:** [[Champagne and Labeau 2004 Discrete Time Signal Processing.pdf|Champagne & Labeau]], **page 20** — formal definition of linearity for discrete systems.

So the F24 Q1-2 trick is just slide 12 + slide 15 chained together: build $\delta$ as a linear combo of inputs → by linearity, $h$ is the same combo of outputs.

---

# Problem 2 -- Anti-aliasing filter (analog Butterworth LP)

**Topic mix:** T6 (sampling, aliasing), T9 (IIR / analog filter design via prototype + transformation).

**Setup from exam:**
- Analog signal: $x_A(t) = 3\cos(2\pi \cdot 200\, t) + 1.5\cos(2\pi \cdot 750\, t)$.
- Sampled by a sampler running at $F_s$ Hz.
- Eventually we design an analog AA filter: 4th-order Butterworth LP, $F_p = 350$ Hz.

**The engineering story:** 750 Hz aliases at $F_s = 1000$. The AA filter kills the 750 Hz component *before* it hits the sampler, so the alias never appears.

---

## P2-1 -- Minimum sampling frequency

Nyquist: $F_s \geq 2 F_\text{max}$, equivalently $F \leq F_s/2$.

$F_\text{max} = F_2 = 750$ Hz $\Rightarrow$ $\boxed{F_s^\text{min} = 1500\,\text{Hz}}$ ✅

---

## P2-2 -- Aliasing at $F_s = 1000$ Hz

**a)** $F_s = 1000 < 1500$ → Nyquist violated → **aliasing occurs**.

**b) DTU folding formula:**

$$F_\text{alias} = F_2 - 2\left(F_2 - \tfrac{F_s}{2}\right) = 750 - 2(750-500) = \boxed{250\,\text{Hz}}$$

Conceptually: $F_2$ is 250 Hz above the fold at $F_s/2 = 500$ → bounces to 250 Hz below the fold = 250 Hz.

Solution remark: "*Det er acceptabelt kun at fremhæve komponenten ved +250 Hz og ikke ved -250 Hz.*"

---

## P2-3 -- MATLAB FFT to visualise the aliasing

```matlab
Fs = 1000;
N  = 1e5;
Ts = 1/Fs;
t  = (0:N-1) * Ts;

A1 = 3;    F1 = 200;
A2 = 1.5;  F2 = 750;
xA = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);

XA = fftshift( fft(xA) ) / N;
f  = (-N/2 : N/2-1) * (Fs/N);

figure;
plot(f, abs(XA), 'LineWidth', 1.5);
xlabel('f·F_s  [Hz]'); ylabel('|X_A[k]|');
title('Spectrum of x_A[n], F_s = 1000 Hz'); grid on;
```

**Expected peaks** (matches solution p. 7):
- 200 Hz, amplitude 1.5 (= $A_1/2$ — two-sided spectrum halves the cosine amplitude).
- 250 Hz, amplitude 0.75 (= $A_2/2$ — **the aliased 750 Hz**).
- Mirror peaks at -200 and -250 Hz.

Why divide by `N`: scales the FFT so that a unit-amplitude cosine shows as 0.5 on each side. Standard DTU convention.

---

## P2-4 -- Design the AA filter (the filter question)

**Spec:** 4th-order Butterworth, LP, $F_p = 350$ Hz.

### a) Prototype filter (from exam appendix, $n=4$)

$$H_\text{proto}(s) = \frac{1}{s^4 + 2.6131\,s^3 + 3.4142\,s^2 + 2.6131\,s + 1}$$

- $\beta_0 = 1$
- $\alpha_4 = 1, \alpha_3 = 2.6131, \alpha_2 = 3.4142, \alpha_1 = 2.6131, \alpha_0 = 1$

### b) Transform prototype to LP with cutoff $F_p = 350$ Hz

> 🚩 **Critical:** `lp2lp` wants $\Omega_p$ in **rad/s**, not Hz. $\Omega_p = 2\pi F_p$.

```matlab
b_proto = 1;
a_proto = [1, 2.6131, 3.4142, 2.6131, 1];

Fp = 350;
Wp = 2*pi*Fp;                          % Hz -> rad/s
[b_AA, a_AA] = lp2lp(b_proto, a_proto, Wp);
H_AA = tf(b_AA, a_AA)
```

**Expected** (matches solution p. 8):

$$H_{AA}(s) = \frac{2.339 \times 10^{13}}{s^4 + 5747\,s^3 + 1.651\times 10^7\,s^2 + 2.779 \times 10^{10}\,s + 2.339 \times 10^{13}}$$

Sanity check: DC gain = $\beta_0 / \alpha_0 = 1$. ✅

---

## P2-5 -- Magnitude response via `freqs`

`freqs` = "frequency response, **s**-domain" (analog). Compare with `freqz` = "**z**-domain" (digital, used in Q4).

```matlab
F = linspace(0, 2000, 4096);     % Hz
W = 2*pi*F;                      % rad/s
H_response = freqs(b_AA, a_AA, W);

figure;
plot(F, abs(H_response), 'LineWidth', 1.5);
xlabel('F  [Hz]'); ylabel('|H_{AA}(F)|');
title('Magnitude of anti-aliasing filter'); grid on;
```

**Key readings** (solution p. 9):

| $F$ [Hz] | $|H_{AA}|$ | meaning |
|---|---|---|
| 200 | 0.994 | signal of interest passes through |
| 350 | 0.707 = $1/\sqrt{2}$ | **3 dB point — *definition* of Butterworth cutoff** |
| 750 | 0.047 | aliasing component killed (~26 dB attenuation) |

---

## 🚩 Pattern: analog Butterworth filter design (memorise)

Re-usable on **every** analog filter-design exam question:

| Step | What | MATLAB |
|---|---|---|
| 1 | Look up prototype coefs (order $n$ from spec) | hardcode `b_proto`, `a_proto` |
| 2 | Cutoff Hz → rad/s | `W = 2*pi*F` |
| 3 | Transform LP→{LP, HP, BP, BS} | `lp2lp` / `lp2hp` / `lp2bp` / `lp2bs` |
| 4 | Pretty-print as TF | `H = tf(b, a)` |
| 5 | Evaluate on frequency grid | `freqs(b, a, 2*pi*F)` |
| 6 | Plot magnitude (or dB) | `plot(F, abs(H))` / `plot(F, 20*log10(abs(H)))` |

Q4 is the **same recipe with two additions**: prewarping the digital edges, and one extra step (`bilinear`) at the end to go analog → digital.

### 📘 Where this is in the slides (verified with NotebookLM)

- **Butterworth prototype table** -- [[62743 E25 Digital filter design FIR part1.pdf]] slide **10**, repeated in [[62743 E25 Digital filter design IIR part3.pdf]] slide **44**.
- **`lp2lp` transformation** ($s \to s/\Omega_p$) -- [[62743 E25 Digital filter design IIR part3.pdf]] slides **40** (math), **41** (MATLAB command), and **134** (worked example "Example 3 - Step 4").
- **`freqs` command** for analog frequency response -- [[62743 Matlab commands used in the course 2024_11_22.pdf]] pages **33–34** (syntax + snippet). Applied in [[62743 E25 Digital Signal Processing Uge 10 Torsdag solutions.pdf]] page **8** (`H2analog = freqs(B2,A2,omegaanalog);`).

---

# Problem 3 -- Sampling theorem in angular form + small FIR + min-phase decomposition

**Topic mix:** T6 (sampling, Nyquist in $\Omega$), T1 (FIR impulse response), T11 (all-pass / min-phase decomposition).

---

## P3-1 -- Apply Nyquist to a band-limited spectrum

**Setup:** $f_a(t)$ has a trapezoidal Fourier spectrum that touches zero at $\pm 200$ rad/s (read straight off the graph).

**Same theorem as P2-1, but in angular form** (multiply both sides of $F_s \geq 2 F_\text{max}$ by $2\pi$):

$$\Omega_s \;\geq\; 2\,\Omega_\text{max}$$

From the plot: $\Omega_\text{max} = 200$ rad/s, so threshold is $2 \cdot 200 = 400$ rad/s.

| Case | $\Omega_s$ | vs $2\Omega_\text{max}=400$ | Verdict |
|---|---|---|---|
| (a) | 200 rad/s | $200 < 400$ | ❌ aliasing |
| (b) | 400 rad/s | $400 = 400$ | ✅ just met (boundary case accepted) |
| (c) | 500 rad/s | $500 > 400$ | ✅ met |

### Intuition (spectrum replication)
Sampling at $\Omega_s$ creates copies of the original spectrum centred at every $k\Omega_s$. Each copy is $2\Omega_\text{max}$ wide. To avoid overlap: copy spacing ($\Omega_s$) must be at least copy width ($2\Omega_\text{max}$).

### 📘 Where this is in the slides (verified with NotebookLM)

The angular-frequency form $\Omega_s \geq 2\Omega_\text{max}$ shows up in three of Maryam's decks:

- [[62743 E25 Under Sampling.pdf]] -- slides **13** (theorem statement) and **16** (case-split as $\Omega_\text{max} \leq \tfrac{1}{2}\Omega_s$).
- [[DSP-Marta-Uge07-torsdag.pdf]] -- slides **2** and **13** (same case-split + theorem).
- [[DSP-Marta-Uge07-tirsdag.pdf]] -- slides **13** and **16** (identical statements).

In Maryam's handwritten notes (`Uge_07_ti_og_to_Marta.pdf`) the same theorem is on pages 4 and 12, but she uses $\Omega_N$ for the band limit instead of $\Omega_\text{max}$.

### 🚩 Pattern: "is sampling OK?" 3-step procedure
1. Read $\Omega_\text{max}$ (or $F_\text{max}$) -- highest non-zero frequency.
2. Threshold = $2\Omega_\text{max}$ (or $2F_\text{max}$).
3. Compare each $\Omega_s$ against threshold. $<$ → alias. $\geq$ → OK.

Same procedure for P3-2 (different signal, same candidates).

---

## P3-2 -- Same Nyquist check, different signal

**Setup:** another band-limited signal $g_a(t)$ with $\Omega_\text{max} = 250$ rad/s.

Threshold: $2 \cdot 250 = 500$ rad/s.

| Case | $\Omega_s$ | vs $2\Omega_\text{max}=500$ | Verdict |
|---|---|---|---|
| (a) | 200 rad/s | $200 < 500$ | ❌ aliasing |
| (b) | 400 rad/s | $400 < 500$ | ❌ aliasing |
| (c) | 500 rad/s | $500 = 500$ | ✅ just met (boundary) |

**Only candidate (c) works.** Same 3-step procedure as P3-1.

---

## P3-3 / P3-4 -- DEFERRED (math, not filter)

P3-3 (small FIR $h[n]$ from a difference equation) and P3-4 (min-phase / all-pass decomposition) are **math questions**, deferred per the filter-first strategy. Not yet worked. Solutions are on pages 11–12 of [[62743 F24 Exam student solutions1.pdf]] if needed later.

---

# Problem 4 -- IIR båndstop Butterworth via BLT (the full digital IIR pipeline)

**Topic mix:** T9 (IIR design, bilinear, prewarp, Butterworth).

**Spec:** BLT with $\alpha = 2/T_s$; IIR bandstop Butterworth; $F_s = 5000$ Hz; digital normalized edges $f_{pL}=45/F_s$, $f_{pH}=55.5/F_s$, $f_{sL}=48/F_s$, $f_{sH}=52.1/F_s$; $A_{pdB}=3$ dB, $A_{sdB}=20$ dB.

## The 5-step pipeline (memorise — every IIR-via-BLT question)

```
1. Digital edges (Hz)  --PREWARP  Ω = 2·Fs·tan(π·f)-->  2. Analog edges Ω
3. Order n from A_p, A_s, ν_s  -->  prototype H_proto(s) from appendix
4. lp2bs (or lp2lp/lp2bp/lp2hp)  -->  analog band filter H_BS(s)
5. bilinear (BLT)  -->  digital H_BS(z)   -->  verify with freqz, dB
```

**Why prewarp:** the BLT warps the frequency axis non-linearly; prewarping pre-distorts the analog edges so they land correctly after BLT.
**Why order doubles in step 4:** `lp2bs`/`lp2bp` are *band* transforms — a prototype of order $n$ → analog BS/BP of order $2n$. (`lp2lp`/`lp2hp` don't double.)

---

## P4-1 -- Prewarp + order + prototype

### (a) Prewarp the four digital edges

$$\Omega = \frac{2}{T_s}\tan\!\left(\frac{\omega}{2}\right) = \frac{2}{T_s}\tan(\pi f) = 2 F_s \tan(\pi f)$$

```matlab
omega_pL = fpL*2*pi;   Omega_pL = (2/Ts)*tan(omega_pL/2);
omega_pH = fpH*2*pi;   Omega_pH = (2/Ts)*tan(omega_pH/2);
omega_sL = fsL*2*pi;   Omega_sL = (2/Ts)*tan(omega_sL/2);
omega_sH = fsH*2*pi;   Omega_sH = (2/Ts)*tan(omega_sH/2);
```

**Expected** (solution p. 13): $\Omega_{sL}\approx 3.01\cdot10^2$, $\Omega_{sH}\approx 3.27\cdot10^2$, $\Omega_{pL}\approx 2.82\cdot10^2$, $\Omega_{pH}\approx 3.49\cdot10^2$ rad/s.

### (b) Minimum prototype order

$$\nu_s = \frac{\Omega_{pH}-\Omega_{pL}}{\Omega_{sH}-\Omega_{sL}}, \quad \varepsilon^2 = 10^{0.1A_{pdB}}-1, \quad n \geq \frac{\log_{10}\!\Big(\frac{10^{0.1A_{sdB}}-1}{\varepsilon^2}\Big)}{2\log_{10}(\nu_s)}$$

```matlab
vs     = (Omega_pH - Omega_pL) / (Omega_sH - Omega_sL);
eps_sq = 10^(0.1*ApdB) - 1;                                   % epsilon^2
n = ceil( log10( (10^(0.1*AsdB) - 1) / eps_sq ) / (2*log10(vs)) )
```

**Expected:** unrounded ≈ 2.44 → `ceil` → **n = 3**.

> 🚩 Two traps: (1) the division by $\varepsilon^2$ goes **inside** the `log10`; (2) always `ceil` (never round/floor) — minimum order must satisfy the inequality. With $A_{pdB}=3$ dB, $\varepsilon^2\approx1$ so trap (1) is nearly invisible here but bites on other specs.

### (c) Prototype TF for n = 3 (appendix)

$$H_\text{proto}(s) = \frac{1}{s^3 + 2s^2 + 2s + 1}$$

```matlab
proto_num = 1;
a_proto   = proto_den{3};      % [1 2 2 1]
H_Proto   = tf(proto_num, a_proto)
```

---

## P4-2 -- Analog bandstop via `lp2bs`

### (a) Transform

$$\Omega_0 = \sqrt{\Omega_{pL}\,\Omega_{pH}} = \sqrt{\Omega_{sL}\,\Omega_{sH}} \quad (\text{geometric centre}), \qquad W = \Omega_{pH} - \Omega_{pL} \quad (\text{bandwidth})$$

```matlab
Omega_0 = sqrt(Omega_pL*Omega_pH);
W       = Omega_pH - Omega_pL;
[num_bs, den_bs] = lp2bs(proto_num, proto_den{3}, Omega_0, W);
H_bs = tf(num_bs, den_bs)
```

**Expected** (solution p. 15): $\Omega_0 \approx 3.14\cdot10^2$ rad/s, $W \approx 66$ rad/s, resulting filter **order 6** (3 doubled).

### (b) Plot magnitude

```matlab
omega_grid = 0:0.1:1000;
h = freqs(num_bs, den_bs, omega_grid);
figure; plot(omega_grid, abs(h), 'LineWidth', 1.5);
xlabel('\Omega [rad/s]'); ylabel('|H_{BS}(\Omega)|');
title('Magnitude af analogt båndstopfilter'); grid on;
```

Clean notch centred near $\Omega_0\approx314$ rad/s, dipping to 0; passband ≈ 1 elsewhere.

---

## P4-3 -- BLT to digital + verify

### (a) `bilinear` + dB plot

```matlab
[bz, az] = bilinear(num_bs, den_bs, Fs);     % Fs in Hz (NOT rad/s)
[H,f] = freqz(bz, az, 4096, Fs);             % f returned in Hz
figure; plot(f, 20*log10(abs(H)));           % dB, not linear
xlabel('f·F_s [Hz]'); ylabel('|H| [dB]');
title('Magnitude Response'); grid on; xlim([40 60]);   % zoom to see the notch
```

> 🚩 Traps: (1) question wants **dB** = `20*log10(abs(H))`, not linear `abs(H)`; (2) default `freqz` range is 0–Fs/2 = 2500 Hz → the 50 Hz notch is invisible, must `xlim`/zoom; (3) `bilinear` and `freqz` take **Fs in Hz** (unlike `freqs` which wants rad/s).

### (b) Read stopband-edge attenuations

```matlab
[H,f] = freqz(bz, az, [fsL*Fs, fsH*Fs], Fs);   % fsL/fsH normalized -> *Fs to get Hz
dB = 20*log10(abs(H));
fprintf('F = %.1f Hz  ->  %.2f dB\n', f(1), dB(1));
fprintf('F = %.1f Hz  ->  %.2f dB\n', f(2), dB(2));
```

**Result obtained:** −24.96 dB @ 48 Hz, −24.13 dB @ 52.1 Hz (solution quotes ≈ −24.5 dB at both; tiny differences from intermediate rounding).

> 🚩 `fsL`/`fsH` are **normalized** ($f=F/F_s$). `freqz(...,Fs)` wants **Hz** → multiply by `Fs`. (`2*pi` is only for *angular* frequency, not Hz.)

### (c) Compare to spec

Spec $A_{sdB}=20$ dB. Actual: −24.96 dB and −24.13 dB — **both stronger than the required 20 dB**, so spec is satisfied at both stopband edges with ~4–5 dB margin. The margin is expected because the exact order was ≈ 2.44 but rounded **up** to 3 → a steeper filter than the bare minimum.

### 📘 Where this is in the slides

- Full BLT/prewarp/lp2bs/bilinear pipeline -- [[62743 E25 Digital filter design IIR part1.pdf]], [[62743 E25 Digital filter design IIR part2.pdf]], [[62743 E25 Digital filter design IIR part3.pdf]] (the IIR design lecture series).
- MATLAB command syntax (`lp2bs`, `bilinear`, `freqz`) -- [[62743 Matlab commands used in the course 2024_11_22.pdf]].
- Truth source: [[62743 F24 Exam student solutions1.pdf]] pages **13–17**.
- *(Precise slide numbers for prewarp/lp2bs/bilinear not yet NLM-verified — re-query if exact citations needed.)*

### 🚩 Pattern: digital IIR BLT design (the full playbook)

```matlab
% 1 SETUP        Fs; Ts=1/Fs; fpL/pH/sL/sH (normalized); ApdB; AsdB
% 2 PREWARP      Omega_x = (2/Ts)*tan(2*pi*f_x/2)         % all four edges
% 3 ORDER        vs = (Omega_pH-Omega_pL)/(Omega_sH-Omega_sL);   % flip for BP
%                eps_sq = 10^(0.1*ApdB)-1;
%                n = ceil( log10((10^(0.1*AsdB)-1)/eps_sq) / (2*log10(vs)) );
% 4 PROTO->BAND  Omega_0=sqrt(Omega_pL*Omega_pH); W=Omega_pH-Omega_pL;
%                [b,a] = lp2bs(1, proto_den{n}, Omega_0, W);     % lp2bp for BP
% 5 BLT          [bz,az] = bilinear(b, a, Fs);
% 6 VERIFY       [H,f]=freqz(bz,az,Fgrid,Fs); plot(f,20*log10(abs(H)));
```

---

# Exam-day takeaways for F24

- **Patterns used:**
  - Linearity extraction for $h[n]$ from two I/O pairs (Q1).
  - Nyquist in Hz (Q2-1/2) and in $\Omega$ (Q3-1/2) — same theorem, watch units.
  - Analog Butterworth design: prototype → `lp2lp` → `freqs` (Q2).
  - **Full IIR BLT pipeline**: prewarp → order → prototype → `lp2bs` → `bilinear` → `freqz` (Q4).
- **What tripped me up:**
  - Hz vs rad/s vs normalized — three different frequency units, each MATLAB function wants a specific one (`freqs`→rad/s, `bilinear`/`freqz`→Hz, prewarp input→normalized).
  - Order formula: division by $\varepsilon^2$ must be **inside** `log10`; always `ceil`.
  - Question wording: "i dB" means `20*log10`, "aflæs" means print the numbers (not plot).
- **Quick reference if this comes up again:** see the two 🚩 pattern boxes (analog Butterworth design + digital IIR BLT playbook) and the gotchas in [[DSP MATLAB helpers cheat sheet]].
