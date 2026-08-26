---
tags: [34722, lcd, exam, worked, F22]
course: 34722 Linear Control Design 1
exam_set: Exam F22 (25 May 2022)
questions: 20
purpose: Full worked walkthrough of Exam F22 — per question the approach, the MATLAB line that nails it, the embedded graph, the facit answer, and the planted trap
---
# W-F22 — Worked Exam

> [!info] Exam Resources
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Paper:** [[LCD1 F22 - Questions no answers.pdf]] · **Official answers:** [[LCD1 F22 - Solutions.pdf]] (Past Exams folder)
> - **Solve script:** `EXAM/Scripts/solved/solve_F22.m` · **Practice yourself:** `EXAM/Scripts/practice/practice_F22.m`
> - Run headless: `matlab -batch "solve_F22"`

**Facit overview:**
`Q1:1 Q2:5 Q3:1 Q4:4 Q5:5 Q6:2 Q7:3 Q8:2 Q9:4 Q10:3`
`Q11:b Q12:b Q13:c Q14:e Q15:d Q16:b Q17:e Q18:d Q19:a Q20:a`

---

## Q1 — Block-diagram reduction

> [!success] Facit: answer 1

> [!example]- Approach
> `A,B` in series (multiply); `C,D` in parallel (add); take-off moved past `E` (so `H1` divides by `E`); reduce inner feedback loop then outer.

$$\frac{Y}{R}=\frac{ABE^2(C+D)}{(1+AB)\,[1+(C+D)E\,H_2]\,E+ABE(C+D)H_1}$$

> [!warning] Trap
> Moving the take-off point past `E` means `H1` picks up a `1/E`. Reduce the **inner** loop first, then the outer.

---

## Q2 — RC time constant, which statement is false?

> [!success] Facit: answer 5 (false)

> [!example]- Approach
> `G=(1/RC)/(s+1/RC)`, `R=50`, `C=160 µF` (the "160F" in the problem is microfarad).

```matlab
RC = 50*160e-6;       % tau = 8 ms,  5*tau = 40 ms,  63.2% at 1*tau = 8 ms
```

> [!warning] Trap
> Statement 5 claims 16 ms — it's **false**; the true `τ=RC=8 ms`. The question asks which statement is wrong, not right.

---

## Q3 — 2nd-order step vs ζ

> [!success] Facit: answer 1

> [!example]- Approach
> `ζ=0` ⇒ undamped sinusoid, **constant amplitude** (poles on the imaginary axis).

> [!warning] Trap
> ζ=0 is *not* a flat line and *not* a decaying ring — it oscillates forever at constant amplitude.

---

## Q4 — Bode identification

> [!success] Facit: answer 4

> [!example]- Approach
> One **real RHP zero** + two conjugate poles **on the imaginary axis** (Re=0).

> [!warning] Trap
> The RHP zero gives `+20 dB/dec` on magnitude but `−90°` on phase (phase *drops* while gain *rises*) — the signature giveaway.

---

## Q5 — Bode read-off → pick `G(s)`

> [!success] Facit: answer 5

> [!example]- Approach
> DC ≈ 5.9 dB ≈ ×2; flat to ω=1 then −40 dB/dec (2 poles); phase 165°→−90° (one zero); no peak ⇒ real poles; positive poles/zero.

$$G(s)=\frac{s-2}{(1+s)^2}$$

```matlab
G5 = (s-2)/(1+s)^2;   % DC |G5(0)| = 2  (= 6.02 dB)
```

![[Q5_bode_RHPzero.png]]

> [!warning] Trap
> The `s−2` is a **RHP zero** — magnitude climbs but phase falls. The Bode magnitude alone looks like a normal zero; the phase is what tells you it's in the RHP.

---

## Q6 — Find `K` so PM=40°, `G=K/(s(s+a))`

> [!success] Facit: answer 2 (K≈8.4)

> [!danger] Misprint
> The paper writes `s+21`, but the facit `K=8.4` only matches `a=2.1`.

> [!example]- Approach
> Find crossover frequency $\omega_c$ where the phase is $-180^\circ + \text{PM} = -140^\circ$, then set $K = 1 / |G_1(j\omega_c)|$.

```matlab
a = 2.1;  G1 = 1/(s*(s+a));
w  = logspace(-2,3,2e5);
ph = squeeze(angle(freqresp(G1,w)))*180/pi;
wc = interp1(ph, w, -180+40);          % phase = -140 -> PM=40
K  = 1/abs(freqresp(G1,wc));           % 8.4  (= 18.5 dB)
```

![[Q6_margin_PM40.png]]

> [!warning] Trap
> PM=40 means find ω where the **phase** is `−180°+40°=−140°`, *then* set `K` so the gain is 1 there. `20log10(8.4)=18.5 dB` matches the facit's dB hint.

---

