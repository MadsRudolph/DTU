---
title: "Week 1 – Tuesday"
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

## Analog vs Digital Signal Processing
- Analog filters: **low-pass, high-pass, band-pass, band-stop**
- DSP chain:  
  $$
  x_a(t) \;\xrightarrow{\text{A/D, sampling}} x_d[n] 
  \;\xrightarrow{\text{digital filter}} y_d[n] 
  \;\xrightarrow{\text{D/A}} y_a(t)
  $$

- Sampling period: $T_s$, frequency $F_s = 1/T_s$

---

🔗 **References**
- [[Week 1 – Thursday]]: Formal definition of discrete-time signals
- [[Week 2 – Thursday]]: Frequency analysis of sampled signals
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
