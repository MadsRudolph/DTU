---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: reference
tags: [IAE2, tools, qspice, spice, python, SPICEPilot]
---
# QSPICE Schematic Generator Library

> [!info] Location
> `SPICEPilot/qspice/` -- Python package inside the [[Cadence Exercise - Two-Stage OpAmp Design|SPICEPilot]] repo (submodule at `DTU/SPICEPilot/`).
> Example: `SPICEPilot/examples/4_qspice_opamp/opamp_qspice.py`

A Python library for programmatically generating QSPICE `.qsch` schematics. Define components and connections in code, then either place them manually or let the auto-layout algorithm arrange everything.

---

## Quick Start

```python
from qspice import Schematic, NMOS, PMOS, R, C, V, I

sch = Schematic()

# Add components
sch.add(PMOS("MQ1", model="PMOS_018", W="24u", L="1u"))
sch.add(NMOS("MQ3", model="NMOS_018", W="6.2u", L="1u"))
sch.add(R("Rc", "995"))
sch.add(C("Cc", "0.8p"))
sch.add(V("Vdd", "1.8"))

# Define connections
sch.connect("MQ1.D", "MQ3.D", net="n_d1")
sch.connect("MQ1.S", "VDD")

# SPICE directives
sch.model("NMOS_018", "nmos", level=1, kp="270u", vto=0.5)
sch.directive(".ac dec 200 1 10G")

# Auto-layout and save
sch.layout()
sch.save("output.qsch")
```

---

## Package Structure

```
SPICEPilot/qspice/
├── __init__.py        Public API exports
├── _types.py          Data structures (NamedTuples)
├── encoding.py        Binary .qsch format encoding
├── symbols.py         Symbol drawing templates + pin definitions
├── components.py      Factory functions: NMOS, PMOS, R, C, V, I, L, D
├── schematic.py       Schematic class (main API)
├── graph.py           Connectivity analysis + topology detection
└── layout.py          Auto-layout algorithm
```

---

## API Reference

### Component Factories

All factories return a `ComponentDef` that gets passed to `sch.add()`.

| Factory | Arguments | SPICE Element |
|---------|-----------|---------------|
| `NMOS(name, model, W, L)` | `model="NMOS"`, `W=""`, `L=""` | N-Channel MOSFET |
| `PMOS(name, model, W, L)` | `model="PMOS"`, `W=""`, `L=""` | P-Channel MOSFET |
| `R(name, value)` | `value="1k"` | Resistor |
| `C(name, value)` | `value="1p"` | Capacitor |
| `V(name, value)` | `value="1"` | Voltage source |
| `I(name, value)` | `value="1m"` | Current source |
| `L(name, value)` | `value="1u"` | Inductor |
| `D(name, model)` | `model="D"` | Diode |

### Pin Names

| Component | Pins |
|-----------|------|
| NMOS | `D` (drain), `G` (gate), `S` (source) |
| PMOS | `D` (drain), `G` (gate), `S` (source) |
| R, C, V, I, L | `+` (top/positive), `-` (bottom/negative) |
| D | `A` (anode), `K` (cathode) |

Pin references in `connect()` use dot notation: `"MQ1.D"`, `"Rc.+"`, `"Vdd.-"`.

Bare strings like `"VDD"` or `"GND"` are treated as net names, not pin references.

### Schematic Class

```python
sch = Schematic()
```

#### Defining the circuit

| Method | Description |
|--------|-------------|
| `sch.add(comp)` | Register a component |
| `sch.connect(a, b, net=None)` | Connect two pins or a pin to a net |
| `sch.model(name, kind, **params)` | Add a `.model` directive |
| `sch.directive(text)` | Add any SPICE directive string |

#### Placement (choose one approach)

| Method | Description |
|--------|-------------|
| `sch.place(name, x, y, rot=0)` | Manually place a component |
| `sch.layout()` | Run auto-layout on all unplaced components |

#### Manual wiring primitives

| Method | Description |
|--------|-------------|
| `sch.wire(x1, y1, x2, y2, name="")` | Add a wire segment |
| `sch.net(x, y, flags, name)` | Add a net label |
| `sch.junc(x, y)` | Add a junction dot |

#### Output

| Method | Description |
|--------|-------------|
| `sch.save(path)` | Write the `.qsch` binary file |
| `sch.pin_pos(ref)` | Get `(x, y)` of a placed pin (e.g. `"MQ1.D"`) |

---

## Rotation System

QSPICE uses a 4-bit rotation code. The lower 3 bits encode 90-degree rotations; bit 3 adds a horizontal mirror.

