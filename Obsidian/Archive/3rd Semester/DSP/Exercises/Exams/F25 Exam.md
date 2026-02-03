> Exam set: [[62743 F25 Exam.pdf]]  
> Solution sheet: [[62743 F25 Exam student solutions.pdf]]  
> Matlab document: Open

---

# 62743 — F25 Exam (Digital Signal Processing)

---

## 📘 Big-Picture Overview

This document contains **fully worked solutions** to the **F25 written exam** in 62743 Digital Signal Processing.

For each exam problem, you get:

- A short **context / theory recap** in your own words.
- Full **derivations** with all intermediate steps (not just final answers).
- **MATLAB templates** you can re-use in the exam (copy → adapt parameters).
- Clear tagging of key formulas and interpretations.

Structure:

1. **Problem 1 — LTI systems, impulse response, linear phase FIR**
2. **Problem 2 — IIR Butterworth Highpass via BLT**
3. **Problem 3 — Sampling, aliasing, pole-zero analysis, inverse systems**
4. **Problem 4 — Filter realization, signal filtering**

---

# Problem 1 — LTI Systems, Impulse Response, Linear Phase FIR

> **Given** Two discrete-time input signals $$ x_1[n] = \delta[n] - 2\delta[n-1], \qquad x_2[n] = -\delta[n] + 3\delta[n-1] $$ are applied separately to an unknown **LTI system**. The outputs $y_1[n]$ and $y_2[n]$ are:

|$n$|$<0$|0|1|2|3|4|5|$>5$|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|$y_1[n]$|0|1|0|2|-10|-3|-2|0|
|$y_2[n]$|0|-1|1|0|16|5|3|0|

You are asked to determine:

1. $x_1[n] + x_2[n]$
2. $y_1[n] + y_2[n]$ and verify $h[n]$
3. The **system function** $H(z)$ and frequency response $H(\omega)$
4. **Analytical** magnitude and phase response
5. Combined system with $T_1$, $T_2$, $T_3$

---

## 1-1) Sum of inputs

**Method:** Treat delta functions like basis vectors and collect coefficients.

We add term-by-term: $$ \begin{aligned} x_1[n] + x_2[n] &= \big(\delta[n] - 2\delta[n-1]\big) + \big(-\delta[n] + 3\delta[n-1]\big) \ &= (1-1)\delta[n] + (-2+3)\delta[n-1] \ &= 0 \cdot \delta[n] + 1 \cdot \delta[n-1] \ &= \delta[n-1]. \end{aligned} $$

So $$ \boxed{x_1[n] + x_2[n] = \delta[n-1]} $$

**Key insight:** This tells us that the sum of inputs is a **delayed unit impulse** - this will be critical for finding h[n] in 1-2b!

> [!code]- MATLAB — 1-1
> 
> ```matlab
> %% Spørgsmål 1-1: Beregn x₁[n] + x₂[n]
> % x₁[n] = (+1)·δ[n] + (-2)·δ[n-1]
> % x₂[n] = (-1)·δ[n] + (+3)·δ[n-1]
> %
> % Combining terms:
> %   δ[n]:   1 + (-1) = 0
> %   δ[n-1]: -2 + 3 = 1
> 
> fprintf('Result: x₁[n] + x₂[n] = δ[n-1]\n');
> ```

---

## 1-2a) Sum of outputs

From the table, we add $y_1[n] + y_2[n]$ for each $n$:

|$n$|0|1|2|3|4|5|
|---|---|---|---|---|---|---|
|$y_1[n]$|1|0|2|-10|-3|-2|
|$y_2[n]$|-1|1|0|16|5|3|
|**Sum**|0|1|2|6|2|1|

So $$ \boxed{y_1[n] + y_2[n] = \delta[n-1] + 2\delta[n-2] + 6\delta[n-3] + 2\delta[n-4] + \delta[n-5]} $$

> [!code]- MATLAB — 1-2a
> 
> ```matlab
> %% Spørgsmål 1-2a: Beregn y₁[n] + y₂[n]
> y1 = [1, 0, 2, -10, -3, -2];
> y2 = [-1, 1, 0, 16, 5, 3];
> y_sum = y1 + y2;
> 
> disp('y1 + y2 ='); disp(y_sum);
> % Result: [0, 1, 2, 6, 2, 1]
> 
> fprintf('Result: y₁[n] + y₂[n] = δ[n-1] + 2δ[n-2] + 6δ[n-3] + 2δ[n-4] + δ[n-5]\n');
> ```

---

## 1-2b) Verify the impulse response

> **Critical Insight:** We found in 1-1 that $x_1[n] + x_2[n] = \delta[n-1]$ (a delayed impulse).
> 
> ⚠️ **Common Mistake Alert:** This is NOT a step response problem!
> 
> - We CANNOT use $h[n] = y[n] - y[n-1]$ (that's only for step → impulse)
> - Instead, use **time-invariance** property directly

**Method: Time-Invariance Shift**

1. **From 1-1:** Input was $x_1[n] + x_2[n] = \delta[n-1]$ (delayed impulse)
2. **By linearity:** Output $y_1[n] + y_2[n]$ = system's response to $\delta[n-1]$
3. **By time-invariance:** Response to $\delta[n-1]$ is $h[n-1]$ (delayed impulse response)
4. **Therefore:** $y_1[n] + y_2[n] = h[n-1]$

From 1-2a: $y_1[n] + y_2[n] = \delta[n-1] + 2\delta[n-2] + 6\delta[n-3] + 2\delta[n-4] + \delta[n-5]$

Since this equals $h[n-1]$, **shift all indices left by 1**:

- $\delta[n-1] \to \delta[n]$
- $\delta[n-2] \to \delta[n-1]$
- $\delta[n-3] \to \delta[n-2]$
- etc.

Result: $$ \boxed{h[n] = \delta[n] + 2\delta[n-1] + 6\delta[n-2] + 2\delta[n-3] + \delta[n-4]} $$

✓ This matches the given impulse response!

> [!info] Observation Notice that $h[n]$ is **symmetric**: coefficients are $[1, 2, 6, 2, 1]$.
> 
> - $h[0]=h[4]=1$, $h[1]=h[3]=2$, $h[2]=6$ (center)
> - This is a **Type I linear phase FIR filter** (odd length, symmetric)
> - Will be critical for analytical magnitude/phase in 1-4!

> [!warning] Method Selection Guide **When to use h[n] = y[n] - y[n-1]:**
> 
> - Input is $u[n]$ (unit step function)
> - $y[n]$ is the **step response**
> - Example: [[E23 Exam]], [[E24 Exam]]
> 
> **When to use time-invariance shift (this problem):**
> 
> - Input is $\delta[n-k]$ (delayed impulse)
> - $y[n]$ is response to that delayed impulse
> - Use: $y[n] = h[n-k]$, shift to get $h[n]$

> [!code]- MATLAB — 1-2b verification
> 
> ```matlab
> %% Spørgsmål 1-2b: Eftervis at h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4]
> % We know from 1-1 that input was x₁ + x₂ = δ[n-1]
> % So the output y₁ + y₂ is the impulse response delayed by 1: h[n-1]
> % y₁ + y₂ = 0·δ[n] + 1·δ[n-1] + 2·δ[n-2] + 6·δ[n-3] + 2·δ[n-4] + 1·δ[n-5]
> % This equals h[n-1]
> % To get h[n], we shift everything left by 1 (replace n-1 with n):
> %   term δ[n-1] becomes δ[n]
> %   term δ[n-2] becomes δ[n-1]
> %   ... and so on
> 
> fprintf('Result: h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4]\n');
> 
> % Verify symmetry
> h = [1, 2, 6, 2, 1];
> fprintf('Symmetric filter: %s\n', mat2str(isequal(h, fliplr(h))));
> ```

---

## 1-3a) System function $H(z)$

**Method:** Take Z-transform of impulse response using $\delta[n-k] \xleftrightarrow{Z} z^{-k}$

For a causal FIR filter, the system function is the Z-transform of $h[n]$: $$ \begin{aligned} H(z) &= \sum_{n=0}^{4} h[n] z^{-n} \ &= \delta[n] + 2\delta[n-1] + 6\delta[n-2] + 2\delta[n-3] + \delta[n-4] \ &= 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4} \end{aligned} $$

So $$ \boxed{H(z) = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}} $$

**Properties:**

- **Numerator coefficients:** $b = [1, 2, 6, 2, 1]$ (symmetric!)
- **Denominator:** $a = [1]$ (FIR filter, no feedback)
- **Zeros:** Can be found with `roots(b)` - all must be evaluated
- **Poles:** Only at $z = 0$ (trivial)

> [!code]- MATLAB — 1-3a
> 
> ```matlab
> %% Spørgsmål 1-3a: Angiv systemfunktionen H(z)
> % h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4]
> %
> % Taking Z-transform (using δ[n-k] → z^(-k)):
> %   δ[n]   → 1
> %   2δ[n-1] → 2z^(-1)
> %   6δ[n-2] → 6z^(-2)
> %   2δ[n-3] → 2z^(-3)
> %   δ[n-4] → z^(-4)
> 
> fprintf('Result: H(z) = 1 + 2z^(-1) + 6z^(-2) + 2z^(-3) + z^(-4)\n\n');
> 
> % Define coefficients and display as transfer function
> b = [1, 2, 6, 2, 1];  % Numerator
> a = [1];              % Denominator (FIR)
> Hz = tf(b, a, -1, 'Variable', 'z^-1');
> fprintf('MATLAB transfer function:\n');
> disp(Hz);
> ```

---

## 1-3b) Frequency response $H(\omega)$

**Method:** Substitute $z = e^{j\omega}$ into $H(z)$

The frequency response is obtained by evaluating $H(z)$ on the **unit circle**, $z = e^{j\omega}$: $$ \begin{aligned} H(\omega) &= H(z)\big|_{z=e^{j\omega}} \ &= 1 + 2(e^{j\omega})^{-1} + 6(e^{j\omega})^{-2} + 2(e^{j\omega})^{-3} + (e^{j\omega})^{-4} \end{aligned} $$

Using $(e^{j\omega})^{-k} = e^{-j\omega k}$: $$ \boxed{H(\omega) = 1 + 2e^{-j\omega} + 6e^{-j2\omega} + 2e^{-j3\omega} + e^{-j4\omega}} $$

**Key insight:** The frequency response is **periodic** with period $2\pi$: $$ H(\omega + 2\pi) = H(\omega) $$

