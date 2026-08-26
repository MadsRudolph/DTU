---
tags: [LCD, regulering, eksamen, Final-Test, loesningsguide]
kilde: "Final Test Exam (Short version).pdf"
eksamen: Final Test (øve-eksamen)
format: Blandet — MC + 2 regneopgaver, fuldt facit
---

# Final Test — Komplet løsningsguide

> [!info] Om dette sæt
> Officielt øve-eksamenssæt med **11 opgaver**: Q1–Q6 og Q9–Q11 er multiple choice, **Q7 er en fuld PI-Lead-regneopgave**, og Q8 er en ja/nej-analyse. Fuldt facit. Q7 er det bedste fuldt-gennemregnede PI-Lead-eksempel i hele materialet. Alle MATLAB-blokke kørt og verificeret.

## Hurtig oversigt

| # | Type | Emne | Svar |
|---|---|---|---|
| 1 | T2 | Blokdiagram (indre+ydre loop) | **2** |
| 2 | T1 | Linearisér om $y=2$ | **2** ($\frac{0.8}{s^2+s+0.6}$) |
| 3 | T3 | $\omega_n$ fra step-periode | **4** ($\approx30$ rad/s) |
| 4 | T3 | $\zeta$ fra overshoot | **3** ($0.5$) |
| 5 | T8 | PM & GM fra Nyquist | **2** ($\gamma_M=60°$, $K_M=1.4$) |
| 6 | T7 | Gain margin for PM=60° | **3** ($18$ dB) |
| 7 | T10 | **PI-Lead fuld design** | $K_P=6.61$ |
| 8 | T4 | Steady-state error (PI servomotor) | begge **NEJ** |
| 9 | T9 | PI-design fra Bode | **1** ($K_P=0.1$, $\tau_i=1$) |
| 10 | T9/T10 | Controller-strategi (1. orden) | **3** (PI) |
| 11 | T10 | Reducér overshoot | **2** (pre-filter) |

---

## Q1 — Blokdiagram *(T2)*

**Hvad spørges om:** Find $G(s)$ for: $a\to K_p\to A\to\frac1s\to w$, med indre feedback $B$ om integratoren + ydre unity feedback.

> [!formula] Reduktion indefra
> $$G_i=\frac{A\frac1s}{1+A\frac1s B}=\frac{A}{s+AB},\qquad G=\frac{K_p G_i}{1+K_p G_i}=\frac{K_p A}{s+A(K_p+B)}$$

```matlab hl:/feedback\(/
syms A B Kp s
Gi = (A/s)/(1+(A/s)*B);
G  = simplify((Kp*Gi)/(1+Kp*Gi))   % Kp*A/(s+A*(Kp+B))
```

**Svar:** $\boxed{G(s)=\dfrac{K_p A}{s+A(K_p+B)} \Rightarrow \text{Mulighed 2}}$

→ Metode: [[Blokdiagram-reduktion]]

## Q2 — Linearisér om $y=2$ *(T1)*

**Hvad spørges om:** $15\dot y+5u\ddot y+9y=2u^2$, linearisér om $y_0=2$. Find $\Delta y/\Delta u$.

**Metode:** Steady state: $9y_0=2u_0^2 \Rightarrow u_0=\sqrt{9\cdot2/2}=3$. Linearisér: $\ddot y_0=0$ → $5\ddot y_0\Delta u$-leddet bortfalder; $2u^2\to4u_0\Delta u=12\Delta u$.

> [!formula] Resultat
> $$15s\Delta y+15s^2\Delta y+9\Delta y=12\Delta u \;\Rightarrow\; \frac{\Delta y}{\Delta u}=\frac{12}{15s^2+15s+9}=\frac{0.8}{s^2+s+0.6}$$

**Svar:** $\boxed{G(s)=\dfrac{0.8}{s^2+s+0.6} \Rightarrow \text{Mulighed 2}}$ — mulighed 1 glemmer at dividere med 15.

→ Metode: [[Transfer-functions-og-poler]] · Teori: [[Lec 5 — Black-box Modelling og Linearisering]]

## Q3 — $\omega_n$ fra step-periode *(T3)*

**Hvad spørges om:** Aflæs $\omega_n$ fra oscillationsperioden $T\approx0.21$ s i step-responsen.

> [!formula] Periode → frekvens
> $$\omega_n\approx\frac{2\pi}{T}=\frac{2\pi}{0.21}\approx30\text{ rad/s}$$

**Svar:** $\boxed{\omega_n\approx30\text{ rad/s} \Rightarrow \text{Mulighed 4}}$

> [!note] Tilnærmelse
> Strengt taget er $T=\frac{2\pi}{\omega_d}$ med $\omega_d=\omega_n\sqrt{1-\zeta^2}$. Med $\zeta=0.5$ (Q4) ville $\omega_n\approx34.6$ — men 30 er klart den nærmeste mulighed, så dæmpningskorrektionen ignoreres.

