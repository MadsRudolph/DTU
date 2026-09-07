---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-09-07
week: 37
lecture: 3
topic: "Analogies: Acoustic Systems"
lecturer: FL
tags: [Electroacoustics, lecture-note, analogies, acoustic-systems]
---
# Lecture 3 — Analogies: Acoustic Systems

> [!info] Lecture Info
> **Date:** Monday 7 September 2026, 13:00–17:00 · room 019, building 352 · **FL**
> **Slides:** `Slides/34870_Lecture3_07092026.pdf` (34 pages)
> **Refs:** Beranek §2.4 · Leach §3.3, 3.7, 2.9–2.10 · Jacobsen §1.6.1–1.6.2, 9.2
> **Also today:** Intro to **Lab A** (analogy circuits in LTspice)
> **Previous:** [[Lecture 2 - Analogies - Mechanical Systems|Lecture 2 — mechanical systems]] · **Next:** Lecture 4 — transducers + microphone intro (Th 10/9)

> [!abstract] Where this lecture sits
> Lecture 1–2 built the electrical ⇔ mechanical analogy. Today does the same for **acoustics**, then goes one level deeper than before: instead of just stating $R_A$, $C_A$, $M_A$, we **derive them from the plane-wave tube** — so you know *why* a tube looks like a mass and a closed box looks like a spring, and more importantly, **when that stops being true**.

---

## 1. Repetition — the analogy table so far

> [!note] Through/across analogy (mechanical-mobility form)
> | | Electrical | Mechanical | Acoustical |
> |---|---|---|---|
> | Potential / Across var. | voltage $v$ | velocity $u$ | pressure $p$ |
> | Kinetic / Through var. | current $i$ | force $f$ | vol. velocity $U$ |
> | Impedance | $Z = v/i$ | $Y_M = u/f$ (mobility) | $Z_A = p/U$ |
> | Real element $K$ | resistor $R$ | damper $1/R_M$ | acoustic loss $R_A$ |
> | Differentiating elem. $j\omega K$ | inductor $L$ | compliance $C_M$ | acoustic mass $M_A$ |
> | Integrating elem. $1/j\omega K$ | capacitor $C$ | mass $M_M$ | acoustic compliance $C_A$ |
>
> Mesh ($\sigma=0$) ⇔ voltage/velocity/pressure; Node ($\sigma=0$) ⇔ current/force/vol. velocity.

> [!question]+ Pop quiz (repetition, from lecture 1–2) — answered
> **Q: What is a lumped element?**
> A spatially-distributed physical component, approximated (under certain assumptions) as a discrete, idealized element with its properties concentrated at a single point. Mathematically: the PDE describing the distributed component collapses to an ODE.
>
> **Q: What is an equivalent circuit?**
> A network of idealized lumped elements connected together, described by a linear system of ODEs that can be solved analytically (mesh/node analysis, same as electrical circuits).
>
> **Q: What are their limitations?**
> - Real dimensions must be **much smaller than the wavelength** — electrical, mechanical, *and* acoustic.
> - Element properties must be **homogeneous**.
> - Idealized behaviour assumed: no parasitics; incompressible/massless/lossless (depending on the element); rigid bodies/walls (depending on the element).
> - *(→ this comes back hard today: every acoustic lumped-element formula in this lecture is only valid below some frequency/length limit — see the warning callouts throughout §3.)*
> - Alternatives when the assumptions break: **distributed element models** (transmission lines/transfer matrices, §4) or **numerical methods** (FEM/BEM) solving the full PDE on a mesh.
>
> **Q: What are the acoustic network variables, and the three acoustic lumped elements?**
> Variables: pressure $p$ (Pa) and volume velocity $U$ (m³/s). Elements: $R_A$ (loss/absorber), $C_A$ (compliance), $M_A$ (mass) — full definitions in the table right below.

### Acoustic network variables & elements

> [!abstract] Definitions
> **Variables:** pressure $p$ (Pa), volume velocity $U$ (m³/s)
>
> | Element | Defining relation | Unit |
> |---|---|---|
> | Absorber (loss) | $R_A = \dfrac{p}{U}$ | Pa·s/m³ = kg/(m⁴·s) |
> | Compliance | $C_A = \dfrac{\Delta V}{p} = \dfrac{1}{j\omega}\dfrac{U}{p}$ | m³/Pa = kg⁻¹·m⁴·s² |
> | Mass | $M_A = \dfrac{p}{\dot U} = \dfrac{1}{j\omega}\dfrac{p}{U}$ | Pa·s²/m³ = kg/m⁴ |
>
> Rough physical dependence: $M_A \propto \rho, L, S$ (density, length, area) · $C_A \propto V, \rho, c$ · $R_A \propto \mu,\kappa,\ldots$ (viscosity, thermal conductivity — material-dependent)

