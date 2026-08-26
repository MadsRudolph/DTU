---
course: "34871"
course-name: "Nonlinear Transducers"
type: home
cssclass: course-home
tags: [Transducers, Audio, home]
---
# 34871 Nonlinear Transducers

> [!info] Course Information
> **Official title:** Nonlinear transducers (*Ulineære transducere*)
> **Semester:** **January 2027** — 3-week intensive, Campus **Lyngby**
> **Placement:** January block · **5 ECTS**
> **Lecturer:** Finn T. Agerkvist (`ftag@dtu.dk`, B352, 4525 3941) — also runs [[34840 Fundamentals of Acoustics and Noise Control|34840]]
> **Department:** 34 — Electrical and Photonics Engineering
> **Exam:** **Oral** + assessment of reports, on the **last day(s) of the 3-week period**
> **Aids:** **No aids** · 7-step scale, **external** censor
> **Teaching:** Lectures + mandatory laboratory and simulation exercises
> **Prerequisites:** **34870** / 31220
> **Replaces:** 31221 (also point-blocking)

> [!warning] No aids at the exam
> Unlike everything else this year, 34871 allows **nothing** in the exam room — no formula sheet, no notes. Plan for memorised derivations, the way the [[34722 Linear Control Design 1|34722]] oral went.

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34871)
> - [[DTU Study Path#5.3 34871 – Nonlinear Transducers (5 ECTS, January 2027, 3-week intensive)|Study path context]]
> - Working folder: `5. Semester/Nonlinear Transducers/` (Matlab, Simulations, Labs)

---

## Roadmap

| Day | Date | Topic | Lab / Sim | Done |
|---|---|---|---|---|
| | | | *To be filled when the January schedule lands* | |

> [!note] Timing
> 3-week intensive block, Mon–Fri. The autumn→January ordering is deliberate: [[34870 Electroacoustics|34870]] finishes with its oral on 9–10 December, and 34871 picks the same models straight back up in January.

---

## Course Content

> [!abstract] What the course actually covers
> - The basic difference between **linear and nonlinear systems**
> - The dominant nonlinearities in **electrodynamic loudspeakers**, and predicting how a given nonlinearity affects cone motion
> - Loudspeaker behaviour in the nonlinear domain — **harmonic spectrum** and **DC offset** of the rest position
> - Techniques for modelling physical systems in **discrete time**
> - Measuring and computing the common **distortion measures**
> - Basic methods for **identifying model parameters**
> - **Numerical methods** for solving nonlinear differential equations
> - Principles of **nonlinear compensation** of distortion

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> Deep dive into **nonlinear behaviour of loudspeakers and transducers**:
> - Distortion mechanisms & measures
> - Nonlinear loudspeaker components, numerical solvers
> - Parameter identification & compensation methods
>
> Completes the loudspeaker track started in [[34870 Electroacoustics]] — from small-signal models to **real-world distortion** and limits.

> [!success] Track Payoff
> Used directly in hi-fi/studio-monitor design, headphones, and hearing-aid transducers. With 34870 + 34840 in the autumn, this closes a full year of acoustics.

> [!tip] Grøn Dyst eligible
> This course allows preparing a project for DTU's sustainability/environment student conference.

---

## Literature & Resources

*To be added when the course opens in January 2027.*

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34871 Nonlinear Transducers/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Labs

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34871 Nonlinear Transducers"
WHERE type = "exercise" OR type = "lab" OR type = "quiz"
SORT date ASC
```
