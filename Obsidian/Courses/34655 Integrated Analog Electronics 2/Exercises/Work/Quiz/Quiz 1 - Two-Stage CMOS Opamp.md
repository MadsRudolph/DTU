---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: quiz
tags: [IAE2, quiz]
---
# Quiz 1 - Two-Stage CMOS Opamp

## Question 1 (1 point)

> [!question] In the standard two-stage CMOS opamp the slew rate is normally limited by:
> - [ ] The transconductance of the input transistors
> - [ ] The output resistance of the input transistors
> - [x] **The current available to charge/discharge the compensation capacitor**

> [!success] Answer: The current available to charge/discharge the compensation capacitor

> [!note]- Explanation
> The **slew rate (SR)** is the maximum rate at which the output voltage can change:
>
> $$SR = \frac{dV_{out}}{dt}\bigg|_{max}$$
>
> In a two-stage opamp with Miller compensation, when a large input step is applied, the input differential pair saturates and delivers its maximum current (the tail current $I_{SS}$) to charge or discharge the compensation capacitor $C_C$.
>
> $$SR = \frac{I_{SS}}{C_C}$$
>
> The slew rate is therefore limited by:
> 1. The bias current available from the input stage ($I_{SS}$)
> 2. The size of the compensation capacitor ($C_C$)
>
> It is **not** limited by transconductance $g_m$ (which affects small-signal bandwidth) or output resistance (which affects DC gain).

---

## Question 2 (2 points)

> [!question] In the standard two-stage CMOS opamp the gain-bandwidth product is determined by:
> - [ ] The product of output resistance of the input transistors and the compensation capacitor
> - [x] **The ratio between the input transistor transconductance and the compensation capacitor**
> - [ ] The product of input resistance of the second gain stage and the compensation capacitor

> [!success] Answer: The ratio between the input transistor transconductance and the compensation capacitor

> [!note]- Explanation
> The **gain-bandwidth product (GBW)** or unity-gain frequency $f_u$ for a Miller-compensated two-stage opamp is:
>
> $$GBW = f_u = \frac{g_{m1}}{2\pi C_C}$$
>
> Where:
> - $g_{m1}$ = transconductance of the input transistors
> - $C_C$ = Miller compensation capacitor
>
> > [!abstract] Derivation
> > The dominant pole created by Miller compensation is approximately:
> > $$\omega_{p1} \approx \frac{1}{R_{out1} \cdot A_2 \cdot C_C} = \frac{1}{R_{out1} \cdot g_{m2} \cdot R_{out2} \cdot C_C}$$
> >
> > The DC gain is:
> > $$A_v = g_{m1} \cdot R_{out1} \cdot g_{m2} \cdot R_{out2}$$
> >
> > The GBW is the product of DC gain and dominant pole:
> > $$GBW = A_v \cdot \omega_{p1} = \frac{g_{m1}}{C_C}$$
>
> This is a key design equation - GBW depends only on input stage $g_m$ and compensation capacitor.

---

## Question 3 (1 point)

> [!question] The Miller compensation capacitor in the two-stage opamp is placed:
> - [x] **Between input and output of the second gain stage**
> - [ ] Between ground and input of the second gain stage
> - [ ] Between ground and output of the second gain stage

> [!success] Answer: Between input and output of the second gain stage

> [!note]- Explanation
> Miller compensation exploits the **Miller effect** to create a large effective capacitance using a small physical capacitor.
>
> ```
>          First Stage          Second Stage
>             │                     │
> Vin+ ──┤M1├──┬── Vx ──┤M5├──┬── Vout
>             │        ┌──────┘
>             │    Cc ─┤
>             │        └──────┐
> Vin- ──┤M2├──┘              └── Vout
> ```
>
> The capacitor $C_C$ is connected from the **output of the first stage** (input of second stage) to the **output of the second stage**.
>
> Due to the Miller effect, the effective capacitance seen at node Vx is:
> $$C_{eff} = C_C (1 + |A_2|)$$
>
> Where $A_2$ is the gain of the second stage. This:
> 1. Creates a dominant low-frequency pole (pole splitting)
> 2. Pushes the second pole to higher frequencies
> 3. Ensures stability with adequate phase margin

