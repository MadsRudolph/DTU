---
cssclass: dashboard
type: home
tags: [dashboard, home]
---
# DTU -- 4th Semester

> [!abstract] Spring 2026
> **Programme:** Diplomingeniør, Electrical Engineering
> **Focus:** Analog IC design, Power electronics, IoT, Digital systems, Control
> **Semester total:** 30 ECTS (3 mandatory + 3 tilvalg)
>
> [[DTU Study Path|Full study plan and career track]]

---

## Courses

> [!course-62711] 62711 -- Digital Systems Design
> **FPGA design, VHDL, soft microprocessor**
> `5 ECTS` | Mandatory | Oral exam (May 28-29)
>
> [[62711 Digital Systems Design|Open course page]]
>
> **Current phase:** PWA (ALU / DataPath)

> [!course-34722] 34722 -- Linear Control Design 1
> **Transfer functions, Bode plots, PID, Regbot**
> `5 ECTS` | Mandatory | Written exam
>
> [[34722 Linear Control Design 1|Open course page]]

> [!course-34655] 34655 -- Integrated Analog Electronics 2
> **CMOS opamps, gain stages, frequency compensation**
> `5 ECTS` | Tilvalg | Written exam
>
> [[34655 Integrated Analog Electronics 2|Open course page]]

> [!course-34620] 34620 -- Basic Power Electronics
> **DC-DC converters, switch-mode, MOSFET drivers**
> `5 ECTS` | Tilvalg | Written exam
>
> [[34620 Basic Power Electronics|Open course page]]

> [!course-34315] 34315 -- Internet of Things
> **Embedded systems, IoT protocols, connected devices**
> `5 ECTS` | Tilvalg
>
> [[34315 Internet of Things|Open course page]]

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
> - [ ] **PWA deadline** -- 05-03-2026 (Week 9)
> - [ ] **MC test PWA** -- Before 21 March 2026
> - [ ] **PWB deadline** -- 02-04-2026 (Week 13)
> - [ ] **MC test PWB** -- Before 25 April 2026
> - [ ] **PWF + Video** -- 11-05-2026 (Week 19)
> - [ ] **Oral exam DSD** -- 28/29-05-2026 (Week 20)

---

## Quick Navigation

> [!tip] Vault Areas
> - [[DTU Study Path]] -- Career planning and course strategy
> - **Archive/** -- Previous semester notes (DSP, Electromagnetics, IAE1)
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
