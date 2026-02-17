---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, cadence, opamp]
---
# Cadence Exercise -- Two-Stage OpAmp Design

> [!info] Exercise Files
> - Specifications: [[Amplifier_design_specifications_v3.pdf]]
> - Textbook: [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=228|Carusone, Ch. 5-6]] | [[cmos_analog_ic_design_fundamentals.pdf#page=258|Bruun (EB), Ch. 7]]
> - Related notes: [[Advanced OpAmps - Lecture Notes]]
> - Background: [[Course Recap - Understanding Analog IC Design]]

> [!tip] How to Read This Document
> This is a complete walkthrough of the paper design. Every design step explains **why** we do it, **what** the equation means physically, and **how** the numbers come out. If you're new to opamp design, read it top-to-bottom. If you just need the results, skip to [[#Design Summary]].

---

## What Are We Building?

We are designing a **two-stage Miller-compensated CMOS operational amplifier**. Let's break that down:

- **Two-stage**: The amplifier has two gain stages in series (a *cascade*). The first stage is a differential pair; the second stage is a common-source amplifier. Two stages give us enough gain (~80-90 dB) for most feedback applications. *([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=266|Carusone Ch. 6.1-6.2]])*
- **Miller-compensated**: We add a capacitor between the output of stage 1 and the output of stage 2. Through the *Miller effect*, this capacitor appears much larger at the first stage output, creating a dominant low-frequency pole. This is how we guarantee **stability** when the opamp is used with feedback. *([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278|Carusone Ch. 6.3]]; [[cmos_analog_ic_design_fundamentals.pdf#page=259|EB Ch. 7.1]])*
- **CMOS**: All transistors are either NMOS or PMOS. No bipolar transistors, no resistors for biasing (except the compensation resistor $R_c$).

The opamp is used in a **non-inverting capacitive-feedback** configuration: the output feeds back to the inverting input through capacitors $C_A$ and $C_B$, giving a closed-loop gain of 2.

> [!abstract] Why This Topology?
> The two-stage opamp is the "textbook" topology. It's simple enough to design by hand, yet powerful enough for many real applications. It has excellent output swing (the output can get close to both supply rails), unlike single-stage opamps like the folded cascode which sacrifice swing for simplicity.
>
> **Downside:** It has two high-impedance nodes (one per stage), which means two poles in the frequency response. Without compensation, these two poles would cause oscillation in feedback. That's why Miller compensation is essential.
>
> See [[Advanced OpAmps - Lecture Notes#2. The Two-Stage OpAmp]] for the key equations and [[Course Recap - Understanding Analog IC Design#Part 8 Feedback and Stability]] for the stability background.

---

## Specifications

These are the targets we must meet. They come from the exercise specification document.

| Parameter | Value | What It Means |
|-----------|-------|---------------|
| $C_A = C_B$ | 1 pF | Feedback capacitors that set the closed-loop gain |
| $C_L$ | 1.5 pF | Load capacitance the opamp must drive |
| $R_1$ | $10^9\;\Omega$ | Very large resistor to set the DC bias of the inverting input (acts like an open circuit for AC signals) |
| $V_{DD}$ | 1.8 V | Supply voltage (typical for 0.18 μm CMOS) |
| Closed-loop gain $V_{out}/V_{in}$ | 2 | The opamp with feedback should amplify by exactly 2x |
| Closed-loop BW $\omega_t$ | $2\pi \times 20$ MHz | The gain of 2 must be maintained up to 20 MHz |
| Slew rate | $\geq 30$ V/μs | How fast the output can change for a large input step |
| Phase margin | $\geq 70°$ | How stable the feedback loop is (70° = very well-behaved, minimal ringing) |

> [!note] Understanding Phase Margin
> Phase margin (PM) tells us how far the loop is from oscillating. At the frequency where the loop gain drops to 1 (0 dB), the phase must be more than -180° for stability. PM is the distance from -180°:
> $$PM = 180° + \angle L(j\omega_t)$$
> - PM = 90° → perfect (no ringing at all)
> - PM = 70° → excellent (very slight overshoot)
> - PM = 60° → acceptable (some ringing)
> - PM = 45° → poor (significant ringing)
> - PM = 0° → oscillation!
>
> We target 70° because the exercise says so, but in practice anything above 60° is usually fine.
>
> *([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=235|Carusone Ch. 5.4]]; [[cmos_analog_ic_design_fundamentals.pdf#page=259|EB Ch. 7.1]]; [[Lecture 1 - Introduction and Prerequisites#Phase Margin]])*

> [!note] Understanding Slew Rate
> Slew rate is the maximum rate of change of the output voltage. It's limited by the available current to charge/discharge capacitors. When the input changes so fast that the differential pair transistors can no longer follow linearly (one transistor turns off completely), the output slews at a fixed rate determined by the bias current divided by the compensation capacitor.
>
> $$SR = \frac{I_{\text{tail}}}{C_c}$$
>
> For a step input, the output ramps linearly at this rate until it catches up.

---

### Process Parameters

**Process: 0.18 μm CMOS ([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=53|Carusone Table 1.5, p. 53]])**

These numbers are fixed by the semiconductor fabrication process. We cannot change them — we can only choose $W/L$ ratios and bias currents.

| Parameter | NMOS | PMOS | What It Is |
|-----------|------|------|------------|
| $k' = \mu C_{ox}$ | 270 μA/V² | 70 μA/V² | Transconductance parameter. NMOS is ~4x larger because electrons move faster than holes. |
| $V_t$ | 0.5 V | $-0.45$ V | Threshold voltage. The minimum gate voltage to turn the transistor on. |
| $\lambda \cdot L$ | 0.08 μm/V | 0.08 μm/V | Channel-length modulation factor times length. Determines output resistance. |
| $\lambda$ (at $L = 1\;\mu$m) | 0.08 V⁻¹ | 0.08 V⁻¹ | At our chosen $L = 1\;\mu$m, $\lambda = 0.08$. This means $r_{ds} = 1/(\lambda I_D)$. |
| $C_{ox}$ | 8.5 fF/μm² | 8.5 fF/μm² | Gate oxide capacitance per unit area. |
| $C_{ov} = L_{ov} C_{ox}$ | 0.35 fF/μm | 0.50 fF/μm | Overlap capacitance per unit width (gate-to-source and gate-to-drain). |

> [!warning] Why $\lambda$ Matters So Much
> The parameter $\lambda$ directly limits the gain. The output resistance of a transistor is $r_{ds} = 1/(\lambda I_D)$. A higher $\lambda$ means lower $r_{ds}$, which means lower gain per stage. With $\lambda = 0.08\;\text{V}^{-1}$, a transistor carrying 12 μA has $r_{ds} = 1/(0.08 \times 12\mu) = 1.04\;\text{M}\Omega$. This is the main reason our simulated gain (81.5 dB) is lower than the ideal hand calculation (~93 dB).
>
> *(See [[Course Recap - Understanding Analog IC Design#Channel Length Modulation]] for intuition)*

---

## Circuit Topology

*([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=266|Carusone Ch. 6, Fig. 6.3]]; [[cmos_analog_ic_design_fundamentals.pdf#page=258|EB Ch. 7, Fig. 7.1]])*

The circuit has 8 transistors, each with a specific role. Understanding these roles is crucial before we size anything.

### First Stage: Differential Pair with Current Mirror Load

- **Q1, Q2** (PMOS) — **Differential input pair.** These are the transistors that actually sense the input voltage difference ($V^+ - V^-$). When $V^+$ goes up relative to $V^-$, Q2 conducts more current and Q1 conducts less. We use PMOS here (instead of NMOS) because the exercise specifies it — in practice, PMOS inputs have the advantage that the input common-mode range extends down to ground.

  *Why matched?* Q1 and Q2 must be identical ($W/L$ and $L$) so they share the tail current equally when the input is balanced. Any mismatch causes offset voltage.

- **Q3, Q4** (NMOS) — **Current mirror active load.** Q3 is diode-connected (gate tied to drain), which makes it the mirror reference. Q4 copies Q3's current. The clever part: Q3 sinks whatever current Q1 pushes down, and Q4 tries to sink the same amount. But Q2 is pushing a *different* current (because the input is unbalanced). The difference between Q2's current and Q4's current flows into the next stage — this is how the differential signal is converted to a single-ended signal.

  *Why not just a resistor load?* Resistors have fixed resistance and would limit the gain. The current mirror has very high output impedance ($r_{ds}$), giving much higher gain. Also, resistors take up enormous area on a chip.

  *(See [[Advanced OpAmps - Lecture Notes#1.2 Current Mirror]] and [[Course Recap - Understanding Analog IC Design#Part 6 Current Mirrors - Biasing Done Right]])*

- **Q5** (PMOS) — **Tail current source.** This sets the total current flowing through the differential pair: $I_{D5} = I_{D1} + I_{D2}$. It's a current mirror that copies (and scales) the reference current from Q8. By making $W_5/L$ different from $W_8/L$, we can scale the current up or down.

  *Why a current source, not a resistor?* A current source has very high impedance to common-mode signals, which gives us high CMRR (common-mode rejection ratio). A resistor would let common-mode noise through.

### Second Stage: Common-Source Amplifier

- **Q7** (NMOS) — **Second stage gain device.** This is a common-source amplifier. Its gate is driven by the first-stage output (node `n_d2`). It provides the second round of voltage gain. Q7 mirrors Q3 — they share the same gate-source voltage structure, which means their $V_\text{eff}$ values are related by their $W/L$ ratios.

  *(See [[Advanced OpAmps - Lecture Notes#1.3 Common Source Stage]] for CS stage properties)*

- **Q6** (PMOS) — **Second stage current source.** This provides the bias current for Q7 and acts as the load for the second stage. Like Q5, it mirrors Q8 but with a different scaling ratio to deliver more current (60 μA vs 24 μA). Together, Q6 and Q7 form the second stage: Q7 amplifies, Q6 provides a high-impedance load.

### Bias Circuit

- **Q8** (PMOS) — **Diode-connected bias reference.** An external ideal current source forces 20 μA through Q8. Since Q8 is diode-connected ($V_{GS} = V_{DS}$), it is always in saturation and establishes a fixed $V_{GS}$. All PMOS current sources (Q5, Q6) copy this $V_{GS}$ via their shared gate connection, creating scaled copies of the reference current.

  *Why diode-connected?* When $V_{GS} = V_{DS}$, the transistor is guaranteed to be in saturation. This makes it a stable voltage reference that other transistors can mirror.

### Current Relationships

When the input is balanced (no differential signal), all currents are determined by the mirror ratios:

$$I_{D1} = I_{D2} = I_{D3} = I_{D4} = \tfrac{1}{2}I_{D5}$$

$$I_{D6} = I_{D7}$$

The first stage splits the tail current equally. The second stage current is set independently by the Q6/Q8 mirror ratio.

### Miller Compensation Network

Between the first-stage output and the second-stage output, we place:
- $C_c$ — the **compensation capacitor** (0.8 pF). Through the Miller effect, this appears as $C_c \times (1 + |A_2|)$ at the first-stage output, creating a very low dominant pole. This pole-splitting technique pushes the first pole down and the second pole up, creating a clean single-pole rolloff and ensuring stability.
- $R_c$ — the **compensation resistor** (~1 kΩ, in series with $C_c$). Without $R_c$, the direct feedforward path through $C_c$ creates a *right-half-plane (RHP) zero* that degrades phase margin. Adding $R_c = 1/g_{m7}$ pushes this zero to infinity, or a larger $R_c$ can turn it into a helpful left-half-plane zero.

*([[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278|Carusone Ch. 6.3]]; [[cmos_analog_ic_design_fundamentals.pdf#page=259|EB Ch. 7.1-7.2]])*

> [!abstract] The Full Picture
> **Stage 1** (Q1-Q5): Converts the differential input voltage into a current, then into a single-ended voltage at node `n_d2`. Gain = $g_{m1} \times (r_{ds2} \| r_{ds4})$.
>
> **Stage 2** (Q6-Q7): Takes the voltage at `n_d2` and amplifies it again. Gain = $g_{m7} \times (r_{ds6} \| r_{ds7})$.
>
> **Total open-loop gain**: Product of both stages, typically 60-90 dB.
>
> **Compensation** ($C_c$, $R_c$): Makes the whole thing stable when we wrap feedback around it.

---

## Design Procedure

The design follows a systematic 10-step procedure from Erik Bruun's textbook ([[cmos_analog_ic_design_fundamentals.pdf#page=258|EB Ch. 7]]). The order matters: each step depends on previous results. We start from the specifications and work our way down to transistor sizes.

> [!tip] The Design Philosophy
> The approach is "top-down": we start from the closed-loop requirements (gain, bandwidth, phase margin) and derive what the open-loop opamp needs to provide. Then we figure out what component values achieve that. Finally, we size the transistors to deliver those component values.

---

### Step 1 -- Feedback Factor $\beta$

*([[cmos_analog_ic_design_fundamentals.pdf#page=259|EB Ch. 7.1]]; [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=229|Carusone Ch. 5.2]])*

**Why:** The feedback factor $\beta$ connects the closed-loop specifications to the open-loop opamp requirements. Everything we design for the opamp depends on knowing $\beta$ first.

**What is $\beta$?** It's the fraction of the output signal that gets fed back to the inverting input. In our circuit, the feedback path is a capacitive voltage divider formed by $C_A$ and $C_B$:

```
Vout ──┤C_B├── n_inv ──┤C_A├── GND
```

The voltage at the inverting input (`n_inv`) relative to the output is:

$$\beta = \frac{C_B}{C_A + C_B} = \frac{1}{1+1}$$

$$\boxed{\beta = 0.5}$$

**What does $\beta = 0.5$ mean?** Half of the output voltage is fed back to the inverting input. The closed-loop gain is $1/\beta = 2$, which matches our specification.

**Physical intuition:** $C_A$ and $C_B$ form an AC voltage divider. Since they're equal, the voltage is split 50/50. If $C_B$ were larger, more signal would feed back, reducing the closed-loop gain.

> [!note] Why Capacitors Instead of Resistors?
> In integrated circuits, capacitors are much more accurate and take less area than resistors. They also don't consume DC power. The tradeoff is that capacitive feedback doesn't set a DC operating point — that's why we need the huge $R_1 = 1\;\text{G}\Omega$ to provide a DC path.

---

### Step 2 -- Second Pole $\omega_{p2}$

*([[cmos_analog_ic_design_fundamentals.pdf#page=261|EB Ch. 7.1, Eq. 7.8]]; [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278|Carusone Ch. 6.3]])*

**Why:** The second pole is the main threat to stability. It adds negative phase shift at the unity-gain frequency. We need to place it far enough away that the total phase shift stays within our phase margin budget.

**Background:** Our compensated opamp has three important frequencies:
1. **Dominant pole** $\omega_{p1}$ — set by Miller compensation (very low, ~100 Hz). This is the pole that makes the gain roll off at -20 dB/decade.
2. **Second pole** $\omega_{p2} = g_{m7}/C_{L,\text{tot}}$ — at the output node. This adds another -20 dB/decade rolloff and -90° phase shift.
3. **RHP zero** $\omega_z = g_{m7}/C_c$ — caused by feedforward through $C_c$. This adds phase lag (because it's in the right half-plane), making stability worse.

At the closed-loop unity-gain frequency $\omega_t$, the phase margin is:

$$PM = 90° - \arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) - \arctan\!\left(\frac{\omega_t}{\omega_z}\right) \geq 70°$$

> [!note] Where Does This Formula Come From?
> The open-loop transfer function near the unity-gain frequency looks like:
> $$A(s) \approx \frac{\omega_{tl}}{s} \cdot \frac{1}{1 + s/\omega_{p2}} \cdot \frac{1 - s/\omega_z}{1}$$
>
> The phase at frequency $\omega_t$ is:
> - From the dominant pole ($\omega_{tl}/s$): $-90°$
> - From the second pole: $-\arctan(\omega_t/\omega_{p2})$
> - From the RHP zero: $-\arctan(\omega_t/\omega_z)$ (negative because RHP!)
>
> Total phase = $-90° - \arctan(\omega_t/\omega_{p2}) - \arctan(\omega_t/\omega_z)$
>
> Phase margin = $180°$ + total phase = $90° - \arctan(\omega_t/\omega_{p2}) - \arctan(\omega_t/\omega_z)$

**Design choice (hint 2a):** We choose $\omega_z = 10\,\omega_t$. This places the RHP zero far above the unity-gain frequency so it barely affects the phase.

Now we solve for $\omega_{p2}$:

$$90° - \arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) - \arctan\!\left(\frac{\omega_t}{10\,\omega_t}\right) \geq 70°$$

$$90° - \arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) - \arctan(0.1) \geq 70°$$

$\arctan(0.1) = 5.71°$, so:

$$\arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) \leq 90° - 70° - 5.71° = 14.29°$$

$$\frac{\omega_t}{\omega_{p2}} \leq \tan(14.29°) = 0.2546$$

$$\omega_{p2} \geq \frac{\omega_t}{0.2546} \approx 3.93\,\omega_t$$

We round up to a clean number:

$$\boxed{\omega_{p2} = 4\,\omega_t = 2\pi \times 80\text{ MHz}}$$

**Physical meaning:** The second pole must be at least 4 times higher than the closed-loop bandwidth. This ensures the second pole's phase contribution ($\arctan(1/4) = 14°$) doesn't eat up too much of our phase margin budget.

---

### Step 3 -- Transconductance Ratio $g_{m7}/g_{m1}$

*([[cmos_analog_ic_design_fundamentals.pdf#page=261|EB Ch. 7.1, Eq. 7.9]])*

**Why:** We need to relate the two stages' transconductances to each other before we can size anything. This ratio comes from the relationship between the open-loop GBW, the RHP zero, and the feedback factor.

**The key relationships:**

1. The open-loop GBW (unity-gain bandwidth of the opamp alone, without feedback) is:
   $$\omega_{tl} = \frac{g_{m1}}{C_c}$$
   This comes from the Miller-compensated transfer function: gain rolls off at -20 dB/decade, crossing 0 dB at $\omega_{tl}$.

2. The closed-loop bandwidth relates to the open-loop GBW through feedback:
   $$\omega_t = \beta \cdot \omega_{tl}$$
   This is the fundamental feedback result: **feedback trades gain for bandwidth**. Since $\beta = 0.5$, the closed-loop bandwidth is half the open-loop GBW.

3. So the open-loop GBW is:
   $$\omega_{tl} = \frac{\omega_t}{\beta} = \frac{\omega_t}{0.5} = 2\,\omega_t$$

4. The RHP zero frequency (our design choice from Step 2):
   $$\omega_z = \frac{g_{m7}}{C_c} = 10\,\omega_t$$

**Taking the ratio:**

$$\frac{g_{m7}}{g_{m1}} = \frac{\omega_z}{\omega_{tl}} = \frac{10\,\omega_t}{2\,\omega_t} = 5$$

$$\boxed{g_{m7} = 5\,g_{m1}}$$

**Physical meaning:** The second stage must have 5x the transconductance of the first stage. This makes sense: the second stage handles more current (it needs to drive the load capacitance), while the first stage is optimized for low noise and high gain (lower current).

---

### Step 4 -- Total Load Capacitance $C_{L,\text{tot}}$

*([[cmos_analog_ic_design_fundamentals.pdf#page=259|EB Ch. 7.1]])*

**Why:** The second pole depends on the total capacitance at the output. We need to count all capacitors connected to the output node.

**What's at the output?** Looking at the circuit, the output node sees:
- $C_L = 1.5$ pF — the external load capacitor (to ground)
- The series combination of $C_B$ and $C_A$ — the feedback network. From the output's perspective, $C_B$ connects to node `n_inv`, and from there $C_A$ goes to ground. So the output sees $C_B$ in series with $C_A$.

$$C_{L,\text{tot}} = C_L + \frac{C_B \cdot C_A}{C_B + C_A} = 1.5 + \frac{1 \times 1}{1+1} = 1.5 + 0.5$$

$$\boxed{C_{L,\text{tot}} = 2.0\text{ pF}}$$

> [!note] Series Capacitor Formula
> Capacitors in series combine like resistors in parallel:
> $$C_{\text{series}} = \frac{C_1 \cdot C_2}{C_1 + C_2}$$
> Two 1 pF caps in series = 0.5 pF. This is smaller than either individual cap — series capacitors always reduce total capacitance.

---

### Step 5 -- Compensation Capacitor $C_c$

*([[cmos_analog_ic_design_fundamentals.pdf#page=261|EB Ch. 7.1, Eq. 7.12]])*

**Why:** $C_c$ is the heart of the compensation network. It determines the dominant pole location and therefore the GBW of the opamp.

**Derivation:** We have two equations involving $g_{m7}$:

- Second pole: $\omega_{p2} = g_{m7} / C_{L,\text{tot}}$
- RHP zero: $\omega_z = g_{m7} / C_c$

Dividing these:

$$\frac{\omega_{p2}}{\omega_z} = \frac{C_c}{C_{L,\text{tot}}}$$

We know from Step 2 that $\omega_{p2} = 4\,\omega_t$ and $\omega_z = 10\,\omega_t$:

$$\frac{C_c}{C_{L,\text{tot}}} = \frac{4\,\omega_t}{10\,\omega_t} = 0.4$$

$$\boxed{C_c = 0.4 \times 2.0 = 0.8\text{ pF}}$$

**Physical meaning:** The compensation capacitor is 40% of the total load capacitance. A larger $C_c$ would push $\omega_{p2}$ further away (better stability), but would also reduce the GBW (since $\omega_{tl} = g_{m1}/C_c$). The value 0.8 pF is the optimal compromise.

> [!tip] Sanity Check
> In two-stage opamps, $C_c$ is typically 20-50% of $C_L$. Our 0.8 pF vs 2.0 pF (40%) is right in this range.

---

### Step 6 -- First Stage Transconductance $g_{m1}$

*([[cmos_analog_ic_design_fundamentals.pdf#page=261|EB Ch. 7.1, Eq. 7.5]])*

**Why:** Now we can calculate the actual transconductance value needed for the first stage. This will determine how much current Q1 and Q2 need.

From the GBW equation:

$$g_{m1} = \omega_{tl} \cdot C_c$$

We know $\omega_{tl} = \omega_t / \beta$:

$$g_{m1} = \frac{\omega_t}{\beta} \cdot C_c = \frac{2\pi \times 20 \times 10^6}{0.5} \times 0.8 \times 10^{-12}$$

$$g_{m1} = 2.513 \times 10^{8} \times 8 \times 10^{-13}$$

$$\boxed{g_{m1} = 201\text{ μA/V}}$$

**Physical meaning:** Each input transistor (Q1, Q2) must have a transconductance of 201 μA/V. This means that a 1 mV change at the gate causes a 0.201 μA change in drain current. This is a modest $g_m$ — we're not pushing for high speed here, which is good for power consumption.

**What sets $g_m$?** Recall from [[Course Recap - Understanding Analog IC Design#1. Transconductance ($g_m$) - "How much current per volt?"]]:
$$g_m = \frac{2I_D}{V_\text{eff}}$$
So $g_m$ depends on both the bias current and the overdrive voltage. We'll use this in Step 10 to find W/L.

---

### Step 7 -- Second Stage Transconductance $g_{m7}$

*(follows directly from Step 3)*

**Why:** From the ratio established in Step 3, we simply scale up.

$$g_{m7} = 5 \times g_{m1} = 5 \times 201$$

$$\boxed{g_{m7} = 1005\text{ μA/V} \approx 1.0\text{ mA/V}}$$

**Verification:** Let's check that the second pole and RHP zero land where we want them:
- $\omega_{p2} = g_{m7}/C_{L,\text{tot}} = 1005\mu / 2.0p = 5.025 \times 10^8$ rad/s $= 2\pi \times 80$ MHz ✓
- $\omega_z = g_{m7}/C_c = 1005\mu / 0.8p = 1.256 \times 10^9$ rad/s $= 2\pi \times 200$ MHz $= 10\,\omega_t$ ✓

---

### Step 8 -- Tail Current $I_{D5}$ (First Stage Slew Rate)

*([[cmos_analog_ic_design_fundamentals.pdf#page=265|EB Ch. 7.2, Eq. 7.21]])*

**Why:** The slew rate specification directly determines the minimum tail current. This is a **large-signal** constraint (unlike the previous steps which were all small-signal).

**How slew rate works in the first stage:**

When a large step is applied to the input, one transistor in the differential pair turns off completely and the other takes all the tail current. This current charges the compensation capacitor $C_c$:

$$SR_1 = \frac{I_{D5}}{C_c}$$

This is because the entire tail current flows through one side of the pair and into $C_c$. The output voltage rate of change is limited by how fast $C_c$ can charge.

Solving for $I_{D5}$:

$$I_{D5} = SR \times C_c = 30 \times 10^6 \times 0.8 \times 10^{-12}$$

$$\boxed{I_{D5} = 24\text{ μA}}$$

**Physical meaning:** The tail current source Q5 must provide at least 24 μA. In normal (small-signal) operation, this splits equally: $I_{D1} = I_{D2} = 12$ μA. During slewing, all 24 μA goes through one transistor.

> [!note] Both Stages Must Slew
> The slew rate is limited by the *slower* of the two stages. The first stage slews $C_c$, the second stage slews $C_{L,\text{tot}}$. We must check both.

---

### Step 9 -- Second Stage Current $I_{D6} = I_{D7}$

*([[cmos_analog_ic_design_fundamentals.pdf#page=265|EB Ch. 7.2, Eq. 7.22]])*

**Why:** The second stage must also be fast enough not to be the bottleneck for slew rate.

**How slew rate works in the second stage:**

The second stage output must charge $C_{L,\text{tot}}$ through Q7 (pull-down) or Q6 (pull-up). The maximum current available is $I_{D7}$ (or $I_{D6}$), giving:

$$SR_2 = \frac{I_{D7}}{C_{L,\text{tot}}}$$

$$I_{D6} = I_{D7} = SR \times C_{L,\text{tot}} = 30 \times 10^6 \times 2.0 \times 10^{-12}$$

$$\boxed{I_{D6} = I_{D7} = 60\text{ μA}}$$

**Why is this larger than $I_{D5}$?** Because the second stage drives a larger capacitance ($C_{L,\text{tot}} = 2.0$ pF vs $C_c = 0.8$ pF). More capacitance to charge = more current needed for the same slew rate.

**Total power consumption:** $I_\text{total} = I_{D5} + I_{D6} + I_{D8} = 24 + 60 + 20 = 104$ μA from a 1.8 V supply, so $P = 1.8 \times 104\mu = 187$ μW. Very low power.

---

### Step 10 -- W/L Ratios (Transistor Sizing)

*([[cmos_analog_ic_design_fundamentals.pdf#page=265|EB Ch. 7.2]]; [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=45|Carusone Ch. 1.2.3]] for MOSFET sizing)*

**Why:** This is the final step where we convert all our electrical requirements ($g_m$, $I_D$) into physical transistor dimensions ($W$ and $L$).

**Design choices:**
- **All transistors: $L = 1$ μm.** This is a common choice. Longer $L$ gives better matching and higher $r_{ds}$ (more gain), but at the cost of speed and area. At 1 μm, $\lambda = 0.08$ V⁻¹.
- **$V_\text{eff} = 200$ mV for current sources (Q5, Q6, Q8).** This is a rule of thumb — 200 mV is a good balance between headroom and transistor size.
- **$V_\text{eff}$ for gain transistors (Q1-Q4, Q7) is set by the $g_m$ requirement.** We use $g_m = 2I_D/V_\text{eff}$ to find $V_\text{eff}$ from the known $g_m$ and $I_D$.

**The fundamental sizing equation** (from the saturation current formula, solved for $W/L$):

$$\frac{W}{L} = \frac{2\,I_D}{k' \cdot V_\text{eff}^2}$$

And the overdrive voltage from transconductance:

$$V_\text{eff} = \frac{2\,I_D}{g_m}$$

> [!note] Where Do These Come From?
> Starting from $I_D = \frac{1}{2} k' \frac{W}{L} V_\text{eff}^2$, solve for $W/L$:
> $$\frac{W}{L} = \frac{2 I_D}{k' V_\text{eff}^2}$$
>
> And from $g_m = \frac{2I_D}{V_\text{eff}}$, solve for $V_\text{eff}$:
> $$V_\text{eff} = \frac{2I_D}{g_m}$$
>
> These are the two most-used equations in MOSFET sizing. See [[Course Recap - Understanding Analog IC Design#The Three Most Important Parameters]].

---

#### Q1, Q2 (PMOS, differential pair)

**Known:** $g_{m1} = 201$ μA/V, $I_{D1} = 12$ μA, $k'_p = 70$ μA/V²

First, find $V_\text{eff}$:
$$V_{\text{eff},1} = \frac{2\,I_{D1}}{g_{m1}} = \frac{2 \times 12}{201} = 119\text{ mV}$$

This is below 200 mV, which is fine — it means the differential pair operates at moderate inversion, giving good $g_m$ per unit current.

Now find $W/L$:
$$\frac{W_1}{L} = \frac{g_{m1}}{k'_p \cdot V_{\text{eff},1}} = \frac{201}{70 \times 0.119} = \frac{201}{8.33} \approx 24$$

> [!tip] Alternative Formula
> You can equivalently use $W/L = 2I_D/(k' V_\text{eff}^2) = 2 \times 12/(70 \times 0.119^2) = 24/0.991 \approx 24$. Same answer.

---

#### Q3, Q4 (NMOS, mirror load) and Q7 (NMOS, second stage gain)

**The mirror constraint:** Q7 and Q3 are in a current mirror relationship — Q3 is the reference (diode-connected) and Q7 copies the current with a different ratio. For the mirror to work properly, they share the same $V_{GS}$, which means their $V_\text{eff}$ values are equal: $V_{\text{eff},3} = V_{\text{eff},7}$.

**Size Q7 first** (we know its requirements):

**Known:** $g_{m7} = 1005$ μA/V, $I_{D7} = 60$ μA, $k'_n = 270$ μA/V²

$$V_{\text{eff},7} = \frac{2\,I_{D7}}{g_{m7}} = \frac{2 \times 60}{1005} = 119\text{ mV}$$

(Interesting coincidence: same $V_\text{eff}$ as Q1!)

$$\frac{W_7}{L} = \frac{2 \times 60}{270 \times 0.119^2} = \frac{120}{3.82} \approx 31$$

**Now size Q3 using the mirror ratio:**

Since Q3 and Q7 have the same $V_\text{eff}$, their $W/L$ ratios scale linearly with current:

$$\frac{W_3}{L} = \frac{W_7}{L} \times \frac{I_{D3}}{I_{D7}} = 31 \times \frac{12}{60} \approx 6.2$$

Q4 = Q3 (they're a matched pair): $W_4/L = 6.2$.

> [!note] Why Mirror Q7 from Q3?
> By making Q3 the mirror reference for Q7, we ensure that Q7's bias point is well-controlled. The current in Q7 is set by the Q6 current source, while Q3 sets the gate voltage. This decouples the biasing of the two stages.

---

#### Q5 (PMOS, tail current source)

**Known:** $I_{D5} = 24$ μA, $k'_p = 70$ μA/V², $V_\text{eff} = 200$ mV (design choice)

$$\frac{W_5}{L} = \frac{2 \times 24}{70 \times 0.2^2} = \frac{48}{2.8} \approx 17$$

---

#### Q6 (PMOS, second stage current source)

**Known:** $I_{D6} = 60$ μA, $k'_p = 70$ μA/V², $V_\text{eff} = 200$ mV

$$\frac{W_6}{L} = \frac{2 \times 60}{70 \times 0.2^2} = \frac{120}{2.8} \approx 43$$

---

#### Q8 (PMOS, bias reference)

**Known:** $I_{D8} = 20$ μA (reference current). Q8 mirrors to Q5 and Q6, so we can determine $W_8/L$ from the mirror ratio with Q5:

$$\frac{W_8}{L} = \frac{W_5}{L} \times \frac{I_{D8}}{I_{D5}} = 17 \times \frac{20}{24} \approx 14$$

**Consistency check:** Does Q6 get the right current?

$$I_{D6} = \frac{W_6/L}{W_8/L} \times I_{D8} = \frac{43}{14} \times 20 = 61\text{ μA} \approx 60\text{ μA}$$

Close enough (the ~1 μA error is from rounding W/L to integers). ✓

> [!note] Why Not Size Q8 Independently?
> Q8's $W/L$ must be consistent with *both* Q5 and Q6 mirrors. We sized it from Q5 and verified Q6. If the Q6 current were way off, we'd need to adjust. In practice, you'd use non-integer $W/L$ ratios in Cadence to get exact currents.

---

## Design Summary

| Transistor | Type | Role | W/L | W (μm) | $I_D$ (μA) | $V_\text{eff}$ (mV) |
|------------|------|------|-----|---------|-------------|----------------------|
| Q1 | PMOS | Diff pair | 24 | 24 | 12 | 119 |
| Q2 | PMOS | Diff pair | 24 | 24 | 12 | 119 |
| Q3 | NMOS | Mirror load (ref) | 6.2 | 6.2 | 12 | 119 |
| Q4 | NMOS | Mirror load | 6.2 | 6.2 | 12 | 119 |
| Q5 | PMOS | Tail current src | 17 | 17 | 24 | 200 |
| Q6 | PMOS | 2nd stage current src | 43 | 43 | 60 | 200 |
| Q7 | NMOS | 2nd stage CS gain | 31 | 31 | 60 | 119 |
| Q8 | PMOS | Bias reference | 14 | 14 | 20 | 200 |

| Component | Value | Purpose |
|-----------|-------|---------|
| $C_c$ | 0.8 pF | Miller compensation (dominant pole) |
| $R_c$ (zero cancellation) | $1/g_{m7} \approx 1$ kΩ | Cancels the RHP zero from $C_c$ feedforward |

---

## Verification (Hand Calculation)

Before building anything, we verify that our design meets all specs on paper.

| Spec | How to Check | Value | Target | Meets? |
|------|-------------|-------|--------|--------|
| Open-loop GBW | $g_{m1}/C_c = 201\mu/0.8p$ | $2\pi \times 40$ MHz | -- | -- |
| Closed-loop BW | $\beta \times GBW = 0.5 \times 40$ | $2\pi \times 20$ MHz | 20 MHz | ✓ |
| $\omega_{p2}$ | $g_{m7}/C_{L,\text{tot}} = 1005\mu/2p$ | $4\,\omega_t = 2\pi \times 80$ MHz | $\geq 4\,\omega_t$ | ✓ |
| $\omega_z$ | $g_{m7}/C_c = 1005\mu/0.8p$ | $10\,\omega_t = 2\pi \times 200$ MHz | $10\,\omega_t$ | ✓ |
| PM | $90° - \arctan(1/4) - \arctan(1/10)$ | **70.3°** | $\geq 70°$ | ✓ |
| SR (1st stage) | $I_{D5}/C_c = 24\mu/0.8p$ | **30 V/μs** | $\geq 30$ V/μs | ✓ |
| SR (2nd stage) | $I_{D7}/C_{L,\text{tot}} = 60\mu/2p$ | **30 V/μs** | $\geq 30$ V/μs | ✓ |

All specifications met in the hand calculation. ✓

---

## Lead Compensation (Optional Enhancement)

*([[cmos_analog_ic_design_fundamentals.pdf#page=265|EB Ch. 7.2]]; [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278|Carusone Ch. 6.3]])*

**The problem:** The compensation capacitor $C_c$ creates a feedforward path from the first-stage output directly to the opamp output. At high frequencies, the signal goes *through* $C_c$ instead of being amplified by Q7. This creates a **right-half-plane (RHP) zero** at:

$$\omega_z = \frac{g_{m7}}{C_c}$$

An RHP zero adds phase lag (just like a pole), which is bad for stability.

**The solution:** Add a resistor $R_c$ in series with $C_c$. This blocks the high-frequency feedforward.

### Option 1: Zero Cancellation ($R_c = 1/g_{m7}$)

Setting $R_c = 1/g_{m7} \approx 995\;\Omega \approx 1\;\text{k}\Omega$ pushes the zero to infinity. The modified zero frequency is:

$$\omega_z' = \frac{1}{C_c(1/g_{m7} - R_c)}$$

When $R_c = 1/g_{m7}$, the denominator is zero, so $\omega_z' \to \infty$. The zero effectively disappears.

With the zero gone, the PM improves from 70.3° to about 76° ($90° - \arctan(1/4) = 90° - 14° = 76°$).

### Option 2: Pole-Zero Cancellation ($R_c > 1/g_{m7}$)

If $R_c > 1/g_{m7}$, the zero moves to the **left half-plane**, which adds positive phase (helpful!). We can place this LHP zero exactly at $\omega_{p2}$ to cancel the second pole:

$$R_c = \frac{1}{g_{m7}} + \frac{1}{\omega_{p2} \cdot C_c} = 995 + \frac{1}{5.03 \times 10^8 \times 0.8 \times 10^{-12}} = 995 + 2486 \approx 3.5\text{ kΩ}$$

This cancels the second pole entirely, leaving only the dominant pole. PM approaches 90°.

> [!tip] In Practice
> In the SPICE simulation below, we use $R_c = 995\;\Omega$ (zero cancellation). In Cadence with real transistor models, you would tune $R_c$ by simulation to hit exactly 70° PM.

---

## SPICE Simulation Results

> [!info] Simulation Setup
> - **Tool:** ngspice 41 via PySpice (Level 1 MOSFET models)
> - **Source:** `SPICEPilot/examples/3_34655_opamp/`
> - **Files:** `two_stage_opamp_34655.cir` (netlist), `two_stage_opamp_34655.py` (PySpice)

### DC Operating Point

The DC operating point shows where each node sits with no input signal. All transistors should be in saturation.

| Node            | Voltage | Description            | Why This Value                                                                                                     |
| --------------- | ------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `vout`          | 0.771 V | Output quiescent point | Set by the balance of Q6 (pull-up) and Q7 (pull-down). Ideally mid-rail (0.9 V); the offset is due to finite gain. |
| `n_bias`        | 1.153 V | PMOS bias rail         | $V_{DD} -V_{GS,Q8}= 1.8 - 0.647 = 1.153$ V. This voltage is shared by all PMOS current source gates.               |
| `n_tail`        | 0.768 V | Diff pair tail         | Set by Q5's drain voltage. Must be high enough for Q1, Q2 to stay in saturation.                                   |
| `n_d1` = `n_d2` | 0.619 V | First stage output     | Balanced (equal) because no differential input. Must be $> V_\text{eff,Q3}$ for Q3/Q4 to be in saturation.         |


### Open-Loop AC Analysis

| Parameter | Simulated | Hand Calc | Status |
|-----------|-----------|-----------|--------|
| DC Gain | **81.5 dB** (11,904 V/V) | ~93 dB | Lower — see discussion below |
| GBW | **40.3 MHz** | 40 MHz | ✓ |
| UGF | **37.2 MHz** | ~40 MHz | ✓ |
| Phase Margin | **67.1°** | 70.3° | Slightly low — see discussion below |

> [!warning] Phase Margin & DC Gain Discrepancy
> The simulated PM (67.1°) is ~3° below the 70° target, and DC gain is 81.5 dB vs ~93 dB.
>
> **Root cause:** The hand calculation for DC gain assumes infinite output resistance at each stage. The actual DC gain is:
> $$A_0 = g_{m1}(r_{ds2} \| r_{ds4}) \times g_{m7}(r_{ds6} \| r_{ds7})$$
>
> With $\lambda = 0.08$ V⁻¹, the $r_{ds}$ values are finite and significantly reduce the gain. For example, $r_{ds,Q7} = 1/(0.08 \times 60\mu) = 208\;\text{k}\Omega$, not infinity.
>
> The lower DC gain means the dominant pole is at a higher frequency than expected, which shifts the unity-gain crossover and reduces the phase margin by ~3°.
>
> **Fix:** Increase $R_c$ from 995 Ω to ~3.5 kΩ to add a LHP zero that recovers the lost phase. In Cadence with X-FAB process models, this would be tuned by simulation.

### Closed-Loop AC Analysis

| Parameter | Simulated | Target | Status |
|-----------|-----------|--------|--------|
| Midband Gain | **6.01 dB** (gain = 2.0) | 6 dB | ✓ |
| $-3$ dB BW | **~20 MHz** | 20 MHz | ✓ |

The closed-loop gain is almost exactly 2.0 (6.01 dB ≈ 6.02 dB), confirming that the feedback network works correctly. The bandwidth matches the 20 MHz target.

### Transient (Slew Rate)

| Parameter | Simulated | Target | Status |
|-----------|-----------|--------|--------|
| Slew Rate | **32.2 V/μs** | $\geq 30$ V/μs | ✓ |

The measured slew rate exceeds the target by ~7%. The small margin above 30 V/μs comes from rounding up currents during the design.

### Bode & Step Response

![[opamp_34655_results.png]]

The four plots show:
1. **Open-loop gain** (top left): Starts at ~81.5 dB, rolls off at -20 dB/decade (single-pole behavior from Miller compensation), crosses 0 dB at ~37 MHz.
2. **Open-loop phase** (top right): Starts near 0°, drops through -90° (dominant pole), continues toward -180°. At the 0 dB crossing, phase is about -113°, giving PM = 180° - 113° = 67°.
3. **Closed-loop gain** (bottom left): Flat at 6 dB up to ~20 MHz, then rolls off.
4. **Step response** (bottom right): Output follows input with gain = 2, with clean slewing behavior and minimal ringing (consistent with 67° PM).

### How to Run

> [!tip] Simulation Files
> Located in `DTU/SPICEPilot/examples/3_34655_opamp/`

**Method 1 -- Double-click (ngspice only)**

Navigate to the folder and double-click `RUN.bat`. Prints DC operating point, gain, UGF, and phase to the console.

**Method 2 -- Terminal (full analysis + plots)**

```
cd ~/DTU/SPICEPilot/examples/3_34655_opamp && /c/Users/Mads2/miniconda3/python.exe two_stage_opamp_34655.py
```

Runs open-loop AC, closed-loop AC, and transient analyses. Saves a 4-panel plot to `opamp_34655_results.png`.

**Method 3 -- ngspice interactive**

```
cd ~/DTU/SPICEPilot/examples/3_34655_opamp && /c/Users/Mads2/miniconda3/Library/bin/ngspice_con.exe two_stage_opamp_34655.cir
```

> [!note] Prerequisites
> ngspice and PySpice are installed via conda (`conda install -c conda-forge ngspice` + `pip install PySpice`).

---

## Book References

> [!tip] Clickable Links
> Every chapter reference below is a clickable link that opens the PDF at the correct page.

| Topic | Carusone | Bruun (EB) |
|-------|----------|------------|
| MOSFET fundamentals | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=38\|Ch. 1.2 (p. 38)]], [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=53\|Table 1.5 (p. 53)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=12\|Ch. 1 (p. 11)]], [[cmos_analog_ic_design_fundamentals.pdf#page=20\|Ch. 2 (p. 19)]] |
| Small-signal model | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=49\|Ch. 1.2.6 (p. 49)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=73\|Ch. 3.5 (p. 72)]] |
| Current mirrors | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=142\|Ch. 3.1 (p. 142)]], [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=153\|Ch. 3.6 Cascode (p. 153)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=279\|Ch. 8.1 (p. 278)]] |
| Differential pair | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=159\|Ch. 3.8 (p. 159)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=133\|Ch. 4.4 (p. 132)]] |
| Common-source stage | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=144\|Ch. 3.2 (p. 144)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=108\|Ch. 4.1 (p. 107)]] |
| Two-stage opamp topology | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=266\|Ch. 6.1 (p. 266)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=258\|Ch. 7 (p. 257)]] |
| Miller compensation | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278\|Ch. 6.2 (p. 278)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=261\|Ch. 7.2 (p. 260)]] |
| RHP zero and $R_c$ | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=279\|Ch. 6.2.2 (p. 279)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=261\|Ch. 7.2 (p. 260)]] |
| Feedback theory & phase margin | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=228\|Ch. 5.1 (p. 228)]], [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=235\|Ch. 5.2.2 PM (p. 235)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=202\|Ch. 6 (p. 201)]], [[cmos_analog_ic_design_fundamentals.pdf#page=239\|Ch. 6.6 Compensation (p. 238)]] |
| Slew rate | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=273\|Ch. 6.1.3 (p. 273)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=265\|Ch. 7.3 (p. 264)]] |
| Transistor sizing ($W/L$) | [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=45\|Ch. 1.2.3 (p. 45)]] | [[cmos_analog_ic_design_fundamentals.pdf#page=57\|Ch. 3.3 (p. 56)]] |

**Full book titles:**
- **Carusone**: Tony Chan Carusone, David Johns, Kenneth Martin — *[[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf|Analog Integrated Circuit Design]]*, 2nd ed., Wiley.
- **Bruun (EB)**: Erik Bruun — *[[cmos_analog_ic_design_fundamentals.pdf|CMOS Analog IC Design: Fundamentals]]* (free supplementary text for 34655).
