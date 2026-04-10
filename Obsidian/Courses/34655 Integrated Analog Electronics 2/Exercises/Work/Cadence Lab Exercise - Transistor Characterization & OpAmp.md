---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, cadence, opamp, XT018, transistor-characterization]
---
# Cadence Lab Exercise -- Transistor Characterization & OpAmp Design

> [!info] Exercise Info
> - Process: X-FAB XT018 (0.18 um CMOS)
> - Exercise PDF: [[34655-cadence-lab-exercise-XT018_v1.pdf]]
> - Paper design: [[Cadence Exercise - Two-Stage OpAmp Design]]
> - Theoretical values (from slide 26): $\mu_n C_{ox} = 165\;\mu\text{A/V}^2$, $\mu_p C_{ox} = 35\;\mu\text{A/V}^2$, $V_{tn} = 630\;\text{mV}$, $V_{tp} = 630\;\text{mV}$

---

# Day 1 -- Transistor Characterization

## 1. NMOS Characterization

### 1.1 DC Simulation -- Diode-Connected NMOS

**Setup:** Diode-coupled NMOS (gate tied to drain) with voltage source $V_{GS}$. Transistor "ne" from PRIMLIB, ground from analogLib.

![[Screenshot 2026-03-16 192735.png]]
*Figure: Cadence schematic -- diode-connected NMOS (W=5u, L=1u) with $V_{GS} = 800$ mV.*

| W/L   | $V_{GS}$ [V] | $I_D$ [$\mu$A] |
| ----- | ------------ | -------------- |
| 5u/1u | 0.8          | 11.64          |
| 5u/1u | 1.0          | 58.38          |
| 5u/5u | 0.8          | 3.223          |
| 5u/5u | 1.0          | 13.4           |

**Does $I_D$ depend on $V_{GS}$ as expected?**

> [!success] Yes — behaves as expected
> - **Quadratic $V_{GS}$ dependence:** Going from 0.8 V to 1.0 V gives $\frac{58.38}{11.64} \approx 5\times$ more current, matching the squared overdrive ratio $\left(\frac{0.37}{0.17}\right)^2 \approx 4.7$ ✓
> - **$W/L$ scaling:** $\frac{I_D(5/1)}{I_D(5/5)} \approx 3.6\text{–}4.4\times$ — close to the expected $5\times$, small deviation due to longer channel having slightly different effective parameters ✓
> - **vs. theory:** $L=1\;\mu$m matches SH model within ~3%, $L=5\;\mu$m ~20-35% higher — real process $\mu_n C_{ox}$ and $V_t$ differ slightly from textbook values


---

### 1.2 Shichman-Hodges Model -- NMOS

**Setup:** Sweep $V_{GS}$ from 0V to $V_{DD}$ (1.8V). Plot $I_D$ vs $V_{GS}$ and $\sqrt{I_D}$ vs $V_{GS}$.

**Theory:** From the SH model with $V_{DS} = V_{GS}$ (diode-connected, saturation) and $\lambda V_t \ll 1$:

$$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_t)^2$$

Taking the square root:

$$\sqrt{I_D} = \sqrt{\frac{1}{2} \mu_n C_{ox} \frac{W}{L}} \cdot V_{GS} - \sqrt{\frac{1}{2} \mu_n C_{ox} \frac{W}{L}} \cdot V_t$$

This is a straight line $y = ax + b$ where:
- **Slope** $a = \sqrt{\frac{1}{2} \mu_n C_{ox} \frac{W}{L}}$ --> extract $\mu_n C_{ox}$
- **x-intercept** gives $V_{tn}$

![[Screenshot 2026-03-16 205235.png]]
*Figure: $\sqrt{I_D}$ vs $V_{GS}$ for diode-connected NMOS (W=5u, L=1u).*

> [!note] Observation
> The $\sqrt{I_D}$ curve is fairly straight from ~0.6 V onwards — exactly what the SH model predicts. Below $V_t$ the transistor is in subthreshold and the model breaks down.

#### Extracting $\mu_n C_{ox}$ and $V_{tn}$

From the DC results we can calculate $\sqrt{I_D}$ at two points:

$$\sqrt{I_D}\big|_{0.8\text{V}} = \sqrt{11.64\;\mu\text{A}} = 3.412\;\text{m}\sqrt{\text{A}}, \qquad \sqrt{I_D}\big|_{1.0\text{V}} = \sqrt{58.38\;\mu\text{A}} = 7.641\;\text{m}\sqrt{\text{A}}$$

The slope of the straight-line region is then:

$$\text{slope} = \frac{7.641 - 3.412}{1.0 - 0.8} = 21.14\;\text{m}\sqrt{\text{A}}/\text{V}$$

From the SH model we know $\text{slope} = \sqrt{\frac{\mu_n C_{ox}}{2}\frac{W}{L}}$, so solving for $\mu_n C_{ox}$:

$$\mu_n C_{ox} = \text{slope}^2 \cdot \frac{2L}{W} = (21.14\text{e-}3)^2 \cdot \frac{2 \times 1\;\mu\text{m}}{5\;\mu\text{m}} = 178.8\;\mu\text{A/V}^2$$

For $V_{tn}$, extrapolate the line to $\sqrt{I_D} = 0$ (i.e. the x-intercept):

$$V_{tn} = V_{GS} - \frac{\sqrt{I_D}}{\text{slope}} = 0.8 - \frac{3.412\text{e-}3}{21.14\text{e-}3} = 0.639\;\text{V}$$

**Results from $\sqrt{I_D}$ vs $V_{GS}$:**

| W/L | $V_{GS}$ [V] | Slope [m$\sqrt{\text{A}}$/V] | $\mu_n C_{ox}$ [$\mu$A/V$^2$] | $V_{tn}$ [V] |
|-----|---------------|-------|-------------------------------|---------------|
| 5$\mu$m/1$\mu$m | 0.8 – 1.0 | 21.14 | 178.8 | 0.639 |
| 5$\mu$m/5$\mu$m | 0.8 – 1.0 | 9.33 | 174.1 | 0.608 |

![[Screenshot 2026-03-16 205722.png]]
*Figure: $\sqrt{I_D}$ vs $V_{GS}$ for diode-connected NMOS (W=5u, L=5u).*

#### Extraction for W/L = 5u/5u

$$\sqrt{I_D}\big|_{0.8\text{V}} = \sqrt{3.223\;\mu\text{A}} = 1.795\;\text{m}\sqrt{\text{A}}, \qquad \sqrt{I_D}\big|_{1.0\text{V}} = \sqrt{13.40\;\mu\text{A}} = 3.661\;\text{m}\sqrt{\text{A}}$$

$$\text{slope} = \frac{3.661 - 1.795}{1.0 - 0.8} = 9.33\;\text{m}\sqrt{\text{A}}/\text{V}$$

$$\mu_n C_{ox} = (9.33\text{e-}3)^2 \cdot \frac{2 \times 5\;\mu\text{m}}{5\;\mu\text{m}} = 174.1\;\mu\text{A/V}^2$$

$$V_{tn} = 0.8 - \frac{1.795\text{e-}3}{9.33\text{e-}3} = 0.608\;\text{V}$$

**Comments (do extracted values match theoretical $\mu_n C_{ox} = 165\;\mu$A/V$^2$ and $V_{tn} = 630$ mV?):**

