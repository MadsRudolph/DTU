# Digital Filter Direct Forms — Visual Reference Guide

**A comprehensive guide to identifying and understanding filter structures**

**📷 Course Images Included:**
This guide references official DTU course diagrams showing:
1. FIR basic structure (tapped delay line)
2. FIR linear phase with symmetric coefficients
3. FIR folded structure (exploiting symmetry)
4. IIR Direct Form I (two separate delay chains)
5. FIR vs IIR comparison table

**Image locations:** Save course images as:
- `FIR_Basic_Structure.png` - Basic FIR tapped delay line
- `FIR_Linear_Phase_Equation.png` - 5-tap symmetric FIR equation
- `FIR_Linear_Phase_Structures.png` - Standard vs folded FIR structures
- `IIR_Direct_Form_I.png` - IIR Direct Form I diagram
- `FIR_vs_IIR_Table.png` - Complete comparison table

---

## 📐 Overview

Digital filters can be implemented in different **structural forms** (also called **realizations**). The structure affects memory usage, computational efficiency, and numerical properties, but **NOT** the transfer function H(z).

**Key Point:** Different structures implement the **same** transfer function with different internal signal flow.

---

## 🎯 FIR Filter Structures

### FIR Direct Form (Transversal Structure)

FIR filters have **no feedback** — only feedforward paths from input x[n] to output y[n].

**Transfer function:**
$$H(z) = b_0 + b_1 z^{-1} + b_2 z^{-2} + \cdots + b_M z^{-M} = \sum_{k=0}^{M} b_k z^{-k}$$

**Difference equation:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] = b_0 x[n] + b_1 x[n-1] + \cdots + b_M x[n-M]$$

### FIR Block Diagram

**Standard FIR structure (tapped delay line):**

![[Images/FIR_Basic_Structure.png]]
*Figure 1: FIR Direct Form - M-tap transversal filter structure (from DTU course materials)*

**Description:**
- Input x[n] flows vertically through chain of delay elements (z⁻¹)
- Creates delayed versions: x[n], x[n-1], x[n-2], ..., x[n-M]
- Each tap (delayed signal) is multiplied by coefficient b_k (triangular gain blocks)
- All products summed at adder nodes (+) to produce output y[n]
- **NO feedback paths** (key FIR characteristic)
- M delays for M-th order filter

**Block diagram legend (from course materials):**
- **Product element:** Triangle with b_k label → multiplies signal by coefficient
- **Delay element:** Box with z⁻¹ → delays signal by one sample (x[n] becomes x[n-1])
- **Adder:** Circle with + → sums all inputs

---

### Linear Phase FIR (Symmetric Coefficients)

**5-tap FIR filter example:**

![[Images/FIR_Linear_Phase_Equation.png]]
*Figure 2: Difference equation for 5-tap FIR with linear phase (symmetric coefficients)*

**Three representations shown:**

1. **Standard difference equation:**
   ```
   y[n] = b₀x[n] + b₁x[n-1] + b₂x[n-2] + b₃x[n-3] + b₄x[n-4]
   ```
   Regular FIR: 5 coefficients, 5 multiplications

2. **Symmetric coefficients recognized:**
   ```
   y[n] = b₀x[n] + b₁x[n-1] + b₂x[n-2] + b₃x[n-3] + b₄x[n-4]
   ```
   If **symmetric:** b₀ = b₄, b₁ = b₃ (coefficients mirror around center)

3. **Simplified using symmetry:**
   ```
   y[n] = b₀{x[n] + x[n-4]} + b₁{x[n-1] + x[n-3]} + b₂x[n-2]
   ```
   **Only 3 multiplications!** (reduced from 5)

**Implementation comparison:**

![[Images/FIR_Linear_Phase_Structures.png]]
*Figure 3: Standard vs. Symmetric (folded) FIR structure implementations*

**Left structure (standard implementation):**
- Direct implementation: 5 multipliers
- Each coefficient applied to one tap
- Straightforward but computationally expensive

**Right structure (symmetric/folded implementation):**
- Exploits symmetry: Only 3 multipliers needed!
- Pairs symmetric taps **before** multiplication:
  - {x[n] + x[n-4]} × b₀
  - {x[n-1] + x[n-3]} × b₁
  - x[n-2] × b₂ (center tap, no pairing)
