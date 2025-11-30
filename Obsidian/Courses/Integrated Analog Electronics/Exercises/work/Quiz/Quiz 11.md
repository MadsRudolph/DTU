# ⚙️ Slew Rate, PSR & CM Range — Quiz 11 Derivations

> [!abstract] **Goal of This Quiz**  
> Understand dynamic and bias limits of a **two-stage CMOS op-amp**:
> - **Slew rate (SR)** as a large-signal limit  
> - How **current sources** and the **Miller capacitor** set SR  
> - **Power supply rejection (PSR)** definition  
> - **Common-mode input range (CMIR)** of an NMOS differential pair with PMOS loads and how **body effect** shifts it.

---

> [!info] **Core Concepts**
>
> - **Slew rate (SR)** for a Miller-compensated op-amp:
>   $$
>   \text{SR} = \frac{I_{\text{CHG/DIS}}}{C_c}
>   $$
>   where $I_{\text{CHG/DIS}}$ is the **maximum current** that the first stage can push into / pull from $C_c$.  
>   This is a **large-signal effect** (current source hits its limit).
>
> - **Common-mode input range** for an NMOS input pair with PMOS loads:
>   - **Lower limit** typically set by keeping the **tail NMOS** in saturation.  
>   - **Upper limit** often set by keeping the **PMOS loads** and **input NMOS** in saturation.
>
> - **Power supply rejection (PSR)** (single-supply view):
>   $$
>   \text{PSR} = \frac{\Delta V_{\text{out}}}{\Delta V_{DD}}
>   $$
>   Smaller PSR magnitude = better rejection (often quoted in dB as PSRR).

---

> [!summary] **Question 1 — Nature of Slew Rate Limitation**
>
> **Question:**  
> In the standard two-stage CMOS op-amp, the slew rate is normally:
>
> - A large signal problem  
> - A small signal problem  
> - Does not depend on the signal amplitude  
>
> **Derivation**
>
> When a large step is applied at the input, the first gain stage drives the Miller capacitor $C_c$.  
> For sufficiently large input steps, the stage saturates and the current is **clamped** at the bias current of the relevant current source:
> $$
> I_{\text{CHG/DIS}} \approx I_{\text{bias,max}}
> $$
> so the output slope is limited to:
> $$
> \text{SR} = \frac{d v_{\text{out}}}{dt} \approx \frac{I_{\text{bias,max}}}{C_c}
> $$
> This limitation only appears for **large signal swings** when the current source saturates. In the **small-signal** regime the response is linear and determined by poles/zeros instead.
>
> ✅ **Answer:** *A large signal problem.*

---

> [!summary] **Question 2 — Physical Cause of Slew Rate**
>
> **Question:**  
> Slew rate is normally caused by:
>
> - Current source transistors limits the charge / discharge current  
> - Voltage source transistors limits the charge / discharge current  
> - A too large bulk current  
>
> **Derivation**
>
> In a two-stage CMOS op-amp:
> - The first stage is usually a differential pair feeding a node with the compensation capacitor $C_c$.  
> - Positive steps drive one transistor on and the other off; the tail/current-mirror **current sources** define the **maximum current** available to charge or discharge $C_c$.  
>
> Thus the max $I$ into $C_c$ is set by **current source transistors**, so they directly determine SR:
> $$
> \text{SR} = \frac{I_{\text{current source}}}{C_c}.
> $$
>
> ✅ **Answer:** *Current source transistors limits the charge / discharge current.*

---

> [!summary] **Question 3 — Location of the Miller Capacitor**
>
> **Question:**  
> The Miller compensation capacitor in the two-stage op-amp is placed:
>
> - Between input and output of the second gain stage  
> - Between ground and input of the second gain stage  
> - Between ground and output of the second gain stage  
>
> **Derivation**
>
> In the classical two-stage CMOS op-amp:
> - Stage 1: differential pair → node $v_1$  
> - Stage 2: common-source gain stage → output node $v_o$  
> - The Miller capacitor $C_c$ is connected **between $v_1$ and $v_o$**.
>
> This creates a Miller effect: $C_c$ appears as an enlarged capacitance at $v_1$ and **splits poles**, giving a low-frequency dominant pole and pushing the high-frequency pole upward.
>
> ✅ **Answer:** *Between input and output of the second gain stage.*

