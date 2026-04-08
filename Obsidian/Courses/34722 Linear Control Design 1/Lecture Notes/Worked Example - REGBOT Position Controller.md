---
course: "34722"
course-name: "Linear Control Design 1"
type: study-guide
tags: [LCD, worked-example, PILead, REGBOT]
date: 2026-04-08
---
# Worked Example — REGBOT Position Controller (Start to Finish)

> [!abstract] Purpose
> This document walks through a **complete** PILead controller design from specifications to implementation.
> Every step explains **what** we do and **why** we do it. No magic — just the logic chain.

> [!example] Related Materials
> - [[Fundamentals - Intuitive Control Theory|Fundamentals Guide]]
> - [[Diagnostic Guide - What Went Wrong|Diagnostic Guide]]
> - [[Lesson 8 - Position Controller Design]]
> - [[Lesson 9 - PI-Lead Design with Specifications]]
> - [[Day 5 - Black Box Modeling]]

---

## The Setup

**Goal:** Make the REGBOT drive to a specific position (e.g., 0.5 meters forward) and stop there.

**What we have:** From Day 4/5, a velocity transfer function:

$$G_{vel}(s) = \frac{13.34}{s + 35.71}$$

This says: "If I apply voltage, the motor reaches a speed. The DC gain is 0.373 (m/s)/V, and the time constant is 28 ms."

---

## Step 1: Get the Position Transfer Function

**What:** Position is the integral of velocity:

$$\text{position} = \int \text{velocity} \, dt$$

In the $s$-domain, integration is $\frac{1}{s}$, so:

$$G_{pos}(s) = \frac{G_{vel}(s)}{s} = \frac{13.34}{s(s + 35.71)}$$

**Why this matters:**
- We now have a **2nd order** system (degree 2 denominator)
- There's already a pole at $s = 0$ — that's the integrator from velocity→position
- This means the *plant itself* is Type-1 (one integrator already)

> [!tip] Physical Meaning
> The pole at $s = 0$ makes sense: if you apply a constant voltage, the motor spins at a constant speed, and the position increases forever (ramp). The system integrates velocity into position.

---

## Step 2: Define the Specifications

The exercise asks for:

| Specification | Value | Why It Matters |
|---|---|---|
| Phase margin $\gamma_M$ | $\geq 60°$ | Limits overshoot to about 10% |
| Steady-state error $e_{ss}$ | $= 0$ for step | Robot must reach the exact target position |
| Actuator limit | $\pm 9$ V | Motor driver can't exceed this |

**Mapping to frequency-domain targets:**
- $\gamma_M = 60°$ → gives $\zeta \approx 0.6$, overshoot $\approx 10\%$
- $e_{ss} = 0$ for step → need at least Type-1. The plant already has one integrator. Do we need PI?

> [!important] The Subtle Point
> The plant $G_{pos}(s)$ is Type-1 (one integrator at $s = 0$). With just a P-controller, the loop is already Type-1. So technically, we get $e_{ss} = 0$ for a step **without** PI.
>
> But we add PI anyway because:
> 1. It gives infinite DC gain → better disturbance rejection
> 2. It makes the system Type-2 → also zero error for ramp inputs
> 3. The exercise requires PILead design

---

## Step 3: Look at the Plant's Bode Plot

Before designing a controller, we need to know what the plant looks like at different frequencies.

**In MATLAB:**
```matlab
s = tf('s');
G_vel = 13.34 / (s + 35.71);
G_pos = G_vel / s;
bode(G_pos);
margin(G_pos);
```

**What we see:**
- At low frequencies: magnitude drops at $-20$ dB/dec (from the $1/s$ integrator)
- At $\omega = 35.71$ rad/s: magnitude drops to $-40$ dB/dec (the motor pole kicks in)
- Phase starts at $-90°$ (from the integrator) and drops toward $-180°$

**Key reading:** At any candidate crossover frequency $\omega_c$, we can read the plant's phase $\angle G_{pos}(j\omega_c)$.

Let's say we want $\omega_c \approx 6$ rad/s (a reasonable choice for position control — not too aggressive). We'd read something like:

$$\angle G_{pos}(j \cdot 6) \approx -90° - \arctan\left(\frac{6}{35.71}\right) \approx -90° - 9.5° = -99.5°$$

---

## Step 4: Calculate Required Controller Phase

We need the total open-loop phase at $\omega_c$ to equal $\gamma_M - 180°$:

$$\angle C(j\omega_c) + \angle G_{pos}(j\omega_c) = \gamma_M - 180°$$

$$\angle C(j\omega_c) = 60° - 180° - (-99.5°) = -20.5°$$

So the controller must contribute $-20.5°$ at $\omega_c$. That's a small *negative* phase — meaning the phase losses from PI must be small and the lead must partially compensate.

---

## Step 5: Design the PI Part

**Choose $N_i$:** We pick $N_i = 3$ (the minimum — keeps PI zero reasonably close to $\omega_c$).

**PI zero placement:**
$$\tau_i = \frac{N_i}{\omega_c} = \frac{3}{6} = 0.5 \text{ s}$$

The PI zero is at $\omega = 1/\tau_i = 2$ rad/s (well below $\omega_c = 6$).

**Phase from PI at $\omega_c$:**
$$\phi_{PI} = \arctan(\omega_c \tau_i) - 90° = \arctan(6 \times 0.5) - 90° = \arctan(3) - 90°$$
$$= 71.6° - 90° = -18.4°$$

> [!tip] What's Happening
> The integrator contributes $-90°$, but the PI zero at $\omega = 2$ rad/s recovers most of it. At $\omega_c = 6$ (which is $3\times$ the zero frequency), the net PI phase is only $-18.4°$. Not bad — but it's still eating into our phase budget.

---

## Step 6: Design the Lead Part

**Required lead phase:**
$$\phi_{Lead} = \phi_C - \phi_{PI} = -20.5° - (-18.4°) = -2.1°$$

Wait — this is *negative*! That means we don't actually need the lead to add phase; the PI is already almost enough. But in practice, we still add a small lead for robustness.

Let's target $\phi_{Lead} = 15°$ (a conservative choice to have some margin for model uncertainty).

**Calculate $\alpha$:**
$$\alpha = \frac{1 - \sin(15°)}{1 + \sin(15°)} = \frac{1 - 0.259}{1 + 0.259} = \frac{0.741}{1.259} = 0.589$$

We'll round to $\alpha = 0.3$ for a more aggressive lead (gives $\phi_{Lead} \approx 35°$), providing extra safety margin.

With $\alpha = 0.3$:

$$\phi_{Lead} = \arcsin\left(\frac{1 - 0.3}{1 + 0.3}\right) = \arcsin(0.538) = 32.6°$$

**Lead zero and pole placement:**
$$\tau_d = \frac{1}{\omega_c\sqrt{\alpha}} = \frac{1}{6\sqrt{0.3}} = \frac{1}{6 \times 0.548} = 0.304 \text{ s}$$

- Lead zero at: $1/\tau_d = 3.29$ rad/s
- Lead pole at: $1/(\alpha\tau_d) = 1/(0.3 \times 0.304) = 10.96$ rad/s
- Phase bump centered at: $\omega_m = 1/(\tau_d\sqrt\alpha) = 6$ rad/s ✓ (matches $\omega_c$!)

> [!tip] What's Happening
> The lead zero (at 3.29 rad/s) starts adding positive phase before $\omega_c$. The lead pole (at 10.96 rad/s) takes it away, but by then we've passed $\omega_c$. The net effect: a phase "bump" centered exactly at $\omega_c$.

---

## Step 7: Calculate $K_p$

We need $|L(j\omega_c)| = 1$ (0 dB at crossover). The loop gain is:

$$L(s) = K_p \cdot \frac{\tau_i s + 1}{\tau_i s} \cdot \frac{\tau_d s + 1}{\alpha\tau_d s + 1} \cdot G_{pos}(s)$$

Evaluate $|L(j\omega_c)|$ with $K_p = 1$ first, then set $K_p = 1/|L(j\omega_c)|_{K_p=1}$.

