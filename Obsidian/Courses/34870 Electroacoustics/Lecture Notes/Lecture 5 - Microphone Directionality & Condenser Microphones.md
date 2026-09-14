---
course: "34870"
course-name: "Electroacoustics"
type: lecture-note
date: 2026-09-14
week: 38
lecture: 5
topic: "Microphone Directionality · Condenser Microphones"
lecturer: VCH
tags: [Electroacoustics, lecture-note, microphones, directional-microphones, condenser-microphone]
---
# Lecture 5 — Microphone Directionality / Condenser Microphones

> [!info] Lecture Info
> **Date:** Monday 14 September 2026, 13:00–17:00 · room 019, building 352, Lyngby · **VCH**
> **Slides:** `Slides/34870_Lecture_5_E26.pdf` (31 numbered slides)
> **Problems:** `Exercises/34870_Problems5_2026.pdf` (condenser microphone, answers in brackets — Q2 parts d/e explicitly deferred to Lecture 6)
> **Refs:** Beranek §5.2–5.6 · Leach §4.6, 5.5, 5.9–5.11
> **Reminder:** the **Lab A quiz** (opened 9 Sep) is due **Sunday 20 Sep**, individual, mandatory for the exam — see [[Lab A - Runthrough]] if not done yet.
> **Previous:** [[Lecture 4 - Analogies - Transducers & Dynamic Microphones|Lecture 4 — transducers + dynamic microphones]] · **Next:** Lecture 6 — condenser mics (2) + metrology & calibration *(VCH, Th 17/9)*

