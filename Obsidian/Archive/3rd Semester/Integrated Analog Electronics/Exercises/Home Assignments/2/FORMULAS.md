# Quick Reference Guide - Key Formulas and Concepts

## Exercise 1: MOSFET Equations

### Saturation Region ($V_{DS} \geq V_{GS} - V_T$)
$$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_T)^2 (1 + \lambda V_{DS})$$

### Triode Region ($V_{DS} < V_{GS} - V_T$)
$$I_D = \mu_n C_{ox} \frac{W}{L} \left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right] (1 + \lambda V_{DS})$$

### Transconductance
$$g_m = \frac{\partial I_D}{\partial V_{GS}} = \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_T) = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

### Output Resistance
$$r_o = \frac{1}{\lambda I_D}$$

### Key Capacitances
$$C_{gs} \approx \frac{2}{3} C_{ox} W L \quad \text{(in saturation)}$$
$C_{gd}$, $C_{db}$: overlap and junction capacitances

---

## Exercise 2: Feedback Equations

### Closed-Loop Gain
$$A_{CL} = \frac{A}{1 + A\beta}$$
where $A$ = open-loop gain, $\beta$ = feedback factor

### Loop Gain
$$T = A\beta$$

### Bandwidth Extension
$$BW_{closed} = BW_{open} \cdot (1 + A\beta)$$

### Input/Output Impedance (Voltage Feedback)
$$Z_{in,closed} = Z_{in,open} \cdot (1 + A\beta)$$
$$Z_{out,closed} = \frac{Z_{out,open}}{1 + A\beta}$$

---

## Exercise 3: Second-Order Systems

### Standard Form
$$H(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

### Pole Locations
$$s = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2} \quad \text{(for } 0 < \zeta < 1\text{)}$$

### Damping Ratio ($\zeta$)
- $\zeta > 1$: Overdamped (two real poles)
- $\zeta = 1$: Critically damped (repeated real poles)
- $0 < \zeta < 1$: Underdamped (complex conjugate poles)

### Quality Factor
$$Q = \frac{1}{2\zeta}$$

### Phase Margin
$$PM \approx 100\zeta \text{ degrees} \quad \text{(rule of thumb for } \zeta < 0.7\text{)}$$

---

## Exercise 4: Bandgap Reference

### VBE Temperature Dependence
$$V_{BE}(T) = V_{BE}(T_0) - k(T - T_0)$$
where $k \approx 2$ mV/°C

### ΔVBE (PTAT voltage)
$$\Delta V_{BE} = V_T \ln(N) = \frac{kT}{q} \ln(N)$$
where $N$ = emitter area ratio, $V_T$ = thermal voltage

### Output Voltage
$$V_{REF} = V_{BE} + \frac{R_2}{R_1} \Delta V_{BE} \approx 1.25 \text{ V}$$

### Temperature Coefficient
$$TC \approx 10-50 \text{ ppm/°C (with good design)}$$

---

## Exercise 5: Two-Stage Op-Amp

### DC Gain
$$A_v = A_{v1} \cdot A_{v2} = (g_{m1} \cdot r_{o2}) \cdot (g_{m6} \cdot r_{o6})$$

### Gain-Bandwidth Product
$$GBW = \frac{g_{m1}}{2\pi C_C}$$

### Unity-Gain Frequency
$$f_u = \frac{g_{m1}}{2\pi C_C}$$

### Slew Rate
$$SR = \frac{I_{tail}}{C_C}$$

### Phase Margin (for dominant pole compensation)
$$PM \approx 90° - \arctan\left(\frac{f_u}{f_{p2}}\right)$$
where $f_{p2}$ = second pole frequency

### Pole Locations (Miller Compensation)
$$f_{p1} \approx \frac{1}{2\pi g_{m6} r_{o6} C_C} \quad \text{(dominant pole)}$$
$$f_{p2} \approx \frac{g_{m6} C_C}{2\pi C_L C_C} \quad \text{(second pole)}$$

---

## Exercise 6: CMRR

### Definition
$$CMRR = \left|\frac{A_d}{A_{cm}}\right| = \left|\frac{\text{Differential Gain}}{\text{Common-Mode Gain}}\right|$$
$$CMRR_{(dB)} = 20\log\left(\frac{A_d}{A_{cm}}\right)$$

### Tail Current Source Impedance Effect
$$CMRR \approx g_m R_{tail}$$
where $R_{tail}$ = output impedance of tail current source

### Cascode Impedance
$$R_{out,cascode} \approx g_m r_o^2$$

### Mismatch Effects
$$\sigma(\Delta V_T) \propto \frac{1}{\sqrt{WL}} \quad \text{(threshold voltage mismatch)}$$
$$\sigma(\Delta \beta) \propto \frac{1}{\sqrt{WL}} \quad \text{(current factor mismatch)}$$

---

## General MOSFET Parameters

### Small-Signal Parameters
$$g_m = \frac{\partial I_D}{\partial V_{GS}}$$
$$r_o = \frac{\partial V_{DS}}{\partial I_D}$$
$$g_{mb} = \frac{\partial I_D}{\partial V_{BS}} \quad \text{(body effect transconductance)}$$

### gm/ID Methodology
$$\frac{g_m}{I_D} = \frac{2}{V_{GS} - V_T} \quad \text{(strong inversion)}$$
Useful for low-power design optimization

### Transit Frequency
$$f_T = \frac{g_m}{2\pi(C_{gs} + C_{gd})}$$

---

## Design Rules of Thumb

### Stability
- Phase margin $\geq 45°$ (preferably $60°$)
- Gain margin $\geq 6$ dB

### Matching
- Larger devices → better matching
- $\sigma(\Delta V_T) \propto \frac{1}{\sqrt{WL}}$
- Use common-centroid layout
- Keep orientation identical

### Bandwidth vs. Power
- Higher current → higher $g_m$ → higher bandwidth
- But also higher power consumption
- Optimize using $g_m/I_D$

### Headroom
- Each transistor needs $V_{DSsat} = V_{GS} - V_T$
- Cascode costs one additional $V_{DSsat}$
- Important for low-voltage design

---

## Useful Constants

- $\frac{kT}{q}$ at room temperature (300K): $\approx 26$ mV
- Silicon bandgap at 0K: $\approx 1.205$ V
- $V_{BE}$ temperature coefficient: $\approx -2$ mV/°C

---

Remember: These are simplified formulas. Real circuits may have additional second-order effects!

---

## Praktisk Anvendelse

| Projekt | Link | Anvendelse |
|---------|------|------------|
| VLF Metaldetektor (34621) | [TX Driver Design](obsidian://open?vault=34621-Metal-Detector&file=Docs%2FTheory%2FTX%20Driver%20Design) | Transferfunktioner, frekvensrespons for H-bro driver |
