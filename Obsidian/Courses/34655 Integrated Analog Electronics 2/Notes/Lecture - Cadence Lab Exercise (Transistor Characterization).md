---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: lecture-note
lecture: "Introduction to Computer Exercise"
source: "34655-cadence-lab-exercise-XT018_v1.pdf, 34655-cadence-tutorial-XT018_v3.pdf"
instructor: "Per Lynggaard"
tags: [IAE2, cadence, transistor-characterization, opamp, simulation, XFAB, XT018]
---
# Cadence Lab Exercise - Transistor Characterization & OpAmp Design

**Instructor:** Per Lynggaard
**Process:** XFAB XT018 (0.18 $\mu$m)

> [!abstract] Lecture Overview
> This lecture introduces the Cadence Virtuoso computer exercise spanning 3 lab days. **Day 1** covers getting started with Cadence and characterizing NMOS/PMOS transistors using the Schichmans-Hodges (SH) model. **Day 2-3** covers designing a two-stage Miller-compensated OpAmp to meet given specifications.

---

## Kursuskalender & Deadlines

| Uge | Aktivitet |
|-----|-----------|
| **Uge 8** (Lecture 3) | 4 timer til OpAmp paper design (teori) |
| **Uge 9** | **Rapport aflevering** (DTU Learn, senest 23:59) |
| **Uge 11** (Lecture 6) | Cadence: transistor-karakterisering |
| **Uge 12+13** (Lecture 7+8) | Cadence: OpAmp design & verifikation |
| **Uge 15** | **Poster aflevering** (DTU Learn, senest 23:59) |

> [!warning] Vigtige krav
> - Rapport-aflevering er **obligatorisk** for at kunne aflevere poster
> - Rapport: max 10 sider, grupper af 2-3 studerende
> - Angiv hvem der har bidraget med hvad

---

## Rapportering

### Rapport (paper design)
- Teori og initialt design ($W/L$ for alle transistorer)
- Beregninger med **teoretiske** $\mu C_{ox}$ og $V_t$ (0.18 $\mu$m fra Carusone)
- Design-overvejelser og beslutninger

### Poster (efter simulering)
- Simuleringsresultater
- Beregninger med **ekstraherede** $\mu C_{ox}$ og $V_t$ (fra Cadence)
- Korrelation mellem forventede og simulerede resultater
- Optimeringsovervejelser og endelig performance
- Kredsløbsdiagrammer, tabeller, verificerede ligninger (tjek enheder)

---

## Day 1: Cadence Basics & Transistor-karakterisering

### Oversigt over flow

```
Day 1                              Day 2 & 3
├─ Cadence introduktion            ├─ Byg OpAmp inkl. bias
├─ Library Manager                 ├─ Komplekse skemaer
├─ Opret celler                    ├─ Symboler & hierarki
├─ Opret skemaer                   ├─ AC simulering
├─ DC simulering                   └─ Transient simulering
└─ Karakterisér NMOS & PMOS
   → Passer SH-modellen?              → Korrelér teori & sim
                                       → Optimér til spec
```

---

### Schichmans-Hodges modellen

> [!question] Hvilke parametre karakteriserer en transistor?
> De tre nøgleparametre i SH-modellen:
> - $\mu C_{ox}$ (procesparameter - mobility * oxide capacitance)
> - $V_t$ (threshold voltage)
> - $\lambda$ (channel-length modulation)

#### Drain-strøm i mætning (Carusone eq. 1.84)

$$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_t)^2 \left(1 + \lambda(V_{DS} - V_{\text{eff}})\right)$$

---

### Metode: Finde $\mu C_{ox}$ og $V_t$

**Setup:** Diode-koblet transistor (gate og drain forbundet), sweep $V_{GS}$.

Når $V_{DS} = V_{GS}$ og $\lambda V_t \ll 1$:

$$I_D \approx \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_t)^2$$

**Procedure:**
1. Tag kvadratroden af $I_D$:

$$\sqrt{I_D} = \sqrt{\frac{1}{2} \mu C_{ox} \frac{W}{L}} \cdot V_{GS} - \sqrt{\frac{1}{2} \mu C_{ox} \frac{W}{L}} \cdot V_t$$

2. Dette er en ret linje ($y = ax + b$) i $\sqrt{I_D}$ vs $V_{GS}$
3. **Hældningen** giver $\mu C_{ox}$ (da $W/L$ er kendt)
4. **x-akseafskæring** (eller beregning fra et punkt) giver $V_t$

---

### Metode: Finde $\lambda$ (eller $V_A$)

**Setup:** Fast $V_{GS}$, sweep $V_{DS}$.

