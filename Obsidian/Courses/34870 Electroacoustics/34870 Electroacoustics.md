---
course: "34870"
course-name: "Electroacoustics"
type: home
cssclass: course-home
tags: [Electroacoustics, Audio, home]
---
# 34870 Electroacoustics

> [!info] Course Information
> **Official title:** Electroacoustic transducers and systems (*Elektroakustiske transducere og systemer*)
> **Semester:** Autumn 2026 (5th semester), 13 weeks · **10 ECTS — the big one this term**
> **Placement:** E2 — **Mon 13:00–17:00 + Thu 8:30–12:00**, Campus **Lyngby**
> **First lecture:** **Monday 31 August, 13:00 — room 019, building 352**
> **Exam:** **Oral, 30 min — 9–10 December 2026 (E2-A/B)**. Lab + project quizzes count **30 %**.
> **Aids:** Written aids allowed · 7-step scale, **external** censor
> **Department:** 34 — Electrical and Photonics Engineering
> **Prerequisites:** **34840** · 22050 · simple analog circuits (Bode plots, coupled resonant circuits, basic mechanical physics)
> **Replaces:** 31220 (also point-blocking)

> [!info] Teaching staff (all building 352)
> | | Name | Room | Email |
> |---|---|---|---|
> | **VCH** | Vicente Cutanda Henríquez *(responsible)* | 016 | `vcuhe@dtu.dk` |
> | **FL** | Frieder Lucklum | 020 | `fluc@dtu.dk` |
> | **FA** | Finn Agerkvist | 010 | `ftag@dtu.dk` |
> | **TA** | Teguh Aditanoyo *(teaching assistant)* | — | `tegad@dtu.dk` |

> [!todo] Before the first lecture (Mon 31 Aug)
> - [x] ~~Install LTspice~~ — already installed and well used
> - [ ] Decide the sim tool per task — see the callout below
> - [ ] Refresh circuit analysis: Kirchhoff laws, R/L/C impedances, current & voltage sources, **dual circuits**, Norton & Thévenin equivalents
> - [ ] Review **chapter 1** of `Literature/00 - Basic Material/Fundamentals_of_acoustics.pdf`
> - [ ] Find a **group of 3** — simulations, labs and the project are all done in threes

> [!tip] Simulator: KiCad/ngspice for your own work, LTspice for following the course
> Current default is **KiCad's built-in ngspice** (everything has run through KiCad for the last few weeks); LTspice is installed and familiar, QSPICE is the personal preference.
>
> For 34870 that split matters in one place: **Lab A is literally "Analogy circuits in LTspice"**, the staff teach LTspice during the lectures, and the quiz behind it is part of the 30 %. The physics is tool-agnostic — an electromechanoacoustical analogy is just an RLC network, and ngspice will produce the same AC sweep — but the worked examples, the hand-outs and any help you ask for will be in LTspice.
>
> Sensible split:
> - **Lab A + in-lecture examples** → LTspice, so you are on the same screen as the staff
> - **Your own modelling, the loudspeaker project, anything that wants a schematic you keep** → KiCad/ngspice
> - Keep `Literature/00 - Basic Material/LTspice circuit simulator - Quick Guide.pdf` around only as a translation reference — you do not need it as a tutorial

