# ⚙️ CMOS Op-Amp Fundamentals — Quiz 10 Derivations

> [!abstract] **Goal of This Quiz**  
> Understand the structure and operation of a **CMOS operational amplifier**, including its  
> **input and output impedances**, **Miller compensation**, **gain stacking**, and how to compute  
> **$g_m$, $r_o$, $A_v$, and $V_{DS}$** for differential and cascaded stages.

---

> [!info] **Concept**  
> A typical CMOS Op-Amp consists of:
> - **Differential input pair** → high input impedance  
> - **Common-source gain stage** → large voltage gain  
> - **Common-drain (source-follower)** → low output impedance for load drive  
>
> **Miller compensation ($C_c$)** introduces *pole splitting*: dominant pole ↓, non-dominant pole ↑, ensuring phase-margin stability.  
>
> **Key relations (saturation region)**  
> $$
> g_m \approx \frac{2I_D}{V_{OV}}, \qquad 
> r_o \approx \frac{|V_A|}{I_D}, \qquad 
> A_v^{CS} \approx g_m(r_{o,n}\parallel r_{o,p})
> $$

---

> [!summary] **Question 1 — Input Impedance**
>
> **Question:** The input impedance of a CMOS Op-Amp is normally …  
>
> **Derivation**  
> The differential pair uses MOSFET gates as inputs, and since the gate current ≈ 0 A,  
> the input resistance is extremely high (limited only by bias/leakage paths).  
>
> ✅ **Answer:** *Very high.*

---

> [!summary] **Question 2 — Output Impedance**
>
> **Question:** The output impedance of a CMOS Op-Amp is often …  
>
> **Derivation**  
> The open-loop output node belongs to a **common-source** stage with an **active-load** mirror.  
> Its small-signal resistance is:
> $$
> R_{out} \approx r_{o,n}\parallel r_{o,p}
> $$
> which is typically **tens of kΩ**, i.e. high.  
>
> ✅ **Answer:** *High.*

---

> [!summary] **Question 3 — Miller Capacitor Effect**
>
> **Question:** In a CMOS Op-Amp, a Miller capacitor moves …  
>
> **Derivation**  
> $C_c$ provides frequency compensation by feeding output back to the high-gain node.  
> It **splits** the poles so that  
> - The **dominant pole** moves **down** in frequency ($p_1↓$)  
> - The **non-dominant pole** moves **up** ($p_2↑$)  
>
> Result → larger phase margin and stable closed-loop response.  
>
> ✅ **Answer:** *The dominant pole down in frequency.*

---

> [!summary] **Question 4 — Overall Gain of a Two-Stage Op-Amp**
>
> **Question:** The gain of a CMOS Op-Amp built from a differential pair and a common-source stage is …  
>
> **Derivation**  
> Each stage contributes its small-signal voltage gain; in cascade, total gain multiplies:  
> $$
> A_v^{\text{total}} = A_v^{\text{diff}} \times A_v^{CS}
> $$
>
> ✅ **Answer:** *The product of the gain for the individual stages.*

---

> [!summary] **Question 5 — Output Resistance of Differential Stage**
>
> **Question:** For the given circuit with $|V_A|=20$ V and $I_T=0.5$ mA, find $r_{out}$.  
>
> **Derivation**
> - Each transistor carries $I_D=I_T/2=0.25$ mA.  
> - Each has $r_o=|V_A|/I_D=20/0.25$ mA = 80 kΩ.  
> - Output node sees $r_{out}=r_{o,n}\parallel r_{o,p}=80\parallel80$ kΩ = 40 kΩ.  
>
> ✅ **Answer:** $\boxed{r_{out}=40~\text{k}\Omega}$.

---

