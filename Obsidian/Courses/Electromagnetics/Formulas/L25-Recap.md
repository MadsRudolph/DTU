
---
title: Electromagnetics — Final Exam Recap Formula Sheet
type: formula
tags: [Electromagnetics, Exam, Recap, TL, PlaneWaves, Electrostatics, Magnetostatics]
aliases: [EM Exam Formula Sheet, EM Recap]
___
# ⚡ 30035 Engineering Electromagnetics — Final Exam Recap  
**DTU · Rasmus E. Jacobsen · Fall 2025**  
**Exam format: Multiple-choice, no negative penalty**

---

# 0. Exam Structure & Strategy

## Format
- X assignments, each with multiple MC questions  
- Typically **4 answer options**, only **1 correct**  
- Correct answer → **Y %**  
- Incorrect → **0 %**  

## Strategy
> [!tip] Exam Strategy  
> - First scan: solve all **easy** questions  
> - Leave computationally heavy / unfamiliar ones for second pass  
> - Try option-testing when unsure  
> - No negative points — **answer everything**

> [!info] Bring a mini-sheet  
> Include constants:  
> - $ε_0$, $μ_0$, $η_0$, $c$  
> - Common wave, TL, and boundary equations

---

# 1. Transmission Lines (TLs)  
🟥 **Exam-critical**

## 1.1 TL Basics
| Quantity | Formula | Meaning |
|---------|---------|---------|
| Propagation constant | $\gamma = \alpha + j\beta$ | Loss + phase |
| Characteristic impedance | $Z_0 = \sqrt{\frac{R'+j\omega L'}{G'+j\omega C'}}$ | Wave impedance |
| Input impedance | $Z_\text{in}$ | TL-transformed load |

### Lossless TL (common exam case)
$$
Z_0 \in \mathbb{R},\quad \gamma = j\beta
$$

Reflection coefficient:
$$
\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}
$$

Input reflection:
$$
\Gamma_\text{in} = \Gamma_L e^{-j2\beta \ell}
$$

Input impedance:
$$
Z_\text{in} = Z_0\,\frac{Z_L + j Z_0 \tan(\beta \ell)}{Z_0 + j Z_L \tan(\beta \ell)}
$$

VSWR:
$$
\text{VSWR} = \frac{1+|\Gamma|}{1-|\Gamma|}
$$

---

## 1.2 Special TL Lengths  
🟥 memorise!

### Half-wave line ($\ell = λ/2$):
$$
Z_\text{in} = Z_L,
\quad
\Gamma_\text{in} = \Gamma_L
$$

### Quarter-wave line ($\ell = λ/4$):
Impedance inverter:
$$
Z_\text{in} = \frac{Z_0^2}{Z_L}
$$

Reflection flips sign:
$$
\Gamma_\text{in} = -\Gamma_L
$$

---

## 1.3 Stubs  
Single-stub tuner condition:
$$
Y_B = G_0 + j(B_\text{in} + B_S)
\quad \Rightarrow \quad
B_S = -B_\text{in}
$$

Short-circuited stub:
$$
Z_\text{stub} = j Z_0 \tan(\beta \ell)
$$

Open-circuited stub:
$$
Z_\text{stub} = -j Z_0 \cot(\beta \ell)
$$

---

## 1.4 Power  
Time-average power:
$$
\bar P = \frac{1}{2}\Re\{ \tilde V\, \tilde I^* \}
$$

Available power from generator:
$$
P_\text{av} = \frac{|V_0|^2}{8 R_g}
$$

Delivered power (lossless TL):
$$
P_L = P_\text{av}(1 - |\Gamma_L|^2)
$$

---

## 1.5 Smith Chart Essentials  
🟧 important

Key identities:
$$
\Gamma = \frac{z - 1}{z + 1},
\qquad z = r + jx
$$

Admittance:
$$
y = \frac{1}{z}
$$

Movement **towards generator** → rotation **clockwise**.

SWR circle: constant $|\Gamma|$.

---

# 2. Plane Waves  
🟥 **Exam-critical**

## 2.1 Maxwell + Wave Equation
In source-free homogeneous medium:
$$
\nabla^2 \mathbf{E} - \gamma^2 \mathbf{E} = 0
$$

Propagation constant:
$$
\gamma^2 = -\omega^2 μ ε_c
$$

Complex permittivity:
$$
ε_c = ε - j\frac{σ}{\omega}
$$

---

## 2.2 Plane-Wave Fields
For a uniform plane wave:
$$
\tilde{\mathbf{E}} = \tilde{E}_0 e^{-\gamma z}
$$
$$
\tilde{\mathbf{H}} = \frac{1}{η}\hat{k} \times \tilde{\mathbf{E}}
$$

Intrinsic impedance:
$$
η = \sqrt{\frac{μ}{ε_c}}
$$

Phase velocity:
$$
u_p = \frac{\omega}{\beta} = \frac{1}{\sqrt{μ ε}}
$$

---

## 2.3 Power Density (Poynting)
$$
\mathbf{P} = \frac{1}{2}\Re\{\mathbf{E} \times \mathbf{H}^*\}
$$

---

## 2.4 Reflection & Transmission (Normal Incidence)
Reflection coefficient:
$$
\Gamma = \frac{η_2 - η_1}{η_2 + η_1}
$$