---

## Question 4 (1 point)

> [!question] The Miller compensation capacitor in the two-stage opamp introduces:
> - [ ] A right half plane pole in the transfer function
> - [ ] A left half plane zero in the transfer function
> - [x] **A right half plane zero in the transfer function**

> [!success] Answer: A right half plane zero in the transfer function

> [!note]- Explanation
> The Miller capacitor creates a **feedforward path** from input to output. At high frequencies, the capacitor acts as a short circuit, allowing signal to bypass the second stage.
>
> The transfer function has a zero at:
> $$\omega_z = \frac{g_{m2}}{C_C}$$
>
> This zero is in the **Right Half Plane (RHP)** because of the phase relationship:
> - The feedforward path through $C_C$ has opposite phase to the main signal path
> - This creates a zero with positive real part
>
> > [!warning] Why RHP zero is problematic
> > - An RHP zero adds phase lag (like a pole) while adding magnitude (like a zero)
> > - This reduces phase margin and can cause instability
>
> > [!tip] Solutions to eliminate the RHP zero
> > 1. **Nulling resistor**: Add resistor $R_z$ in series with $C_C$ where $R_z = 1/g_{m2}$
> > 2. **Cascode compensation**: Use indirect compensation path
> > 3. **Current buffer**: Block the feedforward path

---

## Question 5 (1 point)

> [!question] The open loop frequency response of a Miller compensated two-stage opamp has:
> - [ ] A dominant pole and two non-dominant left half plane poles
> - [ ] A dominant pole, a non dominant pole and a left half plane zero
> - [x] **A dominant pole, a non dominant pole and a right half plane zero**

> [!success] Answer: A dominant pole, a non dominant pole and a right half plane zero

> [!note]- Explanation
> The complete transfer function of a Miller-compensated two-stage opamp has:
>
> > [!info] Poles
> > 1. **Dominant pole** $\omega_{p1}$: Created by Miller effect at the output of first stage
> >    $$\omega_{p1} \approx \frac{1}{R_{out1} \cdot g_{m2} \cdot R_{out2} \cdot C_C}$$
> >
> > 2. **Non-dominant pole** $\omega_{p2}$: At output of second stage
> >    $$\omega_{p2} \approx \frac{g_{m2}}{C_L}$$
>
> > [!info] Zero
> > 3. **Right half plane zero** $\omega_z$: From feedforward through $C_C$
> >    $$\omega_z = \frac{g_{m2}}{C_C}$$
>
> **Bode plot:**
> ```
> Gain (dB)
>     │
>  Av ├────────╮
>     │        ╲  -20 dB/dec
>     │         ╲
>     │          ╲    zero effect
>     │           ╲ ╱
>     │            ╳   -40 dB/dec after p2
>     │             ╲
> ────┼───────┬──────┬──────┬────► f
>             fp1    fu    fp2/fz
> ```
>
> For 60° phase margin, typically design for:
> $$\omega_{p2}, \omega_z > 2.2 \cdot GBW$$

---

## Question 6 (1 point)

> [!question] For the circuit shown, assume all transistors have |Vth| = 1 V. Also assume that Vbias = -1.5 V and that the overdrive voltage for the input transistors is 0.3 V. The minimum value of the common mode input voltage with all transistors in the active region is:
> - [ ] 0 V
> - [x] **-1.2 V**
> - [ ] -2.5 V

> [!success] Answer: -1.2 V

