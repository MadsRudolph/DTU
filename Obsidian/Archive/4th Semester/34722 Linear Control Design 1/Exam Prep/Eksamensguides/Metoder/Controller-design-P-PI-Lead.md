---
tags: [LCD, regulering, eksamen, metode, controller-design]
type: opskrift
dækker: [T9, T10]
---

# Opskrift: Controller-design (P / PI / Lead / PI-Lead)

> [!info] Hvornår bruges denne?
> Genkend i multiple-choice på formuleringer som:
> - *"Find $K$ så phase margin er …"* → **P-controller** (afsnit 1)
> - *"… max overshoot på 10%"* → konvertér spec til PM/$\zeta$ (afsnit 2)
> - *"Find $\alpha$ / $\tau_d$ for Lead-delen"* → **Lead** (afsnit 3)
> - *"Find $K_P$ i en PI-Lead"* → **fuldt PI-Lead** (afsnit 5)
>
> Dette er **design-delen** og kommer i hvert sæt. Alle skabeloner er kørt og verificeret i MATLAB R2025b.

---

## Controller-oversigt: hvad gør hver type

Brug denne til at **genkende** en controller fra dens effekt (fx [[E25]] Q5: *"hvilken controllertype er brugt?"*).

| Controller | Form | Fase / Bode-effekt | Type / $e_{ss}$ | Båndbredde / hastighed | Pris |
|---|---|---|---|---|---|
| **P** | $K_P$ | løfter hele magnituden; **ingen** faseændring | uændret type; større $K_0$ → mindre $e_{ss}$ | større $K_P$ → højere $\omega_c$ | mere gain → mindre PM & GM |
| **I** | $\tfrac{1}{T_i s}$ | $-90°$ fase, $-20$ dB/dek | **+1 type** (fjerner én fejl-orden) | langsom | $-90°$ → ustabil alene |
| **PI** | $K_P\tfrac{\tau_i s+1}{\tau_i s}$ | $-90°\to0°$; løft ved lav $\omega$ | **+1 type** → nul step-fejl | lille fasetab ved $\omega_c$ | koster fase nær crossover |
| **PD** | $K_P(\tau_d s+1)$ | **+fase** (op til $+90°$); $+20$ dB/dek | uændret type | hurtigere, mere robust | forstærker højfrekvent **støj** |
| **PID** | PI $\cdot$ PD | integrator (lav $\omega$) + fase-løft (høj $\omega$) | +1 type **og** fase-løft | hurtig + nul fejl | støj + mere tuning |
| **Lead** | $\tfrac{\tau_d s+1}{\alpha\tau_d s+1},\ \alpha<1$ | **+fase** $\phi_m=\arcsin\tfrac{1-\alpha}{1+\alpha}$ ved $\omega_m$ | uændret type | øger $\omega_c$ → **større båndbredde** | mindre støj end ren PD |
| **Lag** | $\tfrac{\tau s+1}{\beta\tau s+1},\ \beta>1$ | **−fase** (lille); hæver lav-frekv. gain *relativt* (dæmper høj-frekv.) | uændret type; tillader større $K_0$ → mindre $e_{ss}$ | sænker $\omega_c$ lidt | langsommere |
| **PI-Lead** | PI $\cdot$ Lead | integrator (lav $\omega$) + fase-løft (ved $\omega_c$) | +1 type **og** bedre PM | hurtig + nul fejl | mest komplekst |

> [!tip] Genkend fra Bode (Q5-typen)
> 1. **Integrator (I/PI)?** Kig på **lav-frekvens-fasen**: trækkes den mod $-90°$, er der et I-led. Bliver den på $0°$ → **ingen** integrator (altså P/PD/Lead).
> 2. **Fase-løft nær crossover** (mindre negativ fase, $\omega_c$ skubbet op) → **Lead** (eller PD).
> 3. Ingen integrator **+** fase-løft $=$ **P-Lead** (præcis [[E25]] Q5).

> [!note] Eksamens-fokus
> Kurset designer primært **P, PI, Lead, PI-Lead** (afsnit 1–5 nedenfor). PD/PID/Lag er med for sammenligning — sjældne som design-opgaver, men forståelsen hjælper til genkendelse.

---

## 0. Kernen: fasebudgettet ved crossover

Alt frekvens-design hviler på én ligning, evalueret ved crossover-frekvensen $\omega_c$ (hvor $|G_{ol}(j\omega_c)|=1$):

> [!formula] Fasebudget
> $$\underbrace{-180°+\gamma_M}_{\text{ønsket fase}} \;=\; \phi_G+\phi_{\text{Lead}}+\phi_{PI}+\dots$$
> $\gamma_M=\text{PM}$ er ønsket phase margin. $\phi_G$ er anlæggets fase ved $\omega_c$ (aflæses på Bode).