- **More efficient:** Reduces computational load by ~40%
- **Same output:** Mathematically equivalent to left structure

**Key insight:**
- Symmetric coefficients (b₀=b₄, b₁=b₃) → Linear phase
- Pair symmetric taps **before** multiplication → Fewer multipliers
- **Computational savings:** ~50% reduction for symmetric filters

**Why this matters for exams:**
- Symmetric FIR → **Linear phase** (constant group delay)
- Can identify linear phase FIR by checking if h[n] = h[M-n]
- Used in FIR design problems ([[E19 Exam]], [[E20 Exam]], [[E22 Exam]], [[E23 Exam]])

---

### FIR vs IIR Comparison Table

![[Images/FIR_vs_IIR_Table.png]]

**Key differences summary:**

| **Characteristic** | **FIR** | **IIR** |
|-------------------|---------|---------|
| **Output depends on** | Current + past **inputs** only | Current + past inputs **+ past outputs** |
| **Transfer function** | H(z) = Y(z)/X(z) = Σb_k z^(-k) | H(z) = (Σb_k z^(-k))/(1 + Σa_k z^(-k)) |
| **Impulse response** | **Finite** terms (settles after M+1 samples) | **Infinite** terms (never fully settles) |
| **Stability** | **Inherent stable** (no poles except at origin) | **Instability possible** (poles can be outside unit circle) |
| **Phase properties** | **Linear or non-linear** (linear if symmetric) | **Always non-linear** phase |
**Used in:** [[E19 Exam]], [[E20 Exam]], [[E22 Exam]], [[E23 Exam]], [[F23 Exam]]

---

### FIR vs IIR Comparison Summary

**Comprehensive comparison table (from DTU course materials):**

![[Images/FIR_vs_IIR_Comparison.png]]
*Figure 4: Complete characteristics comparison between FIR and IIR filters*

**Key takeaways from table:**

| Characteristic | FIR | IIR |
|----------------|-----|-----|
| **Output dependence** | Current + past **inputs** only | Current + past **inputs** + past **outputs** |
| **Transfer function** | H(z) = Σb_k z^(-k) | H(z) = B(z)/A(z) with denominator |
| **Impulse response** | **Finite** terms | **Infinite** terms |
| **Stability** | **Inherent stable** | **Instability possible** (poles outside unit circle) |
| **Phase properties** | Linear or non-linear | **Always non-linear** |
| **Implementation** | Windowing, frequency sampling | Bilinear transform, impulse invariance |
| **Number of taps** | **Large** (many coefficients) | **Small** (few coefficients) |
| **Computational load** | **High** | **Low** |
| **Robustness** | **Robust** to numerical errors | **Not robust** (rounding accumulation) |

**When to use:**
- **FIR:** Linear phase critical (audio, communications), stability guaranteed, tolerate high computation
- **IIR:** Sharp cutoff with few coefficients, tolerate nonlinear phase, low power/memory

---

## 🔄 IIR Filter Structures

IIR filters have **both feedforward and feedback** paths, resulting in recursive difference equations.

**General transfer function:**
$$H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}} = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}}$$

**General difference equation:**
$$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

Note: Output y[n] depends on **past outputs** y[n-k] (feedback).

---

### Direct Form I

**Structure:** Two separate delay chains (one for input, one for output)

![[Images/IIR_Direct_Form_I.png]]

**Block diagram description:**

**Left side (feedforward/FIR section):**
- Input x[n] flows down through delay chain: x[n] → z⁻¹ → x[n-1] → z⁻¹ → x[n-2] → ... → x[n-M]
- Each tap multiplied by coefficient b_k
- Products feed into adder chain on right

**Right side (feedback/IIR section):**
- Output y[n] flows down through separate delay chain: y[n] → z⁻¹ → y[n-1] → z⁻¹ → y[n-2] → ... → y[n-N]
- Each tap multiplied by coefficient -a_k (note negative sign!)
- Products feed back into adder chain

**Difference equation (as shown in diagram):**
$$y[n] = b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] + \cdots + b_M x[n-M]$$
$$\quad\quad - a_1 y[n-1] - a_2 y[n-2] - \cdots - a_N y[n-N]$$

