---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: lecture-note
lecture: 5
tags: [IAE2, lecture, fabrication, layout, photolithography, CMOS, design-rules, matching, parasitic]
---
# Lecture 5 - Fabrication and Layout

**Course:** 34655 Integrated Analog Electronics 2
**Lecturer:** Per Lynggaard
**Date:** 2026-03-03

> [!quote] Albert Einstein
> *A person who never made a mistake never tried anything new*

> [!abstract] Lecture Overview
> This lecture covers IC fabrication and physical layout: the CMOS fabrication process (wafer manufacturing, photolithography, doping, oxidation, metallization), IC layer structure, layout and design rules, junction capacitances, multi-finger transistors, passive component implementation (resistors, capacitors), matching techniques, and the design flow from schematic to tape-out.

**Related material:** Chapter 2 — Fabrication, Layout, and Simulation (Baker)

---

## Recap: Noise (from Lecture 4)

### Power and SNR

$$P_\text{diss} = V_{n,\text{rms}} \cdot I_{n,\text{rms}} = R \cdot I_{n,\text{rms}}^2 = \frac{V_{n,\text{rms}}^2}{R}$$

$$\text{SNR}_\text{dB} = 10\log\left(\frac{P_\text{signal}}{P_\text{noise}}\right) = 20\log\left(\frac{V_{x,\text{rms}}}{V_{n,\text{rms}}}\right)$$

### Noise Types Summary

| Type | NSD Expression | Spectrum |
|------|---------------|----------|
| **Thermal** (white) | $\frac{\overline{V_{rms}^2}}{\Delta f} = 4kTR$ V²/Hz | Flat |
| **Flicker** (1/f) | $\frac{\overline{V_{rms}^2}}{\Delta f} = \frac{K_f \cdot V_{DC}^2}{f}$ V²/Hz | $-10$ dB/dec |
| **Shot** | $\frac{\overline{I_{rms}^2}}{\Delta f} = 2qI_{DC}$ A²/Hz | Flat (not covered) |

> [!warning] Critical Rule
> **DO NOT ADD NOISE VOLTAGES — ONLY THEIR POWER!**
> Uncorrelated noise sources: $V_{no,\text{rms}}^2 = V_{n1,\text{rms}}^2 + V_{n2,\text{rms}}^2$

### Filtered Noise

Single source through $A(s)$:

$$V_{no}^2(f) = |A(s)|^2 \cdot V_{ni}^2(f)$$

Multiple uncorrelated sources:

$$V_{no}^2(f) = \sum_i |A_i(s)|^2 \cdot V_{ni,i}^2(f)$$

### MOSFET Noise Model (Input-Referred)

$$V_i^2(f) = 4kT\left(\frac{2}{3}\right)\frac{1}{g_m} + \frac{K}{WLC_{ox}f}$$

### Input-Referred Noise — Cascaded Stages

For two stages with gains $G_1$, $G_2$:

$$V_{ni,\text{rms}}^2 = V_{n1,\text{rms}}^2 + \frac{1}{G_1^2}V_{n2,\text{rms}}^2$$

> [!tip] Design Rule
> **ALWAYS AS MUCH GAIN AS EARLY AS POSSIBLE!**
> The second stage noise is suppressed by $G_1^2$ when referred to input.

---

## IC Design: Modeling vs. Physical Implementation

| Modeling | |
|----------|--|
| **Hand calculations** | Simplified modeling — relates component parameters to performance |
| **Simulations** | Accurate modeling — predicts actual performance quite accurately |

Both feed into and interact with the **physical implementation** (layout):
- The blueprint of the design
- Similar to PCB routing, **but** components are also designed/drawn
- Understanding fabrication is essential for good layout

> [!important] Layout Matters
> Good layout is crucial for good performance. Poor layout easily ruins a good design — even very small parasitics can be devastating for performance.

---

## The Layers in an IC

ICs are built from many **layers**:

**In the substrate:**
- N-WELL
- Drain and source diffusion areas

**On top of the substrate:**
- Gate (polysilicon)
- Metal wires and vias

Key facts:
- Each layer is constructed using a **mask**
- Modern processes require **> 50 masks** and even more processing steps
- Masks are unique for each IC design
- Cost: masks ($10k–$10M NRE), wafers ($2k–$10k per wafer)