For transistor i mætning:

$$\alpha = \frac{\partial I_D}{\partial V_{DS}} = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} V_{\text{eff}}^2 \cdot \lambda$$

**Procedure:**
1. Plot $I_D$ vs $V_{DS}$ og find hældningen $\alpha$ i mætningsområdet ($V_{DS} \geq V_{GS}$)
2. Beregn $\lambda$ fra den kendte hældning og $\mu C_{ox}$, $V_{\text{eff}}$

---

### TASK 1: DC simulering NMOS (diode-koblet)

**Kredsløb:** NMOS "ne" fra PRIMLIB, gate-drain forbundet, $V_{GS}$ kilde fra analogLib.

| W/L | $V_{GS}$ [V] | $I_D$ [$\mu$A] |
|-----|-------------|-----------------|
| 5u/1u | 0.8 | |
| 5u/1u | 1.0 | |
| 5u/5u | 0.8 | |
| 5u/5u | 1.0 | |

> [!tip] Tjek
> Afhænger $I_D$ af $V_{GS}$ som forventet? Hvis ej, hvorfor?

---

### TASK 2: SH-model NMOS - Ekstraktion af $\mu_n C_{ox}$ og $V_{tn}$

- Sweep $V_{GS}$ fra 0V til max (1.8V)
- Plot $I_D$ vs $V_{GS}$ og $\sqrt{I_D}$ vs $V_{GS}$
- Find hældning ved 0.8V og 1.0V

| $W/L$ | $V_{GS}$ [V] | Slope | $\mu_n C_{ox}$ [$\mu$A/V$^2$] | $V_{tn}$ [V] |
|-------|-------------|-------|-------------------------------|-------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | |
| | 1.0 | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | |
| | 1.0 | | | |

---

### TASK 3: Transkonduktans $g_m$ for NMOS

- Samme diode-setup, fire simuleringer
- Find $I_D$, $g_m$, $V_{th}$ fra DC operating point
- Beregn $g_m$ via:
  - $g_m = \sqrt{2 \mu_n C_{ox} (W/L) I_D}$
  - $g_m = 2 I_D / V_{\text{eff}}$
- Kommenter forskelle

| $W/L$ | $V_{GS}$ [V] | $I_D$ [$\mu$A] | $g_m$ OP [$\mu$A/V] | $g_m$ calc [$\mu$A/V] | $g_m$ $2I_D/V_{\text{eff}}$ |
|-------|-------------|-----------------|---------------------|----------------------|---------------------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | | |
| | 1.0 | | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | | |
| | 1.0 | | | | |

---

### TASK 4: Udgangskarakteristik NMOS - Finde $\lambda$ og $g_{ds}$

**Nyt kredsløb:** Separat $V_{DS}$ og $V_{GS}$ kilde, sweep $V_{DS}$ 0-1.8V.

| W/L | $V_{GS}$ [V] | $V_{DS}$ [V] | Slope | $\lambda$ [V$^{-1}$] | $g_{ds}$ calc [$\mu$S] | $g_{ds}$ OP [$\mu$S] |
|-----|-------------|-------------|-------|---------------------|----------------------|---------------------|
| 5$\mu$m/1$\mu$m | 0.8 | | | | | |
| | 1.2 | | | | | |
| 5$\mu$m/5$\mu$m | 0.8 | | | | | |
| | 1.2 | | | | | |

---

### TASK 5-8: Gentag for PMOS

> [!warning] PMOS-specifikke ting
> - Transistor: **"pe"** fra PRIMLIB
> - Source og bulk forbindes til **højeste potentiale** ($V_{DD}$)
> - $V_{GS}$ skal være **negativ**
> - Strømme i Cadence er defineret positive **ind i** terminalen

Samme tabeller som NMOS, men brug $|V_{GS}|$.

---

## Day 2 & 3: OpAmp Design

### Specifikationer (non-inverting amplifier konfiguration)

| Parameter | Krav |
|-----------|------|
| Forstærkning (midband) | $V_{out}/V_{in} = 2$ |
| Closed-loop båndbredde | $\omega_t = 2\pi \cdot 20 \times 10^6$ s$^{-1}$ |
| Slew-rate | SR $\geq$ 30 V/$\mu$s |
| Phase margin | PM $\geq$ 70$^\circ$ |
| Forsyningsspænding | 1.8V |

**Feedback-kredsløb:** $C_1 = C_2 = 1$ pF, $R_1 = 10^9 \Omega$, $C_L = 1.5$ pF

### Procesparametre til paper design

