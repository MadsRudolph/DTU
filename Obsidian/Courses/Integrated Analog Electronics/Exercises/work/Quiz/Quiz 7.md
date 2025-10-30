#  Feedback Amplifier Analysis

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
> The general closed-loop gain relation:
> $$
> A_{CL} = \frac{A}{1+\beta A}
> $$
> where  
> $A$ = open-loop gain, $\beta$ = feedback factor, and $(1+\beta A)$ = loop gain.

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

## 🧠 Feedback Amplifier Formula Summary

| Parameter | Without Feedback | With Feedback | Effect |
|------------|------------------|----------------|---------|
| Voltage Gain | $A$ | $\dfrac{A}{1+\beta A}$ | ↓ reduced |
| Input Resistance (series) | $R_i$ | $(1+\beta A)R_i$ | ↑ increased |
| Output Resistance (shunt) | $R_o$ | $\dfrac{R_o}{1+\beta A}$ | ↓ decreased |
| Bandwidth | $f_0$ | $(1+\beta A)f_0$ | ↑ increased |
| Sensitivity | 1 | $\dfrac{1}{1+\beta A}$ | ↓ decreased |

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

