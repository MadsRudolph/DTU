---
tags: [LCD, regulering, eksamen, REExam-F21, loesningsguide]
kilde: "REExam_F21 with Solutions.pdf"
eksamen: Re-eksamen F21 (aug. 2021)
format: Multiple choice (20 spørgsmål, fuldt facit)
---

# REExam-F21 — Komplet løsningsguide

> [!info] Om dette sæt
> Re-eksamen med **20 multiple-choice-spørgsmål** og fuldt facit + detaljerede løsninger. Q11–Q20 har særligt grundige løsninger (godt til at lære metoderne). Alle MATLAB-blokke er kørt og verificeret.
>
> **OCR-rettelser:** Q10's closed-loop nævner er $s^2+\sqrt{2K}s+K$ (ikke $2\sqrt{2K}$); Q20's $F(s)$-tæller er $s^2+4s+25$ (ikke $21$). Begge bekræftet via facittets egne mellemregninger.

## Hurtig oversigt

| # | Type | Emne | Svar |
|---|---|---|---|
| 1 | T1 | Linearisér motormodel | **1** |
| 2 | T4 | Steady-state bilhastighed | **1** ($40.4$ m/s) |
| 3 | T7 | Poler/nuller fra Bode | **1** (komplekse nuller) |
| 4 | T4 | Steady-state error, sammensat input | **1** ($e_{ss}=1$) |
| 5 | T7 | Bode → TF med RHP-pol | **4** ($\frac{100(s+10)}{s-1}$) |
| 6 | T11 | State space → TF | **5** ($\frac{10}{s+1}$) |
| 7 | T3 | Inverse Laplace | **1** ($5e^{-t}-5e^{-3t}$) |
| 8 | T3 | Step-respons + slutværdi | **1** ($y_{ss}=1$) |
| 9 | T2 | Blokdiagram, multi-loop | **1** |
| 10 | T3 | Procent overshoot | **1** ($4.3\%$) |
| 11 | T4 | DC-gain af kaskade | **b** ($0.8$) |
| 12 | T8 | Nyquist-stabilitet (RHP-pol) | **d** (stabil) |
| 13 | — | Konceptuelt (PM/bandbredde) | **e** |
| 14 | T7/T9 | Gain margin → P-grænse | **e** ($K_P=0.25$) |
| 15 | T10 | Lead-bidrag $M_D$ | **a** ($3.3$) |
| 16 | T8 | Nyquist → $K_P$ (RHP-pol) | **a** ($K_P=45$) |
| 17 | T10 | PI-Lead: $\omega_c/\omega_i$ | **c** ($1.57$) |
| 18 | T10 | Pre-filter tidskonstant | **c** ($\tau_f=4.46$) |
| 19 | T4 | Disturbance-sensitivitet | **d** ($e_0=-0.167$, $K_P=2$) |
| 20 | T10 | Feed-forward Bode-match | **a** |

---

## Q1 — Linearisér motormodel *(T1)*

**Hvad spørges om:** Linearisér $J\dot{\omega}=\frac{k}{R}(v-k\omega-1.2)-B\sqrt{\omega}$ om $\omega_0$. Find $\omega(s)/v(s)$.

**Metode:** Konstantled ($1.2$) forsvinder i $\Delta$-ligningen. Linearisér $B\sqrt\omega$: $\frac{d}{d\omega}(B\sqrt\omega)=\frac{0.5B}{\sqrt{\omega_0}}$.

> [!formula] Resultat
> $$\frac{\omega(s)}{v(s)}=\frac{k}{R\left(Js+\frac{k^2}{R}+\frac{0.5B}{\sqrt{\omega_0}}\right)}$$

**Svar:** $\boxed{\text{Mulighed 1}}$ — mulighed 2 har $0.5B\sqrt{\omega_0}$ (forkert afledt), mulighed 3 mangler $\sqrt{\omega_0}$ i nævner.

→ Metode: [[Transfer-functions-og-poler]] · Teori: [[Lec 5 — Black-box Modelling og Linearisering]]

## Q2 — Steady-state bilhastighed *(T4)*

**Hvad spørges om:** $m\dot v=F_p u-0.5\rho A C_d v^2$. $m=500$, $C_d=0.24$, $\rho=1.225$, $A=5$, $F_p=30$, $u_{ss}=40\%$. Find $v_{ss}$.

> [!formula] Sæt $\dot v=0$
> $$v_{ss}=\sqrt{\frac{2F_p u_{ss}}{\rho A C_d}}=\sqrt{\frac{2\cdot30\cdot40}{1.225\cdot5\cdot0.24}}=40.4\text{ m/s}$$

