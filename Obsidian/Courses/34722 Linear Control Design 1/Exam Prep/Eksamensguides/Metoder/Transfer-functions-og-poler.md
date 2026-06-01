---
tags: [LCD, regulering, eksamen, metode, transferfunction, poler]
type: opskrift
dækker: [T1]
---

# Opskrift: Transfer functions, poler og DC-gain

> [!info] Hvornår bruges denne?
> Genkend på: *"Find polerne for differentialligningen"*, *"Hvad er DC-gain i dB"*, *"Find transfer function for RLC-kredsen"*, *"Hvilke poler giver dette Bode-plot"*. Optræder **i hvert sæt** (Q7, Q8, Q5 er typiske slots).

---

## 1. Fra differentialligning til transfer function

$$a_n y^{(n)}+\cdots+a_1\dot{y}+a_0 y = b_0 u$$

Laplace-transformér (nul begyndelsesbetingelser):

$$G(s)=\frac{Y(s)}{U(s)}=\frac{b_0}{a_n s^n+\cdots+a_1 s+a_0}$$

> [!formula] Poler = rødder af nævneren
> $$a_n s^n+a_{n-1}s^{n-1}+\cdots+a_0=0$$

```matlab hl:/roots\(|tf\(/
% 5*y'' + y' + 0.5*y = 3*u  (F22 Q8)
G = tf(3, [5 1 0.5]);          % tf(tæller, nævner)
disp(pole(G).')                 % -0.1 ± 0.3i
disp(roots([5 1 0.5]).')        % samme
```

> [!example] F22 Q8
> $5\ddot{y}+\dot{y}+0.5y=3u \;\Rightarrow\; G=\dfrac{3}{5s^2+s+0.5}$
> $s=\frac{-1\pm\sqrt{1-10}}{10}=-0.1\pm 0.3i$ → **mulighed 2** ($s_{1,2}=-0.1\pm 0.3j$).
>
> **Forkerte MC-svar:** mulighed 1 ($-0.1,-0.1$) = dobbelt reel pol; mulighed 3 ($\pm0.3i$) = imaginær akse; mulighed 4 = positiv realdel (ustabil). Alle kræver en fejl i fortegn eller karakteristisk polynomium.

---

## 1b. Fra state-space / koblede ODE'er til transfer function (F21 Q6 type)

> [!info] Genkend
> *"$\dot x_1=\dots,\ \dot x_2=\dots,\ y=\dots$ — find $G(s)$"* eller *"opskriv $A,B,C,D$"*. Optræder som T11-slot (E25 Q6, E23 Q7, F21 Q6).

### Rute A — den hurtige MC-rute: Laplace pr. tilstand

Når systemet er **afkoblet** (hver $\dot x_i$ afhænger kun af sit eget $x_i$): Laplace-transformér hver linje for sig, isolér $X_i(s)$, og indsæt i $y$.

> [!example] F21 Q6
> $\dot x_1=-x_1+u,\quad \dot x_2=-x_2+9u,\quad y=x_1+x_2$
> $$X_1=\frac{1}{s+1}U,\quad X_2=\frac{9}{s+1}U \;\Rightarrow\; Y=X_1+X_2=\frac{10}{s+1}U$$
> **Intuition:** to parallelle 1.-ordens veje $\frac{1}{s+1}$ og $\frac{9}{s+1}$ summeret i outputtet $\to \frac{10}{s+1}$. → **mulighed 5**.

Til MC er dette næsten altid hurtigst — du slipper for matricer helt.

### Rute B — opskriv $A,B,C,D$ (nødvendig hvis et spørgsmål *giver* dig $A$)

$$\dot{\mathbf x}=A\,\mathbf x+B\,u,\qquad y=C\,\mathbf x+D\,u$$

**Sorteringsreglen — for hvert led, spørg "hvad ganger det?":**

| Leddet ganger… | …havner i |
|---|---|
| en **tilstand** ($x_1,x_2,\dots$) | **$A$** |
| **inputtet** $u$ | **$B$** |
| en tilstand i $y$-ligningen | **$C$** |
| $u$ direkte i $y$ (gennemløb) | **$D$** |

- **$A[i,j]$** = koefficienten til $x_j$ i ligningen for $\dot x_i$. Én **række pr. afledt** ($\dot x_i$), én **søjle pr. tilstand** ($x_j$).
- **$B[i]$** = koefficienten til $u$ i $\dot x_i$.

> [!example] Samme F21 Q6 på matrixform
> $$A=\begin{bmatrix}-1&0\\0&-1\end{bmatrix},\quad B=\begin{bmatrix}1\\9\end{bmatrix},\quad C=\begin{bmatrix}1&1\end{bmatrix},\quad D=[0]$$
> Derefter $G(s)=C(sI-A)^{-1}B+D=\dfrac{10}{s+1}$.