**Key features:**
- ✅ **Two separate delay lines:** M delays for input (left), N delays for output (right)
- ✅ **Total delays:** M + N (maximum)
- ✅ **Easy to implement** directly from difference equation
- ✅ **Better numerical properties** than Direct Form II (less quantization error)
- ❌ **More memory** than Direct Form II (not canonical)

**Visual identification tips:**
1. Look for **two distinct vertical chains** of z⁻¹ blocks
2. Left chain labeled: x[n], x[n-1], x[n-2], ... (input delays)
3. Right chain labeled: y[n-1], y[n-2], y[n-3], ... (output delays)
4. Coefficients b_k on left (feedforward)
5. Coefficients -a_k on right (feedback, note minus signs!)
6. Both chains feed into central adder column

**How to identify Direct Form I:**
1. Look for **two separate chains** of delay blocks
2. Left side: x[n], x[n-1], x[n-2], ... (input delays)
3. Right side: y[n-1], y[n-2], ... (output delays)
4. Both chains feed into adders

**Difference equation implementation:**
```matlab
% Direct Form I
y[n] = b₀*x[n] + b₁*x[n-1] + b₂*x[n-2] + ... + b_M*x[n-M]
       - a₁*y[n-1] - a₂*y[n-2] - ... - a_N*y[n-N]
```

**Example from** [[F25 Exam]] **Problem 4:**
```
Given block diagram with:
- Left side: x[n] → z⁻¹ → x[n-1] → z⁻¹ → x[n-2] → z⁻¹ → x[n-3]
- Feedforward coefficients: 0.0102, 0.0305, 0.0305, 0.0102
- Right side: y[n-1] ← z⁻¹ ← y[n-2] ← z⁻¹ ← y[n-3]
- Feedback coefficients: 2.0038, -1.4471, 0.3618
- Two separate delay chains → Direct Form I ✓
```

**Used in:** [[E22 Exam]], [[F25 Exam]], [[E21 Exam]]

---

### Direct Form II (Canonical Form)

**Structure:** Single shared delay chain (minimum delays)

```
x[n] ──→ (+) ──→ w[n] ──→ b₀ ──→ (+) ──→ y[n]
         ↑                      ↑
    -a₁ ─┤       z⁻¹     b₁ ───┤
         ↑        ↓             ↑
         ├─── w[n-1]            ↑
         ↑                      ↑
    -a₂ ─┤       z⁻¹     b₂ ───┤
         ↑        ↓             ↑
         ├─── w[n-2]            ↑
         ↑        ↓             ↑
        ...      ...      ...   ↑
         ↑        ↓             ↑
    -a_N ─┘  w[n-N]      b_N ──┘
```

**Key features:**
- ✅ **Single delay chain:** Shared between feedback and feedforward
- ✅ **Minimum delays:** max(M, N) only
- ✅ **Memory-efficient** (canonical = minimum state variables)
- ✅ **Default in MATLAB** `filter()` function
- ❌ **Worse numerical properties** than Direct Form I (quantization errors)

**State variable:** w[n] is the intermediate signal (internal state)

**How to identify Direct Form II:**
1. Look for **single chain** of delay blocks
2. Delays are **shared** between feedback and feedforward paths
3. Feedback coefficients feed into **first** adder
4. Feedforward coefficients feed into **second** adder
5. Fewer total delays than Direct Form I

**Two-step computation:**
```matlab
% Step 1: IIR section (compute state w[n])
w[n] = x[n] - a₁*w[n-1] - a₂*w[n-2] - ... - a_N*w[n-N]

% Step 2: FIR section (compute output y[n])
y[n] = b₀*w[n] + b₁*w[n-1] + b₂*w[n-2] + ... + b_M*w[n-M]
```

**Also known as:**
- Canonical form (minimum number of delays)
- Direct Form II Transposed (when signal flow is reversed)

**Used in:** [[E22 Exam]], [[F25 Exam]]

---

## 📊 Quick Comparison Table

