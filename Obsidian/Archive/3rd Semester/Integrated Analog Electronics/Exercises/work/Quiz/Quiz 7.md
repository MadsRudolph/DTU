# ⚙️ Feedback Amplifier Analysis — Quiz 7 Derivations

> [!abstract] **Goal of This Quiz**
> Understand how **negative feedback** shapes amplifier behavior:  
> how it sets **closed-loop gain**, modifies **input/output resistances**,  
> expands **bandwidth**, and reduces **sensitivity** to parameter variation.

---

> [!info] **Concept**
> Negative feedback in amplifiers:
>
> - **Reduces gain sensitivity** to component variation  
> - **Improves bandwidth** by a factor of $(1+\beta A)$  
> - **Modifies resistances**:
>   - Series mixing → ↑ input resistance  
>   - Shunt mixing → ↓ input resistance  
>   - Series sampling → ↑ output resistance  
>   - Shunt sampling → ↓ output resistance  
>
> ✅ **Positive effect:** smoother, predictable response  
> ⚠️ **Trade-off:** reduced overall gain  
> ❌ **Too little feedback:** unstable or nonlinear behavior
>
> **Key Equations**
> $$
> A_{CL} = \frac{A}{1+\beta A}, \qquad
> L = \beta A, \qquad
> S = \frac{1}{1+\beta A}
> $$
> where $A$ = open-loop gain, $\beta$ = feedback factor, $L$ = loop gain, and $S$ = gain sensitivity.

---

> [!summary] **Question 1 — Closed-Loop Gain**
>
> **Given**  
> Amplifier gain $A$ and feedback factor $\beta$  
>
> **Formula**
> $$
> A_{CL} = \frac{A}{1+\beta A}
> $$
>
> ✅ **Conclusion:**  
> The closed-loop gain for a negative-feedback amplifier is  
> $\boxed{A_{CL} = \frac{A}{1+\beta A}}$

---

> [!summary] **Question 2 — Loop Gain**
>
> The **loop gain** is defined as the product of amplifier gain and feedback factor:
> $$
> L = \beta A
> $$
>
> ✅ **Conclusion:**  
> $\boxed{L = \beta A}$

---

> [!summary] **Question 3 — Sensitivity Reduction**
>
> Feedback reduces how much the closed-loop gain changes with variations in $A$:
> $$
> S = \frac{\partial A_{CL}/A_{CL}}{\partial A/A} = \frac{1}{1+\beta A}
> $$
> Hence, the system becomes less sensitive to amplifier parameter drift.
>
> ✅ **Conclusion:**  
> The sensitivity is **lowered** by a factor of $(1+\beta A)$.

---

> [!summary] **Question 4 — Low-Frequency Closed-Loop Gain**
>
> **Given**  
> $A_0 = 10$, $\beta = 0.1$
>
> **Formula**
> $$
> A_{CL} = \frac{A_0}{1+\beta A_0}
> $$
>
> **Calculation**
> $$
> A_{CL} = \frac{10}{1+(0.1)(10)} = 5~\mathrm{V/V}
> $$
>
> ✅ **Answer:**  
> $\boxed{A_{CL}=5~\mathrm{V/V}}$

---

> [!summary] **Question 5 — Feedback Bandwidth**
>
> Feedback increases the bandwidth by $(1+\beta A_0)$:
> $$
> f_{CL} = f_0(1+\beta A_0)
> $$
>
> **Given**  
> $f_0=1.59~\mathrm{kHz}$, $A_0=10$, $\beta=0.2$
>
> **Calculation**
> $$
> f_{CL}=1.59~\mathrm{kHz}\times(1+2)=4.77~\mathrm{kHz}\approx4.8~\mathrm{kHz}
> $$
>
> ✅ **Answer:**  
> $\boxed{f_{CL}\approx4.8~\text{kHz}}$

---

> [!summary] **Question 6 — Input Resistance with Feedback**
>
> For a **series–shunt feedback amplifier**:
> $$
> R_{in,CL}=R_{in}(1+\beta A)
> $$
>
> **Given**  
> $R_{in}=5~\text{k}\Omega$, $\beta A=1$
>
> **Calculation**
> $$
> R_{in,CL}=5~\text{k}\Omega\times2=10~\text{k}\Omega
> $$
>
> ✅ **Answer:**  
> $\boxed{R_{in,CL}=10~\text{k}\Omega}$

---

