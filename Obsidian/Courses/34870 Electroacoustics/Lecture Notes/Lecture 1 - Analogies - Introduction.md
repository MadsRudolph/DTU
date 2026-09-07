---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-08-31
week: 36
lecture: 1
topic: "Analogies: Introduction"
lecturer: FL
tags: [Electroacoustics, lecture-note, analogies]
---
# Lecture 1 — Analogies between Electrical, Mechanical & Acoustic Systems: Introduction

> [!info] Lecture Info
> **Date:** Monday 31 August 2026, 13:00–17:00 · room 019, building 352 · **FL**
> **Slides:** `Slides/34870_Lecture1_31082026.pdf` (30 pages)
> **Previous:** [[Lecture 0 - Course Introduction|Lecture 0 — course intro]] · **Next:** [[Lecture 2 - Analogies - Mechanical Systems|Lecture 2 — mechanical systems]]

> [!abstract] Where this lecture sits
> First technical lecture. Sets up **why** analogies work at all, the ground rules (lumped elements, equivalent circuits), and derives the electrical ⇔ mechanical ⇔ acoustical variable table that every later lecture reuses.

---

## 1. Preparation & repetition (things you should already know)

> [!todo] Refresh before/during this lecture
> **Electrical circuit analysis:**
> - Kirchhoff's laws
> - Active elements: current & voltage sources
> - Passive elements: R, L, C
> - Complex numbers — amplitude, phase, polar form
> - Impedance & admittance
> - Duality and dual circuits
> - Norton & Thévenin equivalents
>
> **LTspice:** use the Quick Guide, build and calculate simple circuits.

---

## 2. Analogies and equivalent circuits

> [!question]+ Q&A from the slides (answered)
> **Q: What is a physics analogy?**
> A method of representing one physical system by an analogous physical system — here, mechanical and acoustical systems represented by a corresponding electrical system.
>
> **Q: Why use analogies?**
> It lets you reuse familiar, powerful electrical-engineering methods in other domains, and a common framework lets you connect different physical domains in **one single model**.
>
> **Q: When can we use analogies?**
> When different physical domains have **analogous mathematical behaviour** — i.e. are described by similar constitutive equations — you can build corresponding elements for each domain.
>
> **Q: Why specifically represent other domains as an electrical system?**
> Electrical engineering already has powerful tools for very complex systems: circuits of connected, discrete ("lumped") elements, solved with linear network analysis. That machinery transfers directly once the mechanical/acoustical system is expressed the same way.
>
> **Q: What is a lumped element?**
> Under certain assumptions, a spatially-distributed component is approximated as a discrete, idealized element with its properties concentrated at one point — the describing PDE collapses to an ODE.
>
> **Q: What is an equivalent circuit?**
> Idealized lumped elements connected into a linear network, described by a linear system of ODEs solvable analytically.

### Limitations of the lumped-element analogy

> [!warning] Assumptions required
> - Real dimensions **much smaller than the wavelength** — electrical, mechanical, *and* acoustic domains alike.
> - **Homogeneous** element properties.
> - **Idealized** element behaviour, e.g.: no parasitic effects; incompressible **or** massless **or** lossless (depending on which element); rigid bodies/walls (depending on the element).
> - → Under these assumptions, you get an **analytical solution using linear algebra**.

> [!note] When the assumptions break down
> - **Distributed element models** (e.g. transmission lines / transfer matrices in electrical engineering) — needs calculus (infinitesimal description).
> - **FEM / BEM** (finite/boundary element method) — numerical methods solving the full PDE on a mesh of small elements.

> [!example] Demo: MEMS microphone model
> A MEMS microphone (~3.5 × 2.65 × 0.98 mm³) modelled as a full LTspice equivalent circuit: mechanical/acoustic elements ($R_{a\_i}, M_{a\_i}, C_{a\_f}, R_{a\_v}, M_{a\_v}$…) plus radiation impedance terms ($C_{rad}, R_{rad1}, R_{rad2}, M_{rad}$) driven through dependent sources (E1/F1/G1/G2) from an AC input. This is the *payoff* of the whole analogy approach — an entire transducer reduced to something LTspice can simulate directly.

---

## 3. Repetition pop quiz — answered

