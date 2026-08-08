---
title: DTU Audio / Amplifier Design Track
type: planning
tags:
  - DTU
  - Tilvalg
  - Audio
  - Amplifier-Design
  - Study-Planning
aliases:
  - Audio Engineering Study Plan
  - Amp Design Track
links:
  - [[DTU – Study Overview]]
  - [[MOC – Audio & Acoustics]]
updated: 2026-06-28
---

# DTU Audio / Amplifier Design Track

> [!summary] **Goal**
> Build a **hardware-focused audio profile** during the Diplomingeniør in Electrical Engineering:
> - Strong in **analog & mixed-signal electronics**  
> - Solid **power electronics / switch-mode** background (useful for class-D + SMPS)  
> - Real **electroacoustics / loudspeaker** understanding  
> - Attractive profile for jobs in **hi-fi, pro audio, hearing aids, speakers, and power amps**

---

## 🎯 Big-picture structure

> [!abstract] Base Programme (Already Planned/Ongoing)
> - 30035 Engineering Electromagnetics
> - 62743 Digital Signal Processing
> - 34636 Integrated Analog Electronics 1
> - 34621 Electromagnetic Sensors and Digital Signal Processing
> - 34722 Linear Control Design 1
> - 62711 Digital Systems, Design Of
> - 62768 Electrical Energy Systems Project
> - 34870 Electroacoustics
> - 62755 Power Electronics
> - Internship (6th term) + Diplomprojekt (7th term)

> [!tip] Tilvalg Focus Strategy
> 1. More **analog / IC design**
> 2. More **power electronics** (for class-D, SMPS, etc.)
> 3. Extra **electroacoustics / transducer** knowledge
> 4. **IoT + embedded systems** (for connected audio products)
> 5. Optional **PCB/EMC & acoustics** polish in 7th term

> [!info] **Unique Profile: Hardware + Software Audio Engineer**
> Combining analog/power electronics expertise with IoT/embedded skills creates a rare and valuable profile:
> - Most audio engineers: strong in analog, weak in embedded/IoT
> - Most embedded engineers: strong in software, weak in analog hardware
> - **This profile**: Full-stack audio engineer (analog → power → embedded → network)
> - **Target companies**: Sonos, KEF, RME, QSC, Devialet, Bang & Olufsen, etc.
> - **Leverages existing hobby skills**: Raspberry Pi, Home Assistant, embedded C programming

---

## 📚 Overview of recommended tilvalg

| Term            | Course code | Title (EN) / (DA)                                    | ECTS | Theme                            |
|-----------------|------------:|------------------------------------------------------|-----:|----------------------------------|
| 4th term (F) ✅ | 34655       | Integrated Analog Electronics 2                      | 5    | Advanced analog / IC design      |
| 4th term (F) ✅ | 34620       | Basic Power Electronics                              | 5    | Switch-mode + converters        |
| 4th term (F) ✅ | 34315       | Internet of Things - Application and Infrastructure  | 5    | IoT + embedded systems for audio |
| 5th term (E)    | 62755       | Power Electronics                                    | 5    | Switch-mode / converters         |
| 5th term (E)    | 34654       | Circuit Technology and EMC                          | 5    | PCB layout & EMC for hardware    |
| 5th term (Jan)  | 34871       | Nonlinear Transducers                                | 5    | Loudspeaker nonlinearity & models |
| 7th term (A)    | 34652       | Power Electronics 1                                  | 10   | Advanced converters / design     |

**Alternative 7th-term combo (if you prefer acoustics + PCB/EMC instead of 34652):**

| Term            | Course code | Title                                               | ECTS | Theme                         |
|-----------------|------------:|-----------------------------------------------------|-----:|-------------------------------|
| 7th term (A)    | 34840       | Fundamentals of Acoustics and Noise                | 5    | General acoustics / noise     |
| 7th term (A)    | 34654       | Circuit Technology and EMC                         | 5    | PCB layout & EMC for hardware |

---

## 🧱 4th Term — Spring 2026 (Tilvalg 15 ECTS) ✅ DONE