To trin går igen:
1. **Fase** bestemmer controller-parametre ($\alpha$, $\tau_d$, $\tau_i$) og evt. $\omega_c$.
2. **Magnitude** (0-dB-betingelsen $|K_P\,C\,G|=1$) bestemmer til sidst $K_P$.

---

## 1. P-controller til ønsket phase margin

**Metode:**
1. $K_P$ ændrer ikke fasen → find $\omega_c$ hvor $\angle G(j\omega_c)=-180°+\gamma_M$.
2. Sæt $K_P=1/|G(j\omega_c)|$ så magnitude bliver $0$ dB der.

```matlab hl:/bode\(|margin\(/
% --- P-controller til ønsket PM ---  (UDFYLD G og PMdes)
s   = tf('s');
G   = 1/(s*(s+2.1));        % ← anlæg
PMdes = 40;                 % ← ønsket phase margin [grader]

w = logspace(-3,4,2e5);
[mag,ph] = bode(G,w); mag = squeeze(mag); ph = squeeze(ph);
idx = find(ph <= -180+PMdes, 1, 'first');
Kp  = 1/mag(idx);
[~,PMcheck] = margin(Kp*G);
fprintf('wc = %.4g rad/s | Kp = %.4g (%.4g dB) | PM = %.4g grader\n',...
        w(idx), Kp, 20*log10(Kp), PMcheck);
```

> [!example] Bruges i
> [[F22]] Q6 ($K_P\approx8.4$) · samme mønster i [[S20]], [[Final-Test]].

---

## 2. Performance-specs → PM / $\zeta$ / $\omega_c$

Mange opgaver giver en **tidsdomæne-spec** (overshoot, settling time, bandbredde) som først skal omsættes til frekvens-krav. Brug kursets færdige funktioner (ligger i `OLD EXAMS/Matlab scripts/` — læg mappen på MATLAB-path med `addpath`).

| Har             | Vil have   | Funktion / formel                        |
| --------------- | ---------- | ---------------------------------------- |
| Overshoot $M_p$ | $\zeta$    | `overshoot2damping(Mp)`                  |
| $\zeta$         | $M_p$      | `damping2overshoot(zeta)`                |
| Overshoot $M_p$ | PM         | `overshoot2phase_margin(Mp)`             |
| $\zeta$         | PM         | `damp2phase_margin(zeta)`                |
| Bandbredde      | $\omega_c$ | `bandwidth2crossover_frequency(wb,zeta)` |
| $\omega_c$      | Bandbredde | `crossover_frequency2bandwidth(wc,zeta)` |

> [!formula] De underliggende sammenhænge
> $$M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}},\qquad \zeta\approx\frac{\text{PM}°}{100}\;(\text{tommelfinger}),\qquad t_s\approx\frac{4}{\zeta\omega_n}$$

```matlab hl:N
Mp   = 0.10;                                            % ← 10% overshoot
zeta = -log(Mp)/sqrt(pi^2+log(Mp)^2);                  % = overshoot2damping(Mp)
PM   = atand(2*zeta/sqrt(-2*zeta^2+sqrt(1+4*zeta^4))); % = overshoot2phase_margin(Mp)
fprintf('Mp=%.2f -> zeta=%.3g -> PM=%.3g grader\n', Mp, zeta, PM);
```
> [!note] Færdige funktioner
> Samme resultat fås med kursets funktioner i `OLD EXAMS/Matlab scripts/` (tabellen ovenfor). De kræver dog at mappen er på MATLAB-path; inline-formlerne her virker altid. Se [[MATLAB-snydeark]] §7.

---

## 3. Lead-design

En Lead $C_D(s)=\dfrac{\tau_d s+1}{\alpha\tau_d s+1}$ ($0<\alpha<1$) tilfører **positiv fase** med maksimum $\phi_m$ midt mellem zero og pol.

> [!formula] Lead-formler
> $$\sin\phi_m=\frac{1-\alpha}{1+\alpha}\;\Rightarrow\;\alpha=\frac{1-\sin\phi_m}{1+\sin\phi_m},\qquad \omega_m=\frac{1}{\tau_d\sqrt{\alpha}}=\omega_c,\qquad |C_D(j\omega_c)|=\frac{1}{\sqrt{\alpha}}$$

**Metode:** Find nødvendigt $\phi_m$ fra fasebudgettet → $\alpha$ → placér $\omega_m=\omega_c$ → $\tau_d=1/(\omega_c\sqrt\alpha)$.

```matlab hl:N
% --- Lead-design ---  (UDFYLD phi_m og wc)
s = tf('s');
phi_m = 19.08;             % ← nødvendig ekstra fase ved wc [grader]
wc    = 6.4;               % ← crossover-frekvens [rad/s]
alpha = (1-sind(phi_m))/(1+sind(phi_m));
taud  = 1/(wc*sqrt(alpha));
CD    = (taud*s+1)/(alpha*taud*s+1);
fprintf('alpha = %.4g | taud = %.4g | |CD(jwc)| = %.4g dB\n',...
        alpha, taud, 20*log10(1/sqrt(alpha)));
```

