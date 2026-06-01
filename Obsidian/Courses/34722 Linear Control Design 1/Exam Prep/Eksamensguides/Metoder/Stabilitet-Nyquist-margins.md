---
tags: [LCD, regulering, eksamen, metode, stabilitet, nyquist, margins]
type: opskrift
dækker: [T5, T8]
---

# Opskrift: Stabilitet — Routh-Hurwitz, Nyquist og margener

> [!info] Hvornår bruges denne?
> Genkend på: *"Find $w$ så systemet er stabilt"*, *"Hvad er gain margin fra Nyquist"*, *"Er den lukkede sløjfe stabil"*. Hyppigt emne — typisk 2 spørgsmål pr. sæt.

---

## 1. Stabilitetsbetingelse

Et LTI-system er **asymptotisk stabilt** $\iff$ **alle poler har negativ realdel** (ligger i venstre halvplan, LHP).

> [!formula] Nødvendig betingelse (hurtig check)
> Karakteristisk polynomium $a_n s^n+\cdots+a_0$: hvis **nogen koefficient** er $\le0$ eller mangler → ustabilt. Men positiv koefficienter er *ikke tilstrækkeligt* for $n\ge3$.

---

## 2. Routh-Hurwitz (T5)

For 2. orden $s^2+a_1 s+a_0$: stabil $\iff a_1>0$ og $a_0>0$.

For et system med en fri parameter $w$ (F22 Q9 — i opgaven kaldt "LTV", men reelt LTI med en konstant parameter): opsæt karakteristisk polynomium → kræv alle koefficienter $>0$ → løs for $w$.

> [!example] F22 Q9 — $A=[-1,1;\,2,-w]$
> $\det(sI-A)=s^2+(1+w)s+(w-2)$.
> Stabilt $\iff$ $1+w>0$ (→ $w>-1$) **og** $w-2>0$ (→ $w>2$) → **$w>2$** er den bindende betingelse.
>
> **Forkerte svar:** $w\le2$ (omvendt inekvation), $w\ge1$ (glemte $a_0$-betingelsen), $w<1$ (begge betingelser vendt).

```matlab hl:/charpoly\(/
syms w real; A = [-1 1; 2 -w];
cp = charpoly(A, 's');   % s^2 + (1+w)*s + (w-2)
```

---

## 3. Nyquist gain margin (T8)

```tikz
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc}
\begin{document}
\begin{tikzpicture}[>=Stealth, font=\small]
\draw[->] (-2.5,0) -- (0.8,0) node[right]{$\mathcal{R}(G)$};
\draw[->] (0,-1.8) -- (0,1.8) node[above]{$\mathcal{I}(G)$};
\draw[fill=none] (0,0) circle (1cm);
\node[above right, font=\scriptsize] at (0.7,0.7) {enhedscirkel};
\filldraw[green!60!black] (-0.1639,0) circle (2pt) node[below left,font=\scriptsize]{$(-0.164,0)$};
\filldraw[red] (-1,0) circle (2pt) node[below,font=\scriptsize]{$(-1,0)$};
\draw[<->] (-1,0.15) -- (-0.1639,0.15) node[midway,above,font=\scriptsize]{$\frac{1}{K_M}$};
\draw[blue,->] (0.9,1.2) .. controls (0,1.4) .. (-0.5,0.2);
\node[blue, font=\scriptsize] at (1.1,1.3) {Nyquist-kurve};
\end{tikzpicture}
\end{document}
```

Åben-sløjfe-kurven $G(j\omega)$ krydser den **negative reelle akse** i punktet $(x,0)$, $x<0$.

> [!formula] Gain margin
> $$K_M=\frac{1}{|x|}\qquad\Rightarrow\qquad K_M\,[\text{dB}]=20\log_{10}\!\left(\frac{1}{|x|}\right)$$

> [!warning] MC-faldgruber (F22 Q11)
> - $K_M=-15.71$ dB: tog $1/K_M$ i stedet for $K_M$.
> - $K_M=6.1$: glemte at konvertere til dB.
> - $K_M=0.1639$: tog bare $|x|$ (inverteret!).
> - $K_M=-6.1$: tog $-K_M$.

```matlab
x = -0.1639;
KM = 1/abs(x);
fprintf('KM = %.4g = %.4g dB\n', KM, 20*log10(KM));  % 6.1 = 15.71 dB
```

---

## 4. Nyquist-kriteriet og lukket sløjfe stabilitet (T8)

**Nyquist-kriteriet:** $Z=P-N$, hvor $Z$ = antal ustabile **closed-loop**-poler (vi vil have $Z=0$), $P$ = antal ustabile **open-loop**-poler, og $N$ = antal **mod-uret (CCW)**-omkredsninger af $(-1,0)$ talt positivt. Stabil closed-loop ($Z=0$) kræver derfor $N=P$.

For praktisk brug i eksamen:

| Situation | Krav for stabil CL |
|---|---|
| Stabilt OL-system ($P=0$) | Kurven omkreder **ikke** $(-1,0)$ |
| 1 ustabil OL-pol ($P=1$) | Kurven omkreder $(-1,0)$ **1 gang mod uret** |

> [!example] F22 Q12 — pol i RHP ($P=1$), krydser i $(-0.0222,0)$
> Kurven løber mod uret (CCW). Kræver **1 CCW-omkredsning** af $(-1,0)$.
> Kryds ved $-0.0222$. For at kurven (skaleret med $K_P$) omkreder $(-1,0)$ én gang:
> $K_P>1/0.0222\approx45$ → eneste mulighed: $K_P=50$ (mulighed b).
>
> **Distractor-analyse:**
> - $0.0222<K_P<1$: for lille gain, kurven skalerer ikke nok til at ramme $(-1,0)$.
> - $-45<K_P<0$: negativ gain spejler kurven om $y$-aksen → ikke den rette omkredsning.
> - $-0.0222<K_P<0$: for lille negativt gain.
> - $K_P=0.0222$: kurven rammer præcis $(-1,0)$ → marginalt stabilt, ikke stabilt.

---

## 5. Phase margin fra Bode (recap)

> [!formula] Sammenhæng GM/PM → step-respons
> | PM | Adfærd |
> |---|---|
> | $>60°$ | over-dæmpet, lille overshoot |
> | $\approx45°$ | ca. $20\%$ overshoot |
> | $<30°$ | stærke oscillationer |
> | $<0°$ | **ustabilt** |

```matlab hl:/margin\(/
[GM,PM,wcg,wcp] = margin(L);
fprintf('GM=%.4g dB, PM=%.4g grader\n', 20*log10(GM), PM);
```

---

## Relateret

- Teori: [[Lec 6 — Bode-plot og Stabilitet]] · [[Lec 7 - Crossover Freq & Nyquist]]
- Naboopskrifter: [[Bode-aflæsning]] · [[Controller-design-P-PI-Lead]]
- Eksempler: [[F22]] Q9, Q11, Q12 · [[S21]] Q9 · [[REExam-F21]]
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
