---
course: "62755"
course-name: "Power Electronics"
type: lecture-note
date: 2026-09-21
lecture: 3
topic: "Diode rectifiers — pre-read (performance parameters, single-phase, three-phase, filters, source inductance)"
tags: [PowerElectronics, lecture-note, rectifiers, pre-read]
---

# Lecture 3 — Diode Rectifiers: pre-read

> [!info] For Monday 21 Sep, 8:30, Ballerup
> **Deck:** [[Diodes Rectifiers.pdf]] (30 slides, posted Sunday evening; it replaces the older `Slides/Lecture 3 Diode Rectifier.pdf`) · **Homework:** [[Assignment 2.pdf]] (13 pages, problems 2.1–2.6 and assignments 2.1–2.3) · Book: Rashid, *Power Electronics*, ch. 3.
> The equations in the deck are pictures, so they are typed out here. **Written before the lecture from the slides: check it against what Ashraf actually says and fix it afterwards.** Bring the laptop with MATLAB + Simscape.

## The one idea

A rectifier turns AC into DC with diodes, which switch themselves: a diode conducts when its anode is the most positive (or its cathode the most negative) point around. No control, so everything follows from the waveform. A good rectifier gives a DC voltage with **little ripple** and draws an input current that is **sinusoidal and in phase** (power factor near 1). Most of the lecture is a set of numbers that say how far a given circuit is from that ideal, and how more phases get closer to it.

```mermaid
flowchart LR
    A[Performance parameters<br/>eta, FF, RF, TUF, PF, CF, HF] --> B[Single-phase full wave<br/>R load, then RL + battery]
    B --> C[Highly inductive load<br/>square-wave input current, PF 0.90]
    C --> D[q-phase star<br/>more phases, less ripple]
    D --> E[Three-phase bridge<br/>6 pulses, the workhorse]
    E --> F[Design: diode ratings,<br/>L, C, LC filters]
    F --> G[Source inductance<br/>commutation overlap, lost volts]
```

## 1. The performance parameters (slides 5–7)

Output side: average $V_{dc}$, $I_{dc}$ and rms $V_{rms}$, $I_{rms}$.

| Quantity | Definition | Ideal |
|---|---|---|
| DC power | $P_{dc} = V_{dc} I_{dc}$ | |
| AC power | $P_{ac} = V_{rms} I_{rms}$ | |
| Efficiency (rectification ratio) | $\eta = P_{dc}/P_{ac}$ | 100 % |
| AC component of the output | $V_{ac} = \sqrt{V_{rms}^2 - V_{dc}^2}$ | 0 |
| Form factor | $FF = V_{rms}/V_{dc}$ | 1 |
| Ripple factor | $RF = V_{ac}/V_{dc} = \sqrt{FF^2 - 1}$ | 0 |
| Transformer utilization factor | $TUF = P_{dc}/(V_s I_s)$, with $V_s$, $I_s$ the rms secondary voltage and current | 1 |
| Displacement factor | $DF = \cos\phi$, $\phi$ = angle between the input voltage and the **fundamental** of the input current | 1 |
| Harmonic factor = THD | $HF = \sqrt{I_s^2 - I_{s1}^2}\,/\,I_{s1}$ | 0 |
| Power factor | $PF = \dfrac{V_s I_{s1}}{V_s I_s}\cos\phi = \dfrac{I_{s1}}{I_s}\cos\phi$ | 1 |
| Crest factor | $CF = I_{s(peak)}/I_s$ | $\sqrt2$ for a sine |

> [!tip] Note that "efficiency" here has nothing to do with losses
> The diodes are ideal. $\eta < 1$ only says that part of the power delivered to a resistor is carried by the ripple, not by the DC component.

## 2. Single-phase rectifiers with a resistive load (slides 8–9)

$v_s = V_m \sin\omega t$, $V_m = \sqrt2 V_s$.

| | Half wave | Full wave, centre tap | Full wave, bridge |
|---|---|---|---|
| $V_{dc}$ | $V_m/\pi = 0.318 V_m$ | $2V_m/\pi = 0.6366 V_m$ | same |
| $V_{rms}$ | $V_m/2$ | $V_m/\sqrt2$ | same |
| $\eta$ | 40.5 % | 81 % | 81 % |
| FF / RF | 1.57 / 1.21 | 1.11 / 0.482 | same |
| TUF | 0.286 | 0.573 | 0.81 |
| PIV per diode | $V_m$ | $2V_m$ | $V_m$ |
| Ripple frequency | $f$ | $2f$ | $2f$ |

The bridge uses four diodes but no centre-tapped transformer, half the PIV and a better TUF: that is why it is the standard. Fourier series of the full-wave output (needed for filter design):

$$v_0(t) = \frac{2V_m}{\pi} - \frac{4V_m}{3\pi}\cos 2\omega t - \frac{4V_m}{15\pi}\cos 4\omega t - \frac{4V_m}{35\pi}\cos 6\omega t - \dots$$

Only even harmonics; the dominant one is at $2f$ with amplitude $4V_m/3\pi$.

