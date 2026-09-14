---
course: "34870"
course-name: "Electroacoustics"
type: exercise
date: 2026-09-14
week: 38
topic: "Problems 5 — Condenser Microphone"
tags: [Electroacoustics, exercise, condenser-microphone, worked-solution]
---
# Problems 5 — Condenser Microphone, Worked Solutions

> [!info] Source
> `Exercises/34870_Problems5_2026.pdf` — two problems, answers to Problem 1 given in brackets. Problem 2 parts d)/e) (adding $T(s)$, optimizing) are explicitly deferred to Lecture 6.
> Theory backing this sheet: [[Lecture 5 - Microphone Directionality & Condenser Microphones|Lecture 5]] §4 (condenser microphone derivation) and [[Lecture 4 - Analogies - Transducers & Dynamic Microphones|Lecture 4]] §2d (electrostatic transduction law) + §8b (piston radiation mass).
> KiCad + ngspice project: `5. Semester/Electroacoustics/KiCad/Problems 5 - Condenser Microphone/Problem_5_Condenser_Microphone/`.

---

## Problem 1 — Condenser microphone

> [!note] Given
> $\rho = 1.18\ \text{kg/m}^3$, $c = 344\ \text{m/s}$.
> **Mechanical:** $C_{MD}=4\times10^{-6}\ \text{m/N}$, $M_{MD}=0.050\ \text{g}$, $R_{MD}=1\ \text{Ns/m}$, effective diaphragm radius $a=9\ \text{mm}$.
> **Acoustic (back of diaphragm):** $M_{AS}=100\ \text{kg/m}^4$, $R_{AS}=10^7\ \text{Ns/m}^5$, $V_{AB2}=1\ \text{cm}^3$. Given: $C_{AB1} \ll C_{AB2}$ ($V_{AB1}$ more than 200× smaller than $V_{AB2}$).
> **Electrical:** $E=200\ \text{V}$ (polarization), $x_0=20\times10^{-6}\ \text{m}$, $R_L'=500\ \text{M}\Omega$.

### Setting up the totals

The sheet gives the *back-side* acoustics but no front-side mass directly. That's what "effective diaphragm radius" is for: $M_{A1}$ is the **piston-on-a-cylinder radiation mass** from Lecture 4 §8b,
$$M_{A1} = \frac{8\rho}{3\pi^2 a}$$
— a direct callback, and skipping it gives a resonance frequency that's *plausible but wrong* (see the gotcha at the end).

$$S_D = \pi a^2 = \pi(0.009)^2 = 2.5447\times10^{-4}\ \text{m}^2 \qquad S_D^2 = 6.4755\times10^{-8}\ \text{m}^4$$
$$M_{A1} = \frac{8\times1.18}{3\pi^2\times0.009} = 35.43\ \text{kg/m}^4$$
$$C_{AB2} = \frac{V_{AB2}}{\rho c^2} = \frac{10^{-6}}{1.18\times344^2} = 7.163\times10^{-12}\ \text{m}^5/\text{N}$$

Using the totals from Lecture 5 §4j (with $C_{AB1}$ dropped, as given):
$$M_{MT} = M_{MD} + S_D^2(M_{A1}+M_{AS}) = 5\times10^{-5} + 6.4755\times10^{-8}\times135.43 = 5.877\times10^{-5}\ \text{kg}$$
$$\frac{1}{C_{MT}} = \frac{1}{C_{MD}} + \frac{S_D^2}{C_{AB2}} = 2.5\times10^5 + 9040.0 = 2.5904\times10^5 \;\Rightarrow\; C_{MT} = 3.860\times10^{-6}\ \text{m/N}$$
$$R_{MT} = R_{MD} + S_D^2 R_{AS} = 1 + 6.4755\times10^{-8}\times10^7 = 1 + 0.6475 = 1.648\ \text{Ns/m}$$

### a) Resonance frequency

$$f_0 = \frac{1}{2\pi\sqrt{M_{MT}C_{MT}}} = \frac{1}{2\pi\sqrt{5.877\times10^{-5}\times3.860\times10^{-6}}} \approx \boxed{10.57\ \text{kHz}}$$

Sheet answer: **10.6 kHz** ✓.

> [!warning] Gotcha #1 — forgetting $M_{A1}$
> Without the front-side radiation mass, $M_{MT}=5\times10^{-5}+6.4755\times10^{-8}\times100=5.647\times10^{-5}$ kg, giving $f_0\approx10.78$ kHz — close enough to look "probably right" on a first pass, but it's off by 1.7 % because it's missing real physics, not just rounding. The radius given in the problem is doing double duty (both $S_D$ *and* $M_{A1}$ depend on it) — that's the tell that it's needed for both.

### b) Quality factor

