---
tags: [LCD, regulering, eksamen, handoff, session-notes]
type: handoff
formål: Overdragelse til ny session — LCD 34722 eksamensguides
---

# HANDOFF — LCD 34722 eksamensguides

> [!info] Til den nye session
> Dette dokument opsummerer en afsluttet session der byggede komplette eksamensguides til den skriftlige **multiple-choice**-eksamen i Reguleringsteknik (LCD 34722). Læs det + [[00_Eksamensanalyse_og_strategi]] for fuld kontekst. Alt arbejde ligger i `4. sem/LCD - 34722/OLD EXAMS/Eksamensguides/`.

---

## 0. OPDATERING (2026-05-29, fortsat) — 6 nye sæt tilføjet

> [!success] Nyt siden første session
> **6 nye per-sæt-guides** i `Sæt/`: [[E25]] (dec 2025, **nyeste rigtige eksamen**, kode 34721), [[E23]], [[E22]] (34721), [[E21]], [[E20]], [[E15]] (kode 31300). Kilder: `OLD EXAMS/Flere eksamenssæt/*.pdf`. Alle 20 spørgsmål hver, F22-format, svar-verificeret.
>
> **Kursuskode-lineage**: 31300 → 34721 → 34722 = samme fag. `F21.pdf` i mappen = allerede dækket som [[S21]].
>
> **[[00_Eksamensanalyse_og_strategi]] opdateret**: nu 11 sæt; mønster-tabel viser at **T9 (P/PI-design) og T2 (blokdiagram) er kerne-emner** (de nye sæt tester dem tungere end de gamle antydede).

> [!warning] VIGTIG erfaring: facit-NUMRE kan være forskudte
> Nogle facit-dokumenter (her **E23**, stale "2020"-template) lister svarmulighederne i en HELT anden rækkefølge end opgave-PDF'en. Det gav **14 forkerte svar-numre (af 20) i E23** — alle nu rettet via fuld content-verifikation (subagent + figur-rendering). Mange svar havde korrekt *indhold* men forkert *mulighed-nummer*. **Match ALTID MC-svar ved INDHOLD, ikke ved "Answer no. N"** — verificér mod teori ($e_{ss}=\frac{1}{1+K_0}$, $K_0=\lim_{s\to0}sL$, $\omega_d=2\pi/T$). [[E15]]/[[E20]]/[[E21]] er separat verificeret og er rene. [[E25]]-løsnings-PDF'en lister korrekt svar ØVERST (forfatter-rækkefølge) → svar angives ved indhold.

> [!success] Status: alt løst
> - E23 fuld-verifikation færdig: **14 af 20 svar-numre var forkerte** (facit-offset) — alle rettet + content-verificeret.
> - F25 Q4/Q17: **bekræftet fraværende** i .mlx-kilden (kan ikke skaffes).
> - E25 *test-exam* ([[E25-test-exam]], 20 spm.): bygget + uafhængigt verificeret (alle 20 korrekte; facit IKKE forskudt her).
> - **F25 Q15**: tilføjet manglende bro $e_{ss}=1-y_{ss}$ (stationær output vs. fejl) i guiden + i [[Steady-state-error-og-disturbance]] (brugeren kunne ikke koble guiden til metoden).
> - Bruger har visuelt bekræftet Obsidian-rendering. **Intet udestående.**

---

## 1. Opgaven (hvad brugeren bad om)

1. Rydde op i `OLD EXAMS/`-mappen (rod, duplikater).
2. Analysere opgavetype-mønster på tværs af gamle eksamenssæt (mistanke om gentagne typer — **bekræftet**).
3. Lave komplette løsningsguides til hvert sæt: korte forklaringer + copy-paste-klar MATLAB-kode til eksamenssituationen.

**Brugerpræferencer** (fra session): dansk + engelske fagtermer; hybrid-guider (emne-opskrifter + per-sæt gennemregning); udførligt niveau med distractor-analyse ("hvorfor er de forkerte MC-svar forkerte"); TikZ-figurer; MATLAB-verificeret kode; samlet snydeark.

---

## 2. Hvad er leveret (status: FÆRDIGT)

