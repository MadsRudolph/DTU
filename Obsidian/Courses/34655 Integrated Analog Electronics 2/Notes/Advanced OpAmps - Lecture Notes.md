# Advanced OpAmps - Lecture Notes
**Course:** 34655 Integrated Analog Electronics 2
**Lecturer:** Per B. Lynggaard
**Date:** 2026-02-10

---

## Topics Covered

1. Recap of building blocks for opamps
2. Differential Pair with cascoding techniques
3. Current mirror types and design
4. Current mirror opamp
5. Fully differential opamp with common mode feedback

---

## 1. Recap: Building Blocks for OpAmps

### 1.1 Small Signal Model (Linearization)

The MOSFET is inherently **nonlinear**:
$$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS} - V_t)^2$$

We linearize around a bias point to get the small signal model.

**Transconductance** $g_m$ (input characteristics):
$$g_m = \frac{\partial i_D}{\partial v_{GS}}\bigg|_{\text{Bias}} = \mu C_{ox}\frac{W}{L}(V_{GS} - V_t) = \frac{2I_D}{V_{eff}}$$

Alternative form:
$$g_m = \sqrt{2\mu C_{ox}\frac{W}{L}I_D}$$

**Output conductance** $g_{ds}$ (channel length modulation):
$$g_{ds} = \frac{1}{r_{ds}} = \frac{\partial i_D}{\partial v_{DS}}\bigg|_{\text{Bias}} \approx I_D\lambda$$

$$r_{ds} \approx \frac{1}{I_D\lambda} = \frac{V_A}{I_D}$$

> **Note:** Capital letters denote bias point values, lowercase denote small signal.

---

### 1.2 Current Mirror

- Mirrors and scales currents: $I_{out} = K \cdot I_B$ (where K is the W/L ratio)
- Output impedance can be increased using cascode transistors
- Very useful for distributing bias currents throughout a circuit

---

### 1.3 Common Source Stage

| Property | Value |
|----------|-------|
| Gain | $A_v = -g_m(r_{ds} \parallel R_L)$ |
| Open-circuit gain | $A_{voc} = -g_m r_{ds}$ |
| Output impedance | $r_o = r_{ds}$ |
| Input impedance | $r_{in} = +\infty$ |

- **Inverting gain**
- Gate-drain capacitance exposed to **Miller effect**
- Very commonly used gain stage

---

### 1.4 Common Drain Stage (Source Follower)

| Property | Value |
|----------|-------|
| Gain (no bulk effect) | $A_v = \frac{g_m}{g_m + g_{ds}} \approx 1 - \frac{g_{ds}}{g_m} \leq 1$ |
| Gain (with bulk effect) | $A_v = \frac{g_m}{g_m + g_s + g_{ds}}$ |
| Output impedance | $r_o = \frac{1}{g_m}$ |
| Input impedance | $r_{in} = +\infty$ |

- Often used as **output stage**
- **Non-inverting** gain
- **Low output impedance**
- If bulk effect present, gain is somewhat below 1

---

### 1.5 Common Gate Stage

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = g_m r_{ds}$ |
| Output impedance | $r_o = r_{ds}(1 + R_S g_m)$ |
| Input impedance | $r_{in} = \frac{1}{g_m}\left(1 + \frac{R_L}{r_{ds}}\right)$ |

- **Low input impedance** (if $R_L$ not large)
- Can obtain **high output impedance**

---

### 1.6 Differential Stage

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = g_{m1}(r_{ds1} \parallel r_{ds4})$ |
| Output impedance | $r_o = r_{ds1} \parallel r_{ds4}$ |

- **High differential gain**
- **Low common mode gain** (ideally zero) → high CMRR
- **Transistor pairs must be matched!** $(W/L)_1 = (W/L)_2$ and $(W/L)_3 = (W/L)_4$

---

### 1.7 Cascode Stages

**Telescopic Cascode:** Common Source followed by Common Gate