$$Q = \frac{1}{R_{MT}}\sqrt{\frac{M_{MT}}{C_{MT}}} = \frac{1}{1.648}\sqrt{\frac{5.877\times10^{-5}}{3.860\times10^{-6}}} \approx \boxed{2.37}$$

Sheet answer: **2.3** ✓ (within rounding).

> [!warning] Gotcha #2 — the exponent slip that nearly wrecked this
> $S_D^2 R_{AS} = 6.4755\times10^{-8}\times10^{7}$. First pass through this by hand gave **647.5**, not **0.6475** — an exponent-arithmetic slip ($10^{-8}\times10^{7}=10^{-1}$, not $10^{2}$) that inflates $R_{MT}$ by exactly $1000\times$. With the wrong value, $Q$ comes out as $0.0059$ — an overdamped, no-resonance system, visibly inconsistent with the sheet's own plot (slide 26) showing a clear peak. **Sanity check any $Q$ result: if the shape doesn't match "there should obviously be a bump here," recheck the exponent arithmetic before anything else.**

### c) Pressure sensitivity, flat band ($T(s)=1$)

$$M = \frac{E S_D C_{MT}}{x_0} = \frac{200\times2.5447\times10^{-4}\times3.860\times10^{-6}}{20\times10^{-6}} \approx 9.82\times10^{-3}\ \text{V/Pa} = \boxed{9.8\ \text{mV/Pa}}$$

Sheet answer: **9.8 mV/Pa** ✓ exact.

---

## Problem 2 — Equivalent circuit (LTspice on the sheet; built here in KiCad/ngspice)

> [!note] Scope
> a)–c) done here. d)/e) (adding $T(s)$, optimizing the response) are covered in Lecture 6 — **keep this circuit**, it's reused directly for that and for Lab C (microphone calibration).

### The circuit topology, and why each piece looks the way it does