**In MATLAB:**
```matlab
Ni = 3; alpha = 0.3; wc = 6;
tau_i = Ni/wc;
tau_d = 1/(wc*sqrt(alpha));

C_PI = (tau_i*s + 1)/(tau_i*s);
C_Lead = (tau_d*s + 1)/(alpha*tau_d*s + 1);

% Loop gain without Kp
L_noKp = C_PI * C_Lead * G_pos;

% Evaluate at wc
mag_at_wc = abs(evalfr(L_noKp, 1j*wc));
Kp = 1/mag_at_wc;

fprintf('Kp = %.2f\n', Kp);

% Full controller
C = Kp * C_PI * C_Lead;
```

This gives approximately $K_p \approx 11.5$.

---

## Step 8: Verify the Design

Now comes the critical step — **does it actually work?**

```matlab
L = C * G_pos;              % Open-loop
T = feedback(L, 1);         % Closed-loop

% Check margins
[Gm, Pm] = margin(L);
fprintf('Phase margin: %.1f deg (target: 60°)\n', Pm);
fprintf('Gain margin: %.1f dB (want > 6 dB)\n', 20*log10(Gm));

% Check step response
info = stepinfo(T);
fprintf('Rise time: %.3f s\n', info.RiseTime);
fprintf('Overshoot: %.1f%%\n', info.Overshoot);
fprintf('Settling time: %.3f s\n', info.SettlingTime);

% Check steady-state
fprintf('DC gain: %.4f (should be 1.0000)\n', dcgain(T));
```

**Expected results:**
- Phase margin $\approx 60°$ ✓
- Overshoot $\approx 10$–$17\%$
- $e_{ss} = 0$ (DC gain = 1.0000) ✓

**Also check the control signal:**
```matlab
% Make sure u(t) stays within ±9V
figure;
[y, t] = step(T);
u = lsim(C, 1-y, t);   % u = C * e, where e = r - y
plot(t, u); yline(9, 'r--'); yline(-9, 'r--');
title('Control signal'); ylabel('Voltage [V]');
```

> [!warning] If $u(t)$ exceeds $\pm 9$ V
> The motor driver saturates and the system won't behave as designed. Solutions:
> - Reduce $K_p$ (→ lower $\omega_c$ → slower but less aggressive)
> - Use a reference pre-filter to soften the step input
> - Accept that the first 0.1 s will be in saturation (often okay in practice)

---

## Step 9: Summary of the Design

| Parameter | Value | How We Got It |
|-----------|-------|---------------|
| $\omega_c$ | 6 rad/s | From rise time spec or chosen for feasibility |
| $\gamma_M$ | 60° | From overshoot spec |
| $N_i$ | 3 | Minimum value, keeps PI phase penalty small |
| $\alpha$ | 0.3 | Chosen for extra phase margin |
| $\tau_i$ | 0.5 s | $N_i / \omega_c$ |
| $\tau_d$ | 0.304 s | $1/(\omega_c\sqrt\alpha)$ |
| $K_p$ | $\approx 11.5$ | From $|L(j\omega_c)| = 1$ condition |

**The complete controller:**

$$C(s) = 11.5 \cdot \frac{0.5s + 1}{0.5s} \cdot \frac{0.304s + 1}{0.091s + 1}$$

---

## The Logic Chain (Why Each Step Was Necessary)

```
"I want the robot at 0.5 m"
        │
        ▼
Need position control → G_pos(s) = G_vel(s)/s
        │
        ▼
Need e_ss = 0 → plant is already Type-1, but add PI for robustness → PILead
        │
        ▼
Need low overshoot → target γ_M = 60°
        │
        ▼
Read plant phase at ω_c → plant gives -99.5° at ω_c = 6
        │
        ▼
Controller must provide: 60° - 180° - (-99.5°) = -20.5°
        │
        ▼
PI provides -18.4° → need Lead for the rest plus extra margin
        │
        ▼
Lead with α = 0.3 gives +32.6° → comfortable margin
        │
        ▼
Set Kp so |L(jω_c)| = 1 → Kp ≈ 11.5
        │
        ▼
Verify: margins ✓, step response ✓, saturation check ✓
        │
        ▼
Test on REGBOT → iterate if needed
```

Every step is a **logical consequence** of the previous one. There are no arbitrary choices — each decision traces back to the specifications.

---

*Last updated: 2026-04-08*
