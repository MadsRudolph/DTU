---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: exercise
tags: [IAE2, exercise, cadence, opamp]
---
# Cadence Exercise -- Two-Stage OpAmp Design

> [!info] Exercise Files
> - Specifications: [[Amplifier_design_specifications_v3.pdf]]
> - Textbook: Carusone, Ch. 5-6 | Bruun (EB), Ch. 7
> - Related notes: [[Advanced OpAmps - Lecture Notes]]

## Specifications

| Parameter | Value |
|-----------|-------|
| $C_A = C_B$ | 1 pF |
| $C_L$ | 1.5 pF |
| $R_1$ | $10^9\;\Omega$ |
| $V_{DD}$ | 1.8 V |
| Closed-loop gain $V_{out}/V_{in}$ | 2 |
| Closed-loop BW $\omega_t$ | $2\pi \times 20$ MHz |
| Slew rate | $\geq 30$ V/μs |
| Phase margin | $\geq 70°$ |

**Process: 0.18 μm CMOS (Carusone Table 1.5, p. 53)**

| Parameter | NMOS | PMOS |
|-----------|------|------|
| $k' = \mu C_{ox}$ | 270 μA/V² | 70 μA/V² |
| $V_t$ | 0.5 V | $-0.45$ V |
| $\lambda \cdot L$ | 0.08 μm/V | 0.08 μm/V |
| $\lambda$ (at $L = 1\;\mu$m) | 0.08 V⁻¹ | 0.08 V⁻¹ |
| $C_{ox}$ | 8.5 fF/μm² | 8.5 fF/μm² |
| $C_{ov} = L_{ov} C_{ox}$ | 0.35 fF/μm | 0.50 fF/μm |

---

## Circuit Topology (Carusone Ch. 6 Fig. 3)

- **Q1, Q2** (PMOS) -- Differential input pair
- **Q3, Q4** (NMOS) -- Current mirror active load
- **Q5** (PMOS) -- Tail current source (mirrors Q8)
- **Q6** (PMOS) -- Second stage current source (mirrors Q8)
- **Q7** (NMOS) -- Second stage CS gain device (mirrors Q3)
- **Q8** (PMOS) -- Bias reference (20 μA)

**Current relationships:** $I_{D1} = I_{D2} = I_{D3} = I_{D4} = \tfrac{1}{2}I_{D5}$, and $I_{D6} = I_{D7}$

---

## Step 1 -- Feedback Factor β

The capacitive divider from output to inverting input:

$$\beta = \frac{C_B}{C_A + C_B} = \frac{1}{1+1}$$

$$\boxed{\beta = 0.5}$$

---

## Step 2 -- Second Pole $\omega_{p2}$ (EB 7.8)

Choose $\omega_z = 10\,\omega_t$ (hint 2a). The PM condition:

$$PM = 90° - \arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) - \arctan\!\left(\frac{\omega_t}{\omega_z}\right) \geq 70°$$

$$90° - \arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) - \arctan(0.1) \geq 70°$$

$$\arctan\!\left(\frac{\omega_t}{\omega_{p2}}\right) \leq 90° - 70° - 5.71° = 14.29°$$

$$\omega_{p2} \geq \frac{\omega_t}{\tan(14.29°)} = \frac{\omega_t}{0.2546} \approx 4\,\omega_t$$

$$\boxed{\omega_{p2} = 4\,\omega_t = 2\pi \times 80\text{ MHz}}$$

---

## Step 3 -- $g_{m7}/g_{m1}$ Ratio (EB 7.9)

Open-loop GBW: $\omega_{tl} = g_{m1}/C_c$, and $\omega_t = \beta\cdot\omega_{tl}$, so $\omega_{tl} = \omega_t/\beta = 2\omega_t$.

RHP zero: $\omega_z = g_{m7}/C_c = 10\,\omega_t$.

$$\frac{g_{m7}}{g_{m1}} = \frac{\omega_z}{\omega_{tl}} = \frac{10\,\omega_t}{2\,\omega_t}$$

$$\boxed{g_{m7} = 5\,g_{m1}}$$

---

## Step 4 -- Total Load Capacitance (EB §7.1)

From the output, $C_L$ is to ground and $C_B$ is in series with $C_A$ to ground:

$$C_{L,\text{tot}} = C_L + \frac{C_B \cdot C_A}{C_B + C_A} = 1.5 + \frac{1 \times 1}{1+1} = 1.5 + 0.5$$

$$\boxed{C_{L,\text{tot}} = 2.0\text{ pF}}$$

---

## Step 5 -- Compensation Capacitor $C_c$ (EB 7.12)

From $\omega_{p2} = g_{m7}/C_{L,\text{tot}}$ and $\omega_z = g_{m7}/C_c$:

$$\frac{C_c}{C_{L,\text{tot}}} = \frac{\omega_{p2}}{\omega_z} = \frac{4\,\omega_t}{10\,\omega_t} = 0.4$$

$$\boxed{C_c = 0.4 \times 2.0 = 0.8\text{ pF}}$$

---

## Step 6 -- First Stage $g_{m1}$ (EB 7.5)

