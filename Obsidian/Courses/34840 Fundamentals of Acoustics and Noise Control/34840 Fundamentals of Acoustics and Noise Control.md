---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: home
cssclass: course-home
tags: [Acoustics, Noise, Audio, home]
---
# 34840 Fundamentals of Acoustics and Noise Control

> [!info] Course Information
> **Official title:** Fundamentals of acoustics and noise control (*Grundkursus i akustik og støj*)
> **Semester:** Autumn 2026 (5th semester), 13 weeks · **5 ECTS**
> **Placement:** E3A — **Tue 08:00–12:00**, **building 358, room 63**, Campus Lyngby
> **First lecture:** **Tuesday 1 September, 08:00 — building 358, room 063**
> **Exam:** **Written, 4 hours — 11 December 2026**. Individual hand-in + lab report count **10 %**.
> **Aids:** All aids, **no internet access** · 7-step scale, **external** censor
> **Department:** 34 — Electrical and Photonics Engineering (Dept. 22 Health Tech participating)
> **Prerequisites:** 01005 / 01007 Mathematics 1 (or equivalent)
> **Replaces:** 31200 (also point-blocking)

> [!info] Teaching staff
> | | Name | Email | Phone |
> |---|---|---|---|
> | **FA** | Finn Agerkvist *(responsible)* | `ftag@dtu.dk` | 4525 3941 |
> | **CHJ** | Cheol-Ho Jeong | `chje@dtu.dk` | 4525 3934 |
> | **TD** | Torsten Dau | `tdau@dtu.dk` | 4525 3977 |
> | **JBR** | Jonas Brunskog | `jbru@dtu.dk` | 4525 3935 |

