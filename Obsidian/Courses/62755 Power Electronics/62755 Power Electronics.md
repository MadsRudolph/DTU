---
course: "62755"
course-name: "Power Electronics"
type: home
cssclass: course-home
tags: [PE, PowerElectronics, home]
---
# 62755 Power Electronics

> [!info] Course Information
> **Official title:** Power Electronics (*Effektelektronik*)
> **Semester:** Autumn 2026 (5th semester), 13 weeks · **5 ECTS**
> **Placement:** E1A — **Mon 8–12**, Campus **Ballerup**
> **Lecturer:** Ashraf Fathi Khalil Sulayman (`ashka@dtu.dk`), Ballerup — *same lecturer as 62768 Electrical Energy Systems*
> **Department:** 62 — Engineering Technology and Didactics
> **Exam:** **Written, 4 hours** + assessment of reports
> **Aids:** All aids, **no internet access** · 7-step scale, **internal** assessment
> **Teaching:** Lectures, problem solving, exercises, company visits, group work / simulations
> **Prerequisites:** 62760 *or* 34601 / **34722** / 62752 — may be taken concurrently
> **Replaces:** 62816

> [!bug] Exam placement conflict — check this in week 1
> The [DTU course page](https://kurser.dtu.dk/course/62755) (updated 16 Apr 2026) says exam placement **E1A**. Slide 8 of `Slides/Lecture 1 Introduction.pdf` says **E2B**.
> That matters: [[34870 Electroacoustics|34870]]'s oral exam is **E2-A/B on 9–10 December**. If 62755 really sits in E2B, the two collide.
> **Action:** confirm with Ashraf at the first lecture, then fix this note.

> [!warning] Campus split — Monday is a Ballerup → Lyngby day
> 62755 runs **Mon 8–12 in Ballerup**; [[34870 Electroacoustics|34870]] runs **Mon 13:00–17:00 in Lyngby** (first lecture 31 Aug). Every Monday this term needs a Ballerup→Lyngby transfer over lunch. Plan the commute before week 1.

> [!success] 34722 LCD1 feeds straight into this
> DTU lists [[34722 Linear Control Design 1|34722]] as one of the valid prerequisite paths. The small-signal converter models and control loops here are Bode plots, phase margin and PI/lead design applied to switching converters — the re-exam material, reused.

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/62755)
> - [[DTU Study Path#🔊 5th Term — Autumn 2026 + January 2027 (25 + 5 ECTS)|Study path context]]
> - Working folder: `5. Semester/Power Electronics/` (PSCAD, Simulink, Matlab, C2000, Labs)

---

## Course Plan

> [!note] Source
> Slide 9 of `Slides/Lecture 1 Introduction.pdf`. Weeks are relative — no calendar dates given yet.

| Wk  | Topic                    | Slides                                                  | Assignment | Lab       | Done |
| --- | ------------------------ | ------------------------------------------------------- | ---------- | --------- | ---- |
| 1   | Introduction             | `Lecture 1 Introduction.pdf`                            |            | **Lab 1** |      |
| 2   | Diode and diode circuits | `Lecture 2 Power diodes.pdf`                            | **A1**     |           |      |
| 3   | Diode rectifier          | `Lecture 3 Diode Rectifier.pdf`                         | **A2**     | **Lab 2** |      |
| 4   | Power transistors        | `Lecture 4 Power Transistors.pdf`                       |            |           |      |
| 5   | DC/DC converters         | `Lecture 5 DC-DC Converters.pdf`                        |            | **Lab 3** |      |
| 6   | DC/DC converters         | `Lecture 5 DC-DC Converters.pdf`                        | **A3**     | **Lab 4** |      |
| 7   | Inverters                | `Lecture 6 Inverters.pdf`                               |            | **Lab 5** |      |
| 8   | Inverters                | `Lecture 6 Inverters.pdf`                               |            |           |      |
| 9   | Multilevel inverters     | —                                                       | **A4**     |           |      |
| 10  | Thyristors               | `Lecture 7 Thyristors and Thyristorized Converters.pdf` |            |           |      |
| 11  | Controlled rectifiers    | `Lecture 7 …`                                           |            |           |      |
| 12  | AC voltage controllers   | —                                                       |            |           |      |

> [!note] Slides for weeks 9 and 12 not handed out yet
> Lectures 1–7 are in `Slides/`. Multilevel inverters (wk 9) and AC voltage controllers (wk 12) have no deck yet — check DTU Learn as the term progresses.

---

## Lab Exercises

| # | Lab | Done |
|---|---|---|
| **1** | Single-switch with low-side drive for a DC motor | |
| **2** | Single-phase rectifier: resistive and inductive loads (DC motor) | |
| **3** | Characteristics of a MOSFET | |
| **4** | Open-loop characteristics of buck, boost and buck-boost converters | |
| **5** | Feedback control of buck and boost converters | |

> [!abstract] The course's own learning arc
> Every topic runs through four stages: **concept of operation → analysis → simulation → practical implementation**. The labs are the last stage.

> [!success] Lab 4 and 5 are 62768 territory
> You already built discrete buck and boost converters in [[62768 Electrical Energy Systems|62768]] last semester. Labs 4–5 are those same converters, now measured open-loop and then closed with a feedback controller. Old Simulink models are in `4. Semester/Electrical Energy Systems/DC-DC Converters/`.

---

## Course Content

> [!abstract] What the course actually covers
> - **Introduction:** applications, types of power semiconductors, types of converters
> - **Power devices:** diodes, silicon-controlled rectifiers, power BJTs, power MOSFETs, IGBTs, thyristors, DIAC, TRIAC, static induction devices — static *and* dynamic characteristics, power modules
> - **DC–DC converters:** buck, boost, buck-boost, bidirectional, isolated — steady-state and transient behaviour, **small-signal models**, control, applications
> - **Rectifiers:** 1-phase and 3-phase, controlled and uncontrolled — steady-state/transient, small-signal, control
> - **DC–AC inverters:** 1- and 3-phase bridge inverters, modulation techniques, voltage-source vs. current-source inverters, voltage & frequency control
> - **AC–AC converters:** steady-state, transient, small-signal, control

> [!example] Tools
> - Simulation and analysis in **Matlab/Simulink** (the course page also names **PSCAD**; Lecture 1 mentions only Matlab — confirm which is actually used)
> - Practical implementation on a **Texas Instruments C2000** microcontroller, programmed from Matlab/Simulink → `5. Semester/Power Electronics/C2000/`

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> Builds on [[34620 Basic Power Electronics|34620]]:
> - Converter design, switching behaviour, control
> - Directly applicable to **class-D output stages** and **SMPS rails** for audio gear
> - Pairs with [[34654 Circuit Technology and EMC|34654]] for proper switch-mode board design

> [!note] Continuity from 4th semester
> Same lecturer as **62768 Electrical Energy Systems** — the buck/boost converters you built with discrete components there are the starting point here, now with proper small-signal models and digital control on top.

---

## Literature

> [!quote] Reading list
> - Muhammad H. Rashid — *Power Electronics: Devices, Circuits, and Applications*, 4th ed., Pearson (2014)

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/62755 Power Electronics/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Labs

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/62755 Power Electronics"
WHERE type = "exercise" OR type = "lab" OR type = "quiz"
SORT date ASC
```
