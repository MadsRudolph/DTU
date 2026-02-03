---
tags: [troubleshooting, debugging, spice, errors, solutions]
date: 2025-12-14
---

# Troubleshooting Guide

Common issues encountered during SPICE simulation setup and their solutions.

## Installation Issues

### PySpice Installation Errors

#### Error: "cannot load library ngspice.dll"

**Symptoms:**
```
OSError: cannot load library 'ngspice.dll': error 0x7e
```

**Cause:** PySpice can't find the ngspice shared library

**Solutions:**

1. **Copy DLL to PySpice directory:**
   ```bash
   cp "C:\Users\Mads2\miniconda3\Library\bin\ngspice.dll" \
      "C:\Users\Mads2\miniconda3\Lib\site-packages\PySpice\Spice\NgSpice\Spice64_dll\dll-vs\"
   ```

2. **Set environment variable:**
   ```bash
   setx PYSPICE_LIBRARY_PATH "C:\Users\Mads2\miniconda3\Library\bin\ngspice.dll"
   ```

3. **Verify ngspice installation:**
   ```bash
   conda list ngspice
   # Should show: ngspice-41, ngspice-lib-41
   ```

#### Warning: "Unsupported Ngspice version 41"

**Symptoms:**
```
Unsupported Ngspice version 41
```

**Cause:** PySpice was developed for older ngspice versions

**Solution:** ✅ **Ignore this warning**
- ngspice 41 works perfectly with PySpice
- This is just a version check warning
- All functionality is available

#### Warning: "can't find initialization file spinit"

**Symptoms:**
```
Note: can't find the initialization file spinit.
```

**Cause:** ngspice looks for optional configuration file

**Solution:** ✅ **Ignore this warning**
- `spinit` is optional
- ngspice works without it
- No functionality affected

### Conda Installation Issues

#### Error: "CondaToSNonInteractiveError: Terms of Service not accepted"

**Cause:** Conda requires TOS acceptance

**Solution:**
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
```

Then retry: `conda install -c conda-forge ngspice -y`

## SPICE Netlist Errors

### Syntax Errors

#### Error: "Unknown control"

**Symptom:**
```
Error on line 5: unknown control "..."
```

**Common causes:**
1. Missing `.` before commands
   ```spice
   # Wrong
   model NMOS nmos (...)

   # Correct
   .model NMOS nmos (...)
   ```

2. Typos in command names
   ```spice
   .tranient 1n 10u  # Wrong
   .tran 1n 10u      # Correct
   ```

#### Error: "Node name is a Python keyword"

**Symptom:**
```
Node name 'in' is a Python keyword
```

**Cause:** Using Python reserved words as node names

**Solution:** Append underscore or rename
```python
# Causes warning
circuit.V('input', 'in', circuit.gnd, 10@u_V)

# Fixed
circuit.V('input', 'vin', circuit.gnd, 10@u_V)
# or
circuit.V('input', 'in_', circuit.gnd, 10@u_V)
```

#### Error: "Floating node"

**Symptom:**
```
Warning: Node X is floating
```

**Cause:** Node not connected to ground or any DC path

**Solution:**
```spice
# Add DC path to ground
R_leak node_x 0 100Meg  # High-value leak resistor
```

### Unit Errors

#### Error: "1kOhm is not defined"

**Symptom:**
```
NameError: name 'kOhm' is not defined
```

**Cause:** Forgetting to use PySpice unit syntax

**Solution:**
```python
# Wrong
circuit.R(1, 'a', 'b', 1kOhm)

