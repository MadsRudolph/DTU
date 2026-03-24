# Cadence Guide - 34655 IAE2

Samlet guide til at forbinde til og bruge Cadence Virtuoso via ThinLinc til XFAB XT018 0.18um processen.

---

## 1. Forbindelse til Cadence-serveren

### Fra DTU campus (on-site)

1. Start **ThinLinc** klienten (download fra [cendio.com](http://www.cendio.com))
2. Indtast forbindelsesoplysninger:
   - **Server:** `alba.elektro.dtu.dk`
   - **Username:** dit tildelte brugernavn (f.eks. `icuser1`)
   - **Password:** dit tildelte password
3. Klik **Connect**
4. I ThinLinc Profile Chooser, klik **Start**
5. Du er nu på et Linux desktop

### Fra hjemmet (off-campus)

Du skal bruge VPN for at tilgå serveren udenfor DTU:

1. Download **Cisco AnyConnect** fra [net.ait.dtu.dk/vpn/](https://net.ait.dtu.dk/vpn/)
2. Start Cisco AnyConnect og forbind til `vpn.dtu.dk`
3. Log ind med dine DTU initialer og password (MFA krav)
4. Herefter kan du forbinde via ThinLinc som beskrevet ovenfor

### Skift password

I terminalen: kør `passwd` og følg instruktionerne. Password vises ikke mens du skriver.

### Vigtigt at vide

- **F8** skifter til dit Windows PC desktop (ThinLinc kører i fullscreen)
- Du kan lukke ThinLinc-vinduet med krydset - din Cadence session kører videre i baggrunden
- Når du er **helt færdig**, brug desktop-menuen og vælg **Log Out**

---

## 2. Start Cadence

1. Højreklik på desktop og vælg **Open Terminal**
2. Kør kommandoen:
   ```
   icload
   ```
3. To vinduer åbner:
   - **Library Manager** - filhåndtering af libraries, cells og views
   - **CIW** (Command Interface Window) - log vindue med status og fejlmeddelelser

---

## 3. Library Manager

Library Manager håndterer al filstruktur i Cadence. Al filhåndtering **skal** gøres herfra.

### Struktur

| Niveau | Beskrivelse |
|--------|-------------|
| **Library** | Mappe der indeholder cells |
| **Cell** | En komponent/design |
| **View** | Repræsentation af en cell (schematic, symbol, etc.) |

### Pre-definerede libraries

- **analogLib** - Ideelle komponenter (vdc, res, cap, etc.)
- **PRIMLIB** - Faktiske XFAB XT018 proceskomponenter (MOS, C, R)

### Opret nyt library

1. **File** -> **New** -> **Library**
2. Giv library et navn
3. Vælg **Attach to an existing technology library**
4. Vælg **TECH_XT018**
5. Klik **OK**

---

## 4. Schematic Editor

### Opret ny schematic

1. Vælg dit library i Library Manager
2. **File** -> **New** -> **Cell View...**
3. Indtast cell name, sæt View/Type til **schematic**
4. En tom Schematic Editor åbner

### Indsæt komponent

- **Create** -> **Instance** (genvej: `i`)
- Angiv Library, Cell og View (skal være `symbol`)
- Klik i editoren for at placere komponenten

### Vigtige analogLib komponenter

| Komponent | Type | Vigtige parametre |
|-----------|------|-------------------|
| `vdc` | DC spændingskilde | DC voltage, AC magnitude |
| `idc` | DC strømkilde | DC voltage, AC magnitude |
| `gnd` | Stel (ground) | Skal altid være i schematic |
| `res` | Ideel modstand | Resistance |
| `cap` | Ideel kondensator | Capacitance |
| `ind` | Ideel spole | Inductance |
| `vcvs` | Spændingsstyret spændingskilde | Voltage gain |
| `vccs` | Spændingsstyret strømkilde | Transconductance |
| `vpulse` | Firkantbølge (spænding) | V1, V2, Period, Rise/Fall, Delay |
| `vsin` | Sinusbølge (spænding) | Amplitude, Frequency, DC voltage |
| `vpwl` | Piecewise linear (spænding) | Time/Voltage pairs |

### Vigtige PRIMLIB komponenter (XFAB XT018)

| Komponent | Type | Parametre |
|-----------|------|-----------|
| `ne` | NMOS transistor | W, L, antal fingre |
| `pe` | PMOS transistor | W, L, antal fingre |
| `cmm3` | Kondensator | W, L, Multiplicity |
| `rpp1k1` | Modstand | W, L, Multiplicity |

### Forbind komponenter med wires

- **Create** -> **Wire (narrow)** (genvej: `w`)
- Tryk `s` nær en terminal for at snappe til den

### Tilføj labels til wires

- **Create** -> **Wire Name...** (genvej: `l`)
- Skriv navne i Names-feltet (f.eks. `vin vout`)
- Klik på wires for at placere labels

### Rediger komponent-properties

- Klik på komponenten for at vælge den
- **Edit** -> **Properties** -> **Objects** (genvej: `q`)
- Ændr parametre i vinduet

### Flyt, roter og flip

- **Flyt:** Edit -> Move (genvej: `Shift+M`)
- **Roter/Flip:** Tryk `F3` mens du flytter, vælg Rotate/Sideways/Upside Down

---

## 5. Pins og Symbols (Hierarki)

### Tilføj pins

- **Create** -> **Pin** (genvej: `p`)
- Sæt **Direction** korrekt:
  - `input` for indgange
  - `output` for udgange
  - `inputOutput` for forsyninger (VDD, VSS)

### Opret symbol fra schematic

1. I Schematic Editor: **Create** -> **Cellview** -> **From Cellview...**
2. Klik **OK**
3. Arrangér pins i Symbol Generation Options:
   - **Left Pins:** inputs
   - **Right Pins:** outputs
   - **Top Pins:** VDD (højeste forsyning)
   - **Bottom Pins:** VSS (laveste forsyning)
4. Klik **OK** - Symbol Editor åbner
5. Check and Save, luk vinduet

### Navigér i hierarki

- **Ned:** Vælg en blok, **Edit** -> **Hierarchy** -> **Descent Edit** (`Shift+E`) eller **Descent Read** (`E`)
- **Op:** **Edit** -> **Hierarchy** -> **Return** (`Ctrl+E`)

---

## 6. Gode vaner for schematics

- Giv plads mellem komponenter, så parametre kan læses
- Forsyning (VDD) i toppen, ground (VSS) i bunden
- Inputs til venstre, outputs til højre
- Brug labels på alle vigtige nets
- Forbind **ikke** via label-navne (brug faktiske wires)
- Opdel komplekse designs i hierarki med cells og symbols

### Test bench best practice

- Placer alt design i cells med symbols
- Kun ideelle kilder og eksterne komponenter på top-level
- Label alle vigtige wires

---

## 7. Simulering (ADE Explorer / Maestro)

### Start simuleringsmiljø

1. I Schematic Editor: **Launch** -> **ADE Explorer**
2. Vælg **Create New View**
3. Sæt View til **maestro**, klik **OK**
4. Maestro åbner med et træ i venstre side

### Opsæt analyse

1. Udvid **Tests** -> dit projekt -> **Analyses**
2. Dobbeltklik på **Click to add analysis**
3. Vælg analysetype i vinduet

### DC Simulation

- Vælg **dc**
- Aktiver **Save DC Operating Point** (gemmer alle DC spændinger og strømme)
- Valgfrit: Sweep en komponent-parameter:
  - Tick **Component Parameter** -> **Select Component** -> klik i schematic
  - Vælg parameter at sweepe (f.eks. `dc`)
  - Sæt Sweep Range og vælg **Automatic** som Sweep Type

### AC Simulation

- Vælg **ac**
- Tick **Frequency** som sweep variable
- Angiv start- og stopfrekvens
- Sweep Type: **Automatic**

### Transient Simulation

- Vælg **tran**
- Angiv **Stop Time**
- Accuracy: vælg **Conservative** for højeste præcision
- Tick **Enabled**

### Design Variables

- Brug variabler i stedet for faste værdier i component properties
- I Maestro: Højreklik **Design Variables** -> **Copy from Cellview**
- Klik de tre prikker for at sweepe en variabel (**From/To**)

---

## 8. Outputs og resultater

### Opsæt outputs

Gå til **Outputs Setup** fanen i Maestro.

#### Signal-metode (simpel)

1. Klik probe-ikonet for at tilføje output
2. Sæt Type til **signal**
3. Dobbeltklik **Details**, klik de tre prikker
4. Vælg signalet i schematic editoren
5. Signalet vises under Details
6. Sørg for at **Plot** er afkrydset

#### Expr-metode (avanceret)

1. Sæt Type til **expr**
2. Dobbeltklik **Details** for at åbne expression builder
3. Vælg signaltype:
   - **VT/IT** - transient signaler
   - **VF/IF** - AC signaler
   - **VDC/IDC** - DC signaler
   - **VS/IS** - DC sweep
4. Vælg signal fra schematic
5. Tryk flueben for at bekræfte
6. Sørg for at **Plot** er afkrydset

Navngivne outputs kan refereres i andre expressions (f.eks. `sqrt(Drain_current)`).

---

## 9. Calculator

- Åbn via **Tools** -> **Calculator...** i Maestro eller plotvinduet
- Vælg signaltype (vt, vdc, etc.) og klik på signal i schematic
- Signalet vises i calculatoren
- Klik på matematiske funktioner for at bearbejde signalet
- Tryk **Enter** for at skubbe expression til stack
- Drag-and-drop fra stack til expression builder i Outputs Setup

---

## 10. Download filer fra serveren

Brug et SFTP-program som **FileZilla**:

- **Host:** `alba.elektro.dtu.dk`
- **Username:** dit brugernavn
- **Port:** `22`
- Dine filer ligger under `/home/<username>/cds/`

---

## 11. Keyboard genveje (oversigt)

| Genvej | Funktion |
|--------|----------|
| `i` | Indsæt komponent (Instance) |
| `w` | Tegn wire |
| `l` | Tilføj wire label |
| `p` | Tilføj pin |
| `q` | Rediger properties |
| `Shift+M` | Flyt komponent |
| `F3` | Stretch/Rotate/Flip options |
| `s` | Snap til terminal |
| `Shift+E` | Descent Edit (ned i hierarki) |
| `E` | Descent Read (ned i hierarki, read-only) |
| `Ctrl+E` | Return (op i hierarki) |
| `F8` | Skift til Windows desktop (ThinLinc) |
