# Z-Transform

## 1. Definition

- **Z-transform**
  $$
  X(z) = \mathcal{Z}\{x[n]\} = \sum_{n=-\infty}^{\infty} x[n] z^{-n}
  $$

- **Examples**
  - $\mathcal{Z}\{\delta[n]\} = 1$
  - $\mathcal{Z}\{\delta[n-k]\} = z^{-k}$
  - $\mathcal{Z}\{a^n u[n]\} = \frac{1}{1 - a z^{-1}} = \frac{z}{z-a}, \quad |z| > |a|$
  - $\mathcal{Z}\{-a^n u[-n-1]\} = \frac{1}{1 - a z^{-1}} = \frac{z}{z-a}, \quad |z| < |a|$

---

## 2. Region of Convergence (ROC)

- **Definition**
  $$
  \text{ROC} = \{z \in \mathbb{C} \;|\; \sum_{n=-\infty}^{\infty} |x[n]| |z|^{-n} < \infty \}
  $$

- **Theorems**
  - For **causal** $x[n]$:  
    $$
    \text{ROC} = \{ z \;|\; |z| > r \}, 
    \quad r = \lim_{n \to \infty} \Big|\frac{x[n+1]}{x[n]}\Big|
    $$
  - For **anti-causal** $x[n]$:  
    $$
    \text{ROC} = \{ z \;|\; |z| < R \}, 
    \quad R = \lim_{n \to \infty} \Big|\frac{x[-n]}{x[-n-1]}\Big|
    $$
  - For **two-sided** $x[n]$:  
    $$
    \text{ROC} = \{ z \;|\; r < |z| < R \}
    $$

- **Link to DTFT**  
  $$
  X(e^{j\omega}) = X(z)\big|_{z = e^{j\omega}}
  $$
  DTFT exists if the **unit circle** is within ROC.

---

## 3. Inverse Z-Transform

- **General integral (not used in practice here)**  
  $$
  x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} \, dz
  $$

- **In practice**:  
  Identify from known pairs or use **partial fraction expansion**.

---

## 4. Properties of the Z-Transform

- **Linearity**  
  $$
  c_1 x_1[n] + c_2 x_2[n] 
  \;\;\xleftrightarrow{\mathcal{Z}}\;\;
  c_1 X_1(z) + c_2 X_2(z)
  $$

- **Time-shifting**  
  $$
  x[n-k] \;\;\xleftrightarrow{\mathcal{Z}}\;\; z^{-k} X(z)
  $$

- **Modulation**  
  $$
  a^n x[n] \;\;\xleftrightarrow{\mathcal{Z}}\;\; X\!\left(\tfrac{z}{a}\right)
  $$

- **Multiplication by $n$**  
  $$
1$$


- **Convolution (in time)**  
  $$
  (x_1 * x_2)[n] \;\;\xleftrightarrow{\mathcal{Z}}\;\; X_1(z) \cdot X_2(z)
  $$

---

## 5. Example: Causal Cosine Signal

- Signal:  
  $$
  x[n] = \cos(\omega_0 n) u[n]
  $$

- Using Euler’s identity:  
  $$
  x[n] = \tfrac{1}{2} e^{j \omega_0 n} u[n] + \tfrac{1}{2} e^{-j \omega_0 n} u[n]
  $$

- Z-transform:  
  $$
  X(z) = \tfrac{1}{2} \cdot \frac{1}{1 - e^{j\omega_0} z^{-1}} 
       + \tfrac{1}{2} \cdot \frac{1}{1 - e^{-j\omega_0} z^{-1}}
  $$

- Simplified form:  
  $$
  X(z) = \frac{1 - \cos(\omega_0) z^{-1}}{1 - 2 \cos(\omega_0) z^{-1} + z^{-2}}, 
  \quad |z| > 1
  $$

---

🔗 **References**
- [[Week 2 – Thursday]]: DTFT is a special case on the **unit circle** ($z = e^{j\omega}$)
- [[Week 3 – Tuesday]]: Frequency response $H(\omega)$ = $H(z)$ evaluated on the unit circle
- [[Week 2 – Tuesday]]: Difference equations solved in frequency-domain via Z-transform
