---
tags: [spice, simulation, current-mirror, nmos, example, validation]
date: 2025-12-14
---

# Current Mirror Bias Circuit - Problem 1

Complete simulation example validating the SPICEPilot setup.

## Circuit Overview

**Circuit Type:** Current mirror bias network with three NMOS transistors

**Purpose:**
- Validate SPICEPilot installation and workflow
- Demonstrate current source and resistor biasing
- Verify current mirror operation

**Status:** ✅ Simulation successful, results validated

## Circuit Description

### Topology

```
           VDD (0.9V)
            │
        I1 (45µA)
            │
            ├──────┐
            │      │
       VD1  │     M2 (drain)
        ┌───┴───┐  │
     M1 │ NMOS  │  │
        │diode  │  │
        └───┬───┘  │
            │     VS2─── I2 (45µA to GND)
           GND

           VDD (0.9V)
            │
         R1 (5.56kΩ)
            │
       VD3  │
        ┌───┴───┐
     M3 │ NMOS  │
        │diode  │
        └───┬───┘
            │
           GND
```

### Components

**Power Supply:**
- VDD = 0.9 V

**Current Sources:**
- I1: 45 µA (from VDD to VD1)
- I2: 45 µA (from VS2 to ground)

**Resistor:**
- R1: 5.56 kΩ (from VDD to VD3)