---

## Principles of Fabrication

> [!note] Scope
> This lecture illustrates **photolithography** as a fundamental technique for building ICs. Many different process variants exist.

As an IC designer we:
- Use the **component models** provided by the vendor to make designs
- Design according to the **layout rules** to make layout
- Know and understand the **design in 3D** — parasitics (capacitors, diodes, ...)

---

## Fabrication Environment — Fabs

- ICs are produced in semiconductor fabrication plants (**Fabs**)
- Very expensive to build and equip (>> $1B)
- Equipment for: stepping, photolithography, etching, and doping
- **Clean room ISO 1** requirement:
  - 1 dust particle per cubic foot
  - Overpressure to push out impurities
  - Access through airlocks

---

## Wafer Manufacturing

### Making the Ingot — Czochralski Process

1. Melt silicon at **1425 °C**
2. Add impurities (dopants)
3. Spin and pull crystal to form a single-crystal ingot

### From Ingot to Wafers

1. **Slice** ingot into wafers (0.25 mm to 1.0 mm thick)
2. **Lap** — flatten the surface
3. **Etch** — chemical cleaning
4. **Polish** one side to mirror finish

---

## Doping — Making the N-WELL

Starting from the raw P-type wafer (doped with **Boron**, acceptor atom):
- Boron: 3 valence electrons → one extra hole → **positive** carrier → P-type substrate
- Drain/source are n-type → **NMOS** transistors sit in the P-substrate

To create N-WELL, dope with **Phosphorus** (donor atom):
- Phosphorus: 5 valence electrons → one extra electron → **negative** carrier → N-type
- Drain/source are p-type → **PMOS** transistors sit in the N-well

> [!tip] Remember
> - **N-wells contain P-channel (PMOS) transistors**
> - NMOS transistors sit directly in the P-substrate
> - Parasitic diodes exist at all PN-junctions (well-to-substrate boundaries)

---

## Photolithography Process — Step by Step

The photolithography sequence (demonstrated for N-WELL creation):

| Step | Process | Description |
|------|---------|-------------|
| 1 | **Grow oxide** | $\text{SiO}_2$ layer grown by adding $\text{H}_2\text{O}$ or $\text{O}_2$ steam + heat (sacrificial oxide) |
| 2 | **Apply photoresist** | Light-sensitive polymer (PR) dispensed at center, wafer spins (~1 μm thick) |
| 3 | **Apply mask** | Photo mask placed — a "negative" of the N-WELL pattern. Cost: ~$10k to ~$10M for all masks |
| 4 | **UV exposure** | UV light passes through transparent areas of the mask |
| 5 | **Polymerization** | Exposed PR polymerizes and becomes insoluble to organic solvents |
| 6 | **Develop (solvent)** | Solvent applied — removes unexposed (un-polymerized) PR |
| 7 | **Bake** | Wafer baked to harden remaining PR, un-exposed PR removed |
| 8 | **Etch (acid)** | Acid removes oxide not covered by hardened PR |
| 9 | **Strip PR** | Second solvent removes remaining PR (required as next step needs high temperature) |
| 10 | **Implant** | N-type dopant implanted through exposed areas (phosphorous gas or ion implantation) |
| 11 | **Remove oxide** | Acid removes remaining $\text{SiO}_2$ — N-WELL completed |

> [!important] Ion Implantation
> Ion implantation is becoming the dominant doping method:
> - Higher dopant levels achievable
> - Less sideways diffusion
> - More expensive than gas diffusion

---

## Annealing

After ion implantation, the doping profile is **uneven**:
- Wafer is heated and **slowly cooled** (annealing)
- This redistributes the dopants more evenly (like shaking sand in a box)
- Smooths the doping concentration profile with depth

---

## Building the Full CMOS Structure

### Thin Oxide and Nitride

- Thin oxide grown over the wafer
- $\text{Si}_3\text{N}_4$ (silicon nitride) deposited
- Photolithography used to remove $\text{Si}_3\text{N}_4$ and oxide where **active areas** should be
- The $\text{Si}_3\text{N}_4$ prevents $\text{SiO}_2$ from growing thick in active regions

### Transistor Isolation (Field Implant)

