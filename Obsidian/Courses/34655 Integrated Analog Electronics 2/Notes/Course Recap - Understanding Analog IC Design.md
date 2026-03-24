---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: overview
tags: [IAE2, overview]
---
# Course Recap - Understanding Analog IC Design

**Course:** 34655 Integrated Analog Electronics 2

> [!tip] How to Use This Document
> This is a simplified overview of the course material. Read through it to build intuition, then dive into the detailed notes and exercises for the full picture.
>
> **Detailed Resources:**
> - [[Lecture 1 - Introduction and Prerequisites]]
> - [[Lecture 2 - Advanced OpAmps]]
> - [[Problem 1 - Amplifier Configurations]]
> - [[Problem 2 - Advanced OpAmps]]

---

## The Big Picture: What Are We Doing?

In this course, we design **operational amplifiers (OpAmps)** using CMOS transistors. An OpAmp is basically a very high-gain amplifier that we use as a building block for analog circuits.

**The challenge:** We want OpAmps with:
- **High gain** (so feedback works well)
- **High bandwidth** (so they're fast)
- **Good output swing** (so signals don't clip)
- **Low power** (so batteries last)

The problem? These goals often conflict! High gain usually means low bandwidth. This course teaches you the tricks to optimize these trade-offs.

---

## Part 1: The Building Block - The MOSFET

### What Does a MOSFET Do?

Think of a MOSFET as a **voltage-controlled current source**:
- Apply a voltage to the **gate** ($V_{GS}$)
- Current flows from **drain** to **source** ($I_D$)

The MOSFET is a **4-terminal device**: Gate, Drain, Source, and Bulk (Body).

```
        Gate
          |
    ──────┴──────
    |           |
  Drain       Source
    |           |
         Bulk
```

---

### The Shichman-Hodges Model (Large Signal)

This is the fundamental equation that describes how a MOSFET behaves. It's called "large signal" because it describes the full DC operating point, not just small variations.

#### The Three Operating Regions

| Region | Condition | Current Equation |
|--------|-----------|------------------|
| **Cutoff (Off)** | $V_{GS} < V_t$ | $I_D = 0$ |
| **Linear (Triode)** | $V_{GS} > V_t$ AND $V_{DS} < V_{eff}$ | $I_D = \mu C_{ox}\frac{W}{L}\left[(V_{GS}-V_t)V_{DS} - \frac{1}{2}V_{DS}^2\right]$ |
| **Saturation (Active)** | $V_{GS} > V_t$ AND $V_{DS} > V_{eff}$ | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2$ |

> [!info] What the Variables Mean
> - $V_t$ = threshold voltage (the "turn-on" voltage, typically ~0.5V)
> - $V_{GS} - V_t = V_{eff}$ = effective voltage (overdrive voltage)
> - $W/L$ = width/length ratio (designer's choice - bigger = more current)
> - $\mu$ = mobility (how easily electrons move, process dependent)
> - $C_{ox}$ = gate oxide capacitance per unit area (process dependent)
> - $\mu C_{ox}$ together is often written as $k'_n$ for NMOS

#### Understanding Each Region

**Cutoff:** The gate voltage is below threshold - no channel forms, no current flows. The transistor is OFF.

**Linear (Triode):** The transistor is ON, but acts like a voltage-controlled resistor. Current depends on BOTH $V_{GS}$ and $V_{DS}$. We avoid this region for amplifiers.

**Saturation:** The transistor is ON and acts like a current source. Current is controlled only by $V_{GS}$ (approximately). This is where we want to operate for amplifiers!

> [!example] Analogy
> Think of water flowing through a pipe:
> - **Cutoff:** Valve is closed, no water flows
> - **Linear:** Valve is partially open, flow depends on pressure difference
> - **Saturation:** Valve is fully open, flow is limited by the valve opening size, not the pressure

---

### Channel Length Modulation

The basic saturation equation says current doesn't depend on $V_{DS}$. But in reality, it does slightly:

$$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2 \cdot (1 + \lambda V_{DS})$$

The factor $(1 + \lambda V_{DS})$ models **channel length modulation**:
- As $V_{DS}$ increases, the effective channel gets shorter
- Shorter channel → more current
- $\lambda$ = channel length modulation parameter (typically 0.01-0.1 V⁻¹)
- $V_A = 1/\lambda$ = Early voltage (typically 10-100 V)

> [!tip] Why This Matters
> Channel length modulation limits our output resistance and therefore our gain!
> Without it, a transistor would be a perfect current source (infinite resistance).
> With it, $r_{ds} = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$

---

### The Bulk (Body) Effect

When the source is not at the same potential as the bulk, the threshold voltage changes:

$$V_t = V_{t0} + \gamma\left(\sqrt{|2\Phi_F| + V_{SB}} - \sqrt{|2\Phi_F|}\right)$$

Where:
- $V_{t0}$ = threshold voltage when $V_{SB} = 0$
- $\gamma$ = body effect coefficient (process dependent, ~0.3-0.5 V^½)
- $\Phi_F$ = Fermi potential (~0.3-0.4 V)
- $V_{SB}$ = source-to-bulk voltage

> [!warning] When Does This Matter?
> - In cascode configurations where the source isn't at ground
> - In source followers
> - Anywhere the source is "floating"
>
> The bulk effect **reduces gain** in these configurations because it effectively reduces $g_m$.

---

### NMOS vs PMOS

Everything above is for NMOS. For PMOS, flip the signs:

| Parameter            | NMOS                 | PMOS                 |
| -------------------- | -------------------- | -------------------- |
| Threshold            | $V_t > 0$ (positive) | $V_t < 0$ (negative) |
| Current direction    | Into drain           | Out of drain         |
| Saturation condition | $V_{DS} > V_{eff}$   | $V_{SD} >V_e$        |
| Mobility             | Higher (~2-3×)       | Lower                |


> [!note] Practical Impact
> PMOS transistors need to be ~2-3× wider than NMOS to get the same $g_m$, because their mobility is lower.

**Key insight:** For amplifiers, we always keep transistors in **saturation**. This is where they act as good current sources.

---

## Part 2: Small Signal Analysis - The Key to Understanding Gain

### Why "Small Signal"?

The MOSFET equations are nonlinear (that $V_{GS}^2$ term). If we tried to analyze circuits with the full nonlinear equations, the math would be horrible.

**The trick:** For small signals around a DC operating point, any smooth curve looks like a straight line if you zoom in enough!

```
I_D
 |        ╱ Actual curve (quadratic)
 |      ╱╱
 |    ╱╱   ← At this point, we approximate
 |  ╱╱       with a tangent line (linear!)
 |╱╱
 └────────── V_GS
```

> [!abstract] Notation Convention
> - **CAPITAL letters** ($V_{GS}$, $I_D$) = DC bias point (the operating point)
> - **lowercase letters** ($v_{gs}$, $i_d$) = small signal variations around that point

---

### From Large Signal to Small Signal

Starting from the Shichman-Hodges equation:
$$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS}-V_t)^2(1 + \lambda V_{DS})$$

We take partial derivatives at the bias point to get the small signal parameters:

$$i_d = \underbrace{\frac{\partial I_D}{\partial V_{GS}}}_{g_m} \cdot v_{gs} + \underbrace{\frac{\partial I_D}{\partial V_{DS}}}_{g_{ds}} \cdot v_{ds}$$

This gives us the **small signal model**: a linear circuit that behaves like the MOSFET for small variations.

---

### The Small Signal Model

```
    Gate ○───────────────────┐
                             │
                          ┌──┴──┐
                          │     │
    Drain ○───────────────┤ gm·vgs ├──┬──○ Drain
                          │  ↓   │  │
                          └─────┘  ═══ rds
                                   │
    Source ○───────────────────────┴──○ Source
```

The model has two elements:
1. **Voltage-controlled current source** ($g_m \cdot v_{gs}$) - the main amplifying action
2. **Output resistance** ($r_{ds}$) - models the non-ideal current source

---

### The Three Most Important Parameters

#### 1. Transconductance ($g_m$) - "How much current per volt?"

$$g_m = \frac{\partial I_D}{\partial V_{GS}}\bigg|_{\text{bias}} = \mu C_{ox}\frac{W}{L}(V_{GS}-V_t) = \mu C_{ox}\frac{W}{L}V_{eff}$$

**Three equivalent ways to write $g_m$:**

| Form | Formula | When to Use |
|------|---------|-------------|
| Process/geometry | $g_m = \mu C_{ox}\frac{W}{L}V_{eff}$ | When you know $W/L$ and $V_{eff}$ |
| Current-based | $g_m = \frac{2I_D}{V_{eff}}$ | When you know bias current (most common!) |
| Square-root form | $g_m = \sqrt{2\mu C_{ox}\frac{W}{L}I_D}$ | Shows $g_m \propto \sqrt{I_D}$ |

> [!example] Intuition
> If $g_m = 1$ mA/V, then a 1 mV change at the gate causes a 1 µA change in drain current.
>
> **Higher $g_m$ = Higher gain!**

> [!tip] Scaling Rule
> If you double the current: $g_m$ increases by $\sqrt{2}$ (not 2×!)
>
> $$g_m \propto \sqrt{I_D}$$

**How to increase $g_m$:**
- Increase bias current $I_D$ (but costs power)
- Decrease $V_{eff}$ (but reduces speed and headroom)
- Increase $W/L$ (but increases capacitance)

---

#### 2. Output Conductance ($g_{ds}$) and Resistance ($r_{ds}$)

$$g_{ds} = \frac{\partial I_D}{\partial V_{DS}}\bigg|_{\text{bias}} = \lambda I_D = \frac{I_D}{V_A}$$

$$r_{ds} = \frac{1}{g_{ds}} = \frac{V_A}{I_D} = \frac{1}{\lambda I_D}$$

> [!example] Intuition
> An ideal current source has infinite output resistance (current doesn't change with voltage).
> Real transistors have finite $r_{ds}$ - the current slightly increases as $V_{DS}$ increases.
>
> **Higher $r_{ds}$ = Better current source = Higher gain!**

> [!tip] Scaling Rule
> If you double the current: $r_{ds}$ halves!
>
> $$r_{ds} \propto \frac{1}{I_D}$$

---

#### 3. Bulk Transconductance ($g_{mb}$) - Often Forgotten!

When the bulk effect matters:

$$g_{mb} = g_m \cdot \eta \quad \text{where} \quad \eta = \frac{\gamma}{2\sqrt{|2\Phi_F| + V_{SB}}}$$

Typically $\eta \approx 0.1$ to $0.3$, so $g_{mb} \approx 0.1 \cdot g_m$ to $0.3 \cdot g_m$.

> [!note] When to Include $g_{mb}$
> - In common-gate stages
> - In source followers
> - In cascode transistors where source isn't at fixed potential
>
> Often we write $(g_m + g_{mb})$ or just remember that the effective $g_m$ is ~20% higher.

---

### Complete Small Signal Model (with Bulk)

```
    Gate ○────────────────────────┐
                                  │
                               ┌──┴──┐
                               │     │
    Drain ○────────────────────┤gmvgs├──┬───┬──○ Drain
                               │  ↓  │  │   │
                               └─────┘  │ ┌─┴─┐
                               ┌─────┐  │ │   │
    Bulk ○─────────────────────┤gmbvbs├─┤═══ rds
                               │  ↓  │  │ │   │
                               └──┬──┘  │ └───┘
                                  │     │
    Source ○──────────────────────┴─────┴──○ Source
```

---

### The Intrinsic Gain - A Fundamental Limit

$$A_i = g_m \cdot r_{ds}$$

Substituting our expressions:
$$A_i = \frac{2I_D}{V_{eff}} \cdot \frac{V_A}{I_D} = \frac{2V_A}{V_{eff}}$$

This is the **maximum gain you can get from a single transistor**.

| Technology | Typical $A_i$ |
|------------|---------------|
| Long-channel (old) | 50-100 V/V |
| Short-channel (modern) | 10-30 V/V |

> [!warning] The Fundamental Trade-off
> - Want high $g_m$? Increase $I_D$ → but $r_{ds}$ decreases
> - Want high $r_{ds}$? Decrease $I_D$ → but $g_m$ decreases
> - The intrinsic gain $A_i = \frac{2V_A}{V_{eff}}$ doesn't depend on current!
>
> **To maximize $A_i$:** Use small $V_{eff}$ (but this reduces speed and headroom)

---

### How to Use the Small Signal Model

1. **Find the DC operating point** (bias currents and voltages)
2. **Calculate small signal parameters** ($g_m$, $r_{ds}$, etc.) at that point
3. **Replace each transistor** with its small signal model
4. **Short all DC voltage sources** (they're constant, so no AC signal)
5. **Open all DC current sources** (they're constant too)
6. **Analyze the resulting linear circuit**

> [!example] Example: Common Source Gain
> 1. Transistor replaced by: current source $g_m v_{gs}$ in parallel with $r_{ds}$
> 2. $v_{gs} = v_{in}$ (input is at gate, source is grounded)
> 3. Output voltage: $v_{out} = -g_m v_{gs} \cdot r_{ds} = -g_m r_{ds} \cdot v_{in}$
> 4. Gain: $A_v = v_{out}/v_{in} = -g_m r_{ds}$

---

## Part 3: Single-Stage Amplifiers

### Common Source (CS) - The Workhorse

**What it does:** Amplifies voltage with phase inversion (output goes down when input goes up)

| Property | Value | Meaning |
|----------|-------|---------|
| Gain | $A_v = -g_m \cdot r_{ds}$ | Negative = inverting |
| Output resistance | $r_{out} = r_{ds}$ | Moderate |
| Bandwidth | $f_{3dB} = \frac{1}{2\pi r_{out} C_L}$ | Limited by output RC |

> [!tip] When to Use
> This is your default gain stage. Simple and effective.

---

### Common Gate (CG) - The Current Buffer

**What it does:** Takes current in, gives current out, but with high output impedance

| Property | Value |
|----------|-------|
| Gain | $A_v = g_m \cdot r_{ds}$ (non-inverting) |
| Input resistance | $r_{in} \approx 1/g_m$ (low!) |
| Output resistance | Can be very high |

> [!tip] When to Use
> Used in **cascode** configurations to boost output impedance.

---

### Common Drain (Source Follower) - The Buffer

**What it does:** Gain ≈ 1, but with low output impedance

| Property | Value |
|----------|-------|
| Gain | $A_v \approx 1$ (slightly less due to bulk effect) |
| Output resistance | $r_{out} \approx 1/g_m$ (low!) |

> [!tip] When to Use
> Output stages where you need to drive a load.

---

## Part 4: Getting More Gain - Cascode and Cascade

### The Problem with Single Stages

A single common-source stage gives gain = $g_m \cdot r_{ds}$ ≈ 20-100 V/V.

For a good OpAmp, we need gains of 1000-10000 V/V. How do we get there?

### Solution 1: Cascode (Stacking Transistors)

Stack a common-gate transistor on top of a common-source transistor:

```
        Vout
          |
         [M2] ← Common Gate (shields M1 from output)
          |
         [M1] ← Common Source (does the amplification)
          |
         GND
```

**The magic:** M2 "shields" the drain of M1 from output voltage changes. This dramatically increases output resistance!

| Property | Single CS | Cascode |
|----------|-----------|---------|
| Gain | $g_m r_{ds}$ | $g_m r_{ds} \cdot g_m r_{ds}$ |
| Output resistance | $r_{ds}$ | $r_{ds} \cdot g_m r_{ds}$ |

> [!success] Result
> Cascode gives **gain squared** compared to single stage!
> If single stage = 50 V/V, cascode = 2500 V/V

> [!warning] The Catch
> **Reduced output swing!** Each stacked transistor needs its $V_{eff}$ headroom.
> See [[Lecture 2 - Advanced OpAmps#6. Folded Cascode Stage]] for the solution.

---

### Solution 2: Cascade (Two Stages in Series)

Put two common-source stages in series:

```
Vin → [CS Stage 1] → [CS Stage 2] → Vout
```

**Result:** Gains multiply! $A_{total} = A_1 \times A_2$

| Property | Single CS | Two-Stage Cascade |
|----------|-----------|-------------------|
| Gain | $g_m r_{ds}$ | $(g_m r_{ds})^2$ |
| Output resistance | $r_{ds}$ | $r_{ds}$ (only last stage matters) |

> [!warning] The Catch
> **Two high-impedance nodes = Two poles = Stability problems!**
> This is why we need frequency compensation (Miller capacitor).

---

## Part 5: The Gain-Bandwidth Trade-off

### A Fundamental Truth

$$GBW = \frac{g_m}{2\pi C_L}$$

The gain-bandwidth product is **constant** for a given $g_m$ and load capacitance!

> [!example] What This Means
> If your amplifier has:
> - Gain = 100, Bandwidth = 1 MHz → GBW = 100 MHz
> - Gain = 1000, Bandwidth = 100 kHz → GBW = 100 MHz (same!)
>
> **You can trade gain for bandwidth, but you can't have both!**

This is demonstrated in [[Problem 1 - Amplifier Configurations]] where cascode and common-source have the same GBW despite different gains.

### How to Increase GBW?

The only ways:
1. **Increase $g_m$** (more current or larger transistors)
2. **Decrease $C_L$** (smaller load)
3. **Use cascade (two-stage)** - this actually multiplies GBW!

---

## Part 6: Current Mirrors - Biasing Done Right

### What's a Current Mirror?

A circuit that copies a reference current to other parts of the chip:

```
    Iref        Iout = K × Iref
      ↓           ↓
     [M1]       [M2]
      |──────────|  (gates connected)
     GND        GND
```

The ratio $K = (W/L)_2 / (W/L)_1$ sets the current scaling.

### The Problem: Output Impedance

A simple current mirror has output impedance = $r_{ds}$ (not great).

When loading a high-gain stage, this limits the overall gain!

### The Solution: Cascode Current Mirror

Add cascode transistors to the mirror → output impedance becomes $g_m r_{ds}^2$

**But there's a catch:** Regular cascode needs more voltage headroom ($V_t + 2V_{eff}$).

### Wide-Swing Cascode - Best of Both Worlds

Clever biasing reduces headroom to just $2V_{eff}$ while keeping high output impedance.

> [!abstract] Design Rule
> For the bias transistor: $(W/L)_{bias} = (W/L)_{mirror} / 4$
>
> This ensures $V_{eff,bias} = 2V_{eff}$, keeping everything in saturation.

See [[Problem 2 - Advanced OpAmps#Problem 1 Wide-Swing Current Mirror]] for the full analysis.

---

## Part 7: OpAmp Topologies Compared

### Summary Table

| Topology | Gain | Output Swing | Complexity | Best For |
|----------|------|--------------|------------|----------|
| Two-stage | High | Excellent | Medium | General purpose |
| Telescopic cascode | Very high | Poor | Low | High-gain, limited swing OK |
| Folded cascode | High | Good | Medium | Good all-rounder |
| Current mirror OTA | Very high | Good | Medium | When you need extra gain |

### Folded Cascode - The Practical Choice

**Why "folded"?** Instead of stacking NMOS on NMOS, we "fold" to PMOS:

```
Traditional:       Folded:
    |                  |
   [N]                [P] ← Folded to opposite type
    |                  |
   [N]                [N]
    |                  |
```

**Advantage:** Much better output swing because we're not stacking same-polarity transistors.

See [[Lecture 2 - Advanced OpAmps#6. Folded Cascode Stage]] for details.

---

## Part 8: Feedback and Stability

### Why Feedback?

OpAmps are used in feedback configurations:

$$A_{closed-loop} = \frac{A_{open-loop}}{1 + \beta \cdot A_{open-loop}} \approx \frac{1}{\beta}$$

With high open-loop gain, the closed-loop gain depends only on the feedback network (resistors, capacitors) - very precise and stable!

### The Stability Problem

Feedback can cause **oscillation** if the phase shift reaches 180° while gain > 1.

**Phase margin** tells us how stable the system is:
- PM > 60° → Stable, well-behaved
- PM = 45° → Significant ringing
- PM < 0° → Oscillation!

### Miller Compensation

For two-stage OpAmps, we add a capacitor between the stages:

```
Stage 1 ──┤├── Stage 2
          Cc (Miller capacitor)
```

This capacitor appears **multiplied by the gain** at the first stage (Miller effect), creating a dominant low-frequency pole that ensures stability.

---

## Part 9: Putting It All Together

### The Design Flow

1. **Specifications:** What gain, bandwidth, output swing, power do you need?
2. **Topology selection:** Based on specs, choose two-stage, folded cascode, etc.
3. **Hand calculations:** Use formulas to get initial transistor sizes
4. **Simulation:** Verify in Cadence, iterate until specs are met
5. **Layout:** Physical design (covered in 34656)

### Key Formulas Cheat Sheet

| What You Want | Formula |
|---------------|---------|
| Transconductance | $g_m = \frac{2I_D}{V_{eff}} = \sqrt{2\mu C_{ox}\frac{W}{L}I_D}$ |
| Output resistance | $r_{ds} = \frac{V_A}{I_D}$ |
| CS gain | $A_v = -g_m r_{ds}$ |
| Cascode gain | $A_v = -g_m^2 r_{ds}^2$ |
| Bandwidth | $f_{3dB} = \frac{1}{2\pi r_{out} C_L}$ |
| GBW | $GBW = \frac{g_m}{2\pi C_L}$ |
| Closed-loop BW | $f_{CL} = \beta \cdot f_{unity}$ |

---

## Quick Reference: What Affects What?

### To Increase Gain:
- Use cascode (squares the gain)
- Increase $r_{ds}$ (longer L, lower current)
- Use current mirror OTA (adds factor K)

### To Increase Bandwidth:
- Decrease output resistance (but hurts gain!)
- Decrease load capacitance
- Increase $g_m$ (more current)

### To Increase Output Swing:
- Use folded cascode instead of telescopic
- Use wide-swing current mirrors
- Minimize $V_{eff}$ (but hurts speed)

### To Decrease Power:
- Lower bias currents (but hurts $g_m$ and speed)
- Use smaller $V_{eff}$ (but hurts swing)

---

## Common Mistakes to Avoid

> [!warning] Mistake 1: Forgetting the GBW trade-off
> You can't have high gain AND high bandwidth. Pick one, or use multi-stage designs cleverly.

> [!warning] Mistake 2: Ignoring output swing
> Cascode gives great gain but terrible swing. Check that your output can actually reach the needed voltage range!

> [!warning] Mistake 3: Simple mirror with cascode stage
> A simple current mirror ($r_{out} = r_{ds}$) wastes the high impedance of a cascode stage. Always match impedances!

> [!warning] Mistake 4: Forgetting stability
> Two-stage designs NEED compensation. Without it, your amplifier will oscillate.

---

## Next Steps

1. **Work through the exercises** - they build intuition for the numbers
   - [[Problem 1 - Amplifier Configurations]] - Compare CS, cascode, cascade
   - [[Problem 2 - Advanced OpAmps]] - Current mirrors, OTA design

2. **Review the detailed notes** for derivations
   - [[Lecture 1 - Introduction and Prerequisites]]
   - [[Lecture 2 - Advanced OpAmps]]

3. **Start the Cadence simulations** - seeing the frequency response plots helps a lot!

---

> [!quote] The Key Insight
> Everything in analog design is a trade-off. Your job is to find the best compromise for your specifications. There's no "best" topology - only the best one for your application.

---

> [!nav]
> [[Lecture 4 - Noise|← Lecture 4]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