> [!summary] **Question 6 — Small-Signal Differential Gain**
>
> **Question:** With $V_{OV}=0.5$ V and $I_D=0.25$ mA per side, find $A_v$.  
>
> **Derivation**
> $$
> g_m \approx \frac{2I_D}{V_{OV}}=\frac{2(0.25\,\text{mA})}{0.5\,\text{V}}=1\,\text{mS}
> $$
> Using $r_{out}=40$ kΩ (from Q5):  
> $$
> A_v = g_m r_{out} = 1\,\text{mS}\times40\,\text{k}\Omega = 40\,\text{V/V}
> $$
>
> ✅ **Answer:** $\boxed{A_v\approx40~\text{V/V}}$.

---

> [!summary] **Question 7 — $V_{DS}$ of the NMOS Transistors**
>
> **Question:** Assume $|V_t|=0.5$ V and $V_{IN1}=V_{IN2}=0$. Find $V_{DS}$ for the NMOS pair.  
>
> **Derivation**  
> For $V_{OV}=0.5$ V → $V_{GS}=V_t+V_{OV}=1.0$ V.  
> Source node ≈ −1 V (0 − 1 V).  
> PMOS current mirror ($V_{SG}=1$ V) → drain node ≈ $3 − 1 = 2$ V.  
> Therefore  
> $$
> V_{DS}=V_D−V_S=2−(−1)=3~\text{V}
> $$
>
> ✅ **Answer:** $\boxed{V_{DS}=3.0~\text{V}}$.

---

> [!summary] **Question 8 — Output Impedance with Final CD Stage**
>
> **Question:** The output impedance of a three-stage Op-Amp (diff pair → CS → CD) is approximately …  
>
> **Derivation**  
> The final **common-drain** (source-follower) stage lowers output impedance to:  
> $$
> R_{out}\approx\frac{1}{g_m}
> $$
> providing strong drive capability for external loads.  
>
> ✅ **Answer:** $\boxed{\tfrac{1}{g_m}\text{ from the common-drain stage}}$.

---

## 🧠 Summary Table

| Topic | Result / Formula | Note |
|---|---|---|
| Input impedance | **Very high** | MOS gate → $\approx\infty$ (DC) |
| Output impedance (open-loop CS) | $r_{o,n}\parallel r_{o,p}$ → **High** | Here $40~\text{k}\Omega$ |
| Miller compensation | $p_1\!\downarrow,\;p_2\!\uparrow$ | Increases PM via pole-splitting |
| Stage combination | $A_v^{\text{total}}=\prod_i A_{v,i}$ | Cascaded gains multiply |
| $g_m$ (sat.) | $g_m\approx\dfrac{2I_D}{V_{OV}}$ | Long-channel model |
| $r_o$ | $r_o\approx\dfrac{|V_A|}{I_D}$ | Early effect |
| CS gain | $A_v^{CS}\approx g_m(r_{o,n}\parallel r_{o,p})$ | Used in Q6 |
| Output with CD stage | $R_{out}\approx\dfrac{1}{g_m}$ | Low-Z driver |

---

> [!tip] **🧠 Key Takeaway — Op-Amp Design Insights**
>
> - **Input stage:** Diff-pair → very high $R_{in}$, sets CMRR.  
> - **Gain stage:** CS + active load → dominant $A_v$ and high $R_{out}$.  
> - **Output stage:** CD → low $R_{out}$ ≈ $1/g_m$ for driving loads.  
> - **Compensation:** Add $C_c$ → $p_1$ down, $p_2$ up → ↑ phase margin and stability.  
> - **Rule of thumb:** Bias for $V_{DS}>V_{OV}$ to maintain saturation and linearity.

---

> [!success] **💡 Practical Application**
>
> In a two-stage CMOS Op-Amp:
> - Choose $C_c$ for target PM (≈ 60–70°).  
> - Set $g_m r_o$ product for desired open-loop gain.  
> - Add a source-follower if $R_L$ is low.  
> - Check headroom so both NMOS and PMOS stay in saturation (typ. $V_O≈2$ V in this quiz).  
> These principles apply directly to two-stage OTA and fully-differential amplifier designs.