**Oprydning:** `OLD EXAMS/` 167 MB → 71 MB. Slettede bit-verificerede duplikater (`eksdok/`, `Eksamensdocs/`, 2 zips, root-mlx-kopi) + Simulink-cache + `.DS_Store`. ⚠️ Mappen er **untracked i git** — sletning var ikke reversibel, men kun verificerede kopier blev fjernet.

**18 guide-filer / ~3350 linjer / 80 MATLAB-blokke** i `Eksamensguides/`:

```
00_Eksamensanalyse_og_strategi.md   ← indgang: mønster + studieplan + distractor-fælder
MATLAB-snydeark.md                  ← copy-paste-skabeloner (path-robuste, inline-formler)
Metoder/  (7 emne-opskrifter, hver med TikZ + genbrugelig MATLAB-skabelon)
  Blokdiagram-reduktion · Transfer-functions-og-poler · Time-response-2nd-order
  Bode-aflæsning · Steady-state-error-og-disturbance · Stabilitet-Nyquist-margins
  Controller-design-P-PI-Lead
Sæt/  (per-sæt gennemregninger)
  F25 ⭐ (nyeste, MATLAB-beregnet) · F22 · S20 · S21 · REExam-F21 · Final-Test
  Quizzer (tematisk indeks) · F21 (pointer→S21) · F23-F24 (uddrag)
```

**Mønster-konklusion:** 6 emner = ~85 % af eksamen: **T7** Bode, **T8** Nyquist/margins, **T10** Lead/PI-Lead, **T4** steady-state/disturbance, **T3** time-response, **T1** transfer functions. Testes **næsten aldrig**: T6 root locus, T11 state space, T12 z-transform.

**Sæt-relationer (vigtigt — undgå at duplikere):**
- **F21 = S21** (samme eksamen, 31. maj 2021).
- **2022-sættets Q1–Q10 = F22**.
- "Exam Questionnaire" (Q11–Q20) genbruges på tværs af sæt i varianter.
- F25/F23/F24 er **studerendes besvarelser** (intet officielt facit).

---

## 3. Tekniske erfaringer (LÆS — sparer tid + fejl)

> [!warning] TikZJax i denne vault
> Diagram-skill'en `/tikz-block-diagram` siger fejlagtigt "ingen `\usepackage{tikz}`". **Det er forkert her.** De fungerende noter (Lec 6, 7, 13) bruger ALLE `\usepackage{tikz}`. Korrekt header:
> ```
> \usepackage{tikz}
> \usetikzlibrary{arrows.meta, positioning, calc}
> \begin{document}
> ```
> De rigtige silent-fail-syndere er: **`thick`-option**, `\dfrac` i node-labels, custom color-styles, line breaks (`\\`) i labels. Match [[Lec 7 - Crossover Freq & Nyquist]] 1:1. (Memory `feedback_tikzjax_requirements` er nu rettet.)

> [!warning] MATLAB-verifikation er ikke valgfri
> Facit-PDF'erne er OCR'ede og fulde af trykfejl. Verifikation fangede bl.a.: F22 Q6 `(s+2.1)` ikke `(s+21)`; F22 Q19 `α=0.01` ikke `0.001`; REExam Q10/Q20; S21/F21 Q9 overshoot-formel. **Kør altid hver kodeblok før den skrives ind.** Brug `project_path` = `.../OLD EXAMS/Matlab scripts` (hjælpefunktionerne ligger der).

> [!warning] Path-robusthed
> `addpath('OLD EXAMS/Matlab scripts')` (relativ) KNÆKKER afhængigt af working dir. Brug **inline-formler** i guiderne (gjort) — de er path-uafhængige. Hjælpefunktionerne (`overshoot2damping` osv.) er kun en bekvemmelighed.

> [!warning] .mlx og .mw formater
> - **.mlx** (MATLAB Live Script) = zip. `unzip -p fil.mlx matlab/document.xml` giver tekst/kode. **MEN** F25.mlx havde **0 kode-celler** — alt indhold lå i `media/*.png` (60 billeder med spørgsmål+svarmuligheder). Tjek ALTID billederne hvis teksten er tom. Pak ud, `sips -Z 1500` (undgå image-crash), læs ÉT ad gangen, helst via subagent (isoleret kontekst).
> - **.mw** (Maple) = XML, men matematikken er **base64-kodet MathML** (ulæselig). Kun `<Text-field>`-forklaringer kan udtrækkes.

