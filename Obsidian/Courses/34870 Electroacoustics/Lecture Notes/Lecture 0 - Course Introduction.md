---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-08-31
week: 36
lecture: 0
topic: "Course Introduction"
tags: [Electroacoustics, lecture-note, admin]
---
# Lecture 0 — Course Introduction

> [!info] Lecture Info
> **Date:** Monday 31 August 2026 (opening slides, before [[Lecture 1 - Analogies - Introduction|Lecture 1]] proper)
> **Slides:** `Slides/34870_Lecture0_E26.pdf` (4 pages)

> [!abstract] Course map
> ```mermaid
> graph TD
>     A[Analogies e.g. microphones] --> B[Microphones]
>     A --> C[Loudspeakers]
>     C --> D[Loudspeaker systems]
>     D --> E[Listening rooms]
>     A --> F[Numerical models]
>     A --> G[Acoustic Metrology]
>     A --> H[μ-transducers / MEMS]
> ```
> Everything downstream (microphones, loudspeakers, systems, metrology) is built on the **analogy framework** covered in lectures 1–3.

> [!note] Core elements of the course
> - Lectures
> - Problem solving
> - Lab exercises
> - Loudspeaker project
> - Guest lectures
> - Company visit

> [!warning] Time commitment
> **10 ECTS ≈ 12–15 hours/week.** Extra time beyond lectures is explicitly expected — don't treat this as a normal 5-ECTS course pace.

> [!important] Teaching vs. Learning
> - **Teaching** = the teacher performs, active; the student listens, passive.
> - **Learning** = an active process. Teaching can *start* it, but learning only happens when **you** are active.
> - 34870 leans on **Learning**, not Teaching: problem solving, simulation work, lab exercises, project work.
>
> Practical implications:
> - Use time on the course **every week**, not just before deadlines.
> - **Take notes and ask questions during (and after) lectures** — review afterwards, don't just passively watch.
> - Slides/videos **support** the lectures, they don't replace them.
> - Study by *solving problems*, reading textbooks, and going through lab exercises.

> [!success] Learning objectives (from course description)
> A student who has met the objectives will be able to:
> - Explain the principles of analogies between electrical, mechanical and acoustic systems
> - Draw equivalent circuits for simple mechanical and acoustic systems
> - Apply the analogies to analyze and model electroacoustic devices
> - Predict the frequency response of dynamic, condenser, and MEMS microphones and explain each component's influence
> - Predict the frequency response of electrodynamic loudspeakers and microspeakers and explain each component's influence
> - Explain the effects of closed and vented enclosures on frequency response and impedance, and design such enclosures for a given driver
> - Explain common crossover-filter design problems and how to solve them
> - Frequency-analyze simple linear circuits in LTspice
> - Perform uncertainty estimation of an acoustic measurement, and calibrate microphones/loudspeakers
> - Design a loudspeaker system's frequency response through measurement, physical principles, and analytical calculation
> - Subjectively evaluate and compare loudspeaker systems via listening tests in a standardized environment

> [!warning] Illegal sharing of digital textbooks
> Sharing/acquiring digital textbooks via Facebook, Messenger, DBA, Dropbox etc. is **illegal** (unless the publisher/author permits it) and has had real consequences — fines, claims, conditional prison sentences, criminal records for students. You're allowed to share **up to 20%** of a textbook via your institution's closed network under the Copydan agreement (see `tekstognode.dk/undervisning`). Not really lecture content, but noted since it was explicitly on the slides.

---

## Content overview (topic list from the slides)

> [!abstract] Analogies (e.g. microphones)
> - Through and across variables (voltage, current, force, velocity, pressure, volume velocity)
> - Impedance analogy
> - Admittance analogy
> - Identification of elements

> [!abstract] Microphones
> - Condenser microphones — principle of operation and equivalent network
> - Dynamic microphones — principle of operation and equivalent network
> - Pressure and gradient microphones, directionality
> - Microphone influence on the sound field, free-field microphones
> - Microphone numerical simulation
> - Acoustic metrology — uncertainty of measurement

> [!abstract] Loudspeakers
> - Principle of operation and equivalent network
> - Effects of enclosures (none / baffle / box)
> - Vented box tuning
> - Loudspeaker systems and crossover networks
> - Radiation impedance, efficiency
> - Basic SPICE modelling (LTspice)
> - Microspeakers

---

> [!tip] Next
> [[Lecture 1 - Analogies - Introduction|Lecture 1 — Analogies: Introduction]] starts the actual technical content: what a lumped element is, why analogies work, and the electrical/mechanical/acoustic variable table.
