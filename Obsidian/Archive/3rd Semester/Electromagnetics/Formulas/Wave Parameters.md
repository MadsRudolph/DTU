---
title: "Electromagnetism – Wave Parameters"
type: "formula"
tags:
- Electromagnetics
  - formula
  - General
aliases: []
links:
  formulas: []
  related: []
updated: "2025-10-28"
---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane Waves]] · [[MOC – Transmission Lines]] · [[MOC – EM Loss & Skin Depth]]

# Electromagnetism – Wave Parameters

---

## Time Domain Representation
$$
y(x,t) = A_0 e^{-\alpha x} \cos(\omega t - \beta x - \phi_0)
$$
- $A_0$ = amplitude (maximum value)  
- $\alpha$ = attenuation constant (how fast the wave decays per meter)  
- $\beta$ = phase constant (how fast the phase changes per meter)  
- $\phi_0$ = initial phase (starting offset)  
- **Meaning:** A damped harmonic wave in time and space.  

🔗 Related: [[Transmission_Lines]] — $\beta$ and $\alpha$ are the same parameters used in the propagation constant $\gamma = \alpha + j\beta$.  

---

## Frequency / Phasor Domain
$$
\tilde{y}(x) = A_0 e^{-\alpha x} e^{-j\beta x} e^{-j\phi_0}
$$
- Uses Euler’s identity $e^{j\omega t}$ for compact representation.  
- **Meaning:** Convenient for analysis, since the time dependence $e^{j\omega t}$ is implicit.  

---

## Periodic in Time
**Angular frequency:**  
$$
\omega = 2\pi f = \frac{2\pi}{T}
$$  
- $f$ = frequency (Hz, oscillations per second)  
- $T$ = period (seconds per oscillation)  
- **Meaning:** How fast the wave repeats in time.  

---

## Periodic in Space
**Phase constant:**  
$$
\beta = \frac{2\pi}{\lambda}
$$  
- $\lambda$ = wavelength (m)  
- Units: rad/m  
- **Meaning:** How fast the phase changes in space – radians per meter.  

🔗 Related: [[Single Terminated TL]] — standing wave positions depend directly on $\beta$ and $\lambda$.  

---

## Phase Velocity
$$
u_p = \frac{\omega}{\beta} = \frac{\lambda}{T} = \lambda f
$$
- $u_p$ = phase velocity (m/s)  
- **Meaning:** Speed at which phase fronts (wave crests) move.
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
