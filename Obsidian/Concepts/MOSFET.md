---
type: concept
aliases: [Metal-Oxide-Semiconductor Field-Effect Transistor, MOS transistor, NMOS, PMOS]
tags:
  - concept
  - semiconductor
  - analog
  - power
courses: [34655, 34620, 62711]
---
# MOSFET

## Definition

A MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor) is a voltage-controlled semiconductor device that acts as a switch or amplifier. The gate-source voltage controls current flow between drain and source; zero gate voltage blocks current (off), while sufficient gate voltage creates an inversion layer, permitting current flow (on). MOSFETs are fundamental building blocks in both analog circuits (gain stages, current mirrors) and power electronics (switching regulators, gate drivers), bridging the gap between small-signal analog design and high-power switching applications.

---

## Key Equations

**Drain current (saturation region, long-channel):**
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2(1 + \lambda V_{DS})$$

**Transconductance (small-signal gain):**
$$g_m = \frac{\partial I_D}{\partial V_{GS}} = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)$$

**Output resistance (small-signal):**
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

**Gate-source capacitance (depletion region):**
$$C_{GS} \approx \frac{2}{3}C_{ox}\frac{W}{L} \cdot L^2$$

**Intrinsic gain (analog figure of merit):**
$$A_0 = g_m \cdot r_o = \frac{\mu_n C_{ox}(W/L)}{2 \lambda I_D}$$

---

## Where It Appears

- [[34655 Integrated Analog Electronics 2|IAE2]] — Small-signal modeling (gm, ro, parasitic capacitances); common-source and cascode amplifier stages; frequency response; noise analysis
- [[34620 Basic Power Electronics|PE]] — Main switching element in DC-DC converters; on-resistance RDS(on), switching losses, thermal management; gate drive requirements
- [[62711 Digital Systems Design|DSD]] — FPGA internal structure: MOSFET transistor arrays form lookup tables (LUTs), multiplexers, and logic gates
- Integrated Analog Electronics 1 (Archive) — Fundamentals of MOSFET operation and biasing

---

## Related Concepts

- [[Frequency Response]] — Parasitic MOSFET capacitances (CGS, CGD, CDB) determine high-frequency cutoff and bandwidth
- [[Feedback]] — MOSFETs in feedback configurations for stable amplifiers and regulators
- [[Noise Analysis]] — Thermal noise from channel resistance (flicker noise at low frequency); input-referred noise in MOSFET amplifiers
- [[Transfer Function]] — MOSFET small-signal model yields transfer functions of single and cascaded stages
- [[Bode Plot]] — Plot magnitude and phase response of MOSFET-based circuits to verify bandwidth and stability margins
