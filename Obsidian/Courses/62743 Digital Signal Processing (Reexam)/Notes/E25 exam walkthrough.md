---
type: walkthrough
tags: [DSP, reexam, exam, E25, walkthrough, handoff]
aliases:
  - E25 walkthrough
  - E25 handoff
  - E25 exam log
---
# E25 exam -- walkthrough & handoff

> [!info] What this note is
> Working log + **cross-PC handoff** for re-solving the **E25 exam** (the
> one that was failed, Dec 2025). Re-solve from the skeleton, verify every
> answer against the official solution PDF.

**Exam PDF:** `Obsidian/Archive/3rd Semester/DSP/62743 E25 Exam v3.pdf`
**Solution PDF (TRUTH SOURCE):** `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/Solutions/62743 E25 Exam student solutions.pdf`
**Working script:** `3.semester/DSP/EXAMS/E25_new.m` (skeleton built, all 3 problems scaffolded)
**Do NOT trust:** `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/E25 Exam.md` — own post-exam writeup, contains the P2 error that caused the fail.

> [!warning] Archive PDFs are gitignored
> The solution PDF lives under `Obsidian/Archive/...` which is gitignored —
> it will **not** sync via git. On the other PC it must already be there via
> Drive sync, or re-copy it from Downloads into the `Solutions/` folder.

---

## ▶️ PICK UP HERE

Re-solve **E25** filter-first: **P2 → P3 → P1**.

**Status (verified vs official solution PDF):**
- ✅ **P2 COMPLETE** — 2-1…2-5 all solved & verified (DF-II trap fixed; filtered amplitudes 0.50/0.98/0.044 → −30.6 dB ≈ 2-1).
- ✅ **P3 partial** — 3-1 (rect window, N=9, M=8, K=4), 3-2 (`FIR_fourier("HP",…)`, causal shift by K), 3-3 (freqz dB, meets ≥20 dB) all done.
- ⏭️ **NEXT = P3-4** — phase response + linearity argument from impulse-response symmetry (Type-I FIR). Then 3-5 (redesign As=40 dB → Hann, N=31), 3-6 (verify).
- ⬜ **P1 not started** — Z-transform math (40%). Answers below if time runs short.

Hints-first: attempt, then ask for a check. "walk me through PX-Y" for the guided version.

---

## 🚩 P2 — the trap that failed E25 (most important)

The filter is **Direct Form II**. The feedback gains −0.4860 and −0.0177
sit **after the 2nd and 4th** `z⁻¹` delay blocks in the diagram, so they
belong to `z⁻²` and `z⁻⁴` — **not** `z⁻¹` and `z⁻²`.

```matlab
B2 = [0.0940, 0.3759, 0.5639, 0.3759, 0.0940];   % z^0 .. z^-4
A2 = [1, 0, 0.4860, 0, 0.0177];                   % z^-2 and z^-4 (zeros between!)
```

$$H(z)=\frac{0.094+0.3759z^{-1}+0.5639z^{-2}+0.3759z^{-3}+0.094z^{-4}}{1+0.486z^{-2}+0.0177z^{-4}}$$

**Verified vs official solution:**

| Check | Official value |
|---|---|
| Dæmpning @ 400 Hz | **−3.01 dB** → matches the stated spec (it IS true) |
| Dæmpning @ 600 Hz | **−30.61 dB** |
| Phase in passband | non-linear (IIR) — expected |
| Stability | stable (all poles inside unit circle) |

> The failed `E25 Exam.md` used `A2=[1,0.486,0.0177]` and wrongly concluded
> "−9 dB @ 400 Hz, spec is wrong". Don't repeat that. Read DF-II delay
> positions carefully.

### P2 rest (verified vs official)
- **2-2:** `zplane(B2,A2)` + impulse response via `filter(B2,A2,imp)`, `imp=[zeros(1,10) 1 zeros(1,30)]`, n=-10:30. Stable (poles inside circle).
- **2-3:** XA = A1cos(2πF1t)+A2cos(2πF2t)+A3cos(2πF3t); F=100/300/600, A=1/2/3; Fs=1600; N=2¹⁴. Max freq w/o aliasing = Fs/2 = **800 Hz**; all components < 800 → no aliasing. `t=0:Ts:(N-1)*Ts`, plot 0–0.05 s.
- **2-4:** two-sided FFT, `DeltaF=1/(N*Ts)`, `freq=-Fs/2:DeltaF:Fs/2-DeltaF`, `fftshift(fft(x))/N`. Lines at ±100/±300/±600 Hz, amps **0.5 / 1 / 1.5** (half of A via Euler).
- **2-5:** `filter(B2,A2,x)`, FFT again. After: 100 Hz→0.5, 300 Hz→0.981, 600 Hz→0.044 ⇒ atten @600 = 20log10(0.044/1.5) ≈ **−30.6 dB**, matches 2-1.

---

## P3 — FIR highpass via windowing (skeleton verified correct)

Spec: HP, Fourier/window method, Fpass=1750, Fstop=1250, As=20 dB, Fs=5000.

