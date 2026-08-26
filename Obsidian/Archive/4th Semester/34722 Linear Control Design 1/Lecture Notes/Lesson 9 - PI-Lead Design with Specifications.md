---
course: "34722"
course-name: "Linear Control Design 1"
type: lecture-note
lesson: 9
tags: [LCD, lecture, notes]
date: 2026-04-08
---

# Lesson 9 - PI-Lead Design with Specifications

> [!abstract] Lecture Overview
> Lesson 9/13 — Teachers: Silvia Tolu & Dimitrios Papageorgiou
> Topics: Closed-loop time-domain specifications, bandwidth, control design based on specifications, type-n systems, P-Lead forward vs. feedback placement.
> Schedule: 13:00–15:00 Lecture, 15:00–17:00 Exercises.

> [!example] Related Materials
> - Slides: [[Lecture_09_PI_LEAD_design_specifications.pdf]]
> - MATLAB: `Example_first_order_specifications_control.m`, `Example_second_order_specifications_control.m`, `Bandwidth_bode_sine.m`, `stable_spring_simulator.m`
> - Exercises: [[Theoretical Exercises LCD1.pdf]] — problems 1, 2, 4, 5, 6, 7, 9
> - Previous: [[Lesson 8 - Position Controller Design (180330)]]

---

## Learning Objectives

- Transform closed-loop specifications into open-loop specifications for design
- Decide which controller parts are needed for a given system
- Design feedback controllers based on closed-loop system specifications
- Interpret Bode plots for control design

---

## 1. Closed-Loop Specifications

Consider the step response of a closed-loop system to a step input of size $h_0$. The following **time-domain specifications** characterize the response:

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=3]]

### 1.1 Time-Domain Metrics

**Rise time ($t_r$):** Time for the output to go from 10% to 90% of its final value. Measures how quickly the system responds.

**Settling time ($t_s$):** Time until the output remains within $\pm 2\%$ of the final value. Measures how quickly oscillations die out.

**Peak time ($t_p$):** Time until the output reaches its maximum value.

**Overshoot ($M_p$):** Difference between the maximum and steady-state value, expressed as a percentage:
$$M_p = \frac{y_{\max} - y_{ss}}{y_{ss}}$$

**Stationary (steady-state) error ($e_{ss}$):** Difference between the step reference and the steady-state output:
$$e_{ss} = |h_0 - y_{ss}| \quad \text{or} \quad e_{ss} = \left|\frac{h_0 - y_{ss}}{y_{ss}}\right| \cdot 100\%$$

**Undershoot:** Minimum value minus initial value (relevant for non-minimum-phase systems).

### 1.2 From Closed-Loop to Open-Loop Specifications

Closed-loop specifications are **intuitive** and how industry describes requirements. However, we need **open-loop specifications** for the actual controller design:

| Closed-loop specs | Open-loop specs |
|---|---|
| Rise time ($t_r$) | Phase margin ($\gamma_M$) |
| Settling time ($t_s$) | Gain margin ($K_M$) |
| Peak time ($t_p$) | Controller type (P, PI, PI-Lead...) |
| Overshoot ($M_p$) | Controller gains ($K_P$) |
| Steady-state error ($e_{ss}$) | Crossover frequency ($\omega_c$) |

The design flow is: System requirements $\to$ Closed-loop specs $\to$ Open-loop specs $\to$ Controller design $\to$ Implementation $\to$ Performance assessment.

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=5]]

---

## 2. Bandwidth

### 2.1 Definition

**Bandwidth ($\omega_{BW}$):** The frequency at which the closed-loop magnitude drops by 3 dB compared to the low-frequency horizontal asymptote:

$$|G_{cl}(j\omega_{BW})| = \frac{\sqrt{2}}{2} |G_{cl}(0)|$$

This represents the highest frequency up to which the system can substantially follow the input. Beyond $\omega_{BW}$, the output amplitude is significantly attenuated.

### 2.2 Properties

- **Higher bandwidth** $\to$ the system can respond to faster inputs (more aggressive control)
- Bandwidth is a property of the **closed-loop** system
- Only meaningful for stable closed-loop systems with finite low-frequency amplitude

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=7]]

### 2.3 Multiple Crossings

When the Bode plot has multiple 0 dB or $-3$ dB crossings:
- For $\omega_c$: choose the one giving the **smallest phase margin** (typically the largest $\omega_c$)
- For $\omega_{BW}$: choose the one giving the **slowest system** (the smallest $\omega_{BW}$)

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=9]]