> [!code]- MATLAB — 1-3b
> 
> ```matlab
> %% Spørgsmål 1-3b: Angiv frekvensresponset H(ω) = H(z)|_{z=e^{jω}}
> % H(z) = 1 + 2z^(-1) + 6z^(-2) + 2z^(-3) + z^(-4)
> % Substitute z = e^(jω) to get frequency response
> % H(ω) = 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)
> 
> fprintf('Result: H(ω) = 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)\n\n');
> ```

---

## 1-4a) Analytical magnitude and phase

> **Strategy:** Exploit the **symmetry** of $h[n] = [1, 2, 6, 2, 1]$ to factor out a linear phase term.
> 
> **Key observation:** Symmetric coefficients → Linear Phase FIR → Can extract magnitude analytically

For a symmetric FIR filter of length $M+1 = 5$ (so order $M=4$), we can write: $$ H(\omega) = e^{-j\omega M/2} \cdot A(\omega) $$ where:

- $A(\omega)$ is a **real-valued amplitude function**
- $M/2 = 2$ (center of filter)

### Step-by-Step Derivation

**Given:** $$ H(\omega) = 1 + 2e^{-j\omega} + 6e^{-j2\omega} + 2e^{-j3\omega} + e^{-j4\omega} $$

**Step 1: Factor out center phase term $e^{-j2\omega}$**

Factor out $e^{-j2\omega}$ from each term: $$ \begin{aligned} H(\omega) &= e^{-j2\omega} \cdot e^{j2\omega} \cdot 1 \ &\quad + e^{-j2\omega} \cdot e^{j\omega} \cdot 2e^{-j\omega} \ &\quad + e^{-j2\omega} \cdot 6 \ &\quad + e^{-j2\omega} \cdot e^{-j\omega} \cdot 2e^{-j3\omega+j\omega} \ &\quad + e^{-j2\omega} \cdot e^{-j2\omega} \cdot e^{-j4\omega+j2\omega} \end{aligned} $$

Simplifying: $$ H(\omega) = e^{-j2\omega}\Big[e^{j2\omega} + 2e^{j\omega} + 6 + 2e^{-j\omega} + e^{-j2\omega}\Big] $$

**Step 2: Group symmetric terms**

Group exponentials that are conjugate pairs: $$ H(\omega) = e^{-j2\omega}\Big[\underbrace{(e^{j2\omega} + e^{-j2\omega})}_{\text{pair 1}} + \underbrace{2(e^{j\omega} + e^{-j\omega})}_{\text{pair 2}} + 6\Big] $$

**Step 3: Apply Euler's identity**

Use $e^{jk\omega} + e^{-jk\omega} = 2\cos(k\omega)$: $$ \begin{aligned} H(\omega) &= e^{-j2\omega}\Big[2\cos(2\omega) + 2 \cdot 2\cos(\omega) + 6\Big] \ &= e^{-j2\omega}\Big[2\cos(2\omega) + 4\cos(\omega) + 6\Big] \end{aligned} $$

So the **amplitude function** is: $$ \boxed{A(\omega) = 2\cos(2\omega) + 4\cos(\omega) + 6} $$

**Step 4: Verify that A(ω) ≥ 0 for all ω**

Check key points:

- At $\omega = 0$: $A(0) = 2(1) + 4(1) + 6 = 12$ ✓
- At $\omega = \pi$: $A(\pi) = 2(1) + 4(-1) + 6 = 4$ ✓
- At $\omega = \pi/2$: $A(\pi/2) = 2(-1) + 4(0) + 6 = 4$ ✓

Since $-1 \leq \cos(\theta) \leq 1$: $$ A(\omega) \geq 2(-1) + 4(-1) + 6 = 0 $$

Therefore $A(\omega) \geq 0$ for all $\omega$ ✓

### Final Results

**Magnitude response:**

Since $H(\omega) = e^{-j2\omega} \cdot A(\omega)$ and $|e^{-j2\omega}| = 1$: $$ |H(\omega)| = |e^{-j2\omega}| \cdot |A(\omega)| = 1 \cdot |A(\omega)| = |A(\omega)| $$

Because $A(\omega) \geq 0$: $$ \boxed{|H(\omega)| = 2\cos(2\omega) + 4\cos(\omega) + 6} $$

**Phase response:**

Since $A(\omega) > 0$ everywhere (no sign changes): $$ \boxed{\angle H(\omega) = -2\omega} $$

This is **pure linear phase** with:

- **Group delay:** $\tau_g = 2$ samples (constant for all frequencies)
- **Phase delay:** $\tau_p = 2$ samples

> [!warning] Common Mistake Alert! The magnitude is $|A(\omega)|$, **not** $A(\omega)$!
> 
> - If $A(\omega) < 0$ for some $\omega$, then $|H(\omega)| = -A(\omega)$ in that region
> - In this problem, $A(\omega) \geq 0$ everywhere, so $|A(\omega)| = A(\omega)$

> [!info] Why This Works **For symmetric FIR filters:**
> 
> 1. Symmetry forces all imaginary parts to cancel out after factoring
> 2. Only real cosine terms remain: $A(\omega)$ is real-valued
> 3. Phase is purely linear: $-\omega(M/2)$
> 4. This is why they're called "**Linear Phase FIR**" filters
> 
> **Reference:** See [[Week 1-4]], Section 3.3.2 for complete methodology

> [!code]- MATLAB — 1-4a analytical check
> 
> ```matlab
> %% Spørgsmål 1-4a: Beregn |H(ω)| og ∠H(ω) analytisk
> % Given: H(ω) = 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)
> %
> % Step 1: Factor out center phase term e^(-j2ω)
> %   H(ω) = e^(-j2ω) (e^(j2ω) + 2e^(jω) + 6 + 2e^(-jω) + e^(-j2ω))
> %
> % Step 2: Group symmetric terms
> %   H(ω) = e^(-j2ω) [(e^(j2ω) + e^(-j2ω)) + 2(e^(jω) + e^(-jω)) + 6]
> %
> % Step 3: Apply Euler's identity: e^(jθ) + e^(-jθ) = 2cos(θ)
> %   H(ω) = e^(-j2ω) [2cos(2ω) + 4cos(ω) + 6]
> %
> % Step 4: Extract magnitude and phase
> %   Since H(ω) = e^(-j2ω) · A(ω) where A(ω) is real:
> %   |H(ω)| = |A(ω)| and ∠H(ω) = -2ω
> 
> fprintf('Magnitude response:\n');
> fprintf('|H(ω)| = 2cos(2ω) + 4cos(ω) + 6\n\n');
> 
> fprintf('Phase response:\n');
> fprintf('∠H(ω) = -2ω\n\n');
> 
> % Verification
> omega = linspace(-pi, pi, 1024);
> A_omega = 2*cos(2*omega) + 4*cos(omega) + 6;
> fprintf('Min A(omega) = %.4f (should be >= 0)\n', min(A_omega));
> fprintf('Max A(omega) = %.4f\n', max(A_omega));
> ```

---

## 1-4b) Plot magnitude and phase response

**Task:** Plot $|H(\omega)|$ and $\angle H(\omega)$ for $-\pi \leq \omega \leq \pi$

**Method:** Use the analytical formulas derived in 1-4a and plot directly.

From 1-4a, we have:

- **Magnitude:** $|H(\omega)| = 2\cos(2\omega) + 4\cos(\omega) + 6$
- **Phase:** $\angle H(\omega) = -2\omega$

**Expected characteristics:**

- **Magnitude:** Symmetric around $\omega = 0$, peaks at DC ($|H(0)| = 12$), minimum at edges ($|H(\pm\pi)| = 4$)
- **Phase:** Perfect linear phase (straight line through origin)

> [!code]- MATLAB — 1-4b
> 
> ```matlab
> %% Global image directory (Obsidian path)
> imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\DSP\Images';
> if ~exist(imgDir, 'dir')
>     mkdir(imgDir);
> end
> 
> %% Spørgsmål 1-4b: Plot |H(ω)| og ∠H(ω) for -π ≤ ω ≤ π
> 
> % Frequency vector
> omega = linspace(-pi, pi, 1024);
> 
> % Analytical formulas from 1-4a
> mag = 2*cos(2*omega) + 4*cos(omega) + 6;
> phase = -2*omega;
> 
> % Create plots
> figure;
> 
> % Magnitude Response
> subplot(2,1,1);
> plot(omega, mag, 'b-', 'LineWidth', 1.5);
> xlabel('\omega (rad/sample)');
> ylabel('|H(\omega)|');
> title('Magnitude Response');
> ylim([0 14]);
> grid on;
> 
> % Phase Response
> subplot(2,1,2);
> plot(omega, phase, 'b-', 'LineWidth', 1.5);
> xlabel('\omega (rad/sample)');
> ylabel('\angle H(\omega) (rad)');
> title('Phase Response');
> ylim([-8 8]);
> xlim([-4 4]);
> grid on;
> 
> % Export figure
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_Exam_F25_1_4b_MagPhase.png'), 'Resolution', 300);
> ```

![[Images/DSP_Exam_F25_1_4b_MagPhase.png]]

**Results:**

**Magnitude Plot:**

- Smooth curve from 0 to ~12
- Maximum at DC: $|H(0)| = 2(1) + 4(1) + 6 = 12$ ✓
- Minimum at Nyquist: $|H(\pi)| = 2(1) + 4(-1) + 6 = 4$ ✓
- Symmetric around $\omega = 0$ ✓

**Phase Plot:**

- Perfect straight line: $\angle H(\omega) = -2\omega$
- Passes through origin: $\angle H(0) = 0$ ✓
- At $\omega = \pi$: $\angle H(\pi) = -2\pi$ ✓
- This confirms **linear phase** characteristic ✓

> [!info] Linear Phase Confirmation The phase plot being a perfect straight line confirms this is a **Type I Linear Phase FIR filter** with:
> 
> - **Group delay:** $\tau_g = 2$ samples (constant for all frequencies)
> - **Zero phase distortion:** All frequency components delayed equally
> - **Applications:** Audio processing, communications (where phase linearity matters)

---

## 1-5) Combined system: $T_1$, $T_2$, $T_3$

> **Given:**
> 
> - $H_1(z) = H(z) = 1 + 2z^{-1} + 6z^{-2} + 2z^{-3} + z^{-4}$ (from Problem 1-3)
> - $H_2(z) = 3 - 10z^{-1} - 11z^{-2}$
> - $H_3(z) = \dfrac{1}{1 - \frac{1}{4}z^{-2}}$
> 
> **Block diagram:** $T_1$ and $T_2$ in **parallel**, then $T_3$ in **series**.
> 
> **Task:** Find $H_{\text{total}}(z)$ and argue that it's FIR.

