# ⚙️ CMOS Op-Amp Fundamentals — Quiz 10 Derivations

> [!abstract] **Goal of This Quiz**  
> Understand the structure and operation of a **CMOS operational amplifier**, including  
> **input/output impedances**, **Miller compensation**, **gain stacking**, and how to compute  
> **$g_m$, $r_o$, $A_v$, and $V_{DS}$** in differential and cascaded stages.

---

> [!info] **Concept**  
> A typical CMOS Op-Amp consists of:
> - **Differential input pair** → very high input impedance  
> - **Common-source gain stage** → large intrinsic voltage gain  
> - **Common-drain (source follower)** → low output impedance  
>
> **Miller compensation ($C_c$)** provides stability by **splitting poles**:  
> - Dominant pole moves **down** in frequency  
> - Non-dominant pole moves **up**  
>
> **Core equations (long-channel, saturation)**  
> $$
> g_m \approx \frac{2I_D}{V_{OV}},\qquad
> r_o \approx \frac{|V_A|}{I_D},\qquad
> A_v^{CS} \approx g_m\bigl(r_{o,n}\parallel r_{o,p}\bigr)
> $$

---

> [!summary] **Question 1 — Input Impedance**
>
> **Question:** The input impedance of a CMOS Op-Amp is normally …  
>
> **Derivation**  
> MOS gates draw ~0 A DC current. The differential input pair presents essentially  
> **infinite resistance**, limited only by leakage and biasing networks.  
>
> ✅ **Answer:** *Very high.*

---

> [!summary] **Question 2 — Output Impedance**
>
> **Question:** The output impedance of a CMOS Op-Amp is often …  
>
> **Derivation**  
> Before the output buffer, the output node belongs to a **common-source** stage with  
> an **active load**. Its small-signal impedance is  
> $$
> R_{out} \approx r_{o,n} \parallel r_{o,p}
> $$
> typically tens of kΩ.  
>
> ✅ **Answer:** *High.*

---

> [!summary] **Question 3 — Miller Capacitor Effect**
>
> **Question:** In a CMOS Op-Amp, a Miller capacitor moves …  
>
> **Derivation**  
> A Miller capacitor between the high-gain node and the output feeds back a current  
> proportional to voltage difference, resulting in **pole splitting**:
> - Dominant pole: $p_1\downarrow$  
> - Non-dominant pole: $p_2\uparrow$  
>
> This dramatically increases phase margin and stabilizes the loop.  
>
> ✅ **Answer:** *The dominant pole down in frequency.*

---

> [!summary] **Question 4 — Overall Gain of a Two-Stage Op-Amp**
>
> **Question:** The gain of a CMOS Op-Amp built from a differential pair and a common-source stage is …  
>
> **Derivation**  
> A cascaded amplifier multiplies individual stage gains:
> $$
> A_v^{\text{total}}
> = A_v^{\text{diff}}
> \times
> A_v^{CS}
> $$
>
> The quiz explicitly refers to this cascade behavior.  
>
> ✅ **Answer:** *The product of the individual gains.*

---

> [!summary] **Question 5 — Output Resistance of Differential Stage (with Early Voltage)**
>
> **Question:** Given $|V_A|=20~\text{V}$ and $I_T=0.5~\text{mA}$, find $r_{out}$ at the single-ended output.  
>
> **Derivation**
>
> **Step 1 — Current per device**  
> Tail current splits equally:
> $$
> I_D = \frac{0.5~\text{mA}}{2} = 0.25~\text{mA}
> $$
>
> **Step 2 — Output resistance of each transistor**  
> Using the Early-voltage model:
> $$
> r_o = \frac{|V_A|}{I_D}
>     = \frac{20}{0.25\,\text{mA}}
>     = 80~\text{k}\Omega
> $$
>
> **Step 3 — Output node small-signal resistance**  
> One NMOS $r_o$ downward, one PMOS $r_o$ upward:
> $$
> r_{out} = r_{o,n}\parallel r_{o,p}
> = 80\parallel 80
> = 40~\text{k}\Omega
> $$
>
> ✅ **Answer:** $\boxed{40~\text{k}\Omega}$.