## Q7 — DC gain in dB, `G=12/((s+2)(s+3))`

> [!success] Facit: answer 3 (6 dB)

> [!example]- Approach
> Substitute $s=0$ to find the DC gain $G(0)$, then convert to decibels using $20\log_{10}(|G(0)|)$.

```matlab
G7 = 12/((s+2)*(s+3));  % DC = 12/6 = 2  (= 6.02 dB)
```

> [!warning] Trap
> `dcgain = 12/(2·3) = 2`, and `20log10(2)=6 dB`. Plug `s=0`, don't forget to convert to dB.

---

## Q8 — ODE `5y''+y'+0.5y=3u` → poles

> [!success] Facit: answer 2

> [!example]- Approach
> Convert the ODE to the transfer function $G(s) = \frac{3}{5s^2 + s + 0.5}$ and find its poles.

```matlab
G8 = 3/(5*s^2 + s + 0.5);  pole(G8)   % -0.1 +/- 0.3j
```

> [!warning] Trap
> Divide the whole denominator by 5 before reading ωn/ζ, or just let `pole()` do it. Complex pair `−0.1±0.3j`.

---

## Q9 — State-space, find `w` for all poles in LHP

> [!success] Facit: answer 4 (w>2)

> [!example]- Approach
> Given $A=\begin{bmatrix} -1 & 1 \\ 2 & -w \end{bmatrix}$, find the characteristic equation $s^2 + (1+w)s + (w-2) = 0$. Apply the Routh-Hurwitz stability criterion or verify eigenvalues.

```matlab
for w = [1.5 2 3], disp(max(real(eig([-1 1; 2 -w])))); end  % only w=3 stable
```

> [!warning] Trap
> The constant term `w−2` is the binding condition (`>0 ⇒ w>2`); the `1+w>0` term is satisfied for all sensible `w`.

---

## Q10 — `s²+2s+2=0` → damping type

> [!success] Facit: answer 3 (underdamped)

> [!example]- Approach
> Compare the characteristic equation $s^2 + 2\zeta\omega_n s + \omega_n^2 = 0$ with $s^2 + 2s + 2 = 0$ to extract $\omega_n$ and $\zeta$.