> [!warning] De to klassiske misforståelser
> **Hvorfor er $B$ ikke $-1+9=8$?** Fordi $-1$ ganger en **tilstand** ($-x_2$ → hører i $A$), mens $9$ ganger **inputtet** ($9u$ → hører i $B$). Forskellige variable ⟹ forskellige matricer — de lægges aldrig sammen.
>
> **Hvorfor er $A$ ikke $-1+1=0$?** $A$ er ikke ét tal, men et $2\times2$-gitter (2 tilstande). De to $-1$'er sidder i **forskellige celler**: øverst-venstre $-1$ = "$x_1$'s effekt på $\dot x_1$", nederst-højre $-1$ = "$x_2$'s effekt på $\dot x_2$". Kun led i **samme celle** lægges sammen (fx hvis én ligning havde både $-x_1$ og $+2x_1$ → $+1\cdot x_1$).
>
> **Tommelfinger:** en koefficients plads er låst af *(hvilken ligning, hvilken variabel)*. Samme ligning, anden variabel → anden søjle. Anden ligning → anden række.

> [!note] Diagonal $A$ = afkoblet system
> Her optræder $x_2$ aldrig i $\dot x_1$-ligningen (og omvendt) → nuller off-diagonalt → $A$ bliver diagonal. Det er præcis derfor Rute A virker: de to tilstande påvirker kun sig selv.

```matlab hl:/minreal\(|ss\(/
% F21 Q6: byg ss-objekt og reducér til G(s)
G = minreal(tf(ss([-1 0;0 -1],[1;9],[1 1],0)));
zpk(G)        % 10/(s+1)
```

---

## 2. DC-gain

$$G(0)=\lim_{s\to 0}G(s)=\frac{b_0}{a_0}$$

> [!warning] Type-0 vs. Type-1
> - **Type-0** (ingen integrator): DC-gain = endelig. $G(0)=b_0/a_0$.
> - **Type-1** (én integrator, $s$ i nævner): DC-gain $=\infty$.
>
> Brug final value theorem: $y(\infty)=\lim_{s\to0} s\cdot Y(s)$. Sæt $u=1/s$ (unit step).

> [!formula] DC-gain i dB
> $$|G(0)|_\text{dB}=20\log_{10}|G(0)|$$
> $6$ dB $\approx 2$, $20$ dB $=10$, $-6$ dB $\approx 0.5$, $-20$ dB $=0.1$

```matlab hl:/dcgain\(/
s = tf('s');
G = 12/((s+2)*(s+3));
fprintf('DC = %.3g = %.3g dB\n', dcgain(G), 20*log10(dcgain(G)));
% 12/(2*3) = 2 = 6 dB  (F22 Q7)
```

> [!example] F22 Q7
> $G(0)=12/(2\cdot3)=2=6.02$ dB → **mulighed 3**.
>
> **Forkerte svar:** $2$ (lineær, ikke dB), $12$ (tæller alene), $0$ (fejlagtig type-1 antagelse), $-15.6$ dB ($=20\log(1/6)$, dvs. inverteret).

---

## 3. Systemtype: 0, 1, 2 — antal integratorer

> [!formula] Type = antal poler i origo
> Skriv åben sløjfe som $L(s)=\dfrac{N(s)}{s^{k}\,D(s)}$ med $D(0)\ne0$ og $N(0)\ne0$. Så er $$\boxed{\text{type}=k}=\text{antal rene integratorer }(1/s)\text{ i sløjfen.}$$

**Tre måder at bestemme typen på — de skal give samme $k$:**

| Fra | Sådan |
|---|---|
| **Transfer function** | Faktorisér $s^k$ ud af nævneren — dvs. antal poler præcis i $s=0$. |
| **Bode-plot** | Lavfrekvens-hældning $=-20k$ dB/dek **og** startfase $=-90k°$. |
| **State-space** | Antal nul-egenværdier af $A$ (egenværdier i $s=0$). |

| Type | $L$ ved lav $\omega$ | DC-gain | Bode-start | Startfase | $e_{ss}$ step | $e_{ss}$ ramp |
|:--:|---|---|---|---|:--:|:--:|
| **0** | $K_0$ | endelig $=K_0$ | flad | $0°$ | $\tfrac{1}{1+K_0}$ | $\infty$ |
| **1** | $K_0/s$ | $\infty$ | $-20$ dB/dek | $-90°$ | $0$ | $\tfrac{1}{K_v}$ |
| **2** | $K_0/s^2$ | $\infty$ | $-40$ dB/dek | $-180°$ | $0$ | $0$ |

