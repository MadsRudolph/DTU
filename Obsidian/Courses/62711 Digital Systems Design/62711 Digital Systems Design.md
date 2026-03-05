---
course: "62711"
course-name: "Digital Systems Design"
type: home
cssclass: course-home
tags: [DSD, home]
---
# 62711 Digital Systems Design

> [!info] Course Information
> **Course:** 62711 Design af digitale systemer
> **Semester:** Spring 2026 (4th semester)
> **Lecturers:** jmgm, osch@dtu.dk
> **Textbook:** Logic & Computer Design Fundamentals, M.M. Mano & C.R. Kime, 5th ed., Pearson, 2016
> **FPGA Board:** Nexys 4 DDR (Xilinx Artix-7 XC7A100T-1CSG324C)
> **Exam:** Oral exam (weeks 20, 28 May - 29 May 2026)
> **Teaching:** Lectures + Lab work Fridays 9:30-13:00, groups of 4 (2x2 subgroups)

> [!tip] Quick Links
> - Team repo: [digital-systems-design](https://github.com/gigurd/Design-of-digital-systems-62711) | [[Team Workflow]]
> - Lesson plan: [[62711_Lektionsplan_F2026.pdf|Lektionsplan F2026]]
> - Report template: [[Rapport_template_v22.dotx|Report template]]

---

## Roadmap

| Wk  | Date  | Lec | Topic                                                         | Reading                                              | Phase     | Deliverables                            | Done  |
| --- | ----- | --- | ------------------------------------------------------------- | ---------------------------------------------------- | --------- | --------------------------------------- | ----- |
| 6   | 06-02 | 1   | Intro, structural VHDL, FPGA architecture                     | 3.1-3.5, 3.7, 3.8, Datasheet                         | PWA       |                                         | - [x] |
| 7   | 13-02 | 2   | Digital Arithmetic, combinatorial & register logic            | 4.2, 4.3, 6.1, 3.1-3.4, 3.5, 3.7, 3.8, 8.2-8.4 hints | PWA       | Opg 2                                   | - [ ] |
| 8   | 20-02 | 3   | Digital Arithmetic video, adders                              | 3.9, 3.10, 3.11, 3.12, 8.2, 8.3, 8.4 (FU)            | PWA       | Opg 3                                   | - [ ] |
| 9   | 27-02 | 4   | PWA function unit                                             |                                                      | PWA       | **PWA deadline (05-03-2025)**           | - [ ] |
| 10  | 06-03 | 5   | Micro-operations, register transfer, shift register, counters | 6.2-6.6, 6.8, 8.1-8.6                                | PWB       |                                         | - [ ] |
| 11  | 13-03 | 6   | Control word, Datapath architecture, Midterm evaluation       | 6.8, 6.10, 6.11, 6.13, 8.6-8.9                       | PWB       | Opg 5                                   | - [ ] |
| 12  | 20-03 | 7   | Control & register transfer, ASM (Algorithmic State Machines) | 8.9                                                  | PWB       | Opg 6, **MC test PWA (before 21 Mar)**  | - [ ] |
| 13  | 27-03 | 8   | Computer design, summing up                                   | 8.7, 8.8, 8.9                                        | PWB       | **PWB deadline (02-04-2025)**           | - [ ] |
| 14  |       |     | *Paskeferie*                                                  |                                                      |           |                                         |       |
| 15  | 10-04 | 9   | Memory Design, FPGA Memory                                    | 7.1-7.7, ug473                                       | Final PWF |                                         | - [ ] |
| 16  | 17-04 | 10  | Assembler Language Programming                                | 9.1-9.9, 9.5, 9.7, 9.6, 9.8, 9.9                     | Final PWF | **MC test PWB (before 25 Apr)**         | - [ ] |
| 17  | 24-04 | 11  | I/O, Interfaces & Memory Systems                              | 11.1-11.8, 12.1-12.4                                 | Final PWF |                                         | - [ ] |
| 18  | 01-05 | 12  | CPU Models                                                    | 10.1-10.5                                            | Final PWF | Opg 9 (simulation for PWA)              | - [ ] |
| 19  | 08-05 | 13  | PWF completion & final evaluation                             |                                                      | Final PWF | **Video presentation + Report (11-05)** | - [ ] |
| 20  | 28-05 |     | **Oral exam**                                                 | All pensum                                           |           |                                         | - [ ] |

---

## Project Overview

### PWA -- ALU / DataPath

> [!abstract] PWA
> **Goal:** Design and implement an ALU (Arithmetic Logic Unit) as part of the DataPath
> **Lectures:** 1-4
> **Deadline:** 05-03-2026 (Week 9)
>
> **Key components:**
> - Structural VHDL design
> - Digital arithmetic circuits (adders, etc.)
> - Function unit
> - **[[PWA Project|PWA Project Documentation]]** -- detailed notes on every module
>
> **Deliverables:**
> - [ ] PWA report
> - [ ] Multiple choice test (before 21 March)
> - [ ] Opg 2, Opg 3

### PWB -- MPU / Control Unit

> [!abstract] PWB
> **Goal:** Design and implement the Control Unit (MPU -- Micro Processing Unit)
> **Lectures:** 5-8
> **Deadline:** 02-04-2025 (Week 13)
>
> **Key components:**
> - Micro-operations and register transfer
> - Shift registers, counters
> - Control word and Datapath architecture
> - ASM (Algorithmic State Machines)
>
> **Deliverables:**
> - [ ] PWB report (template: [[templatePWB.dotx]])
> - [ ] Multiple choice test (before 25 April)
> - [ ] Opg 5, Opg 6

### PWF -- Final Microprocessor

> [!abstract] PWF
> **Goal:** Complete working soft microprocessor on FPGA hardware
> **Lectures:** 9-13
> **Final deadline:** 11-05-2025 (Week 19)
>
> **Key components:**
> - Memory design (Block RAM, FPGA memory)
> - Assembler language programming
> - I/O, interfaces & memory systems
> - CPU models
>
> **Deliverables:**
> - [ ] Video presentation (11-05)
> - [ ] Final report: PWA + PWB + PWF combined
> - [ ] Table of student responsibility areas
> - [ ] Opg 9 (simulation for PWA)

---

## Exam

> [!warning] Oral Exam
> **Dates:** 28-05 / 29-05-2026 (Week 20)
> **Format:** Oral examination
> **Coverage:** All pensum listed in the lesson plan table
> **Includes:** Slides, quizzes, MC tests, exercises, PWA/PWB/PWF reports

> [!warning] Multiple Choice Tests
> | Test | Deadline |
> |---|---|
> | MC test -- PWA | Before 21 March 2026 |
> | MC test -- PWB | Before 25 April 2026 |

---

## Lecture Notes

| Lec | Topic | Link |
|---|---|---|
| 1 | Digital Arithmetic | [[Lecture 01 - Digital Arithmetic]] |
| 2 | Arithmetic Circuits & ALU | [[Lecture 02 - Arithmetic Circuits & ALU]] |
| 3 | Digital Arithmetic -- Adders | [[Lecture 03 - Adders]] |
| 4 | PWA Function Unit | [[Lecture 04 - Function Unit]] |
| 5 | Micro-operations & Register Transfer | [[Lecture 05 - Micro-operations]] |
| 6 | Control Word & Datapath | [[Lecture 06 - Datapath Architecture]] |
| 7 | ASM & Control Transfer | [[Lecture 07 - ASM]] |
| 8 | Computer Design | [[Lecture 08 - Computer Design]] |
| 9 | Memory Design & FPGA Memory | [[Lecture 09 - Memory Design]] |
| 10 | Assembler Language | [[Lecture 10 - Assembler Programming]] |
| 11 | I/O & Memory Systems | [[Lecture 11 - IO and Memory Systems]] |
| 12 | CPU Models | [[Lecture 12 - CPU Models]] |
| 13 | PWF Completion | [[Lecture 13 - PWF Final]] |

---

## Quizzes & Exercises

> [!tip] Quizzes
> - [[Quiz 1]]
> - [[Quiz 2]]

> [!tip] Exercises
> - [[Opg 2 - Digital Arithmetic|Opg 2 -- Digital Arithmetic (notes)]]
> - [[opg2.doc|Opg 2 (original)]]
> - [[Opg 3 - Function Unit & Adder-Subtractor|Opg 3 -- Function Unit & Adder-Subtractor (notes)]]
> - [[opg3.pdf|Opg 3 (original)]]
> - [[opg5 - Copy.doc|Opg 5]]
> - [[test_eksempel.docx|Test eksempel]]
> - [[62711_ProjectWork_A_F2026.pdf|PWA Project Assignment]]

> [!tip] Solutions
> - [[opg3_solution_opdateret.pdf|Opg 3 solution]]
> - [[opg5_solution.pdf|Opg 5 solution]]
> - [[test_eksempel.pdf|Test eksempel solution]]

---

## Literature & Resources

### Course Materials
- [[62711_Lektionsplan_F2026.pdf|Lesson plan]]
- [[Assembler mockup guide_v4.pdf|Assembler mockup guide]]
- [[Rapport_template_v22.dotx|Report template]]
- [[templatePWB.dotx|PWB template]]

### Guides
- [[Installing Xilinx Vivado.pdf|Installing Xilinx Vivado]]
- [[Guide til vivado simulering.pdf|Vivado simulation]]
- [[Hints for using vhdl test benches in vivado.pdf|VHDL test benches]]
- [[Guide for generering af Block RAM.pdf|Block RAM generation]]
- [[guide for creating the bit file.ppt|Creating bit file]]
- [[Guide for getting a connection to the Gbar computer_updated.pdf|GBAR connection]]
- [[Guide for running xilinx vivado on gbar.pdf|Vivado on GBAR]]
- [[guide start af gbar-computer.pdf|Start GBAR]]
- [[WINSCP til at overfører filer til PC fra GBAR.pdf|WinSCP file transfer]]
- [[LinuxCommandLineCheatSheet.pdf|Linux cheat sheet]]

### VHDL References
- [[The_Practical_guide_to_VHDL_ver2_6.pdf|Practical guide to VHDL]]
- [[VHDL_guide.pdf|VHDL guide]]

### Textbook & Reference
- [[Logic and Computer Design Fundamentals 5th Edition.pdf|Textbook (full PDF)]]
- [[M_Morris_Mano_Charles_R_Kime-Logic_and_Computer_Design_Fundamentals-EN.pdf|Mano & Kime -- Logic and Computer Design Fundamentals]]
- [[manual_atrix_ddr4.pdf|Nexys 4 DDR manual]]

### Xilinx Documentation
- [[ug473_7Series_Memory_Resources.pdf|7 Series Memory Resources (ug473)]]
- [[ug835-vivado-tcl-commands.pdf|Vivado TCL Commands (ug835)]]
- [[ug892-vivado-design-flows-overview.pdf|Vivado Design Flows (ug892)]]
- [[ug903-vivado-using-constraints.pdf|Vivado Constraints (ug903)]]
- [[ug953-vivado-7series-libraries.pdf|7 Series Libraries (ug953)]]
- [[vivado-logic-simulation-pages-239_TCL_commands.pdf|Vivado Logic Simulation TCL]]

### Slides
- [[62711_lesson1_f2026.pdf|Lesson 1]]
- [[62711_lesson2_f2026.pdf|Lesson 2]]
- [[62711_lesson3_f2026.pdf|Lesson 3]]
- [[Lecture_01_Preparation.pdf|Lecture 01 Preparation]]
- [[Preparation slides lecture 2.pdf|Lecture 02 Preparation]]
- [[Preparation slides lesson 3.pdf|Lecture 03 Preparation]]
- [[Eksempel på multiplexer og decoder med when else.pdf|Multiplexer & decoder example]]
- [[Example_Flip-flops.pdf|Flip-flops example]]
- [[05_Carrylookahead_supp4.pdf|Carry-lookahead (supplement)]]
- [[06_Mulitpliers_Dividers_supp4.pdf|Multipliers & Dividers (supplement)]]

---

## Quick Reference

> [!tip] Vivado -- Open Project via TCL
> ```tcl
> cd "C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/Vivado/Adder_Test"
> source create_project.tcl
> ```

> [!tip] Team Repo
> ```bash
> cd "4. Semester/Digital Systems Design/team"
> git pull
> ```
> See [[Team Workflow]] for full workflow.

> [!info] Board Specs
> **Board:** Digilent Nexys 4 DDR
> **FPGA:** Xilinx Artix-7 XC7A100T-1CSG324C
> **Constraints:** [[Nexys_4_DDR_Master.xdc]]