> [!important] This is the gateway course
> DTU states plainly that 34840 is the academic prerequisite for **all** advanced acoustics courses — including [[34870 Electroacoustics|34870]], which you are taking *in the same semester*. Getting the fundamentals solid early pays off twice this term.

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34840)
> - [[DTU Study Path#5.2 34840 – Fundamentals of Acoustics and Noise Control (5 ECTS, autumn, E3A)|Study path context]]
> - Working folder: `5. Semester/Acoustics and Noise Control/` (Matlab, Assignments)

---

## Lecture Plan — Autumn 2026

> [!note] Source
> `Literature/34840 lecture plan 2026_v1.pdf`. Page numbers refer to `Literature/Fundamentals_of_acoustics_2022.pdf`.

| # | Date | By | Topic | Pages | Done |
|---|---|---|---|---|---|
| 1 | Tue 01/09 | FA | Intro, fundamental acoustic concepts; **plane waves** | 1–8 | |
| 2 | Tue 08/09 | FA | Reflection and interference; **spherical waves** | 8–15 | |
| 3 | Tue 15/09 | FA | Decibels and levels; frequency analysis; acoustic measurements · **Matlab exercise** | 15–27 | |
| 4 | Tue 22/09 | FA | The concept of **impedance**; sound intensity and sound power | 27–36 | |
| 5 | Tue 29/09 | FA | Radiation of sound; **monopoles, dipoles, pistons** · *midterm evaluation* | 37–48 | |
| 6 | Tue 06/10 | CHJ | **Modes and eigenfrequencies in rooms**; the diffuse sound field | 81–101 | |
| | | | 🍂 *Autumn break* | | |
| 7 | Tue 20/10 | CHJ | **Sound absorption**; room acoustic design | 103–112 | |
| 8 | Tue 27/10 | FA | **Loudspeakers** *(additional lecture note)* | — | |
| 9 | Tue 03/11 | TD | Our hearing: **frequency selectivity and masking** | ch. 2 | |
| 10 | Tue 10/11 | TD | **Physiological acoustics** | ch. 2 | |
| 11 | Tue 17/11 | JBR | **Structure-borne sound**; vibration isolation | 133–162 | |
| 12 | Tue 24/11 | JBR | **Sound insulation**; single and double walls | 113–132 | |
| 13 | Tue 01/12 | FA | Summary and evaluation | — | |
| 🎓 | **Fri 11/12** | | **WRITTEN EXAM (4 h)** | | |

---

## Compulsory Hand-ins — 10 % of the grade

> [!important] Problem assignment — **individual**
> Problem set uploaded **Monday 28 September**, hand-in deadline **Friday 9 October**.
> Derivations *and* solutions must be handed in **by each student individually** — this one is not group work.

> [!important] Experimental exercise — one lab
> One laboratory exercise, roughly **two hours** of measurements. The report is due **no later than two weeks after conducting the lab**.
> Scheduled on mornings and afternoons during the period of **lectures 8–11** (27 Oct – 17 Nov).

→ Working folder: `5. Semester/Acoustics and Noise Control/Assignments/`

---

## Course Material

> [!success] Already in `Literature/` — all downloaded
> - `Fundamentals_of_acoustics_2022.pdf` — **the main course text**
>   (Jacobsen, Poulsen, Rindel, Gade & Ohlrich, *Fundamentals of Acoustics and Noise Control*, AT note no. 31200)
> - `Introduction to Loudspeakers -2021.pdf` — Finn Agerkvist's loudspeaker note, used for lecture 8
> - `34840 lecture plan 2026_v1.pdf` — the plan above
>
> **`Literature/00 - Prerequisites/`** — the background material Finn Agerkvist *strongly recommends*:
> - `1-Basics on complex numbers.pdf` · `2-Exercises on complex numbers.pdf` · `3-Solutions to Exercises on complex numbers.pdf`
> - `11-Signals and systems 101_ContTime.pptx` · `12-Signals and systems 101_DiscreteTime.pptx`
>   (the matching **video lectures live on DTU Learn** — not downloadable)

> [!todo] Before Tuesday 1 September
> - [ ] Work through the complex-numbers problems (solutions provided)
> - [ ] Watch the Signals & Systems 101 video lectures on DTU Learn
> - [ ] Skim pp. 1–8 of the main text — lecture 1 covers plane waves
>
> Finn's own words: do this **even if you have learnt these things previously**, if you have not used them actively for a while.

> [!note] PDFs are drive-synced
> Large files here are gitignored and stored in Google Drive. On a fresh PC: `python Obsidian/scripts/drive-sync/download.py`

---

## Course Content

> [!abstract] What the course actually covers
> - **Field quantities & units:** sound pressure, particle velocity, speed of sound, characteristic impedance; complex notation
> - **Measuring sound:** the dB scale, A-weighting, time constants, energy-equivalent level $L_{eq}$, octave and 1/3-octave analysis, adding uncorrelated sources
> - **Energy:** energy density, sound intensity, sound power — and what sound power is actually good for
> - **Wave fields:** plane and spherical waves, standing waves, interference fields; reflection and transmission between media; the effect of a reflecting plane
> - **Radiation:** monopole, dipole, and a piston in a baffle
> - **Rooms:** modes in a rectangular room, the diffuse field, the energy-balance equation, reverberation time, absorbing materials
> - **Hearing:** basic properties, threshold of hearing, masking
> - **Noise control:** resonances in simple mechanical/acoustic systems, structure-borne sound, vibration isolation of machines, sound insulation of single and double constructions
> - **Electrodynamic loudspeakers** — the handshake into 34870

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> The general **acoustics & noise** foundation of the audio track:
> - Sound fields, propagation, absorption, room interactions
> - Noise metrics and noise-control principles
> - Complements [[34870 Electroacoustics]] (same autumn) — transducers meet the rooms they play into

> [!success] Track Payoff
> 34870 + 34840 in the same autumn + [[34871 Nonlinear Transducers]] in January = electro-, room- and nonlinear acoustics covered in one year.

> [!tip] Grøn Dyst eligible
> This course allows preparing a project for DTU's sustainability/environment student conference — an easy portfolio win if a noise-control topic fits.

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34840 Fundamentals of Acoustics and Noise Control/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Hand-ins

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34840 Fundamentals of Acoustics and Noise Control"
WHERE type = "exercise" OR type = "assignment" OR type = "quiz"
SORT date ASC
```