| Property | Value |
|----------|-------|
| Open-circuit gain | $A_{voc} = -A_{i1}A_{i2} = -g_{m1}r_{ds1}g_{m2}r_{ds2}$ |
| Output impedance | $r_o = r_{ds1}A_{i2} = r_{ds1}g_{m2}r_{ds2}$ |

Where $A_i$ is the intrinsic gain of a transistor.

**Key advantages:**
- Very high gain and output resistance
- Gate-drain capacitance of M1 **not exposed to Miller effect** (source of M2 has low signal swing)

---

### 1.8 Cascade Stages (Two CS stages in series)

| Property | Value |
|----------|-------|
| Stage 1 gain | $A_1 = -g_{m1}r_{ds1}$ |
| Stage 2 gain | $A_2 = -g_{m2}r_{ds2}$ |
| Total gain | $A_v = A_1 A_2 = g_{m1}r_{ds1}g_{m2}r_{ds2}$ |
| Output impedance | $r_o = r_{ds2}$ |

- Each stage analyzed individually (but remember loading effects)
- Gain same as cascode but **opposite sign**
- **Output impedance smaller** than cascode

---

## 2. The Two-Stage OpAmp

### Structure
- **Stage 1:** Differential-input first stage
- **Stage 2:** Common-source second stage
- **Bias circuitry** for current reference

### Key Equations

| Parameter | Expression |
|-----------|------------|
| Open-loop gain | $\|A_o\| = G_{diff}G_{CS} = g_{m1}(r_{ds2}\parallel r_{ds4})g_{m7}(r_{ds6}\parallel r_{ds7})$ |
| Approximation | $\sim \frac{1}{4}g_m^2 r_{ds}^2$ |
| Dominant pole | $\omega_o^{-1} = (r_{ds2}\parallel r_{ds4})A_{CS}C_C$ (Miller effect) |
| Zero | $\omega_z \approx \frac{-g_{m7}}{C_C}$ |
| Non-dominant pole | $\omega_{p2} \approx \frac{g_{m7}}{C_1 + C_2 + \frac{C_1 C_2}{C_C}}$ |
| Output swing max | $V_{o,max} = V_{DD} - \|V_{eff6}\|$ |
| Output swing min | $V_{o,min} = V_{eff7}$ |

> **Problem:** Performance of the simple two-stage OpAmp is often insufficient in terms of GBW, Noise, Slew Rate...

---

## 3. Improving the OpAmp with Cascoding

### 3.1 Differential Pair with Cascode

Adding cascodes to the differential pair increases gain:
$$A_{voc} = -A_{i1}A_{i2} = -g_{m1}r_{ds1}g_{m2}r_{ds2}$$

Output impedance increased:
$$r_o = r_{ds1}g_{m2}r_{ds2} \sim r_{ds}g_m r_{ds}$$

**Problem:** A simple current mirror would result in $r_o \approx r_{ds}$ in parallel with $r_{ds}g_m r_{ds}$, wasting the high cascode output resistance.

→ **A better (cascode) current mirror is needed!**

---

## 4. Current Mirror Types

### 4.1 Cascode Current Mirror

**Output impedance increased:**
$$r_{out} = r_{ds2}A_{i4} = r_{ds2}g_{m4}r_{ds4}$$

**Input impedance (still low):**
$$r_{in} = \frac{1}{g_{m1}}\parallel r_{ds1} + \frac{1}{g_{m3}}\parallel r_{ds3}$$

**Problem - Minimum output voltage increased:**
$$V_{o,min} = V_{GS1} + V_{eff4} = V_{tn} + V_{eff1} + V_{eff4} \sim V_t + 2V_{eff}$$

Compared to simple current mirror: $V_{o,min} = V_{eff}$

> **Typical values:** $V_{eff} \sim 100-200$ mV, $V_t \sim 500-600$ mV

---

### 4.2 Wide-Swing Cascode Current Mirror

**Key improvement:** Reduces minimum output voltage!

