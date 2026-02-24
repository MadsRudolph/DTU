---
type: project
tags: [project, tools, spicepilot-kicad, kicad, qspice, spice, python, AI]
status: active
created: 2026-02-24
repo: https://github.com/MadsRudolph/spicepilot-kicad
---
# SPICEPilot-KiCad

AI-powered circuit schematic generator that produces KiCad (`.kicad_sch`) and QSPICE (`.qsch`) files from circuit images or text descriptions.

> [!info] Location
> Submodule at `DTU/spicepilot-kicad/`
> [GitHub](https://github.com/MadsRudolph/spicepilot-kicad) (private)

---

## Relation to SPICEPilot

Successor to the original [[QSPICE Schematic Generator Library|SPICEPilot]] (`DTU/SPICEPilot/`). Key additions:

- **Dual output**: KiCad 8 (`.kicad_sch`) + QSPICE (`.qsch`) from the same `Schematic` object
- **AI pipeline**: Claude API converts images or text descriptions into structured `CircuitDefinition` JSON, then deterministic Python generates the schematic files
- **CLI**: `spicepilot generate --from-image circuit.png` or `--from-text "NMOS current mirror"`

---

## Quick Start

```bash
cd DTU/spicepilot-kicad
pip install -e .
```

### Python API

```python
from spicepilot import Schematic, NMOS, PMOS, R, C, V, I

sch = Schematic(title="NMOS Current Mirror")
sch.add(NMOS("M1", model="NMOS_018", W="6.2u", L="1u"))
sch.add(NMOS("M2", model="NMOS_018", W="6.2u", L="1u"))
sch.add(V("Vdd", "1.8"))
sch.add(I("Iref", "20u"))

sch.connect("M1.D", "M1.G", net="bias")
sch.connect("M1.G", "M2.G")
sch.connect("Iref.+", "VDD")
sch.connect("Iref.-", "M1.D")
sch.connect("M1.S", "GND")
sch.connect("M2.S", "GND")
sch.connect("M2.D", "VDD")
sch.connect("Vdd.+", "VDD")
sch.connect("Vdd.-", "GND")

sch.model("NMOS_018", "nmos", level=1, kp="200u", vto="0.5")
sch.directive(".op")

sch.layout()
sch.save("current_mirror.kicad_sch", format="kicad")
sch.save("current_mirror.qsch", format="qspice")
```

### CLI with AI

```bash
export ANTHROPIC_API_KEY=sk-ant-...
spicepilot generate --from-image circuit.png --format both -o my_circuit
spicepilot generate --from-text "NMOS current mirror with 20uA ref" -o mirror
spicepilot components   # list supported component types
```

---

## Supported Components

| Type | Pins | Description |
|------|------|-------------|
| NMOS | G, D, S | N-channel MOSFET |
| PMOS | G, D, S | P-channel MOSFET |
| R | +, - | Resistor |
| C | +, - | Capacitor |
| V | +, - | Voltage source |
| I | +, - | Current source |
| L | +, - | Inductor |
| D | A, K | Diode |

---

## Architecture

```
spicepilot/
├── core/       Types, schematic API, graph analysis, layout, registry
├── kicad/      KiCad .kicad_sch S-expression backend
├── qspice/     QSPICE .qsch binary format backend
├── pipeline/   Claude API: image/text -> CircuitDefinition JSON -> schematic
└── cli.py      Command-line interface
```

**Pipeline**: `Image/Text -> Claude API -> CircuitDefinition JSON -> Schematic -> layout() -> KiCad / QSPICE`

---

## Examples

- `examples/current_mirror.py` -- NMOS current mirror
- `examples/two_stage_opamp.py` -- Two-stage CMOS operational amplifier