```matlab hl:N
vss = sqrt(2*30*40/(1.225*5*0.24));
fprintf('vss = %.4g m/s\n', vss);
```

**Svar:** $\boxed{40.4\text{ m/s} \Rightarrow \text{Mulighed 1}}$ — $20.2$ glemmer faktor 2; $80.8$ er $2\times$.

→ Metode: [[Steady-state-error-og-disturbance]]

## Q3 — Poler/nuller fra Bode *(T7)*

**Hvad spørges om:** Magnitude $14$ dB → $0$ dB, fase dykker til $-50°$ og vender til $0°$. Find pol/nul-struktur.

**Metode:** Magnitude flad i begge ender (relativ grad 0) + fase tilbage til $0°$ → lige antal poler og nuller. Komplekse nuller + to reelle poler.

> [!formula] System
> $$G(s)=\frac{s^2+3s+5}{(s+1)^2} \quad(\text{nuller }-1.5\pm1.66i,\ \text{dobbelt pol }-1)$$

```matlab hl:/roots\(/
disp(roots([1 3 5]).')   % -1.5 +/- 1.66i  (komplekse, negativ realdel)
```

**Svar:** $\boxed{\text{Komplekse negative nuller + 2 reelle poler} \Rightarrow \text{Mulighed 1}}$

→ Metode: [[Bode-aflæsning]] · [[Transfer-functions-og-poler]]

## Q4 — Steady-state error, sammensat input *(T4)*

**Hvad spørges om:** $r(t)=5+2t+\frac{t^2}{2}$, $G(s)=\frac{5(s+4)}{s^2(s+1)(s+20)}$ (Type-2). Find $e_{ss}$.

**Metode:** Superposition pr. inputkomponent. Type-2-system ($s^2$ i nævner) → nul fejl på step og ramp, endelig fejl på parabel.

> [!formula] Pr. komponent
> | Input | $e_{ss}$ |
> |---|---|
> | step $5$ | $0$ |
> | ramp $2t$ | $0$ |
> | parabel $t^2/2$ | $1/K_a=1$ |
>
> $K_a=\lim_{s\to0}s^2 G(s)=\frac{5\cdot4}{1\cdot20}=1$, så parabel-fejl $=1$.

**Svar:** $\boxed{e_{ss}=1 \Rightarrow \text{Mulighed 1}}$

→ Metode: [[Steady-state-error-og-disturbance]]

## Q5 — Bode → TF med RHP-pol *(T7)*

**Hvad spørges om:** Magnitude $60\to40$ dB, fase stiger fra $-180°$ mod $0°$. Hvilket udsagn?

**Metode:** Fase ved $-180°$ ved lav frekvens ⟹ **positiv (RHP) pol**. Nul løfter fasen tilbage. DC $=60$ dB $=1000$.

> [!formula] System
> $$G(s)=\frac{100(s+10)}{s-1},\quad G(0)=\frac{1000}{-1}=-1000,\ |G(0)|=60\text{ dB}$$

```matlab hl:/dcgain\(/
s=tf('s'); G=100*(s+10)/(s-1);
fprintf('|DC| = %.4g dB\n', 20*log10(abs(dcgain(G))));   % 60 dB
```

**Svar:** $\boxed{\text{1 positiv reel pol + 1 negativt reelt nul} \Rightarrow \text{Mulighed 4}}$

→ Metode: [[Bode-aflæsning]]

## Q6 — State space → TF *(T11)*

**Hvad spørges om:** $\dot x_1=-x_1+u$, $\dot x_2=-x_2+9u$, $y=x_1+x_2$. Find $G(s)$.

> [!formula] Laplace pr. tilstand
> $$X_1=\frac{1}{s+1}U,\ X_2=\frac{9}{s+1}U \Rightarrow Y=\frac{10}{s+1}U$$

```matlab hl:/minreal\(/
G = minreal(tf(ss([-1 0;0 -1],[1;9],[1 1],0)));
zpk(G)    % 10/(s+1)
```

**Svar:** $\boxed{G(s)=\dfrac{10}{s+1} \Rightarrow \text{Mulighed 5}}$

→ Metode: [[Transfer-functions-og-poler]]

## Q7 — Inverse Laplace *(T3)*

**Hvad spørges om:** $G(s)=\frac{5}{s+1}$, input $u(t)=2e^{-3t}$. Find $y(t)$.

