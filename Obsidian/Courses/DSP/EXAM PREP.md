# DSP — EXAM PREPARATION MASTER NOTE  
*DTU 62743 — Digital Signal Processing*

This is your **central exam command center**:  
All topics → heatmap → attack plan → risk map.  
Use this page as the index for all other notes (Uge X, Home Assignments, DSP Bible, Exams).

---

# 1) DSP TOPIC MAP  
Full overview of everything examinable.

## A. Discrete-Time Signals & Sampling
- Basic sequences: δ[n], u[n], exponentials, cosines  
- Operations: shift, scale, reverse  
- Even/odd, energy/power signals  
- DT sinusoid properties, normalized frequency, periodicity  
- Sampling and aliasing intuition  

### Linked Exercises
- [[E23 Exam]] — Problem 3 (part 1): analog ↔ digital frequency, aliasing conditions (🟥, conceptual + computational)  
- [[F24 Exam]] — (sampling sub-problem, if present in set): sanity check for discrete-time frequency mapping (🟧, conceptual)

---

## B. LTI Systems in Time Domain
- Impulse response h[n]  
- Convolution y[n] = x[n] * h[n]  
- Step response ↔ impulse response  
- Causality, stability (BIBO), FIR vs IIR  
- Difference equations ↔ system behavior  

### Linked Exercises
- [[Uge 4 Tirsdag]] — Frequency response from difference equation, classification of system (🟥, derivation-based + MATLAB)  
- [[E23 Exam]] — Problem 1: step → impulse, FIR classification, cascade interpretation (🟥, derivation + conceptual)  
- [[F24 Exam]] — Problem 1: impulse response from two step-like outputs, H(z) from h[n] (🟥, computational + conceptual)

---

## C. DTFT & Frequency Response
- DTFT definition & inverse  
- Properties (shift, modulation, conjugation, Parseval)  
- Magnitude/phase response  
- Ideal filters, non-causal nature  

### Linked Exercises
- [[Uge 4 Tirsdag]] — Full analytic |H(ω)| and ∠H(ω) from difference equation + MATLAB plot check (🟥, derivation + MATLAB)  
- [[E23 Exam]] — Problem 1-2/1-3: H(ω), magnitude & phase of symmetric FIR, analytic vs `freqz` (🟥, derivation + MATLAB)  

---

## D. z-Transform & Inverse z
- Definition, ROC, convergence  
- Properties, common z-pairs  
- Inverse z via:  
  - Partial fractions  
  - Power series  
- Poles/zeros, stability, causality  
- ROC reasoning patterns  

### Linked Exercises
- [[E23 Exam]] — Problem 3-2/3-3: ROC, IIR stability, inverse system, pole-zero/ROC reasoning (🟥, conceptual + derivation)  
- [[F24 Exam]] — IIR ROC/inverse sub-question (🟥, conceptual + derivation, exam-style ROC traps)

---

## E. System Function H(z)
- H(z) from difference equation  
- Impulse response from H(z)  
- Minimum-phase & allpass  
- Inverse systems (existence, stability, causality)  

### Linked Exercises
- [[Uge 4 Tirsdag]] — Implicit H(z) via substitution z = e^{jω}, classification as stable/causal (🟧, computational)  
- [[E23 Exam]] — Problems 1 & 2: FIR H(z) from h[n], IIR H(z) from prototype via BLT, inverse systems (🟥, derivation-heavy)  
- [[F24 Exam]] — Problem 1–2: H(z) derivation and pole/zero-based stability check (🟥, computational)

---

## F. DFT / IDFT
- Definitions & matrix form  
- Periodicity in x[n] and X[k]  
- DFT of basic sequences  
- IDFT reconstruction  

### Linked Exercises
- [[E23 Exam]] — Problem 4 (partly): interpretation of discrete spectral bins for noisy tones (🟧, computational + conceptual)  
- (For hand-DFT details, use separate notes: `[[Ugesedler uge 05 - uge 07]]` / your DFT exercise markdown when created.)

---

## G. Circular Convolution
- Relation to DFT multiplication  
- Zero-padding to emulate linear convolution  
- Time-shifts in circular domain  

### Linked Exercises
- (Planned) Link to your future `circconv` implementation note based on Uge 07 exercises.

---

## H. FFT & Spectrum Analysis
- `fft` / `ifft` / `fftshift` patterns  
- Δf, TW, F_N, bin–frequency mapping  
- Amplitude scaling (divide by N)  
- Spectrum interpretation & axis construction  

### Linked Exercises
- [[Uge 12 - Tirsdag]] — FFT-based spectra before/after decimation & interpolation, axis construction (🟧, MATLAB-heavy)  
- [[Uge 12 - Torsdag]] — FFT-based bandpass spectra under different sampling frequencies (🟧, MATLAB-heavy)  
- [[E23 Exam]] — Problem 4: use FFT to estimate amplitudes of tones before/after FIR HP filtering (🟥, MATLAB + interpretation)

---

