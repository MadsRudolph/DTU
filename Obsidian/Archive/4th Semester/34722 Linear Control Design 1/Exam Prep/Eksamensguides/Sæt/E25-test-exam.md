---
tags: [LCD, regulering, eksamen, E25, 34721, test-exam, loesningsguide]
kilde: "34721-E25-test-exam.pdf + 34721-E25-test-exam-answers.pdf"
eksamen: E25 Test-exam (19. nov 2025)
format: Multiple choice øve-eksamen (20 spørgsmål)
---

# E25 Test-exam (øve-eksamen) — Komplet løsningsguide

> [!info] Om dette sæt
> Dette er en **øve-eksamen** ("test exam") i **34721 Linear Control Design 1**, dateret **19. nov 2025** — den blev udleveret til træning og er **ikke** den rigtige decembereksamen (se det rigtige sæt: [[E25]]). Scoringen er "One best answer": præcis ét svar er mere rigtigt end de andre, 1 point pr. korrekt svar, ingen minuspoint. Spørgsmålene er **ikke nummereret** i printet — de er her nummereret **Q1–Q20** i den rækkefølge de står, grupperet i klynger om fælles blokdiagrammer/Bode-plots.
>
> ⚠️ **Om facit-numrene:** Facit-PDF'en bærer den samme stale **"11. august 2020"-footer** som søstersættet [[E23]] — hvor facit-numrene viste sig **upålidelige** (14 af 20 forkerte), fordi facit listede svarmulighederne i en anden rækkefølge end opgave-PDF'en. Derfor er **alle 20 svar her content-matchet** mod opgave-PDF'ens faktiske svarmuligheder + figurer (uafhængigt udregnet/aflæst), ikke kopieret fra facit-nummeret. **Gode nyheder for netop dette sæt:** efter content-matchingen viste det sig at **alle 20 facit-numre faktisk er korrekte** (de stemmer med opgave-PDF'ens rækkefølge) — men numrene er stadig verificeret ved indhold, så følg ALTID svarets **indhold**, ikke nummeret.
>
> **Figurklynger:** **Q1–Q4** deler ét blokdiagram, **Q5–Q11** deler ét open-loop Bode-plot, **Q12–Q14** deler én step-respons-figur, **Q15–Q16** deler én sinus-figur (input/output). **Q17–Q20** er enkeltstående.

## Hurtig oversigt

| # | Type | Emne | Svar |
|---|---|---|---|
| Q1 | T2/T4 | Loop-gain $K_0$ fra blokdiagram | $K_0=0.1K$ ⇒ Mul. 1 |
| Q2 | T1/T2 | Type af systemet | Type 1 ⇒ Mul. 5 |
| Q3 | T4 | Stationær fejl, step på $r$ | $e_{r,ss}=0$ ⇒ Mul. 2 |
| Q4 | T4 | Find $K$ fra $y_{ss,d}=2.86$ | $K=7$ ⇒ Mul. 1 |
| Q5 | T7 | Type & orden fra Bode | Type 1, orden 4 ⇒ Mul. 4 |
| Q6 | T8 | Phase margin & gain margin | begge **negative** ⇒ Mul. 4 |
| Q7 | T7/T8 | $\omega_c$ & $\omega_\pi$ | $\omega_c{=}5.2,\ \omega_\pi{=}3.9$ ⇒ Mul. 2 |
| Q8 | T7 | Bandbredde $\omega_b$ | kan ikke læses på open-loop ⇒ Mul. 3 |
| Q9 | T9 | P-gain $K_p$ for PM$=60°$ | $K_p=0.2$ ⇒ Mul. 3 |
| Q10 | T10 | Øg bandbredde uden tab af PM | Lead-led tilføjes ⇒ Mul. 5 |
| Q11 | T10 | Stor bandbredde + $e_{ss}=0$ | Lead-controller ⇒ Mul. 1 |
| Q12 | T3 | Statisk gain $K_0$ for $G_1$ | $K_0=8$ ⇒ Mul. 5 |
| Q13 | T3 | $\omega_n$ & $\zeta$ for $G_2$ | $\omega_n{=}0.25,\ \zeta{=}0.1$ ⇒ Mul. 3 |
| Q14 | T3 | $\tau$ for $G_1$ | $\tau=11$ ⇒ Mul. 2 |
| Q15 | T7 | Faseskift $\phi(\omega_0)$ fra sinus | $\approx-116°$ ⇒ Mul. 4 |
| Q16 | T9 | P-gain $K$ så $\omega_0$ bliver crossover | $K\approx1.85$ ⇒ Mul. 3 |
| Q17 | T1/T2 | Closed-loop TF (unit feedback) | $\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$ ⇒ Mul. 4 |
| Q18 | T10 | Non-minimum phase i closed-loop | neg. fase ⇒ mindre PM ⇒ Mul. 2 |
| Q19 | T5/T11 | Orden af $G(s)$ fra 2 ODE'er | orden 4 eller lavere ⇒ Mul. 5 |
| Q20 | T3/T1 | Impuls-respons af stabil $G$ | $\mathcal{L}\{y(t)\}=G(s)$ ⇒ Mul. 5 |

*(Alle facit-numre stemte ved content-match — ingen ⚠-afvigelser i dette sæt, modsat [[E23]].)*

---

# Klynge Q1–Q4 — Figur 1 (blokdiagram, lukket sløjfe med disturbance)

