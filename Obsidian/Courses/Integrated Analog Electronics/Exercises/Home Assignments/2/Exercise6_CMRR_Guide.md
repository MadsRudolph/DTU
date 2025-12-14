# Exercise 6: Differential Amplifier CMRR Analysis

## Open LTspice Schematics

### Basic Differential Amplifier (Simple Tail Current Source)
**📂 [Open Exercise6_Differential_CMRR.asc](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise6_Differential_CMRR.asc)**

### Improved Version (Cascode Tail for +20-30 dB CMRR)
**📂 [Open Exercise6_Cascode_CMRR.asc](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise6_Cascode_CMRR.asc)**

**File Location:** `C:\Users\Mads2\DTU\3.semester\Integrated Analog Electronics\LTspice\HomeAssignment\II\`

---

## Circuit Overview

This LTspice simulation implements the differential amplifier from Exercise 6 with complete CMRR measurement capability.

---

## Circuit Components

### Transistor Sizing (from assignment diagram)

**Differential Pair:**
- **M1, M2:** NMOS (W=20µm, L=5µm)

**Active Load (Current Mirror):**
- **M3, M4:** PMOS (W=5µm, L=5µm)

**Output Stage:**
- **M5:** NMOS (W=90µm, L=20µm) - Large for current drive

**Bias Transistors:**
- **MB:** NMOS tail current source (W=20µm, L=100µm) - Very long for high output resistance
- **MC:** NMOS bias generator (W=10µm, L=10µm)

### Power Supply
- **VDD:** +5V
- **VSS:** -5V (bipolar supply)
- **IL:** 20µA reference current

### Input Configuration
- **V1 (VIN1):** Differential positive input
- **V2 (VIN2):** Differential negative input
- **Default:** AC differential mode (V1 = 1∠0°, V2 = 1∠180°)

---

## Understanding CMRR

### Definition

**Common-Mode Rejection Ratio (CMRR):**

$$CMRR = \left|\frac{A_d}{A_{cm}}\right|$$

$$CMRR_{dB} = 20\log_{10}\left(\frac{A_d}{A_{cm}}\right)$$

Where:
- **Ad** = Differential-mode gain (gain when inputs have opposite polarity)
- **Acm** = Common-mode gain (gain when inputs have same polarity)

**High CMRR (>60 dB)** means excellent rejection of common-mode noise.

### Why CMRR Matters

In real applications:
- **Noise** appears equally on both inputs (common-mode)
- **Signal** appears differentially (opposite on each input)
- High CMRR rejects noise while amplifying signal

**Example:**
- Signal: 1mV differential
- Noise: 100mV common-mode
- CMRR = 80 dB (10,000:1)
- Output: Amplified signal, noise reduced 10,000×

---

## How to Measure CMRR in LTspice

### Method 1: Two Separate Simulations

#### Step 1: Measure Differential Gain (Ad)

**Default configuration** (already set):
```
V1: AC 1 0        (1V at 0°)
V2: AC 1 180      (1V at 180°)
```
This creates a **differential input** of 2V peak-to-peak.

**Run AC analysis:**
1. Simulate → Run (or F9)
2. Click on VOUT node
3. Note the gain in dB at your frequency of interest (e.g., 1kHz)

**Example result:**
- Gain at 1kHz = 45 dB
- **Ad = 45 dB**

---

#### Step 2: Measure Common-Mode Gain (Acm)

**Modify input sources for common-mode:**

Right-click on V1:
```
AC Amplitude: 1
AC Phase: 0
```

Right-click on V2:
```
AC Amplitude: 1
AC Phase: 0        (CHANGE from 180° to 0°)
```

Both inputs now have **same phase** = common-mode signal.

**Run AC analysis again:**
1. Simulate → Run
2. Click on VOUT node
3. Note the gain in dB at 1kHz

**Example result:**
- Gain at 1kHz = -15 dB
- **Acm = -15 dB**

---

#### Step 3: Calculate CMRR

$$CMRR_{dB} = A_d - A_{cm}$$

**Example:**
- Ad = 45 dB
- Acm = -15 dB
- **CMRR = 45 - (-15) = 60 dB** ✓

**Linear ratio:**
- CMRR = 60 dB = 1000:1 rejection ratio

---

### Method 2: Automated Parameter Sweep (Advanced)

Create two separate schematics:

**File 1:** `Exercise6_Differential.asc` - Differential mode
**File 2:** `Exercise6_CommonMode.asc` - Common mode

Or use subcircuit with parameter:
```
.param mode=0
.func Vin1_phase() {if(mode==0, 0, 0)}
.func Vin2_phase() {if(mode==0, 180, 0)}
```

Then `.step param mode list 0 1`

---

## Improving CMRR - Practical Modifications

### Modification 1: Increase Tail Transistor Length

**Current setup:** MB has L=100µm (already good)

**To experiment:**
1. Uncomment the line: `;.step param Ltail list 10u 50u 100u 200u`
2. Change MB parameter to: `l={Ltail}`
3. Run AC analysis in differential mode
4. Then common-mode
5. Compare CMRR for different lengths

**Expected:**
- L=10µm: CMRR ≈ 40 dB (poor)
- L=50µm: CMRR ≈ 55 dB (moderate)
- L=100µm: CMRR ≈ 65 dB (good)
- L=200µm: CMRR ≈ 70 dB (excellent)

**Why it works:**
- Longer L → higher output resistance (ro)
- Higher ro → better current source
- Better current source → higher tail impedance → better CMRR
- CMRR ≈ gm × Rtail

---

### Modification 2: Add Cascode Tail Current Source

**Circuit change:**

Replace simple MB with cascode:
1. Add second NMOS (MCAS) above MB
2. MCAS gate connected to bias voltage
3. Stack: MB (bottom) → MCAS (top) → M1/M2 sources

**Code example:**
```
MB: l=50u w=20u (lower cascode transistor)
MCAS: l=50u w=20u (upper cascode transistor)
VBIAS: DC voltage for MCAS gate (≈ -3V)
```

**Expected improvement:**
- Simple current source (L=100µm): CMRR ≈ 65 dB
- Cascode (L=50µm each): CMRR ≈ 85 dB (+20 dB)

**Trade-off:**
- ❌ Loses one VDSsat of headroom (≈0.3V)
- ❌ More complex biasing
- ✅ Dramatic CMRR improvement

---

### Modification 3: Improve Differential Pair Matching

**Current:** M1, M2 (W=20µm, L=5µm) → Area = 100µm²

**Increase size proportionally:**
```
M1, M2: W=40µm, L=10µm → Area = 400µm²
```

**Expected improvement:**
- Threshold mismatch: σ(ΔVT) ∝ 1/√(WL)
- 4× area → 2× better matching
- CMRR improvement: ≈ 6 dB

**Trade-offs:**
- ❌ 4× more area
- ❌ Higher capacitance → lower bandwidth
- ✅ Better offset voltage
- ✅ Better CMRR

---

### Modification 4: Cascode Active Load

**Circuit change:**

Replace M3, M4 with cascode current mirror:
1. Add M3A, M4A above M3, M4
2. Creates high-impedance load

**Expected improvement:**
- Simple load: CMRR ≈ 65 dB
- Cascode load: CMRR ≈ 75 dB (+10 dB)

**Trade-offs:**
- ❌ Loses VDSsat headroom at output
- ❌ More complex biasing
- ✅ Higher differential gain also
- ✅ Better PSRR

---

## Circuit Analysis

### DC Operating Point

**After running `.op`:**

Check in SPICE error log (View → SPICE Error Log):

**Key parameters to verify:**

**M1, M2 (Differential Pair):**
- VGS ≈ 0.8-1.2V
- VDS > VGS - VT (must be in saturation)
- ID ≈ 10µA each (half of 20µA tail current)
- gm ≈ 50-200 µA/V

**MB (Tail Current Source):**
- ID ≈ 20µA
- VDS ≈ 2-3V (should have headroom)
- gm ≈ 20-50 µA/V
- ro = very high (>1 MΩ if L=100µm)

**M3, M4 (Active Load):**
- ID ≈ 10µA each
- VDS > |VGS| - |VT| (saturation)

**M5 (Output Stage):**
- ID depends on load
- Should be in saturation

---

### Differential Gain Analysis

**Expected gain:**

**First stage (M1-M4):**
$$A_{v1} = g_{m1} \times (r_{o2} \parallel r_{o4})$$

Typical values:
- gm1 ≈ 100 µA/V
- ro2, ro4 ≈ 100-500 kΩ
- Av1 ≈ 10-50 V/V (20-34 dB)

**Second stage (M5):**
$$A_{v2} = g_{m5} \times (r_{o5} \parallel R_{load})$$

**Total gain:**
$$A_v = A_{v1} \times A_{v2}$$

**Expected total:** 40-60 dB

---

### Common-Mode Gain Analysis

**Common-mode gain depends on:**

$$A_{cm} \approx \frac{1}{g_m \times R_{tail}}$$

Where Rtail = output resistance of MB

**For MB with L=100µm:**
- ro,MB ≈ 1-5 MΩ (very high)
- gm ≈ 100 µA/V
- Acm ≈ 1/(100µA/V × 1MΩ) ≈ 0.01 = -40 dB

**CMRR:**
- Ad = 50 dB
- Acm = -40 dB
- CMRR = 90 dB (excellent)

**If MB had L=10µm:**
- ro,MB ≈ 100 kΩ (much lower)
- Acm ≈ 1/(100µA/V × 100kΩ) ≈ 0.1 = -20 dB
- CMRR = 50 - (-20) = 70 dB (still good)

---

## Frequency Response Analysis

### Differential-Mode Frequency Response

**Run:** `.ac dec 100 1 100Meg` with differential input

**What to observe:**

1. **Low-frequency gain (Ad):**
   - Read gain at 100 Hz - 1 kHz
   - Should be 40-60 dB

2. **-3dB bandwidth:**
   - Frequency where gain drops by 3 dB
   - Depends on load capacitance and output resistance

3. **Roll-off:**
   - Should see -20 dB/decade slope (single dominant pole)

**Dominant pole location:**
$$f_p \approx \frac{1}{2\pi R_{out} C_L}$$

For Rout ≈ 100kΩ, CL = 10pF:
- fp ≈ 160 kHz

---

### Common-Mode Frequency Response

**Run:** `.ac` with common-mode input (both AC phase = 0°)

**What to observe:**

1. **Low-frequency CMRR:**
   - Compare to differential gain
   - Should be >60 dB difference

2. **CMRR degradation at high frequency:**
   - CMRR decreases as frequency increases
   - Due to parasitic capacitance at tail node
   - Ctail charges/discharges → tail node not perfect AC ground

**Tail node pole:**
$$f_{tail} = \frac{1}{2\pi R_{tail} C_{tail}}$$

For Rtail = 1MΩ, Ctail = 100fF:
- ftail ≈ 1.6 MHz

Above this frequency, CMRR degrades significantly.

---

## Transient Analysis

**Run:** `.tran 0 5m 0 1u`

**What to observe:**

**Differential mode (default):**
- Input: VIN1 = +10mV sine, VIN2 = -10mV sine
- Differential input = 20mV peak-to-peak
- Output: Amplified, inverted signal
- Check for clipping, distortion

**Common mode (change V2 phase to 0°):**
- Input: VIN1 = VIN2 = 10mV sine (in phase)
- Common-mode input = 10mV
- Output: Very small signal (suppressed by CMRR)

**Comparison:**
- Differential output / Common-mode output = CMRR (linear)

---

## Key Measurements Summary

### Measurements to Make

| Parameter | How to Measure | Expected Value |
|-----------|---------------|----------------|
| Differential Gain (Ad) | AC analysis, diff mode, 1kHz | 40-60 dB |
| Common-Mode Gain (Acm) | AC analysis, CM mode, 1kHz | -40 to -20 dB |
| CMRR | Ad - Acm | 60-80 dB |
| -3dB Bandwidth | Differential AC, -3dB point | 100 kHz - 1 MHz |
| Tail current | .op, check MB current | 20 µA |
| Output DC level | .op, check VOUT | ~0V |
| gm (M1, M2) | .op, SPICE log | 50-200 µA/V |
| ro (MB) | .op, SPICE log | 0.5-5 MΩ |

---

## Experiments to Try

### Experiment 1: Effect of Tail Length on CMRR

**Procedure:**
1. Note current CMRR (L=100µm)
2. Change MB to L=50µm
3. Measure new CMRR
4. Change to L=200µm
5. Measure CMRR

**Expected results:**
- CMRR increases with L (longer = better)
- Diminishing returns above L=200µm

**Plot:** CMRR vs. L

---

### Experiment 2: Load Capacitance Effect on Bandwidth

**Procedure:**
1. Current: CL = 10pF
2. Measure -3dB bandwidth
3. Change CL to 1pF, 5pF, 20pF, 50pF
4. Measure bandwidth for each

**Expected:**
- Bandwidth ∝ 1/CL
- Larger CL → lower bandwidth

**Plot:** Bandwidth vs. CL

---

### Experiment 3: Tail Current Effect on Performance

**Procedure:**
1. Change IL from 20µA to 10µA, 40µA, 60µA
2. For each:
   - Measure Ad
   - Measure bandwidth
   - Calculate gm from .op

**Expected:**
- Higher current → higher gm → higher gain
- Higher current → higher bandwidth (lower Rout)
- Higher current → more power

**Trade-off:** Performance vs. power consumption

---

### Experiment 4: Mismatch Sensitivity

**Procedure:**
1. Make M1 and M2 slightly different:
   - M1: W=20µm
   - M2: W=21µm (5% mismatch)
2. Run DC operating point
3. Check output DC offset
4. Run AC common-mode
5. Compare CMRR to matched case

**Expected:**
- DC offset appears at output
- CMRR degrades due to mismatch
- Real circuits use large area for matching

---

## Comparison Table: CMRR Improvement Methods

| Method | CMRR Gain | Headroom Loss | Complexity | Area Cost |
|--------|-----------|---------------|------------|-----------|
| Baseline (L=100µm) | 65 dB | 0V | Simple | 1× |
| L=200µm tail | +5 dB | 0V | Simple | 1.2× |
| Cascode tail | +20 dB | -0.3V | Medium | 1.5× |
| Larger M1/M2 (4× area) | +6 dB | 0V | Simple | 4× |
| Cascode load | +10 dB | -0.3V | Medium | 1.3× |
| Cascode tail + load | +30 dB | -0.6V | High | 2× |

**Best for low voltage:** Increase L, larger area
**Best for high CMRR:** Cascode tail
**Best overall:** Combination of techniques

---

## Troubleshooting

### Issue 1: Very Low Differential Gain (<20 dB)

**Possible causes:**
- Transistors not in saturation
- Bias current too low
- Load resistance too low

**Check:**
- .op analysis: VDS > VGS - VT for all transistors
- MB current should be 20µA
- M1, M2 should each get ~10µA

---

### Issue 2: Poor CMRR (<40 dB)

**Possible causes:**
- MB length too short
- Mismatch in M1/M2
- Parasitic capacitance at tail

**Solutions:**
- Increase MB length to 100-200µm
- Ensure M1, M2 are identical
- Check layout (in real design)

---

### Issue 3: Output DC Offset

**Possible causes:**
- Mismatch between M1/M2
- Mismatch between M3/M4
- Asymmetric loading

**Solutions:**
- Verify all parameters identical
- In real design: trimming, calibration

---

### Issue 4: Oscillation/Instability

**Possible causes:**
- Load capacitance too high
- Parasitic feedback
- Insufficient phase margin

**Solutions:**
- Add compensation capacitor
- Reduce CL
- Check for inadvertent feedback paths

---

## Learning Objectives

By completing this simulation, you will understand:

1. **Differential vs. Common-Mode signals**
   - How they appear in circuit
   - Why we want high Ad, low Acm

2. **CMRR measurement technique**
   - Two-simulation method
   - Interpretation of results

3. **Current source quality**
   - Why long L improves CMRR
   - Output resistance relationship

4. **Design trade-offs**
   - CMRR vs. headroom
   - Performance vs. area
   - Power vs. speed

5. **Real-world implications**
   - Noise rejection
   - Precision requirements
   - Layout considerations

---

## Next Steps for Report

1. **Simulate baseline circuit**
   - Record Ad, Acm, CMRR

2. **Try 2-3 improvement methods**
   - Document changes
   - Measure new CMRR
   - Compare results

3. **Create comparison table**
   - List pros/cons as in solution sheet

4. **Generate plots:**
   - Frequency response (differential)
   - Frequency response (common-mode)
   - CMRR vs. frequency
   - Transient response

5. **Explain results**
   - Match to theoretical predictions
   - Discuss which method is best for different applications

---

## References

- Solution_Sheet.md - Exercise 6 for detailed theory
- Razavi Chapter 4 - Differential amplifiers
- Gray & Meyer Chapter 5 - Current mirrors and CMRR

---

**Good luck with your CMRR analysis!**