| Feature | FIR | IIR Direct Form I | IIR Direct Form II |
|---------|-----|-------------------|-------------------|
| **Feedback** | None | Yes | Yes |
| **Delay chains** | 1 | 2 (separate) | 1 (shared) |
| **Total delays** | M | M + N | max(M, N) |
| **Memory usage** | Medium | High | Low (minimum) |
| **Stability** | Always stable | Depends on poles | Depends on poles |
| **Linear phase** | Possible | No | No |
| **Numerical properties** | Excellent | Good | Worse (quantization) |
| **Implementation** | Simple | Straightforward | Requires state variable |
| **MATLAB default** | `fir1()`, `fir2()` | Custom | `filter(b, a, x)` |

---

## 🔍 How to Identify Structure on Exam

### Step-by-step identification:

**1. Check for feedback:**
```
NO feedback paths? → FIR
Feedback paths present? → IIR (go to step 2)
```

**2. Count delay chains (IIR only):**
```
Two separate delay chains? → Direct Form I
One shared delay chain? → Direct Form II
```

**3. Verify by counting delays:**
```
Direct Form I: Total delays = M + N
Direct Form II: Total delays = max(M, N)
```

**4. Check structure diagram:**
```
Direct Form I:
- Left side: x[n] delays
- Right side: y[n] delays
- Two separate paths to output adder

Direct Form II:
- Single vertical chain: w[n-k] states
- Feedback coefficients on left
- Feedforward coefficients on right
- Both use same delays
```

---

## 🎯 Exam Strategy

### Quick identification checklist:

**FIR Filter:**
- ☑ No feedback loops
- ☑ Only x[n-k] terms in diagram
- ☑ Denominator = 1
- ☑ Transfer function: H(z) = Σ b_k z^(-k)

**Direct Form I (IIR):**
- ☑ Two separate delay chains visible
- ☑ Left chain: x[n], x[n-1], x[n-2], ...
- ☑ Right chain: y[n-1], y[n-2], ...
- ☑ Total delays = M + N

**Direct Form II (IIR):**
- ☑ Single delay chain
- ☑ State variables w[n], w[n-1], w[n-2], ...
- ☑ Delays shared between paths
- ☑ Total delays = max(M, N)

---

## 💻 MATLAB Implementation

### FIR Filter:
```matlab
% FIR coefficients only
b = [b0, b1, b2, ..., bM];
a = 1;  % No denominator

% Filter signal
y = filter(b, a, x);
```

### IIR Filter (Both Direct Forms):
```matlab
% Both numerator and denominator
b = [b0, b1, b2, ..., bM];
a = [1, a1, a2, ..., aN];

% filter() uses Direct Form II by default
y = filter(b, a, x);
```

**Note:** MATLAB's `filter()` function always uses **Direct Form II Transposed** internally, regardless of how you conceptualize the structure.

---

## 📚 Exam Appearances

**Direct Form identification tested in:**
- [[E21 Exam]] Q4: Cascade form (SOS)
- [[E22 Exam]] Q2: Direct Form I/II identification
- [[F25 Exam]] Q4: Direct Form I diagram
- [[E23 Exam]] Q2: Filter structure from block diagram

**Common exam tasks:**
1. ✅ Identify structure from block diagram
2. ✅ Extract transfer function H(z) from diagram
3. ✅ Write difference equation
4. ✅ Count total delays
5. ✅ Determine FIR vs IIR
6. ✅ Check stability (poles inside unit circle)

---

## ⚡ Quick Reference Card

**Is it FIR or IIR?**
```
No feedback → FIR
Has feedback → IIR
```

**Which IIR Direct Form?**
```
Two delay chains → Direct Form I
One delay chain → Direct Form II
```

**How many delays?**
```
FIR: M delays
Direct Form I: M + N delays
Direct Form II: max(M, N) delays
```

**Memory efficiency:**
```
Most efficient: Direct Form II (minimum delays)
Least efficient: Direct Form I (maximum delays)
```

**Numerical quality:**
```
Best: FIR (no feedback)
Good: Direct Form I (separate chains)
Worse: Direct Form II (shared states)
```

---

**Master these diagrams → Ace structure problems → Better exam results!** 🎯🚀

---

## References

**Course materials:**
- Week 8-9 Lectures: Digital Filter Structures (Lars)
- [[Week 8-11]] Formula Sheet
- [[E19 Exam]] through [[F25 Exam]] - Structure problems

**Key exam problems:**
- F25 Q4: Direct Form I identification
- E22 Q2: Direct Form I/II comparison
- E21 Q4: Cascade structure

---
