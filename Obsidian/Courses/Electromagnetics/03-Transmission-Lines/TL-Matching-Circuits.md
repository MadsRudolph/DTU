---
title: "TL Matching Circuits"
type: "formula"
tags: [electromagnetics, transmission-lines, formula]
aliases: []
links: {"formulas": [], "related": []}
updated: "2025-10-28"


---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane-Waves]] · [[MOC – Transmission-Lines]] · [[MOC – EM Loss & Skin Depth]]

*(Based on Lecture 10 slides + Ulaby Ch. 3-1 & 7-1)*

---

## 1️⃣ Telegrapher’s Equations (Ch. 3-1)

### Differential form (time domain)
For an incremental section Δz with line parameters per unit length:
- Series resistance R′ [Ω/m]  
- Series inductance L′ [H/m]  
- Shunt conductance G′ [S/m]  
- Shunt capacitance C′ [F/m]

$$
\begin{aligned}
-\frac{\partial v(z,t)}{\partial z} &= R' i(z,t) + L' \frac{\partial i(z,t)}{\partial t} \\
-\frac{\partial i(z,t)}{\partial z} &= G' v(z,t) + C' \frac{\partial v(z,t)}{\partial t}
\end{aligned}
$$

---

### Phasor form
Assuming $e^{j\omega t}$ dependence:
$$
\frac{dV(z)}{dz}=-(R'+j\omega L')I(z),
\qquad
\frac{dI(z)}{dz}=-(G'+j\omega C')V(z)
$$

Differentiate again → **wave equations:**
$$
\frac{d^2V}{dz^2}=\gamma^2V,
\qquad
\frac{d^2I}{dz^2}=\gamma^2I
$$

---

### Propagation constant and Characteristic impedance
$$
\boxed{
\gamma=\sqrt{(R'+j\omega L')(G'+j\omega C')}
\quad , \quad
Z_0=\sqrt{\frac{R'+j\omega L'}{G'+j\omega C'}}
}
$$

- $\gamma=\alpha+j\beta$  
 → α = attenuation constant [Np/m], β = phase constant [rad/m]  
- Lossless line (\(R′=G′=0\)):   
 $\gamma=j\beta=j\omega\sqrt{L′C′}$,  $Z_0=\sqrt{L′/C′}$

---

## 2️⃣ Forward & Reflected Waves

### Voltage and Current along the line
$$
\begin{aligned}
V(z)&=V_0^+ e^{-\gamma z}+V_0^- e^{+\gamma z}\\
I(z)&=\frac{V_0^+}{Z_0} e^{-\gamma z}-\frac{V_0^-}{Z_0} e^{+\gamma z}
\end{aligned}
$$

---

### Reflection Coefficient (at the load)
$$
\boxed{
\Gamma_L=\frac{Z_L-Z_0}{Z_L+Z_0}
}
\quad\Rightarrow\quad
V_0^-=\Gamma_L V_0^+
$$

At a distance ℓ from the load:
$$
\Gamma_{\text{in}}=\Gamma_L e^{-2\gamma\ell}
$$

Normalized impedance:
$$
z_{\text{in}}=\frac{Z_{\text{in}}}{Z_0}
=\frac{1+\Gamma_{\text{in}}}{1-\Gamma_{\text{in}}}
$$

---

## 3️⃣ Power Relations (Ch. 7-1 + Lecture 10 “Power: Something was forgotten!”)

### Time-average power in phasor form
$$
\bar{P}=\tfrac{1}{2}\Re\{V I^*\}
$$

### Power from generator to line
For available generator power:
$$
\bar{P}_{\text{av}}=\frac{|\tilde V_0|^2}{8R_g}
$$

Delivered power to load (lossless line):
$$
\boxed{
\bar{P}_L=\bar{P}_{\text{av}}(1-|\Gamma_L|^2)
}
$$

Reflected power:
$$
\bar{P}_r=|\Gamma_L|^2 \bar{P}_{\text{av}}
$$

Lossy line:
$$
\bar{P}_L=\bar{P}_{\text{av}} e^{-2\alpha\ell}(1-|\Gamma_L|^2)
$$

---

### Standing-Wave Ratio (VSWR)
$$
S=\frac{1+|\Gamma_L|}{1-|\Gamma_L|}
$$

Voltage max/min:
$$
V_{\max,\min}=|V_0^+|(1\pm|\Gamma_L|)
$$

---

## 4️⃣ Series and Parallel TL Connections (Lecture Slides 7–8)

### Series connection of two lines
For sections 1 and 2 with $\gamma_1,\gamma_2$ and $Z_{01},Z_{02}$:
$$
Z_B=Z_{01}\frac{Z_L+Z_{01}\tanh(\gamma_1\ell_1)}{Z_{01}+Z_L\tanh(\gamma_1\ell_1)}
$$
$$
Z_A=Z_{02}\frac{Z_B+Z_{02}\tanh(\gamma_2\ell_2)}{Z_{02}+Z_B\tanh(\gamma_2\ell_2)}
$$

