---
course: "34722"
course-name: "Linear Control Design 1"
type: study-guide
tags: [LCD, diagnostics, troubleshooting]
date: 2026-04-08
---
# Diagnostic Guide — What Went Wrong?

> [!abstract] Purpose
> A quick-lookup guide for when your system isn't behaving as expected. Start with the **symptom** you observe, and follow it to the **cause** and **fix**.
> Use this during exercises, simulations, and REGBOT testing.

> [!example] Related Materials
> - [[Fundamentals - Intuitive Control Theory|Fundamentals Guide]]
> - [[Midterm Cheatsheet]]
> - [[Lesson 8 - Position Controller Design]]
> - [[Lesson 9 - PI-Lead Design with Specifications]]

---

## How to Use This Guide

1. Observe the **symptom** (what does the step response / Bode plot / system look like?)
2. Find the symptom in the table below
3. Read the likely **cause** and **fix**

---

## Symptom Lookup Table

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| System oscillates and never settles | Unstable (poles in RHP) | Reduce $K_p$, add Lead, increase $\gamma_M$ |
| Large overshoot (> 20%) | Low phase margin ($\gamma_M < 45°$) | Add Lead controller, reduce $K_p$ |
| System is very slow (long rise time) | $\omega_c$ too low, gain too low | Increase $K_p$, increase $\omega_c$ target |
| Output never reaches reference (offset) | No integrator in loop (Type-0) | Add I-action (switch to PI or PILead) |
| Output reaches reference but drifts away | Integrator wind-up or marginal stability | Check saturation limits, check pole locations |
| Noisy control signal (chattering motor) | D-action amplifying noise | Increase $\alpha$ (less aggressive lead), lower $\omega_c$ |
| System works in simulation but not on robot | Model mismatch, saturation, delay | Check actuator limits ($\pm 9$ V), re-identify model |
| Bode plot shows negative gain margin | System is already unstable! | Redesign: lower $K_p$ or add more phase |

---

## Detailed Diagnostics

### Problem 1: "My system oscillates"

```
Step Response:
     ╱╲    ╱╲    ╱╲
    ╱  ╲  ╱  ╲  ╱  ╲   ← constant or growing amplitude = UNSTABLE
───╱    ╲╱    ╲╱    ╲──
```

**Ask yourself these questions in order:**

1. **Is it unstable (growing oscillations) or underdamped (decaying oscillations)?**
   - Growing → You have poles in the RHP. Emergency: reduce gain.
   - Decaying but too much → You have complex poles too close to the imaginary axis.

2. **What is the phase margin?**
   - Check with `[Gm, Pm] = margin(L)` in MATLAB
   - $\gamma_M < 30°$ → Almost certainly the problem. Need more phase.
   - $\gamma_M = 45°$–$60°$ → Should be okay. Look elsewhere.

3. **Is the plant model accurate?**
   - Re-check your system identification (Day 5 method)
   - Uncertainty in the model means your real phase margin is less than calculated

**Fixes, in order of preference:**
- Add or increase Lead (adds phase at $\omega_c$)
- Reduce $K_p$ (moves $\omega_c$ down where the plant has more phase)
- Increase $N_i$ (less phase penalty from PI)

---

### Problem 2: "My system has too much overshoot"

```
Step Response:
        ╱──╲
       ╱    ╲
──────╱      ╲────────── reference
     ╱        ╲──────── 
    ╱                    ← overshoot = peak above reference
───╱
```

**Overshoot is directly related to phase margin:**

| Phase Margin $\gamma_M$ | Approximate Overshoot | Damping $\zeta$ |
|---|---|---|
| $75°$ | $\sim 2\%$ | $\sim 0.9$ |
| $65°$ | $\sim 5\%$ | $\sim 0.7$ |
| $55°$ | $\sim 12\%$ | $\sim 0.55$ |
| $45°$ | $\sim 23\%$ | $\sim 0.42$ |
| $35°$ | $\sim 35\%$ | $\sim 0.32$ |

**Fixes:**
- Increase $\gamma_M$ target and redesign
- Move Lead from forward path to feedback path (reduces overshoot at cost of slower rise time — see Day 8-9 results)
- Increase $\alpha$ is **wrong** — that *reduces* lead phase and makes it worse

---

### Problem 3: "My system never reaches the reference"

```
Step Response:
                          ────── reference = 1.0
────────────────────────── output settles at 0.85
                          ← steady-state error = 0.15
```

**This is a Type-n problem.** Check:

1. **How many integrators are in the loop?** Count $1/s$ terms in $L(s) = C(s)G(s)$.
   - Zero integrators (Type-0) → $e_{ss} \neq 0$ for step input. **You need PI.**
   - One integrator (Type-1) → $e_{ss} = 0$ for step. If you still see error, check below.

