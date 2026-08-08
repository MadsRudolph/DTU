---
type: reference
tags: [DSP, reexam, reference, z-transform, LTI]
aliases:
  - LTI canonical
  - Canonical LTI problem
  - z-transform flow
---
# LTI z-transform flow -- diff eq to h[n]

> [!info] What this note is
> The canonical "Eksamensopgave 1" pattern that appears on **every** past DSP exam. One difference equation, five sub-questions, all hanging off H(z).
>
> Running example: **F20 Problem 1.** Read top to bottom once. Then use as lookup during exams.

> [!tip] Can't do the math by hand on the day? → [[Q1 via MATLAB cookbook]]
> Every Q1 sub-type mapped to exact MATLAB commands + the Danish `Svar` to write. Has a **panic protocol** for when you're fully stuck. A computed answer + stated method beats a blank.

---

## The problem template

Every exam has a problem with this 5-step arc:

1. Find **H(z)** from the difference equation
2. Find **poles, zeros, pole-zero plot, stability**
3. Find the **impulse response h[n]**
4. Find the **output y[n]** for a given input x[n]
5. Find **energy** (or a similar summing property)

## Running example (F20 P1)

$$y[n] + 0.1\,y[n-1] - 0.06\,y[n-2] \;=\; x[n] + 0.2\,x[n-1]$$

---

# Step 1 -- Difference equation to H(z)

## The only tool you need

$$\boxed{\;x[n-k] \;\longleftrightarrow\; z^{-k}\,X(z)\;}$$

In words: a k-sample delay in time = multiplication by $z^{-k}$ in the z-domain.

### Why (one-line proof)

$$\sum_{n} x[n-k]\,z^{-n} \;\stackrel{m=n-k}{=}\; z^{-k}\sum_{m} x[m]\,z^{-m} \;=\; z^{-k}\,X(z)$$

## Recipe

1. z-transform **both sides**, term by term.
2. Every `y[n-k]` becomes `z^(-k) Y(z)`. Every `x[n-k]` becomes `z^(-k) X(z)`.
3. Collect all Y on the left, all X on the right.
4. Factor out Y(z) and X(z).
5. H(z) = Y(z) / X(z) = (X-side polynomial) / (Y-side polynomial).

**Mnemonic:** numerator comes from the x side, denominator from the y side.

## Worked -- F20 P1-1

### Transform term by term

| Original term | z-transform |
|---|---|
| $y[n]$ | $Y(z)$ |
| $0.1\,y[n-1]$ | $0.1\,z^{-1}\,Y(z)$ |
| $-0.06\,y[n-2]$ | $-0.06\,z^{-2}\,Y(z)$ |
| $x[n]$ | $X(z)$ |
| $0.2\,x[n-1]$ | $0.2\,z^{-1}\,X(z)$ |

### Sum both sides

$$Y(z) + 0.1\,z^{-1}Y(z) - 0.06\,z^{-2}Y(z) \;=\; X(z) + 0.2\,z^{-1}X(z)$$

### Factor

$$\bigl(1 + 0.1\,z^{-1} - 0.06\,z^{-2}\bigr)\,Y(z) \;=\; \bigl(1 + 0.2\,z^{-1}\bigr)\,X(z)$$

### Divide

$$\boxed{\;H(z) \;=\; \frac{1 + 0.2\,z^{-1}}{1 + 0.1\,z^{-1} - 0.06\,z^{-2}}\;}$$

---

# Step 2 -- Poles, zeros, stability

## Definitions

| Term | Meaning | How to find |
|---|---|---|
| **Zero** | Value of z where $H(z) = 0$ | Root of the numerator |
| **Pole** | Value of z where $H(z) \to \infty$ | Root of the denominator |

## Trap: z vs z^(-1) form

> [!danger] Always convert to z form before reading off roots.
> Reading roots directly off the z^(-1) form **misses zeros/poles at z = 0**.