> [!formula] Partial fractions
> $$Y=\frac{5}{s+1}\cdot\frac{2}{s+3}=\frac{10}{(s+1)(s+3)}=\frac{5}{s+1}-\frac{5}{s+3} \Rightarrow y(t)=5e^{-t}-5e^{-3t}$$

```matlab hl:/residue\(/
[r,p] = residue(10,[1 4 3]);
disp([r p])    % [5, -1; -5, -3]
```

**Svar:** $\boxed{y(t)=5e^{-t}-5e^{-3t} \Rightarrow \text{Mulighed 1}}$ — pol-tidskonstanten er $-1$ (fra $G$), ikke $-0.5$.

→ Metode: [[Time-response-2nd-order]]

## Q8 — Step + slutværdi *(T3)*

**Hvad spørges om:** $Y(s)=\frac{4(s+50)}{s^2+30s+200}R(s)$, unit step. Find $y(t)$ og $y_{ss}$.

> [!formula] Faktorisér + FVT
> $$s^2+30s+200=(s+10)(s+20),\quad y_{ss}=\lim_{s\to0}sY(s)=\frac{4\cdot50}{200}=1$$
> $$y(t)=1+0.6e^{-20t}-1.6e^{-10t}$$

**Svar:** $\boxed{y_{ss}=1 \Rightarrow \text{Mulighed 1}}$

→ Metode: [[Steady-state-error-og-disturbance]] · [[Time-response-2nd-order]]

## Q9 — Blokdiagram, multi-loop *(T2)*

**Hvad spørges om:** Find $T(s)=Y/R$ for diagram med forward $K G_1 G_2\frac{1}{s}$ og tre feedback-loops ($H_3$, $H_1$, unity).

> [!formula] Resultat
> $$T(s)=\frac{KG_1G_2\frac{1}{s}}{1+G_1G_2H_1+G_1H_3+KG_1G_2\frac{1}{s}}$$

**Svar:** $\boxed{\text{Mulighed 1}}$ — de øvrige har $K$ forkert placeret i nævneren (mulighed 3 mangler $K$ i tæller).

→ Metode: [[Blokdiagram-reduktion]]

## Q10 — Procent overshoot *(T3)*

> [!warning] OCR-rettelse
> Facit trykker nævneren som $s^2+2\sqrt{2K}s+K$ — men det giver ikke $\zeta=0.707$. Korrekt (fra $L(s)$) er $\boxed{s^2+\sqrt{2K}\,s+K}$.

**Hvad spørges om:** Unity feedback, $L(s)=\frac{K}{s(s+\sqrt{2K})}$. Find procent overshoot.

> [!formula] Lukket sløjfe → $\zeta$
> $$T(s)=\frac{K}{s^2+\sqrt{2K}s+K},\quad \omega_n=\sqrt K,\ \zeta=\frac{\sqrt{2K}}{2\sqrt K}=\frac{\sqrt2}{2}=0.707$$
> $$M_p=100\,e^{-\pi\zeta/\sqrt{1-\zeta^2}}=4.3\%$$

```matlab hl:N
zeta=sqrt(2)/2;
fprintf('Mp = %.3g %%\n', 100*exp(-pi*zeta/sqrt(1-zeta^2)));
```

**Svar:** $\boxed{M_p=4.3\% \Rightarrow \text{Mulighed 1}}$ — bemærk $\zeta=0.707$ er uafhængig af $K$.

→ Metode: [[Time-response-2nd-order]]

## Q11 — DC-gain af kaskade *(T4)*

**Hvad spørges om:** Unity feedback, forward $=\frac{4}{s+1}\cdot\frac{2}{s+2}\cdots\frac{N}{s+N}$ (blok $i$: $\frac{i}{s+i}$, første tæller $4$). Find $G_{cl}(0)$.

> [!formula] Open-loop DC → closed-loop DC
> $$G_{ol}(0)=4\prod_{i=1}^N\frac{i}{i}=4,\qquad G_{cl}(0)=\frac{4}{1+4}=0.8$$

**Svar:** $\boxed{G_{cl}(0)=0.8 \Rightarrow \text{b}}$ — $0.2$ er error-TF'ens DC ($\frac{1}{1+4}$); $0.5$ glemmer faktor 4.

→ Metode: [[Steady-state-error-og-disturbance]]

## Q12 — Nyquist-stabilitet (RHP-pol) *(T8)*

**Hvad spørges om:** $G$ med 1 RHP-pol; Nyquist omkredser $(-1,0)$ én gang CCW. Stabil?

