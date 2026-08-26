---
tags: [34722, lcd, exam, theory, pattern]
course: 34722 Linear Control Design 1
pattern: P7
purpose: The 10 official theory exercises worked — the derivations behind the design recipes, plus the exam-style numeric ones (poles, ess, K2, feedforward choice)
---
# P7 — Theory Exercises (Worked Proofs & Derivations)

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Source:** *Theoretical Exercises LCD1* (Papageorgiou) + its official Solutions manual.

These are the proofs *behind* the cheat-sheet formulas. Q1–Q3 and Q10 are derivations (know the result + the one trick that cracks each). Q4–Q9 are exam-style numerics (Q4, Q5, Q6, Q9 appeared on real exams) — those are the ones to be able to *reproduce cold*.

---

## Q1 — Lead: prove `ω_m = 1/(τ_d√α)` and `φ_m`

> [!example]- Derivation
> Given $C_D(s) = \frac{\tau_d s + 1}{\alpha\tau_d s + 1}$ with $0 < \alpha < 1$. Substitute $s=j\omega$ to get the phase angle function:

$$\phi(\omega)=\arctan(\tau_d\omega)-\arctan(\alpha\tau_d\omega)$$

> [!example]- Derivation (continued)
> Set the derivative $\frac{d\phi}{d\omega} = 0$:

$$\frac{\tau_d}{1+(\tau_d\omega)^2}-\frac{\alpha\tau_d}{1+(\alpha\tau_d\omega)^2}=0 \;\Rightarrow\; \boxed{\omega_m=\frac{1}{\tau_d\sqrt\alpha}}$$

> [!example]- Derivation (continued)
> Evaluating the maximum phase $\varphi_m$ and magnitude at $\omega_m$ yields $|C_D(j\omega_m)| = \frac{1}{\sqrt{\alpha}}$ and:

$$\varphi_m=\arctan\!\Big(\frac{1-\alpha}{2\sqrt\alpha}\Big)=\arcsin\!\Big(\frac{1-\alpha}{1+\alpha}\Big)$$

> [!tip] Key Trick
> The centre frequency is the **geometric mean** of the zero ($1/\tau_d$) and the pole ($1/(\alpha\tau_d)$). The two trigonometric forms of $\varphi_m$ are mathematically identical — the exam may print either.
> 
> *Connects to:* [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]].

---

## Q2 — First-order LPF: `ω_c=ω_BW=1/τ`, `t_r≈2.2τ`, `t_s≈4τ`

> [!example]- Derivation
> Given the standard first-order low-pass filter $G(s) = \frac{1}{\tau s + 1}$:
> - **Bandwidth** (frequency $\omega_{BW}$ where magnitude drops by $-3\text{ dB}$ or $\frac{1}{\sqrt{2}}$ of DC gain):
>   $$\frac{1}{\sqrt{(\tau\omega_{BW})^2+1}}=\frac{1}{\sqrt{2}} \;\Rightarrow\; (\tau\omega_{BW})^2+1=2 \;\Rightarrow\; \omega_{BW}=\frac{1}{\tau}$$
> - **Crossover**: Treated as unity feedback around $G_{ol} = \frac{1}{\tau s}$; crossover occurs when $|G_{ol}(j\omega_c)| = 1$:
>   $$\frac{1}{\tau\omega_c}=1 \;\Rightarrow\; \omega_c=\frac{1}{\tau} \;\Rightarrow\; \omega_c=\omega_{BW}$$
> - **Rise time** ($10\% \to 90\%$): Derived from the step response $y(t) = 1 - e^{-t/\tau}$:
>   $$e^{(t_2-t_1)/\tau}=9 \;\Rightarrow\; t_r = \tau\ln(9) \approx 2.2\tau$$
> - **Settling time** ($2\%$ band, $98\%$ settled):
>   $$e^{-t_s/\tau}=0.02 \;\Rightarrow\; t_s = \tau\ln(50) \approx 4\tau$$

> [!note] Why it matters
> These derivations establish the rules of thumb on your cheat-sheet ($t_r \approx 1.8/\omega_n$, $t_s \approx 4/(\zeta\omega_n)$) specialized for a single real pole. For any **first-order system, crossover frequency = bandwidth = pole frequency**.

---

## Q3 — P-Lag phase contribution

> [!example]- Derivation
> For the lag controller $C_L(s) = \frac{\tau_i s + 1}{\tau_i s + 1/\beta}$ with $\beta > 0$, evaluated at the target crossover frequency $\omega_c = N_i / \tau_i$:

$$\phi_L=\arctan\!\Big(N_i\,\frac{1-\beta}{1+\beta N_i^2}\Big)$$

> [!example]- Derivation (continued)
> Since $\beta > 1$ for a phase lag, the term $1-\beta < 0$, which mathematically proves that **$\phi_L < 0$ (a lag subtracts phase)**. In the limit as $\beta \to \infty$:

$$\lim_{\beta\to\infty}\phi_L=-\arctan\!\Big(\frac1{N_i}\Big)$$

> [!tip] Key Takeaway
> As the static gain factor $\beta \to \infty$, the P-Lag phase contribution converges exactly to the **PI lag term** $\phi_{PI} = -\arctan(1/N_i)$ used in the phase-budget equation. Thus, a P-Lag controller with infinite static gain *is* a PI controller.
> 
> *Connects to:* [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] & [[P7 — Theory Exercises (Worked Proofs & Derivations)#Q10 — Why P-Lag cuts ess by β (and β→∞ ⇒ PI ⇒ ess→0)|Q10 below]].

---

## Q4 — Poles from an ODE (Exam 2021) ⭐

> [!example]- Solution
> Given $y^{(4)} + 9y^{(3)} + 20\ddot{y} = 71u$. Taking the Laplace transform with zero initial conditions yields:

$$G(s)=\frac{71}{s^4+9s^3+20s^2}=\frac{71}{s^2(s^2+9s+20)}=\frac{71}{s^2(s+4)(s+5)}$$

> [!success] Poles: $\{0, 0, -4, -5\}$

> [!note] Why it matters
> - A **double pole at the origin ($s^2$) means the open-loop system is unstable** and represents a **type-2** system.
> - **Shortcut:** The highest derivative of $y$ (4th) determines the total number of poles (4); the lowest derivative of $y$ ($\ddot{y}$, 2nd) determines the number of poles at the origin (2).
> 
> *Connects to:* [[P1 — Transfer Functions, Block Reduction & Modelling]].

---

## Q5 — ess with the controller in the *feedback* branch (Exam 2021) ⭐

> [!example]- Solution
> Given the plant $G(s) = \frac{1224}{s^3 + 30s^2 + 257s + 612}$ and feedback gain $K_P = 2$.
> 
> The error transfer function is:

$$G_{er}(s)=\frac{1}{1+K_P G(s)}, \qquad e_{ss}=\lim_{s\to0}s G_{er}(s)\frac{1}{s}=G_{er}(0)$$

> [!example]- Solution (continued)
> Since $G(0) = \frac{1224}{612} = 2$, evaluating at DC yields:
> $$e_{ss} = \frac{1}{1 + K_P G(0)} = \frac{1}{1 + 2 \cdot 2} = \frac{1}{5} = 0.2$$

> [!success] Facit: e_ss = 0.2

> [!warning] Trap
> Even though the controller $K_P$ is in the **feedback path** (not the forward path), the closed-loop error denominator is still $1 + K_P G(s)$. Do not accidentally use the complementary tracking sensitivity $\frac{K_P G(0)}{1+K_P G(0)}$.

---

## Q6 — Nested loop, solve for `K₂` (Exam 2021) ⭐

> [!example]- Solution
> Given inner loop closed around $K_1 G_1$, outer gain $K_2$, and plant $G_2$ with DC gain $G_2(0) = -7.9588\text{ dB} = 0.4$.
> - Outer loop opened: a step input $1/K_2$ yields inner loop steady-state error $e_1(0) = \varepsilon_1 = 0.4$.
> - Outer loop closed: a unit step input yields outer steady-state error $e_2(0) = \varepsilon_2 = 0.05$.
> 
> The inner loop's closed-loop DC gain is $G_{cl,1}(0) = 1 - \varepsilon_1$. The outer loop steady-state error is:

$$\varepsilon_2=\frac{1}{1+K_2(1-\varepsilon_1)G_2(0)} \;\Rightarrow\; K_2=\frac{1-\varepsilon_2}{\varepsilon_2\,G_2(0)\,(1-\varepsilon_1)}$$

> [!example]- Solution (continued)
> Substituting the linear values:
> $$K_2 = \frac{0.95}{0.05 \cdot 0.4 \cdot (1 - 0.4)} = \frac{0.95}{0.012} = 79.17$$

> [!success] Facit: K_2 = 79.17

> [!note] Why it matters
> Peel nested loops **inside-out**. Each successfully closed loop contributes a DC tracking gain of $(1-\varepsilon)$ as an input multiplier to the next outer loop.
> 
> Always convert $G_2(0)$ from **dB to linear** ($10^{-7.9588/20} = 0.4$) before using it.

---

## Q7 — Static gain of a cascade with unity feedback (Re-Exam 2021)

> [!example]- Solution
> Given $G_{ol}(s) = \frac{4}{s+1} \cdot \frac{2}{s+2} \cdots \frac{N}{s+N} = 4 \prod_{i=1}^{N}\frac{i}{s+i}$.
> 
> To find the closed-loop DC gain $G_{cl}(0)$, first evaluate $G_{ol}(s)$ at $s=0$:
> $$\text{For each cascade term: } \lim_{s \to 0} \frac{i}{s+i} = \frac{i}{i} = 1$$
> $$G_{ol}(0) = 4 \cdot (1 \cdot 1 \cdots 1) = 4$$

$$G_{cl}(0)=\frac{G_{ol}(0)}{1+G_{ol}(0)}=\frac{4}{5}=\mathbf{0.8}$$

> [!success] Facit: G_cl(0) = 0.8

> [!tip] Key Trick
> The product **telescopes** at DC ($s=0$) because every rational factor $\frac{i}{s+i}$ simplifies exactly to $1$. Do not expand the $N$-th order polynomial; simply set $s=0$ directly.

---

## Q8 — Pick the right feed-forward `F_d` (Exam 2022) ⭐

> [!example]- Solution
> A disturbance enters after a chain of $n$ first-order lags $G_1(s) = \prod_{k=1}^n \frac{1}{\tau_k s + 1}$. The disturbance dynamics are $D(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$.
> 
> The ideal, exact cancelling feed-forward controller is:

$$F_d(s)=\frac{D(s)}{G_1(s)}=\frac{\omega_n^2\prod_{k=1}^n(\tau_k s+1)}{s^2+2\zeta\omega_n s+\omega_n^2}$$

> [!example]- Solution (continued)
> Since $F_d(s)$ has $n$ zeros and only $2$ poles, it is **improper by $n-2$ orders**. To make it realizable, we append an $(n-2)$-order low-pass filter with a fast time constant $\tau_f$:

$$\boxed{F_d(s)=\frac{\omega_n^2\prod_{k=1}^n(\tau_k s+1)}{(s^2+2\zeta\omega_n s+\omega_n^2)(\tau_f s+1)^{n-2}}, \quad \tau_f\le\frac{\min(\tau_k)}{5}} \;\text{— option (d)}$$

> [!warning] Distractor Elimination
> - **Options (a), (b), (c):** Either remain improper (insufficient filter poles) or incorrectly drop the disturbance dynamics $D(s)$.
> - **Option (e):** Appends the correct pole order, but uses a filter time constant $\tau_f \ge \text{max}(\tau_k)/5$, which is **too slow** and filters out the actual plant dynamics.
> - **Option (d) (Correct):** Proper and uses a fast filter ($\tau_f \le \text{min}(\tau_k)/5$) to preserve control action.
> 
> *Connects to:* [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)#Feed-forward disturbance rejection|Feed-forward in P6]].

---

## Q9 — Two nested P-controllers, solve for `K_P` (Re-Exam 2022) ⭐

> [!example]- Solution
> The inner closed loop is $G_1(s) = \frac{K_P G(s)}{1 + K_P G(s)}$. The outer loop has error transfer function:

$$G_e(s)=\frac{1}{1+K_P G_1(s)}=\frac{1+K_P G(s)}{1+K_P G(s)+K_P^2 G(s)}$$

> [!example]- Solution (continued)
> At DC ($s=0$), we are given $G(0)=0.75$ and steady-state step tracking error $e(0)=0.25$:
> 
> $$0.25=\frac{1+0.75K_P}{1+0.75K_P+0.75K_P^2} \;\Rightarrow\; K_P^2-3K_P-4=0 \;\Rightarrow\; (K_P-4)(K_P+1)=0$$
> 
> Discarding the negative root ($K_P = -1$), we find the stabilizing positive gain.

> [!success] Facit: K_P = 4

> [!warning] Trap
> The nested architecture results in a **quadratic equation** in terms of the gain parameter ($K_P^2 G(0)$). Do not try to linearize or approximate it — solve the quadratic equation directly and choose the positive, stable root.

---

## Q10 — Why P-Lag cuts ess by `β` (and `β→∞` ⇒ PI ⇒ ess→0)

> [!example]- Derivation
> For a proportional controller, steady-state step error is $e_{ss} = \frac{1}{1 + K_P p}$ where $p = G(0)$.
> 
> Under a P-Lag controller $C_L(s) = K_P \frac{\tau_i s + 1}{\tau_i s + 1/\beta}$, the DC gain of the controller is $C_L(0) = K_P \beta$. The resulting error is:

$$e_{ss,l}=G_{e,l}(0)=\frac{1}{1+K_P\,\beta\,p}$$

> [!example]- Derivation (continued)
> Taking the ratio of errors under high gain ($K_P p \gg 1$):
> 
> $$\frac{e_{ss}}{e_{ss,l}}=\frac{1+K_P\beta p}{1+K_P p}\approx\frac{K_P\beta p}{K_P p}=\boxed{\beta}$$

> [!note] Why it matters
> - The P-Lag controller reduces the steady-state tracking error by an exact factor of **$\beta$**.
> - As $\beta \to \infty$, the lag controller converges to a **PI controller** (adding a pole exactly at the origin, changing the system to a Type-1 system) which yields **zero** steady-state step error ($e_{ss} \to 0$).
> 
> *Connects to:* [[P5 — Steady-State Error & System Type]].