## 3. Full wave with an RL load and a battery E (slides 10–14)

During each half cycle $L\,\dfrac{di_0}{dt} + R i_0 + E = \sqrt2 V_s \sin\omega t$, whose solution is

$$i_0 = \frac{\sqrt2 V_s}{Z}\sin(\omega t - \theta) + A_1 e^{-(R/L)t} - \frac{E}{R}, \qquad Z = \sqrt{R^2 + (\omega L)^2},\quad \theta = \tan^{-1}\frac{\omega L}{R}$$

**Case 1, continuous current.** Steady state means the current at the end of a half cycle equals the current at its start: $i_0(\omega t = \pi) = i_0(0) = I_0$. That fixes $A_1$ and gives

$$I_0 = \frac{\sqrt2 V_s}{Z}\sin\theta\;\frac{1 + e^{-(R/L)(\pi/\omega)}}{1 - e^{-(R/L)(\pi/\omega)}} - \frac{E}{R} \qquad (I_0 \ge 0)$$

Each diode carries the load current for half the period:

$$I_{D(av)} = \frac{1}{2\pi}\int_0^{\pi} i_0\, d(\omega t), \qquad I_{D(rms)} = \sqrt{\frac{1}{2\pi}\int_0^{\pi} i_0^2\, d(\omega t)}, \qquad I_{o(rms)} = \sqrt2\, I_{D(rms)}$$

**Case 2, discontinuous current.** The battery holds the diodes off until $v_s > E$: conduction starts at $\alpha = \sin^{-1}(E/V_m)$ and stops at $\beta$ where the current returns to zero. $\beta$ comes from a transcendental equation, solved by iteration (MATLAB `fzero`).

**Boundary** between the two: set $I_0 = 0$. With $x = E/V_m$ this gives a curve $x(\theta)$; above it the current is discontinuous. The slide's three points: $x = 63.67\,\%$ at $\theta = 1.5567$ rad (almost pure L), $43.65\,\%$ at $\theta = 30°$, $0$ at $\theta = 0$ (pure R: any battery at all makes the current discontinuous).

## 4. Highly inductive load (slide 15)

A large L holds the load current constant at $I_a$. Each diode pair then carries a flat $I_a$, so the **input current is a square wave** of amplitude $I_a$:

$$i_s(t) = \frac{4I_a}{\pi}\left(\sin\omega t + \tfrac13\sin 3\omega t + \tfrac15\sin 5\omega t + \dots\right)$$

$I_{s1} = \dfrac{4I_a}{\pi\sqrt2} = 0.90\,I_a$, $I_s = I_a$, so $HF = THD = \sqrt{(1/0.90)^2 - 1} = 48.3\,\%$. The fundamental is in phase with the voltage ($\phi = 0$, $DF = 1$), so $PF = I_{s1}/I_s = 0.90$ **lagging nothing, just distorted**: a power factor below 1 with zero phase shift. This is Assignment 2.2 word for word.

## 5. More phases: the q-phase star rectifier (slides 16–18)

Single-phase full wave gives $0.6366\,V_m$ and is used up to about 15 kW. Above that, more phases. With $q$ secondary phases and one diode per phase, each diode conducts for $2\pi/q$ (the phase with the highest voltage wins) and the ripple frequency becomes $q f$:

$$V_{dc} = V_m\,\frac{q}{\pi}\sin\frac{\pi}{q}, \qquad V_{rms} = V_m\sqrt{\frac{q}{2\pi}\left(\frac{\pi}{q} + \frac12\sin\frac{2\pi}{q}\right)}, \qquad I_{s} = I_m\sqrt{\frac{1}{2\pi}\left(\frac{\pi}{q} + \frac12\sin\frac{2\pi}{q}\right)}$$

($I_m = V_m/R$; $I_s$ is the rms current of one diode = one transformer secondary.) $q = 3$: $V_{dc} = 0.827 V_m$, $\eta = 96.8\,\%$, RF = 18.2 %, TUF = 0.664, PIV $= \sqrt3 V_m$. The catch: the secondary current is unidirectional, so the transformer sees DC (saturation), which is why the star circuit is rarely used as such.

## 6. The three-phase bridge (slides 19–24)

Six diodes, numbered in firing order, each conducting 120°. At any instant the pair connected to the **largest line-to-line voltage** conducts: D1-D2, D3-D2, D3-D4, D5-D4, D5-D6, D1-D6. The output follows the envelope of the line-to-line voltages, six pulses per period (ripple at $6f$). With $V_m$ the peak **phase** voltage:

$$V_{dc} = \frac{3\sqrt3}{\pi}V_m = 1.654\,V_m, \qquad V_{rms} = \sqrt{\frac32 + \frac{9\sqrt3}{4\pi}}\;V_m = 1.6554\,V_m$$

| $\eta$ | FF | RF | TUF | PIV | diode rms | secondary rms |
|---|---|---|---|---|---|---|
| 99.83 % | 1.0008 | 4 % | 0.954 | $\sqrt3 V_m$ | $0.5518\,I_m$ | $0.7804\,I_m$ |

