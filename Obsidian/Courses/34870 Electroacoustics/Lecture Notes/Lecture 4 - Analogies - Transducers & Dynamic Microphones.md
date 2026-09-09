---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-09-10
week: 37
lecture: 4
topic: "Analogies: Transducers · Dynamic Microphones"
lecturer: FL + VCH
tags: [Electroacoustics, lecture-note, analogies, transducers, microphones, dynamic-microphone]
---
# Lecture 4 — Analogies: Transducers & Dynamic Microphones

> [!info] Lecture Info
> **Date:** Thursday 10 September 2026, 8:30–12:00 · Lyngby · **FL** (4A, transducers) then **VCH** (4B, dynamic microphones)
> **Slides:** `Slides/34870_Lecture4A_10092026.pdf` (24 pages, FL) · `Slides/34870_Lecture_4B_E26.pdf` (VCH)
> **Problems:** `Exercises/34870_Problems4_2026.pdf` (dynamic microphones, with answers in brackets)
> **Refs:** Beranek §3.5–3.7, ch. 5 · Leach §4.4–4.7, §5.1–5.4
> **Also today:** the **Lab A quiz opens** (Frieder's announcement of 9 Sep) and is previewed during the morning class — **deadline 20 Sep**, individual, mandatory for the exam, part of the 30 %. Sign up to a Lab Group in DTU Learn if not done.
> **Previous:** [[Lecture 3 - Analogies - Acoustic Systems|Lecture 3 — acoustic systems]] · **Next:** Lecture 5 — microphones: dynamic & condenser (1) *(VCH, Mo 14/9)*

> [!abstract] Where this lecture sits
> Lectures 1–3 gave us three separate toolboxes: electrical, mechanical and acoustic lumped networks, each living in its own domain. Today the domains get **wired together**. A transducer is nothing more than a pair of **controlled sources** (or a transformer/gyrator two-port) whose gain is a physical constant — $S$ for a diaphragm, $Bl$ for a voice coil, $v_0/x_0$ for a condenser. Once you can draw that pair correctly (and with the right *signs*), you can model a complete microphone or loudspeaker as one circuit and simulate it. VCH's half then does exactly that for the **dynamic microphone**, ending in the band-pass formula whose three total elements $M_{MT}, R_{MT}, C_{MT}$ are the whole design story.
>
> This is also the theory behind **Lab A parts 3 and 4** (coupled mechanical–acoustic and electrical–mechanical systems) — see [[Lab A - Runthrough]].

---

## 1. Repetition — pop quiz, answered

> [!question]+ Pop quiz
> **Q1 — Equivalent systems: describe lumped mechanical networks/circuits.**
> Variables: velocity $u$ and force $f$. Elements: mass $M_M$ (needs a reference velocity = ground), compliance $C_M$, damper $R_M$. Equilibrium (sum of forces) and continuity (sum of velocities) written per node/mesh. Two analogies: **impedance** ($f\leftrightarrow v$, $u\leftrightarrow i$, mass = inductor) and **mobility** ($u\leftrightarrow v$, $f\leftrightarrow i$, mass = capacitor to ground) — graphically converted by turning every mesh into a node, adding one node outside (ground), and replacing each element by its dual ([[Lecture 2 - Analogies - Mechanical Systems|Lecture 2]]).
>
> **Q1 — … and lumped acoustic networks/circuits.**
> Variables: pressure $p$ and volume velocity $U$. Elements derived from the plane-wave tube: open tube → mass $M_A=\rho l^*/S$, closed volume → compliance $C_A = V/\rho c^2$ (**always to ground**), losses → $R_A$. Sources: pressure ⇔ voltage, volume velocity ⇔ current ([[Lecture 3 - Analogies - Acoustic Systems|Lecture 3]]).
>
> **Q2 — Coupled systems: which network variables are coupled to each other?**
> One variable of each domain is a function of a variable in the neighbouring domain, in *both* directions:
> - electrical $\leftrightarrow$ mechanical: $v \leftrightarrow f\ \text{or}\ u$, $i \leftrightarrow u\ \text{or}\ f$
> - mechanical $\leftrightarrow$ acoustical: $f \leftrightarrow p$, $u \leftrightarrow U$
>
> **Q2 — What defines the coupling?**
> A **physical law** of the transducer, which gives a (constant) **transduction factor**: pressure on an area ($f = Sp$, $U = Su$), Lorentz force + Faraday induction ($f = Bl\,i$, $v = Bl\,u$), electrostatics ($v_0/x_0$), piezoelectricity ($1/d$). Transduction is bidirectional (excitation *and* response), so both directions must appear in the circuit.

### The analogy table, extended with the coupling column

> [!note] Mobility (mechanical) + impedance (acoustic) form — the one the course uses
> | | Electrical | Mechanical (mobility) | Acoustical |
> |---|---|---|---|
> | Across variable | $v$ | $u$ | $p$ |
> | Through variable | $i$ | $f$ | $U$ |
> | Real element | $R$ | $1/R_M$ | $R_A$ |
> | $j\omega$ element (L) | $L$ | $C_M$ | $M_A$ |
> | $1/j\omega$ element (C) | $C$ | $M_M$ (to ground) | $C_A$ (to ground) |
> | Coupling to the right → | $f = Bl\,i$, $v = Bl\,u$ | $f = S\,p$, $U = S\,u$ | — |

---

## 2. Transducers — connecting the systems

> [!abstract] Definitions
> **Transduction** = transfer of energy between physical domains. The domains become **coupled** (dependent on each other), and the coupling is generally **bidirectional**.
> **Transducer** = the component connecting the variables. In network terms: **controlled sources** whose control variable lives in the other domain. Alternative: a **two-port** (transformer or gyrator) with the transduction factor $x$ as its parameter.

### 2a. The four controlled sources

> [!important] Pick the source from the pair of variables it connects
> | Coupling | Source type | LTspice | SPICE letter | KiCad symbol |
> |---|---|---|---|---|
> | across ⇔ across | voltage-controlled voltage source | E, E2 | `E` | `Simulation_SPICE:ESOURCE` |
> | through ⇔ through | current-controlled current source | F | `F` | *(no symbol — sense the current as a voltage across a resistor and use a G)* |
> | across ⇔ through | voltage-controlled current source | G, G2 | `G` | `Simulation_SPICE:GSOURCE` |
> | through ⇔ across | current-controlled voltage source | H | `H` | *(same trick, use an E)* |
>
> Procedure: (1) write the physical relations between the domains for *all* network variables, (2) connect the domains with the controlled sources matching those relations, (3) assign the control to the right variable and give the source the (constant) transduction factor $x$.

> [!note] Two-port view
> Forward: through-current-through with factor $x$; backward: across-voltage-across with factor $1/x$ — i.e. a transformer $\begin{pmatrix} x & 0 \\ 0 & 1/x\end{pmatrix}$ when both couplings are across↔across / through↔through, and a **gyrator** when they cross over (the electrodynamic case in §2c).

### 2b. Mechanical ↔ acoustical: a vibrating surface $S$

$$f = S\,p \qquad U = S\,u$$

Example: a piston driven by force $f_0$, with pressure $p_f$ on its front and $p_b$ on its back. The net pressure is $p = p_f - p_b$, the mechanical impedance the force sees is $Z_M = (f_0 - f)/u$, and the acoustic impedance the piston sees is
$$Z_A = \frac{p}{U} = \frac{p_f - p_b}{U} = Z_{Af} + Z_{Ab}$$
— front and back loads are simply **in series** in the acoustic domain (the same $U$ flows through both).

> [!example]+ The two ways to draw it (slide 8)
> **Mechanical mobility analogy** — force source $f_0$ = current source into node $u$; the piston's own mobility $Y_M$ hangs from that node; the acoustic side is driven by a VCCS $U = S\,u$ (control = node $u$), and the reaction force comes back as a VCCS $f = S\,p$ drawn from node $u$ (control = node $p$). Two **G** sources.
>
> **Mechanical impedance analogy** — force source = voltage source in series with $Z_M$; the piston current is $u$; a VCVS $f = S\,p$ appears in series in the mechanical loop (control = node $p$, an **E** source), and a CCCS $U = S\,u$ (control = the loop current $u$, an **F** source) drives $Z_{Af} + Z_{Ab}$.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.9]
% mobility form
\draw (0,0) node[ground]{} to[isource, l=$f_0$] (0,3) -- (2,3) coordinate(u);
\draw (u) to[generic, l=$Y_M$] (2,0) node[ground]{};
\draw (u) -- (4,3) to[cisource, l=$f{=}Sp$] (4,0) node[ground]{};
\node at (2,3.4) {node $u$};
% acoustic side
\draw (7,0) node[ground]{} to[cisource, l_=$U{=}Su$] (7,3) -- (9,3) coordinate(p)
      to[generic, l=$Z_{Af}$] (9,1.5) to[generic, l=$Z_{Ab}$] (9,0) node[ground]{};
