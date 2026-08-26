---
tags: [34722, lcd, exam, worked-exam]
course: 34722 Linear Control Design 1
pattern: W-F26
purpose: My sat F26 MCQ — every question worked out, with the trap I fell for and the P-note that cracks it
exam: F26 multiple-choice, sat 2-June-2026
---
# W-F26 — Worked Exam (MCQ)

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - Topic notes: [[P1 — Transfer Functions, Block Reduction & Modelling]] · [[P2 — Frequency Response & Bode Read-Off]] · [[P3 — Stability, Margins & Nyquist]] · [[P4 — Second-Order Specs (Time & Frequency)]] · [[P5 — Steady-State Error & System Type]] · [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] · [[P7 — Theory Exercises (Worked Proofs & Derivations)]]

> [!summary] Result on the sat attempt: **3 / 20** (Q1, Q7, Q11)
> Almost every miss was the **trap distractor sitting next to the right answer** —
> reciprocals, the raw input value, the *critical* (marginal) gain, the smallest
> option, a non-physical sign. The fix is finishing the last algebraic step and
> sanity-checking physics, not relearning the theory. ✅ = correct · ❌ = missed.

---
## Q1 ✅ — DC-motor block reduction → [[P1 — Transfer Functions, Block Reduction & Modelling]]

Inner loop $\dfrac{K_m}{s+0.01}$ with $K_b$ feedback $\to \dfrac{K_m}{s+0.01+K_mK_b}$.
Series with $K$ and the integrator $1/s$, close the unity outer loop:
$$\frac{Y}{U}=\frac{L}{1+L}=\frac{KK_m}{s^2+(0.01+K_mK_b)s+KK_m}$$

## Q2 ❌ — critically damped, $\omega_d=0$ · *picked "$\omega_d<2$, underdamped"* → [[P4 — Second-Order Specs (Time & Frequency)]]

Normalise the ODE first: $\ddot y+\dot y = 4u-y-\dot y \Rightarrow \ddot y+2\dot y+y=4u$.
Characteristic $s^2+2s+1=(s+1)^2 \Rightarrow \omega_n=1,\ 2\zeta\omega_n=2 \Rightarrow \zeta=1$.
**Critically damped**, $\omega_d=\omega_n\sqrt{1-\zeta^2}=0$.

## Q3 ❌ — $10<\omega_c<20$ ($\omega_c=15$) · *picked $\omega_c>30$* → [[P3 — Stability, Margins & Nyquist]]

$G=\dfrac{K}{s(s+15)}$, $PM=45^\circ \Rightarrow \angle G(j\omega_c)=-135^\circ$:
$$-90^\circ-\arctan\tfrac{\omega}{15}=-135^\circ \Rightarrow \arctan\tfrac{\omega}{15}=45^\circ \Rightarrow \omega_c=15.$$
Phase depends only on $\omega$, not $K$ — the crossover is pinned at 15.

## Q4 ❌ — $\omega_d\approx4$ rad/s · *picked $\omega_d=5$* → [[P4 — Second-Order Specs (Time & Frequency)]]

10% overshoot $\Rightarrow \zeta=0.591$. $\omega_d=5\sqrt{1-0.591^2}=5(0.807)=4.03$.
$\omega_d=5$ would mean $\zeta=0$ (100% overshoot) — contradicts 10%.

## Q5 ❌ — $e_{ss}\approx29$ · *picked 30* → [[P5 — Steady-State Error & System Type]]

Type-0. $K_{pos}=C(0)G(0)=0.3\cdot\tfrac{1}{10}=0.03$ (delay $e^{-0.1s}=1$ at DC).
$$e_{ss}=\frac{30}{1+K_{pos}}=\frac{30}{1.03}=29.1\to 29.$$
Picking 30 drops the $1+K_{pos}$.

## Q6 ❌ — $H=\dfrac{AB}{1+B(C+D)}$ · *picked $\dfrac{AB}{1+BCD}$* → [[P1 — Transfer Functions, Block Reduction & Modelling]]

$C$ and $D$ are both driven by the output and **summed** at the $++$ junction
(parallel), then fed back negatively around $B$; $A$ is in series in front.
Parallel feedback $\Rightarrow (C+D)$, not the cascade $C\cdot D$.

## Q7 ✅ — Not stable → [[P3 — Stability, Margins & Nyquist]]

Substituting blocks: $H=\dfrac{s+2}{s^2-4s-16}$. Roots $2\pm\sqrt{20}=\{6.47,-2.47\}$ →
RHP pole → **unstable**.

