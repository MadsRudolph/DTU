# Exercise II – Integrated Analogue Electronics 1
*Conceptual answers to Exercises 1–6.*

---

## Exercise 1 – MOSFET $W/L$ Ratio

In the Shichman–Hodges long-channel MOSFET model, the drain current in saturation is approximately proportional to $\beta (V_{GS}-V_{TH})^{2}$, where $\beta = \mu C_{ox} \dfrac{W}{L}$. The width‑to‑length ratio $W/L$ therefore directly scales the transconductance parameter and thus the current drive and small‑signal transconductance $g_m$.

Increasing $W$ (for fixed $L$) increases current capability, transconductance, and achievable speed, but also increases gate and diffusion capacitances, layout area, and power consumption. Increasing $L$ (for fixed $W$) improves matching and reduces channel‑length‑modulation and some short‑channel effects, but reduces current drive, lowers $g_m$, and generally makes circuits slower. Decreasing $W$ or $L$ has the opposite trade‑offs: smaller $W$ saves area and capacitance but limits current, while smaller $L$ enables higher speed and density but worsens short‑channel effects and variation.

---

## Exercise 2 – Feedback in MOSFET Op‑Amp Circuits

Negative feedback in MOSFET‑based op‑amps stabilizes the closed‑loop gain, reduces sensitivity to process and temperature variations, and allows accurate gain setting with passive components. It also improves linearity, reduces distortion, and broadens the usable bandwidth compared with the very high but poorly controlled open‑loop gain.

The disadvantages are mainly related to stability: feedback can introduce ringing or oscillations if the loop has insufficient phase margin. Achieving stable feedback requires careful pole‑zero placement and compensation (for example, Miller capacitors), which can limit bandwidth, reduce slew rate, and increase design complexity and sometimes power consumption.

---

## Exercise 3 – Second‑Order Feedback System Pole Placement

A standard second‑order closed‑loop system has complex‑conjugate poles characterized by natural frequency $\omega_n$ and damping ratio $\zeta$. Placing poles further left in the complex plane (higher $\omega_n$) increases bandwidth and speeds up the time response, but typically requires higher loop gain and can increase demands on current and device performance.

A lower damping ratio ($\zeta < 1$) yields faster response and higher bandwidth but more overshoot and ringing. A higher damping ratio (closer to critical damping) improves stability, reduces overshoot, and tends toward monotonic responses at the cost of slower settling and narrower bandwidth. If one pole is dominant and the other is far left, the system behaves more like a first‑order system with predictable stability but lower speed.

---

## Exercise 4 – Bandgap Voltage Reference

A bandgap reference generates an almost temperature‑independent voltage by summing a base–emitter voltage (with negative temperature coefficient) and a proportional‑to‑absolute‑temperature (PTAT) voltage derived from two BJTs operating at different current densities. The PTAT term is scaled so that its positive temperature coefficient cancels the negative coefficient of the base–emitter voltage, yielding a nearly flat reference around $1.2$–$1.25\ \text{V}$ in silicon.

Advantages include good temperature stability, relatively process‑insensitive absolute reference level, and suitability as an on‑chip reference for ADCs, DACs, and various analog bias circuits. Disadvantages are the need for bipolar devices and accurate resistors, which consume area, as well as non‑negligible power consumption and a minimum supply voltage requirement above the reference plus device headroom.

---

## Exercise 5 – Two‑Stage CMOS Op‑Amp with Miller Compensation

### 5a) Subcircuit functionality (first figure)

The first figure shows a two‑stage CMOS op‑amp with Miller compensation and a source‑follower‑like output arrangement.

- **M1–M2 and M3–M4 (input differential pair and active loads)**  
  M1 and M2 form the input differential pair, converting the input voltage difference $v_{IN}$ into differential currents. M3 and M4 act as current‑mirror active loads, turning the differential current into a single‑ended voltage at the first high‑impedance node that feeds the second stage.

