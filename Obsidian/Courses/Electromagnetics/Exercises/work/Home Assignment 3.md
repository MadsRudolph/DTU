
> 🔗 [[MOC – Electromagnetics]]  
> **Context:** Electrostatics & magnetostatics in matter – conductors with cavities, charge distributions, capacitors, Ampère’s law, Lorentz force, and inductors.

> [!info] 🧩 Quick Formula Recap — HA3
>
> **Gauss’ law (electric)**
> - $\displaystyle \oint_S \mathbf D\cdot d\mathbf s = Q_{\text{enc}}$  
> - $\displaystyle \mathbf D = \varepsilon \mathbf E,\quad \varepsilon = \varepsilon_0\varepsilon_r$
> - **Conductor in electrostatics:** $\mathbf E = 0$ inside; any excess free charge lives on surfaces.
>
> **Symmetric charge distributions**
> - Uniform sphere, charge density $\rho_v$:
>   $$
>   Q_{\text{tot}} = \rho_v \frac{4}{3}\pi r_s^3
>   $$
>   $$
>   E(r) =
>   \begin{cases}
>   \dfrac{\rho_v r}{3\varepsilon}, & r<r_s\\[4pt]
>   \dfrac{Q_{\text{tot}}}{4\pi\varepsilon r^2}, & r\ge r_s
>   \end{cases}
>   $$
>
> **Electrostatic work**
> - $\displaystyle W = q\int_{\mathbf r_1}^{\mathbf r_2}\mathbf E\cdot d\mathbf l$  
> - If motion is perpendicular to $\mathbf E$ → $W=0$.
>
> **Capacitance**
> - Parallel plates: $\displaystyle C=\frac{\varepsilon A}{d}$, with $E_{\max}=V_{\max}/d$ (dielectric strength).  
> - Two parallel wires (radius $R$, spacing $d$):
>   $$
>   C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\bigl(\dfrac{d}{2R}\bigr)},
>   \qquad C = C'\ell
>   $$
>
> **Magnetostatics**
> - Ampère: $\displaystyle \oint_C \mathbf H\cdot d\mathbf l = I_{\text{free,enc}}$  
> - Right–hand rule: thumb along current, fingers curl in direction of $\mathbf B$; or fingers along current loop, thumb along $\mathbf B$ at its center.
> - Lorentz force: $\displaystyle \mathbf F = q\,\mathbf v\times \mathbf B$.
>
> **Fields from simple currents**
> - Long straight wire: $\displaystyle H_\phi = \dfrac{I}{2\pi\rho}$  
> - Square loop (side $\ell$) at center:
>   $$
>   H = \frac{2\sqrt{2}I}{\pi\ell}
>   $$
>
> **Inductance**
> - Long solenoid: $\displaystyle L=\frac{\mu N^2 A}{\ell}$  
> - Toroid (mean path length $\ell_m$, cross-section area $A$):
>   $$
>   L=\frac{\mu N^2 A}{\ell_m},\qquad \mu = \mu_0\mu_r
>   $$
>
> **Unit reminders**
> - $1~\text{fC}=10^{-15}$ C, $1~\text{nC}=10^{-9}$ C  
> - $1~\text{mm}=10^{-3}$ m, $1~\text{cm}=10^{-2}$ m  

---

## Section 1 — Conductor with a cavity (Q1–Q2)

![[Images/Section1.png]]

> [!summary] **Question 1 — Regions with non-zero $\vec E$**
>
> A neutral conductor has an air-filled cavity (**Region 1**). The conductor itself is **Region 2**, and the exterior is **Region 3**.  
> Four point charges inside the cavity (not touching the conductor):
> $$
> Q_1=7~\text{fC},\quad Q_2=-2~\text{fC},\quad Q_3=-3~\text{fC},\quad Q_4=2~\text{fC}.
> $$
> **Which regions have non-zero electrostatic field $\vec E$?**

💡 **Concept**

- Electrostatic equilibrium in a perfect conductor:
  $$
  \mathbf E = 0 \quad \text{everywhere inside the conductor (Region 2).}
  $$
- Charges in the cavity produce an electric field in the cavity volume (Region 1).
- The net cavity charge induces equal and opposite surface charge on the **inner surface**, and a compensating charge on the **outer surface**, which creates a field in Region 3.

🧮 **Reasoning**

Total charge in the cavity:

$$
Q_{\text{cav}} = 7-2-3+2 = 4~\text{fC}\neq 0.
$$

