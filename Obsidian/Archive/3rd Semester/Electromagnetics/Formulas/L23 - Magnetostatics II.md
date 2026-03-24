---
title: Magnetostatics II — Quick Formula Sheet
type: formula
tags: [Electromagnetics, Magnetostatics, Magnetization, Inductance]
aliases: [Magnetostatics II, Magnetic Materials, Inductors]
links:
  - "[[MOC – Electromagnetics]]"
  - "[[MOC – Lectures]]"
  - "[[MOC – Exercises]]"
  - "[[Lecture 22 - Magnetostatics I]]"
  - "[[L23_Magnetostatics_II.pdf]]"
updated: 2025-11-24
---

> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]]  
> **Quick refs:** [[Lecture 22 - Magnetostatics I]] · [[L23_Magnetostatics_II.pdf]] · Ulaby & Ravaioli Ch. 5-7 → 5-8  
> Exercises [[Exercise 20 - Magnetostatics]]    [[Home Assignment 3]]
> Based on **Lecture 23 – Magnetostatics II** (Rasmus E. Jacobsen, DTU Space).  
> Topics: B-field calculation methods, magnetic dipoles, magnetization & materials, boundary conditions, inductance, magnetic energy, typical devices.

---

## 🔁 Recap — Three Ways to Compute the B-Field

> [!note]  
> All three methods assume **steady currents (dc)** and **magnetostatics**.

### 1. Ampère’s Circuital Law
Integral equation:
$$
\oint_C \mathbf{B} \cdot d\mathbf{\ell} = \mu_0 I
$$

- Best for **high symmetry** (infinite wire, solenoid, toroid).
- Gives $\mathbf{B}$ directly from total current piercing the loop.

### 2. Biot–Savart’s Law
Field from current distribution along a filament $C$:
$$
\mathbf{B}(\mathbf{R}) = \frac{\mu_0 I}{4\pi}
\int_C \frac{d\mathbf{\ell}' \times (\mathbf{R} - \mathbf{R}')}{\lvert \mathbf{R} - \mathbf{R}' \rvert^3}
$$

- Integral expression, usually solvable analytically only for **simple geometries**.
- Always valid (even without symmetry) but often needs **numerical evaluation**.

### 3. Via the Vector Potential $\mathbf{A}$

First compute the vector potential:
$$
\mathbf{A}(\mathbf{R}) = \frac{\mu_0 I}{4\pi}
\int_C \frac{d\mathbf{\ell}'}{\lvert \mathbf{R} - \mathbf{R}' \rvert}
$$

Then take the curl:
$$
\mathbf{B} = \nabla \times \mathbf{A}
$$

- Also integral-based + curl.
- Useful in more advanced settings (radiation, numerical methods).

---

## 🌀 Circular Loop Current in Vacuum → Magnetic Dipole

Consider a circular loop of radius $a$ in the $xy$-plane carrying current $I$.

> [!info] **Far-field approximation (observation point far from the loop)**  
> Valid for $\lvert \mathbf{r} \rvert \gg a$.

Magnetic flux density:
$$
\mathbf{B}(\mathbf{r}) =
\frac{\mu_0 I \pi a^2}{4\pi \lvert\mathbf{r}\rvert^3}
\left(2 \cos\theta\, \hat{\mathbf{r}} + \sin\theta\, \hat{\boldsymbol{\theta}} \right),
\qquad (\lvert \mathbf{r} \rvert \gg a)
$$

Often we define the **magnetic moment**
$$
m = I \pi a^2
$$
so the field resembles that of a **magnetic dipole** with moment $\mathbf{m}$.

- Same **$1/r^3$ decay** and angular dependence as an *electric dipole* in electrostatics.
- Valid far away from the loop: either the loop is tiny, or the observation point is very far.

---

## ⚡ Electric vs Magnetic Dipole

> [!note] **Field pattern analogy**
> - Electric dipole: two opposite charges separated by a small distance → electric field $\mathbf{E}$ with characteristic dipole pattern.
> - Magnetic dipole: small current loop → magnetic flux density $\mathbf{B}$ with very similar dipole-like pattern far away.

- **Far away**: field lines of an electric dipole and a small current loop look almost identical.  
- **Close to the source**: field structures are different (loop has current distribution, electric dipole has point charges).

---

## 🧲 B-Field of a Bar Magnet vs Loop Current

- Bar magnet field lines outside the magnet look like those of a dipole (emerging from “N”, entering “S”).  
- A current loop produces a very similar pattern: outside the loop its $\mathbf{B}$ closely resembles that of a bar magnet.

> [!tip]
> This is why we often **model bar magnets as magnetic dipoles** in magnetostatic problems.

---

## 🧲 Magnetization of Materials

> [!note] **Magnetization from microscopic currents**
> - **Loop currents** generate $\mathbf{B}$ (just like our circular loop).  
> - On the microscopic level:  
>   - Orbiting electrons behave like tiny current loops.  
>   - Electron **spin** also contributes a magnetic moment.  
> - Random orientation → macroscopic field cancels → no net magnetization.  
> - External $\mathbf{B}$ can partially align these moments → **magnetization**.

We decompose $\mathbf{B}$ into contributions from **vacuum** and **material response**:
$$
\mathbf{B}
  = \mathbf{B}_0 + \mathbf{B}_M
  = \mu_0 \mathbf{H} + \mu_0 \mathbf{M}
  = \mu_0(\mathbf{H} + \mathbf{M})
$$

- $\mathbf{M}$ — **magnetization vector** [A/m], dipole moment per unit volume.  
- $\mathbf{H}$ — magnetic field intensity (due to **free currents**).  
- Compare to dielectrics: $\mathbf{D} = \varepsilon_0 \mathbf{E} + \mathbf{P}$ where $\mathbf{P}$ is polarization.

For a **simple linear medium**:
$$
\mathbf{M} = \chi_m \mathbf{H}
$$

where $\chi_m$ is the **magnetic susceptibility**.

---

## 🧭 Magnetic Susceptibility & Permeability

From $\mathbf{M} = \chi_m \mathbf{H}$ we get:
$$
\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M})
           = \mu_0(1 + \chi_m)\mathbf{H}
           = \mu_0 \mu_r \mathbf{H}
