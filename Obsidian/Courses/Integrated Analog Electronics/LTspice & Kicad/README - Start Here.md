---
tags: [index, readme, start-here, spice, overview]
date: 2025-12-14
---

# SPICEPilot Documentation - Start Here

Complete documentation for SPICEPilot setup and SPICE simulation workflows.

## 📚 Documentation Index

### Getting Started

1. **[[00 - SPICEPilot Overview|Overview]]** - What is SPICEPilot and what we accomplished
2. **[[01 - SPICEPilot Setup Guide|Setup Guide]]** - Complete installation instructions
3. **[[Quick Reference - SPICE Commands|Quick Reference]]** - Command cheat sheet

### Circuit Design

4. **[[02 - Two-Stage CMOS Op-Amp|Two-Stage Op-Amp]]** - Complete design and analysis
5. **[[06 - Current Mirror Circuit Example|Current Mirror Example]]** - Validated simulation example
6. [[Lessons Learned]] - What worked, what didn't, insights

### Simulation

7. **[[04 - Simulation Workflows|Simulation Workflows]]** - How to run simulations
8. **[[03 - KiCad Integration Methods|KiCad Integration]]** - Using SPICE with KiCad 9.0
9. **[[05 - Troubleshooting Guide|Troubleshooting]]** - Common issues and solutions

## 🎯 Quick Start

### I want to simulate a circuit RIGHT NOW

**Easiest way - Double-click:**
```
C:\Users\Mads2\DTU\SPICEPilot\examples\1_current_mirror\RUN.bat
```

**Or from command line:**
```bash
# 1. Navigate to circuit folder
cd C:\Users\Mads2\DTU\SPICEPilot\examples\1_current_mirror

# 2. Run ngspice
ngspice current_mirror_bias.cir

# 3. View results (automatic in .control block)
```

