---
tags: [LCD, regulering, eksamen, metode, steady-state, fejl, disturbance]
type: opskrift
dækker: [T4]
---

# Opskrift: Steady-state error og disturbance

> [!info] Hvornår bruges denne?
> Genkend på: *"Hvad er steady-state fejlen til et step"*, *"Find $K_P$ fra stationær fejl"*, *"Hvilken forstyrrelse giver stationær fejl"*, *"Hvad er DC-gain i dB"*. Optræder typisk i 2 spørgsmål pr. sæt.

---

## 1. Final value theorem (FVT)

$$y(\infty)=\lim_{s\to0}s\,Y(s)$$

Brug til at finde steady-state fra transfer function og input. Gælder kun for **stabile** systemer (alle poler i LHP).

```matlab
s = tf('s');
G = tf(0.4,[0.1 1]);       % første orden, DC=0.4
T = feedback(2*G, 1);      % lukket sløjfe med Kp=2
ess = 1 - dcgain(T);       % fejl = 1 - y_ss for unit step
fprintf('e_ss = %.4g\n', ess);  % = 0.556
```

---

## 2. Stationær fejl for type-0 system med P-controller

```tikz
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc}
\begin{document}
\begin{tikzpicture}[
    block/.style={draw, minimum height=2.5em, minimum width=3.5em},
    sum/.style={draw, circle, minimum size=1.5em, inner sep=0pt},
    input/.style={coordinate}, output/.style={coordinate},
    >=Stealth
]
\node[input] (inp) {};
\node[sum, right=1cm of inp] (sum) {};
\node[block, right=1cm of sum] (Kp) {$K_P$};
\node[block, right=1.2cm of Kp] (G) {$G(s)$};
\node[output, right=1.3cm of G] (out) {};
\draw[->] (inp) -- node[above]{$R$} (sum);
\draw[->] (sum) -- node[above]{$E$} (Kp);
\draw[->] (Kp) -- (G);
\draw[->] (G) -- node[above]{$Y$} (out);
\coordinate (fb) at ($(G.east)+(0.6,0)$);
\coordinate (fbb) at ($(fb)+(0,-0.9)$);
\draw (G.east) -- (fb);
\draw[->] (fb) -- (fbb) -- (fbb -| sum.south) -- (sum.south);
\node at ($(sum)+(-0.3,0.3)$) {\tiny$+$};
\node at ($(sum)+(0.3,-0.3)$) {\tiny$-$};
\end{tikzpicture}
\end{document}
```

> [!formula] Type-0, unit step
> $$e_{ss}=\frac{1}{1+K_P G(0)}\qquad\Rightarrow\qquad K_P=\frac{1}{G(0)}\!\left(\frac{1}{e_{ss}}-1\right)$$
> For et **type-0**-system efterlader en P-controller altid en rest-fejl på step → brug **PI** (integrator gør loopet type-1). (Er anlægget allerede type-1, er step-fejlen $0$ med ren P.)

> [!tip] Hvis opgaven giver $y_{ss}$ (output) i stedet for $e_{ss}$ (fejl)
> De er **ikke** det samme — for unit step på reference (unity feedback) er de komplementære: $\;e_{ss}=1-y_{ss}$, hvor $y_{ss}=\dfrac{K_PG(0)}{1+K_PG(0)}$. Konvertér derfor først ($e_{ss}=1-y_{ss}$) og brug så formlen ovenfor. Eksempel: [[F25]] Q15 har $y_{ss}=0.999\Rightarrow e_{ss}=0.001$, så $K_P=\frac{1}{512}\big(\frac{1}{0.001}-1\big)=1.95$.

> [!example] F22 Q16
> $e_{ss}=0.555$, $G(0)=10^{-7.96/20}=0.4$:
> $K_P=\frac{1}{0.4}\!\left(\frac{1}{0.555}-1\right)=2.0$ → mulighed b.
>
> **Forkerte svar:** $K_P=1$ (unit gain, glemte $G(0)$), $K_P=2.5$ (brugte $1/G(0)=2.5$ i stedet for formlen), $K_P=0.4$ (bare DC-gain), $K_P=7.96$ (aflæste dB-værdien direkte).

| System-type | Input | Stationær fejl med P-ctrl |
|---|---|---|
| Type-0 | Step | $\dfrac{1}{1+K_P G(0)}\ne0$ |
| Type-0 | Ramp | $\infty$ |
| Type-1 | Step | $0$ |
| Type-1 | Ramp | $\dfrac{1}{K_v}$ |

---

## 3. Forståelse: hvor forstyrrelsen tilføjes afgør alt

> [!formula] Forstyrrelses-transfer-function
> For en forstyrrelse $D(s)$ der adderes **ved anlæggets input**:
> $$Y_D(s)=\frac{G(s)}{1+K_P G(s)}\,D(s)\quad\Rightarrow\quad y_D(\infty)=\frac{G(0)}{1+K_P G(0)}\,d$$
> For en forstyrrelse **ved output**: $Y_D=\dfrac{1}{1+K_P G}\,D$ → $y_D(\infty)=\dfrac{1}{1+K_P G(0)}\,d$.

Stationær fejl fra forstyrrelse kan kun elimineres med **integrator** i controller (PI/I) — en P-controller efterlader altid en rest.

---

## 4. Closed-loop Bode → stationær fejl (F22 Q14 type)

Fra **closed-loop** magnitude Bode ved $\omega=0$ (DC):
- $|T(0)|=1$ (0 dB) $\Rightarrow$ stationær fejl **=0** (systemet følger referencen præcist).
- $|T(0)|<1$ $\Rightarrow$ stationær fejl $= 1-T(0)>0$.

Resonanstop i closed-loop Bode $\Rightarrow$ komplekse poler $\Rightarrow$ **oscillationer** i step-respons.

```matlab hl:/dcgain\(/
s = tf('s');
G = 1/(s*(s+1));       % type-1 (integrator)
T = feedback(G, 1);    % lukket sløjfe
fprintf('T(0) = %.3g (0 dB = %.3g)\n', dcgain(T), 20*log10(dcgain(T)));
% = 1.0  => stationær fejl = 0
```

---

## 5. Feed-forward disturbance (F22 Q18 type)

Ideal feed-forward: $F_d(s)=D(s)/G_1(s)$ annullerer forstyrrelsen fuldstændigt.
Krav: $F_d$ skal være **proper** (antal poler ≥ antal zeros) — filter det med lavpas.

> [!formula] Feed-forward gain (statisk)
> $$K_{ff}=\frac{1}{G(0)}\qquad\text{(statisk kompensation af DC-forstyrrelse)}$$

→ Teori: [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]] · [[Lec 13 — Feed-forward Control]]

---

## Relateret

- Teori: [[Lec 3 — Laplace Transform & Transfer Functions]] (FVT) · [[Lec 12 — Forstyrrelser, Sensitivitet og Pre-filtre]]
- Naboopskrifter: [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]]
- Eksempler: [[F22]] Q2, Q14, Q15, Q16, Q18 · [[S21]] Q2, Q7
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