\node at (9,3.4) {node $p$};
\node[align=left] at (4.5,-1) {\small mobility: two G sources ($S$)};
\end{circuitikz}
\end{document}
```

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.9]
% impedance form
\draw (0,0) node[ground]{} to[vsource, l=$f_0$] (0,3) to[generic, l=$Z_M$, i=$u$] (3,3)
      to[cvsource, l=$f{=}Sp$] (3,0) node[ground]{};
\draw (6,0) node[ground]{} to[cisource, l_=$U{=}Su$] (6,3) -- (8,3) coordinate(p)
      to[generic, l=$Z_{Af}$] (8,1.5) to[generic, l=$Z_{Ab}$] (8,0) node[ground]{};
\node at (8,3.4) {node $p$};
\node[align=left] at (4,-1) {\small impedance: E (voltage) + F (current), factor $S$};
\end{circuitikz}
\end{document}
```

> [!warning] Signs and polarities (this is what Lab A's hint is about)
> The reaction force must **oppose** the motion: the $f = Sp$ source draws current *out of* node $u$ when $p$ is positive. Get it backwards and the acoustic load becomes a negative damper — the response blows up instead of being damped. Sanity check every coupled circuit by looking for the expected damping/mass-loading, and by checking that the mobility and impedance versions give **the same** result (Problem 4.4 does exactly that).

> [!example]+ Exercise — massless piston (slide 9), worked
> Massless rigid piston, $a = 10$ cm ($S = \pi a^2 = 3.14\times10^{-2}$ m²), front: baffled radiation impedance $Z_{Af}$, back: closed 10 L volume $Z_{Ab} = 1/(j\omega C_{Ab})$.
> $$Z_M = \frac{f}{u} = S^2\,(Z_{Af} + Z_{Ab})$$
> Numbers ($\rho=1.18$, $c=344$; Lecture 3 §8b network): $M_{A1} = 8\rho/(3\pi^2 a) = 3.19$ kg/m⁴ · $R_{A1} = 0.441\rho c/(\pi a^2) = 5.70\times10^3$ · $R_{A2} = \rho c/(\pi a^2) = 1.29\times10^4$ Pa·s/m³ · $C_{A1} = 5.94 a^3/(\rho c^2) = 4.25\times10^{-8}$ · $C_{Ab} = V/(\rho c^2) = 7.16\times10^{-8}$ m⁵/N.
>
> What the $|Z_M|$ plot looks like:
> - **Low frequency:** the back volume dominates, $|Z_M| \approx S^2/(\omega C_{Ab})$ — a spring, falling at −20 dB/decade, phase −90°.
> - **Series resonance** where the front air mass cancels the back spring: $f_0 = 1/(2\pi\sqrt{M_{A1} C_{Ab}}) \approx 333$ Hz — a sharp **minimum** in $|Z_M|$, only the radiation resistance is left.
> - **Above:** mass-like ($S^2\,\omega M_{A1}$, +90°) until $ka \approx 1$ ($f = c/2\pi a \approx 550$ Hz), where the radiation impedance turns resistive and flattens towards $S^2 R_{A2} \approx 12.8$ Ns/m.
>
> Both drawings (mobility with two G's, impedance with E + F) must give this same curve.

### 2c. Electrical ↔ mechanical: electrodynamic (moving coil)

> [!important] Lorentz force + Faraday induction
> $$f = i\,lB \qquad v = u\,lB$$
> Force source controlled by the **current**, voltage source controlled by the **velocity**, both with the same constant factor $Bl$ (units T·m = N/A = V·s/m).

- **Mobility:** electrical loop $v_0 \to Z_e \to$ VCVS $v = Bl\,u$ (an **E**, control = node $u$); mechanical node $u$ driven by a CCCS $f = Bl\,i$ (an **F**, control = the loop current) into the mobility $Y_M$.
- **Impedance:** the mechanical loop gets a CCVS $f = Bl\,i$ (an **H**) in series with $Z_M$, and the electrical loop a CCVS $v = Bl\,u$ (another **H**, control = the mechanical loop current $u$).

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.9]
\draw (0,0) node[ground]{} to[vsource, l=$v_0$] (0,3) to[generic, l=$Z_e$, i=$i$] (3,3)
      to[cvsource, l=$v{=}Bl\,u$] (3,0) node[ground]{};
\draw (6,0) node[ground]{} to[cisource, l_=$f{=}Bl\,i$] (6,3) -- (8,3) coordinate(u)
      to[generic, l=$Y_M$] (8,0) node[ground]{};
\node at (8,3.4) {node $u$};
\node at (4,-1) {\small electrodynamic transducer, mobility form (gyrator)};
\end{circuitikz}
\end{document}
```

> [!tip] Transformer or gyrator? It depends on the analogy
> In the **mobility** analogy $i \to f$ is through→through (an F) and $u \to v$ is across→across (an E): the coupling is a **transformer** with ratio $Bl$. In the **impedance** analogy the same two laws become $i \to f$ = through→across and $u \to v$ = through→across (two H's): a **gyrator**. Physics unchanged — but a gyrator *inverts* impedances, which is why the electrical side sees $(Bl)^2/Z_M$ (§2e).

### 2d. Electrostatic and piezoelectric transduction (linearised)

> [!note] Electrostatic (capacitive): gap $x_0$, bias voltage $v_0$
> $$v = \frac{1}{j\omega C_E}\,i + \frac{v_0}{j\omega x_0}\,u \qquad f = -\frac{v_0}{j\omega x_0}\,i - \frac{1}{j\omega C_M}\,u$$
> **Nonlinear** in general — this is the small-signal linearisation around the bias $v_0$ (the electrical DC source is drawn explicitly on the slide). The $1/j\omega$ in the coupling terms can be moved into the elements, giving **frequency-independent** sources: $v_0 C_E u/x_0$ and $v_0 C_M i/x_0$ (mobility: G + H; impedance: two F's, with $C_E$ and $C_M$ absorbing the integrations).

> [!note] Piezoelectric: coefficient $d$ (C/N)
> $$v = -\frac{1}{j\omega d}\,u + \frac{1}{j\omega C_E}\,i \qquad f = \frac{1}{j\omega d}\,i - \frac{1}{j\omega C_M}\,u$$
> Also nonlinear in general. Same trick: frequency-independent sources $C_E u/d$ and $C_M i/d$ (mobility: G2 + H; impedance: two F's). These come back in [[34871 Nonlinear Transducers]] and in the condenser-microphone lectures (14/9, 17/9).

### 2e. Impedance conversion — what one domain sees of the next

> [!important] The two conversion rules
> **Acoustic → mechanical** (vibrating surface $S$):
> $$Z_{M,A} = S^2 Z_A = S^2\,(Z_{Af} + Z_{Ab}) \quad\text{(impedance analogy)}, \qquad Y_{M,A} = 1/Z_{M,A} \quad\text{(mobility analogy)}$$
> A transformer just scales: $S^2$ multiplies impedances, loads stay in the same "shape".
>
> **Mechanical → electrical** (electrodynamic): an **inversion**!
> $$Z_{E,M} = \frac{(Bl)^2}{Z_M} = (Bl)^2\,Y_M$$
> (for capacitive transducers: $Z_{E,M} = (v_0/j\omega x_0)^2 / Z_M$.) A mechanical *series* resonance (impedance minimum) becomes an electrical *parallel* resonance (impedance **maximum**) — the famous impedance peak of every loudspeaker at $f_s$.

> [!example]+ Exercise — microphone diaphragm with suspension and coil (slides 17–20)
> Mechanical: $f = u\,(j\omega M_M + 1/j\omega C_M + R_M)$. Coupling: $f = i\,lB$, $v = u\,lB$. Electrical: $Z_E = v/i$.
> Inverting the mechanical impedance:
> $$Z_{E,M} = \frac{(lB)^2}{j\omega M_M + \dfrac{1}{j\omega C_M} + R_M} \qquad\Rightarrow\qquad \boxed{Z_E = R_c + j\omega L_c + \frac{(lB)^2}{j\omega M_M + \dfrac{1}{j\omega C_M} + R_M}}$$
> The LTspice circuits on the slide: mobility form with `E1` ($v = lB\,u$) and `F1` ($f = lB\,i$) feeding `C2 = {Mm}`, `L2 = {Cm}`, `R2 = {1/Rm}`; impedance form with two `H` sources and `L2 = {Mm}`, `C2 = {Cm}`, `R2 = {Rm}` in series. Plotting $Z_E$ from both gives the same curve: $R_c$ at low frequency, a **motional peak** of height $R_c + (lB)^2/R_M$ at $f_0 = 1/(2\pi\sqrt{M_M C_M})$, then the coil inductance rising.
>
> **Full capsule with felt damping** — three domains: $Z_E$ (voice coil $R_c$, $L_c$), $Z_M$ (diaphragm mass, stiffness, damping), $Z_{Af}$ (radiation) and $Z_{Ab}$ (back cavity + absorber). Network analysis gives
> $$v_{out} = -\frac{R_L}{Z_E + R_L}\cdot\frac{Bl\,S}{\dfrac{(Bl)^2}{Z_E + R_L} + Z_M + S^2\,(Z_{Af} + Z_{Ab})}\;p_{in}$$
> — read it as: (potential divider $R_L/(Z_E + R_L)$) × (transduction $Bl\,S$) ÷ (total mechanical impedance, with the electrical load reflected in as $(Bl)^2/(Z_E+R_L)$ and the acoustics reflected in as $S^2 Z_A$). Slide 20's plot (output in dBV vs. frequency): a band-pass whose flatness depends on the **felt damping** — low damping = a resonance hump, high damping = a wide, flat, lower plateau. This is exactly VCH's formula in §4, derived in one line.

---

## 3. Problem solving (in-class) — Problems 4.1–4.4, worked

> [!example]+ Problem 4.1 — Loudspeaker box with bass reflex (builds on [[Lecture 3 - Analogies - Acoustic Systems#9. Problem solving (in-class, part 2) — worked|Problem 2.3]])
> Vented box: vent $l^* = 12$ cm, Ø 10 cm, $V = 23$ L → $M_{Av} = \rho l^*/S_v = 18.0$ kg/m⁴, $C_A = V/\rho c^2 = 1.65\times10^{-7}$ m⁵/N, box–port resonance $f_B = 1/(2\pi\sqrt{M_{Av}C_A}) = 92.4$ Hz. Driver: baffled, **massless** piston, same diameter as the vent ($S_D = 7.85\times10^{-3}$ m²), vibrating with velocity $u$.
>
> **a) Circuit.** A velocity source $u$ on the mechanical side, coupled by $S_D$ into the acoustic domain: the piston's volume velocity $U_D = S_D u$ flows *into* the box node (pressure $p_{box}$), from which the box compliance $C_A$ goes to ground and the vent mass $M_{Av}$ goes to the outside (ground = $p_{out}\approx0$). Its front side sees the front radiation impedance $Z_{Af}$ directly. In the mobility form: a VCCS $U = S_D u$ into node $p_{box}$ and a VCCS $f = S_D(p_f - p_{box})$ back on node $u$ (irrelevant for a *prescribed* velocity, but needed as soon as the driver has mass/compliance).
>
> **b) With radiation impedance.** Replace the vent's ground connection with the unflanged-tube radiation network $M_{A1}\,\|\,[R_{A2} + (R_{A1}\|C_{A1})]$ from Lecture 3 §8b/8c (and remember the vent's effective length already contains the end corrections), and put the baffled-piston network on the piston's front side.
>
> **c) Acoustic impedance seen by the piston (back side):**
> $$Z_{A,back} = \frac{1}{j\omega C_A}\;\Big\|\;\big(j\omega M_{Av} + Z_{rad,vent}\big)$$
> Lossless shape: $\to 0$ at DC (all flow escapes through the vent), a **parallel resonance = impedance peak** at $f_B \approx 92$ Hz, then $\to 1/(j\omega C_A)$ (the vent mass blocks, the box is just a sealed compliance). Total $Z_A = Z_{Af} + Z_{A,back}$; mechanically $Z_M = S_D^2 Z_A$.
>
> **d) Far field, box as a point source.** Total volume velocity $U_{tot} = U_D + U_v$ (in phase above $f_B$, opposing below — that is why a reflex box falls off at 24 dB/octave below tuning). For a point source in free space $p(r) = j\omega\rho\,U_{tot}\,e^{-jkr}/(4\pi r)$ (half-space/baffle: $2\pi r$), so $|p| \propto 1/r$ — plotting pressure over distance is a straight −6 dB per doubling line, valid while $kr \gg 1$ and the box is small compared to $\lambda$.

> [!example]+ Problem 4.2 — Coupling between mechanical and acoustic systems, worked
> Force $f$ on an ideal (zero-thickness) piston of mass $M_{mp}$, area $S$, mounted in an infinite baffle; radiation impedance seen from one side $Z_{ar}$.
>
> **a) Circuit.** Mobility: current source $f$ into node $u$; $M_{mp}$ = capacitor to ground; a VCCS $U = Su$ drives the acoustic node, where **both sides** radiate: $Z_{Af} = Z_{Ab} = Z_{ar}$ in series; a VCCS $f_{ac} = S\,p$ pulls the reaction force from node $u$.
>
> **b) Total mechanical impedance.** Hint used: $p = Z_A U = 2Z_{ar}\,S\,u$, so the reaction force is $S p = 2 S^2 Z_{ar}\,u$ and
> $$\boxed{Z_{M,tot} = \frac{f}{u} = j\omega M_{mp} + 2 S^2 Z_{ar}}$$
> At low frequency $Z_{ar}\approx j\omega M_{A1}$: the piston simply looks **heavier**, $M_{mp} + 2S^2 M_{A1}$ (the classic "air load"). At high frequency $Z_{ar}\to R_{A2}$: pure damping $2S^2 R_{A2} = 2\rho c S$ — the piston radiates.
>
> **c) Baffle thickness $d$.** The back of the piston now sits at the bottom of a tube of length $d$ and area $S$: an **acoustic mass $M_{Ad} = \rho d/S$ in series** with the back radiation impedance. "Small" means $d \ll \lambda$, in practice $d < \lambda/10$ so the tube is a lumped mass (and the tube's own radiation end correction is included in $Z_{ar}$ of the back opening). $Z_{M,tot} = j\omega M_{mp} + S^2(Z_{ar} + j\omega M_{Ad} + Z_{ar})$.
>
> **d) Enclosure of volume $V$ on the back.** The back opening no longer radiates: replace the back $Z_{ar}$ by the box compliance $C_{AB} = V/\rho c^2$ **to ground** (a closed volume is always grounded). Back branch: $j\omega M_{Ad} + 1/(j\omega C_{AB})$. Net effect on the piston: an added *stiffness* $S^2/C_{AB}$ that raises the resonance — the sealed-box effect that the enclosure lecture (1/10) builds on.
>
> **e) Radiation network.** Replace the front $Z_{ar}$ by $M_{A1}\,\|\,[R_{A2} + (R_{A1}\|C_{A1})]$ with $M_{A1} = 8\rho/(3\pi^2 a)$, $R_{A1} = 0.441\rho c/\pi a^2$, $R_{A2} = \rho c/\pi a^2$, $C_{A1} = 5.94a^3/\rho c^2$, $a = \sqrt{S/\pi}$.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.85]
\draw (0,0) node[ground]{} to[isource, l=$f$] (0,3) -- (2,3) coordinate(u)
      to[C, l=$M_{mp}$] (2,0) node[ground]{};
\draw (u) -- (4,3) to[cisource, l=$f{=}Sp$] (4,0) node[ground]{};
\node at (2,3.4) {node $u$};
\draw (7,0) node[ground]{} to[cisource, l_=$U{=}Su$] (7,3) -- (9,3) coordinate(p)
      to[generic, l=$Z_{Af}$ (rad.)] (9,1.5) to[L, l=$M_{Ad}$] (9,0)
      to[C, l=$C_{AB}$] (9,-1.5) node[ground]{};
\node at (9,3.4) {node $p$};
\node at (4.5,-1.2) {\small Problem 4.2d: baffled piston, tube $d$ on the back, closed box $V$};
\end{circuitikz}
\end{document}
```

> [!example]+ Problem 4.3 — Coupling between electrical and mechanical systems, worked
> Coil (effective length $l$, field $B$, mass $M_{mc}$, DC resistance $R_e$, inductance $L_e$) on a suspension ($C_{ms}$, $R_{ms}$).
>
> **a) Impedance analogy for the mechanics.** Electrical loop: $v \to R_e \to L_e \to$ CCVS $Bl\,u$ (control = mechanical loop current $u$). Mechanical loop: CCVS $Bl\,i$ (control = electrical current $i$) $\to L = M_{mc} \to C = C_{ms} \to R = R_{ms}$ back to ground; the loop current is $u$.
>
> **b) Impedance seen from the electrical terminals.** $v = i(R_e + j\omega L_e) + Bl\,u$ and $Bl\,i = u\,Z_M$ with $Z_M = j\omega M_{mc} + R_{ms} + 1/(j\omega C_{ms})$, so
> $$\boxed{Z_E = \frac{v}{i} = R_e + j\omega L_e + \frac{(Bl)^2}{j\omega M_{mc} + R_{ms} + \dfrac{1}{j\omega C_{ms}}}}$$
> **c) Mobility analogy.** Electrical loop: $v \to R_e \to L_e \to$ VCVS $Bl\,u$ (an E, control = node $u$). Mechanical node $u$: CCCS $f = Bl\,i$ (an F) into the node; $C = M_{mc}$, $L = C_{ms}$, $R = 1/R_{ms}$ all to ground.
>
> **d) Compare.** Identical $Z_E$ — the mobility circuit computes $u = f\,Y_M = Bl\,i\,Y_M$ and feeds back $Bl\,u = (Bl)^2 Y_M\,i$, which is the same $(Bl)^2/Z_M$ term. The motional term is a **parallel RLC** seen from the electrical side: $R_{mot} = (Bl)^2/R_{ms}$, $L_{mot} = (Bl)^2 C_{ms}$, $C_{mot} = M_{mc}/(Bl)^2$.
>
> **e) Velocity and forces vs. driving current.** $u = Bl\,i/Z_M$: at resonance $f_0 = 1/(2\pi\sqrt{M_{mc}C_{ms}})$ the velocity peaks at $u = Bl\,i/R_{ms}$ (in phase with $i$); below $f_0$ the spring dominates ($u \approx j\omega C_{ms} Bl\,i$, velocity leads), above it the mass ($u \approx Bl\,i/(j\omega M_{mc})$, lags). Forces: the Lorentz force $Bl\,i$ is split between inertia $j\omega M_{mc} u$, damping $R_{ms}u$ and the spring $u/(j\omega C_{ms})$; at resonance inertia and spring cancel and the whole $Bl\,i$ goes into the damper.