### **Solution Strategy**

The combined system formula is: $$ H_{\text{total}}(z) = \big(H_1(z) + H_2(z)\big) \cdot H_3(z) $$

Since $H_3(z) = \dfrac{1}{1 - \frac{1}{4}z^{-2}}$, multiplying by it is the same as dividing by its denominator:

$$ H_{\text{total}}(z) = \frac{H_1(z) + H_2(z)}{1 - \frac{1}{4}z^{-2}} $$

**Key insight:** The exam says **"It is allowed to use MATLAB to perform polynomial calculations"** → Use `deconv()` to check for pole-zero cancellation!

---

### **Step 1: Add parallel systems (T1 + T2)**

Add coefficients term by term:

|Power|$H_1$|$H_2$|Sum|
|---|---|---|---|
|$z^0$|1|3|4|
|$z^{-1}$|2|-10|-8|
|$z^{-2}$|6|-11|-5|
|$z^{-3}$|2|0|2|
|$z^{-4}$|1|0|1|

**Result:** $$ H_1(z) + H_2(z) = 4 - 8z^{-1} - 5z^{-2} + 2z^{-3} + z^{-4} $$

---

### **Step 2: Divide by $H_3$ denominator to cancel factors**

Before simplification, the system is: $$ H_4(z) = \frac{4 - 8z^{-1} - 5z^{-2} + 2z^{-3} + z^{-4}}{1 - \frac{1}{4}z^{-2}} $$

To check for pole-zero cancellation, multiply numerator and denominator by $z^4$ to get positive powers: $$ H_4(z) = \frac{4z^4 - 8z^3 - 5z^2 + 2z + 1}{z^2(z^2 - \frac{1}{4})} $$

The denominator $z^2(z^2 - \frac{1}{4})$ factors as $z^2(z - \frac{1}{2})(z + \frac{1}{2})$.

**Polynomial division:** Divide numerator by $(z^2 - \frac{1}{4})$ to cancel common factors.

Using MATLAB `deconv()`:

Numerator (positive powers): `[4, -8, -5, 2, 1]` represents $4z^4 - 8z^3 - 5z^2 + 2z + 1$  
Denominator factor: `[1, 0, -1/4]` represents $z^2 - \frac{1}{4}$

**Division result:** $$ \frac{4z^4 - 8z^3 - 5z^2 + 2z + 1}{z^2 - \frac{1}{4}} = 4z^2 - 8z - 4 \quad (\text{remainder} = 0) $$

Convert back to $z^{-n}$ form (divide by $z^2$): $$ \boxed{H_4(z) = 4 - 8z^{-1} - 4z^{-2}} $$

---

### **Step 3: Verify it's FIR**

**Final system function:** $$ H_4(z) = 4 - 8z^{-1} - 4z^{-2} $$

**Impulse response:** $$ h_4[n] = 4\delta[n] - 8\delta[n-1] - 4\delta[n-2] $$

**Why it's FIR:**

1. ✅ **Denominator = 1** (no feedback terms)
2. ✅ **Finite length:** Only 3 non-zero samples
3. ✅ **Pole-zero cancellation:** The poles from $H_3(z)$ at $z = \pm\frac{1}{2}$ were canceled by zeros in $H_1(z) + H_2(z)$

> [!success] Conclusion The combined system is **FIR** because polynomial division shows the denominator $(z^2 - 1/4)$ divides evenly into the numerator, leaving no poles in the simplified transfer function.

---

> [!code]- MATLAB — 1-5 Solution
> 
> ```matlab
> %% Spørgsmål 1-5: Combined system (T1, T2, T3)
> 
> % Given systems
> H1_B = [1, 2, 6, 2, 1];      % From problem 1-3
> H2_B = [3, -10, -11];         % Given
> H3_A = [1, 0, -1/4];          % Denominator of H3
> 
> %% Step 1: Add parallel systems (T1 + T2)
> % T1: [1, 2, 6, 2, 1]
> % T2: [3, -10, -11, 0, 0]  % pad with zeros
> H_parallel_B = [4, -8, -5, 2, 1];  % Add coefficients
> 
> fprintf('H1(z) + H2(z) = 4 - 8z^(-1) - 5z^(-2) + 2z^(-3) + z^(-4)\n\n');
> 
> %% Step 2: Divide by H3 denominator to cancel factors
> % Use polynomial division (positive powers)
> num = [4, -8, -5, 2, 1];      % 4z^4 - 8z^3 - 5z^2 + 2z + 1
> den = [1, 0, -1/4];            % z^2 - 1/4
> 
> [H_total_B, remainder] = deconv(num, den);
> 
> fprintf('After polynomial division:\n');
> fprintf('H_total(z) = 4 - 8z^(-1) - 4z^(-2)\n\n');
> 
> %% Step 3: Show it's FIR
> fprintf('=== FIR Verification ===\n');
> fprintf('Coefficients: [%g, %g, %g]\n', H_total_B);
> fprintf('Denominator = 1 → FIR system ✓\n');
> fprintf('Impulse response: h4[n] = 4δ[n] - 8δ[n-1] - 4δ[n-2]\n');
> ```

---

# Problem 2 — IIR Butterworth Highpass Filter (BLT)

> **Given specifications:**
> 
> - Design method: **Bilinear Transform (BLT)** with $\alpha = 2/T_s$
> - Filter type: **IIR Highpass Butterworth**
> - Sampling frequency: $F_s = 4000$ Hz
> - Stopband edge: $f_s = 450$ Hz (normalized: $f_s/F_s$)
> - Passband edge: $f_p = 1000$ Hz (normalized: $f_p/F_s$)
> - Stopband attenuation: $A_s = 30$ dB
> - Passband attenuation: $A_p = 3$ dB

---

## 2-1) Analog prototype Butterworth filter

### (a) Calculate $\varepsilon$

For a Butterworth filter with passband ripple $A_p$ dB: $$ \varepsilon = \sqrt{10^{A_p/10} - 1} $$

With $A_p = 3$ dB: $$ \varepsilon = \sqrt{10^{0.3} - 1} = \sqrt{1.9953 - 1} = \sqrt{0.9953} \approx 1 $$

$$ \boxed{\varepsilon = 1.00} $$

---

### (b) Pre-warped analog frequencies

**Step 1: Calculate digital angular frequencies**

$$ \omega_s = 2\pi \frac{f_s}{F_s} = 2\pi \frac{450}{4000} = 0.225\pi \text{ rad/sample} $$

$$ \omega_p = 2\pi \frac{f_p}{F_s} = 2\pi \frac{1000}{4000} = 0.5\pi \text{ rad/sample} $$

**Step 2: Apply BLT pre-warping**

Pre-warping formula (from [[Uge 10 - Tirsdag]]): $$ \Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2F_s \tan\left(\frac{\omega}{2}\right) $$

**For stopband edge:** $$ \Omega_s = 2 \times 4000 \times \tan\left(\frac{0.225\pi}{2}\right) = 8000 \times \tan(0.1125\pi) = 2951.36 \text{ rad/s} $$

**For passband edge:** $$ \Omega_p = 2 \times 4000 \times \tan\left(\frac{0.5\pi}{2}\right) = 8000 \times \tan(0.25\pi) = 8000 \times 1 = 8000 \text{ rad/s} $$

$$ \boxed{\Omega_s = 2951.36 \text{ rad/s}, \quad \Omega_p = 8000.00 \text{ rad/s}} $$

> [!info] Why Ω_p is exact At $\omega = \pi/2$, we have $\tan(\pi/4) = 1$ exactly, so $\Omega_p = 8000$ rad/s is not an approximation.

---

### (c) Minimum filter order $n$

For **highpass** Butterworth, the selectivity ratio is: $$ \text{ratio} = \frac{\Omega_p}{\Omega_s} $$

> [!warning] Highpass vs Lowpass For **highpass**, the ratio is $\Omega_p/\Omega_s$ (inverted compared to lowpass!)
> 
> - **Highpass:** ratio = $\Omega_p / \Omega_s$ (passband / stopband)
> - **Lowpass:** ratio = $\Omega_s / \Omega_p$ (stopband / passband)