$$V_{o,min} = V_{eff1} + V_{GS3} - V_{GS4} + V_{eff4}$$

Since $V_{GS3} = V_{GS4}$:
$$V_{o,min} = V_{eff1} + V_{eff4} \sim 2V_{eff}$$

**Much better than regular cascode:** $\sim V_t + 2V_{eff}$

### Design Rule for Wide-Swing Cascode

To find W/L for the bias transistor M5:

**Principle:** Bias VDS of transistors as close to minimum as possible without leaving saturation.

**Result:**
$$\left(\frac{W}{L}\right)_3 = 4\left(\frac{W}{L}\right)_5$$

This ensures $V_{eff5} = 2V_{eff}$, keeping M1 and M2 just in saturation.

---

### 4.3 Self-Regulating Current Mirror (Enhanced Output Impedance)

Add an amplifier around the cascode transistor:

**Output impedance increased by factor A:**
$$r_o \approx r_{ds2}A_{i1}(1+A) \approx r_{ds2}g_{m1}r_{ds1}A \sim g_m r_{ds}^2 A$$

**Using a current mirror as amplifier:**
$$V_{DS2} = 2V_{eff2} - V_{eff4} \sim V_{eff}$$

---

## 5. Differential Pair with Full Cascode

### With Cascode Current Mirror Load

**Output impedances (both high):**
$$r_{o,n} = r_{ds2}A_{i6} = r_{ds2}g_{m6}r_{ds6}$$
$$r_{o,p} = r_{ds4}A_{i8} = r_{ds4}g_{m8}r_{ds8}$$

**High gain:**
$$|A_o| = g_{m1}r_o = g_{m1}[(r_{ds2}g_{m6}r_{ds6})\parallel(r_{ds4}g_{m8}r_{ds8})] \sim \frac{1}{2}g_m^2 r_{ds}^2$$

**Dominant pole from load (all internal nodes low impedance):**
$$\omega_o^{-1} = r_o C_L \sim \frac{1}{2}g_m r_{ds}^2 C_L$$

### Output Voltage Swing Problem

**Maximum output:**
$$V_{o,max} = V_{DD} - |V_{GS3}| - |V_{GS7}| + |V_{GS8}| - |V_{eff8}| = V_{DD} - V_t - 2V_{eff}$$

**Minimum output (worst case: unity feedback, $V_{IN} = V_{DD}/2$):**
$$V_{o,min} = \frac{1}{2}V_{DD} - V_t + V_{eff}$$

→ **Output swing very limited!**

---

### With Wide-Swing Cascodes

**Maximum output improved by $V_t$:**
$$V_{o,max} = V_{DD} - |V_{eff4}| - |V_{eff8}| \sim V_{DD} - 2V_{eff}$$

**Minimum output unchanged:**
$$V_{o,min} \sim \frac{1}{2}V_{DD} - V_t + V_{eff}$$

→ Minimum output voltage **still a problem**

---

## 6. Folded Cascode Stage

**Key idea:** Use NMOS and PMOS together instead of two transistors of same type.

### Comparison: Telescopic vs Folded

| Property | Telescopic | Folded |
|----------|------------|--------|
| Output impedance | $r_o = r_{ds1}g_{m2}r_{ds2} \sim g_m r_{ds}^2$ | Same |
| Minimum output | $V_{o,min} = V_{eff1} + V_{eff2} \sim 2V_{eff}$ | $V_{o,min} = V_{eff1} - \|V_{eff2}\| \sim 0$ |

**Folded cascode achieves near-zero minimum output voltage!**

---

## 7. Folded Cascode Differential Pair (OpAmp)

### Key Parameters

**Gain (similar to two-stage OpAmp):**
$$|A_o| = g_{m1}[([r_{ds4}\parallel r_{ds2}]g_{m6}r_{ds6})\parallel(r_{ds10}g_{m8}r_{ds8})] \sim \frac{1}{3}g_m^2 r_{ds}^2$$