2. **If you have PI but still see offset:**
   - Is the integrator actually working? Check that $\tau_i$ is reasonable (not extremely large)
   - Is the simulation time long enough? Integrators are slow — run for $10\times$ the settling time
   - Is the actuator saturating? If $u(t)$ hits the $\pm 9$ V limit, the integrator can't push harder

3. **If the reference is a ramp (not step):**
   - Type-1 gives finite error to ramp. You'd need Type-2 for zero ramp error.

---

### Problem 4: "My system is too slow"

```
Step Response:
                                    ────── reference
                          ─────────
                    ─────
              ────── 
────────                  ← takes forever to get there
```

**Slowness = low bandwidth = low $\omega_c$:**

1. **Is $K_p$ too low?** Higher gain pushes $\omega_c$ up → faster response.
2. **Is $N_i$ too high?** Very high $N_i$ makes the PI zero very slow, which can slow the overall response.
3. **Is the Lead in the feedback path?** Lead in feedback reduces bandwidth (see Lesson 9). Try it in the forward path.
4. **Is the plant itself slow?** If $G(s)$ has a pole very close to origin, the system is fundamentally slow. You can increase $\omega_c$ but you'll need more phase compensation.

**The speed formula:** $t_r \approx 1.8 / \omega_c$. If you want $t_r = 0.2$ s, you need $\omega_c \approx 9$ rad/s.

---

### Problem 5: "My MATLAB simulation looks great but the REGBOT doesn't work"

This is the **most common** real-world problem. Causes:

| Issue | How to Check | Fix |
|-------|-------------|-----|
| **Actuator saturation** | Plot $u(t)$. Does it hit $\pm 9$ V? | Reduce $K_p$, accept slower response |
| **Model mismatch** | Compare simulated vs measured step response | Re-identify the plant model (Day 5 method) |
| **Sensor noise** | Look at raw encoder data — is it noisy? | Increase $\alpha$ (filter more), reduce $\omega_c$ |
| **Sampling delay** | Digital controller adds delay at each sample | Adds extra phase lag. Account for it or lower $\omega_c$ |
| **Wrong units** | Radians vs degrees, m/s vs rpm? | Double-check all conversions |
| **Mission script error** | REGBOT not receiving the right commands | Check mission syntax in GUI |

> [!tip] Debug Order
> Always check **saturation first**. If the motor is hitting the voltage rail, no amount of controller tuning will fix the problem — the controller is asking for more than the system can give.

---

### Problem 6: "I don't know where to start designing"

Follow this checklist:

- [ ] **Step 1:** Do I have a plant model $G(s)$? If not → system identification (Day 5)
- [ ] **Step 2:** What are my specs? (Rise time, overshoot, $e_{ss}$)
- [ ] **Step 3:** Map specs to $\omega_c$ and $\gamma_M$ (see [[Fundamentals - Intuitive Control Theory#12. Connecting It All The Design Flow|Fundamentals, Section 12]])
- [ ] **Step 4:** Do I need $e_{ss} = 0$? If yes → need integrator → PI or PILead
- [ ] **Step 5:** Read $\angle G(j\omega_c)$ from Bode plot of plant
- [ ] **Step 6:** Calculate how much phase the controller needs to provide
- [ ] **Step 7:** Can PI alone provide enough? If not → add Lead
- [ ] **Step 8:** Use the phase balance equation to compute parameters
- [ ] **Step 9:** Simulate with `step(feedback(C*G, 1))`
- [ ] **Step 10:** Check margins with `margin(C*G)`

---

## MATLAB Quick Debug Commands

```matlab
%% Check stability margins
[Gm, Pm, Wcg, Wcp] = margin(C*G);
fprintf('Gain margin: %.1f dB\n', 20*log10(Gm));
fprintf('Phase margin: %.1f deg\n', Pm);
fprintf('Crossover freq: %.1f rad/s\n', Wcp);

%% Check closed-loop poles
T = feedback(C*G, 1);
poles = pole(T);
fprintf('Closed-loop poles:\n');
disp(poles);
if all(real(poles) < 0)
    fprintf('✓ System is stable\n');
else
    fprintf('✗ UNSTABLE — poles in RHP!\n');
end

%% Check DC gain (steady-state)
fprintf('Closed-loop DC gain: %.3f\n', dcgain(T));
% Should be 1.000 for zero steady-state error

%% Check step response metrics
info = stepinfo(T);
fprintf('Rise time: %.3f s\n', info.RiseTime);
fprintf('Settling time: %.3f s\n', info.SettlingTime);
fprintf('Overshoot: %.1f%%\n', info.Overshoot);

%% Plot everything
figure;
subplot(2,2,1); step(T); title('Step Response');
subplot(2,2,2); bode(C*G); title('Open-loop Bode');
subplot(2,2,3); nyquist(C*G); title('Nyquist');
subplot(2,2,4); pzmap(T); title('Pole-Zero Map');
```

---

*Last updated: 2026-04-08*
