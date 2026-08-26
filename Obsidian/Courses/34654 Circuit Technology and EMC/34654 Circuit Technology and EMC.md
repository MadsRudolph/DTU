---
course: "34654"
course-name: "Circuit Technology and EMC"
type: home
cssclass: course-home
tags: [EMC, PCB, home]
---
# 34654 Circuit Technology and EMC

> [!info] Course Information
> **Official title:** Circuit technology and EMC (*Kredsløbsteknologi og EMC*)
> **Semester:** Autumn 2026 (5th semester), 13 weeks · **5 ECTS**
> **Placement:** E4A — **Tue 13:00–17:00**, Campus Lyngby
> **First lecture:** **Tuesday 1 September, 13:00 — building 341, room 023**
> **Lecturers:** Arnold Knott (`knott@dtu.dk`, 4525 3490) — responsible
> · Ziwei Ouyang (`ziou@dtu.dk`) · Tiberiu-Gabriel Zsurzsan (`tgzsur@dtu.dk`, B325)
> **Department:** 34 — Electrical and Photonics Engineering
> **Exam:** **No exam.** Assessment of reports — **4 assignments**, one report each, group work.
> **Aids:** All aids **including internet** — anything legal goes
> **Grading:** **Pass / not pass**, internal assessment. **At least 3 of the 4 reports must pass.**
> **Teaching:** Flipped classroom, class teaching, project and lab work — roughly **half the course time** is reserved for the group work behind the 4 hand-ins
> **Prerequisites:** Basic electronics — Ohm, Kirchhoff, Fourier, Laplace, components, electromagnetism, analog and/or digital circuits
> **Replaces:** 31354, 31024 (point-blocks 31495, 31024, 31355, 31354)

> [!todo] Before the first lecture (Tue 1 Sep)
> - [ ] **Complete the opening quiz** on DTU Learn — knowledge refresher + questions about how you study
> - [ ] **Join the course Discord** — used for finding team-mates and questions
>       *("you never disturb, you always contribute!" — Arnold)*
> - [ ] **Sign up for a group in DTU Learn** — ideally **groups of 5**
> - [ ] Note: the first lecture opens with ~15 min **guided meditation** — optional, you can wait outside and be invited in afterwards

> [!warning] Group deadline: 8 September, 14:00
> If you have not signed up for a group by **14:00 during the second lecture (8 September)**, DTU Learn **assigns you automatically**. Pick your own group before then.

