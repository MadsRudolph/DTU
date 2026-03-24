---
course: "30035"
course-name: "Engineering Electromagnetics"
type: formula
date: 2025-11-10
tags:
  - Electromagnetics
  - formula
  - Electrostatics
---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Courses/Electromagnetics/Formulas/Electrostatics — Quick Formula Sheet]]  
> **Quick refs:** [[MOC – Maxwell’s Equations]] · [[MOC – Charge Distributions]] · [[MOC – Electric Fields]] · [[30035 Engineering Electromagnetics]]  
> For **30035 Engineering Electromagnetics – Fall 2025** (DTU Space, Rasmus E. Jacobsen) — complete, highly descriptive reference for **Electrostatics I** (Lecture 19, 10 Nov 2025) and corresponding summary slides I–III.  
> Constants: $\epsilon_0 = 8.854 \times 10^{-12}$ F/m, $k = \dfrac{1}{4\pi \epsilon_0} \approx 9 \times 10^9$ Nm$^2$/C$^2$, charge of an electron $q_e = -1.602 \times 10^{-19}$ C.  
> Textbook: Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, 8th Global Ed., Ch.4.

---

## 🧭 Maxwell's Equations in Electrostatics (Summary Slide I)
> [!note] **Electrostatics (vacuum)**  
> In electrostatics we consider **charges at rest**. There are **no currents**, since they describe a flow of moving charges.  
> Stationary charges → no current → $\nabla \times \mathbf{E} = 0$, $\mathbf{H} = 0$, $\mathbf{B} = 0$.

| Name                  | Differential Form                                 | Integral Form                                              | Description |
|:----------------------|:---------------------------------------------------|:-----------------------------------------------------------|:------------|
| **Gauss’s Law**       | $\nabla \cdot \mathbf{E} = \dfrac{\rho_v}{\epsilon_0}$ | $\oint_S \mathbf{E} \cdot d\mathbf{s} = \dfrac{Q_{tot}}{\epsilon_0}$ | Electric flux through closed surface equals enclosed charge divided by $\epsilon_0$. |
| **Kirchhoff’s Law**   | $\nabla \times \mathbf{E} = 0$                    | $\oint_C \mathbf{E} \cdot d\mathbf{l} = 0$                 | Electric field is **conservative** → line integral around any closed loop is zero. |
| **No magnetic field** | $\mathbf{B} = 0$                                   | –                                                         | Static charges produce no magnetic field. |