→ Metode: [[Time-response-2nd-order]]

## Q4 — $\zeta$ fra overshoot *(T3)*

**Hvad spørges om:** Peak $\approx1.16$ → $M_p\approx0.16$. Find $\zeta$.

> [!formula] Overshoot → dæmpning
> $$\zeta=\frac{-\ln 0.16}{\sqrt{\pi^2+(\ln 0.16)^2}}\approx0.5 \quad(\text{kontrol: }\zeta=0.5\Rightarrow M_p=0.163)$$

```matlab hl:N
Mp = 0.16;
zeta = -log(Mp)/sqrt(pi^2+log(Mp)^2);   % = overshoot2damping(0.16)
fprintf('zeta = %.4g\n', zeta);          % 0.504
```

**Svar:** $\boxed{\zeta\approx0.5 \Rightarrow \text{Mulighed 3}}$

→ Metode: [[Time-response-2nd-order]]

## Q5 — PM & GM fra Nyquist *(T8)*

**Hvad spørges om:** Aflæs phase margin og gain margin fra Nyquist (ingen RHP-poler). Kurven krydser neg. reel akse ved $\approx-0.7$.

> [!formula] Aflæsning
> $$\gamma_M=60°\ (\text{vinkel ved enhedscirkel-kryds}),\qquad K_M=\frac{1}{0.7}\approx1.4$$

**Svar:** $\boxed{\gamma_M=60°,\ K_M\approx1.4 \Rightarrow \text{Mulighed 2}}$

→ Metode: [[Stabilitet-Nyquist-margins]]

## Q6 — Gain margin for PM=60° *(T7)*

**Hvad spørges om:** $G(s)=\frac{600}{(s+0.1)(s+20)(s+30)}$. Hvilken gain margin (dB) hvis P-controller designes til PM=60°?

**Metode:** Find $\omega$ hvor fase $=-120°$ (giver PM=60°). Aflæs $|G|\approx-18$ dB der → gain skal hæves $+18$ dB.

```matlab hl:/bode\(/
s=tf('s'); G=600/((s+0.1)*(s+20)*(s+30));
w=logspace(-2,3,3e5); [m,ph]=bode(G,w); m=squeeze(m); ph=squeeze(ph);
i=find(ph<=-120,1,'first');
fprintf('wc=%.4g, |G|=%.4g dB -> KM=%.4g dB (lineær %.4g)\n',w(i),20*log10(m(i)),-20*log10(m(i)),1/m(i));
```

**Svar:** $\boxed{K_M=18\text{ dB} \Rightarrow \text{Mulighed 3}}$ (eksakt $17.1$ dB).

> [!warning] Enheds-fælde
> Spørgsmålet vil have $K_M$ i **dB**. Mulighed 5 ($7.9$) er den *lineære* ratio af samme svar ($10^{18/20}\approx7.9$). Læs enheden!

→ Metode: [[Bode-aflæsning]] · [[Controller-design-P-PI-Lead]]

## Q7 — PI-Lead fuld design *(T10)* ⭐

**Hvad spørges om:** Design PI-Lead $C(s)=K_P\frac{\tau_i s+1}{\tau_i s}\frac{\tau_d s+1}{\alpha\tau_d s+1}$ for $G(s)=\frac{600}{(s+0.1)(s+20)(s+30)}$ med $N_i=3$, $\alpha=0.2$, $\gamma_M=60°$. Find $K_P$, $\tau_i$, $\tau_d$.

**Metode (4 trin — den centrale design-procedure):**

> [!formula] Trin 1 — fasebidrag og crossover
> $$\phi_i=\arctan\tfrac{-1}{N_i}=-18.44°,\qquad \phi_m=\arcsin\tfrac{1-\alpha}{1+\alpha}=41.81°$$
> Find $\omega_c$ hvor $\angle G=-180°-\gamma_M-\phi_i-\phi_m=-143.37°$ → $\omega_c=12.29$ rad/s.

> [!formula] Trin 2–4 — tidskonstanter og gain
> $$\tau_i=\frac{N_i}{\omega_c}=0.244\text{ s},\quad \tau_d=\frac{1}{\omega_c\sqrt\alpha}=0.182\text{ s},\quad K_P=\frac{1}{|C(j\omega_c)G(j\omega_c)|}=6.61$$

```matlab hl:/bode\(|evalfr\(/
s=tf('s'); G=600/((s+0.1)*(s+20)*(s+30));
Ni=3; alpha=0.2; gM=60;
phi_i=atand(-1/Ni); phi_m=asind((1-alpha)/(1+alpha));
% find wc hvor angle(G) = -180-gM-phi_i-phi_m... (her: -143.37 grader)
w=logspace(-1,3,4e5); [~,ph]=bode(G,w); ph=squeeze(ph);
wc=w(find(ph<=-143.37,1,'first'));
taui=Ni/wc; taud=1/(wc*sqrt(alpha));
CPI=(taui*s+1)/(taui*s); CD=(taud*s+1)/(alpha*taud*s+1);
Kp=1/abs(evalfr(G*CPI*CD,1j*wc));
[~,PM]=margin(Kp*G*CPI*CD);
fprintf('wc=%.4g, taui=%.4g, taud=%.4g, Kp=%.4g, PM=%.4g\n',wc,taui,taud,Kp,PM);
```