---

## 3. Control Design Based on Specifications

### 3.1 Ideal Closed-Loop Behaviour

Ideally, a closed-loop system should behave like a 1st or 2nd order lowpass filter with:
- Unit static gain
- Low (or no) overshoot
- Short rise time and settling time
- Large bandwidth

### 3.2 First-Order Lowpass Filter Target

If we want the closed-loop to behave as a 1st order lowpass filter with time constant $\tau$:

$$G(s) = \frac{1}{\tau s + 1} \quad \Longrightarrow \quad G_{ol}(s) = \frac{1}{\tau s}$$

The relationships are simple:

| Specification | Formula |
|---|---|
| Crossover frequency | $\omega_c = \frac{1}{\tau}$ |
| Bandwidth | $\omega_{BW} = \frac{1}{\tau}$ |
| Rise time | $t_r \cong 2.2\tau$ |
| Settling time | $t_s \cong 4\tau$ |
| Phase margin | Always $90°$ |

> [!tip] Key Insight
> For a 1st order target: $\omega_c = \omega_{BW} = 1/\tau$, and the phase margin is always 90°. This is the simplest design target — no overshoot by definition.

### 3.3 Second-Order Lowpass Filter Target

More realistically, we target a 2nd order lowpass filter:
$$G_{cl}(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

The corresponding open-loop transfer function is:
$$G_{ol}(s) = \frac{\omega_n^2}{s(s + 2\zeta\omega_n)}$$

| Specification | Formula |
|---|---|
| Rise time | $t_r \approx \frac{1.8}{\omega_n}$ |
| Settling time | $t_s \approx \frac{4}{\zeta\omega_n}$ |
| Peak time | $t_p = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}}$ |
| Overshoot | $M_p = e^{\frac{-\pi\zeta}{\sqrt{1-\zeta^2}}}$ |
| Bandwidth | $\omega_{BW} = \omega_n\sqrt{\sqrt{2 - 4\zeta + 4\zeta^4} + 1 - 2\zeta^2}$ |
| Crossover frequency | $\omega_c = \omega_n\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}$ |
| Phase margin | $\gamma_M = \arctan\left(\frac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4} - 2\zeta^2}}\right)$ |

Once we have $\omega_n$ and $\zeta$ from the time-domain specs, we can derive all the open-loop specifications needed for design.

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=18]]

---

## 4. Design Examples

### 4.1 First-Order Target Example

**Plant:** $G(s) = \frac{7.603}{s^2 + 11.35s + 25.59}$

**Specification:** $t_r \cong 0.11$ s, no overshoot, zero steady-state error.

**Analysis:**
- No overshoot + zero $e_{ss}$ $\to$ target a 1st order lowpass filter with $\tau = t_r/2.2 = 0.05$ s
- Required crossover frequency: $\omega_c = 1/\tau = 2.2/0.11 = 20$ rad/s
- Zero $e_{ss}$ $\to$ need an I-part (PI controller)
- Phase margin is always 90° for 1st order target $\to$ also need Lead

**Design ($N_I = 3$):**
- $\tau_i = N_I/\omega_c = 3/20 = 0.15$
- Phase balance: $-\pi + \frac{\pi}{2} = \angle G(20j) - \arctan(1/3) + \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$
- Solving: $\alpha = 0.013$, $\tau_d = \frac{1}{\omega_c\sqrt{\alpha}} = 0.44$
- Gain: $K_P = \frac{1}{|C_{PI}(s)C_D(s)G(s)|_{s=j\omega_c}} = 6.24$

**Result:** Rise time = 0.138 s, settling time = 0.603 s, overshoot = 0%, bandwidth = 20.04 rad/s.

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=14]]

### 4.2 Second-Order Target Example

**Plant:** $G(s) = \frac{0.1(s+2)(s+100)}{(s+0.1)(s^2+11.35s+25.59)}$

**Specification:** $t_s \cong 0.4$ s, $M_p \leq 20\%$, zero steady-state error.

**Analysis:**
- $M_p = 0.2$ $\Rightarrow$ $\zeta = 0.456$ $\Rightarrow$ $\gamma_M = 48.14°$
- $t_s = 0.4$ $\Rightarrow$ $\omega_n = 4/(\zeta \cdot t_s) = 21.9$ $\Rightarrow$ $\omega_c = 17.9$ rad/s