$$

Definitions:

- **Magnetic susceptibility**:  
  $$
  \mathbf{M} = \chi_m \mathbf{H}
  $$
- **Relative permeability**:  
  $$
  \mu_r = 1 + \chi_m
  $$
- **Absolute permeability**:  
  $$
  \mu = \mu_0 \mu_r
  $$

Where $\mu_0 = 4\pi\times10^{-7}\,\text{H/m}$ is the permeability of free space.

---

## 🧩 Types of Magnetic Materials

> [!info] From Ulaby Table 5-2 and lecture slides.

| Type | $\chi_m$ (sign & size) | $\mu_r$ | Field behavior | Common examples |
|:--|:--|:--|:--|:--|
| **Diamagnetic** | small, negative | $\mu_r \lesssim 1$ | Weakly *repelled* by external $\mathbf{B}$; induced moment opposite $ \mathbf{H}$ | Bismuth, copper, gold, water |
| **Paramagnetic** | small, positive | $\mu_r \gtrsim 1$ | Weakly *attracted*; induced moment aligns with $\mathbf{H}$ | Aluminum, oxygen, magnesium |
| **Ferromagnetic** | large, positive | $\mu_r \gg 1$ | Strong alignment of **domains**, can retain magnetization | Iron, nickel, cobalt |

Direction of $\mathbf{M}$ vs $\mathbf{H}$:

- Diamagnets: $\mathbf{M}$ anti-parallel to $\mathbf{H}$.  
- Paramagnets, ferromagnets: $\mathbf{M}$ parallel to $\mathbf{H}$.

---

## 🌀 Magnetic Hysteresis (Ferromagnets)

Ferromagnetic materials show a **non-linear** $\mathbf{B}-\mathbf{H}$ relation, described by the **hysteresis loop**.

Key points:

- **Saturation**: all domains aligned → $B$ no longer increases significantly with $H$.  
- **Residual flux density / remanence** $B_r$: remaining $B$ when $H$ is reduced back to zero.  
- **Coercive field** $H_c$: required $H$ in the opposite direction to bring $B$ back to zero.  
- Loop area ∝ **energy loss per magnetization cycle** (important for transformers, inductors).

> [!summary]
> Hysteresis = **memory effect** in ferromagnets: material “remembers” previous magnetization states.