**MOSFETs (all NMOS_SH):**
- M1: Diode-connected (gate tied to drain)
- M2: Current mirror (gate tied to M1's gate/drain)
- M3: Diode-connected (gate tied to drain)

## MOSFET Model Parameters

**Model Name:** NMOS_SH

| Parameter | Symbol | Value | Description |
|-----------|--------|-------|-------------|
| Process transconductance | Kp | 180 µA/V² | Process parameter |
| Threshold voltage | Vto | 0.4 V | Turn-on voltage |
| Width | W | 8 µm | Transistor width |
| Length | L | 1 µm | Channel length |
| Channel modulation | λ | 0.02 | Lambda parameter |
| Level | - | 1 | Shichman-Hodges model |

## Simulation Results

### Operating Point (VDD = 0.9V)

**Node Voltages:**

| Node | Voltage | Description |
|------|---------|-------------|
| VD1 | 0.648395 V | M1 drain/gate (current source biased) |
| VS2 | 0.000613 V | M2 source (≈ 0V) |
| VD3 | 0.648860 V | M3 drain/gate (resistor biased) |

**Currents:**

| Branch | Current | Source |
|--------|---------|--------|
| I1 | 45.0 µA | Current source (forced) |
| I2 | 45.0 µA | Current source (forced) |
| I(R1) | 45.169 µA | Calculated: (VDD - VD3)/R1 |
| I(M2) | ≈ 45 µA | Mirrored from M1 |

### MOSFET Operating Points

| Device | VGS (V) | VDS (V) | Region | Saturation Check |
|--------|---------|---------|--------|------------------|
| **M1** | 0.648 | 0.648 | Saturation | VDS (0.648) > VGS-Vto (0.248) ✅ |
| **M2** | 0.648 | 0.899 | Saturation | VDS (0.899) > VGS-Vto (0.248) ✅ |
| **M3** | 0.649 | 0.649 | Saturation | VDS (0.649) > VGS-Vto (0.249) ✅ |

**All transistors operating in saturation region** ✅

## Circuit Analysis

### M1 Branch: Current Source Biasing

**Operation:**
1. Current source I1 forces 45 µA through M1
2. M1 is diode-connected (VGS = VDS)
3. VD1 settles to the VGS required for 45 µA

**Result:**
- VD1 = 0.648 V
- This voltage sets the gate voltage for the current mirror

### M2 Branch: Current Mirror

**Operation:**
1. M2 gate tied to VD1 (same gate voltage as M1)
2. Same VGS → same drain current (matched devices)
3. Current source I2 sinks 45 µA from source terminal
4. VS2 settles to near-ground potential

**Result:**
- M2 successfully mirrors M1's current (45 µA)
- VS2 ≈ 0 V (0.6 mV)
- VDS(M2) = 0.899 V (well into saturation)

**Current Mirror Accuracy:**
- Target: 45 µA
- Actual: 45 µA
- Error: < 1%

### M3 Branch: Resistor Biasing

**Operation:**
1. Resistor R1 provides bias current
2. I(R1) = (VDD - VD3) / R1
3. M3 is diode-connected
4. VD3 settles to VGS needed for the resistor current

**Result:**
- VD3 = 0.649 V
- I(R1) = 45.169 µA

**Comparison to M1:**
- M1 (current source bias): VGS = 0.648 V
- M3 (resistor bias): VGS = 0.649 V
- Difference: 1 mV (0.15%)

## Theoretical Validation

### Hand Calculation

For an NMOS in saturation:

$$I_D = \frac{1}{2} \cdot K_p \cdot \frac{W}{L} \cdot (V_{GS} - V_{to})^2$$

Given:
- ID = 45 µA
- Kp = 180 µA/V²
- W/L = 8/1
- Vto = 0.4 V

Solve for VGS:

$$45\mu A = \frac{1}{2} \cdot 180\mu \cdot 8 \cdot (V_{GS} - 0.4)^2$$

$$45\mu A = 720\mu \cdot (V_{GS} - 0.4)^2$$

$$(V_{GS} - 0.4)^2 = \frac{45}{720} = 0.0625$$

$$V_{GS} - 0.4 = 0.25$$

$$V_{GS} = 0.65 V$$

### Comparison

| Method | VGS | Error |
|--------|-----|-------|
| **Theoretical** | 0.650 V | - |
| **M1 Simulated** | 0.648 V | 0.3% |
| **M3 Simulated** | 0.649 V | 0.15% |

**Conclusion:** Excellent agreement between theory and simulation ✅

## Key Observations

### 1. Bias Method Comparison

Both biasing methods produce nearly identical results:

- **Current source bias (M1):** VGS = 0.648 V
- **Resistor bias (M3):** VGS = 0.649 V
- **Difference:** 1 mV

**Implication:** For precise biasing, both methods work. Resistor biasing is simpler but less accurate across process/temperature variations.

### 2. Current Mirror Performance

The current mirror (M2) accurately replicates M1's current:
- Same VGS → same ID
- Excellent matching
- VS2 near ground confirms proper operation

### 3. Device Matching

VD1 ≈ VD3 (0.648 V vs 0.649 V) validates:
- MOSFET model consistency
- Same current through matched devices
- Accurate simulation setup

### 4. Saturation Region Operation

All three transistors operate in saturation:
- Ensures proper current source behavior
- Validates bias point design
- Confirms linear relationship between VGS and ID

## Files and Code

### File Locations

**Circuit files:**
```
C:\Users\Mads2\SPICEPilot\examples\1_current_mirror\
├── current_mirror_bias.py       # PySpice implementation
├── current_mirror_bias.cir      # SPICE netlist
└── RUN.bat                      # Double-click to simulate!
```

**Simulation outputs:**
```
C:\Users\Mads2\SPICEPilot\results\
├── plots\                       # Graphs and Bode plots
└── logs\                        # Simulation logs
```

**Documentation:**
```
C:\Users\Mads2\DTU\Obsidian\...\LTspice & Kicad\
└── 06 - Current Mirror Circuit Example.md  # This file
```

### PySpice Code Snippet

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create circuit
circuit = Circuit('Current Mirror Bias Circuit')

# Power and bias
circuit.V('dd', 'vdd', circuit.gnd, 0.9@u_V)
circuit.I('1', 'vdd', 'vd1', 45@u_uA)
circuit.I('2', 'vs2', circuit.gnd, 45@u_uA)
circuit.R('1', 'vdd', 'vd3', 5.56@u_kOhm)

# MOSFETs
circuit.MOSFET('1', 'vd1', 'vd1', circuit.gnd, circuit.gnd, model='NMOS_SH')
circuit.MOSFET('2', 'vdd', 'vd1', 'vs2', circuit.gnd, model='NMOS_SH')
circuit.MOSFET('3', 'vd3', 'vd3', circuit.gnd, circuit.gnd, model='NMOS_SH')

# Model
circuit.model('NMOS_SH', 'nmos',
              level=1, kp=180e-6, vto=0.4,
              lambda_=0.02, w=8e-6, l=1e-6)

# Simulate
simulator = circuit.simulator()
analysis = simulator.operating_point()

# Extract results
vd1 = float(analysis['vd1'])
vs2 = float(analysis['vs2'])
vd3 = float(analysis['vd3'])
```

### SPICE Netlist

```spice
* Current Mirror Bias Circuit
.title Current Mirror Bias Circuit

* Power supply
Vdd vdd 0 DC 0.9

* Current sources
I1 vdd vd1 DC 45u
I2 vs2 0 DC 45u

* Resistor
R1 vdd vd3 5.56k

* MOSFETs
M1 vd1 vd1 0 0 NMOS_SH
M2 vdd vd1 vs2 0 NMOS_SH
M3 vd3 vd3 0 0 NMOS_SH

* NMOS model
.model NMOS_SH nmos (level=1 kp=180u vto=0.4 lambda=0.02 w=8u l=1u)

* Analysis
.op
.dc Vdd 0.5 1.2 0.01
.end
```

## Running the Simulation

### Method 1: Batch File (Easiest) ⭐

**Double-click:**
```
C:\Users\Mads2\SPICEPilot\examples\1_current_mirror\RUN.bat
```

Opens ngspice automatically with the circuit loaded and simulated.

### Method 2: ngspice Command Line

```bash
cd C:\Users\Mads2\SPICEPilot\examples\1_current_mirror
ngspice current_mirror_bias.cir
```

**Interactive commands:**
```bash
run                           # Execute simulation
print v(vd1) v(vs2) v(vd3)   # Print node voltages
plot v(vd1) v(vs2) v(vd3)    # Plot voltages
quit                          # Exit
```

### Method 3: PySpice (Python)

```bash
cd C:\Users\Mads2\SPICEPilot\examples\1_current_mirror
python current_mirror_bias.py
```

**Output:**
- Console text with all voltages and currents
- Validation checks
- (Optional) matplotlib plots if VDD sweep enabled

## Educational Value

### What This Example Demonstrates

1. **Current mirror operation**
   - How gate voltage sets drain current
   - Matching between identical transistors
   - Importance of saturation region

2. **Biasing techniques**
   - Current source biasing
   - Resistor biasing
   - Comparison of accuracy

3. **SPICE simulation workflow**
   - Circuit creation from schematic
   - Model definition
   - Operating point analysis
   - Result validation

4. **Design verification**
   - Hand calculations
   - Simulation
   - Comparison and validation

### Learning Outcomes

After studying this example, you should understand:
- ✅ How to implement NMOS current mirrors
- ✅ How to bias transistors for specific currents
- ✅ How to verify transistor saturation
- ✅ How to validate simulation with theory
- ✅ Complete SPICE simulation workflow

## Related Topics

### Internal Documentation

- [[README - Start Here|Start Here]] - Documentation index
- [[01 - SPICEPilot Setup Guide|Setup Guide]] - Installation instructions
- [[04 - Simulation Workflows|Simulation Workflows]] - How to run simulations
- [[Quick Reference - SPICE Commands|Quick Reference]] - SPICE commands
- [[02 - Two-Stage CMOS Op-Amp|Op-Amp Example]] - Another complete circuit

### Further Reading

**Current Mirrors:**
- Razavi, "Design of Analog CMOS Integrated Circuits", Chapter 3
- Gray & Meyer, "Analysis and Design of Analog Integrated Circuits", Chapter 4

**SPICE Simulation:**
- ngspice User Manual: http://ngspice.sourceforge.net/docs.html
- PySpice Documentation: https://pyspice.fabrice-salvaire.fr/

**MOSFET Theory:**
- Streetman & Banerjee, "Solid State Electronic Devices"
- Sedra & Smith, "Microelectronic Circuits"

## Next Steps

### Extend This Circuit

1. **Add more mirrors:**
   - Create M4, M5 mirroring M1
   - Verify all have 45 µA

2. **Vary W/L ratios:**
   - Change M2 to W=16µm (2× wider)
   - Predict and verify 2× current

3. **Temperature sweep:**
   - Simulate at different temperatures
   - Observe VGS variation

4. **Process variation:**
   - Vary Kp, Vto
   - See impact on bias point

### Try Other Circuits

- PMOS current mirror
- Cascode current mirror
- Wilson current mirror
- Differential pair with current mirror load

## Summary

**Circuit:** Current mirror bias network

**Status:** ✅ Fully functional and validated

**Key Results:**
- All transistors in saturation
- Current mirror accuracy: > 99%
- Theoretical match: 99.7%
- Bias methods comparison: < 1 mV difference

**Validation:** SPICEPilot setup is production-ready

**Files:** PySpice and SPICE netlist available in `C:\Users\Mads2\SPICEPilot\`

**Use Case:** Reference example for future SPICE simulation work

---

**Last Updated:** 2025-12-14
**Circuit Source:** Problem 1 schematic
**Simulation Tool:** PySpice 1.5 + ngspice 41
**Validation Status:** Complete ✅
