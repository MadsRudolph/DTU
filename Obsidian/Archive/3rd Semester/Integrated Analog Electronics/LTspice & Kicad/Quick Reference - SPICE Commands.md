---
tags: [reference, cheatsheet, spice, commands, quick-ref]
date: 2025-12-14
---

# Quick Reference - SPICE Commands

Essential commands and syntax for SPICE simulation.

## ngspice Interactive Commands

| Command | Description | Example |
|---------|-------------|---------|
| `run` | Execute simulation | `run` |
| `plot` | Plot signal | `plot v(vout)` |
| `vdb()` | Voltage in dB | `plot vdb(vout)` |
| `vp()` | Phase in degrees | `plot vp(vout)` |
| `print` | Print value | `print v(vout)` |
| `print all` | All node voltages | `print all` |
| `display` | List available signals | `display` |
| `alter` | Change parameter | `alter R1 = 2k` |
| `write` | Save data | `write output.raw` |
| `quit` | Exit ngspice | `quit` |
| `help` | Help system | `help ac` |

## SPICE Netlist Syntax

### Components

```spice
* Resistor: R<name> <node+> <node-> <value>
R1 in out 1k
R2 out 0 10k

* Capacitor: C<name> <node+> <node-> <value> [IC=<initial>]
C1 in out 10u
C2 out 0 1n IC=2.5

* Inductor: L<name> <node+> <node-> <value> [IC=<initial>]
L1 in out 1m IC=0.1

* Voltage Source: V<name> <node+> <node-> [DC <value>] [AC <value>]
V1 vdd 0 DC 5
Vin in 0 DC 2.5 AC 1

* Current Source: I<name> <node+> <node-> <value>
I1 vdd out 100u

* MOSFET: M<name> <drain> <gate> <source> <bulk> <model> [params]
M1 out in vdd vdd PMOS w=20u l=2u
M2 out in 0 0 NMOS w=10u l=2u
```

### Models

```spice
.model <name> <type> (<param1>=<val1> <param2>=<val2> ...)

* NMOS example
.model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=30u l=2u)

* PMOS example
.model PMOS pmos (level=1 kp=40u vto=-0.7 lambda=0.02 w=60u l=2u)
```

### Analysis Commands

```spice
* Operating point
.op

* AC analysis: .ac <sweep_type> <points> <start> <stop>
.ac dec 100 1 1G          # Decade sweep, 100 pts/decade
.ac lin 1000 1k 10k       # Linear sweep, 1000 points
.ac oct 10 1 1Meg         # Octave sweep, 10 pts/octave

* Transient: .tran <step> <stop> [<start>] [<max_step>]
.tran 1n 10u              # 1ns step, stop at 10us
.tran 1n 10u 0 100p       # Start at 0, max step 100ps

* DC sweep: .dc <source> <start> <stop> <step>
.dc Vin 0 5 0.01          # Sweep Vin from 0 to 5V
.dc Vgs 0 5 0.1 Vds 0 5 1 # Nested sweep
```

### Control Statements

```spice
* Include external file
.include "filename.cir"

* Set options
.options reltol=1e-3 abstol=1e-12

* Save specific nodes (optional)
.save v(out) v(in) i(V1)

* Temperature
.temp 27

* Parameters
.param vdd=5 rbias=10k

* Control block (for scripting)
.control
run
plot v(out)
quit
.endc

* End of netlist
.end
```

## PySpice Syntax

### Circuit Creation

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('Circuit Name')
```

### Components

```python
# Resistor
circuit.R('R1', 'node1', 'node2', 1@u_kOhm)

# Capacitor
circuit.C('C1', 'node1', 'node2', 10@u_uF)
circuit.C('C2', 'n1', 'n2', 1@u_pF, ic=2.5@u_V)  # Initial condition

# Inductor
circuit.L('L1', 'node1', 'node2', 1@u_mH)

# Voltage source
circuit.V('dd', 'vdd', circuit.gnd, 5@u_V)
circuit.V('in', 'vin', circuit.gnd, '2.5 AC 1')  # DC + AC

# Current source
circuit.I('bias', 'node', circuit.gnd, 100@u_uA)

# MOSFET
circuit.MOSFET('M1', 'drain', 'gate', 'source', 'bulk', model='NMOS')

# Model definition
circuit.model('NMOS', 'nmos', level=1, kp=120e-6, vto=0.7,
              lambda_=0.02, w=30e-6, l=2e-6)
```

### Simulation

```python
# Create simulator
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Operating point
analysis = simulator.operating_point()
vout = float(analysis['vout'])

# AC analysis
analysis = simulator.ac(
    start_frequency=1@u_Hz,
    stop_frequency=1@u_GHz,
    number_of_points=100,
    variation='dec'  # or 'lin' or 'oct'
)

# Transient analysis
analysis = simulator.transient(
    step_time=1@u_ns,
    end_time=10@u_us
)

# DC sweep
analysis = simulator.dc(Vin=slice(0, 5, 0.01))
```

### Data Access

```python
# Get node voltage
voltage = analysis['node_name']

# For operating point
v = float(analysis['vout'])

# For AC (returns complex array)
import numpy as np
vout = np.array(analysis['vout'])
magnitude = np.abs(vout)
phase = np.angle(vout, deg=True)
gain_db = 20*np.log10(magnitude)

