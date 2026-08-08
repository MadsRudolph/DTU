---
cssclass: dashboard
type: home
tags: [dashboard, home]
---
# DTU -- 5th Semester

> [!abstract] Autumn 2026 + January 2027
> **Programme:** Diplomingeniør, Electrical Engineering
> **Focus:** Electroacoustics, Acoustics & noise, Power electronics, PCB/EMC
> **Autumn total:** 25 ECTS (34870 + 62755 + 34840 + 34654)
> **January:** 34871 Nonlinear Transducers (5 ECTS, 3-week)
>
> [[DTU Study Path|Full study plan and career track]]

---

## Courses

> [!course-34870] 34870 -- Electroacoustics
> **Loudspeaker & microphone modelling, transducers, radiation**
> `10 ECTS` | E2
>
> [[34870 Electroacoustics|Open course page]]

> [!course-62755] 62755 -- Power Electronics
> **Converter design, switching, control (builds on 34620)**
> `5 ECTS` | E1A
>
> [[62755 Power Electronics|Open course page]]

> [!course-34840] 34840 -- Fundamentals of Acoustics and Noise Control
> **Sound fields, propagation, noise metrics & control**
> `5 ECTS` | E3A
>
> [[34840 Fundamentals of Acoustics and Noise Control|Open course page]]

> [!course-34654] 34654 -- Circuit Technology and EMC
> **PCB layout, grounding/shielding, EMC/EMI, lab project**
> `5 ECTS` | E4A (Tue 13--17)
>
> [[34654 Circuit Technology and EMC|Open course page]]

> [!course-34871] 34871 -- Nonlinear Transducers
> **Loudspeaker nonlinearity, distortion, compensation**
> `5 ECTS` | January 2027 (3-week intensive)
>
> [[34871 Nonlinear Transducers|Open course page]]

---

## Recent Activity

```dataview
TABLE course-name AS "Course", type AS "Type", file.mtime AS "Modified"
FROM "Courses"
WHERE type != "home"
SORT file.mtime DESC
LIMIT 10
```

---

## Upcoming Deadlines

> [!deadline] Key Dates
> - [ ] **34722 LCD1 re-exam** -- August 2026 (active prep: [[00 LCD1 — Exam Hub]])
> - [x] ~~Register for 5th term courses~~ -- done Aug 2026 (62999 dropped, 34840 added)
> - [ ] **34840 prerequisites self-study** -- before 1 September (complex numbers + signals)
> - [ ] **Autumn 2026 start** -- 1 September 2026
> - [ ] **January 2027 (34871)** -- 3-week period, Jan 2027

---

## Quick Navigation

> [!tip] Vault Areas
> - [[DTU Study Path]] -- Career planning and course strategy
> - **Archive/** -- Previous semester notes (DSP, Electromagnetics, IAE1, 4th sem)
> - **Projects/** -- Project workspace
> - **Resources/** -- General references

---

## All Notes by Course

```dataview
TABLE length(rows) AS "Notes"
FROM "Courses"
WHERE type != "home"
GROUP BY course-name
```
