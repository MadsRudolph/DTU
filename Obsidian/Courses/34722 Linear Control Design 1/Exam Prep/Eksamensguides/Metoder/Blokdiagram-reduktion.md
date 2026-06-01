---
tags: [LCD, regulering, eksamen, metode, blokdiagram]
type: opskrift
dækker: [T2]
---

# Opskrift: Block diagram reduction

> [!info] Hvornår bruges denne?
> Genkend i multiple-choice på: *"Find $Y(s)/R(s)$ for blokdiagrammet"* — altid **Q1 i hvert sæt** (fast slot!). Diagrammet er altid mere komplekst end det ser ud til; gå systematisk indefra.

---

## Standard lukket sløjfe

```tikz
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc}
\begin{document}
\begin{tikzpicture}[
    block/.style={draw, minimum height=2.5em, minimum width=3.5em},
    sum/.style={draw, circle, minimum size=1.5em, inner sep=0pt},
    input/.style={coordinate},
    output/.style={coordinate},
    >=Stealth
]
\node[input] (inp) {};
\node[sum, right=1.0cm of inp] (sum) {};
\node[block, right=1.0cm of sum] (C) {$C(s)$};
\node[block, right=1.2cm of C] (G) {$G(s)$};
\node[output, right=1.3cm of G] (out) {};
\node[block, below=0.8cm of G] (H) {$H(s)$};

\draw[->] (inp) -- node[above]{$R(s)$} (sum);
\draw[->] (sum) -- node[above]{$E(s)$} (C);
\draw[->] (C) -- node[above]{$U(s)$} (G);
\draw[->] (G) -- node[above]{$Y(s)$} (out);
\coordinate (fb) at ($(G.east)+(0.6,0)$);
\draw (G.east) -- (fb);
\draw[->] (fb) -- (fb |- H.east) -- (H.east);
\draw[->] (H.west) -- (H.west -| sum.south) -- (sum.south);
\node at ($(sum)+(-0.3,0.3)$) {\tiny$+$};
\node at ($(sum)+(0.3,-0.3)$) {\tiny$-$};
\end{tikzpicture}
\end{document}
```

> [!formula] Standard feedback-formel
> $$\frac{Y(s)}{R(s)}=\frac{C(s)\,G(s)}{1+C(s)\,G(s)\,H(s)}$$
> Med unity feedback ($H=1$): $\;\dfrac{CG}{1+CG}$

---

## Find G fra punkt A til punkt B (generel opskrift)

Du behøver ikke huske en formel pr. opgave — én regel dækker alt i en single-loop-struktur:

> [!formula] Master-reglen
> $$\frac{Y}{X}=\frac{\text{forward path fra }X\text{ til }Y}{1+\text{loop gain}}$$
> - **Forward path** = produktet af blokkene på vejen fra input $X$ frem til output $Y$ (uden at gå rundt i sløjfen).
> - **Loop gain** $L$ = produktet af alle blokke hele vejen **rundt** i sløjfen. Den er **fælles for alle inputs** → nævneren $1+L$ er den samme uanset hvilket punkt du ser fra.
> - Flere inputs? Sæt **alle andre inputs $=0$** og læg bidragene sammen (superposition).

**Tre skridt, helt simpelt:**
1. Find **nævneren** én gang: $1+L$ (gå hele vejen rundt). Unity feedback med forward $CG$: $L=CG$.
2. **Tælleren** = forward path fra det input du kigger på, frem til outputtet.
3. Har du flere inputs (fx reference $r$ **og** forstyrrelse $d$), behandl ét ad gangen.

> [!example] Tre klassiske "fra A til B" — samme nævner
> Standard sløjfe: forward $G$, controller $C$, feedback $H$, reference $r$ og forstyrrelse $d$ adderet ved anlæggets input.
> $$\frac{Y}{R}=\frac{CG}{1+CGH}\ (d{=}0),\qquad \frac{Y}{D}=\frac{G}{1+CGH}\ (r{=}0),\qquad \frac{E}{R}=\frac{1}{1+CGH}$$
> **Samme nævner** $1+CGH$ overalt — kun tælleren (forward path) skifter. For $Y/D$ er forward path kun $G$ (forstyrrelsen rammer *efter* $C$); for fejlen $E/R$ er den $1$. Det er hele tricket.

