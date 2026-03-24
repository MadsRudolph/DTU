---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise]
date: 2026-02-18
---
# Day 3 - Block Diagram Exercises

> [!abstract] Exercise Overview
> Block diagram manipulation: reducing block models to transfer functions, converting formulas to block diagrams, and decomposing transfer functions into integrator-chain block diagrams.

> [!info] Files
> - Exercise PDF: [[Exercises_Day3.pdf]]
> - Assignment: [[Assignment_3_BlockDiagrams.pdf]]

> [!example] Related Materials
> - Lecture notes: [[Lesson 3 - Laplace Transform and Transfer Functions]]
> - Slides: [[3_Laplace_TF.pdf|Lecture 3 -- Laplace & Transfer Functions]]
> - Previous exercise: [[Day 2 - Hand-Tuning Exercise]]

---

## Reminder — Transfer Function Format

> [!warning] Required Form
> Reduce to one transfer function $G = \frac{x}{\tau} = \frac{\text{numerator}}{\text{denominator}}$, where:
> - Integration is replaced by $\frac{1}{s}$
> - Numerator and denominator are polynomials in $s$ with **positive powers**
> - No $\frac{1}{s}$ or $s^{-1}$ terms remaining in the final expression

![[3_Laplace_TF.pdf#page=19]]

---

## Exercise 1 — Block Model to Transfer Function

> [!note] Problem
> Block diagram: $u \to \Sigma(+,-) \to G \to \int \to y$, with feedback $y \to H \to (-)\Sigma$
>
> Find $\dfrac{y}{u} = \;?$

### Solution

The forward path (from summing junction to output):

$$\text{Forward} = G \cdot \frac{1}{s} = \frac{G}{s}$$

The loop gain (forward path $\times$ feedback):

$$\text{Loop} = \frac{G}{s} \cdot H = \frac{GH}{s}$$

Applying the closed-loop formula $\frac{\text{Forward}}{1 + \text{Loop}}$ for negative feedback:

$$\frac{y}{u} = \frac{G/s}{1 + GH/s} = \frac{G/s}{(s + GH)/s}$$

$$\boxed{\frac{y}{u} = \frac{G}{s + GH}}$$

> [!tip] Compare with RL Circuit Example (Slide 20)
> This is the same structure as the RL circuit: $V(s) \to \Sigma(+,-) \to [1/L] \to [1/s] \to I(s)$ with feedback through $R$, giving $\frac{I}{V} = \frac{1}{Ls + R}$.

![[3_Laplace_TF.pdf#page=20]]

---

## Exercise 2 — Formula to Block Model

> [!note] Problem
> System with input $\tau$ (torque) and output $x$ (position):
> $$x = R \int \omega \, dt$$
> $$\omega = \int \frac{1}{J}(\tau - B\omega) \, dt$$
>
> Draw a block diagram where summation, multiplication, and integration are separated.

### Solution

**Second equation** (dynamics): $\dot{\omega} = \frac{1}{J}(\tau - B\omega)$

1. Summing junction: $\tau - B\omega$ (torque minus friction)
2. Gain $\frac{1}{J}$: gives $\dot{\omega}$
3. Integrator $\frac{1}{s}$: gives $\omega$
4. Feedback: $\omega$ through gain $B$ to (−) of summing junction

**First equation** (kinematics): $\dot{x} = R\omega$

1. Gain $R$: gives $\dot{x}$
2. Integrator $\frac{1}{s}$: gives $x$

```
                  Dynamics                          Kinematics
        ┌─────────────────────────────┐     ┌──────────────────┐
        │                             │     │                  │
τ ──→ Σ(+,−) ──→ [1/J] ──→ [1/s] ──→ ω ──→ [R] ──→ [1/s] ──→ x
        ↑                        │
        └────── [B] ◄────────────┘
```

> [!tip] Construction Method (from Lecture Slide 12)
> 1. Isolate the highest derivative ($\ddot{x}$ or $\dot{\omega}$)
> 2. Add integrators ($\frac{1}{s}$) — as many as the order of the equation
> 3. Add feedback paths for lower-order terms
> 4. Add inputs and constants as gain blocks

![[3_Laplace_TF.pdf#page=12]]

---

## Exercise 3 — Reduce Block Model to Transfer Function

> [!note] Problem
> Reduce the block diagram from Exercise 2 to one transfer function $x/\tau$.

### Solution

**Step 1: Reduce the inner feedback loop** ($\tau$ to $\omega$)

Forward: $\frac{1}{J} \cdot \frac{1}{s} = \frac{1}{Js}$

Feedback: $B$

$$\frac{\omega}{\tau} = \frac{1/(Js)}{1 + B/(Js)} = \frac{1/(Js)}{(Js + B)/(Js)} = \frac{1}{Js + B}$$

**Step 2: Cascade with the outer path** ($\omega$ to $x$)

$$\frac{x}{\omega} = R \cdot \frac{1}{s} = \frac{R}{s}$$

**Step 3: Total transfer function**

$$\frac{x}{\tau} = \frac{\omega}{\tau} \cdot \frac{x}{\omega} = \frac{1}{Js + B} \cdot \frac{R}{s}$$

$$\boxed{\frac{x}{\tau} = \frac{R}{s(Js + B)}}$$

> [!success] Verification
> - Numerator: $R$ (constant) ✓
> - Denominator: $Js^2 + Bs$ (polynomial with positive powers of $s$) ✓
> - Physical sense: two integrators (position from velocity, velocity from acceleration) give $s^2$ in denominator; friction $B$ provides damping

---

## Exercise 4 — Block Model to Transfer Function

> [!note] Problem
> Block diagram with two parallel forward paths:
> - $u \to \Sigma_1(+,-) \to G \to \Sigma_2(+,+) \to D \to y$
> - Also: $\Sigma_1$ output $\to K \to \int \to \Sigma_2$ (+)
> - Feedback: $y \to \Sigma_1$ (−)
>
> Find $\dfrac{y}{u} = \;?$

### Solution

Let $e = u - y$ (error signal from $\Sigma_1$). Both $G$ and $K \to \frac{1}{s}$ receive $e$:

**At $\Sigma_2$** (parallel paths add):

$$\text{input to } D = Ge + \frac{K}{s}e = e\left(G + \frac{K}{s}\right) = e \cdot \frac{Gs + K}{s}$$

**Output:**

$$y = D \cdot e \cdot \frac{Gs + K}{s}$$

**Substituting** $e = u - y$:

$$y = \frac{D(Gs + K)}{s}(u - y)$$

$$ys + D(Gs + K)y = D(Gs + K)u$$

$$y\left[s + D(Gs + K)\right] = D(Gs + K)u$$

$$\boxed{\frac{y}{u} = \frac{D(Gs + K)}{s + D(Gs + K)} = \frac{D(Gs + K)}{(1 + DG)s + DK}}$$

> [!tip] Structure Insight
> The parallel combination of $G$ (proportional path) and $\frac{K}{s}$ (integral path) forms a **PI-like controller**: $G + \frac{K}{s} = \frac{Gs + K}{s}$. This is exactly how PI controllers appear in block diagrams — a proportional gain in parallel with an integrator.

---

## Exercise 5 — Transfer Function to Block Model

> [!note] Problem
> $$\frac{y}{u} = A \cdot \frac{B}{Cs^2 + Ds + 1}$$
>
> Draw the block diagram with integration and constants ($A$, $B$, $C$, $D$) in separate blocks.

### Solution

Define $q = \frac{u}{Cs^2 + Ds + 1}$ so that $y = ABq$.

From $(Cs^2 + Ds + 1)q = u$, isolate the highest derivative:

$$s^2 q = \frac{1}{C}(u - D \cdot sq - q)$$

$$\ddot{q} = \frac{1}{C}(u - D\dot{q} - q)$$

**Block diagram:**

```
u ──→ Σ(+,−,−) ──→ [1/C] ──→ [1/s] ──→ q̇ ──→ [1/s] ──→ q ──→ [B] ──→ [A] ──→ y
          ↑                                │                  │
          │(−)         [D] ◄───────────────┘                  │
          │             │                                     │
          │(−)          ▼                                     │
          └─────────────+─────────────────────────────────────┘
```

**Signal flow:**
1. Summing: $u - D\dot{q} - q$
2. Gain $\frac{1}{C}$: gives $\ddot{q}$
3. First integrator: $\ddot{q} \to \dot{q}$
4. Second integrator: $\dot{q} \to q$
5. Gains $B$ then $A$: gives $y = ABq$

**Feedback paths:**
- $\dot{q}$ through gain $D$ → (−) of summing junction
- $q$ feeds back directly → (−) of summing junction

> [!tip] Compare with Simulink Example (Slide 47)
> The lecture shows $G(s) = \frac{40}{s^2 + 4s + 40}$ implemented in Simulink as:
> `Step → [40] → Σ(+,−,−) → [1/s] → [1/s] → y`, with feedback gains 4 and 40.
> Exercise 5 follows the exact same pattern!

![[3_Laplace_TF.pdf#page=47]]

> [!success] Verification
> From the diagram: $q = \frac{u}{Cs^2 + Ds + 1}$ and $y = ABq$, so $\frac{y}{u} = \frac{AB}{Cs^2 + Ds + 1}$ ✓

---

## Exercise 6 — Transfer Function to Block Model

> [!note] Problem
> $$\frac{y}{u} = A \cdot \frac{Bs + 1}{Cs + D}$$
>
> Draw the block diagram with integration and constants ($A$, $B$, $C$, $D$) in separate blocks.

### Solution

Define $q = \frac{u}{Cs + D}$ so that $y = A(Bs + 1)q = A(B\dot{q} + q)$.

From $(Cs + D)q = u$, isolate the derivative:

$$sq = \frac{1}{C}(u - Dq) \quad \Rightarrow \quad \dot{q} = \frac{1}{C}(u - Dq)$$

**Block diagram:**

```
                                  ┌─────── [B] ───────┐
                                  │                    ▼
u ──→ Σ(+,−) ──→ [1/C] ──→ q̇ ──→┤──→ [1/s] ──→ q ──→ Σ(+,+) ──→ [A] ──→ y
          ↑                       │               │
          └────────── [D] ◄───────┘───────────────┘
```

**Signal flow:**
1. Summing: $u - Dq$
2. Gain $\frac{1}{C}$: gives $\dot{q}$
3. $\dot{q}$ splits:
   - Through $[B]$ → output summing (+)
   - Through $[1/s]$ → gives $q$
4. $q$ splits:
   - Through $[D]$ → feedback to input summing (−)
   - Direct → output summing (+)
5. Output summing: $B\dot{q} + q$
6. Gain $[A]$: gives $y$

> [!success] Verification
> - $q = \frac{u}{Cs + D}$ and $y = A(Bsq + q) = A(Bs + 1)q$
> - So $\frac{y}{u} = \frac{A(Bs + 1)}{Cs + D}$ ✓

---

## Key Takeaways

> [!abstract] Block Diagram Rules
> 1. **Closed-loop formula:** $\dfrac{y}{u} = \dfrac{\text{Forward}}{1 + \text{Loop gain}}$ (negative feedback)
> 2. **Series blocks** multiply: $G_1 \cdot G_2$
> 3. **Parallel blocks** add: $G_1 + G_2$
> 4. **Integration** → $\frac{1}{s}$, always express result with positive powers of $s$
> 5. **From TF to block diagram:** isolate highest derivative, use integrator chain with feedback
> 6. **From formula to block diagram:** separate summation, multiplication, and integration into individual blocks

![[3_Laplace_TF.pdf#page=11]]

---

> [!nav]
> [[Day 2 - Hand-Tuning Exercise|← Day 2]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