- Region 1: non-zero field due to the four charges.  
- Region 2: field must be zero in an ideal conductor.  
- Region 3: non-zero field due to induced net charge on the outer surface.

✅ **Answer:** $\boxed{\text{Regions 1 and 3}}$

---

> [!summary] **Question 2 — Charge on the outer conducting surface**
>
> **What is the total charge on the conducting surface between Region 2 and 3?**

💡 **Concept**

- Choose a Gaussian surface **inside** the conductor, hugging the inner cavity surface. Since $\mathbf E=0$ there:
  $$
  Q_{\text{enc}} = Q_{\text{cav}} + Q_{\text{inner}} = 0
  \Rightarrow Q_{\text{inner}} = -Q_{\text{cav}}.
  $$
- The **total conductor** is given as neutral:
  $$
  Q_{\text{conductor}} = Q_{\text{inner}} + Q_{\text{outer}} = 0
  \Rightarrow Q_{\text{outer}} = -Q_{\text{inner}}.
  $$

🧮 **Derivation**

1. Inner surface charge:
   $$
   Q_{\text{inner}} = -Q_{\text{cav}} = -4~\text{fC}.
   $$
2. Outer surface charge:
   $$
   Q_{\text{outer}} = -Q_{\text{inner}} = +4~\text{fC}.
   $$

✅ **Answer:** $\boxed{Q_{\text{outer}} = 4~\text{fC}}$

🧩 **Interpretation**

The conductor “rearranges” its charges so that:

- The field inside the metal is zero.  
- The conductor’s net charge remains zero.  

This forces $-4$ fC onto the inner cavity surface and $+4$ fC onto the outer surface.

---

## Section 2 — Charge distributions & electrostatic work (Q3–Q4)

> [!summary] **Question 3 — Field of a uniformly charged sphere in a dielectric**
>
> A sphere of radius $r_s = 2.2~\text{cm}$ carries a uniform volume charge density $\rho_v = 4.0~\text{nC/m}^3$.  
> It is embedded in a dielectric with $\varepsilon_r = 2.1$.  
> **Find** the electric field magnitude at $R=4.5~\text{cm}$ from the center, in $\text{V/m}$.

💡 **Concept**

For $R>r_s$, a uniformly charged sphere behaves like a **point charge** $Q$ at its center:

$$
E(R) = \frac{Q}{4\pi\varepsilon R^2},\quad Q=\rho_v\frac{4}{3}\pi r_s^3.
$$

🧮 **Derivation**

Convert to SI:

- $r_s = 2.2~\text{cm} = 0.022~\text{m}$  
- $R = 4.5~\text{cm} = 0.045~\text{m}$  
- $\rho_v = 4.0~\text{nC/m}^3 = 4.0\times 10^{-9}~\text{C/m}^3$  
- $\varepsilon = \varepsilon_0\varepsilon_r = 8.854\times 10^{-12}\cdot 2.1~\text{F/m}$

Total charge:

$$
Q = \rho_v\frac{4}{3}\pi r_s^3
  \approx 1.78\times 10^{-13}~\text{C}.
$$

Field at $R$:

$$
E(R) = \frac{Q}{4\pi\varepsilon R^2}
      \approx 0.377~\text{V/m}.
$$

✅ **Answer:** $\boxed{E(4.5~\text{cm}) \approx 0.38~\text{V/m}}$

---

> [!summary] **Question 4 — Work done moving a charge in a uniform field**
>
> A charge $Q = 1~\text{nC}$ is (slowly) moved along the $x$-axis from $x_1 = 2~\text{mm}$ to $x_2 = 7~\text{mm}$ in a uniform electric field  
> $\vec E = -5\,\hat{\mathbf y}~\text{V/m}$.  
> **What is the work required to move the charge?**

💡 **Concept**

Work done by the electric field:

$$
W = Q\int_{\mathbf r_1}^{\mathbf r_2} \vec E\cdot d\vec l.
$$

If motion is **perpendicular** to $\vec E$, then $\vec E\cdot d\vec l = 0$ everywhere and $W=0$.

🧮 **Derivation**

- Displacement is along $\hat{\mathbf x}$.  
- Field is along $-\hat{\mathbf y}$.

Thus the dot product:

$$
\vec E\cdot d\vec l = (-5\hat{\mathbf y})\cdot (dx\,\hat{\mathbf x}) = 0.
$$

Therefore

$$
W = 0.
$$