- **M5 and M8 with $R_{BIAS}$ (bias network and current mirror)**  
  $R_{BIAS}$ together with M8 sets up a reference bias current from the supply, which is mirrored by M5 and other devices to bias the input and gain stages. This network defines the operating points of M1–M4 and the rest of the amplifier.

- **M6–M7 (second gain stage and load)**  
  M6 is a common‑source second‑gain stage receiving the first‑stage output and generating a large voltage gain at the output node $v_O$. M7 provides a current‑source load for M6, contributing high output resistance and setting the bias current of the second stage.

- **Capacitors $C_C$, $C_A$, $C_B$, and $C_L$**  
  $C_C$ is the Miller compensation capacitor between the first‑stage output node and the second‑stage input/output node; it creates a dominant pole and shapes the loop transfer to ensure stability. $C_A$, $C_B$, and the explicit load capacitor $C_L$ represent the total capacitance at the output node and auxiliary compensation paths, setting the output pole and helping control phase margin and transient response.

### 5b) Gain, GBW, and stability vs. currents and device parameters

Increasing the bias currents (for example by reducing $R_{BIAS}$ so that M8 and its mirrors conduct more current) increases the transconductance $g_m$ of M1–M2 and M6, which raises low‑frequency gain (within the limits set by output resistance) and pushes the dominant pole to higher frequency, thereby increasing the gain‑bandwidth product (GBW). However, higher currents also increase power consumption and can reduce intrinsic gain if channel‑length‑modulation becomes stronger, and non‑dominant poles may move such that phase margin is reduced, risking overshoot or instability.

Changing MOSFET dimensions affects both gain and stability. Increasing $W$ of M1–M2 or M6 (at fixed current) increases $g_m$, improving gain and potentially GBW, but also increases parasitic capacitances that lower pole frequencies and complicate compensation. Using longer $L$ or cascoding (if added) can increase output resistance and DC gain but introduces extra internal nodes and poles, requiring adjustment of $C_C$, $C_A$, and $C_B$ to preserve adequate phase margin. Overall, higher currents and larger devices can provide higher GBW and faster settling but at the cost of more power, area, and more delicate stability design.

---

## Exercise 6 – Differential Pair with Current‑Mirror Loads

The second figure shows a single‑ended differential amplifier with MOS input pair M1–M2, current‑mirror loads M3–M4, an output device M5, and tail/bias devices MA, MB, MC plus the ideal current source $I_0$. The output is taken at the drain of M5, so the circuit converts the differential input at M1–M2 into a single‑ended output at $v_{OUT}$.

### 6a) Increasing CMRR

Common‑mode rejection ratio (CMRR) is strongly influenced by the quality of the tail current source and the symmetry of the loads. Replacing the simple tail‑current arrangement ( $I_0$ with MA/MB ) by a higher‑output‑resistance current source (for example cascoded devices and long‑channel transistors) makes the tail current less sensitive to common‑mode input variations, directly improving CMRR.

Improving matching and output resistance of the load transistors M3–M4 also increases CMRR. This can be done by using identical $W/L$ ratios, careful common‑centroid layout, and possibly cascoding M3–M4 to raise their output resistance and reduce conversion of common‑mode signals into differential output. A more radical modification is to use a fully differential output (both sides of the mirror) together with a common‑mode feedback circuit, which further enhances rejection of common‑mode disturbances.

### 6b) Pros and cons of these modifications

The main advantages of these modifications are higher CMRR and often higher gain, making the amplifier more robust against supply and substrate noise and common‑mode input variations. A more ideal tail source and higher‑resistance loads reduce the influence of common‑mode changes on differential currents, and cascoding can boost intrinsic gain.

The disadvantages are increased circuit complexity, area, and sometimes power consumption, because additional devices and bias voltages are required. Stacking devices for cascoding and common‑mode feedback reduces voltage headroom and output‑swing capability between the $\pm 5\ \text{V}$ rails and introduces extra internal nodes, which add poles and can make frequency‑compensation and stability more challenging.
