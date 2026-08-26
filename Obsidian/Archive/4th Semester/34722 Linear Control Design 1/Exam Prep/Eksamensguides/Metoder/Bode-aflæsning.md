---
tags: [LCD, regulering, eksamen, metode, bode, frekvensrespons]
type: opskrift
dækker: [T7]
---

# Opskrift: Bode-aflæsning

> [!info] Hvornår bruges denne?
> Genkend på: *"Hvilket Bode-plot svarer til…"*, *"Find crossover-frekvensen"*, *"Aflæs phase margin fra Bode"*, *"Hvad er DC-gain af G(s)"*. En af de **hyppigste kategorier** — typisk 2–3 spørgsmål i MC-sæt.

---

## 1. Aflæsningsregler: hvert bidrag til magnitude og fase

| Element | Magnitude | Fase |
|---|---|---|
| Konstant $K>0$ | $20\log K$ dB (flad) | $0°$ |
| Integrator $1/s$ | $-20$ dB/dek (startende i $-20$ dB/dek) | $-90°$ |
| 1. ordens pol $1/({\tau s+1})$ | $-20$ dB/dek fra $\omega=1/\tau$ | $0°\to-90°$ |
| **LHP-zero** $(\tau s+1)$ | $+20$ dB/dek fra $\omega=1/\tau$ | $0°\to+90°$ (op) |
| **RHP-zero** $(s-z_0),\,z_0>0$ | $+20$ dB/dek (løft, som LHP) | $+180°$ ved DC $\to+90°$ (**ned**) |
| Komplekse poler | resonanstop i magnitude, fase $-180°$ | skarp dip |

> [!formula] Kombiner lineært
> Magnitude i dB: summer bidrag. Fase: summer bidragene fra alle elementer.

---

## 2. Genkend transfer function fra Bode-plot

**Systematisk 5-trins metode:**

1. **DC-gain**: $|G(0)|=10^{\text{dB}/20}$ (aflæs ved $\omega\to 0$ eller lav frekvens).
2. **Netto-hældning ved lav frekvens**: $-20n$ dB/dek → $n$ integratorpoler (type-$n$).
3. **Knæk nedad**: pol ved $\omega_k$ → $-20$ dB/dek ekstra fra $\omega_k$.
4. **Knæk opad**: zero ved $\omega_z$ → $+20$ dB/dek ekstra.
5. **Fase-signatur**:
   - Fase starter $0°$ → ingen integratorpoler/zeros udover dem ved $\omega=0$.
   - Fase starter $-90°$ → 1 integrator-pol.
   - Fase ender negativt + **resonanstop** i magnitude → komplekse poler.
   - Fase starter **over $90°$** (fx $+180°$) → RHP-zero.

> [!example] F22 Q5 — aflæs G(s) fra Bode
> - DC-mag $\approx 5.9$ dB $\Rightarrow |G(0)|=2$.
> - Flad til $\omega=1$, derefter $-40$ dB/dek $\Rightarrow$ **to poler** ($s=-1$ begge).
> - Fase starter **højt** ($\approx180°$; markør viser $165°$ ved $\omega=0.1$) og **daler** mod $-90°$ $\Rightarrow$ **RHP-zero** (non-minimum phase).
> - En RHP-zero $(s-z_0)$, $z_0>0$, bidrager $\angle(-z_0)=+180°$ ved DC og trækker fasen **ned** mod $+90°$ — modsat en LHP-zero der trækker op fra $0°$.
> - Slutfase $-90°$: to poler ($-180°$) $+$ zero ($+90°$) $=-90°$. Ingen resonanstop $\Rightarrow$ reelle poler.
> - $\Rightarrow G(s)=\dfrac{s-2}{(1+s)^2}$ — verificeret i MATLAB: fase $178°\to-88°$, $|G(0)|=2$. ✓