> [!formula] Nyquist-kriteriet
> $$Z=P-N=1-1=0 \Rightarrow \text{closed-loop stabil}$$

**Svar:** $\boxed{\text{Stabil} \Rightarrow \text{d}}$ — netop fordi CCW-omkredsningen modregner den ustabile open-loop pol.

→ Metode: [[Stabilitet-Nyquist-margins]]

## Q13 — Konceptuelt *(PM/bandbredde)*

**Svar:** $\boxed{\text{e}}$ — højere phase margin ⟹ færre oscillationer + mere robusthed.

> [!note] Forkerte
> Lavere bandbredde = **langsommere** respons (ikke hurtigere); at flytte Lead mellem grene ændrer ikke input-disturbance-respons.

→ Metode: [[Controller-design-P-PI-Lead]]

## Q14 — Gain margin → P-grænse *(T7/T9)*

**Hvad spørges om:** $G(s)=\frac{25}{s^3+s^2+10s}$. Ved $\omega_{180}=3.16$ er $|G|=7.96$ dB. For hvilket $K_P$ er closed-loop stabil?

> [!formula] Stabilitetsgrænse
> $$|G(j\omega_{180})|=10^{7.96/20}=2.5 \Rightarrow K_P<\frac{1}{2.5}=0.4$$

```matlab hl:/margin\(/
s=tf('s'); G=25/(s^3+s^2+10*s);
[GM,~,wcg]=margin(G);
fprintf('GM=%.4g (=%.4g dB) ved w=%.4g -> Kp_max=%.4g\n',GM,20*log10(GM),wcg,GM);
```

**Svar:** $\boxed{K_P=0.25 \Rightarrow \text{e}}$ (eneste positive $<0.4$).

> [!warning] Fortegns-fælde
> $|G|$ er **over** $0$ dB ved $\omega_{180}$, så gain margin er negativ i dB ($-7.96$ dB) = faktor $0.4$. Distractor $b$ ($7.96$) aflæser bare dB-tallet.

→ Metode: [[Stabilitet-Nyquist-margins]] · Snydeark: [[MATLAB-snydeark]]

## Q15 — Lead-bidrag $M_D$ *(T10)*

**Hvad spørges om:** $G(s)=\frac{s+7}{s^3+10s^2+29s+20}$. Ved $\omega=15$: $\angle G=-167.84°$. PI-Lead med $\gamma_M=50°$, $\omega_c=15$, $N_i=3$. Find $M_D$.

> [!formula] Fasebudget → $\alpha$ → $M_D$
> $$\phi_d=-180°+\gamma_M-\phi_G+\arctan\tfrac1{N_i}=-180+50+167.84+18.43=56.28°$$
> $$\alpha=\frac{1-\sin\phi_d}{1+\sin\phi_d}=0.092,\qquad M_D=\frac{1}{\sqrt\alpha}=3.3$$

```matlab hl:N
phiG=-167.842; phid=-180+50-phiG+atand(1/3);
alpha=(1-sind(phid))/(1+sind(phid));
fprintf('phid=%.4g, alpha=%.4g, MD=%.4g\n', phid, alpha, 1/sqrt(alpha));
```

**Svar:** $\boxed{M_D=3.3 \Rightarrow \text{a}}$ — $0.22$ er $\tau_d$; $10.57$ blander grader/radianer.

→ Metode: [[Controller-design-P-PI-Lead]]

## Q16 — Nyquist → $K_P$ (RHP-pol) *(T8)*

**Hvad spørges om:** Ustabilt system (1 RHP-pol), Nyquist krydser ved $(-0.0247,0)$. Find stabiliserende $K_P$.

> [!formula] Marginal gain
> $$K_{marg}=\frac{1}{0.0247}=40.5 \Rightarrow K_P>40.5$$

**Svar:** $\boxed{K_P=45 \Rightarrow \text{a}}$ (eneste $>40.5$).

→ Metode: [[Stabilitet-Nyquist-margins]]

## Q17 — PI-Lead: $\omega_c/\omega_i$ *(T10)*

**Hvad spørges om:** $G(s)=\frac{5s+60}{s^3+26s^2+173s+340}$. Ved $\omega=25$: $\angle G=-151.06°$. $\gamma_M=75°$, $\alpha=0.01$. Find $N_i=\omega_c/\omega_i$.

> [!formula] Fasebudget → $N_i$
> $$\arctan\tfrac1{N_i}=180°-\gamma_M+\phi_G+\arcsin\tfrac{1-\alpha}{1+\alpha}=180-75-151.06+78.58=32.5°$$
> $$N_i=\frac{1}{\tan 32.5°}=1.57$$