---

## ⚖️ Rewriting Ampère’s Circuital Law in Magnetized Media

Originally (for total currents):
$$
\nabla \times \mathbf{B} = \mu_0 \mathbf{J}_\text{all}
$$

With $\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M})$:
$$
\nabla \times \big(\mu_0\mathbf{H} + \mu_0\mathbf{M}\big) = \mu_0 \mathbf{J}_\text{all}
$$

Divide by $\mu_0$:
$$
\nabla \times \mathbf{H} + \nabla \times \mathbf{M}
= \mathbf{J}_\text{all}
$$

Define:

- **Free current density**: $\mathbf{J}_\text{free}$ (currents in wires, sources),
- **Magnetization current density**: $\mathbf{J}_M = \nabla \times \mathbf{M}$,
- Total current: $\mathbf{J}_\text{all} = \mathbf{J}_\text{free} + \mathbf{J}_M$.

Then:
$$
\nabla \times \mathbf{H}
= \mathbf{J}_\text{all} - \nabla \times \mathbf{M}
= \mathbf{J}_\text{free}
$$

> [!important]
> In magnetostatics, **Ampère’s law in materials** is written in terms of $\mathbf{H}$ and **free** currents only:
> $$
> \nabla \times \mathbf{H} = \mathbf{J}_\text{free}
> $$

---

## 📏 Maxwell’s Equations in Magnetostatics

> [!info] Steady dc currents, no time-varying electric fields.

| Differential form | Integral form | Name |
|:--|:--|:--|
| $\nabla \times \mathbf{H} = \mathbf{J}_\text{free}$ | $\displaystyle \oint_C \mathbf{H}\cdot d\mathbf{\ell} = I_\text{free}$ | Ampère’s circuital law |
| $\nabla \cdot \mathbf{B} = 0$ | $\displaystyle \oint_S \mathbf{B}\cdot d\mathbf{s} = 0$ | Gauss’s law for magnetism |

- No magnetic monopoles → **normal component of $\mathbf{B}$ is continuous**.  
- $\mathbf{J}_\text{free}$ is the **current density of sources** (currents in conductors).

---

## 🌫️ Boundary Conditions in Magnetostatics

Interface between **medium 1** and **medium 2**, with outward normal $\hat{\mathbf{n}}$ pointing from 2 → 1.
![[Boundary_conditions.png]]
We use:

- $\displaystyle \oint_S \mathbf{B}\cdot d\mathbf{s} = 0$ over a small “pillbox” (thin Gaussian cylinder across interface).  
- $\displaystyle \oint_C \mathbf{H}\cdot d\mathbf{\ell} = I_\text{free}$ over a tiny rectangle straddling the interface.

Resulting boundary conditions:

1. **Normal component of $\mathbf{B}$ is continuous**
   $$
   B_{1n} = B_{2n}
   $$

2. **Tangential component of $\mathbf{H}$ jumps with surface current**
   $$
   \hat{\mathbf{n}} \times (\mathbf{H}_1 - \mathbf{H}_2) = \mathbf{J}_{S,\text{free}}
   $$
   where $\mathbf{J}_{S,\text{free}}$ is the **surface current density of free currents** [A/m].

> [!tip]
> If there is **no surface current** at the boundary, then the tangential components of $\mathbf{H}$ are also continuous.

---

## 🧮 Magnetic Force on a Moving Charge
![[magnetic_force.png]]
For a charge $q$ moving with velocity $\mathbf{u}$ in a magnetic field $\mathbf{B}$, the magnetic (Lorentz) force is:

$$
\mathbf{F}_m = q\, \mathbf{u} \times \mathbf{B}
$$

**Key properties**

- The force is **always perpendicular** to both $\mathbf{u}$ and $\mathbf{B}$.  
- For a **negative charge** ($q < 0$), the direction is **opposite** the right-hand rule.  
- Magnitude:
  $$
  F_m = |q|\,uB\sin\alpha
  $$
  where $\alpha$ is the angle between $\mathbf{u}$ and $\mathbf{B}$.

---

### 🔍 Direction of the Force (from the slide)

Given:

- $\mathbf{u}$ is in the **$+\hat{\boldsymbol{\phi}}$ direction** (tangential).
- $\mathbf{B}$ is **into the page** ($-\hat{\mathbf{z}}$).
- Charge is **negative** ($-q$).
- Using the cross product:
  $$
  \mathbf{u} \times \mathbf{B} = \hat{\boldsymbol{\phi}} \times (-\hat{\mathbf{z}}) = -(\hat{\boldsymbol{\phi}} \times \hat{\mathbf{z}})
  $$
- For a positive charge, this would point **radially inward** ($-\hat{\mathbf{r}}$).  
- Since the charge is **negative**, the final direction flips:

$$
\boxed{\mathbf{F}_m \propto +\hat{\mathbf{r}}}
$$

**Result:**  
The magnetic force on the particle points **radially outward**, along the $+\hat{\mathbf{r}}$ direction (exactly as shown on the slide).


---

## 🪫 Inductance & Inductor — Concepts

> [!note] **Analogy to capacitance**
> - **Capacitance**: stores energy in an **electric field**; resists change in voltage.  
> - **Inductance**: stores energy in a **magnetic field**; resists change in current.

- **Inductance** $L$ is a property of the magnetic field configuration and the geometry and material.  
- We distinguish:
  - **Self-inductance** (of a single circuit)  
  - **Mutual inductance** (between two circuits)

### Magnetic Flux and Flux Linkage

- Magnetic flux through an open surface $S$:
  $$
  \Phi = \int_S \mathbf{B}\cdot d\mathbf{s}
  $$
- For a coil with $N$ turns, the **flux linkage** is:
  $$
  \Lambda = N\Phi
  $$
![[Inductance_Inductor.png]]
---

## 🔗 Mutual Inductance

Consider two circuits (coils) with currents $I_1$ and $I_2$ and $N_1$, $N_2$ turns:
![[Mutual_Inductance.png]]
- Current $I_1$ in coil 1 produces flux that **links** coil 2.  
- Let $\Phi_{12}$ be the flux through a single turn of coil 2 caused by $I_1$.  
- Total flux linkage in coil 2:
  $$
  \Lambda_{12} = N_2 \Phi_{12} = N_2 \int_{S_2} \mathbf{B}_1 \cdot d\mathbf{s}
  $$

By definition, the **mutual inductance** $L_{12}$ is:
$$
L_{12} = \frac{\Lambda_{12}}{I_1}
$$

Similarly, $L_{21} = \Lambda_{21}/I_2$ if current flows in coil 2 and links coil 1.

> [!tip]  
> For linear, reciprocal media (no hysteresis, etc.):  
> $$
> L_{12} = L_{21}
> $$

This is the basis of **transformer operation**: changing current in one coil induces a voltage in the other.

---

## 🔁 Self-Inductance (Inductance)

Now consider a single coil with $N$ turns carrying current $I$.
![[Self_Inductance.png]]
- Magnetic flux through a **single turn**: $\Phi$.  
- Flux linkage for the coil:
  $$
  \Lambda = N\Phi = N \int_S \mathbf{B}\cdot d\mathbf{s}
  $$

**Self-inductance**:
$$
L = \frac{\Lambda}{I}
$$

- In electric circuit language, “inductance” typically means **self-inductance**.

---

## 💾 Magnetic Energy in an Inductor

Energy stored in the magnetic field of an inductor:
$$
W_m = \frac{1}{2} L I^2
$$

Interpretation:

- Inductance is a kind of **inertia** for current: it resists changes in $I$.  
- To increase current, the source must do work against this opposition → energy stored in the magnetic field.  
- When current decreases, the magnetic field collapses and tends to **keep the current flowing** (Lenz’s law).

---

## 🧮 Self-Inductance of a Very Long Solenoid

We consider a solenoid with:

- $N$ windings  
- length $\ell$  
- radius $a$ (cross-section area $S = \pi a^2$)  
- permeability $\mu = \mu_0 \mu_r$  
- current $I$ flowing through the windings  
- Field outside the solenoid ≈ **zero** (long solenoid approximation)
![[verylong2.png]]
![[verylong.png]]

---

### **1. Choose the coordinate system**

Use **cylindrical coordinates** $(r, \phi, z)$ with the solenoid aligned along $\hat{\mathbf{z}}$.

---

