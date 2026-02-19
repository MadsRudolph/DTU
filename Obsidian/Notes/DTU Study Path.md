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
updated: 2026-01-04
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
> - 34870 Electroacoustic Transducers and Systems
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
| 4th term (F)    | 34655       | Integrated Analog Electronics 2                      | 5    | Advanced analog / IC design      |
| 4th term (F)    | 34620       | Basic Power Electronics                              | 5    | Switch-mode + converters        |
| 4th term (F)    | 34315       | Internet of Things - Application and Infrastructure  | 5    | IoT + embedded systems for audio |
| 5th term (Jan)  | 34871       | Nonlinear Transducers                                | 5    | Loudspeaker nonlinearity & models |
| 7th term (A)    | 34652       | Power Electronics 1                                  | 10   | Advanced converters / design     |

**Alternative 7th-term combo (if you prefer acoustics + PCB/EMC instead of 34652):**

| Term            | Course code | Title                                               | ECTS | Theme                         |
|-----------------|------------:|-----------------------------------------------------|-----:|-------------------------------|
| 7th term (A)    | 34840       | Fundamentals of Acoustics and Noise                | 5    | General acoustics / noise     |
| 7th term (A)    | 34654       | Circuit Technology and EMC                         | 5    | PCB layout & EMC for hardware |

---

## 🧱 4th Term — Spring 2026 (Tilvalg 15 ECTS)

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

## 🔊 5th Term — January 2027 Tilvalg (5 ECTS)

Autumn 5th-term courses (already in plan):
- 62999 Innovation Pilot (10 ECTS)  
- 34870 Electroacoustic Transducers and Systems (10 ECTS)  
- 62755 Power Electronics (5 ECTS)

### 5.1 34871 – Nonlinear Transducers (5 ECTS, January)

> [!note] Why It Matters for Audio
> Deep dive into **nonlinear behaviour of loudspeakers and other transducers**:
> - Distortion mechanisms
> - Modelling and simulation of nonlinearities
> - Compensation and control strategies
>
> With 34870 + 34871 you get a **full loudspeaker engineer flavour**:
> - From small-signal modelling to **real-world distortion** and limits

> [!success] Key Outcomes
> Ability to **model, simulate and interpret nonlinearity** in speakers/mics
>
> Knowledge directly used in:
> - Hi-fi and studio monitor design
> - Headphones and hearing-aid transducers

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

#### 7.2 34840 – Fundamentals of Acoustics and Noise (5 ECTS)

> [!note] Course Content
> Broader **acoustics & noise** foundation:
> - Sound fields, propagation, room interactions
> - Noise control basics
>
> Good complement to electroacoustics courses and useful for:
> - Room acoustics
> - Noise-sensitive audio environments

#### 7.3 34654 – Circuit Technology and EMC (5 ECTS)

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

### 34374 – IoT Hardware and PCB Design (5 ECTS, spring, F4B)

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

> [!todo] Immediate Actions (4th Term Registration)
> - [ ] Register for 4th term courses before deadline
> - [ ] Verify **prerequisites** for selected courses:
>   - [ ] 34655 requires 34636 (should be completed in 3rd semester)
>   - [ ] Check 34315 prerequisites
> - [ ] Talk to **study counsellor** to:
>   - [ ] Get approval for tilvalg combination (34655, 34620, 34315)
>   - [ ] Confirm no timetable collisions

> [!important] DSP Reexam — May 20, 2026 (exam code E2-B)
> - [x] Create study schedule alongside 4th semester courses → [[62743 Digital Signal Processing (Reexam)]]
> - [ ] Register for re-exam (April 1--15, 2026)
> - [ ] Phase 1: Foundation refresh (Feb 19 -- Mar 22)
> - [ ] Phase 2: Filter design deep dive (Mar 23 -- Apr 26)
> - [ ] Phase 3: Exam drilling (Apr 27 -- May 20)

> [!todo] Future Course Planning
> - [ ] Verify 34871 runs in January 2027
> - [ ] Check 34652 / 34840 / 34654 availability for 7th term
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