- Photoresist applied over PMOS area (to protect it)
- Ion implantation of **p+** (Boron) in field regions
- Creates **field implants** that increase threshold voltage under field oxide, preventing parasitic channels

### Thick / Field Oxide

- Thick oxide (field oxide) grown in non-active areas
- Purpose: prevent substrate underneath from inverting when high voltage is applied on metal above
- Can also be done using **Shallow Trench Isolation (STI)**

### Threshold Voltage Adjust

- $\text{Si}_3\text{N}_4$ removed from active areas
- Old thin oxide removed, new thin **gate oxide** grown:
  - ~20 nm in 0.8 μm process
  - ~1.2 nm in 45 nm process
- Threshold voltage adjusted via ion implant directly through thin oxide

### Transistor Gates

- **Polysilicon** ("Poly") deposited over entire wafer at high temperature (1000–1250 °C)
- Resistivity: 10–30 Ω/□
- Thickness: ~250 nm
- Poly also used for **resistors** (doped differently, 100–10 kΩ/□)
- Photolithography patterns the gate shapes

### Junction Implants

**p+ implant:**
- Creates PMOS source and drain junctions (in the N-well)
- Also creates the **substrate connection** (p+ tie to P-substrate)

**n+ implant:**
- Creates NMOS source and drain junctions (in the P-substrate)
- Also creates the **N-well connection** (n+ tie to N-well)

### Metal Layers

- Metal interconnect made as a **repeated process**:
  1. Add thick oxide over entire wafer
  2. Make holes (contacts and vias)
  3. Add metal over entire wafer
  4. Remove metal where not wanted
- Last step: make very **thick top metal** layer (low resistivity for power routing)
- Between **3 and 10** metal layers depending on process

---

## Role of the Analog IC Designer

The designer is responsible for:
1. Which **components** to use
2. Where to **place** the components
3. How they are **connected**

> [!important] Division of Responsibility
> - **Designer**: circuit design (schematic) + layout
> - **Vendor (IC-fab)**: process and processing (doping levels, etc. cannot be altered)
>
> The layout is sent to the vendor as the specification for fabrication. The vendor makes the masks based on the layout.

---

## Layout and Design Rules

- Layout is made **AFTER** the schematic design is completed
- Must fulfil **design rules** for the process
- Design rules are constraints on how layers must be placed relative to each other
- Purpose: accommodate for **process variations**
- Design rules are provided by the vendor

### Verification Tools

| Tool | Full Name | Purpose |
|------|-----------|---------|
| **DRC** | Design Rule Checking | Verifies layout geometry against process rules |
| **LVS** | Layout vs. Schematic | Verifies layout matches the schematic netlist |
| **PEX** | Parasitic Extraction | Extracts parasitic R, C, L from layout for post-layout simulation |

### Layout Dimensions

- Layout is made by drawing **polygons for each layer**
- $2\lambda$ is normally referred to as the **process node** (e.g., 0.18 μm)
  - This is also the **minimum dimension** for the process
  - Normally equals $L_\text{min}$

---

## Multi-Finger Transistors

### Common Centroid Layout

In a **common centroid layout**, any linear gradient in electrical properties across the chip affects two or more devices equally — critical for **matching** in differential pairs and current mirrors.

### Benefits of Multi-Finger Structures

Wide transistors are split into multiple parallel "fingers" instead of one long gate:

| Property | Single Finger | Multi-Finger (6 fingers) |
|----------|--------------|--------------------------|
| Source area $A_S$ | $6\lambda \cdot W$ | $4\lambda \cdot W$ (smaller) |
| Drain area $A_D$ | $6\lambda \cdot W$ | $3\lambda \cdot W$ (smaller) |
| Source perimeter $P_S$ | $12\lambda + W$ | $48\lambda + W/3$ |
| Drain perimeter $P_D$ | $12\lambda + W$ | $36\lambda$ |

> [!tip] Advantages
> - **Smaller junction areas** → reduced parasitic capacitance (especially at drain)
> - More **uniform** layout
> - Better **matching** between paired transistors
> - Perimeter is calculated **without gate length** (only sidewalls and end-caps)

---

## Wafer Cross Section — Full Stack