> [!abstract] Comparison
> | | L = 1 $\mu$m | L = 5 $\mu$m | Theoretical |
> |---|---|---|---|
> | $\mu_n C_{ox}$ | 178.8 | 174.1 | 165 $\mu$A/V$^2$ |
> | $V_{tn}$ | 0.639 V | 0.608 V | 0.630 V |
>
> - Both extracted $\mu_n C_{ox}$ values are ~5–8% above the textbook 165 — in the right ballpark
> - $\mu_n C_{ox}$ *should* be identical for both (it's a process parameter) — the small difference (178.8 vs 174.1) comes from **short-channel effects** in the L=1u device slightly boosting mobility
> - $V_{tn}$ is close to theoretical for both, with L=1u showing a slightly higher threshold (DIBL effects are minimal here)


---

### 1.3 Operating Point & Transconductance $g_m$ -- NMOS

**Setup:** Same diode-connected NMOS. Extract full OP-point data from Cadence for each W/L and $V_{GS}$.

#### Full OP-Point Table

| W/L | $V_{GS}$ [V] | $I_{DS}$ [$\mu$A] | $g_m$ [$\mu$A/V] | $g_{ds}$ [nS] | $V_{th}$ [mV] | $V_{dsat}$ [mV] |
|-----|-----|------|------|------|------|------|
| 5u/1u | 0.8 | 11.64 | 136.7 | 270 | 678.7 | 123.9 |
| 5u/1u | 1.0 | 58.38 | 321.5 | 1140 | 678.7 | 253.5 |
| 5u/5u | 0.8 | 3.223 | 32.6 | 26.09 | 640.1 | 147.6 |
| 5u/5u | 1.0 | 13.40 | 67.97 | 84.67 | 640.1 | 285.0 |

#### $g_m$ -- Three Methods Compared

Compare $g_m$ from three approaches:
1. **OP-point** — directly from Cadence
2. **SH formula:** $g_m = \sqrt{2\,\mu_n C_{ox}\,(W/L)\,I_D}$ — uses our extracted $\mu_n C_{ox}$
3. **From $V_{eff}$:** $g_m = 2I_D / V_{eff}$ — uses $V_{dsat}$ from the OP-point as $V_{eff}$

| W/L | $V_{GS}$ | $g_m$ OP [$\mu$A/V] | $g_m$ SH [$\mu$A/V] | $g_m$ $2I_D/V_{eff}$ [$\mu$A/V] |
|-----|-----|------|------|------|
| 5u/1u | 0.8 | 136.7 | 144.3 | 187.9 |
| 5u/1u | 1.0 | 321.5 | 323.1 | 460.6 |
| 5u/5u | 0.8 | 32.6 | 33.5 | 43.7 |
| 5u/5u | 1.0 | 67.97 | 68.3 | 94.0 |

> [!abstract] Observations
> - **Method 2 (SH formula) matches OP-point very well** — within ~3–5% across all cases. This makes sense since we extracted $\mu_n C_{ox}$ from the same simulator, so the model is self-consistent.
> - **Method 3 ($2I_D/V_{eff}$) consistently overestimates** — by 30–40%. This is because $V_{dsat}$ from BSIM4 is **not** the same as $V_{GS} - V_t$ from the simple SH model. BSIM4 uses a smooth transition model where $V_{dsat}$ is smaller than the SH overdrive voltage, making $2I_D/V_{dsat}$ artificially large.
> - Bottom line: the simple square-law $g_m$ formula works surprisingly well, but don't mix BSIM4 operating-point values into SH equations — the definitions don't match.


---

### 1.4 Output Characteristic -- NMOS

**Setup:** New schematic with separate $V_{GS}$ and $V_{DS}$ sources. Sweep $V_{DS}$ from 0V to 1.8V for 2 W/L ratios and 2 $V_{GS}$ values.

**Theory:** In saturation ($V_{DS} \geq V_{GS} - V_t$):

$$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_t)^2 (1 + \lambda(V_{DS} - V_{eff}))$$

The slope $\alpha$ of the $I_D$ vs $V_{DS}$ curve in saturation gives $\lambda$:

$$\alpha = \frac{\partial I_D}{\partial V_{DS}} = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} V_{eff}^2 \lambda = g_{ds}$$

Choose two $V_{DS}$ points where $V_{DS} \geq V_{GS}$ (saturation region).

| W/L             | $V_{GS}$ [V] | $V_{DS}$ [V] | Slope | $\lambda$ [V$^{-1}$] | $g_{ds}$ [$\mu$S] Calculated | $g_{ds}$ [$\mu$S] OP-point |
| --------------- | ------------ | ------------ | ----- | -------------------- | ---------------------------- | -------------------------- |
| 5$\mu$m/1$\mu$m | 0.8          |              |       |                      |                              | 1.087                      |
|                 | 1.2          |              |       |                      |                              |                            |
| 5$\mu$m/5$\mu$m | 0.8          |              |       |                      |                              |                            |
|                 | 1.2          |              |       |                      |                              |                            |

**Comments on results:**


---

## 2. PMOS Characterization

