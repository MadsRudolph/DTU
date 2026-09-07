---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-09-03
week: 36
lecture: 2
topic: "Analogies: Mechanical Systems"
lecturer: FL
tags: [Electroacoustics, lecture-note, analogies, mechanical-systems]
---
# Lecture 2 — Analogies: Mechanical Systems

> [!info] Lecture Info
> **Date:** Thursday 3 September 2026, 8:30–12:00 · Lyngby · **FL**
> **Slides:** `Slides/34870_Lecture2_03092026.pdf` (24 pages)
> **Previous:** [[Lecture 1 - Analogies - Introduction|Lecture 1 — introduction]] · **Next:** [[Lecture 3 - Analogies - Acoustic Systems|Lecture 3 — acoustic systems]]

> [!abstract] Where this lecture sits
> Lecture 1 gave the general analogy framework and the two competing conventions (impedance vs. through/across). This lecture applies it concretely to **mechanical** systems — dampers, springs, masses, sources — with a full worked 1-DOF resonator, then a real numeric 2-DOF shaker example. Direct template for [[Lecture 3 - Analogies - Acoustic Systems|Lecture 3]]'s acoustic derivations.

---

## 1. Repetition pop quiz — answered

> [!question]+ 1. Analogies (from lecture 1)
> **What are lumped elements?** A spatially-distributed component approximated, under certain assumptions, as a discrete idealized element with properties concentrated at one point (PDE → ODE).
> **What are equivalent circuits?** A network of such lumped elements described by a linear system of ODEs, solvable analytically.
> **What are their limitations?** Object dimensions ≪ wavelength; homogeneous properties; idealized behaviour (no parasitics, incompressible/massless/lossless as applicable, rigid bodies/walls as applicable).

> [!question]+ 2. Mechanical systems
> **What are the mechanical network variables?** Force $f$ (N) and velocity $u$ (m/s).
> **What are the lumped mechanical elements?** Damper $R_M$ (real/loss), mass $M_M$ (differential), compliance $C_M$ (integral) — full definitions in §3.
> **Difference between mechanical impedance and mobility analogy?** In the **impedance analogy**, mass ⇔ inductor and compliance ⇔ capacitor (matches the electrical intuition directly). In the **mobility (through/across) analogy**, it's inverted: compliance ⇔ inductor, mass ⇔ capacitor — because velocity is mapped to voltage instead of current. Same physics, different circuit-drawing convention — see [[Lecture 1 - Analogies - Introduction#7. Lumped elements — real, mass, compliance (both mechanical & acoustic)|Lecture 1 §6]] for the full swapped tables.

### Repetition tables (carried over from Lecture 1)

> [!note] Domain variable & impedance table
> | | Electrical | Mechanical | Acoustic |
> |---|---|---|
> | Impedance | $Z=v/i$ | $Z_M=f/u$ | $Z_A=p/U$ |
>
> **Network ≠ Impedance** — mapping network variables (to create the analogy) can be done via *impedance mapping* or *network mapping*; they aren't automatically identical.

> [!note] Impedance analogy vs. through/across analogy — side by side
> | | Impedance analogy | Through/across (mobility) analogy |
> |---|---|---|
> | mass $M_M$ | inductor $L$ | capacitor $C$ |
> | compliance $C_M$ | capacitor $C$ | inductor $L$ |
> | damper $R_M$ | resistor $R$ | conductance $1/R$ |
> | acoustic mass $M_A$ | inductor $L$ | capacitor $C$ |
> | acoustic compliance $C_A$ | capacitor $C$ | inductor $L$ |

---

## 2. Mechanical network variables & elements

> [!abstract] Definitions
> **Variables:** force $f$ (N), velocity $u$ (m/s)
>
> | Element | Defining relation | Unit |
> |---|---|---|
> | Damper | $R_M = \dfrac{f}{u}$ | Ns/m = kg/s |
> | Compliance | $C_M = \dfrac{x}{f} = \dfrac{1}{j\omega}\dfrac{u}{f}$ | m/N = s²/kg |
> | Mass | $M_M = \dfrac{f}{a} = \dfrac{1}{j\omega}\dfrac{f}{u}$ | Ns²/m = kg |

> [!note] Physical dependence & validity
> $M_M = \rho V$ (density × volume); $C_M \propto L/(ES)$ (length / elasticity·area); $R_M \propto \mu, S, \ldots$ (viscosity, geometry).
> Lumped mechanical elements are only valid for specific assumptions (e.g. **rigid masses**) and within certain **(low) frequencies** — same warning as everywhere else in this course.

---

## 3. Exercise — Mechanical resonator, 1-DOF (worked through)

> [!example] Setup
> Identify and label the velocity of every mass. Newton's 1st law (force nodal rule):
> $$f = f_M + f_C + f_R$$
> $$f = M_M\frac{du}{dt} + \frac{1}{C_M}\int u\,dt + R_M u = j\omega M_M u + \frac{1}{j\omega C_M}u + R_M u$$
> $$f = \left(j\omega M_M + \frac{1}{j\omega C_M} + R_M\right)u = Z_M u$$

