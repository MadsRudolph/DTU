# Manual Math Problems - Complete Derivation Guide

**Mastering the theoretical/derivation problems that appear before MATLAB sections**

---

## 📋 Table of Contents

- [[#Problem Types Overview]]
- [[#Time-Domain Analysis]]
- [[#Frequency-Domain Analysis]]
- [[#Z-Domain Analysis]]
- [[#Linear Phase Derivations]]
- [[#Common Tricks & Patterns]]
- [[#Step-by-Step Examples]]
- [[#Exam Strategy]]

---

## Problem Types Overview

### What are "Manual Math Problems"?

These are the **first 1-2 sub-problems** in each exam problem that require:
- ✍️ Hand calculations (no MATLAB)
- 📐 Algebraic derivations
- 🧮 Mathematical manipulations
- 📊 Analytical reasoning

**Typical point distribution:**
- Problem X-1: Derive/Calculate something (10-15% of problem points)
- Problem X-2: Show/Prove something (10-15% of problem points)
- Problem X-3+: MATLAB implementation (70-80% of problem points)

**Key insight:** These problems test **understanding**, not just MATLAB skills!

---

### Common Manual Problem Types

| Type | What You're Asked | Tools Needed | Example |
|------|-------------------|--------------|---------|
| **LTI Relations** | Find impulse from step response | First difference | [[E23 Exam]] Q1 |
| **Frequency Response** | Find $H(e^{j\omega})$ from $h[n]$ | DTFT, Euler's identity | [[E22 Exam]] Q1 |
| **Linear Phase** | Show filter has linear phase | Factor out center phase | [[E23 Exam]] Q1 |
| **Transfer Function** | Find $H(z)$ from difference eq | Z-transform properties | [[E21 Exam]] Q2 |
| **Pole-Zero** | Find poles/zeros by hand | Factor or quadratic formula | [[F25 Exam]] Q2 |
| **Stability** | Prove stability analytically | Check if $\|p\| < 1$ | [[E22 Exam]] Q2 |
| **Convolution** | Calculate $y[n] = h[n] * x[n]$ | Time-domain convolution | [[E20 Exam]] Q1 |

---

## Time-Domain Analysis

### 1. LTI Relations: Step → Impulse

**The DTU Way (from [[E23 Exam]] Q1):**

**Given:** Unit step response $y_{step}[n]$  
**Find:** Impulse response $h[n]$

**Method:** **First difference**

$$h[n] = y_{step}[n] - y_{step}[n-1]$$

**Why this works:**
$$y_{step}[n] = h[n] * u[n] = \sum_{k=-\infty}^{\infty} h[k] u[n-k] = \sum_{k=-\infty}^{n} h[k]$$

Taking first difference:
$$y_{step}[n] - y_{step}[n-1] = \sum_{k=-\infty}^{n} h[k] - \sum_{k=-\infty}^{n-1} h[k] = h[n]$$

---

**Example from E23 Q1:**

Given step response:
$$y_{step}[n] = \begin{cases}
0 & n < 0 \\
1 & n = 0 \\
2 & n = 1 \\
3 & n = 2 \\
4 & n \geq 3
\end{cases}$$

Find $h[n]$:

| $n$ | $y_{step}[n]$ | $y_{step}[n-1]$ | $h[n] = y_{step}[n] - y_{step}[n-1]$ |
|-----|---------------|-----------------|--------------------------------------|
| -1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 1 |
| 2 | 3 | 2 | 1 |
| 3 | 4 | 3 | 1 |
| 4 | 4 | 4 | 0 |

**Result:**
$$h[n] = \begin{cases}
1 & 0 \leq n \leq 3 \\
0 & \text{otherwise}
\end{cases}$$

Or: $h[n] = [1, 1, 1, 1]$ for $n = 0, 1, 2, 3$

---

### 2. Convolution by Hand

**Given:** Two finite sequences $h[n]$ and $x[n]$  
**Find:** $y[n] = h[n] * x[n]$

**Method:** Flip and slide

$$y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k]$$

**For finite sequences:**
1. List out $h[k]$
2. Flip $x[k]$ to get $x[-k]$
3. For each $n$, slide $x[n-k]$ and multiply with $h[k]$
4. Sum the products

---

**Example:**

Let $h[n] = [1, 2, 1]$ for $n = 0, 1, 2$  
Let $x[n] = [1, 1]$ for $n = 0, 1$

Find $y[n]$:

**Method 1: Polynomial multiplication**
$$H(z) = 1 + 2z^{-1} + z^{-2}$$
$$X(z) = 1 + z^{-1}$$
$$Y(z) = H(z)X(z) = (1 + 2z^{-1} + z^{-2})(1 + z^{-1})$$
$$= 1 + 2z^{-1} + z^{-2} + z^{-1} + 2z^{-2} + z^{-3}$$
$$= 1 + 3z^{-1} + 3z^{-2} + z^{-3}$$

**Result:** $y[n] = [1, 3, 3, 1]$ for $n = 0, 1, 2, 3$

**Method 2: Tabular method**

```
    h:  1  2  1
    x:  1  1
    ─────────────
    n=0:  1
    n=1:  2  1    → sum = 3
    n=2:  1  2    → sum = 3
    n=3:     1    → sum = 1
```

**Result:** $y[n] = [1, 3, 3, 1]$

---

### 3. Difference Equations

**Given:** Difference equation  
**Find:** Output sequence or transfer function

**Standard form:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**Two approaches:**

#### Approach 1: Direct calculation (for initial conditions)

**Example:** 
$$y[n] = x[n] + 0.5y[n-1]$$

With $x[n] = \delta[n]$ (impulse) and $y[-1] = 0$:

| $n$ | $x[n]$ | $y[n-1]$ | $y[n] = x[n] + 0.5y[n-1]$ |
|-----|--------|----------|---------------------------|
| 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0.5 |
| 2 | 0 | 0.5 | 0.25 |
| 3 | 0 | 0.25 | 0.125 |

**Result:** $h[n] = (0.5)^n u[n]$

#### Approach 2: Z-transform (for general solution)

$$Y(z) = X(z) + 0.5z^{-1}Y(z)$$
$$Y(z)(1 - 0.5z^{-1}) = X(z)$$
$$H(z) = \frac{Y(z)}{X(z)} = \frac{1}{1 - 0.5z^{-1}}$$

---

## Frequency-Domain Analysis

### 1. DTFT of Finite Sequences

**Definition:**
$$H(e^{j\omega}) = \sum_{n=-\infty}^{\infty} h[n] e^{-j\omega n}$$

For finite sequence $h[n] = [h_0, h_1, h_2, \ldots, h_M]$:
$$H(e^{j\omega}) = h_0 + h_1 e^{-j\omega} + h_2 e^{-j2\omega} + \cdots + h_M e^{-j\omega M}$$

---

**Example from E23 Q1:**

Given: $h[n] = [1, 1, 1, 1]$ for $n = 0, 1, 2, 3$

Find: $H(e^{j\omega})$

**Step 1: Write DTFT**
$$H(e^{j\omega}) = 1 + e^{-j\omega} + e^{-j2\omega} + e^{-j3\omega}$$

**Step 2: Factor out center phase** (for linear phase FIR)

Center is at $n = 3/2$, so factor out $e^{-j\omega \cdot 3/2}$:

$$H(e^{j\omega}) = e^{-j3\omega/2} \left[ e^{j3\omega/2} + e^{j\omega/2} + e^{-j\omega/2} + e^{-j3\omega/2} \right]$$

**Step 3: Pair symmetric terms**
$$= e^{-j3\omega/2} \left[ (e^{j3\omega/2} + e^{-j3\omega/2}) + (e^{j\omega/2} + e^{-j\omega/2}) \right]$$

**Step 4: Apply Euler's identity**

Recall: $e^{jx} + e^{-jx} = 2\cos(x)$

$$= e^{-j3\omega/2} \left[ 2\cos(3\omega/2) + 2\cos(\omega/2) \right]$$

$$= 2e^{-j3\omega/2} \left[ \cos(3\omega/2) + \cos(\omega/2) \right]$$

**Result:**
- **Magnitude:** $|H(e^{j\omega})| = 2|\cos(3\omega/2) + \cos(\omega/2)|$
- **Phase:** $\angle H(e^{j\omega}) = -3\omega/2$ (linear!)

---

### 2. Frequency Response from Transfer Function

**Given:** $H(z)$  
**Find:** $H(e^{j\omega})$

**Method:** Substitute $z = e^{j\omega}$

**Example:**
$$H(z) = \frac{1 + z^{-1}}{1 - 0.5z^{-1}}$$

**Frequency response:**
$$H(e^{j\omega}) = \frac{1 + e^{-j\omega}}{1 - 0.5e^{-j\omega}}$$

**To find magnitude and phase:**

**Numerator:**
$$N(e^{j\omega}) = 1 + e^{-j\omega} = e^{-j\omega/2}(e^{j\omega/2} + e^{-j\omega/2}) = 2e^{-j\omega/2}\cos(\omega/2)$$

**Denominator:**
$$D(e^{j\omega}) = 1 - 0.5e^{-j\omega}$$

Magnitude: $|D| = \sqrt{1 - 2(0.5)\cos(\omega) + 0.25} = \sqrt{1.25 - \cos(\omega)}$

**Result:**
$$|H(e^{j\omega})| = \frac{2|\cos(\omega/2)|}{\sqrt{1.25 - \cos(\omega)}}$$

$$\angle H(e^{j\omega}) = -\omega/2 - \angle(1 - 0.5e^{-j\omega})$$

---

### 3. Geometric Sum Formula (Very Useful!)

**For frequency responses like:**
$$H(e^{j\omega}) = \sum_{n=0}^{M} e^{-j\omega n}$$

**Use geometric sum:**
$$\sum_{n=0}^{M} r^n = \frac{1 - r^{M+1}}{1 - r}$$

**With $r = e^{-j\omega}$:**
$$H(e^{j\omega}) = \frac{1 - e^{-j\omega(M+1)}}{1 - e^{-j\omega}}$$

**Then factor and use Euler:**
$$= e^{-j\omega M/2} \frac{\sin(\omega(M+1)/2)}{\sin(\omega/2)}$$

**This is the Dirichlet kernel** - rectangular window spectrum!

---

## Z-Domain Analysis

### 1. Transfer Function from Difference Equation

**Method:** Take Z-transform of both sides

**Example:**
$$y[n] = 0.5x[n] + 0.3x[n-1] - 0.2y[n-1]$$

**Step 1: Z-transform**
$$Y(z) = 0.5X(z) + 0.3z^{-1}X(z) - 0.2z^{-1}Y(z)$$

**Step 2: Collect terms**
$$Y(z) + 0.2z^{-1}Y(z) = 0.5X(z) + 0.3z^{-1}X(z)$$

$$Y(z)(1 + 0.2z^{-1}) = X(z)(0.5 + 0.3z^{-1})$$

**Step 3: Solve for H(z)**
$$H(z) = \frac{Y(z)}{X(z)} = \frac{0.5 + 0.3z^{-1}}{1 + 0.2z^{-1}}$$

---

### 2. Finding Poles and Zeros by Hand

**Given:** $H(z) = \frac{B(z)}{A(z)}$

**Zeros:** Solve $B(z) = 0$  
**Poles:** Solve $A(z) = 0$

---

**Example 1: Simple factoring**

$$H(z) = \frac{1 + z^{-1}}{1 - 0.5z^{-1}}$$

**Zeros:** $1 + z^{-1} = 0 \Rightarrow z = -1$

**Poles:** $1 - 0.5z^{-1} = 0 \Rightarrow z = 0.5$

---

**Example 2: Quadratic formula**

$$H(z) = \frac{1}{1 - 0.5z^{-1} + 0.25z^{-2}}$$

**Multiply by $z^2$:**
$$z^2 - 0.5z + 0.25 = 0$$

**Quadratic formula:**
$$z = \frac{0.5 \pm \sqrt{0.25 - 1}}{2} = \frac{0.5 \pm \sqrt{-0.75}}{2}$$

$$= \frac{0.5 \pm j0.866}{2} = 0.25 \pm j0.433$$

**Check magnitude:**
$$|z| = \sqrt{0.25^2 + 0.433^2} = \sqrt{0.0625 + 0.1875} = 0.5$$

**Complex conjugate poles at $r = 0.5$**

---

### 3. Stability by Hand

**Criterion:** System is stable if **all poles** satisfy $|p| < 1$

**For real poles:** Just check magnitude directly

**For complex poles:** Use $|a + jb| = \sqrt{a^2 + b^2}$

---

**Example:**

Poles: $p_1 = 0.7$, $p_2 = 0.3 + j0.4$, $p_3 = 0.3 - j0.4$

**Check $p_1$:**
$$|p_1| = 0.7 < 1 \quad ✓$$

**Check $p_2, p_3$:** (conjugate pair, same magnitude)
$$|p_2| = \sqrt{0.3^2 + 0.4^2} = \sqrt{0.09 + 0.16} = \sqrt{0.25} = 0.5 < 1 \quad ✓$$

**Conclusion:** All poles inside unit circle → **STABLE** ✓

---

### 4. Partial Fraction Expansion (for Inverse Z-Transform)

**Given:** 
$$H(z) = \frac{1}{(1 - 0.5z^{-1})(1 - 0.3z^{-1})}$$

**Find:** $h[n]$

**Method:** Partial fractions

**Step 1: Set up**
$$H(z) = \frac{A}{1 - 0.5z^{-1}} + \frac{B}{1 - 0.3z^{-1}}$$

**Step 2: Solve for A and B**

Multiply both sides by $(1 - 0.5z^{-1})(1 - 0.3z^{-1})$:
$$1 = A(1 - 0.3z^{-1}) + B(1 - 0.5z^{-1})$$

**Method:** Cover-up rule

For A: Set $z^{-1} = 2$ (makes first denominator zero)
$$1 = A(1 - 0.6) \Rightarrow A = \frac{1}{0.4} = 2.5$$

For B: Set $z^{-1} = 10/3$ (makes second denominator zero)
$$1 = B(1 - 5/3) \Rightarrow B = -1.5$$

**Step 3: Inverse Z-transform**
$$h[n] = 2.5(0.5)^n u[n] - 1.5(0.3)^n u[n]$$

---

## Linear Phase Derivations

### The Standard Linear Phase Proof

**Goal:** Show that symmetric FIR has linear phase

**Given:** $h[n] = h[M-n]$ (symmetric coefficients)

**Find:** Show $\angle H(e^{j\omega}) = -\omega M/2$ (linear in $\omega$)

---

**Step-by-Step Procedure:**

**Step 1: Write frequency response**
$$H(e^{j\omega}) = \sum_{n=0}^{M} h[n] e^{-j\omega n}$$

**Step 2: Factor out center phase**

Center point: $n = M/2$

$$H(e^{j\omega}) = e^{-j\omega M/2} \sum_{n=0}^{M} h[n] e^{-j\omega(n - M/2)}$$

**Step 3: Split sum around center**

$$= e^{-j\omega M/2} \left[ \sum_{n=0}^{M/2-1} h[n] e^{j\omega(M/2 - n)} + h[M/2] + \sum_{n=M/2+1}^{M} h[n] e^{-j\omega(n - M/2)} \right]$$

**Step 4: Use symmetry**

For $n < M/2$: Let $k = M - n$, then $h[n] = h[k]$

The two sums become equal after substitution.

**Step 5: Combine using Euler**

Each pair $e^{j\omega k} + e^{-j\omega k} = 2\cos(\omega k)$

**Result:** Sum is real!

$$H(e^{j\omega}) = e^{-j\omega M/2} \times [\text{real-valued amplitude function}]$$

**Conclusion:**
- **Magnitude:** $|H(e^{j\omega})| = |A(\omega)|$ (real amplitude)
- **Phase:** $\angle H(e^{j\omega}) = -\omega M/2$ (linear!) ✓

---

### Linear Phase Example (E23 Q1 Style)

**Given:** $h[n] = [1, 1, 1, 1]$ for $n = 0, 1, 2, 3$

**Show:** Linear phase

**Solution:**

**Check symmetry:**
- $h[0] = 1 = h[3]$ ✓
- $h[1] = 1 = h[2]$ ✓
- Symmetric! → Will have linear phase

**Frequency response:**
$$H(e^{j\omega}) = 1 + e^{-j\omega} + e^{-j2\omega} + e^{-j3\omega}$$

**Factor out $e^{-j3\omega/2}$:** (center at $M/2 = 3/2$)
$$= e^{-j3\omega/2}[e^{j3\omega/2} + e^{j\omega/2} + e^{-j\omega/2} + e^{-j3\omega/2}]$$

**Pair terms:**
$$= e^{-j3\omega/2}[(e^{j3\omega/2} + e^{-j3\omega/2}) + (e^{j\omega/2} + e^{-j\omega/2})]$$

**Use Euler ($e^{jx} + e^{-jx} = 2\cos x$):**
$$= e^{-j3\omega/2}[2\cos(3\omega/2) + 2\cos(\omega/2)]$$

$$= 2e^{-j3\omega/2}[\cos(3\omega/2) + \cos(\omega/2)]$$

**Result:**
- Real amplitude: $A(\omega) = 2[\cos(3\omega/2) + \cos(\omega/2)]$
- Phase: $\phi(\omega) = -3\omega/2$ ← **Linear!** ✓

**Therefore:** Filter has linear phase with group delay $\tau = 3/2$ samples

---

## Common Tricks & Patterns

### 1. Euler's Identity (Use This Everywhere!)

$$e^{j\omega} = \cos(\omega) + j\sin(\omega)$$

$$e^{-j\omega} = \cos(\omega) - j\sin(\omega)$$

**Adding:**
$$e^{j\omega} + e^{-j\omega} = 2\cos(\omega)$$

**Subtracting:**
$$e^{j\omega} - e^{-j\omega} = 2j\sin(\omega)$$

**This is THE KEY to simplifying frequency responses!**

---

### 2. Complex Magnitude Formula

For $z = a + jb$:

$$|z| = \sqrt{a^2 + b^2}$$

**For denominators in frequency response:**

$$|1 - re^{-j\omega}| = \sqrt{(1-r\cos\omega)^2 + (r\sin\omega)^2}$$

$$= \sqrt{1 - 2r\cos\omega + r^2}$$

---

### 3. Geometric Sum (Rectangular Window Spectrum)

$$\sum_{n=0}^{M} e^{-j\omega n} = \frac{1 - e^{-j\omega(M+1)}}{1 - e^{-j\omega}}$$

**Simplified form:**
$$= e^{-j\omega M/2} \frac{\sin(\omega(M+1)/2)}{\sin(\omega/2)}$$

**This is the Dirichlet kernel!**

---

### 4. First Difference Property

Time domain:
$$y[n] - y[n-1]$$

Z-domain:
$$Y(z)(1 - z^{-1})$$

**Used for:** Step → Impulse conversion

---

### 5. Symmetry Shortcuts

**For symmetric FIR:**
- Always has linear phase
- Magnitude is real-valued function
- Only need to calculate magnitude, phase is $-\omega M/2$

**For antisymmetric FIR:**
- Also linear phase
- But amplitude function involves $j\sin$ terms
- Less common in exams

---

## Step-by-Step Examples

### Example 1: Complete LTI + Linear Phase Problem (E23 Style)

**Given:** Step response
$$y_{step}[n] = [0, 1, 2, 3, 4, 4, 4, \ldots]$$

**Part (a):** Find impulse response $h[n]$

**Solution:**
$$h[n] = y_{step}[n] - y_{step}[n-1]$$

| $n$ | $y_{step}[n]$ | $y_{step}[n-1]$ | $h[n]$ |
|-----|---------------|-----------------|--------|
| 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 1 |
| 2 | 3 | 2 | 1 |
| 3 | 4 | 3 | 1 |
| 4 | 4 | 4 | 0 |

**Answer:** $h[n] = [1, 1, 1, 1]$ for $n = 0, 1, 2, 3$

---

**Part (b):** Find frequency response $H(e^{j\omega})$ and show linear phase

**Solution:**

**Step 1:** DTFT
$$H(e^{j\omega}) = 1 + e^{-j\omega} + e^{-j2\omega} + e^{-j3\omega}$$

**Step 2:** Check symmetry
- $M = 3$, center at $M/2 = 1.5$
- $h[0] = h[3] = 1$ ✓
- $h[1] = h[2] = 1$ ✓
- Symmetric → linear phase

**Step 3:** Factor out center phase $e^{-j3\omega/2}$
$$= e^{-j3\omega/2}[e^{j3\omega/2} + e^{j\omega/2} + e^{-j\omega/2} + e^{-j3\omega/2}]$$

**Step 4:** Pair symmetric terms
$$= e^{-j3\omega/2}[(e^{j3\omega/2} + e^{-j3\omega/2}) + (e^{j\omega/2} + e^{-j\omega/2})]$$

**Step 5:** Apply Euler
$$= e^{-j3\omega/2}[2\cos(3\omega/2) + 2\cos(\omega/2)]$$

$$= 2e^{-j3\omega/2}[\cos(3\omega/2) + \cos(\omega/2)]$$

**Answer:**
- **Magnitude:** $|H(e^{j\omega})| = 2|\cos(3\omega/2) + \cos(\omega/2)|$
- **Phase:** $\angle H(e^{j\omega}) = -3\omega/2$ ← Linear! ✓
- **Group delay:** $\tau = 3/2$ samples

---

### Example 2: Transfer Function + Stability (E22 Style)

**Given:** Difference equation
$$y[n] = x[n] - 0.5y[n-1] + 0.25y[n-2]$$

**Part (a):** Find $H(z)$

**Solution:**

Z-transform:
$$Y(z) = X(z) - 0.5z^{-1}Y(z) + 0.25z^{-2}Y(z)$$

Rearrange:
$$Y(z)[1 + 0.5z^{-1} - 0.25z^{-2}] = X(z)$$

**Answer:**
$$H(z) = \frac{1}{1 + 0.5z^{-1} - 0.25z^{-2}}$$

---

**Part (b):** Find poles and check stability

**Solution:**

**Find poles:** Solve $1 + 0.5z^{-1} - 0.25z^{-2} = 0$

Multiply by $z^2$:
$$z^2 + 0.5z - 0.25 = 0$$

Quadratic formula:
$$z = \frac{-0.5 \pm \sqrt{0.25 + 1}}{2} = \frac{-0.5 \pm \sqrt{1.25}}{2}$$

$$= \frac{-0.5 \pm 1.118}{2}$$

**Poles:**
- $p_1 = \frac{-0.5 + 1.118}{2} = 0.309$
- $p_2 = \frac{-0.5 - 1.118}{2} = -0.809$

**Check stability:**
- $|p_1| = 0.309 < 1$ ✓
- $|p_2| = 0.809 < 1$ ✓

**Answer:** Both poles inside unit circle → **STABLE** ✓

---

### Example 3: Frequency Response Magnitude (F21 Style)

**Given:** 
$$H(z) = \frac{1 + z^{-1}}{1 - 0.8z^{-1}}$$

**Find:** $|H(e^{j\omega})|$ at $\omega = 0$ and $\omega = \pi$

**Solution:**

Substitute $z = e^{j\omega}$:
$$H(e^{j\omega}) = \frac{1 + e^{-j\omega}}{1 - 0.8e^{-j\omega}}$$

---

**At $\omega = 0$:**

$$H(e^{j0}) = \frac{1 + 1}{1 - 0.8} = \frac{2}{0.2} = 10$$

$$|H(e^{j0})| = 10$$

---

**At $\omega = \pi$:**

$$H(e^{j\pi}) = \frac{1 + e^{-j\pi}}{1 - 0.8e^{-j\pi}}$$

Note: $e^{-j\pi} = \cos(\pi) - j\sin(\pi) = -1$

$$= \frac{1 - 1}{1 + 0.8} = \frac{0}{1.8} = 0$$

$$|H(e^{j\pi})| = 0$$

**Answer:**
- DC gain: $|H(e^{j0})| = 10$
- At Nyquist: $|H(e^{j\pi})| = 0$
- This is a lowpass filter!

---

## Exam Strategy

### Time Management

**Typical problem structure:**
- Sub-problem 1: Theory/derivation (10 min)
- Sub-problem 2: More theory (10 min)
- Sub-problems 3-5: MATLAB (40 min)

**Strategy:**
1. **Do theory first** (gets you points even if MATLAB fails)
2. **Show all steps** (partial credit possible)
3. **Check symmetry first** (for linear phase problems)
4. **Use known formulas** (don't re-derive Euler every time)

---

### Common Mistakes to Avoid

❌ **Forgetting to check $n = M/2$ case** in DTFT (avoid 0/0)
❌ **Wrong sign on feedback terms** in difference equations
❌ **Forgetting $z^2$ multiply** when finding poles
❌ **Not checking magnitude** of complex poles
❌ **Dropping $e^{-j\omega M/2}$ phase term** in linear phase
❌ **Confusing $e^{j\omega}$ and $e^{-j\omega}$** in Euler's identity

---

### What Examiners Look For

✅ **Correct method** (even if arithmetic wrong)
✅ **Clear steps** (show your work!)
✅ **Proper notation** ($\Omega$ vs $\omega$, etc.)
✅ **Verification** (check answer makes sense)
✅ **Conclusion statement** ("Therefore filter is stable")

---

### Quick Reference Formulas

**Euler's Identity:**
$$e^{j\omega} + e^{-j\omega} = 2\cos(\omega)$$

**First Difference:**
$$h[n] = y_{step}[n] - y_{step}[n-1]$$

**Complex Magnitude:**
$$|a + jb| = \sqrt{a^2 + b^2}$$

**Stability:**
$$\text{Stable} \Leftrightarrow \text{all } |p_i| < 1$$

**Linear Phase:**
$$h[n] = h[M-n] \Rightarrow \angle H = -\omega M/2$$

**Geometric Sum:**
$$\sum_{n=0}^{M} r^n = \frac{1-r^{M+1}}{1-r}$$

---

## Summary

**Key Takeaways:**

1. **LTI Relations:** First difference converts step → impulse
2. **DTFT:** Sum with exponentials, use Euler to simplify
3. **Linear Phase:** Check symmetry, factor out center phase
4. **Z-Transform:** Standard tool for difference equations
5. **Poles/Zeros:** Solve denominators/numerators
6. **Stability:** Check $|p| < 1$ for ALL poles
7. **Show your work:** Partial credit is real!

**Practice makes perfect!** Work through past exam problems with these techniques.

---

**You now have the tools to tackle ANY manual math problem!** 📐✨🎯
