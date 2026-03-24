---
course: "34620"
course-name: "Basic Power Electronics"
type: home
cssclass: course-home
tags: [PE, home]
---
# 34620 Basic Power Electronics

> [!info] Course Information
> **Course:** 34620 Basic Power Electronics
> **Semester:** Spring 2026 (4th semester)
> **Lecturers:** TBD
> **ECTS:** 5
> **Exam:** Written exam
> **Teaching:** TBD
> **Prerequisites:** Circuit theory, basic electronics

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34620)
> - [[DTU Study Path#4.2 34620 -- Basic Power Electronics|Study path context]]

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| | | | *To be filled when schedule is available* | | |

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> Foundation for class-D amplifiers and SMPS design:
> - DC-DC converter topologies (buck, boost, buck-boost)
> - MOSFET switching, gate drivers
> - Efficiency and thermal management
> - Directly applicable to audio power stage design

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34620 Basic Power Electronics/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34620 Basic Power Electronics/Exercises"
WHERE type = "exercise" OR type = "quiz"
SORT date ASC
```

> [!tip] Completed Exercises
> - [[Exercises_Week2|Week 2 -- Waveforms, Mean & RMS Values]]

---

## Slides

- [[presentation.pdf|Course Presentation]]

---

## Literature & Resources

*To be added as course materials become available.*

---

## Formulas

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | Mean value | $V_{avg} = \frac{1}{T}\int_0^T v(t)\,dt$ |
> | RMS value | $V_{RMS} = \sqrt{\frac{1}{T}\int_0^T v^2(t)\,dt}$ |
> | Crest factor | $\xi = \frac{\hat{V}}{V_{RMS}}$ |
> | Linear reg. efficiency | $\eta = \frac{V_{out}}{V_{in}}$ |

---

## Quick Reference

> [!tip] Useful Identities
> ```
> Sine RMS:     V_hat / sqrt(2)
> Triangle RMS: V_hat / sqrt(3)
> Square d:     sqrt(d) * V_hat
> ```
