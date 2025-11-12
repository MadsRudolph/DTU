# ⚙️ Differential Pair Fundamentals — Quiz 9 Derivations

> [!abstract] **Goal of This Quiz**  
> Understand the behavior of a **differential amplifier**, distinguishing between  
> **differential** and **common-mode** signals, and relate its gain structure  
> to basic transistor amplifier topologies.

---

> [!info] **Concept**  
> A **differential pair** amplifies the *difference* between two input voltages while rejecting any voltage that is *common* to both.  
> 
> Definitions:  
> $$
> v_{id} = v_{in1} - v_{in2}, \qquad  
> v_{icm} = \frac{v_{in1} + v_{in2}}{2}
> $$
>  
> The ideal differential amplifier output is  
> $$
> v_o = A_d\,v_{id} + A_{cm}\,v_{icm}
> $$
> where $A_d$ is the differential gain and $A_{cm}$ the common-mode gain.  
> Ideally $A_{cm}=0$, meaning *perfect common-mode rejection*.

---

> [!summary] **Question 1 — Common-Mode Input Voltage**  
> **Question:** The common-mode input voltage to a differential stage is …  
> 
> **Derivation**  
> The common-mode voltage is the *average* of the two input voltages, i.e. the part that is **common to both inputs**.  
> $$
> v_{icm} = \frac{v_{in1}+v_{in2}}{2}
> $$  
> It shifts both transistor inputs equally and does *not* affect the differential current (ideally).  
> 
> ✅ **Answer:** *Common for both pins.*

---

> [!summary] **Question 2 — Differential Gain Definition**  
> **Question:** The differential gain of a differential stage is …  
> 
> **Derivation**  
> The output depends on the *difference* between the two input voltages:  
> $$
> A_d = \frac{v_o}{v_{in1}-v_{in2}}
> $$  
> This expresses how effectively the circuit amplifies only the differential component.  
> 
> ✅ **Answer:** *$v_o / (v_{in1} - v_{in2})$.*

---

> [!summary] **Question 3 — Common-Mode Output Dependence**  
> **Question:** For an ideal differential stage, the common-mode output voltage depends …  
> 
> **Derivation**  
> In an ideal differential pair, the two sides are perfectly matched, so any common-mode input produces equal changes that cancel in the differential output.  
> Only the *common-mode input* can shift the output baseline (through bias conditions).  
> 
> ✅ **Answer:** *Only on the common-mode input voltage.*

---

> [!summary] **Question 4 — Differential Gain Type**  
> **Question:** An NMOS differential pair with PMOS active load (current mirror, single-ended output) has a differential voltage gain …  
> 
> **Derivation**  
> The small-signal equivalent of one side is a **common-source amplifier** with load resistance ≈ $r_{oN}\parallel r_{oP}$.  
> The differential gain is  
> $$
> A_d \approx -g_m\,(r_{oN}\parallel r_{oP})
> $$
> which is similar in magnitude and sign to a single-transistor **common-source** stage.  
> 
> ✅ **Answer:** *Almost equal to a single-transistor common-source amplifier.*

---

> [!summary] **Question 5 — Transconductance of Each Transistor**  
> **Given**  
> - Tail current: $I_T = 1.0\,\text{mA}\Rightarrow I_D \approx I_T/2 = 0.5\,\text{mA}$ per side (quiescent, symmetric).  
> - Overdrive: $V_{OV}=V_{GS}-V_{t0}=0.25\,\text{V}$.
>
> **Derivation**  
> Long-channel MOS in saturation:  
> $$
> g_m \approx \frac{2I_D}{V_{OV}}
> = \frac{2\cdot 0.5\,\text{mA}}{0.25\,\text{V}}
> = \frac{1.0\,\text{mA}}{0.25\,\text{V}}
> = 4.0\,\frac{\text{mA}}{\text{V}}
> $$
>
> ✅ **Answer:** $g_m = 4.0~\text{mA/V}$.

---

> [!summary] **Question 6 — Quiescent Output Voltages**  
> **Given**  
> - Each drain load: $R_D=6\,\text{k}\Omega$ tied to $+3\,\text{V}$.  
> - $I_D=0.5\,\text{mA}$ per side.
>
> **Derivation**  
> Voltage drop on each resistor:  
> $\Delta V = I_D R_D = 0.5\,\text{mA}\cdot 6\,\text{k}\Omega = 3\,\text{V}$  
> Node at the top is $+3\text{ V}$, so drain (output) sits at  
> $V_O = 3\text{ V} - 3\text{ V} = 0\text{ V}$ (both sides, by symmetry).
>
> ✅ **Answer:** $V_{O1}=V_{O2}=0~\text{V}$.

---

> [!summary] **Question 7 — Differential Gain**  
> **Assumption (standard small-signal):** ignore $r_o$, matched devices, differential input; single-ended gain per side is  
> $|A_{v,se}| \approx g_m R_D$.
>
> **Compute**  
> $g_m R_D = (4\,\text{mA/V})(6\,\text{k}\Omega)=24~\text{V/V}$.
>
> ⚠️ **Note:** True **differential output** $v_{od}=v_{o1}-v_{o2}$ would be $|A_{v,dd}|\approx 2g_mR_D$ (≈48 V/V). Since 48 isn’t an option, the question is clearly using the **single-ended** magnitude.
>
> ✅ **Answer:** **24**

---

> [!summary] **Question 8 — Harmonic Distortion of Differential Circuits**  
> **Concept**  
> A symmetric differential pair cancels **even-order** nonlinear terms; THD is typically **lower** than a comparable single-ended common-source stage (which doesn’t cancel even harmonics).
>
> ✅ **Answer:** *Lower than the harmonic distortion in a common-source stage.*

---

> [!tip] **🧠 Key Takeaway — Differential Pair Insights**  
> - Differential input: $v_{id}=v_{in1}-v_{in2}$  
> - Common-mode input: $v_{icm}=(v_{in1}+v_{in2})/2$  
> - Ideal pair rejects $v_{icm}$ (CMRR → ∞)  
> - NMOS diff-pair + PMOS mirror load ≈ high-gain, single-ended **common-source** output  
> - Differential structure → reduced harmonic distortion & better linearity