> [!warning] Type tælles i ÅBEN sløjfe — og kun ægte integratorer
> Tæl integratorer i $L=CG$, ikke i closed-loop. En pol i $-a$ ($\tfrac{1}{s+a}$) er **ikke** en integrator — kun $\tfrac{1}{s}$ (pol præcis i origo). Et **I-led / PI** hæver typen med 1 (fjerner én fejl-orden, koster $90°$ fase); **P / Lead** ændrer ikke typen.

> [!example] E25 Q1 & Q8
> - **Q1** (fra Bode): magnituden er **flad** ved lav $\omega$ + startfase $0°$ → ingen integrator → **Type 0**. *(Orden aflæses separat fra pol-overskuddet — se [[Bode-aflæsning]].)*
> - **Q8** (fra blokdiagram): kun feedback-grenens $\tfrac{1}{s}$ er en ægte integrator (den indre $\tfrac{1}{s}$ blev til $\tfrac{1}{s+a}$, pol i $-a$) → **Type 1**.

> [!tip] Verificér med LCD1 Exam Suite
> Solver-mode rapporterer **type + orden** automatisk for en indtastet $G(s)$, og `ess`-tabellen giver $K_p/K_v/K_a$ + step/ramp-fejl. Symbolske parametre ($K,a,\tau$) håndteres i app-UI'en. Fejl-detaljer: [[Steady-state-error-og-disturbance]]. Se [[00_Eksamensanalyse_og_strategi]] for værktøjet.

---

## 4. Poler fra state-space / LTV-system (F22 Q9 type)

Systemmatrix $A$ → karakteristisk polynomium $\det(sI-A)$ → stabilitet kræver alle rødder i venstre halvplan (negativt realdel).

> [!formula] 2×2 stabilitetsbetingelse
> $$s^2+(a_{11}+a_{22})s+(a_{11}a_{22}-a_{12}a_{21})$$
> Stabil $\iff$ alle koefficienter $>0$: trace $<0$ og determinant $>0$.

```matlab hl:/charpoly\(/
% Q9: A = [-1 1; 2 -w]  -> stabilt for w>?
syms w real
A = [-1 1; 2 -w];
cp = charpoly(A, 's');        % s^2 + (w+1)*s + (w-2)
% stabil: w+1>0 (=> w>-1) og w-2>0 (=> w>2) -> kombineret: w>2
```

---

## 5. Poler og systemkarakter

| Pol-placering | Tidssvar | Stabil? |
|---|---|---|
| Reel, negativ: $s=-a$ | eksponentielt aftagende $e^{-at}$ | ✓ |
| Reel, positiv: $s=+a$ | eksponentielt voksende | ✗ |
| Kompleks, neg. realdel: $-\sigma\pm j\omega$ | dæmpet oscillation | ✓ |
| Rent imaginær: $\pm j\omega$ | vedvarende oscillation | ✗ (grænse) |
| Kompleks, pos. realdel | voksende oscillation | ✗ |
| Dobbelt pol i origo | $t\cdot e^0 = t$ (rampe) | ✗ |

---

## 6. Genkend transfer function fra Bode (F22 Q5 type)

Systematisk aflæsning:
1. **DC-gain**: aflæs magnitude ved lav $\omega$ (herunder $s=0$).
2. **Antal poler**: tæl $-20$ dB/dek pr. pol i den endelige hældning.
3. **Antal zeros**: hver zero løfter med $+20$ dB/dek.
4. **Fase-startværdi**: $+90°\cdot (\#\text{zeros}_\text{LHP}-\#\text{zeros}_\text{RHP})-90°\cdot\#\text{poler}$ (ved $\omega\to0$).
5. **RHP-zero**: fase *falder* (som pol) — se [[Bode-aflæsning]] for detaljer.

> [!example] F22 Q5 — $G(0)\approx6$ dB, hældning $-40$ dB/dek, fase starter højt og daler
> DC-gain $=10^{6/20}=2$. To poler (hældning $-40$ dB/dek). Ingen resonanstop → reelle poler. Fasen **starter $\approx180°$** (markør $165°$) og **daler** til $-90°$ → en **RHP-zero**: $(s-z_0)$ bidrager $\angle(-z_0)=+180°$ ved DC og trækker fasen ned. Slutfase $-90°=$ to poler $(-180°)+$ zero $(+90°)$.
> $$\Rightarrow G(s)=\frac{s-2}{(1+s)^2}$$

---

## Relateret

- Teori: [[Lec 3 — Laplace Transform & Transfer Functions]] · [[Lec 4 — Frekvensdomæne og S-plan]]
- Naboopskrifter: [[Bode-aflæsning]] · [[Time-response-2nd-order]]
- Eksempler: [[F22]] Q5, Q7, Q8, Q9 · [[S21]] Q8, Q9
- Oversigt: [[00_Eksamensanalyse_og_strategi]]