> [!warning] Trap
> ζ=0.707 is the classic "just underdamped" value (~5 % overshoot), *not* critically damped (that's ζ=1).

---

## Q11 — Nyquist gain margin

> [!success] Facit: answer b (15.71 dB)

> [!example]- Approach
> Find the distance from the origin where the Nyquist plot crosses the negative real axis. The gain margin is $GM = 1 / |x_{crossing}|$.

```matlab
GM = 1/0.1639;  20*log10(GM)           % 15.71 dB
```

> [!warning] Trap
> GM = `1/|crossing|`, then convert to dB. The crossing value is already the distance to the origin.

---

## Q12 — Unstable plant (RHP pole), `K` for stability

> [!success] Facit: answer b (KP=50)

> [!example]- Approach
> With one open-loop RHP pole ($P=1$), the closed-loop system is stable ($Z=0$) if and only if the Nyquist plot encircles the critical point $-1$ exactly once counter-clockwise ($N = -1$). This requires $K_P > 1/|x_{crossing}|$.

```matlab
1/0.0222                               % 45.05  -> KP=50 > 45 is stable
```

> [!warning] Trap
> An **unstable** plant flips the stable interval — you need `K > K_min`, not `0<K<GM`. The encirclement count `Z=N+P` requires the curve to wrap `(−1,0)` *counter-clockwise* P times.

---

## Q13 — Lead contribution in dB

> [!success] Facit: answer c (11 dB)

> [!example]- Approach
> Use the lead center frequency relationship $\tau_d = 1 / (\omega_c\sqrt{\alpha})$ to solve for $\alpha$. The maximum lead gain is $M_D = 1/\sqrt{\alpha}$.

```matlab
tau_d = 0.355;  wc = 10;
alpha = (1/(wc*tau_d))^2;  MD = 1/sqrt(alpha);  20*log10(MD)   % ~11 dB
```

> [!warning] Trap
> The lead's peak gain is `1/√α` (in dB: `−10log10(α)`). Get α from `τ_d=1/(ωc√α)` first.

---

## Q14 — Closed-loop Bode → error step response

> [!success] Facit: answer e

> [!example]- Approach
> Analyze the low-frequency magnitude and high-frequency resonance peak of the closed-loop transfer function.

> [!warning] Trap
> "0 dB at DC" on the *closed-loop* magnitude means the output tracks the input ⇒ zero steady-state error; the peak only adds ringing.

---

## Q15 — 4th-order type-0, zero below the poles

> [!success] Facit: answer d

> [!example]- Approach
> Sketch or analyze the magnitude asymptotes and phase shifts when a zero lies below the poles.

> [!warning] Trap
> The early zero can push the magnitude back up through 0 dB twice — two gain crossovers, which is the option-d signature.

---

## Q16 — Steady-state error → `KP`

> [!success] Facit: answer b (KP=2)

> [!example]- Approach
> Solve for $K_P$ using the steady-state error equation $e_{ss} = \frac{1}{1 + K_P G(0)}$.

```matlab
G0 = 10^(-7.9588/20);                  % ~0.4
KP = (1/G0)*(1/0.555 - 1);             % 2
```

> [!warning] Trap
> Convert `G(0)` from dB to **linear** (`10^(dB/20)`) before plugging in. `0.4` linear, not `−7.96`.

---

## Q17 — PI-Lead, find α

> [!success] Facit: answer e (α=0.5)

> [!example]- Approach
> Set up the phase-budget equation: $-180^\circ + \gamma_M = \phi_G + \phi_{Lead} + \phi_{PI}$. Solve for the required lead phase $\phi_m$, then compute $\alpha = \frac{1-\sin(\phi_m)}{1+\sin(\phi_m)}$.

```matlab
phi_i = -atand(1/5);                   % PI lag contribution
phi_m = -180 + 75 - (-112.77) - phi_i; % needed lead phase
alpha = (1 - sind(phi_m))/(1 + sind(phi_m));   % 0.5
```

> [!warning] Trap
> Phase budget `−180+γM = φ_G + φ_Lead + φ_PI`, all in **degrees**. The PI term `φ_PI=−atan(1/Ni)` is *negative* (a lag). Don't mix radians.

---

## Q18 — (conceptual)

> [!success] Facit: answer d

> [!example]- Approach
> Review the ideal feedforward disturbance rejection conditions and realizability constraints.

---

## Q19 — PI-Lead, find `KP`

> [!success] Facit: answer a (3.4154)

> [!danger] Misprint
> The paper says `α=0.001`, but the **official solution computes with α=0.01** (confirmed: `τ_d=0.1983=1/(50.42√0.01)` and `φ_m=78.58°=asin((1−0.01)/(1+0.01))`). With α=0.001 you'd get `KP≈1.2`; the facit 3.4154 requires **0.01**.

> [!example]- Approach
> Apply the phase budget to solve for $\omega_c$. Build the controller term $C_{PI}(s)C_D(s)$ and set $K_P = 1 / |G(j\omega_c)C_{PI}(j\omega_c)C_D(j\omega_c)|$.

```matlab
G19 = 900/((0.25*s+1)*(s^2+50*s+3000));
Ni = 3;  alpha = 0.01;  gammaM = 75;
phi_i = -atand(1/Ni);  phi_m = asind((1-alpha)/(1+alpha));
phiG_req = -180 + gammaM - phi_i - phi_m;
w = logspace(-2,3,2e5);
wc = interp1(squeeze(angle(freqresp(G19,w)))*180/pi, w, phiG_req);
tau_i = Ni/wc;  tau_d = 1/(wc*sqrt(alpha));
CPI = (tau_i*s+1)/(tau_i*s);  CD = (tau_d*s+1)/(alpha*tau_d*s+1);
KP = 1/abs(freqresp(G19*CPI*CD, wc));  % 3.4154
```

![[Q19_PIlead_margin.png]]

> [!warning] Trap
> The `α=0.001` typo. If your `KP` comes out ~1.2, you used the printed α — switch to 0.01 to match the official answer key.

---

## Q20 — (conceptual)

> [!success] Facit: answer a

> [!example]- Approach
> Analyze the trade-offs between phase margin, transient response oscillations, and system robustness.

> [!warning] Trap
> More phase margin trades **speed for stability** — slower but better-damped. Answer a captures the robustness/damping gain.

---

## ⚠️ Got wrong / review

> [!todo] Review Checklist
> Fill this in after a practice run with `practice_F22.m`. Candidates that bite:
> - [ ] Q12 — did I use `0<K<GM` instead of `K>K_min` for the unstable plant?
> - [ ] Q16 — did I forget to convert `G(0)` dB→linear?
> - [ ] Q19 — did I use the printed α=0.001 and get KP≈1.2?
> - [ ] Q5/Q4 — did I miss the RHP zero (phase falls while gain rises)?
> - [ ] Q6 — PM=40 ⇒ phase at `−140°`, then set gain=1 there?

---

## Links
- Patterns: [[P1 — Transfer Functions, Block Reduction & Modelling]] (Q1,Q8,Q9) · [[P2 — Frequency Response & Bode Read-Off]] (Q4,Q5,Q7) · [[P3 — Stability, Margins & Nyquist]] (Q9,Q11,Q12) · [[P4 — Second-Order Specs (Time & Frequency)]] (Q3,Q10) · [[P5 — Steady-State Error & System Type]] (Q16) · [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] (Q6,Q13,Q17,Q19)
- Companion paper exam: [[W-ReExam F22 — Worked Exam]]
