---
tags: [kicad, spice, simulation, integration, troubleshooting]
date: 2025-12-14
---

# KiCad 9.0 Integration Methods

Guide to integrating SPICE netlists with KiCad 9.0 for circuit simulation.

## Overview

KiCad 9.0 has built-in ngspice integration, but getting external SPICE netlists to work requires understanding several approaches.

## The Challenge

**What we tried:**
1. ✅ Created complete SPICE netlist (`two_stage_opamp_kicad.cir`)
2. ⚠️ Created KiCad schematic (visual wiring issues)
3. ✅ Used `.include` directive (partial success)
4. ❌ Direct schematic-to-simulation (components not connecting)

**Key lesson:** KiCad expects components in the schematic OR needs proper netlist import methods.

## Method 1: `.include` Directive (Attempted)

### Concept
Add a text directive to your schematic that includes an external SPICE file.

### Steps

1. **Create minimal schematic:**
   - Add one resistor + GND (to satisfy KiCad requirements)
   - This creates a valid schematic

2. **Add .include directive:**
   - Place → Text (press 'T')
   - Type: `.include "C:/Users/Mads2/DTU/SPICEPilot/two_stage_opamp_kicad.cir"`
   - **Important:** Use forward slashes `/` not backslashes `\`

3. **Run simulation:**
   - Inspect → Simulator (Ctrl+Shift+S)
   - Configure AC analysis
   - Run

### Result
✅ **Simulation runs**
❌ **No signals from included file appear**

> [!warning] Limitation
> The `.include` directive works for SPICE but KiCad doesn't merge the external netlist into the signal list.
>
> **Why:** KiCad only shows signals from components in the active schematic.

### What We Learned
- KiCad simulation log shows the included circuit runs
- But signal browser only displays nodes from schematic components
- This is a KiCad design limitation, not a SPICE issue

## Method 2: Hierarchical Schematic with Subcircuit (Not Fully Tested)

### Concept
Create the op-amp as a hierarchical block in KiCad.

### Theory

1. **Create subcircuit definition:**
   ```spice
   .subckt OPAMP_2STAGE vin_p vin_n vout vdd vss
   * (all transistors and components here)
   .ends
   ```

2. **Use in main schematic:**
   - Create hierarchical sheet
   - Link to subcircuit file
   - Instance as: `X1 in+ in- out VDD VSS OPAMP_2STAGE`

### Status
⚠️ Not implemented - requires rewriting netlist as subcircuit

## Method 3: Full Schematic (Visual Wiring Issues)

### What Was Created
- `two_stage_opamp.kicad_pro` - Project file ✅
- `two_stage_opamp.kicad_sch` - Schematic with all components ⚠️

### Components Placed
- M2-M8: All 7 MOSFETs with correct models
- CA, CB, CL: All capacitors
- Voltage sources: VDD, Vbias_p, Vbias_n, Vin_p, Vin_n
- Ground symbols
- SPICE models as text

### The Problem
**Wires didn't connect properly** in KiCad's schematic format.

> [!note] Technical Details
> KiCad schematics use specific wire junction syntax:
> - `(wire (pts (xy x1 y1) (xy x2 y2)))`
> - `(junction (at x y))`
> - Connections must align precisely
>
> Manual schematic file generation is error-prone.

### Visual Result
![[kicad_disconnected_schematic.png]]

Components present but not electrically connected.

## Method 4: ngspice Direct (Recommended ✅)

### Why This Works Best

Your SPICE netlist is **perfect and complete**. The issue is purely KiCad integration, not the circuit itself.

### Using ngspice Command Line

**Interactive Mode:**
```bash
cd C:\Users\Mads2\DTU\SPICEPilot
ngspice two_stage_opamp_kicad.cir
```

Then at `ngspice 1 ->` prompt:
```
run
plot vdb(vout)       # Bode magnitude
plot vp(vout)        # Bode phase
plot v(vout) v(vin_p)  # Time domain
```

**Batch Mode:**
```bash
ngspice -b two_stage_opamp_kicad.cir -o results.txt
```

**With Batch File:**
Double-click: `run_with_plots.bat`

### Advantages
- ✅ **Works immediately** - no integration issues
- ✅ **Full control** - all ngspice features available
- ✅ **Fast** - no KiCad overhead
- ✅ **Scriptable** - can automate simulations

### Example Interactive Session

```bash
$ ngspice two_stage_opamp_kicad.cir

Circuit: Two-Stage CMOS Op-Amp

ngspice 1 -> run
Doing analysis at TEMP = 27.000000 and TNOM = 27.000000

ngspice 2 -> plot vdb(vout)
# Plot window opens with Bode magnitude

ngspice 3 -> plot vp(vout)
# Plot window opens with phase

ngspice 4 -> print v(vout)
vout = 9.054408e-02

