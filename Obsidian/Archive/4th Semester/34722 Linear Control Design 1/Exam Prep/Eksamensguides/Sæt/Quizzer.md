---
tags: [LCD, regulering, eksamen, quizzer, loesningsguide, indeks]
kilde: "eksamen/Quiz Sol/*.pdf + Quiz Combined Linear 34721.pdf"
format: Multiple choice øvelsesquizzer (Quiz 2–12 + Midterm)
---

# Quizzer — tematisk indeks (MC-træning)

> [!info] Om quizzerne
> Kursets ugentlige multiple-choice-quizzer (Quiz 2–12 + Midterm) med fulde løsninger i `eksamen/Quiz Sol/`. De er den bedste **MC-træning**, fordi formatet er identisk med eksamen. Alle opgavetyper er gennemregnet med tal i eksamenssæt-guiderne; denne fil kobler hver quiz til den rette metode-opskrift, så du kan øve målrettet.

> [!tip] Det quizzerne træner ekstra
> Quizzerne dækker **modellering, linearisering, disturbance og pre-filter/feed-forward** (T13/T4) tungere end de gamle eksamenssæt. Bruger du kun eksamenssættene, så tag især **Quiz 5, 10, 11, 12** for disse emner.

## Quiz → emne → opskrift

| Quiz | Hovedemner | Øv med opskrift |
|---|---|---|
| **Quiz 2** | Motor-TF, gear-forhold, Ziegler-Nichols, closed-loop | [[Transfer-functions-og-poler]] · [[Blokdiagram-reduktion]] |
| **Quiz 3** | TF fra diff.ligning, step-respons, closed-loop, gain ved frekvens | [[Transfer-functions-og-poler]] · [[Time-response-2nd-order]] · [[Bode-aflæsning]] |
| **Quiz 4** | Poler/nuller fra nævner, vælg $G(s)$ fra DC+pol/nul, magnitude ved frekvens | [[Transfer-functions-og-poler]] · [[Bode-aflæsning]] |
| **Quiz 5** | **Linearisering**: elbil, kugle på flade, to-masse-system | [[Transfer-functions-og-poler]] (linearisering) · Teori: [[Lec 5 — Black-box Modelling og Linearisering]] |
| **Quiz 6** | Crossover-definition, Routh-stabilitetsrange for $K$, Bode→TF, Nyquist-margins | [[Stabilitet-Nyquist-margins]] · [[Bode-aflæsning]] |
| **Quiz 8** | Nyquist (static gain, max fase), P-tuning til PM, Lead $\alpha$, PI-Lead crossover | [[Controller-design-P-PI-Lead]] · [[Stabilitet-Nyquist-margins]] |
| **Quiz 9** (12 spm) | Closed-loop step, type-1 (0 fejl), P-Lead crossover, bandbredde, PM, disturbance | [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]] · [[Steady-state-error-og-disturbance]] |
| **Quiz 10** | Integrator-**windup**, RHP-poler → ustabil, komplekse poler, Nyquist+P | [[Stabilitet-Nyquist-margins]] · [[Transfer-functions-og-poler]] |
| **Quiz 11** | **Disturbance rejection**: hvilken forstyrrelse giver stat. fejl, error-TF, resonans | [[Steady-state-error-og-disturbance]] |
| **Quiz 12** | **Pre-filter** (overshoot), **feed-forward** $K_{ff}=1/G(0)$, disturbance feed-forward | [[Steady-state-error-og-disturbance]] · Teori: [[Lec 13 — Feed-forward Control]] |
| **Midterm** | Blokdiagram, fase ved frekvens, FVT, 1.-ordens, integrator, Bode-stabilitet, pol/nul-kort, Nyquist | [[Blokdiagram-reduktion]] · [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] |

## Tilbagevendende MC-spørgsmålstyper (samme som eksamen)

> [!example] Disse mønstre går igen — øv genkendelse
> - **"Find $K_{ff}$ til feed-forward"** → $K_{ff}=1/G(0)$ (Quiz 12). Se [[Steady-state-error-og-disturbance]].
> - **"Hvilken forstyrrelse giver stationær fejl?"** → den der rammer *efter* en integrator undertrykkes; *før* en P-only-loop giver rest (Quiz 11).
> - **"Find $\alpha$ for Lead"** → $\alpha=\frac{1-\sin\phi_m}{1+\sin\phi_m}$ (Quiz 8). Se [[Controller-design-P-PI-Lead]].
> - **"Stabilitetsrange for $K$"** → find $\omega$ hvor fase $=-180°$, $\bar K=1/|G(j\omega_{180})|$ (Quiz 6). Se [[Stabilitet-Nyquist-margins]].
> - **"Integrator-windup"** → begræns I-delen ved aktuator-mætning (Quiz 10). Teori: [[Lec 11 — Begrænsede Systemer]].

## Sådan bruger du quizzerne til eksamen

1. Tag en quiz **uden** løsning først (find dem i `Quiz Sol/` — dæk facit til).
2. For hvert forkert svar: slå op i den koblede opskrift ovenfor.
3. Genkend hvilken **T-type** spørgsmålet er → brug den tilhørende MATLAB-skabelon fra [[MATLAB-snydeark]].
4. De fuldt gennemregnede taleksempler ligger i eksamenssæt-guiderne: [[F22]], [[S20]], [[S21]], [[REExam-F21]], [[Final-Test]].

→ Metoder: [[Controller-design-P-PI-Lead]] · [[Bode-aflæsning]] · [[Stabilitet-Nyquist-margins]] · [[Steady-state-error-og-disturbance]] · [[Time-response-2nd-order]] · [[Transfer-functions-og-poler]] · [[Blokdiagram-reduktion]]
→ Snydeark: [[MATLAB-snydeark]] | Oversigt: [[00_Eksamensanalyse_og_strategi]]
