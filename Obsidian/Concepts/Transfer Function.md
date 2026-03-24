---
type: concept
aliases: [System Transfer Function, H(s), H(z)]
tags:
  - concept
  - frequency-domain
  - control-theory
courses: [34722, 62743, 34655, 34620]
---
# Transfer Function

## Definition

A transfer function is a mathematical representation of the input-output relationship of a linear, time-invariant (LTI) system in the frequency domain. It describes how a system responds to different frequencies and is the ratio of the Laplace transform of the output to the Laplace transform of the input, assuming zero initial conditions. Transfer functions form the foundation of control system analysis and are essential for understanding system behavior, stability, and performance.

---

## Key Equations

**Laplace-domain transfer function:**
$$H(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + b_{m-1}s^{m-1} + \cdots + b_0}{a_n s^n + a_{n-1}s^{n-1} + \cdots + a_0}$$

**General form (pole-zero representation):**
$$H(s) = K \frac{(s - z_1)(s - z_2)\cdots(s - z_m)}{(s - p_1)(s - p_2)\cdots(s - p_n)}$$

**z-domain transfer function (discrete-time):**
$$H(z) = \frac{Y(z)}{U(z)} = \frac{b_0 + b_1 z^{-1} + \cdots + b_m z^{-m}}{1 + a_1 z^{-1} + \cdots + a_n z^{-n}}$$

**First-order system (RC circuit example):**
$$H(s) = \frac{\omega_0}{s + \omega_0}$$

**Second-order system:**
$$H(s) = \frac{\omega_n^2}{s^2 + 2\zeta \omega_n s + \omega_n^2}$$

---

## Where It Appears

- [[34722 Linear Control Design 1|LCD]] — Core foundation for all control system analysis; used to derive frequency response and design feedback controllers
- [[62743 Digital Signal Processing (Reexam)|DSP (Archive)]] — z-domain transfer functions for discrete filters and digital system analysis
- [[34655 Integrated Analog Electronics 2|IAE2]] — Transfer functions of amplifier stages, opamp circuits, and frequency-dependent network analysis
- [[34620 Basic Power Electronics|PE]] — DC-DC converter transfer functions, control-to-output relationships, and stability analysis
- [[62711 Digital Systems Design|DSD]] — System-level behavioral modeling and digital signal flow

---

## Related Concepts

- [[Bode Plot]] — Graphical representation of transfer function magnitude and phase vs. frequency
- [[Frequency Response]] — How the transfer function varies with input frequency
- [[Fourier Transform]] — Foundation for converting time-domain signals to frequency domain
- [[Feedback]] — Transfer functions in closed-loop systems and closed-loop stability
- [[Noise Analysis]] — Noise transfer functions and signal-to-noise ratio in cascaded systems