> [!tip]  
> $\mathbf{R}$ = observation point, $\mathbf{R}'$ = source point (location of charge).  
> Vector from source to observation: $\mathbf{R} - \mathbf{R}'$, unit vector $\hat{R} = \dfrac{\mathbf{R} - \mathbf{R}'}{|\mathbf{R} - \mathbf{R}'|}$.

---

### 📐 Total Charge from Distributions (Summary Slide III)
> [!example] **Total enclosed charge $Q_{tot}$** – sum of discrete charges or integration of densities.

| Distribution          | Formula                                               | Illustration |
|:----------------------|:------------------------------------------------------|:-------------|
| **Discrete charges**  | $Q_{tot} = \sum_{k=1}^N Q_k$                          | $Q_1, Q_2, \dots, Q_k$ |
| **Volume charge**     | $Q_{tot} = \int_\Omega \rho_v(\mathbf{R}')\, d\Omega'$ | Cube with $\rho_v(\mathbf{R}')$ |
| **Surface charge**    | $Q_{tot} = \int_S \rho_s(\mathbf{R}')\, dS'$          | Plate with $\rho_s(\mathbf{R}')$ |
| **Line charge**       | $Q_{tot} = \int_\ell \rho_\ell(\mathbf{R}')\, dl'$    | Wire with $\rho_\ell(\mathbf{R}')$ |

> [!summary]  
> $\rho_v$ (C/m$^3$), $\rho_s = \sigma$ (C/m$^2$), $\rho_\ell = \lambda$ (C/m).

---

### ⚡ Coulomb’s Law & Force on a Charge (Summary Slide I)
Force on charge $q_1$ due to electric field $\mathbf{E}$:  
$$
\mathbf{F} = q \mathbf{E} \quad [\text{N}]
$$

Coulomb’s law for **two point charges** $q_1$, $q_2$:  
$$
\mathbf{F}_{12} = q_1 q_2 \dfrac{\mathbf{R}_1 - \mathbf{R}_2}{4\pi \epsilon_0 \lvert \mathbf{R}_1 - \mathbf{R}_2\rvert^3} = \frac{q_1 q_2}{4\pi \epsilon_0 R^2}\,\hat{R}_{12}
$$
- $\mathbf{F}_{12} = -\mathbf{F}_{21}$ (Newton’s 3rd law).  
- Same sign → **repulsive**, opposite sign → **attractive**.

> [!example] **Exercise 19.1 (from slides)**  
> $Q_1 = 2Q$, $Q_2 = 2$ fC at positions $P_1(x,y,z)=(-2,4,1)$ nm, $P_2(1,-1,5)$ nm.  
> Vector $\mathbf{R}_1 - \mathbf{R}_2 = (-3,5,-4)$ nm, $\lvert\mathbf{R}_1 - \mathbf{R}_2\rvert = 7.141$ nm.  
> Force magnitude $\lvert\mathbf{F}_{12}\rvert = 36.82$ aN, direction repulsive (positive × positive).  
> When $Q_2 = -2$ fC → force becomes **attractive** $-36.82$ aN.

---

### 🧩 Electric Field from Charge Distributions (Summary Slide II)
Observation point $\mathbf{R}$, source point $\mathbf{R}'$.

| Distribution          | Electric Field $\mathbf{E}(\mathbf{R})$                                                                 | Potential $V(\mathbf{R})$                                                                 |
|:----------------------|:---------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------|
| **N discrete charges**| $\displaystyle \mathbf{E}(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \sum_{k=1}^N Q_k \frac{\mathbf{R} - \mathbf{R}_k}{\lvert \mathbf{R} - \mathbf{R}_k\rvert^3}$ | $\displaystyle V(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \sum_{k=1}^N \frac{Q_k}{\lvert \mathbf{R} - \mathbf{R}_k\rvert}$ |
| **Volume $\rho_v$**   | $\displaystyle \mathbf{E}(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_\Omega \rho_v(\mathbf{R}') \frac{\mathbf{R} - \mathbf{R}'}{\lvert \mathbf{R} - \mathbf{R}'\rvert^3} d\Omega'$ | $\displaystyle V(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_\Omega \frac{\rho_v(\mathbf{R}')}{\lvert \mathbf{R} - \mathbf{R}'\rvert} d\Omega'$ |
| **Surface $\sigma$**  | $\displaystyle \mathbf{E}(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_S \sigma(\mathbf{R}') \frac{\mathbf{R} - \mathbf{R}'}{\lvert \mathbf{R} - \mathbf{R}'\rvert^3} dS'$      | $\displaystyle V(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_S \frac{\sigma(\mathbf{R}')}{\lvert \mathbf{R} - \mathbf{R}'\rvert} dS'$      |
| **Line $\lambda$**    | $\displaystyle \mathbf{E}(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_\ell \lambda(\mathbf{R}') \frac{\mathbf{R} - \mathbf{R}'}{\lvert \mathbf{R} - \mathbf{R}'\rvert^3} dl'$     | $\displaystyle V(\mathbf{R}) = \frac{1}{4\pi \epsilon_0} \int_\ell \frac{\lambda(\mathbf{R}')}{\lvert \mathbf{R} - \mathbf{R}'\rvert} dl'$     |

> [!tip]  
> The **denominator is always cubed** for $\mathbf{E}$, **linear** for $V$.

---

### 🔄 Gauss’s Law Applications (Summary Slide I + common examples)
- **Point charge:** $\mathbf{E} = \dfrac{Q}{4\pi \epsilon_0 R^2}\,\hat{R}$  
- **Infinite line charge $\lambda$:** $\mathbf{E} = \dfrac{\lambda}{2\pi \epsilon_0 r}\,\hat{r}$  
- **Infinite plane $\sigma$:** $\mathbf{E} = \dfrac{\sigma}{2\epsilon_0}\,\hat{n}$ (direction away from sheet if $\sigma > 0$)  
- **Uniformly charged sphere** (radius $a$, total $Q$):  
  - Inside ($r < a$): $\mathbf{E} = \dfrac{Q r}{4\pi \epsilon_0 a^3}\,\hat{r} = \dfrac{\rho_v r}{3 \epsilon_0}\,\hat{r}$  
  - Outside ($r > a$): same as point charge at centre.

> [!example] **Exercise 19.2 – Three charges in Cartesian, cylindrical, spherical**  
> Sketch the configuration in $xy$-plane with $Q_1$ on the $x$-axis at $x = R_0$.

---

### 🔋 Electric Potential (Summary Slide I)
Electric field is **curl-free** → gradient of a scalar field:  
$$
\mathbf{E} = -\nabla V
$$
Potential difference between points $P_1$ and $P_2$:  
$$
V_2 - V_1 = V(P_2) - V(P_1) = -\int_{P_1}^{P_2} \mathbf{E} \cdot d\mathbf{l}
$$
- Reference usually taken at infinity ($V(\infty) = 0$).  
- Energy to assemble charge $q$ at potential $V$: $W = q V$.

> [!example] **Infinite line charge potential**  
> $$V(r) = -\dfrac{\lambda}{2\pi \epsilon_0} \ln\!\left(\dfrac{r}{r_0}\right) + V_0$$  
> (reference at $r_0$).

---

## 🧮 Worked Example – Infinite Line Charge (from Lecture 19)
Infinite uniform line charge $\lambda$ along $z$-axis. Find $\mathbf{E}$ at distance $r$.  

**Step 1 – Symmetry:** Cylindrical, $\mathbf{E} = E_r(r)\,\hat{r}$ (no $\phi$, $z$ dependence).  
**Step 2 – Gaussian surface:** Cylinder radius $r$, length $L$.  
**Flux:** $\displaystyle \oint \mathbf{E} \cdot d\mathbf{s} = E_r \cdot 2\pi r L$ (only radial contribution).  
**Enclosed charge:** $Q_{enc} = \lambda L$.  
**Gauss’s law:** $E_r \cdot 2\pi r L = \dfrac{\lambda L}{\epsilon_0}$  
**Solve:**  
$$
E_r = \dfrac{\lambda}{2\pi \epsilon_0 r} \quad \Rightarrow \quad \mathbf{E} = \dfrac{\lambda}{2\pi \epsilon_0 r}\,\hat{r}
$$
$$
\boxed{\mathbf{E} = \dfrac{\lambda}{2\pi \epsilon_0 r}\,\hat{r}}
$$

---

## 📊 Summary Table: Key Electrostatics Formulas (All from Slides)
| Quantity                     | Formula                                                                                           | Notes |
|:-----------------------------|:--------------------------------------------------------------------------------------------------|:------|
| Coulomb force (two charges)  | $\mathbf{F}_{12} = \dfrac{q_1 q_2}{4\pi \epsilon_0 R^2}\,\hat{R}_{12}$                             | Repulsive if same sign |
| Electric field (point charge)| $\mathbf{E} = \dfrac{q}{4\pi \epsilon_0 R^2}\,\hat{R}$                                             | |
| Superposition                | $\mathbf{E}_{tot} = \sum \mathbf{E}_i$                                                            | Linear |
| Infinite line                | $\mathbf{E} = \dfrac{\lambda}{2\pi \epsilon_0 r}\,\hat{r}$                                         | |
| Infinite plane               | $\mathbf{E} = \dfrac{\sigma}{2\epsilon_0}\,\hat{n}$                                                | |
| Uniform sphere (inside)      | $\mathbf{E} = \dfrac{\rho_v r}{3\epsilon_0}\,\hat{r}$                                              | |
| Potential (point charge)     | $V = \dfrac{q}{4\pi \epsilon_0 R}$                                                                | $V(\infty)=0$ |
| $\mathbf{E}$ from $V$        | $\mathbf{E} = -\nabla V$                                                                          | |
| Gauss’s law (integral)       | $\displaystyle \oint_S \mathbf{E} \cdot d\mathbf{s} = \dfrac{Q_{enc}}{\epsilon_0}$                 | Vacuum |

> [!summary]  
> Electrostatics I covers everything needed for static charge problems: Coulomb → field → Gauss → potential. Next lecture: dielectrics and conductors.

**Key Citations & Sources:**  
- 30035 Engineering Electromagnetics, Fall 2025 – Summary Slides I, II, III on Electrostatics I (10 Nov 2025)  
- Lecture 19 Slides – Rasmus E. Jacobsen, DTU Space  
- Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, 8th Global Ed., Ch.4  
- Exercises 19.1 & 19.2 (ver. 2025.11.10)  
- [DTU 30035 Course Page](https://kurser.dtu.dk/course/30035)  
- [Electrostatics - Wikipedia](https://en.wikipedia.org/wiki/Electrostatics)  
- [Griffiths Introduction to Electrodynamics – Ch.2](https://www.physics.rutgers.edu/grad/501/)
