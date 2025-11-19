**worked examples**:[[Exercise 20 - Magnetostatics]]
**Slides**:[[L22_Magnetostatics_I.pdf]]

Goal: **steady (dc) currents** and the **magnetic fields** they create:  
Maxwell’s equations in magnetostatics, Lorentz force, current densities, Ampère’s law, vector potential, and Biot–Savart.

---

## 1. Maxwell’s Equations in Magnetostatics (Vacuum)

**Static / steady conditions**

- Charges move in a **steady flow** (direct current, constant in time).
- Fields are **time-invariant** (no $\partial/\partial t$ terms).
- Electric and magnetic subsystems are **decoupled**.

Electrostatics (for reference):

$$
\nabla \times \vec E = 0, \qquad
\nabla \cdot \vec D = \rho_v
$$

Magnetostatics (steady flow of charges: direct current $dc$):

- Differential form:
  $$
  \nabla \times \vec H = \vec J_{dc}, \qquad
  \nabla \cdot \vec B = 0
  $$

- Integral form:
  $$
  \oint_C \vec B \cdot d\vec \ell = \mu_0 I_{dc}, \qquad
  \oint_S \vec B \cdot d\vec s = 0
  $$

In vacuum:

$$
\vec B = \mu_0 \vec H, \qquad \mu_0 = 4\pi \times 10^{-7}\ \text{H/m}
$$

Later lectures: $\vec J$ will include induced currents in magnetic materials as well.

---

## 2. Electromagnetic Forces — Lorentz Force

Electric force on a charge $q$ in $\vec E$:

$$
\vec F_e = q\vec E
$$

Magnetic force on charge $q$ moving with velocity $\vec u$ in $\vec B$:

$$
\vec F_m = q\,\vec u \times \vec B
$$

**Lorentz force (total electromagnetic force):**

$$
\vec F_{em} = q\big(\vec E + \vec u \times \vec B\big)
$$

Right-hand rule: $\vec u \times \vec B$ gives the direction of the magnetic force for **positive** $q$.

---

## 3. Electric vs Magnetic Forces — Qualitative

Using

$$
\vec F_{em} = q(\vec E + \vec u \times \vec B)
$$

1. **Direction**
   - Electric: $\vec F_e$ is in the **same direction** as $\vec E$.
   - Magnetic: $\vec F_m$ is **perpendicular** to both $\vec u$ and $\vec B$.

2. **When it acts**
   - Electric: acts on any charge (moving or at rest).
   - Magnetic: acts **only** when the charge moves ($\vec u \neq 0$).

3. **Energy / work**
   - Electric: does work $\Rightarrow$ can change kinetic energy (speed).
   - Magnetic: does **no work** (force $\perp$ velocity) $\Rightarrow$ can only change **direction** of motion, not speed.

---

## 4. Magnetic Flux Density $\vec B$ and Field Intensity $\vec H$

- $\vec B$: **magnetic flux density**, analogous to $\vec E$ in electrostatics.  
  Units: tesla (T) $=\text{Wb/m}^2$.
- $\vec H$: **magnetic field intensity**, analogous to $\vec D$.  
  Units: A/m.

For now we work mainly with $\vec B$; $\vec H$ and materials show up in later lectures.

**Definition of $\vec B$ via test charge:**

For a small test charge $q_0$ moving with velocity $\vec u$ in $\vec B$:

$$
\vec F_m \equiv \lim_{q_0 \to 0} q_0\,\vec u \times \vec B
$$

---

## 5. Steady Current and Current Density

A **steady current** is a continuous flow of charge with constant rate.

**Current through a surface $S$:**

- Total charge that has passed through $S$: $Q(t)$.
- **Current:**
  $$
  I = \frac{dQ}{dt}
  $$
  Units: A $=\text{C/s}$.

### 5.1 Volume Current Density

Volume charge density: $\rho_v$ $C/m^3$  
Particle velocity: $\vec u$.

Total charge through a small element $dS$ (normal $\hat n$) in time $dt$:

$$
dQ' = \rho_v\,\vec u \cdot \hat n\, dS\, dt
$$

Current element:

$$
dI = \frac{dQ'}{dt} = \rho_v\,\vec u \cdot \hat n\, dS
$$

**Define the volume current density**

$$
\vec J = \rho_v \vec u \qquad [\text{A/m}^2]
$$

Then

$$
dI = \vec J \cdot \hat n\, dS
$$

**Total current through surface $S$:**

$$
I = \int_S \vec J(\vec R)\cdot \hat n\, dS
$$

$\vec J(\vec R)$ is a vector point function.

### 5.2 Surface and Line Current Densities

- **Surface current density** $\vec J_S$ $A/m$ flows along a surface.
- **Line current** $I$ [A] flows along a filamentary path $C$.

General summary (from the slide):

- Volume distribution:
  $$
  I = \int_S \vec J(\vec R')\cdot \hat n\, dS'
  $$
- Surface distribution:
  $$
  I = \int_\ell \vec J_S(\vec R')\cdot \hat n\, d\ell'
  $$
- Line distribution:
  $$
  I = I(\vec R')
  $$

> There are **no discrete magnetic charges**; sources are always **currents**.

---

## 6. Ampère’s Circuital Law and Right-Hand Rule

Magnetostatic Maxwell equations in vacuum:

$$
\nabla \times \vec B = \mu_0 \vec J, \qquad
\nabla \cdot \vec B = 0
$$

Applying Stokes’ theorem:

- **Ampère’s circuital law (integral form):**
  $$
  \oint_C \vec B \cdot d\vec \ell = \mu_0 I_{\text{enc}}
  $$

- **No magnetic charges (flux form):**
  $$
  \oint_S \vec B \cdot d\vec s = 0
  $$

**Right-hand rule (Ampère’s law):**

- If you point the thumb of your right hand along the direction of **current** $I$, your fingers curl in the direction of the circulation of $\vec B$ (and $d\vec \ell$).
- Equivalently: choose integration direction $d\vec \ell$; the corresponding positive $I_{\text{enc}}$ flows along the right-hand thumb.

---

## 7. B-Field from a Straight Wire (Solid Cylinder)

Consider an **infinitely long straight circular cylindrical wire** of radius $a$ with uniform volume current density

$$
\vec J(r) = \hat z\, J_0, \qquad r \le a
$$

### 7.1 Total Current

$$
I_0 = \int_S \vec J \cdot \hat z\, dS
    = J_0 \pi a^2
$$

### 7.2 Symmetry

- Cylindrical symmetry $\Rightarrow$ $\vec B$ is purely azimuthal:
  $$
  \vec B(r) = \hat \phi\, B_\phi(r)
  $$
- No radial or axial components: $B_r = 0$, $B_z = 0$.

### 7.3 Field Inside and Outside the Wire

Use an Amperian circle of radius $r$, coaxial with the wire.

**Inside ($r < a$)**

Enclosed current:

$$
I_{\text{enc}}(r) = J_0 \pi r^2
$$

Ampère’s law:

$$
B_\phi(r) (2\pi r) = \mu_0 I_{\text{enc}}(r)
$$

Hence

$$
B_\phi(r) = \frac{\mu_0 J_0 r}{2}
          = \frac{\mu_0 I_0}{2\pi a^2} r
$$

So

$$
\vec B(r) = \hat \phi \frac{\mu_0 I_0}{2\pi a^2}\, r, \qquad r < a
$$

**Outside ($r \ge a$)**

Enclosed current:

$$
I_{\text{enc}} = I_0 = \pi a^2 J_0
$$

Ampère’s law:

$$
B_\phi(r) (2\pi r) = \mu_0 I_0
$$

So

$$
\vec B(r) = \hat \phi \frac{\mu_0 I_0}{2\pi r}, \qquad r \ge a
$$

> Inside: $B \propto r$.  
> Outside: $B \propto 1/r$.  
> Direction: $\hat \phi$ (circulates around the wire).

---

## 8. Vector Magnetic Potential $\vec A$

Analogy to electrostatics:

- Electrostatics: scalar potential $V$ with $\vec E = -\nabla V$.
- Magnetostatics: **vector potential** $\vec A$ with
  $$
  \nabla \cdot \vec B = 0 \quad \Rightarrow \quad \vec B = \nabla \times \vec A
  $$

We can derive $\vec A$ from Ampère’s law. For **volume current density** $\vec J$ in vacuum:

$$
\vec A(\vec R) = \frac{\mu_0}{4\pi} \int_\Omega \frac{\vec J(\vec R')}{|\vec R - \vec R'|}\, d\Omega'
$$

This gives an **indirect** way to find $\vec B$:

1. Compute $\vec A(\vec R)$.
2. Take the curl: $\vec B = \nabla \times \vec A$.

### 8.1 Vector Potential for Different Current Distributions

- **Volume distribution**:
  $$
  \vec A(\vec R)
  = \frac{\mu_0}{4\pi} \int_\Omega
    \frac{\vec J(\vec R')}{|\vec R - \vec R'|}\, d\Omega'
  $$
- **Surface distribution**:
  $$
  \vec A(\vec R)
  = \frac{\mu_0}{4\pi} \int_S
    \frac{\vec J_S(\vec R')}{|\vec R - \vec R'|}\, dS'
  $$
- **Line distribution**:
  $$
  \vec A(\vec R)
  = \frac{\mu_0 I}{4\pi} \oint_C
    \frac{d\vec \ell'}{|\vec R - \vec R'|}
  $$

---

## 9. Biot–Savart’s Law

Starting from the line-current form of $\vec A$ and using $\vec B = \nabla \times \vec A$, we obtain **Biot–Savart’s law**.

### 9.1 Line Current (standard Biot–Savart form)

For a filamentary current $I$ along a closed path $C$:

$$
\vec B(\vec R)
= \frac{\mu_0 I}{4\pi} \oint_C
  \frac{d\vec \ell' \times (\vec R - \vec R')}
       {|\vec R - \vec R'|^3}
$$

Here:

- $\vec R$: observation point.  
- $\vec R'$: source point on the wire.  
- $d\vec \ell'$: differential line element at $\vec R'$.

### 9.2 Different Current Distributions

- **Volume distribution**:
  $$
  \vec B(\vec R)
  = \frac{\mu_0}{4\pi} \int_\Omega
    \frac{\vec J(\vec R') \times (\vec R - \vec R')}
         {|\vec R - \vec R'|^3}\, d\Omega'
  $$
- **Surface distribution**:
  $$
  \vec B(\vec R)
  = \frac{\mu_0}{4\pi} \int_S
    \frac{\vec J_S(\vec R') \times (\vec R - \vec R')}
         {|\vec R - \vec R'|^3}\, dS'
  $$
- **Line distribution** (same as above):
  $$
  \vec B(\vec R)
  = \frac{\mu_0 I}{4\pi} \oint_C
    \frac{d\vec \ell' \times (\vec R - \vec R')}
         {|\vec R - \vec R'|^3}
  $$

Note: $C$ must be a **closed path** (otherwise there is no steady current).

---

## 10. Example: Finite Straight Wire (Line Current)

We consider a thin straight wire of length $2L$ carrying a current $I$ along the $z$-axis, from $z=-L$ to $z=+L$.

We want $\vec B$ at point $P$ in cylindrical coordinates $(r,\phi=0,z=0)$ (on the mid-plane of the wire).

Using Biot–Savart’s law for a line current:

$$
\vec B(\vec R)
= \frac{\mu_0 I}{4\pi} \int_{-L}^{L}
  \frac{d\vec \ell' \times (\vec R - \vec R')}
       {|\vec R - \vec R'|^3}
$$

With $d\vec \ell' = \hat z\,dz'$ and $\vec R - \vec R' = \hat r\,r - \hat z\,z'$:

After integration (see Ulaby for full derivation):

$$
\vec B(r)
= \hat \phi\, \frac{\mu_0 I L}{2\pi r \sqrt{r^2 + L^2}}
$$

**Special case: infinite wire**

If $L \gg r$ (i.e., wire effectively infinite):

$$
\vec B(r) \approx \hat \phi \frac{\mu_0 I}{2\pi r}
$$

which matches the result from Ampère’s law.

---

## 11. Circular Loop Current

A circular loop of radius $a$, carrying current $I$.  
We look along the axis of the loop $(x=y=0, z\ \text{variable})$.

Using Biot–Savart’s law (axial field):

$$
\vec B(z)
= \hat z\, \frac{\mu_0 I a^2}{2(a^2 + z^2)^{3/2}}
\qquad (x = y = 0)
$$

Special cases:

- **At the centre of the loop** ($z = 0$):
  $$
  \vec B(0) = \hat z\, \frac{\mu_0 I}{2a}
  $$

- **Far away along the axis** ($|z| \gg a$):
  $$
  \vec B(z) \approx \hat z\, \frac{\mu_0 I a^2}{2|z|^3}
  $$

This is the classic **magnetic dipole** far-field behaviour.

---

## 12. Three Methods to Calculate $\vec B$

From the “Three methods” slide:

1. **Ampère’s circuital law**
   $$
   \oint_C \vec B \cdot d\vec \ell = \mu_0 I_{\text{enc}}
   $$
   - Integral **equation**.  
   - Needs **high symmetry** for an analytic solution (infinite wire, solenoid, etc.).

2. **Biot–Savart’s law**
   $$
   \vec B(\vec R)
   = \frac{\mu_0 I}{4\pi} \oint_C
     \frac{d\vec \ell' \times (\vec R - \vec R')}
          {|\vec R - \vec R'|^3}
   $$
   - Integral **expression** for $\vec B$.  
   - Analytic solution possible for some simple geometries (straight wire, loop).  
   - Often solved **numerically** for complex geometries.

3. **Indirect field via vector potential**
   $$
   \vec A(\vec R)
   = \frac{\mu_0 I}{4\pi} \oint_C
     \frac{d\vec \ell'}{|\vec R - \vec R'|}
   $$
   then
   $$
   \vec B = \nabla \times \vec A
   $$
   - Integral expression for $\vec A$ + a curl to get $\vec B$.  
   - Useful in more advanced / numerical formulations (e.g. with magnetic materials).

---

## 13. Summary — Magnetostatics I (Collected Key Formulas)

### 13.1 Magnetostatics (vacuum, steady dc)

- Differential form:
  $$
  \nabla \times \vec H = \vec J_{dc}, \qquad
  \nabla \cdot \vec B = 0
  $$
- Integral form:
  $$
  \oint_C \vec B \cdot d\vec \ell = \mu_0 I_{dc}, \qquad
  \oint_S \vec B \cdot d\vec s = 0
  $$

### 13.2 Electromagnetic forces

- Electric force:
  $$
  \vec F_e = q\vec E
  $$
- Magnetic force:
  $$
  \vec F_m = q\,\vec u \times \vec B
  $$
- Lorentz force:
  $$
  \vec F_{em} = q(\vec E + \vec u \times \vec B)
  $$

### 13.3 Magnetic flux density and vector potential

- Definition of $\vec B$ (via test charge):  
  $\vec F_m = q_0\,\vec u \times \vec B$ for small $q_0$.
- Vector magnetic potential:
  $$
  \vec B = \nabla \times \vec A
  $$

### 13.4 Fields from a Straight Wire

- **Finite wire length $2L$**:
  $$
  \vec B(r)
  = \hat \phi\, \frac{\mu_0 I L}{2\pi r \sqrt{r^2 + L^2}}
  $$
- **Infinite wire**:
  $$
  \vec B(r)
  = \hat \phi\, \frac{\mu_0 I}{2\pi r}
  $$

### 13.5 Field from Circular Loop (on axis)

$$
\vec B(z) = \hat z\, \frac{\mu_0 I a^2}{2(a^2 + z^2)^{3/2}}
$$

Centre:

$$
\vec B(0) = \hat z\, \frac{\mu_0 I}{2a}
$$

Far field ($|z| \gg a$):

$$
\vec B(z) \approx \hat z\, \frac{\mu_0 I a^2}{2|z|^3}
$$

### 13.6 Magnetic Field and Potential from Currents (general forms)

Let $\vec R$ be the observation point and $\vec R'$ the source point.

**Volume distribution**:

$$
\vec B(\vec R)
= \frac{\mu_0}{4\pi} \int_\Omega
  \frac{\vec J(\vec R') \times (\vec R - \vec R')}
       {|\vec R - \vec R'|^3}\, d\Omega',
\qquad
\vec A(\vec R)
= \frac{\mu_0}{4\pi} \int_\Omega
  \frac{\vec J(\vec R')}{|\vec R - \vec R'|}\, d\Omega'
$$

**Surface distribution**:

$$
\vec B(\vec R)
= \frac{\mu_0}{4\pi} \int_S
  \frac{\vec J_S(\vec R') \times (\vec R - \vec R')}
       {|\vec R - \vec R'|^3}\, dS',
\qquad
\vec A(\vec R)
= \frac{\mu_0}{4\pi} \int_S
  \frac{\vec J_S(\vec R')}{|\vec R - \vec R'|}\, dS'
$$

**Line distribution**:

$$
\vec B(\vec R)
= \frac{\mu_0 I}{4\pi} \oint_C
  \frac{d\vec \ell' \times (\vec R - \vec R')}
       {|\vec R - \vec R'|^3},
\qquad
\vec A(\vec R)
= \frac{\mu_0 I}{4\pi} \oint_C
  \frac{d\vec \ell'}{|\vec R - \vec R'|}
$$

> No discrete magnetic charges — **currents only** are the sources of magnetostatic fields.

---
