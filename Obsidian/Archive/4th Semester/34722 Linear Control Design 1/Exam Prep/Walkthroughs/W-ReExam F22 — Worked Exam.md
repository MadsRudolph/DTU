---
tags: [34722, lcd, exam, worked, ReExam-F22]
course: 34722 Linear Control Design 1
exam_set: RE-exam F22 (17 August 2022)
questions: 10
purpose: Full worked walkthrough of the RE-exam F22 — per question the approach, the MATLAB line that nails it, the embedded graph, the facit answer, and the planted trap
---
# W-ReExam F22 — Worked Exam

> [!info] Exam Resources
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Paper:** [[LCD1 ReExam F22 - Questions with answers.pdf]] (Past Exams folder)
> - **Solve script:** `EXAM/Scripts/solved/solve_ReExam_F22.m` · **Practice yourself:** `EXAM/Scripts/practice/practice_ReExam_F22.m`
> - Run headless: `matlab -batch "solve_ReExam_F22"`

**Facit overview:** Q1:1 Q2:3 Q3:4 Q4:2 Q5:3 Q6:1 Q7:4 Q8:3 Q9:1 Q10:1

---

## Q1 — Linearization, error at a nearby point

> [!success] Facit: answer 1

> [!example]- Approach
> Linearize `z = y² + 5xy − 3x²` about `(x̄=3, ȳ=11)`, then ask: what's the % error of the linear model at `(4,12)`? Partials at the operating point, build the affine model, compare to the true value.

$$\frac{\partial z}{\partial x}=5y-6x=37,\qquad \frac{\partial z}{\partial y}=2y+5x=37$$

```matlab
zb = 11^2 + 5*3*11 - 3*3^2;           % 259  (operating point)
z_lin  = zb + 37*(4-3) + 37*(12-11);  % 333
z_true = 12^2 + 5*4*12 - 3*4^2;       % 336
e1 = abs(z_true - z_lin)/z_true*100;  % 0.89 %  -> e < 1 %
```

> [!warning] Trap
> The error is *relative to the true value* (`|true−lin|/true`), and it asks which **band** the error falls in — 0.89 % → "< 1 %", answer 1. Don't forget the constant term `zb` in the linear model.

---

## Q2 — Closed loop, 17 % overshoot → damped frequency `ωd`

> [!success] Facit: answer 3

> [!example]- Approach
> overshoot fixes ζ; the `2ζωn = 2` coefficient fixes ωn; then `ωd = ωn√(1−ζ²)`.
> $Y/R = K/(s²+2s+K) = ωn²/(s²+2ζωn s+ωn²)$. Given 17 % overshoot.

$$M_p=17\% \Rightarrow \zeta\approx0.5,\quad 2\zeta\omega_n=2\Rightarrow\omega_n=2,\quad \omega_d=\omega_n\sqrt{1-\zeta^2}=1.73$$

```matlab
zeta = 0.5;  wn = 1/zeta;             % =2  (from 2*zeta*wn=2)
wd = wn*sqrt(1-zeta^2);               % 1.732 rad/s
```

![[Q2_step_overshoot.png]]

> [!warning] Trap
> Memorise the `Mp→ζ` pegs: **ζ=0.5 → ~16 %, ζ=0.7 → ~5 %**. 17 % is the ζ=0.5 peg. The matching `K = ωn² = 4`.

---

## Q3 — Block interconnection, symbolic `H(s)`

> [!success] Facit: answer 4

> [!example]- Approach
> `G3,G4` in parallel; that sum in a feedback loop around `G2`; `G1` in series in front.

$$H=\frac{G_1G_2}{1-G_2(G_3+G_4)}$$

> [!warning] Trap
> The feedback sign. The loop here is **positive** feedback of `G2·(G3+G4)`, so the denominator is `1 − G2(G3+G4)`, not `1 +`. Reduce parallel (`+`) before the loop.

---

## Q4 — Same structure, plug in the `Gᵢ`, is it stable?

> [!success] Facit: answer 2 (unstable)

> [!example]- Approach
> `G1=1/(s−2), G2=(s−2)/(s−7), G3=2/(s+2), G4=−1/(s+2)`. Form `H`, then check the **characteristic polynomial** for RHP roots.

```matlab
den4 = [1 -6 -12];                    % s^2 - 6s - 12  (denominator of H)
p4   = sort(roots(den4),'descend');   % [7.58, -1.58]  -> one RHP pole
```

> [!warning] Trap
> `minreal()` on `G1*G2/(1-G2*(G3+G4))` numerically **cancels the wrong factor** and reports a spurious pole at −2. Build the char-poly by hand (`s²−6s−12`) and take `roots`. One pole at +7.58 → **RHP → unstable**.

---

## Q5 — Bode identification: flat phase that drops → poles/zeros + DC gain

> [!success] Facit: answer 3

> [!example]- Approach
> Phase flat then falling toward the magnitude break ⇒ a **double pole** plus **one zero**.
> $G(s)=\frac{s+2}{(s+4)^2}\quad(\text{zero }-2,\ \text{double pole }-4)$

```matlab
G5 = (s+2)/(s+4)^2;
dcdB = 20*log10(abs(dcgain(G5)));     % -18.06 dB
```

![[Q5_bode.png]]

> [!warning] Trap
> DC gain `= 2/16 = 0.125 → −18.1 dB`, a *negative* dB. Convert before matching to the options; don't read the gain as positive.

---