## Recipe: convert z^(-1) form to z form

Multiply top and bottom by $z^k$ where $k$ = highest power of $z^{-1}$ present.

### Worked -- F20

$k = 2$ (because of $z^{-2}$ in the denominator):

$$H(z) \;=\; \frac{1 + 0.2 z^{-1}}{1 + 0.1 z^{-1} - 0.06 z^{-2}} \cdot \frac{z^{2}}{z^{2}} \;=\; \frac{z^{2} + 0.2\,z}{z^{2} + 0.1\,z - 0.06}$$

Factor both:

$$H(z) \;=\; \frac{z\,(z + 0.2)}{(z + 0.3)(z - 0.2)}$$

Read off:

- **Zeros:** $z = 0$ and $z = -0.2$  *(two zeros -- the one at origin only appears after converting to z form)*
- **Poles:** $z = -0.3$ and $z = 0.2$

---

## Factoring a quadratic denominator

Two methods. Pick whichever suits the numbers.

### Method A -- Quadratic formula

For $az^{2} + bz + c = 0$:

$$z \;=\; \frac{-b \pm \sqrt{b^{2} - 4ac}}{2a}$$

**Applied to F20** ($z^{2} + 0.1 z - 0.06 = 0$):

1. Identify coefficients: $a = 1$, $b = 0.1$, $c = -0.06$.
2. Discriminant:

$$b^{2} - 4ac \;=\; (0.1)^{2} - 4(1)(-0.06) \;=\; 0.01 + 0.24 \;=\; 0.25$$

3. Square root: $\sqrt{0.25} = 0.5$.
4. Plug in:

$$z \;=\; \frac{-0.1 \pm 0.5}{2}$$

5. Two roots:

$$z \;=\; \frac{0.4}{2} = 0.2 \quad\text{or}\quad z \;=\; \frac{-0.6}{2} = -0.3$$

6. Factored form:

$$z^{2} + 0.1 z - 0.06 \;=\; (z - 0.2)(z + 0.3)$$

---

### Method B -- Match coefficients

Assume the factored form and expand:

$$(1 + a\,z^{-1})(1 + b\,z^{-1}) \;=\; 1 + (a+b)\,z^{-1} + ab\,z^{-2}$$

Then find $a, b$ that make the coefficients match. Fast when numbers are "nice."

**Applied to F20** (denominator $1 + 0.1 z^{-1} - 0.06 z^{-2}$):

1. Match the $z^{-1}$ coefficient:

$$a + b \;=\; 0.1$$

2. Match the $z^{-2}$ coefficient:

$$a \cdot b \;=\; -0.06$$

3. Try $a = 0.3$, $b = -0.2$.

4. Sum check:

$$0.3 + (-0.2) \;=\; 0.1 \;\checkmark$$

5. Product check:

$$0.3 \cdot (-0.2) \;=\; -0.06 \;\checkmark$$

6. Factored form:

$$1 + 0.1 z^{-1} - 0.06 z^{-2} \;=\; (1 + 0.3 z^{-1})(1 - 0.2 z^{-1})$$

---

## Pole-zero plot conventions

On the complex plane:

- Draw the **unit circle** (radius 1, centered at origin)
- Mark **zeros** as `o`
- Mark **poles** as `x`
- Horizontal axis = real part, vertical axis = imaginary part

F20: all four points sit on the real axis, all inside the unit circle.

## Causal stability rule

**Step 1 -- check causality** from the difference equation.

Causal = y[n] depends only on present and past samples. All $y[n-k]$ and $x[n-k]$ must have $k \ge 0$. F20 satisfies this.

**Step 2 -- apply the stability rule.**

> [!important] Stability (causal system)
> Stable iff **every** pole $z_p$ satisfies $|z_p| < 1$ (strictly inside the unit circle).

F20:

| Pole       | $     | z_p | $   | Inside unit circle? |
| ---------- | ----- | --- | --- | ------------------- |
| $z = -0.3$ | $0.3$ | yes |     |                     |
| $z = +0.2$ | $0.2$ | yes |     |                     |

**Verdict: stable.**

## MATLAB

```matlab
b = [1, 0.2];         % numerator (z^-1 form)
a = [1, 0.1, -0.06];  % denominator

% Zeros, poles, gain -- tf2zpk includes zeros at z = 0
[z_all, p_all, k] = tf2zpk(b, a);

% Pole-zero plot with unit circle
zplane(b, a);

% Stability test
isstable(tf(b, a, -1))
```

---

# Step 3 -- Impulse response h[n] via partial fractions

> [!warning] Documented weak spot.
> This is the part that cost you points on E25. Move slowly. Every sign matters.

## Big picture

$$h[n] \;=\; \mathcal{Z}^{-1}\{H(z)\}$$

Don't compute from the integral definition. Use a **table** of known pairs. Strategy: split H(z) into pieces that each match a table entry.

## The one table entry you need

$$\boxed{\;a^{n}\,u[n] \;\longleftrightarrow\; \frac{1}{1 - a\,z^{-1}}\,,\quad \text{ROC: } |z| > |a|\;}$$

## What PFD actually is

**Partial fraction decomposition is the reverse of adding fractions.**

You already know how to add fractions:

$$\frac{1}{2} + \frac{1}{3} \;=\; \frac{3}{6} + \frac{2}{6} \;=\; \frac{5}{6}$$

You put them over a common denominator. Easy direction.

**PFD is the opposite:** given $\tfrac{5}{6}$, split it back into $\tfrac{1}{2} + \tfrac{1}{3}$. One big fraction -> sum of smaller fractions.

> Analogy: think of it like a chord. C major = C + E + G. You can't play a chord "as a chord" on a single-note instrument, but you can play each note in turn. PFD decomposes the chord into its notes.

## Why we do it in DSP

The z-transform table only has entries for **simple** fractions like $\tfrac{1}{1 - a z^{-1}}$. Your H(z) is one big fraction -- no table entry matches. Decompose it into pieces that each match an entry, look up each piece, and sum.

---

## The method (full algebra, no shortcuts)

Walk through a plain-algebra example first, then apply to F20. Same mechanic both times.

### Plain-algebra example

Given:

$$\frac{3x + 1}{(x-1)(x+3)}$$

Two factors in the denominator -> split into two pieces, one per factor:

$$\frac{3x + 1}{(x-1)(x+3)} \;=\; \frac{A}{x - 1} + \frac{B}{x + 3}$$

**(1) Combine the RHS back** over a common denominator:

$$\frac{A}{x-1} + \frac{B}{x+3} \;=\; \frac{A(x+3) + B(x-1)}{(x-1)(x+3)}$$

**(2) Equate numerators** with the original (denominators already match):

$$3x + 1 \;=\; A(x+3) + B(x-1)$$

**(3) Plug in clever x values to kill terms.** This equation holds for every $x$, so pick values that zero one term and leave the other standing alone.

Plug in $x = 1$ (zeros the B term):

$$3(1) + 1 \;=\; A(1 + 3) + B(0)$$

$$4 \;=\; 4A \;\Rightarrow\; A = 1$$

Plug in $x = -3$ (zeros the A term):

$$3(-3) + 1 \;=\; A(0) + B(-3 - 1)$$

$$-8 \;=\; -4B \;\Rightarrow\; B = 2$$

**Result:**

$$\frac{3x + 1}{(x-1)(x+3)} \;=\; \frac{1}{x-1} + \frac{2}{x+3}$$

**That's the whole method.** Split -> combine back -> equate -> plug in clever values -> solve.

---

## Applying to F20

Exactly the same method, just in $z^{-1}$.

### Step 3a -- Set up the PFD

Two factors in the denominator -> two pieces:

$$H(z) \;=\; \frac{1 + 0.2\,z^{-1}}{(1 + 0.3\,z^{-1})(1 - 0.2\,z^{-1})} \;=\; \frac{A}{1 + 0.3\,z^{-1}} + \frac{B}{1 - 0.2\,z^{-1}}$$

### Step 3b -- Combine back and equate numerators

Combine the RHS over the common denominator:

$$\frac{A(1 - 0.2\,z^{-1}) + B(1 + 0.3\,z^{-1})}{(1 + 0.3\,z^{-1})(1 - 0.2\,z^{-1})}$$

Equate numerators with the original:

$$\boxed{\;1 + 0.2\,z^{-1} \;=\; A(1 - 0.2\,z^{-1}) + B(1 + 0.3\,z^{-1})\;} \quad (*)$$

Now plug in clever $z^{-1}$ values to kill one term at a time.

### Step 3c -- Find A (kill the B term)

The B term has factor $(1 + 0.3\,z^{-1})$. Set it = 0:

$$1 + 0.3\,z^{-1} = 0 \;\Rightarrow\; z^{-1} = -\tfrac{10}{3}$$

Plug $z^{-1} = -\tfrac{10}{3}$ into equation (*).

**LHS:**

$$1 + 0.2 \cdot \left(-\tfrac{10}{3}\right) \;=\; 1 - \tfrac{2}{3} \;=\; \tfrac{1}{3}$$

**RHS:**

$$A\left(1 - 0.2 \cdot \left(-\tfrac{10}{3}\right)\right) + B\left(1 + 0.3 \cdot \left(-\tfrac{10}{3}\right)\right)$$

$$=\; A\left(1 + \tfrac{2}{3}\right) + B\,(0) \;=\; A \cdot \tfrac{5}{3}$$

**Solve:**

$$\tfrac{1}{3} \;=\; A \cdot \tfrac{5}{3} \;\Rightarrow\; \boxed{\,A = \tfrac{1}{5} = 0.2\,}$$

### Step 3d -- Find B (kill the A term)

The A term has factor $(1 - 0.2\,z^{-1})$. Set it = 0:

$$1 - 0.2\,z^{-1} = 0 \;\Rightarrow\; z^{-1} = 5$$

Plug $z^{-1} = 5$ into equation (*).

**LHS:** $1 + 0.2 \cdot 5 \;=\; 2$

**RHS:** $A(0) + B(1 + 0.3 \cdot 5) \;=\; B \cdot 2.5$

**Solve:** $2 = 2.5\,B \;\Rightarrow\; \boxed{\,B = 0.8\,}$

---

## The cover-up shortcut (once the full method feels solid)

After doing the above a few times, there's a time-saver. Instead of writing out "combine the RHS" and "equate numerators" explicitly, you skip straight to the plug-in:

- **For A:** literally **cover up** the factor $(1 + 0.3 z^{-1})$ in the **original** H(z), then evaluate what's left at $z^{-1} = -\tfrac{10}{3}$.
- **For B:** cover up $(1 - 0.2 z^{-1})$, evaluate what's left at $z^{-1} = 5$.

Same A and B, fewer written lines. Use this only once the full method feels natural -- not before.

---

## Step 3e -- Inverse transform each piece

The table says $\dfrac{1}{1 - a\,z^{-1}} \leftrightarrow a^{n}\,u[n]$. But your pieces may be written with a `+`.

> [!danger] The sign trap
> Always rewrite each factor as $1 - (\ldots) z^{-1}$ **before** reading off $a$.
>
> - $(1 + 0.3 z^{-1}) = 1 - (-0.3) z^{-1}$ so $a = -0.3$ (not $+0.3$)
> - $(1 - 0.2 z^{-1})$ already correct, $a = +0.2$

Apply to each piece:

| PFD piece | Rewrite as $1 - a z^{-1}$ | $a$ | Inverse transform |
|---|---|---|---|
| $\dfrac{0.2}{1 + 0.3 z^{-1}}$ | $\dfrac{0.2}{1 - (-0.3) z^{-1}}$ | $-0.3$ | $0.2\,(-0.3)^{n}\,u[n]$ |
| $\dfrac{0.8}{1 - 0.2 z^{-1}}$ | (already right) | $+0.2$ | $0.8\,(0.2)^{n}\,u[n]$ |

## Result

$$\boxed{\;h[n] \;=\; 0.2\,(-0.3)^{n}\,u[n] \;+\; 0.8\,(0.2)^{n}\,u[n]\;}$$

## Always verify by recombining

Adding the two PFD pieces back should reproduce the original H(z):

$$\frac{0.2\,(1 - 0.2 z^{-1}) + 0.8\,(1 + 0.3 z^{-1})}{(1 + 0.3 z^{-1})(1 - 0.2 z^{-1})}$$

Expand the numerator:

$$=\; \frac{(0.2 + 0.8) + (-0.04 + 0.24)\,z^{-1}}{(1 + 0.3 z^{-1})(1 - 0.2 z^{-1})} \;=\; \frac{1 + 0.2 z^{-1}}{(1 + 0.3 z^{-1})(1 - 0.2 z^{-1})} \;\checkmark$$

**Do this check every time** -- it catches sign errors before they cost you.

## MATLAB

```matlab
[r, p, k] = residuez(b, a);
% r = residues (the A, B coefficients)
% p = poles (the a_i, correct sign baked in)
% k = direct terms (empty if numerator < denominator)
%
% Interpretation: h[n] = sum_i r(i) * p(i)^n * u[n]

% Plot h[n] directly
[h, n] = impz(b, a, 30);
stem(n, h); title('h[n]'); xlabel('n');
```

---

# Step 4 -- Output y[n] for a given x[n]

## Recipe

1. Write $X(z)$ (from the z-transform table).
2. Compute $Y(z) = H(z) \cdot X(z)$.
3. Expand as a single rational in $z^{-1}$.
4. PFD (same method as Step 3).
5. Inverse-transform each piece.

## Typical exam inputs

| x[n] | X(z) | Added pole |
|---|---|---|
| $\delta[n]$ | $1$ | none (so $y[n] = h[n]$) |
| $u[n]$ | $\dfrac{1}{1 - z^{-1}}$ | pole at $z = 1$ |
| $a^{n} u[n]$ | $\dfrac{1}{1 - a z^{-1}}$ | pole at $z = a$ |
| $\cos(\omega_0 n)\,u[n]$ | (see table) | two conjugate poles on unit circle |

## Watch for pole collisions

> [!tip] Collision rules
> - Pole of X(z) matches a **zero** of H(z) -> they cancel, PFD shrinks.
> - Pole of X(z) matches a **pole** of H(z) -> repeated pole.
>
> For repeated poles, use the second table entry:
> $$n\,a^{n}\,u[n] \;\longleftrightarrow\; \frac{a\,z^{-1}}{(1 - a z^{-1})^{2}}$$

## MATLAB

```matlab
nx = 0:30;
x  = (-0.2).^nx;         % x[n] = (-0.2)^n u[n]
y  = filter(b, a, x);    % run the difference equation
stem(nx, y); title('y[n]');
```

---

# Step 5 -- Energy

## Definition

$$E_x \;=\; \sum_{n=-\infty}^{\infty} |x[n]|^{2}$$

## Closed form for $x[n] = a^{n} u[n]$ with $|a| < 1$

$$E_x \;=\; \sum_{n=0}^{\infty} |a|^{2n} \;=\; \frac{1}{1 - |a|^{2}}$$

*(Geometric series sum.)*

## For y[n]

Two options:

1. **Closed form:** get y[n] from Step 4, then sum the geometric-ish series.
2. **Parseval's theorem:**