Transmission coefficient:
$$
t = \frac{2η_2}{η_2 + η_1}
$$

Reflectance / Transmittance:
$$
R = |\Gamma|^2,
\quad T = 1 - R
$$

---

## 2.5 Oblique Incidence (TE/TM)
Snell’s law:
$$
n_1 \sin\theta_i = n_2 \sin\theta_t
$$

TE (“⊥”) and TM (“∥”) have **different** Fresnel coefficients.

Brewster angle (TM polarization):
$$
\tan\theta_B = \frac{n_2}{n_1}
$$

Critical angle (total internal reflection):
$$
\sin\theta_c = \frac{n_2}{n_1}
$$

---

# 3. Coordinate Systems + Vector Calculus  
🟧 important

## Coordinate transforms
Cartesian → Cylindrical:
$$
r=\sqrt{x^2+y^2},\quad \phi=\tan^{-1}\frac{y}{x}
$$

Cartesian → Spherical:
$$
R=\sqrt{x^2+y^2+z^2},\quad
\theta=\cos^{-1}\frac{z}{R}
$$

---

## Differential Operators
Gradient:
$$
\nabla V
$$

Divergence:
$$
\nabla\cdot \mathbf{A}
$$

Curl:
$$
\nabla\times\mathbf{A}
$$

Gauss:
$$
\oint_S \mathbf{E}\cdot d\mathbf{s} = \frac{Q_\text{free}}{ε}
$$

Stokes:
$$
\oint_C \mathbf{E}\cdot d\ell =
\int_S (\nabla\times\mathbf{E})\cdot d\mathbf{s}
$$

---

# 4. Electrostatics  
🟥 **Exam-critical**

## 4.1 Laws
Coulomb:
$$
\mathbf{E} = \frac{1}{4\pi ε}\frac{q}{R^2}\hat{R}
$$

Gauss:
$$
\nabla\cdot \mathbf{D} = ρ_v
$$

Potential:
$$
V(B)-V(A)= -\int_A^B \mathbf{E}\cdot d\ell
$$

---

## 4.2 Conductors
- $E=0$ inside conductor  
- $V=\text{const}$  
- Surface charge density:
$$
ρ_s = \hat{n}\cdot \mathbf{D}
$$

Field direction: **perpendicular to surface**.

Charge accumulates at **sharp edges** (field enhancement → breakdown risk).

---

## 4.3 Boundary Conditions  
Between two dielectrics:
$$
\hat{n}\cdot(D_1 - D_2) = ρ_s
$$
$$
E_{1t} = E_{2t}
$$

Dielectric–conductor:
$$
E_t = 0,
\qquad \hat{n}\cdot D = ρ_s
$$

---

## 4.4 Dielectric Strength
Maximum field before breakdown:
$$
E_\text{max}
$$

Example values:
- Air: $3 \times 10^6$ V/m  
- Mica: $200 \times 10^6$ V/m  

---

## 4.5 Capacitors
Parallel-plate:
$$
C = \frac{εA}{d}
$$

Two-wire line:
$$
C' = \frac{\pi ε}{\operatorname{arcosh}(d/2R)}
$$

Energy:
$$
W = \frac{1}{2} C V^2
$$

---

# 5. Magnetostatics  
🟥 **Exam-critical**

## 5.1 Laws
Ampère’s law:
$$
\nabla\times \mathbf{H} = \mathbf{J}
$$

Gauss for magnetism:
$$
\nabla\cdot \mathbf{B} = 0
$$

---

## 5.2 Magnetic Field of Currents
Long straight wire:
$$
H = \frac{I}{2\pi r}
$$

Biot–Savart:
$$
d\mathbf{B} = \frac{μ_0}{4\pi}\frac{I\, d\boldsymbol{\ell}\times\hat{R}}{R^2}
$$

---

## 5.3 Magnetic Materials
$$
\mathbf{B} = μ \mathbf{H}
$$

---

## 5.4 Inductance
Solenoid:
$$
L = μ N^2 \frac{A}{\ell}
$$

Flux linkage:
$$
\lambda = N Φ
$$

Energy:
$$
W = \frac{1}{2} L I^2
$$

---

# ✔️ Summary Table — Core Exam Formulas

| Concept | Formula | When to Use |
|--------|---------|--------------|
| Reflection coefficient | $\Gamma=\frac{Z_L-Z_0}{Z_L+Z_0}$ | TL, matching, SWR |
| Input reflection | $\Gamma_\text{in}=\Gamma_L e^{-j2\beta\ell}$ | TL distance from load |
| Quarter-wave TL | $Z_\text{in}=\frac{Z_0^2}{Z_L}$ | $\ell=λ/4$ transformer |
| Plane-wave impedance | $η=\sqrt{\frac{μ}{ε_c}}$ | Field relation $E↔H$ |
| Snell's law | $n_1\sinθ_i = n_2\sinθ_t$ | Oblique incidence |
| Poynting vector | $\bar{P}=\frac12\Re\{E×H^*\}$ | Power density |
| Coulomb | $E = \frac{1}{4\pi ε}\frac{q}{R^2}$ | Point charge |
| Boundary cond. | $E_t\ \text{continuous},\ n\cdot D=ρ_s$ | Interfaces |
| Ampère | $\nabla\times H = J$ | Current-generated fields |
| Solenoid inductance | $L = μN^2A/\ell$ | Coils, magnetics |

---
