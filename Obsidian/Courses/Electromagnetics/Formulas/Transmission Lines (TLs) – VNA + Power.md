	
## 1. Power on a Lossless Transmission Line (Chap. 2-9)

- **Forward & reflected voltage waves**  
  $$
  V(z) = V_0^+ e^{-j\beta z} + V_0^- e^{+j\beta z}
  $$

- **Current**  
  $$
  I(z) = \frac{V_0^+}{Z_0} e^{-j\beta z} - \frac{V_0^-}{Z_0} e^{+j\beta z}
  $$

- **Reflection coefficient at load**  
  $$
  \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}, 
  \quad V_0^- = \Gamma_L V_0^+
  $$

- **Average power carried by forward wave**  
  $$
  P_f = \frac{|V_0^+|^2}{2Z_0}
  $$

- **Average power carried by reflected wave**  
  $$
  P_r = \frac{|V_0^-|^2}{2Z_0} = |\Gamma_L|^2 P_f
  $$

- **Power delivered to load**  
  $$
  P_L = P_f - P_r = \frac{|V_0^+|^2}{2Z_0}\,(1 - |\Gamma_L|^2)
  $$

---

## 2. Smith Chart Essentials (Chap. 2-10)

- **Normalized impedance**  
  $$
  z = \frac{Z_L}{Z_0} = r + jx
  $$

- **Reflection coefficient (in terms of z)**  
  $$
  \Gamma = \frac{z - 1}{z + 1}
  $$

- **Normalized admittance (duality)**  
  $$
  y = \frac{1}{z} = g + jb
  $$

- **VSWR (Standing Wave Ratio)**  
  $$
  S = \frac{1 + |\Gamma|}{1 - |\Gamma|}
  $$

👉 Smith chart plots constant-$|\Gamma|$ circles (VSWR circles), and can convert between **impedance ↔ admittance** by rotating 180°.

---


- **Instantaneous power**  
  $$
  p(t) = V_A(t)\, I_A(t)
  $$

- **Time-average power**  
  $$
  \bar{P} = \tfrac{1}{2}\,\Re\{ \tilde{V}_A \tilde{I}_A^* \}
  $$

- With load impedance $Z_A$ and generator impedance $Z_g$:  
  $$
  \tilde{V}_A = \frac{Z_A}{Z_A + Z_g}\,\tilde{V}_0,
  \quad 
  \tilde{I}_A = \frac{\tilde{V}_0}{Z_A + Z_g}
  $$

- **Power delivered to load**  
  $$
  \bar{P}_A = \frac{1}{2}\,\Re\!\left\{\frac{Z_A}{(Z_A+Z_g)(Z_A^*+Z_g^*)}\right\}\,|\tilde{V}_0|^2
  $$

- **Maximum (available) power transfer** (impedance matching $Z_A = Z_g^*$):  
  $$
  P_{\text{av}} = \frac{|\tilde{V}_0|^2}{8R_g}
  $$

- **Power dissipated in generator (at match)**  
  $$
  P_d = P_{\text{av}}
  $$

---