> [!note] Om figuren
> Blokdiagram (Figur 1): $r(s)\to$ summationspunkt ($+r$, $-$feedback) $\to C(s)=K$ (ren gain) $\to G_1(s)=\dfrac{s+5}{s^2+2s+10}\to$ summationspunkt hvor disturbance $d(s)$ adderes ($+,+$) $\to G_2(s)=\dfrac{2}{s}\to y(s)$. Feedback-grenen fra $y$ går gennem en **gain-blok $H=0.1$** tilbage til input-summationspunktet (negativ feedback). Bemærk: $d$ kommer ind **mellem** $G_1$ og integratoren $G_2$.

## Q1 — Loop-gain $K_0$ *(T2/T4)*

**Hvad spørges om:** Bestem den statiske loop-gain $K_0$ for den lukkede sløjfe.

**Metode:** Åbn sløjfen og skriv loop-transfer-funktionen $L(s)=C\,G_1\,G_2\,H$. Loopet indeholder integratoren $G_2=\frac{2}{s}$, så systemet er **type 1** — den statiske loop-gain er da grænsen af $sL(s)$:

> [!formula] Statisk loop-gain (type 1)
> $$L(s)=K\cdot\frac{s+5}{s^2+2s+10}\cdot\frac{2}{s}\cdot 0.1$$
> $$K_0=\lim_{s\to0}sL(s)=K\cdot\frac{5}{10}\cdot 2\cdot 0.1=K\cdot 0.5\cdot 0.2=0.1K$$

```matlab hl:N
syms s K real
L = K*(s+5)/(s^2+2*s+10) * (2/s) * 0.1;
K0 = limit(s*L, s, 0)            % = K/10 = 0.1*K
```

**Svar:** $\boxed{K_0=0.1K \Rightarrow \text{Mulighed 1}}$

> [!tip] Hvorfor $\lim sL(s)$ og ikke $L(0)$?
> Fordi $L$ har en pol i origo (integrator) er $L(0)=\infty$. For type-1-systemer er den meningsfulde statiske gain $K_0=\lim_{s\to0}sL(s)$ (jf. form (11.16) hos Andersen) — den ene faktor $s$ "annullerer" integratoren.

→ Metode: [[Blokdiagram-reduktion]] · Teori: [[Lec 2 — Blokdiagrammer og Håndjustering]]

## Q2 — Type af systemet *(T1/T2)*

**Hvad spørges om:** Hvad er **typen** af systemet?

**Metode:** Typen = antal rene integratorer (poler i origo) i loop-transfer-funktionen $L(s)$.

> [!formula] Typetælling
> $$L(s)=\underbrace{K}_{\text{gain}}\cdot\underbrace{\frac{s+5}{s^2+2s+10}}_{\text{ingen pol i }0}\cdot\underbrace{\frac{2}{s}}_{1\text{ integrator}}\cdot\underbrace{0.1}_{\text{gain}}$$

Kun $G_2=\frac{2}{s}$ bidrager med en pol i origo $\Rightarrow$ **én** integrator $\Rightarrow$ **Type 1**.

**Svar:** $\boxed{\text{Type 1} \Rightarrow \text{Mulighed 5}}$

> [!note] $G_1$ giver ingen integrator
> $G_1$ har polerne fra $s^2+2s+10$ (komplekse, i venstre halvplan), **ingen** i origo. Derfor tæller den ikke med i typen — kun integratoren $1/s$ i $G_2$ gør.

→ Metode: [[Transfer-functions-og-poler]] · Teori: [[Lec 3 — Laplace Transform & Transfer Functions]]

## Q3 — Stationær fejl ved step på $r$ *(T4)*

**Hvad spørges om:** Find den stationære referencefejl $e_{r,ss}$ for et step med amplitude $3$ på $r$ (med $K=1$).

**Metode:** Fejlen er $E(s)=\frac{1}{1+L(s)}R(s)$. Brug Final Value Theorem. Da systemet er **type 1**, går $L(0)\to\infty$ for et step, så fejlen forsvinder:

> [!formula] Stationær step-fejl, type 1
> $$e_{r,ss}=\lim_{s\to0}s\cdot\frac{1}{1+L(s)}\cdot\frac{3}{s}=\frac{3}{1+\lim_{s\to0}L(s)}=\frac{3}{1+\infty}=0$$

Et type-1-system følger et step **uden** stationær fejl — uanset step-amplituden (her $3$). (Jf. tabel 11.1 hos Andersen: type 1 $\Rightarrow$ step-fejl $=0$.)

**Svar:** $\boxed{e_{r,ss}=0 \Rightarrow \text{Mulighed 2}}$

> [!tip] Pas på type-0-fælden
> For et **type-0**-system ville svaret være $e_{ss}=\frac{3}{1+K_0}$ (IKKE $3/K_0$). Men her er integratoren i loopet $\Rightarrow$ type 1 $\Rightarrow$ fejlen er præcis $0$. Distractoren $0.909$ svarer til at man fejlagtigt behandlede systemet som type 0.

→ Metode: [[Steady-state-error-og-disturbance]] · Teori: [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]]

## Q4 — Find $K$ ud fra disturbance-respons *(T4)*

**Hvad spørges om:** Den stationære outputværdi for et **unit-step på disturbance** $d$ er $y_{ss,d}=2.86$. Hvad er gainet $K$?

**Metode:** Find transferfunktionen fra $d$ til $y$. Da $d$ kommer ind efter $G_1$, lige før $G_2$, er fremadvejen fra $d$ kun $G_2$, og hele loopet $L=C G_1 G_2 H$ optræder i nævneren:

> [!formula] Disturbance-til-output + Final Value
> $$\frac{Y(s)}{D(s)}=\frac{G_2}{1+L(s)}=\frac{2/s}{1+0.1K\frac{2(s+5)}{s(s^2+2s+10)}}$$
> $$y_{ss,d}=\lim_{s\to0}s\cdot\frac{Y}{D}\cdot\frac{1}{s}=\frac{2/s\cdot s}{\;\dots\;}\Big|_{s\to0}=\frac{20}{K}$$

Sæt lig den aflæste værdi:

$$\frac{20}{K}=2.86 \;\Rightarrow\; K=\frac{20}{2.86}\approx 6.99\approx 7$$

```matlab hl:/dcgain\(/
syms s K real
G1=(s+5)/(s^2+2*s+10); G2=2/s; H=0.1; C=K;
L = C*G1*G2*H;
Tdy = G2/(1+L);                 % disturbance -> output
y_dss = limit(s*Tdy*(1/s), s, 0)   % = 20/K
K_sol = solve(y_dss == 2.86, K)    % ~ 7
```

**Svar:** $\boxed{K=7 \Rightarrow \text{Mulighed 1}}$

> [!note] Hvorfor er det muligt at finde $K$?
> Selvom forstyrrelsen indgår, er den stationære disturbance-respons en **lukket form** i $K$ ($y_{ss,d}=20/K$) — ét tal ($2.86$) er nok til at løse for $K$. Derfor er distractoren "It is not possible…" forkert.

→ Metode: [[Steady-state-error-og-disturbance]] · Teori: [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]]

---

# Klynge Q5–Q11 — Figur 2 (open-loop Bode-plot, stabilt system)

> [!note] Om figuren
> Figur 2 er et Bode-plot af et **åben-sløjfe stabilt** system, x-akse $10^{-1}$ til $10^{2}$ rad/s. **Magnitude:** $\approx +30$ dB ved $\omega=0.1$, falder svagt (integrator-hældning) med et lille **plateau/shelf** omkring $\omega\approx1$–$2$ ($\approx+15$ dB, en zero), derefter en stejl rolloff, krydser $0$ dB ved $\omega\approx5$ og når $\approx-75$ dB ved $\omega=100$. **Fase:** starter på $-90°$ ved $\omega=0.1$ (én integrator), løftes svagt over $-90°$ omkring $\omega\approx0.5$ (zero), falder så gennem $-135°$, krydser $-180°$ ved $\omega\approx3.9$ og ender på $-270°$ ved høje frekvenser.

## Q5 — Type & orden fra Bode *(T7)*

**Hvad spørges om:** Aflæs *type* og *orden* af systemet fra Figur 2.

**Metode:** To aflæsninger:

> [!formula] Type fra startfase · orden fra slutfase + zeros
> - **Type:** lavfrekvens-fasen starter på $-90°$ $\Rightarrow$ **én integrator** $\Rightarrow$ **Type 1**.
> - **Slutfase:** fasen ender på $-270°$. Startfase $-90°$ (integrator) $+$ et zero-løft $(+90°)$ kræver poler der bidrager $-270°$ ekstra $\Rightarrow$ i alt $4$ poler, $1$ zero.

Regnestykket på slutfasen: $-90°\,(\text{integrator})+90°\,(\text{zero})-3\cdot90°\,(\text{3 ekstra poler})=-270°$. Det giver **4 poler** (orden 4) og **1 zero**. Magnituden bekræfter: høj-frekvens-hældning $=-(4-1)\cdot20=-60$ dB/dek (fra $\approx-20$ dB ved $\omega=10$ til $\approx-75$ dB ved $\omega=100$ $\approx-55$ dB/dek). ✓

**Svar:** $\boxed{\text{Type 1 og orden 4} \Rightarrow \text{Mulighed 4}}$

> [!tip] Det lille fase-løft = en zero
> At fasen kortvarigt stiger over $-90°$ inden den falder mod $-270°$ er signaturen for en **LHP-zero** (den giver $+90°$ lokalt). Uden zero'en ville et type-1-system af orden 3 også ende på $-270°$, men uden plateauet i magnituden — det er zero'en der tvinger orden op til 4.

→ Metode: [[Bode-aflæsning]] · Teori: [[Lec 6 — Bode-plot og Stabilitet]]

## Q6 — Phase margin & gain margin *(T8)*

**Hvad spørges om:** Aflæs phase margin (PM) og gain margin (GM) fra Figur 2.

**Metode:** Begge margins aflæses fra open-loop-plottet. Det afgørende er **rækkefølgen** af crossover og π-frekvens:

> [!formula] Margins fra Bode
> $$\text{PM}=180°+\angle G(j\omega_c)\quad\text{ved}\quad |G(j\omega_c)|=0\text{ dB}$$
> $$\text{GM}=-20\log_{10}|G(j\omega_\pi)|\quad\text{ved}\quad \angle G(j\omega_\pi)=-180°$$

På denne figur ligger **π-frekvensen før crossover**: fasen rammer $-180°$ ved $\omega_\pi\approx3.9$ rad/s, men magnituden er dér stadig **over** $0$ dB. Crossover ($0$ dB) sker først ved $\omega_c\approx5.2$ rad/s, hvor fasen allerede er **under** $-180°$. Begge målepunkter ligger derfor "på den forkerte side":

- Ved $\omega_c$ er $\angle G<-180°\Rightarrow \text{PM}=180°+\angle G(j\omega_c)<0$ $\Rightarrow$ **PM negativ**.
- Ved $\omega_\pi$ er $|G|>0$ dB $\Rightarrow \text{GM}=-20\log_{10}|G|<0$ $\Rightarrow$ **GM negativ**.

