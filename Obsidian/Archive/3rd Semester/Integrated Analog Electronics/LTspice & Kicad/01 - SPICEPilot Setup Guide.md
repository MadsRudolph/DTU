---
tags: [spice, setup, installation, python, ngspice]
date: 2025-12-14
---

# SPICEPilot Setup Guide

Complete installation and configuration guide for SPICEPilot framework.

## Prerequisites

- ✅ Miniconda/Anaconda installed
- ✅ Python 3.8+
- ✅ Windows 10/11 (or Linux/macOS with modifications)

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install PySpice matplotlib numpy
```

**Installed packages:**
- `PySpice 1.5` - Python interface to SPICE
- `matplotlib 3.10.8` - Plotting library
- `numpy 2.3.5` - Numerical computing

### 2. Install ngspice Simulator

#### Option A: Via Conda (Recommended)

```bash
# Accept conda terms of service (one-time)
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2

# Install ngspice
conda install -c conda-forge ngspice -y
```

**Installed:**
- `ngspice-41` - SPICE engine
- `ngspice-lib-41` - Shared library
- `ngspice-exe-41` - Executable

#### Option B: Manual Download

1. Download from: https://sourceforge.net/projects/ngspice/files/ngspice-devel/
2. Get the **DLL version** (e.g., `ngspice-45-64-dll.zip`)
3. Extract to `C:\ngspice\` or similar

### 3. Configure PySpice to Find ngspice

PySpice needs the `ngspice.dll` file. Copy it to the expected location:

```bash
cp "C:\Users\Mads2\miniconda3\Library\bin\ngspice.dll" \
   "C:\Users\Mads2\miniconda3\Lib\site-packages\PySpice\Spice\NgSpice\Spice64_dll\dll-vs\ngspice.dll"
```

> [!tip] Path Details
> - **Source:** Where conda installed ngspice
> - **Destination:** Where PySpice looks for the DLL

### 4. Clone SPICEPilot Repository

```bash
cd C:\Users\Mads2\
git clone https://github.com/ACADLab/SPICEPilot.git
cd SPICEPilot
```

### 5. Verify Installation

Create a test file `test_setup.py`:

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Create simple circuit
circuit = Circuit('Test')
circuit.V('input', 'in', circuit.gnd, 10@u_V)
circuit.R(1, 'in', 'out', 1@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 1@u_kOhm)

print("Circuit created successfully!")
print(circuit)

# Test simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

print("\nResults:")
for node in analysis.nodes.values():
    print(f"  {str(node)}: {float(node):.3f} V")

print("\n✓ SPICEPilot setup is working!")
```

**Run the test:**
```bash
python test_setup.py
```

**Expected output:**
```
Circuit created successfully!
.title Test
Vinput in 0 10V
R1 in out 1kOhm
R2 out 0 1kOhm

Results:
  out: 5.000 V
  in: 10.000 V

✓ SPICEPilot setup is working!
```

## Directory Structure

After setup, you should have:

```
C:\Users\Mads2\
├── miniconda3\
│   ├── Library\bin\ngspice.dll          # ngspice shared library
│   └── Lib\site-packages\
│       └── PySpice\                     # PySpice package
└── SPICEPilot\
    ├── Pilot_prompt.md                  # SPICEPilot instructions
    ├── Claude_tests\                    # Example circuits
    ├── GPT_tests\                       # More examples
    └── your_circuits\                   # Your work goes here
```

## Common Issues and Solutions

### Issue: "cannot load library ngspice.dll"

**Solution:**
```bash
# Copy ngspice.dll to PySpice directory
cp "$CONDA_PREFIX/Library/bin/ngspice.dll" \
   "$CONDA_PREFIX/Lib/site-packages/PySpice/Spice/NgSpice/Spice64_dll/dll-vs/"
```

### Issue: "Unsupported Ngspice version"

**Solution:** This is just a warning. PySpice was tested with older ngspice but works fine with version 41.

### Issue: "Note: can't find initialization file spinit"

**Solution:** Harmless warning - ngspice works without this file.

### Issue: Import errors

**Solution:**
```bash
# Reinstall PySpice
pip uninstall PySpice
pip install PySpice --no-cache-dir
```

## Environment Variables (Optional)

For system-wide ngspice access:

```bash
# Add to PATH
setx PATH "%PATH%;C:\Users\Mads2\miniconda3\Library\bin"

# Or set PySpice library path
setx PYSPICE_LIBRARY_PATH "C:\Users\Mads2\miniconda3\Library\bin\ngspice.dll"
```

## Testing ngspice Directly

Verify ngspice installation:

```bash
# Check ngspice is accessible
ngspice --version

# Test with a simple circuit
echo ".title Test
V1 1 0 DC 5
R1 1 0 1k
.op
.end" > test.cir

ngspice -b test.cir
```

## SPICEPilot Usage

The `Pilot_prompt.md` file contains instructions for generating SPICE code with LLMs. Key sections:

1. **MOSFET Definition** - NMOS/PMOS syntax
2. **Component Values** - Resistors, capacitors, etc.
3. **Simulation Types** - AC, DC, Transient
4. **Error Prevention** - Common pitfalls

> [!example] Using SPICEPilot
> Describe your circuit to an AI:
>
> *"Create a CMOS inverter with VDD=5V and analyze its transient response"*
>
> The AI (using Pilot_prompt.md) will generate the PySpice code.

## Next Steps

- [[02 - Two-Stage CMOS Op-Amp|Build the two-stage op-amp]]
- [[04 - Simulation Workflows|Learn simulation workflows]]
- Explore example circuits in `SPICEPilot/Claude_tests/`

---

**Installation Date:** 2025-12-14
**Versions:** PySpice 1.5, ngspice 41, Python 3.13