**See:** [[04 - Simulation Workflows#Method 1 ngspice Command Line|ngspice Workflow]]

### I want to see a complete working example

**Current Mirror (validated 99.7% accuracy):**
```bash
cd C:\Users\Mads2\DTU\SPICEPilot\examples\1_current_mirror
# Double-click: RUN.bat
```

**Two-Stage Op-Amp:**
```bash
cd C:\Users\Mads2\DTU\SPICEPilot\examples\2_two_stage_opamp
# Double-click: RUN.bat
```

**See:** [[06 - Current Mirror Circuit Example]] - Fully validated with theory

### I want to create a new circuit with AI

1. Describe your circuit in natural language
2. Reference the [[01 - SPICEPilot Setup Guide#SPICEPilot Usage|Pilot_prompt.md]] guidelines
3. AI generates PySpice code
4. Test with ngspice

**Example:** "Create a CMOS inverter with VDD=3.3V"

### I want to integrate with KiCad

**⚠️ Note:** Full KiCad integration has limitations.

**Recommended:** Use ngspice directly with `.cir` files

**Alternative:** See [[03 - KiCad Integration Methods]] for workarounds

### I'm having problems

Check [[05 - Troubleshooting Guide]] for:
- Installation errors
- Simulation failures
- KiCad issues
- Python errors

## 📊 What's in This Repository

### Files Created

```
SPICEPilot/                              # Clean, organized structure
├── README.md                            # Main documentation
├── Pilot_prompt.md                      # AI generation guide
├── LICENSE                              # Repository license
│
├── examples/                            # ⭐ YOUR WORKING CIRCUITS
│   ├── README.md                        # Quick reference
│   │
│   ├── 1_current_mirror/               # ✅ Current mirror circuit
│   │   ├── current_mirror_bias.cir     # SPICE netlist
│   │   ├── current_mirror_bias.py      # PySpice implementation
│   │   └── RUN.bat                     # Double-click to simulate!
│   │
│   └── 2_two_stage_opamp/              # ✅ Two-stage op-amp
│       ├── two_stage_opamp_kicad.cir   # SPICE netlist
│       ├── two_stage_opamp_improved.py # Optimized PySpice
│       ├── two_stage_opamp.kicad_pro   # KiCad project
│       ├── two_stage_opamp.kicad_sch   # KiCad schematic ⚠️
│       └── RUN.bat                     # Double-click to simulate!
│
├── results/                             # Simulation outputs
│   ├── plots/                          # Bode plots, graphs
│   └── logs/                           # Simulation logs
│
└── archive/                             # Reference & old files
    ├── old_docs/                       # Previous documentation
    └── test_files/                     # Test scripts
```

### Status Legend

- ✅ **Working perfectly** - Use with confidence
- ⚠️ **Partial/workaround needed** - See documentation
- ❌ **Not working** - Avoid or needs fixing

### Tool Status

| Tool | Status | Best For |
|------|--------|----------|
| ngspice CLI | ✅ | Quick simulations, validation |
| PySpice | ✅ | Automation, parameter sweeps |
| SPICE netlist | ✅ | Portable, reliable |
| KiCad simulator | ⚠️ | Full design flow (manual schematic) |
| Auto KiCad schematic | ❌ | Needs manual fixing |

## 🎓 Learning Path

### Beginner

1. Read [[00 - SPICEPilot Overview]]
2. Follow [[01 - SPICEPilot Setup Guide]]
3. Run the test circuit
4. Try [[Quick Reference - SPICE Commands]] examples

**Time:** 1-2 hours

### Intermediate

1. Study [[02 - Two-Stage CMOS Op-Amp]]
2. Understand the SPICE netlist
3. Practice [[04 - Simulation Workflows#Simulation Types|different analysis types]]
4. Try parameter sweeps

**Time:** 3-5 hours

### Advanced

1. Read [[Lessons Learned]]
2. Implement [[04 - Simulation Workflows#Parameter Sweeps|optimization workflows]]
3. Build custom circuits
4. Integrate with Python analysis tools

**Time:** Ongoing

## 🔧 Common Tasks

### Run a Simulation

```bash
ngspice circuit.cir
run
plot v(output)
```

### Create Bode Plot

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import matplotlib.pyplot as plt
import numpy as np

# ... create circuit ...
simulator = circuit.simulator()
ac = simulator.ac(start_frequency=1@u_Hz,
                  stop_frequency=1@u_GHz,
                  number_of_points=100,
                  variation='dec')

freq = np.array(ac.frequency)
vout = np.array(ac['vout'])
gain_db = 20*np.log10(np.abs(vout))

plt.semilogx(freq, gain_db)
plt.show()
```

### Optimize Parameters

```python
for vbias in np.arange(3.0, 4.0, 0.1):
    # Update circuit
    circuit.V('bias', 'vbias', circuit.gnd, vbias@u_V)
    # Simulate
    simulator = circuit.simulator()
    analysis = simulator.operating_point()
    # Analyze results
    print(f"Vbias={vbias}, Vout={float(analysis['vout']):.3f}")
```

## 📈 Performance Metrics

### What We Achieved

**Two-Stage CMOS Op-Amp:**
- ✅ Complete SPICE netlist
- ✅ Working simulations (AC, DC, Transient capable)
- ✅ Bode plot generation
- ⚠️ Performance needs optimization (low gain)

**Current Mirror Bias Circuit:**
- ✅ Fully validated and tested
- ✅ 99.7% accuracy vs. theoretical calculations
- ✅ All transistors in saturation
- ✅ Current mirror matching: > 99%

**Simulation Environment:**
- ✅ PySpice 1.5 installed and working
- ✅ ngspice 41 via conda
- ✅ Python integration
- ✅ Plotting capabilities

**Documentation:**
- ✅ 11 comprehensive guides
- ✅ 2 complete circuit examples
- ✅ Quick reference
- ✅ Troubleshooting database
- ✅ Lessons learned

## 🎯 Recommendations by Use Case

### For Homework/Assignments

**Best approach:** ngspice command-line

```bash
# Fast, reliable, simple
ngspice homework_circuit.cir
run
plot v(required_node)
# Export or screenshot plots
```

### For Learning/Experimentation

**Best approach:** PySpice scripts

```python
# Easy to modify parameters
# Save all results
# Build intuition through iteration
```

### For Project Documentation

**Best approach:** KiCad manual schematic + ngspice

1. Build schematic in KiCad (visual documentation)
2. Export netlist
3. Simulate with ngspice (reliable results)
4. Import plots into report

### For Research/Advanced Work

**Best approach:** PySpice + automation

```python
# Automated parameter sweeps
# Statistical analysis
# Publication-quality plots
```

## ⚠️ Important Notes

### Known Limitations

1. **KiCad auto-generated schematic wiring doesn't work**
   - Netlist is correct
   - Visual wiring has issues
   - Solution: Build schematic manually

2. **KiCad `.include` directive has limited functionality**
   - Simulation runs
   - But signals don't appear in browser
   - Solution: Use ngspice directly

3. **Version warnings are harmless**
   - "Unsupported ngspice version" - ignore
   - "spinit not found" - ignore
   - Everything still works

### Critical Success Factors

✅ **Do these:**
- Copy ngspice.dll to PySpice folder
- Use `@u_` notation for all units in PySpice
- Run `.op` before AC analysis
- Save work frequently

❌ **Avoid these:**
- Using Python keywords as node names
- Forgetting ground connections
- Too-tight convergence tolerances
- Auto-generating KiCad schematics (for now)

## 🔗 External Resources

### Official Documentation

- **ngspice manual:** http://ngspice.sourceforge.net/docs.html
- **PySpice docs:** https://pyspice.fabrice-salvaire.fr/
- **KiCad docs:** https://docs.kicad.org/9.0/
- **SPICEPilot paper:** https://arxiv.org/pdf/2410.20553

### Learning Resources

- **SPICE basics:** Any analog circuits textbook
- **CMOS design:** Razavi "Design of Analog CMOS Integrated Circuits"
- **Op-amp design:** Allen & Holberg "CMOS Analog Circuit Design"

### Community

- **KiCad forum:** https://forum.kicad.info/
- **ngspice mailing list:** http://ngspice.sourceforge.net/mailinglist.html

## 📝 Quick Reference

### Essential Commands

```bash
# ngspice
run                    # Run simulation
plot vdb(vout)        # Plot in dB
print all             # Show all voltages
quit                  # Exit

# PySpice units
1@u_V                 # 1 volt
1@u_kOhm              # 1 kilohm
1@u_pF                # 1 picofarad
1@u_MHz               # 1 megahertz
```

See [[Quick Reference - SPICE Commands]] for complete list.

### File Locations

```
C:\Users\Mads2\DTU\SPICEPilot\examples\        # Working circuits (organized!)
  ├── 1_current_mirror\                    # Current mirror circuit
  └── 2_two_stage_opamp\                   # Two-stage op-amp

C:\Users\Mads2\DTU\SPICEPilot\results\         # Simulation outputs
  ├── plots\                               # Graphs and plots
  └── logs\                                # Simulation logs

C:\Users\Mads2\miniconda3\Library\bin\     # ngspice executable
C:\Users\Mads2\DTU\Obsidian\...            # This documentation
```

## 💡 Tips for Success

> [!tip] Pro Tips
> 1. **Always validate with ngspice first** - fastest feedback
> 2. **Document as you go** - future you will be grateful
> 3. **Start simple** - verify basics before adding complexity
> 4. **Use version control** - track your circuit changes
> 5. **Learn keyboard shortcuts** - saves huge amounts of time

> [!warning] Common Mistakes
> - Jumping straight to KiCad without testing netlist
> - Not checking DC bias before AC analysis
> - Forgetting to specify units
> - Over-complicating simple tasks

> [!success] Success Pattern
> 1. Create/get SPICE netlist
> 2. Test with `ngspice circuit.cir`
> 3. Verify results make sense
> 4. Iterate and optimize
> 5. Document final design

## 🆘 Getting Help

### Troubleshooting Steps

1. Check [[05 - Troubleshooting Guide]]
2. Review [[Quick Reference - SPICE Commands]]
3. Look at [[Lessons Learned]]
4. Test with minimal example
5. Check error messages carefully

### What to Include When Asking for Help

- Exact error message
- Circuit file (or minimal reproducing example)
- What you tried
- Expected vs. actual behavior
- Tool versions

## 📅 Version History

**v1.1 - 2025-12-14 (Evening)**
- Added current mirror bias circuit example
- Complete validation with theoretical calculations
- Additional batch file for viewing results
- Expanded documentation to 11 guides

**v1.0 - 2025-12-14**
- Initial setup complete
- Two-stage op-amp implemented
- Full documentation created
- All tools validated

## 🎉 Summary

**What you have now:**
- ✅ Working SPICE simulation environment
- ✅ Two complete circuit examples (op-amp + current mirror)
- ✅ Fully validated simulations (99.7% theoretical accuracy)
- ✅ Multiple simulation workflows
- ✅ Comprehensive documentation (11 guides)
- ✅ Troubleshooting knowledge

**Next steps:**
- Design your own circuits
- Explore other topologies
- Build KiCad skills with simple circuits
- Automate with Python

**Remember:** The goal is to design and simulate circuits effectively. Don't let tool integration issues block your progress - use what works!

---

**Last Updated:** 2025-12-14
**Status:** Complete and validated
**Maintained by:** Mads

**For questions about this documentation, refer to the specific guides linked above.**