> [!warning] Negative margins ⟺ ustabil lukket sløjfe
> At **både** PM og GM er negative betyder, at den lukkede sløjfe er **ustabil** — selvom det åbne system er stabilt. Det er præcis fælden i opgaven: man må aflæse, at $\omega_\pi<\omega_c$ (fasen krydser $-180°$ *inden* magnituden krydser $0$ dB). De positive-margin-distractorer ("$21°$ og $6$ dB") forudsætter den omvendte rækkefølge.

**Svar:** $\boxed{\text{PM}<0 \text{ og GM}<0\ (-21°,\ -6\text{ dB}) \Rightarrow \text{Mulighed 4}}$

→ Metode: [[Stabilitet-Nyquist-margins]] · Teori: [[Lec 7 - Crossover Freq & Nyquist]]

## Q7 — Crossover- & π-frekvens *(T7/T8)*

**Hvad spørges om:** Angiv crossover-frekvensen $\omega_c$ og π-frekvensen $\omega_\pi$ fra Figur 2.

**Metode:** Samme to punkter som i Q6 — nu kun frekvenserne:

- $\omega_\pi$: hvor $\angle G=-180°$ $\Rightarrow \omega_\pi\approx 3.9$ rad/s.
- $\omega_c$: hvor $|G|=0$ dB $\Rightarrow \omega_c\approx 5.2$ rad/s.

> [!note] Rækkefølgen er pointen
> Fordi $\omega_\pi(3.9)<\omega_c(5.2)$ krydser fasen $-180°$ **før** magnituden krydser $0$ dB — netop betingelsen for de **negative** margins i Q6. Distractoren "$3.9$ og $5.2$" (dvs. $\omega_c=3.9<\omega_\pi=5.2$) ville svare til et stabilt system med positive margins — i modstrid med figuren.

**Svar:** $\boxed{\omega_c\approx5.2\text{ rad/s},\ \omega_\pi\approx3.9\text{ rad/s} \Rightarrow \text{Mulighed 2}}$

→ Metode: [[Bode-aflæsning]] · Teori: [[Lec 7 - Crossover Freq & Nyquist]]

## Q8 — Bandbredde $\omega_b$ *(T7)*

**Hvad spørges om:** Hvad er bandbredden $\omega_b$ for det **lukkede** system?

**Metode:** Bandbredden er en **closed-loop**-egenskab: den frekvens hvor closed-loop-magnituden $|G_{cl}(j\omega)|$ er faldet til $-3$ dB i forhold til lavfrekvens-niveauet. Det er **ikke** noget der kan aflæses direkte fra et **open-loop** Bode-plot.

> [!formula] Bandbredde defineres på closed-loop
> $$|G_{cl}(j\omega_b)|=\frac{1}{\sqrt2}\,|G_{cl}(0)| \quad(-3\text{ dB})$$

Figur 2 viser kun det åbne system $G(j\omega)$ — man ville skulle danne $G_{cl}=\frac{G}{1+G}$ og tegne **dets** Bode-plot for at aflæse $\omega_b$.

> [!tip] Crossover ≈ bandbredde — men kun som tommelfinger
> Selvom $\omega_b\approx\omega_c$ ofte bruges som approksimation, er den **eksakte** bandbredde en closed-loop-størrelse. Spørgsmålet beder ikke om en approksimation men om aflæsning — og den kan ikke gøres på open-loop-plottet. Derfor er det "ikke-læsbare"-svaret det korrekte.

**Svar:** $\boxed{\text{Kan ikke læses på open-loop Bode-plottet} \Rightarrow \text{Mulighed 3}}$

→ Metode: [[Bode-aflæsning]] · Teori: [[Lec 6 — Bode-plot og Stabilitet]]

## Q9 — P-controller for PM$=60°$ *(T9)*

**Hvad spørges om:** Systemet styres nu med en P-controller. Bestem $K_p$ så phase margin $=60°$.

**Metode (fasen bestemmer $\omega_c$, magnituden bestemmer $K_p$):**

> [!formula] P-design fra Bode
> 1. PM$=60°$ kræver fasen $=-180°+60°=-120°$ ved crossover. $K_p$ ændrer **ikke** fasen, så $\omega_c$ aflæses dér hvor $\angle G=-120°$.
> 2. Aflæs $|G(j\omega_c)|$ og vælg $K_p=\dfrac{1}{|G(j\omega_c)|}$ så $|K_p G|=0$ dB ved $\omega_c$.

- Fasen rammer $-120°$ ved $\omega_c\approx 2.5$ rad/s (mellem $-90°$ og $-135°$ på fasekurven).
- Magnituden dér er $\approx +14$ dB $\Rightarrow |G(j\omega_c)|\approx10^{14/20}\approx 5\Rightarrow K_p=\dfrac{1}{5}\approx 0.2$.

```matlab hl:/bode\(|margin\(/
% Verifikation når G(s) er kendt: find wc hvor fasen = -120 grader
s = tf('s');
% G = ...   % indsæt aflaest/identificeret G(s)
w = logspace(-2,2,2e5);
[mag,ph] = bode(G,w); mag = squeeze(mag); ph = squeeze(ph);
idx = find(ph <= -120, 1, 'first');   % fase = -180 + PM
Kp  = 1/mag(idx);
fprintf('wc = %.3g rad/s,  Kp = %.3g\n', w(idx), Kp);
[~,PM] = margin(Kp*G);  fprintf('Kontrol: PM = %.3g grader\n', PM);
```

**Svar:** $\boxed{K_p\approx0.2 \Rightarrow \text{Mulighed 3}}$

