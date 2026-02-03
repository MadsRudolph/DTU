> Quick refs: [[Digital Filter Design — IIR (Part 2)]]
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 13 Tirsdag.pdf]]
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 13 Tirsdag solutions.pdf]]
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE13/Tirsdag.mlx>)

---

# Week 13 — Highpass Filters (FIR Fourier Design + IIR BLT)

---

# Exercise 1 — FIR Highpass Filters
w
## **Given (shared for all of Exercise 1)**

- Filter design method: **Fourier transformation design**
- Filter type: **Highpass FIR filter**
- Sampling frequency:  
  $$F_s = 2000\ \text{Hz}$$
- Normalised digital cutoff frequency:  
  $$f_c = 500\ \text{Hz} \cdot T_s = 0.25 \quad\Rightarrow\quad \omega_c = 2\pi f_c = \frac{\pi}{2}$$

---

# **Exercise 1-A**

## **Task**
1. Write the expression for the ideal highpass impulse response.  
2. Insert the filter parameters into the expression.

## **Solution**

The ideal lowpass impulse response is

$$
h_{\text{LP}}[n] = 
\begin{cases}
\dfrac{\sin(\omega_c n)}{\pi n}, & n\neq 0, \\
\dfrac{\omega_c}{\pi}, & n = 0.
\end{cases}
$$

The ideal highpass is obtained via **spectral inversion**:

$$
h_{\text{HP}}[n] = \delta[n] - h_{\text{LP}}[n].
$$

Since  
$$\omega_c = \frac{\pi}{2},$$  
we get:

$$
h_{\text{LP}}[0] = \frac{1}{2}, \qquad
h_{\text{HP}}[0] = 1 - \frac{1}{2} = \frac{1}{2}.
$$

---

# **Exercise 1-B**

## **Task**
Let $n$ vary from $-30$ to $30$.

1. Plot the impulse response of the ideal HP filter.  
2. Argue whether the impulse response is causal.  
3. Argue whether the impulse response is finite or infinite.

## **Solution**

### Plot  
![[DSP_U13_Tirsdag_1B_hp_ideal_impulse.png]]

### Interpretation
- The impulse response is **non-zero for negative $n$** → **non-causal**.  
- The ideal formula extends to infinite $|n|$ → **infinite impulse response**.

---

# **Exercise 1-C — FIR1 (9 taps)**

## **Task**
Given  
$$N_{\text{taps}} = 9,$$  
do the following:

1. Compute the filter order  
   $$M = N_{\text{taps}} - 1.$$
2. Compute the symmetry index  
   $$K = M/2.$$
3. Calculate the FIR coefficients using the truncated ideal highpass impulse response  
   $$b[n] = h_{\text{HP}}[n - K].$$
4. Write the transfer function  
   $$H_{\text{FIR1}}(z) = \sum_{n=0}^{8} b[n]z^{-n}.$$

---

## **Solution**

### **1) Compute M and K**

For a Type-I linear-phase FIR filter:

$$
N_{\text{taps}} = 2K + 1
$$

Given:

$$
N_{\text{taps}} = 9 = 2K + 1
$$

So:

$$
K = 4, \qquad M = N_{\text{taps}} - 1 = 8.
$$

Thus the symmetric index runs from:

$$
n = -4, -3, -2, -1, 0, 1, 2, 3, 4.
$$

---

### **2) Ideal highpass impulse response**

From Exercise 1-A, the ideal HP filter is:

$$
h_{\text{HP}}[n] = \delta[n] - h_{\text{LP}}[n],
$$

with

$$
h_{\text{LP}}[n] =
\begin{cases}
\dfrac{\sin(\omega_c n)}{\pi n}, & n\neq 0 \\
\dfrac{\omega_c}{\pi}, & n=0
\end{cases}
$$

and

$$
\omega_c = \frac{\pi}{2}.
$$

So:

- At \(n = 0\):

$$
h_{\text{HP}}[0] = 1 - \frac{\omega_c}{\pi}
= 1 - \frac{1}{2}
= 0.5.
$$

- For $n \neq 0$:

$$
h_{\text{HP}}[n]
= -\,\frac{\sin\!\left(\frac{\pi}{2}n\right)}{\pi n}.
$$

---

### **3) Truncation and shifting to form FIR1**

To obtain a causal FIR filter:

$$
b[n] = h_{\text{HP}}[n-K], \qquad K = 4,\quad n = 0,\dots,8.
$$

This extracts the **central 9 samples** of the ideal HP response and shifts them so the filter becomes **causal**.

---

### **4) MATLAB computation**

> [!code]- MATLAB — FIR1 Coefficients  
> ```matlab
Taps = 9  
M = Taps - 1  
K = (Taps - 1)/2  
n = -K:K  
bFIR1 = -(omegac/pi).*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2  
bFIR1(center) = (pi - omegac)/pi  
>```

