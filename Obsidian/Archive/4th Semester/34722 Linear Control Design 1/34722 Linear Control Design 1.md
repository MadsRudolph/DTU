---
course: "34722"
course-name: "Linear Control Design 1"
type: home
cssclass: course-home
tags: [LCD, home]
---
# 34722 Linear Control Design 1

> [!info] Course Information
> **Course:** 34722 Linear Control Design 1
> **Semester:** Spring 2026 (4th semester)
> **Lecturers:** Silvia Tolu & Dimitrios Papageorgiou
> **ECTS:** 5
> **Textbook:** TBD
> **Robot:** Regbot (balance robot)
> **Exam:** Written exam
> **Teaching:** Lectures + Lab exercises with Regbot

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34722)
> - [[Regbot GUI|Regbot GUI setup]]
> - [[DTU Study Path|Study path context]]
> - [[Fundamentals - Intuitive Control Theory|Fundamentals Guide — Intuition-first study reference]]
> - [[Diagnostic Guide - What Went Wrong|Diagnostic Guide — Troubleshooting symptoms & fixes]]
> - [[Worked Example - REGBOT Position Controller|Worked Example — PILead design start-to-finish]]
> - [[Midterm Cheatsheet|Midterm Cheatsheet — Formulas & quick reference]]

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| 5 | | 1 | Introduction | Intro to feedback control, Pre-Test | x |
| 6 | | 2 | Control concepts | Block diagrams, hand tuning, Z-N | x |
| 7 | 18/02 | 3 | Transfer function & Laplace | Laplace transform, phasors, block diagrams | x |
| 8 | 25/02 | 4 | Frequency domain | Frequency domain properties, poles, zeros | x |
| 9 | | 5 | Modelling & Linearization | White/black box modelling | x |
| 10 | | 6 | Bode plots & Stability | Bode plot, stability margins, P-design | x |
| 11 | | 7 | Nyquist plot & Stability | Nyquist criterion, stability analysis | x |
| 12 | | 8 | PI-Lead Design | PI-Lead controller, phase balance equation | x |
| 13 | 08/04 | 9 | PI-Lead with Specifications | Closed-loop specs, bandwidth, type-n systems | x |
| 15 | 15/04 | 10 | Unstable systems | Instability, stabilising open-loop unstable systems via Nyquist, cascaded control for REGBOT balance | |

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> Control theory is fundamental to audio system design:
> - Feedback loop analysis for amplifier stability
> - PID controllers for active speaker crossovers
> - Bode plot analysis (frequency response)
> - Transfer function manipulation (used daily in analog design)

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34722 Linear Control Design 1/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Tools

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34722 Linear Control Design 1/Exercises"
WHERE type = "exercise" OR type = "quiz"
SORT date ASC
```

> [!tip] Exercises
> - [[Day 1 - MATLAB Exercise|Day 1 -- MATLAB Basics, Transfer Functions, Robot Data]]
> - [[Day 2 - Hand-Tuning Exercise|Day 2 -- P/PI Hand-Tuning & Ziegler-Nichols]]
> - [[Day 3 - Block Diagram Exercise|Day 3 -- Block Diagrams & Transfer Functions]]
> - [[Day 3 - MATLAB Exercise|Day 3 -- MATLAB: Laplace, TFs & Frequency Response]]
> - [[Day 4 - REGBOT Introduction|Day 4 -- REGBOT Introduction & Motor Characterization]]
> - [[Day 5 - Black Box Modeling|Day 5 -- Black Box Modeling & System Identification]]
> - [[Day 6 - Bode and P-Controller Design|Day 6 -- Bode Plot & P-Controller Design]]
> - [[Day 8 - Position Controller|Day 8 -- PI-Lead Position Controller Design]]
> - [[Day 9 - PI-Lead with Specifications|Day 9 -- PI-Lead Design with Specifications]]
> - [[Pretest Answers|Pretest -- Math, Physics, Frequency, MATLAB]]
> - [[Day1_MATLAB_Exercise.pdf|Exercise 1 PDF]]
> - [[matlabexercise.pdf|MATLAB Exercise PDF]]
> - [[Exercises_Day3.pdf|Exercise 3 PDF]]
> - [[Assignment_3_BlockDiagrams.pdf|Assignment 3 -- Block Diagrams]]
> - [[Extra_Exercises_Day5.pdf|Extra Exercises Day 5 PDF]]
> - [[Theoretical Exercises LCD1.pdf|Theoretical Exercises 1-9 PDF]]

> [!tip] Quizzes
> - [[Quiz 1 - Block Diagrams and Control Concepts|Quiz 1 -- Block Diagrams & Control Concepts]]

---

## Tools & Setup

> [!tools] Regbot Robot
> Python GUI for controlling the Regbot balance robot.
> See [[Regbot GUI]] for full setup instructions.
>
> ```
> pip install pyqt5 pyserial pyqtgraph numpy
> python regbot.py
> ```

---

## Slides

- [[1_Welcome_Lecture.pdf|Lecture 1 -- Welcome]]
- [[2_block_control_concept.pdf|Lecture 2 -- Block Diagrams & Control Concepts]]
- [[3_Laplace_TF.pdf|Lecture 3 -- Laplace & Transfer Functions]]
- [[4_Frequency_and_Time_Analysis_NoSol.pdf|Lecture 4 -- Frequency & Time Analysis]]
- [[5_Modelling.pdf|Lecture 5 -- Modelling]]
- [[6_bode_plot_and_stability.pdf|Lecture 6 -- Bode Plots & Stability]]
- [[7_Nyquist_Plot_and_Stability.pdf|Lecture 7 -- Nyquist Plot & Stability]]
- [[8_PI_Lead_Design.pdf|Lecture 8 -- PI-Lead Design]]
- [[9_PI_Lead_Design_with_Specifications.pdf|Lecture 9 -- PI-Lead with Specifications]]
- [[Lecture_10_Unstable_systems.pdf|Lecture 10 -- Unstable Systems]]

---

## Literature & Resources

*To be added as course materials become available.*

---

## Formulas

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | Transfer function | $G(s) = \frac{N(s)}{D(s)}$ |
> | Closed-loop TF | $\frac{\text{Forward}}{1 + \text{Loop gain}}$ |
> | Laplace of integral | $\int f \to \frac{1}{s}F(s)$ |
> | Laplace of derivative | $\dot{f} \to sF(s) - f(0)$ |
> | Frequency response | $G(j\omega) = Me^{j\varphi}$ |
> | Final value theorem | $\lim_{t\to\infty}f(t) = \lim_{s\to 0}sF(s)$ |
> | Capacitor impedance | $Z_C = \frac{1}{sC}$ |
> | Inductor impedance | $Z_L = sL$ |
> | Complex magnitude | $\|V\| = \sqrt{a^2 + b^2}$ |
> | Complex phase | $\theta = \arctan(b/a)$ |
> | Newton 2nd law | $F = Ma$ |
> | Rotational | $\tau = I\dot{\omega}$ |

---

## Quick Reference

> [!tip] MATLAB Commands
> ```matlab
> G = tf(num, den);    % Create transfer function
> step(G, t);          % Step response
> impulse(G);          % Impulse response
> lsim(G, u, t);       % Arbitrary input response
> bode(G);             % Bode plot
> s = tf('s');          % Define s variable
> z = evalfr(G, w*i);  % Evaluate G at s = jw
> abs(z);              % Magnitude
> rad2deg(angle(z));   % Phase in degrees
> ```
