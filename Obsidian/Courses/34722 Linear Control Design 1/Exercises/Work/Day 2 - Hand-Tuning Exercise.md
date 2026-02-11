# Day 2 - Hand-Tuning Exercise

> [!abstract] Exercise Overview
> Select the gains of a P and PI controller for a DC motor system (voltage to position) using hand-tuning and the Ziegler-Nichols method.
> Reference: [[Lesson 2 - Block Diagrams and Control Concepts]]

> [!info] Files
> - Simulink model: DC motor (voltage → angular position)
> - MATLAB script: `Day2_HandTuning.m`
> - Tunable block: "P/PI controller" (`K_P` and `K_I_gain`)

---

## Requirements

Given a Simulink model of a DC motor (voltage to position):

1. Find appropriate values for a **P controller** ($K_p$) and a **PI controller** ($K_p$, $\tau_i$)
2. For each case, plot the results in a **2×1 subplot grid**:
   - **Top**: Angular position + position reference
   - **Bottom**: Applied voltage

---

## 1. Hand-Tuning — Disturbance OFF

> [!note] Setup
> `Load = 0`, `K_I_gain = 0` (P-only). Re-run each section with `Ctrl+Enter`.

### Part 1a: Find K_P for ~6s settling time

- `K_P = 0.1` → unstable, system diverges ($10^8$ rad)
- `K_P = 0.001` → still unstable
- `K_P = 0.0001` → stable but very slow (only 0.15 rad after 20s)
- **`K_P = 0.008`** → reaches ref ~6s, no overshoot

![[ex2_part1a_P_6s.png]]

### Part 1b: Find K_P for ~2.5s settling, overshoot ≤2%

- `K_P = 0.02` → ~5% overshoot, oscillations — too high
- `K_P = 0.019` → still ~3-4% overshoot
- **`K_P = 0.015`** → ~1-2% overshoot, settles ~3-4s — good compromise

> [!tip] Tuning approach
> - If too slow → increase `K_P`
> - If overshoot > 2% → decrease `K_P` slightly
> - Target: settling ~2.5s, overshoot ≤2%

![[ex2_part1b_P_fast.png]]

---

## 2. Hand-Tuning — Disturbance ON

> [!note] Setup
> `Load = 0.0001` (torque disturbance stepped at $t = 10$ s), `t_f = 30`.

### Part 2a: P-only with disturbance

- `K_P = 0.008`, `K_I_gain = 0` — P-only tracks ref well until t=10s
- At t=10s the load disturbance hits → position drifts to ~5 rad
- The P controller **cannot reject a constant disturbance** → large steady-state error

![[ex2_part2a_P_with_load.png]]

### Part 2b: PI-controller with disturbance

- `K_P = 0.008`, `tau_i = 5` (`K_I_gain = 0.2`)
- Reference tracking t=1-10s works well (same as P-only)
- After disturbance at t=10s: position spikes to ~4 rad but I-action pulls it back
- By t=30s position returns close to reference — **disturbance rejected**

> [!warning] Overshoot
> Large overshoot (~3 rad) after disturbance, but the exercise notes this may not be avoidable. The key result: PI **eliminates steady-state error** unlike P-only.

![[ex2_part2b_PI_with_load.png]]

---

## 3. Ziegler-Nichols — Disturbance OFF/ON

### Part 3a: Find K_u (sustained oscillations)

- Start from `K_P = 0.008`, `K_I_gain = 0`, `Load = 0`
- **Gradually increase** `K_P` until the system shows **sustained oscillations**
- **`K_u = 0.0483`** — constant-amplitude oscillations around the reference
- **`P_u ≈ 1.0 s`** — measured period between peaks

> [!tip] Finding K_u
> - Oscillations **decay** → $K_p$ is below $K_u$, increase it
> - Oscillations **grow** → $K_p$ is above $K_u$, decrease it
> - Oscillations **constant amplitude** → you found $K_u$
> - Measure **period** $P_u$ = time between two peaks

![[ex2_part3a_finding_Ku.png]]

### Ziegler-Nichols calculated parameters

With $K_u = 0.0483$ and $P_u = 1.0$ s, the script auto-calculates:

| Controller | $K_p$ | $T_i$ | $T_d$ |
|------------|--------|--------|--------|
| P | $0.5 \times 0.0483 = 0.0242$ | — | — |
| PI | $0.45 \times 0.0483 = 0.0217$ | $\frac{1.0}{1.2} = 0.83$ s | — |
| PID | $0.6 \times 0.0483 = 0.0290$ | $0.5 \times 1.0 = 0.50$ s | $0.125 \times 1.0 = 0.125$ s |

### Part 3b: Z-N P-Controller (Load OFF)

- `K_P = 0.0242` (Z-N P), `K_I_gain = 0`, `Load = 0`
- Oscillatory response with ~5-10% overshoot, settles by ~6s
- **Tracks the reference** — no steady-state error without disturbance
- More oscillatory than hand-tuned P (Z-N aims for quarter-decay ratio)

> [!note] Is $\tau_i$ necessary?
> Without disturbance, the P controller tracks the reference with no steady-state error. However, the response is more oscillatory than the hand-tuned version. The I-term is not strictly needed for reference tracking here.

![[ex2_part3b_ZN_P_no_load.png]]

### Part 3c: Z-N P-Controller (Load ON)

- `K_P = 0.0242`, `K_I_gain = 0`, `Load = 0.0001`
- Tracks reference well until t=10s
- After disturbance: position spikes to ~2.7 rad, settles at ~2.3 rad
- **P-only cannot reject** the constant disturbance → large steady-state error (~1.3 rad)

![[ex2_part3c_ZN_P_with_load.png]]

### Part 3d: Z-N PI-Controller (Load ON)

- `K_P = 0.0217`, `tau_i = 0.83` (`K_I_gain = 1.20`), `Load = 0.0001`
- Initial response more oscillatory than hand-tuned (~40% overshoot to ~1.4 rad)
- After disturbance at t=10s: position spikes to ~2.7 rad
- **I-action pulls position back** to reference by ~20s — **disturbance rejected**

> [!success] Z-N PI vs Hand-Tuned PI
> Both reject the disturbance. The Z-N PI is more aggressive (faster tau_i = 0.83 vs 5.0), causing more oscillation but faster disturbance rejection (~20s vs ~30s).

![[ex2_part3d_ZN_PI_with_load.png]]

---

## Results

### Part 1 — P Controller (No Disturbance)

| $K_p$ | Settling Time | Overshoot | Steady-State Error | Notes |
|--------|---------------|-----------|-------------------|-------|
| 0.1 | N/A | N/A | N/A | Unstable — system diverges |
| 0.0001 | >20 s | 0% | ~85% | Stable but way too slow |
| 0.008 | ~6 s | ~0% | ~0% | Target 1a achieved |
| 0.02 | ~4 s | ~5% | ~0% | Too much overshoot |
| 0.015 | ~3-4 s | ~1-2% | ~0% | Target 1b achieved |

### Part 2 — With Disturbance

| $K_p$ | $\tau_i$ | Controller | Disturbance Rejection | Notes |
|--------|----------|------------|----------------------|-------|
| 0.008 | inf | P-only | Cannot reject | Drifts to ~5 rad after load |
| 0.008 | 5 | PI | Returns to ref ~30s | ~3 rad overshoot after load |

### Part 3 — Ziegler-Nichols

| Parameter | Value |
|-----------|-------|
| $K_u$ (ultimate gain) | 0.0483 |
| $P_u$ (ultimate period) | ~1.0 s |
| Z-N $K_p$ (P) | 0.0242 |
| Z-N $K_p$ (PI) | 0.0217 |
| Z-N $T_i$ (PI) | 0.83 s |

| Test | Controller | Load | Tracks Ref? | Disturbance Rejection | Notes |
|------|-----------|------|-------------|----------------------|-------|
| 3b | Z-N P | OFF | Yes | N/A | ~5-10% overshoot, settles ~6s |
| 3c | Z-N P | ON | Until t=10s | Cannot reject | Drifts to ~2.3 rad (1.3 rad error) |
| 3d | Z-N PI | ON | Yes | Returns to ref ~20s | ~2.7 rad spike, faster rejection than hand-tuned |
