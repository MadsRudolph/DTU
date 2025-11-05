---
title: "DTFT & Difference Equations"
type: "formula"
tags:
- DSP
- formula
- General
aliases: []
links:
  formulas: []
  related: []
updated: "2025-10-28"
---
> 🔗 [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]] · [[Formulas/Week 3 – Tuesday]]
> **Quick refs (DSP):** [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]]


> **Quick refs:** [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]]

# DTFT & Difference Equations

## Difference Equations
General form:  
$$
\sum_{k=0}^N a_k y[n-k] = \sum_{\ell=0}^M b_\ell x[n-\ell]
$$  
With initial rest → defines an LTI system

---

## DTFT
- Definition:  
  $$
  X(\omega)=\sum_{n=-\infty}^\infty x[n]e^{-jn\omega}
  $$
- Inverse:  
  $$
  x[n]=\frac{1}{2\pi}\int_{-\pi}^\pi X(\omega)e^{jn\omega}d\omega
  $$
- Periodicity: $X(\omega+2\pi)=X(\omega)$

---

## Parseval’s Theorem
$$
\sum_n |x[n]|^2 = \frac{1}{2\pi}\int_{-\pi}^\pi |X(\omega)|^2d\omega
$$

---

🔗 **References**
- [[Week 2 – Tuesday]]: Difference eqns ↔ impulse response
- [[Week 3 – Tuesday]]: DTFT properties (shift, modulation, etc.)
- [[Week 3 – Thursday]]: Z-transform generalizes DTFT
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
