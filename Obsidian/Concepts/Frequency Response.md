---
type: concept
aliases: [Bandwidth, -3dB Frequency, Cutoff Frequency, AC Response]
tags:
  - concept
  - frequency-domain
  - signal-processing
  - design
courses: [34722, 34655, 34620, 62743]
---
# Frequency Response

## Definition

Frequency response describes how a system's output amplitude and phase vary as the input frequency changes. It is obtained by evaluating the transfer function H(s) or H(z) at frequency points H(jω) and plotting magnitude and phase versus frequency. Frequency response reveals system bandwidth (passband and stopband), resonances, rolloff rates, and stability margins. It is the practical bridge between transfer function theory and real-world system behavior, directly measurable by swept-sine testing and visualized via Bode plots or Nyquist diagrams.

---

## Key Equations

**Magnitude response from transfer function:**
$$|H(j\omega)| = \frac{|N(j\omega)|}{|D(j\omega)|}$$

**Phase response:**
$$\angle H(j\omega) = \angle N(j\omega) - \angle D(j\omega)$$

**Bandwidth (-3 dB point, power drops to half):**
$$|H(j\omega_{-3dB})|^2 = \frac{1}{2}|H(0)|^2 \quad \Rightarrow \quad |H(j\omega_{-3dB})| = \frac{|H(0)|}{\sqrt{2}}$$

**Group delay (phase vs. frequency slope):**
$$\tau_g(\omega) = -\frac{d\angle H(j\omega)}{d\omega}$$

**Quality factor (resonance sharpness):**
$$Q = \frac{\omega_0}{\Delta\omega_{3dB}} = \frac{\omega_0}{2\zeta\omega_0} = \frac{1}{2\zeta}$$

**Gain-Bandwidth Product (GBW, opamp figure of merit):**
$$\text{GBW} = A_0 \cdot f_{-3dB} = \text{constant (for dominant-pole compensation)}$$

---

## Where It Appears

- [[34722 Linear Control Design 1|LCD]] — Primary analysis tool: Bode plots, Nyquist plots, phase/gain margins; feedback bandwidth design; control system frequency-domain specifications
- [[34655 Integrated Analog Electronics 2|IAE2]] — Amplifier bandwidth, GBW product, bandwidth extension via feedback, peaking from parasitic poles, compensation network design
- [[34620 Basic Power Electronics|PE]] — Control-to-output bandwidth, output impedance vs. frequency, load-transient response, switching harmonics filtering
- [[62743 Digital Signal Processing (Reexam)|DSP (Archive)]] — Digital filter design (FIR, IIR), passband/stopband ripple, filter order selection via frequency response
- [[34315 Internet of Things|IoT]] — Channel frequency response, link budget analysis, wireless protocol frequency selectivity

---

## Related Concepts

- [[Transfer Function]] — Frequency response is the transfer function evaluated at s = jω (or z = e^{jωT} for discrete systems)
- [[Bode Plot]] — Standard graphical representation of magnitude and phase frequency response on logarithmic scales
- [[Feedback]] — Feedback extends (or reduces) closed-loop bandwidth while maintaining stability; trades speed vs. stability
- [[Fourier Transform]] — Frequency response is the Fourier Transform of system impulse response h(t)
- [[MOSFET]] — Parasitic capacitances (Cgs, Cgd, Cdb) determine MOSFET intrinsic frequency response and fT (transit frequency)
- [[Noise Analysis]] — Noise is spectrally shaped by system frequency response; in-band noise integrated over bandwidth determines SNR