$$g_{m1} = \omega_{tl} \cdot C_c = \frac{\omega_t}{\beta} \cdot C_c = \frac{2\pi \times 20 \times 10^6}{0.5} \times 0.8 \times 10^{-12}$$

$$g_{m1} = 2.513 \times 10^{8} \times 8 \times 10^{-13}$$

$$\boxed{g_{m1} = 201\text{ μA/V}}$$

---

## Step 7 -- Second Stage $g_{m7}$

$$g_{m7} = 5 \times g_{m1} = 5 \times 201$$

$$\boxed{g_{m7} = 1005\text{ μA/V} \approx 1.0\text{ mA/V}}$$

---

## Step 8 -- Tail Current $I_{D5}$ (EB 7.21)

First stage slew rate: $SR = I_{D5}/C_c$

$$I_{D5} = SR \times C_c = 30 \times 10^6 \times 0.8 \times 10^{-12}$$

$$\boxed{I_{D5} = 24\text{ μA}}$$

---

## Step 9 -- Second Stage Current $I_{D6} = I_{D7}$ (EB 7.22)

Second stage slew rate: $SR_2 = I_{D7}/C_{L,\text{tot}}$

$$I_{D6} = I_{D7} = SR \times C_{L,\text{tot}} = 30 \times 10^6 \times 2.0 \times 10^{-12}$$

$$\boxed{I_{D6} = I_{D7} = 60\text{ μA}}$$

---

## Step 10 -- W/L Ratios

**Branch currents:**
- $I_{D1} = I_{D2} = I_{D3} = I_{D4} = I_{D5}/2 = 12$ μA
- $I_{D6} = I_{D7} = 60$ μA
- $I_{D8} = 20$ μA (reference)

All transistors: $L = 1$ μm. Rule of thumb: $V_\text{eff} = 200$ mV for Q5, Q6.