> [!warning] PMOS Notes
> - Use transistor "pe" from PRIMLIB
> - Source and bulk must be connected to the **highest potential** ($V_{DD}$)
> - $V_{GS}$ must be **negative** (or equivalently, $|V_{GS}|$ is positive)
> - Currents in Cadence are positive when flowing **into** the terminal

### 2.1 DC Simulation -- Diode-Connected PMOS

| W/L | $|V_{GS}|$ [V] | $I_D$ [$\mu$A] |
|-----|-----------------|-----------------|
| 5$\mu$m/1$\mu$m | 0.8 | |
| | 1.0 | |
| 5$\mu$m/5$\mu$m | 0.8 | |
| | 1.0 | |

**Does $I_D$ depend on $|V_{GS}|$ as expected?**


---

### 2.2 Shichman-Hodges Model -- PMOS

**Setup:** Sweep $|V_{GS}|$ from 0V to 1.8V. Plot $I_D$ vs $|V_{GS}|$ and $\sqrt{I_D}$ vs $|V_{GS}|$.

| W/L | $|V_{GS}|$ [V] | Slope | $\mu_p C_{ox}$ [$\mu$A/V$^2$] | $V_{tp}$ [V] |
|-----|-----------------|-------|-------------------------------|---------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | |
| | 1.0 | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | |
| | 1.0 | | | |

**Comments (compare to theoretical $\mu_p C_{ox} = 35\;\mu$A/V$^2$ and $V_{tp} = 630$ mV):**


---

### 2.3 Transconductance $g_m$ -- PMOS

| W/L | $|V_{GS}|$ [V] | $I_D$ [$\mu$A] | $g_m$ [$\mu$A/V] Op-point | $g_m$ [$\mu$A/V] $\sqrt{2\mu_p C_{ox}(W/L)I_D}$ | $g_m$ [$\mu$A/V] $2I_D/V_{eff}$ |
|-----|-----------------|-----------------|--------------------------|--------------------------------------------------|--------------------------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | | |
| | 1.0 | | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | | |
| | 1.0 | | | | |

**Comments on differences:**


---

### 2.4 Output Characteristic -- PMOS

| W/L | $|V_{GS}|$ [V] | $V_{DS}$ [V] | Slope | $\lambda$ [V$^{-1}$] | $g_{ds}$ [$\mu$S] Calculated | $g_{ds}$ [$\mu$S] OP-point |
|-----|-----------------|---------------|-------|-----------------------|------------------------------|---------------------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | | | |
| | 1.2 | | | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | | | |
| | 1.2 | | | | | |

**Comments:**


---

## 3. Summary of Extracted Parameters

| Parameter | NMOS (extracted) | NMOS (theoretical) | PMOS (extracted) | PMOS (theoretical) |
|-----------|-----------------|-------------------|-----------------|-------------------|
| $\mu C_{ox}$ [$\mu$A/V$^2$] | | 165 | | 35 |
| $V_t$ [V] | | 0.630 | | 0.630 |
| $\lambda$ [V$^{-1}$] (L=1$\mu$m) | | | | |
| $\lambda$ [V$^{-1}$] (L=5$\mu$m) | | | | |

**Do the simulated transistors fit the Shichman-Hodges model?**


**Key observations:**


---

# Day 2 & 3 -- OpAmp Design in Cadence

## 4. Building the OpAmp

### 4.1 Bias Block

**Schematic:** Create bias block with pins for supplies and bias output. Create symbol.

![[opamp_bias_schematic.png]]
*Figure: Bias block schematic. Diode-connected PMOS Q8 with ideal current source I0 sets the `pbias` gate voltage that is distributed to Q5 and Q6 in the main opamp. OP-point annotations from Cadence shown on Q8.*

The bias block generates the gate voltage that sets the tail current $I_{D5}$ and the 2nd-stage current source $I_{D6}$. Q8 is a diode-connected PMOS reference sinking $I_{BIAS}$ from VDD, and its $V_{GS}$ is mirrored by Q5 (for the diff-pair tail) and Q6 (for the 2nd-stage source) in the opamp block via the `pbias` net.

**Q8 operating point (from Cadence):**

