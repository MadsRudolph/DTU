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

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| 5 | | 1 | Introduction | Intro to feedback control, Pre-Test | |
| 6 | | 2 | Control concepts | Block diagrams, hand tuning, Z-N | |
| 7 | 18/02 | 3 | Transfer function & Laplace | Laplace transform, phasors, block diagrams | x |
| 8 | | 4 | Frequency domain | Frequency domain properties | |
| 9 | | 5 | Modelling & Linearization | White/black box modelling | |
| 10 | | 6 | Bode plots & Stability | Bode plot, stability margins, P-design | |

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
> - [[Pretest Answers|Pretest -- Math, Physics, Frequency, MATLAB]]
> - [[Day1_MATLAB_Exercise.pdf|Exercise 1 PDF]]
> - [[matlabexercise.pdf|MATLAB Exercise PDF]]
> - [[Exercises_Day3.pdf|Exercise 3 PDF]]
> - [[Assignment_3_BlockDiagrams.pdf|Assignment 3 -- Block Diagrams]]

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