✅ **Answer:** $\boxed{W = 0~\text{J}}$

🧩 **Interpretation**

Electrostatic potential only depends on movement **along** the field lines.  
Moving purely sideways in a uniform field changes neither potential energy nor potential.

---

## Section 3 — Capacitors (Q5–Q6)

> [!summary] **Question 5 — Capacitance of two parallel wires**
>
> Two parallel cylindrical wires form a capacitor.  
> - Radius: $R = 0.23~\text{mm}$  
> - Length: $\ell = 105~\text{cm}$  
> - Center–to–center distance: $d = 1.2~\text{mm}$  
> - Dielectric: $\varepsilon_r = 94$  
>
> **Find** the capacitance $C$ in nF.

💡 **Concept**

Capacitance per unit length for two parallel wires:

$$
C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\left(\frac{d}{2R}\right)},
\qquad C = C'\,\ell.
$$

🧮 **Derivation**

Convert to SI:

- $R = 0.23~\text{mm} = 0.00023~\text{m}$  
- $d = 1.2~\text{mm} = 0.0012~\text{m}$  
- $\ell = 105~\text{cm} = 1.05~\text{m}$  
- $\varepsilon = \varepsilon_0\varepsilon_r = 8.854\times 10^{-12}\cdot 94$

Capacitance:

$$
C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\left(\dfrac{d}{2R}\right)}
\approx 1.62\times 10^{-9}~\text{F/m},
$$
$$
C = C'\ell \approx 1.70\times 10^{-9}~\text{F} = 1.70~\text{nF}.
$$

✅ **Answer:** $\boxed{C \approx 1.70~\text{nF}}$

---

> [!summary] **Question 6 — Plate area with capacitance and breakdown constraints**
>
> A parallel-plate capacitor must satisfy:
> - Capacitance: $C = 744~\text{pF}$  
> - Max voltage: $V_{\max} = 1.22~\text{kV}$  
> - Dielectric: $\varepsilon_r = 182$, dielectric strength $E_{\max} = 35~\text{kV/mm}$  
>
> **Find** the required area $A$ of each plate in $\text{mm}^2$.

💡 **Concept**

We must satisfy **both**:

1. Breakdown: $E = V_{\max}/d \le E_{\max}$ → choose $d = V_{\max}/E_{\max}$.
2. Capacitance: $C = \varepsilon A/d$ → solve for $A$.

🧮 **Derivation**

1. Convert units and find $d$:
   $$
   E_{\max} = 35~\frac{\text{kV}}{\text{mm}}
            = 3.5\times 10^{7}~\text{V/m},
   $$
   $$
   V_{\max} = 1.22\times 10^{3}~\text{V},
   $$
   $$
   d = \frac{V_{\max}}{E_{\max}}
     \approx 3.49\times 10^{-5}~\text{m}.
   $$

2. Capacitance condition with $\varepsilon = \varepsilon_0\varepsilon_r$:

   $$
   A = \frac{C d}{\varepsilon}
     = \frac{744\times 10^{-12}\cdot 3.49\times 10^{-5}}
            {8.854\times 10^{-12}\cdot 182}
     \approx 1.61\times 10^{-5}~\text{m}^2.
   $$

3. Convert to $\text{mm}^2$:

   $$
   A_{\text{mm}^2} = A\cdot 10^{6} \approx 16.1~\text{mm}^2.
   $$

✅ **Answer:** $\boxed{A \approx 16.1~\text{mm}^2}$

🧩 **Interpretation**

The dielectric strength fixes the **minimum spacing**; once $d$ is set, the only way to hit the required $C$ is by choosing the proper plate area.

---
## Section 4 — Ampère’s law & Lorentz force (Q7–Q9)

> [!summary] **Question 7 — Correct sketches for current and $\vec B$**
>
> Several sketches show either:  
> - a circular **current** with a central $\vec B$ indicated by $\odot$ (out of page) / $\otimes$ (into page), or  
> - a central **current** ($\odot$ / $\otimes$) and a circular $\vec B$.  
>
> **Which sketches have consistent directions according to the right-hand rule?**

**Sketches**

| Sketch 1 | Sketch 2 |
| --- | --- |
| ![[Images/1.png]] | ![[Images/2.png]] |

| Sketch 3 | Sketch 4 |
| --- | --- |
| ![[Images/3.png]] | ![[Images/4.png]] |

💡 **Concept**