> [!warning] 34840 is a formal prerequisite — and you are taking it *in parallel*
> DTU lists [[34840 Fundamentals of Acoustics and Noise Control|34840]] as a prerequisite, but both run this autumn (34840 is E3A, Tue mornings). For the first weeks 34870 runs ahead of your acoustics foundation — which is exactly why the staff hand out the *Fundamentals of Acoustics* note as background reading.

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34870)
> - [[DTU Study Path#🔊 5th Term — Autumn 2026 + January 2027 (25 + 5 ECTS)|Study path context]]
> - Working folder: `5. Semester/Electroacoustics/` (KiCad, LTspice, Matlab, Labs, Project)

---

## Course Plan — Autumn 2026

> [!note] Source
> `Literature/00 - Basic Material/34870 Course plan Fall2026.pdf` (dated 20 Aug 2026). **The staff update this document during the course** — re-download from DTU Learn periodically and re-check this table.

| Date | Activity | Beranek | Leach | Done |
|---|---|---|---|---|
| Mo 31/8 | Introduction to the course · Analogies intro *(FL)* | 3.2–3.4 | 3/4 | |
| Th 3/9 | Analogies: **mechanical** systems *(FL)* | 3.2–3.4 | 3/4 | |
| Mo 7/9 | Analogies: **acoustic** systems *(FL)* · Intro **Lab A** | 3.2–3.4 | 3/4 | |
| Th 10/9 | Analogies: **transducers** *(FL)* · Microphone intro *(VCH)* | 3.5–3.7, 5 | 4.4–4.7, 5.1–5.4 | |
| Mo 14/9 | Microphones: dynamic & condenser (1) *(VCH)* | 5 | 5.1–5.8 | |
| Th 17/9 | Microphones: condenser (2) · **Metrology & calibration** *(VCH)* | as above | BIPM / Peters | |
| Mo 21/9 | Microphone scattering · Lab intro · **Labs B/C** *(VCH)* | — | 2.15, 5.2 | |
| Th 24/9 | Loudspeakers: **moving coil** *(VCH)* | 6.1–6.11, 6.18 | 6.1–6.21, 11.7.1–11.7.4 | |
| Mo 28/9 | **Labs B/C** | — | — | |
| Th 1/10 | Loudspeakers: **enclosures** *(VCH)* | 7.6, 7.8–7.15 | 7.1–7.10, 8.1–8.13 | |
| Mo 5/10 | **Labs D/E** | — | — | |
| Th 8/10 | Loudspeaker systems — **project intro** *(VCH)* | 7.20 | 10.1–10.6 | |
| | 🍂 *Autumn break* | | | |
| Mo 19/10 | Project work · **Labs D/E** | — | — | |
| Th 22/10 | Radiation, acoustic environment, speakers · **Nonlinear circuit models** *(FA)* | 13.7, 8.2 | 2.13 | |
| Mo 26/10 | Advanced topics in electroacoustics: projects and courses | — | — | |
| Th 29/10 | Guest lecture TBD · Project Q&A *(VCH)* | — | — | |
| Mo 2/11 | Guest lecture TBD | — | — | |
| Th 5/11 | Guest lecture TBD · Project Q&A *(VCH)* | — | — | |
| Mo 9/11 | Guest lecture TBD | — | — | |
| Th 12/11 | Guest lecture TBD · Project Q&A *(VCH)* | — | — | |
| Mo 16/11 | Guest lecture TBD | — | — | |
| Th 19/11 | Guest lecture TBD · Project Q&A *(VCH)* | — | — | |
| Mo 23/11 | Guest lecture TBD | — | — | |
| Th 26/11 | **Exam Q&A + evaluation** | — | — | |
| Mo 30/11 | ⏰ **Project quiz deadline** | — | — | |
| Th 3/12 | **Project presentations and demonstrations** | — | — | |
| **9–10/12** | 🎓 **ORAL EXAM (E2-A/B)** | — | — | |

> [!note] Format drifts through the term
> Mondays start as lectures and become lab exercises, guest lectures and follow-up. Thursdays turn into practical work later on. From late October it is almost entirely guest lectures + project work.

---

## Compulsory Lab Exercises & Project

> [!important] All quizzes must pass before their deadline — they are 30 % of the grade
> Active participation in the lab work **and** the project presentation is mandatory. Work happens in **groups of 3**.

| | Exercise | Period | Quiz deadline |
|---|---|---|---|
| **A** | Analogy circuits in **LTspice** | 8/9 – 20/9 | ⏰ **20/9** |
| **B** | Scaled microphone measurement | 21/9 – 29/9 | ⏰ **5/10** |
| **C** | Microphone calibration | 21/9 – 29/9 | ⏰ **5/10** |
| **D** | Loudspeaker enclosures | 5/10 – 20/10 | ⏰ **26/10** |
| **E** | Loudspeaker response | 5/10 – 20/10 | ⏰ **26/10** |
| 🔧 | **Loudspeaker project** | 19/10 – 30/11 | ⏰ **30/11** |

→ Working folders: `5. Semester/Electroacoustics/Labs/` and `.../Project - Loudspeaker System/`

> [!tip] Optional: visit the DFM primary metrology lab
> Danish national primary lab for acoustics, in the **cellar of building 352**. Book with Salvador Barrera Figueroa (`sbf@dfm.dk`, office 025, b. 352) — [DFM acoustics calibration](https://dfm.dk/en/services/calibration/calibration-acoustics/). Worth doing around the 17/9 metrology lecture.

---

## Course Content

> [!abstract] What the course actually covers
> - **Analogies** between mechanical, acoustical and electrical systems — the spine of the whole course
> - Equivalent networks for simple acoustic and mechanical systems
> - **Transducers:** standard *and* MEMS loudspeakers, telephones, microphones — theory, construction, directivity, radiation
> - Frequency response of condenser, dynamic and MEMS **microphones**, and which parameter moves what
> - Frequency response of electrodynamic **loudspeakers** and micro-speakers
> - **Enclosures:** sealed vs. bass-reflex — effect on impedance and SPL, and designing a box for a given driver
> - **Crossover** design — the usual problems and how they get solved
> - Acoustic **metrology**: measurement, calibration, uncertainty assessment
> - Frequency analysis of simple linear networks in **LTspice**
> - Microphone and loudspeaker arrays

---

## Literature

> [!success] Already downloaded — in `Literature/`
> **`00 - Basic Material/`** (from DTU Learn):
> - `34870 Course plan Fall2026.pdf` — the schedule above
> - `Fundamentals_of_acoustics.pdf` — background refresher, **review ch. 1**
> - `LTspice circuit simulator - Quick Guide.pdf`
>
> **`Metrology - BIPM/`** (downloaded from bipm.org — required reading for the 17/9 metrology lecture):
> - `SI Brochure 9th ed (EN).pdf` (102 pp) · `… Concise Summary` · `… Appendix 3` · `SI Brochure - FAQs`

> [!success] Books downloaded via DTU Library (26 Aug) — in `Literature/`
> - **`Beranek & Mellow - Acoustics, Sound Fields and Transducers (2nd ed 2019).pdf`** — **877 pp**, the complete book assembled from the ScienceDirect per-chapter downloads into one file, with a **bookmark on every chapter, appendix and the index** (open the PDF outline/sidebar to jump)
> - **`Lenk et al - Electromechanical Systems in Microtechnology and Mechatronics (2011).pdf`** — 483 pp, Springer

> [!warning] Edition mismatch — check section numbers before reading
> The course plan cites Beranek as the **2012 edition**; what we have is the **2019 2nd edition** (15 chapters instead of 13). Chapter *topics* line up for the early references, but the later ones do not: the plan's **"8.2"** for *radiation and acoustic environment* points at **Ch 08 = Cell phone acoustics** in our copy, which is clearly not the same section. Treat the mapping below as a starting point and confirm against the lecture.
>
> | Course plan ref | Chapter in our copy | PDF page |
> |---|---|---|
> | 3.2–3.7 | Ch 03 — Electromechanoacoustical circuits | **86** |
> | 5 | Ch 05 — Microphones | **234** |
> | 6.1–6.11, 6.18 | Ch 06 — Electrodynamic loudspeakers | **279** |
> | 7.6, 7.8–7.15, 7.20 | Ch 07 — Loudspeaker systems | **333** |
> | 13.7 | Ch 13 — Radiation/scattering, boundary integral method | **604** |
> | 8.2 ⚠️ | Ch 08 — Cell phone acoustics | 446 — **does not match, verify** |
>
> *(PDF page = the page in the merged file, not the book's printed page number.)*

> [!quote] Still to get yourself
> 1. **Marshall Leach** — *Introduction to Electroacoustics and Audio Amplifier Design*, 4th ed. Excerpts (<50 pp) distributed during the course; **buying it is not necessary**. [Kendall Hunt](https://he.kendallhunt.com/product/introduction-electroacoustics-and-audio-amplifier-design) · DTU bookstore · older editions in the library.
> 2. **R. Peters (ed.)** — *Uncertainty in Acoustics: Measurement, Prediction and Assessment* (2021) → [findit](https://findit.dtu.dk/en/catalog/2691236388) — needed for the 17-Sep metrology lecture
> 3. Circuit-analysis basics, if needed → [findit](https://findit.dtu.dk/en/catalog/2301801656)

> [!note] Two copies of *Fundamentals of Acoustics*
> 34870's copy (`Literature/00 - Basic Material/`) and [[34840 Fundamentals of Acoustics and Noise Control|34840]]'s `Fundamentals_of_acoustics_2022.pdf` are **different files** (4.35 vs 4.32 MB) — different revisions of the same Jacobsen text. Both kept deliberately.

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> The core **electroacoustics** course of the audio track:
> - Loudspeaker & microphone modelling (electrical–mechanical–acoustical analogies)
> - Transducer small-signal behaviour, radiation, enclosures
> - Foundation for [[34871 Nonlinear Transducers]] (January) — the formal prerequisite

> [!success] Track Payoff
> 34870 (autumn) + [[34871 Nonlinear Transducers|34871]] (January) = a full **loudspeaker engineer** flavour, from small-signal models to real-world distortion.

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34870 Electroacoustics/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Labs

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34870 Electroacoustics"
WHERE type = "exercise" OR type = "lab" OR type = "quiz"
SORT date ASC
```