**Dominant pole (all internal nodes low impedance):**
$$\omega_o^{-1} = r_o C_L \sim \frac{1}{3}g_m r_{ds}^2 C_L$$

### Output Voltage Swing

| Parameter | Value | Comparison |
|-----------|-------|------------|
| $V_{o,min}$ | $V_{eff10} + V_{eff8} \sim 2V_{eff}$ | **Better** than WS-cascode |
| $V_{o,max}$ | $V_{DD} - \|V_{eff4}\| - \|V_{eff6}\| \sim V_{DD} - 2V_{eff}$ | Same as WS-cascode |

---

## 8. Current Mirror OpAmp

Uses current mirrors to achieve additional gain factor K.

### Key Parameters

**Gain:**
$$A_v(s) = \frac{Kg_{m1}r_o}{1 + sr_oC_L}$$

**DC Gain:**
$$A_0 = Kg_{m1}r_o$$

**Dominant pole:**
$$\omega_0^{-1} = r_o C_L$$

- All internal nodes have low impedance
- Same as folded cascode OpAmp but with **extra gain factor K**

---

## 9. Fully Differential OpAmp

### Advantages of Differential Output

1. **Suppresses common mode noise**
2. **Suppresses even-order distortion**
3. **SNR improved by potentially 3dB**
4. **Signal swing doubled** ($2V_{pp,max}$ vs $V_{pp,max}$)

### Common Mode Feedback (CMFB)

**Problem:** Without CMFB, the output will drift to one of the supply rails.

**Solution:** Add CMFB circuit to set a well-defined common-mode output voltage level.

The CMFB circuit:
- Senses the average (common-mode) of both outputs
- Compares it to a reference voltage
- Adjusts the bias current to maintain the desired common-mode level

---

## Summary Table: OpAmp Topologies

| Topology | Gain | Dominant Pole | $V_{o,min}$ | $V_{o,max}$ |
|----------|------|---------------|-------------|-------------|
| Two-stage | $\frac{1}{4}g_m^2 r_{ds}^2$ | Miller: $\frac{1}{4}g_m r_{ds}^2 C_C$ | $V_{eff}$ | $V_{DD}-V_{eff}$ |
| Telescopic cascode | $\frac{1}{2}g_m^2 r_{ds}^2$ | $\frac{1}{2}g_m r_{ds}^2 C_L$ | $\frac{1}{2}V_{DD}-V_t+V_{eff}$ | $V_{DD}-V_t-2V_{eff}$ |
| WS-Cascode | $\frac{1}{2}g_m^2 r_{ds}^2$ | $\frac{1}{2}g_m r_{ds}^2 C_L$ | $\frac{1}{2}V_{DD}-V_t+V_{eff}$ | $V_{DD}-2V_{eff}$ |
| Folded cascode | $\frac{1}{3}g_m^2 r_{ds}^2$ | $\frac{1}{3}g_m r_{ds}^2 C_L$ | $2V_{eff}$ | $V_{DD}-2V_{eff}$ |
| Current mirror | $\frac{K}{3}g_m^2 r_{ds}^2$ | $\frac{1}{3}g_m r_{ds}^2 C_L$ | $2V_{eff}$ | $V_{DD}-2V_{eff}$ |

---

## Key Takeaways

1. **Cascoding increases both gain and output impedance** by approximately the intrinsic gain factor $A_i = g_m r_{ds}$

2. **Wide-swing cascodes** reduce the voltage headroom penalty of regular cascodes from $V_t + 2V_{eff}$ to $2V_{eff}$

3. **Folded cascodes** provide the best output voltage swing (nearly rail-to-rail) while maintaining high gain

4. **Current mirrors must match the impedance** of the stage they load - a simple mirror wastes the high impedance of a cascode stage

5. **Fully differential outputs** suppress common-mode noise and even-order distortion but **require CMFB** to set the output common-mode level

6. **All internal nodes should have low impedance** so the dominant pole comes from the output load, not internal nodes (avoids Miller effect issues)