> [!tip] Mønstre der går igen (udover hældnings-tælling)
> - **Resonanstop** (pukkel over asymptoten) $=$ **komplekse poler**; jo højere/skarpere top, jo mindre dæmpning $\zeta$. *Kvantitativt* gælder pukkelhøjden $M_r\approx\tfrac{1}{2\zeta\sqrt{1-\zeta^2}}$ ($\zeta<0.7$) **kun for et rent/dominerende 2. ordens par** — i højere-ordens systemer (fx [[E25]] Q1, orden 4) er den blot en kvalitativ indikator. Ingen top → reelle poler.
> - **Plateau** (kurven flader ud før den falder stejlere igen) $=$ en **zero**: dens $+20$ dB/dek udligner midlertidigt en pols $-20$ dB/dek, så hældningen "pauser". Mønstret i [[E25]] Q1: resonanstop (komplekse poler) → plateau (zero) → stejl rolloff (resterende poler).
> - **Knæk ned, så hurtigt op igen** ($-20$ så $+20$ dB/dek tæt på hinanden) $=$ et **pol-zero-par** der næsten ophæver hinanden.
> - **Slutfase** $=-90°\cdot(\#\text{poler}-\#\text{zeros})$: pol-overskuddet bestemmer den (fx $-270°$ ⇒ pol-overskud $3$).

---

## 3. Crossover-frekvens og phase margin fra Bode

**Phase margin** aflæses fra **åben-sløjfe** Bode-plot:

> [!formula] Aflæsning af PM
> 1. Find $\omega_c$ hvor $|L(j\omega_c)|=0$ dB ($|L|=1$).
> 2. Aflæs fase $\angle L(j\omega_c)$.
> 3. $\text{PM}=180°+\angle L(j\omega_c)$.

> [!formula] $\omega_c$ vs. $\omega_\pi$ — to FORSKELLIGE frekvenser
> | Frekvens | Defineret ved | Aflæs på | Bruges til |
> |---|---|---|---|
> | **$\omega_c$** (gain crossover) | $\lvert L(j\omega_c)\rvert=0$ dB ($=1$) | magnitude-kurven | **phase margin** |
> | **$\omega_\pi$** (phase crossover) | $\angle L(j\omega_\pi)=-180°$ | fase-kurven | **gain margin** ($=-\lvert L(j\omega_\pi)\rvert_\text{dB}$) |
>
> De er **ikke** ens (kun tilfældigt sammenfaldende). Stabil closed-loop $\iff \omega_c<\omega_\pi$ (magnituden er allerede under $0$ dB når fasen rammer $-180°$).

> [!warning] $\omega_c$ er IKKE plottets start og IKKE −3 dB-punktet
> - **Plot-start** (fx $10^{-2}$ rad/s) er bare den valgte frekvensakse — ikke $\omega_c$.
> - **−3 dB-punktet** er **closed-loop båndbredden** $\omega_b$ (aflæst på den *lukkede* sløjfes magnitude, hvor den er faldet $3$ dB under DC) — et andet begreb end open-loop $\omega_c$.
> - $\omega_c$ er **kun** der hvor open-loop $\lvert L\rvert$ krydser $0$ dB.

```matlab hl:/bode\(|margin\(/
s = tf('s'); L = 8.4/(s*(s+2.1));
[GM,PM,wcg,wcp] = margin(L);
fprintf('PM=%.3g grader ved wc=%.3g rad/s\n', PM, wcp);
bode(L); hold on;
plot([wcp wcp],[-40 10],'r--');   % marker crossover
```

> [!warning] Open-loop vs. closed-loop Bode
> PM aflæses **kun** fra open-loop $L(s)=C(s)G(s)$ — **ikke** fra closed-loop $T(s)$.
> Resonanstop i **closed-loop** Bode $\Rightarrow$ systemet er underdamped ($\zeta$ lille) $\Rightarrow$ oscillationer i step-respons.

> [!tip] Verificér med LCD1 Exam Suite
> Solver-mode aflæser **$\omega_c$, $\omega_\pi$, GM og PM** automatisk og tegner Bode — du kan **overlay eksamens eget plot** og fade imellem for at bekræfte at din rekonstruerede $G(s)$ matcher. Se [[00_Eksamensanalyse_og_strategi]].

---

## 4. Bode-plot for typiske systemer (huske-kort)

```tikz
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc}
\begin{document}
\begin{tikzpicture}[>=Stealth, font=\scriptsize]
% Axes for magnitude
\draw[->] (0,0) -- (5,0) node[right]{$\omega$};
\draw[->] (0,-1.5) -- (0,1.5) node[above]{$|G|$ dB};
% Integrator: -20 dB/dek fra 0
\draw[blue] (0,1.0) -- (4.5,-0.5) node[right,blue]{$1/s$};
% 1st order pole: flat then -20 dB/dek
\draw[red] (0,0.5) -- (2,0.5) -- (4.5,-0.25) node[right,red]{$\frac{1}{\tau s+1}$};
\draw[dashed,red] (2,-1.5) -- (2,1.5) node[above,red]{$1/\tau$};
% 2nd order: resonance peak
\draw[teal] (0,0) -- (2.5,0) -- (3.0,0.8) -- (3.5,-0.5) -- (4.5,-1.0) node[right,teal]{complex poles};
\draw[dashed,teal] (2.5,-1.5) -- (2.5,1.5) node[above,teal]{$\omega_n$};
\end{tikzpicture}
\end{document}
```

---

## 5. MC-faldgruber

| Forkert udsagn (set i eksamenssvar) | Korrekt |
|---|---|
| "Magnitude starter i $0$ dB $\Rightarrow$ DC-gain $=0$" | $0$ dB $= 1$ (lineært) |
| "Hældning $-40$ dB/dek $\Rightarrow$ 4 poler" | nej, $-40$ = **2** poler pr. dek |
| "Positiv pol $\Rightarrow$ fase stiger i Bode" | positiv pol **sænker** fasen (som to poler) |
| "Resonanstop i closed-loop $\Rightarrow$ RHP-zero" | nej, det er komplekse poler |
| "Phase margin kan aflæses fra closed-loop Bode" | kun fra **open-loop** |

---

## Relateret

- Teori: [[Lec 6 — Bode-plot og Stabilitet]] · [[Lec 7 - Crossover Freq & Nyquist]]
- Naboopskrifter: [[Transfer-functions-og-poler]] · [[Stabilitet-Nyquist-margins]]
- Eksempler: [[F22]] Q4, Q5, Q6 · [[S21]] Q4, Q5, Q6
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