Using $W/L = \dfrac{2\,I_D}{k' \cdot V_\text{eff}^2}$ and $V_\text{eff} = \dfrac{2\,I_D}{g_m}$:

### Q1, Q2 (PMOS, diff pair)

$V_\text{eff}$ set by $g_{m1}$ requirement:

$$V_{\text{eff},1} = \frac{2\,I_{D1}}{g_{m1}} = \frac{2 \times 12}{201} = 119\text{ mV}$$

$$\frac{W_1}{L} = \frac{g_{m1}}{k'_p \cdot V_{\text{eff},1}} = \frac{201}{70 \times 0.119} = \frac{201}{8.33} \approx 24$$

### Q3, Q4 (NMOS, mirror load)

Q7 mirrors Q3 so $V_{\text{eff},3} = V_{\text{eff},7}$:

$$V_{\text{eff},7} = \frac{2\,I_{D7}}{g_{m7}} = \frac{120}{1005} = 119\text{ mV}$$

$$\frac{W_7}{L} = \frac{2 \times 60}{270 \times 0.119^2} = \frac{120}{3.82} \approx 31$$

$$\frac{W_3}{L} = \frac{W_7}{L} \times \frac{I_{D3}}{I_{D7}} = 31 \times \frac{12}{60} \approx 6.2$$

### Q5 (PMOS, tail current source)

$$\frac{W_5}{L} = \frac{2 \times 24}{70 \times 0.2^2} = \frac{48}{2.8} \approx 17$$

### Q6 (PMOS, 2nd stage current source)

$$\frac{W_6}{L} = \frac{2 \times 60}{70 \times 0.2^2} = \frac{120}{2.8} \approx 43$$

### Q8 (PMOS, bias reference)

Mirrors to Q5 and Q6:

$$\frac{W_8}{L} = \frac{W_5}{L} \times \frac{I_{D8}}{I_{D5}} = 17 \times \frac{20}{24} \approx 14$$

Check: $I_{D6} = \dfrac{W_6/L}{W_8/L} \times 20 = \dfrac{43}{14} \times 20 = 61$ μA $\approx 60$ μA ✓

---

## Design Summary

| Transistor | Type | W/L | W (μm) | $I_D$ (μA) | $V_\text{eff}$ (mV) |
|------------|------|-----|---------|-------------|----------------------|
| Q1 | PMOS | 24 | 24 | 12 | 119 |
| Q2 | PMOS | 24 | 24 | 12 | 119 |
| Q3 | NMOS | 6.2 | 6.2 | 12 | 119 |
| Q4 | NMOS | 6.2 | 6.2 | 12 | 119 |
| Q5 | PMOS | 17 | 17 | 24 | 200 |
| Q6 | PMOS | 43 | 43 | 60 | 200 |
| Q7 | NMOS | 31 | 31 | 60 | 119 |
| Q8 | PMOS | 14 | 14 | 20 | 200 |

| Component | Value |
|-----------|-------|
| $C_c$ | 0.8 pF |
| $R_c$ (zero cancellation) | $1/g_{m7} \approx 1$ kΩ |

---

## Verification

| Spec | Calculation | Value | Meets? |
|------|-------------|-------|--------|
| GBW | $g_{m1}/C_c = 201\mu/0.8p$ | $2\pi \times 40$ MHz | -- |
| CL BW | $\beta \times GBW$ | $2\pi \times 20$ MHz | ✓ |
| $\omega_{p2}$ | $g_{m7}/C_{L,\text{tot}} = 1005\mu/2p$ | $4\,\omega_t$ | ✓ |
| $\omega_z$ | $g_{m7}/C_c = 1005\mu/0.8p$ | $10\,\omega_t$ | ✓ |
| PM | $90° - 14.0° - 5.7°$ | **70.3°** | ✓ |
| SR (1st) | $I_{D5}/C_c = 24\mu/0.8p$ | **30 V/μs** | ✓ |
| SR (2nd) | $I_{D7}/C_{L,\text{tot}} = 60\mu/2p$ | **30 V/μs** | ✓ |

---

## Lead Compensation (Optional)

Adding $R_c$ in series with $C_c$ moves the RHP zero. Without $R_c$, the RHP zero at $\omega_z = g_{m7}/C_c = 10\,\omega_t$ already satisfies PM $\geq$ 70°.

**Zero cancellation:** $R_c = 1/g_{m7} \approx 1$ kΩ pushes the zero to infinity, improving PM to ~76°.

**Pole-zero cancellation:** To place a LHP zero at $\omega_{p2}$:

$$R_c = \frac{1}{g_{m7}} + \frac{1}{\omega_{p2} \cdot C_c} = 995 + \frac{1}{5.03 \times 10^8 \times 0.8 \times 10^{-12}} = 995 + 2486 \approx 3.5\text{ kΩ}$$

This cancels the second pole and further improves stability.

---

## SPICE Simulation Results

> [!info] Simulation Setup
> - **Tool:** ngspice 41 via PySpice (Level 1 MOSFET models)
> - **Source:** `SPICEPilot/examples/3_34655_opamp/`
> - **Files:** `two_stage_opamp_34655.cir` (netlist), `two_stage_opamp_34655.py` (PySpice)

### DC Operating Point

| Node | Voltage | Description |
|------|---------|-------------|
| `vout` | 0.771 V | Output quiescent (~mid-rail) |
| `n_bias` | 1.153 V | PMOS bias rail ($V_{DD} - \|V_{GS,Q8}\|$) |
| `n_tail` | 0.768 V | Diff pair tail |
| `n_d1` = `n_d2` | 0.619 V | First stage output (balanced) |

### Open-Loop AC Analysis

| Parameter | Simulated | Hand Calc | Status |
|-----------|-----------|-----------|--------|
| DC Gain | **81.5 dB** (11,904 V/V) | ~93 dB | Lower (λ doubles $r_{ds}$ reduction) |
| GBW | **40.3 MHz** | 40 MHz | ✓ |
| UGF | **37.2 MHz** | ~40 MHz | ✓ |
| Phase Margin | **67.1°** | 70.3° | Slightly low |

> [!warning] Phase Margin & DC Gain
> The simulated PM (67.1°) is ~3° below the 70° target, and DC gain is 81.5 dB vs the ~93 dB hand calculation. Both are due to the corrected $\lambda = 0.08\;\text{V}^{-1}$ (from Table 1.5), which is 2× larger than the value initially assumed. The higher $\lambda$ halves the output resistance $r_{ds} = 1/(\lambda I_D)$, reducing the gain of each stage. In Cadence with X-FAB process models, $R_c$ would be tuned upward to compensate the PM.

### Closed-Loop AC Analysis

| Parameter | Simulated | Target | Status |
|-----------|-----------|--------|--------|
| Midband Gain | **6.01 dB** (gain = 2.0) | 6 dB | ✓ |
| $-3$ dB BW | **~20 MHz** | 20 MHz | ✓ |

### Transient (Slew Rate)

| Parameter | Simulated | Target | Status |
|-----------|-----------|--------|--------|
| Slew Rate | **32.2 V/μs** | $\geq 30$ V/μs | ✓ |

### Bode & Step Response

![[opamp_34655_results.png]]

### How to Run

> [!tip] Simulation Files
> Located in `DTU/SPICEPilot/examples/3_34655_opamp/`

**Method 1 -- Double-click (ngspice only)**

Navigate to the folder and double-click `RUN.bat`. Prints DC operating point, gain, UGF, and phase to the console.

**Method 2 -- Terminal (full analysis + plots)**

```
cd ~/DTU/SPICEPilot/examples/3_34655_opamp && /c/Users/Mads2/miniconda3/python.exe two_stage_opamp_34655.py
```

Runs open-loop AC, closed-loop AC, and transient analyses. Saves a 4-panel plot to `opamp_34655_results.png`.

**Method 3 -- ngspice interactive**

```
cd ~/DTU/SPICEPilot/examples/3_34655_opamp && /c/Users/Mads2/miniconda3/Library/bin/ngspice_con.exe two_stage_opamp_34655.cir
```

> [!note] Prerequisites
> ngspice and PySpice are installed via conda (`conda install -c conda-forge ngspice` + `pip install PySpice`).
