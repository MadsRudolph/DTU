# LTspice Simulation - Exercise 5 Two-Stage Op-Amp

## Open LTspice Schematic

**📂 [Open Exercise5_TwoStage_OpAmp.asc](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise5_TwoStage_OpAmp.asc)**

**File Location:** `C:\Users\Mads2\DTU\3.semester\Integrated Analog Electronics\LTspice\HomeAssignment\II\Exercise5_TwoStage_OpAmp.asc`

---

## File Information

This LTspice schematic implements the two-stage CMOS operational amplifier from Exercise 5.

---

## Circuit Components

### Main Transistors
- **M1, M2:** NMOS differential input pair (W=50µm, L=1µm)
- **M3, M4:** NMOS current mirror tail (W=20µm, L=2µm - longer for better output resistance)
- **M5, M6:** PMOS current mirror active load (W=50µm, L=1µm)
- **M7:** NMOS output/second stage (W=100µm, L=1µm)

### Key Components
- **VDD:** 5V power supply
- **RBIAS:** 100kΩ bias resistor (sets tail current)
- **CC:** 5pF Miller compensation capacitor
- **CL:** 10pF load capacitance
- **CA, CB:** 1pF parasitic capacitances
- **ROUT:** 1kΩ output resistance

### Input Sources
- **VIN_P:** Positive input (DC: 2.5V, AC: 10mV, 1kHz sine wave)
- **VIN_N:** Negative input (DC: 2.5V, AC: -10mV, 1kHz sine wave)
- Both configured for differential AC analysis

---

## MOSFET Models

### NMOS Model (NMOS_5V)
```
Level = 1 (Shichman-Hodges)
VTO = 0.7V (threshold voltage)
KP = 200µA/V² (transconductance parameter)
Lambda = 0.02 V⁻¹ (channel-length modulation)
Gamma = 0.4 (body effect parameter)
Phi = 0.7V (surface potential)
```

### PMOS Model (PMOS_5V)
```
Level = 1 (Shichman-Hodges)
VTO = -0.7V (threshold voltage)
KP = 100µA/V² (transconductance parameter, ~50% of NMOS)
Lambda = 0.02 V⁻¹ (channel-length modulation)
Gamma = 0.4 (body effect parameter)
Phi = 0.7V (surface potential)
```

---

## Included Simulations

The schematic includes three simulation commands:

### 1. **Operating Point Analysis** (.op)
Calculates DC operating point of all nodes and transistor parameters.

**To run:**
- Menu: `Simulate → Edit Simulation Cmd`
- Select `.op` tab
- Click OK, then Run

**What to check:**
- All transistors in saturation (VDS > VGS - VT)
- Reasonable bias currents (10-100µA range)
- Output voltage around mid-supply (2.5V)

---

### 2. **Transient Analysis** (.tran 0 5m 0 1u)
Time-domain simulation for 5ms with 1µs time step.

**To run:**
- Menu: `Simulate → Edit Simulation Cmd`
- Select `.tran` tab
- Settings: Stop time = 5m, Time to start saving = 0, Max timestep = 1u
- Click OK, then Run

**What to observe:**
- Input differential signal (VIN+ - VIN-)
- Output voltage VOUT
- Phase relationship (should be inverted for differential amplifier)
- Slew rate limits during large signal swings
- Settling behavior

**Expected results:**
- Gain ≈ 60-80 dB (1000-10000 V/V)
- Output should be amplified version of input
- Some distortion possible at high amplitude

---

### 3. **AC Analysis** (.ac dec 100 1 100Meg)
Frequency response from 1 Hz to 100 MHz, 100 points per decade.

**To run:**
- Menu: `Simulate → Edit Simulation Cmd`
- Select `.ac` tab
- Type: Decade, Points/decade: 100, Start: 1, Stop: 100Meg
- Click OK, then Run

**What to observe:**
Click on VOUT node to plot:
- **Magnitude:** Shows gain vs. frequency
  - DC gain (low frequency)
  - -3dB bandwidth
  - Unity-gain frequency (GBW)
  - Roll-off slope (-20dB/dec for single pole)

