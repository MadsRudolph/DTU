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

**Transistor sizes used:**

| Transistor | Type | W/L | Role |
|------------|------|-----|------|
| Q8 | PMOS | | Bias reference (diode-connected) |
| Q3 | NMOS | | Mirror load reference |

---

### 4.2 OpAmp Block

**Schematic:** Two-stage Miller-compensated opamp (Q1-Q7, $C_c$, $R_c$).

**Transistor sizes used (updated with extracted parameters if needed):**

| Transistor | Type | W/L (paper) | W/L (Cadence) | Role |
|------------|------|-------------|---------------|------|
| Q1 | PMOS | | | Diff pair |
| Q2 | PMOS | | | Diff pair |
| Q3 | NMOS | | | Mirror load (ref) |
| Q4 | NMOS | | | Mirror load |
| Q5 | PMOS | | | Tail current source |
| Q6 | PMOS | | | 2nd stage current source |
| Q7 | NMOS | | | 2nd stage CS gain |

| Component | Value |
|-----------|-------|
| $C_c$ | |
| $R_c$ | |

---

## 5. Open-Loop Test Bench

**Setup:**
- Insert OpAmp + Bias block
- Add feedback network ($C_1 = C_2 = 1$ pF, $R_1 = 1$ G$\Omega$, $C_L = 1.5$ pF) but **do not connect to "-" terminal** (break the loop)
- Supply: $V_{DD} = 1.8$ V
- Bias current source: $I_{BIAS}$
- DC voltage sources at both OpAmp inputs (set to 800 mV)

### 5.1 DC Simulation -- Operating Point

**Output DC voltage:**

**Is it mid-rail ($V_{DD}/2 = 0.9$ V)? Why or why not?**


**Is this a problem?**


---

### 5.2 Finding the Input Voltage for $V_{out} = V_{DD}/2$

**Procedure:** Sweep the DC source at "+" terminal. Find input voltage that gives $V_{out} = V_{DD}/2 = 0.9$ V.

> [!warning] The open-loop gain is very high -- ensure sufficient accuracy in the sweep!

**Input voltage for $V_{out} = V_{DD}/2$:**

---

### 5.3 Open-Loop AC Simulation

**Setup:** Set the DC voltage to the value found in 5.2. Set AC magnitude = 1V. Run AC simulation.

| Parameter | Simulated | Expected (paper design) | Meets spec? |
|-----------|-----------|------------------------|-------------|
| DC Gain [dB] | | | |
| 3dB cut-off frequency | | | |
| Unity-gain frequency (UGF) | | | |
| Phase margin | | $\geq 70^\circ$ | |

**Do the simulation results match your expectations?**


**Bode plot observations:**


---

## 6. Slew Rate -- Closed-Loop

**Setup:** New schematic with closed-loop configuration. Apply voltage pulse (vpulse) at input.
- Amplitude: ensure rail-to-rail swing at output
- Rise/fall times: sufficiently small (not to affect SR at output)

| Parameter | Simulated | Target | Meets spec? |
|-----------|-----------|--------|-------------|
| Slew rate (rising) [V/$\mu$s] | | $\geq 30$ | |
| Slew rate (falling) [V/$\mu$s] | | $\geq 30$ | |

**Does the simulated SR match the expected $SR = I_{D5}/C_c$?**


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

| Specification | Target | Simulated | Meets? |
|---------------|--------|-----------|--------|
| Closed-loop gain | 2 (6 dB) | | |
| Closed-loop BW | 20 MHz | | |
| Slew rate | $\geq 30$ V/$\mu$s | | |
| Phase margin | $\geq 70^\circ$ | | |
| Supply voltage | 1.8 V | 1.8 V | |

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