## Q8 ❌ — three real poles, one at the origin · *picked "no pole at origin"* → [[P2 — Frequency Response & Bode Read-Off]]

Phase asymptote $-90^\circ$ at low $\omega$ **and** a very low gain-crossover
(0.331 rad/s) are both integrator signatures. Reverse-engineer: poles $\{0,5,6\}$ give
$\angle=-180^\circ$ at exactly **5.48 rad/s** (the stated $G_m$ frequency) and
$PM\approx83^\circ$ at 0.331 — a type-0 system can't hit those markers.
**Diagnostic:** low gain-crossover + big phase margin ⟹ a $1/s$ is present.

## Q9 ❌ — $\zeta\approx0.814,\ \omega_n\approx4.916$ · *picked the negative-$\zeta$ option* → [[P4 — Second-Order Specs (Time & Frequency)]]

1.23% overshoot $\Rightarrow \zeta=0.814$. $T_s=\dfrac{4}{\zeta\omega_n}=1 \Rightarrow \omega_n=\dfrac{4}{0.814}=4.92$.
Negative $\zeta$ = unstable, so it can't produce a settling overshoot — eliminate on sight.

## Q10 ❌ — $y(0)=0,\ \lim=0$ · *picked $y(0)=5$* → [[P1 — Transfer Functions, Block Reduction & Modelling]]

$G_1+G_2G_3=\tfrac{4}{s+10}+\tfrac{1}{s+10}=\tfrac{5}{s+10}$; positive feedback closes to
$H=\tfrac{5}{s+5}$. With $u=e^{-2t}$ ($U=\tfrac{1}{s+2}$): $Y=\tfrac{5}{(s+5)(s+2)}$.
$y(0^+)=\lim_{s\to\infty}sY=0$ (strictly proper); $\lim_{t\to\infty}y=\lim_{s\to0}sY=0$.

## Q11 ✅ — $K_P=6.6$ → [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]]

$PM=75^\circ$ wants the crossover where $\angle G=-105^\circ$ — the marker puts that at
$\omega=1.39$, where $|G|=-16.4$ dB. Raise gain to 0 dB there: $K_P=10^{16.4/20}=6.6$.

## Q12 ❌ — "relative degree $\ge3 \Rightarrow$ large $K_P$ destabilises" · *picked the Lead-branch statement* → [[P7 — Theory Exercises (Worked Proofs & Derivations)]]

Root-locus asymptotes for $n-m\ge3$ head into the RHP, so enough gain always
destabilises. Others false: higher $PM$ = *fewer* oscillations; rate limits are
*non*linear; static feed-forward doesn't move closed-loop poles; moving the Lead
between branches leaves $L=CG$ (so $G/(1+L)$) unchanged.

## Q13 ❌ — "0 dB at low freq $\Rightarrow$ zero steady-state error" · *picked "lower bandwidth $\Rightarrow$ faster"* → [[P5 — Steady-State Error & System Type]]

$|T(j\omega)|\to1$ as $\omega\to0$ means $T(0)=1$, so step output = reference → zero
error. Lower bandwidth means a **slower** response (the opposite of the trap).

## Q14 ❌ — the plot flat at $+12$ dB · *picked the $-28$ dB plot* → [[P5 — Steady-State Error & System Type]]

$|D|=\dfrac{|G_{ed}|}{|G_{er}|}$, in dB $|D|=|G_{ed}|-|G_{er}|$. At DC:
$-22.11-(-34.15)=+12.04$ dB → low-pass flat at $\approx+12$ dB then rolls off.
(Check: $|G_{er}(0)|=-34.15$ dB $\Rightarrow 1+K_PG(0)=51 \Rightarrow G(0)=10$; $|D(0)|=4=+12$ dB.)

## Q15 ❌ — $K_P=2.5$ · *picked 1.57* → [[P3 — Stability, Margins & Nyquist]]

One RHP open-loop pole ($P=1$) ⟹ need **one CCW encirclement** of $-1$. Crossing at
$-0.6356$ ⟹ critical gain $1/0.6356=1.573$; the $-1$ point is enclosed only once
$K_P$ pushes the crossing past it: **stable for $K_P>1.573$**. $2.5$ is in that region;
$1.57$ is *below* the boundary (marginal/unstable). Classic "found the critical gain,
forgot the inequality" trap — see Hub trap list.

