---
tags: [LCD, regulering, eksamen, metode, tidsrespons, 2nd-order]
type: opskrift
dækker: [T3]
---

# Opskrift: Time response — 1./2. orden

> [!info] Hvornår bruges denne?
> Genkend på: *"Hvilken step-respons svarer til $\zeta=0$"*, *"Hvad er settling time"*, *"Klassificér systemet"*, *"Hvad er tidskonstanten for RC-kredsen"*. Optræder **i hvert sæt** (typisk 2–3 spørgsmål).

---

## 1. Første orden — RC-kreds / lavpas

$$G(s)=\frac{K}{\tau s+1},\qquad \tau=RC$$

| Tidspunkt | Amplitude (step $K=1$) |
|---|---|
| $t=\tau$ | $63.2\%$ |
| $t=3\tau$ | $95\%$ |
| $t=5\tau$ | $99\%$ ($\approx$ steady state) |
| $t=0$ | $0$ (initial value theorem: $\lim_{s\to\infty}sG(s)/s=0$) |
| $t\to\infty$ | $K$ (final value theorem) |

> [!warning] Hyppig MC-fælde
> *"Systemet er ved 63.2% efter 1 tidskonstant."* — sandt. Men *"efter RC ms"* kræver at du beregner $\tau=RC$ med rigtige enheder. F22 Q2: $R=50\ \Omega$, $C=160\ \mu\text{F}$ → $\tau=8\ \text{ms}$, **ikke** $16\ \text{ms}$.

```matlab
R = 50; C = 160e-6;
tau = R*C;
fprintf('tau = %.4g ms | t95 = %.4g ms | t99 = %.4g ms\n',...
        tau*1e3, 3*tau*1e3, 5*tau*1e3);
```

---

## 2. Anden orden — standardform

$$G(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$$

| Parameter | Aflæsning fra karakteristisk ligning $s^2+as+b$ |
|---|---|
| $\omega_n$ | $\sqrt{b}$ |
| $\zeta$ | $a/(2\omega_n)$ |

### Dæmpningsklassifikation (F22 Q10 type)

| $\zeta$ | Navn | Polerne | Step-respons |
|---|---|---|---|
| $0$ | Udæmpet | $\pm j\omega_n$ (imaginære) | vedvarende oscillation |
| $0<\zeta<1$ | **Underdamped** | $-\sigma\pm j\omega_d$ | oscillation → steady state |
| $=1$ | Kritisk dæmpet | dobbelt reel: $-\omega_n$ | ingen overshoot, hurtigste |
| $>1$ | Overdæmpet | to reelle negative | ingen overshoot, langsom |

```matlab hl:/roots\(|damp\(/
% Fra karakteristisk ligning
p = roots([1 2 2]);           % s^2 + 2s + 2 -> -1 ± 1i
damp(tf(1,[1 2 2]))           % viser wn, zeta, tidskonstant
```

---

## 3. Overshoot ↔ $\zeta$ ↔ phase margin

> [!formula] Overshoot og dæmpning
> $$M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}},\qquad \zeta = \frac{-\ln M_p}{\sqrt{\pi^2+(\ln M_p)^2}}$$
> $M_p$ er her den **lineære** andel (ikke procent): 10% overshoot $= M_p=0.10$.

> [!formula] Tidsdomæne-specs
> $$t_s \approx \frac{4}{\zeta\omega_n}\ (2\%\text{-kriterium};\ \tfrac{3}{\zeta\omega_n}\text{ for }5\%),\qquad t_r \approx \frac{1.8}{\omega_n}\ (\text{bedst for }\zeta\approx0.5),\qquad \omega_d=\omega_n\sqrt{1-\zeta^2}$$

```matlab hl:/stepinfo\(/
% Inline-konvertering (path-uafhængig); samme som overshoot2damping/damp2phase_margin:
Mp   = 0.10;
zeta = -log(Mp)/sqrt(pi^2+log(Mp)^2);                   % 0.591
PM   = atand(2*zeta/sqrt(-2*zeta^2+sqrt(1+4*zeta^4)));  % 58.6 grader
fprintf('zeta=%.3g, PM=%.3g grader\n', zeta, PM);
% Fuldt system-info direkte fra MATLAB:
G = tf(25, [1 6 25]);               % wn=5, zeta=0.6
info = stepinfo(G);
fprintf('Mp=%.3g%%, tr=%.3g s, ts=%.3g s\n',...
        info.Overshoot, info.RiseTime, info.SettlingTime);
```

---

## 4. MC-aflæsning: genkend step-respons fra plot

| Plot-karakteristik | System-type |
|---|---|
| Konstant oscillation, ingen dæmpning | $\zeta=0$, rene imaginære poler |
| Overshoot + dæmpede oscillationer | $0<\zeta<1$ (underdamped) |
| Ingen overshoot, eksponentiel | $\zeta\ge1$ (over- eller kritisk) |
| Steady-state $\ne$ 1 (ved unit step) | DC-gain $\ne 1$ |
| Starter stejlt, ender fladt | typisk 2. orden, underdamped |
| Stiger monotont, rammer ikke 1 | type-0 med P-ctrl, stationær fejl |

> [!warning] Hyppig MC-fælde ($\zeta=0$)
> Opgaven (F22 Q3, S21 Q3, F21 Q3) viser typisk 4 plot: (1) konstant oscillation ✓, (2) overdæmpet til 0.5 ✗, (3) underdamped til 0.5 ✗, (4) overdæmpet til 0.5 ✗. Det korrekte er **vedvarende oscillation med konstant amplitude** — ikke et der oscillerer og dæmpes. DC-gain i Q3 er $\omega_n/(s^2+\omega_n^2)|_{s=0}=1/\omega_n$ — men $\zeta=0$ systemet har *ingen* steady state (konstant oscillation). Vælg den eneste med **uændret amplitude**.

---

## 5. Genkend polernes placering fra respons

```tikz
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc}
\begin{document}
\begin{tikzpicture}[>=Stealth, font=\small]
\draw[->] (-3.5,0) -- (1.5,0) node[right]{$\mathrm{Re}$};
\draw[->] (0,-2.2) -- (0,2.2) node[above]{$\mathrm{Im}$};
\node at (-2,0) [circle,fill,inner sep=2pt,label=below:{$\zeta{>}1$}] {};
\node at (-1,0) [circle,fill,inner sep=2pt,label=below:{$\zeta{=}1$}] {};
\node at (-1, 1.2) [circle,fill,inner sep=2pt,label=right:{$0{<}\zeta{<}1$}] {};
\node at (-1,-1.2) [circle,fill,inner sep=2pt] {};
\node at (0, 1.5) [circle,fill,inner sep=2pt,label=right:{$\zeta{=}0$}] {};
\node at (0,-1.5) [circle,fill,inner sep=2pt] {};
\draw[dashed] (-3.5,-2) -- (-3.5,2) node[above,font=\scriptsize]{stabil grænse};
\end{tikzpicture}
\end{document}
```

---

## Relateret

- Teori: [[Lec 4 — Frekvensdomæne og S-plan]] · [[Lec 3 — Laplace Transform & Transfer Functions]]
- Næste trin: [[Controller-design-P-PI-Lead]] (design specs → controller)
- Eksempel: [[F22]] Q2, Q3, Q10 · [[S21]] Q3, Q10
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