> [!success] Completed June 2026
> All six courses finished (34722, 62711, 62768, 34655, 34620, 34315 = 30 ECTS). DSP 62743 reexam passed (May 2026). Section kept for reference.

Mandatory courses already in the plan:
- 34722 Linear Control Design 1 (5 ECTS)  
- 62711 Digital Systems, Design Of (5 ECTS)  
- 62768 Electrical Energy Systems Project (5 ECTS, June)

### 4.1 34655 – Integrated Analog Electronics 2 (5 ECTS)

> [!note] Why It Matters for Audio
> Continuation of **34636** with focus on:
> - Advanced **CMOS op-amp structures**
> - Gain stages, frequency compensation, stability
> - Data converters and integrated analog building blocks
>
> Directly relevant for:
> - Pre-amps, tone controls, active crossovers
> - On-chip parts of class-D drivers or mixed-signal audio ICs

> [!success] Key Outcomes
> - Comfort with **$g_m$, $r_o$, $A_v$, $V_{DS}$** etc. in multi-stage amplifiers
> - Ability to read and design realistic **amp schematics** and **IC-style circuits**

---

### 4.2 34620 – Basic Power Electronics (5 ECTS)

> [!note] Why It Matters for Audio
> Introduction to **switch-mode power conversion**:
> - DC–DC topologies, rectifiers, basic DC–AC
> - Device operation (MOSFETs, diodes, etc.)
>
> Forms the conceptual basis for:
> - **Class-D output stages** (basically controlled DC–AC converters)
> - **SMPS rails** for analog + digital audio gear
> - Efficiency / losses / thermal considerations in amps

> [!success] Key Outcomes
> - Can analyse and roughly design **converter stages**
> - Understand **waveforms, losses and control** at a level that transfers well to audio power stages

---

### 4.3 34315 – Internet of Things - Application and Infrastructure Implementation (5 ECTS)

> [!note] Why It Matters for Audio
> Combines **embedded systems, IoT protocols and application development**
>
> Directly relevant for:
> - **Connected audio products** (smart speakers, networked amps, multi-room systems)
> - **Embedded control** for class-D amplifiers (microcontroller-based PWM, DSP)
> - **Remote monitoring/control** of audio equipment (Home Assistant integration, web interfaces)
> - **Complete product design** - bridging hardware and software layers
>
> Modern audio companies (Sonos, KEF, RME, QSC, Devialet) increasingly need engineers who understand both analog/power hardware AND IoT/embedded software

> [!success] Key Outcomes
> Ability to design **complete connected audio products**:
> - Analog front-end (34655) + Power stage (34620) + IoT control (34315)
> - Network-enabled amplifiers with remote control and monitoring
> - Integration with smart home systems (Home Assistant, MQTT, web APIs)
>
> **Leverages existing skills:**
> - Raspberry Pi, embedded C, and IoT protocols
>
> **Unique skillset:** most audio engineers are weak in embedded/IoT, most embedded engineers are weak in analog hardware

> [!info] Note on Measurement Skills
> - Originally planned 30020 (Electronic Measurement and Instrumentation) for lab/measurement skills
> - Can be self-learned through hobby projects or taken in future semester (5th/7th term or MSc)
> - Measurement skills will also be developed during internship and diploma project
> - IoT skills can enable building custom measurement tools as projects

---

## 🔊 5th Term — Autumn 2026 + January 2027 (25 + 5 ECTS)

> [!abstract] Enrolled per the DTU planner (checked 8-Aug-2026; registration window 8.7–5.8.2026)
> **Autumn 2026 (13 weeks) — 25 ECTS:**
> - 34870 Electroacoustics (10 ECTS) — *E2*
> - 62755 Power Electronics (5 ECTS) — *E1A*
> - 34840 Fundamentals of Acoustics and Noise Control (5 ECTS) — *E3A*
> - 34654 Circuit Technology and EMC (5 ECTS) — *E4A*
>
> **January 2027 (3-week intensive) — 5 ECTS:**
> - 34871 Nonlinear Transducers (5 ECTS) — fills the previously-empty January slot
>
> **Change vs. June-2026 plan:** **62999 Innovation Pilot (10 ECTS) was dropped**; **34840** (originally a 7th-term Option B candidate) moved up instead — autumn is 25 ECTS, not 30. The full acoustics trio (34870 + 34840 + 34871) now lands in one year. See the 34374 note below for why the wanted IoT/PCB course didn't make it.

