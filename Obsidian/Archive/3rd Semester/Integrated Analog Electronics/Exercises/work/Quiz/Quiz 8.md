# ⚙️ Feedback & Stability — Quiz 8 Derivations

> [!abstract] **Goal of This Quiz**
> Understand how **negative feedback** affects amplifier **stability**,  
> how to evaluate **phase margin (PM)** and **gain margin (GM)** from **Bode/Nyquist plots**,  
> and how **Miller compensation** shifts pole locations to achieve a **stable and well-damped design**.

---

> [!info] **Concept**
> The **stability** of a negative-feedback amplifier depends on the **closed-loop pole locations** and **loop-gain phase margin**.
>
> - ✅ **Stable** → all poles in the **left-half plane (LHP)** ($\text{Re}\{p\}<0$)  
> - ❌ **Unstable** → any pole in the **right-half plane (RHP)** ($\text{Re}\{p\}>0$)  
> - ⚠️ **Marginally Stable** → poles on the imaginary axis (sustained oscillations)  
>
> Feedback effects (*CMOS Analog IC Design Fundamentals*):  
> - Increases bandwidth by $(1+\beta A)$  
> - Reduces distortion and gain sensitivity  
> - Alters pole locations and introduces **phase lag**  
> - Miller compensation adds a **dominant pole** and performs **pole-splitting**
>
> **Key Equations**
> $$
> A_{CL} = \frac{A}{1+\beta A}, \qquad
> L(s) = A(s)\beta, \qquad
> \text{PM} = 180^\circ + \angle L(j\omega_{0dB})
> $$

---

> [!summary] **Question 1 — Stability Condition**  
> **Question:** A system with negative feedback is stable if …  
>
> **Given:**  
> A linear feedback system with open-loop transfer function $A(s)$ and feedback factor $\beta$.  
> The closed-loop transfer is:
> $$
> A_{CL}(s) = \frac{A(s)}{1+\beta A(s)}.
> $$
>
> **Derivation**
>
> The denominator $(1+\beta A(s))$ defines the **characteristic equation**:
> $$
> 1+\beta A(s)=0
> $$
> whose roots are the **closed-loop poles**.
>
> - If $\text{Re}\{p_i\}<0$ → **stable**, output decays exponentially.  
> - If $\text{Re}\{p_i\}>0$ → **unstable**, output grows unbounded.  
> - If $\text{Re}\{p_i\}=0$ → **marginally stable**, sustained oscillation.
>
> Negative feedback normally **moves poles leftward** (increases damping).  
> Too much gain or excess phase lag can move them rightward, reducing PM and risking oscillation.
>
> **Condition**
> $$
> \text{System is stable if all closed-loop poles satisfy Re}\{p_i\} < 0
> $$
>
> ✅ **Answer:** *The transfer function of the system has only left-half-plane poles.*

---

> [!summary] **Question 2 — Role of Negative Feedback**
>
> **Question:** Negative feedback helps …  
>
> **Explanation**
>
> Feedback modifies the **loop gain** $L(s)=A(s)\beta$.  
> The equation $1+\beta A(s)=0$ shows that feedback directly sets the **closed-loop pole positions**, and thus the **stability**.  
> It doesn’t change open-loop pole positions, but controls how they move when feedback is applied.
>
> ✅ **Answer:** *Controlling stability of the closed-loop system.*

---

> [!summary] **Question 3 — First-Order Feedback System**
>
> **Question:** A first-order system with negative feedback is …  
>
> **Derivation**
>
> Let
> $$
> A(s)=\frac{A_0}{1+s/\omega_p}, \qquad L(s)=\beta A(s).
> $$
> The phase of $L(j\omega)$ never exceeds $-90^\circ$, so the Nyquist curve can’t encircle $(-1,0)$.  
> The magnitude $|L|$ falls smoothly, meaning poles remain in the LHP.
>
> ✅ **Answer:** *Never unstable* (always stable for a single-pole loop).

---

> [!summary] **Question 4 — Phase Margin of a 1st-Order Loop**
>
> **Question:** A first-order system with negative feedback and $A_0\beta\gg1$ has a phase margin of about …  
>
> **Derivation**
>
> For $L(s)=A_0\beta/(1+s/\omega_p)$:
> $$
> \text{PM} = 90^\circ + \tan^{-1}\!\left(\frac{1}{A_0\beta}\right) \approx 90^\circ
> $$
> Such a loop is **unconditionally stable**, since its phase never reaches $-180^\circ$ before unity gain.
>
> ✅ **Answer:** *≈ 90° that ensures stability.*