> [!summary] **Question 7 — Output Resistance with Feedback**
>
> In series–shunt feedback, output resistance decreases:
> $$
> R_{out,CL}=\frac{R_{out}}{1+\beta A}
> $$
>
> **Given**  
> $R_{out}=2~\text{k}\Omega$, $\beta A=1$
>
> **Calculation**
> $$
> R_{out,CL}=\frac{2000}{2}=1000~\Omega
> $$
>
> ✅ **Answer:**  
> $\boxed{R_{out,CL}=1~\text{k}\Omega}$

---

> [!summary] **Question 8 — Series–Series Feedback**
>
> For **series–series feedback**:
> - The **input** connection is **series**, increasing $R_{in}$  
> - The **output** sampling is **series**, increasing $R_{out}$  
>
> ✅ **Answer:**  
> $\boxed{\text{Input resistance increases}}$

---

## 🧠 Summary of Feedback Relationships

| Parameter | Formula | Effect |
|-----------|---------|--------|
| Voltage Gain | $A_{CL}=\dfrac{A}{1+\beta A}$ | ↓ reduced |
| Loop Gain | $L=\beta A$ | sets accuracy/stability |
| Input Resistance (series) | $R_{in,CL}=(1+\beta A)R_{in}$ | ↑ increased |
| Output Resistance (shunt) | $R_{out,CL}=\dfrac{R_{out}}{1+\beta A}$ | ↓ decreased |
| Bandwidth | $f_{CL}=(1+\beta A_0)f_0$ | ↑ increased |
| Sensitivity | $S=\dfrac{1}{1+\beta A}$ | ↓ decreased |

---

## 🧮 MATLAB Template — Feedback Amplifier Calculator

> [!code]- MATLAB Script
> ```matlab
> % ==========================================================
> % Feedback Amplifier Calculator (Reusable Template)
> % ==========================================================
> clear; clc
> 
> % --- USER INPUT ---
> A0   = 10;        % Open-loop gain
> beta = 0.1;       % Feedback factor
> f0   = 1.59e3;    % Original -3dB frequency [Hz]
> Rin  = 5e3;       % Input resistance [ohm]
> Rout = 2e3;       % Output resistance [ohm]
> 
> % --- DERIVED VALUES ---
> LoopGain = beta * A0;
> ACL      = A0 / (1 + LoopGain);
> fCL      = f0 * (1 + LoopGain);
> Rin_CL   = Rin * (1 + LoopGain);
> Rout_CL  = Rout / (1 + LoopGain);
> Sens     = 1 / (1 + LoopGain);
> 
> % --- DISPLAY RESULTS ---
> fprintf('--- FEEDBACK AMPLIFIER RESULTS ---\n');
> fprintf('Loop Gain (βA)      = %.2f\n', LoopGain);
> fprintf('Closed-loop Gain    = %.2f V/V\n', ACL);
> fprintf('Bandwidth (Hz)      = %.1f\n', fCL);
> fprintf('Input Resistance    = %.0f Ω\n', Rin_CL);
> fprintf('Output Resistance   = %.0f Ω\n', Rout_CL);
> fprintf('Gain Sensitivity    = %.3f\n', Sens);
> 
> % --- CHECK Q5–Q7 VALUES ---
> if abs(beta-0.2)<1e-6
>     fprintf('\nFor β=0.2, f_CL = %.1f kHz\n', fCL/1e3);
> end
> % ==========================================================
> ```

---

> [!tip] **🧠 Key Takeaway — Design Insights**
>
> - **Loop gain ($\beta A$)** controls both **accuracy** and **stability**.  
> - Large $\beta A$ → accurate, wide-band but lower raw gain.  
> - Small $\beta A$ → higher gain but poorer linearity and bandwidth.  
> - For precision amplifiers, aim for $\beta A \gg 1$ so $A_{CL}\approx 1/\beta$ and relative error $\approx 1/(1+\beta A)$.
> - Feedback topology (series–shunt, shunt–series, etc.) determines how input/output impedances change.

---

> [!success] **💡 Practical Application**
>
> In CMOS op-amp stages, use feedback to set **closed-loop voltage gain** while device sizing sets open-loop $A$.  
> Maintaining $\beta A > 20$ typically ensures **linear, low-distortion operation** and **predictable bandwidth**.  
> Combine with **compensation** (if needed) to preserve adequate phase margin in higher-order designs.