### Parallel connection
$$
Z_{A1}=Z_{01}\frac{Z_{L1}+Z_{01}\tanh(\gamma_1\ell_1)}{Z_{01}+Z_{L1}\tanh(\gamma_1\ell_1)},\quad
Z_{A2}=Z_{02}\frac{Z_{L2}+Z_{02}\tanh(\gamma_2\ell_2)}{Z_{02}+Z_{L2}\tanh(\gamma_2\ell_2)}
$$
$$
Z_A=\frac{Z_{A1}Z_{A2}}{Z_{A1}+Z_{A2}}
$$

---

## 5️⃣ Smith Chart Relations (Slides 9–12)

- Normalized impedance and reflection coefficient:
  $$
  \Gamma=\frac{z-1}{z+1},\qquad z=r+jx
  $$
- Lines of constant $r$ → circles (center on real axis)  
- Lines of constant $x$ → arcs through center (vertical)  
- Use for:
  - Visualizing $\Gamma_{\text{in}}$ rotation with line length ($2βℓ$)
  - Impedance matching and VSWR evaluation

---

## 6️⃣ Quarter-Wave Transformer (λ/4 Matching)

Used to match a real load $R_L$ to line impedance $Z_0$:
$$
\boxed{
Z_{0,\text{qw}}=\sqrt{Z_0 R_L}
}
$$
Length $\ell_{\text{qw}}=\lambda/4$.

General (load complex): use a short intermediate line to make load real before λ/4 section.

---

## 7️⃣ Stub Tuning (Matching with Reactive Stubs)

- Stub types: short-circuited or open-circuited.  
- Impedance seen into stub:
  - Short: $Z_A=jZ_0\tan(βℓ)$  
  - Open: $Z_A=-jZ_0\cot(βℓ)$
- Reactive component $jX_c$ replaced by a stub length ℓs such that:
  $$
  X_c=Z_0 \tan(βℓ_s)
  $$

---

## 8️⃣ Practical Matching Summary (Lecture Slides 13–20)

| Technique             | Type              | Key Formula                     | Notes                     |
| --------------------- | ----------------- | ------------------------------- | ------------------------- |
| λ/4 Transformer       | Transmission line | $Z_{0,\text{qw}}=\sqrt{Z_0Z_L}$ | Matches real loads only   |
| Single-Stub Tuner     | TL + stub         | $Y_M=Y_M'+jB_c$                 | Adjusts for complex load  |
| Lumped Elements       | L, C components   | $X=jωL$, $B=jωC$                | Equivalent near resonance |
| Series / Parallel TLs | Two sections      | $Z_{eq}$ formulas above         | Multi-stage matching      |
| Smith Chart Design    | Graphical         | $\Gamma=\frac{z-1}{z+1}$        | Visual solution           |

---

## 9️⃣ Power and Efficiency

- Forward power: $(P_f=|V_0^+|^2/(2Z_0))$  
- Reflected power: $(P_r=|V_0^-|^2/(2Z_0))$  
- Delivered power: $(P_L=P_f-P_r=P_f(1-|\Gamma_L|^2))$

Lossless line: total power constant along z.  
Lossy line: power decays as \(e^{-2αz}\).

---

## 🔟 Summary of Key Quantities

| Symbol              | Quantity                    | Formula / Definition                                   | Units                                                    |
| :------------------ | :-------------------------- | :----------------------------------------------------- | :------------------------------------------------------- |
| $R',\,L',\,G',\,C'$ | Line parameters per length  | material & geometry dependent                          | $\Omega/\text{m},\,\text{H/m},\,\text{S/m},\,\text{F/m}$ |
| $\gamma$            | Propagation constant        | $\sqrt{(R' + j\omega L')(G' + j\omega C')}$            | $1/\text{m}$                                             |
| $Z_0$               | Characteristic impedance    | $\sqrt{\frac{R' + j\omega L'}{G' + j\omega C'}}$       | $\Omega$                                                 |
| $\Gamma_L$          | Load reflection coefficient | $\frac{Z_L - Z_0}{Z_L + Z_0}$                          | –                                                        |
| $S$                 | VSWR                        | $\frac{1+\lvert\Gamma\rvert}{1-\lvert\Gamma\rvert}$    | –                                                        |
| $P_{\text{av}}$     | Available source power      | $\frac{\lvert V_0\rvert^2}{8R_g}$                      | W                                                        |
| $P_L$               | Delivered power             | $P_{\text{av}}\!\left(1-\lvert\Gamma_L\rvert^2\right)$ | W                                                        |

---

🔗 **Cross-References**


---

🧭 **Conceptual Summary**
- Transmission lines bridge circuit and field theory.  
- Telegrapher’s equations ⟺ Maxwell’s wave equations in 1-D.  
- Power reflection and matching critical for max transfer.  
- Smith chart visualizes Γ, Z, Y transformations along line.  
- Matching networks (λ/4, stub) cancel reactance and improve power delivery.

---
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