This yields:

$$
b = 
[0.0000,\ 
0.1061,\ 
-0.0000,\ 
-0.3183,\ 
0.5000,\ 
-0.3183,\ 
-0.0000,\ 
0.1061,\ 
0.0000].
$$

Because the filter is symmetric:

$$
\begin{aligned}
b_0 &= b_8 = 0.0000, \\
b_1 &= b_7 = 0.1061, \\
b_2 &= b_6 = -0.0000, \\
b_3 &= b_5 = -0.3183, \\
b_4 &= 0.5000.
\end{aligned}
$$

This confirms that FIR1 is a **Type-I linear-phase FIR filter**.

---

### **5) Transfer function**

Using:

$$
H_{\text{FIR1}}(z)
= \sum_{n=0}^{8} b_n z^{-n},
$$

we obtain:

$$
\boxed{
H_{\text{FIR1}}(z)
= 0.1061z^{-1}
- 0.3183z^{-3}
+ 0.5000z^{-4}
- 0.3183z^{-5}
+ 0.1061z^{-7}
}
$$

(All terms with zero coefficients are omitted for clarity.)

---

### **Summary**

- FIR1 uses **9 taps**, hence **M = 8**, **K = 4**  
- Coefficients come from **truncating** the ideal highpass response  
- The filter is **causal** and **linear-phase**  
- Transfer function built directly from the coefficients


---

# **Exercise 1-D — FIR1 Impulse Response**

## **Task**
1. Plot the FIR1 impulse response for $n = -30\dots 30$.  
2. Argue whether the filter is causal.  
3. Argue whether the filter is finite or infinite.

## **Solution**

### Plot  
![[DSP_U13_Tirsdag_1D_FIR1_impulse.png]]

### Interpretation
- Non-zero only for $0 \le n \le 8$ → **causal**.  
- Only 9 taps → **finite impulse response**.

---

# **Exercise 1-E — Frequency Response of FIR1**

## **Task**
1. Explain what **b** and **a** represent in `freqz`.  
2. Compute the **physical cutoff frequency** corresponding to $f_c$.  
3. Compute and plot the magnitude frequency response.  
4. Mark the cutoff frequency on the plot.

## **Solution**

### Explanation
- **b** = numerator FIR coefficients  
- **a** = denominator coefficients (FIR → $a = 1$)

### Physical cutoff  
$$
f_c = \tilde f_c \cdot F_s = 0.25 \cdot 2000 = 500\ \text{Hz}.
$$

### Magnitude plot  
![[DSP_U13_Tirsdag_1E_FIR1_mag.png]]

### Phase plot  
![[DSP_U13_Tirsdag_1E_FIR1_phase.png]]

Cutoff correctly appears at **500 Hz**.

---

# **Exercise 1-F — FIR2 & FIR3 Filter Comparison**

## **Task**
Given:

- FIR2: $N_{\text{taps}} = 19$  
- FIR3: $N_{\text{taps}} = 29$

Do the following:

1. Compute  
   $$M = N_{\text{taps}} - 1$$  
   for both FIR2 and FIR3.
2. Compute  
   $$K = \frac{M}{2}$$  
   for both filters.
3. Compute the filter coefficients using the Fourier design method.  
4. Compute and plot the magnitude frequency responses of FIR1, FIR2, and FIR3.

---

## **Solution**

FIR2 and FIR3 use the **same Fourier design principle** as FIR1.  
For a Type-I linear-phase FIR filter:

$$
N_{\text{taps}} = 2K + 1
$$

This guarantees:

- symmetry: $b_n = b_{M-n}$  
- linear phase  
- a center coefficient at $n = K$

---

## **1) Compute $M$ and $K$**

### **FIR2**
$$
N_{\text{taps}} = 19 = 2K + 1
$$

Solving:

$$
K = 9,\qquad M = N_{\text{taps}} - 1 = 18
$$

### **FIR3**
$$
N_{\text{taps}} = 29 = 2K + 1
$$

Solving:

$$
K = 14,\qquad M = 28
$$

Thus the symmetric indices are:

- FIR2: $n = -9,\dots,9$  
- FIR3: $n = -14,\dots,14$

Increasing $N_{\text{taps}}$ increases the **window width** of the ideal impulse response, improving the filter.

---

## **2) Compute the FIR coefficients (same method as FIR1)**

The ideal highpass response is:

$$
h_{\text{HP}}[n] = \delta[n] - \frac{\sin(\omega_c n)}{\pi n},
\qquad \omega_c = \frac{\pi}{2}.
$$

For $n = 0$:

$$
h_{\text{HP}}[0] = 1 - \frac{1}{2} = 0.5.
$$

For $n \neq 0$:

$$
h_{\text{HP}}[n]
= -\,\frac{\sin\left(\frac{\pi}{2} n\right)}{\pi n}.
$$

We then truncate:

$$
n = -K,\dots,K
$$

and shift to obtain causal coefficients:

$$
b[n] = h_{\text{HP}}[n - K],\qquad n = 0,\dots,M.
$$

### MATLAB for FIR2

> [!code]- MATLAB — FIR2  
> ```matlab
Taps = 19  
M = Taps - 1  
K = (Taps - 1)/2  
n = -K:K  
bFIR2 = -(omegac/pi)*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2  
bFIR2(center) = (pi - omegac)/pi  
aFIR2 = [1];  
[HFIR2, fFIR2] = freqz(bFIR2, aFIR2, 1024, Fs);
>```
### MATLAB for FIR3

> [!code]- MATLAB — FIR3  
> ```matlab
Taps = 29  
M = Taps - 1  
K = (Taps - 1)/2  
n = -K:K  
bFIR3 = -(omegac/pi)*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2  
bFIR3(center) = (pi - omegac)/pi  
aFIR3 = [1];  
[HFIR3, fFIR3] = freqz(bFIR3, aFIR3, 1024, Fs);
>```
---

## **3) Plot the magnitude responses**

![[DSP_U13_Tirsdag_1F_FIR123_mag.png]]

---

## **4) Interpretation**

### **Sharper Transition Band**
A larger number of taps means a **longer window** in the time domain.  
Truncation acts like multiplying the ideal HP impulse response by a rectangular window $w[n]$:

$$
h_{\text{FIR}}[n] = h_{\text{ideal}}[n] \cdot w[n].
$$

This corresponds to convolution with a sinc in the frequency domain.

As $N_{\text{taps}}$ increases:

- the main lobe of the sinc becomes **narrower**,  
- the frequency response becomes **closer to ideal**,  
- the **transition band becomes sharper**.

Thus:

- FIR1 (9 taps): widest transition  
- FIR2 (19 taps): sharper  
- FIR3 (29 taps): even sharper and closest to the ideal HP response

---

### **Improved Stopband Attenuation**
A longer impulse response reduces leakage into the stopband:

- sidelobes shrink  
- stopband ripple is lower  
- overall attenuation improves

---

### **Linear Phase**
Because all these FIRs are Type-I with symmetric coefficients:

$$
b[n] = b[M - n],
$$

they maintain:

$$
H(e^{j\omega}) = A(\omega)\,e^{-j\omega M/2}.
$$

Thus all FIR1–FIR3 have **perfectly linear phase**, regardless of tap count.

---

## **Summary**

- FIR2 and FIR3 simply use **more samples** of the ideal highpass impulse response.  
- Increasing $N_{\text{taps}}$ improves:
  - transition sharpness  
  - stopband attenuation  
  - approximation to the ideal HP filter
- Phase remains **linear** for all three filters.

> **Key takeaway:**  
> $$\text{More taps} \quad \Rightarrow \quad \text{closer to ideal frequency response}.$$

---

# Exercise 2 — IIR Highpass Filter (BLT)

## **Given (shared for all of Exercise 2)**

- Filter design method: **BLT (α = 2/Ts)**  
- Sampling frequency:  
  $$F_s = 2000\ \text{Hz}$$
- Normalized passband frequency:  
  $$f_p = 500\ \text{Hz}\cdot T_s = 0.25$$
- Prototype filter: **4th-order Butterworth** (ε = 1)

---

# **Exercise 2-A — Analog Filter Characteristics**

## **Task**
1. Use the BLT prewarping formula to compute the analog passband angular frequency $\Omega_p$ and the corresponding physical passband frequency $F_p$.  
2. Write the analog **prototype lowpass** transfer function for a 4th-order Butterworth filter with $\varepsilon = 1$.  
3. State which substitution converts the prototype lowpass filter into a highpass filter in the $s$-domain.

---

## **Solution**

### **1) Compute the normalized passband frequencies**

We are given:

- Normalized passband frequency:  
  $$f_p = 500\ \text{Hz} \cdot T_s = \frac{500}{2000} = 0.25$$

- Corresponding digital angular passband frequency:  
  $$
  \omega_p = 2\pi f_p = 2\pi \cdot 0.25 = 0.50\pi.
  $$

These values determine where the analog filter must have its cutoff after prewarping.

---

### **2) Apply BLT prewarping to determine $\Omega_p$**

The bilinear transform uses:

$$
\alpha = \frac{2}{T_s}.
$$

The prewarped analog angular frequency is:

$$
\Omega_p = \frac{2}{T_s}\,\tan\!\left(\frac{\omega_p}{2}\right)
= \alpha \,\tan\!\left(\frac{\omega_p}{2}\right).
$$

