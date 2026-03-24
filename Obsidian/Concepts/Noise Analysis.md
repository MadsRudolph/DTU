---
type: concept
aliases: [Noise Figure, SNR, Signal-to-Noise Ratio, Thermal Noise, Flicker Noise]
tags:
  - concept
  - analog
  - signal-integrity
  - measurement
courses: [34655, 34620, 34315]
---
# Noise Analysis

## Definition

Noise analysis characterizes unwanted random variations superimposed on signals. Sources include thermal noise (Johnson noise from resistances), flicker noise (1/f noise in semiconductor devices), and switching noise in power electronics. Noise is quantified by spectral density (V²/Hz or A²/Hz), integrated power (noise figure, SNR), and input-referred quantities. Noise analysis is critical in low-noise amplifier design, sensor interfaces, and IoT systems where signal margins are tight and noise directly limits measurement resolution.

---

## Key Equations

**Thermal noise voltage spectral density (Nyquist formula):**
$$\overline{v_n^2}/\Delta f = 4kTR \text{ (V}^2\text{/Hz)}$$

**Thermal noise current:**
$$\overline{i_n^2}/\Delta f = \frac{4kT}{R} \text{ (A}^2\text{/Hz)}$$

**MOSFET thermal noise (channel):**
$$\overline{v_{n,channel}^2}/\Delta f = \frac{4}{3} \frac{kT}{g_m}$$

**Noise figure (single stage):**
$$NF = \frac{SNR_{in}}{SNR_{out}} = 1 + \frac{\text{noise added}}{signal \times G}$$

**Cascaded noise figure (Friis formula):**
$$NF_{total} = NF_1 + \frac{NF_2 - 1}{G_1} + \frac{NF_3 - 1}{G_1 G_2} + \cdots$$

**Signal-to-noise ratio (SNR):**
$$\text{SNR} = \frac{P_{signal}}{P_{noise}} = \frac{\text{Signal Power}}{\int_0^{BW} S_n(f) df}$$

---

## Where It Appears

- [[34655 Integrated Analog Electronics 2|IAE2]] — Fundamental topic: thermal and flicker noise from MOSFETs and resistors; noise figure calculation; low-noise amplifier design; input-referred noise optimization
- [[34620 Basic Power Electronics|PE]] — Switching noise, conducted/radiated EMI, noise coupling in power converters and control loops
- [[34315 Internet of Things|IoT]] — Sensor noise budgets, signal conditioning, SNR constraints in wireless links and data acquisition systems
- [[62743 Digital Signal Processing (Reexam)|DSP (Archive)]] — Quantization noise, dithering, noise shaping in ADC/DAC systems

---

## Related Concepts

- [[Transfer Function]] — Noise transfer function H_n(s) relates input noise spectrum to output; shaped by system bandwidth and compensation
- [[Frequency Response]] — Noise spectral shaping depends on amplifier bandwidth and filter poles; affects total integrated noise power
- [[Fourier Transform]] — Noise power spectral density (PSD) analyzed in frequency domain; white noise has constant PSD, 1/f noise increases at low frequencies
- [[MOSFET]] — Intrinsic source of thermal and flicker noise; gm inversely affects input-referred noise; W/L ratio trades noise vs. bandwidth
- [[Feedback]] — Negative feedback reduces in-band noise proportional to (1+L); out-of-band noise may increase (noise boosting)
