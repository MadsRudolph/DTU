---
course: "62743"
course-name: "Digital Signal Processing (Reexam)"
type: home
tags: [DSP, reexam, home]
aliases:
  - DSP Reexam
---
# 62743 DSP Re-exam — Hub

> [!info] Exam
> **Date:** Wednesday 20 May 2026 — code **E2-B**
> **Format:** 4 hours, written, all aids allowed, no internet
> **Room/time:** `eksamensplan.dtu.dk` publishes ~1 week before

> [!todo]+ ▶️ EXAM-DAY CHECKLIST — do this the moment you open the computer (~5 min)
> 1. **`git pull`** in `C:\Users\Mads2\DTU` — pulls this hub, the cookbook, F26.m, every walkthrough.
> 2. **Open the exam skeleton:** `3.semester\DSP\EXAMS\F26.m` — it has the same checklist at the top + 3-question scaffold ready to fill.
> 3. **Open all previous solutions in the MATLAB editor** (as reference tabs), from `3.semester\DSP\EXAMS\`:
>    `E25_new.m` (the closest to F26 — full P1+P2+P3, facit-grade) · `F24.m` · `F25_new.m` · `F23.m` · `F20.m` · `E19.m` · `E20.m` · `E22.m` · `F21.m`
> 4. **Toolbox test** — paste into MATLAB, must not error:
>    `ver` (must list **Signal Processing Toolbox**) · `which residuez tf2zpk zplane impz freqz` · (Symbolic listed? → `syms`/`iztrans`/`ztrans` also usable)
> 5. **Read the exam.** For each problem, find its type in the **[chart below](#📊-problem--which-exam-set-has-a-worked-example)** → open the linked flow/cookbook + the named walkthrough.
> 6. **Order of attack:** Q3 (~60 min) → Q2 (~70 min) → Q1 (~80 min) → 30 min review + `pretty F26.m` → hand in **PDF + .m**.
> 7. **Q1 trap:** a sub-part saying *"uden brug af MATLAB/Maple"* → write the analytic setup by hand (table pair, PFD ansatz) even if unfinished; a residuez-only answer there scores **0**.

> [!important]+ 📄 PUBLISH FOR SUBMISSION — copy-paste in PowerShell
> Save `F26.m` first. Then from `(base) PS C:\Users\Mads2>` (any directory works — it auto-finds the file in `EXAMS\`):
> ```powershell
> & "C:\Users\Mads2\DTU\3.semester\DSP\pretty.bat" F26.m --open
> ```
> **Submit this file:** `C:\Users\Mads2\DTU\3.semester\DSP\EXAMS\html\F26_pretty.pdf` (+ the `.m`).
> Name/ID default to **Mads Rudolph / s246132** (baked in). `--open` opens the PDF to eyeball before handing in.
>
> Faster re-render after a tiny styling tweak (skips MATLAB):
> ```powershell
> & "C:\Users\Mads2\DTU\3.semester\DSP\pretty.bat" F26.m --no-matlab --open
> ```
> If the PDF is locked (left open in a viewer) it auto-saves a **timestamped** copy instead of failing — grab the newest.
>
> ⚠️ **Test this tonight** so the toolchain is proven before exam pressure:
> ```powershell
> & "C:\Users\Mads2\DTU\3.semester\DSP\pretty.bat" E25_new.m --open
> ```
> Clean `E25_new_pretty.pdf` ⇒ you're good for tomorrow.

> [!important] Expected structure — **3 questions** (re-exam of the E25 sitting)
> The Dec-2025 (**E25**) exam dropped from 4 questions to **3**, weighted **40 / 30 / 30**. The May-2026 re-exam re-examines that sitting, so plan for **3 questions**:
>
> | # | Weight | Topic | Your level |
> |---|---|---|---|
> | **Q1** | **~40 %** | LTI / Z-transform: poles-zeros, H(z), ROC, stability, inverse-Z, **min-phase/all-pass** | ⚠️ weak — but biggest |
> | **Q2** | ~30 % | Filter realisation (block diagram → H(z)) + sampling + **FFT** + filtering | ✅ strong |
> | **Q3** | ~30 % | **FIR design** (Fourier + window method) | ✅ strong |
>
> *(Content didn't shrink — E25 merged the old sampling/FFT/filter-realisation questions into one big Q2 and grew Q1 to 40 %. Treat 3-question as the plan; if it's 4, the archetypes below still cover every part.)*

---

## 📊 Re-exam (F) vs ordinary (E) — the pattern

**The re-exam is a parallel form of the ordinary exam it follows** — same archetypes, same difficulty, different numbers. Evidence from 6 sittings:

| Sitting           | Type        | #Q               | Weights       | Q1                | Q2                 | Q3                 | Q4                 |
| ----------------- | ----------- | ---------------- | ------------- | ----------------- | ------------------ | ------------------ | ------------------ |
| E23 (Dec '23)     | ordinary    | 4                | 25·25·25·25   | LTI table         | IIR BLT (Cheby)    | sampling/ROC       | FIR window         |
| **F24 (May '24)** | **re-exam** | 4                | 25·25·25·25   | LTI table         | sampling+AA filt   | spectrum+min-phase | IIR BLT            |
| E24 (Dec '24)     | ordinary    | 4                | 25·30·20·25   | LTI table         | 3 given H(z)       | sampling+min-phase | FIR window         |
| **F25 (May '25)** | **re-exam** | 4                | 25·25·25·25   | LTI table         | IIR BLT            | sampling+ROC       | filter realisation |
| **E25 (Dec '25)** | ordinary    | **3**            | **40·30·30**  | LTI+min-phase     | filt-real+samp+FFT | FIR window         | —                  |
| **F26 (May '26)** | **re-exam** | **3 ⟵ expected** | **~40·30·30** | *(this is yours)* |                    |                    |                    |

**Findings:**
1. **Same 6-archetype pool, recycled every time:** (A) LTI/Z-transform by hand — *always Q1, every exam*; (B) IIR design via BLT; (C) sampling/aliasing/spectrum; (D) FIR Fourier+window; (E) filter realisation from block diagram; (F) min-phase/all-pass (rides on A or C).
2. **The re-exam tracks its paired ordinary in count & structure.** E23→F24 and E24→F25 are both 4-question parallel forms with the same topic set, only renumbered/reweighted.
3. **The only real change is packaging.** Through F25: 4 questions. **E25 consolidated to 3 (40/30/30)** — no content cut, just merged C+E+FFT into Q2 and inflated archetype A to 40 %.
4. **Difficulty is constant** — re-exam is *not* harder; it's a re-shuffle of the same templates.
5. **Conclusion:** since the re-exam mirrors its paired ordinary, and E25 (the sitting F26 re-examines) was **3 × 40/30/30**, plan firmly for **3 questions, Q1 ≈ 40 %**. Practising E25 ≈ practising F26.

---

## ▶️ IN-EXAM TRIAGE — "what kind of problem is this?"

Read the question, match the cue, click the flow. Each flow is a top-to-bottom recipe with MATLAB + the traps.

### 🟧 Looks like Q1 — LTI / Z-transform  *(by-hand, ~40 %)*

**Cue:** a difference equation **or** "poler/nulpunkter er…" + `H(1)=1`; asks H(z), ROC, stable?, h[n], y[n], or "minimum fase / all-pass".

→ **[[LTI z-transform flow]]** — diff eq → H(z) → poles/zeros/stability → h[n] → y[n] → energy
→ **[[Partial fraction practice]]** — the inverse-Z step (your documented weak spot)
→ 🆘 **[[Q1 via MATLAB cookbook]]** — **can't do the math by hand? every Q1 sub-type → exact MATLAB commands + Danish `Svar`, with a panic protocol. Go here if stuck.**

> [!warning] E25 added two Q1 twists not yet in the flow note — know these cold:
> **(a) Poles/zeros given, reconstruct H(z):** build $H(z)=G\dfrac{\prod(1-z_k z^{-1})}{\prod(1-p_k z^{-1})}$, then fix the gain `G` from the stated `H(1)=1` (plug z=1, solve for G).
> **(b) Min-phase / all-pass split** $H(z)=H_{mp}(z)\,H_{ap}(z)$ — course procedure for a **zero outside** the unit circle at $z_0$ ($|z_0|>1$):
> 1. In $H_{mp}$: **replace** the bad factor $(1-z_0 z^{-1})$ with its reflection $(1-\tfrac{1}{z_0^{*}}z^{-1})$ (zero moved *inside*). Poles unchanged.
> 2. Build the all-pass section $H_{ap}(z)=G\,\dfrac{1-z_0 z^{-1}}{1-\tfrac{1}{z_0^{*}}z^{-1}}$ (standard 1st-order all-pass form $\tfrac{z^{-1}-a^{*}}{1-a z^{-1}}$).
> 3. Fix gain `G` from $H_{ap}(1)=1$ → then $H_{mp}$ carries the matching $1/G$, so $H_{mp}H_{ap}=H$ exactly.
> 4. Check: `freqz(Hap)` → **flat magnitude** (only phase varies). That's the plot the exam asks for.
>
> Appears in **E24 Q3 and E25 Q1** — recurring, drill it.

### 🟦 Looks like Q2 — filter analysis + sampling + FFT  *(MATLAB, ~30 %)*

**Cue:** a **block diagram** (Direct Form I/II, gains on z⁻¹ taps) or given H(z); then "samples med Fs…", "frekvensspektrum (FFT)", "filtrer signalet med `filter`".

→ **[[Filter analysis and FFT flow]]** — block diagram → b,a → freqz/zplane → sampling → **FFT scaling** → filter & read dB

### 🟩 Looks like Q3 — FIR design  *(MATLAB, ~30 %)*

**Cue:** "Filter design metode: **Fourier transform**", gives Fpass/Fstop/As/Fs, asks Fc, ωc, window, Ntaps, truncated causal h[n].

→ **[[FIR window design flow]]** — Fc → ωc → window-from-As table → Ntaps → truncated h[n] → freqz → phase

### Other patterns (could appear as a sub-part)

- **IIR design via BLT** (butterworth, `lp2hp`/`bilinear`): see [[F25 exam walkthrough]] Q2, [[F24 exam walkthrough]] Q4 — prewarp → prototype (appendix) → `lp2xx` → `bilinear` → `freqz`.
- **Sampling spectrum sketch / aliasing only:** see [[Filter analysis and FFT flow]] §5 and [[F25 exam walkthrough]] Q3.
- **Multirate / under-sampling:** [[Multirate Digital Signal Processing]].

---

## 📊 Problem → which exam set has a worked example

Match what's in front of you to a row → open that **walkthrough** for a fully solved twin, and the **flow/cookbook** for the recipe.

| If the problem is… | Worked example (open this) | Recipe |
|---|---|---|
| **Q1** diff eq → H(z), poles/zeros, h[n], y[n] | [[F20 exam walkthrough]] P1 · [[F23 exam walkthrough]] P1 | [[LTI z-transform flow]] · [[Q1 via MATLAB cookbook]] §1 |
| **Q1** poles/zeros given **+ H(1)=1** → H(z), ROC | [[E25 exam walkthrough]] §P1 (1-1…1-3) | [[Q1 via MATLAB cookbook]] §2 |
| **Q1** two input/output pairs → h[n] (linearity) | [[F24 exam walkthrough]] P1 | [[Q1 via MATLAB cookbook]] §1B |
| **Q1** given H(z) factored → ROC/h[n]/y[n]/realisation | [[F20 exam walkthrough]] P3 | [[Q1 via MATLAB cookbook]] §6/§10 |
| **Q1** Z-transform of a signal (formula given) | [[E25 exam walkthrough]] 1-4 | [[Q1 via MATLAB cookbook]] §5 |
| **Q1** inverse-Z / partial fractions → h[n], y[n] | [[F20 exam walkthrough]] P1-3/P1-4 | [[Q1 via MATLAB cookbook]] §6 · [[Partial fraction practice]] |
| **Q1** min-phase / all-pass decomposition ⭐ | [[F24 exam walkthrough]] P3-4 · [[E25 exam walkthrough]] 1-7 | [[Q1 via MATLAB cookbook]] §8 |
| **Q1** cascade / parallel realisation | [[F20 exam walkthrough]] P3-5 | [[Q1 via MATLAB cookbook]] §10 |
| **Q2** filter from block diagram (DF-I/II) → H(z) | [[E25 exam walkthrough]] §P2 · [[F25 exam walkthrough]] Q4 | [[Filter analysis and FFT flow]] |
| **Q2** sampling + aliasing + **FFT spectrum** scaling | [[F20 exam walkthrough]] P2 · [[E25 exam walkthrough]] 2-3/2-4 | [[Filter analysis and FFT flow]] §5 |
| **Q2** product/AM signal — hidden sum/diff frequency | [[F20 exam walkthrough]] P2-3 | [[Filter analysis and FFT flow]] |
| **Q2** filter a signal, read dB before/after | [[E25 exam walkthrough]] 2-5 · [[F25 exam walkthrough]] Q4 | [[Filter analysis and FFT flow]] |
| **Q3** FIR window design (Fourier method) | [[E25 exam walkthrough]] §P3 · [[F23 exam walkthrough]] Q4 | [[FIR window design flow]] |
| sub-part: **IIR via BLT** (Butterworth, lp2xx+bilinear) | [[F24 exam walkthrough]] Q4 · [[F25 exam walkthrough]] Q2 | [[F24 exam walkthrough]] §IIR-BLT playbook |
| sub-part: analog AA filter (`lp2lp`+`freqs`) | [[F24 exam walkthrough]] Q2 | same playbook |
| sub-part: sampling theorem in Ω (angular) | [[F24 exam walkthrough]] P3-1/P3-2 | [[Filter analysis and FFT flow]] §5 |

> [!tip] No exact twin? Q1 is **always** the LTI/Z-transform archetype, just a different entry point — go straight to [[Q1 via MATLAB cookbook]] (it has a 🟥 panic protocol that banks partial credit for *any* Q1).

---

## ⏱️ Strategy for the 3-question format

> [!important] "Filter-first" still holds — but Q1 is 40 %, so it's no longer optional.
> Q2+Q3 (~60 %) are your strong MATLAB areas. Q1 (~40 %) is the weak by-hand area **and the single biggest block**.

**Order of attack:**
1. **Q3 first** (~30 %, strong, most formulaic) — bank it cleanly with [[FIR window design flow]].
2. **Q2** (~30 %, strong) — [[Filter analysis and FFT flow]]; the only risk is FFT scaling, which the flow nails.
3. **Q1** (~40 %, weak) — even if the deep partial-fraction / min-phase parts are hard, the **early sub-parts are free MATLAB points**: pole-zero plot (`zplane`), write H(z), ROC, stability. *Never* leave those blank — they're ~half of Q1's marks and pure recipe.

Rough time budget (4 h): Q3 ≈ 60 min · Q2 ≈ 70 min · Q1 ≈ 80 min · 30 min review/publish.

---

## 🖨️ Publishing your answer (the new way)

The submission must be **kommenteret kode** and the examiners run your `.m`. Use the converter for a clean PDF — but the *style of the code itself* is what scores.

**Result-presentation convention** (already applied to `F25_new.m`; use it for every exam):

| Content | How |
|---|---|
| Conclusions / "FIR vs IIR fordi…" / "opfylder kravene" | a **bare `%%`** then `% *Svar X-Y:* …` → renders as prose **outside** the code box, no TOC clutter, works in raw MATLAB too |
| A computed value that *is* the answer | **no semicolon** (`poler = roots(a)`) or a value-bearing `fprintf('%.2f dB', dB)` |
| A static sentence in `fprintf('...')` | ❌ never — duplicates code line + echoed output |

**Make the PDF** — from `C:\Users\Mads2\DTU\3.semester\DSP\` :

```
pretty F25_new.m                ← MATLAB publish + styled PDF (one command)
pretty F25_new.m --open         ← also open it when done
pretty F25_new.m --no-matlab    ← just re-style (skip the ~30 s MATLAB run)
```

Output → `EXAMS\html\F25_new_pretty.pdf`. It forces white figures, real syntax highlighting, collapses RCOND warning spam, strips internal scaffolding, and renders each `Svar` block as a green ✓ callout. Defaults to *Mads Rudolph / s246132* (`--name/--studentid` to change). If you have the PDF open in a viewer it auto-writes a timestamped copy instead of failing.

> [!tip] During the exam: write answers as `%%` `Svar` blocks **as you go**, then run `pretty <exam>.m` once at the end. No rework.

---

## 📚 Reference shelf (pull up mid-exam to fill a gap)

**Master refs:** [[EXAM PREP]] · [[DSP-Bible]]
**Cheat sheets:** [[Exam_Cheat_Sheet_OPTIMIZED]] · [[Exam_Quick_Reference_OPTIMIZED]] · [[DSP MATLAB helpers cheat sheet]]
**Formula sheets:** [[Week 1-4]] (DT/LTI/DTFT/z) · [[Week 5-7]] (DFT/sampling) · [[Week 8-11]] (filter structures, IIR+FIR) · [[Week 12-13]] (multirate)
**Topic depth:** [[FIR_Windowing_Complete_Guide]] · [[Multirate Digital Signal Processing]]
**Worked exams:** [[F20 exam walkthrough]] · [[F23 exam walkthrough]] · [[F24 exam walkthrough]] · [[F25 exam walkthrough]]

Exam + solution PDFs: `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/` (E25 set: `Archive/3rd Semester/DSP/62743 E25 Exam v3.pdf`).

---

## 🎯 Known weak spots (from failed E25)

Flags so I explain these harder when they show up — all live in **Q1**:
1. Partial fractions under time pressure → [[Partial fraction practice]]
2. Fast DTFT via properties (not from definition)
3. ROC classification (causal ⇒ outside outermost pole)
4. Min-phase / all-pass decomposition  *(E24 Q3, E25 Q1 — drill this)*
5. FIR linear-phase indexing (K = M/2)
6. Time management

Self-assessed: **filter design (Q2/Q3) OK, Z-transform/DTFT (Q1) weak.**

---

## Pre-exam practice schedule

Older/simpler first; golden annotated ones last. Tick and move on; fill `Exam Evals/_template.md → Exam Evals/<exam>.md` after each.

- [ ] F20 · [ ] F21 · [ ] F23 · [ ] E19 · [ ] E20 · [ ] E22
- [ ] E23 (golden, `EXAMS\E23.mlx`, [[E23 Exam]]) · [ ] F24 (golden, `EXAMS\F24.m`, [[F24 Exam]])
- [ ] E24 (`EXAMS\E24.mlx`) · [ ] F25 (golden, `EXAMS\F25.mlx`, [[F25 Exam]])
- [ ] **E25** — the one you failed, final attempt (`EXAMS\E25.mlx`, [[E25 Exam]]) — **this is the format the re-exam mirrors; do it last and full-speed**

---

## MATLAB setup
- R2025a + Signal Processing Toolbox confirmed
- Helpers on path: `C:\Users\Mads2\DTU\3.semester\DSP\Helpers\`
- Publisher: `C:\Users\Mads2\DTU\3.semester\DSP\pretty.bat`