---

> [!summary] **Question 4 — Definition of Power Supply Rejection**
>
> **Question:**  
> Power supply rejection is defined as:
>
> - Change in supply voltage (Vdd) divided by change in Vout  
> - Change in supply current (Idd) divided by change in Vout  
> - Change in Vout divided by change in supply voltage (Vdd)  
>
> **Derivation**
>
> For small variations in supply $V_{DD}$, power-supply rejection (PSR) is the **transfer** from supply to output:
> $$
> \text{PSR} = \frac{\Delta V_{\text{out}}}{\Delta V_{DD}}
> $$
> A **smaller** $|\text{PSR}|$ means **better** rejection (less of the supply noise appears at the output). Often the inverse is taken and expressed in dB as PSRR, but here the statement uses the direct PSR definition.
>
> ✅ **Answer:** *Change in Vout divided by change in supply voltage (Vdd).*

---

> [!summary] **Question 5 — Minimum Common-Mode Input Voltage**
>
> **Question:**  
> For the shown NMOS-input differential pair with PMOS loads and an NMOS tail source (supplies at $+3$ V and $-3$ V), assuming all transistors have
> $$
> |V_t| = 0.4~\text{V},\qquad |V_{GS}| = 1.0~\text{V},
> $$
> find the **minimum** common-mode input voltage $V_{\text{CM,min}}$ such that all transistors remain in saturation.
>
> **Step 1 — Overdrive voltage**
>
> For both NMOS and PMOS:
> $$
> V_{OV} = |V_{GS}| - |V_t| = 1.0 - 0.4 = 0.6~\text{V}.
> $$
>
> **Step 2 — Lower limit usually from the tail NMOS**
>
> Let $V_{\text{CM}}$ be the input common-mode voltage.  
> Input NMOS source node:
> $$
> V_S = V_{\text{CM}} - V_{GS} = V_{\text{CM}} - 1.0.
> $$
>
> The **tail NMOS** has drain at $V_S$ and source at $-3$ V.  
> For saturation:
> $$
> V_{DS,\text{tail}} = V_S - (-3) = V_S + 3 \ge V_{OV} = 0.6.
> $$
> Substitute $V_S$:
> $$
> (V_{\text{CM}} - 1.0) + 3 \ge 0.6
> \Rightarrow V_{\text{CM}} + 2.0 \ge 0.6
> \Rightarrow V_{\text{CM}} \ge -1.4~\text{V}.
> $$
>
> For this $V_{\text{CM}}$, the input NMOS and PMOS loads still have enough $V_{DS}$ headroom, so the tail device is the limiting factor.
>
> ✅ **Answer:** *$V_{\text{CM,min}} = -1.4~\text{V}$.*

---

> [!summary] **Question 6 — Maximum Common-Mode Input Voltage (No Bulk Effect)**
>
> **Question:**  
> For the same circuit, find the **maximum** common-mode input voltage $V_{\text{CM,max}}$ while keeping all transistors in saturation (no bulk effect yet).
>
> **Step 1 — PMOS load saturation**
>
> PMOS sources at $+3$ V, drains at output $V_O$.  
> For PMOS saturation:
> $$
> V_{SD,p} = 3 - V_O \ge V_{OV,p} = 0.6
> \Rightarrow V_O \le 2.4~\text{V}.
> $$
>
> **Step 2 — Input NMOS saturation**
>
> Input NMOS drains at $V_O$, sources at
> $$
> V_S = V_{\text{CM}} - 1.0.
> $$
> For NMOS saturation:
> $$
> V_{DS,n} = V_O - V_S \ge V_{OV,n} = 0.6
> \Rightarrow V_O \ge V_S + 0.6 = (V_{\text{CM}} - 1.0) + 0.6 = V_{\text{CM}} - 0.4.
> $$
>
> **Step 3 — Combine inequalities**
>
> $$
> V_{\text{CM}} - 0.4 \le V_O \le 2.4
> \Rightarrow V_{\text{CM}} - 0.4 \le 2.4
> \Rightarrow V_{\text{CM}} \le 2.8~\text{V}.
> $$
>
> ✅ **Answer:** *$V_{\text{CM,max}} \approx 2.8~\text{V}$.*

