---
type: walkthrough
tags: [DSP, reexam, exam, F23, walkthrough]
aliases:
  - F23 walkthrough
  - F23 exam log
---
# F23 exam -- MATLAB walkthrough

> [!info] What this note is
> Step-by-step log of how I'm solving the **F23 exam** in [[62743 F23 Exam.pdf]].
> **Filter-first**: Q2 (spectrum + given filter) and Q4 (FIR HP via Fourier + Blackman) are the priority. Q1 and Q3 are deferred math.
> Weighting: Q1 30% | Q2 20% | Q3 20% | Q4 30%.

**Exam PDF:** [[62743 F23 Exam.pdf]]
**Solution PDF:** [[62743 F23 Exam student solutions.pdf]]
**Working script:** `3.semester/DSP/EXAMS/F23.m` (outside vault)

---

# Problem 1 -- LTI: H(z) / ROC / stability / h[n]  [DEFERRED - math]

Difference eq $y[n]-\tfrac12 y[n-1]=x[n]-b\,x[n-2]$, $b>0$. Z-transform/ROC/FIR-condition/output math. Deferred per filter-first strategy.

---

# Problem 2 -- Spectrum + given digital filter  [FILTER -- priority]

**Topic:** T5/T6 (DFT spectrum), T7 (filter characterization). Signal $x_a(t)=A_1\cos(2\pi F_1 t)\,[1+A_2\cos(2\pi F_2 t)]$ — note the **product** form (AM-like). $F_1=70$, $F_2=100$ Hz, $A_1=4$, $A_2=2$.

## P2-1 -- spectrum via FFT (Fs=5000, N=1e7)

<!-- fill in -->

## P2-2 -- analytic rewrite (product-to-sum) + amplitude comparison

<!-- fill in -->

## P2-3 -- characterize given H(z) (magnitude plot, linear; what type)

<!-- fill in -->

## P2-4 -- attenuation at the spectral lines from 2-1

<!-- fill in -->

---

# Problem 3 -- Impulse-train sampling, S(Ω), sampling theorem  [DEFERRED - hand-drawn]

Draw $S(\Omega)$ and FT of $y(t)=x(t)s(t)$ for $T_s=\pi/3$ and $2\pi/3$; conclude via sampling theorem. Hand-drawn, no MATLAB. Deferred.

---

# Problem 4 -- FIR highpass via Fourier design + Blackman window  [FILTER -- priority]

**Topic:** T8 (FIR design — windowing). FIR highpass, Fourier-transform design, $f_C = 200/F_s$, $F_s = 2000$ Hz. Uses helpers `FIR_fourier`, `FIR_window`, `MK_values`.

## P4-1 -- ideal HP filter (ωC, h_ideel[n] for n=-20..20, read values)

<!-- fill in -->

## P4-2 -- truncated causal FIR (K, M, delay, Ntaps=23, dB plot, attenuations)

<!-- fill in -->

## P4-3 -- Blackman window (h_W[n], dB plot, attenuations at 100/200/300 Hz)

<!-- fill in -->

---

# Exam-day takeaways for F23

> Filled in after we finish the filter problems.

- **Patterns used:**
- **What tripped me up:**
- **Quick reference if this comes up again:**