Three domains, same pattern as [[Lecture 4 - Analogies - Transducers & Dynamic Microphones#4. Lecture 4B — Dynamic microphones (VCH)|Lecture 4B's dynamic mic]] wherever the physics is the same, and one genuinely new piece where it isn't.

**Acoustical (impedance analogy, series loop) — copied almost verbatim from Problem 4B:**
$$p_i \xrightarrow{M_{A1}} \text{node } p_f \xrightarrow{\text{diaphragm (forces } U=S_D u\text{)}} \text{node } p_b \xrightarrow{R_{AS}} \xrightarrow{M_{AS}} \xrightarrow{C_{AB2}} \text{gnd}$$
An ideal current source (a G-source, gain $S_D$, controlled by the mechanical node's velocity $u$) sits *in series* at the diaphragm's position, forcing the loop current to $S_D u$ throughout — exactly Problem 4B's `G1`. This works because a voltage source and a current source in series is a perfectly valid, non-degenerate configuration: the current source dictates the current, the voltage source ($p_i$) just contributes its own fixed voltage to the loop's KVL sum. Reading off $p_f-p_b$ (both nodes straddling the forced-current injection point) gives exactly
$$p_f - p_b = p_i - S_D u\,\big[j\omega(M_{A1}+M_{AS}) + R_{AS} + 1/j\omega C_{AB2}\big]$$
— the front mass and the whole back chain combine into **one** additive impedance, which is *why* the mechanical reaction must sense the **difference** $p_f-p_b$, not $p_f$ alone (an earlier draft of this circuit sensed only $p_f$ and silently dropped every back-side element's effect on the resonance — caught by checking that $M_{AS}/R_{AS}/C_{AB2}$ actually moved $f_0$ in a test sweep, which the "$p_f$-only" version failed).

**Mechanical (mobility analogy, node $u$):** $M_{MD}$ → capacitor to ground, $C_{MD}$ → inductor to ground, $R_{MD}$ → resistor of value $1/R_{MD}$ to ground — same convention as every mobility-form node all course ([[Lecture 4 - Analogies - Transducers & Dynamic Microphones]] §2c, Problem 4.4b). Two current sources injected here: $+S_D(p_f-p_b)$ (acoustic reaction, plain frequency-independent G-source, no tricks — it's the ordinary piston law $f=Sp$ used everywhere else in this course) and the electrostatic reaction (next).

**Electrical (series loop) and the one genuinely new trick:**

Lecture 4 §2c's electrodynamic coupling ($f=Bl\,i$, $v=Bl\,u$) is frequency-independent — SPICE-native, no conversion needed, which is why Problem 4B's electrical↔mechanical coupling was two plain sources. The **electrostatic** coupling (§4d/e of Lecture 5) is not:
$$e = \frac{i}{j\omega C_{E0}} + \frac{E}{j\omega x_0}u \qquad f = -\frac{E}{j\omega x_0}i - \frac{u}{j\omega C_{MD}}$$
Both cross-terms carry an extra $1/j\omega$ that $Bl$ never had — a direct consequence of the coupling arising from *charge* ($q=\int i\,dt$) and *displacement* ($x=\int u\,dt$) rather than direct force/velocity. A plain SPICE E/G source has a constant (frequency-independent) gain, so neither cross-term can be built directly.

The fix (this is exactly Lecture 5 slide 20's own point about "frequency-independent sources"): don't invent a new integrator — **reuse a capacitor that's already carrying the right current**.
- **Electrical → mechanical:** the voltage *across $C_{E0}$ itself* is, by definition of a capacitor, $i/(j\omega C_{E0})$. So the mechanical reaction $-\big(E/(j\omega x_0)\big)i = -(E C_{E0}/x_0)\cdot V(C_{E0})$ is a **plain, frequency-independent** G-source with gain $-EC_{E0}/x_0$, controlled directly by the voltage across $C_{E0}$ (no sense resistor needed — just probe both of its terminals).
- **Mechanical → electrical:** $C_{MD}$ is represented as an *inductor* (mobility form), and an inductor's own branch current is $u/(j\omega C_{MD})$ — exactly the integral of $u$ needed. Sense that branch current via a tiny (1 µΩ) series resistor to ground, and the electrical source $\big(E/(j\omega x_0)\big)u = (EC_{MD}/(x_0 R_{\text{sense}}))\cdot V(R_{\text{sense}})$ is likewise a plain, frequency-independent E-source.

No Laplace/behavioural sources, no auxiliary integrators invented from scratch — both directions reuse a capacitor (or inductor) that the physical circuit already needs anyway.

> [!warning] Gotcha #3 — a control pin's own column shorts to its neighbour
> A KiCad `GSOURCE`/`ESOURCE`'s two control pins ($C+$/$C-$) sit on their own x-column, one grid step over from the $N+$/$N-$ column — and $C+$ and $C-$ themselves share *that* column, one above the other. Wiring one control pin straight up/down to a rail, with no horizontal offset first, sends a vertical wire segment right through the *other* control pin's exact coordinate — and the schematic-generator's own wire-splitting (which exists specifically so KiCad's cleanup pass can't silently disconnect a mid-wire junction) turns that pass-through into a real short. Hit this **three separate times** building this one schematic: $E_1$'s $N-$ routed through its own $N+$; $G_3$'s $C+$ label routed through $G_3$'s own $C-$-to-ground wire; and the fix for that promptly landed $C-$'s new column on top of the *unrelated* $N+/N-$ column instead. Diagnosed each time the same way — dump `sh.netlist()`, find a node with pins that have no business being together, then check with `_on_seg()` whether a "clean-looking" wire silently threads through a third pin's coordinates. **Rule going forward: any time two pins share an x (or y) column, route the wire for one of them *sideways off that column* before running it anywhere near the other pin's coordinate range — never assume "it's just passing near it, not through it" without checking the actual numbers.**

### Verification

Checked three independent ways, matching to within numerical noise:
1. **ngspice's `V(out)`** vs **a 4-equation linear system solved directly in Python** from this same circuit's own node/loop equations (no hand-simplification, no reuse of the Problem 1 formulas) — agree to $8\times10^{-5}$ dB. This confirms the *schematic* is a faithful realisation of the intended topology, independent of whether the topology itself matches Problem 1's simplified picture.
2. That same simulation vs **Problem 1's simple $M_{MT},R_{MT},C_{MT}$ formula** (valid in the $R_L'\to$ large limit) — agree to within 0.004 dB across 100 Hz–30 kHz. Confirms $R_L'=500\ \text{M}\Omega$ really is "large enough" for the two pictures to coincide in the audio band.
3. Peak sensitivity from the sweep: **23.8 mV/Pa at 10.1 kHz** — below $f_0=10.57$ kHz, as expected for $Q=2.37>1/\sqrt2$ (a peaked response's maximum sits at $f_0\sqrt{1-1/(2Q^2)}$, not exactly at $f_0$). Flat-band sensitivity **9.82 mV/Pa**, matching part c) exactly, with the low-pass rolloff above resonance matching Lecture 5 §4j's "compliance control" description.

![[Problem_5.1_CondenserMic_sensitivity.png]]

### c) "Adjust for flatness" — is there anything to adjust?

Not much, at these values. Lecture 5 §4l's output-impedance analysis gives the $R_L'$-limited low-frequency corner as roughly
$$f_{\text{droop}} \sim \frac{E^2 C_{MT}}{2\pi x_0^2 R_L'}$$
which, plugging in Problem 1's numbers, lands **below 1 Hz** — far outside the audio band. The response is already essentially flat below $f_0$ at $R_L'=500\ \text{M}\Omega$; there's nothing left to tune without changing the capsule's own mechanical/acoustic values (which the problem doesn't ask for). This is presumably also why the exercise waits until d)/e) — with $T(s)$ added — before there's a genuinely open design choice to make.
