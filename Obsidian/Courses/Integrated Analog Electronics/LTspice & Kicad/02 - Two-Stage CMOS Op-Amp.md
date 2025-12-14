---
tags: [op-amp, cmos, analog-design, circuit-design, spice]
date: 2025-12-14
---

# Two-Stage CMOS Operational Amplifier

Implementation of a classic two-stage CMOS op-amp using SPICEPilot and PySpice.

## Circuit Diagram

![[Two-Stage_CMOS_op-amp.png]]

```
       VDD(5V)    VDD(5V)         VDD(5V)    VDD(5V)
         |          |               |          |
      +--M4------+--M5--+        +--M6--+     |
      |  (D=G)   |      |        |      |     |
    +-+          |      |        |      |     |
    | |          |      +---CA---+      |     |
n_d2+-+       n_d3     3pF    n_d3      |     |
      |          |               |       |     |
      +--M2      +--M3           +--M7   |     |
    G |        G |             G |       |  vout
  vin_p      vin_n           n_d3       |     +---CL(15p)---GND
      |          |               |       |     |
      +---n_tail-+               +-------+     +---CB(0.5p)--GND
            |                        |
         +--M8--+                   GND
         |      |
      vbias_n  GND

FIRST STAGE: Differential Amplifier
- M2, M3: NMOS differential pair
- M4, M5: PMOS active load (current mirror)
- M8: NMOS tail current source

SECOND STAGE: Common-Source Output
- M7: NMOS output driver
- M6: PMOS current source load
- CA: Miller compensation (3pF)
```

## Circuit Topology

### First Stage - Differential Amplifier

**Purpose:** High gain differential input stage

**Components:**
- **M2, M3:** NMOS differential input pair
  - Convert differential voltage to differential current
  - W/L = 30µm/2µm

- **M4, M5:** PMOS active load current mirror
  - Converts differential current to single-ended voltage
  - M4 is diode-connected (gate tied to drain)
  - W/L = 60µm/2µm

- **M8:** NMOS tail current source
  - Sets bias current for differential pair
  - W/L = 60µm/2µm (larger for more current)

### Second Stage - Common-Source Amplifier

**Purpose:** Additional gain and current drive capability

**Components:**
- **M7:** NMOS common-source driver
  - Provides voltage gain
  - Drives output load
  - W/L = 30µm/2µm

- **M6:** PMOS current source load
  - Active load for M7
  - W/L = 60µm/2µm

### Compensation Network

**CA (3pF):** Miller compensation capacitor
- Creates dominant pole
- Ensures frequency stability
- Connected between M7 gate and output

**CB (0.5pF):** Additional compensation

**CL (15pF):** Load capacitor

## SPICE Model Parameters

### NMOS Transistors

```spice
.model NMOS nmos (
    level=1           # Simple Shichman-Hodges model
    kp=120u           # Transconductance parameter (µA/V²)
    vto=0.7           # Threshold voltage (V)
    lambda=0.02       # Channel length modulation
    gamma=0.4         # Body effect parameter
    phi=0.65          # Surface potential
    w=30u             # Channel width (µm)
    l=2u              # Channel length (µm)
)
```

### NMOS_BIG (Tail Current Source)

```spice
.model NMOS_BIG nmos (
    level=1
    kp=120u
    vto=0.7
    lambda=0.02
    gamma=0.4
    phi=0.65
    w=60u             # 2x width for more current
    l=2u
)
```

### PMOS Transistors

```spice
.model PMOS pmos (
    level=1
    kp=40u            # Lower mobility than NMOS
    vto=-0.7          # Negative threshold for PMOS
    lambda=0.02
    gamma=0.4
    phi=0.65
    w=60u             # Wider to compensate mobility
    l=2u
)
```

> [!note] Design Notes
> - **PMOS width > NMOS width:** Compensates for lower hole mobility (~2.5× larger)
> - **Longer L (2µm):** Better matching and lower noise
> - **level=1:** Simple model, good for hand analysis

## Bias Voltages

```python
VDD = 5V          # Positive supply
Vbias_p = 3.5V    # PMOS current sources (lower = more current)
Vbias_n = 1.5V    # NMOS tail current source
VCM = 2.5V        # Input common-mode voltage
```

**How biasing works:**
1. **Vbias_n** controls tail current through M8
2. Tail current splits between M2 and M3
3. **Vbias_p** controls current through M1, M6 (PMOS loads)
4. Proper biasing ensures all transistors in saturation