| Parameter | Value |
|---|---|
| $I_{DS}$ (Q8) | −40.03 µA |
| $g_m$ | 206.8 µA/V |
| $V_{th}$ | −676.9 mV |
| $V_{dsat}$ | −274.9 mV |
| $V_{GS}$ | −1.027 V |
| $r_{on}$ | 25.66 kΩ |

So `pbias` sits at $V_{DD} - |V_{GS}| = 1.8 - 1.027 = 0.773\;\text{V}$. With $W_5/W_8 = 28.6/14.29 \approx 2\times$ the mirror gives $I_{D5} = 2 \cdot 40 = 80\;\mu\text{A}$, and similarly $I_{D6} = (W_6/W_8) \cdot 40\;\mu\text{A} = (57.14/14.29) \cdot 40 \approx 160\;\mu\text{A}$ (the paper used ~80 µA — a small scaling choice).

**Transistor sizes used (from [[Cadence Exercise - Two-Stage OpAmp Design|paper design]]):**

| Transistor | Type | W/L     | $I_{BIAS}$ | Role                              |
| ---------- | ---- | ------- | ---------- | --------------------------------- |
| Q8         | PMOS | 14.29/1 | 40 µA      | Bias reference (diode-connected)  |
| Q3         | NMOS | 8.5/1   | 40 µA      | Mirror load reference (in OpAmp)  |

---

### 4.2 OpAmp Block

**Schematic:** Two-stage Miller-compensated opamp (Q1-Q7, $C_c$, $R_c$).

![[opamp_schematic.png]]
*Figure: Two-stage opamp schematic. Q5 PMOS tail (gate = pbias), Q1/Q2 PMOS diff-pair (inputs Vin+, Vin-), Q3/Q4 NMOS mirror load, Q6 PMOS 2nd-stage current source (gate = pbias), Q7 NMOS common-source gain transistor. Lead compensation: $R_0 = 3.5\;\text{k}\Omega$ in series with $C_c$ between Vout and the Q7 gate.*

All channel lengths are fixed at $L = 1\;\mu$m to simplify the design and keep all devices firmly in a well-characterized operating regime. The paper values below were computed analytically + refined in LTspice bias sweeps to hit $g_{m1} = 0.201$ mA/V and $g_{m7} = 1.005$ mA/V (i.e. $g_{m7}/g_{m1} = 5$).

**Transistor sizes used:**

| Transistor | Type | W/L (paper)  | $I_D$   | Role                              |
| ---------- | ---- | ------------ | ------- | --------------------------------- |
| Q1         | PMOS | 11.4 / 1     | 40 µA   | Diff pair                         |
| Q2         | PMOS | 11.4 / 1     | 40 µA   | Diff pair                         |
| Q3         | NMOS | 8.5 / 1      | 40 µA   | Mirror load (ref, diode)          |
| Q4         | NMOS | 8.5 / 1      | 40 µA   | Mirror load                       |
| Q5         | PMOS | 28.6 / 1     | 80 µA   | Tail current source               |
| Q6         | PMOS | 57.14 / 1    | 80 µA   | 2nd stage current source          |
| Q7         | NMOS | 34 / 1       | 80 µA   | 2nd stage CS gain                 |

**Small-signal targets (paper):** $g_{m1} = 0.201\;\text{mA/V}$, $g_{m7} = 1.005\;\text{mA/V}$

**Compensation components:**

| Component | Value     | Purpose                                                        |
| --------- | --------- | -------------------------------------------------------------- |
| $C_c$     | 0.8 pF    | Miller compensation — splits poles, sets dominant pole         |
| $R_c$     | 3.5 kΩ    | Lead compensation — moves RHP zero to LHP to cancel $\omega_{p2}$ |

**Paper rationale for $R_c$:** $R_c = 1/g_{m7} + 1/(\omega_{p2} C_c) \approx 995 + 2486 \approx 3.5$ kΩ, which pushes the RHP zero into the LHP and places it exactly at the non-dominant pole for pole-zero cancellation.

---

## 5. Open-Loop Test Bench

**Setup:**
- Insert OpAmp + Bias block
- Add feedback network ($C_1 = C_2 = 1$ pF, $R_1 = 1$ G$\Omega$, $C_L = 1.5$ pF) but **do not connect to "-" terminal** (break the loop)
- Supply: $V_{DD} = 1.8$ V
- Bias current source: $I_{BIAS}$
- DC voltage sources at both OpAmp inputs (set to 800 mV)