> [!warning] The central warning of this lecture
> **Acoustic systems are NOT discrete systems.** A tube or a box is a *continuous, distributed* medium — pressure and flow vary with position and, at high enough frequency, wavelength gets comparable to the object's size. Simple lumped elements ($R_A$, $C_A$, $M_A$) are only an **approximation valid in a limited (usually low) frequency range**. Using a lumped model outside that range gives wrong answers — always check the frequency limit before trusting a lumped circuit.

---

## 2. Problem solving (in-class, part 1) — worked

> [!example]+ Problem 2.1 — Tube in a box (SOLVED)
> An open tube is connected to a closed box, both open and closed (air) volumes connected.
>
> **a) What lumped elements do the tube and the box represent?**
> - The **open tube** → an **acoustic mass** $M_A$ (derived in §3a below: an open-ended air column just sloshes back and forth, pure inertance).
> - The **closed box** → an **acoustic compliance** $C_A$ (derived in §3b: a sealed volume compresses like a spring).
>
> **b) Which assumptions must hold?** (this is just §1's central warning, applied)
> - Low frequency: $l \ll \lambda$, specifically $l^* < \lambda/10$ (Limitation #3, §3a/3b) — otherwise the tube/box stop looking like simple lumped elements.
> - Plane-wave assumption: tube radius $\ll$ wavelength (Limitation #1) — no higher-order modes.
> - Rigid, immobile box walls (compliance derivation assumes a hard boundary).
> - No losses assumed in this idealization — real tube/box would also pick up a small $R_A$ (viscous/thermal boundary losses), ignored here.
>
> **c) Circuit, driven by $U$ from outside:** the tube ($M_A$) in **series** with the box ($C_A$) to ground — this is exactly the **Helmholtz resonator** topology (§7), diagram below.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american]
\draw (0,0) node[ground]{} to[isource, l=$U$] (0,3)
      to[L, l=$M_A$ (tube)] (4,3) coordinate(p)
      to[C, l_=$C_A$ (box)] (4,0) node[ground]{};
\node at (4,3.4) {node $p$};
\end{circuitikz}
\end{document}
```

> [!success] Problem 2.1d — Resonance frequency
> The network is a lossless series $M_A$–$C_A$ pair, so it resonates where the two reactances cancel ($\omega M_A = 1/\omega C_A$):
> $$\omega_0 = \frac{1}{\sqrt{M_A C_A}} \quad\Rightarrow\quad f_0 = \frac{1}{2\pi\sqrt{M_A C_A}}$$
> Substituting $M_A=\rho l^*/S$ and $C_A = V/(\rho c^2)$, the $\rho$ cancels and you get the classic **Helmholtz resonator formula**:
> $$\boxed{f_0 = \frac{c}{2\pi}\sqrt{\frac{S}{l^*\,V}}}$$

> [!example]+ Problem 2.2 — Equivalent circuit, simulated (SOLVED, worked example)
> **KiCad + ngspice project ready to open:** `5. Semester/Electroacoustics/KiCad/Problem_2.1-2.2_Helmholtz_Resonator/Problem_2.1-2.2_Helmholtz_Resonator.kicad_sch` — already wired up with the values below plus a 100 MΩ DC-bias resistor (needed so ngspice has a DC operating point at all — an ideal current source in series with a bare capacitor has none). The `.ac dec 200 10 1000` sweep is embedded directly on the schematic sheet as a plain text directive (confirmed, via KiCad's own source: any schematic text starting with a recognized SPICE directive like `.AC` is picked up automatically — no workbook required at all), so **Inspect → Simulator → Run** should just work. The `.wbk` alongside it additionally pre-loads the `V(/Zin)` trace for convenience. *(Note: the actual graded Lab A submission still has to be done in LTspice per the course requirement — this is just for working through the problem here.)*
>
> **a) Build the circuit from 2.1c:** an AC current source $U$ (`I1`, `Sim.Params = AC 1`) driving an inductor `L1` (representing $M_A$) in series with a capacitor `C1` (representing $C_A$) to ground. KiCad's `Device:L`/`Device:C` take the value directly (no separate impedance-analogy translation needed, unlike LTspice's raw L/C fields — same underlying electrical analogy either way, just check the value goes on the right part).
>
> **b) Choosing values for $f_0 = 100$ Hz** — one valid worked example (many other choices work too):
> - Tube: radius $a = 1\text{ cm}$ → $S = \pi a^2 = 3.14\times10^{-4}\ \text{m}^2$, length $l^* = 5\text{ cm} = 0.05\text{ m}$
> - Solve the boxed formula for $V$: $V = \dfrac{S c^2}{l^*\,\omega_0^2}$, with $\omega_0 = 2\pi(100) = 628.3\ \text{rad/s}$
> $$V = \frac{(3.14\times10^{-4})(344^2)}{(0.05)(628.3^2)} \approx 1.88\times10^{-3}\ \text{m}^3 \approx 1.9\ \text{L}$$
>   (roughly a 12×12×13 cm box)
> - **Check the validity assumption (2.1b):** $\lambda = c/f_0 = 344/100 = 3.44\ \text{m}$, so we need $l^* < \lambda/10 = 0.344\ \text{m}$. Our $l^*=0.05\text{ m}$ comfortably satisfies this. ✅
> - Resulting element values: $M_A = \rho l^*/S = 1.18\times0.05/3.14\times10^{-4} \approx 188\ \text{kg/m}^4$, $C_A = V/(\rho c^2) \approx 1.34\times10^{-8}\ \text{m}^5/\text{N}$
>
> **c) Impedance of the network, and why it looks like that:**
> $$Z(0) = j\omega M_A + \frac{1}{j\omega C_A} = j\left(\omega M_A - \frac{1}{\omega C_A}\right)$$
> | Frequency regime | $|Z|$ behaviour | Phase |
> |---|---|---|
> | $f \to 0$ | $\to\infty$ (compliance dominates, $1/\omega C_A$ blows up) | $-90°$ (capacitive) |
> | $f = f_0$ | $\to 0$ (lossless — the two reactances exactly cancel) | undefined / jumps |
> | $f \to \infty$ | $\to\infty$ (mass dominates, $\omega M_A$ grows) | $+90°$ (inductive) |
>
> So the curve is a **V-shaped dip in $|Z|$** bottoming out at $f_0$ (ideally all the way to zero, since this idealization has no resistance), with the phase flipping from $-90°$ below resonance to $+90°$ above it. This is the acoustic-domain version of a series LC "impedance minimum = resonance" — same pattern as the electrical/mechanical resonators from [[Lecture 1 - Analogies - Introduction|Lecture 1]]/[[Lecture 2 - Analogies - Mechanical Systems|Lecture 2]].
>
> Since `I1` is a unit AC source, `V(/Zin)` in the simulator plots exactly $|Z(f)|$ in ohms — verified in ngspice directly: dips to ~140 Ω (vs. the theoretical 0 Ω, floored only by the 100 MΩ bias resistor) right at 100.0 Hz.

---

## 3. Deriving the elements: the plane-wave tube

> [!important] The recipe (memorize this — it's reused for every element today)
> 1. Set up the pressure & volume-velocity equations for the element/system.
> 2. Determine the acoustic impedance as a function of frequency.
> 3. Arrange the impedance into **real**, **differential** ($j\omega$), and **integral** ($1/j\omega$) parts.
> 4. Assign the matching electrical lumped element to each part — **within its valid frequency range**.

Starting point: 1D plane wave solution inside a tube of cross-section $S$,

$$p(x,t) = p_i\, e^{j(\omega t - kx)} + p_r\, e^{j(\omega t + kx)}$$
$$u(x,t) = \frac{1}{\rho c}\Big(p_i\, e^{j(\omega t - kx)} - p_r\, e^{j(\omega t + kx)}\Big), \qquad U = Su$$

> [!warning] Limitation #1
> No transversal (higher-order) modes assumed — the tube radius must be small compared to the wavelength. Only **plane waves** travel down the tube.

At $x=l$ the load impedance is $Z_{AL} = p(l)/U(l)$. Working backward to the source ($x=0$):

$$Z(0) = \frac{p(0)}{U(0)} = \frac{\rho c}{S}\cdot \frac{Z_{AL}\cos(kl) + j\dfrac{\rho c}{S}\sin(kl)}{\dfrac{\rho c}{S}\cos(kl) + jZ_{AL}\sin(kl)}$$

> [!example] Sanity check — infinite tube
> If the tube never ends, there's no reflected wave: $p_r = 0$. Then $Z(0) = \rho c/S = Z_{AL}$ — a pure real resistance, the **characteristic acoustic impedance** of the medium. No reactive (mass/compliance) behaviour at all — makes sense, nothing to store energy in if the wave never comes back.

### 3a. Open tube → acoustic mass

Boundary condition: open to free space, so $p(\infty)=0 \Rightarrow Z_{AL}\to 0$ (using an *effective* length $l^*$).

$$Z(0) = j\frac{\rho c}{S}\tan(kl^*)$$

> [!warning] Limitation #2 — small $kl$
> For $kl = \omega l/c \ll 1$: $\tan(kl)\approx kl$, giving

$$Z(0) \approx j\omega \frac{\rho l^*}{S} \quad\Rightarrow\quad \boxed{M_A = \frac{\rho l^*}{S}}$$

> [!note] Physically
> A short open tube just looks like a lump of air being pushed back and forth — pure inertance, no springiness, no loss (in this idealization). That's exactly a series inductor in the electrical analogy.

> [!warning] Limitation #3 — very low frequency, $l < \lambda/10$
> Needed for the mass approximation of a real (finite) open volume to hold at all.
>
> Narrow tubes additionally pick up a resistive part from **viscous and thermal boundary losses** at the walls — not captured by this ideal derivation.

### 3b. Closed tube → acoustic compliance (+ small mass correction)

Boundary condition: hard wall at $x=l$, so $U(l)=0 \Rightarrow Z_{AL}\to\infty$.

$$Z(0) = -j\frac{\rho c}{S}\cot(kl)$$

For small $kl$: $\cot(kl) \approx \dfrac{1}{kl} - \dfrac{kl}{3}$, so

$$Z(0) \approx \frac{\rho c^2}{j\omega S l} + \frac{j\omega \rho l}{3S}$$

$$\boxed{C_A = \frac{V}{\rho c^2}} \qquad \text{(dominant term)} \qquad M_A = \frac{\rho l}{3S} \text{ (small correction, series)}$$

> [!success] Generalizes beyond a tube
> For very small frequencies ($l<\lambda/10$), a **closed volume of any shape** behaves as a pure compliance:
> $$Z(0) \approx \frac{\rho c^2}{j\omega S l} \;\Rightarrow\; C_A = \frac{V}{\rho c^2}$$
> This is the formula you'll reuse constantly for boxes/enclosures later in the course (loudspeaker enclosures, lecture on 1/10).

> [!tip] Intuition
> A sealed volume compresses like a spring: push air in, pressure rises, it pushes back. Pure capacitor analogy. The correction term is just the small mass of air actually moving inside the tube before it hits the closed end.

---

## 4. EXTRA — Transmission line / two-port / ABCD matrix

> [!note] Marked "EXTRA" in the slides — background/deeper material, likely not exam-critical but useful for understanding *why* lumped models break down
> Lumped elements are **0-dimensional** — they can't represent wave propagation (a signal arriving at different times at different points). The fix: model the tube as a **1D distributed (two-port) element** with an explicit input and output.

Two-port (ABCD / transfer matrix) definition:
$$\begin{pmatrix}p_i\\U_i\end{pmatrix} = \begin{pmatrix}A & B\\ C & D\end{pmatrix}\begin{pmatrix}p_o\\U_o\end{pmatrix}$$

For a lossless tube of length $l$, characteristic impedance $Z_0=\rho c/S$:
$$A = \cos(kl),\quad B = jZ_0\sin(kl),\quad C = \frac{j}{Z_0}\sin(kl),\quad D=\cos(kl)$$

- Reciprocal network: $AD - BC = 1$
- Symmetric network: $A = D$
- **Cascading:** multiply ABCD matrices of successive sections together (order matters, right-to-left signal flow).
- Input impedance for a matched/anechoic termination: $Z_i\big|_{p_o=0} = j Z_0\tan(kl)$; for a rigid termination: $Z_i\big|_{U_o=0} = -jZ_0\cot(kl) = Z_0^2/B$.

> [!info] Reading material (if you want the full derivation)
> - F. Jacobsen & P.M. Juhl, *Fundamentals of general linear acoustics*, ch. 7 — Duct Acoustics
> - N. Jiménez, O. Umnova, J.-P. Groby, *Modelling 1D Acoustic Systems...*, ch. 4 — Transfer Matrix Method
> - Wikipedia: *Transmission line*, *Two-port network*

---

## 5. Losses

> [!abstract] What a loss element represents
> A **resistance** $R_A$ models *all* dissipative processes — by definition, purely resistive (real) impedance, i.e. pressure and flow **in phase**.
> $$p = p_1 - p_2 = R_A U$$

> [!warning] Porous materials are not actually purely resistive
> Mineral wool, foam, textiles etc. dissipate energy through **thermal and viscous effects**, but:
> - no clean analytical formula in general
> - properties usually come from **measurement or numerical simulation**
> - the acoustic impedance is then **fitted** with an empirical model, not derived

---

## 6. Sources

> [!note] Ideal pressure source
> Fixed $p$, independent of $U$ drawn — analogous to an ideal AC **voltage** source.
> Examples to think about: an incoming plane wave? A loudspeaker membrane (in which regime)?

> [!note] Ideal volume-velocity source
> Fixed $U$, independent of $p$ — analogous to an ideal AC **current** source.
> Examples: a piston, a bass-reflex port, a loudspeaker membrane (again — depends on the operating regime/frequency!).

> [!important] Real sources — finite output impedance
> A real source = ideal source **+ output impedance** $Z_0$. Two equivalent models:
> - **Thévenin** (pressure source $p_{Th}$ in series with $Z_0$)
> - **Norton** (volume-velocity source $U_{No}$ in parallel with $Z_0$)
>
> Conversion (impedance analogy): $p_{Th} = Z_0\, U_{No}$

---

## 7. In-class exercises — Helmholtz resonator & box with two tubes

> [!example] Helmholtz resonator
> $$p = \left(j\omega M_A + \frac{1}{j\omega C_A}\right) U$$
> Series $M_A$–$C_A$ network driven by $U$ — the textbook Helmholtz resonator: neck = mass, cavity = compliance. Diagram below.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american]
\draw (0,0) node[ground]{} to[isource, l=$U$] (0,3)
      to[L, l=$M_A$ neck] (4,3)
      to[C, l_=$C_A$ cavity] (4,0) node[ground]{};
\end{circuitikz}
\end{document}
```

> [!example] Box with two tubes
> $$U_2 = \frac{\dfrac{1}{j\omega C_A}}{j\omega M_{A2} + \dfrac{1}{j\omega C_A}}\,U, \qquad p = j\omega M_{A2}\,U_2 \quad (p_{out}\to 0)$$
> Diagram below.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american]
\draw (0,0) node[ground]{} to[isource, l=$U$] (0,2)
      to[L, l=$M_{A1}$] (3,2) coordinate(p)
      to[C, l_=$C_A$ (box)] (3,0) node[ground]{};
