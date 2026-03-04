---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: quiz
tags: [IAE2, quiz]
---
# Quiz 3 - Fabrication and Layout

> [!info] Related Notes
> - [[Lecture 5 - Fabrication and Layout]]
> - [[Problem 5 - Layout]]

---

## Question 1 (1 point)

> [!question] The main lay-out parameters that a designer has available when designing analog CMOS transistor circuits are
> - [x] **channel width and length**
> - [ ] channel depth
> - [ ] gate oxide thickness

> [!success] Answer: Channel width and length

> [!note]- Explanation
> In CMOS IC design, the designer controls two primary layout parameters:
>
> - **Channel width ($W$)** — determines current drive capability
> - **Channel length ($L$)** — determines speed, gain, and matching
>
> Other parameters like **gate oxide thickness** and **channel depth** are **process parameters** set by the foundry and cannot be changed by the designer.
>
> > [!quote] From Lecture 5
> > *"The designer: circuit design (schematic) + layout. The vendor: process and processing (doping levels, etc. cannot be altered)."*
>
> See: [[Lecture 5 - Fabrication and Layout#Role of the Analog IC Designer]]

---

## Question 2 (1 point)

> [!question] In a modern CMOS process the gate material of a transistor is made of
> - [ ] aluminium
> - [ ] copper
> - [x] **polycrystalline silicon**

> [!success] Answer: Polycrystalline silicon

> [!note]- Explanation
> The gate material in standard CMOS processes is **polycrystalline silicon** (polysilicon or "poly"):
>
> - Deposited at high temperature (1000–1250 °C)
> - Resistivity: 10–30 Ω/□
> - Thickness: ~250 nm
> - Also used for resistors (with different doping: 100–10 kΩ/□)
>
> | Material | Role in CMOS |
> |----------|-------------|
> | **Polysilicon** | Gate electrode |
> | Aluminium / Copper | Metal interconnect layers (not the gate) |
>
> > [!tip] Historical Note
> > Very advanced nodes (≤ 45 nm) use **high-k metal gate** (HKMG) technology, but polysilicon remains the standard answer for most analog CMOS processes.
>
> See: [[Lecture 5 - Fabrication and Layout#Transistor Gates]]

---

## Question 3 (1 point)

> [!question] The order of magnitude for the minimum channel length for a transistor in an analog circuit in a modern CMOS process is
> - [x] **100 nm**
> - [ ] 1 um
> - [ ] 10 um

> [!success] Answer: 100 nm

> [!note]- Explanation
> Modern CMOS process nodes for analog design include 180 nm, 130 nm, 65 nm, and 28 nm. All of these have minimum channel lengths on the **order of 100 nm**.
>
> From the lecture:
> $$2\lambda = L_\text{min} = \text{process node}$$
>
> | Process Node | $L_\text{min}$ | Order of Magnitude |
> |-------------|---------------|-------------------|
> | 180 nm | 180 nm | **100 nm** |
> | 130 nm | 130 nm | **100 nm** |
> | 65 nm | 65 nm | **100 nm** |
> | 28 nm | 28 nm | **10 nm** (cutting edge) |
>
> - **10 μm** is decades old (1970s–1980s era)
> - **1 μm** was typical in the 1990s
> - **100 nm** is the correct order for modern processes
>
> See: [[Lecture 5 - Fabrication and Layout#Layout Dimensions]]

---

## Question 4 (1 point)

### Transistor Layout

> [!question] The figure shown here illustrates a single transistor layout. The transistor is
> - [ ] an NMOS transistor
> - [x] **a PMOS transistor**
> - [ ] a bipolar transistor

> [!success] Answer: A PMOS transistor

> [!note]- Explanation
> The layout shows a **p-diffusion** active region, which means the source and drain are **p-type** doped. This identifies the transistor as **PMOS**:
>
> | Transistor | Source/Drain Type | Sits In |
> |-----------|------------------|---------|
> | **NMOS** | n+ diffusion | P-substrate |
> | **PMOS** | p+ diffusion | N-well |
>
> Key identification rule:
> - **p-diffusion** → p-type source/drain → **PMOS** (in N-well)
> - **n-diffusion** → n-type source/drain → **NMOS** (in P-substrate)
>
> See: [[Lecture 5 - Fabrication and Layout#Junction Implants]]

---

## Question 5 (1 point)

> [!question] For the transistor shown above the channel length $L$ is
> - [ ] $\lambda$
> - [x] **$2\lambda$**
> - [ ] $6\lambda$

> [!success] Answer: $L = 2\lambda$

> [!note]- Explanation
> The **channel length** $L$ is the dimension of the polysilicon gate in the direction of current flow (from source to drain).
>
> From the layout figure, the polysilicon gate strip is labeled as **$2\lambda$** wide. This width is the channel length:
>
> $$L = \text{poly width} = 2\lambda$$
>
> This is consistent with the minimum feature size:
> - $2\lambda = L_\text{min}$ = process node
> - The polysilicon gate defines the channel length through self-aligned processing
>
> See: [[Lecture 5 - Fabrication and Layout#Layout Dimensions]]

---

## Question 6 (1 point)

> [!question] For the transistor shown above the channel width $W$ is
> - [ ] $\lambda$
> - [x] **$2\lambda$**
> - [ ] $6\lambda$

> [!success] Answer: $W = 2\lambda$

> [!note]- Explanation
> The **channel width** $W$ is the dimension of the active region **perpendicular** to the direction of current flow (i.e., along the gate edge where it crosses the active region).
>
> From the layout, the active region extends $2\lambda$ in the direction perpendicular to current flow, making this a **minimum-size transistor**:
>
> $$W = L = 2\lambda$$
>
> | Parameter | Direction | Value |
> |-----------|-----------|-------|
> | $L$ (channel length) | Parallel to current flow | $2\lambda$ |
> | $W$ (channel width) | Perpendicular to current flow | $2\lambda$ |

---

## Question 7 (1 point)

> [!question] For the transistor shown above the area of the drain diffusion is
> - [x] **$4\lambda^2$**
> - [ ] $16\lambda^2$
> - [ ] $36\lambda^2$

> [!success] Answer: $A_D = 4\lambda^2$

> [!note]- Explanation
> The drain diffusion area is the area of the active region on the **drain side** of the polysilicon gate:
>
> $$A_D = W \times d_{\text{ext}}$$
>
> Where $d_{\text{ext}}$ is the drain extension from the poly gate edge to the end of the active region.
>
> From the layout:
> - $W = 2\lambda$ (from Q6)
> - $d_{\text{ext}} = 2\lambda$ (accommodates the $2\lambda \times 2\lambda$ contact hole)
>
> $$A_D = 2\lambda \times 2\lambda = \boxed{4\lambda^2}$$
>
> > [!tip] Why Drain Area Matters
> > The drain diffusion area directly determines the **junction capacitance** at the drain node:
> > $$C_j = C_{j0} \cdot A_D$$
> > Minimizing drain area reduces parasitic capacitance, which is why **multi-finger** layouts are used for wide transistors.
>
> See: [[Lecture 5 - Fabrication and Layout#Multi-Finger Transistors]]

---

## Question 8 (1 point)

> [!question] For a process using a p-type substrate the PMOS transistors are made in
> - [ ] the substrate
> - [x] **a N-WELL**
> - [ ] a P-WELL

> [!success] Answer: A N-WELL

> [!note]- Explanation
> In a **p-type substrate** CMOS process:
>
> | Transistor | Location | Reason |
> |-----------|----------|--------|
> | **NMOS** | Directly in P-substrate | N-type source/drain in P-type body ✓ |
> | **PMOS** | In **N-WELL** | P-type source/drain needs N-type body |
>
> PMOS transistors require an **n-type body** (bulk) to form the necessary PN junctions at the source and drain. Since the substrate is p-type, an **N-well** must be created to provide the n-type body for PMOS.
>
> > [!important] Remember
> > - **N-wells contain PMOS transistors**
> > - NMOS transistors sit directly in the P-substrate
> > - The N-well is created by doping with **Phosphorus** (donor, 5 valence electrons)
>
> See: [[Lecture 5 - Fabrication and Layout#Doping — Making the N-WELL]]

---

## Question 9 (1 point)

> [!question] One effect of splitting a transistor with a very wide $W/L$-ratio into more transistors connected in parallel is
> - [x] **to reduce the parasitic capacitance at drain and source**
> - [ ] to increase gm of the transistor
> - [ ] to reduce the gate-source capacitance, Cgs, of the transistor

> [!success] Answer: To reduce the parasitic capacitance at drain and source

> [!note]- Explanation
> When a wide transistor is split into **multiple parallel fingers**, adjacent fingers **share** their inner source/drain diffusions. This reduces the total drain and source junction areas:
>
> | Property | Single Finger | Multi-Finger |
> |----------|--------------|--------------|
> | Source area $A_S$ | Large | **Reduced** (shared diffusions) |
> | Drain area $A_D$ | Large | **Reduced** (shared diffusions) |
> | $g_m$ | $g_{m}$ | **Same** $g_m$ (same total $W/L$) |
> | $C_{gs}$ | $C_{gs}$ | **Same** $C_{gs}$ (same total $W \times L$) |
>
> **Why the other options are wrong:**
> - $g_m = \frac{2I_D}{V_{eff}}$ depends on total $W/L$, which is unchanged by splitting
> - $C_{gs} \propto W \times L \times C_{ox}$, which is also unchanged (total gate area is the same)
>
> The junction capacitance $C_j \propto A_{D/S}$ is reduced because shared diffusions eliminate redundant junction areas.
>
> See: [[Lecture 5 - Fabrication and Layout#Multi-Finger Transistors]]

---

## Question 10 (1 point)

> [!question] The design rules for a process is made by the foundry
> - [x] **to ensure that the wafer are produced with a high yield**
> - [ ] to ensure that optimal performance of circuits
> - [ ] to annoy you

> [!success] Answer: To ensure that the wafer are produced with a high yield

> [!note]- Explanation
> **Design rules** are geometric constraints on layout dimensions and spacings. They exist to accommodate **process variations** during fabrication:
>
> - Minimum widths → ensure features are reliably printed by photolithography
> - Minimum spacings → prevent shorts between adjacent features
> - Overlap rules → ensure proper alignment between layers despite registration errors
>
> | Purpose | Design Rules? | Performance Optimization? |
> |---------|:------------:|:------------------------:|
> | High manufacturing **yield** | ✅ Primary purpose | ❌ |
> | Optimal circuit **performance** | ❌ | Designer's responsibility |
>
> > [!important] Key Distinction
> > - **Design rules** → ensure the IC can be **manufactured** reliably (yield)
> > - **Circuit design** → ensure the IC **performs** well (designer's job)
> >
> > The foundry provides design rules; the designer is responsible for performance.
>
> See: [[Lecture 5 - Fabrication and Layout#Layout and Design Rules]]

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Key Concept |
> |---|--------|-------------|
> | 1 | Channel width and length | Designer-controlled layout parameters |
> | 2 | Polycrystalline silicon | Standard CMOS gate material |
> | 3 | 100 nm | Modern process node order of magnitude |
> | 4 | PMOS transistor | p-diffusion → p-type S/D → PMOS |
> | 5 | $L = 2\lambda$ | Poly gate width = channel length |
> | 6 | $W = 2\lambda$ | Active region extent ⊥ to current flow |
> | 7 | $4\lambda^2$ | $A_D = W \times d_\text{ext} = 2\lambda \times 2\lambda$ |
> | 8 | N-WELL | PMOS needs n-type body in p-substrate |
> | 9 | Reduce parasitic $C_{D/S}$ | Shared diffusions in multi-finger layout |
> | 10 | High yield | Design rules accommodate process variations |

---

## Key Concepts

> [!abstract] Fabrication & Layout Reference
> | Concept | Detail |
> |---------|--------|
> | Designer parameters | $W$ and $L$ only; process params are fixed |
> | Gate material | Polysilicon (poly) |
> | Process node | $2\lambda = L_\text{min}$ (modern: ~100 nm) |
> | PMOS location | In N-WELL (p-substrate process) |
> | NMOS location | Directly in P-substrate |
> | Channel length | Poly gate width (direction of current flow) |
> | Channel width | Active region extent (⊥ to current flow) |
> | Drain area | $A_D = W \times d_\text{ext}$ → determines $C_j$ |
> | Multi-finger benefit | Reduced $A_{D/S}$ → lower parasitic capacitance |
> | Design rules purpose | Manufacturing yield (not performance) |

---

> [!nav]
> [[Quiz 2 - OpAmp Building Blocks|← Quiz 2]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
