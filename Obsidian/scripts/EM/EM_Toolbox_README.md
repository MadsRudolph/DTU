# EM_Assistant

Interactive menu-driven interface for solving electromagnetic problems.

---

## Setup

1. Put all `.m` files in one folder
2. Add to MATLAB path:
   ```matlab
   addpath('C:\path\to\EM_Toolbox')
   ```
3. Run:
   ```matlab
   EM_Assistant
   ```

---

## How It Works

```
  ╔══════════════════════════════════════════════════════════╗
  ║            ⚡ EM TOOLBOX ASSISTANT ⚡                    ║
  ╚══════════════════════════════════════════════════════════╝

  ┌────────────────────────────────────────┐
  │         WHAT DO YOU NEED HELP WITH?    │
  ├────────────────────────────────────────┤
  │  1. Plane Wave Verification            │
  │  2. Polarization Analysis              │
  │  3. Fresnel (Reflection/Transmission)  │
  │  4. Medium Properties (η, β, λ, etc.)  │
  │  5. Transmission Lines                 │
  │  6. Stub Matching                      │
  │  7. Poynting Vector / H-field          │
  │  8. Magnetic Field (Infinite Wire)     │
  │  9. Coulomb Force                      │
  │                                        │
  │  0. Exit                               │
  └────────────────────────────────────────┘
```

1. **Select a topic** (1-9)
2. **Answer the guided questions** — the assistant asks for exactly what's needed
3. **See the function call** — shows you what command was used
4. **Get results** — displayed with all relevant outputs
5. **Press Enter** — solve another problem

---

## Topics Covered

| # | Topic | What It Solves |
|---|-------|----------------|
| 1 | Plane Wave Verification | Is this E, H, k a valid plane wave? |
| 2 | Polarization | Linear/Circular/Elliptical? RHCP/LHCP? Axial ratio? |
| 3 | Fresnel | Γ, τ, R, T at interfaces. Brewster/critical angles |
| 4 | Medium Properties | η, β, λ, skin depth, classification |
| 5 | Transmission Lines | Zin, ZL, Γ, VSWR, quarter-wave, stubs |
| 6 | Stub Matching | Find d and ℓ for single-stub matching |
| 7 | Poynting Vector | H-field from E-field, time-average power |
| 8 | B-field (Wire) | Magnetic field around infinite wire |
| 9 | Coulomb Force | Force between point charges |

---

## Entering Values

### Numbers
```
Enter choice (1-9): 3
εr1: 1
εr2: 4
θi [degrees]: 45
```

### Complex Numbers
The assistant accepts several formats:
```
Ex: 1
Ey: -1j
Ez: 0

Ex: 2+1j*3
Ey: 1j*5
```

### Vectors
Entered component by component:
```
Enter E-field phasor components:
  Ex: 1
  Ey: -1j
  Ez: 0
```

### Yes/No Questions
```
Use custom η? (y/n): n
```

---

## Example Session

```
>> EM_Assistant

  ╔══════════════════════════════════════════════════════════╗
  ║            ⚡ EM TOOLBOX ASSISTANT ⚡                    ║
  ╚══════════════════════════════════════════════════════════╝

  Enter choice (0-9): 2

  ═══════════════════════════════════════════
       POLARIZATION ANALYSIS
  ═══════════════════════════════════════════

  What format is your E-field?

    1. Complex phasor: E = [Ex; Ey; Ez]
    2. Amplitude/Phase: Ex∠φx, Ey∠φy
    3. Time-domain: u·cos + v·sin

  Enter format (1-3): 1

  --- Enter E-field phasor components ---
  Ex: 1
  Ey: -1j
  Ez: 0

  Use default +z? (y/n): y

  Calling: Polarization(E, k_hat)

  ========================================
         POLARIZATION ANALYSIS           
  ========================================
    Type:        Circular
    Handedness:  RHCP
    Axial Ratio: 1.000 (0.00 dB)
  ========================================

  Press Enter to continue...
```

---

## Tips

### Before the Exam
- Run `EM_Assistant` once to verify everything works
- Practice entering complex numbers and vectors

### During Use
- The assistant shows the actual function call used — helpful for learning
- If you make a mistake, press Enter and start over
- Check units before entering (Hz not GHz, m not cm)

### When Not to Use It
If you know exactly what function and parameters you need, calling the script directly is faster:
```matlab
Polarization([1; -1j; 0])
```

---

## Required Files

The assistant needs all these scripts in the same folder:

```
EM_Toolbox/
├── EM_Assistant.m       ← The assistant itself
├── PlaneWaveCheck.m
├── Polarization.m
├── Fresnel.m
├── Medium.m
├── TLine.m
├── StubMatch.m
├── poynting_pw.m
├── B_inf_wire.m
├── coulomb_pair.m
├── rect2pol.m
└── smithchart_plot.m
```

---

## Documentation

For detailed script documentation, theory, and examples:
- **[Helpers.md](Helpers.md)** — Master reference for all scripts