**Design ($N_I = 3$):**
- $\tau_i = 3/\omega_c = 0.1675$
- Phase balance: $-\pi + \gamma_M = \angle G(17.9j) - \arctan(1/3) + \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$
- Solving: $\alpha = 0.36$, $\tau_d = 0.092$, $K_P = 20.1$

**Result:** Rise time = 0.115 s, settling time = 0.403 s, overshoot = 9.88%, bandwidth = 18.56 rad/s (feedback config).

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=17]]

---

## 5. Type-n Systems and Steady-State Error

### 5.1 System Type Definition

A system is called **type-$n$** if it has $n$ integrators (poles at the origin) and no zeros at the origin:
$$G(s) = \frac{1}{s^n} G_0(s) \qquad \text{where } G_0(0) \text{ is finite}$$

### 5.2 Steady-State Error with P Controller

With a P controller ($K_P$) and unit feedback, the error transfer function is:
$$G_e(s) = \frac{1}{1 + K_P G(s)} = \frac{s^n}{s^n + K_P G_0(s)}$$

**For a unit step input:**

| System type | $e_{ss}$ |
|---|---|
| Type-0 ($n = 0$) | $\frac{1}{1 + K_P G_0(0)}$ |
| Type-1 ($n \geq 1$) | $0$ |

**For a unit ramp input:**

| System type | $e_{ss}$ |
|---|---|
| Type-0 ($n = 0$) | $\infty$ |
| Type-1 ($n = 1$) | $\frac{1}{K_P G_0(0)}$ |
| Type-2 ($n \geq 2$) | $0$ |

> [!important] Key Rule
> To achieve zero $e_{ss}$ for a step input, we need **at least one integrator** in the open loop. If the plant doesn't have one, add a **PI controller**. For zero $e_{ss}$ to a ramp, we need at least two integrators.

### 5.3 Handling Zeros at the Origin

If the system has $n$ zeros at the origin (and no integrators), with P controller:
$$G_e(s) = \frac{1}{1 + K_P G(s)} = \frac{1}{1 + s^n K_P G_0(s)}$$

For a unit step input, $e_{ss} = 1$ when $n \geq 1$. We need $n+1$ PI parts (integrators) in the open loop to achieve zero steady-state error.

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=19]]

---

## 6. Quick Assessment from Bode Plots

When looking at an open-loop Bode plot, quickly determine the controller needs:

**$G_2(s) = \frac{0.13}{(0.01s^2 + 0.03s + 1)(0.05s + 1)}$ (type-0):**
- Flat low-frequency gain $\to$ needs PI for zero $e_{ss}$
- Steep phase drop near $\omega_\pi$ $\to$ need aggressive (small $\alpha$) Lead
- Be careful with multiple crossover frequencies

**$G_3(s) = \frac{0.13}{0.01s^3 + 0.1s^2 + s}$ (type-1):**
- Large low-frequency gain $\to$ no PI needed
- Mild phase drop near $\omega_\pi$ $\to$ moderate Lead is sufficient

**$G_4(s) = \frac{10}{0.17s^3 + s^2}$ (type-2):**
- No I-part needed (already has two integrators)
- P-Lead controller will stabilize the system by adding phase around $\omega_c$

**$G_5(s) = \frac{0.13}{(0.01s^2 + 0.01s + 1)(s + 1)}$:**
- Do NOT place $\omega_c$ at the resonance peak — too steep phase drop at $\omega_\pi$

**$G_6(s) = \frac{1}{s+1}$:**
- Phase never reaches $-180°$ $\to$ no PI or Lead needed
- Can arbitrarily increase $K_P$ (infinite gain margin)