> [!tip] $K_p<1$ giver mening her
> Ved $-120°$-punktet ligger magnituden **over** $0$ dB ($\approx+14$ dB), så P-gainet skal **dæmpe** ($K_p=0.2$, dvs. $-14$ dB) for at trække crossover ned til den ønskede frekvens. Et $K_p>1$ ville løfte kurven og rykke crossover til en højere frekvens med for lille (eller negativ) PM.

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 7 - Crossover Freq & Nyquist]]

## Q10 — Øg bandbredde uden tab af PM *(T10)*

**Hvad spørges om:** Man ønsker **større** bandbredde end med P-controlleren, men **uden** at reducere phase margin. Hvordan?

**Metode:** Bandbredde $\approx$ crossover-frekvens. At skubbe crossover op koster normalt PM (fasen er mere negativ ved højere $\omega$). Et **Lead-led** tilfører positivt fasebidrag netop omkring crossover, så man kan flytte $\omega_c$ op **og** holde PM:

> [!formula] Lead løfter fasen ved crossover
> $$C_\text{lead}(s)=\frac{\tau_d s+1}{\alpha\tau_d s+1},\ \alpha<1\quad\Rightarrow\quad \text{max faseløft }\phi_m=\arcsin\frac{1-\alpha}{1+\alpha}$$

- **Øget $K_p$:** flytter crossover op, men **reducerer** PM (fasen falder) — opfylder ikke kravet.
- **Reduceret $K_p$:** sænker crossover (mindre bandbredde) — forkert retning.
- **I-led / lag-led:** trækker fasen **ned** ved crossover $\Rightarrow$ mindre PM.
- **Lead-led:** løfter fasen $\Rightarrow$ tillader højere $\omega_c$ med bevaret PM. ✓

**Svar:** $\boxed{\text{Et Lead-led tilføjes til P-controlleren} \Rightarrow \text{Mulighed 5}}$

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 8 — PI-Lead Controller Design]]

## Q11 — Stor bandbredde + nul stationær fejl *(T10)*

**Hvad spørges om:** Systemet skal styres så **både** en stor bandbredde opnås **og** den stationære fejl $e_{ss,r}$ ved et step er $0$. Hvilken controller skal tilføjes P-controlleren?

**Metode:** Nøglen er at systemet **allerede er Type 1** (jf. Q5: fasen starter på $-90°$). Et type-1-system har **allerede** $e_{ss}=0$ for et step — der skal **ikke** tilføjes en integrator (I-led) for at fjerne step-fejlen.

> [!formula] Type 1 ⇒ step-fejl allerede nul
> $$e_{r,ss}=\frac{1}{1+\lim_{s\to0}L(s)}=0\quad(\text{type 1, integrator i loopet})$$

Tilbage står ønsket om **stor bandbredde** — det leverer et **Lead-led** (jf. Q10). Derfor: kun et **Lead** behøves; en ekstra integrator ville være overflødig (og koste fase/bandbredde).

**Svar:** $\boxed{\text{En Lead-controller} \Rightarrow \text{Mulighed 1}}$

> [!note] Hvorfor ikke "Både lead og I"?
> Et I-led ville kun give mening hvis systemet var **type 0** (endelig step-fejl). Her er det allerede type 1, så I-leddet er unødvendigt — og det ville sænke bandbredden via ekstra fasetab. "A lead controller" alene er det mest rigtige.

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 8 — PI-Lead Controller Design]]

---

# Klynge Q12–Q14 — Figur 3 (step-respons af $G_1$ og $G_2$)

> [!note] Om figuren
> Et 1.-ordens og et stabilt 2.-ordens system: $G_1(s)=\dfrac{k_1}{\tau s+1}$, $G_2(s)=\dfrac{k_2}{s^2+2\zeta\omega_n s+\omega_n^2}$. Et **unit-step** påføres begge; de har **samme statiske gain $K_0$**. Figur 3 (Step Response, tid $0$–$100$ s): **$G_1$ (blå)** stiger monotont (intet oversving) mod slutværdien **$8$**. **$G_2$ (grøn)** svinger kraftigt med første top $\approx13.7$ ved $t\approx12$ s og toppe ved $\approx t=12,\,37,\,62$ s, og dæmpes mod slutværdien $8$. Den stiplede vandrette linje ligger på $8$.

## Q12 — Statisk gain $K_0$ for $G_1$ *(T3)*

**Hvad spørges om:** Hvad er den statiske gain $K_0$ for $G_1(s)$?

**Metode:** For et **unit-step** er slutværdien lig den statiske gain (DC-gain). Aflæs hvor $G_1$ (blå) ender:

> [!formula] Final Value = DC-gain ved unit-step
> $$y_{1,\infty}=\lim_{s\to0}s\cdot\frac{1}{s}\,G_1(s)=G_1(0)=k_1=K_0$$

$G_1$ (blå) flader ud ved **$8$** $\Rightarrow K_0=8$. (Begge systemer har samme $K_0$, hvilket den grønne kurves middelværdi $8$ bekræfter.)

**Svar:** $\boxed{K_0=8 \Rightarrow \text{Mulighed 5}}$

> [!tip] Aflæs slutniveauet, ikke toppen
> Distractoren "$4$" kunne friste hvis man halverede; "$1/8$" er den reciprokke. Men slutværdien af step-responsen *er* DC-gainet — og den er tydeligt $8$ for begge kurver.

→ Metode: [[Time-response-2nd-order]] · Teori: [[Lec 3 — Laplace Transform & Transfer Functions]]

## Q13 — $\omega_n$ & $\zeta$ for $G_2$ *(T3)*