---

> [!summary] **Question 5 — Second-Order System with Q = 0.7**
>
> **Question:** A second-order system with negative feedback and $Q=0.7$ has a frequency response where the gain has …  
>
> **Derivation**
>
> $$
> |A_{CL}(j\omega)| = \frac{A_0}{\sqrt{(1-(\omega/\omega_n)^2)^2+(2Q\omega/\omega_n)^2}}.
> $$
> For $Q≈0.707=1/\sqrt{2}$, the response is **maximally flat (Butterworth)**.  
> Lower $Q$ → overdamped; higher $Q$ → underdamped with peaking.
>
> ✅ **Answer:** *A flat response.*

---

> [!summary] **Question 6 — Nyquist Criterion**
>
> **Question:** According to the Nyquist plot, a system is stable if …  
>
> **Explanation**
>
> **Nyquist stability criterion:**
> - Each **clockwise encirclement** of $(-1,0)$ adds one unstable closed-loop pole.  
> - If $L(s)$ has no RHP poles and the plot does **not encircle** $(-1,0)$, the system is stable.  
>
> ✅ **Answer:** *Stable as the curve does not enclose (−1,0).*
>
> ```
>        Im{L(jω)}
>           ↑
>           |
> (-1,0)◉ ←---→ Stable region
>           |
> ------------------------→ Re{L(jω)}
> ```

---

> [!summary] **Question 7 — Miller Compensation**
>
> **Question:** A method for modifying frequency response to get a desired phase margin uses a Miller capacitor. This capacitor …  
>
> **Derivation**
>
> In two-stage op-amps, $C_c$ connects the high-gain node to the output, producing **pole splitting**:
> - Dominant pole moves **downward** ($p_1↓$)  
> - Non-dominant pole moves **upward** ($p_2↑$)  
>
> This increases PM and ensures the loop is effectively **first-order** near unity gain.
>
> ✅ **Answer:** *Splits the poles and moves the low-frequency pole downwards.*

---

> [!summary] **Question 8 — 2nd-Order System Stability Criterion**
>
> **Question:** A second-order system is stable if …  
>
> **Derivation**
>
> Stability requires that at the frequency where the phase shift is $-180^\circ$, the gain is below unity:
> $$
> |L(j\omega_{-180°})| < 1
> $$
> i.e. positive phase margin.  
> If $|L|$ is “much smaller than 1” there, the system is robustly stable.
>
> ✅ **Answer:** *The phase margin is 0° and the gain is much smaller than 1 → stable.*

---

> [!summary] **Question 9 — High Phase Margin Effect**
>
> **Question:** A second-order system with high phase margin …  
>
> **Derivation**
>
> $$
> \text{PM} \approx \tan^{-1}\!\left(\frac{2\zeta}{\sqrt{-2\zeta^2+1}}\right), \qquad Q = \frac{1}{2\zeta}.
> $$
> Large PM → large damping ratio $\zeta$ → small $Q$ → no peaking in $|A_{CL}|$.  
>
> ✅ **Answer:** *Has almost no peak in closed-loop frequency response.*

---

## 🧠 Summary of Stability Relationships

| Concept | Formula | Typical Stable Value |
|----------|----------|----------------------|
| Loop gain | $L(s)=A(s)\beta$ | — |
| Phase margin | $\text{PM}=180^\circ+\angle L(j\omega_{0dB})$ | $>45^\circ$ |
| Gain margin | $\text{GM}=1/|L|$ at $-180^\circ$ | $>6$ dB |
| Damping ↔ PM | $\text{PM}\approx\tan^{-1}\!\frac{2\zeta}{\sqrt{-2\zeta^2+1}}$ | $\zeta≈0.7\Rightarrow\text{PM}≈65°$ |
| Q factor | $Q=1/(2\zeta)$ | $Q≈0.7$ (flat) |
| Miller effect | — | moves $p_1↓$, $p_2↑$ |

---

## 🧮 MATLAB Template — Stability & Phase Margin Analyzer

