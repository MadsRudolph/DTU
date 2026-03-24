# ⚡ Current Mirrors & References — Quiz 12 Derivations

> [!abstract] **Goal of This Quiz**  
> Work with **CMOS current mirrors and bias circuits**, including:
> - Setting bias currents via $R_B$ and $V_{\text{eff}}$
> - Ensuring mirror transistors stay in **saturation**
> - Understanding **W/L scaling** ($N$) and how it affects $I_D$ and $g_m$
> - Recognizing swing limits of **cascode mirrors**
> - Understanding the temperature behavior of a **bandgap reference**

---

> [!info] **Core MOSFET Relations (long-channel, saturation)**
>
> - Overdrive: $V_{OV} = V_{GS} - V_t$
> - Drain current:
>   $$
>   I_D = \frac{1}{2}k'\frac{W}{L}V_{OV}^2
>   $$
> - If two devices share the same $V_{GS}$:
>   $$
>   \frac{I_{D2}}{I_{D1}} = \frac{(W/L)_2}{(W/L)_1} = N
>   $$
> - Transconductance:
>   $$
>   g_m \approx \frac{2I_D}{V_{OV}}
>   $$

---

## Question 1 — Bias Current $I_1$ with $R_B$
![[quiz12_1.png|400]]
> **Question:**  
> For the circuit with $V_{DD}=3~\text{V}$, $V_t=1.0~\text{V}$, and effective gate voltage $V_{eff}=V_{OV}=0.3~\text{V}$, find the current $I_1$ when $R_B=1.7~\text{k}\Omega$.

**Idea**

Q1 is **diode-connected** and biased through $R_B$:

- Gate and drain of $Q_1$ are tied together.
- $V_{GS1} = V_t + V_{OV} = 1.0 + 0.3 = 1.3~\text{V}$.
- The node at gate/drain sits at $V_{G1}=1.3~\text{V}$.
- $R_B$ drops the remaining voltage from $V_{DD}$ to this node.

**Current through $R_B$ (and through $Q_1$)**

$$
I_1
= \frac{V_{DD} - V_{G1}}{R_B}
= \frac{3.0 - 1.3}{1.7~\text{k}\Omega}
= \frac{1.7}{1.7~\text{k}\Omega}
= 1.0~\text{mA}
$$

✅ **Answer:** $I_1 = 1.00~\text{mA}$.

---

## Question 2 — Condition on $R_L$ for $I_1 = I_2$

> **Question:**  
> To ensure $I_1 = I_2$ in the same circuit, how must the load resistance $R_L$ be chosen?

**Idea**

- $Q_1$ and $Q_2$ are identical; $Q_1$ is diode-connected and sets the bias current.
- $Q_2$ mirrors that current **only if it stays in saturation**:
  $$
  V_{DS2} \ge V_{OV} = 0.3~\text{V}
  $$

**Voltages at $Q_2$**

- Source of $Q_2$ is at ground.
- Drain voltage of $Q_2$:
  $$
  V_{D2} = V_{DD} - I_2 R_L
  $$
  with $I_2 = I_1 = 1.0~\text{mA}$.

Saturation condition:
$$
V_{D2} = 3.0 - (1.0~\text{mA}) R_L \ge 0.3
$$

Solve for $R_L$:
$$
3.0 - 0.001R_L \ge 0.3
\Rightarrow 0.001R_L \le 2.7
\Rightarrow R_L \le 2.7~\text{k}\Omega
$$

So $R_L$ must be **no larger than** $2.7~\text{k}\Omega$.

✅ **Answer:** *$R_L$ must be **smaller than $2.7~\text{k}\Omega$*** (to keep $Q_2$ in saturation and preserve $I_1 = I_2$).

---

## Question 3 — Required Scaling $N$ in Self-Biased Mirror
![[quiz12_3.png|400]]
> **Question:**  
> In the self-biased bias circuit, the $(W/L)$-scaling ratio $N$ between $Q_2$ and $Q_1$ must be …  

**Idea**

In this kind of **self-biased current source**:

- $Q_1$ and $Q_2$ share the same $V_{GS}$.
- $Q_2$ has a **source resistor/bias network**, so its effective overdrive is **smaller** than that of $Q_1$.
- To still obtain **similar or larger current** through $Q_2$, we need:
  $$
  I_2 = \frac{1}{2}k'\frac{W}{L}\bigg\rvert_{Q_2}V_{OV2}^2
  $$
  with $V_{OV2} < V_{OV1}$.
- Therefore $(W/L)_{Q2}$ must be **larger** than $(W/L)_{Q1}$.

So the ratio
$$
N = \frac{(W/L)_{Q2}}{(W/L)_{Q1}} > 1
$$

✅ **Answer:** *$N$ must be **larger than 1***.

---

## Question 4 — Finding $R_B$ for $N = 4$ and $I_1 = I_2 = 0.2 mA$

> **Question:**  
> With $N=4$ and $V_{eff,1}=V_{OV1}=0.4~\text{V}$ for $Q_1$, find $R_B$ such that  
> $I_1 = I_2 = 0.2~\text{mA}$.

**Step 1 — Relate overdrives of $Q_1$ and $Q_2$**

Same $V_{GS}$ for both; different $(W/L)$.

Using $I_D = \tfrac{1}{2}k(W/L)V_{OV}^2$ and $I_1 = I_2$:

$$
\frac{1}{2}k(W/L)_1 V_{OV1}^2
=
\frac{1}{2}k(W/L)_2 V_{OV2}^2
=
\frac{1}{2}kN(W/L)_1 V_{OV2}^2
$$

So:
$$
V_{OV1}^2 = N V_{OV2}^2
\Rightarrow
V_{OV2} = \frac{V_{OV1}}{\sqrt{N}}
= \frac{0.4}{\sqrt{4}}
= 0.2~\text{V}
$$

**Step 2 — Source voltage of $Q_2$**

Gate voltage:
$$
V_G = V_t + V_{OV1}
$$

For $Q_2$:
$$
V_{GS2} = V_G - V_{S2} = V_t + V_{OV2}
$$

Subtract:
$$
V_{OV1} - V_{OV2} = V_{S2}
\Rightarrow
V_{S2} = 0.4 - 0.2 = 0.2~\text{V}
$$

This source node of $Q_2$ is tied to the top of $R_B$, so:
$$
V_{S2} = I_2 R_B
$$

**Step 3 — Solve for $R_B$**

Given $I_2 = 0.2~\text{mA}$:
$$
R_B = \frac{V_{S2}}{I_2}
= \frac{0.2~\text{V}}{0.2~\text{mA}}
= 1.0~\text{k}\Omega
$$

✅ **Answer:** $R_B = 1~\text{k}\Omega$.

---

## Question 5 — Transconductance $g_{m1}$ in Terms of $R_B$

> **Question:**  
> With $N=4$ in the same circuit, what is $g_{m1}$ (of $Q_1$) in terms of $R_B$?

We already have:
- $V_{OV1}$ and $V_{OV2} = V_{OV1}/\sqrt{N}$.
- $V_{S2} = V_{OV1} - V_{OV2} = V_{OV1}\left(1 - \frac{1}{\sqrt{N}}\right)$.
- $I_2 = I_1 = I$.
- $V_{S2} = I R_B$.

So:
$$
I = \frac{V_{S2}}{R_B}
= \frac{V_{OV1}\left(1 - \frac{1}{\sqrt{N}}\right)}{R_B}
$$

Transconductance of $Q_1$:
$$
g_{m1} = \frac{2I}{V_{OV1}}
= \frac{2}{V_{OV1}} \cdot
\frac{V_{OV1}\left(1 - \frac{1}{\sqrt{N}}\right)}{R_B}
= \frac{2\left(1 - \frac{1}{\sqrt{N}}\right)}{R_B}
$$

For $N=4$, $\sqrt{N}=2$:
$$
g_{m1} = \frac{2\left(1 - \tfrac{1}{2}\right)}{R_B}
       = \frac{2\cdot\frac{1}{2}}{R_B}
       = \frac{1}{R_B}
$$

✅ **Answer:** $g_{m1} = \dfrac{1}{R_B}$.

---

## Question 6 — Voltage Swing in Cascode Current Mirrors

> **Question:**  
> In cascode current mirrors, the available output voltage swing is …  

**Concept**

- Cascoding **stacks** transistors vertically to greatly increase **output resistance** and reduce current variation with $V_{OUT}$.
- However, each transistor needs its own **minimum $V_{DS}$** to stay in saturation.
- The required headroom is therefore **larger**, which **reduces the allowed $V_{OUT}$ swing**.

✅ **Answer:** *The voltage swing is **reduced***.

---

## Question 7 — Bandgap Voltage Reference Principle

> **Question:**  
> A bandgap voltage reference:  

**Concept**

- A bandgap reference combines:
  - A **PTAT** (proportional-to-absolute-temperature) voltage derived from a **difference of base-emitter voltages** of two BJTs/diodes with different current densities.
  - A **CTAT** (complementary-to-absolute-temperature) $V_{BE}$ of a single diode/BJT.
- Properly weighted sum:
  $$
  V_{REF} \approx V_{BE} + k\Delta V_{BE} \approx 1.2~\text{V}
  $$
  yields **temperature-independent** reference.
- Even in CMOS processes, the core uses **diode-connected BJTs / parasitic bipolar devices**, not MOSFETs alone.

✅ **Answer:** *Uses **diodes** to reduce the impact of temperature.*

---

## 🧠 Quick Reference Summary

| Topic | Key Relation / Insight | Comment |
|---|---|---|
| Simple mirror bias (Q1) | $I_1 = \dfrac{V_{DD}-V_{GS}}{R_B}$ | with $V_{GS}=V_t+V_{OV}$ |
| Saturation condition | $V_{DS} \ge V_{OV}$ | used to bound $R_L$ in Q2 |
| Self-biased mirror scaling | $V_{OV2} = V_{OV1}/\sqrt{N}$ | since $I_1 = I_2$ but $(W/L)_2 = N(W/L)_1$ |
| Source node of $Q_2$ | $V_{S2}=V_{OV1}-V_{OV2}$ | sets $R_B$ via $V_{S2} = I R_B$ |
| $R_B$ for $N=4$ and $I=0.2$ mA | $R_B = 1~\text{k}\Omega$ | from $V_{S2}=0.2$ V |
| $g_{m1}$ for $N=4$ | $g_{m1} = 1/R_B$ | general: $g_{m1} = 2(1-1/\sqrt{N})/R_B$ |
| Cascode mirror swing | **Reduced** | more devices ⇒ more headroom needed |
| Bandgap reference | $V_{REF} \approx V_{BE} + k\Delta V_{BE}$ | uses multiple diodes/BJTs to cancel temperature dependence |

---