```matlab hl:N
phiG=-151.064; alpha=0.01;
phid=asind((1-alpha)/(1+alpha));
ang=180-75+phiG+phid;
fprintf('Ni = wc/wi = %.4g\n', 1/tand(ang));
```

**Svar:** $\boxed{\omega_c/\omega_i=1.57 \Rightarrow \text{c}}$ — $0.51$ blander grader/radianer; $3$ er den typiske (men forkerte) standardværdi.

→ Metode: [[Controller-design-P-PI-Lead]]

## Q18 — Pre-filter tidskonstant *(T10)*

**Hvad spørges om:** Magnitude-top ved $\omega_p=0.77$ med $|G|=11.08$ dB. Pre-filter $G_f=\frac{1}{\tau_f s+1}$ skal bringe toppen til $0$ dB. Find $\tau_f$.

> [!formula] Kræv $|G_f(j\omega_p)|\cdot M_p=1$
> $$M_p=10^{11.08/20}=3.58,\quad \tau_f=\frac{\sqrt{M_p^2-1}}{\omega_p}=4.46\text{ s}$$

```matlab hl:N
wp=0.770715; Mp=10^(11.0827/20);
fprintf('tauf = %.4g s\n', sqrt(Mp^2-1)/wp);
```

**Svar:** $\boxed{\tau_f=4.46\text{ s} \Rightarrow \text{c}}$ — $2.1$ glemmer at kvadrere $M_p$.

→ Metode: [[Steady-state-error-og-disturbance]] · Teori: [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]]

## Q19 — Disturbance-sensitivitet *(T4)*

**Hvad spørges om:** Disturbance $d$ før $G$. Bode-DC: $|G_{yr}(0)|=-3.52$ dB, $|G_{yd}(0)|=-15.56$ dB. Find $e(0)$ og $K_P$.

> [!formula] Løs baglæns
> $$G_{yr}(0)=0.667=\frac{K_P G(0)}{1+K_P G(0)},\ G(0)=1 \Rightarrow K_P=2$$
> $$G_{yd}(0)=0.167=\frac{D(0)G(0)}{1+K_P G(0)} \Rightarrow D(0)=0.5,\quad e(0)=-\frac{D(0)G(0)}{1+K_P G(0)}=-0.167$$

```matlab hl:N
Gyr0=10^(-3.52183/20); Gyd0=10^(-15.563/20);
Kp=Gyr0/(1-Gyr0); D0=Gyd0*(1+Kp); e0=-D0/(1+Kp);
fprintf('Kp=%.4g, e0=%.4g\n', Kp, e0);
```

**Svar:** $\boxed{e(0)=-0.167,\ K_P=2 \Rightarrow \text{d}}$

→ Metode: [[Steady-state-error-og-disturbance]]

## Q20 — Feed-forward Bode-match *(T10)*

> [!warning] OCR-rettelse
> Facit trykker $F(s)$-tæller som $s^2+4s+21$ — bør være $s^2+4s+25$ (= $G$'s nævner).

**Hvad spørges om:** $K_P=2$, $G(s)=\frac{2s+4}{s^2+4s+25}$, filter $G_{filt}=\frac{1}{0.08s+1}$. Vælg Bode for $G_{yr}$ og $G_{er}$.

**Metode:** Dynamisk feed-forward $F=\frac{G_{filt}}{G}$ giver $|G_{yr}|\approx1$ (0 dB) og $|G_{er}|\approx0$ (stor negativ dB) op til filterets cutoff $\omega_f=1/0.08=125$ rad/s.

**Svar:** $\boxed{\text{Mulighed a (Fig. 14)}}$

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 13 — Feed-forward Control]]

---

## Nøgletermer

| Term | Formel |
|---|---|
| Steady-state (kvadratisk drag) | $v_{ss}=\sqrt{2F_p u/(\rho A C_d)}$ |
| Acceleration error const. | $K_a=\lim_{s\to0}s^2 G(s)$ |
| Kaskade closed-loop DC | $G_{cl}(0)=\frac{G_{ol}(0)}{1+G_{ol}(0)}$ |
| Lead-bidrag | $M_D=1/\sqrt\alpha$ |
| Pre-filter til $0$ dB | $\tau_f=\sqrt{M_p^2-1}/\omega_p$ |

→ Metoder: [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] | Snydeark: [[MATLAB-snydeark]] | Oversigt: [[00_Eksamensanalyse_og_strategi]]
