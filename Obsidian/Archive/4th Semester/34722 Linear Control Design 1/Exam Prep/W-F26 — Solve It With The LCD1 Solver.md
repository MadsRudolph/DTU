---
tags: [34722, lcd, exam, tool, how-to]
course: 34722 Linear Control Design 1
pattern: W-F26-tool
purpose: Exact click-by-click recipe for solving every F26 MCQ in the LCD1 Solver app
exam: F26 multiple-choice
---
# W-F26 — Solve It With The LCD1 Solver

> [!info] Quick Links
> - Worked maths: [[W-F26 — Worked Exam (MCQ)]] · Hub: [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - The app: `lcd1-exam-suite` — launch with **`Double-Click-To-Run.bat`** (Windows) / `Launch-Mac.command` (mac).

Every numeric F26 question is reproduced by the app's engine — verified in
`spike/test/exam-f26.test.js` (`npm test`, 21/21). This note is the **operator's
manual**: which box, what to type, what you should see.

---
## The four regions of LCD1 Solver mode

1. **System box** — type or paste one `G(s)` (numeric or symbolic). It immediately shows poles, DC gain, margins, ζ/ωₙ, step values…
2. **Smart Paste** — paste a *whole* exam question; it repairs the text, drops `G(s)` into the System box, lists the answer options, and hints at the question type.
3. **answer options box** — paste the multiple-choice options, one per line. Every tool then **flags the option that matches** its result (dB matched in dB; a result close to nothing stays unflagged rather than guessing).
4. The tools, in two strips:
   - **Design · pick a goal, reuse the G above** — everything that needs the loop `G`: margins, stable-K, P-for-PM, **Controller K_P**, **Lead from magnitude**, close the loop…
   - **Calculators (not based on one G)** — 2nd-order specs, ess, value theorems, nested-ess, **Disturbance |D|**, Bode read-off…

> [!tip] General loop
> Smart-Paste the question → paste the options → pick the matching tool below →
> fill any read-offs → read the **flagged** option. Always set **degrees / dB**
> consistently, and remember design `K_P` answers are *approximate* (±a few %).

---
## Question-by-question recipe

> Tool names below are the form titles in the app. ✅ = an answer the engine flags directly · ◑ = engine gives the number, you pick the option · ★ = conceptual, tool only checks the supporting fact.

### Q1 — DC-motor block reduction ✅
**Block Diagram** mode → draw K, the motor `Km/(s+0.01)`, the `1/s` integrator and the two feedback paths (`Kb` inner, unity outer) → **Use in LCD1 Solver →**. The reduced `Y/U` lands in the System box: `KKm/(s²+(0.01+KmKb)s+KKm)`.
*Shortcut:* in LCD1 mode, use **Close the loop · T = L/(1+L)** on the forward path to collapse each loop.

### Q2 — ODE → damping nature ◑
**P1 — ODE → TF**: `y coeffs = 1,2,1` (from `ÿ+2ẏ+y`), `u coeffs = 4`. Then read the System box / **Characterize TF**: `ζ = 1` ⇒ *critically damped*, `ω_d = 0`.

### Q3 — ω_c range for a target PM ◑
System box `G = 1/(s*(s+15))` → **P6 — P for PM**, target `γ_M = 45`. Result `ω_c ≈ 15` → lies in **10–20 rad/s**.

### Q4 — ω_d from overshoot + ω_n ✅
**P4 — 2nd-order specs**: `Mp = 0.10`, `ω_n = 5` → `ω_d ≈ 4.03`.

### Q5 — steady-state error ◑
**P5 — ess table**: System/`G = (0.5*s+0.3)/(s+10)` (that's `C·G` at DC; the delay = 1 at DC). Read `ess_step = 1/(1+K_pos)`; multiply by the input size 30 → `29.1 → 29`.

### Q6 — four-block reduction ✅
**Block Diagram** mode → draw `A` in series, then `B` with the **summed** `C+D` parallel feedback → reduce. Get `AB/(1+B(C+D))`. (Not `AB/(1+BCD)`.)

### Q7 — is it stable? ✅
Put the reduced `H(s)` (or just its char. poly plant) in the System box → **Closed-loop stability** (or read the poles): a pole at `+6.47` ⇒ **not stable**.

### Q8 — poles/zeros from a Bode plot ★
Identify by eye: phase → −90° at low ω **and** a low gain-crossover ⇒ a pole at the origin → *three real poles, one at origin*. **Verify**: System box `G = 9.97/(s*(s+5)*(s+6))` → **P3 — Margins** reproduces `Gm≈31.8 dB @ 5.48`, `PM≈82° @ 0.331` — matching the figure.

### Q9 — ζ, ω_n from overshoot + settling ✅
**P4 — 2nd-order specs**: `Mp = 0.0123`, `t_s_2pct = 1` → `ζ ≈ 0.814`, `ω_n ≈ 4.916`.

### Q10 — initial/final value ✅
Reduce to `H = 5/(s+5)` (parallel `G1+G2G3` then positive feedback — use **Close the loop**). Then **Initial / final value** with `F = 5/((s+5)*(s+2))` (i.e. `H·U`, `U=1/(s+2)`): `y(0⁺)=0`, `y(∞)=0`.

### Q11 — P-gain for a PM (Bode read-off) ✅
**P6 — Controller K_P**: leave `G(s)` blank, fill the read-off `ω_c = 1.39`, `|G| = -16.4` dB, `γ_M = 75`, no lead/lag → `K_P = 6.6`.

### Q12 — which statement is true? ★
Answer: *"relative degree ≥3 ⇒ large K_P destabilises."* Check it in the tool: System box `G = 1/(s*(s+1)*(s+2))` → **Closed-loop stability** with `K = 1` (stable) vs `K = 50` (unstable).

### Q13 — which statement is true? ★
Answer: *"0 dB at low frequency ⇒ zero steady-state error."* (Lower bandwidth = *slower*, not faster.) Sanity-check with **P5 — ess table** on any type-1 `G = 1/s`: `ess_step = 0`.

### Q14 — which |D(s)| plot? ✅
**P5 — Disturbance |D| from sensitivities**: `|G_ed| = -22.11` dB, `|G_er| = -34.15` dB, `K_P = 5`. Result `|D| = +12 dB` (and implied `G(0)=10`) → pick the plot **flat at ≈+12 dB** at low ω.

### Q15 — stable K from a Nyquist crossing ◑
**GM from a Nyquist crossing**: `|crossing| = 0.6356` → critical gain `1/d = 1.573`. The plant has one RHP pole, so stable for **K_P > 1.573** ⇒ pick **2.5** (1.57 is the marginal value, *not* stable).

### Q16 — Lead part from its magnitude ✅
**P6 — Lead part from its magnitude**: `ω_c = 45`, `mag = 20` dB → `α = 0.01`, `(0.22s+1)/(0.0022s+1)`. (The zero time-constant is on top — a lead. The reciprocal is the lag trap.)

### Q17 — P-Lead-Lag K_P (read-off) ✅
**P6 — Controller K_P** (read-off): `ω_c = 25.49`, `|G| = -40.96` dB, `∠G = -167.41`°, `γ_M = 70`, `α = 0.02`, `N_i = 3`, `β = 10` → `K_P = 15`.

### Q18 — P-Lead K_P (plant given) ✅
**P6 — Controller K_P**: `G = 3.652/(s*(s+1)*(s+5))`, `γ_M = 45`, `α = 0.01`, leave `N_i`/`β` blank → `ω_c ≈ 5`, `K_P ≈ 4.9` (the option is **5** — design answers are approximate).

### Q19 — pick the control law ★
Answer: *`u = K_P·e + F(0)r + F_d(0)d`* — static feed-forward both, because the **RHP zero at +7.5** makes dynamic inversion `1/G` unstable. Check: System box `G = (s-7.5)/(s²+6s+5)` → the zero shows at `+7.5` (RHP).

### Q20 — number of stages N from ess ✅
**P7 — Nested ess**, architecture `kp_g0_lag_chain`: `K_P = 105`, `G_k(0)=0.5`, `G_0(0)=0.5`, `ess target = 0.25` → `N = 5`.

---
> [!warning] Tool gotchas (same traps, mechanised)
> - **Blank vs filled** in *Controller K_P*: leave `G(s)` blank to use a Bode read-off; fill it to let the tool find `ω_c`. Leave `α`/`N_i`/`β` blank to drop the lead/PI/lag.
> - **dB fields are dB** — the tool converts; don't pre-convert `|G|` or the lead magnitude.
> - **Design K_P is approximate** — the flagged option may read "closest, 2% off". `4.9 → 5`, `0.5073 → 0.5`. Trust the nearest sensible option.
> - **Conceptual Q12/Q13/Q19** have no single button — use the listed check to confirm the reasoning, then pick the statement.
> - **Block diagrams (Q1/Q6)** are fastest in **Block Diagram** mode, then *Use in LCD1 Solver →*.
