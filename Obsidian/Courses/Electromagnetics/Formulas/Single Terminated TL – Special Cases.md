	# Electromagnetism – Single Terminated TL: Special Cases

---

## Lossless TL
- For lossless lines: $Z_0 \in \mathbb{R}$, $\gamma = j\beta$  
- Reflection coefficient magnitude is unchanged along the line:  
$$
\Gamma_A = \Gamma_B e^{-j2\beta \ell}, \quad |\Gamma_A| = |\Gamma_B|
$$
- Input impedance:  
$$
Z_A = Z_0 \frac{Z_B + j Z_0 \tan(\beta \ell)}{Z_0 + j Z_B \tan(\beta \ell)}
$$

🔗 Related: [[Single Terminated TL]] — this is a refinement of the general input impedance formulas for the special case of a **lossless line**.  

---

## Special Line Lengths Lossless

**Half-wavelength ($\ell = m \lambda/2$)**  

$$
\Gamma_A = \Gamma_B, \quad Z_A = Z_B
$$
- TL is “invisible” to the source.  

**Quarter-wavelength ($\ell = (2m+1)\lambda/4$)**  
$$
\Gamma_A = -\Gamma_B, \quad Z_A = \frac{Z_0^2}{Z_B}
$$
- Impedance inverter (quarter-wave transformer).  
- Links to: [[Courses/Electromagnetics/Exercises/work/3-3.2]]  

🔗 Related: [[Transmission_Lines]] — relies on $Z_0$ and $\beta$ from TL fundamentals.  

---

## Special Terminations

**Matched Load** ($Z_L = Z_0$)  
$$
\Gamma_B = 0, \quad Z_A = Z_0, \quad \text{VSWR} = 1
$$
- No reflections, no standing waves.  

**Passive Load** ($Z_L = R_L + jX_L$, $R_L \geq 0$)  
$$
|\Gamma_B| \leq 1, \quad |\Gamma_A| = |\Gamma_B|
$$
$$
|\Gamma_L| = \left|\frac{Z_L - Z_0}{Z_L + Z_0}\right| \leq 1
$$


**Resistive Load** ($Z_L = R_L > 0$)  
$$
\Gamma_B \in \mathbb{R}, \quad |\Gamma_B| < 1
$$

**Reactive Load** ($Z_L = jX_L$)  
$$
|\Gamma_B| = 1, \quad \text{VSWR} \to \infty
$$
- Full reflection, no power delivered.  


**Short/Open Circuits**  
| **Termination** | **Short**                     | **Open**                  |
|---------------|---------------------|-------------------|
| $Z_L$                | $0$                            | $\infty$                       |
| $\Gamma_L$                | $-1$                          | $1$                        |
| $Z_A$                | $j Z_0 \tan(\beta \ell)$            | $-j Z_0 \cot(\beta \ell)$      |
| VSWR           | $\infty$                          | $\infty$                       |

🔗 Related: [[Wave Parameters]] — standing wave behavior here depends directly on $\lambda$ and $\beta$.  

---

## Stubs (Reactive Elements)

**Short-circuited stub:**  
$$
Z_A = j Z_0 \tan(\beta \ell)
$$

**Open-circuited stub:**  
$$
Z_A = -j Z_0 \cot(\beta \ell)
$$

- Input impedance purely imaginary.  
- Behaves like inductance or capacitance depending on $\ell$:  

| Length range                   | Shorted stub                   | Open stub                          |
| ------------------------------ | ------------------------------ | ---------------------------------- |
| $0 < \ell < \lambda/4$         | $Z_A = j \omega L_{\text{eq}}$ | $Z_A = -j/( \omega C_{\text{eq}})$ |
| $\lambda/4 < \ell < \lambda/2$ | Capacitive                     | Inductive                          |

🔗 Related: [[Transmission_Lines]] — stubs are a practical application of the general $Z_A$ formula.  

---

## TL Characterization (using Open/Short)

Measure impedances with open- and short-circuits:  
$$
Z_A^{sc} = Z_0 \tanh(\gamma \ell), \quad Z_A^{oc} = \frac{Z_0}{\tanh(\gamma \ell)}
$$

For **lossless TL** ($\gamma = j\beta$):  
$$
X_A^{sc} = j Z_0 \tan(\beta \ell), \quad X_A^{oc} = -j Z_0 \cot(\beta \ell)
$$

From measurements:  
$$
R_0 = \sqrt{-X_A^{sc} X_A^{oc}}, \quad
\beta = \frac{1}{\ell} \tan^{-1}\! \sqrt{-\frac{X_A^{sc}}{X_A^{oc}}}
$$

Then:  
$$
u_p = \frac{\omega}{\beta}, \quad
\varepsilon_r = \left(\frac{c_0}{u_p}\right)^2
$$

🔗 Related: [[Wave Parameters]] — $\beta$ and $u_p$ come directly from general wave definitions.  

---

## Summary
- **$\lambda/2$ line**: transparent.  
- **$\lambda/4$ line**: impedance inverter.  
- **Matched load**: no reflection.  
- **Reactive load**: full reflection.  
- **Short/Open**: infinite VSWR.  
- **Stubs**: act as inductors or capacitors.  
- **Measurement method**: open/short loads give $Z_0$ and $\beta$.  

🔗 Related: [[Single Terminated TL]] — this sheet is the extension of general TL termination formulas into **special, practically important cases**.  