> [!example]+ Problem 4.4 — LTspice / KiCad implementation, expected numbers
> **a)** Problem 4.2 with $S = 100$ cm², $M_{mp} = 20$ g, $V = 40$ L, $d = 2$ cm, both analogies must agree. Hand numbers: $a = 5.64$ cm, $M_{A1} = 5.65$ kg/m⁴ → air load $S^2 M_{A1} = 0.57$ g per side; tube $M_{Ad} = \rho d/S = 2.36$ kg/m⁴ → $0.24$ g; box $C_{AB} = 2.86\times10^{-7}$ m⁵/N → mechanical compliance $C_{AB}/S^2 = 2.86$ mm/N. With the box on the back (4.2d): total mass ≈ 21.4 g on 2.86 mm/N → **$f_0 \approx 20$ Hz** (piston-on-box resonance), damped only by the front radiation resistance.
> **b)** Problem 4.3 with $l = 3$ m, $B = 0.7$ T ($Bl = 2.1$ Tm), $M_{mc} = 10$ g, $C_{ms} = 1$ mm/N, $R_{ms} = 2$ Ns/m, $R_e = 5$ Ω, $L_e = 0.3$ mH: $f_0 = 1/(2\pi\sqrt{M_{mc}C_{ms}}) = 50.3$ Hz, mechanical $Q_m = \sqrt{M_{mc}/C_{ms}}/R_{ms} = 1.58$, motional resistance $(Bl)^2/R_{ms} = 2.2$ Ω → **$|Z_E|$ peaks at $R_e + 2.2 = 7.2$ Ω at 50.3 Hz**, then rises as $\omega L_e$ above $R_e/(2\pi L_e) = 2.65$ kHz. Driven by a voltage source the electrical damping $(Bl)^2/R_e = 0.88$ Ns/m adds to $R_{ms}$.
> **c)** Coil rigidly attached to the piston of a): mass $10 + 21.4 = 31.4$ g, suspension $C_{ms}$ in series (springs in parallel, compliances combine as $1/(1/C_{ms} + S^2/C_{AB}) = 0.74$ mm/N) → **$f_0 \approx 33$ Hz**; the electrical impedance now shows *that* peak, heavier and broader (radiation damping added), instead of the 50 Hz one.
>
> **KiCad + ngspice project ready to open (4.4b):** `5. Semester/Electroacoustics/KiCad/Problem_4.4b_Coil_Electromechanical/Problem_4.4b_Coil_Electromechanical.kicad_sch` — mobility analogy: `V1` (1 V AC) → `R1 = R_e` → `L1 = L_e` → `E1` (back-EMF $Bl\,u$, sensing node `u`); `G1` injects $f = Bl\,i$ into node `u` (KiCad has no F symbol, so the current is sensed as the voltage across `R1`, gain $Bl/R_e = 0.42$); `C1 = M_{mc}`, `L2 = C_{ms}`, `R2 = 1/R_{ms}` to ground. `.ac dec 200 1 10k` is on the sheet, the `.wbk` pre-loads `V(/u)` and `I(V1)`; `sim.py` exports the netlist with `kicad-cli`, runs ngspice and plots $Z_E = V(\text{vin})/I(V1)$ against the closed form.
> **Simulated:** motional peak **7.206 Ω at 50.1 Hz** (theory 7.205 Ω at 50.3 Hz, sweep granularity), $|Z_E| = 5.000$ Ω at 1 Hz, 19.5 Ω at 10 kHz, ngspice vs. the formula in b) agree to $10^{-9}$ relative; coil velocity peaks at **146 mm/s per volt** at 50.7 Hz.
>
> ![[Problem_4.4b_Ze.png]]

