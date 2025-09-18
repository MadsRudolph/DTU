

## Discrete-Time (DT) Signals
- Definition: $x: \mathbb{Z} \to \mathbb{C}$
- **Unit impulse**: $\delta[n] = \begin{cases}1,&n=0\\0,&n\neq 0\end{cases}$
- **Unit step**: $u[n] = \begin{cases}1,&n\ge0\\0,&n<0\end{cases}$
  - Relation: $u[n] = \sum_{k=0}^\infty \delta[n-k]$
- **Exponential**: $x[n]=A\alpha^n$
- **Complex sinusoid**: $x[n]=Ae^{j\omega n}$

Periodicity: $e^{j\omega n}$ is periodic iff $\omega=2\pi k/N$

---

## Sampling & Aliasing
- Discretization: $x[n]=x_a(nT_s)$
- Aliasing: frequencies $F_0+kF_s$ map to the same DT frequency
- Normalized frequencies:  
  $f=\tfrac{F_p}{F_s}, \quad \omega=\tfrac{\Omega_p}{F_s}$  
  with $-1/2 < f \le 1/2,\; -\pi < \omega \le \pi$
- **Shannon theorem**: perfect reconstruction if $F_s > 2F_{\max}$

---

## Convolution
- Definition:  
  $$
  (x*y)[n] = \sum_{k=-\infty}^\infty x[k]y[n-k]
  $$
- Properties: commutative, associative, distributive
- Identity: $x * \delta = x$

---

🔗 **References**
- [[Week 1 – Tuesday]]: Sampling motivation
- [[Week 2 – Tuesday]]: LTI systems defined via convolution
- [[Week 2 – Thursday]]: Convolution property in DTFT