### 5.1 34654 – Circuit Technology and EMC (5 ECTS, autumn, E4A)

> [!note] Why It Matters for Audio
> The PCB-layout + EMC course brought forward from the original 7th-term plan:
> - Grounding, shielding, routing for low noise
> - EMC/EMI compliance thinking
> - Flipped classroom + 4 assignments + lab/PCB project (lecturer Arnold Knott, Tue 13–17)
>
> Very relevant for:
> - Low-noise analog boards (pre-amps, phono stages)
> - Layout of high-$dV/dt$, high-$dI/dt$ class-D stages
> - Keeping your amp from radiating like a radio transmitter

> [!success] Key Outcomes
> - Hands-on PCB layout + EMC design skills — scratches much of the **34374** itch a term early
> - Pairs with 62755 power electronics for proper switch-mode board design

### 5.2 34840 – Fundamentals of Acoustics and Noise Control (5 ECTS, autumn, E3A)

> [!note] Why It Matters for Audio
> Moved up from the 7th-term Option B plan (replacing 62999 Innovation Pilot):
> - Sound fields, propagation, room interactions
> - Noise metrics and noise-control basics
> - Lecturer: Finn Agerkvist (also runs 34871 — same teacher across the acoustics track)
>
> Pairs with 34870 in the same autumn: transducers (34870) + the acoustic fields they create (34840).

> [!success] Key Outcomes
> - Room/environment acoustics understanding to complement electroacoustics
> - Frees the 7th-term tilvalg slot entirely for power electronics (34652) or other choices

### 5.3 34871 – Nonlinear Transducers (5 ECTS, January 2027, 3-week intensive)

> [!note] Why It Matters for Audio
> Deep dive into **nonlinear behaviour of loudspeakers and other transducers**:
> - Distortion mechanisms
> - Modelling and simulation of nonlinearities
> - Compensation and control strategies
>
> With 34870 (autumn) + 34871 (January) you get a **full loudspeaker engineer flavour**:
> - From small-signal modelling to **real-world distortion** and limits
> - 34870 is the recommended prerequisite — the autumn→January ordering lines up perfectly
> - 3-week intensive, Mon–Fri 8–17 (lecturer Finn T. Agerkvist)

> [!success] Key Outcomes
> Ability to **model, simulate and interpret nonlinearity** in speakers/mics
>
> Knowledge directly used in:
> - Hi-fi and studio monitor design
> - Headphones and hearing-aid transducers

> [!tip] Why not 34374 in January?
> You wanted **34374 IoT Hardware and PCB Design** in this slot, but it's a **13-week spring course (F4B)** — it can't run in a 3-week January block, and autumn 2026 is already full at 30 ECTS. So January is filled with **34871** (a true 3-week course that finishes your loudspeaker track), and **34374 stays a high-priority MSc/later target** — see "Future MSc hardware courses". Note that **34654 (this autumn) already covers a lot of the PCB-layout + EMC ground** 34374 would.

---

## ⚡ 7th Term — Autumn 2027 Tilvalg (10 ECTS)

You already have:
- Diplomingeniørprojekt (20 ECTS)

You need **10 ECTS tilvalg** on top.

### Option A — Power-focused (recommended if you want to be a hardcore amp / power engineer)

#### 7.1 34652 – Power Electronics 1 (10 ECTS)

> [!note] Why It Matters for Audio
> Advanced power-electronics course covering:
> - Detailed converter design
> - Device selection and losses
> - Control and practical design aspects
>
> Extremely useful for:
> - Designing **class-D power stages** properly
> - Designing **low-noise yet efficient SMPS** for audio
> - High-power active speakers, subwoofers, PA amps, etc.

> [!success] Key Outcomes
> - Can design realistic power-converter stages (not just follow app notes)
> - Much more attractive for companies doing **power-heavy audio products**

---

### Option B — Acoustics + PCB/EMC polish (if you lean more towards acoustics & practical hardware)