- **Straight wire:** thumb along current $I$, fingers curl in direction of $\vec B$.  
- **Current loop:** fingers along current direction, thumb gives the direction of $\vec B$ through the loop.

🧮 **Reasoning**

All four sketches use the **same circular direction** for the ring (clockwise as seen from the viewer).

1. **Sketch 1 — Loop current clockwise, $\vec B$ out of page ($\odot$)**  
   - For a clockwise loop, curling fingers clockwise makes the thumb point **into** the page.  
   - Here $\vec B$ is drawn **out** of the page → mismatch. ✖ Incorrect.

2. **Sketch 2 — Loop current clockwise, $\vec B$ into page ($\otimes$)**  
   - Clockwise loop → thumb points **into** the page.  
   - $\vec B$ is into the page → consistent with the right-hand rule. ✔ Correct.

3. **Sketch 3 — Current out of page ($\odot$), $\vec B$ clockwise**  
   - For a straight current **out** of the page, fingers curl **counter-clockwise** around the wire.  
   - $\vec B$ is drawn clockwise → wrong sense. ✖ Incorrect.

4. **Sketch 4 — Current into page ($\otimes$), $\vec B$ clockwise**  
   - For a straight current **into** the page, fingers curl **clockwise**.  
   - $\vec B$ is clockwise → correct. ✔ Correct.

✅ **Answer:** $\boxed{\text{Sketches 2 and 4 are correct}}$


---
> [!summary] **Question 8 — Path of a moving positive charge in $\vec B$**
>
> A positive charge $+q$ moves with constant velocity $\vec u$ to the right, in a magnetic flux density $\vec B$ that points **into** the page.  
> Three possible curved paths (1 up, 2 straight, 3 down) are shown.  
> **Which path does the charge follow?**

![[Images/Section6.png]]

💡 **Concept**

Magnetic force (Lorentz):

$$
\mathbf F = q\,\mathbf u\times\mathbf B.
$$

For $q>0$, the direction is that of $\mathbf u\times\mathbf B$.

🧮 **Direction**

Take coordinates:

- $\vec u$ along $+\hat{\mathbf x}$ (to the right)  
- $\vec B$ along $-\hat{\mathbf z}$ (into page)

Then

$$
\mathbf u\times\mathbf B
= \hat{\mathbf x}\times(-\hat{\mathbf z})
= -(\hat{\mathbf x}\times\hat{\mathbf z})
= -(-\hat{\mathbf y})
= +\hat{\mathbf y},
$$

which is **upward**.

✅ **Answer:** $\boxed{\text{Path 1}}$ (deflection upward)

🧩 **Interpretation**

A positive charge curves in the direction given by the usual right-hand rule.  
A negative charge would follow the opposite (downward) path.


---

> [!summary] **Question 9 — $|\vec H|$ at the center of a square current loop**
>
> A square loop of wire with side length $\ell = 4.2~\text{mm}$ carries a current $I = 2.69~\text{mA}$.  
> It is in a magnetic medium with $\mu_r = 5$.  
> **Find** the magnitude of the magnetic field intensity $|\vec H|$ at the center, in $\text{A/m}$.

💡 **Concept**

- Magnetic field from free currents is described by $\vec H$ via Ampère’s law:
  $\nabla\times\vec H = \vec J_{\text{free}}$.  
  The solution for $\vec H$ in a given geometry does **not** depend on $\mu_r$ (only $\vec B=\mu\vec H$ does).
- For a square loop (side $\ell$), the field at the center is the sum of four equal contributions. For one side:

  $$
  H_{\text{side}} = \frac{I}{2\pi a}\sin\theta,
  $$

  where $a=\ell/2$ is the distance from the center to the side and $\theta$ is the angle to the ends.  
  For a square, $\tan\theta = \dfrac{\ell/2}{a}=1\Rightarrow\theta=45^\circ,\ \sin\theta = 1/\sqrt{2}$.

- All four sides add with the same direction, so

  $$
  H_{\text{tot}} = 4H_{\text{side}} = \frac{2\sqrt{2}I}{\pi\ell}.
  $$

🧮 **Derivation**

Convert units:

- $\ell = 4.2~\text{mm} = 4.2\times 10^{-3}~\text{m}$  
- $I = 2.69~\text{mA} = 2.69\times 10^{-3}~\text{A}$

Compute:

$$
H = \frac{2\sqrt{2}I}{\pi\ell}
  \approx \frac{2\sqrt{2}\cdot 2.69\times 10^{-3}}{\pi\cdot 4.2\times 10^{-3}}
  \approx 0.577~\text{A/m}.