> [!success] Result — impedance analogy (series impedances)
> $$Z_M = \frac{f}{u} = j\omega M_M + \frac{1}{j\omega C_M} + R_M$$
>
> Converting to the dual admittance/mobility form (parallel admittances):
> $$Y_M = \frac{u}{f} = \frac{1}{Z_M} = \frac{1}{\dfrac{1}{j\omega M_M} + j\omega C_M + \dfrac{1}{R_M}}$$
> $$\boxed{Y_M = \frac{1}{j\omega M_M} \;\|\; j\omega C_M \;\|\; \frac{1}{R_M}} \quad\text{(parallel admittances)}$$

> [!important] Drawing the equivalent circuit
> - **Set a reference point (zero velocity)** for the mass — i.e. ground it — and **always show this explicitly** in the mechanical sketch. This is the mechanical-domain analogue of "ground the compliance" that comes back in [[Lecture 3 - Analogies - Acoustic Systems#7. In-class exercises — Helmholtz resonator & box with two tubes|Lecture 3 §7]].
> - Draw the mechanical "circuit" (optional, but helps).
> - Draw the equivalent electrical circuit: $M_M$, $C_M$, $R_M$ **in series** (impedance analogy) — spring and damper fixed at one end ($u_2=0$), other end fixed to the mass ($u_1=u$).
> - Confirm the impedance/admittance expression matches the equations above.
>
> ```mermaid
> graph LR
>     F((f source)) --> MM[M_M] --> CM[C_M] --> RM[R_M] --> GND((u = 0, ground))
> ```

---

## 4. Problem solving (in-class, part 1)

> [!todo] Problem 2.1 — Graphical conversion
> a) Convert a given impedance-analogy equivalent circuit into its **dual mobility analogy** circuit.
> b) Draw the **mechanical** circuit/sketch corresponding to that impedance-analogy circuit.
>
> **Space to fill in during class:**
> - a) dual circuit: ⬜
> - b) mechanical sketch: ⬜

---

## 5. Lumped elements in detail, with derivation examples

> [!abstract] Mass — with reference point!
> $$Z_M = \frac{f}{u} = j\omega M_M \qquad Y_M = \frac{u}{f} = \frac{1}{j\omega M_M}$$
> **Example — continuous rigid body:**
> $$M_M = \rho V = \rho\int_0^L S(x)\,dx = \rho L S$$
> ($\rho$ = density, $L$ = length, $S$ = cross-section area, $V$ = volume)

> [!abstract] Spring / compliance
> $$Z_M = \frac{f}{u} = \frac{1}{j\omega C_M} \qquad Y_M = \frac{u}{f} = j\omega C_M$$
> **Example — elastic rod:**
> $$C_M = \frac{L}{ES}$$
> ($E$ = elasticity/Young's modulus, $L$ = length, $S$ = area)

> [!abstract] Damper / loss element
> $$Z_M = \frac{f}{u} = R_M \qquad Y_M = \frac{u}{f} = \frac{1}{R_M}$$
> **Example — viscous cylindrical damper** (e.g. bike/car shocks): shear stress between two parallel plates, $\tau = \mu\, u/g$.
> $$R_M \approx \frac{f}{u} = \frac{\tau A}{u} = \frac{\mu A}{g} = \frac{2\pi\mu r L}{g}$$
> ($\mu$ = viscosity, $L,r,g$ = geometry — length, radius, gap)

---

## 6. Sources

> [!note] Force source (ideal)
> $$f = \sum_i f_i$$
> Examples: **Lorentz force**, Coulomb force, inverse piezoelectric effect.

> [!note] Velocity source (ideal)
> Fixes $u_1-u_2$ independent of the force drawn.
> Examples: external vibrations, a rotating system driving a piston.

> [!important] Real sources — finite output impedance/admittance
> Real source = ideal source **+ output impedance $Z_0$** (or admittance $Y_0$). Two equivalent models:
> - **Thévenin** (force source $f_{Th}$ in series with $Z_0$)
> - **Norton** (velocity source $u_{No}$ in parallel with $Z_0$/$Y_0$)
>
> Conversion:
> - Impedance analogy: $f_{Th} = Z_0\, u_{No}$
> - Mobility analogy: $u_{Th} = Y_0\, f_{No}$

> [!question] Exercise — "Which circuit is correct?"
> An in-class multiple-choice check on drawing sources correctly (impedance vs. mobility analogy). Work through the reasoning live and fill in:
> - Answer: ⬜
> - Why the others are wrong: ⬜

---

## 7. Exercise — Vibration exciter (shaker), 2-DOF

> [!example] The physical picture
> - **Shaker ≈ loudspeaker** (electrodynamic actuator).
> - **Stinger** = stiff metal rod connecting shaker to the device under test.
> - **DUT** = free mass $M_{DUT}$.
>
> **Equivalent mechanical circuit:** a mechanical resonator ($Z_M = R+j\omega M+1/j\omega C$) with a spring **mechanically in series** (the stinger) and a mass **mechanically in parallel** (the DUT).

> [!success] Numeric example — worked resonances
> $$R_{res}=40\ \text{Ns/m},\quad M_{res}=100\ \text{g},\quad C_{res}=10^{-5}\ \text{m/N},\quad C_{sting}=10^{-8}\ \text{m/N},\quad M_{DUT}=250\ \text{g},\quad f_0=10\ \text{N}$$
>
> Tasks: plot the mechanical transfer function and input impedance; find all (anti-)resonances (type, frequency, $Q$).
>
> **Given results (from the slides — use these to check your own plot):**
> | | Type | Frequency | $Q$ |
> |---|---|---|---|
> | 1st | impedance minimum = resonance | $f_1 = 85\ \text{Hz}$ | $Q_1 = 4.7$ |
> | 2nd | impedance maximum = anti-resonance | $f_2 = 3.183\ \text{kHz}$ | $Q_2 \to \infty$?! |
> | 3rd | impedance minimum = resonance | $f_1 = 5.956\ \text{kHz}$ | $Q_1 = 132$ |
>
> The $Q_2\to\infty$ flagged with a "?!" on the slide is worth asking about live — an ideal anti-resonance with no damping path *can* look like infinite $Q$ in this idealized 2-DOF model; worth confirming what physically limits it in practice (the stinger/DUT losses that were neglected).

---

## 8. Problem solving (in-class, part 2)

> [!todo] Problem 2.2 — Mass on a spring
> a) Model a mass on a spring: $M_M = 20\ \text{g}$, spring stiffness $k=1000\ \text{N/m}$ (⚠️ note: $C_M = 1/k$), damping $R_M = 0.5\ \text{Ns/m}$ — these are **typical low-frequency loudspeaker mechanical parameters**.
> b) Drive with a **force** of 10 N — plot the velocity frequency response. Describe the behaviour quantitatively.
> c) Drive with a **velocity** of 1 m/s — plot the force exerted by the source. Explain why the response looks different from (b).
> *(This (b) vs (c) contrast is exactly the impedance-source vs. mobility-source distinction from §6 — a force-driven vs. velocity-driven resonator peak/dip at resonance in opposite ways.)*
>
> **Working space:** $C_M = $ ⬜ · resonance $f_0 = $ ⬜