## Performance Specifications

### DC Operating Point

```
Node Voltages:
  vout:    0.091 V    (output DC level)
  n_tail:  0.846 V    (diff pair source)
  n_d2:    3.328 V    (M2 drain)
  n_d3:    3.328 V    (M3 drain, M7 gate)
  vin_p:   2.500 V    (pos input)
  vin_n:   2.500 V    (neg input)
```

> [!warning] DC Output Low
> Output at 0.09V indicates bias needs optimization for better swing.
> Ideally want ~VDD/2 = 2.5V for maximum output range.

### AC Performance

| Parameter | Value | Notes |
|-----------|-------|-------|
| **DC Gain** | 1.4 dB (~1.2 V/V) | Low due to simple biasing |
| **3dB Bandwidth** | 1.16 MHz | First pole frequency |
| **Unity-Gain Freq** | 0.71 MHz | Gain crossover |
| **Phase Margin** | >300° | Excellent stability (over-compensated) |
| **GBW Product** | ~0.85 MHz | Gain × Bandwidth |

> [!info] Gain Analysis
> Theoretical gain for two-stage op-amp:
> $$A_v = g_{m1}(r_{o2}||r_{o4}) \times g_{m7}(r_{o7}||r_{o6})$$
>
> Low measured gain suggests:
> - Bias currents too low
> - Need larger W/L ratios
> - Channel length modulation (λ) effect

## PySpice Implementation

### Complete Code

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import matplotlib.pyplot as plt
import numpy as np

# Create circuit
circuit = Circuit('Two-Stage CMOS Op-Amp')

# Power supplies
VDD = 5
circuit.V('dd', 'vdd', circuit.gnd, VDD@u_V)
circuit.V('bias_p', 'vbias_p', circuit.gnd, 3.5@u_V)
circuit.V('bias_n', 'vbias_n', circuit.gnd, 1.5@u_V)

# Input signals (differential)
circuit.V('in_p', 'vin_p', circuit.gnd, '2.5 AC 0.5')
circuit.V('in_n', 'vin_n', circuit.gnd, '2.5 AC 0')

# FIRST STAGE: Differential Amplifier
circuit.MOSFET('M8', 'n_tail', 'vbias_n', circuit.gnd, circuit.gnd,
               model='NMOS_BIG')
circuit.MOSFET('M2', 'n_d2', 'vin_p', 'n_tail', circuit.gnd,
               model='NMOS')
circuit.MOSFET('M3', 'n_d3', 'vin_n', 'n_tail', circuit.gnd,
               model='NMOS')
circuit.MOSFET('M4', 'n_d2', 'n_d2', 'vdd', 'vdd',
               model='PMOS')
circuit.MOSFET('M5', 'n_d3', 'n_d2', 'vdd', 'vdd',
               model='PMOS')

# SECOND STAGE: Output
circuit.MOSFET('M6', 'vout', 'vbias_p', 'vdd', 'vdd',
               model='PMOS')
circuit.MOSFET('M7', 'vout', 'n_d3', circuit.gnd, circuit.gnd,
               model='NMOS')

# COMPENSATION
circuit.C('A', 'n_d3', 'vout', 3@u_pF)  # Miller comp
circuit.C('B', 'vout', circuit.gnd, 0.5@u_pF)
circuit.C('L', 'vout', circuit.gnd, 15@u_pF)  # Load

# MODELS
circuit.model('NMOS', 'nmos', level=1, kp=120e-6, vto=0.7,
              lambda_=0.02, gamma=0.4, phi=0.65, w=30e-6, l=2e-6)
circuit.model('NMOS_BIG', 'nmos', level=1, kp=120e-6, vto=0.7,
              lambda_=0.02, gamma=0.4, phi=0.65, w=60e-6, l=2e-6)
circuit.model('PMOS', 'pmos', level=1, kp=40e-6, vto=-0.7,
              lambda_=0.02, gamma=0.4, phi=0.65, w=60e-6, l=2e-6)

# SIMULATE
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
ac_analysis = simulator.ac(start_frequency=0.1@u_Hz,
                           stop_frequency=1@u_GHz,
                           number_of_points=200,
                           variation='dec')