- **Phase:** Right-click plot → Add Trace → `phase(V(VOUT))`
  - Phase shift vs. frequency
  - Phase margin at unity-gain frequency

**Expected results:**
- **DC Gain:** 60-80 dB
- **GBW (Unity-gain frequency):** ~10-100 MHz (depends on gm1 and CC)
  - GBW = gm1 / (2π × CC) ≈ (2mA/V) / (2π × 5pF) ≈ 64 MHz
- **Phase margin:** Should be ≥45° (preferably ≥60°) for stability
- **Dominant pole:** ~100 Hz to 1 kHz (set by CC and output resistance)

---

## How to Analyze Key Parameters

### 1. **Calculate Transconductance (gm)**
After running `.op`:
- View → SPICE Error Log
- Look for transistor parameters
- Find `gm` for M1, M2, M7

**Expected:**
- gm1, gm2 ≈ 0.5 - 2 mA/V
- gm7 ≈ 1 - 3 mA/V

### 2. **Measure DC Gain (Av)**
From AC analysis:
- Cursor at lowest frequency point on magnitude plot
- Read dB value directly
- Or: Av = 20log(Vout/Vin)

**Formula:**
- First stage: Av1 = gm1 × (ro2 || ro6)
- Second stage: Av2 = gm7 × ro7
- Total: Av = Av1 × Av2

### 3. **Measure GBW**
From AC analysis magnitude plot:
- Find frequency where gain = 0 dB
- This is the unity-gain frequency = GBW

**Formula:**
GBW = gm1 / (2π × CC)

### 4. **Measure Phase Margin**
From AC analysis:
1. Find unity-gain frequency (f_u) from magnitude plot (0 dB crossing)
2. Plot phase: Right-click → Add Trace → `phase(V(VOUT))`
3. Read phase at f_u
4. Phase Margin = 180° + phase(f_u)

**Example:**
- If phase = -120° at f_u
- PM = 180° - 120° = 60° ✓ (stable)

**Requirement:** PM ≥ 45° (preferably ≥60°)

### 5. **Measure Slew Rate**
From transient analysis:
- Apply large step input (modify VIN to PULSE)
- Measure output slope: SR = ΔV/Δt

**Formula:**
SR = Itail / CC = Ibias / CC

For typical values:
- Itail ≈ 50µA, CC = 5pF
- SR ≈ 10 V/µs

---

## Modifying the Circuit

### To increase Gain:
1. **Increase transistor length (L)** → higher ro → higher gain
   - Change M1-M7 from `l=1u` to `l=2u`
2. **Increase bias current** → higher gm (but lower ro, net effect varies)

### To increase Bandwidth (GBW):
1. **Decrease CC** (WARNING: may cause instability)
   - Change CC from `5p` to `3p`
2. **Increase bias current** → higher gm → higher GBW
   - Decrease RBIAS from `100k` to `50k`

### To improve Stability (Phase Margin):
1. **Increase CC** → more compensation
   - Change CC from `5p` to `10p`
2. **Decrease load capacitance CL**
   - Change CL from `10p` to `5p`

### To change Bias Current:
**Current calculation:**
- Ibias ≈ (VDD - VGS3) / RBIAS
- For VGS ≈ 1.5V, VDD = 5V: Ibias ≈ 3.5V / 100kΩ = 35µA

**To increase current:**
- Decrease RBIAS (e.g., 50kΩ → 70µA)

**To decrease current:**
- Increase RBIAS (e.g., 200kΩ → 17µA)

---

## Common Issues and Troubleshooting

### Issue 1: Transistors not in saturation
**Symptom:** Low gain, distorted output
**Check:** Operating point, verify VDS > VGS - VT for all transistors
**Fix:** Adjust RBIAS or transistor sizes

### Issue 2: Oscillation/Instability
**Symptom:** Ringing in transient, negative phase margin
**Check:** Phase margin in AC analysis
**Fix:** Increase CC (compensation capacitor)

