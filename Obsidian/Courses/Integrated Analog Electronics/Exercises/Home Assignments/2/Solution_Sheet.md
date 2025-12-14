# Home Assignment 2 - Descriptive Solution Sheet
## Integrated Analog Electronics (34630) - Autumn 2023

---

## 📄 LaTeX Submission Document

**📂 [[Home_Assignment_II_Submission.pdf|Open Submitted Assignment PDF (3 pages)]]**

**LaTeX Source Location:** `C:\Users\Mads2\DTU\3.semester\Integrated Analog Electronics\Home-Assignment\Integrated_Analog_Electronics___Home_Assignment_II\`

This solution sheet provides **detailed explanations** and **extended theory** beyond the condensed submission version.

> **Note:** Click the link above to view the PDF directly in Obsidian. The original LaTeX files and source are in the location shown above.

---

## Exercise 1: W/L Ratio in MOSFET Transistor Model

### What the W/L Ratio Expresses

The **W/L ratio** (Width-to-Length ratio) in the Shichman-Hodges MOSFET model directly controls the **current-driving capability** of the transistor. It appears as a scaling factor in the drain current equations:

**Saturation Region:**
$$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_T)^2 (1 + \lambda V_{DS})$$

**Triode Region:**
$$I_D = \mu_n C_{ox} \frac{W}{L} \left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right]$$

The W/L ratio fundamentally determines:
- **Current capacity** for a given gate overdrive voltage
- **Transconductance** ($g_m = \sqrt{2\mu_n C_{ox} (W/L) I_D}$)
- **Gate capacitance** ($C_{gs} \approx \frac{2}{3} C_{ox} W L$)
- **Device matching** characteristics

### Effects of Increasing/Decreasing W (Width)

#### Increasing W - Advantages:
1. **Higher current drive** - More current for same $V_{GS}$, useful for power stages
2. **Higher transconductance** ($g_m \propto \sqrt{W}$) - Better voltage gain in amplifiers
3. **Lower on-resistance** - Beneficial for switches and current mirrors
4. **Better matching** - Threshold voltage mismatch $\sigma(\Delta V_T) \propto 1/\sqrt{WL}$ improves

#### Increasing W - Disadvantages:
1. **Larger gate capacitance** ($C_{gs} \propto WL$) - Reduces bandwidth, increases delay
2. **Higher parasitic capacitances** ($C_{db}, C_{sb}$) - Degrades frequency response
3. **More chip area** - Increases cost
4. **Higher gate drive requirement** - More power to charge/discharge gate

#### Decreasing W - Advantages:
1. **Lower capacitance** - Higher speed, lower power consumption
2. **Smaller area** - Lower cost, higher integration density
3. **Lower gate charge** - Faster switching, less driver power

#### Decreasing W - Disadvantages:
1. **Lower current capability** - Cannot drive large loads
2. **Lower $g_m$** - Reduced gain
3. **Worse matching** - More sensitive to process variations
4. **Higher sensitivity to lithography errors** - Minimum width constraints

### Effects of Increasing/Decreasing L (Length)

#### Increasing L - Advantages:
1. **Higher output resistance** ($r_o = 1/(\lambda I_D)$ where $\lambda \propto 1/L$) - Better current source, higher gain
2. **Better matching** - $\sigma(\Delta V_T) \propto 1/\sqrt{WL}$ improves
3. **Reduced short-channel effects** - More ideal device behavior
4. **Lower channel-length modulation** - More constant current vs. $V_{DS}$
5. **Lower flicker noise** (1/f noise $\propto 1/(WL)$)

#### Increasing L - Disadvantages:
1. **Lower transconductance** for fixed current ($g_m \propto 1/\sqrt{L}$ at constant $I_D$)
2. **Larger gate capacitance** ($C_{gs} \propto WL$) - Slower
3. **More chip area** - Higher cost
4. **Lower transit frequency** ($f_T = g_m/(2\pi(C_{gs} + C_{gd}))$) - Bandwidth limitation

#### Decreasing L - Advantages:
1. **Higher speed** - Lower gate capacitance, higher $f_T$
2. **Smaller area** - Cost reduction
3. **Higher $g_m/I_D$ ratio** - Better for low-power design

#### Decreasing L - Disadvantages:
1. **Lower output resistance** - Worse current sources, lower gain
2. **Short-channel effects** - Velocity saturation, DIBL, threshold rolloff
3. **Worse matching** - Process variation sensitivity
4. **Higher leakage currents** - Subthreshold conduction
5. **Minimum length constraints** - Cannot go below process limits

### Design Guidelines

**For high-gain analog circuits:** Use large L for high $r_o$ (better current sources)
**For high-speed circuits:** Use minimum L, optimize W for capacitance/speed trade-off
**For matching-critical circuits:** Maximize WL product within area/speed constraints
**For low-power circuits:** Optimize $g_m/I_D$ ratio, often means moderate L

---

## Exercise 2: Feedback in MOSFET-Based Circuits

### Advantages of Feedback

#### 1. **Gain Desensitization**
- **Closed-loop gain:** $A_{CL} = A/(1 + A\beta) \approx 1/\beta$ for large loop gain $A\beta$
- Makes gain **independent of open-loop gain** variations (process, temperature, aging)
- **Example:** Op-amp gain varies 20:1 across process corners, but with feedback, closed-loop gain varies <1%

#### 2. **Bandwidth Extension**
- **Bandwidth increase:** $BW_{closed} = BW_{open} \times (1 + A\beta)$
- **Gain-bandwidth trade-off:** Lower gain → wider bandwidth
- **Example:** Op-amp with 100 dB gain and 10 Hz bandwidth becomes 40 dB gain with 1 MHz bandwidth

#### 3. **Reduced Distortion (Linearity Improvement)**
- **Distortion reduction factor:** $(1 + A\beta)$
- Feedback corrects nonlinearities by comparing output to input
- THD (Total Harmonic Distortion) reduced proportionally to loop gain

#### 4. **Impedance Control**

**Voltage feedback (series input, shunt output):**
- Input impedance: $Z_{in,closed} = Z_{in,open} \times (1 + A\beta)$ - **Increases**
- Output impedance: $Z_{out,closed} = Z_{out,open} / (1 + A\beta)$ - **Decreases**

**Current feedback (shunt input, series output):**
- Input impedance: **Decreases**
- Output impedance: **Increases**

Allows **impedance matching** to source/load requirements.

#### 5. **Noise Reduction (at input)**
- Noise generated **after the input summing point** is reduced by factor $(1 + A\beta)$
- Input-referred noise from later stages is suppressed
- **Caveat:** Input stage noise is not reduced, can even increase with shunt feedback

### Disadvantages of Feedback

#### 1. **Reduced Gain**
- **Sacrifice:** $A_{CL} = A/(1 + A\beta) < A$
- Need **high open-loop gain** $A$ to achieve desired $A_{CL}$ with good desensitization
- More gain stages required → more power, area, complexity

#### 2. **Stability Issues**
- Feedback can cause **oscillation** if phase shift reaches 180° at unity loop gain
- **Nyquist stability criterion:** Loop gain $A\beta$ must have $|A\beta| < 1$ when $\angle A\beta = -180°$
- Requires **compensation:** Miller compensation, dominant pole, damping
- **Phase margin requirement:** Typically PM ≥ 45° (preferably 60°) for stable operation
- **Peaking/ringing:** Insufficient phase margin causes overshoot in step response

#### 3. **Bandwidth-Gain Trade-off**
- **Gain-bandwidth product is constant:** GBW = $A_{CL} \times BW_{closed}$
- Cannot simultaneously maximize both gain and bandwidth
- High-frequency applications limited by transistor $f_T$

#### 4. **Increased Circuit Complexity**
- Need **feedback network** (resistors, capacitors) - more components
- **Biasing considerations** for feedback path
- **Layout complexity** - careful routing to avoid unintended feedback
- More **pins/connections** in packaged ICs

#### 5. **Performance Degradation with Loop Gain Reduction**
- All benefits **proportional to loop gain** $A\beta$
- At high frequencies where $|A\beta| < 1$: lose desensitization, linearity improvement
- Need adequate loop gain across **frequency range of interest**

#### 6. **Potential for Instability with Capacitive Loads**
- **Load capacitance** adds pole → phase shift → potential instability
- Op-amps may need **output isolation** (series resistor) or load-compensated design
- Unity-gain stable op-amps sacrifice performance for universal stability

### Practical Considerations

**When to use feedback:**
- Precision required (gain accuracy, linearity)
- Wide environmental variation (temperature, supply voltage)
- Impedance control needed
- Acceptable to trade gain for bandwidth

**When to avoid feedback:**
- Maximum gain needed at all costs
- Stability is problematic (high capacitive loading)
- Ultra-low power (cannot afford extra stages for loop gain)
- Simple circuits where open-loop is adequate

---

## Exercise 3: Second-Order Feedback System - Pole Placement

### Transfer Function and Pole Locations

**Standard second-order system:**
$$H(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

**Pole locations:**
$$s_{1,2} = -\zeta\omega_n \pm \omega_n\sqrt{\zeta^2 - 1} \quad \text{(real poles, } \zeta > 1\text{)}$$
$$s_{1,2} = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2} \quad \text{(complex poles, } 0 < \zeta < 1\text{)}$$

Where:
- $\omega_n$ = natural frequency
- $\zeta$ = damping ratio
- $Q = 1/(2\zeta)$ = quality factor

### Case 1: Overdamped ($\zeta > 1$) - Two Real, Separated Poles

**Pole configuration:** Two distinct real poles on negative real axis

**Advantages:**
1. **No overshoot** - Monotonic step response, no ringing
2. **Unconditionally stable** - Large phase margin (PM ≈ 90° if widely separated)
3. **Predictable behavior** - First-order-like response dominates
4. **Robust to variations** - Pole movements don't cause oscillation
5. **Low noise sensitivity** - No resonant peaking in frequency response

**Disadvantages:**
1. **Slow settling** - Two time constants to wait out
2. **Poor bandwidth utilization** - Second pole "wasted" far from crossover
3. **Lower bandwidth for given power** - Not optimized for speed
4. **Sluggish response** - Cannot track fast input changes efficiently

**Design implications:**
- Use when **stability is paramount** (power supplies, references)
- Acceptable when **speed is not critical**
- Common in **single-dominant-pole compensated op-amps**

**Typical specifications:** $\zeta = 1.5$, PM ≈ 75°

### Case 2: Critically Damped ($\zeta = 1$) - Repeated Real Pole

**Pole configuration:** Two coincident real poles (double pole)

**Advantages:**
1. **Fastest response without overshoot** - Optimal for step input tracking
2. **No ringing** - Smooth, controlled response
3. **Good phase margin** - PM ≈ 65°
4. **Better bandwidth than overdamped** - Both poles at same frequency

**Disadvantages:**
1. **Sensitive operating point** - Small variations → overshoot or slower response
2. **Difficult to achieve precisely** - Requires exact component matching
3. **Still relatively slow** - Not as fast as underdamped for band-limited applications
4. **Moderate bandwidth efficiency** - Not optimal for sinusoidal tracking

**Design implications:**
- **Theoretical optimum** for step response without overshoot
- Rarely achieved precisely in practice (tolerance issues)
- Good **compromise design target**

**Typical specifications:** $\zeta = 1.0$, PM ≈ 65°

### Case 3: Underdamped ($0 < \zeta < 1$) - Complex Conjugate Poles

**Pole configuration:** Complex conjugate pair with imaginary parts

**Advantages:**
1. **Fastest settling to within tolerance band** - Oscillations settle within few cycles
2. **Maximum bandwidth utilization** - Poles placed for optimal frequency response
3. **Higher bandwidth for given power** - More aggressive design
4. **Better high-frequency tracking** - Peaking extends usable bandwidth
5. **Optimized for sinusoidal signals** - Flat magnitude response up to $\omega_n$

**Disadvantages:**
1. **Overshoot and ringing** - Step response oscillates
2. **Reduced phase margin** - PM decreases with lower $\zeta$ (PM ≈ 100$\zeta$ degrees)
3. **Risk of instability** - Close to stability boundary, sensitive to variations
4. **Frequency-domain peaking** - $|H(j\omega)|$ has peak at $\omega_r = \omega_n\sqrt{1-2\zeta^2}$
   - Peak magnitude: $M_p = 1/(2\zeta\sqrt{1-\zeta^2})$ for small $\zeta$
5. **Noise amplification** - Peaking amplifies noise at resonant frequency
6. **Poor load tolerance** - Additional capacitance can cause instability

**Design implications:**
- Use when **speed is critical** and some overshoot acceptable
- Common in **high-speed data acquisition**, **control systems**
- **Trade-off:** Lower $\zeta$ → faster but more overshoot

**Typical specifications:**
- Conservative: $\zeta = 0.7$ (Butterworth), PM ≈ 65°, overshoot ≈ 5%
- Aggressive: $\zeta = 0.5$, PM ≈ 50°, overshoot ≈ 16%
- Very aggressive: $\zeta = 0.3$, PM ≈ 30°, overshoot ≈ 37%

### Pole Separation Effects (for real poles)

**Widely separated poles** ($\omega_{p2} \gg \omega_{p1}$):
- **Dominant pole behavior** - System approximates first-order
- Second pole contributes minimal phase shift at crossover
- High phase margin, very stable
- Common in **op-amp compensation**: $f_{p1}$ ≈ 10 Hz, $f_{p2}$ ≈ 10 MHz

**Closely spaced poles** ($\omega_{p2} \approx \omega_{p1}$):
- **Second-order response** - Both poles significant
- Cumulative phase shift ≈ 180° around $\omega_n$
- **Phase margin reduction** - Less stable
- Can be **overdamped** ($\zeta > 1$) or **critically damped** ($\zeta = 1$)

### Practical Design Strategy

**Step 1: Determine application requirements**
- Can you tolerate overshoot? (Yes → underdamped, No → critically/overdamped)
- Speed critical? (Yes → underdamped, No → overdamped)
- Bandwidth or settling time primary spec?

**Step 2: Choose damping ratio**
- **Maximally flat (Butterworth):** $\zeta = 0.707$, good compromise
- **No overshoot:** $\zeta \geq 1$
- **Fast settling:** $\zeta = 0.5$ to $0.7$
- **Ultra-stable:** $\zeta > 1.5$ (dominant pole)

**Step 3: Set phase margin**
- PM ≈ $100\zeta$ for $\zeta < 0.7$
- PM ≈ 65° for $\zeta = 1$
- PM ≈ 90° for widely separated poles

**Step 4: Verify under all conditions**
- Worst-case process corners
- Temperature extremes
- Load capacitance variations
- Supply voltage range

### Summary Table

| Damping | $\zeta$ | Poles | PM | Overshoot | Bandwidth | Use Case |
|---------|---------|-------|----|-----------|-----------| ---------|
| Overdamped | >1 | Real, separated | ~75-90° | 0% | Low | Precision, stability |
| Critical | 1 | Real, coincident | ~65° | 0% | Medium | Fast without overshoot |
| Underdamped | 0.7 | Complex | ~65° | ~5% | High | General purpose |
| Underdamped | 0.5 | Complex | ~50° | ~16% | Higher | High-speed systems |
| Underdamped | <0.5 | Complex | <45° | >20% | Highest | Aggressive designs |

**General guideline:** For analog circuit stability, aim for **PM ≥ 60°** ($\zeta \approx 0.6$ to $1.0$).

---

## Exercise 4: Bandgap Voltage Reference

### How a Bandgap Reference Works

A **bandgap voltage reference** generates a temperature-stable voltage ≈ 1.25 V by combining two voltages with **opposite temperature coefficients** that cancel:

1. **CTAT (Complementary To Absolute Temperature):** $V_{BE}$ of BJT
   - Decreases ≈ -2 mV/°C

2. **PTAT (Proportional To Absolute Temperature):** $\Delta V_{BE}$
   - Increases ≈ +2 mV/°C

#### Basic Principle

**VBE temperature behavior:**
$$V_{BE}(T) = V_{BE}(T_0) - k(T - T_0)$$
where $k \approx 2$ mV/°C

**ΔVBE from two BJTs with different current densities:**
$$\Delta V_{BE} = V_{BE1} - V_{BE2} = V_T \ln\left(\frac{I_1/A_1}{I_2/A_2}\right) = V_T \ln(N)$$

where:
- $V_T = kT/q$ ≈ 26 mV at 300K (thermal voltage, PTAT)
- $N$ = current density ratio (typically 8-10)

**Temperature coefficient of $\Delta V_{BE}$:**
$$\frac{d(\Delta V_{BE})}{dT} = \frac{k}{q}\ln(N) \approx +0.086 \text{ mV/°C} \times \ln(N)$$

For $N = 8$: ≈ +0.18 mV/°C (PTAT)

#### Circuit Operation

**Output voltage:**
$$V_{REF} = V_{BE} + \alpha \Delta V_{BE}$$

where $\alpha = R_2/R_1$ is chosen to cancel temperature coefficients:

$$\frac{dV_{REF}}{dT} = \frac{dV_{BE}}{dT} + \alpha \frac{d(\Delta V_{BE})}{dT} = 0$$

$$\alpha = \frac{|dV_{BE}/dT|}{d(\Delta V_{BE})/dT} \approx \frac{2 \text{ mV/°C}}{0.18 \text{ mV/°C}} \approx 11$$

**Result:**
$$V_{REF} = V_{BE}(T_0) + \alpha V_T \ln(N) \approx 1.25 \text{ V}$$

This voltage ≈ **silicon bandgap at 0K** (1.205 V), hence the name.

#### Implementation

**Typical circuit:**
- Two BJTs (Q1, Q2) with area ratio $N:1$
- Resistor network forces PTAT current: $I_{PTAT} = \Delta V_{BE}/R_1 = V_T \ln(N)/R_1$
- This current flows through $R_2$, generating weighted PTAT voltage
- Summed with $V_{BE}$ at output

**Startup circuit** required - bandgap has **zero-current degenerate state** that must be avoided.

### Advantages of Bandgap Reference

#### 1. **Temperature Stability**
- **Best achievable:** 10-50 ppm/°C with trimming
- **Typical untrimmed:** 50-100 ppm/°C
- Much better than simple diode or Zener references

#### 2. **Supply Independence**
- With good op-amp and current mirrors: PSRR > 60 dB
- Output largely independent of $V_{DD}$ variations
- Works over wide supply range (2.5V - 30V+)

#### 3. **Long-Term Stability**
- Resistor-based, no special components
- Less aging than Zener references
- Predictable drift characteristics

#### 4. **IC Integration**
- **Standard CMOS/BiCMOS process** - no special fabrication
- Uses **substrate/parasitic BJTs** available in CMOS
- Small area, low cost
- Can be integrated with any analog circuit

#### 5. **Low Noise**
- Lower noise than Zener references (no avalanche)
- Can be filtered easily
- Predictable 1/f and thermal noise

#### 6. **Design Flexibility**
- Output voltage can be scaled with additional resistor divider
- Can generate multiple reference voltages
- Trimming possible for high accuracy

### Disadvantages of Bandgap Reference

#### 1. **Minimum Supply Voltage**
- **Requires $V_{DD} \geq V_{REF} + V_{DSsat}$** ≈ 1.5 - 2.0 V minimum
- Not suitable for **sub-1V applications** without modifications
- Modern solutions: sub-bandgap references (≈600 mV) sacrifice some performance

#### 2. **Curvature Error (Second-Order Effects)**
- VBE temperature dependence **not perfectly linear**
- Residual **parabolic error** over wide temperature range
- Typical: ±0.5°C error from -40°C to +125°C
- **Requires curvature compensation** for high-precision designs
  - Piecewise-linear correction
  - Higher-order compensation

#### 3. **Process Sensitivity**
- $V_{BE}$ absolute value varies with **process (±20 mV typical)**
- Resistor matching critical for TC cancellation
- **Requires trimming** for high accuracy (laser trim, e-fuse)
  - Untrimmed: ±3% output variation
  - Trimmed: ±0.5% achievable

#### 4. **Startup Issues**
- **Degenerate zero-current state** - circuit can power up with all currents = 0
- **Startup circuit required** - adds complexity, power
- Must ensure startup works across PVT (process, voltage, temperature)

#### 5. **Speed/Settling Time**
- **Slow startup** - milliseconds typical
- High-impedance node (compensation cap) limits speed
- Not suitable for fast transient response applications
- **Line regulation** can be slow

#### 6. **Power Consumption**
- Requires **bias current** (typically 10-100 μA)
- Not suitable for ultra-low-power applications
- Power consumption proportional to accuracy (more current = better PSRR, lower noise)

#### 7. **Package Stress and Hysteresis**
- Plastic package stress affects output voltage
- **Thermal hysteresis** - output changes with thermal cycling
- Can be significant in low-cost packages (±1 mV)

#### 8. **1/f Noise from BJTs**
- BJT flicker noise at low frequencies
- Limits noise performance in precision applications
- Requires careful low-pass filtering

### Pros and Cons in IC Design Context

**When to use bandgap reference:**
- **Precision ADC/DAC** - need stable, accurate reference
- **Voltage regulators** - stable reference for feedback
- **Temperature sensors** - compare PTAT voltage to bandgap
- **General analog ICs** - standard building block

**When NOT to use:**
- **Ultra-low voltage** ($V_{DD} < 1.5$ V) - use sub-bandgap or resistor-based
- **Ultra-low power** (nanoampere budgets) - use simpler current-starved reference
- **Cost-critical, low-precision** - simple $V_T$-based or resistor divider adequate
- **Very high speed** - startup and settling time problematic

**Alternatives:**
- **Zener diode** - Higher voltage (5-7V), higher noise, but simpler
- **PTAT/Resistor ratio** - Lower accuracy, but works at low voltage
- **Current reference** - Generate $V_{REF}$ via $I_{REF} \times R$

### Typical Performance Metrics

| Parameter | Typical Value | High-Performance |
|-----------|---------------|------------------|
| Output Voltage | 1.20 - 1.25 V | 1.2000 V |
| TC (untrimmed) | 50-100 ppm/°C | 10-20 ppm/°C |
| TC (trimmed) | 10-30 ppm/°C | 3-10 ppm/°C |
| Supply voltage | 2.5 - 5 V | 1.8 - 5 V |
| PSRR | 60 - 80 dB | >80 dB |
| Current consumption | 20 - 100 μA | 10 - 50 μA |
| Startup time | 1 - 10 ms | 0.1 - 1 ms |
| Initial accuracy (trim) | ±1% | ±0.2% |

---

## Exercise 5: Two-Stage Op-Amp Analysis

### Part (a): Subcircuit Functionality

#### Subcircuit 1: **Differential Input Stage (M1, M2, M3, M4)**

**Components:**
- **M1, M2:** NMOS input differential pair
- **M3, M4:** NMOS current source tail (diode-connected M3 mirrors to M4)
- **VIN:** Differential input voltage

**Functionality:**
- **Converts differential input voltage to differential current**
- M1, M2 are the differential pair - respond to $V_{IN+} - V_{IN-}$
- M3-M4 form current mirror providing **tail current** $I_{tail}$
- This tail current splits between M1 and M2 based on input voltage
- **Transconductance:** $g_{m1,2}$ converts input voltage to output current

**Why this configuration:**
- **Differential input** - rejects common-mode noise
- **Current source tail** (M3-M4) improves CMRR and tail impedance
- NMOS input pair → moderate input impedance, good noise performance

#### Subcircuit 2: **Current Mirror Active Load (M5, M6)**

**Components:**
- **M5, M6:** PMOS current mirror (diode-connected M5 mirrors to M6)

**Functionality:**
- **Converts differential current to single-ended output**
- M5 is diode-connected, forces $V_{GS5} = V_{DS5}$
- M5 carries drain current of M1
- M6 mirrors this current and **sinks current from M2's drain**
- **Differential-to-single-ended conversion:**
  - If $V_{IN+} > V_{IN-}$: M2 conducts more → M6 needs to sink more → pulls $V_O$ down
  - If $V_{IN+} < V_{IN-}$: M2 conducts less → M6 sinks less → $V_O$ rises
- **High impedance** at output node ($V_O$) - parallel combination of $r_{o2} \parallel r_{o6}$

**Why this configuration:**
- **Active load** provides high gain: $A_{v1} = g_{m1,2} (r_{o2} \parallel r_{o6})$
- **Single-ended output** drives second stage
- **Good PSRR** from power supply

#### Subcircuit 3: **Second Gain Stage / Output Stage (M7)**

**Components:**
- **M7:** NMOS common-source amplifier
- Input: $V_O$ from first stage
- Output: $V_{OUT}$ (final output)

**Functionality:**
- **Voltage amplification** - common-source configuration
- **Gain:** $A_{v2} = g_{m7} (r_{o7} \parallel R_{load})$
- Provides **additional voltage gain**
- Drives output load $C_L$

**Why this configuration:**
- **Second stage** needed for higher total DC gain
- **Current source load** (implied, or explicit if there's a load transistor)
- Can provide **rail-to-rail output swing** with proper biasing

#### Subcircuit 4: **Biasing (RBIAS, VIN bias)**

**Components:**
- **$R_{BIAS}$:** Sets bias current
- **$V_{IN}$:** DC bias point for input stage

**Functionality:**
- $R_{BIAS}$ connected to current mirror (M3-M4) sets $I_{tail}$
- **All circuit currents scale from this reference**
- Establishes **quiescent operating point** for all transistors

#### Subcircuit 5: **Miller Compensation ($C_C$)**

**Components:**
- **$C_C$:** Compensation capacitor between output and intermediate node $V_O$

**Functionality:**
- **Creates dominant pole** at node $V_O$
- **Miller effect** multiplies $C_C$ by voltage gain of second stage
- Effective capacitance seen at $V_O$: $C_{eff} = C_C (1 + A_{v2})$
- **Dominant pole frequency:**
  $$f_{p1} = \frac{1}{2\pi (r_{o2} \parallel r_{o6}) C_C (1 + g_{m7}(r_{o7} \parallel R_L))}$$
- **Pushes second pole** higher via right-half-plane zero cancellation (if $C_B$ present)
- Ensures **phase margin ≥ 60°** for stability

**Why needed:**
- Without compensation: Two high-gain stages → two poles close together → **poor phase margin**
- $C_C$ enforces **single dominant pole** - makes op-amp stable

#### Subcircuit 6: **Load Capacitance ($C_L$) and Bypass ($C_B$)**

**Components:**
- **$C_L$:** External load capacitance
- **$C_B$:** Bypass/decoupling capacitor (if present)

**Functionality:**
- $C_L$ represents external load (ADC input, feedback network, etc.)
- Creates pole at output: $f_{p,out} = 1/(2\pi R_{out} C_L)$
- Can **degrade phase margin** if not accounted for
- $C_B$ provides **local decoupling** for supply noise

### Part (b): Effect of Parameter Changes

#### Effect of Increasing Currents

**Increasing $I_{tail}$ (bias current through M3-M4):**

**Gain:**
- **Increases $g_m$:** $g_m = \sqrt{2\mu_n C_{ox} (W/L) I_D} \propto \sqrt{I_D}$
- First stage gain: $A_{v1} = g_{m1,2}(r_{o2} \parallel r_{o6})$
  - $g_m \uparrow$ but $r_o = 1/(\lambda I_D) \downarrow$
  - **Net effect:** Modest gain increase (typically gain decreases slightly)
- **Dominant effect:** $g_m$ increase is $\sqrt{I}$, $r_o$ decrease is $1/I$
  - **Gain typically decreases** with higher current

**GBW Product:**
- **GBW increases:** $GBW = g_{m1}/(2\pi C_C)$
- $g_m \propto \sqrt{I}$ → GBW $\propto \sqrt{I}$
- **More current = wider bandwidth**

**Stability:**
- **Second pole frequency increases:** $f_{p2} \approx g_{m7}/(2\pi C_L)$
- Higher $g_{m7}$ pushes $f_{p2}$ further from $f_u$ (unity-gain frequency)
- **Phase margin improves**
- **Better stability**

**Slew Rate:**
- **SR increases linearly:** $SR = I_{tail}/C_C$
- **More current = faster large-signal response**

**Pros:**
- ✅ Higher bandwidth (GBW $\uparrow$)
- ✅ Better stability (PM $\uparrow$)
- ✅ Higher slew rate
- ✅ Better noise performance (lower input-referred noise)
- ✅ Higher $f_T$ of transistors

**Cons:**
- ❌ Higher power consumption
- ❌ Gain may decrease slightly
- ❌ More headroom required ($V_{DSsat} \uparrow$)
- ❌ Thermal issues in high-power designs

---

#### Effect of Increasing W/L Ratios

**Increasing W/L of input pair (M1, M2):**

**Gain:**
- **First stage gain:** $A_{v1} = g_{m1,2}(r_{o2} \parallel r_{o6})$
- $g_m = \sqrt{2\mu_n C_{ox}(W/L)I_D}$ → $g_m \uparrow$ with $\sqrt{W/L}$
- $r_o$ unchanged (depends on L and $I_D$, not W)
- **Gain increases** proportionally to $\sqrt{W/L}$

**GBW:**
- **GBW increases:** $GBW = g_{m1}/(2\pi C_C)$
- GBW $\propto \sqrt{W/L}$

**Stability:**
- Parasitic capacitance at $V_O$ node increases ($C_{db2}, C_{sb2} \propto W$)
- Dominant pole shifts lower: $f_{p1} \downarrow$
- Unity-gain frequency may shift
- **Phase margin impact:** Depends on whether $f_{p2}$ is affected

**Pros:**
- ✅ Higher gain (better $g_m$)
- ✅ Higher GBW
- ✅ Lower input-referred noise: $\overline{v_n^2} \propto 1/(g_m) \propto 1/\sqrt{W/L}$
- ✅ Better matching (if both increased)

**Cons:**
- ❌ Higher capacitance (slower if not compensated)
- ❌ More chip area
- ❌ Higher gate charge (more power to drive)

---

**Increasing W/L of current mirror load (M5, M6):**

**Gain:**
- **First stage gain:** $g_{m1,2}(r_{o2} \parallel r_{o6})$
- Increasing M5, M6 W/L improves current matching
- $r_{o6} = 1/(\lambda_p I_{D6})$ - **$r_o$ depends on L, not W**
- **Gain mostly unchanged**

**GBW:**
- Little direct effect (GBW set by $g_{m1}$ and $C_C$)

**Stability:**
- $C_{gd}$ of M6 increases → more capacitance at $V_O$
- Dominant pole $f_{p1}$ may decrease slightly
- Phase margin impact minimal if $C_C$ >> parasitic capacitances

**Pros:**
- ✅ Better current matching in mirror
- ✅ Lower offset voltage
- ✅ Better PSRR

**Cons:**
- ❌ Slightly higher capacitance at $V_O$
- ❌ More area

---

**Increasing L (length) of all transistors:**

**Gain:**
- **$r_o$ increases:** $r_o \approx L/(\lambda I_D)$ (approximately)
- **Gain increases significantly:** $A_v = g_m r_o$
- $g_m$ decreases slightly: $g_m \propto 1/\sqrt{L}$ (at fixed $I_D$)
- **Net: Gain increases** (output resistance effect dominates)

**GBW:**
- $g_m$ decreases → **GBW decreases**
- Gate capacitance $C_{gs} \propto WL$ increases → further speed reduction

**Stability:**
- Higher gain → need to check phase margin
- Parasitics increase → poles shift
- May need to **increase $C_C$** to maintain PM

**Pros:**
- ✅ Much higher DC gain
- ✅ Better output resistance (better current sources)
- ✅ Reduced short-channel effects
- ✅ Better matching

**Cons:**
- ❌ Lower bandwidth (GBW $\downarrow$)
- ❌ Slower response
- ❌ More area

---

#### Effect of Changing Compensation Capacitor ($C_C$)

**Increasing $C_C$:**

**Gain:**
- **DC gain unchanged** (set by $g_m$ and $r_o$)

**GBW:**
- **GBW decreases:** $GBW = g_{m1}/(2\pi C_C)$
- GBW $\propto 1/C_C$

**Stability:**
- **Dominant pole shifts lower:** $f_{p1} \propto 1/C_C$
- Unity-gain frequency $f_u = GBW$ decreases
- Second pole $f_{p2}$ stays approximately constant
- **Phase margin increases:** $f_u$ further from $f_{p2}$ → less phase shift at $f_u$
- **More stable, more conservative design**

**Slew Rate:**
- **SR decreases:** $SR = I_{tail}/C_C$
- Slower large-signal response

**Pros:**
- ✅ Better stability (higher PM)
- ✅ Robust to load capacitance variations
- ✅ Less peaking in frequency response
- ✅ Lower overshoot in step response

**Cons:**
- ❌ Lower bandwidth (GBW $\downarrow$)
- ❌ Lower slew rate
- ❌ Slower settling time

---

**Decreasing $C_C$:**

**Effect:**
- **GBW increases**
- **Phase margin decreases** (risk of instability)
- **Slew rate increases**

**Pros:**
- ✅ Higher bandwidth
- ✅ Faster slew rate
- ✅ Smaller capacitor (less area if on-chip)

**Cons:**
- ❌ **Stability risk** - may oscillate
- ❌ Overshoot and ringing
- ❌ Sensitive to load capacitance

---

### Summary Table: Parameter Effects

| Parameter | Gain | GBW | Stability | Power | Trade-off |
|-----------|------|-----|-----------|-------|-----------|
| $I \uparrow$ | ↓ | ↑ | ↑ (better) | ↑ | Power vs. Speed |
| $(W/L)_{1,2} \uparrow$ | ↑ | ↑ | ~→ | ~→ | Area vs. Performance |
| $L \uparrow$ (all) | ↑↑ | ↓ | ? | ~→ | Gain vs. Speed |
| $C_C \uparrow$ | → | ↓ | ↑ (better) | → | Stability vs. Speed |

**Optimization strategy:**
1. **Choose $C_C$** for desired phase margin (PM ≥ 60°)
2. **Set current** for required GBW and slew rate (within power budget)
3. **Size transistors** (W/L) for gain, noise, matching requirements
4. **Iterate** to optimize all specifications

---

## Exercise 6: CMRR Improvement in Differential Amplifier

### Part (a): Methods to Increase CMRR

The **Common-Mode Rejection Ratio (CMRR)** measures how well a differential amplifier rejects common-mode signals:

$$CMRR = \left|\frac{A_d}{A_{cm}}\right| = \frac{\text{Differential Gain}}{\text{Common-Mode Gain}}$$

$$CMRR_{dB} = 20\log_{10}\left(\frac{A_d}{A_{cm}}\right)$$

Higher CMRR means better rejection of noise and interference common to both inputs.

**For the given circuit (differential pair with current source tail):**

$$CMRR \approx g_m R_{tail}$$

where $R_{tail}$ is the output impedance of the tail current source.

#### Method 1: **Use Cascode Current Source for Tail**

**Modification:**
- Replace simple current source (single transistor) with **cascode current source**
- Stack two NMOS transistors for tail current source

**How it works:**
- **Cascode impedance:** $R_{out,cascode} \approx g_m r_o^2$
- Simple current source: $R_{out} = r_o$
- **Impedance increase:** Factor of $g_m r_o$ (typically 20-100×)
- **CMRR improvement:** Same factor ($g_m r_o$)

**Expected CMRR increase:** 20-40 dB

#### Method 2: **Increase Tail Current Source Transistor Length**

**Modification:**
- Increase L of tail current source transistor(s)

**How it works:**
- **Output resistance:** $r_o \propto L / (\lambda I_D)$
- Longer channel → smaller $\lambda$ → higher $r_o$
- **CMRR improvement** proportional to $r_o$ increase

**Expected CMRR increase:** 2-4× improvement (6-12 dB) for 2-4× length increase

#### Method 3: **Increase W/L of Differential Pair (M1, M2)**

**Modification:**
- Increase W/L ratio of input transistors M1 and M2 (proportionally)

**How it works:**
- $CMRR = g_m R_{tail}$
- $g_m = \sqrt{2\mu_n C_{ox}(W/L)I_D}$
- Larger W/L → higher $g_m$ → higher CMRR

**Expected CMRR increase:** $\sqrt{2}$ for 2× W/L increase (~3 dB)

#### Method 4: **Improve Matching of Differential Pair**

**Modifications:**
- **Increase area** of M1, M2 (both W and L, maintaining ratio)
- **Common-centroid layout**
- **Matched orientation** of transistors
- **Dummy transistors** around critical devices
- **Interdigitated finger layout**

**How it works:**
- **Threshold voltage mismatch:** $\sigma(\Delta V_T) \propto 1/\sqrt{WL}$
- **Current factor mismatch:** $\sigma(\Delta\beta/\beta) \propto 1/\sqrt{WL}$
- Mismatches create **differential error from common-mode signals**
- Better matching → less conversion of CM to DM

**Expected CMRR increase:** 2-4× (6-12 dB) from layout improvements

#### Method 5: **Add Common-Mode Feedback (CMFB)**

**Modification:**
- Add **CMFB circuit** that senses output common-mode voltage
- **Adjust tail current or load** to correct CM output level

**How it works:**
- **Active correction** of common-mode gain
- Reduces $A_{cm}$ → increases CMRR
- Particularly effective in **fully differential amplifiers**

**Expected CMRR increase:** 10-20 dB

#### Method 6: **Use Active Load with High Output Impedance**

**Modification:**
- Replace simple current mirror load with **cascode active load**
- Wilson or cascoded PMOS current mirror

**How it works:**
- **Load mismatch** contributes to finite CMRR
- Higher load impedance reduces CM signal conversion
- **Current mirror accuracy** affects CMRR

**Expected CMRR increase:** 6-12 dB

---

### Part (b): Trade-offs of Modifications

#### Method 1: Cascode Tail Current Source

**Pros:**
- ✅ **Dramatic CMRR improvement** (20-40 dB)
- ✅ Most effective single modification
- ✅ No change to signal path transistors
- ✅ Relatively simple circuit addition

**Cons:**
- ❌ **Headroom loss:** Need extra $V_{DSsat}$ for cascode device
  - Voltage headroom: $V_{DS,tail} = 2 \times V_{DSsat}$
  - Limits **minimum supply voltage** or **input common-mode range**
- ❌ **Noise increase:** Cascode device adds thermal noise (modest)
- ❌ More complex biasing - need stable $V_{bias}$ for cascode gate
- ❌ Slightly higher mismatch sensitivity (two transistors to match vs. one)

**Impact on functionality:**
- **Input common-mode range reduced** by one $V_{DSsat}$ (≈0.2-0.4 V)
- May not work for **low-voltage designs** (VDD < 1.5V)

---

#### Method 2: Increase Length of Tail Current Source

**Pros:**
- ✅ **Moderate CMRR improvement** (6-12 dB)
- ✅ **No headroom loss** - single device
- ✅ Reduced short-channel effects
- ✅ Better output resistance (more ideal current source)
- ✅ Better matching (larger area)

**Cons:**
- ❌ **Larger area** - cost increase
- ❌ **Higher capacitance** ($C_{db}, C_{sb}$ increase)
  - Degrades frequency response of tail node
  - Affects high-frequency CMRR
- ❌ Diminishing returns - $r_o$ increase sublinear with L in short channels

**Impact on functionality:**
- **AC CMRR degrades faster** with frequency (parasitic capacitance at tail node)
- Slew rate limited slightly by tail node capacitance charging
- Otherwise minimal impact

---

#### Method 3: Increase W/L of Differential Pair

**Pros:**
- ✅ **Modest CMRR improvement** (3 dB per 2× W/L)
- ✅ **Higher transconductance** - more gain
- ✅ **Lower input-referred noise** - better SNR
- ✅ **Better matching** (larger area)
- ✅ Higher $f_T$ - better high-frequency performance

**Cons:**
- ❌ **Much larger gate capacitance** - loads previous stage
  - $C_{gs} \propto WL$ increases significantly
  - If op-amp used in feedback, may affect stability
- ❌ **Larger area**
- ❌ **Higher power to drive gates** (in AC-coupled or dynamic circuits)
- ❌ **Offset voltage** may increase if W increased without careful layout

**Impact on functionality:**
- **Input capacitance increases** - loading effect on source
- **Bandwidth** of input stage may decrease (if $C_{gs}$ dominates)
- **Better for amplifier gain and noise**

---

#### Method 4: Improve Matching (Layout Techniques)

**Pros:**
- ✅ **Moderate CMRR improvement** (6-12 dB)
- ✅ **Lower offset voltage** - critical for precision
- ✅ **Better temperature tracking** - less drift
- ✅ **No circuit changes** - pure layout optimization
- ✅ **No power increase**
- ✅ Benefits **all performance metrics** (gain, CMRR, offset)

**Cons:**
- ❌ **Larger area** (common-centroid, dummy devices)
- ❌ **Layout complexity** - more design time
- ❌ **Routing challenges** - symmetric interconnect required
- ❌ **Requires skilled layout engineer**

**Impact on functionality:**
- **Minimal negative impact**
- Slight area increase
- **High benefit-to-cost ratio** for precision designs

---

#### Method 5: Common-Mode Feedback (CMFB)

**Pros:**
- ✅ **Significant CMRR improvement** (10-20 dB)
- ✅ **Active correction** - adapts to variations
- ✅ **Stabilizes output CM level** - essential for fully differential
- ✅ Can compensate for load imbalance

**Cons:**
- ❌ **High complexity** - CMFB amplifier needed
- ❌ **Additional power consumption** (CMFB loop)
- ❌ **Stability concerns** - new feedback loop to stabilize
  - Need to ensure CMFB loop is stable independently
  - Interaction with main loop possible
- ❌ **More area** (CMFB sense and correction circuits)
- ❌ **CMFB settling time** - may slow overall response

**Impact on functionality:**
- **Fully differential designs:** Almost mandatory, huge benefit
- **Single-ended output:** May be overkill
- **Design complexity** significantly increased

---

#### Method 6: Cascode Active Load

**Pros:**
- ✅ **Moderate CMRR improvement** (6-12 dB)
- ✅ **Higher differential gain** - better $r_o$ in load
- ✅ **Better PSRR** - supply noise rejection improved

**Cons:**
- ❌ **Headroom loss** at output - cascode needs one $V_{DSsat}$
  - **Output swing reduced**
  - Critical for low-voltage designs
- ❌ **More complex biasing** for cascode gates
- ❌ **Parasitic pole** from cascode node capacitance
  - May affect frequency response and stability
- ❌ Higher sensitivity to load mismatch

**Impact on functionality:**
- **Output voltage swing reduced** by $\approx V_{DSsat}$ (0.2-0.4 V)
- **Not suitable for rail-to-rail output** designs
- **Higher gain** may require revisiting compensation strategy

---

### Recommended Strategy for Maximum CMRR

**Best single modification:** **Cascode tail current source** (if headroom allows)

**Comprehensive high-CMRR design:**
1. **Cascode tail current source** (+30 dB)
2. **Large area, well-matched differential pair** (+10 dB layout)
3. **Cascode active load** (+10 dB)
4. **CMFB if fully differential** (+15 dB)

**Total CMRR:** 80-100 dB achievable

**For low-voltage designs (headroom-limited):**
1. **Long-L tail current source** (+8 dB)
2. **Excellent layout matching** (+10 dB)
3. **Large W/L differential pair** (+3 dB)

**Total CMRR:** 60-70 dB achievable without headroom loss

---

### Design Decision Tree

**Question 1: What is your supply voltage?**
- **VDD ≥ 2.5V:** Use cascode techniques (tail and/or load)
- **VDD < 2.5V:** Avoid cascodes, focus on length and matching

**Question 2: Is CMRR critical (>70 dB required)?**
- **Yes:** Use cascode tail + matching + possibly CMFB
- **No:** Increase tail L, basic matching sufficient

**Question 3: Is output swing critical?**
- **Yes:** Avoid cascode load, simple current mirror OK
- **No:** Cascode load for extra gain and CMRR

**Question 4: Is offset voltage critical?**
- **Yes:** Prioritize matching (area, layout), maybe CMFB
- **No:** Focus on CMRR circuit techniques

---

## Summary

This solution sheet provides comprehensive explanations for all six exercises in Home Assignment 2:

1. **W/L Ratio:** Controls current drive, $g_m$, capacitance - key trade-offs between gain, speed, area, and matching
2. **Feedback:** Enables precision, bandwidth, linearity at cost of gain and complexity - stability critical
3. **Second-Order Systems:** Pole placement determines speed vs. stability - damping ratio is key parameter
4. **Bandgap Reference:** Temperature-stable 1.25V from PTAT+CTAT cancellation - standard IC reference
5. **Two-Stage Op-Amp:** Differential pair, active load, second stage, Miller compensation - current and W/L affect gain/GBW/stability trade-offs
6. **CMRR Improvement:** Cascode tail most effective - trade-offs between CMRR, headroom, power, complexity

Each topic includes detailed analysis of principles, trade-offs, design guidelines, and practical considerations for IC design.

---

**Study Tip:** Focus on understanding the **fundamental trade-offs** - they appear in every analog circuit design decision. The specific numbers matter less than the directional relationships and design reasoning.
