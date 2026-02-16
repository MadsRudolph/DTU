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
> **Lecturers:** TBD
> **ECTS:** 5
> **Textbook:** TBD
> **Exam:** Written exam
> **Teaching:** TBD
> **Prerequisites:** 34636 Integrated Analog Electronics 1

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34655)
> - [[DTU Study Path#4.1 34655 -- Integrated Analog Electronics 2|Study path context]]

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| | | | *To be filled when schedule is available* | | |

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
> - [[31632-problems-intro.pdf|Problem set -- Introduction]]
> - [[31632-problems-avd-opamp.pdf|Problem set -- Advanced OpAmps]]

> [!tip] Quizzes
> - [[Quiz 1 - Two-Stage CMOS Opamp|Quiz 1 -- Two-Stage CMOS Opamp]]
> - [[Quiz 2 - OpAmp Building Blocks|Quiz 2 -- OpAmp Building Blocks]]

> [!tip] Solutions
> - [[31632-solution-intro.pdf|Solution -- Introduction problems]]

---

## Slides

- [[34655-01a-introduction-to-course_v1.pdf|01a -- Introduction to Course]]
- [[34655-01b-introduction-prerequisites_v1.pdf|01b -- Introduction Prerequisites]]
- [[34655-advanced-opamps_v4.pdf|Advanced OpAmps]]

---

## Literature & Resources

*To be added as course materials become available.*

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

---

## Quick Reference

> [!tip] Two-Stage CMOS Opamp Essentials
> - **Miller capacitor** between input and output of 2nd stage
> - Creates dominant pole (pole splitting)
> - RHP zero at $\omega_z = g_{m2}/C_C$ -- needs nulling resistor
> - Phase margin target: 60 degrees minimum