**Svar:** $\boxed{K_P=6.61,\ \tau_i=0.244\text{ s},\ \tau_d=0.182\text{ s}}$

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 9 — PI-Lead Design med Specifikationer]] · Snydeark: [[MATLAB-snydeark]]

## Q8 — Steady-state error (PI servomotor) *(T4)*

**Hvad spørges om:** Servomotor med PI-controller. Er der stationær fejl på (a) reference-step? (b) disturbance-step?

**Metode:** Plant er Type-1 (integrator hastighed→position). PI tilføjer endnu en integrator → loopet er Type-2-agtigt. Anvend FVT:

> [!formula] Begge fejl → 0
> $$e_{ss,r}=\lim_{s\to0}\frac{s^2\tau_i(\dots)}{s^2\tau_i(\dots)+K_PK_\tau(\tau_i s+1)}=\frac{0}{K_PK_\tau}=0$$
> Disturbance-error har faktor $s$ i tæller → også $0$. **Integratoren i PI fjerner begge stationære fejl.**

**Svar:** $\boxed{\text{(a) NEJ}\quad\text{(b) NEJ}}$ — ingen stationær fejl i nogen af tilfældene.

→ Metode: [[Steady-state-error-og-disturbance]]

## Q9 — PI-design fra Bode *(T9)*

**Hvad spørges om:** PI-controller $C=K_P\frac{\tau_i s+1}{\tau_i s}$. Vælg parametre for bedste stabilitet+performance. Gain margin er kun $6$ dB; fase krydser $-180°$ ved $\omega\approx1$.

**Metode:** Begrænset gain margin + integratorens fasetab ($-45°$ ved $\omega_i=1/\tau_i$) → vælg **lavt** $K_P$. Med $\tau_i=1$ ligger zero ved $\omega=1$. Lav margin tvinger $K_P=0.1$.

**Svar:** $\boxed{K_P=0.1,\ \tau_i=1 \Rightarrow \text{Mulighed 1}}$ — de høj-$K_P$-muligheder overskrider den smalle margin.

→ Metode: [[Controller-design-P-PI-Lead]]

## Q10 — Controller-strategi (1. orden) *(T9/T10)*

**Hvad spørges om:** $G(s)=\frac{6}{0.83s+1}$ (identificeret model). Krav: stabilt, hurtigt, statisk fejl $<10\%$. Bedste strategi?

**Metode:** Modellen er kun en approksimation → urealistisk at jage ekstrem bandbredde. Vælg $\omega_c$ nær den dominante pol ($1/0.83\approx1.2$ rad/s) + brug **PI** for statisk fejl.

**Svar:** $\boxed{\omega_c=1.2\text{ rad/s},\ \tau_i=0.2\text{ s},\ K_P=0.06\ (\text{PI}) \Rightarrow \text{Mulighed 3}}$ — mulighed 2 ($\omega_c=800$, $K_P=100$) er urealistisk for en approksimeret model.

→ Metode: [[Controller-design-P-PI-Lead]]

## Q11 — Reducér overshoot *(T10/T13)*

**Hvad spørges om:** PI-Lead (Lead i feedback-gren) giver for stort overshoot. Hvad hjælper?

**Metode:** Et **pre-filter** på referencen dæmper hurtige reference-ændringer → mindre overshoot **uden** at ændre loopets stabilitet.

**Svar:** $\boxed{\text{Tilføj pre-filter } G_f(s)=\dfrac{1}{s+1} \Rightarrow \text{Mulighed 2}}$

> [!note] Forkerte
> Flytte Lead til forward = **mere** overshoot (mindre PM); lavpas i feedback = ekstra fasetab; ekstra Lead-prefilter = mere højfrekvent gain → mere overshoot.

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]]

---

## Nøgletermer

| Term | Formel |
|---|---|
| Indre loop reduktion | $G_i=\frac{A/s}{1+AB/s}=\frac{A}{s+AB}$ |
| $\omega_n$ fra periode | $\omega_n\approx2\pi/T$ |
| PI-Lead fasebudget | $\angle G(\omega_c)=-180°-\gamma_M-\phi_i-\phi_m$ |
| PI fjerner stat. fejl | integrator → Type$+1$ |
| Pre-filter | dæmper ref-step uden at røre loopet |

→ Metoder: [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]] · [[Time-response-2nd-order]] | Snydeark: [[MATLAB-snydeark]] | Oversigt: [[00_Eksamensanalyse_og_strategi]]