| Parameter | Værdi |
|-----------|-------|
| $\mu_p C_{ox}$ | 35 $\mu$A/V$^2$ |
| $\mu_n C_{ox}$ | 165 $\mu$A/V$^2$ |
| $V_{tp}$ | 630 mV |
| $V_{tn}$ | 630 mV |

---

### OpAmp Topologi: Two-stage Miller-compensated

```
                                    V_DD
                                     |
                    Q8 ──┬── Q5 ──┬── Q6
                         |        |        |
             Vin- ──┤ Q1    Q2 ├── Vin+   Vout
                         |   Cc   |        |
          I_BIAS ──( )── Q3 ──┬── Q4       Q7
                              |            |
                             V_SS         V_SS
```

**Bias-blok** og **OpAmp** designes som separate hierarkiske celler med symboler.

---

### Simuleringsflow for OpAmp

#### 1. Open-loop test bench
- Indsæt OpAmp + bias blok
- Tilføj feedback-kredsløb (uden at forbinde til "-" terminal)
- DC sweep "+" input for at finde $V_{DD}/2$ ved output
- Brug denne spænding som DC bias, sæt AC magnitude = 1V

#### 2. AC simulering (open-loop)
- Plot magnitude og fase
- Find: **DC gain**, **3dB frekvens**, **unity-gain frekvens**, **phase margin**
- Matcher resultaterne forventningerne?

#### 3. Transient simulering (slew-rate, closed-loop)
- Closed-loop konfiguration med vpulse input
- Amplitude: rail-to-rail swing ved output
- Rise/fall tider: tilstrækkeligt små
- Matcher SR med forventning?
- Prøv at ændre $C_L$ med faktor 10

#### 4. Optimering
- Hvis spec ikke opfyldes: juster transistor-dimensioner
- Brug teori (GBW, SR, PM udtryk) til at guide ændringer
- Brug operating point til at ekstrahere og justere småsignal-parametre

---

## Cadence Quick Reference

### Vigtige biblioteker

| Bibliotek | Indhold |
|-----------|---------|
| **analogLib** | Ideelle komponenter (vdc, idc, gnd, res, cap, vsin, vpulse, vcvs, vccs) |
| **PRIMLIB** | XFAB XT018 proceskomponenter (ne, pe, cmm3, rpp1k1) |

### PRIMLIB komponenter

| Komponent | Type | Parametre |
|-----------|------|-----------|
| **ne** | NMOS transistor | W, L, nf (fingers) |
| **pe** | PMOS transistor | W, L, nf (fingers) |
| **cmm3** | Kapacitor | W, L, Multiplicity |
| **rpp1k1** | Modstand | W, L, Multiplicity |

### Vigtige genveje i Schematic Editor

| Genvej | Funktion |
|--------|----------|
| `i` | Insert instance (komponent) |
| `w` | Wire (forbind) |
| `l` (lille L) | Wire name/label |
| `p` | Add pin |
| `q` | Edit properties |
| `Shift-m` | Move component |
| `F3` | Stretch/rotate/flip |
| `s` | Snap wire til terminal |
| `Shift-e` | Descent edit (hierarki ned) |
| `e` | Descent read (hierarki ned, read-only) |
| `Ctrl-e` | Return (hierarki op) |

### Simulation setup (ADE Explorer / Maestro)

1. **Start:** Launch -> ADE Explorer -> Create New View -> maestro
2. **Tilføj analyse:** Expand Tests -> Analyses -> double-click "Click to add analysis"
3. **DC:** Tick "dc", enable "Save DC Operating Point", vælg sweep variable
4. **AC:** Tick "ac", tick "Frequency", sæt start/stop, sweep type = Automatic
5. **Transient:** Tick "tran", sæt stop time, accuracy = Conservative

### Output-typer i expression builder

| Funktion | Brug |
|----------|------|
| **VT/IT** | Transient signaler |
| **VF/IF** | AC signaler |
| **VDC/IDC** | DC signaler |
| **VS/IS** | DC sweep |

### Design Variables
- Sæt komponentværdi til et variabelnavn i skemaet
- I Maestro: højreklik Design Variables -> "Copy from Cellview"
- Kan swepes via "From/To" parameterisering

---

## Forberedelsestjekliste

- [ ] Gennemgå Cadence Tutorial inden lab
- [ ] Forstå SH-modellen og parameter-ekstraktion ($\mu C_{ox}$, $V_t$, $\lambda$)
- [ ] Hav paper design klar med $W/L$ for alle transistorer
- [ ] Kend OpAmp-specifikationerne og relevante formler
- [ ] Forstå kredsløbet: two-stage Miller-compensated OTA med feedback
