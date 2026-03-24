---
type: concept
aliases: [Frequency Response Plot, Magnitude Plot, Phase Plot]
tags:
  - concept
  - frequency-domain
  - control-theory
  - visualization
courses: [34722, 34655, 34620, 62743]
---
# Bode Plot

## Definition

A Bode plot is a pair of logarithmic graphs that display the magnitude (in dB) and phase (in degrees) of a transfer function as a function of frequency. Magnitude is plotted on a logarithmic scale with frequency on the x-axis, while phase is plotted below it on the same frequency axis. Bode plots provide intuitive insight into system frequency response, stability margins, bandwidth, and are fundamental tools for control system design, filter analysis, and amplifier characterization.

---

## Key Equations

**Magnitude in decibels:**
$$|H(j\omega)|_{dB} = 20 \log_{10}|H(j\omega)|$$

**Phase of transfer function:**
$$\angle H(j\omega) = \arg(H(j\omega))$$

**Phase margin (degrees):**
$$\text{PM} = 180° - \angle H(j\omega)|_{\omega = \omega_{gc}}$$

**Gain margin (dB):**
$$\text{GM} = -|H(j\omega)|_{dB}|_{\omega = \omega_{pc}}$$

**Bandwidth (−3 dB point for first-order system):**
$$\omega_{-3dB} = \sqrt{2} \cdot \omega_0 \text{ for } H(s) = \frac{\omega_0}{s + \omega_0}$$

---

## Where It Appears

- [[34722 Linear Control Design 1|LCD]] — Primary tool for analyzing frequency response; used extensively in PID tuning, margin analysis, and system stability assessment
- [[34655 Integrated Analog Electronics 2|IAE2]] — Characterizing amplifier bandwidth, gain peaking, phase margin for stability; designing compensation networks
- [[34620 Basic Power Electronics|PE]] — Loop gain analysis, control-to-output response, and closed-loop bandwidth verification of regulators
- [[62743 Digital Signal Processing (Reexam)|DSP (Archive)]] — Filter design and verification using magnitude and phase response
- Electromagnetics (Archive) — Transmission line and antenna frequency response analysis

---

## Related Concepts

- [[Transfer Function]] — The underlying system representation that Bode plot visualizes
- [[Feedback]] — Bode plots reveal stability margins and closed-loop performance in feedback systems
- [[Frequency Response]] — Direct representation; Bode plot is the standard way to display frequency response
- [[MOSFET]] — Intrinsic Bode plot from parasitic capacitances and transconductance