**Hvad spørges om:** Bestem $\omega_n$ og $\zeta$ for $G_2(s)$ fra step-responsen.

**Metode (oversving → $\zeta$, periodetid → $\omega_n$):**

> [!formula] Oversving → damping
> $$M_p=\frac{y_{\max}-y_\infty}{y_\infty}=\frac{13.7-8}{8}\approx0.71$$
> $$\zeta=\frac{-\ln M_p}{\sqrt{\pi^2+\ln^2 M_p}}=\frac{-\ln(0.71)}{\sqrt{\pi^2+\ln^2(0.71)}}\approx0.11\approx0.1$$

> [!formula] Periodetid → $\omega_n$
> $$T\approx25\text{ s (top-til-top)}\;\Rightarrow\;\omega_d=\frac{2\pi}{T}=\frac{2\pi}{25}\approx0.25\text{ rad/s}$$
> $$\omega_n=\frac{\omega_d}{\sqrt{1-\zeta^2}}\approx\frac{0.25}{0.995}\approx0.25\text{ rad/s}$$

```matlab hl:N
ymax = 13.7; yinf = 8;
Mp   = (ymax - yinf)/yinf;                 % ~0.71
zeta = -log(Mp)/sqrt(pi^2 + log(Mp)^2);    % ~0.11
T    = 25;                                 % top-til-top fra figuren
wd   = 2*pi/T;                             % ~0.25 rad/s
wn   = wd/sqrt(1-zeta^2);                  % ~0.25 rad/s
fprintf('zeta=%.2f, wn=%.2f rad/s\n', zeta, wn);
```

**Svar:** $\boxed{\omega_n\approx0.25\text{ rad/s},\ \zeta\approx0.1 \Rightarrow \text{Mulighed 3}}$

> [!note] Det store oversving ⇒ lille damping
> $M_p\approx71\%$ er meget kraftigt, hvilket tvinger $\zeta\approx0.1$ (svagt dæmpet). Distractoren "$\omega_n=4$" forveksler typisk $\omega_n$ med en frekvens i rad i stedet for at bruge periodetiden $T\approx25$ s.

→ Metode: [[Time-response-2nd-order]] · Teori: [[Lec 4 — Frekvensdomæne og S-plan]]

## Q14 — $\tau$ for $G_1$ *(T3)*

**Hvad spørges om:** Bestem tidskonstanten $\tau$ for $G_1(s)$ fra step-responsen.

**Metode:** For et 1.-ordens system er tidskonstanten den tid, outputtet bruger på at nå **$63{,}2\%$** af slutværdien:

> [!formula] Tidskonstant fra 1.-ordens step
> $$y_1(\tau)=0.632\cdot y_\infty=0.632\cdot8\approx5.06$$

Den blå kurve passerer $\approx5.06$ ved $t\approx 11$ s $\Rightarrow \tau\approx 11$ s. (Konsistens: $4\tau\approx44$ s svarer godt til hvor $G_1$ er færdig-indsvinget mod $8$ i figuren.)

**Svar:** $\boxed{\tau=11\text{ s} \Rightarrow \text{Mulighed 2}}$

> [!tip] $\tau$ er en tid, ikke en reciprok
> Distractorerne "$1/11$" og "$1/16$" er reciprokke (det ville være pol-placeringen $1/\tau$, ikke tidskonstanten). $\tau$ aflæses **direkte** i sekunder på tidsaksen ved $63{,}2\%$-punktet.

→ Metode: [[Time-response-2nd-order]] · Teori: [[Lec 3 — Laplace Transform & Transfer Functions]]

---

# Klynge Q15–Q16 — Figur 4 (sinus-respons: input $u$ og output $y$)

> [!note] Om figuren
> Et stabilt open-loop system **uden zeros**: $y(s)=G(s)u(s)$, med input $u(t)=1\times\sin(\omega_0 t)$. Figur 4 (tid $100$–$200$ s) viser **input $u(t)$ (blå)** med amplitude $1$ (toppe på $\pm1$) og **output $y(t)$ (grøn stiplet)** med amplitude $\approx0.53$ (dæmpet). Outputtet er **forskudt** (lagging) i forhold til input: målt forskydning $\Delta t\approx20$ s med periodetid $T\approx63$ s.

## Q15 — Faseskift $\phi(\omega_0)$ *(T7)*

**Hvad spørges om:** Hvad er faseskiftet $\phi(\omega_0)$ mellem input $u(t)$ og output $y(t)$?

**Metode:** Mål tidsforskydningen $\Delta t$ mellem to ens kendetegn (top-til-top eller nul-gennemgang) og omregn til grader via periodetiden:

> [!formula] Tidsforskydning → fase
> $$\phi(\omega_0)=-\frac{\Delta t}{T}\cdot360°$$
> $$\Delta t\approx20\text{ s},\quad T\approx63\text{ s}\;\Rightarrow\;\phi=-\frac{20}{63}\cdot360°\approx-114°\approx-116°$$

Outputtet topper **efter** inputtet (grøn top ved $t\approx162$ s mod blå top ved $t\approx142$ s) $\Rightarrow$ **negativt** faseskift på ca. $-116°$.

```matlab hl:N
dt = 20;     % aflaest tidsforskydning (output lagger input), sek
T  = 63;     % aflaest periodetid, sek
phi = -dt/T*360;          % ~ -114 grader -> naermeste mulighed -116
fprintf('phi = %.0f grader\n', phi);
```

**Svar:** $\boxed{\phi(\omega_0)\approx-116° \Rightarrow \text{Mulighed 4}}$