## Q16 ❌ — $\dfrac{0.22s+1}{0.0022s+1}$ · *picked the reciprocal (a lag)* → [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]]

$+20$ dB at $\omega_c \Rightarrow \tfrac{1}{\sqrt\alpha}=10 \Rightarrow \alpha=0.01$. Centre the lead at
$\omega_c=45$: $\tau_d=\tfrac{1}{\omega_c\sqrt\alpha}=\tfrac{1}{45\cdot0.1}=0.222$, pole at
$\alpha\tau_d=0.00222$. A **lead** has the zero *before* the pole. Your pick is the
lag (gives $-20$ dB, phase lag).

## Q17 ❌ — $K_P=15$ · *picked 30* → [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]]

$PM=70^\circ \Rightarrow$ controller adds $-110-(-167.41)=+57.4^\circ$. Lead ($\alpha=0.02$) gives
$+73.9^\circ$ at centre, lag/PI part ($N_i=3$) gives $-16.5^\circ$: sum $+57.4^\circ$ — so the
lead is at max phase, $|lead(\omega_c)|=\tfrac{1}{\sqrt\alpha}=7.07$. Magnitude:
$K_P\cdot7.07\cdot|PI|\cdot|G|=1$ with $|G|=10^{-40.96/20}=0.00895$, $|PI|\approx1.05 \Rightarrow K_P=15$.

## Q18 ❌ — $K_P=5$ · *picked 0.2 ($=1/5$)* → [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]]

$G=\dfrac{3.652}{s(s+1)(s+5)}$, lead $\alpha=0.01 \Rightarrow \phi_{max}=78.6^\circ$. Crossover:
$-90-\arctan\omega-\arctan\tfrac{\omega}{5}+78.6=-135 \Rightarrow \arctan\omega+\arctan\tfrac{\omega}{5}=123.6^\circ \Rightarrow \omega_c\approx5$.
At $\omega_c$: $|G|=0.0204$, $|lead|=10 \Rightarrow K_P=\tfrac{1}{10\cdot0.0204}=4.9\approx5$ (full Bode → $PM=45.0^\circ$).

## Q19 ❌ — $u=K_Pe+F(0)r+F_d(0)d$ · *picked $u=K_Pe+F_d(s)d$* → [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]]

Plot shows **zero steady-state error to the reference** (so reference feed-forward
$F$ is needed — a type-0 plant with finite $K_P$ alone leaves error) **and** full
disturbance rejection. Both feed-forwards must be **static** $F(0),F_d(0)$: the plant's
zero at $s=+7.5$ is RHP, so the dynamic inverse $1/G$ has an unstable pole — you can't
use $F(s)=1/G(s)$. The picked option has no reference feed-forward, so it can't give
zero reference error.

## Q20 ❌ — $N=5$ · *picked $N=2$* → [[P7 — Theory Exercises (Worked Proofs & Derivations)]]

$G_0(0)=\tfrac12$, each $G_k(0)=\tfrac12$. The three nested summers give DC gain
$y_{ss}=\dfrac{K_Px}{1+K_Px+x+2x}$ with $x=(\tfrac12)^N$. Then
$e_{ss}=\dfrac{1+3x}{1+108x}=0.25 \Rightarrow x=\tfrac{1}{32} \Rightarrow N=5$
(exact: $\tfrac{1+3/32}{1+108/32}=\tfrac{35}{140}=0.25$).

---
> [!warning] My personal trap list (from this attempt)
> 1. **Finish the inequality / the "+1".** Q5 ($\div1.03$), Q15 ($K_P>$ not $=$).
> 2. **Lead vs lag orientation.** Q16/Q18 — a lead is zero-before-pole and *raises* gain by $1/\sqrt\alpha$. Don't grab $1/x$.
> 3. **Sanity-check physics first.** Q9 negative $\zeta$, Q4 $\omega_d=\omega_n$, Q2 $\zeta=1$ — kill the impossible option before computing.
> 4. **Read the Bode origin behaviour.** Q8 phase $-90^\circ$ + low crossover = pole at origin; Q13/Q14 low-freq level = steady-state behaviour.
> 5. **Feed-forward needs DC for steady state; RHP zeros forbid dynamic inversion.** Q19.

> [!note] Cross-check
> Every numeric answer here is reproduced by the LCD1 Solver engine
> (`lcd1-exam-suite/spike/test/exam-f26.test.js`, part of `npm test`). Paste a
> problem into LCD1 Solver mode and diff your hand result against the engine.