---

## 4. Lecture 4B — Dynamic microphones (VCH)

### 4a. Construction and the simple equivalent circuit (Leach ch. 5)

> [!abstract] Dynamic pressure microphone
> - The **moving coil** sits in a magnetic field (Lorentz/Faraday transducer, §2c)
> - The **diaphragm front** is exposed to the sound
> - A **closed volume** loads the back of the diaphragm
> - **Acoustic damping material** (felt) is placed behind the diaphragm

> [!note] Element list — three domains
> | Domain | Element | Meaning |
> |---|---|---|
> | Electrical | $R_L$ | amplifier (load) impedance |
> | | $R_E$ | coil resistance |
> | | $Bl$ | magnetic force factor |
> | Mechanical | $M_{MD}$ | moving mass of diaphragm and coil |
> | | $C_{MS}$ | compliance of the diaphragm suspension |
> | | $R_{MS}$ | damping of the suspension |
> | | $S_D$ | diaphragm area |
> | Acoustical | $M_{A1}$ | air mass in front (radiation impedance — piston on a cylinder) |
> | | $R_{AF}$ | acoustic resistance of the damping material |
> | | $C_{AB}$ | acoustic compliance of the back volume |
> | | $p_i$ | incident sound pressure (influence of the mic on the field not included) |
> | | $T(s)$ | free-field scattering correction (mimics the influence on the field, normal incidence) |

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.85]
% acoustic loop (impedance analogy)
\draw (0,0) node[ground]{} to[vsource, l=$p_i$] (0,3) to[L, l=$M_{A1}$, i=$U{=}S_Du_D$] (3,3)
      to[cvsource, l=$p_D$] (3,0) node[ground]{};