---

> [!summary] **Question 7 — Maximum Common-Mode Input with Bulk Effect**
>
> **Question:**  
> Now assume the **bulk contacts of the input NMOS** are connected to the **negative supply** ($-3$ V) instead of to their sources, and that the body effect increases $|V_t|$ by $0.1$ V.  
> Find the new $V_{\text{CM,max}}$ with all transistors in saturation.
>
> **Step 1 — New threshold and overdrive for input NMOS**
>
> $$
> |V_t'| = 0.4 + 0.1 = 0.5~\text{V},\qquad
> V_{OV,n}' = V_{GS} - |V_t'| = 1.0 - 0.5 = 0.5~\text{V}.
> $$
>
> **Step 2 — PMOS saturation constraint (unchanged)**
>
> $$
> V_O \le 3 - V_{OV,p} = 3 - 0.6 = 2.4~\text{V}.
> $$
>
> **Step 3 — New NMOS saturation constraint**
>
> $$
> V_{DS,n} = V_O - V_S \ge V_{OV,n}' = 0.5
> \Rightarrow V_O \ge V_S + 0.5
> = (V_{\text{CM}} - 1.0) + 0.5
> = V_{\text{CM}} - 0.5.
> $$
>
> Combine:
> $$
> V_{\text{CM}} - 0.5 \le V_O \le 2.4
> \Rightarrow V_{\text{CM}} \le 2.9~\text{V}.
> $$
>
> The closest multiple-choice option is **$3.0$ V**.
>
> ✅ **Answer:** *$V_{\text{CM,max}} \approx 3.0~\text{V}$ (with body effect).*

---

## 🧠 Summary Table

| Topic | Relation / Result | Comment |
|---|---|---|
| Slew rate | $\text{SR} = I_{\text{CHG/DIS}}/C_c$ | Large-signal limit (current sources) |
| Cause of SR | Limited current from bias/current-source transistors | Sets max dv/dt on $C_c$ |
| Miller compensation | $C_c$ between stage-2 input and output | Splits poles: $p_1\downarrow,\;p_2\uparrow$ |
| PSR definition | $\text{PSR} = \Delta V_{\text{out}} / \Delta V_{DD}$ | Smaller PSR ⇒ better rejection |
| CMIR (low end) | $V_{\text{CM,min}}$ from tail NMOS: $V_S + 3 \ge V_{OV}$ | Here: $-1.4$ V |
| CMIR (high end, no body) | $V_{\text{CM,max}}$ s.t. $V_O \le 3 - V_{OV,p}$ and $V_O \ge V_{\text{CM}} - 0.4$ | Here: $2.8$ V |
| CMIR (with body effect) | Increased $V_t$ ⇒ smaller $V_{OV,n}$ ⇒ slightly higher $V_{\text{CM,max}}$ | Here: $\sim 3.0$ V |

---

> [!tip] **Key Design Insights**
>
> - **SR is a large-signal limit**: improve it by increasing bias currents or reducing $C_c$ (while keeping stability).  
> - **CMIR is set by headroom** of the input devices, tail source, and loads — always check **all** devices for saturation.  
> - **Body effect** raises $V_t$ and shifts CMIR; tying bulk to source removes this penalty but may not be layout-feasible.  
> - **Good PSR** keeps supply noise from corrupting the output; cascode biasing and differential architectures help.