---

> [!summary] **Question 6 — Small-Signal Differential Gain**
>
> **Question:** With $V_{OV}=0.5\text{ V}$ and $I_D=0.25\text{ mA}$, find $A_v$.  
>
> **Derivation**  
> Compute transconductance:
> $$
> g_m\approx\frac{2I_D}{V_{OV}}
> =\frac{2(0.25\,\text{mA})}{0.5\,\text{V}}
> =1\,\text{mS}
> $$
> Use $r_{out}=40~\text{k}\Omega$ from Q5:
> $$
> A_v = g_m r_{out}
>     = 1\,\text{mS}\cdot40\,\text{k}\Omega
>     = 40~\text{V/V}
> $$
>
> *Note: The quiz refers to the **single-ended** gain, not differential double-ended gain.*  
>
> ✅ **Answer:** $\boxed{40~\text{V/V}}$.

---

> [!summary] **Question 7 — $V_{DS}$ of the NMOS Transistors**
>
> **Question:** With $|V_t|=0.5$ V and both inputs at 0 V, find $V_{DS}$.  
>
> **Derivation**  
> Overdrive of 0.5 V ⇒  
> $$
> V_{GS}=V_t+V_{OV}=1.0~\text{V}
> $$
> Source at approximately  
> $$
> V_S = 0 - 1 = -1~\text{V}
> $$
> PMOS mirror sets drain at  
> $$
> V_D \approx 3 - 1 = 2~\text{V}
> $$
> Therefore:
> $$
> V_{DS}=V_D - V_S = 2 - (-1) = 3~\text{V}
> $$
>
> ✅ **Answer:** $\boxed{3.0~\text{V}}$.

---

> [!summary] **Question 8 — Output Impedance with Final CD Stage**
>
> **Question:** The output impedance of a diff → CS → CD op-amp is approximately …  
>
> **Derivation**  
> The final stage is a **source follower**, whose output impedance is:
> $$
> R_{out}\approx\frac{1}{g_m}
> $$
> (small and load-friendly).  
>
> ✅ **Answer:** $\boxed{\tfrac{1}{g_m}\text{ from the common-drain stage}}$.

---

## 🧠 Summary Table

| Topic | Result / Formula | Note |
|---|---|---|
| Input impedance | **Very high** | MOS gates → $\approx\infty$ (DC) |
| Output impedance (open-loop CS) | $r_{o,n}\parallel r_{o,p}$ → **High** | ~40 kΩ in Q5 |
| Miller compensation | $p_1\downarrow,\;p_2\uparrow$ | Improves PM via pole-splitting |
| Stage combination | $A_v = \prod_i A_{v,i}$ | Cascaded gains multiply |
| $g_m$ | $g_m = 2I_D/V_{OV}$ | Long-channel saturation |
| $r_o$ | $r_o = |V_A|/I_D$ | Early effect |
| CS gain | $A_v^{CS} = g_m(r_{o,n}\parallel r_{o,p})$ | Basis for Q6 |
| CD output stage | $R_{out} \approx 1/g_m$ | Low output impedance |

---

> [!tip] **🧠 Key Takeaway — Op-Amp Design Insights**
>
> - **Input stage:** Diff pair → huge input resistance + good CMRR  
> - **Gain stage:** CS + active load → high gain, high $r_o$  
> - **Output stage:** CD → low $R_{out}$ for load drive  
> - **Compensation:** $C_c$ lowers $p_1$, raises $p_2$ → increases phase margin  
> - Keep transistors in saturation → ensure $V_{DS} > V_{OV}$ for all stages  

---

> [!success] **💡 Practical Application**
>
> In a two-stage CMOS Op-Amp:
> - Choose $C_c$ for a phase margin of 60–70°  
> - Ensure $A_v = g_m r_o$ is large enough for required open-loop gain  
> - Add source-follower if the load is low-impedance  
> - Check headroom across all devices  
>
> These principles map directly to OTA design, Gm-C filters, and precision CMOS analog circuits.