#### 7.2 34840 – Fundamentals of Acoustics and Noise (5 ECTS) — ✅ now taken in 5th term

> [!warning] Moved up
> **Enrolled in 5th term autumn 2026** (replacing the dropped 62999 Innovation Pilot). Option B for 7th term therefore needs a different partner course for 34840's slot.

> [!note] Course Content
> Broader **acoustics & noise** foundation:
> - Sound fields, propagation, room interactions
> - Noise control basics
>
> Good complement to electroacoustics courses and useful for:
> - Room acoustics
> - Noise-sensitive audio environments

#### 7.3 34654 – Circuit Technology and EMC (5 ECTS) — ✅ now taken in 5th term

> [!warning] Moved up
> Originally a 7th-term option; **now scheduled in 5th term (autumn 2026)**. If keeping Option B for 7th term, pick a different 5-ECTS partner for 34840 (e.g. acoustics/EMC alternative).

> [!note] Course Content
> Focus on **PCB layout, manufacturing, EMC/EMI**:
> - Grounding, shielding, routing for low noise
> - EMC compliance thinking
>
> Very relevant for:
> - Low-noise analog boards
> - Layout of high-$dV/dt$, high-$dI/dt$ class-D stages
> - Keeping your amp from radiating like a radio transmitter

---

## 🧪 Project & Internship alignment

### 6th Term – Internship

> [!example] Target Industries
> - Hi-fi / consumer audio (amps, DAC/amp combos, active speakers)
> - **Connected audio products** (smart speakers, wireless/networked audio systems, multi-room)
> - Pro audio (mixers, power amps, studio monitors, networked audio interfaces)
> - Hearing-aid / headset companies (audio + power + acoustics)
> - Power-electronics companies with interest in **class-D / motor drives / converters**

> [!tip] Companies Particularly Interested in IoT + Audio Combination
> **Consumer audio**: Sonos, Bowers & Wilkins, KEF, Bang & Olufsen, Devialet
> **Pro audio**: RME, Universal Audio, Focusrite, Yamaha, QSC, Lab.Gruppen
> **Nordic companies**: Dynaudio, System Audio, Danish Sound Technology, GN Audio (Jabra)
> **Smart home audio**: Google, Amazon, Apple (audio teams)

> [!success] Nice Selling Points from Your Course Mix
> - Analog IC background (34636 + 34655)
> - Power electronics (34620 + 62755, and possibly 34652)
> - Electroacoustics (34870 + 34871)
> - DSP (62743) + EM (30035, 34621)
> - **IoT + embedded systems** (34315) - unique differentiator for connected audio products
> - **Full-stack audio engineer**: analog hardware → power stages → embedded control → network connectivity

---

### 7th Term – Diplomingeniørprojekt (20 ECTS)

> [!example] Good Project Themes
> **Traditional audio projects:**
> - Design and measurement of a **class-D audio power amplifier**
> - **Active loudspeaker**: SMPS + class-D + DSP crossover + loudspeaker modelling
> - Low-noise **analog pre-amp / phono stage** with attention to EMC and layout
> - Integrated **audio front-end** (mic preamp + ADC + DSP + power stage)
>
> **IoT-enabled audio products** (combining analog/power hardware with embedded control):
> - Networked multi-room amplifier system with Home Assistant integration
> - Smart active speaker with wireless control and DSP
> - IoT-enabled class-D amp with remote monitoring and configuration
> - Wireless audio measurement/analysis system

> [!tip] Combine Multiple Elements
> - Courses on **analog + power + acoustics + IoT/embedded**
> - Your side projects (passive speakers, DIY amps, crossovers, Raspberry Pi, Home Assistant)
> - Possibly a company collaboration in audio/hearing or connected audio products
---

## 🔭 Future MSc hardware courses I want

> [!warning] Not Part of Current Diplom Plan
> These courses are **not** included in the current Diplom study plan (due to timetable and internship constraints), but should be prioritised when starting an MSc in Electrical Engineering / Electronics / Acoustics.

### 34374 – IoT Hardware and PCB Design (5 ECTS, spring, F4B) ⭐ TOP PRIORITY

