# DTFT Properties & LTI in Frequency Domain

## DTFT Properties
- Linearity
- Shift: $x[n-k] \;\leftrightarrow\; e^{-j\omega k}X(\omega)$
- Modulation: $e^{j\omega_0n}x[n]\;\leftrightarrow\;X(\omega-\omega_0)$
- Multiplication by $n$: $nx[n]\;\leftrightarrow\; j\frac{dX}{d\omega}$

---

## Convolution & Multiplication
- Time convolution: $(x_1*x_2)[n] \;\leftrightarrow\; X_1(\omega)X_2(\omega)$
- Time multiplication: $(x_1\cdot x_2)[n]\;\leftrightarrow\;\tfrac{1}{2\pi}\int X_1(\nu)X_2(\omega-\nu)d\nu$

---

## Energy Theorems
- Plancherel: $\sum_n x[n]y^*[n] = \tfrac{1}{2\pi}\int X(\omega)Y^*(\omega)d\omega$
- Parseval: $\sum_n |x[n]|^2 = \tfrac{1}{2\pi}\int |X(\omega)|^2d\omega$

---

## LTI in Frequency Domain
- Frequency response: $H(\omega)=\sum_n h[n]e^{-jn\omega}$
- Relation: $Y(\omega)=H(\omega)X(\omega)$
- Magnitude: $|H(\omega)|$, Phase: $\arg(H(\omega))$

---

## Ideal Filters
- **Low-pass**:  
  $$
  H_{LP}(\omega)=\begin{cases}1,&|\omega|\le\omega_c\\0,&|\omega|>\omega_c\end{cases}
  $$
  Impulse: $h_{LP}[n]=\tfrac{\omega_c}{\pi}\,\text{sinc}(\tfrac{\omega_c}{\pi}n)$
- **High-pass**: $h_{HP}[n]=\delta[n]-h_{LP}[n]$
- **Band-pass**: $h_{BP}[n]=\tfrac{B}{\pi}\,\text{sinc}(\tfrac{B}{2\pi}n)\cos(\omega_0n)$
- **Band-stop**: $h_{BS}[n]=\delta[n]-h_{BP}[n]$

---

🔗 **References**
- [[Week 2 – Thursday]]: DTFT definition
- [[Week 3 – Thursday]]: Z-transform generalizes DTFT and solves difference eqns
