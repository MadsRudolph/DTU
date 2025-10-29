---
title: "Exercise 1 – Frequency Response of LTI System"
type: "exercise"
tags:
- DSP
- exercise
- General
aliases: []
links:
  formulas: []
  related: []
updated: "2025-10-28"
---
> 🔗 [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]] · [[Formulas/Week 3 – Tuesday]]
> **Quick refs (DSP):** [[Formulas/Week 1 – Tuesday]] · [[Formulas/Week 2 – Tuesday]] · [[Formulas/Week 3 – Tuesday]]


> **Quick refs:** [[MOC – DSP]] · [[MOC – Exercises (DSP)]] · [[MOC – Lectures (DSP)]]

# Exercise 1 – Frequency Response of LTI System

A causal and stable LTI system is determined by the difference equation:

$$
y[n] - \tfrac{3}{4}y[n-1] + \tfrac{1}{8}y[n-2] = x[n]
$$

Where $x[n]$ and $y[n]$ are respectively the input and output of the system.

---

## 1. Frequency Response
Determine the frequency response $H(\omega)$ of the system and show that it can be written as:

$$
H(\omega) = \frac{1}{\big(1 - \tfrac{1}{2}e^{-j\omega}\big)\big(1 - \tfrac{1}{4}e^{-j\omega}\big)}
$$

---

## 2. Magnitude and Phase Response
- Magnitude response:  

$$
|H(\omega)| = \frac{1}{\left(\tfrac{5}{4} - \cos(\omega)\right)\left(\tfrac{17}{16} - \tfrac{1}{2}\cos(\omega)\right)}
$$

- Phase response:  

$$
\angle H(\omega) = -\arctan\!\left(\frac{\sin(\omega)}{2 - \cos(\omega)}\right)
- \arctan\!\left(\frac{\sin(\omega)}{4 - \cos(\omega)}\right)
$$

---

## 3. Graphs
[Open MatLab File](file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE3/exercise-1-tirsdag.mlx)



![[MagnitudeResponse.png]]

![[PhaseResponse.png]]

---

## 4. Solution
![[Uge 3.pdf]]
---

**See also:** [[MOC – DSP]]

Recent in same folder

```dataview
LIST FROM "Courses/DSP"
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.mtime desc
LIMIT 5
```


Outgoing links

```dataview
LIST FROM outgoing([[]])
WHERE contains(file.path,"Courses/DSP")
```