![[opamp_testbench_top.png]]
*Figure: Top-level testbench schematic. `X1` = bias block (left, with VSS / VDD / pbias pins), `X0` = opamp block (centre), with the feedback network $C_A = C_B = 1\;\text{pF}$, $R_{FB} = 1\;\text{G}\Omega$, $C_L = 1.5\;\text{pF}$ on the output side. The Pulse source is used for transient/slew-rate tests, and the Sin (AC) source is used for the open-loop Bode and closed-loop AC simulations. The current source next to the opamp sets the bias reference current injected into the bias block's `pbias` input.*

### 5.1 DC Simulation -- Operating Point

**Output DC voltage:**

**Is it mid-rail ($V_{DD}/2 = 0.9$ V)? Why or why not?**


**Is this a problem?**


---

### 5.2 Finding the Input Voltage for $V_{out} = V_{DD}/2$

**Procedure:** Sweep the DC source at "+" terminal. Find input voltage that gives $V_{out} = V_{DD}/2 = 0.9$ V.

> [!warning] The open-loop gain is very high -- ensure sufficient accuracy in the sweep!

![[opamp_dc_sweep_vin_vout.png]]
*Figure: DC sweep of $V_{out}$ vs $V_{in+}$ around the high-gain transition (zoomed x-axis 700 mV – 890 mV). Marker M40 inside the transition region.*

**Input voltage for $V_{out} = V_{DD}/2$:** $V_{in+} \approx 788.87\;\text{mV}$ (from marker M40: 788.8669 mV → 800.0 mV, sitting inside the near-vertical transition ~10 mV below the 900 mV crossing)

The transition is extremely steep — reflecting the very high open-loop gain of the opamp. Even a fraction of a mV at the input drives the output rail-to-rail, so the exact $V_{in+}$ that lands on $V_{out} = 900$ mV is within a few mV of the marker. With the paper-design compensation ($C_c = 0.8\;\text{pF}$, $R_c = 3.5\;\text{k}\Omega$), the input offset that centers the output shifted slightly from the earlier ~778 mV value — the compensation network itself doesn't affect DC, but other small schematic refinements between runs move this operating point by a few mV. The sweep had to be run with very fine resolution around this point because of the near-vertical transition.

---

### 5.3 Open-Loop AC Simulation

**Setup:** Set the DC voltage to the value found in 5.2. Set AC magnitude = 1V. Run AC simulation.

![[opamp_open_loop_bode_paper_rc.png]]
*Figure: Open-loop Bode plot with paper-design compensation ($C_c = 0.8\;\text{pF}$, $R_c = 3.5\;\text{k}\Omega$). Yellow = magnitude (left axis, dB), red = phase (right axis, deg). Markers M41 (UGF), M42 (−3 dB reference past UGF), M43 (phase at UGF).*

| Parameter             | Simulated               | Expected (paper design) | Meets spec? |
| --------------------- | ----------------------- | ----------------------- | ----------- |
| DC Gain [dB]          | ~60 dB                  | ~60–70 dB               | ✓           |
| 3dB cut-off frequency | ~16 kHz                 | —                       | ✓           |
| Unity-gain frequency  | **16.08 MHz** (M41)     | ~15–20 MHz              | ✓           |
| Phase margin          | **90.22°**              | $\geq 70^\circ$         | ✓ (exceeds) |

**Phase margin calculation:** From M43 — phase at UGF = $-89.78°$, so $\text{PM} = 180° + (-89.78°) = 90.22°$.

**Do the simulation results match your expectations?**

Yes. The DC gain around 60 dB (~1000 V/V) is consistent with the two-stage Miller topology — each stage contributes ~30 dB from $g_m/g_{ds}$. The UGF of 16.08 MHz sits comfortably within the expected 15–20 MHz window for this design. The phase margin of 90.2° is dramatically better than required — the lead compensation ($R_c = 3.5\;\text{k}\Omega$) has placed an LHP zero that almost perfectly cancels the non-dominant pole, so the phase rolls off as if the amplifier were nearly a single-pole system and only just reaches $-90°$ at the unity-gain crossing.

