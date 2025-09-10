# Electromagnetism – Transmission Line Fundamentals

---

## Wave Equation (Telegrapher’s Equations)

**Voltage & Current Wave Equations**  
$$
\frac{d^2 \tilde{V}(z)}{dz^2} = \gamma^2 \tilde{V}(z), \quad
\frac{d^2 \tilde{I}(z)}{dz^2} = \gamma^2 \tilde{I}(z)
$$

**Solutions**  
$$
\tilde{V}(z) = \tilde{V}_0^+ e^{-\gamma z} + \tilde{V}_0^- e^{+\gamma z}
$$
$$
\tilde{I}(z) = \tilde{I}_0^+ e^{-\gamma z} + \tilde{I}_0^- e^{+\gamma z}
$$
- $\gamma = \alpha + j\beta = \sqrt{Z'_s Y'_p}$ = propagation constant.  
- $\alpha$ = attenuation constant (Np/m), $\beta$ = phase constant (rad/m).  
- **Meaning:** Voltage and current propagate as damped waves along $z$.  

🔗 Related: [[Wave Parameters]] — $\alpha$ and $\beta$ come from the general wave definitions.  

---

## Distributed Circuit Parameters

Per-unit-length parameters (lumped-element model):  
- $R'$ = series resistance (Ω/m) of conductors  
- $L'$ = series inductance (H/m)  
- $G'$ = shunt conductance (S/m) of dielectric  
- $C'$ = shunt capacitance (F/m)  

**Equivalent relations:**  
$$
Z'_s = R' + j\omega L' , \quad Y'_p = G' + j\omega C'
$$

---

## Lossless TEM Transmission Line

**Phase Velocity**  
$$
v_p = \frac{1}{\sqrt{\mu \varepsilon}}
= \frac{c_0}{\sqrt{\varepsilon_r \mu_r}}
$$
- $c_0 = 1/\sqrt{\mu_0 \varepsilon_0} \approx 3\cdot 10^8 \,\text{m/s}$ (speed of light).  
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Wave Parameters]] — $v_p$ is the same phase velocity defined for general waves.  

---

**Propagation Constant**  
$$
\gamma = j\beta = j\omega \sqrt{\mu \varepsilon}
= j\frac{\omega}{v_p}
$$
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Single Terminated TL]] — $\gamma$ determines how reflections decay or shift phase in a terminated line.  

---

**Characteristic Impedance**  
$$
Z_0 = \sqrt{\frac{L'}{C'}} = \sqrt{\frac{\mu}{\varepsilon}} \, K
$$
- $K =$ geometry factor (depends on line type).  
- In free space: $\eta_0 = \sqrt{\mu_0/\varepsilon_0} \approx 377\,\Omega$.  
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Single Terminated TL]] — $Z_0$ is used directly in the reflection coefficient and input impedance formulas.  

---

## Common TEM Line Parameters (Lossless)

**Coaxial Line**  
$$
C' = \frac{2 \pi \varepsilon}{\ln(b/a)}, \quad
L' = \frac{\mu}{2\pi} \ln\!\left(\frac{b}{a}\right), \quad
Z_0 = \frac{60}{\sqrt{\varepsilon_r}} \ln\!\left(\frac{b}{a}\right)
$$
- $a =$ inner radius, $b =$ outer radius.  
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

**Two-Wire Line** (wire radius $a$, spacing $D$)  
$$
C' = \frac{\pi \varepsilon}{\ln(D/a)}, \quad
L' = \frac{\mu}{\pi} \ln(D/a), \quad
Z_0 = \frac{120}{\sqrt{\varepsilon_r}} \ln(D/a)
$$

**Parallel Plate Line** (plate width $w$, separation $d$)  
$$
C' = \frac{\varepsilon w}{d}, \quad
L' = \frac{\mu d}{w}, \quad
Z_0 = \frac{d}{w} \sqrt{\frac{\mu}{\varepsilon}}
$$