\draw (3,2) to[L, l=$M_{A2}$] (6,2)
      to[short, -o] (6,0) node[ground]{};
\node at (3,2.4) {node $p$};
\node at (6.3,1) {$U_2$};
\end{circuitikz}
\end{document}
```

> [!warning] Always ground the volume compliance!
> A compliance $C_A$ representing an enclosed volume must always have one terminal tied to the **reference pressure (ground)** — otherwise the circuit topology is wrong. Called out explicitly on the slides — an easy mistake in Lab A.

> [!question] "Which circuit is correct?" (in-class quiz — 4 options a/b/c/d)
> Fill in the reasoning during the lecture:
> - Option chosen: D
> - Why the others are wrong: ⬜

---

## 8. Wave impedance & radiation impedance

### 8a. Spherical wave from a point source

$$p(r,t) = \frac{A}{r}e^{j(\omega t - kr)}, \qquad Z_A(r) = \frac{p(r)}{U(r)} = \frac{j\omega\rho}{4\pi r(1+jkr)}$$

Split into real/imaginary parts:
$$Z_A(r) = \frac{1}{4\pi r} \;\Big\|\; \frac{j\omega\rho}{4\pi r} \quad\text{(mass-like)} \quad\Rightarrow\quad M_A(r)\big|_{r\gg0} = \frac{\rho}{4\pi r} = \frac{\rho r}{S}$$
$$R_A(r)\big|_{r\gg0} = \frac{\rho c}{4\pi r^2} \to 0 \quad \text{(no losses in the far field — energy just radiates away)}$$

> [!tip] Reading refs for this part
> Leach §2.9–2.10, 3.2 · Jacobsen §1.6.1, 9.2 · Beranek §4.10

### 8b. Radiation impedance — piston in an infinite baffle

Model for loudspeakers *and* microphones. Radius $a$, area $S=\pi a^2$. **Not a simple point source at higher frequencies!**

$$Z_A = \frac{p(0)}{U(0)} = \frac{\rho c}{\pi a^2}\left[1 - \frac{J_1(2ka)}{ka} + j\frac{H_1(2ka)}{ka}\right]$$

($J_1$ = 1st-order Bessel function, $H_1$ = 1st-order Struve function — exact, but not something you fit a lumped circuit to directly.)

> [!success] Fitted lumped-element equivalent
> - Low-frequency imaginary part → inductive → **mass $M_{A1}$**, in parallel with the rest of the circuit
> - High-frequency real part (flattening out, imaginary → 0) → high-pass shelving → **$R_{A1} \parallel C_{A1}$, in series with $R_{A2}$**
>
> $$M_{A1} = \frac{8}{3\pi^2}\frac{\rho}{a}, \qquad R_{A1} = 0.441\,\frac{\rho c}{\pi a^2}, \qquad R_{A2} = \frac{\rho c}{\pi a^2}, \qquad C_A = 5.94\,\frac{a^3}{\rho c^2}$$

> [!note] Regime simplifications ($ka$ = frequency-like parameter, $k=\omega/c$)
> | Regime | Behaviour |
> |---|---|
> | $ka \gg 1$ | $R_{A2}$ only (purely resistive, "piston radiates efficiently") |
> | $ka < 1$ | $M_{A1} \parallel (R_{A1}+R_{A2})$ |
> | $ka \ll 1$ | $M_{A1}$ only → $p = j\omega M_{A1}U$ (pure mass-loading) |

> [!note] Piston in a long tube (outlet)
> No closed-form analytical solution — same network topology used as an **approximation**:
> $$M_{A1} = 0.6133\,\frac{\rho}{\pi a}, \quad C_A = 0.55\pi^2\frac{a^3}{\rho c^2}, \quad R_{A1} = 0.5045\,\frac{\rho c}{\pi a^2}, \quad R_{A2} = \frac{\rho c}{\pi a^2}$$

### 8c. Open tubes revisited — end corrections

An open tube is a mass $M_A = \rho l^*/S$ (from §3a) — but real openings add extra mass around them ("added mass"), captured by extending the tube's **effective length** $l^*$:

> [!important] End-correction lengths
> | Opening type | Added mass | Effective length increment |
> |---|---|---|
> | Flanged / baffled end | $M_{A,f} = \dfrac{8}{3\pi^2}\dfrac{\rho}{a}$ | $l_f = \dfrac{8}{3\pi}a \approx 0.8488\,a$ |
> | Unflanged / unbaffled end | $M_{A,uf} = 0.6133\,\dfrac{\rho}{\pi a}$ | $l_{uf} = 0.6133\,a$ |
>
> Example (tube flanged on one end, unflanged on the other): $l^* = l + l_f + l_{uf} = l + 1.4621\,a$

> [!question] Exercise — Helmholtz resonator with radiation impedance
> Redraw the Helmholtz resonator circuit from §7, but now **include the radiation impedance** at the neck opening (from §8b/8c) instead of treating it as an ideal open end.
> - Sketch: ⬜
> - Which of $M_{A1}, R_{A1}, R_{A2}, C_A$ actually matter at the resonator's operating frequency? ⬜

---

## 9. Problem solving (in-class, part 2) — worked

> [!example]+ Problem 2.3 — Tubes in a box, builds on 2.1 (SOLVED)
> $\rho=1.18\ \text{kg/m}^3,\; c=344\ \text{m/s}$. Open tube, effective length $l^*=12\ \text{cm}=0.12\text{ m}$, diameter $10\ \text{cm}$ (radius $a_1=0.05\text{ m}$), in a box of volume $V=23\ \text{L}=0.023\text{ m}^3$, driven by $U$ from outside.
>
> **a) Elements at low frequency:**
> $$S_1 = \pi a_1^2 = \pi(0.05)^2 = 7.854\times10^{-3}\ \text{m}^2$$
> $$M_{A1} = \frac{\rho l^*}{S_1} = \frac{1.18\times0.12}{7.854\times10^{-3}} \approx 18.03\ \text{kg/m}^4$$
> $$C_A = \frac{V}{\rho c^2} = \frac{0.023}{1.18\times344^2} \approx 1.647\times10^{-7}\ \text{m}^5/\text{N}$$
> Circuit: identical to Problem 2.1c — $U \to M_{A1} \to$ node $p \to C_A \to$ ground.
>
> **b) Resonance frequency** (same series-LC formula as 2.1d):
> $$f_0 = \frac{1}{2\pi\sqrt{M_{A1}C_A}} \approx \frac{1}{2\pi\sqrt{18.03 \times 1.647\times10^{-7}}} \approx \boxed{92.4\ \text{Hz}}$$
>
> **c) Second, narrower tube** (diameter $1\text{ cm}$, radius $a_2=0.005\text{ m}$, same $l^*$) placed in the box — this is a **second opening**, i.e. exactly [[Lecture 3 - Analogies - Acoustic Systems#7. In-class exercises — Helmholtz resonator & box with two tubes|§7's "box with two tubes"]] topology:
> $$S_2 = \pi (0.005)^2 = 7.854\times10^{-5}\ \text{m}^2 \qquad M_{A2} = \frac{\rho l^*}{S_2} \approx 1803\ \text{kg/m}^4 \;\; (=100\times M_{A1},\text{ since } S\propto a^2)$$
> Diagram below (values labeled).

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american]
\draw (0,0) node[ground]{} to[isource, l=$U$] (0,2)
      to[L, l=$M_{A1}$] (3.5,2) coordinate(p)
      to[C, l_=$C_A$] (3.5,0) node[ground]{};
\draw (3.5,2) to[L, l=$M_{A2}$] (7.5,2)
      to[short, -o] (7.5,0) node[ground]{};
\node at (3.5,2.4) {node $p$};
\node at (7.8,1) {$U_2$};
\end{circuitikz}
\end{document}
```
*(Values: $U$ = wide-tube drive · $M_{A1}=18.0$ · $C_A=1.65\times10^{-7}$ · $M_{A2}=1803$ (narrow tube) — numbers moved out of the diagram labels below since this is the block that wasn't rendering.)*

> [!example]+ Problem 2.3 (cont.) — d, e, f, g
> **d) Where is $p$ measured, and its shape?** $p$ is the pressure right at the **node** shown above — where the box, the wide tube, and the narrow tube all meet. From §7's formula, with $U$ injected at that node and $C_A \parallel M_{A2}$ both returning to ground:
> $$p(\omega) = U \cdot Z_{C_A}\|Z_{M_{A2}}, \qquad \text{diverges (anti-resonance) at } \omega_0' = \frac{1}{\sqrt{M_{A2}C_A}} \Rightarrow f_0' \approx \frac{92.4}{\sqrt{100}} \approx \boxed{9.2\ \text{Hz}}$$
> Shape: $p\to 0$ as $f\to0$ (at DC all the flow just escapes out the narrow tube, no pressure builds up), rises and **peaks sharply near $9.2$ Hz** (undamped in this ideal model — a real box would round this off with the neglected $R_A$), then **falls off ∝ $1/f$** above that as the narrow tube's mass increasingly blocks flow and the box behaves like a plain sealed compliance again.
>
> **e) Impedance seen from the wide tube's opening** ($Z_{in} = j\omega M_{A1} + Z_{C_A}\|Z_{M_{A2}}$), solving $Z_{in}=0$:
> $$\omega_{res}^2 = \frac{M_{A1}+M_{A2}}{M_{A1}M_{A2}C_A} \;\Rightarrow\; f_{res} \approx 92.8\ \text{Hz}$$
> So driven from the **wide** tube you get **two features far apart**: a sharp low-frequency **anti-resonance around 9.2 Hz** (impedance peak — from the narrow tube/box pair alone) and the **main resonance just above 92.8 Hz** (impedance minimum, barely shifted from the standalone 92.4 Hz of part b, because $M_{A2}\gg M_{A1}$ so the small tube barely loads the big one).
>
> **KiCad + ngspice project ready to open:** `5. Semester/Electroacoustics/KiCad/Problem_2.3_Two_Tube_Network/Problem_2.3_Two_Tube_Network.kicad_sch` — wired up with $M_{A1}, C_A, M_{A2}$ already, node $p$ labeled `p` for part d) and the drive point labeled `Zin` for part e). Same as 2.2: the `.ac dec 200 1 1000` sweep is embedded as a schematic text directive, so **Inspect → Simulator → Run** works with no manual setup; the `.wbk` additionally pre-loads `V(/Zin)` and `V(/p)`. For part g), move `I1` over to drive the `L2` branch instead. *(Same note as 2.2 — this is for working the problem here; the graded Lab A submission stays in LTspice.)*
>
> **f) Simulate:** run an `.ac` sweep of $Z_{in}$ (`V(/Zin)`, since $I=1$A) and $p$ (`V(/p)`). Directly confirmed in ngspice: **`V(/p)` peaks at 9.12 Hz** and **`V(/Zin)` dips at 91.2 Hz** on a 50-points/decade sweep — matching the hand-calculated $f_0'\approx9.2$ Hz and $f_{res}\approx92.8$ Hz (the small gap is just sweep coarseness near the extrema, not a real discrepancy). No singular-matrix/convergence warnings — the L1–L2 path already gives ngspice a genuine DC operating point, so (unlike 2.1/2.2) no extra bias resistor was needed here.
>
> **g) Driving from the narrow tube instead:** now $Z_{in} = j\omega M_{A2} + Z_{C_A}\|Z_{M_{A1}}$.
> - The **resonance** condition ($Z_{in}=0$) uses the *same* symmetric formula as (e) — $\omega_{res}^2=(M_{A1}+M_{A2})/(M_{A1}M_{A2}C_A)$ is unchanged by swapping which tube drives — so $f_{res}\approx92.8\ \text{Hz}$ again.
> - But the **anti-resonance** now comes from the *other* pair, $C_A\|M_{A1}$ (the wide tube is now the load): $f_0'' = 1/(2\pi\sqrt{M_{A1}C_A}) \approx 92.4\ \text{Hz}$ — almost exactly on top of the resonance!
> - **What happens:** driving from the narrow tube squeezes the anti-resonance and resonance right next to each other (92.4 Hz vs. 92.8 Hz) instead of spreading them apart (9.2 Hz vs. 92.8 Hz) as in (e). The response looks like one sharp combined feature instead of two well-separated ones — a nice preview of how driver vs. port placement matters once we get to vented loudspeaker enclosures (1 Oct).
>
> *(Worked out from the formulas given in §7 — double-check against what's derived live in class/LTspice; if your instructor's numbers differ, trust the live derivation over this note.)*

