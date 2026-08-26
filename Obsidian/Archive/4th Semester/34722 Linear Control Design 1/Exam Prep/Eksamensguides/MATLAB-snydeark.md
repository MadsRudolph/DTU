---
tags: [LCD, regulering, eksamen, matlab, snydeark, cheatsheet]
type: snydeark
---

# MATLAB-snydeark — LCD eksamen

> [!tip] Brug under eksamen
> Alle blokke er **kørt og verificeret** i MATLAB R2025b. Kopiér, udfyld `← ...` og kør.
> ```matlab
> s = tf('s');     % gør det muligt at skrive G = 1/(s+1)
> ```
> De fleste opgaver klares med ren kerne-MATLAB (`tf`, `bode`, `margin`) — **ingen hjælpefunktioner nødvendige**. Vil du bruge de færdige konverteringsfunktioner (§7), så peg MATLAB på deres mappe først:
> ```matlab
> addpath(genpath(fileparts(pwd)))      % hvis du står i en undermappe af OLD EXAMS
> % eller cd til mappen "Matlab scripts" / brug den fulde sti
> ```
> Alle konverteringer kan også skrives **inline** (se §7) — så er du uafhængig af path.

## 1. Byg en transfer function

```matlab
s = tf('s');
G = 12/((s+2)*(s+3));          % direkte
G = tf([1 0],[1 2 2]);         % tæller/nævner: (s)/(s^2+2s+2)
G = zpk([-2],[-1 -3],5);       % zeros, poler, gain
% Differentialligning a2*y'' + a1*y' + a0*y = b*u  ->
G = tf(b,[a2 a1 a0]);          % nævner = karakteristisk polynomium
```

> [!tip] Byg open-loop $L(s)$ fra et blokdiagram
> ```matlab
> C = 5*(s+1)/(s+3);  G = 1/(s*(s+2));  H = 1;   % ← UDFYLD blokke
> L = C*G;                 % serie = gang blokkene (series(C,G) gør det samme)
> Lpar = C + G;            % parallelle grene til samme sum (= parallel(C,G))
> T = feedback(L,H);       % luk sløjfen: L/(1+L*H)
> ```
> Til større/rodede diagrammer: brug **LCD1 Exam Suite**'s Block Diagram-mode (tegn eller importér screenshot → eksakt symbolsk $L(s)$). Se [[00_Eksamensanalyse_og_strategi]].

## 2. Analysér et system (poler, nuller, respons)

```matlab hl:/pole\(|damp\(|dcgain\(/
pole(G), zero(G)               % poler og nuller
dcgain(G)                      % DC-gain = G(0)
damp(G)                        % wn, zeta og tidskonstant for alle poler
step(G)                        % step-respons
bode(G), grid on               % Bode-plot
nyquist(G)                     % Nyquist-plot
```

> [!formula] dB ↔ lineær (bruges konstant)
> $$\text{dB}=20\log_{10}|G|,\qquad |G|=10^{\text{dB}/20}$$
> $\;6$ dB $\approx 2\quad|\quad 20$ dB $=10\quad|\quad 40$ dB $=100\quad|\quad -3$ dB $\approx 0.707$

## 3. Stabilitetsmargener

```matlab hl:/margin\(/
[GM,PM,wcg,wcp] = margin(L);   % L = open-loop. GM lineær, PM i grader
fprintf('GM=%.3g (%.3g dB), PM=%.3g grader ved wc=%.3g\n',...
        GM, 20*log10(GM), PM, wcp);
T = feedback(L,1);             % lukket sløjfe (unity feedback)
isstable(T)                    % 1 = stabil
```

> [!formula] Margener
> $$\text{PM}=180°+\angle L(j\omega_c)\;\big|_{|L|=1},\qquad \text{GM}=\frac{1}{|L(j\omega_{180})|}$$
> **Nyquist gain margin** fra reelt aksekryds $x$: $\;\text{GM}=\dfrac{1}{|x|}$ → dB med $20\log_{10}$.

## 4. P-controller → ønsket phase margin

```matlab hl:/bode\(|margin\(/
G = 1/(s*(s+2.1));   PMdes = 40;        % ← UDFYLD
w = logspace(-3,4,2e5);
[mag,ph] = bode(G,w); mag=squeeze(mag); ph=squeeze(ph);
i  = find(ph <= -180+PMdes, 1, 'first');
Kp = 1/mag(i);
fprintf('Kp=%.4g (%.4g dB) ved wc=%.4g\n', Kp, 20*log10(Kp), w(i));
```

