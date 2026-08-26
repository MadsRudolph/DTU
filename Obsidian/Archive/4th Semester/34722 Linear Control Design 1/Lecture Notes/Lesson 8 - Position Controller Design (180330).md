---
course: "34722"
course-name: "Linear Control Design 1"
type: lecture-note
lesson: 8
tags: [LCD, lecture, notes]
date: 2026-03-25
---

# Lesson 8 - Position Controller Design

## Introduction [00:32]

Welcome to the eighth lecture of Linear Control Design 1. This is arguably the most important lecture of the class as we will be doing systematic control design and laying the foundations for designs that will be revisited for the entire rest of the course.

Today we will discuss **PI-Lead design**, which is a variation of the PID design mentioned in the first lecture. We'll understand why we replace the differential part with what's called a "lead part" - a variation and modification of the differential part of the PID controller.

## Learning Objectives

- Design proportional, integral, and lead controllers for given systems with known transfer functions
- Evaluate designs against specifications
- Understand control-theoretic specifications (phase margin) vs. engineering specifications (speed, accuracy, overshoot)

## Fundamental Control Block Diagram [04:18]

Our benchmark block diagram consists of:
- System transfer function $G(s)$ (open-loop stable)
- Feedback from output compared to reference
- Error signal passed through controller $K(s)$
- Three controller variations: P, PI, and PI-Lead

### Transfer Function Relationships

**Loop Transfer Function:**
$$G_{OL}(s) = K(s) \cdot G(s)$$

**Closed-Loop Transfer Function:**
$$T(s) = \frac{K(s)G(s)}{1 + K(s)G(s)}$$

**Error Transfer Function:**
$$E(s) = \frac{1}{1 + K(s)G(s)}$$

> Note: All closed-loop transfer functions from the same system have identical denominators, ensuring consistent stability properties regardless of which input-output pair is examined.

## Proportional (P) Controller Design [12:51]

### Basic P Controller
$$K(s) = K_p$$

### Bode Plot Effects
- Multiplying by gain $K_p$ shifts magnitude plot upward by $20\log_{10}(K_p)$ dB
- Phase remains unchanged
- Higher gains → higher crossover frequency → reduced phase margin

### Steady-State Error [19:48]

Using the **Final Value Theorem:**
$$e_{ss} = \lim_{t \to \infty} e(t) = \lim_{s \to 0} s \cdot G_e(s) \cdot \frac{1}{s}$$

For P controller:
$$e_{ss} = \frac{1}{1 + K_p G(0)}$$

**Key Insight:** For stable systems, P controllers alone cannot achieve zero steady-state error without infinite gain.

### Phase Margin Design Method [30:28]

**Phase Balance Equation:**
$$-180° + \phi_m = \phi_G(\omega_c)$$

Where:
- $\phi_m$ = desired phase margin
- $\omega_c$ = new crossover frequency
- $\phi_G(\omega_c)$ = plant phase at crossover frequency

**Design Steps:**
1. Calculate required plant phase: $\phi_G(\omega_c) = -180° + \phi_m$
2. Find frequency where plant has this phase from Bode plot
3. Measure magnitude deficit at this frequency
4. Set $K_p$ to compensate: $K_p = 10^{|\text{deficit in dB}|/20}$

### Example: Third-Order System [29:12]
For phase margin of 60°:
- Required plant phase: $-120°$
- From Bode plot: $\omega_c = 0.556$ rad/s
- Magnitude at $\omega_c$: $9.1$ dB
- Therefore: $K_p = 10^{-9.1/20} = 0.35$

## Proportional-Integral (PI) Controller Design [63:44]

### Motivation for Integration
- P controllers leave steady-state error for stable systems
- Pure integrator $\frac{1}{s}$ provides infinite gain at $\omega = 0$
- But introduces permanent $-90°$ phase penalty

### PI Controller Structure
$$K_{PI}(s) = \frac{\tau_I s + 1}{\tau_I s}$$

Where $\tau_I$ is the integral time constant.

**Bode Plot Characteristics:**
- Zero at $\omega = \frac{1}{\tau_I}$
- Pole at origin
- Provides infinite gain at $\omega = 0$ (eliminates steady-state error)
- Phase penalty recovers after zero frequency

### Design Parameter: $N_I$ [81:33]

$$N_I = \frac{\omega_c}{\omega_I} = \omega_c \tau_I$$