> [!example]+ Problem 2.4 — Dynamic microphone (SOLVED)
> Diaphragm motion generates volume velocity $U$ (ideal source) into a small volume $V_1$ right behind it; $V_1$ connects through a canal to a larger volume $V_2$; porous material at the canal end provides an acoustic resistance $R_A$.
>
> Reading off the elements directly (same pattern as §7's "box with two tubes" / this lecture's whole derivation toolkit):
> - $V_1$ (enclosed volume) → compliance $C_{A1} = V_1/(\rho c^2)$, to ground
> - Porous material in the canal → resistance $R_A$, in series
> - $V_2$ (enclosed volume) → compliance $C_{A2} = V_2/(\rho c^2)$, to ground
> Diagram below.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american]
\draw (0,0) node[ground]{} to[isource, l=$U$ diaphragm] (0,2)
      -- (1,2) coordinate(n1)
      to[C, l_=$C_{A1}$ ($V_1$)] (1,0) node[ground]{};
\draw (1,2) to[R, l=$R_A$ porous canal] (4,2) coordinate(n2)
      to[C, l_=$C_{A2}$ ($V_2$)] (4,0) node[ground]{};
\node at (1,2.4) {node 1};
\node at (4,2.4) {node 2};
\end{circuitikz}
\end{document}
```

> [!example] Problem 2.4 (cont.)
> This is a lumped acoustic **low-pass** network (compliance–resistance–compliance) — it's literally why a dynamic microphone's high-frequency response rolls off: at high $\omega$, $C_{A1}$'s impedance drops low enough that it shunts most of $U$ to ground before it ever reaches $V_2$. Keep this circuit in mind — it resurfaces almost unchanged when dynamic microphones are covered on 14 Sep.

---

## Summary — what to walk away with

> [!success] Key takeaways
> - Acoustic lumped elements ($R_A$, $C_A$, $M_A$) are **derived**, not given — always from: set up $p,U$ → find $Z(\omega)$ → split real/diff/int parts → assign element, **within a validity range**.
> - **Open tube → mass**, **closed volume → compliance** (+ small mass correction), both only valid for $l \ll \lambda$ (low frequency / small $kl$).
> - **End corrections** matter for real (finite) openings — flanged vs. unflanged add different effective lengths.
> - **Radiation impedance** (piston in baffle) is the standard loudspeaker/microphone radiation model — mass at low $ka$, resistive at high $ka$, exact solution needs Bessel/Struve functions but is fitted to a simple $R\|C$-in-series-$R$ + parallel-$M$ network.
> - Losses are always modeled as pure resistances by definition, but real porous materials need empirical fitting.
> - Always **ground the compliance** representing an enclosed volume in your circuit.
> - Two-port/ABCD matrices exist for when lumped (0D) elements aren't enough — distributed 1D wave behaviour.

> [!question] Open questions from this lecture to revisit
> - ⬜
> - ⬜

> [!tip] Looking ahead
> Thursday 10/9: analogies for **transducers** + microphone intro (VCH) — this is where $R_A$/$C_A$/$M_A$ start turning into real diaphragms and magnets. The closed-volume compliance formula $C_A = V/\rho c^2$ will resurface directly when enclosures are covered (1 Oct).