with $I_m = \sqrt3 V_m / R$ the peak load (and diode) current. Compare the single-phase bridge (81 %, RF 48 %): this is already nearly pure DC with no filter at all.

With an RL + E load the same steady-state trick is used over one 60° pulse, $\pi/3 \le \omega t \le 2\pi/3$, with $v_{ab} = \sqrt2 V_{ab}\sin\omega t$: $i_0(\pi/3) = i_0(2\pi/3) = I_0$. Each diode now carries the current for two of the six pulses: $I_{D(av)} = \frac{2}{2\pi}\int_{\pi/3}^{2\pi/3} i_0\,d(\omega t)$, $I_{o(rms)} = \sqrt3\,I_{D(rms)}$. Boundary curve: $x = 95.49\,\%$ at $\theta = 1.5598$ rad, $95.03\,\%$ at 30°, $86.68\,\%$ at $\theta = 0$: the six-pulse output never dips below $0.866\,V_{m,LL}$, so a battery below that can never make the current discontinuous.

## 7. Design: ratings and filters (slides 26–27)

Diodes are chosen on **average current, rms current, peak current and PIV**. Filters on the DC side are L, C or LC; designing one means knowing the amplitude and frequency of the dominant harmonic (§2: $2f$, $4V_m/3\pi$ for single phase; $6f$ for the three-phase bridge).

- **L filter** (series): the inductor's impedance $n\omega L$ blocks the ripple current. For the $n$-th harmonic $I_n = V_n/\sqrt{R^2 + (n\omega L)^2}$; keep $I_{ac}/I_{dc}$ below the spec using the dominant harmonic (Problem 2.6: 5 %).
- **C filter** (parallel), single-phase bridge: the capacitor charges to $V_m$ and discharges through R between peaks. $V_{r(pp)} \approx \dfrac{V_m}{2fRC}$, $V_{dc} = V_m\left(1 - \dfrac{1}{4fRC}\right)$, $RF = \dfrac{1}{\sqrt2\,(4fRC - 1)}$. Less ripple costs short, high charging current pulses (bad crest factor and power factor).

## 8. Source inductance: commutation overlap (slides 28–29)

A real supply has inductance, so the current cannot jump from one diode to the next. For a short **overlap angle $\mu$** both diodes conduct, their anodes are shorted together and the output sits at the average of the two phase voltages: volts are lost. Assuming the current rises linearly from 0 to $I_{dc}$ in the incoming phase, each commutation costs $\Delta t\cdot v_L = L_c I_{dc}$ volt-seconds, and with the commutations of one period added up

$$V_x = 6 f L_c I_{dc} \quad \text{(three-phase bridge, equal inductances)}$$

The rectifier behaves as if it had an internal resistance $6fL_c$ that dissipates nothing: the output voltage drops in proportion to the load current.

## Assignment 2 at a glance

| | Topic | Uses |
|---|---|---|
| P 2.1 | full-wave rectifier, R load: $\eta$, FF, RF, TUF, PIV, CF, PF | §1, §2 |
| P 2.2 | Fourier series of the output with an RL load | §2 |
| **A 2.1** | bridge with L = 6.5 mH, R = 2.5 Ω, E = 10 V, 120 V, **50 Hz**: $I_0$, $I_{D(av)}$, $I_{D(rms)}$, $I_{o(rms)}$, PF, plot $i_0$ in MATLAB | §3 case 1 |
| **A 2.2** | bridge with a ripple-free motor current: HF and PF | §4 (48.3 %, 0.90) |
| P 2.3 | three-phase star: parameters; q-phase Fourier series; $q = 6$, 170 V: dominant harmonic | §5 |
| P 2.4 | three-phase bridge, R load, 60 A at 280.7 V | §6 |
| **A 2.3** | three-phase bridge with L = 1.5 mH, R = 2.5 Ω, E = 10 V, 208 V line-line | §6 |
| P 2.5 | diode ratings for a three-phase bridge, 60 A ripple-free, 120 V phase | §6, §7 |
| P 2.6 | series L so that $I_{ac} < 5\,\%$ of $I_{dc}$, 220 V, R = 500 Ω | §7 |

> [!warning] A 2.1 is Rashid's example 3.4 moved from 60 Hz to 50 Hz
> The book's answers (32.8 A, 19.61 A, 28.5 A, 40.3 A) are for 60 Hz and will **not** match. At 50 Hz: $Z = 3.23\ \Omega$, $\theta = 39.2°$, and a quick numerical check gives $I_0 \approx 30.7$ A with the current continuous (minimum about 22.9 A). Work it through yourself before comparing.

## Questions to settle in the lecture

- Which results does Ashraf expect **derived** and which just **used** (the $I_0$ expression, the boundary curves)?
- Is the MATLAB part of the assignment meant as a script (evaluate the formula) or a Simscape model? The diode parameters IS and BV in the text come from the book's PSpice version.
- Deadline and hand-in form of Assignment 2, and whether it is done in the groups.
