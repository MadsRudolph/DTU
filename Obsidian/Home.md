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
> **Term starts:** Monday **31 August 2026**
>
> [[DTU Study Path|Full study plan and career track]]

---

## Weekly Timetable — Autumn 2026

| | Morning | Afternoon |
|---|---|---|
| **Mon** | **62755** Power Electronics · 8–12 · 🚉 *Ballerup* | **34870** Electroacoustics · 13–17 · *Lyngby b.352 r.019* |
| **Tue** | **34840** Acoustics & Noise · 8–12 · *Lyngby b.358 r.063* | **34654** Circuit Tech & EMC · 13–17 · *Lyngby* |
| **Wed** | — | — |
| **Thu** | **34870** Electroacoustics · 8:30–12 · *Lyngby* | — |
| **Fri** | — | — |

> [!warning] Monday is a two-campus day
> 62755 is in **Ballerup** (8–12), 34870 is in **Lyngby** (13–17). Every Monday needs a campus transfer over lunch — sort the commute before week 1.

> [!tip] Wednesdays and Fridays are free
> That is where the 34654 group work, the 34870 labs and the loudspeaker project have to live. 34654 explicitly schedules group work outside the timetable.

---

## Courses

> [!course-34870] 34870 -- Electroacoustics
> **Loudspeaker & microphone modelling, transducers, radiation**
> `10 ECTS` | E2 | Oral exam **9--10 Dec**
>
> [[34870 Electroacoustics|Open course page]]

> [!course-62755] 62755 -- Power Electronics
> **Converter design, switching, control (builds on 34620)**
> `5 ECTS` | E1A | Written exam, 4 h
>
> [[62755 Power Electronics|Open course page]]

> [!course-34840] 34840 -- Fundamentals of Acoustics and Noise Control
> **Sound fields, propagation, noise metrics & control**
> `5 ECTS` | E3A | Written exam **11 Dec**
>
> [[34840 Fundamentals of Acoustics and Noise Control|Open course page]]

> [!course-34654] 34654 -- Circuit Technology and EMC
> **PCB layout, grounding/shielding, EMC/EMI, lab project**
> `5 ECTS` | E4A | **No exam** -- 4 reports, pass/fail
>
> [[34654 Circuit Technology and EMC|Open course page]]

> [!course-34871] 34871 -- Nonlinear Transducers
> **Loudspeaker nonlinearity, distortion, compensation**
> `5 ECTS` | January 2027 (3-week intensive) | Oral, no aids
>
> [[34871 Nonlinear Transducers|Open course page]]

---

## Key Dates

> [!deadline] Semester start
> - [ ] **Before Tue 1 Sep** — 34654 **opening quiz** on DTU Learn + join the course **Discord**
> - [ ] **Mon 31 Aug, 13:00** — 34870 first lecture, b.352 room 019 · *install LTspice first*
> - [ ] **Mon 31 Aug, 08:00** — 62755 first lecture, Ballerup *(time assumed from E1A — confirm)*
> - [ ] **Tue 1 Sep, 08:00** — 34840 first lecture, b.358 room 063
> - [ ] **Tue 1 Sep, 13:00** — 34654 first lecture, b.341 room 023 *(opens with ~15 min optional meditation)*
> - [ ] **Tue 8 Sep, 14:00** — ⚠️ 34654 **group sign-up deadline** (groups of 5) — after this DTU Learn auto-assigns
> - [ ] **Week 1** — find a **group of 3** for the 34870 labs + loudspeaker project

> [!deadline] Autumn deadlines
> - [ ] **20 Sep** — 34870 Lab A quiz (LTspice analogy circuits)
> - [ ] **28 Sep** — 34840 problem set released
> - [ ] **5 Oct** — 34870 Labs B/C quiz (mic measurement + calibration)
> - [ ] **9 Oct** — 34840 problem set due *(individual hand-in)*
> - [ ] **26 Oct** — 34870 Labs D/E quiz (enclosures + response)
> - [ ] **27 Oct – 17 Nov** — 34840 lab exercise window (report due 2 weeks after)
> - [ ] **30 Nov** — 34870 loudspeaker project quiz
> - [ ] **3 Dec** — 34870 project presentations & demos

> [!deadline] Exams
> - [ ] **9–10 Dec** — 34870 **oral** (30 min, written aids allowed)
> - [ ] **11 Dec** — 34840 **written** (4 h, all aids, no internet)
> - [ ] **TBC** — 62755 written (4 h) — *placement conflict E1A vs E2B, confirm week 1*
> - [ ] **January 2027** — 34871, 3-week block, oral with **no aids**

> [!success] Done
> - [x] ~~**34722 LCD1 re-exam**~~ — **passed, oral, 25 August 2026** 🎉 → archived to `Archive/4th Semester/`
> - [x] ~~Register for 5th term courses~~ — done Aug 2026 (62999 dropped, 34840 added)
> - [x] ~~34840 prerequisite material downloaded~~ — complex numbers + signals in `00 - Prerequisites/`

---

## Quick Navigation

> [!tip] Vault Areas
> - [[DTU Study Path]] -- Career planning and course strategy
> - **Archive/4th Semester/** -- 34722 LCD1, 62711 DSD, 62768 EES, 34655 IAE2, 34620 BPE, 34315 IoT
> - **Archive/** -- Earlier semesters (DSP, Electromagnetics, IAE1)
> - **Projects/** -- Project workspace
> - **Resources/** -- General references

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

## All Notes by Course

```dataview
TABLE length(rows) AS "Notes"
FROM "Courses"
WHERE type != "home"
GROUP BY course-name
```
