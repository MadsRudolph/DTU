---
tags: [LCD, regulering, eksamen, analyse, strategi, oversigt]
type: oversigt
---

# Eksamensanalyse & strategi — LCD 34722

> [!abstract] Hovedkonklusion
> Den skriftlige eksamen er **multiple choice** og genbruger de samme opgavetyper år efter år. Analysen dækker nu **11 eksamenssæt (2015–2025)** på tværs af kursuskoderne **31300 → 34721 → 34722** (samme fag). **6–8 emner dækker ~90% af eksamen.** Tre emner testes næsten aldrig (root locus, z-transform, state space) — spring dem. Denne side er din studieplan.

## Start her

1. Læs [[MATLAB-snydeark]] — copy-paste-skabelonerne du skal bruge.
2. Læs de 6 [[#De 6 emner du SKAL kunne|emne-opskrifter]] i `Metoder/`.
3. Regn de fuldt gennemgåede sæt — start med de nyeste [[E25]] (dec 2025) og [[E23]], og fortsæt bagud: [[E22]], [[E21]], [[E20]], [[E15]], [[F22]], [[S20]], [[S21]], [[REExam-F21]], [[Final-Test]].
4. Træn genkendelse med [[Quizzer]].

---

## Værktøj: LCD1 Exam Suite (øvelse & verifikation)

> [!tip] Offline app til at *verificere* dine hånd-svar
> En medstuderendes værktøj ligger i `OLD EXAMS/lcd1-exam-suite/` — en offline desktop-app der dækker **beregningsdelen** af hele pensum. Motoren er **verificeret** (385/385 tests; CLI-svar matcher hånd-beregninger eksakt). Brug den til at tjekke dine svar — ikke som erstatning for metoderne (til selve MC-eksamen har du den næppe).
>
> - **◧ Block Diagram** — tegn (eller importér screenshot af) et blokdiagram → eksakt symbolsk $L(s)$, $Y/R$, disturbance-respons, poler.
> - **∑ Solver** — skriv $G(s)$ → auto type/orden, GM/PM, $\omega_c/\omega_\pi$, ess, båndbredde, stabilitet; Step/Bode/Nyquist/PZ-plots (kan **overlay eksamens-plot**); **Smart Paste** trækker TF + svarmuligheder ud af en paste'et opgave. Eksporterer kørbar MATLAB.

| App-funktion (P1–P7) | Opgavetype → opskrift |
|---|---|
| ODE / state-space → TF (P1) | T1 → [[Transfer-functions-og-poler]] |
| Bode read-off → type/orden/GM/PM/$\omega_c$/$\omega_\pi$ (P2) | T7/T8 → [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] |
| Stable-K, margins (P3) | T8 → [[Stabilitet-Nyquist-margins]] |
| 2.-ordens specs (P4) | T3 → [[Time-response-2nd-order]] |
| ess-tabel, $K_P$ fra ess (P5) | T4 → [[Steady-state-error-og-disturbance]] |
| PI-Lead / P-for-PM (P6) | T9/T10 → [[Controller-design-P-PI-Lead]] |
| Feed-forward, nested ess (P7) | T4 → [[Steady-state-error-og-disturbance]] |
| Block reduction (Block Diagram-mode) | T2 → [[Blokdiagram-reduktion]] |

> [!warning] Kryds vigtige svar tjek
> Uofficiel studenter-app. Motoren er testet, men den numeriske CLI håndterer **ikke symboler** (symbolsk arbejde går gennem app-UI'en), og Smart Paste vælger bevidst **aldrig** ét svar automatisk. Brug den som tjek mod hånd-metoderne — især efter [[E23]]-erfaringen med forskudte facit-numre.

---

## Materialeoversigt (hvad er hvad)

| Guide | Sæt | Opgaver | Facit |
|---|---|---|---|
| [[E25]] ⭐ | **dec 2025 — nyeste** (34721) | 20 | X-markeret |
| [[E23]] | dec 2023 (34721) | 20 | fuldt (detaljeret) |
| [[E22]] | dec 2022 (34721) | 20 | fuldt (markeret) |
| [[E21]] | 2021 (31300) | 20 | fuldt (detaljeret) |
| [[E20]] | 2020 (31300) | 20 | fuldt (detaljeret) |
| [[E15]] | 2015 (31300) | 20 | fuldt (markeret) |
| [[F25]] | forår 2025 | 20 | beregnet (MATLAB) |
| [[F22]] | 25. maj 2022 (= "2022"-sættet) | 20 | fuldt |
| [[S20]] | forår 2020 | 19 | fuldt |
| [[S21]] | 31. maj 2021 (= **F21**) | 20 | fuldt |
| [[REExam-F21]] | re-eksamen aug. 2021 | 20 | fuldt |
| [[Final-Test]] | øve-eksamen | 11 | fuldt |
| [[E25-test-exam]] | E25 øve-eksamen (19. nov 2025) | 20 | fuldt (m. begrundelse) |
| [[Quizzer]] | uge-quizzer 2–12 + Midterm | ~60 | fuldt |
| [[F23-F24]] | 2023/2024 besvarelser | uddrag | ingen (kun konceptuelt) |

> [!tip] Start med den nyeste
> [[E25]] (dec 2025, kode 34721) er det **nyeste rigtige eksamenssæt** med officielt afkrydset facit — mest repræsentativt. Bemærk at løsnings-PDF'en lister det korrekte svar **øverst** (svar gives derfor ved indhold, ikke nummer; den rigtige eksamen randomiserer rækkefølgen). [[F25]] (forår 2025) er en studenterbesvarelse uden officielt facit — alle svar dér er **beregnet og MATLAB-verificeret**.

> [!note] Kursuskoder & dubletter (vigtigt at vide)
> - Kurset har skiftet kode: **31300 → 34721 → 34722** (samme fag, samme pensum). [[E15]]/[[E20]]/[[E21]] er 31300; [[E22]]/[[E23]]/[[E25]] er 34721.
> - **F21 = S21** — samme eksamen (31. maj 2021). Brug [[S21]].
> - **2022-sættets Q1–Q10 = [[F22]]**. "Exam Questionnaire"-delen (Q11–Q20) genbruges på tværs af sæt i varianter.
> - **[[E25]]-løsnings-PDF'en** lister korrekt svar **øverst** (forfatter-rækkefølge) → svar gives ved indhold, ikke nummer; den rigtige eksamen randomiserer.
> - **[[E23]]-facit** har forskudte svarnumre på Q13 og Q17 (template-artefakt) — følg mellemregningen, ikke "Answer no."-nummeret.
> - Kursusgangene genbruger endda **samme Bode-figur** i forskellige opgaver (fx phase-margin-opgaven).

---

## Mønster: opgavetype × sæt

Optælling af hvor mange spørgsmål hvert sæt bruger på hver type (T1–T13):

Primær opgavetype pr. spørgsmål, summeret over alle 11 sæt:

| Type | Emne | Gl. 5 sæt | Nye 6 sæt | **I alt** |
|---|---|:--:|:--:|:--:|
| **T4** | Steady-state / disturbance | 13 | 19 | **32** |
| **T10** | Lead / PI-Lead design | 16 | 14 | **30** |
| **T7** | Bode-aflæsning | 12 | 17 | **29** |
| **T8** | Nyquist / margins / stabilitet | 15 | 14 | **29** |
| **T9** | P / PI design | 8 | 17 | **25** |
| **T3** | Time response (2. orden) | 13 | 9 | **22** |
| **T2** | Block diagram reduction | 6 | 15 | **21** |
| **T1** | Transfer function / poler | 10 | 7 | **17** |
| **T5** | Modellering / linearisering | 0 | 6 | **6** |
| **T11** | State space | 3 | 2 | **5** |
| T6 | Root locus | 0 | 0 | **0** |
| T12 | Diskret / z-transform | 0 | 0 | **0** |

> *Gl. 5 sæt* = F22, S20, S21, REExam-F21, Final-Test. *Nye 6* = E15, E20, E21, E22, E23, E25. De gamle sæts "find $K$-range for stabilitet" (tidl. T5 Routh) er talt under **T8**; **T5** dækker nu modellering/linearisering, som 31300/34721-sættene tester eksplicit (elbil, kugle-på-flade, to-masse).

> [!success] Kerne-emnerne (de 6 + 2)
> **T4, T10, T7, T8, T3, T1** holder som kerne. Men de nyere 34721/31300-sæt **løfter to mere frem**: **T9 (P/PI-design)** og **T2 (blokdiagram-reduktion)** testes langt tungere end de gamle sæt antydede. Tilsammen er **T4, T10, T7, T8, T9, T3, T2, T1** ~90% af alle spørgsmål.

> [!fail] Spring (eller bare orienter dig)
> - **T6 Root locus** — 0 forekomster i alle 11 sæt.
> - **T12 z-transform / diskret** — 0 forekomster (kurset er kontinuert).
> - **T11 State space** — sjælden (5 lette spørgsmål, typisk bare "byg TF fra $\dot x = Ax+Bu$").
> - **T5 Modellering/linearisering** — kun i de ældre 31300/34721-sæt; lette hvis du kender opskriften.

---

## Det faste skelet i et MC-sæt

Sættene følger næsten samme rækkefølge. Genkend hvor du er:

1. **Blokdiagram-reduktion** (T2) — typisk Q1. → [[Blokdiagram-reduktion]]
2. **Modellering / linearisering / RC-RLC** (T1/T13) — Q1–Q2. → [[Transfer-functions-og-poler]]
3. **Time response, 2. orden** (T3) — vælg step-respons, find $\zeta$/$\omega_n$. → [[Time-response-2nd-order]]
4. **Bode-aflæsning** (T7) — match plot ↔ poler/nuller. → [[Bode-aflæsning]]
5. **P-design til phase margin** (T9) — find $K$ for PM. → [[Controller-design-P-PI-Lead]]
6. **DC-gain / steady-state error** (T4) — FVT, fejlkonstanter. → [[Steady-state-error-og-disturbance]]
7. **Poler fra diff.ligning** (T1) — Laplace → karakteristisk polynomium. → [[Transfer-functions-og-poler]]
8. **Stabilitet** (T5/T8) — Nyquist, gain margin, RHP-poler. → [[Stabilitet-Nyquist-margins]]
9. **Design-blok** (T10) — Lead/PI-Lead: find $\alpha$, $\tau_d$, $K_P$. → [[Controller-design-P-PI-Lead]]
10. **Disturbance / feed-forward / pre-filter** (T4/T13) — sensitivitet, $K_{ff}=1/G(0)$. → [[Steady-state-error-og-disturbance]]

---

## MC-strategi under eksamen

> [!tip] Distractor-fælderne (de forkerte svar er systematiske)
> De forkerte svarmuligheder repræsenterer **specifikke regnefejl**. Kender du fælderne, kan du ofte eliminere 3 muligheder:
>
> | Fælde | Sådan undgår du den |
> |---|---|
> | **dB vs. lineær** | $K=10^{\text{dB}/20}$. Læs om svaret skal være i dB eller ej (fx [[Final-Test]] Q6). |
> | **Reciprok** $1/K$ | Gain margin $=\frac{1}{\mid x \mid}$; controller-gain $K_P=\frac{1}{\mid GC \mid}$ — ikke omvendt. |
> | **Glemt at kvadrere** $\alpha$ | $\alpha=(1/(\omega_c\tau_d))^2$, og $M_D=1/\sqrt\alpha$. |
> | **Fortegn på gain margin** | $\mid G \mid$ over $0$ dB ved $\omega_{180}$ → negativ gain margin i dB ([[REExam-F21]] Q14). |
> | **Grader vs. radianer** | Tjek `sin` vs `sind` i fasebudgettet. |
> | **Take-off-punkt** | Flyttet take-off forbi en blok → del feedback med blokken ([[Blokdiagram-reduktion]]). |

> [!tip] Tidsallokering
> - **Hurtige point** (aflæsning/genkendelse): T2 blokdiagram, T3 step-respons-match, T1 poler fra ODE, T7 Bode-match. Tag dem først.
> - **Regnetunge** (brug MATLAB-skabelon): T9/T10 design ($K_P$, $\alpha$), T8 margins. Brug [[MATLAB-snydeark]].
> - Forkert svar koster ikke (typisk) → efterlad **aldrig** blankt.

> [!tip] MATLAB i eksamen
> Har du MATLAB til rådighed: byg $G$ med `tf`, og brug skabelonerne i [[MATLAB-snydeark]]. De fleste design-opgaver løses med `bode` + `evalfr` + `margin`. Husk `addpath` til hjælpefunktionerne.

---

## Genkendelses-træning (de 6 kerne-genkendelser)

> [!example] Lær at se opgavetypen på 5 sekunder
> - Ser du **et Bode-plot + "hvilke poler/nuller"** → T7, tæl hældninger og fase. [[Bode-aflæsning]]
> - Ser du **"find $K$ så PM = …"** → T9, find fase $=-180+$PM, $K=1/|G|$. [[Controller-design-P-PI-Lead]]
> - Ser du **"find $\alpha$ / $\tau_d$ / $K_P$" i PI-Lead** → T10, fasebudget. [[Controller-design-P-PI-Lead]]
> - Ser du **"steady-state error" / "DC-gain i dB"** → T4, FVT. [[Steady-state-error-og-disturbance]]
> - Ser du **et Nyquist-plot** → T8, tæl omkredsninger af $-1$ vs. RHP-poler. [[Stabilitet-Nyquist-margins]]
> - Ser du **en differentialligning** → T1, Laplace → rødder. [[Transfer-functions-og-poler]]

---

→ Snydeark: [[MATLAB-snydeark]]
→ Metoder: [[Blokdiagram-reduktion]] · [[Transfer-functions-og-poler]] · [[Time-response-2nd-order]] · [[Bode-aflæsning]] · [[Steady-state-error-og-disturbance]] · [[Stabilitet-Nyquist-margins]] · [[Controller-design-P-PI-Lead]]
→ Sæt: [[E25]] · [[E25-test-exam]] · [[E23]] · [[E22]] · [[E21]] · [[E20]] · [[E15]] · [[F25]] · [[F22]] · [[S20]] · [[S21]] · [[REExam-F21]] · [[Final-Test]] · [[Quizzer]] · [[F23-F24]]