> [!warning] The only pass/fail course this term
> No exam, no 7-step grade — but **3 of 4 reports must pass**, and group work can land **outside the scheduled Tue 13–17 slot** (groups organise that themselves). The risk here is scheduling, not difficulty.

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34654)
> - [[DTU Study Path#5.1 34654 – Circuit Technology and EMC (5 ECTS, autumn, E4A)|Study path context]]
> - Working folder: `5. Semester/Circuit Technology and EMC/` (KiCad, LTspice, one folder per assignment)

---

## The Four Assignments

> [!note] Briefs are in `Projects/`
> All four assignment PDFs live in `Projects/`; the PCB reference schematics and the TI EVM user guide are in `Literature/Reference Designs/`.

| # | Assignment | Brief | Working folder | Done |
|---|---|---|---|---|
| 1 | **Passives** — components & filter | `Projects/Assignment 1 - Passives.pdf` | `Assignment 1 - Passives/` | |
| 2 | **PCB** — schematic → layout → cross-review | `Projects/Assignment 2 - PCB.pdf` | `Assignment 2 - PCB/` | |
| 3 | **EMC** — input filter for conducted emission | `Projects/Assignment 3 - EMC.pdf` | `Assignment 3 - EMC/` | |
| 4 | **Environmental** — temperature chamber | `Projects/Assignment 4 - Environmental.pdf` | `Assignment 4 - Environmental/` | |

> [!important] They chain together
> Assignment 1 gives you a characterised **capacitor and inductor**. Assignment 3 has you **build a filter**. Assignment 4 then lets you put *either* of those into the temperature chamber. Choosing well in 1 and 3 makes 4 much easier.

---

### 1 — Passives

> [!abstract] Parts 1 & 2 — reverse-engineer a datasheet (hands-on)
> A pile of "homeless" capacitors and inductors with no datasheets. Each group picks **one capacitor and one inductor** and writes a **1-page datasheet** for each, containing at minimum:
> 1. A picture of the component
> 2. Capacitance / inductance
> 3. Small-signal **impedance vs. frequency** (amplitude *and* phase)
> 4. Block diagram of the test setup — including equipment model numbers and settings (e.g. signal level)
> 5. Equivalent circuit with **quantified values**, modelling at least the first resonance
> 6. **Q-value / damping factor / tan δ**
> 7. For the inductor: derive the **thermal resistance** — apply different DC currents, compute losses from the equivalent circuit

> [!abstract] Part 4 — π-filter with parasitics
> Plot $V(C_2)/V_1$ (log-log, amplitude & phase) from **10 kHz to 100 MHz**, then add parasitics **one at a time**, each plotted against the previous:
> | | Parasitic | Added to |
> |---|---|---|
> | a | $R_s = 0.4\ \Omega$ | C1 |
> | b | $L_s = 7\ \text{nH}$ | C1 |
> | c | $R_p = 17.3\ \text{k}\Omega$ | L1 |
> | d | $C_p = 16.2\ \text{pF}$ | L1 |
> | e | $R_s = 0.4\ \Omega$ | C2 |
> | f | $L_s = 7\ \text{nH}$ | C2 |
>
> → **7 Bode plots** total, one sentence of comment each, **max 2 slides**.

> [!quote] Arnold's hand-in rules (all four assignments)
> **KISS** — keep it simple. **No novels** — presentation style, stick to the facts, answer the question asked. **Graphs** — big, clear, quantified axes. **Diagrams** — clear and visible. **Share the workload.**

---

### 2 — PCB

> [!abstract] The flow
> `Schematic → Layout → BOM → PCB order`, with a **design review** and a **layout review** built in.
> Two teams work in parallel and **cross-check each other**: Team A and Team B each do schematic capture → layout checklist → PCB layout, then **check the other team's PCB** and give feedback.

> [!example] Choose one of two schematics
> - **Option A — Microcontroller** → `Literature/Reference Designs/PCB option A - Microcontroller (schematic).pdf` (ATmega328-class design)
> - **Option B — Power Supply** → `Literature/Reference Designs/PCB option B - Power Supply flyback (schematic).pdf` (flyback, 2 pages)

> [!deadline] Two deadlines
> 1. **Hand-over** — pass your schematic + constraints to the other team
> 2. **Learning reflections** — written reflection after the review lecture

> [!tip] You already own this toolchain
> The [[62768 Electrical Energy Systems|62768]] KiCad → mill → laser-silkscreen pipeline transfers directly. See the `kicad-schematic` and `kicad-laser-pcb` skills. Work in `5. Semester/Circuit Technology and EMC/KiCad/`.

> [!warning] Learning reflections go into a form
> Write the equations in **plain text**, not LaTeX — the DTU reflection forms do not render `$...$`.

---

### 3 — EMC

> [!abstract] The task
> Design and build an **input filter** that makes a buck converter meet the conducted-emission limits of **EN 55022**.
>
> | Parameter | Value |
> |---|---|
> | Hardware | TI **TPS40200EVM-001** evaluation module |
> | Input | 12 V DC |
> | Output | 3.3 V DC |
> | Load | 1.65 Ω |
> | Switching frequency | 300 kHz |
>
> → EVM user guide: `Literature/Reference Designs/TPS40200EVM-001 - TI buck EVM user guide.pdf`

> [!abstract] Steps
> 1. **Calculate** the disturbance voltage at the LISN for the fundamental and the first 6–7 harmonics (pen & paper, LTspice, whatever)
> 2. **Measure** the actual voltage with the EMI receiver — table of the fundamental + first 7 harmonics + the last 5 harmonics below 30 MHz
> 3. **Design** the smallest/cheapest filter that gets you under EN 55022
> 4. **Measure** the filter response on the network analyzer
> 5. **Reconnect** the filter to the converter and repeat the EMI-receiver measurement
> 6. **Present** — max 2 slides per bullet + 1 title slide = **max 11 slides**, pitched as if to a customer

> [!info] Where the equipment lives
> - **EMC chamber + LISN + EMI receiver:** building **325, room 261**
> - **Network analyzer / oscilloscopes:** **329A-020**
> - Intro video to the EMC equipment: https://youtu.be/fiSCyV1R1Fw

---

### 4 — Environmental

> [!abstract] Temperature-chamber measurements
> Pick a **device under test**: the capacitor *and* inductor from assignment 1, **or** the filter you built for assignment 3, **or** any other circuit of yours.
>
> ⚠️ **The DUT may be destroyed** — do not use anything you care about.
>
> 1. Find datasheet/manual info and extract the **minimum and maximum thermal ratings**
> 2. Set the DUT up in the temperature chamber (building **325, room 261** — the EMC room). Place it on the wood, run wires through the openings, add the insulation.
> 3. Measure relevant parameters across temperature — impedance, transfer function, drain current, rise/fall times, jitter — using the **Bode100** impedance / gain-phase analyzer outside the chamber (plus a scope for active DUTs).

---

## Course Content

> [!abstract] Component knowledge
> - Choosing components for a given application against electrical, thermal, mechanical, environmental and manufacturing requirements
> - **Resistors:** types, materials, packages, drift, noise, derating
> - **Capacitors:** dielectrics, parasitic model; plastic/paper, ceramic Class I/II/III, electrolytic; derating
> - **Inductors:** models with parasitics
> - Extracting **parasitics from datasheets** for resistors, capacitors, inductors and PCB traces

> [!abstract] PCB technique
> - PCB materials and their properties
> - Trace dimensioning: voltage drop, max temperature rise, short-circuit behaviour, clearances
> - The steps of an industrial PCB production process

> [!abstract] EMC
> - EMC phenomena and basic definitions
> - Noise sources and **coupling mechanisms**
> - EMC components · filtering · shielding · mechanical design · **grounding principles**
> - PCB design for EMC
> - The **EMC Directive** and standards; EMC test procedures; practical troubleshooting
> - Identifying noise sources and computing total output noise

> [!abstract] Thermal
> - Conduction, convection, radiation
> - Heatsink dimensioning, max junction temperature
> - Heat capacity and **equivalent thermal circuits in SPICE**
> - Circuit drift as a function of time and temperature

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> The **PCB layout + EMC** course brought forward from the original 7th-term plan:
> - Grounding, shielding, routing for low noise
> - EMC/EMI compliance thinking
> - Flipped classroom + 4 assignments + lab/PCB project
>
> Very relevant for:
> - Low-noise analog boards (pre-amps, phono stages)
> - Layout of high-$dV/dt$, high-$dI/dt$ class-D stages
> - Keeping your amp from radiating like a radio transmitter

> [!note] Covers much of 34374
> Scratches a large part of the **34374 IoT Hardware and PCB Design** itch a term early (34374 itself is a spring course that didn't fit the Diplom plan — kept as MSc target).

> [!success] Pairs with 62755
> Component parasitics, grounding and thermal design are exactly what [[62755 Power Electronics|62755]]'s switching converters need — and assignment 3 *is* a buck converter. Take the two together and class-D board design gets serious.

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34654 Circuit Technology and EMC/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Assignments

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34654 Circuit Technology and EMC"
WHERE type = "exercise" OR type = "assignment" OR type = "project"
SORT date ASC
```
