# Week 2 Problems (MOSFET)

## Problem 1
**Task:**  
NMOS transistors, given W/L = 8, μnCox = 180 μA/V², Vt = 0.4 V, λ = 0.  
Find **VD1, VS2, VD3**.
![[Pasted image 20250912094031.png]]
**Formulas Needed:**  
- **Operating regions (NMOS):**
  - Cutoff: $V_{GS} \leq V_t \implies I_D = 0$  
  - Triode: $V_{DS} < V_{GS} - V_t$  
    $$
    I_D = \mu_n C_{ox} \frac{W}{L}\left[(V_{GS}-V_t)V_{DS} - \tfrac{1}{2}V_{DS}^2\right]
    $$  
  - Saturation: $V_{DS} \geq V_{GS} - V_t$  
    $$
    I_D = \tfrac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS}-V_t)^2
    $$

- **No channel length modulation (λ=0):** $I_D$ independent of $V_{DS}$.

**Solution:**  
*Write your step-by-step solution here...*

---

### Solution

**Given:** (copy from figure)
- [ ] Supply voltages:
- [ ] Transistor params (W/L, μCox, Vt, λ, γ, 2ΦF, λL):
- [ ] Node labels from the schematic:

**Plan:**
1) **Assume region** for each MOSFET (cutoff / triode / saturation) using:
   - NMOS: cutoff if $V_{GS} \le V_t$; sat if $V_{DS} \ge V_{GS}-V_t$; triode otherwise.
   - PMOS (use magnitudes): sat if $|V_{DS}| \ge |V_{GS}|-|V_{tp}|$.
2) **Compute $I_D$** using the region’s equation (include body effect if $V_{SB}\ne 0$):
   - $V_t = V_{to} + \gamma\big(\sqrt{|2\Phi_F + V_{SB}|}-\sqrt{|2\Phi_F|}\big)$
3) **Write KCL/KVL** at the unknown node(s) (resistors, current sources, mirrors, etc.).
4) **Solve** for requested voltages (**VD1**, **VS2**, **VD3**), then **verify** region consistency.
5) If using channel-length modulation: multiply by $(1+\lambda V_{DS})$ (only in saturation).

**Scratch:**
```calc
Assumptions:
- 
Equations:
- 
Numeric solve:
- 
Check regions:
- 
```


## Problem 2
**Task:**  
NMOS (W/L = 8, μnCox = 180 μA/V², Vto = 0.4 V, λ=0, γ = 0.5 √V, |2ΦF|=0.7 V).  
PMOS (W/L = 32, μpCox = 45 μA/V², Vt = −0.42 V, λ=0).  
Find **VD1, VD2, VD3**.
![[Pasted image 20250912094114.png]]
**Formulas Needed:**  
- Same **NMOS/PMOS region conditions** as above.  
- **Body effect:**  
  $$
  V_{t} = V_{to} + \gamma\left(\sqrt{|2\Phi_F + V_{SB}|} - \sqrt{|2\Phi_F|}\right)
  $$
- **PMOS condition (absolute values):**
  - Cutoff: $|V_{GS}| \leq |V_{tp}|$  
  - Triode: $|V_{DS}| < |V_{GS}| - |V_{tp}|$  
  - Saturation: $|V_{DS}| \geq |V_{GS}| - |V_{tp}|$  
- **PMOS current equations:** Same as NMOS but using p-parameters, with sign conventions.

**Solution:**  
*Write your step-by-step solution here...*

---

### Solution

**Given:** (copy from figure)
- [ ] Supply voltages:
- [ ] Transistor params (W/L, μCox, Vt, λ, γ, 2ΦF, λL):
- [ ] Node labels from the schematic:

**Plan:**
1) **Assume region** for each MOSFET (cutoff / triode / saturation) using:
   - NMOS: cutoff if $V_{GS} \le V_t$; sat if $V_{DS} \ge V_{GS}-V_t$; triode otherwise.
   - PMOS (use magnitudes): sat if $|V_{DS}| \ge |V_{GS}|-|V_{tp}|$.
2) **Compute $I_D$** using the region’s equation (include body effect if $V_{SB}\ne 0$):
   - $V_t = V_{to} + \gamma\big(\sqrt{|2\Phi_F + V_{SB}|}-\sqrt{|2\Phi_F|}\big)$
3) **Write KCL/KVL** at the unknown node(s) (resistors, current sources, mirrors, etc.).
4) **Solve** for requested voltages (**VD1**, **VS2**, **VD3**), then **verify** region consistency.
5) If using channel-length modulation: multiply by $(1+\lambda V_{DS})$ (only in saturation).

**Scratch:**
```calc
Assumptions:
- 
Equations:
- 
Numeric solve:
- 
Check regions:
- 
```


## Problem 3
**Task:**  
NMOS (W=16 µm, L=2 µm, μnCox = 180 µA/V², Vt=0.4 V, λL = 0.1 µm/V).  
PMOS (W=30 µm, L=3 µm, μpCox = 45 µA/V², Vt= −0.42 V, λL=0.14 µm/V).  
Find **VD1, VS2, VD3**.
![[Pasted image 20250912094132.png]]
**Formulas Needed:**  
- Same **MOSFET current laws** (triode & saturation).  
- **Channel length modulation:**
  - Effective channel: $L_{eff} = L - \Delta L$  
  - Approximate formula:  
    $$
    I_D = I_{D,sat}(1 + \lambda V_{DS}), \quad \lambda = \frac{\Delta L}{L\cdot V_{DS}}
    $$  
  - Sometimes expressed as $\lambda L$ (given here) → compute $\lambda = (\lambda L)/L$.

**Solution:**  
*Write your step-by-step solution here...*

---

### Solution

**Given:** (copy from figure)
- [ ] Supply voltages:
- [ ] Transistor params (W/L, μCox, Vt, λ, γ, 2ΦF, λL):
- [ ] Node labels from the schematic:

**Plan:**
1) **Assume region** for each MOSFET (cutoff / triode / saturation) using:
   - NMOS: cutoff if $V_{GS} \le V_t$; sat if $V_{DS} \ge V_{GS}-V_t$; triode otherwise.
   - PMOS (use magnitudes): sat if $|V_{DS}| \ge |V_{GS}|-|V_{tp}|$.
2) **Compute $I_D$** using the region’s equation (include body effect if $V_{SB}\ne 0$):
   - $V_t = V_{to} + \gamma\big(\sqrt{|2\Phi_F + V_{SB}|}-\sqrt{|2\Phi_F|}\big)$
3) **Write KCL/KVL** at the unknown node(s) (resistors, current sources, mirrors, etc.).
4) **Solve** for requested voltages (**VD1**, **VS2**, **VD3**), then **verify** region consistency.
5) If using channel-length modulation: multiply by $(1+\lambda V_{DS})$ (only in saturation).

**Scratch:**
```calc
Assumptions:
- 
Equations:
- 
Numeric solve:
- 
Check regions:
- 
```
