---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: home
cssclass: course-home
tags: [IAE2, home]
---
# 34655 Integrated Analog Electronics 2

> [!info] Course Information
> **Course:** 34655 Integrated Analog Electronics 2
> **Semester:** Spring 2026 (4th semester)
> **Lecturers:** Per Barner Lynggaard (plyn@dtu.dk), Christian (exercises)
> **ECTS:** 5
> **Textbook:** T.C. Carusone, D. Johns & K. Martin, *Analog Integrated Circuit Design* + Erik Bruun, *CMOS Analog IC Design: Fundamentals* & *Problems and Solutions*
> **Exam:** No formal exam -- continuous assessment (7-step scale, internal examiner)
> **Grading:** Report on OpAmp paper design (~33%), Poster (~33%), Quizzes (~34%)
> **Teaching:** Tuesdays 13:00-17:00 (Lectures 13-15, Exercises 15-17), B421 A071
> **Schedule:** Spring F4A
> **Prerequisites:** 34630, 31631, 31606 (Knowledge of MOS transistor models and basic CMOS amplifier circuits)

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34655)
> - [[DTU Study Path#4.1 34655 -- Integrated Analog Electronics 2|Study path context]]

---

## Roadmap

![[34655.png]]

| Wk  | Date  | Lec | Topic                                                    | Reading                                    | Deliverables                       | Done  |
| --- | ----- | --- | -------------------------------------------------------- | ------------------------------------------ | ---------------------------------- | ----- |
| 6   | 03-02 | 1   | Introduction, pre-requisites                             | Carusone: Ch. 1, Bruun: Entire book        | Quiz 01                            | - [x] |
| 7   | 10-02 | 2   | Advanced OpAmps (Two-stage Miller OTA, Folded Cascode, Current Mirror OTA, Full Diff. + CMFB) | Carusone: Ch. 6.3                          | Quiz 02                            | - [x] |
| 8   | 17-02 | 3   | Group work: OpAmp paper design (theory)                  | Carusone: Ch. 5, 6.1-6.2, Bruun: Ch. 6-7  |                                    | - [x] |
| 9   | 24-02 | 4   | Noise (Time/Freq Domain, White/Pink, Sources, Circuits)  | Carusone: Ch. 3                            | **Report (27-02)**, Quiz 04        | - [ ] |
| 10  | 03-03 | 5   | Layout (Fabrication, Junction Cap, Layout Rules, Matching) | Carusone: Ch. 2                            | Quiz 05                            | - [ ] |
| 11  | 10-03 | 6   | Computer Exercise (Cadence)                              | Carusone: Ch. 5, 6.1-6.2                   |                                    | - [ ] |
| 12  | 17-03 | 7   | Computer Exercise (Cadence)                              | Carusone: Ch. 5, 6.1-6.2                   |                                    | - [ ] |
| 13  | 24-03 | 8   | Computer Exercise (Cadence)                              | Carusone: Ch. 5, 6.1-6.2                   |                                    | - [ ] |
| 14  |       |     | *Påskeferie*                                             |                                            |                                    |       |
| 15  | 07-04 | 9   | Data converters fundamentals (ADC/DAC, Nyquist converters) | Carusone: Ch. 15                           | Quiz 06                            | - [ ] |
| 16  | 14-04 | 10  | DTU Chip Day / Poster presentation                       |                                            | **Poster (10-04)**                 | - [ ] |

---

## Deliverables

> [!warning] Upcoming: Report due 27 Feb 2026
> Paper design of two-stage CMOS opamp. Worth ~33% of grade.

| Deliverable | Weight | Deadline | Status | Link |
|-------------|--------|----------|--------|------|
| Report -- OpAmp Paper Design | ~33% | 27-02-2026 | In progress | [[Cadence Exercise - Two-Stage OpAmp Design\|Design notes]], Overleaf repo |
| Poster -- OpAmp | ~33% | 10-04-2026 | Not started | |
| Quizzes (6 total) | ~34% | Throughout | 2/6 done | [[Quiz 1 - Two-Stage CMOS Opamp\|Q1]], [[Quiz 2 - OpAmp Building Blocks\|Q2]] |

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> Advanced analog IC design for audio applications:
> - Multi-stage CMOS opamp design and compensation
> - Gain stages for preamps and active crossovers
> - Frequency compensation and stability analysis
> - Data converters (ADC/DAC) for audio interfaces

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34655 Integrated Analog Electronics 2/Notes"
WHERE type = "lecture-note"
SORT week ASC
```

> [!tip] Notes
> - [[Lecture 1 - Introduction and Prerequisites|Lecture 1 -- Introduction and Prerequisites]]
> - [[Advanced OpAmps - Lecture Notes|Advanced OpAmps]]
> - [[Course Recap - Understanding Analog IC Design|Course Recap -- Analog IC Design]]

---

## Exercises & Quizzes

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34655 Integrated Analog Electronics 2/Exercises"
WHERE type = "exercise" OR type = "quiz"
SORT date ASC
```

> [!tip] Exercises
> - [[Problem 1 - Amplifier Configurations|Problem 1 -- CS, Cascode, Cascade comparison]]
> - [[Problem 2 - Advanced OpAmps|Problem 2 -- Advanced OpAmps]]
> - [[Cadence Exercise - Two-Stage OpAmp Design|Cadence Exercise -- Two-Stage OpAmp Paper Design]]
> - [[31632-problems-intro.pdf|Problem set -- Introduction]]
> - [[31632-problems-avd-opamp.pdf|Problem set -- Advanced OpAmps]]

> [!tip] Quizzes
> - [[Quiz 1 - Two-Stage CMOS Opamp|Quiz 1 -- Two-Stage CMOS Opamp]]
> - [[Quiz 2 - OpAmp Building Blocks|Quiz 2 -- OpAmp Building Blocks]]

> [!tip] Solutions
> - [[31632-solution-intro.pdf|Solution -- Introduction problems]]
> - [[31632-solutions-avd-opamp.pdf|Solution -- ADV Opamps]]

---

## Slides

- [[34655-01a-introduction-to-course_v1.pdf|01a -- Introduction to Course]]
- [[34655-01b-introduction-prerequisites_v1.pdf|01b -- Introduction Prerequisites]]
- [[34655-advanced-opamps_v4.pdf|Advanced OpAmps]]

---

## Literature & Resources

> [!tip] Course Textbooks (click to open PDF)
> - [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf|Carusone -- Analog Integrated Circuit Design]] ([Polyteknisk Boghandel](https://www.polyteknisk.dk/home/dtu/detailed_view/1111118379455))
> - [[cmos_analog_ic_design_fundamentals.pdf|Bruun -- CMOS Analog IC Design: Fundamentals]] ([Free - Bookboon](https://bookboon.com/da/cmos-analog-ic-design-fundamentals-ebook))
> - [[cmos_analog_ic_design_problems_and_solutions.pdf|Bruun -- CMOS Analog IC Design: Problems and Solutions]] ([Free - Bookboon](https://bookboon.com/da/cmos-analog-ic-design-problems-and-solutions-ebook))

> [!tip] Key Chapters for Report
> - [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=266|Carusone Ch. 6.1 -- Two-Stage CMOS Opamp]]
> - [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=278|Carusone Ch. 6.2 -- Opamp Compensation]]
> - [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=228|Carusone Ch. 5 -- Feedback Amplifiers]]
> - [[cmos_analog_ic_design_fundamentals.pdf#page=258|Bruun Ch. 7 -- The Two-Stage Opamp]]
> - [[cmos_analog_ic_design_fundamentals.pdf#page=202|Bruun Ch. 6 -- Feedback]]
> - [[T.C. Carusone, D. Johns & K. Martin, Analog Integrated Circuit Design.pdf#page=53|Carusone Table 1.5 -- 0.18 μm CMOS Parameters (p. 53)]]

> [!tip] Simulation Tools
> - **Cadence Virtuoso** -- IC design, schematic + simulation (X-FAB 0.18 μm CMOS process)
> - **ngspice + PySpice** -- SPICE verification of paper design (files in `SPICEPilot/examples/3_34655_opamp/`)
> - [[LT_Spice_notest.pdf|LTSpice notes]]
> - [[cmos-integrated-circuit-simulation-with-ltpice (1).pdf|CMOS IC Simulation with LTSpice]]

---

## Formulas

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | CS Gain | $A_v = -g_m \cdot r_{ds}$ |
> | Cascode $r_{out}$ | $r_{out} \approx g_{m2} \cdot r_{ds1} \cdot r_{ds2}$ |
> | Bandwidth | $f_{3dB} = \frac{1}{2\pi r_{out} C_L}$ |
> | GBW (single stage) | $GBW = \frac{g_m}{2\pi C_L}$ |
> | Slew Rate | $SR = \frac{I_{SS}}{C_C}$ |
> | GBW (two-stage) | $GBW = \frac{g_{m1}}{2\pi C_C}$ |
> | Closed-loop BW | $BW_{CL} = \beta \cdot GBW$ |
> | Feedback factor | $\beta = \frac{C_B}{C_A + C_B}$ |
> | Phase margin | $PM = 90° - \arctan(\omega_t/\omega_{p2}) - \arctan(\omega_t/\omega_z)$ |

---

## Quick Reference

> [!tip] Two-Stage CMOS Opamp Essentials
> - **Miller capacitor** between input and output of 2nd stage
> - Creates dominant pole (pole splitting)
> - RHP zero at $\omega_z = g_{m2}/C_C$ -- needs nulling resistor $R_c = 1/g_{m7}$
> - Phase margin target: 70° for this exercise (60° minimum in general)
> - See [[Cadence Exercise - Two-Stage OpAmp Design|full design walkthrough]] for the complete 10-step procedure