### **2. Assume a steady current $I$ in the windings**

Each turn contributes to the magnetic field inside the solenoid.

---

### **3. Find $\mathbf{B}$ using Ampère’s circuital law**

Ampère's law:

$$
\oint_C \mathbf{H} \cdot d\boldsymbol{\ell} = I_{\text{enc}}
$$

Choose an Amperian loop that runs:

- along the interior of the solenoid over length $\ell$
- returns outside (contribution ≈ 0 because field outside ≈ 0)

Thus:

$$
H_z\,\ell = N I
\quad\Rightarrow\quad
H_z = \frac{N I}{\ell}
$$

Magnetic flux density:

$$
\mathbf{B} = \mu \mathbf{H} = \mu_0 \mu_r \frac{N I}{\ell}\,\hat{\mathbf{z}}
$$

(Inside only; outside field assumed zero.)

---

### **4. Compute the flux linkage $\Lambda$**

Magnetic flux through **one turn**:

$$
\Phi = \int_S \mathbf{B}\cdot d\mathbf{s}
     = B\, S
     = \left(\mu_0\mu_r \frac{N I}{\ell}\right) S
$$

Flux linkage for $N$ turns:

$$
\Lambda = N \Phi
        = N\left(\mu_0\mu_r \frac{N I}{\ell}\right) S
        = \mu_0\mu_r \frac{N^2 S}{\ell}\, I
$$

This matches the slide’s integration:

$$
\Lambda = N \int_0^{2\pi} \int_0^a 
  \frac{\mu I N}{\ell}\, r \, dr\, d\phi
      = \frac{\mu I N^2}{\ell} \pi a^2
      = \frac{\mu I N^2 S}{\ell}
$$

---

### **5. Determine the self-inductance**

By definition:

$$
L = \frac{\Lambda}{I}
$$

Thus:

$$
\boxed{
L = \mu_0\mu_r\,\frac{N^2 S}{\ell}
}
$$

---

### **Final Result (from the slide)**

For a very long solenoid:

$$
\boxed{L = \mu_0 \mu_r \frac{N^2 S}{\ell}}
$$
---

## 🧲 Inductors — Solenoid

For a long solenoid:

- Approximate uniform field inside:
  $$
  \lvert \mathbf{B} \rvert \approx \mu_0 \mu_r \frac{N I}{\ell}
  ,\qquad
  \lvert \mathbf{H} \rvert \approx \frac{N I}{\ell}
  $$
- Exterior field is weak and resembles that of a bar magnet.

> [!summary]
> Solenoid inductor ≈ bar magnet with current-generated dipole moment.

---

## 🧲 Inductors — Coaxial Cable & Toroid

Let $\mu_r$ be the relative permeability of the medium enclosing the current.

### Coaxial Cable (length $\ell$, inner radius $R_i$, outer radius $R_o$)

Self-inductance:
$$
L = \frac{\mu_0 \mu_r \ell}{2\pi} \ln\left(\frac{R_o}{R_i}\right)
$$

Inductance per unit length:
$$
L' = \frac{L}{\ell}
   = \frac{\mu_0 \mu_r}{2\pi} \ln\left(\frac{R_o}{R_i}\right)
$$

### Toroidal Inductor (rectangular cross-section)

Toroid with $N$ turns, inner radius $a$, outer radius $b$, height $h$:

Approximate self-inductance:
$$
L \approx \frac{\mu_0 \mu_r N^2 h}{2\pi}
          \ln\left(\frac{b}{a}\right)
$$

### Fields in a Toroid

Assuming $a < r < b$:

$$
\mathbf{H} = \frac{N I}{2\pi r} \, \hat{\boldsymbol{\phi}}, \qquad
\mathbf{B} = \mu_0 \mu_r \frac{N I}{2\pi r} \, \hat{\boldsymbol{\phi}}
$$

- Field is confined mainly **inside the core**; outside ($r<a$ or $r>b$) the field is very weak.

---

## 🔁 Toroidal Transformer (Qualitative)

- Instead of a rectangular core, use a **toroidal core**.  
- Primary current $I_1$ and secondary current $I_2$ flow through windings on the same toroidal core.  
- Circular geometry reduces **flux leakage** and **EMI**, allowing compact transformer designs.

---