> [!tip] Verificér med LCD1 Exam Suite
> I **Block Diagram-mode** tegner du diagrammet (eller importerer et screenshot og tracer over det), vælger **Source** og **Sink**, og får den eksakte symbolske $\tfrac{Y}{X}$ — inkl. open-loop $L(s)$, closed-loop $Y/R$ og **disturbance-respons** direkte. Se [[00_Eksamensanalyse_og_strategi]].

---

## Reduktionsregler

| Konfiguration | Resultat |
|---|---|
| **Serie** (A→B) | $AB$ |
| **Parallel** (A og B til samme sum) | $A+B$ |
| **Feedback** ($G$ forward, $H$ feedback, $-$) | $\dfrac{G}{1+GH}$ |
| **Flyt take-off-punkt forbi blok $B$** (bagud) | Del $H$ med $B$ |
| **Flyt take-off-punkt forbi blok $B$** (fremad) | Gang $H$ med $B$ |
| **Flyt summeringspunkt forbi blok $B$** (bagud) | Gang input med $B$ |

> [!warning] Hyppig fejl: take-off-punkt
> Når du *rykker et take-off-punkt* til den anden side af en blok $E$ (fx for at samle feedback-loops), skal feedback-grenen **divideres** med $E$ (flytning bagud). Det er kilden til den forkerte multiplikation med $E$ i F22 Q1, mulighed 2.

---

## Systematisk fremgangsmåde (fra inderst til yderst)

1. **Find det inderste loop** — det loop med ingen andre loops inde i sig.
2. **Reducer det** med feedback-formlen til ét blok.
3. **Gentag** til kun ét loop er tilbage.
4. Husk: efter reduktion *kan* du skulle flytte et take-off-punkt for at næste loop lader sig reducere — husk at justere feedback-grenen.

> [!example] F22 Q1 — trin-for-trin
> Diagram: $R\to\sum\to A\to B\to\sum\to C\to E\to Y$, med $D$ parallel til $C$, feedback $H_2$ fra udgangen af $C+D$ (vist som $C+D$-sum), og feedback $H_1$ fra $Y$ tilbage til $R$-summeren.
>
> 1. $A,B$ i serie → $AB$. Indre unity-loop om $AB$ → $\dfrac{AB}{1+AB}$.
> 2. $C \parallel D$ → $C+D$.
> 3. Flyt take-off-punkt *bag* $E$ (forlæns) → $H_1$ divideres med $E$ (dvs. $H_1/E$).
> 4. $(C+D)\cdot E$ i serie med blok fra trin 1. Ydre loop med $H_2$ → reduktion.
> 5. Samlet feedback med $H_1$ → slutformel.
>
> $$\frac{Y}{R}=\frac{ABE^2(C+D)}{(1+AB)[1+(C+D)EH_2]E+ABE(C+D)H_1}$$

---

## MC-afkodning: sådan gennemskuer du forkerte svar

| Symptom på forkert svar | Fejl-type |
|---|---|
| Mangler $E^2$ i tæller | Glemte take-off-punkt → mangler én $E$ |
| Forkert fortegn i nævner ($-$ i stedet for $+$) | Forkert feedback-polaritet |
| $E$ i stedet for $E^2$ i tæller | Rykket take-off-punkt forkert vej |
| Mangler $H_1$ i nævner | Ydre loop ikke medregnet |

---

## MATLAB (til hurtig verifikation)

```matlab hl:/feedback\(/
s = tf('s');
A=1; B=2; C=3; D=4; E=5; H1=0.1; H2=0.2;   % ← UDFYLD med konkrete TFs
% Trin 1: indre loop
T1 = feedback(A*B, 1);
% Trin 2: parallel
CD = C + D;
% Trin 3: ydre loop (tager take-off-punktflytning højde for med E)
T2 = feedback(T1 * CD * E, H2);
% Trin 4: samlet feedback
T = feedback(T2 * E, H1/E);   % H1 divideret med E fordi take-off rykket bagud
% NB: kun relevant for symbolske blokke — gælder ikke disse tal!
```

> [!note] I multiple-choice
> Du skal sjældent **beregne** noget — du skal **genkende fejlen** i de forkerte svar. Følg take-off-punkterne og tjek fortegn systematisk.

→ Teori: [[Lec 2 — Blokdiagrammer og Håndjustering]] · Eksempel: [[F22]] Q1