## 5. Lead-design

```matlab hl:N
phi_m = 19.08;  wc = 6.4;               % ← UDFYLD nødvendig fase + crossover
alpha = (1-sind(phi_m))/(1+sind(phi_m));
taud  = 1/(wc*sqrt(alpha));
CD    = (taud*s+1)/(alpha*taud*s+1);
fprintf('alpha=%.4g, taud=%.4g, loeft=%.4g dB\n', alpha, taud, 20*log10(1/sqrt(alpha)));
```

## 6. Fuldt PI-Lead → find K_P

```matlab hl:/bode\(|evalfr\(/
G  = 900/((0.25*s+1)*(s^2+50*s+3000));  % ← UDFYLD anlæg
gM = 75;  Ni = 3;  alpha = 0.01;        % ← UDFYLD specs
phi_i = atand(-1/Ni);  phi_m = asind((1-alpha)/(1+alpha));
phiG  = -180 + gM - phi_m - phi_i;
w = logspace(-2,4,4e5); [~,ph]=bode(G,w); ph=squeeze(ph);
wc = w(find(ph <= phiG,1,'first'));
taui = Ni/wc;  taud = 1/(wc*sqrt(alpha));
CPI = (taui*s+1)/(taui*s);  CD = (taud*s+1)/(alpha*taud*s+1);
Kp  = 1/abs(evalfr(G*CPI*CD,1j*wc));
fprintf('wc=%.4g, Kp=%.5g\n', wc, Kp);
```

## 7. Spec-konverteringer (hjælpefunktioner)

```matlab hl:N
% INLINE-formler (uafhængige af path — sikrest til eksamen):
Mp   = 0.10;
zeta = -log(Mp)/sqrt(pi^2 + log(Mp)^2);          % overshoot -> zeta  (= 0.591)
Mp   = exp(-pi*zeta/sqrt(1-zeta^2));             % zeta -> overshoot
PM   = atand(2*zeta/sqrt(-2*zeta^2+sqrt(1+4*zeta^4)));  % zeta -> phase margin (= 58.6)
% Tommelfinger: zeta ~ PM[grader]/100

% FÆRDIGE funktioner (kræver path til "Matlab scripts", se top):
%   overshoot2damping  damping2overshoot  overshoot2phase_margin
%   damp2phase_margin  bandwidth2crossover_frequency  crossover_frequency2bandwidth
```

> [!formula] Vigtigste sammenhænge
> $$M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}},\quad t_s\approx\frac{4}{\zeta\omega_n}\,(2\%),\quad t_r\approx\frac{1.8}{\omega_n}\,(\zeta\approx0.5),\quad \zeta\approx\frac{\text{PM}°}{100}$$

## 8. Bode-aflæsning (hurtig-reference)

| På plottet | Betyder |
|---|---|
| Start-magnitude flad | type-0; start-hældning $-20$ dB/dek → 1 integrator (type-1) |
| Hældning $-20\,n$ dB/dek | $n$ poler dominerer |
| Knæk nedad ($-20$ dB/dek) | pol ved den frekvens |
| Knæk opad ($+20$ dB/dek), fase **op** | LHP-zero |
| Knæk opad ($+20$ dB/dek), fase **ned** | RHP-zero (non-minimum phase, starter $+180°$ ved DC) |
| Resonanstop | komplekse poler ($\zeta$ lille) |
| Slutfase $-90°\cdot(\#\text{poler}-\#\text{zeros})$ | tæl netto poler |

## 9. Karakteristisk ligning → dæmpning

```matlab hl:/roots\(/
roots([1 2 2])                 % poler; komplekse -> underdamped
% s^2 + 2*zeta*wn*s + wn^2 :  wn=sqrt(a0); zeta = a1/(2*wn)
```

| $\zeta$ | Type | Poler |
|---|---|---|
| $0$ | udæmpet | rent imaginære |
| $0<\zeta<1$ | underdamped | komplekse, neg. realdel |
| $1$ | kritisk dæmpet | dobbelt reel |
| $>1$ | overdæmpet | to reelle |

---

→ Metoder i detaljer: [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] · [[Time-response-2nd-order]]
→ Oversigt: [[00_Eksamensanalyse_og_strategi]]