ngspice 5 -> quit
```

## Method 5: KiCad External Netlist (Untested)

### Theory

Some KiCad versions allow specifying external netlist directly in simulator.

### Steps to Try

1. **Open Simulator** without running from schematic
2. **Look for options:**
   - File → Open...
   - Simulation → Load Netlist
   - Settings → Custom Netlist

3. **If available:**
   - Browse to `.cir` file
   - Load directly

### Status
⚠️ Feature availability varies by KiCad version/build

## Comparison Table

| Method | Integration | Difficulty | Status |
|--------|-------------|------------|--------|
| `.include` directive | KiCad GUI | Easy | ⚠️ Partial (runs but no signals) |
| Full schematic | KiCad GUI | Hard | ❌ Wiring issues |
| Subcircuit | KiCad GUI | Medium | ⚠️ Not attempted |
| ngspice direct | Command line | Easy | ✅ **Works perfectly** |
| External netlist | KiCad GUI | Medium | ⚠️ Unknown if available |

## Recommended Workflow

### For Quick Simulations
**Use ngspice directly:**
```bash
ngspice two_stage_opamp_kicad.cir
run
plot vdb(vout)
```

### For Documentation/Presentations
1. Run simulation with ngspice
2. Export data to CSV
3. Plot in Python/MATLAB/Excel
4. Include in reports

### For KiCad Integration (Future)
1. Build schematic manually in KiCad GUI
   - Place each component individually
   - Wire with 'W' key (ensure connections snap)
   - Add SPICE models to each component

2. **OR** use simpler circuits
   - Start with basic circuits (inverter, diff pair)
   - Verify KiCad workflow
   - Scale up to complex designs

## ngspice Advanced Usage

### Plotting Multiple Signals

```bash
ngspice> plot v(vout) v(n_d2) v(n_d3)
```

### Sweeping Parameters

```bash
ngspice> alter Vbias_p = 3.8
ngspice> run
ngspice> plot vdb(vout)
```

### Saving Data

```bash
ngspice> set hcopydevtype=postscript
ngspice> hardcopy bode.ps vdb(vout)

# Or export to CSV
ngspice> write results.csv v(vout)
```

### Scripting Batch Simulations

Create `batch_sim.cir`:
```spice
.title Batch Simulation

.include two_stage_opamp_kicad.cir

.control
* Run op point
op
print all > op_results.txt

* Run AC sweep
ac dec 100 0.1 1G
set hcopydevtype=postscript
hardcopy bode_plot.ps vdb(vout) vp(vout)
write ac_data.csv v(vout)

* Try different bias
alter Vbias_p = 3.8
ac dec 100 0.1 1G
write ac_data_optimized.csv v(vout)

quit
.endc

.end
```

Run: `ngspice -b batch_sim.cir`

## Python Post-Processing

After exporting CSV from ngspice:

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read ngspice CSV export
data = pd.read_csv('ac_data.csv', skiprows=1)

# Extract frequency and vout
freq = data['frequency'].values
vout_real = data['v(vout)_real'].values
vout_imag = data['v(vout)_imag'].values

# Calculate magnitude and phase
vout_mag = np.sqrt(vout_real**2 + vout_imag**2)
vout_phase = np.arctan2(vout_imag, vout_real) * 180/np.pi
gain_db = 20 * np.log10(vout_mag)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.semilogx(freq, gain_db)
ax1.grid(True)
ax1.set_ylabel('Gain (dB)')
ax1.set_title('Two-Stage Op-Amp Bode Plot')

ax2.semilogx(freq, vout_phase)
ax2.grid(True)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Phase (degrees)')

plt.tight_layout()
plt.savefig('bode_plot_python.png', dpi=300)
plt.show()
```

## KiCad Schematic Best Practices (For Future)

When manually creating schematics:

1. **Grid Alignment**
   - Keep grid at 50 mil or 1.27mm
   - Ensure all wire endpoints snap to grid

2. **Junction Markers**
   - Press 'J' to add junction dots
   - Verify connections visually

3. **Net Labels**
   - Label all important nets
   - Makes debugging easier

4. **SPICE Models**
   - Add to each component's properties
   - Or use text directives for global models

5. **Testing**
   - Start with simple circuit (inverter)
   - Verify simulation works
   - Build up complexity

## Lessons Learned

> [!success] What Works
> - SPICE netlist is correct and complete ✅
> - PySpice generates proper code ✅
> - ngspice simulates perfectly ✅
> - Batch files automate workflows ✅

> [!warning] What Doesn't (Yet)
> - KiCad schematic visual wiring ❌
> - `.include` directive signal visibility ⚠️
> - Seamless KiCad integration ⚠️

> [!tip] Best Approach
> **For this project:**
> Use ngspice directly - it's faster and works perfectly.
>
> **For future projects:**
> Build schematics manually in KiCad GUI for full integration.

## Related Topics

- [[04 - Simulation Workflows|Simulation Workflows]]
- [[05 - Troubleshooting Guide|Troubleshooting]]
- [[02 - Two-Stage CMOS Op-Amp|The Circuit Design]]

---

**Last Updated:** 2025-12-14
**Status:** ngspice method validated, KiCad integration ongoing
