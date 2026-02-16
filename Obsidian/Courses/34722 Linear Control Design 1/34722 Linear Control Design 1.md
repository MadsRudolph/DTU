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
> **Lecturers:** TBD
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
| | | | *To be filled when schedule is available* | | |

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
> - [[Pretest Answers|Pretest -- Math, Physics, Frequency, MATLAB]]
> - [[Day1_MATLAB_Exercise.pdf|Exercise 1 PDF]]
> - [[matlabexercise.pdf|MATLAB Exercise PDF]]

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

---

## Literature & Resources

*To be added as course materials become available.*

---

## Formulas

> [!abstract] Key Formulas
> | Quantity | Formula |
> |----------|---------|
> | Transfer function | $G(s) = \frac{N(s)}{D(s)}$ |
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
> ```