## Q6 — `G=1/(1+τs)`, input `r=1+6t`, is `e_ss` bigger for τ=5 or τ=4?

> [!success] Facit: answer 1

> [!example]- Approach
> Error TF $E(s)=R(s)[1−G]=R(s)\cdot\frac{\tau s}{1+\tau s}$, with $R(s)=1/s+6/s^2$. Apply Final-value theorem.

$$e_{ss}=\lim_{s\to0}sE=6\tau\quad(\text{ramp term dominates; the step term }\to0)$$

```matlab
ess_5 = 6*5;   ess_4 = 6*4;           % 30 vs 24  -> larger at tau=5
```

> [!warning] Trap
> The step part of the input contributes **zero** steady-state error (this is a type-1-like tracking of the constant), so only the ramp `6t` survives → `e_ss=6τ`. Bigger τ ⇒ bigger error.

---

## Q7 — Settling to 99 % → dominant (slowest) pole

> [!success] Facit: answer 4 (≈50 s)

> [!example]- Approach
> The slowest pole sets the time constant; 99 % settling ≈ `5τ`. $G=10(s+1)/((s+0.1)(s^2+20s+100))$. Poles $\{ -0.1, -10, -10 \}$.

```matlab
p7 = pole(10*(s+1)/((s+0.1)*(s^2+20*s+100)));  % -0.1, -10, -10
tau_dom = 1/0.1;                       % dominant pole -> tau = 10
ts99 = 5*tau_dom;                      % 50 s
```

![[Q7_settling.png]]

> [!warning] Trap
> 99 % uses `5τ` (not 98 %→`4τ`). The dominant pole is the one **closest to the imaginary axis** (−0.1), i.e. the *slowest*, not the biggest-magnitude one.

---

## Q8 — RLC series, V→I step response shape

> [!success] Facit: answer 3

> [!example]- Approach
> $R=1, C=1\mu F, L=1H$. $I/V = s/(Ls^2+Rs+1/C) = (s/L)/(s^2+(R/L)s+1/(LC))$. Pick the plot by **two qualitative facts** — initial and final current:
> - **Zero at the origin** ⇒ `i(0⁺)=0` *and* `i(∞)=0` (the capacitor blocks DC).
> - Complex poles ⇒ it overshoots and rings before dying out.

```matlab
IV_facit = s/(s^2 + 1000*s + 1e6);    % the facit/plot uses zeta=0.5
```

![[Q8_current_step.png]]

> [!warning] Trap
> With the *literal* `R=1, L=1` you get `s/(s²+s+1e6)`, ζ≈0.0005 — it would ring for ~300 cycles. The official facit and the printed plot actually use `s²+1000s+1e6` (zeta=0.5, i.e. `R/L=1000`). **The MC answer n.3 is robust either way** because you choose it from the *shape* (start 0 → oscillate → die to 0), not the exact damping.

---

## Q9 — Laplace of an ODE with initial conditions

> [!success] Facit: answer 1

> [!example]- Approach
> `x'' + x' − 2x = 4`, `x(0)=2, x'(0)=1`. Transform each term carrying its ICs, then isolate `X(s)`.

$$(s^2X-2s-1)+(sX-2)-2X=\frac{4}{s}\ \Rightarrow\ (s^2+s-2)X=\frac{4}{s}+2s+3$$

$$\boxed{X(s)=\frac{2s^2+3s+4}{s(s-1)(s+2)}}$$

> [!warning] Trap
> The IC terms. `ℒ{x''}=s²X−sx(0)−x'(0)` and `ℒ{x'}=sX−x(0)` — drop one and the numerator is wrong. Factor `s²+s−2=(s−1)(s+2)`; the `4` on the RHS becomes `4/s`.

---

## Q10 — Closed loop, type-1 plant, step error

> [!success] Facit: answer 1 (e_ss = 0)

> [!example]- Approach
> $K\cdot G / (1 + K\cdot G\cdot H)$, $G=1/(s(s+0.1))$, $K=5$, $H=1$, step input $r=5$. The open loop has an integrator (`1/s`) ⇒ **type 1** ⇒ zero steady-state error to a step.

```matlab
L10 = 5/(s*(s+0.1));                   % open loop, type 1
Etf = minreal(1/(1+L10));              % error TF E/R
ess10 = 5*dcgain(Etf);                 % 5 * 0 = 0
```

> [!warning] Trap
> The input amplitude (5) is a distractor — a type-1 system tracks **any** constant step with zero error. Don't compute a finite `1/(1+Kp)`; recognise the system type first.

---

## ⚠️ Got wrong / review

> [!todo] Review Checklist
> Fill this in after a practice run with `practice_ReExam_F22.m`. Candidates that bite:
> - [ ] Q4 — did I trust `minreal` and get the −2 pole? Build char-poly by hand.
> - [ ] Q8 — did I try to compute ζ instead of reading the shape?
> - [ ] Q5 — did I forget the DC gain is *negative* dB?
> - [ ] Q6 — did I include the step term in `e_ss` (should be ramp-only)?

---

## Links
- Patterns: [[P1 — Transfer Functions, Block Reduction & Modelling]] (Q1,Q3,Q4,Q9) · [[P2 — Frequency Response & Bode Read-Off]] (Q5) · [[P3 — Stability, Margins & Nyquist]] (Q4) · [[P4 — Second-Order Specs (Time & Frequency)]] (Q2,Q7) · [[P5 — Steady-State Error & System Type]] (Q6,Q10)
- Companion paper exam: [[W-F22 — Worked Exam]]
