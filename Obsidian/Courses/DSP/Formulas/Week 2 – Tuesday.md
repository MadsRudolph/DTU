#  DT Systems & LTI Systems

## System Properties
- **Linearity**: $T(\alpha_1x_1+\alpha_2x_2)=\alpha_1T(x_1)+\alpha_2T(x_2)$
- **Time-invariance**: $T(D_kx)=D_k(Tx)$
- **Causality**: depends only on present/past inputs
- **Stability (BIBO)**: bounded input ⇒ bounded output

---

## LTI Systems
- Impulse response: $h[n]=T\delta[n]$
- **Main theorem**:  
  $$
  y[n]=(h*x)[n]
  $$
- **FIR** if $h[n]$ finite, **IIR** if infinite

---

## Example
Difference eqn: $y[n]-\tfrac12 y[n-1]=x[n]$  
Impulse response: $h[n]=(1/2)^n u[n]$

---

## Stability
- Stable ⇔ $\sum_n |h[n]| < \infty$

---

🔗 **References**
- [[Week 1 – Thursday]]: Convolution identity
- [[Week 2 – Thursday]]: Difference equations in frequency domain
- [[Week 3 – Tuesday]]: Frequency response $H(\omega)$ = DTFT of $h[n]$