This ensures that the digital passband edge $\omega_p$ maps exactly to the analog passband edge $\Omega_p$.

The corresponding **analog passband frequency in hertz** is:

$$
F_p = \frac{\Omega_p}{2\pi}.
$$

These values are used in the upcoming LP→HP transformation.

---

### **3) Write the analog prototype 4th-order Butterworth LP transfer function**

The normalized 4th-order Butterworth lowpass prototype with $\varepsilon = 1$ has transfer function:

$$
H_{\text{LP}}(s)
= \frac{1}{s^{4}
+ 2.6131s^{3}
+ 3.4142s^{2}
+ 2.6131s
+ 1 }.
$$

This form comes directly from the standard Butterworth pole polynomial of order 4.

---

### **4) State the analog lowpass → highpass transformation**

To convert the prototype lowpass filter into a **highpass** filter with passband edge $\Omega_p$, we use the classic substitution:

$$
s \;\longrightarrow\; \frac{\Omega_p}{s}.
$$

This inversion in frequency swaps low-frequency gain with high-frequency gain, turning the Butterworth LP into a Butterworth HP.

---

### **Summary**

- Normalized passband:  
  $$f_p = 0.25,\qquad \omega_p = 0.5\pi.$$
- BLT prewarping gives:  
  $$\Omega_p = \frac{2}{T_s}\tan\left(\frac{\omega_p}{2}\right).$$
- Physical passband:  
  $$F_p = \Omega_p / (2\pi).$$
- Prototype LP filter:  
  $$
  H_{\text{LP}}(s)=\frac{1}{s^{4}+2.6131s^{3}+3.4142s^{2}+2.6131s+1}.
  $$
- LP→HP transformation:  
  $$
  s\rightarrow \frac{\Omega_p}{s}.
  $$


---

# **Exercise 2-B — Analog Highpass Transfer Function**

## **Task**
1. Calculate and state the analog highpass filter coefficients $\alpha_k$ and $\beta_k$.  
2. Explain how the constant term $\alpha_0$ is related to the prewarped analog passband frequency $\Omega_p$.  
3. Write the highpass transfer function $H_{\text{HP}}(s)$ in the $s$-domain.

---

## **Solution**

We start from the **prototype 4th-order Butterworth lowpass filter** (from Exercise 2-A):

$$
H_{\text{LP}}(s)
= \frac{1}{s^{4} + 2.6131s^{3} + 3.4142s^{2} + 2.6131s + 1 }.
$$

To transform this LP filter into a HP filter with analog cutoff $\Omega_p$, we use the substitution:

$$
s \;\longrightarrow\; \frac{\Omega_p}{s}.
$$

This transformation **inverts the frequency axis**, turning the LP into a HP filter.

---

## **1) Apply LP → HP substitution**

Starting with:

$$
H_{\text{HP}}(s)
= H_{\text{LP}}\!\left(\frac{\Omega_p}{s}\right)
= 
\frac{1}{
\left(\frac{\Omega_p}{s}\right)^{4}
+ 2.6131\left(\frac{\Omega_p}{s}\right)^{3}
+ 3.4142\left(\frac{\Omega_p}{s}\right)^{2}
+ 2.6131\left(\frac{\Omega_p}{s}\right)
+ 1 }.
$$

Factor the denominator:

$$
H_{\text{HP}}(s)
= \frac{1}{
\frac{\Omega_p^{4}}{s^{4}}
+ 2.6131\frac{\Omega_p^{3}}{s^{3}}
+ 3.4142\frac{\Omega_p^{2}}{s^{2}}
+ 2.6131\frac{\Omega_p}{s}
+ 1 }.
$$

Multiply numerator and denominator by $s^{4}$:

$$
H_{\text{HP}}(s)
= \frac{s^{4}}{
\Omega_p^{4}
+ 2.6131\Omega_p^{3}s
+ 3.4142\Omega_p^{2}s^{2}
+ 2.6131\Omega_p s^{3}
+ s^{4} }.
$$

Now we can clearly identify the HP coefficients.

---

## **2) Identify $\beta_k$ and $\alpha_k$**

The general HP form is:

$$
H_{\text{HP}}(s)
=
\frac{
\beta_4 s^{4} + \beta_3 s^{3} + \beta_2 s^{2} + \beta_1 s + \beta_0
}{
\alpha_4 s^{4} + \alpha_3 s^{3} + \alpha_2 s^{2} + \alpha_1 s + \alpha_0
}.
$$

From the derived expression:

### **Numerator coefficients**
The numerator is simply:

$$
s^{4}
\quad\Rightarrow\quad
\beta_4 = 1,\qquad
\beta_3 = \beta_2 = \beta_1 = \beta_0 = 0.
$$

### **Denominator coefficients**

From:

$$
\alpha_4 s^{4}
+ \alpha_3 s^{3}
+ \alpha_2 s^{2}
+ \alpha_1 s
+ \alpha_0
=
s^{4}
+ 2.6131\Omega_p s^{3}
+ 3.4142\Omega_p^{2} s^{2}
+ 2.6131\Omega_p^{3} s
+ \Omega_p^{4},
$$

we directly obtain:

- $\alpha_4 = 1$
- $\alpha_3 = 2.6131\Omega_p$
- $\alpha_2 = 3.4142\Omega_p^{2}$
- $\alpha_1 = 2.6131\Omega_p^{3}$
- $\alpha_0 = \Omega_p^{4}$

These match the MATLAB results from `lp2hp`.

---

## **3) How is $\alpha_0$ related to $\Omega_p$?**

We clearly see:

$$
\boxed{\alpha_0 = \Omega_p^{4}}.
$$

This comes from the constant term of the denominator after substitution:

$$
\left(\frac{\Omega_p}{s}\right)^4.
$$

**Important note:**  
Different normalizations are possible — some designers divide numerator and denominator by $\Omega_p^{4}$ so that $\alpha_0 = 1$ instead.

---

## **4) MATLAB verification**

> [!code]- MATLAB — lp2hp Coefficient Conversion  
> ```matlab
Beta_PLP = [1];  
Alpha_PLP = [1 2.6131 3.4142 2.6131 1];  
[Beta_HP, Alpha_HP] = lp2hp(Beta_PLP, Alpha_PLP, Omega_p);
>```

The Toolbox extracts:

- $\alpha_4 =$ Alpha\_HP(1)  
- $\alpha_3 =$ Alpha\_HP(2)  
- $\alpha_2 =$ Alpha\_HP(3)  
- $\alpha_1 =$ Alpha\_HP(4)  
- $\alpha_0 =$ Alpha\_HP(5)$ = \Omega_p^{4}$  

And:

- $\beta_4 = 1$  
- $\beta_3 = \beta_2 = \beta_1 = \beta_0 = 0$

---

## **5) Final highpass transfer function**

$$
H_{\text{HP}}(s)
=
\frac{s^{4}}{
s^{4}
+ 2.6131\Omega_p s^{3}
+ 3.4142\Omega_p^{2} s^{2}
+ 2.6131\Omega_p^{3} s
+ \Omega_p^{4}
}.
$$

---

## **Summary**

- The LP→HP substitution $s \rightarrow \Omega_p/s$ yields a correct analog HP filter.
- Numerator becomes $s^{4}$ → $\beta_4 = 1$.  
- Denominator becomes a polynomial whose constant term is:

$$
\alpha_0 = \Omega_p^{4}.
$$

- MATLAB `lp2hp` reproduces the same coefficients.


---

# **Exercise 2-C — Analog Magnitude Response**

## **Task**
1. Plot the magnitude frequency response of the analog highpass filter $H(s)$ as a function of **frequency (Hz)**, not angular frequency.  
2. Mark the analog passband frequency $F_p$ found in Exercise 2-A.  
3. Comment on whether $|H(F_p)|$ equals the expected Butterworth value of $1/\sqrt{2}$.

---

## **Solution**

### **1) Create a frequency axis in Hz**

The solution sheet uses a **linear frequency axis**:

- Start at $0$ Hz  
- End at $2000$ Hz  
- Convert to angular frequency using  
  $$
  \Omega = 2\pi F.
  $$

This ensures the plot looks exactly like the figure in the provided solution.

### **2) Evaluate the analog highpass filter using `freqs`**

The command:

$$
H_{\text{analog}}(j\Omega) = \text{freqs}(\beta,\alpha,\Omega)
$$

returns the continuous-time frequency response.

### **3) Expected magnitude at $F_p$**

For a 4th-order Butterworth filter:

$$
|H(F_p)| = \frac{1}{\sqrt{2}} \approx 0.707.
$$

### **Plot**

![[DSP_U13_Tirsdag_2C_analog_HP_mag.png]]

### **Interpretation**

At the marked point $F_p$:

$$
|H(F_p)| \approx \frac{1}{\sqrt{2}} = 0.707,
$$

which matches the Butterworth **−3 dB** passband condition.

This confirms the design is correct.

---

# **Exercise 2-D — Digital Highpass Filter via Bilinear Transform**

## **Task**
1. Use the bilinear transform (BLT) to convert the **analog highpass filter** $H_{\text{HP}}(s)$ into a **digital highpass filter** $H_{\text{HP}}(z)$.  
2. Compute the resulting digital filter coefficients $b_k$ and $a_k$ (rounded to 4 decimals).  
3. Write the complete digital transfer function in the $z$-domain.

---

## **Solution**

After completing Exercise 2-B, we have the **analog highpass filter**:

$$
H_{\text{HP}}(s)
= \frac{\beta_4 s^4 + \beta_3 s^3 + \beta_2 s^2 + \beta_1 s + \beta_0}
{\alpha_4 s^4 + \alpha_3 s^3 + \alpha_2 s^2 + \alpha_1 s + \alpha_0}.
$$

To convert this analog filter into a **digital IIR filter**, we apply the **bilinear transform**:

$$
s = \frac{2}{T_s}\,\frac{1 - z^{-1}}{1 + z^{-1}},
$$

which preserves stability and warps all analog frequencies into the digital domain.

MATLAB performs this transformation using the command:

> [!code]- MATLAB — Bilinear Transform  
> ```matlab
[b_z, a_z] = bilinear(b_hp, a_hp, Fs);
>```

This produces the digital numerator coefficients ($b_k$)  
and digital denominator coefficients ($a_k$).

---

## **1) Digital filter numerator coefficients**

From MATLAB output:

$$
B = [0.0940,\; -0.3759,\; 0.5639,\; -0.3759,\; 0.0940].
$$

Thus:

- $b_0 = 0.0940$
- $b_1 = -0.3759$
- $b_2 = 0.5639$
- $b_3 = -0.3759$
- $b_4 = 0.0940$

This symmetric pattern is expected for a **4th-order highpass** derived from a Butterworth prototype.

---

## **2) Digital filter denominator coefficients**

MATLAB computes:

$$
A = [1.0000,\; -0.0000,\; 0.4860,\; -0.0000,\; 0.0177].
$$

Thus:

- $a_0 = 1$
- $a_1 = 0$
- $a_2 = 0.4860$
- $a_3 = 0$
- $a_4 = 0.0177$

The zeros in odd positions occur because the original analog HP filter was **even-order and symmetric**, and the BLT preserves this structure.

---

## **3) Digital transfer function**

The digital IIR highpass filter is therefore:

$$
H_{\text{HP}}(z)
=
\frac{
0.0940
- 0.3759z^{-1}
+ 0.5639z^{-2}
- 0.3759z^{-3}
+ 0.0940z^{-4}
}{
1
+ 0z^{-1}
+ 0.4860z^{-2}
+ 0z^{-3}
+ 0.0177z^{-4}
}.
$$

This is the final digital highpass filter obtained using:

- analog Butterworth design  
- LP→HP frequency transformation  
- bilinear transform (BLT)

It is a **stable**, **causal**, **4th-order IIR** highpass filter with cutoff determined by the prewarped frequency $\Omega_p$ from Exercise 2-A.

---

## **Final Remarks**
- The numerator is symmetric → expected for HP.  
- The denominator coefficients match the BLT mapping of the analog poles.  
- This digital filter will show a **sharp highpass response** compared to the FIR filters in Exercise 1.


---

# **Exercise 2-E — Difference Equation & Filter Structure**

## **Task**
1. Write the difference equation corresponding to the digital highpass filter $H_{\text{HP}}(z)$ from Exercise 2-D.  
2. Identify the filter structure (Direct Form I or Direct Form II).

---

## **Solution**

An IIR filter with transfer function  

$$
H(z) = \frac{Y(z)}{X(z)} =
\frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + \cdots + b_M z^{-M}}
     {1 + a_1 z^{-1} + a_2 z^{-2} + \cdots + a_N z^{-N}}
$$

is described in the time domain by the **general difference equation**:

$$
y[n]
= b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] + \cdots + b_M x[n-M]
- a_1 y[n-1] - a_2 y[n-2] - \cdots - a_N y[n-N].
$$

For the highpass filter computed in Exercise 2-D we have:

### **Numerator coefficients**
$$
b_0 = 0.0940,\qquad
b_1 = -0.3759,\qquad
b_2 = 0.5639,\qquad
b_3 = -0.3759,\qquad
b_4 = 0.0940.
$$

### **Denominator coefficients**
$$
a_0 = 1,\qquad
a_1 = 0,\qquad
a_2 = 0.4860,\qquad
a_3 = 0,\qquad
a_4 = 0.0177.
$$

---

## **Difference equation for this filter**

Substituting the specific $b_k$ and $a_k$ values:

$$
\begin{aligned}
y[n] =\;&
0.0940\,x[n]
- 0.3759\,x[n-1]
+ 0.5639\,x[n-2]
- 0.3759\,x[n-3]
+ 0.0940\,x[n-4] \\
&\;-\; 0\,y[n-1]
-\; 0.4860\,y[n-2]
-\; 0\,y[n-3]
-\; 0.0177\,y[n-4].
\end{aligned}
$$

Or more compactly:

$$
y[n] = 0.0940x[n]
- 0.3759x[n-1]
+ 0.5639x[n-2]
- 0.3759x[n-3]
+ 0.0940x[n-4]
- 0.4860y[n-2]
- 0.0177y[n-4].
$$