\draw (3,3) -- (4,3) to[R, l=$R_{AF}$] (6,3) to[C, l=$C_{AB}$] (6,0) node[ground]{};
% mechanical loop (impedance analogy)
\draw (8,0) node[ground]{} to[cvsource, l=$S_Dp_D$] (8,3) to[L, l=$M_{MD}$, i=$u_D$] (10,3)
      to[R, l=$R_{MS}$] (12,3) to[C, l=$C_{MS}$] (12,1.5) to[cvsource, l=$Bl\,i$] (12,0) node[ground]{};
% electrical loop
\draw (14,0) node[ground]{} to[cvsource, l=$Bl\,u_D$] (14,3) to[R, l=$R_E$, i=$i$] (16,3)
      to[R, l=$R_L$, v=$e$] (16,0) node[ground]{};
\node at (1.5,-1) {\small acoustical};
\node at (10,-1) {\small mechanical};
\node at (15,-1) {\small electrical};
\end{circuitikz}
\end{document}
```
*(Leach draws the couplings as transformers/gyrators; here they are written out as the controlled sources of §2 so the loop equations below can be read straight off the drawing.)*

### 4b. Transfer function

> [!important] The three loop equations
> **Acoustical:** $\;p_D = p_i - S_D u_D\,(j\omega M_{A1} + R_{AF} + 1/j\omega C_{AB}) = p_i - S_D u_D\,Z_A$
> **Mechanical:** $\;Bl\,i + S_D p_D = u_D\,(j\omega M_{MD} + R_{MS} + 1/j\omega C_{MS}) = u_D Z_M$ *(sign of the $Bl\,i$ term depends on the chosen polarity; the electrical load ends up as damping either way)*
> **Electrical:** $\;e = -Bl\,u_D\,\dfrac{R_L}{R_E + R_L}, \qquad i = \dfrac{-Bl\,u_D}{R_E + R_L}, \qquad e = i R_L$
>
> Eliminating $p_D$, $u_D$, $i$:
> $$\boxed{\frac{e}{p_i} = \frac{-Bl\,S_D\,R_L}{R_E + R_L}\cdot\frac{1}{Z_M + S_D^2 Z_A + \dfrac{(Bl)^2}{R_E + R_L}}}$$
> — the same structure as FL's capsule formula in §2e: transduction factor over the *total* mechanical impedance, with the acoustics reflected by $S_D^2$ and the electrical load reflected by $(Bl)^2$.

> [!success] Collecting terms: one band-pass, three totals
> $$\frac{e}{p_i} = \frac{R_L}{R_E + R_L}\cdot\frac{-Bl\,S_D}{j\omega M_{MT} + R_{MT} + \dfrac{1}{j\omega C_{MT}}}$$
> | | | |
> |---|---|---|
> | Total mass | $M_{MT} = M_{MD} + S_D^2 M_{A1}$ | diaphragm + air load |
> | Total resistance | $R_{MT} = R_{MS} + S_D^2 R_{AF} + \dfrac{(Bl)^2}{R_E + R_L}$ | suspension + felt + electrical damping |
> | Total compliance | $C_{MT} = \dfrac{1}{1/C_{MS} + S_D^2/C_{AB}}$ | suspension spring + back-volume spring (in parallel → stiffnesses add) |
>
> *(Typo in Leach eq. 5.27: $C_{MD}$ should read $C_{MS}$.)* Normally $R_L \gg R_E$, so the divider is ≈ 1.

In normalised form:
$$\frac{e}{p_i} = \frac{R_L}{R_E+R_L}\cdot\frac{-Bl\,S_D}{R_{MT}}\cdot\frac{(1/Q)(j\omega/\omega_0)}{-(\omega/\omega_0)^2 + (1/Q)(j\omega/\omega_0) + 1}, \qquad \omega_0 = \frac{1}{\sqrt{M_{MT}C_{MT}}}, \quad Q = \frac{\omega_0 M_{MT}}{R_{MT}} = \frac{1}{R_{MT}}\sqrt{\frac{M_{MT}}{C_{MT}}}$$

> [!tip] Band-pass filter → **damping control**
> A second-order band-pass: +6 dB/oct below $f_0$ (spring-controlled), −6 dB/oct above (mass-controlled), flat only in the middle where $R_{MT}$ rules. A dynamic microphone therefore works in its **damping-controlled** region, and the designer's main knob is the felt resistance $R_{AF}$ (via $S_D^2 R_{AF}$ in $R_{MT}$). Compare the condenser microphone (next lectures), which is stiffness-controlled, and the loudspeaker, which is mass-controlled.

### 4c. Sensitivity and bandwidth

> [!note] Sensitivity $M$
> The value of the transfer function at mid frequencies (usually quoted at one normalised frequency, e.g. 1 kHz):
> $$M \simeq \frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D}{R_{MT}} \approx \frac{Bl\,S_D}{R_{MT}} \qquad M_{dB} = 20\log_{10}\frac{M}{1\ \text{V/Pa}}$$
> Example: $M = 5$ mV/Pa $\Leftrightarrow$ $-46$ dB re 1 V/Pa.

> [!note] Bandwidth — the −3 dB points
> $$f_a f_b = f_0^2, \qquad f_b - f_a = \frac{f_0}{Q} \;(= BW) \qquad\Rightarrow\qquad f_{a,b} = f_0\left(\sqrt{1 + \frac{1}{4Q^2}} \mp \frac{1}{2Q}\right)$$
> Sensitivity as a function of $Q$: $M = \dfrac{Bl\,S_D}{R_{MT}} = Q\,Bl\,S_D\sqrt{\dfrac{C_{MT}}{M_{MT}}}$.
> **The trade-off:** high $Q$ → narrow bandwidth, high sensitivity; low $Q$ → wide bandwidth, low sensitivity. Slide 9 shows the two-curve plot (V(v1)/V(v2): output in dB re 1 V/Pa and phase for two dampings).

### 4d. Extending the bandwidth

> [!example] Increasing the *upper* bandwidth — split the back volume (slide 11)
> Back volume divided into $V_1$ (small, right behind the diaphragm) and $V_2$ (large), connected by a tube (+ damping). The tube's air mass **blocks $V_2$ at high frequencies**, so the diaphragm then only sees the small, stiff $V_1$ — a **new, higher resonance** determined by $V_1$ and the moving mass, which props up the response (the plot shows the roll-off pushed from ≈ 3 kHz towards 10 kHz+). Circuit: $C_{A1}$ ($V_1$) to ground, then $M_{A,tube} + R_A$ to a second node with $C_{A2}$ ($V_2$) to ground — [[Lecture 3 - Analogies - Acoustic Systems#9. Problem solving (in-class, part 2) — worked|Problem 2.4]] from Lecture 3, now with the mass included.

> [!example] Increasing the *lower* bandwidth — a tube into the large cavity (slide 12)
> Add a tube from the outside into $V_2$. Tube mass + $V_2$ compliance form a **Helmholtz resonator** that boosts the response around its resonance (the plot shows the low end lifted around 100 Hz), at the price of a **steeper attenuation below** the resonance (the vent short-circuits the pressure at DC — same physics as the bass-reflex box in Problem 4.1).

> [!note] LTspice model (slide 13) — controlled sources
> | Symbol | input | output = gain × input |
> |---|---|---|
> | E | voltage | voltage |
> | F | current | current |
> | G | voltage | current |
> | H | current | voltage |
>
> The slide's three-domain LTspice circuit uses `Re`, `E1`/`F1`-style couplings for $Bl$ and $S_D$, `Mmd, Rms, Cms` in the middle and `Ma1, Raf, Cab` on the right. The KiCad/ngspice version below does the same with two G's per coupling (there is no F symbol in KiCad's `Simulation_SPICE` library).

---

## 5. Problems 4 — dynamic microphones, worked

> [!example]+ Problem 1 — Dynamic microphone design ($\rho=1.18$, $c=344$, 1 inch = 2.54 cm)
> $M_{MD} = 0.2$ g, $R_{MS} = 1$ Ns/m, $C_{MS} = 0.21$ mm/N, diaphragm Ø 1 inch → $a = 12.7$ mm, $S_D = \pi a^2 = 5.067\times10^{-4}$ m², $S_D^2 = 2.567\times10^{-7}$ m⁴. $Bl = 20$ Tm, $R_E = 200$ Ω, $R_L = 47$ kΩ.
>
> **a) Total mass and compliance with $V_{AB} = 30$ cm³.** Air load: $M_{A1} = 8\rho/(3\pi^2 a) = 8\cdot1.18/(3\pi^2\cdot0.0127) = 25.1$ kg/m⁴, so $S_D^2 M_{A1} = 6.4\times10^{-6}$ kg:
> $$M_{MT} = 0.200 + 0.0064 = \boxed{0.206\ \text{g}}\ (\approx 0.205\ \text{g})$$
> Back volume: $C_{AB} = V/\rho c^2 = 30\times10^{-6}/(1.18\cdot344^2) = 2.15\times10^{-10}$ m⁵/N → $S_D^2/C_{AB} = 1195$ N/m; $1/C_{MS} = 4762$ N/m:
> $$C_{MT} = \frac{1}{4762 + 1195} = 1.68\times10^{-4}\ \text{m/N} = \boxed{0.168\ \text{mm/N}}\ ✓$$
>
> **b) Back volume for $f_0 = 1$ kHz.** $C_{MT} = 1/(\omega_0^2 M_{MT}) = 1/((2\pi\cdot1000)^2\cdot2.06\times10^{-4}) = 1.23\times10^{-4}$ m/N → $S_D^2/C_{AB} = 1/C_{MT} - 1/C_{MS} = 8150 - 4762 = 3390$ N/m → $C_{AB} = 2.567\times10^{-7}/3390 = 7.58\times10^{-11}$ m⁵/N → $V = C_{AB}\rho c^2 = \boxed{10.6\ \text{cm}^3}$. The sheet says 10.8 cm³: that is what you get if you carry the *rounded* 0.205 g through ($C_{MT} = 1.236\times10^{-4}$ → 3330 N/m → 10.8 cm³) — a 2 % rounding sensitivity, because $C_{AB}$ comes out of a *difference* of two stiffnesses. Same physics, keep more digits.
>
> **c) $R_{AF}$ for $M = 1$ mV/Pa, and the bandwidth.** $R_{MT} = \dfrac{R_L}{R_E+R_L}\cdot\dfrac{Bl\,S_D}{M} = 0.9958\cdot\dfrac{20\cdot5.067\times10^{-4}}{10^{-3}} = 10.09$ Ns/m. Electrical damping $(Bl)^2/(R_E+R_L) = 400/47200 = 0.0085$ Ns/m (negligible with a 47 kΩ load):
> $$R_{AF} = \frac{R_{MT} - R_{MS} - (Bl)^2/(R_E+R_L)}{S_D^2} = \frac{10.09 - 1 - 0.01}{2.567\times10^{-7}} = \boxed{3.54\times10^{7}\ \text{Ns/m}^5}\ (\approx 3.56\times10^7)$$
> $Q = \dfrac{1}{R_{MT}}\sqrt{\dfrac{M_{MT}}{C_{MT}}} = \dfrac{1}{10.09}\sqrt{\dfrac{2.06\times10^{-4}}{1.23\times10^{-4}}} = 0.129$ → $BW = f_0/Q = \boxed{7.8\ \text{kHz}}$ (7.88 kHz with the rounded values). A $Q$ of 0.13 is *heavily* damped — that is the damping-controlled design.
>
> **d) −3 dB frequencies.** $1/(2Q) = 3.89$, $\sqrt{1 + 1/4Q^2} = 4.02$:
> $$f_a = 1000\,(4.02 - 3.89) = \boxed{126\ \text{Hz}}, \qquad f_b = 1000\,(4.02 + 3.89) = \boxed{7.9\ \text{kHz}}$$
> (sheet: 125 Hz and 8.01 kHz; check $f_a f_b = 10^6$ ✓ and $f_b - f_a = BW$ ✓).

> [!example]+ Problem 2 — Dynamic microphone in LTspice / KiCad
> **a) Model with $V = 5$ cm³ and $R_{AF} = 2\times10^7$ Ns/m⁵** (the mic's influence on the field at high frequency ignored, i.e. no $T(s)$). Hand prediction: $C_{AB} = 3.58\times10^{-11}$, $C_{MT} = 8.38\times10^{-5}$ m/N, $R_{MT} = 1 + 5.13 + 0.01 = 6.14$ Ns/m → $f_0 = 1.21$ kHz, $Q = 0.26$, $M = 1.64$ mV/Pa = **−55.7 dB re 1 V/Pa**, band 291 Hz – 5.0 kHz.
>
> **KiCad + ngspice project ready to open:** `5. Semester/Electroacoustics/KiCad/Problem_4B_Dynamic_Microphone/Problem_4B_Dynamic_Microphone.kicad_sch`. Three blocks left to right — acoustic (impedance analogy: `V1` = $p_i$ = 1 Pa, `L1` = $M_{A1}$, `G1` = the diaphragm carrying $U = S_D u$ from node `pf` to node `pb`, `R1` = $R_{AF}$, `C1` = $C_{AB}$ to ground with a 1 TΩ DC leak), mechanical (mobility: `G2` injects $f = S_D(p_f - p_b)$ into node `u`; `C2` = $M_{MD}$, `L2` = $C_{MS}$, `R4` = $1/R_{MS}$; `G3` draws the electromagnetic reaction $Bl\,i$ with $i = V(\text{out})/R_L$), electrical (`E1` = $Bl\,u$ → `R5` = $R_E$ → node `out` → `R6` = $R_L$). `.ac dec 200 10 100k` on the sheet; the `.wbk` pre-loads gain and phase of `V(/out)`; `sim.py` runs it headless and overlays the closed-form band-pass.
> **Simulated:** peak **−55.69 dB re 1 V/Pa = 1.643 mV/Pa at 1216 Hz**, −3 dB band **295 Hz – 5.0 kHz**; ngspice and the $M_{MT}/R_{MT}/C_{MT}$ formula agree to 0.001 dB over the whole sweep (the whole three-domain circuit really does collapse to one band-pass).
>
> ![[Problem_4B_DynamicMic_sensitivity.png]]
>
> **b) 0.3 mV/Pa and 3 mV/Pa:** $M \propto 1/R_{MT}$ and $R_{MT}$ is dominated by $S_D^2 R_{AF}$ → raise $R_{AF}$ to ≈ $1.3\times10^{8}$ for 0.3 mV/Pa (Q drops to ≈ 0.05, band spreads to ≈ 60 Hz – 25 kHz), lower it to ≈ $9\times10^{6}$ for 3 mV/Pa (Q ≈ 0.47, the band narrows to ≈ 0.5–2.9 kHz). Alternatively change $Bl$ — the sensitivity goes up linearly but $(Bl)^2/(R_E+R_L)$ stays negligible with 47 kΩ.
> **c) Two back cavities + tube + damping (slide 11):** split `C1` into $C_{A1}$ (small, right behind the diaphragm, to ground) and $C_{A2}$ (large, to ground) joined by $M_{A,tube} + R_{A,tube}$; play with the tube (mass) and $V_1$ to place the second resonance above the original roll-off.
> **d) Tube in the large cavity (slide 12):** add $M_{A,vent}$ from the $C_{A2}$ node to ground (outside) → Helmholtz boost at $1/(2\pi\sqrt{M_{A,vent} C_{A2}})$ and a steeper fall below it.
> *(Both variants are a two-minute edit of `layout.py`: add the extra `L`/`R`/`C` in the acoustic block and re-run `sim.py`.)*

---

## Summary — what to walk away with

> [!success] Key takeaways
> - A **transducer is a pair of controlled sources** (or a two-port) with a constant transduction factor: $S$ (area), $Bl$ (moving coil), $v_0/x_0$ (condenser), $1/d$ (piezo). Both directions must be drawn, and the reaction source must **oppose** the motion.
> - Choose the source type from the variable pair: across⇔across = **E**, through⇔through = **F**, across⇔through = **G**, through⇔across = **H**. In KiCad only E and G exist — sense a current as a voltage across a resistor.
> - **Impedance conversion:** acoustic → mechanical is a scaling, $Z_{M,A} = S^2 Z_A$ (front + back in series); mechanical → electrical (electrodynamic) is an **inversion**, $Z_{E,M} = (Bl)^2/Z_M$ — series mechanical resonance = electrical impedance **peak**.
> - **Dynamic microphone** = one second-order **band-pass**, $e/p_i = -Bl S_D\,/\,(j\omega M_{MT} + R_{MT} + 1/j\omega C_{MT})$ with $M_{MT} = M_{MD} + S_D^2 M_{A1}$, $R_{MT} = R_{MS} + S_D^2 R_{AF} + (Bl)^2/(R_E+R_L)$, $C_{MT} = 1/(1/C_{MS} + S_D^2/C_{AB})$. It is **damping-controlled**: sensitivity $M \approx Bl S_D/R_{MT}$, bandwidth $f_0/Q$, and $Q$ trades sensitivity against bandwidth.
> - Bandwidth tricks: split the back volume (new HF resonance from $V_1$ + moving mass) and vent the big cavity (Helmholtz LF boost, steeper roll-off below).
> - Always verify a coupled circuit two ways (mobility vs. impedance, or simulation vs. closed form) — the KiCad projects for 4.4b and the microphone agree with the formulas to numerical precision.

> [!question] Open questions from this lecture to revisit
> - Sign convention of the $Bl\,i$ term in VCH's mechanical loop vs. FL's E/F drawings — confirm which polarity the slides use, the magnitude is unaffected.
> - What does $T(s)$ (free-field scattering) look like numerically, and from which $ka$ does it matter for a 1-inch capsule? (Lecture 21/9.)
> - ⬜

> [!tip] Looking ahead
> Monday 14/9: **microphones — dynamic & condenser (1)** (VCH, Beranek ch. 5, Leach 5.1–5.8). The condenser mic is the electrostatic transducer of §2d with a bias voltage — stiffness-controlled instead of damping-controlled. Thursday 17/9 adds **metrology & calibration** (BIPM brochures in `Literature/Metrology - BIPM/`). And **Lab A** (deadline 20/9) uses today's material directly in parts 3 and 4 — see [[Lab A - Runthrough]].