> [!tip] Effektiv arbejdsmetode brugt
> PDF/billed-udtræk parallelliseret via general-purpose subagenter (isoleret kontekst → undgår image-crash i hovedsession). MATLAB-verifikation + skrivning gjort i hovedsession (kvalitetskontrol). note-review-agent kørt på de færdige opskrifter (fangede RHP-zero-fase, Nyquist-fortegn, PI-Lead-varianter).

---

## 4. Kendte forbehold (ikke-løste)

- **F25 Q4 + Q17**: svarmulighederne er **bekræftet fraværende i .mlx-kilden** (kun spørgsmål + figur er gemt — verificeret via medie-udtræk). Q4: `G=K/(s(s+3))`. Q17: P-Lead-Lag, β≈1.54 (MATLAB-bekræftet). Kan kun skaffes hvis den officielle F25-opgave-PDF dukker op.
- **F25 Q14**: beregnet `Kp=12` (fra DC=−2.5 dB→G0=0.75) matcher ingen svarmulighed; nærmest (d) 22.5 hvis DC reelt er −7.96 dB. Aflæsningsusikkerhed — metoden er korrekt.
- **F25 Q19**: feed-forward med RHP-nuller — argumenteret for (c) `1/G(0)`, men ikke 100 % sikkert uden facit (markeret `[!todo]` i guiden).
- **F23**: kun konceptuelle forklaringer (base64-matematik); F24 for sparsom — begge i `F23-F24.md`.
- **Sæt-specifikke blokdiagrammer**: ikke gengivet som TikZ (kun generiske figurer i opskrifterne) — bevidst valg (risiko > værdi for komplekse diagrammer; opgaverne har dem i PDF).

---

## 5. TODOs / mulige næste skridt

> [!done] Afklaret (luk ikke op igen)
> - ~~Bruger-verifikation i Obsidian~~ — brugeren har **visuelt bekræftet alt** (TikZ + wiki-links renderer korrekt).
> - ~~F25 Q4/Q17 svarmuligheder~~ — **bekræftet fraværende** i .mlx-kilden (kan ikke skaffes derfra; se §4).
> - ~~E25 test-exam~~ — bygget ([[E25-test-exam]]) + uafhængigt verificeret.

Kun **valgfrit** fremtidigt arbejde tilbage:
- [ ] **Quizzer**: pt. kun tematisk indeks ([[Quizzer]]). Kan udbygges til fuld gennemgang af enkelte quizzer (Quiz Sol/*.pdf) hvis ønsket.
- [ ] **Eksamenstræning**: kør de fuldt-løste sæt under tidspres; juster guiderne hvis noget er uklart i praksis.
- [ ] Evt. flere års sæt hvis brugeren skaffer dem.

---

## 6. Hurtig orientering for ny session

- **Indgang:** [[00_Eksamensanalyse_og_strategi]] (mønster + studieplan).
- **Kildemateriale:** `OLD EXAMS/Eksamensopgaver/*.pdf` (officielle sæt m. facit), `OLD EXAMS/eksamen/Quiz Sol/*.pdf`, `OLD EXAMS/*.mlx`/`*.mw` (besvarelser).
- **Genbrugskode:** `OLD EXAMS/Matlab scripts/*.m`.
- **Teori at linke til:** `Lecture Notes/Lec 1–13`.
- **MATLAB-MCP:** R2025b m. Control System + Symbolic Math Toolbox — brug `project_path` = `.../OLD EXAMS/Matlab scripts`.
- **Format-regler:** se vault `CLAUDE.md` + `LCD/CLAUDE.md` (dansk+engelsk, `$$..$$`, `\boxed{}`, Code Styler `hl:`, callouts, wiki-links uden backticks).
- **Session-log:** håndteres nu via `/session-end` (kursus-lokal `CURRENT_TASK.md` ved siden af `LCD/CLAUDE.md`); ældre historik ligger i vault-roden `SESSION_ARKIV.md`.

> [!success] Bundlinje
> Guiderne er komplette og MATLAB-verificerede. Den primære udestående handling er **brugerens visuelle verifikation i Obsidian** (TikZ-rendering). Alt andet er klar til eksamenslæsning.