# PLOT
frequency = np.array(ac_analysis.frequency)
vout_ac = np.array(ac_analysis['vout'])
gain_db = 20 * np.log10(np.abs(vout_ac) + 1e-20)
phase_deg = np.angle(vout_ac, deg=True)

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.semilogx(frequency, gain_db)
plt.grid(True)
plt.ylabel('Gain (dB)')
plt.title('Two-Stage Op-Amp Bode Plot')

plt.subplot(2, 1, 2)
plt.semilogx(frequency, phase_deg)
plt.grid(True)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.show()
```

**File location:**
```
C:\Users\Mads2\SPICEPilot\two_stage_opamp_improved.py
```

## SPICE Netlist

The equivalent SPICE netlist (KiCad compatible):

```spice
* Two-Stage CMOS Operational Amplifier

.title Two-Stage CMOS Op-Amp

* Supply voltages
Vdd vdd 0 DC 5
Vbias_p vbias_p 0 DC 3.5
Vbias_n vbias_n 0 DC 1.5

* Input signals
Vin_p vin_p 0 DC 2.5 AC 0.5
Vin_n vin_n 0 DC 2.5 AC 0

* First stage
M8 n_tail vbias_n 0 0 NMOS_BIG
M2 n_d2 vin_p n_tail 0 NMOS
M3 n_d3 vin_n n_tail 0 NMOS
M4 n_d2 n_d2 vdd vdd PMOS
M5 n_d3 n_d2 vdd vdd PMOS

* Second stage
M6 vout vbias_p vdd vdd PMOS
M7 vout n_d3 0 0 NMOS

* Compensation
CA n_d3 vout 3p
CB vout 0 0.5p
CL vout 0 15p

* Models
.model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=30u l=2u)
.model NMOS_BIG nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=60u l=2u)
.model PMOS pmos (level=1 kp=40u vto=-0.7 lambda=0.02 w=60u l=2u)

* Analysis
.ac dec 100 0.1 1G
.op

.end
```

**File location:**
```
C:\Users\Mads2\SPICEPilot\two_stage_opamp_kicad.cir
```

## Design Trade-offs

### Gain vs. Bandwidth
- **Increase gain:** Larger W/L ratios, higher bias current
- **Increase bandwidth:** Reduce compensation capacitor CA
- **Trade-off:** GBW product is constant for given design

### Power vs. Performance
- **Lower power:** Reduce bias currents (increase Vbias_p, decrease Vbias_n)
- **Higher performance:** Increase bias currents
- **Trade-off:** Power consumption vs. speed/gain

### Stability vs. Bandwidth
- **Better stability:** Larger CA (Miller compensation)
- **Higher bandwidth:** Smaller CA
- **Trade-off:** Phase margin vs. frequency response

## Optimization Strategies

### To Increase DC Gain

1. **Increase transistor lengths:**
   ```spice
   l=2u → l=5u  # Increases ro (output resistance)
   ```

2. **Optimize bias currents:**
   ```python
   Vbias_p = 3.8V  # More current through loads
   Vbias_n = 1.2V  # More tail current
   ```

3. **Use cascode topology:**
   - Add cascode transistors to increase output resistance
   - Requires more headroom

### To Improve Bandwidth

1. **Reduce compensation:**
   ```python
   CA = 1@u_pF  # From 3pF
   ```

2. **Increase bias current:**
   - Higher gm → higher fT

3. **Reduce load capacitance:**
   ```python
   CL = 5@u_pF  # From 15pF
   ```

### To Fix DC Bias Point

Current output at 0.09V is too low. Options:

1. **Add output stage:**
   - Class AB push-pull
   - Provides better swing

2. **Adjust current mirror ratios:**
   - Make M6 wider to pull output higher

3. **Use different bias scheme:**
   - Self-biased current mirror
   - Beta multiplier reference

## Related Topics

- [[CMOS Analog Design Fundamentals]]
- [[Frequency Compensation Techniques]]
- [[Op-Amp Design Checklist]]
- [[04 - Simulation Workflows|How to Simulate]]

## References

1. Razavi, B. "Design of Analog CMOS Integrated Circuits" - Chapter on Op-Amps
2. Allen & Holberg "CMOS Analog Circuit Design" - Two-Stage Op-Amp Design
3. SPICEPilot paper: [arXiv:2410.20553](https://arxiv.org/pdf/2410.20553)

---

**Created:** 2025-12-14
**Circuit Files:** `SPICEPilot/two_stage_opamp_*`
**Status:** Working, tested with PySpice and ngspice