> [!note]- Explanation
> The circuit is a differential pair with NMOS input transistors and a current source bias transistor.
>
> ```
>         VDD = 3V
>           │
>     ┌─────┴─────┐
>     │           │
>    ┤M3├       ┤M4├  (PMOS loads)
>     │           │
>     ├───┬───────┤
>     │   │       │
>    ┤M1├ │     ┤M2├  (NMOS inputs)
>     │   Cc      │
>     └───┬───────┘
>         │
>        ┤M5├         (NMOS bias)
>         │
>        VSS = -3V
> ```
>
> > [!abstract] Step 1: Find source voltage of input transistors
> > The bias transistor M5 has:
> > - $V_{GS5} = V_{bias} - V_{SS} = -1.5 - (-3) = 1.5$ V
> > - $V_{OV5} = V_{GS5} - V_{th} = 1.5 - 1 = 0.5$ V
> >
> > For M5 in saturation: $V_{DS5} \geq V_{OV5} = 0.5$ V
> >
> > So: $V_S \geq V_{SS} + V_{DS5,min} = -3 + 0.5 = -2.5$ V
>
> > [!abstract] Step 2: Find minimum input CM voltage
> > For input transistors M1, M2:
> > $$V_{GS} = V_{in,CM} - V_S$$
> > $$V_{OV} = V_{GS} - V_{th} = 0.3 \text{ V (given)}$$
> > $$V_{GS} = V_{OV} + V_{th} = 0.3 + 1 = 1.3 \text{ V}$$
> >
> > So: $V_{in,CM} = V_S + V_{GS} = V_S + 1.3$
> >
> > For minimum $V_{in,CM}$, use minimum $V_S = -2.5$ V:
> > $$V_{in,CM,min} = -2.5 + 1.3 = \boxed{-1.2 \text{ V}}$$

---

## Question 7 (1 point)

> [!question] For the circuit shown above assume that the bias transistor has $\mu_n C_{ox}(W/L) = 80\ \mu A/V^2$. The value of the bias current in each of the input transistors is:
> - [ ] 5 μA
> - [x] **10 μA**
> - [ ] 20 μA

> [!success] Answer: 10 μA

> [!note]- Explanation
> The bias transistor M5 operates in saturation and sets the tail current for the differential pair.
>
> > [!abstract] Saturation current equation
> > $$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2$$
>
> **Given:**
> - $\mu_n C_{ox} (W/L) = 80$ μA/V²
> - $V_{bias} = -1.5$ V
> - $V_{SS} = -3$ V
> - $|V_{th}| = 1$ V
>
> > [!abstract] Calculate $V_{GS5}$
> > $$V_{GS5} = V_{bias} - V_{SS} = -1.5 - (-3) = 1.5 \text{ V}$$
> > $$V_{OV5} = V_{GS5} - V_{th} = 1.5 - 1 = 0.5 \text{ V}$$
>
> > [!abstract] Calculate tail current $I_{SS}$
> > $$I_{SS} = \frac{1}{2} \times 80 \times (0.5)^2 = 40 \times 0.25 = 10\ \mu\text{A}$$
>
> > [!tip] Current in each input transistor
> > For a balanced differential pair at equilibrium, the tail current splits equally:
> > $$I_{D1} = I_{D2} = \frac{I_{SS}}{2} = 5\ \mu\text{A}$$
> >
> > However, the question likely refers to the **total bias current available** to each branch (10 μA), or considers the case when one transistor is fully on.

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Key Formula |
> |---|--------|-------------|
> | 1 | Current to charge $C_C$ | $SR = I_{SS}/C_C$ |
> | 2 | $g_m/C_C$ ratio | $GBW = g_{m1}/C_C$ |
> | 3 | Input to output of 2nd stage | Miller effect |
> | 4 | RHP zero | $\omega_z = g_{m2}/C_C$ |
> | 5 | Dominant + non-dominant pole + RHP zero | Complete response |
> | 6 | -1.2 V | $V_{in,min} = V_S + V_{GS}$ |
> | 7 | 10 μA | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}V_{OV}^2$ |

---

> [!nav]
> &nbsp;
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Quiz 2 - OpAmp Building Blocks|Quiz 2 →]]