Where $\omega_I = \frac{1}{\tau_I}$ is the zero frequency.

**PI Phase Contribution at Crossover:**
$$\phi_{PI} = -\arctan\left(\frac{1}{N_I}\right)$$

### Modified Phase Balance Equation
$$-180° + \phi_m = \phi_G(\omega_c) + \phi_{PI}(\omega_c)$$

**Design Steps:**
1. Choose $N_I$ (typically 3-5)
2. Calculate PI contribution: $\phi_{PI} = -\arctan(1/N_I)$
3. Find required plant phase: $\phi_G(\omega_c) = -180° + \phi_m - \phi_{PI}$
4. Locate $\omega_c$ from plant Bode plot
5. Calculate $\tau_I = N_I/\omega_c$
6. Adjust with $K_p$ for unity crossover

### Example: PI Design [90:32]
System: $G(s) = \frac{40}{s(s+10)^2}$

For $\phi_m = 60°$, $N_I = 3$:
- $\phi_{PI} = -\arctan(1/3) \approx -18.4°$
- Required plant phase: $-120° - (-18.4°) = -101.6°$
- From Bode plot: $\omega_c = 2.68$ rad/s
- $\tau_I = 3/2.68 = 1.12$ s
- Final adjustment: $K_p = 7.21$

## Lead Controller Design [99:44]

### Motivation for Lead Compensation
- PI controller introduces phase penalty at crossover frequency
- Need positive phase contribution to improve phase margin
- Lead controller provides localized phase boost

### Lead Controller Structure
$$K_{\text{lead}}(s) = \frac{\tau_D s + 1}{\alpha \tau_D s + 1}$$

Where $0 < \alpha < 1$.

**Characteristics:**
- Zero at $\omega = \frac{1}{\tau_D}$
- Pole at $\omega = \frac{1}{\alpha \tau_D}$ (higher frequency)
- Provides phase boost between zero and pole
- Maximum phase boost at $\omega_m = \frac{1}{\tau_D\sqrt{\alpha}}$

### Lead Phase Contribution [113:05]
$$\phi_{\text{lead}} = \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$$

### Complete PI-Lead Design

**Full Phase Balance Equation:**
$$-180° + \phi_m = \phi_G(\omega_c) + \phi_{PI}(\omega_c) + \phi_{\text{lead}}(\omega_c)$$

**Design Steps:**
1. Choose $N_I$ and $\alpha$
2. Calculate PI and lead contributions
3. Find required plant phase
4. Locate $\omega_c$ from plant Bode plot
5. Calculate time constants:
   - $\tau_I = N_I/\omega_c$
   - $\tau_D = 1/(\omega_c\sqrt{\alpha})$
6. Adjust with $K_p$

### Example: Complete PI-Lead Design [116:33]

For $\phi_m = 60°$, $N_I = 3$, $\alpha = 0.3$:
- $\phi_{PI} = -18.4°$
- $\phi_{\text{lead}} = +32.2°$
- Net controller contribution: $+13.8°$
- Required plant phase: $-133.8°$

Results in well-damped response with zero steady-state error.

## Design Guidelines [122:04]

### Recommended Starting Values
| Parameter | Typical Range | Starting Value |
|-----------|---------------|----------------|
| Phase Margin | 45° - 75° | 60° |
| $N_I$ | 2 - 10 | 3 |
| $\alpha$ | 0.01 - 0.1 | 0.05 |

### Design Process Summary
1. **Specify** desired phase margin
2. **Select** design parameters ($N_I$, $\alpha$)
3. **Calculate** controller contributions
4. **Apply** phase balance equation
5. **Find** crossover frequency from plant Bode plot
6. **Compute** controller parameters
7. **Adjust** proportional gain
8. **Evaluate** and iterate if necessary

## Key Takeaways

- **P controllers** provide basic control but cannot eliminate steady-state error in stable systems
- **PI controllers** eliminate steady-state error but introduce phase penalties
- **Lead controllers** provide phase boost to improve stability margins
- **Phase balance equation** is fundamental to all frequency-domain designs
- **Systematic design process** allows predictable performance while maintaining stability
- **Parameter selection** requires engineering judgment and iteration
- **Bode plot analysis** is essential for understanding frequency-domain behavior

The methods presented today form the foundation for all subsequent controller designs in this course. Master these techniques through practice with the provided examples.

---

← [[34722 Linear Control Design 1|34722 Home]]