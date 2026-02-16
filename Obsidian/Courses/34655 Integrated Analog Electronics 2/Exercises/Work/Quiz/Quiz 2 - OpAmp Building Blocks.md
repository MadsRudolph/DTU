---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: quiz
tags: [IAE2, quiz]
---
# Quiz 2 - OpAmp Building Blocks

> [!info] Related Notes
> - [[Lecture 1 - Introduction and Prerequisites]]
> - [[Advanced OpAmps - Lecture Notes]]
> - [[Course Recap - Understanding Analog IC Design]]

---

## Question 1 (1 point)

> [!question] The input stage in a CMOS opamp is normally
> - [ ] a common source stage
> - [ ] a source follower
> - [x] **a differential pair**

> [!success] Answer: A differential pair

> [!note]- Explanation
> The **differential pair** is the standard input stage for CMOS opamps because it provides:
>
> 1. **High input impedance** - The gates of MOSFETs draw essentially no DC current
> 2. **Differential input capability** - Can amplify the difference between two inputs
> 3. **Common-mode rejection** - Rejects signals that appear on both inputs equally
> 4. **Level shifting** - Can handle input signals at various DC levels
>
> A common source stage only has one input, and a source follower has gain ≈ 1, making them unsuitable as the primary input stage.
>
> See: [[Lecture 1 - Introduction and Prerequisites#Differential Stage]]

---

## Question 2 (1 point)

> [!question] In order to obtain low output resistance from a CMOS opamp the output stage can be configured as
> - [ ] a common source stage
> - [x] **a common drain stage**
> - [ ] a common gate stage

> [!success] Answer: A common drain stage

> [!note]- Explanation
> The **common drain stage** (also called **source follower**) has:
>
> $$r_{out} \approx \frac{1}{g_m}$$
>
> This is typically in the range of 1-10 kΩ, which is **much lower** than other configurations.
>
> | Configuration | Output Resistance |
> |---------------|-------------------|
> | Common Source | $r_{ds}$ (high, ~100 kΩ - MΩ) |
> | Common Drain | $1/g_m$ (low, ~1-10 kΩ) |
> | Common Gate | $r_{ds}(1 + g_m R_S)$ (very high) |
>
> Low output resistance is important for:
> - Driving capacitive loads without losing bandwidth
> - Providing current to resistive loads without voltage drop
>
> See: [[Lecture 1 - Introduction and Prerequisites#Common Drain (Source Follower)]]

---

## Question 3 (1 point)

> [!question] In a CMOS opamp built from a differential pair, a common source stage and a common drain stage, the dominant pole normally comes from
> - [x] **the input to the common source stage**
> - [ ] the input to the common drain stage
> - [ ] the source node for the input differential pair

> [!success] Answer: The input to the common source stage

> [!note]- Explanation
> The **dominant pole** occurs at the node with the **highest impedance** combined with significant capacitance.
>
> **Analyzing each node:**
>
> | Node | Impedance | Dominant Pole? |
> |------|-----------|----------------|
> | Input to CS stage (output of diff pair) | $r_{ds} \parallel r_{ds}$ (high!) | **Yes** |
> | Input to CD stage (output of CS) | $r_{ds}$ (high, but less capacitance) | Secondary |
> | Source node of diff pair | $1/g_m$ (low) | No |
>
> The output of the differential pair (input to CS stage) has:
> - High resistance: $r_{o,diff} = r_{ds,NMOS} \parallel r_{ds,PMOS}$
> - Significant capacitance: gate capacitance of CS transistor + parasitic capacitances
>
> This creates the dominant low-frequency pole:
> $$\omega_{p1} = \frac{1}{R_{out,diff} \cdot C_{total}}$$

---

## Question 4 (1 point)

> [!question] In a CMOS opamp consisting of a differential pair, a common source stage and a common drain stage, the frequency response is normally controlled by a compensation capacitor inserted between
> - [ ] gate and source of the common drain stage
> - [ ] gate and source of the common source stage
> - [x] **gate and drain of the common source stage**

> [!success] Answer: Gate and drain of the common source stage

> [!note]- Explanation
> This is **Miller compensation**. The capacitor is placed across the inverting gain stage (common source):
>
> ```
> Diff Pair → ──┬── CS Stage ──┬── CD Stage → Vout
>               │              │
>               └──────┤├──────┘
>                      Cc
> ```
>
> **Why gate-to-drain of CS stage?**
>
> The Miller effect multiplies the effective capacitance:
> $$C_{eff} = C_C(1 + |A_{CS}|)$$
>
> This creates a **dominant low-frequency pole** that:
> 1. Pushes other poles to higher frequencies (pole splitting)
> 2. Ensures the amplifier crosses unity gain with adequate phase margin
> 3. Makes the frequency response predictable and stable
>
> **Why not the other options?**
> - Gate-source of CD: No gain across this, no Miller multiplication
> - Gate-source of CS: Wrong nodes, wouldn't provide pole splitting
>
> See: [[Advanced OpAmps - Lecture Notes#2. The Two-Stage OpAmp]]

---

## Question 5 (1 point)

### Circuit

![[Quiz2_Q5_schematic.png|400]]

> [!question] For the circuit shown here, assume that all transistors have an Early voltage $|V_A| = 25$ V. The output resistance of the differential stage is
> - [ ] $r_{out} = 25\ \text{k}\Omega$
> - [x] **$r_{out} = 50\ \text{k}\Omega$**
> - [ ] $r_{out} = 100\ \text{k}\Omega$

> [!success] Answer: $r_{out} = 50\ \text{k}\Omega$

> [!note]- Explanation
> **Given:**
> - Tail current $I_{SS} = 0.5$ mA
> - Early voltage $|V_A| = 25$ V for all transistors
>
> > [!abstract] Step 1: Find current in each branch
> > In a balanced differential pair, the tail current splits equally:
> > $$I_{D} = \frac{I_{SS}}{2} = \frac{0.5\ \text{mA}}{2} = 0.25\ \text{mA}$$
>
> > [!abstract] Step 2: Calculate $r_{ds}$ for each transistor
> > $$r_{ds} = \frac{V_A}{I_D} = \frac{25\ \text{V}}{0.25\ \text{mA}} = 100\ \text{k}\Omega$$
> >
> > This applies to both the NMOS input transistor and the PMOS load transistor.
>
> > [!abstract] Step 3: Find output resistance
> > At the output node, we see the NMOS $r_{ds}$ in parallel with the PMOS $r_{ds}$:
> > $$r_{out} = r_{ds,N} \parallel r_{ds,P} = \frac{100\ \text{k}\Omega \times 100\ \text{k}\Omega}{100\ \text{k}\Omega + 100\ \text{k}\Omega} = \boxed{50\ \text{k}\Omega}$$
>
> > [!tip] General Formula
> > For a differential pair with current mirror load:
> > $$r_{out} = r_{ds,input} \parallel r_{ds,load}$$

---

## Question 6 (1 point)

> [!question] With all transistors in the circuit above having an effective gate voltage of $|V_{GS} - V_{t0}| = 0.5$ V, the small signal differential gain is
> - [x] **$A_v = 50\ \text{V/V}$**
> - [ ] $A_v = 100\ \text{V/V}$
> - [ ] $A_v = 200\ \text{V/V}$

> [!success] Answer: $A_v = 50\ \text{V/V}$

> [!note]- Explanation
> **Given:**
> - $V_{eff} = |V_{GS} - V_{t0}| = 0.5$ V
> - $I_D = 0.25$ mA (from previous question)
> - $r_{out} = 50\ \text{k}\Omega$ (from previous question)
>
> > [!abstract] Step 1: Calculate transconductance $g_m$
> > Using $g_m = \frac{2I_D}{V_{eff}}$:
> > $$g_m = \frac{2 \times 0.25\ \text{mA}}{0.5\ \text{V}} = \frac{0.5\ \text{mA}}{0.5\ \text{V}} = 1\ \text{mA/V}$$
>
> > [!abstract] Step 2: Calculate differential gain
> > For a differential pair with current mirror load:
> > $$A_v = g_m \cdot r_{out}$$
> > $$A_v = 1\ \text{mA/V} \times 50\ \text{k}\Omega = \boxed{50\ \text{V/V}}$$
>
> > [!tip] Alternative Check Using Intrinsic Gain
> > $$A_i = g_m \cdot r_{ds} = 1\ \text{mA/V} \times 100\ \text{k}\Omega = 100$$
> >
> > Since output sees two $r_{ds}$ in parallel:
> > $$A_v = g_m \cdot (r_{ds} \parallel r_{ds}) = g_m \cdot \frac{r_{ds}}{2} = \frac{A_i}{2} = 50\ \text{V/V}$$ ✓

---

## Question 7 (1 point)

> [!question] In the circuit above, assume that the PMOS transistor threshold voltage is -1 V. With a quiescent value of 0 V for both input voltages, the quiescent value of the gate voltage for the PMOS transistors is
> - [ ] 4.5 V
> - [ ] 2.5 V
> - [x] **1.5 V**

> [!success] Answer: 1.5 V

> [!note]- Explanation
> **Given:**
> - $V_{DD} = 3$ V
> - $V_{t,PMOS} = -1$ V
> - $V_{eff} = 0.5$ V (from Q6)
> - Both inputs at 0 V (balanced condition)
>
> > [!abstract] Analysis
> > The PMOS transistors form a **current mirror** (diode-connected on left, mirror on right).
> >
> > For PMOS in saturation:
> > $$V_{SG} = |V_{t,PMOS}| + V_{eff} = 1\ \text{V} + 0.5\ \text{V} = 1.5\ \text{V}$$
> >
> > Since the source is connected to $V_{DD}$:
> > $$V_G = V_S - V_{SG} = V_{DD} - V_{SG} = 3\ \text{V} - 1.5\ \text{V} = \boxed{1.5\ \text{V}}$$
>
> > [!tip] Sanity Check
> > The gate voltage (1.5 V) is below $V_{DD}$ (3 V) by $V_{SG}$ = 1.5 V, which makes sense for a PMOS that needs negative $V_{GS}$ (or positive $V_{SG}$) to turn on.

---

## Question 8 (1 point)

> [!question] If the input voltages are changed so that all of the bias current flows in the leftmost NMOS/PMOS transistors, the gate voltage of the PMOS transistors is changed to
> - [x] **1.3 V**
> - [ ] 1.7 V
> - [ ] 4.7 V

> [!success] Answer: 1.3 V

> [!note]- Explanation
> **New condition:** All tail current flows through the left branch
> - $I_{D,left} = I_{SS} = 0.5$ mA (doubled from 0.25 mA)
> - $I_{D,right} = 0$ mA
>
> > [!abstract] Step 1: Find new $V_{eff}$ for left PMOS
> > The saturation current equation is:
> > $$I_D = \frac{1}{2}\mu_p C_{ox}\frac{W}{L}V_{eff}^2$$
> >
> > Since $I_D \propto V_{eff}^2$, if current doubles:
> > $$\frac{I_{D,new}}{I_{D,old}} = \frac{V_{eff,new}^2}{V_{eff,old}^2} = 2$$
> >
> > $$V_{eff,new} = V_{eff,old} \cdot \sqrt{2} = 0.5\ \text{V} \times \sqrt{2} = 0.707\ \text{V}$$
>
> > [!abstract] Step 2: Calculate new gate voltage
> > $$V_{SG,new} = |V_{t,PMOS}| + V_{eff,new} = 1\ \text{V} + 0.707\ \text{V} = 1.707\ \text{V}$$
> >
> > $$V_G = V_{DD} - V_{SG,new} = 3\ \text{V} - 1.707\ \text{V} = 1.293\ \text{V} \approx \boxed{1.3\ \text{V}}$$
>
> > [!tip] Key Insight
> > When the current through a transistor changes, $V_{eff}$ changes as $\sqrt{I_D}$, not linearly!
> > $$V_{eff} \propto \sqrt{I_D}$$

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Key Concept |
> |---|--------|-------------|
> | 1 | Differential pair | Standard opamp input stage |
> | 2 | Common drain | Low output resistance: $r_o = 1/g_m$ |
> | 3 | Input to CS stage | Highest impedance node = dominant pole |
> | 4 | Gate-drain of CS | Miller compensation |
> | 5 | 50 kΩ | $r_{out} = r_{ds,N} \parallel r_{ds,P}$ |
> | 6 | 50 V/V | $A_v = g_m \cdot r_{out}$ |
> | 7 | 1.5 V | $V_G = V_{DD} - V_{SG}$ |
> | 8 | 1.3 V | $V_{eff} \propto \sqrt{I_D}$ |

---

## Key Formulas Used

> [!abstract] Formulas Reference
> | Quantity | Formula |
> |----------|---------|
> | Output resistance | $r_{ds} = V_A / I_D$ |
> | Parallel resistance | $r_{out} = r_1 \parallel r_2 = \frac{r_1 r_2}{r_1 + r_2}$ |
> | Transconductance | $g_m = 2I_D / V_{eff}$ |
> | Differential gain | $A_v = g_m \cdot r_{out}$ |
> | PMOS gate voltage | $V_G = V_{DD} - V_{SG} = V_{DD} - (\lvert V_t \rvert + V_{eff})$ |
> | Current-Veff relation | $I_D \propto V_{eff}^2$ so $V_{eff} \propto \sqrt{I_D}$ |

---

> [!nav]
> [[Quiz 1 - Two-Stage CMOS Opamp|← Quiz 1]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