This is exactly the form shown in the solution sheet.

---

## **Filter Structure**

Once the coefficients are known, the filter can be implemented using:

### **Direct Form I**
- Separate FIR section (the $b_k$ terms)  
- Followed by IIR feedback section (the $a_k$ terms)  
- Two delay lines

### **Direct Form II (Transposed or Normal)**
- Combines delays  
- Uses one delay line of length $\max(M, N)$  
- More memory-efficient and used in many DSP systems

Both structures satisfy the difference equation above and match the diagrams in the lecture notes (Figures 8.6 and 8.8).

---

## **Summary**
- The difference equation directly follows from the BLT-derived coefficients.  
- The filter can be drawn or implemented as **Direct Form I** or **Direct Form II** depending on memory requirements.  
- The numerator is symmetric (as expected for a 4th-order highpass), while the denominator maintains even-order IIR symmetry.



---

# **Exercise 2-F — Digital Magnitude Response**

## **Task**
1. Explain what the vectors $b$ and $a$ represent when used in the MATLAB command `freqz`.  
2. Compute the **physical passband frequency** $F_p$ of the digital highpass filter.  
3. Use `freqz` to compute and plot the digital magnitude frequency response $|H_{\text{HP}}(e^{j\omega})|$.  
4. Mark the passband frequency $F_p$ on the plot.

---

## **Solution**

After Exercise 2-D, we have the digital highpass filter coefficients:

### Numerator (feedforward)
$$
b = [0.0940,\; -0.3759,\; 0.5639,\; -0.3759,\; 0.0940]
$$

### Denominator (feedback)
$$
a = [1.0000,\; 0,\; 0.4860,\; 0,\; 0.0177]
$$

These are used directly by the MATLAB frequency-response command:

> $$
 [H, f] = \text{freqz}(b,\, a,\, N,\, F_s)
 $$

---

## **1) Meaning of $a$ and $b$ in `freqz`**

- The vector **$b$** contains the **numerator coefficients** of the digital filter:
  $$
  b_0 + b_1 z^{-1} + b_2 z^{-2} + \cdots + b_M z^{-M}.
  $$

- The vector **$a$** contains the **denominator coefficients**:
  $$
  1 + a_1 z^{-1} + a_2 z^{-2} + \cdots + a_N z^{-N}.
  $$

Thus, `freqz(b,a,…)` computes the frequency response of:

$$
H_{\text{HP}}(z)
=
\frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + b_3 z^{-3} + b_4 z^{-4}}
     {1 + a_1 z^{-1} + a_2 z^{-2} + a_3 z^{-3} + a_4 z^{-4}}.
$$

---

## **2) Compute the physical passband frequency**

We use the normalized digital passband frequency:

$$
f_p = 500\ \text{Hz}\cdot T_s = 0.25.
$$

Multiplying by the sampling frequency:

$$
F_p = f_p \cdot F_s = 0.25 \cdot 2000 = 500\ \text{Hz}.
$$

So the digital passband edge is **500 Hz**.

---

## **3) MATLAB computation**

> [!code]- MATLAB — Digital frequency response  
> ```matlab
[HPdigital, fDigital] = freqz(b, a, 1024, Fs);  
Fp = fp_tilde * Fs;
>```

`freqz` returns:

- `HPdigital`: complex frequency response  
- `fDigital`: corresponding frequency vector in **Hz**

---

## **4) Plot**

In the plot below:

- The **vertical blue line** marks the passband frequency  
  $$F_p = 500\ \text{Hz}.$$
- The **horizontal blue line** marks the Butterworth magnitude level  
  $$|H(F_p)| = \frac{1}{\sqrt{2}}.$$

![[DSP_U13_Tirsdag_2F_IIR_HP_mag.png]]

---

## **Interpretation**

- The digital highpass filter shows the expected **S-shaped Butterworth response**.  
- At the passband edge:
  $$
  |H(F_p)| \approx \frac{1}{\sqrt{2}} \approx 0.707,
  $$
  confirming the **−3 dB** Butterworth condition.  
- Above the cutoff, the magnitude tends toward 1, as expected for a highpass filter.


---

# **Exercise 2-G — FIR vs IIR Comparison**

## **Task**
In Exercise 1, three different FIR highpass filters (FIR1, FIR2, FIR3) were designed using Fourier transformation.

Now:

1. Plot the magnitude responses of these FIR filters **together with the IIR highpass filter** from Exercise 2.  
2. Comment on similarities and differences between the FIR filters and the IIR filter.  
3. Discuss advantages and disadvantages of the designed FIR and IIR filters.

---

## **Solution**

To make the comparison fair, all filters are evaluated using the same frequency grid:

- FIR1: $N_{\text{taps}} = 9$  
- FIR2: $N_{\text{taps}} = 19$  
- FIR3: $N_{\text{taps}} = 29$  
- IIR HP: 4th-order Butterworth transformed via BLT

---

## **MATLAB (for reference)**

> [!code]- MATLAB — Frequency responses  
> ```matlab
% FIR1  
Taps = 9;  M = Taps-1;  K = (Taps-1)/2;  
n = -K:K;  
bFIR1 = -(omegac/pi)*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2;  
bFIR1(center) = (pi-omegac)/pi;  
aFIR1 = [1];  
[HFIR1, fFIR1] = freqz(bFIR1, aFIR1, 1024, Fs);
>
% FIR2  
Taps = 19; M = Taps-1; K = (Taps-1)/2;  
n = -K:K;  
bFIR2 = -(omegac/pi)*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2;  
bFIR2(center) = (pi-omegac)/pi;  
aFIR2 = [1];  
[HFIR2, fFIR2] = freqz(bFIR2, aFIR2, 1024, Fs);
>
% FIR3  
Taps = 29; M = Taps-1; K = (Taps-1)/2;  
n = -K:K;  
bFIR3 = -(omegac/pi)*sin(n.*omegac)./(n.*omegac);  
center = 0.5 + length(n)/2;  
bFIR3(center) = (pi-omegac)/pi;  
aFIR3 = [1];  
[HFIR3, fFIR3] = freqz(bFIR3, aFIR3, 1024, Fs);
>
% IIR HP (digital)  
[HPdigital, fDigital] = freqz(b_z, a_z, 1024, Fs);
>```
---

## **Plot**

![[DSP_U13_Tirsdag_2G_FIR_vs_IIR_mag.png]]

**Color meaning **

- **Red** — IIR highpass filter  
- **Blue** — FIR1 ($N=9$)  
- **Orange** — FIR2 ($N=19$)  
- **Yellow** — FIR3 ($N=29$)

The passband frequency $F_p = 500$ Hz is marked with a vertical green line.  
The horizontal green line marks the Butterworth level $|H(F_p)| = 1/\sqrt{2}$.

---

# **Discussion**

## **1) FIR vs IIR — Visual comparison**

### **Transition sharpness**
- FIR1 (9 taps) has a **very wide transition band**.  
- FIR2 (19 taps) improves significantly.  
- FIR3 (29 taps) is the sharpest FIR and approaches IIR performance.  
- The IIR filter shows the **sharpest transition** because Butterworth designs allow high roll-off with low order.

### **Ripple / Oscillations**
- All FIR filters show **Gibbs oscillations** due to truncating the ideal impulse response.  
- The IIR Butterworth filter has **no oscillations** and a smooth monotonic magnitude curve.

### **Passband magnitude at cutoff**
- For the 4th-order Butterworth IIR filter:
  $$
  |H(F_p)| = \frac{1}{\sqrt{2}} \approx 0.707.
  $$
- For the FIR filters, the cutoff magnitude is:
  - FIR1 ≈ 0.5  
  - FIR2 ≈ 0.5  
  - FIR3 ≈ 0.5  
  because Fourier-designed FIR HP filters satisfy:
  $$
  h_{\text{HP}}[0] = 1 - \frac{\omega_c}{\pi} = 0.5,
  $$
  giving a magnitude of about 0.5 around the cutoff.

---

## **2) Advantages & disadvantages**

### **FIR Filters**

**Advantages**
- **Perfect linear phase** (due to symmetric coefficients).  
- Always **stable** (no feedback).  
- Conceptually simple, easy to design from ideal prototype.  
- FIR3 (29 taps) gives good approximation of IIR without instability risk.

**Disadvantages**
- Require **many taps** (long impulse response) for sharp transitions.  
- More computations per sample → higher CPU cost.  
- Show **Gibbs ripple** in transition and stopband regions.

---

### **IIR Butterworth Filter**

**Advantages**
- **Much sharper transition** for the same effective order.  
- Very **efficient** (only 4 poles).  
- No Gibbs oscillations → smooth magnitude response.  
- Small memory footprint.

**Disadvantages**
- **Nonlinear phase**, causing waveform distortion unless compensated.  
- Must ensure **stability** (feedback structure).  
- More sensitive to coefficient quantization.

---

## **Conclusion**

- FIR filters approximate the ideal highpass response but require many taps.  
- Increasing FIR order improves transition sharpness but cannot beat IIR efficiency.  
- The IIR highpass filter gives:
  - sharper transition  
  - Butterworth monotonic behavior  
  - but nonlinear phase  
- Choice between FIR and IIR depends on:  
  - **Phase linearity requirements**  
  - **Stability guarantees**  
  - **Computational resources**  
  - **Ripple tolerance**