## I. Sampling, Aliasing, Interpolation
- Analog → DT frequency mapping  
- Aliased frequency computation  
- Upsampling & imaging  
- Downsampling & aliasing  

### Linked Exercises
- [[Uge 12 - Tirsdag]] — Multirate DSP (M=2 decimation, L interpolation, AA and interpolation filters) (🟧, conceptual + MATLAB)  
- [[Uge 12 - Torsdag]] — Bandpass sampling / under-sampling of AM signal, integer-band positioning, admissible Fs intervals (🟥, conceptual + computational)  
- [[E23 Exam]] — Problem 3-1: Sampling/aliasing reasoning + consistent mapping between F, f, ω (🟥, conceptual)  
- [[F24 Exam]] — Sampling/aliasing sub-problem (🟧, conceptual + quick calculations)

---

## J. FIR Filter Design
- Frequency sampling method  
- Fourier-series-based FIR  
- Window method  
- Linear-phase Types I–IV  
- Parks–McClellan concept  

### Linked Exercises
- [[Uge 11 - Tirsdag]] — FIR LP/BP via Fourier transform (ideal response → h[n] → causal coefficients) (🟥, derivation + MATLAB)  
- [[Uge 11 - Torsdag]] — FIR LP via windowing + Hamming vs rectangular, FIR via frequency-sampling (🟥, design + interpretation)  
- [[E23 Exam]] — Problem 4: High-pass FIR via truncated Fourier series + spectral inversion + delay (🟥, derivation + implementation)  
- [[F24 Exam]] — FIR-related design sub-problem (likely HP/LP design from specs) (🟥, derivation + exam-format computation)

---

## K. IIR Filter Design (BLT)
- Bilinear Transform mapping  
- Pre-warping formulas  
- Butterworth & Chebyshev prototypes  
- Order formulas  
- LP ↔ HP transformations  

### Linked Exercises
- [[Uge 10 - Tirsdag]] — IIR low-pass via BLT: prewarp → analog prototype → BLT → H(z) → diff eq (🟥, computational + derivation)  
- [[Uge 10 - Torsdag]] — IIR high-pass + bandpass via BLT: LP→HP + LP→BP transforms (🟥, computational + MATLAB)  
- [[E23 Exam]] — Problem 2: Chebyshev type-I HP via BLT (full exam pipeline with order, analog design, BLT) (🟥, derivation + MATLAB)  
- [[F24 Exam]] — IIR BLT problem (Butterworth/Cheby design from spec) (🟥, computational + derivation)

---

# 2) EXAM HEATMAP  
Likelihood + importance for each topic.

| Topic | Importance | Notes |
|-------|------------|-------|
| LTI + Convolution | 🟥 | 100% appears; fast convolution / h[n] tricks needed |
| DTFT & Properties | 🟥 | Evaluate or use properties for shortcuts |
| z-Transform + ROC | 🟥 | Core of big multi-part questions |
| H(z) + Stability | 🟥 | Poles/zeros → system analysis |
| DFT/IDFT | 🟥 | Small N computations guaranteed |
| FIR Design | 🟥 | Uge 11 + exams = strong predictor |
| IIR via BLT | 🟥 | Always one full problem |
| FFT & Δf | 🟧 | Often in practical question |
| Sampling/Aliasing | 🟧 | High probability subquestion |
| Allpass/Min-Phase | 🟧 | Often conceptual sub-part |
| Multirate basics | 🟨 | Sometimes appears in small 1–2 point items |

---

# 3) ATTACK PLAN (WEEK BEFORE EXAM)

## Day 1 — Foundations
- DT signals, convolution, LTI properties  
- Derive h[n] from difference eq quickly  
- Mini-sheet: core z-pairs + ROC rules  

## Day 2 — H(z), ROC, Minimum-Phase
- Difference eq → H(z) → poles & zeros  
- Decide causality, stability, inverse existence  
- Practice inverse z (partial fractions)  

## Day 3 — DFT/IDFT + Circular Conv
- Re-derive DFT/IDFT by formula for N=4,8  
- Zero-padding rules  
- FFT scaling + Δf/Nyquist drills  

## Day 4 — Sampling & FIR
- Aliasing derivations  
- FIR linear-phase classification  
- Frequency sampling FIR practice  

## Day 5 — IIR via BLT
- Pre-warp → order → prototype → BLT  
- Butterworth & Cheby workflows  

## Day 6 — Full Mock Exam
- Sit a past exam 100% timed  
- Analyze where you lose points/time  

## Day 7 — Condensed Review
- Make two mini-sheets:  
  1. Formulas  
  2. Tricks & Mistakes  
- Flashcards for DTFT pairs, z-pairs, BLT, FIR types  

---

# 4) RISK LEVEL (HONEST ASSESSMENT)

## Strengths  
- MATLAB workflow  
- DFT/FFT understanding  
- Detailed notes and strong structure  

## Medium-Risk Areas  
- ROC classification (tricky mixed cases)  
- Inverse z for two-sided sequences  
- Minimum-phase vs allpass decision logic  
- FIR linear-phase indexing (off-by-one traps)  
- Butterworth/Cheby order formulas under pressure  