## ⚔️ Force Between Two (Infinite) Parallel Wires

Two infinitely long, parallel wires separated by distance $d$,
carrying currents $I_1$ and $I_2$ in the $z$-direction.

Magnetic flux density from wire 1 at the location of wire 2:
$$
B = \frac{\mu_0 I_1}{2\pi d}
$$

Force per unit length on wire 2:
$$
\frac{\mathbf{F}_2}{L}
  = I_2 \, \hat{\mathbf{\ell}} \times \mathbf{B}
  = -\,\frac{\mu_0 I_1 I_2}{2\pi d} \, \hat{\mathbf{x}}
$$
(similarly for wire 1 with opposite direction).

Magnitude:
$$
\boxed{\frac{F}{L} =
\frac{\mu_0 I_1 I_2}{2\pi d}}
$$

- **Same direction currents** → wires attract.  
- **Opposite direction currents** → wires repel.  
- Opposite behavior to **electrostatics**, where equal charges repel each other.

---

## 🧾 Grand Summary — Magnetostatics II

| Topic | Key Relations | Notes |
|:--|:--|:--|
| **Magnetostatics (general)** | $\nabla\times\mathbf{H}=\mathbf{J}_\text{free}$, $\nabla\cdot\mathbf{B}=0$ | Steady dc currents |
| **Magnetization** | $\mathbf{B} = \mu_0(\mathbf{H} + \mathbf{M})$ | $\mathbf{M}$ from aligned microscopic currents |
| **Susceptibility & permeability** | $\mathbf{M}=\chi_m\mathbf{H}$, $\mu_r=1+\chi_m$, $\mathbf{B}=\mu_0\mu_r\mathbf{H}$ | Linear, homogeneous, isotropic media |
| **Material types** | Diamagnet: $\chi_m<0$; paramagnet: small $\chi_m>0$; ferromagnet: large $\chi_m$ | Field response & domain behavior |
| **Hysteresis** | Loop in $B$–$H$ plane: $B_s$, $B_r$, $H_c$ | Non-linear ferromagnets; energy loss per cycle |
| **Boundary conditions** | $B_{1n}=B_{2n}$, $\hat{\mathbf{n}}\times(\mathbf{H}_1-\mathbf{H}_2)=\mathbf{J}_{S,\text{free}}$ | Interface between media |
| **Magnetic force on charge** | $\mathbf{F}_m = q\,\mathbf{u}\times\mathbf{B}$ | Perpendicular to $\mathbf{u}$ and $\mathbf{B}$ |
| **Flux & flux linkage** | $\Phi=\int_S\mathbf{B}\cdot d\mathbf{s}$, $\Lambda=N\Phi$ | Basis for $L$ |
| **Mutual inductance** | $L_{12}=\Lambda_{12}/I_1$, $L_{21}=\Lambda_{21}/I_2$ | $L_{12}=L_{21}$ in linear media |
| **Self-inductance** | $L=\Lambda/I$ | Inductor property in circuits |
| **Magnetic energy** | $W_m=\tfrac{1}{2}LI^2$ | Energy in magnetic field |
| **Solenoid (long)** | $B\approx\mu_0\mu_r\frac{NI}{\ell}$, $L=\mu_0\mu_r\frac{N^2S}{\ell}$ | Nearly uniform field inside |
| **Coaxial cable** | $L=\dfrac{\mu_0\mu_r\ell}{2\pi}\ln\!\dfrac{R_o}{R_i}$ | Self-inductance |
| **Toroid** | $H=\dfrac{NI}{2\pi r}$, $B=\mu_0\mu_r\dfrac{NI}{2\pi r}$, $L\approx \dfrac{\mu_0\mu_rN^2h}{2\pi}\ln\!\dfrac{b}{a}$ | Confined field |
| **Parallel wires** | $F/L=\mu_0I_1I_2/(2\pi d)$ | Attract if currents are parallel |

---

## Praktisk Anvendelse

| Projekt | Link | Anvendelse |
|---------|------|------------|
| VLF Metaldetektor (34621) | [Spole Design](obsidian://open?vault=34621-Metal-Detector&file=Docs%2FTheory%2FCoil%20Design) | Wheeler formel til beregning af flerlagsspole induktans, gensidig induktans for TX/RX kobling |