> [!tip] Fortegnet: output lagger ⇒ negativt
> En kausal, stabil $G$ giver altid en **faseforsinkelse** (lag) for et sinus-input $\Rightarrow$ $\phi<0$. De positive/små distractorer ($0°,\,-26°$) svarer til en næsten samtidig respons, hvilket figuren modsiger.

→ Metode: [[Bode-aflæsning]] · Teori: [[Lec 4 — Frekvensdomæne og S-plan]]

## Q16 — P-gain så $\omega_0$ bliver crossover *(T9)*

**Hvad spørges om:** En P-controller med gain $K$ skal designes så det åbne system får phase margin $\gamma_m=180°+\phi(\omega_0)$. Bestem $K$.

**Metode:** Kravet $\gamma_m=180°+\phi(\omega_0)$ er præcis definitionen af phase margin **netop ved frekvensen $\omega_0$**. Det betyder, at $\omega_0$ skal være den nye **crossover-frekvens** — altså skal $|K\,G(j\omega_0)|=1$:

> [!formula] Sæt crossover ved $\omega_0$
> $$|K\,G(j\omega_0)|=1\;\Rightarrow\;K=\frac{1}{|G(j\omega_0)|}$$

Magnituden $|G(j\omega_0)|$ aflæses fra figuren som amplitudeforholdet output/input:

$$|G(j\omega_0)|=\frac{|y|}{|u|}=\frac{0.53}{1}\approx0.53\;\Rightarrow\;K=\frac{1}{0.53}\approx1.85$$

```matlab hl:N
y_amp = 0.53;     % aflaest output-amplitude
u_amp = 1.0;      % input-amplitude (1*sin)
Gmag  = y_amp/u_amp;        % |G(jw0)| ~0.53
K = 1/Gmag;                 % ~1.85
fprintf('|G(jw0)| = %.2f,  K = %.2f\n', Gmag, K);
```

**Svar:** $\boxed{K\approx1.85 \Rightarrow \text{Mulighed 3}}$

> [!note] "En faktor lidt mindre end 2"
> Da output-amplituden er lidt **over** $0.5$ ($\approx0.53$), bliver $K=1/0.53$ lidt **under** $2$ — altså $\approx1.85$. Havde amplituden været præcis $0.5$ ville $K=2$; figurens en-anelse-større amplitude giver $1.85$.

→ Metode: [[Controller-design-P-PI-Lead]] · Teori: [[Lec 7 - Crossover Freq & Nyquist]]

---

## Q17 — Closed-loop transfer function (unit feedback) *(T1/T2)*

**Hvad spørges om:** Et open-loop system $G(s)=\dfrac{\omega_n^2}{s(s+2\zeta\omega_n)}$ lukkes med en **unit feedback loop**. Find den lukkede sløjfes transferfunktion $G_{cl}(s)$.

**Metode:** Med unity feedback er $G_{cl}=\dfrac{G}{1+G}$:

> [!formula] Closed-loop, unit feedback
> $$G_{cl}=\frac{G}{1+G}=\frac{\dfrac{\omega_n^2}{s(s+2\zeta\omega_n)}}{1+\dfrac{\omega_n^2}{s(s+2\zeta\omega_n)}}=\frac{\omega_n^2}{s(s+2\zeta\omega_n)+\omega_n^2}=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$$

```matlab hl:/feedback\(/
syms s wn zeta real
G = wn^2/(s*(s+2*zeta*wn));
Gcl = simplify(G/(1+G))        % = wn^2/(s^2 + 2*zeta*wn*s + wn^2)
```

**Svar:** $\boxed{G_{cl}=\dfrac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2} \Rightarrow \text{Mulighed 4}}$

> [!tip] Genkend standard-2.-ordensformen
> Det lukkede system er præcis standard-2.-ordenssystemet $\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$ med DC-gain $1$. Distractorerne med "$+1$" i stedet for "$+\omega_n^2$" i nævneren (eller manglende $\omega_n^2$ i tælleren) giver forkert DC-gain eller forkerte poler.

→ Metode: [[Blokdiagram-reduktion]] · Teori: [[Lec 3 — Laplace Transform & Transfer Functions]]

## Q18 — Non-minimum phase i closed-loop *(T10)*

**Hvad spørges om:** Hvilke problemer kan opstå når et **non-minimum phase** system indgår i en lukket sløjfe?

**Metode:** Et non-minimum-phase (NMP) system har en **RHP-zero**, som tilfører ekstra **negativt** faseskift (modsat en LHP-zero, der løfter fasen):

> [!formula] RHP-zero ⇒ ekstra fasetab
> En RHP-zero $(s-z_0),\ z_0>0$ bidrager $\angle\to-90°$ ved høje frekvenser (trækker fasen **ned**), hvilket **reducerer** $\angle G(j\omega_c)$ og dermed $\text{PM}=180°+\angle G(j\omega_c)$.

Det store negative faseskift gør det **svært at opnå en god phase margin** $\Rightarrow$ vanskeligere at stabilisere/gøre robust.

**Svar:** $\boxed{\text{Det store negative faseskift kan reducere phase margin} \Rightarrow \text{Mulighed 2}}$

> [!note] "Positivt faseskift" er forkert
> Distractorerne med "positivt faseskift" er forkerte: NMP-zeros giver netop **negativ** fase. Det er den negative fase, der spiser af phase margin og begrænser hvor høj crossover man kan vælge.

→ Metode: [[Stabilitet-Nyquist-margins]] · Teori: [[Lec 8 — PI-Lead Controller Design]]