## High-Risk Under Time Pressure  
- Partial fractions algebra  
- Fast evaluation of DTFT using properties  
- Pre-warping + BLT small details  

## Overall  
- **Conceptual risk: Low–Medium**  
- **Execution / speed risk: Medium–High**  
- **Grade potential: High**, if time control + drills are enforced.

---

# 5) 🔥 HIGH-RISK ERRORS (PATTERNS FROM EXERCISES & EXAMS)

From `[[Uge 4 Tirsdag]]`, weeks 10–12, and `[[E23 Exam]]` + `[[F24 Exam]]`:

1. **Sign / index mistakes in h[n] and H(z)**  
   - Dropping a minus sign when going from difference equation → frequency response.  
   - Misplacing exponents in z^{-k} when rewriting from h[n].  

2. **BLT & prewarping slips**  
   - Forgetting to convert Hz → rad/s or rad/sample.  
   - Using $F_p$ instead of $\omega_p$ in prewarp formulas.  
   - Swapping passband/stopband edges in HP/BP designs.

3. **ROC + stability / causality confusion**  
   - Not tying ROC to pole magnitudes correctly.  
   - Forgetting that inverse systems swap zeros ↔ poles and can break stability.

4. **FIR linear-phase indexing**  
   - Off-by-one around $K = M/2$ when mapping $h[n]$ ↔ $b[n]$.  
   - Forgetting the necessary delay $e^{-j\omega K}$ factor in frequency-domain expressions.

5. **FFT scaling & frequency axis**  
   - Missing the 1/N factor when interpreting amplitudes.  
   - Misaligning axes when using `fftshift` (wrong Δf or range).

6. **Bandpass sampling region mistakes**  
   - Plugging $F_L, F_H$ into the inequality
     $$
     \frac{2F_H}{k} \le F_s \le \frac{2F_L}{k-1}
     $$
     with the wrong k or using the wrong edges.  
   - Forgetting that even vs odd “m” changes inversion.

---

# 6) MUST-REVISIT EXERCISES (HIGHEST EXAM VALUE)

Do these again **on paper**, then verify with your existing solution notes:

1. **IIR via BLT**
   - [[Uge 10 - Tirsdag]] — full LP BLT design with numeric specs.  
   - [[Uge 10 - Torsdag]] — HP + BP transforms, including prewarp and analog prototypes.  
   - [[E23 Exam]] — Problem 2 (Chebyshev HP design).

2. **FIR Design**
   - [[Uge 11 - Tirsdag]] — LP / BP Fourier-transform method.  
   - [[Uge 11 - Torsdag]] — windowing vs frequency-sampling.  
   - [[E23 Exam]] — Problem 4 (HP FIR via Fourier series).

3. **Sampling / Multirate / Under-sampling**
   - [[Uge 12 - Tirsdag]] — decimation & interpolation chain, AA/interpolation filters.  
   - [[Uge 12 - Torsdag]] — bandpass sampling / integer band positioning.  
   - [[E23 Exam]] — Problem 3-1 (aliasing) and Problem 3-2/3-3 (link to IIR ROC).

4. **LTI + H(z) Core**
   - [[Uge 4 Tirsdag]] — frequency response from difference equation.  
   - [[E23 Exam]] — Problem 1 (step → impulse → H(z)).  
   - [[F24 Exam]] — Problem 1 (impulse response from table data).

---

# 7) MATLAB I MUST RERUN BEFORE EXAM

Open and re-execute these Live Scripts / scripts, focusing on **understanding each line**, not just the outputs:

- `UGE10/Tirsdag.mlx` — IIR LP BLT pipeline  
- `UGE10/Torsdag.mlx` — IIR HP/BP BLT pipeline  
- `UGE11/Tirsdag.mlx` — FIR LP/BP Fourier transform design  
- `UGE11/Torsdag.mlx` — Windowed FIR + frequency-sampling FIR  
- `UGE12/Tirsdag.mlx` — Multirate decimation/interpolation (anti-alias & interpolation filters)  
- `UGE12/Torsdag.mlx` — Under-sampling of AM bandpass signal (integer band positioning)  
- `EXAM/E23.mlx` — Full implementation of E23 problems (especially Problems 2–4)  
- `EXAM/F24.mlx` — Full implementation of F24 problems (mirror structure to E23)

When ready:  
Use this page as your index. Jump from each topic to:

- `[[DSP Bible]]`  
- `[[MOC – DSP]]`  
- `[[Uge 4 Tirsdag]]`, `[[Uge 10 - Tirsdag]]`, `[[Uge 10 - Torsdag]]`  
- `[[Uge 11 - Tirsdag]]`, `[[Uge 11 - Torsdag]]`  
- `[[Uge 12 - Tirsdag]]`, `[[Uge 12 - Torsdag]]`  
- `[[E23 Exam]]`, `[[F24 Exam]]`