![[Lecture_09_PI_LEAD_design_specifications.pdf#page=22]]

---

## 7. P-Lead in Forward vs. P-Lead in Feedback

Two common architectures for placing the Lead part $C_D(s)$:

1. **Forward path:** $R(s) \to C_D(s) \to C_{PI}(s) \to [\oplus d(s)] \to G(s) \to y(s)$
2. **Feedback path:** $R(s) \to C_{PI}(s) \to [\oplus d(s)] \to G(s) \to y(s)$, with $C_D(s)$ in the feedback branch

### 7.1 What Changes and What Doesn't

| Question | Answer |
|---|---|
| Does $C_D(s)$ location affect open-loop calculations? | **No.** $C_{ol}(s) = C_D(s) C_{PI}(s) G(s)$ in both cases. |
| Does it affect closed-loop performance? | **Yes.** Bandwidth drops if $C_D(s)$ is in feedback. |
| Does it affect disturbance rejection? | **No.** $G_{y,d}(s) = \frac{G(s)}{1 + C_D(s)C_{PI}(s)G(s)}$ in both cases. |
| Does it affect the control signal $u(s)$? | **Yes.** Forward: $G_{u,r} = \frac{C_D C_{PI}}{1 + C_D C_{PI} G}$. Feedback: $G_{u,r} = \frac{C_{PI}}{1 + C_D C_{PI} G}$. |

> [!tip] Why Use Feedback Placement?
> The Lead part in the forward path amplifies high-frequency content in the reference signal, producing large control signals $u(s)$ for fast-changing references. Placing $C_D(s)$ in the feedback path avoids this — the control effort is smaller, at the cost of reduced bandwidth.

---

## 8. Extra Considerations

- If a controller part is not needed, **omit it** from the phase balance equation. For example: $-180° + \gamma_M = \phi_G + \phi_m$ (no PI) or $-180° + \gamma_M = \phi_G + \phi_i$ (no Lead).

- For type-0 systems with no PI, smaller static error requires higher gain, which implies lower phase margin. There is an inherent trade-off.

- When the required Lead contribution exceeds 90°, use **multiple Lead terms** in cascade:
$$\phi_m = \phi_{m,1} + \phi_{m,2}$$
$$C_D(s) = C_{D,1}(s) \cdot C_{D,2}(s)$$
  Each term is designed independently with its own $\alpha$ and $\tau_D$.

---

## 9. Comprehension Questions

- **Does a lower crossover frequency give a lower bandwidth?** In general, yes. $\omega_c \propto \omega_{BW}$.
- **Does a lower bandwidth give a longer settling time?** In general, yes. $t_s \cong 4/(\zeta\omega_n)$, $\omega_n \propto \omega_{BW}$.
- **Does a shorter settling time give a stronger control signal?** In general, yes. Large bandwidth $\to$ large $\omega_c$ $\to$ high $K_P$ gain.
- **Does a closed-loop Bode plot always start at 0 dB?** Not necessarily — when there is non-zero static error, it doesn't start from 0 dB.
- **Is the closed-loop bandwidth the same as the open-loop crossover frequency?** No, although they are usually close.

---

## Key Takeaways

1. **Closed-loop specifications** (rise time, settling time, overshoot, steady-state error) are intuitive but must be **translated to open-loop specifications** (phase margin, crossover frequency, controller type) for design.

2. **Bandwidth** is the $-3$ dB frequency of the closed-loop system. It determines how fast the system can track inputs. Higher bandwidth = faster response = more aggressive control.

3. **1st order target** ($\tau$) gives simple formulas: $\omega_c = 1/\tau$, $t_r = 2.2\tau$, $t_s = 4\tau$, $\gamma_M = 90°$, zero overshoot.

4. **2nd order target** ($\omega_n$, $\zeta$) is more realistic and allows trading off overshoot for speed via $\zeta$.

5. **Type-$n$ systems** have $n$ integrators. To get zero $e_{ss}$ for step inputs, need at least one integrator in the open loop (add PI if the plant has none).

6. **Lead placement** in forward vs. feedback affects bandwidth and control effort but not the open-loop analysis or disturbance rejection.

7. When Lead contribution needs to exceed 90°, use **multiple cascaded Lead terms**.

---

## Key Formulas

> [!abstract] Quick Reference
> | Concept | 1st Order Target | 2nd Order Target |
> |---------|-----------------|------------------|
> | Rise time | $t_r \cong 2.2\tau$ | $t_r \approx 1.8/\omega_n$ |
> | Settling time | $t_s \cong 4\tau$ | $t_s \approx 4/(\zeta\omega_n)$ |
> | Peak time | — | $t_p = \pi/(\omega_n\sqrt{1-\zeta^2})$ |
> | Overshoot | — | $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ |
> | Bandwidth | $\omega_{BW} = 1/\tau$ | $\omega_{BW} = \omega_n\sqrt{\sqrt{2-4\zeta+4\zeta^4}+1-2\zeta^2}$ |
> | Phase margin | $\gamma_M = 90°$ | $\gamma_M = \arctan\left(\frac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}}\right)$ |
> | Crossover freq. | $\omega_c = 1/\tau$ | $\omega_c = \omega_n\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}$ |

---

> [!nav]
> [[Lesson 8 - Position Controller Design (180330)|← Lesson 8]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