A complete IC cross section includes (bottom to top):
- **P-Substrate** / **N-Well** / **P-Well**
- **Field oxide (FOX)** — transistor isolation
- **ILDFOX** — inter-layer dielectric
- **Metal1** — first metal interconnect
- **IMD1, Via1** — inter-metal dielectric and vias
- **Metal2, IMD2, Via2** — second metal layer
- **Metal3, IMD3, Via3** — third metal layer
- **Metal4 / Thick Metal** — top metal (low resistivity for power)
- **PROT1, PROT2** — passivation layers

Additional structures: POLY1-POLY2 capacitor, MIM capacitor, POLY2 resistor

---

## Passive Components in IC Layout

### Resistors

$$R = R_\square \cdot \frac{L}{W}$$

Where $R_\square$ is the **sheet resistance** (Ω/□).

| Material | Typical $R_\square$ | Notes |
|----------|---------------------|-------|
| Poly (undoped) | 10–30 Ω/□ | Standard |
| Poly (doped for resistors) | 100–10 kΩ/□ | High-value resistors |
| Well | Varies | Voltage-dependent |
| Metal | Very low | Only for small R values |

> [!warning] Parasitic Capacitance
> Resistors have parasitic capacitance to the substrate or the well they are formed above/in.

### Capacitors

$$C = C_\square \cdot L \cdot W$$

Where $C_\square$ is the **capacitance per unit area**.

| Type | Structure | Notes |
|------|-----------|-------|
| **MiM** | Metal-insulation-Metal | Linear, accurate |
| **PiP** | POLY-insulator-POLY | Linear, accurate |
| **$C_{gs}$** | Gate-oxide capacitance | Non-linear, cannot float |

- Normally only one capacitor type available per process
- $C_{gs}$ can be used but **not as a floating capacitor** and it is non-linear

---

## IC Design Flow

### Block-Level Design

1. Block specification
2. Schematic design
3. Build test benches
4. Simulate → spec fulfilled?
5. **Layout** (with matching, dummy structures, pads)
6. **DRC** → pass?
7. **LVS** → pass?
8. **Parasitic extraction (PEX/QRC)**
9. Simulate with parasitics → spec fulfilled?
10. Block OK — ready for top-level

### Top-Level Design

1. All blocks OK
2. Top-level schematic including padring
3. Build test benches → simulate
4. Layout → DRC → LVS → PEX → simulate
5. IC ready to send to vendor (tape-out)

> [!note] Course 34656
> The full design flow with PVT simulation, matching, dummy structures, and pad cells is covered in depth in course **34656**.

---

## More than Moore

The semiconductor industry follows two parallel trends:

| Trend | Focus | Examples |
|-------|-------|---------|
| **More Moore** (miniaturization) | Smaller transistors, more density | CPU, memory, logic (130 nm → 22 nm → 5 nm) |
| **More than Moore** (diversification) | Adding functionality | Analog/RF, sensors, HV power, biochips |

Digital content drives **System-on-Chip (SoC)**, while non-digital content drives **System-in-Package (SiP)**. The future combines both approaches for higher-value systems.

---

## Key Takeaways

> [!summary] Essential Concepts
> 1. **Photolithography** is the fundamental patterning technique: oxide → PR → mask → UV → develop → etch → implant
> 2. **N-wells** contain PMOS transistors; NMOS sit in P-substrate
> 3. **Ion implantation** is replacing gas diffusion for doping (higher precision, less lateral spread)
> 4. **Layout rules** are set by the vendor to accommodate process variations — verified by DRC
> 5. **LVS** confirms layout matches schematic; **PEX** extracts parasitics for post-layout simulation
> 6. **Multi-finger transistors** reduce parasitic capacitance and improve matching
> 7. **Common centroid layout** ensures matched devices see the same process gradients
> 8. Resistors use $R = R_\square \cdot L/W$; capacitors use $C = C_\square \cdot L \cdot W$
> 9. **Parasitic capacitances** exist at every PN-junction and between every conductor and substrate
> 10. The designer does the layout; the vendor does the processing — the process cannot be altered

---

> [!nav]
> &nbsp;
>
> [[Lecture 4 - Noise|← Lecture 4]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> [[Lecture 5 - Fabrication and Layout|Lecture 5 →]]
