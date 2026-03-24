---
type: concept
aliases: [Negative Feedback, Closed-Loop, Feedback Control, Loop Gain]
tags:
  - concept
  - control-theory
  - stability
  - design-technique
courses: [34722, 34655, 34620]
---
# Feedback

## Definition

Feedback is a mechanism in which the output of a system is sampled and compared to a reference input, with the error signal used to adjust the system's behavior. In negative feedback, the error reduces the input, driving the system toward the desired setpoint. Negative feedback fundamentally improves system stability, reduces sensitivity to disturbances and parameter variations, and enables precise control. It is a unifying principle across control systems (PID regulators), analog circuits (opamp amplifiers, current mirrors), and power electronics (voltage regulators).

---

## Key Equations

**Closed-loop transfer function (unity feedback):**
$$T(s) = \frac{G(s)}{1 + G(s)H(s)} = \frac{G(s)}{1 + L(s)}$$

**Loop gain:**
$$L(s) = G(s)H(s)$$

**Error signal:**
$$E(s) = R(s) - Y(s) = \frac{R(s)}{1 + L(s)}$$

**Sensitivity (effect of plant variation on closed-loop transfer function):**
$$S(s) = \frac{1}{1 + L(s)}$$

**Closed-loop input impedance (opamp inverting amplifier):**
$$Z_{in,CL} = -\frac{Z_1}{A}$$

**Stability criterion (Nyquist, simplified for minimum-phase systems):**
$$\text{PM} > 0° \text{ and } \text{GM} > 0 \text{ dB at loop gain crossover}$$

---

## Where It Appears

- [[34722 Linear Control Design 1|LCD]] — Core foundation: feedback control systems, PID design, closed-loop transfer functions, stability analysis, error reduction, disturbance rejection
- [[34655 Integrated Analog Electronics 2|IAE2]] — Negative feedback in opamp circuits for linearization, bandwidth extension, input/output impedance control; stability compensation networks
- [[34620 Basic Power Electronics|PE]] — Voltage/current feedback in DC-DC converters for regulation; load-line control; closed-loop bandwidth and transient response
- [[34315 Internet of Things|IoT]] — Embedded feedback control systems for sensors and actuators

---

## Related Concepts

- [[Transfer Function]] — Feedback modifies the transfer function from open-loop G(s) to closed-loop T(s)
- [[Bode Plot]] — Loop gain L(s) plotted to verify gain and phase margins
- [[Frequency Response]] — Feedback flattens and extends frequency response of circuits and systems
- [[MOSFET]] — Feedback biasing in differential pairs and current mirrors for linearization
- [[Noise Analysis]] — Feedback reduces integrated noise proportional to 1/(1+L) within feedback bandwidth