# Correct - use @ operator with u_ prefix
circuit.R(1, 'a', 'b', 1@u_kOhm)
# or
circuit.R(1, 'a', 'b', 1000@u_Ohm)
```

**Common units:**
- `@u_V` - volts
- `@u_A` - amps
- `@u_Ohm` - ohms
- `@u_kOhm` - kilohms
- `@u_F` - farads
- `@u_pF` - picofarads
- `@u_Hz` - hertz
- `@u_MHz` - megahertz

## Simulation Errors

### Convergence Problems

#### Error: "Timestep too small; simulation aborted"

**Symptoms:**
```
doAnalyses: Timestep too small; time = X, timestep = Y
```

**Causes:**
1. Unrealistic component values
2. Stiff circuit (very different time constants)
3. Poor initial conditions

**Solutions:**

1. **Adjust convergence options:**
   ```python
   simulator.options(reltol=1e-3, abstol=1e-12, vntol=1e-6)
   ```

   ```spice
   .options reltol=1e-3 abstol=1e-12
   ```

2. **Increase iteration limits:**
   ```python
   simulator.options(itl1=300, itl2=100)
   ```

3. **Set initial conditions:**
   ```python
   circuit.C('1', 'node1', circuit.gnd, 10@u_uF, ic=5@u_V)
   ```

4. **Use UIC (Use Initial Conditions):**
   ```python
   analysis = simulator.transient(step_time=1@u_ns, end_time=10@u_us,
                                  use_initial_condition=True)
   ```

5. **Check component values:**
   ```python
   # Problematic
   circuit.C('1', 'a', 'b', 1e-20@u_F)  # Too small!

   # Better
   circuit.C('1', 'a', 'b', 1@u_pF)
   ```

#### Error: "singular matrix"

**Symptoms:**
```
singular matrix: check node X
```

**Causes:**
1. Zero-resistance loop (voltage sources in series)
2. Capacitor-only loops
3. Disconnected subcircuits

**Solutions:**

1. **Add small resistance:**
   ```spice
   * Between voltage sources
   V1 n1 0 DC 5
   R_small n1 n2 1m  # 1 milliohm
   V2 n2 0 DC 3

   * In capacitor loops
   C1 n1 n2 10u
   R_damping n2 0 1Meg  # Prevents pure C loop
   ```

2. **Check circuit topology:**
   - Ensure all nodes have DC path to ground
   - No capacitor-only loops
   - No voltage source loops

### No Data / Empty Results

#### Issue: "Simulation runs but no data"

**Symptoms:**
- Simulation completes
- No error messages
- But `analysis.nodes` is empty or plotting fails

**Causes:**
1. Simulation type doesn't match what you're accessing
2. Wrong node names

**Solutions:**

1. **Check node names:**
   ```python
   # After simulation
   print(list(analysis.nodes.keys()))  # See available nodes
   ```

2. **Access correct analysis type:**
   ```python
   # For operating point
   op = simulator.operating_point()
   print(op['vout'])  # Access by node name

   # For AC analysis
   ac = simulator.ac(...)
   print(ac['vout'])  # Returns complex array

   # For transient
   tran = simulator.transient(...)
   print(tran['vout'])  # Returns real array
   ```

3. **Verify analysis ran:**
   ```python
   if analysis is None:
       print("Simulation failed!")
   else:
       print("Simulation succeeded")
       print(f"Data points: {len(analysis['vout'])}")
   ```

## KiCad Integration Issues

### No Signals in Signal Browser

#### Issue: `.include` directive runs but no signals appear

**Symptom:**
- Simulation log shows included circuit ran
- Signal browser is empty or only shows schematic components

**Cause:** KiCad only shows signals from components in active schematic

**Solution:** ✅ **Use ngspice directly**
```bash
ngspice two_stage_opamp_kicad.cir
```

**Alternative:** Build complete schematic in KiCad (not just .include)

### Schematic Components Not Connecting

#### Issue: Components placed but wires don't connect

**Symptoms:**
- Visual wires drawn
- Simulation runs but wrong results
- ERC shows "pins not connected"

**Causes:**
1. Wires not snapping to pins
2. Junction dots missing
3. Grid alignment issues

**Solutions:**

1. **Check grid alignment:**
   - View → Grid Settings
   - Use 50 mil (1.27mm) grid
   - Ensure snap to grid enabled

2. **Add junction dots:**
   - Press 'J' key at wire intersections
   - Verify green dot appears

3. **Verify connections:**
   - Click on wire - should highlight all connected components
   - Use Tools → ERC to check connections

4. **Rebuild connections:**
   - Select wire → Delete
   - Press 'W' and redraw
   - Ensure endpoints snap to pins (should see crosshair)

### KiCad Can't Find SPICE Models

#### Error: "Model NMOS not found"

**Symptoms:**
```
Error: Unknown model 'NMOS'
```

**Solutions:**

1. **Add models to schematic as text:**
   - Place → Text
   - Type complete .model statement:
     ```spice
     .model NMOS nmos (level=1 kp=120u vto=0.7 lambda=0.02 w=30u l=2u)
     ```

2. **Add to component properties:**
   - Right-click component → Properties
   - Simulation Model tab
   - Add model parameters

3. **Use .include for model library:**
   ```spice
   .include "models.lib"
   ```

## Python/PySpice Errors

### Import Errors

#### Error: "No module named 'PySpice'"

**Solution:**
```bash
pip install PySpice
```

Verify:
```bash
python -c "import PySpice; print(PySpice.__version__)"
```

#### Error: "No module named 'matplotlib'"

**Solution:**
```bash
pip install matplotlib numpy
```

### Numpy Deprecation Warnings

#### Warning: "Conversion of ndim > 0 to scalar deprecated"

**Symptoms:**
```
DeprecationWarning: Conversion of an array with ndim > 0 to scalar is deprecated
```

**Cause:** Numpy version incompatibility

**Solution:** ✅ **Ignore for now**
- Code still works
- Will be fixed in future PySpice update

**Workaround:**
```python
# Instead of
vout = float(analysis['vout'])