$$\sum_{n} |y[n]|^{2} \;=\; \frac{1}{2\pi} \int_{-\pi}^{\pi} |Y(e^{j\omega})|^{2}\,d\omega$$

---

# MATLAB toolkit

All Signal Processing Toolbox (you have it).

| Function | Purpose |
|---|---|
| `tf(b, a, -1, 'Variable', 'z^-1')` | Display H(z) as discrete-time TF |
| `roots(p)` | Roots of polynomial vector |
| `tf2zpk(b, a)` | Zeros, poles, gain (includes z=0) |
| `zplane(b, a)` | Pole-zero plot + unit circle |
| `isstable(tf(b, a, -1))` | Stability test (causal) |
| `residuez(b, a)` | Partial fraction decomposition |
| `impz(b, a, N)` | First N samples of h[n] |
| `filter(b, a, x)` | Apply filter to x (runs diff eq) |
| `freqz(b, a, N)` | $H(e^{j\omega})$ at N points |

---

# Quick reference cheat sheet

## Properties

| Property | Time | z-domain |
|---|---|---|
| Linearity | $\alpha x[n] + \beta y[n]$ | $\alpha X(z) + \beta Y(z)$ |
| Shift | $x[n-k]$ | $z^{-k}\,X(z)$ |
| Convolution | $x[n] * h[n]$ | $X(z)\,H(z)$ |
| Modulation | $a^{n}\,x[n]$ | $X(z/a)$ |

## Essential pairs

| x[n]              | X(z)                                   | ROC   |     |      |     |     |
| ----------------- | -------------------------------------- | ----- | --- | ---- | --- | --- |
| $\delta[n]$       | $1$                                    | all z |     |      |     |     |
| $u[n]$            | $\dfrac{1}{1 - z^{-1}}$                | $     | z   | > 1$ |     |     |
| $a^{n}\,u[n]$     | $\dfrac{1}{1 - a z^{-1}}$              | $     | z   | >    | a   | $   |
| $n\,a^{n}\,u[n]$  | $\dfrac{a z^{-1}}{(1 - a z^{-1})^{2}}$ | $     | z   | >    | a   | $   |
| $-a^{n}\,u[-n-1]$ | $\dfrac{1}{1 - a z^{-1}}$              | $     | z   | <    | a   | $   |

## Stability (causal)

All poles $|z_p| < 1$.

## ROC rules

| System | ROC |
|---|---|
| Causal | Outside the outermost pole |
| Anticausal | Inside the innermost pole |
| Two-sided | Ring between two poles |

**Exam default:** assume causal unless told otherwise.

---

# Top 6 traps (the ones that cost points)

1. **Sign on z^(-1) form.**
   $(1 + 0.3 z^{-1})$ is a pole at $a = -0.3$, not $+0.3$.
   Always rewrite as $1 - (\ldots) z^{-1}$ before reading off $a$.

2. **Missing zero/pole at z = 0.**
   Reading roots off z^(-1) form misses origin-located ones.
   Convert to z form first by multiplying top and bottom by $z^{k}$.

3. **PFD algebra slip.**
   Sign errors under time pressure.
   Always verify by recombining the PFD and comparing to the original H(z).

4. **Forgetting $u[n]$.**
   $a^{n}$ alone is defined for all $n$. $a^{n}\,u[n]$ is zero for $n < 0$ (the causal answer).

5. **Repeated poles.**
   Squared factor in denominator -> PFD needs a second term using $n\,a^{n}\,u[n]$.

6. **Unit confusion for poles/zeros.**
   Poles and zeros are values of $z$, not $z^{-1}$.

---

# Links

- [[DSP-Bible]] -- full theory reference
- [[Week 1-4]] -- formula sheet
- [[EXAM PREP]] -- exam-focused overview
- [[62743 Digital Signal Processing (Reexam)]] -- hub