- **3-1:** `Fc=(Fpass+Fstop)/2=1500 Hz`; `ωc=2πFc/Fs=1.885`; `ΔFsharp=|Fstop−Fpass|/Fs=0.1`. **Rectangular** window (≈21 dB ≥ 20) → `N=0.9/ΔFsharp=9`.
- **3-2:** `M=N−1=8`, `K=M/2=4`. Ideal HP: `hHP=-ωc/π*sinc(ωc*n/π)` for `n=-K:K`, then `hHP(K+1)=(π−ωc)/π`. (Rect window → just truncate+shift, no window multiply.)
- **3-3:** `tf(hHP,1,1/Fs,'variable','z^-1')`, `freqz(hHP,1)`, plot dB vs Hz, mark Fc/Fpass/Fstop/As. Meets spec.
- **3-4:** phase linear in passband — because impulse response is **symmetric** (linear-phase FIR).
- **3-5:** As=40 dB → **Hann** window (≈44 dB) → `N=3.1/ΔFsharp=31`. `M2=30, K2=15`, Hann `wham=0.5-0.5*cos(2π*(0:M2)/M2)`, `hwindow=hHP2.*wham`.
- **3-6:** `freqz(hwindow,1)` dB plot. Meets new spec, but note: attenuation at 1250 Hz is only ≈ **−39.07 dB** (just shy of 40; first sidelobe is −44).

> Window appendix table (rect ≈21 dB/C=0.9, Hann ≈44/C=3.1, Hamming ≈53/C=3.3,
> Blackman ≈74/C=5.5) is in `E25_new.m`. `N ≈ C/ΔFsharp = C·Fs/ΔF`, make odd for Type-I.

---

## P1 — Z-domain math (40%, deferred, answers from official PDF)

zeros −2,(1±i)/2; poles 0,⅓,⅔; H(1)=1.
- **1-2:** `G=4/27`; `H(z)=(4/27)·(1+2z⁻¹)(1−½(1+i)z⁻¹)(1−½(1−i)z⁻¹)/[(1−⅓z⁻¹)(1−⅔z⁻¹)]`; **ROC |z|>2/3** (causal).
- **1-3:** stable (unit circle ⊂ ROC).
- **1-4:** `X₁(z)=½z⁻¹/(1−z⁻¹+½z⁻²)`, |z|>√2/2.
- **1-5:** `Y₁(z)=(2/27)·z⁻¹(1+2z⁻¹)/[(1−⅓z⁻¹)(1−⅔z⁻¹)]` (the conj-pair factor cancels X₁'s denominator).
- **1-6:** `y₁[n] = (2/27)(−7(⅓)ⁿ⁻¹ + 8(⅔)ⁿ⁻¹)·u[n−1]`.
- **1-7:** `H=Hmp·Hap`; `Hap(z)=(z⁻¹+½)/(1+½z⁻¹)` (moves the zero at −2 outside the circle); `|Hap|=1` (0 dB) for all ω.

---

## Conventions reminder (from CLAUDE.md)
- Hints-first; user attempts, then asks for a check.
- Truth source = the official solution PDF (absolute). It supersedes
  notebooklm for E25.
- MATLAB comments in Danish with real øæå.
- After completing a sub-question, log result here, then continue.

# Exam-day takeaways for E25

> P2 ✅ complete, P3 ✅ to 3-3. Filled as sub-questions are completed.

- **Patterns used:**
  - DF-II read-off + sign-flip → `freqz` dB / phase / `datatip` value read-off.
  - Two-sided FFT spectrum (`fftshift(fft(x)/N)`), amplitude = A/2 per ±line; filter the signal, re-FFT, attenuation = `20log10(A_out/A_in)`.
  - FIR window method: `Fc=(Fpass+Fstop)/2`, `wc=2π Fc/Fs`, `ΔF=|Fstop−Fpass|/Fs`, window from As table, `N`, `M=N−1`, `K=M/2`, `FIR_fourier("HP",-K:K,wc)`, causal shift by K.
- **What tripped me up (besides the P2 DF-II trap) — helper/MATLAB gotchas:**
  - `MK_values(9)` crashes (`sym/double … maplemex … unevaluated name 'M'`) on this PC's symbolic backend → **use closed form** `M=N−1; K=M/2`.
  - `0.9/0.1 = 8.999…` not 9 → `n_taps = ceil(0.9/ΔF)` before use.
  - `FIR_fourier(HP,…)` errors — type arg must be the **quoted string** `"HP"`.
  - `tf(b,a,Fs,…)` wrong — 3rd arg is **Ts = 1/Fs**; add `'Variable','z^-1'`.
  - Reusing `h` for both impulse response *and* `freqz` output overwrites it; and `datatip` needs a **plot line handle** (`hLine=plot(...)`), not the response vector.
  - All of these are now in [[DSP MATLAB helpers cheat sheet]].
- **Quick reference if this comes up again:** see the cheat-sheet sections "Mark specific values on a plot", "Impulse response over any n-range", and the `MK_values` danger callout.