# For transient (returns real array)
time = np.array(analysis.time)
vout = np.array(analysis['vout'])
```

## Common Units

### PySpice Units (use @ operator)

| Quantity | Unit Suffix | Example |
|----------|-------------|---------|
| Voltage | `@u_V`, `@u_mV` | `5@u_V` |
| Current | `@u_A`, `@u_mA`, `@u_uA` | `100@u_uA` |
| Resistance | `@u_Ohm`, `@u_kOhm`, `@u_MOhm` | `1@u_kOhm` |
| Capacitance | `@u_F`, `@u_uF`, `@u_nF`, `@u_pF` | `10@u_pF` |
| Inductance | `@u_H`, `@u_mH`, `@u_uH` | `1@u_mH` |
| Frequency | `@u_Hz`, `@u_kHz`, `@u_MHz`, `@u_GHz` | `1@u_MHz` |
| Time | `@u_s`, `@u_ms`, `@u_us`, `@u_ns`, `@u_ps` | `1@u_ns` |

### SPICE Netlist Units (suffix notation)

| Suffix | Multiplier | Example | Value |
|--------|-----------|---------|-------|
| T | 10¹² | 1T | 1e12 |
| G | 10⁹ | 1G | 1e9 |
| Meg | 10⁶ | 1Meg | 1e6 |
| k | 10³ | 1k | 1e3 |
| m | 10⁻³ | 1m | 1e-3 |
| u | 10⁻⁶ | 1u | 1e-6 |
| n | 10⁻⁹ | 1n | 1e-9 |
| p | 10⁻¹² | 1p | 1e-12 |
| f | 10⁻¹⁵ | 1f | 1e-15 |

> [!warning] Case Sensitive
> - `M` or `Meg` = 10⁶ (mega)
> - `m` = 10⁻³ (milli)
> - Use `Meg` not `M` to avoid confusion with milli

## Measurement Commands (ngspice)

```bash
# Measure at specific point
meas ac gain_at_1k find vdb(vout) at=1k

# Measure when condition met
meas ac ugf when vdb(vout)=0

# Find maximum
meas tran vout_max max v(vout)

# Find derivative (slew rate)
meas tran slew_rate deriv v(vout) at=5u
```

## Plotting Commands

### ngspice Plotting

```bash
# Single signal
plot v(vout)

# Multiple signals
plot v(vout) v(vin) v(n_d2)

# Magnitude in dB
plot vdb(vout)

# Phase
plot vp(vout)

# Current
plot i(V1)           # Current through voltage source V1

# Derivatives
plot deriv(v(vout))  # dV/dt
```

### Python/Matplotlib Plotting

```python
import matplotlib.pyplot as plt
import numpy as np

# After simulation
freq = np.array(analysis.frequency)
vout = np.array(analysis['vout'])
gain_db = 20*np.log10(np.abs(vout))

# Bode plot
plt.figure(figsize=(10, 6))
plt.semilogx(freq, gain_db)
plt.grid(True)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('Bode Plot')
plt.show()
```

## Common Patterns

### AC Analysis with Bode Plot

```python
# Circuit with AC source
circuit.V('in', 'vin', circuit.gnd, '2.5 AC 1')

# Simulate
simulator = circuit.simulator()
ac = simulator.ac(start_frequency=1@u_Hz,
                  stop_frequency=1@u_GHz,
                  number_of_points=100,
                  variation='dec')

# Extract data
freq = np.array(ac.frequency)
vout = np.array(ac['vout'])
gain_db = 20*np.log10(np.abs(vout))
phase = np.angle(vout, deg=True)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.semilogx(freq, gain_db)
ax2.semilogx(freq, phase)
plt.show()
```

### Parameter Sweep

```python
results = []
for r_value in range(1000, 10000, 1000):
    circuit.R('load', 'out', circuit.gnd, r_value@u_Ohm)
    simulator = circuit.simulator()
    analysis = simulator.operating_point()
    results.append(float(analysis['out']))
```

### Saving Results

```python
# To CSV
import pandas as pd
df = pd.DataFrame({
    'frequency': freq,
    'gain_db': gain_db,
    'phase': phase
})
df.to_csv('results.csv', index=False)

# To numpy
np.savez('results.npz', freq=freq, gain=gain_db, phase=phase)

# Load later
data = np.load('results.npz')
freq = data['freq']
```

## File Locations Reference

```
C:\Users\Mads2\DTU\SPICEPilot\
├── two_stage_opamp.py                    # PySpice script
├── two_stage_opamp_improved.py           # Optimized version
├── two_stage_opamp_kicad.cir            # SPICE netlist
├── two_stage_opamp.kicad_pro            # KiCad project
├── two_stage_opamp.kicad_sch            # KiCad schematic
├── Pilot_prompt.md                       # SPICEPilot guide
├── run_with_plots.bat                    # Batch script
└── guides/                               # Documentation
```

## Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| "cannot load library ngspice.dll" | Copy DLL to PySpice folder |
| No signals in KiCad | Use ngspice directly |
| Convergence failed | Add `.options reltol=1e-3` |
| "unknown control" | Add `.` before command |
| Float/syntax error | Check units: use `@u_V` |
| No AC response | Ensure AC source: `'DC AC 1'` |

## Links to Full Guides

- [[00 - SPICEPilot Overview|Overview]]
- [[01 - SPICEPilot Setup Guide|Setup]]
- [[02 - Two-Stage CMOS Op-Amp|Op-Amp Design]]
- [[03 - KiCad Integration Methods|KiCad Integration]]
- [[04 - Simulation Workflows|Workflows]]
- [[05 - Troubleshooting Guide|Troubleshooting]]

---

**Print this page for quick reference during simulations!**

**Last Updated:** 2025-12-14