## Q19 — Orden af $G(s)$ fra 2 ODE'er *(T5/T11)*

**Hvad spørges om:** Et system beskrives af **to 2.-ordens differentialligninger** ($\ddot{x}=f(x,u)$, $\ddot{y}=g(y,u)$) **plus en statisk lineær ligning**. Efter linearisering + Laplace fås $G(s)$. Hvad kan vi sige om $G(s)$?

**Metode:** Tæl tilstande/poler:

> [!formula] Orden = antal tilstande (poler)
> $$\ddot{x}=f \Rightarrow 2 \text{ tilstande},\quad \ddot{y}=g \Rightarrow 2 \text{ tilstande}\;\Rightarrow\;\text{op til }4\text{ poler}$$
> Den statiske ligning tilføjer **ingen** dynamik (ingen ekstra poler).

$G(s)$ har derfor **højst orden 4** — men hvis det ene delsystem bidrager med en **zero** der annullerer en pol i det andet, kan den effektive orden blive **lavere**. Altså: **orden 4 eller lavere**.

**Svar:** $\boxed{G(s)\text{ er af orden 4 eller lavere} \Rightarrow \text{Mulighed 5}}$

> [!tip] Pole-zero-annullering trækker orden ned
> Distractoren "præcis orden 4" overser, at zeros fra koblingen mellem ligningerne kan annullere poler. Og "orden 4 eller højere" er udelukket: en statisk ligning + to 2.-ordens-ligninger kan **aldrig** give mere end 4 poler.

→ Metode: [[Transfer-functions-og-poler]] · Teori: [[Lec 5 — Black-box Modelling og Linearisering]]

## Q20 — Impuls-respons af stabil $G(s)$ *(T3/T1)*

**Hvad spørges om:** Et **unit-impulse** påføres et stabilt lineært system $G(s)$. Hvad gælder for outputtet $y(t)$?

**Metode:** Et unit-impulse har Laplace-transform $U(s)=1$, så outputtet i s-domænet er simpelthen $G(s)$:

> [!formula] Impuls-respons = $\mathcal{L}^{-1}\{G\}$
> $$Y(s)=G(s)\,U(s)=G(s)\cdot1=G(s)\;\Rightarrow\;\mathcal{L}\{y(t)\}=G(s)$$

Impuls-responsen er pr. definition den inverse Laplace af transferfunktionen. (Da $G$ er stabilt går $y(t)\to0$ for $t\to\infty$ — men det er ikke en konstant $k>0$, og $y(t)\ne0$ for $t>0$.)

**Svar:** $\boxed{\mathcal{L}\{y(t)\}=G(s) \Rightarrow \text{Mulighed 5}}$

> [!note] Hvorfor de andre er forkerte
> - **$y\to\infty$:** ville kræve et ustabilt system.
> - **$y=0$ for $t>0$:** kun sandt hvis $G=0$.
> - **$y\to k>0$:** ville kræve en integrator (pol i origo) — men så var systemet ikke asymptotisk stabilt.
> - **$y\to k\sin(\omega t+\phi)$:** ville kræve udæmpede poler på imaginæraksen (marginal stabilitet).

→ Metode: [[Time-response-2nd-order]] · Teori: [[Lec 3 — Laplace Transform & Transfer Functions]]

---

## Nøgletermer

| Term | Betydning | Nøgleformel |
|---|---|---|
| Statisk loop-gain $K_0$ | DC-loop-gain (type 1) | $K_0=\lim_{s\to0}sL(s)$ |
| Type | Antal integratorer (poler i origo) | startfase $/(-90°)$ eller lavfrekvens-hældning |
| Orden | Antal poler | slutfase $/(-90°)$ $+$ antal zeros |
| Stationær step-fejl | Type 0: $\frac{1}{1+K_0}$; Type $\ge1$: $0$ | $e_{ss}=\lim_{s\to0}\frac{sR(s)}{1+L(s)}$ |
| Phase margin (PM) | Fase-afstand til $-180°$ ved crossover | $\text{PM}=180°+\angle G(j\omega_c)$ |
| Gain margin (GM) | Afstand til $0$ dB ved $\omega_\pi$ | $\text{GM}=-20\log_{10}\lvert G(j\omega_\pi)\rvert$ |
| Ustabil closed-loop | $\omega_\pi<\omega_c$ | **begge** margins negative |
| Bandbredde $\omega_b$ | $-3$ dB på **closed-loop** | $\lvert G_{cl}(j\omega_b)\rvert=\frac{1}{\sqrt2}\lvert G_{cl}(0)\rvert$ |
| Oversving → damping | 2.-ordens | $\zeta=\frac{-\ln M_p}{\sqrt{\pi^2+\ln^2 M_p}}$ |
| Periodetid → $\omega_n$ | 2.-ordens | $\omega_d=\frac{2\pi}{T}$, $\omega_n=\frac{\omega_d}{\sqrt{1-\zeta^2}}$ |
| Tidskonstant $\tau$ | 1.-ordens, $63{,}2\%$-punkt | $y(\tau)=0.632\,y_\infty$ |
| Faseskift fra sinus | Tidsforskydning → grader | $\phi=-\frac{\Delta t}{T}\cdot360°$ |
| Lead-fase | Maks. faseløft | $\phi_m=\arcsin\frac{1-\alpha}{1+\alpha}$ |
| Impuls-respons | Inverse Laplace af $G$ | $\mathcal{L}\{y(t)\}=G(s)$ ved unit-impulse |

→ Tilbage til [[00_Eksamensanalyse_og_strategi]] · Se også det rigtige sæt: [[E25]]