### Issue 3: Very low gain
**Symptom:** Gain < 40 dB
**Check:** Transistor ro values, ensure saturation
**Fix:** Increase transistor length L, check bias current

### Issue 4: Low bandwidth
**Symptom:** GBW < 10 MHz
**Check:** CC value, gm values
**Fix:** Decrease CC or increase bias current

### Issue 5: Circuit won't converge
**Symptom:** Simulation fails to find operating point
**Fix:**
- Add `.options gmin=1e-12`
- Add initial conditions `.ic V(node)=voltage`
- Check for floating nodes

---

## Advanced Analysis

### 1. **Input/Output Impedance**
Add `.ac` analysis with current probe at input/output:
- Zin = V(input) / I(input)
- Zout = V(output) / I(output)

### 2. **Common-Mode Rejection Ratio (CMRR)**
Modify input sources to common-mode:
- Set both VIN_P and VIN_N to same AC magnitude
- Measure output
- CMRR = Differential gain / Common-mode gain

### 3. **Power Supply Rejection Ratio (PSRR)**
- Add AC source in series with VDD
- Measure output
- PSRR = Gain from VDD to output

### 4. **Noise Analysis**
Add `.noise V(VOUT) VIN_P dec 100 1 100Meg`
- Shows input-referred noise spectral density
- Integrated noise

### 5. **Parameter Sweep**
Study effect of component variations:
```
.step param Ccomp list 3p 5p 10p 15p
```
Then change CC value to `{Ccomp}`

---

## Expected Performance Summary

| Parameter | Typical Value | Formula/Note |
|-----------|---------------|--------------|
| DC Gain | 60-80 dB | Av = gm1(ro2||ro6) × gm7×ro7 |
| GBW | 10-100 MHz | gm1 / (2π×CC) |
| Phase Margin | 45-65° | At unity-gain frequency |
| Slew Rate | 5-20 V/µs | Itail / CC |
| Power | 0.2-1 mW | VDD × (Itail + Ibias) |
| Input CM Range | 0.7-3.5V | Limited by M1/M2 saturation |
| Output Swing | 0.5-4.5V | Limited by M7 saturation |

---

## Learning Objectives

By simulating this circuit, you should understand:

1. **DC Operating Point:** How bias resistor sets current, transistor sizing affects bias
2. **Small-Signal Gain:** Relationship between gm, ro, and voltage gain
3. **Frequency Response:** Dominant pole compensation, GBW product
4. **Stability:** Phase margin, compensation capacitor effects
5. **Trade-offs:** Gain vs. bandwidth, power vs. performance
6. **Transistor Sizing:** Effects of W/L ratio on circuit performance

---

## Next Steps

1. **Run all three analyses** and verify circuit operates correctly
2. **Measure key parameters:** Gain, GBW, phase margin
3. **Compare to hand calculations** from your coursework
4. **Experiment with modifications:**
   - Change CC: observe effect on stability and bandwidth
   - Change RBIAS: observe effect on gain and GBW
   - Change transistor L: observe effect on gain and bandwidth
5. **Generate plots for report:**
   - Frequency response (magnitude and phase)
   - Transient response
   - Export via: File → Export → Save as PNG/PDF

---

## Tips for LTspice

- **Zoom:** Mouse wheel
- **Pan:** Right-click and drag
- **Cursor:** Click plot, use cursor to measure
- **Add trace:** Right-click plot area
- **Delete trace:** Click trace label, press Delete
- **Change colors:** Tools → Control Panel → Waveforms
- **Grid:** Tools → Control Panel → Waveforms → Grid

---

## Reference

For more on two-stage op-amp design, see:
- Razavi, "Design of Analog CMOS Integrated Circuits," Chapter 9
- Gray & Meyer, "Analysis and Design of Analog Integrated Circuits," Chapter 6
- Your course lecture notes on op-amp design

---

**Good luck with your simulation and analysis!**
