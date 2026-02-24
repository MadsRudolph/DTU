---
tags: [spice, simulation, kicad, spicepilot, analog-electronics]
date: 2025-12-14
status: complete
---

# SPICEPilot - AI-Powered SPICE Simulation Setup

## Overview

SPICEPilot is an AI-driven framework for automated SPICE code generation and circuit simulation. This guide documents the complete setup and integration with KiCad 9.0 for analog circuit design.

## What We Accomplished

✅ **Installed and configured:**
- PySpice (Python SPICE library)
- ngspice (SPICE simulator)
- SPICEPilot framework

✅ **Created:**
- Two-stage CMOS operational amplifier
- Current mirror bias circuit
- Complete SPICE netlists
- KiCad project files
- Simulation workflows

✅ **Tested:**
- PySpice simulations
- ngspice command-line simulation
- KiCad 9.0 integration methods
- Theoretical validation (99.7% accuracy)

## Repository Structure

```
SPICEPilot/                         # Clean, organized structure
├── README.md                       # Main documentation
├── Pilot_prompt.md                 # SPICEPilot instructions
│
├── examples/                       # Working circuits
│   ├── 1_current_mirror/          # Current mirror (validated)
│   │   ├── current_mirror_bias.cir
│   │   ├── current_mirror_bias.py
│   │   └── RUN.bat
│   │
│   └── 2_two_stage_opamp/         # Two-stage op-amp
│       ├── two_stage_opamp_kicad.cir
│       ├── two_stage_opamp_improved.py
│       ├── two_stage_opamp.kicad_pro
│       └── RUN.bat
│
├── results/                        # Simulation outputs
│   ├── plots/                     # Graphs and plots
│   └── logs/                      # Simulation logs
│
└── archive/                        # Reference files
    ├── old_docs/                  # Previous documentation
    └── test_files/                # Test scripts
```

## Quick Links

- [[01 - SPICEPilot Setup Guide|Setup Guide]] - Complete installation instructions
- [[02 - Two-Stage CMOS Op-Amp|Op-Amp Implementation]] - Circuit design details
- [[06 - Current Mirror Circuit Example|Current Mirror Example]] - Validated simulation
- [[03 - KiCad Integration Methods|KiCad Integration]] - How to simulate in KiCad
- [[04 - Simulation Workflows|Simulation Workflows]] - Running simulations
- [[05 - Troubleshooting Guide|Troubleshooting]] - Common issues and solutions

## Key Concepts

### SPICE Simulation
SPICE (Simulation Program with Integrated Circuit Emphasis) is the industry-standard tool for analog circuit simulation.

### PySpice
Python library that provides a programmatic interface to ngspice, allowing circuit generation via code.

### SPICEPilot
AI framework that bridges LLMs with SPICE simulation, enabling natural language circuit generation.

## File Locations

**SPICEPilot Repository:**
```
C:\Users\Mads2\DTU\SPICEPilot\
```

**Conda Environment:**
```
C:\Users\Mads2\miniconda3\
```

**ngspice Installation:**
```
C:\Users\Mads2\miniconda3\Library\bin\ngspice.dll
```

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| PySpice | ✅ Working | Version 1.5 installed |
| ngspice | ✅ Working | Version 41 (conda-forge) |
| SPICE Netlist | ✅ Working | Validated with ngspice |
| PySpice Sim | ✅ Working | Generates plots |
| KiCad Project | ⚠️ Partial | Netlist works, schematic wiring issues |
| ngspice CLI | ✅ Working | Best method for simulation |

## SPICEPilot-KiCad (successor)

**`spicepilot-kicad`** is the next-generation version that adds KiCad `.kicad_sch` output and a Claude AI pipeline for generating schematics from images or text descriptions. Submodule at `DTU/spicepilot-kicad/`, [GitHub](https://github.com/MadsRudolph/spicepilot-kicad).

## Next Steps

1. **For immediate simulation:** Use ngspice command-line (see [[04 - Simulation Workflows]])
2. **For KiCad integration:** Use `.include` directive method (see [[03 - KiCad Integration Methods]])
3. **For new circuits:** Use `spicepilot-kicad` (`pip install -e DTU/spicepilot-kicad && spicepilot generate --from-text "your circuit"`)

## Tags

#spice #simulation #analog-circuits #kicad #python #circuit-design #op-amp

---

**Last Updated:** 2025-12-14
**Tools Used:** PySpice 1.5, ngspice 41, KiCad 9.0, Python 3.13