**Butterworth order formula:** $$ n \geq \frac{\log_{10}\left(\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\log_{10}(\text{ratio})} $$

**Numerical calculation:**

$$ \text{ratio} = \frac{8000}{2951.36} = 2.7103 $$

$$ n_{\text{exact}} = \frac{\log_{10}\left(\frac{10^{30/10} - 1}{10^{3/10} - 1}\right)}{2\log_{10}(2.7103)} = \frac{\log_{10}\left(\frac{999}{0.9953}\right)}{2\log_{10}(2.7103)} $$

$$ n_{\text{exact}} = \frac{\log_{10}(1003.71)}{2 \times 0.4331} = \frac{3.0016}{0.8662} = 3.47 $$

Since $n$ must be an integer: $$ \boxed{n = \lceil 3.47 \rceil = 4} $$

---

### (d) Prototype transfer function

From the **Butterworth prototype table** (Appendix, $n=4$, $\varepsilon = 1$):

$$ \boxed{H_{LP}(s) = \frac{1}{s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1}} $$

**Verification:** This is the standard 4th-order Butterworth lowpass prototype with 3 dB passband ripple.

---

> [!code]- MATLAB — 2-1 Complete Solution
> 
> ```matlab
> %% Spørgsmål 2-1: Analog prototype Butterworth filter
> 
> % Given specifications
> Fs = 4000;         % Sampling frequency (Hz)
> Ts = 1/Fs;         % Sampling period
> 
> fs_hz = 450;       % Stopband edge (Hz)
> fp_hz = 1000;      % Passband edge (Hz)
> As_dB = 30;        % Stopband attenuation (dB)
> Ap_dB = 3;         % Passband attenuation (dB)
> 
> % Digital angular frequencies
> omega_s = 2*pi*fs_hz/Fs;
> omega_p = 2*pi*fp_hz/Fs;
> 
> % (1) Beregn epsilon (ε)
> epsilon = sqrt(10^(Ap_dB/10) - 1);
> fprintf('ε = %.2f\n\n', epsilon);
> 
> % (2) Beregn digitale vinkelfrekvenser (ω)
> fprintf('Digital frequencies:\n');
> fprintf('ω_s = %.4f rad/sample = %.4fπ\n', omega_s, omega_s/pi);
> fprintf('ω_p = %.4f rad/sample = %.4fπ\n\n', omega_p, omega_p/pi);
> 
> % Pre-warping: Digital → Analog
> Omega_s = 2*Fs * tan(omega_s/2);
> Omega_p = 2*Fs * tan(omega_p/2);
> 
> fprintf('Pre-warped analog frequencies:\n');
> fprintf('Ω_s = %.2f rad/s\n', Omega_s);
> fprintf('Ω_p = %.2f rad/s\n\n', Omega_p);
> 
> % (3) Beregn minimum filter orden n
> % For HIGHPASS: ratio = Omega_p / Omega_s (inverted!)
> ratio = Omega_p / Omega_s;
> 
> % Butterworth order formula
> n_exact = log10((10^(As_dB/10) - 1) / (10^(Ap_dB/10) - 1)) / (2*log10(ratio));
> n = ceil(n_exact);
> 
> fprintf('Filter order calculation:\n');
> fprintf('Ratio (Ω_p/Ω_s) = %.4f\n', ratio);
> fprintf('n_exact = %.4f\n', n_exact);
> fprintf('n_min = %d\n\n', n);
> 
> % (4) Opskriv prototype lavpas transferfunktion (se appendix)
> B_proto = 1;
> A_proto = [1, 2.6131, 3.4142, 2.6131, 1];
> 
> % Create transfer function object
> fprintf('Prototype Butterworth lowpass transfer function H_LP(s):\n');
> H_proto = tf(B_proto, A_proto)
> ```

---

## 2-2) LP to HP transformation

> **Note:** We use $n = 4$ from Problem 2-1(c).

### (a) Transformation formula

To convert a lowpass prototype $H_{LP}(s)$ to highpass with analog cutoff $\Omega_p$:

$$\boxed{s_{LP} \rightarrow \frac{\Omega_p}{s}}$$

**What this transformation does:**

- **Inverts the frequency axis** (low ↔ high frequencies swap)
- DC response (s = 0) becomes response at infinity
- Response at infinity becomes DC response
- The -3 dB cutoff of the prototype becomes $\Omega_p$ in the highpass filter

**Reference:** See [[Uge 10 - Torsdag]], [[Uge 13 - Tirsdag]]

---

### (b) Analog highpass $H_{HP}(s)$

**Method:** Use MATLAB's `lp2hp()` function to apply the transformation.

Starting from the lowpass prototype: $$H_{LP}(s) = \frac{1}{s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1}$$

After transformation with $\Omega_p = 8000$ rad/s:

$$H_{HP}(s) = \frac{s^4}{a_4 s^4 + a_3 s^3 + a_2 s^2 + a_1 s + a_0}$$

where the coefficients are scaled by powers of $\Omega_p$.

**Key observation:** The numerator becomes $s^4$ (pure highpass - passes only high frequencies).

---

### (c) Plot analog magnitude response

The plot shows $|H_{HP}(j\Omega)|$ in dB vs. analog angular frequency $\Omega$ (rad/s).

**Blue specification lines indicate:**

- Vertical lines: $\Omega_s = 2951.36$ rad/s, $\Omega_p = 8000$ rad/s
- Horizontal lines: -30 dB (stopband), -3 dB (passband)

---

### (d) Does it meet analog specs?

**Visual verification from plot:**

- ✅ At $\Omega_p = 8000$ rad/s: attenuation is **exactly -3 dB** (by Butterworth design with $\varepsilon = 1$)
- ✅ At $\Omega_s = 2951.36$ rad/s: attenuation is **≤ -30 dB** (barely meets requirement)

**Conclusion:** The analog highpass filter **meets the analog design specifications**.

> [!info] Critical Understanding: Frequency Representations **Why are the analog frequencies different from 450 Hz and 1000 Hz?**
> 
> There are **4 different frequency representations** in this problem:
> 
> |Type|Symbol|Units|Your Values|Used For|
> |---|---|---|---|---|
> |**Physical**|$F$|Hz|450, 1000|Real-world specs|
> |**Normalized**|$f$|dimensionless|0.1125, 0.25|Initial specs ($f = F/F_s$)|
> |**Digital Angular**|$\omega$|rad/sample|0.225π, 0.5π|Digital filters (z-domain)|
> |**Analog Angular**|$\Omega$|rad/s|2951.36, 8000|Analog filters (s-domain)|
> 
> **The analog frequencies are "pre-warped"** to compensate for the nonlinear frequency mapping of the Bilinear Transform: $$\Omega = \frac{2}{T_s}\tan\left(\frac{\omega}{2}\right)$$
> 
> This ensures that after applying BLT (Problem 2-3), the **digital filter** will have edges at exactly 450 Hz and 1000 Hz.
> 
> **Conversion between representations:**
> 
> - Physical → Normalized: $f = F/F_s$
> - Normalized → Digital: $\omega = 2\pi f$
> - Digital → Analog (with warping): $\Omega = 2F_s \tan(\omega/2)$
> - Analog → Physical: $F = \Omega/(2\pi)$

> [!warning] Intermediate Verification This analog filter verification is an **intermediate step**. The **real test** comes in Problem 2-4 where we verify the **digital filter** at 450 Hz and 1000 Hz after applying the Bilinear Transform.

---

> [!code]- MATLAB — 2-2 Complete Solution
> 
> ```matlab
> %% Spørgsmål 2-2: LP → HP transformation
> 
> fprintf('\n=== Problem 2-2: LP → HP Transformation ===\n\n');
> 
> % (a) Transformation formula
> fprintf('(a) Transformation formula: s → Ω_p/s\n');
> fprintf('    Where Ω_p = %.2f rad/s\n\n', Omega_p);
> 
> % (b) Apply LP to HP transformation
> fprintf('(b) Analog Highpass Filter H_HP(s):\n');
> 
> % Use MATLAB's lp2hp function
> [B_hp, A_hp] = lp2hp(B_proto, A_proto, Omega_p);
> 
> % Display transfer function
> H_hp = tf(B_hp, A_hp)
> 
> % (c) Plot analog magnitude response
> fprintf('\n(c) Plotting analog magnitude response...\n');
> 
> Omega = [0:1:1E4];  % 0 to 10 krad/s (match official solution)
> H_analog = freqs(B_hp, A_hp, Omega);
> 
> figure;
> plot(Omega, 20*log10(abs(H_analog)), 'LineWidth', 2);
> hold on;
> 
> % Add specification lines (blue lines like official solution)
> xline(Omega_s, 'b-', 'LineWidth', 2);  % Stopband edge
> xline(Omega_p, 'b-', 'LineWidth', 2);  % Passband edge
> yline(-30, 'b-', 'LineWidth', 2);      % Stopband requirement
> yline(-3, 'b-', 'LineWidth', 2);       % Passband requirement
> 
> xlabel('\Omega (rad/s)');
> ylabel('20log_{10}(|H(\Omega)|) (dB)');
> title('Analog Highpass Butterworth Filter');
> grid on;
> xlim([0 10000]);
> ylim([-40 5]);
> 
> hold off;
> 
> % Export figure
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_Exam_F25_2_2_AnalogHP_Magnitude.png'), 'Resolution', 300);
> 
> % (d) Visual verification
> fprintf('\n(d) Verification:\n');
> fprintf('De blå linjer på plottet indikerer kravspecifikationerne for det analoge filter.\n');
> fprintf('Filteret opfylder de analoge design krav.\n');
> ```

![[Images/DSP_Exam_F25_2_2_AnalogHP_Magnitude.png]]

**Interpretation:**

- The analog filter shows classic Butterworth highpass characteristics
- Magnitude increases smoothly from stopband to passband
- At $\Omega_p = 8000$ rad/s: exactly -3 dB
- At $\Omega_s = 2951.36$ rad/s: approximately -30 dB (meets spec)
- The filter order n = 4 was correctly chosen to just meet the stopband requirement

---

## 2-3) Bilinear transformation to digital

### (a) BLT relation

The **Bilinear Transform (BLT)** maps the analog s-plane to the digital z-plane:

$$\boxed{s = \frac{2}{T_s} \cdot \frac{z - 1}{z + 1} = \alpha \cdot \frac{z - 1}{z + 1}}$$

Or equivalently in $z^{-1}$ form:

$$s = \frac{2}{T_s} \cdot \frac{1 - z^{-1}}{1 + z^{-1}}$$

**With our parameters:**

- $T_s = 1/F_s = 1/4000 = 0.00025$ s
- $\alpha = 2/T_s = 2F_s = 2 \times 4000 = 8000$

**BLT Properties:**

- Maps **left-half s-plane (stable analog) → inside unit circle (stable digital)**
- **Monotonic frequency mapping** (no aliasing)
- Introduces **frequency warping** (compensated by pre-warping in 2-1b)

**Reference:** [[Uge 10 - Tirsdag]]

---

### (b) Digital highpass $H_{HP}(z)$

**Method:** Use MATLAB's `bilinear()` function to apply the BLT transformation.

**Result:**

$$ H_{HP}(z) = \frac{0.09398 - 0.3759z^{-1} + 0.5639z^{-2} - 0.3759z^{-3} + 0.09398z^{-4}}{1 + 0z^{-1} + 0.486z^{-2} + 0z^{-3} + 0.01767z^{-4}} $$

**Simplified (ignoring numerical noise ~$10^{-16}$):**

$$ \boxed{H_{HP}(z) = \frac{0.09398 - 0.3759z^{-1} + 0.5639z^{-2} - 0.3759z^{-3} + 0.09398z^{-4}}{1 + 0.486z^{-2} + 0.01767z^{-4}}} $$

**Coefficient Arrays:**

```matlab
b = [0.09398, -0.3759, 0.5639, -0.3759, 0.09398]
a = [1, 0, 0.486, 0, 0.01767]
```

**Key observations:**

1. **Numerator symmetry:** $b_0 = b_4$, $b_1 = b_3$ (characteristic of linear phase)
2. **Denominator structure:** $a_1 = 0$, $a_3 = 0$ (only even powers of $z^{-1}$)
3. **Filter order:** 4 (matches analog prototype)
4. **Filter type:** IIR (has feedback terms in denominator)

---

### **Verification: Comparison with Official Solution**

The official solution gives: $$ H_{HP}(z) = \frac{0.09398 - 0.3759z^{-1} + 0.5639z^{-2} - 0.3759z^{-3} + 0.09398z^{-4}}{1 + 3.903 \times 10^{-16}z^{-1} + 0.486z^{-2} + 3.662 \times 10^{-16}z^{-3} + 0.01767z^{-4}} $$

**Coefficient Comparison:**

|Coefficient|Official|Your Result|Status|
|---|---|---|---|
|**Numerator**||||
|$b_0$|0.09398|0.09398|✅ Identical|
|$b_1$|-0.3759|-0.3759|✅ Identical|
|$b_2$|0.5639|0.5639|✅ Identical|
|$b_3$|-0.3759|-0.3759|✅ Identical|
|$b_4$|0.09398|0.09398|✅ Identical|
|**Denominator**||||
|$a_0$|1|1|✅ Identical|
|$a_1$|+3.903e-16|≈-4.545e-16|✅ Same (numerical noise)|
|$a_2$|0.486|0.486|✅ Identical|
|$a_3$|+3.662e-16|≈+1.585e-16|✅ Same (numerical noise)|
|$a_4$|0.01767|0.01767|✅ Identical|

> [!success] Verification Result **✅ Transfer functions are IDENTICAL within numerical precision!**
> 
> The coefficients $a_1$ and $a_3$ on the order of ~$10^{-16}$ are **numerical round-off errors** from floating-point arithmetic. These are effectively **zero** and the tiny differences between solutions are just different round-off patterns - completely negligible.
> 
> **Theoretical values:** $a_1 = 0$ and $a_3 = 0$ exactly.

> [!info] Why This Structure? This is a **4th-order highpass Butterworth filter** with special properties:
> 
> - **Numerator symmetry** ($b_0 = b_4$, $b_1 = b_3$): Characteristic of this filter type
> - **Only even-power denominators** ($a_1 = a_3 = 0$): Results from the specific transformation
> - **IIR structure:** Has feedback (denominator ≠ 1) for efficient highpass filtering

---

> [!code]- MATLAB — 2-3 Complete Solution
> 
> ```matlab
> %% Spørgsmål 2-3: Bilinear transformation (BLT)
> 
> fprintf('\n=== Problem 2-3: Bilinear Transform ===\n\n');
> 
> % (a) BLT relation
> alpha = 2/Ts;
> fprintf('(a) BLT parameter α = 2/T_s = 2·F_s = %.0f\n', alpha);
> fprintf('    Transformation: s = α·(z-1)/(z+1)\n\n');
> 
> % (b) Apply Bilinear Transform
> fprintf('(b) Digital Highpass Filter H_HP(z):\n');
> 
> % Use MATLAB's bilinear function
> [Bz, Az] = bilinear(B_hp, A_hp, Fs);
> 
> % Normalize so a[0] = 1 (should already be, but good practice)
> Bz = Bz / Az(1);
> Az = Az / Az(1);
> 
> % Display transfer function
> H_digital = tf(Bz, Az, Ts, 'Variable', 'z^-1')
> ```

```

**Transfer function for use in freqz():**

```matlab
b = [0.09398, -0.3759, 0.5639, -0.3759, 0.09398]
a = [1, 0, 0.486, 0, 0.01767]  % Ignoring ~1e-16 terms
```

---

## 2-4) Verify digital filter

Now we verify that the **digital filter** meets the **original specifications** at 450 Hz and 1000 Hz.

**Recall the specifications:**

- **Stopband:** At $f_s = 450$ Hz, attenuation should be ≤ -30 dB
- **Passband:** At $f_p = 1000$ Hz, attenuation should be ≥ -3 dB

---

### (a) Plot magnitude response in dB vs frequency (Hz)

We plot $|H_{HP}(e^{j\omega})|$ in dB as a function of **physical frequency F in Hz**.

**Note:** Unlike Problem 2-2 where we used **analog angular frequency Ω (rad/s)**, here we use **digital physical frequency F (Hz)** - the frequencies we started with!

The blue specification lines indicate:

- **Vertical lines:** $f_s = 450$ Hz, $f_p = 1000$ Hz
- **Horizontal lines:** -30 dB (stopband), -3 dB (passband)

---

### (b) & (c) Visual verification from plot

**Reading from the plot at specification frequencies:**

|Frequency|Measured|Requirement|Status|
|---|---|---|---|
|450 Hz (stopband)|≈ -34.6 dB|≤ -30 dB|✅ PASS|
|1000 Hz (passband)|≈ -3.0 dB|≥ -3 dB|✅ PASS|

**Observations:**

1. **At 450 Hz:** The magnitude is **well below** the -30 dB requirement (approximately -34.6 dB)
2. **At 1000 Hz:** The magnitude is **exactly at** the -3 dB requirement (approximately -3.0 dB)
3. The filter shows classic **highpass characteristics**: blocks low frequencies, passes high frequencies

$$\boxed{\text{The digital filter MEETS all specifications}}$$

> [!success] Pre-warping Verification **The BLT pre-warping worked perfectly!**
> 
> Recall from Problem 2-1(b):
> 
> - We pre-warped 450 Hz → Ω_s = 2951.36 rad/s (analog stopband)
> - We pre-warped 1000 Hz → Ω_p = 8000 rad/s (analog passband)
> 
> After applying BLT in Problem 2-3, the digital filter has specification edges **exactly where we wanted** at 450 Hz and 1000 Hz in the digital domain.
> 
> This confirms that the pre-warping formula $\Omega = 2F_s \tan(\omega/2)$ successfully compensated for the BLT's frequency warping!

> [!info] Why Visual Verification? The official solution uses **visual verification** from the plot rather than printing exact numerical values. This approach:
> 
> - Matches exam expectations (plots are primary verification tool)
> - Shows the overall filter characteristic (not just two points)
> - Demonstrates understanding of frequency response interpretation
> - Is the standard method in the course (see past exam solutions)

---

> [!code]- MATLAB — 2-4 Complete Solution
> 
> ```matlab
> %% Spørgsmål 2-4: Verificer digital filter
> 
> fprintf('\n=== Problem 2-4: Digital Filter Verification ===\n\n');
> 
> % (a) Plot magnitude response in dB vs frequency (Hz)
> fprintf('(a) Plotting digital magnitude response...\n');
> 
> [H, f] = freqz(Bz, Az, 1E4, Fs);  % Match official solution
> 
> figure;
> plot(f, 20*log10(abs(H)), 'LineWidth', 2);
> hold on;
> 
> % Add specification lines (blue lines like official solution)
> xline(fs_hz, 'b-', 'LineWidth', 2);  % Stopband edge at 450 Hz
> xline(fp_hz, 'b-', 'LineWidth', 2);  % Passband edge at 1000 Hz
> yline(-30, 'b-', 'LineWidth', 2);    % Stopband requirement
> yline(-3, 'b-', 'LineWidth', 2);     % Passband requirement
> 
> xlabel('F = f·F_s (Hz)');
> ylabel('20log_{10}(|H(F)|) (dB)');
> title('Digital Highpass Butterworth Filter');
> grid on;
> xlim([0 1300]);  % Match official solution range
> ylim([-40 5]);
> 
> hold off;
> 
> % Export figure
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_Exam_F25_2_4_DigitalHP_Magnitude.png'), 'Resolution', 300);
> 
> % (b) Visual verification from plot
> fprintf('\n(b) De blå linjer på plottet indikerer de digitale filter kravspecifikationerne\n');
> fprintf('    (The blue lines indicate the digital filter specifications)\n\n');
> 
> fprintf('(c) Aflæste værdier på plottet:\n');
> fprintf('    (Values read from the plot:)\n');
> fprintf('    At 450 Hz: ≈ -34.6 dB (requirement: ≤ -30 dB) ✓\n');
> fprintf('    At 1000 Hz: ≈ -3.0 dB (requirement: ≥ -3 dB) ✓\n\n');
> 
> fprintf('Filteret opfylder kravspecifikationerne.\n');
> fprintf('(The filter meets the specifications.)\n');
> ```

![[Images/DSP_Exam_F25_2_4_DigitalHP_Magnitude.png]]

**Plot interpretation:**

- The digital highpass filter shows classic Butterworth characteristics with smooth magnitude response
- At low frequencies (< 450 Hz): strong attenuation (stopband)
- Smooth transition region between 450 Hz and 1000 Hz
- At high frequencies (> 1000 Hz): minimal attenuation (passband)
- The blue specification lines clearly show that both requirements are met

---

# Problem 3 — Sampling, Aliasing, and Inverse Systems

> **Given:** Continuous-time signal: $$ x(t) = 3\cos(2\pi \cdot 1500 \cdot t) + 2\cos(2\pi \cdot 4200 \cdot t), \quad t \geq 0 $$ Sampling frequency: $F_s = 8000$ Hz

> [!tip] Spectrum Plotting Tool This problem uses `plot_spectrum.m` for beautiful frequency spectrum plots.  
> **See:** [[plot_spectrum_README]] for complete usage guide and exam templates.

---

## 3-1) Sketch amplitude spectrum from -10 kHz to 10 kHz

### Signal Analysis

**Component 1:**

- Frequency: $F_1 = 1500$ Hz
- Amplitude: $A_1 = 3$
- Spectrum: Two spikes at $\pm 1500$ Hz with amplitude $3/2 = 1.5$ each

**Component 2:**

- Frequency: $F_2 = 4200$ Hz
- Amplitude: $A_2 = 2$
- Spectrum: Two spikes at $\pm 4200$ Hz with amplitude $2/2 = 1.0$ each

### Nyquist Analysis

$$F_{Nyquist} = \frac{F_s}{2} = \frac{8000}{2} = 4000 \text{ Hz}$$

**Aliasing Check:**

- $F_1 = 1500$ Hz $< 4000$ Hz → ✅ **No aliasing**
- $F_2 = 4200$ Hz $> 4000$ Hz → ⚠️ **ALIASING!**

### Aliased Frequency

For $F_2 = 4200$ Hz above Nyquist: $$F_{2,\text{alias}} = F_s - F_2 = 8000 - 4200 = 3800 \text{ Hz}$$

The 4200 Hz component **appears at 3800 Hz** after sampling (indistinguishable from a true 3800 Hz signal).

### Spectral Replication

Sampling creates replicas at multiples of $F_s$: $$F_{\text{replica}} = F \pm k \cdot F_s, \quad k = 0, \pm 1, \pm 2, \ldots$$

**In range [-10 kHz, 10 kHz]:**

|Frequency|Amplitude|Source|Color|
|---|---|---|---|
|$\pm 1500$ Hz|1.5|Original $F_1$ (k=0)|Blue|
|$\pm 3800$ Hz|1.0|Aliased $F_2$ (k=0)|Red|
|$\pm 6500$ Hz|1.5|Replica $F_1$ at $8000-1500$ (k=±1)|Blue|
|$\pm 9500$ Hz|1.5|Replica $F_1$ at $8000+1500$ (k=±1)|Blue|

> [!info] Why These Frequencies?
> 
> - **1500 Hz:** Original component (below Nyquist)
> - **3800 Hz:** Where 4200 Hz appears after aliasing
> - **6500 Hz:** $|8000 - 1500| = 6500$ Hz (replica at k=-1)
> - **9500 Hz:** $8000 + 1500 = 9500$ Hz (replica at k=+1)

---

> [!code]- MATLAB — 3-1 Spectrum Plot
> 
> ```matlab
> %% Problem 3-1: Aliasing Spectrum
> 
> % Signal parameters
> F1 = 1500;  A1 = 3;
> F2 = 4200;  A2 = 2;
> Fs = 8000;
> 
> fprintf('Nyquist = %d Hz\n', Fs/2);
> fprintf('F1 = %d Hz < Nyquist → NO aliasing\n', F1);
> fprintf('F2 = %d Hz > Nyquist → ALIASING to %d Hz\n\n', F2, Fs-F2);
> 
> % Calculate aliased frequency
> F2_alias = Fs - F2;  % 3800 Hz
> 
> % Build spectrum with replicas (k = -1, 0, 1)
> freqs = [];
> amps = [];
> colors = {};
> 
> for k = -1:1
>     % F1 component (blue - no aliasing)
>     freqs = [freqs, F1 + k*Fs, -F1 + k*Fs];
>     amps = [amps, A1/2, A1/2];
>     colors = [colors, 'b', 'b'];
>     
>     % F2 component (red - aliased)
>     freqs = [freqs, F2_alias + k*Fs, -F2_alias + k*Fs];
>     amps = [amps, A2/2, A2/2];
>     colors = [colors, 'r', 'r'];
> end
> 
> % Plot spectrum
> plot_spectrum(freqs, amps, ...
>               'Colors', colors, ...
>               'XRange', [-10000, 10000], ...
>               'XStep', 2000, ...
>               'Title', 'Sampled Signal Spectrum (Fs = 8000 Hz)');
> 
> % Add Nyquist markers
> hold on;
> xline(Fs/2, '--', 'Color', [1 1 0], 'LineWidth', 2, 'Label', 'Nyquist');
> xline(-Fs/2, '--', 'Color', [1 1 0], 'LineWidth', 2);
> hold off;
> 
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_Exam_F25_3_1_Spectrum.png'), 'Resolution', 300);
> ```

**Note:** Requires `plot_spectrum.m` - see [[plot_spectrum_README]] for usage guide.

![[Images/DSP_Exam_F25_3_1_Spectrum.png]]

---

## 3-2) Is there aliasing in [-4 kHz, 4 kHz]?

**Analysis:**

The baseband (first Nyquist zone) extends from $-F_s/2$ to $+F_s/2 = [-4000, 4000]$ Hz.

**Component 1 ($F_1 = 1500$ Hz):**

- Since $1500 < 4000$, this component is **below Nyquist**
- ✅ No aliasing occurs
- Appears at correct frequencies: $\pm 1500$ Hz

**Component 2 ($F_2 = 4200$ Hz):**

- Since $4200 > 4000$, this component is **above Nyquist**
- ⚠️ **ALIASING occurs**
- Original 4200 Hz "folds back" into baseband
- Aliased frequency: $F_{2,\text{alias}} = 8000 - 4200 = 3800$ Hz
- Appears at: $\pm 3800$ Hz

$$\boxed{\text{Yes, aliasing occurs. Component at 4200 Hz appears at 3800 Hz}}$$

> [!warning] Critical Point After sampling, the 3800 Hz component is **indistinguishable** from a true 3800 Hz signal. The original 4200 Hz information is **lost** - this is why anti-aliasing filters are essential!

### Verification

Using the folding formula for first fold above Nyquist: $$F_{\text{alias}} = F_s - F = 8000 - 4200 = 3800 \text{ Hz}$$

Alternative formula (general): $$F_{\text{alias}} = |F - k \cdot F_s| \quad \text{for } k \text{ chosen so } F_{\text{alias}} \in [0, F_s/2]$$

With $k=1$: $|4200 - 8000| = 3800$ Hz ✓

---

## 3-3) Digital filter $H_1(z)$ analysis

> **Given difference equation:** $$y[n] - 0.7y[n-1] + 0.1y[n-2] = x[n] + x[n-1]$$

### (a) System function $H_1(z)$

Taking the Z-transform of both sides: $$Y(z) - 0.7z^{-1}Y(z) + 0.1z^{-2}Y(z) = X(z) + z^{-1}X(z)$$

Factor out $Y(z)$ and $X(z)$: $$Y(z)\big(1 - 0.7z^{-1} + 0.1z^{-2}\big) = X(z)\big(1 + z^{-1}\big)$$

Transfer function: $$\boxed{H_1(z) = \frac{Y(z)}{X(z)} = \frac{1 + z^{-1}}{1 - 0.7z^{-1} + 0.1z^{-2}}}$$

---

### (b) Poles and zeros

**Numerator (zeros):** $$B(z) = 1 + z^{-1}$$

Setting $B(z) = 0$: $$1 + z^{-1} = 0 \Rightarrow z^{-1} = -1 \Rightarrow z = -1$$

**Zero:** $z_0 = -1$ (on unit circle)

**Denominator (poles):** $$A(z) = 1 - 0.7z^{-1} + 0.1z^{-2}$$

Multiply by $z^2$ to get standard polynomial form: $$z^2 - 0.7z + 0.1 = 0$$

Using quadratic formula: $$z = \frac{0.7 \pm \sqrt{0.49 - 0.4}}{2} = \frac{0.7 \pm \sqrt{0.09}}{2} = \frac{0.7 \pm 0.3}{2}$$

$$p_1 = \frac{0.7 + 0.3}{2} = 0.5, \quad p_2 = \frac{0.7 - 0.3}{2} = 0.2$$

**Poles:** $p_1 = 0.5$, $p_2 = 0.2$ (both inside unit circle)

### Pole-Zero Summary

|Type|Location|$\|z\|$|Position|
|---|---|---|---|
|Zero|$z = -1$|1|On unit circle|
|Pole|$z = 0.5$|0.5|Inside UC|
|Pole|$z = 0.2$|0.2|Inside UC|

---

### (c) ROC and stability

For a **causal system**, the ROC is the region **outside** the outermost pole: $$\text{ROC: } |z| > \max(|p_1|, |p_2|) = |z| > 0.5$$

**Stability check:**

- All poles are **strictly inside** the unit circle: $|0.5| < 1$ and $|0.2| < 1$
- The ROC **includes the unit circle** ($|z| = 1$) ← **This is key!**
- Since ROC contains the unit circle, the system is **BIBO stable**

$$\boxed{H_1(z) \text{ is STABLE (ROC includes unit circle)}}$$

> [!success] Stability Verification **Rule:** A causal LTI system is BIBO stable if and only if:
> 
> 1. All poles lie strictly inside the unit circle, AND
> 2. The ROC includes the unit circle
> 
> **For $H_1(z)$:**
> 
> - $|p_1| = 0.5 < 1$ ✓
> - $|p_2| = 0.2 < 1$ ✓
> - ROC: $|z| > 0.5$ includes unit circle ($|z| = 1$) ✓
> 
> **Conclusion:** System is BIBO stable because ROC is part of (includes) the unit circle.

---

### (d) Inverse system $H_2(z) = 1/H_1(z)$

The inverse system swaps numerator and denominator: $$H_2(z) = \frac{1}{H_1(z)} = \frac{1 - 0.7z^{-1} + 0.1z^{-2}}{1 + z^{-1}}$$

**Poles and zeros swap:**

- **Poles of $H_2$:** zeros of $H_1$ → $z = -1$
- **Zeros of $H_2$:** poles of $H_1$ → $z = 0.5, 0.2$

|$H_2(z)$|Location|$\|z\|$|Position|
|---|---|---|---|
|Pole|$z = -1$|1|**On unit circle**|
|Zero|$z = 0.5$|0.5|Inside UC|
|Zero|$z = 0.2$|0.2|Inside UC|

**Stability analysis:**

$H_2(z)$ has a pole at $z = -1$, which is **on the unit circle** ($|z| = 1$).

$$\boxed{H_2(z) \text{ is MARGINALLY STABLE (pole on unit circle at } z = -1\text{)}}$$

> [!warning] Marginal Stability A system with poles **on** (not inside) the unit circle is called **marginally stable**:
> 
> - A bounded input **may** produce unbounded output
> - Impulse response neither decays nor grows exponentially
> - System oscillates without damping
> - Not suitable for practical applications
> 
> **For $H_2(z)$:** The pole at $z=-1$ corresponds to a frequency $\omega = \pi$ (Nyquist frequency), causing sustained oscillation at half the sampling rate.

---

> [!code]- MATLAB — 3-3 Filter Pole-Zero Diagrams
> 
> ```matlab
> %% Problem 3-3: Filter Pole-Zero Diagrams
> 
> % From difference equation: y[n] - 0.7y[n-1] + 0.1y[n-2] = x[n] + x[n-1]
> 
> % Numerator coefficients (x terms, right side)
> B = [1, 1];  % Corresponds to: x[n] + x[n-1]
> 
> % Denominator coefficients (y terms, left side)
> A = [1, -0.7, 0.1];  % Corresponds to: y[n] - 0.7y[n-1] + 0.1y[n-2]
> 
> % Display transfer function
> fprintf('H1(z) Transfer Function:\n');
> H1 = tf(B, A, -1)  % -1 = discrete, unspecified sample time
> 
> % H1(z) pole-zero plot
> figure;
> zplane(B, A);
> title('H_1(z) Pole-Zero Diagram');
> grid on;
> set(gcf, 'Position', [100, 100, 800, 800]);
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_3_3_H1.png'), ...
>                'Resolution', 300);
> 
> % Inverse system
> fprintf('\nH2(z) = 1/H1(z) Transfer Function:\n');
> H2 = tf(A, B, -1)  % Swap numerator/denominator
> 
> % H2(z) pole-zero plot
> figure;
> zplane(A, B);
> title('H_2(z) = 1/H_1(z) Inverse System');
> grid on;
> set(gcf, 'Position', [100, 100, 800, 800]);
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_3_3_H2.png'), ...
>                'Resolution', 300);
> ```
> 
> **Analysis from plots:**
> 
> - **H₁(z):** Poles at 0.5 and 0.2 (both inside unit circle) → **STABLE** ✓
>     - ROC: $|z| > 0.5$ includes the unit circle
> - **H₂(z):** Pole at -1 (on unit circle) → **MARGINALLY STABLE** ⚠️
>     - Pole on unit circle causes sustained oscillation without decay

> **Analysis from plots:**
> 
> - **H₁(z):** Poles at 0.5 and 0.2 (both inside unit circle) → **STABLE** ✓
>     - ROC: $|z| > 0.5$ includes the unit circle
> - **H₂(z):** Pole at -1 (on unit circle) → **MARGINALLY STABLE** ⚠️
>     - Pole on unit circle causes sustained oscillation without decay

![[Images/DSP_Exam_F25_3_3_H1.png]]

![[Images/DSP_Exam_F25_3_3_H2.png]]

# Problem 4 — Filter Realization and Signal Filtering

> **Given:** A digital lowpass filter with 3 dB attenuation at 400 Hz, realized as shown in the block diagram.
> 
> **Coefficients from diagram:**
> 
> - Feedforward (numerator): $b_0 = 0.0102$, $b_1 = 0.0305$, $b_2 = 0.0305$, $b_3 = 0.0102$
> - Feedback (denominator): $a_1 = -2.0038$, $a_2 = 1.4471$, $a_3 = -0.3618$
> 
> Sampling frequency: $F_s = 5000$ Hz

---

## 4-1) Identify filter structure
![[DSP_Exam_F25_4_1.png|350]]
### (a) Filter form

Looking at the block diagram structure:

- **Left side:** Input $x[n]$ with feedforward coefficients ($b$ values)
- **Right side:** Output $y[n]$ with feedback from delayed outputs ($a$ values)
- **Two separate delay chains** (one for input, one for output)

$$ \boxed{\text{Direct Form I}} $$

> [!info] Direct Form I vs II **Direct Form I:**
> 
> - Separate feedforward and feedback sections
> - Two separate delay chains ($z^{-1}$ blocks)
> - More delays but better numerical properties
> 
> **Direct Form II:**
> 
> - Shared delays between feedforward and feedback
> - Single delay chain (fewer delays)
> - Also called "canonical form"

### (b) FIR or IIR?

**IIR** because:

- There are **feedback terms** (output $y[n]$ depends on past outputs $y[n-1], y[n-2], y[n-3]$)
- Denominator is not just 1
- The filter has **poles** (not just zeros)

$$ \boxed{\text{IIR filter — has feedback (recursive structure)}} $$

### (c) Transfer function $H(z)$

From the coefficients: $$ H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + b_3 z^{-3}}{1 + a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3}} $$

$$ \boxed{H(z) = \frac{0.0102 + 0.0305z^{-1} + 0.0305z^{-2} + 0.0102z^{-3}}{1 - 2.0038z^{-1} + 1.4471z^{-2} - 0.3618z^{-3}}} $$

> [!code]- MATLAB — 4-1
> 
> ```matlab
> % Problem 4-1: Filter coefficients
> b = [0.0102, 0.0305, 0.0305, 0.0102];
> a = [1, -2.0038, 1.4471, -0.3618];
> Fs = 5000;
> 
> % Display transfer function
> H = tf(b, a, 1/Fs, 'Variable', 'z^-1');
> disp('H(z) ='); disp(H);
> ```

---

## 4-2) Magnitude response and -3 dB frequency

### (a) Plot magnitude response in dB

> [!code]- MATLAB — 4-2: Magnitude Response with Automatic -3 dB Detection
> 
> ```matlab
> %% Problem 4-2: Plot magnitude response og verificer -3 dB frekvens
> 
> % Frequency vector (0 to Nyquist)
> F_vec = linspace(0, Fs/2, 10000);  % High resolution for accurate detection
> 
> % Compute frequency response
> [H_freq, F_resp] = freqz(B, A, F_vec, Fs);
> 
> % Magnitude in dB
> Mag_dB = 20*log10(abs(H_freq));
> 
> % Plot
> figure;
> plot(F_resp, Mag_dB, 'b-', 'LineWidth', 1.5);
> hold on;
> grid on;
> xlabel('Frequency [Hz]');
> ylabel('Magnitude [dB]');
> title('Lowpass Filter Magnitude Response');
> 
> % Mark -3 dB reference line
> yline(-3, '--r', '-3 dB', 'LineWidth', 1.5, 'FontSize', 12);
> 
> % TECHNIQUE: Find -3 dB frequency automatically
> % Find last index where magnitude is still >= -3 dB
> idx_3dB = find(Mag_dB >= -3, 1, 'last');
> F_3dB = F_resp(idx_3dB);
> 
> % Mark the found frequency
> xline(F_3dB, '--g', sprintf('%.1f Hz', F_3dB), ...
>       'LineWidth', 1.5, 'FontSize', 12, 'LabelOrientation', 'horizontal');
> 
> % Also mark specified frequency for comparison
> xline(400, '--k', '400 Hz (spec)', 'LineWidth', 1, 'FontSize', 10);
> 
> xlim([0, 1500]);  % Focus on relevant range
> ylim([-60, 5]);
> hold off;
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_2_Magnitude.png'), ...
>                'Resolution', 300);
> 
> % Display results
> fprintf('\n=== Problem 4-2 Results ===\n');
> fprintf('Measured -3 dB frequency: %.2f Hz\n', F_3dB);
> fprintf('Specified frequency:      400.00 Hz\n');
> fprintf('Difference:               %.2f Hz\n', abs(F_3dB - 400));
> fprintf('Relative error:           %.2f%%\n\n', abs(F_3dB - 400)/400 * 100);
> 
> if abs(F_3dB - 400) < 10
>     fprintf('✓ Filter meets specification\n');
> end
> ```

> [!tip] Technique: Finding Cutoff Frequencies Automatically **The `find()` method for detecting -3 dB (or any threshold):**
> 
> ```matlab
> % Step 1: Compute magnitude response with high resolution
> F_vec = linspace(0, Fs/2, 10000);  % Many points for accuracy
> [H, F] = freqz(B, A, F_vec, Fs);
> Mag_dB = 20*log10(abs(H));
> 
> % Step 2: Find last point where magnitude >= threshold
> idx = find(Mag_dB >= -3, 1, 'last');  % Last point above -3 dB
> F_cutoff = F(idx);
> 
> % Step 3: Mark on plot
> xline(F_cutoff, '--g', sprintf('%.1f Hz', F_cutoff));
> ```
> 
> **Why use `'last'` instead of `'first'`?**
> 
> - For lowpass: Last point ≥ -3 dB gives the **passband edge**
> - For highpass: First point ≥ -3 dB gives the **passband edge**
> 
> **Key parameters:**
> 
> - `Mag_dB >= -3`: Finds passband edge (still above threshold)
> - `Mag_dB <= -30`: Finds stopband edge (below threshold)
> - `'last'/'first'`: Depends on filter type and what you're finding

![[Images/DSP_Exam_F25_4_2_Magnitude.png]]

### (b) Verification and Discussion

From the plot and calculations:

**Measured values:**

- **-3 dB frequency:** $\approx 400$ Hz ✓
- **Attenuation at 1000 Hz:** $\approx -27$ dB (strong stopband attenuation)

**Filter characteristics:**

- **Passband (0-400 Hz):** Minimal attenuation (< 3 dB)
- **Transition band (400-800 Hz):** Rapid rolloff
- **Stopband (> 800 Hz):** Strong attenuation (> 20 dB)
- **Filter order:** 3rd order IIR

$$\boxed{\text{Filter meets specification: } f_{-3dB} \approx 400 \text{ Hz}}$$

> [!success] Specification Check The designed filter achieves:
> 
> - ✅ -3 dB attenuation at 400 Hz (as required)
> - ✅ Smooth passband response
> - ✅ Good stopband attenuation
> 
> **Conclusion:** Filter design is successful

---

## 4-3) Pole-zero analysis and stability

### Task: Find poles and zeros, plot pole-zero diagram, and discuss stability

> [!code]- MATLAB — 4-3: Pole-Zero Analysis
> 
> ```matlab
> %% Spørgsmål 4-3: Pole-zero analyse
> 
> % Find poles and zeros
> zeros_H4 = roots(B4);
> poles_H4 = roots(A4);
> 
> % Display
> fprintf('\nZeros:\n');
> disp(zeros_H4);
> fprintf('Zeros magnitudes: ');
> disp(abs(zeros_H4)');
> 
> fprintf('\nPoles:\n');
> disp(poles_H4);
> fprintf('Pole magnitudes: ');
> disp(abs(poles_H4)');
> 
> % Stability check
> fprintf('\n--- Stability ---\n');
> if all(abs(poles_H4) < 1)
>     fprintf('✓ STABLE (all |p| < 1)\n');
> else
>     fprintf('✗ NOT STABLE\n');
> end
> 
> % Plot pole-zero diagram
> figure;
> zplane(B4, A4);
> title('F25 Problem 4-3: Pole-Zero Diagram');
> grid on;
> 
> % Make plot prettier
> hold on;
> plot(real(poles_H4), imag(poles_H4), 'rx', 'MarkerSize', 12, 'LineWidth', 2);
> plot(real(zeros_H4), imag(zeros_H4), 'bo', 'MarkerSize', 12, 'LineWidth', 2);
> hold off;
> 
> set(gcf, 'Position', [100, 100, 800, 800]);
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_3_PoleZero.png'), ...
>                'Resolution', 300);
> ```

![[Images/DSP_Exam_F25_4_3_PoleZero.png]]

---

### Analysis and Results

**Stability Criterion:**

A filter is **BIBO stable** if all poles are strictly inside the unit circle:

$$\boxed{|p_i| < 1 \text{ for all poles } p_i}$$

**For this filter:**

- All pole magnitudes are less than 1
- Maximum pole magnitude < 1

$$\boxed{\text{Filter is STABLE}}$$

> [!success] Conclusion **The filter is BIBO stable** because all poles are strictly inside the unit circle.
> 
> This means:
> 
> - Bounded inputs produce bounded outputs
> - Impulse response decays to zero
> - No sustained oscillations

---

## 4-4) Sampling an analog signal

> **Given analog signal:** $$ x_a(t) = 5\cos(2\pi \cdot 50 \cdot t) + 3\cos(2\pi \cdot 1000 \cdot t) $$
> 
> - $A_1 = 5$, $F_1 = 50$ Hz
> - $A_2 = 3$, $F_2 = 1000$ Hz
> - Sampling: $F_s = 5000$ Hz

### (a) Is there aliasing?

> [!code]- MATLAB — 4-4: Aliasing Check with Verification Pattern
> 
> ```matlab
> %% Spørgsmål 4-4: Sampling og aliasing
> 
> % Given analog signal: xa(t) = 5*cos(2π*50*t) + 3*cos(2π*1000*t)
> A1 = 5;   F1 = 50;      % First component
> A2 = 3;   F2 = 1000;    % Second component
> Fs4 = 5000;             % Sampling frequency
> 
> % Check aliasing using verification pattern
> F_Nyquist = Fs4/2;
> fprintf('\n=== Problem 4-4: Aliasing Check ===\n');
> fprintf('Nyquist frequency: %.0f Hz\n\n', F_Nyquist);
> 
> fprintf('Component 1: F1 = %.0f Hz\n', F1);
> if F1 < F_Nyquist
>     fprintf('  %.0f < %.0f → NO aliasing ✓\n\n', F1, F_Nyquist);
> else
>     fprintf('  %.0f >= %.0f → ALIASING! ⚠️\n\n', F1, F_Nyquist);
> end
> 
> fprintf('Component 2: F2 = %.0f Hz\n', F2);
> if F2 < F_Nyquist
>     fprintf('  %.0f < %.0f → NO aliasing ✓\n\n', F2, F_Nyquist);
> else
>     fprintf('  %.0f >= %.0f → ALIASING! ⚠️\n\n', F2, F_Nyquist);
> end
> ```

**Analysis:**

Nyquist frequency: $F_{Nyquist} = F_s/2 = 2500$ Hz

- $F_1 = 50$ Hz: $50 < 2500$ ✓ **No aliasing**
- $F_2 = 1000$ Hz: $1000 < 2500$ ✓ **No aliasing**

$$ \boxed{\text{No aliasing — both frequencies are below Nyquist (2500 Hz)}} $$

### (b) Sample and plot signal (0 to 0.05 seconds)

> [!code]- MATLAB — 4-4: Sampling and Plotting
> 
> ```matlab
> % Sample the signal (0 to 0.05 seconds)
> t4 = 0:1/Fs4:0.05;
> x4_sampled = A1*cos(2*pi*F1*t4) + A2*cos(2*pi*F2*t4);
> 
> % OPTION 1: Continuous plot (more illustrative, recommended)
> figure;
> plot(t4, x4_sampled, 'b', 'LineWidth', 1.5);
> grid on;
> xlabel('Time [s]');
> ylabel('Amplitude');
> title('F25 Problem 4-4: Sampled Signal (50 Hz + 1000 Hz)');
> xlim([0 0.05]);
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_4_Sampled_Plot.png'), ...
>                'Resolution', 300);
> 
> % OPTION 2: Stem plot (shows discrete nature)
> figure;
> stem(t4, x4_sampled, 'b', 'LineWidth', 1.5, 'MarkerSize', 4);
> grid on;
> xlabel('Time [s]');
> ylabel('Amplitude');
> title('F25 Problem 4-4: Sampled Signal - Discrete (Stem)');
> xlim([0 0.05]);
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_4_Sampled_Stem.png'), ...
>                'Resolution', 300);
> ```

> [!tip] Exam Hint from Student Solutions The exam hint suggests using `plot()` instead of `stem()` for discrete-time signals because it is "more illustrative" (mere illustrativt), even though time is discrete. Both are valid, but `plot()` makes it easier to observe the waveforms.

**Continuous plot (recommended for visualization):**

![[Images/DSP_Exam_F25_4_4_Sampled_Plot.png]]

**Stem plot (shows discrete nature):**

![[Images/DSP_Exam_F25_4_4_Sampled_Stem.png]]

**Observation:** The sampled signal shows:

- Slow oscillation: 50 Hz component (large amplitude)
- Fast ripple: 1000 Hz component (superimposed on slow wave)
- Combined signal is "bumpy" due to high-frequency content

---

## 4-5) Filter the sampled signal

### (a) What does the filter do to each component?

The filter is a **lowpass** with $f_{-3dB} = 400$ Hz.

|Component|Frequency|Relative to cutoff|Effect|
|---|---|---|---|
|$F_1 = 50$ Hz|In passband|$50 \ll 400$|**Passes through** (minimal attenuation)|
|$F_2 = 1000$ Hz|In stopband|$1000 > 400$|**Attenuated** (significant reduction)|

$$ \boxed{\text{50 Hz component passes; 1000 Hz component is attenuated}} $$

### (b) Filter using MATLAB and compare

> [!code]- MATLAB — 4-5: Filter and Overlay Plot
> 
> ```matlab
> %% Spørgsmål 4-5: Filter signalet
> 
> fprintf('\n=== Problem 4-5: Filtering ===\n');
> 
> % Filter the signal using the lowpass filter from 4-1
> y4_filtered = filter(B4, A4, x4_sampled);
> 
> % OVERLAY PLOT: Both signals on same axes (matches student solution)
> figure;
> plot(t4, x4_sampled, 'b', 'LineWidth', 1.5);
> hold on;
> plot(t4, y4_filtered, 'r', 'LineWidth', 1.5);
> hold off;
> 
> grid on;
> xlabel('Tid (s)');
> ylabel('Amplitude (a.u.)');
> title('F25 Problem 4-5: Sampled vs Filtered Signal');
> legend('Sampled signal', 'Filtered signal', 'Location', 'best');
> xlim([0 0.05]);
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_5_Overlay.png'), ...
>                'Resolution', 300);
> 
> % OPTIONAL: Separate subplots for detailed view
> figure;
> subplot(2,1,1);
> plot(t4, x4_sampled, 'b', 'LineWidth', 1.5);
> grid on;
> xlabel('Time [s]');
> ylabel('Amplitude');
> title('Input: x[n] = 50 Hz + 1000 Hz');
> xlim([0 0.05]);
> 
> subplot(2,1,2);
> plot(t4, y4_filtered, 'r', 'LineWidth', 1.5);
> grid on;
> xlabel('Time [s]');
> ylabel('Amplitude');
> title('Output: y[n] (After Lowpass Filter)');
> xlim([0 0.05]);
> 
> exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_4_5_Separate.png'), ...
>                'Resolution', 300);
> 
> % Analysis
> fprintf('\nFilter effect:\n');
> fprintf('  - 50 Hz (in passband):   PASSES ✓\n');
> fprintf('  - 1000 Hz (in stopband): ATTENUATED ✓\n');
> fprintf('  - Result: Smooth 50 Hz sine wave\n\n');
> ```

![[Images/DSP_Exam_F25_4_5_Overlay.png]]

> [!tip] Plot Comparison **Overlay plot (recommended):**
> 
> - Shows both signals on same axes
> - Direct visual comparison
> - Matches student solution format
> 
> **Separate subplots (optional):**
> 
> - Detailed view of each signal
> - Easier to see individual characteristics

**Separate subplots for detailed view:**

![[Images/DSP_Exam_F25_4_5_Separate.png]]

### (c) Observations and Analysis

**From the overlay plot:**

1. **Blue signal (input):**
    
    - Shows both slow 50 Hz oscillation AND fast 1000 Hz ripple
    - Appears "bumpy" due to high-frequency component
    - Amplitude varies between approximately ±8
2. **Red signal (output):**
    
    - Only the slow 50 Hz oscillation remains
    - Smooth sine wave (no high-frequency ripple)
    - Slightly reduced amplitude due to passband attenuation
    - Clean, filtered result
3. **Filter effectiveness:**
    
    - 50 Hz component: **Passes through** (in passband, < 400 Hz)
    - 1000 Hz component: **Removed** (in stopband, > 400 Hz)
    - The overlay clearly shows the smoothing effect
4. **Transient behavior:**
    
    - Small startup transient at t = 0 (first ~0.01 s)
    - Due to filter initial conditions (IIR filter)
    - Settles to steady-state response quickly

$$ \boxed{\text{Lowpass filter successfully removes 1000 Hz, leaving smooth 50 Hz signal}} $$

> [!success] Conclusion The 3rd-order IIR lowpass filter (cutoff = 400 Hz) effectively:
> 
> - ✅ Preserves the low-frequency component (50 Hz)
> - ✅ Attenuates the high-frequency component (1000 Hz)
> - ✅ Produces a clean, smooth output
> 
> **Result:** The filtered signal is a smooth 50 Hz sine wave, demonstrating successful lowpass filtering.

---

# Appendix — Butterworth Lowpass Prototype (ε = 1, 3 dB)

|Order $n$|Denominator polynomial|
|:-:|:--|
|1|$s + 1$|
|2|$s^2 + 1.4142s + 1$|
|3|$s^3 + 2s^2 + 2s + 1$|
|4|$s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1$|
|5|$s^5 + 3.2361s^4 + 5.2361s^3 + 5.2361s^2 + 3.2361s + 1$|
|6|$s^6 + 3.8637s^5 + 7.4641s^4 + 9.1416s^3 + 7.4641s^2 + 3.8637s + 1$|

All have numerator = 1.

---

# Quick Reference — Key Formulas

## Sampling & Aliasing

$$ F_{Nyquist} = \frac{F_s}{2}, \qquad F_{alias} = |F - k \cdot F_s| \text{ (folded into } [0, F_s/2]) $$

## Pre-warping (BLT)

$$ \Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2F_s \tan\left(\pi \frac{F}{F_s}\right) $$

## Butterworth Order

$$ n \geq \frac{\log_{10}\left(\frac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\log_{10}(\text{ratio})} $$

- **Lowpass:** ratio = $\Omega_s / \Omega_p$
- **Highpass:** ratio = $\Omega_p / \Omega_s$

## Bilinear Transform

$$ s = \frac{2}{T_s} \cdot \frac{1 - z^{-1}}{1 + z^{-1}} $$

## Linear Phase FIR (Symmetric)

$$ H(\omega) = e^{-j\omega M/2} \cdot A(\omega), \qquad |H(\omega)| = |A(\omega)|, \qquad \angle H(\omega) = -\frac{M}{2}\omega $$

## Stability

- **Stable:** All poles strictly inside unit circle ($|p| < 1$)
- **Marginally stable:** At least one pole ON unit circle ($|p| = 1$)
- **Unstable:** At least one pole outside unit circle ($|p| > 1$)