> [!code]- MATLAB Script
> ```matlab
> % ==========================================================
> % Stability & Phase-Margin Analyzer (Reusable Template)
> % ==========================================================
> clear; clc
> 
> % --- USER INPUT ---
> A0   = 1e4;           % DC open-loop gain
> beta = 0.01;          % Feedback factor
> wp1  = 2*pi*10;       % Dominant pole [rad/s]
> wp2  = 2*pi*1e6;      % Non-dominant pole [rad/s]
> 
> % --- TRANSFER FUNCTION ---
> s = tf('s');
> A  = A0 / ((1 + s/wp1)*(1 + s/wp2));
> L  = beta * A;
> 
> % --- MARGINS ---
> [Gm,Pm,Wcg,Wcp] = margin(L);
> 
> % --- DISPLAY RESULTS ---
> fprintf('Loop Gain βA0 = %.2f\n', beta*A0);
> fprintf('Phase Margin  = %.1f°  at  ω = %.1f rad/s\n', Pm, Wcp);
> fprintf('Gain Margin   = %.1f dB  at  ω = %.1f rad/s\n', 20*log10(Gm), Wcg);
> 
> % --- BODE & NYQUIST ---
> figure; margin(L); title('Loop Gain with Feedback');
> exportgraphics(gcf, 'C:\Users\Mads2\DTU\Obsidian\Resources\Quiz8_BodeMargin.png', 'Resolution', 300);
> 
> figure; nyquist(L); grid on; title('Nyquist Plot of L(jω)');
> exportgraphics(gcf, 'C:\Users\Mads2\DTU\Obsidian\Resources\Quiz8_Nyquist.png', 'Resolution', 300);
> 
> % --- OPTIONAL: Damping Ratio & Peaking ---
> zeta = sqrt(Pm/100);                % rough estimate
> Mp   = exp(-pi*zeta/sqrt(1-zeta^2));
> fprintf('Estimated Damping ζ = %.2f, Overshoot ≈ %.2f%%\n', zeta, 100*Mp);
> % ==========================================================
> ```

---

### 📊 MATLAB-Generated Stability Plots
![[Resources/Quiz8_BodeMargin.png|width=640]]  
![[Resources/Quiz8_Nyquist.png|width=640]]

---

> [!info] **Interpretation of the Results**
>
> **Bode Plot (top):**
> - The **magnitude** plot shows $|L(j\omega)|$ beginning flat (~40 dB) and rolling off at −20 dB/dec after the first pole ($\omega_p≈10$ rad/s).  
> - The **phase** falls smoothly to about −90°, typical for a single-pole system.  
> - The **unity-gain crossover** occurs at $6.3×10^3$ rad/s where MATLAB marks the **phase margin** $PM≈90.5°$.  
>   A 90° PM indicates a **first-order** (unconditionally stable) response.
>
> ---
>
> **Nyquist Plot (bottom):**
> - The blue curve shows $L(j\omega)$ in the complex plane.  
> - The red × marks the **critical point (-1, 0)**.  
> - Because the curve does **not encircle** this point, the system is **stable**.  
> - Its wide clearance from (−1, 0) signifies a **large phase margin** → negligible ringing or overshoot.
>
> ---
>
> **Damping Ratio & Overshoot:**
> - From $PM≈90°$, the estimated damping ratio is $\zeta≈0.95$ and overshoot $M_p≈0.01\%$.  
> - The step response is therefore **critically damped** — no oscillation or undershoot.
>
> ✅ **Conclusion:**  
> The amplifier demonstrates **robust stability** with a **dominant pole** and **wide bandwidth**, ideal for **voltage followers** or **buffer stages** requiring precise phase and fast settling.

---

> [!tip] **🧠 Key Takeaway — Design Insights**
>
> - **Phase Margin (PM):**  
>   - $PM>45°$ → stable  
>   - $PM≈60°$ → well-damped (fast + minimal overshoot)  
>   - $PM≈90°$ → extremely stable but less bandwidth gain  
>
> - **Tuning Stability:**  
>   - ↑$\beta$ → ↑bandwidth, ↓PM (less stable)  
>   - ↓$\beta$ → ↓bandwidth, ↑PM (more stable)  
>   - Lower $p_1$ or raise $p_2$ to increase PM (via **Miller compensation**).  
>
> - **Goal:**  
>   Balance **speed** and **stability**.  
>   For analog amplifiers, a PM of **60–75°** achieves fast transient response with clean settling.

---

> [!success] **💡 Practical Application**
>
> In CMOS op-amp design:
> - The **dominant pole** is set by the output resistance and compensation capacitance  
>   $$p_1 = \frac{1}{R_o C_c}$$  
> - Increasing $C_c$ improves stability (↑PM) but reduces bandwidth.  
> - Typical design targets:  
>   - $PM ≈ 60–70°$ for general-purpose amplifiers  
>   - $PM ≈ 45°$ for high-speed but lightly damped circuits  
>
> **Rule of thumb:**  
> - Every 10° decrease in PM roughly doubles overshoot.  
> - Miller compensation provides a practical way to keep the **dominant pole low** and ensure **predictable transient behavior**.