> [!todo] Problem 2.3 — Loudspeaker driver as equivalent source
> Using the driver from Problem 2.2, set up equivalent circuits in **both** impedance and mobility analogy, driven by a harmonic **Lorentz force** of 10 N.
> a) Calculate impedance and admittance.
> b) Set up the correct Norton/Thévenin force source for each analogy.
> c) Convert the force source into a velocity source — what's the equivalent velocity **at resonance**?
>
> **Working space:** ⬜

> [!todo] Problem 2.4 — Two-mass system
> Build an equivalent circuit model of a two-mass system (masses $M_1, M_2$ coupled via $C_1, R_1$). Use LTspice to check $u_1$ and $u_2$ vs. frequency, then investigate these limiting cases against that reference:
> - $M_1\to\infty$
> - $M_2\to\infty$
> - $C_1\to 0$
> - $R_1\to\infty$
> - $R_1\to 0\ \&\ C_1\to\infty$
>
> *(Hint for intuition while filling this in: each limit effectively removes or rigidifies one element — e.g. $M_1\to\infty$ pins that mass in place, $R_1\to 0\ \&\ C_1\to\infty$ makes the coupling a rigid short. Predict the qualitative effect before running LTspice, then compare.)*
>
> **Working space:**
> - $M_1\to\infty$: ⬜
> - $M_2\to\infty$: ⬜
> - $C_1\to 0$: ⬜
> - $R_1\to\infty$: ⬜
> - $R_1\to0\ \&\ C_1\to\infty$: ⬜

---

## Summary — what to walk away with

> [!success] Key takeaways
> - Mechanical $R_M$, $C_M$, $M_M$ defined exactly like their electrical counterparts once you fix $f\leftrightarrow$ across/through convention — same $j\omega$-method algebra.
> - **Impedance analogy:** mass↔inductor, compliance↔capacitor. **Mobility analogy:** the reverse. Always state which one a circuit uses.
> - Series mechanical elements (impedance analogy) driven by a force source, summed like series impedances; the dual (mobility) is a parallel admittance network.
> - **Always ground the zero-velocity reference point** in a mechanical sketch — same discipline as grounding acoustic compliances later.
> - Real sources = ideal source + finite $Z_0$/$Y_0$; Norton ⇔ Thévenin conversion is $f_{Th}=Z_0 u_{No}$ (impedance analogy) or $u_{Th}=Y_0 f_{No}$ (mobility analogy).
> - The shaker 2-DOF example is the template for reading off resonances/anti-resonances and $Q$ straight from an impedance plot — useful pattern-matching skill for the rest of the course.

> [!tip] Looking ahead
> [[Lecture 3 - Analogies - Acoustic Systems|Lecture 3]] repeats this whole exercise for acoustic systems, but goes one step further and **derives** $R_A$, $C_A$, $M_A$ from the physics of a plane-wave tube instead of just stating them.