| `rot` | Transform $(dx, dy) \to$ | Typical use |
|-------|--------------------------|-------------|
| 0 | $(x, y)$ | Default orientation |
| 2 | $(-y, x)$ | 90 CCW -- horizontal capacitor |
| 4 | $(-x, -y)$ | 180 -- flipped |
| 6 | $(y, -x)$ | 270 CCW -- horizontal resistor |
| 8 | $(-x, y)$ | Mirror -- diff pair right side |
| 10 | $(-y, -x)$ | Mirror + 90 |
| 12 | $(x, -y)$ | Mirror + 180 |
| 14 | $(y, x)$ | Mirror + 270 |

### Common rotation choices

- **PMOS/NMOS normal** (`rot=0`): gate faces left
- **Diff pair right side** (`rot=8`): gate faces right (mirrored)
- **Horizontal resistor** (`rot=6`): `+` pin at left, `-` at right
- **Horizontal capacitor** (`rot=2`): `+` pin at left, `-` at right

---

## Net Label Flags

| `flags` | Direction | Use |
|---------|-----------|-----|
| 7 | Left-pointing | Signal label |
| 11 | Right-pointing | Signal label |
| 13 | Down-pointing | GND flag |
| 14 | Up-pointing | VDD flag |

---

## Auto-Layout Algorithm

The `layout()` method performs automatic placement and wiring in three phases.

### 1. Stage Assignment (columns)

Components are assigned to stages (columns, left to right) based on their role:

| Stage | X Position | Contents |
|-------|-----------|----------|
| -1 | Far left | Standalone sources (Vdd, Vin, Ibias) |
| 0 | Bias column | Diode-connected MOSFETs (bias references) |
| 1 | Center | Diff pair + mirror loads + tail sources |
| 2+ | Right | Second stage, output, compensation |

### 2. Topology Detection (`graph.py`)

The `NetGraph` analyses connections to identify common analog patterns:

- **Diode-connected**: gate and drain on the same net
- **Current mirror**: two same-type MOSFETs sharing a gate net, one diode-connected
- **Differential pair**: two same-type MOSFETs sharing a source net
- **Cascode**: same-type MOSFETs where one's drain connects to the other's source

### 3. Placement + Wiring (`layout.py`)

**Vertical ordering** within each column:
- PMOS devices at top (near VDD rail)
- NMOS devices at bottom (near GND)
- Passives in the middle

**Wire routing**:
- **VDD**: horizontal rail wire across the top, connecting all PMOS sources and V+ pins
- **GND**: individual downward net labels (`flags=13`) below each NMOS source
- **Short nets** (pins within ~3 stages): direct wires (straight or L-shaped) with junction dots
- **Long nets** (>3 stages apart): net labels instead of long wires

---

## Binary Format (`.qsch`)

The `.qsch` format is a binary text format with these conventions:

| Element | Bytes |
|---------|-------|
| File header | `\xff\xd8\xff\xdb` |
| Block open | `\xab` |
| Block close | `\xbb` |
| Line ending | `\r\n` |
| SPICE text prefix | `\xef\xbb\xbf` (UTF-8 BOM) |

All coordinates are integers in QSPICE grid units (100 units = 1 grid square). Text content is encoded as Latin-1.

---

## Example: 34655 Two-Stage OpAmp

The full example is at `SPICEPilot/examples/4_qspice_opamp/opamp_qspice.py`. It generates the same opamp from the [[Cadence Exercise - Two-Stage OpAmp Design|paper design exercise]] in two modes:

1. **Manual placement** -- reproduces the exact layout from `gen_qsch.py` (byte-for-byte identical element counts)
2. **Auto-layout** -- defines only components + connections, lets the algorithm arrange everything

```bash
cd SPICEPilot
python examples/4_qspice_opamp/opamp_qspice.py
# Generates:
#   examples/4_qspice_opamp/two_stage_opamp_manual.qsch
#   examples/4_qspice_opamp/two_stage_opamp_auto.qsch
```

Open either `.qsch` file in QSPICE to view, simulate, or verify against the reference netlist at `SPICEPilot/examples/3_34655_opamp/two_stage_opamp_34655.cir`.

### Circuit topology

```
VDD ─────────────────────────────────────────────
  │           │              │
 MQ8(P)     MQ5(P)         MQ6(P)
 diode     tail src       load
  │           │              │
 Ibias    ┌───┴───┐     vout├──Rc──Cc──┐
  │      MQ1(P) MQ2(P)      │          │
 GND     inv   non-inv    MQ7(N)       │
          │       │        CS gain      │
         MQ3(N) MQ4(N)      │       feedback
         diode  mirror     GND      CB,CA,R1,CL
          │       │
         GND     GND
```

### SPICE directives included

- `.model NMOS_018` / `PMOS_018` (Level 1, 0.18 um parameters)
- `.ac dec 200 1 10G`
- `.meas` for DC gain, UGF, and phase margin