$$

✅ **Answer:** $\boxed{|\vec H| \approx 0.58~\text{A/m}}$

🧩 **Interpretation**

The result is **independent of $\mu_r$**; $\mu_r$ would only scale $\vec B = \mu\vec H$.

---

## Section 5 — Inductors (Q10–Q11)

> [!summary] **Question 10 — Inductance of a toroidal inductor**
>
> A toroidal inductor with rectangular cross-section has:
> - Height: $h = 4.4~\text{mm}$  
> - Inner radius: $a = 8~\text{mm}$  
> - Outer radius: $b = 12~\text{mm}$  
> - Windings: $N = 56$  
> - Core relative permeability: $\mu_r = 130$  
>
> **Find** its inductance $L$ in $\mu\text{H}$.

💡 **Concept**

Approximate the toroid using:

- Cross-section area: $A \approx h(b-a)$  
- Mean radius: $r_m = (a+b)/2$  
- Magnetic path length: $\ell_m \approx 2\pi r_m$  
- Permeability: $\mu = \mu_0\mu_r$

Inductance:

$$
L = \frac{\mu N^2 A}{\ell_m}.
$$

🧮 **Derivation**

Convert to meters:

- $h = 4.4\times 10^{-3}~\text{m}$  
- $a = 8\times 10^{-3}~\text{m}$  
- $b = 12\times 10^{-3}~\text{m}$  

Area:

$$
A = h(b-a)
  = 4.4\times10^{-3}\cdot 4\times10^{-3}
  = 1.76\times 10^{-5}~\text{m}^2.
$$

Mean path length:

$$
r_m = \frac{a+b}{2} = 10\times10^{-3}~\text{m},\quad
\ell_m = 2\pi r_m \approx 6.283\times10^{-2}~\text{m}.
$$

Permeability:

$$
\mu = \mu_0\mu_r
    = (4\pi\times10^{-7})\cdot 130.
$$

Inductance:

$$
L = \frac{\mu N^2 A}{\ell_m}
  \approx 1.44\times 10^{-4}~\text{H}
  = 144~\mu\text{H}.
$$

✅ **Answer:** $\boxed{L \approx 144~\mu\text{H}}$

---

> [!summary] **Question 11 — Number of turns for a solenoid on a ferrite rod**
>
> You want an inductor with inductance $L = 584~\mu\text{H}$.  
> - Ferrite rod: diameter $d_f = 5.0~\text{mm}$, $\mu_r = 200$  
> - Copper wire: diameter $d_w = 0.2~\text{mm}$  
> - One **single layer** of windings (turns tightly side-by-side)  
>
> **Find** the number of turns $N$ (round up to nearest integer).

💡 **Concept**

- Cross-section area of the rod:
  $$
  A = \pi\left(\frac{d_f}{2}\right)^2.
  $$
- For a single layer, coil length is approximately
  $$
  \ell \approx N d_w.
  $$
- Solenoid inductance:
  $$
  L = \frac{\mu N^2 A}{\ell} = \frac{\mu N^2 A}{N d_w}
    = \frac{\mu N A}{d_w}
    \Rightarrow
    N = \frac{L d_w}{\mu A}.
  $$

🧮 **Derivation**

Convert units:

- $d_f = 5.0\times 10^{-3}~\text{m}$  
- $d_w = 0.2\times 10^{-3}~\text{m}$  
- $L = 584\times 10^{-6}~\text{H}$  

Area:

$$
A = \pi\left(\frac{d_f}{2}\right)^2
  = \pi(2.5\times10^{-3})^2
  \approx 1.96\times10^{-5}~\text{m}^2.
$$

Permeability:

$$
\mu = \mu_0\mu_r = (4\pi\times10^{-7})\cdot 200.
$$

Number of turns:

$$
N = \frac{L d_w}{\mu A}
  \approx 23.7.
$$

Round **up** to the nearest integer:

$$
N = 24~\text{turns}.
$$

✅ **Answer:** $\boxed{N = 24\ \text{turns}}$

🧩 **Interpretation**

With $N=24$ and $\ell\approx 24d_w$, the actual inductance comes out slightly above the target (about $592~\mu\text{H}$), which is acceptable given the rounding and core tolerances.

---

Recent in same folder

```dataview
LIST
FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.path != this.file.path
SORT file.mtime desc
LIMIT 5
```