> [!question]+ 1. Complex numbers
> - Complex variables, polar form; complex plane / polar plot.
> - **Watch out for:** the *definition* of amplitude and phase, **counter-clockwise** phase rotation convention, and vector/phasor calculus rules (they aren't quite the same as plain complex-number algebra when you also track a rotating $e^{j\omega t}$).

> [!question]+ 2. Complex functions
> - Time-domain formulation → transient plot. Frequency-domain formulation → Bode plot.
> - **Watch out for:** angular frequency $\omega=2\pi f$ vs. $f$; phase direction convention; the definitions of **resonance** and **anti-resonance**; **bandwidth** and **quality factor** $Q$.

> [!question]+ 3. Units
> - Effective (RMS) variables vs. relative (dB) units.
> - **Watch out for:** the definition of RMS **depends on the waveform** (sine ≠ square ≠ triangle); dB always needs a **reference value**; use $\log_{10}$, not $\ln$; amplitude ratios use $20\log_{10}$, power ratios use $10\log_{10}$; logarithmic calculus (adding dB = multiplying ratios).

### The $j\omega$ method (time ⇔ frequency domain)

> [!abstract] Core relations
> Time-harmonic signal: $x(t) = A_x\cos(\omega t+\varphi_x)$, with $\omega=2\pi f$, $j=\sqrt{-1}$.
>
> Euler form: $\underline{x}(t) = A_x\, e^{j(\omega t+\varphi_x)}$ (or its complex conjugate), and in the frequency domain this simplifies to the phasor $\underline{x} = A_x e^{j\varphi_x}$.
>
> | Operation | Time-domain | Frequency-domain |
> |---|---|---|
> | Differentiation | $w(t) = dx(t)/dt$ | $\underline{w} = j\omega\,\underline{x}$ |
> | Integration | $w(t) = \int x(t)\,dt$ | $\underline{w} = \dfrac{1}{j\omega}\underline{x}$ |
> | Addition | $w(t) = x_1(t)+x_2(t)$ | $\underline{w} = \underline{x}_1+\underline{x}_2$ |
>
> This is *the* trick that turns ODEs into algebra for every circuit in this course.

---

## 4. Network analysis (repetition)

> [!note] The 4-step recipe
> 1. Define lumped elements with a concentrated physical property.
> 2. Build the circuit model (lumped elements + ideal connections + network variables: through/flow/effect, across/difference).
> 3. Set up **meshes** (M) and **nodes** (N) → system of linear equations.
> 4. Calculate network variables, output, transmission, etc.

> [!abstract] Network variables via power conjugates
> Power-conjugate variables: two domain variables whose **product is power**.
>
> | | Electrical |
> |---|---|
> | voltage | $v$ (V) |
> | current | $i$ (A) |
> | power | $P=vi$ (W) |
> | impedance | $Z=v/i$ (Ω) |
> | admittance | $Y=i/v$ (S) |
>
> Passive elements are described by impedance **or** admittance (mobility) — network variables are interchangeable due to **duality**.

### Duality of electrical circuits

> [!important] Dual-circuit transformation table
> | | Impedance-analogy | | | | Dual (admittance) |
> |---|---|---|---|---|---|
> | Complex relation | $Z=1\ \Omega$ | $v=Zi$ | $\Leftrightarrow$ | $i=Yv$ | $Y=1\ \text{S}$ |
> | Real element | $R=1\ \Omega$ | $v=Ri$ | $\Leftrightarrow$ | $i=Gv,\ G=1/R$ | $G=1\ \text{S}$ |
> | Diff. element (+j) | $L=1\ \text{H}$ | $v_L=L\,di_L/dt=j\omega L i_L$ | $\Leftrightarrow$ | $i_C=C\,dv_C/dt=j\omega C v_C$ | $C=1\ \text{F}$ |
> | Int. element (−j) | | $v_C=\frac{1}{C}\int i_C\,dt = \frac{1}{j\omega C}i_C$ | $\Leftrightarrow$ | $i_L=\frac{1}{L}\int v_L\,dt=\frac{1}{j\omega L}v_L$ | |
> | Series | $Z_1,Z_2$ | $Z=Z_1+Z_2$ | $\Leftrightarrow$ | $Y=Y_1\|Y_2$ | parallel |
> | Parallel | $Z_1,Z_2$ | $Z=Z_1\|Z_2$ | $\Leftrightarrow$ | $Y=Y_1+Y_2$ | series |
>
> Rule of thumb: going to the dual circuit swaps **series ⇔ parallel**, **mesh ⇔ node**, $\sum v=0 \Leftrightarrow \sum i = 0$, and swaps every element for its dual ($R\leftrightarrow G$, $L\leftrightarrow C$).

---

## 5. Problem solving (in-class, part 1)

> [!todo] Problem 1.1 — Validate the duality of electrical circuits
> Given a circuit with $Z_1$ (series) feeding a parallel $Z_2$/$Z_3$ combination:
> 1. **Mathematical proof:** show $v=Zi$, $\sum_{\text{mesh}}v=0$ ⇔ $i=Yv$, $\sum_{\text{node}}i=0$ leads to the dual admittance network ($Y_1$ parallel feeding series $Y_2$/$Y_3$... work through the mesh/node equations by hand).
> 2. **LTspice model validation.** ⚠️ Note: LTspice works in impedance, so **units change** when you build the dual circuit — don't just copy component values across.
>
> **Space to fill in:** ⬜

> [!todo] Problem 1.2 — Validate the duality of AC electrical circuits
> Same idea as 1.1 but for an AC (frequency-dependent) circuit — work it through in class.
>
> **Space to fill in:** ⬜

---

## 6. Electrical, mechanical & acoustic systems — the full variable table

> [!abstract] Domain variable table
> | | Electrical | Mechanical (translational) | Mechanical (rotational) | Acoustic |
> |---|---|---|---|---|
> | Potential/across | voltage $v$ (V) | force $f$ (N) | torque | pressure $p$ (Pa = N/m²) |
> | Kinetic/through | current $i$ (A) | velocity $u$ (m/s) | angular velocity | vol. velocity $U$ (m³/s) |
> | Power | $vi$ (W) | $fu$ (Nm/s = W) | — | $pU$ (Pa·m³/s = W) |
> | Impedance | $v/i$ (Ω) | $f/u$ (Ns/m = kg/s) | — | $p/U$ (Pa·s/m³) |
> | Admittance | $i/v$ (S) | $u/f$ (m/Ns = s/kg) | — | $U/p$ (m³/Pa·s) |
>
> Two named analogy conventions: the **impedance analogy** and the **through-and-across analogy** (a.k.a. mechanical mobility/admittance analogy).

> [!important] Network ≠ Impedance!
> Mapping network *variables* is what creates the analogy — you can do it via **impedance mapping** or **network (topology) mapping**, and they are not automatically the same thing. This distinction is exactly why there are two different tables below (impedance analogy vs. through/across analogy) with mass/compliance swapped between mechanical and electrical.

### Impedance analogy

> [!note] Impedance analogy table
> | | Electrical | Mechanical | Acoustical |
> |---|---|---|---|
> | Potential var. | voltage $v$ | force $f$ | pressure $p$ |
> | Kinetic var. | current $i$ | velocity $u$ | vol. velocity $U$ |
> | Across | voltage $v$ | — | pressure $p$ |
> | Through | current $i$ | — | vol. velocity $U$ |
> | Real elem. $K$ | resistor $R$ | damper $R_M$ | acoustic loss $R_A$ |
> | Diff. elem. $j\omega K$ | inductor $L$ | mass $M_M$ | acoustic mass $M_A$ |
> | Int. elem. $1/j\omega K$ | capacitor $C$ | compliance $C_M$ | acoustic compliance $C_A$ |

### Through/across analogy (mechanical mobility)

> [!note] Through/across table — note mass and compliance swap roles vs. the impedance analogy!
> | | Electrical | Mechanical | Acoustical |
> |---|---|---|---|
> | Across | voltage $v$ | velocity $u$ | pressure $p$ |
> | Through | current $i$ | force $f$ | vol. velocity $U$ |
> | Real elem. $K$ | resistor $R$ | damper $1/R_M$ | acoustic loss $R_A$ |
> | Diff. elem. $j\omega K$ | inductor $L$ | compliance $C_M$ | acoustic mass $M_A$ |
> | Int. elem. $1/j\omega K$ | capacitor $C$ | mass $M_M$ | acoustic compliance $C_A$ |

> [!warning] This swap is the single most common source of confusion in this course
> In the **impedance analogy**, mechanical mass ⇔ electrical inductor and compliance ⇔ capacitor. In the **through/across (mobility) analogy**, it flips: mechanical compliance ⇔ inductor, mass ⇔ capacitor. Always check which analogy a given circuit diagram is using before reading off values.

---

## 7. Lumped elements — real, mass, compliance (both mechanical & acoustic)

> [!abstract] Mechanical damper / Acoustic loss (real element)
> **Mechanical:** viscous/frictional loss. $R_M = f/u$, unit $\text{Ns/m} = \text{kg/s}$.
> $$f_{R_M} = R_M(u_1-u_2) = R_M u \;\Rightarrow\; u = \frac{1}{R_M}f$$
> **Acoustic:** porous materials (mineral wool, foam, textiles) → purely resistive impedance $R_A=p/U$, unit Pa·s/m³ — pressure and flow in phase.
> $$p = p_1-p_2 = R_A U$$

> [!abstract] Mass (differential element, $j\omega K$)
> **Mechanical:** Newton's 2nd law $f=M_M a$, unit $\text{Ns}^2/\text{m} = \text{kg}$.
> $$f_{M_M} = M_M\frac{du}{dt} = j\omega M_M u \;\Rightarrow\; u = \frac{1}{j\omega M_M}f$$
> **Acoustic:** an open-ended air volume (e.g. a tube) approximated as a differential element, unit kg/m⁴.
> $$p_{M_A} = p_1-p_2 = M_A\frac{dU}{dt} = j\omega M_A U$$

> [!abstract] Compliance (integral element, $1/j\omega K$)
> **Mechanical:** Hooke's law $f=kx$, $k=1/C_M$, unit m/N.
> $$f_{C_M} = \frac{1}{C_M}\int_{-\infty}^t (u_1-u_2)\,dt = \frac{1}{j\omega C_M}u$$
> **Acoustic:** a closed air volume (e.g. a box) approximated as an integral element, unit m⁵/N.
> $$p_{C_A} = \frac{1}{C_A}\int_{-\infty}^t U\,dt = \frac{1}{j\omega C_A}U$$

> [!note] Sources (active elements)
> - **Force / velocity sources** (mechanical, ideal): $f=\sum_i f_i$ for a force source; a velocity source fixes $u_1-u_2$.
> - **Pressure / volume-velocity sources** (acoustic, ideal): the direct analogues.
> - These are drawn just like electrical AC voltage/current sources — impedance-analogy and mobility-analogy versions look like mirror images of each other (across becomes through and vice versa).

---

## 8. Problem solving (in-class, part 2)

> [!todo] Problem 1.3 — Series resonator (ref: LTspice Quick Guide)
> - Set up the system of equations for a series R-L-C-type resonator (electrical, then repeat structurally for mechanical/acoustical).
> - Calculate the **resonance frequency**, current, and impedance.
> - Plot current and impedance (amplitude and phase).
> - **Then:** build a **mechanical** and an **acoustical** resonator with the *same* impedance behaviour — what element values are needed? (This is the first real "translate between domains" exercise — good one to actually work through by hand.)
>
> **Working space:**
> - $f_0 = $ ⬜
> - Electrical values: ⬜
> - Mechanical equivalents: ⬜
> - Acoustical equivalents: ⬜

---

## Summary — what to walk away with

> [!success] Key takeaways
> - An analogy works whenever two domains share the same **constitutive equations** — that's the whole justification, not a coincidence.
> - **Lumped element** = distributed component approximated at a point (PDE → ODE), valid only when the object is small compared to the wavelength.
> - There are **two different analogy conventions** (impedance vs. through/across) and they assign mass/compliance to *opposite* electrical elements — always check which one you're looking at.
> - Mechanical & acoustic real/mass/compliance elements all reduce to the same $j\omega$-method algebra as electrical R/L/C once you've picked variables.
> - The $j\omega$ method turns differentiation into $\times j\omega$ and integration into $\div j\omega$ — this is used in every derivation from here on.

> [!tip] Looking ahead
> [[Lecture 2 - Analogies - Mechanical Systems|Lecture 2]] applies all of this specifically to mechanical systems (dampers, springs, masses) with worked resonator examples; [[Lecture 3 - Analogies - Acoustic Systems|Lecture 3]] does the same for acoustics and *derives* $R_A, C_A, M_A$ from first principles (plane-wave tube).