> [!example] Bruges i
> [[F22]] Q13 ($M_D=11$ dB), Q17 ($\alpha=0.5$).

---

## 4. PI-del

En PI $C_{PI}(s)=\dfrac{\tau_i s+1}{\tau_i s}$ giver **uendelig DC-gain** (fjerner stationær fejl) men koster fase. Zero placeres typisk en faktor $N_i$ under $\omega_c$.

> [!formula] PI-parametre
> $$N_i=\omega_c\tau_i\;\Rightarrow\;\tau_i=\frac{N_i}{\omega_c},\qquad \phi_{PI}=-\arctan\!\frac{1}{N_i}\;(\text{negativt fasebidrag})$$

Vælg $N_i$ stort nok (typisk 3–5) til at fasetabet ved $\omega_c$ er lille.

---

## 5. Fuldt PI-Lead-design

Kombinér: $C(s)=K_P\cdot\dfrac{\tau_i s+1}{\tau_i s}\cdot\dfrac{\tau_d s+1}{\alpha\tau_d s+1}$.

Der er **to varianter** afhængigt af hvad opgaven giver:

**Variant A — $\alpha$ er givet, find $K_P$** (fx [[F22]] Q19; det er denne koden nedenfor løser):
1. $\phi_i=\arctan(-1/N_i)$, $\phi_m=\arcsin\frac{1-\alpha}{1+\alpha}$ (begge følger af de givne $N_i,\alpha$).
2. Nødvendig anlægsfase ved crossover: $\phi_G=-180°+\gamma_M-\phi_m-\phi_i$.
3. Find $\omega_c$ hvor $\angle G(j\omega_c)=\phi_G$ (på Bode).
4. $\tau_i=N_i/\omega_c$, $\tau_d=1/(\omega_c\sqrt\alpha)$.
5. $K_P=1/|G\,C_{PI}\,C_D|$ ved $j\omega_c$ (0-dB-betingelsen).

**Variant B — $\omega_c$ er givet, find $\alpha$** (fx [[F22]] Q17): aflæs $\phi_G$ ved $\omega_c$, beregn nødvendigt $\phi_m=-180°+\gamma_M-\phi_G-\phi_i$, og find så $\alpha=\frac{1-\sin\phi_m}{1+\sin\phi_m}$ (afsnit 3).

```matlab hl:/bode\(|evalfr\(/
% --- Fuldt PI-Lead ---  (UDFYLD G, gM, Ni, alpha)
s  = tf('s');
G  = 900/((0.25*s+1)*(s^2+50*s+3000));   % ← anlæg
gM = 75;  Ni = 3;  alpha = 0.01;          % ← specs

phi_i = atand(-1/Ni);
phi_m = asind((1-alpha)/(1+alpha));
phiG  = -180 + gM - phi_m - phi_i;        % nødvendig anlægsfase ved wc
w = logspace(-2,4,4e5); [~,ph]=bode(G,w); ph=squeeze(ph);
wc = w(find(ph <= phiG, 1, 'first'));
taui = Ni/wc;  taud = 1/(wc*sqrt(alpha));
CPI  = (taui*s+1)/(taui*s);
CD   = (taud*s+1)/(alpha*taud*s+1);
Kp   = 1/abs(evalfr(G*CPI*CD, 1j*wc));
[~,PM] = margin(Kp*G*CPI*CD);
fprintf('wc=%.4g | taui=%.4g | taud=%.4g | Kp=%.5g | PM=%.4g grader\n',...
        wc, taui, taud, Kp, PM);
```

> [!example] Bruges i
> [[F22]] Q19 ($K_P=3.4154$, $\text{PM}=75°$).

---

## Faldgruber i multiple-choice

| Forkert svar repræsenterer      | Husk                                         |
| ------------------------------- | -------------------------------------------- |
| $K_P$ i dB i stedet for lineært | $K_P=10^{(\text{dB})/20}$                    |
| Glemt at kvadrere ved $\alpha$  | $\alpha=(1/(\omega_c\tau_d))^2$              |
| Reciprokt $K_P$ ($1/K_P$)       | $K_P=1/G C$, **ikke** $GC$                   |
| Fase ikke omsat til grader/rad  | tjek `sin`/`sind` konsistens                 |
| Større $\alpha$ "forbedrer" PM  | nej — større $\alpha$ **forringer** $\phi_m$ |

---

## Relateret

- Teori: [[Lec 7 - Crossover Freq & Nyquist]] · [[Lec 8 — PI-Lead Controller Design]] · [[Lec 9 — PI-Lead Design med Specifikationer]]
- Naboopskrifter: [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] · [[Time-response-2nd-order]]
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