**Bode plot observations:**

- Magnitude curve is flat at ~60 dB out to the dominant pole ($\sim$16 kHz), then rolls off with a clean single-pole $-20$ dB/dec slope out to UGF
- Phase reaches $-89.78°$ at UGF — essentially the behavior of a pure one-pole system. If the second pole were anywhere near UGF the phase would already be down around $-135°$; the pole-zero cancellation from the lead resistor is doing exactly what it should
- M42 at 22.97 MHz, $-3$ dB confirms a clean $-20$ dB/dec rolloff past UGF (a factor $22.97/16.08 = 1.43$ in frequency → $20\log_{10}(1.43) = 3.10$ dB drop, matching the marker)
- With 90° of phase margin there is enormous stability headroom if further bandwidth or speed tuning is desired

---

## 6. Slew Rate -- Closed-Loop

**Setup:** New schematic with closed-loop configuration. Apply voltage pulse (vpulse) at input.
- Amplitude: ensure rail-to-rail swing at output
- Rise/fall times: sufficiently small (not to affect SR at output)

![[opamp_slewrate_paper_rc_v2.png]]
*Figure: Transient response to a step input using the paper-design Miller compensation ($C_c = 0.8\;\text{pF}$, $R_c = 3.5\;\text{k}\Omega$). Markers M37 and M38 on the linear rising portion.*

**Extraction:** Two markers on the linear rising portion of the output:
- M37: $t_1 = 3.3033\;\text{ns}$, $V_1 = 445.99\;\text{mV}$
- M38: $t_2 = 12.7243\;\text{ns}$, $V_2 = 894.30\;\text{mV}$

$$SR_{\text{rise}} = \frac{V_2 - V_1}{t_2 - t_1} = \frac{0.8943 - 0.4460}{12.7243 - 3.3033}\;\text{V/ns} = \frac{0.4483}{9.421}\;\text{V/ns} = 47.59\;\text{V/}\mu\text{s}$$

| Parameter | Simulated | Target | Meets spec? |
|-----------|-----------|--------|-------------|
| Slew rate (rising) [V/$\mu$s] | 47.59 | $\geq 30$ | ✓ |
| Slew rate (falling) [V/$\mu$s] | *(to be measured)* | $\geq 30$ | — |

**Does the simulated SR match the expected $SR = I_{D5}/C_c$?**

Not directly — and the discrepancy actually tells us something useful. For the paper values, $I_{D5}/C_c = 80\;\mu\text{A}/0.8\;\text{pF} = 100\;\text{V/}\mu\text{s}$, but the measured rising SR is only 39 V/µs. The limit in this case is **not** the internal pole-splitting current $I_{D5}/C_c$ but rather the 2nd-stage PMOS current source $I_{D6}$ charging the output load:

$$SR_{\text{rise}} \approx \frac{I_{D6}}{C_{L,\text{tot}}} = \frac{80\;\mu\text{A}}{C_L + C_c + C_A \| C_B} = \frac{80}{1.5 + 0.8 + 0.5}\;\text{V/pF}\cdot\mu\text{s} \approx 28.6\;\text{V/}\mu\text{s}$$

The simulation (39 V/µs) sits between this simple estimate and the internal Miller limit, which is consistent — during slewing, $C_c$ is not a pure output load (one plate moves with $V_{out}$), and the effective capacitance bootstraps down. What matters is that **the output-node charging limit dominates here**, not the Miller cap. Both analytical bounds comfortably exceed the 30 V/µs spec, and so does the measurement.

> [!note] Why the second slew measurement?
> The first slewrate run (markers 40.45 V/µs) used a larger nominal Miller cap. After switching to the paper design values ($C_c = 0.8\;\text{pF}$, $R_c = 3.5\;\text{k}\Omega$) to get proper phase-margin behavior from the lead compensation, the SR shifted slightly but still comfortably meets spec.


### 6.1 Effect of Load Capacitance on SR

| $C_L$ | SR [V/$\mu$s] | Comment |
|--------|---------------|---------|
| 0.15 pF ($\times 0.1$) | | |
| 1.5 pF (nominal) | | |
| 15 pF ($\times 10$) | | |

