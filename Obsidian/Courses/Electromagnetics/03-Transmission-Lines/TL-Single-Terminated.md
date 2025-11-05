---
title: "TL Single Terminated"
type: formula
tags:
  - electromagnetics
  - formula
  - transmission-lines
aliases: []
links:
  formulas: []
  related: []
updated: 2025-10-28
updated: "2025-11-05"
tags: [electromagnetics, transmission-lines, formula]
---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane-Waves]] · [[MOC – Transmission-Lines]] · [[MOC – EM Loss & Skin Depth]]

# Electromagnetism – Single Terminated Transmission Line

---

## Reflection Coefficient at the Load
$$
\Gamma_B = \frac{Z_L - Z_0}{Z_L + Z_0}
$$
- $Z_L =$ load impedance, $Z_0 =$ characteristic impedance.  
- $|\Gamma_B|=0$ → matched load, no reflection.  
- $|\Gamma_B|=1$ → total reflection.  

🔗 Related: [[TL-Fundamentals]] — uses $Z_0$ from line fundamentals.  

---

## Reflection Coefficient at TL Input
$$
\Gamma_A = \Gamma_B e^{-2\gamma \ell}
$$
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Wave-Parameters]] — depends on $\beta$ (phase constant) through $\gamma = j\beta$.  

---

## Input Impedance at TL Input
$$
Z_A = Z_0 \frac{Z_L + Z_0 \tanh(\gamma \ell)}{Z_0 + Z_L \tanh(\gamma \ell)}
$$
For **lossless line**:  
$$
Z_A = Z_0 \frac{Z_L + jZ_0 \tan(\beta \ell)}{Z_0 + jZ_L \tan(\beta \ell)}
$$  
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Wave-Parameters]] — $\beta$ determines impedance oscillation along the line.  

---

## Voltage Standing-Wave Ratio (VSWR)
$$
S = \frac{1+|\Gamma|}{1-|\Gamma|}
$$
- $S=1$ → matched line.  
- $S \to \infty$ → short/open circuit.  

🔗 Related: [[Wave-Parameters]] — standing wave pattern spacing is set by $\lambda$.  

---

## Standing Wave Locations
- **Voltage maxima:**  
$$
d_1 = \frac{\phi_B}{2\pi}\lambda + n\frac{\lambda}{2}
$$
- **Voltage minima:**  
$$
d_2 = \frac{\phi_B}{2\pi}\lambda + \frac{\lambda}{4} + n\frac{\lambda}{2}
$$

where $\phi_B = \arg(\Gamma_B)$.  

🔗 Related: [[Wave-Parameters]] — position depends on $\lambda$ and $\beta$.  

---

## Wave Impedance Along the Line
$$
Z(d) = Z_0 \frac{1 + \Gamma_B e^{-j2\beta d}}{1 - \Gamma_B e^{-j2\beta d}}
$$
- Oscillates between max/min depending on $d$.  
- Reduces to $Z_0$ for matched load ($\Gamma=0$).  

🔗 Related: [[TL-Fundamentals]] — $Z_0$ comes from per-unit-length $L'$ and $C'$.
---

**See also:** [[MOC – Electromagnetics]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]

Recent in same folder

```dataview
LIST FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.mtime desc
LIMIT 5
```


Outgoing links

```dataview
LIST FROM outgoing([[]])
WHERE contains(file.path,"Courses/Electromagnetics")
```