> [!abstract] Where this lecture sits
> Lecture 4B built one microphone from one transduction law: the **electrodynamic** (Lorentz/Faraday) dynamic pressure mic, sealed at the back, giving a **band-pass** response. Today does two things:
> 1. **Opens the back of the diaphragm on purpose.** Exposing the back to sound (with some path delay) turns a pressure mic into a **directional** one — gradient and combination microphones, ending in the whole cardioid family as one parameter $B$.
> 2. **Swaps the transduction law.** Instead of $f=Bl\,i,\ v=Bl\,u$ (electrodynamic), the **condenser** mic uses electrostatics — exactly the linearised law already written down in [[Lecture 4 - Analogies - Transducers & Dynamic Microphones#2d. Electrostatic and piezoelectric transduction (linearised) — slide 15|Lecture 4 §2d]]. Same recipe as always (three domains, controlled sources, total mass/resistance/compliance) but a different coupling constant ($E/x_0$ instead of $Bl$) and — because the coupling is now *voltage*-controlled current sources both ways instead of a gyrator — a **low-pass**, compliance-controlled response instead of a band-pass one.

---

## 1. Repetition — bridge from Lecture 4

> [!question]+ Pop quiz (answered)
> **Q — What made the dynamic mic in Lecture 4B a band-pass filter?**
> The transfer function collapsed to $e_{oc} \propto 1/(j\omega M_{MT} + R_{MT} + 1/j\omega C_{MT})$ — a series $M$–$R$–$C$ with **both** a mass and a compliance in the total impedance (diaphragm mass + air load; suspension compliance backed by a sealed cavity). Low end rolls off because $C_{MT}$ dominates (stiffness-controlled), high end because $M_{MT}$ dominates (mass-controlled), flat band in between set by $R_{MT}$.
>
> **Q — What are the two controlled sources of an electrodynamic transducer, again?**
> $f = Bl\,i$ (force from current) and $v = Bl\,u$ (voltage from velocity) — a **gyrator** in the impedance analogy (§2c/2e of Lecture 4): mechanical impedance reflects into the electrical side **inverted**, $(Bl)^2/Z_M$.
>
> **Q — And the electrostatic (condenser) transducer's laws, from Lecture 4 §2d?**
> $$v = \frac{1}{j\omega C_E}i + \frac{v_0}{j\omega x_0}u \qquad f = -\frac{v_0}{j\omega x_0}i - \frac{1}{j\omega C_M}u$$
> Today re-derives exactly this pair from first principles (energy method) and builds the full three-domain circuit around it. Note the crucial structural difference from the gyrator: **both** couplings here are *current*-controlled-by-voltage and *voltage*-controlled-by-current with the **same sign structure on both sides** (not crossed like Bl) — it behaves as a **transformer**-like pair of dependent sources, not a gyrator, which is why the mechanical resonance shows up as a genuine **low-pass**, not inverted into a parallel-resonance peak the way the loudspeaker voice coil's electrical impedance was in Lecture 4 §2e.

---

## 2. Directional microphones

### 2a. The gradient microphone principle — slide 4

> [!important] Exposing the back of the diaphragm
> If sound also reaches the **back** of the diaphragm after travelling an extra effective path $\Delta l$, the diaphragm only feels the *difference*:
> $$p_D = p_F - p_B = p_F - \left(p_F + \frac{dp}{dx}\Delta l\cos\theta\right) = -\Delta l\cos\theta\,\frac{dp}{dx}$$
> For a plane wave ($dp/dx = -jk\,p$, since $p \propto e^{-jkx}$):
> $$\boxed{p_D = jk\,\Delta l\,p\,\cos\theta}$$
> — a **pressure-gradient** microphone: the diaphragm responds to $dp/dx$, not $p$ itself, and the response is $\cos\theta$-weighted (figure-8 pattern) and proportional to $\omega$ (since $k=\omega/c$).

### 2b. Dynamic gradient microphone (no back cavity) — slide 5

Same electrodynamic transfer function as Lecture 4B, but **without** a back cavity — so the "total compliance" is just the diaphragm's own suspension, $C_{MS}$, not a combined $C_{MT}$ with an air-spring term:

$$\frac{e}{p_D} = \frac{R_L}{R_E+R_L}\cdot\frac{-Bl\,S_D}{j\omega M_{MT} + R_{MT} + 1/j\omega C_{MS}}$$

with $M_{MT} = M_{MD} + S_D^2 M_{AF}$ and $R_{MT} = R_{MS} + S_D^2 R_{AF} + (Bl)^2/(R_E+R_L)$ — same total-impedance bookkeeping as Lecture 4B, just no $C_{AB}$ term.

Substituting the gradient relation $p_D = p\,jk\Delta l\cos\theta$:

$$\boxed{\frac{e}{p} = \frac{R_L}{R_E+R_L}\cdot\frac{-j\omega\,Bl\,S_D\,\Delta l\cos\theta/c}{j\omega M_{MT}+R_{MT}+1/j\omega C_{MS}}}$$

> [!warning] High-pass filter — mass control!
> At low frequency the denominator is compliance-dominated ($1/j\omega C_{MS}$ large), so $e/p \propto j\omega \times 1/(1/j\omega) = (j\omega)^2$ — the response falls at **12 dB/octave** below the corner instead of being flat. This is the structural price of directionality: gradient mics are inherently weak at low frequencies (a **signal-to-noise problem**, flagged explicitly on the slide) unless something else (proximity effect, §2d, or deliberate low-frequency boost in the design) compensates.

### 2c. Ribbon microphone — slides 6–7

The classic dynamic gradient microphone: a thin corrugated aluminium **ribbon** suspended in a strong magnetic field between two pole pieces acts simultaneously as diaphragm *and* voice coil (no separate diaphragm/coil/suspension — the ribbon's own compliance and mass are $C_{MS}$, $M_{MD}$). Typical sensitivity plot: sharp low-frequency rolloff (the mass-control high-pass above), flat mid/high band — exactly the §2b shape.

### 2d. Near-field (proximity) effect — slide 8

The plane-wave assumption behind $p_D = jk\Delta l\,p\cos\theta$ breaks down close to a source. Replace the plane wave with a **spherical wave** from a near point source:
$$p = A\frac{e^{j(\omega t-kr)}}{r} \qquad \frac{dp}{dr} = jkA\frac{e^{j(\omega t-kr)}}{r}\left(1+\frac{1}{jkr}\right)$$

> [!success] The extra term is the whole effect
> The factor $\left(1+\frac{1}{jkr}\right)$ is $\approx 1$ far away (recovering the plane-wave result of §2a) but **blows up at low frequency and short distance** ($kr\ll1$): the gradient microphone gets an automatic **low-frequency boost** the closer the source is. This is the "proximity effect" every singer leaning into a ribbon or cardioid mic exploits — and it is the natural fix for §2b's high-pass problem, *if* you're close enough to the source. Slide 8's plot: flat/rising low end for $r=0.37$–$1.5$ m, converging to the plane-wave (falling) curve as $r\to\infty$.

### 2e. Combination microphone — slides 9–10

Instead of an open back, delay sound to the back through an **internal acoustic path** $\Delta l'$ (a resistive/inertive duct — literally the Problem 2.4 low-pass network from [[Lecture 3 - Analogies - Acoustic Systems#9. Problem solving (in-class, part 2) — worked|Lecture 3 §9]]), *in addition to* the direct external path $\Delta l\cos\theta$:

$$p_D = -\big(\Delta l\cos\theta+\Delta l'\big)\frac{dp}{dx} \qquad\xrightarrow{\text{plane wave}}\qquad p_D = jk\,p\,\Delta l'\,(1+B\cos\theta), \quad B=\frac{\Delta l}{\Delta l'}$$

Mixing a **pure pressure** response (the $1$) with a **pure gradient** response (the $B\cos\theta$) in ratio $B$ is the whole trick — it turns the directivity into a **tunable dial**:

> [!important] The cardioid family — one parameter $B$
> $$R(\theta) = \frac{p_d(\theta)}{p_d(0)} = \frac{1+B\cos\theta}{1+B}$$
>
> | $B$ | Pattern |
> |---|---|
> | $0$ | Omnidirectional (pure pressure) |
> | $1/2$ | Subcardioid |
> | $1$ | **Cardioid** |
> | $\sqrt3$ | Supercardioid |
> | $3$ | Hypercardioid |
> | $\infty$ | Figure-8 / bidirectional (pure gradient) |
>
> Every "directional microphone" on a spec sheet is just this dial turned to one setting — worth memorising the shape, not just the name.

---

## 3. Classification of microphones — slide 11

> [!warning] Two completely different meanings of "pressure microphone" — don't confuse them
> 1. **Closed microphones** (audio jargon: **"pressure" mics**\*) — sealed back, respond to $p$ alone. Two flavours:
>    - (a) designed for **cavities / flush-mount / diffuse field** — this is what sound-measurement people call **"pressure"\*\*** microphones (flat response to the pressure actually present at the diaphragm)
>    - (b) designed for **free-field, normal incidence** — deliberately shaped to *compensate* the pressure build-up in front of an obstacle at high frequency (this is exactly $T(s)$, coming up in §4i)
> 2. **Open microphones** (sound reaches the back): **gradient** (§2a–2d) and **combination** (§2e).
>
> The slide's own emphasis: *do not confuse pressure\* (closed, audio sense) with pressure\*\* (free-field-compensated, measurement sense)* — they describe different design targets that happen to share a name.

---

## 4. Condenser microphones

### 4a. Characteristics — slides 13–14

> [!abstract] What a condenser mic buys you
> High quality, long-term stability, large bandwidth — at the cost of needing a **polarization voltage**. This is why it's the reference standard for calibration and high-end measurement/audio, per the ideal-microphone checklist on slide 13 (flat response, low noise, high sensitivity, orientation-independent, doesn't disturb the field — the last two being aspirational, not achieved).

### 4b. Static analysis — slide 15

A condenser capsule is, statically, just a parallel-plate capacitor: diaphragm (one plate) at rest distance $x_0$ from the fixed back plate.
$$Q = C_{E0}E, \qquad C_{E0}=\varepsilon_0\frac{S}{x_0}, \qquad \varepsilon_0 = 8.85\times10^{-12}\ \text{F/m}$$
Rearranged, this is also the definition used constantly below: $E = Q\,x_0/(\varepsilon_0 S)$.

### 4c. Dynamic transductor model — slides 16–17

Let the diaphragm move: gap becomes $x_0+x(t)$, so capacitance and charge both become time-varying, $C_E(t)=\varepsilon_0 S/(x_0+x(t))$:
$$Q+q(t) = C_E(t)\,\big(E+e(t)\big)$$
where $E,Q$ are the static bias (DC) and $e(t),q(t),x(t)$ are the dynamic voltage, charge and displacement. **Nonlinear** in general (a real diaphragm even has a static, position-dependent deflection under polarization — slide 17's 3-D bowl plot — ignored here by treating $x_0$ as spatially uniform).

### 4d. Electrical analysis — small-signal linearisation — slide 18

$$C_E(t) = \frac{C_{E0}}{1+x(t)/x_0}, \qquad E+e(t) = \frac{Q+q(t)}{C_{E0}}\big(1+x(t)/x_0\big)$$

Expanding and **dropping the second-order term** $q(t)x(t)/(C_{E0}x_0)$ (small × small):
$$E+e(t) \approx E + \frac{q(t)}{C_{E0}} + E\frac{x(t)}{x_0} \quad\Rightarrow\quad e(t) = \frac{q(t)}{C_{E0}} + E\frac{x(t)}{x_0}$$

In the frequency domain ($q = i/j\omega$, $x = u/j\omega$):
$$\boxed{e = \frac{1}{j\omega C_{E0}}\,i + \frac{E}{j\omega x_0}\,u}$$
— a series capacitor $C_{E0}$ carrying $i$, **plus** a voltage source controlled by the mechanical velocity $u$ (an **E**-source, gain $E/x_0$, with the usual $1/j\omega$ pending absorption into a frequency-independent element — done in §4f).

### 4e. Mechanical analysis — energy method — slide 19

Same trick as always, but here the *force* comes from an **energy** argument instead of a direct force law (electrostatics has no simple "Lorentz force" shortcut): stored energy $W = E_E+E_M$, force is minus its gradient with position.
$$W = \frac12\frac{Q_t^2}{C_E}+\frac12\frac{x_t^2}{C_M} = \frac{[Q+q(t)]^2}{2C_E(t)} + \frac{[d-(x(t)+x_0)]^2}{2C_M}$$
Neglecting the $q(t)^2$ term (small-signal) and using $C_E(t)=C_{E0}/(1+x(t)/x_0)$:
$$f(t) = -\frac{dW}{dx} = \underbrace{\left[\frac{Q^2}{2x_0C_{E0}}-\frac{d-x_0}{C_M}\right]}_{\text{static bias — cancelled by the mechanical rest position}} -\ \frac{E}{x_0}q(t) - \frac{x(t)}{C_M}$$

The bracket is the **static** electrostatic force balanced against the static spring preload — it sets the rest position, not the AC response, so it drops out of the small-signal picture. What survives:
$$\boxed{f = -\frac{E}{x_0\,j\omega}\,i - \frac{1}{C_M\,j\omega}\,u}$$
— a **G**-source (current-controlled by voltage $i$, gain $-E/x_0$) plus the diaphragm's own mechanical compliance $C_M$ — matching the electrostatic law quoted from Lecture 4 §2d exactly (with $v_0\to E$).

### 4f. The full transductor model — frequency-independent form — slide 20

Collecting §4d and §4e:
$$e = \frac{1}{j\omega C_{E0}}i+\frac{E}{j\omega x_0}u, \qquad f=-\frac{E}{j\omega x_0}i-\frac{1}{j\omega C_M}u$$

> [!tip] Move the $1/j\omega$ into the source gain — SPICE wants frequency-independent sources
> Multiply/absorb the integration into each element instead of the source: the electrical side becomes a plain capacitor $C_{E0}$ in parallel with a current source $\dfrac{E\,C_{E0}}{x_0}u$ (a **Norton** equivalent), and the mechanical side becomes a plain compliance $C_M$ in parallel with a current source $\dfrac{E\,C_M}{x_0}i$. Two **G**-sources, frequency-independent gains — exactly the pattern flagged as necessary for SPICE in Lecture 4 §2d, now spelled out.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american, scale=0.9]
\draw (0,0) node[ground]{} to[C, l=$C_{E0}$] (0,3) -- (2,3) coordinate(e)
      to[cisource, l_=$\frac{EC_{E0}}{x_0}u$] (2,0) node[ground]{};
\node[above] at (1,3.1) {$e$ (electrical, Norton)};
\draw (5,0) node[ground]{} to[C, l=$C_M$] (5,3) -- (7,3) coordinate(f)
      to[cisource, l_=$\frac{EC_M}{x_0}i$] (7,0) node[ground]{};
\node[above] at (6,3.1) {$f$ (mechanical, Norton)};
\end{circuitikz}
\end{document}
```

### 4g. Polarized condenser microphone — practical bias circuit — slide 21

> [!note] Real-world wiring
> The capsule ($C_{E0}$ + the transductor model) sits between a **large polarization resistor $R_1$** (feeds the bias $E$ without loading the AC signal) and, downstream, an **AC coupling capacitor $C_1$** (blocks the DC bias from the preamp) into the **load resistance $R_L$** (the amplifier input). $R_1$ and $C_1$ must both be large enough not to disturb the audio band — exactly the role $R_L'$ plays generically in the equivalent circuits below (§4i onward): $R_L' = R_L \| R_1$.

### 4h. Pre-polarized (electret) microphone — slide 22

> [!note] Skip the external bias
> A permanently polarized backplate or diaphragm (an electret) makes its **own** built-in field, so no external $E$ supply is needed. Used in hearing aids, mobile phones — small, cheap, no bias circuitry — but **less stable over time** than an externally, actively polarized capsule (the charge decays; externally polarized studio/measurement mics don't have this problem).

### 4i. Full equivalent circuit — three domains — slide 23

> [!abstract] Element glossary
> | Domain | Element | Meaning |
> |---|---|---|
> | Electrical | $R_L'$ | effective load ($R_L \| R_1$) |
> | Mechanical | $M_{MD}$ | effective diaphragm mass |
> | | $C_{MD}$ | effective diaphragm compliance |
> | | $R_{MD}$ | damping of diaphragm |
> | Acoustical | $C_{AB1}$ | compliance of the **small** volume between electrode and diaphragm |
> | | $C_{AB2}$ | compliance of the (larger) back volume |
> | | $M_{AS}$ | acoustic mass of the holes in the back electrode |
> | | $R_{AS}$ | acoustic damping associated with the back electrode |
> | | $M_{A1}$ | air mass in front (radiation impedance — piston on a cylinder, from [[Lecture 4 - Analogies - Transducers & Dynamic Microphones#8b. Radiation impedance — piston in an infinite baffle|Lecture 4 §8b]]-style formulas) |
> | | $T(s)$ | free-field scattering effect: $T(s) = 1+\dfrac{Z_{AR}}{\rho c/S_D}$ |
>
> Topology: electrical loop ($R_L'$, $C_{E0}$, source $\frac{E}{x_0s}u_D$) ↔ mechanical loop ($C_{MD}$–$u_D$–$M_{MD}$–$R_{MD}$, sources $\frac{Ei}{x_0s}$ and $S_D p_D$) ↔ acoustical network: the diaphragm's volume velocity $S_D u_D$ is injected into the **small** front-of-backplate gap ($C_{AB1}$), which connects through $R_{AS}$–$M_{AS}$ (the backplate holes) to the **large** back volume ($C_{AB2}$); $p_D$ is measured at the injection node; $M_{A1}$ and the incident pressure $T(s)p_i$ sit on the front side.

> [!warning] The correction that isn't in Leach or Beranek
> Slide 24, in red: **losses happen mostly in the narrow front gap, not through the backplate holes** — i.e. the textbook model's $R_{AS}$ (holes) is the *wrong place* to put the dominant damping; the real dissipation is squeeze-film damping in the thin gap between diaphragm and backplate. The lumped-element topology above is still what you calculate with (and what Problem 5.1 uses), but know that it's a simplification the lecturer explicitly flagged as physically imprecise — a genuine research-level correction to two textbooks the course otherwise treats as authoritative.

### 4j. Transfer function — slide 25

> [!important] Three loop equations (assuming $C_{AB1}\ll C_{AB2}$, so it drops out entirely)
> **Acoustical:** $\;p_D = T(j\omega)p_i + S_D u_D\left[j\omega(M_{A1}+M_{AS})+R_{AS}+\dfrac{1}{j\omega C_{AB2}}\right]$
> **Mechanical:** $\;-\dfrac{E}{j\omega x_0}i - S_D p_D = u_D\left[j\omega M_{MD}+R_{MD}+\dfrac{1}{j\omega C_{MD}}\right]$
> **Electrical:** $R_L'\uparrow\uparrow \;\Rightarrow\; i\approx0 \;\Rightarrow\; e\approx e_{OC} = \dfrac{E}{j\omega x_0}u_D$
>
> Eliminating $p_D$, $u_D$ (same substitution pattern as Lecture 4B §4b, but now with **no** electrical-load term surviving, since $i\to0$):
> $$\boxed{e_{OC} = -\frac{E\,S_D}{j\omega x_0\big[j\omega M_{MT}+R_{MT}+1/j\omega C_{MT}\big]}\,T(j\omega)\,p_i}$$
> $$M_{MT}=M_{MD}+S_D^2(M_{A1}+M_{AS}), \qquad R_{MT}=R_{MD}+S_D^2 R_{AS}, \qquad \frac1{C_{MT}}=\frac1{C_{MD}}+\frac{S_D^2}{C_{AB2}}$$

> [!success] Low-pass filter — compliance control!
> Rearranged into the standard second-order form:
> $$e_{OC} = -\frac{ES_DC_{MT}}{x_0}\cdot\frac{1}{-(\omega/\omega_0)^2+(1/Q)(j\omega/\omega_0)+1}\,T(j\omega)p_i$$
> $$\omega_0=\frac{1}{\sqrt{M_{MT}C_{MT}}}, \qquad Q=\frac{\omega_0 M_{MT}}{R_{MT}}=\frac1{R_{MT}}\sqrt{\frac{M_{MT}}{C_{MT}}}, \qquad \text{sensitivity } M = \frac{ES_DC_{MT}}{x_0}$$
> Unlike the dynamic mic (band-pass) and the dynamic gradient mic (high-pass, §2b), the condenser mic's electrical output is **flat below $\omega_0$, then falls off above it** — a straightforward low-pass with a possible resonance bump right at the corner if $Q>1/\sqrt2$ (compliance-controlled at low/mid frequency, exactly the opposite failure mode from the mass-controlled gradient mic).

### 4k. Extracting $f_s$ and $Q$ from a measured sensitivity curve — slide 27 (this is Lab C)

> [!tip] The two-step method
> **Step 1 ($f_s$):** find the frequency where the *phase* has dropped **90°** from its mid-band value.
> **Step 2 ($Q$):** $Q = e_{OC}(f_s)/e_{OC}(f\ll f_s)$ — the **linear** sensitivity ratio at resonance vs. in the flat band.
>
> **Gotcha, worth remembering going into Lab C:** for a mic design with $Q<1$ (overdamped, no visible peak), this ratio is **less than 1**, which is a **negative number in dB** — "a drop in sensitivity at resonance," not a rise. Don't assume a resonance always means a bump; read the sign.

### 4l. Equivalent output impedance — slide 28

$$Z_{out} = \frac{e_{oc(i=0)}}{-i_{sc(e=0)}} = \frac{1}{j\omega C_{E0}}\cdot\frac{E^2}{x_0^2(j\omega)^2 Z_{MT}}$$

Representable as a small RLC network in parallel with $C_1$ ($=C_{E0}$'s companion): $C_1 = \left[\dfrac{1}{C_{E0}}-\dfrac{E^2C_{MT}}{x_0^2}\right]^{-1}$, $C_2=\dfrac{x_0^2}{E^2C_{MT}}$, $R=\dfrac{E^2R_{MT}C_{MT}^2}{x_0^2}$, $L=\dfrac{E^2M_{MT}C_{MT}^2}{x_0^2}$.

> [!warning] Practical consequence
> **The output voltage droops at low frequency if $R_L'$ isn't large enough** — the "large polarization resistor" of §4g isn't just about not loading the bias supply, it's what keeps the *output* flat down to the bottom of the audio band. This is exactly the mechanism behind every condenser mic datasheet's warning about minimum preamp input impedance.

### 4m. LTspice circuit — slide 30 (this is Problem 5.2)

Three sub-circuits matching §4i one-for-one: **Electrical** — `Vd2` (polarization) → `Ce0` ∥ `FECe0u` (current-controlled... actually voltage-controlled, gain $EC_{E0}/x_0$) → `RL` → `OUT`. **Mechanical** — `FECmi` (mirror source) ∥ `Cmd` – `Rmd` – `Mmd` – `ESdPd` (the $S_D p_D$ reaction voltage). **Acoustical** — `Ras`–`Mas` in series between `Cab2` and `Cab1`, `FSdUd` (the $S_D u_D$ injection) at that node, `Ra1`∥`Ra2` + `Ma1` on the front side, driven by `Vpi` (AC 1, the incident pressure) through the `Gpb` scattering block realising $T(s)$.

---

## 5. Problem solving

> [!example]+ Problem 5.1 — Condenser microphone, worked
> $\rho=1.18$ kg/m³, $c=344$ m/s. $C_{MD}=4\times10^{-6}$ m/N, $M_{MD}=0.050$ g $=5\times10^{-5}$ kg, $R_{MD}=1$ Ns/m, effective diaphragm radius $a=9$ mm. $M_{AS}=100$ kg/m⁴, $R_{AS}=10^7$ Ns/m⁵, $V_{AB2}=1$ cm³. $C_{AB1}\ll C_{AB2}$ (given, drop it — §4j). $E=200$ V, $x_0=20\times10^{-6}$ m, $R_L'=500$ MΩ (large — confirms the $i\approx0$ assumption of §4j).
>
> **Setting up the totals.** The problem gives the *back-side* acoustics but not a front-side mass directly — that's what the "effective diaphragm radius" is for: $M_{A1}$ is the **piston-on-a-cylinder radiation mass** from [[Lecture 4 - Analogies - Transducers & Dynamic Microphones#8b. Radiation impedance — piston in an infinite baffle|Lecture 4 §8b]], $M_{A1}=\dfrac{8\rho}{3\pi^2 a}$ — a direct callback, and it turns out to matter (see below).
>
> $$S_D=\pi a^2 = \pi(0.009)^2 = 2.5447\times10^{-4}\ \text{m}^2 \qquad S_D^2 = 6.4755\times10^{-8}\ \text{m}^4$$
> $$M_{A1}=\frac{8\times1.18}{3\pi^2\times0.009}=35.43\ \text{kg/m}^4$$
> $$C_{AB2}=\frac{V_{AB2}}{\rho c^2}=\frac{10^{-6}}{1.18\times344^2}=7.163\times10^{-12}\ \text{m}^5/\text{N}$$
>
> $$M_{MT}=M_{MD}+S_D^2(M_{A1}+M_{AS}) = 5\times10^{-5}+6.4755\times10^{-8}\times135.43 = 5.877\times10^{-5}\ \text{kg}$$
> $$\frac1{C_{MT}}=\frac1{C_{MD}}+\frac{S_D^2}{C_{AB2}} = 2.5\times10^5+9040.0=2.5904\times10^5 \;\Rightarrow\; C_{MT}=3.860\times10^{-6}\ \text{m/N}$$
> $$R_{MT}=R_{MD}+S_D^2 R_{AS} = 1+6.4755\times10^{-8}\times10^7 = 1+0.6475 = 1.648\ \text{Ns/m}$$
>
> **a) Resonance frequency:**
> $$f_0=\frac1{2\pi\sqrt{M_{MT}C_{MT}}}=\frac1{2\pi\sqrt{5.877\times10^{-5}\times3.860\times10^{-6}}}\approx\boxed{10.57\ \text{kHz}}$$
> (sheet: **10.6 kHz** ✓ — matches once $M_{A1}$ is included; leaving it out gives 10.8 kHz.) **Official MATLAB solution (`Exercises/34870_Solutions5_2026.pdf`, delivered 14-Sep):** it takes $M_{A1} = 0.6133\rho/(\pi r) = 25.6$ kg/m⁴ ("piston in a tube, free field"), giving $M_{MT} = 5.813\times10^{-5}$ kg, $f_0 = 10\,624$ Hz and $Q = 2\pi M_{MT} f_0/R_{MT} = 2.355$ — same answers to the sheet's precision, but that is the convention the course uses for the front air mass of a microphone (same as in the Problems 4 solutions).
>
> **b) Quality factor:**
> $$Q=\frac1{R_{MT}}\sqrt{\frac{M_{MT}}{C_{MT}}} = \frac1{1.648}\sqrt{\frac{5.877\times10^{-5}}{3.860\times10^{-6}}}\approx\boxed{2.37}$$
> (sheet: **2.3** ✓, within rounding.)
>
> **c) Sensitivity (flat band, $T(s)=1$):**
> $$M=\frac{ES_DC_{MT}}{x_0}=\frac{200\times2.5447\times10^{-4}\times3.860\times10^{-6}}{20\times10^{-6}}\approx 9.82\times10^{-3}\ \text{V/Pa}=\boxed{9.8\ \text{mV/Pa}}$$
> (sheet: **9.8 mV/Pa** ✓ exact.)
>
> **Gotcha worth keeping:** $S_D^2R_{AS}$ (giving $R_{MT}$) and $S_D^2/C_{AB2}$ (giving $C_{MT}$) look similar but are **three orders of magnitude apart in scale** ($0.65$ vs $9040$, in incompatible-looking but dimensionally-correct units) — easy to mis-key on a calculator (a $\times10^{-8}\times10^{7}$ slip costing a factor of $1000$ turns a believable $Q\approx2.4$ into a nonsense $Q\approx0.006$). Always sanity-check $Q$ against "does the plot look like it has a resonance bump" before trusting the arithmetic.

> [!example]+ Problem 5.2 — equivalent circuit, worked (a–c; d–e next lecture)
> Built and simulated the full three-domain circuit (KiCad + ngspice, not LTspice — the graded LTspice build in Lab C still has to be done separately by hand): `5. Semester/Electroacoustics/KiCad/Problems 5 - Condenser Microphone/Problem_5_Condenser_Microphone/` — electrical loop ($C_{E0}$ in series with a Norton-realised source, then $R_L'$), mechanical mobility node ($M_{MD}$ cap, $C_{MD}$ inductor, $R_{MD}$ resistor to ground, driven by two G-sources), acoustical series loop ($p_i \to M_{A1} \to$ diaphragm $\to R_{AS} \to M_{AS} \to C_{AB2}$, $T(s)=1$ ignored, mirroring [[Lecture 4 - Analogies - Transducers & Dynamic Microphones|Lecture 4]]'s dynamic-mic acoustic block almost verbatim).
>
> **The one genuinely new circuit trick** (beyond copying Problem 4B's pattern): the electrostatic coupling constant $E/x_0$ carries an extra $1/j\omega$ that $Bl$ never had (§4d/e), so a plain frequency-independent G/E-source can't realise it directly. Fix (exactly slide 20's own advice): tap the *voltage across $C_{E0}$ itself* (already $=i/(j\omega C_{E0})$ by definition of a capacitor) for the electrical→mechanical reaction, and tap the *current through the $C_{MD}$-as-inductor branch* (via a 1 µΩ sense resistor, sensing $u/(j\omega C_{MD})$) for the mechanical→electrical direction — both frequency-independent by construction, no Laplace sources needed.
>
> **Gotcha hit repeatedly while wiring it up:** a controlled source's two control pins ($C+/C-$) sit on their own dedicated x-column, one grid step from the $N+/N-$ column — route each pin's sense wire *sideways off that column* before running it to a rail. Sending it straight to a rail at the same x it started from will pass directly through the *other* control pin (or through $N+/N-$) purely by coordinate coincidence, silently shorting two unrelated nodes together. Caught three separate instances of this while building this one schematic — cheap to avoid, expensive to debug from a netlist dump alone.
>
> **Verified three ways, all agreeing:** ngspice's `V(out)` matches an independent 4-equation linear-system solve (same topology, solved directly in Python, no hand-simplification) to $8\times10^{-5}$ dB — confirms the schematic is a faithful realisation of the intended circuit — and matches Problem 5.1's simple $M_{MT},R_{MT},C_{MT}$ total-impedance formula to within 0.004 dB in-band (100 Hz–30 kHz), confirming $R_L'=500\,\text{M}\Omega$ really is "large enough" that the two models coincide. Peak sensitivity **23.8 mV/Pa at 10.1 kHz** (below $f_0=10.57$ kHz, as expected for $Q=2.37>1/\sqrt2$ — the peak sits at $f_0\sqrt{1-1/(2Q^2)}$), flat-band sensitivity 9.82 mV/Pa, low-pass rolloff above resonance — the "compliance control" shape from §4j, reproduced from first principles.
>
> ![[Problem_5.1_CondenserMic_sensitivity.png]]
>
> **Response is already close to flat** at the given $R_L'$ (no further "adjustment" needed for part c) — §4l's droop estimate puts the $R_L'$-limited corner below 1 Hz at this polarization resistance, far outside the audio band. **Keep this circuit** — Problem 5.2 d)/e) (adding $T(s)$ and optimizing) are covered in Lecture 6, and the same capsule model is reused directly in **Lab C** (microphone calibration). Full worked derivation + the sign/topology reasoning: [[Problems 5 - Condenser Microphone, Worked|Problems 5 — Worked Solutions]].

---

## Summary — what to walk away with

> [!success] Key takeaways
> - **Gradient microphones** respond to $dp/dx$, not $p$: inherently a **high-pass** (mass-controlled, 12 dB/oct rolloff) unless the **near-field/proximity effect** compensates at short range.
> - **Combination microphones** blend a pressure path and a gradient path in ratio $B$ — the entire cardioid family (omni → figure-8) is one dial, $R(\theta)=(1+B\cos\theta)/(1+B)$.
> - **Closed vs. open**, and **"pressure" (audio, sealed) vs. "pressure" (measurement, diffuse-field/flush-mount)** are two different classifications that happen to share vocabulary — don't conflate them.
> - The **condenser transducer's** two controlled sources ($e=i/j\omega C_{E0}+Eu/j\omega x_0$, $f=-Ei/j\omega x_0-u/j\omega C_M$) come straight from linearising $Q+q=C_E(E+e)$ and an energy argument — same coupling law already quoted (unresolved) back in Lecture 4 §2d.
> - The full capsule ends in the **same total-mass/-resistance/-compliance bookkeeping** as the dynamic mic, but because there's no gyrator, the result is a **low-pass** (compliance-controlled) response, not a band-pass.
> - **Losses in a real condenser capsule are dominated by the front squeeze-film gap, not the backplate holes** — the standard textbook lumped model ($R_{AS}$ on the holes) is a known simplification.
> - **Lab C's $f_s$/$Q$-from-measurement recipe:** 90°-phase-drop frequency, then the *linear* sensitivity ratio at that frequency vs. mid-band — watch the sign when $Q<1$.

> [!question] Open questions from this lecture to revisit
> - ⬜ Confirm the small ~0.3–3 % gaps between the hand-calculated Problem 5.1 numbers above and the sheet's bracketed answers — likely just intermediate rounding, but worth checking against the worked solution if one is posted.

> [!tip] Looking ahead
> Thursday 17/9: **condenser microphones (2) + metrology & calibration** (VCH) — Problem 5.2 parts d)/e) ($T(s)$, optimization) get covered, and this is the lecture the `Literature/Metrology - BIPM/` reading was fetched for. Worth a look at the DFM primary metrology lab (cellar of building 352) around this week.