> [!important] Wanted now, but couldn't fit the Diplom plan
> Strongly wanted (5th term), but it's a **13-week spring (F4B)** course: autumn 2026 is already full at 30 ECTS and it can't compress into the January 2027 3-week slot. Reserved for **MSc** — or revisit if a 6th-term spring window opens around the internship. In the meantime, **34654 (5th term autumn) covers much of the PCB/EMC overlap**.

> [!note] Course Overview
> Focus on **embedded hardware and PCB design** for IoT devices.
>
> Complements Diplom background in:
> - **Analog IC design** (34636 + 34655)
> - **Power electronics** (34620 + 62755)
> - **Electroacoustics** (34870 + 34871)
>
> Directly relevant for:
> - Designing **PCBs for audio amplifiers** and active speakers
> - Mixed-signal boards combining MCUs, DACs/ADCs and power stages

> [!tip] Other Candidates to Keep in Mind
> - **34654** – Circuit technology and EMC (PCB layout, EMC/EMI – very relevant for low-noise audio)
> - **34373** – Introduction to microcontroller development for IoT using embedded C (more embedded IoT firmware alongside hardware)
> - **22001 / 22003** – Acoustic signal processing / Auditory signal processing and perception (push more into audio DSP + hearing)

> [!idea] Future Planning
> When applying for the MSc, revisit this section and turn it into a concrete MSc study plan with exact semesters and course combinations.

## ✅ Action List

> [!check] Completed Tasks
> - [x] ~~Check the latest DTU course catalogue to confirm 4th term spring courses~~ (Completed 2026-01-04)
> - [x] ~~Select 4th term tilvalg courses~~ (Completed 2026-01-04)
>   - Selected: 34655, 34620, 34315 (replaced 30020 with IoT course)
>   - Total 4th semester: 30 ECTS (34722, 62711, 62768, 34655, 34620, 34315)
> - [x] ~~Complete all 4th semester courses + exams~~ (Done June 2026)
> - [x] ~~Pass DSP 62743 reexam~~ (exam code E2-B, May 2026)
> - [x] ~~Select 5th term courses~~ (Confirmed June 2026)
>   - Autumn 2026: 62999 (10), 34870 (10), 62755 (5), 34654 (5) = 30 ECTS
>   - January 2027: 34871 Nonlinear Transducers (5) — replaces the wanted-but-incompatible 34374
> - [x] ~~Verify 34871 runs in January 2027~~ (Confirmed — 3-week intensive, 34870 recommended as prereq)

> [!todo] Immediate Actions (5th Term)
> - [x] ~~Register for 5th term courses~~ (Done Aug 2026 — enrolled: 34870, 62755, 34840, 34654 autumn + 34871 January; **62999 dropped**, autumn = 25 ECTS)
> - [ ] **34722 LCD1 re-exam (August 2026)** — failed the June ordinary exam; re-exam prep is the active project (see [[00 LCD1 — Exam Hub]])
> - [ ] Work through the 34840 `00 - Prerequisites` material before September (complex numbers + signals refresher, Finn Agerkvist's strong recommendation)
> - [ ] Ask whether **34374** could ever be slotted into 6th-term spring 2027 around the internship

> [!todo] Future Course Planning
> - [ ] 34374 IoT Hardware and PCB Design — keep as **top-priority MSc** target (spring F4B, doesn't fit Diplom plan)
> - [ ] Check 34652 / 34840 availability for 7th term (note: 34654 already taken in 5th term)
> - [ ] Consider 30020 for future semester or self-learn measurement skills

> [!tip] Internship & Project Preparation
> - [ ] Reach out to **relevant DTU groups** (Electronics, Acoustic Technology) for potential internship ideas
> - [ ] Look for companies working on connected audio products (leverage IoT + audio skills)
> - [ ] Early brainstorming for IoT-audio Diplomprojekt topics

> [!example] Portfolio Development (GitHub / Obsidian)
> - [ ] Speaker design project
> - [ ] Amp / power-electronics experiments
> - [ ] Home Assistant / Raspberry Pi audio projects
> - [ ] Course-related mini-projects and reports
> - [ ] Potential 34315 project ideas combining IoT + audio

---