# Use
vout = float(analysis['vout'].item())
# or
vout = float(np.array(analysis['vout']))
```

### Unicode Encoding Errors

#### Error: "UnicodeEncodeError: 'charmap' codec can't encode character"

**Cause:** Terminal doesn't support special characters (✓, →, etc.)

**Solution:**
```python
# Avoid fancy characters
print("\nDone!")  # Instead of print("\n✓ Done!")
```

Or set encoding:
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Performance Issues

### Slow Simulations

#### Issue: AC analysis takes very long

**Causes:**
1. Too many frequency points
2. Complex circuit
3. Tight convergence tolerances

**Solutions:**

1. **Reduce points:**
   ```spice
   # From
   .ac dec 100 0.1 1G  # 100 points/decade

   # To
   .ac dec 50 0.1 1G   # 50 points/decade
   ```

2. **Relax tolerances:**
   ```python
   simulator.options(reltol=1e-3)  # From 1e-4
   ```

3. **Limit frequency range:**
   ```spice
   .ac dec 100 1 1Meg  # Instead of 0.1 to 1G
   ```

### Memory Issues

#### Error: "MemoryError" or system slowdown

**Cause:** Large number of data points

**Solutions:**

1. **Reduce simulation points**
2. **Run in batches:**
   ```python
   # Instead of 0.1 Hz to 1 GHz
   # Run multiple smaller ranges
   sim1 = simulator.ac(start_frequency=1@u_Hz,
                       stop_frequency=1@u_MHz, ...)
   sim2 = simulator.ac(start_frequency=1@u_MHz,
                       stop_frequency=1@u_GHz, ...)
   ```

3. **Clear memory between runs:**
   ```python
   import gc
   del analysis
   gc.collect()
   ```

## Results Analysis Issues

### Unexpected Results

#### Issue: Gain is 0 dB or -inf dB

**Causes:**
1. No AC stimulus
2. Wrong node measured
3. Circuit not biased properly

**Solutions:**

1. **Check AC source:**
   ```python
   # Must have AC component
   circuit.V('in', 'vin', circuit.gnd, '2.5 AC 1')  # ✓
   # Not just DC
   circuit.V('in', 'vin', circuit.gnd, 2.5@u_V)     # ✗
   ```

2. **Verify DC bias:**
   ```python
   op = simulator.operating_point()
   print("DC voltages:")
   for node in op.nodes.values():
       print(f"  {node}")

   # Check transistors in saturation
   ```

3. **Check signal path:**
   - Verify connections from input to output
   - Look for open circuits or shorts

#### Issue: Phase is constant (0° or 180°)

**Cause:** Plotting magnitude instead of phase

**Solution:**
```python
# For phase, use np.angle
phase = np.angle(vout_complex, deg=True)