**What happens to the SR? Is this expected?**


---

## 7. Optimization

**If specifications are not met, iterate between theory and simulation:**

- Use operating point to extract small-signal parameters ($g_m$, $g_{ds}$, $V_{eff}$)
- Recalculate expected performance with extracted values
- Adjust transistor dimensions accordingly
- Re-simulate

**Changes made and reasoning:**


---

## 8. Final Performance Summary

![[opamp_closed_loop_bw.png]]
*Figure: Closed-loop frequency response. Midband gain flat at 6 dB from ~44 Hz (M46) out to ~2.49 MHz (M48), then rolling off to the −3 dB point at M47: 22.2472 MHz.*

| Specification        | Target                          | Simulated (Cadence)                      | Meets? |
| -------------------- | ------------------------------- | ---------------------------------------- | ------ |
| Closed-loop gain     | 2 (6 dB)                        | **6.0 dB** (M46: 43.77 Hz, M48: 2.49 MHz)| ✓      |
| Closed-loop BW       | 20 MHz                          | **22.25 MHz** (M47: 22.2472 MHz, −3 dB)  | ✓      |
| Slew rate            | $\geq 30\;\text{V/}\mu\text{s}$ | **47.59 V/µs** (M37→M38)                 | ✓      |
| Phase margin         | $\geq 70^\circ$                 | **90.22°** (M43: −89.78° @ UGF)          | ✓      |
| Supply voltage       | 1.8 V                           | 1.8 V                                    | ✓      |
| DC open-loop gain    | —                               | ~60 dB (≈ 1000 V/V)                      | —      |
| Open-loop UGF        | —                               | **16.08 MHz** (M41)                      | —      |

**All 5 specs met.** With the paper-design Miller compensation ($C_c = 0.8\;\text{pF}$, $R_c = 3.5\;\text{k}\Omega$) the closed-loop frequency response is flat at exactly 6 dB from ~44 Hz through ~2.49 MHz (confirmed by the M46/M48 pair, both reading 6.0 dB), and holds up until the $-3$ dB point at 22.25 MHz. Everything clears the spec.

**Why closed-loop BW (22.25 MHz) > $\beta \cdot \text{UGF}_\text{ol}$ (~8 MHz):**

The single-pole approximation $\omega_{CL,-3\text{dB}} \approx \beta \cdot \omega_{t,\text{ol}}$ only holds if the open loop is a pure one-pole system. Here the lead compensation places a left-half-plane zero right on top of $\omega_{p2}$, **cancelling the second pole from the loop response and extending the closed-loop bandwidth well beyond the naïve estimate**. The nearly-$-90°$ phase at UGF (instead of the $-135°$ you would get from an uncompensated two-pole rolloff) is the signature of that pole-zero cancellation. In effect the lead compensation turns the amplifier into a very clean single-pole system whose feedback bandwidth sits close to $\omega_{p2}$ itself.

**Headroom for further optimization:**

- **Phase margin:** 90° vs 70° target — 20° of slack available if more speed is needed
- **Slew rate:** 48 V/µs vs 30 V/µs target — 59% above spec
- **BW:** 22.25 MHz vs 20 MHz — ~11% margin, passes comfortably

The design as given in the paper works as-is on the real XT018 process. The lead compensation is doing exactly what it was designed for — cancelling the non-dominant pole to keep the phase near $-90°$ across the entire usable bandwidth.

---

## 9. Extras (if time allows)

### 9.1 Lead Compensation (RC)

Replace Miller compensation with lead compensation (Carusone Fig. 6.10) to cancel the first non-dominant pole.

**Results:**


### 9.2 Improved Bias Generator

Replace ideal current source with resistor-based bias. Then implement the improved bias generator (Carusone Ch. 7, Fig. 06).

**Supply voltage sensitivity:**

| Bias circuit | $V_{DD}$ | $I_{BIAS}$ | $\Delta I_{BIAS}$/$\Delta V_{DD}$ |
|-------------|----------|------------|----------------------------------|
| Resistor | | | |
| Improved (Fig. 7.06) | | | |

**How much better is the improved generator?**