# Not
phase = np.abs(vout_complex)  # This is magnitude!
```

## Debugging Strategies

### Systematic Approach

1. **Simplify:**
   - Start with minimal circuit
   - Add complexity incrementally
   - Identify where problem appears

2. **Check DC first:**
   - Always run .op before AC/tran
   - Verify bias points are reasonable
   - Check transistor regions

3. **Use test points:**
   ```python
   # Add voltage sources as test points
   circuit.V('test', 'internal_node', circuit.gnd, 0@u_V)
   # Can now measure current through V_test
   ```

4. **Compare to known-good:**
   - Use simple test circuits (voltage divider)
   - Verify tools work with basic examples
   - Then add your complex circuit

### Logging and Debugging

**Enable verbose output:**
```python
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
simulator.save_internal_parameters()  # Save more data
```

**Check raw output:**
```python
print(circuit)  # Print SPICE netlist
```

**Save intermediate results:**
```python
import pickle

# Save simulation results
with open('results.pkl', 'wb') as f:
    pickle.dump(analysis, f)

# Load later
with open('results.pkl', 'rb') as f:
    analysis = pickle.load(f)
```

## Quick Diagnostic Checklist

- [ ] PySpice installed? (`pip list | grep PySpice`)
- [ ] ngspice.dll in correct location?
- [ ] All components have values?
- [ ] Ground node present?
- [ ] DC paths to ground for all nodes?
- [ ] AC source present (for AC analysis)?
- [ ] Units specified correctly (@u_V, @u_kOhm)?
- [ ] No Python keywords as node names?
- [ ] Convergence options set if needed?
- [ ] Checking correct analysis type?

## When All Else Fails

1. **Test with minimal example:**
   ```python
   from PySpice.Spice.Netlist import Circuit
   from PySpice.Unit import *

   circuit = Circuit('Test')
   circuit.V('in', 'vin', circuit.gnd, 10@u_V)
   circuit.R(1, 'vin', 'vout', 1@u_kOhm)
   circuit.R(2, 'vout', circuit.gnd, 1@u_kOhm)

   simulator = circuit.simulator()
   analysis = simulator.operating_point()

   print(f"vout = {float(analysis['vout']):.3f} V")  # Should be 5.000 V
   ```

2. **Use ngspice directly:**
   - Your `.cir` file is correct
   - ngspice works perfectly
   - Bypass integration issues

3. **Check versions:**
   ```bash
   python --version
   pip show PySpice
   ngspice --version
   ```

4. **Reinstall clean:**
   ```bash
   pip uninstall PySpice
   conda remove ngspice
   conda install -c conda-forge ngspice -y
   pip install PySpice --no-cache-dir
   ```

## Getting Help

### Information to Provide

When asking for help, include:

1. **Error message** (full traceback)
2. **Circuit file** (or minimal reproducing example)
3. **Python/PySpice versions**
4. **OS and environment**
5. **What you tried**

### Useful Resources

- **ngspice manual:** http://ngspice.sourceforge.net/docs.html
- **PySpice docs:** https://pyspice.fabrice-salvaire.fr/
- **SPICE basics:** Any undergraduate electronics textbook
- **KiCad forum:** https://forum.kicad.info/

## Related Topics

- [[01 - SPICEPilot Setup Guide|Setup Guide]]
- [[04 - Simulation Workflows|Simulation Workflows]]
- [[00 - SPICEPilot Overview|Main Overview]]

---

**Last Updated:** 2025-12-14
**Based on:** Actual issues encountered during setup
