# EM Assistant (Python Edition)

Interactive menu-driven interface for solving electromagnetic problems.

---

## Quick Start

1. Put both files in the same folder:
   ```
   em_calc.py
   em_assistant.py
   ```

2. Run:
   ```bash
   python em_assistant.py
   ```

---

## ⚠️ Python Environment (READ THIS IF NOTHING RUNS)

> **TL;DR:**  
> Do **NOT** use the default `python` in Git Bash.  
> It points to **MSYS2 Python**, which will NOT install NumPy cleanly.  
> Always use a **Windows Python virtual environment (`venv`)**.

### ✅ One-Time Setup (DO THIS ONCE)

From the **Assistant** folder:

```bash
py -3 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install numpy
```

Verify everything works:

```bash
python -c "import numpy as np; print(np.__version__)"
python em_assistant.py
```

---

### ✅ Daily Use

```bash
cd ~/DTU/3.semester/Electromagnetics/Assistant
source .venv/Scripts/activate
python em_assistant.py
```

If you see:

```
ModuleNotFoundError: No module named 'numpy'
```

You forgot to activate the venv.

---

### 🔍 Sanity Check

```bash
python -c "import sys; print(sys.executable)"
```

Should point to:

```
.../Assistant/.venv/Scripts/python.exe
```

## Problem → Menu Guide

**Use this table to quickly find the right menu option based on your exam problem.**

### Keywords → Menu Option

| If the problem mentions... | Use Menu | Option |
|---------------------------|----------|--------|
| "Is this a valid plane wave?" | **1** | Plane Wave Verification |
| "Polarization", "RHCP/LHCP", "axial ratio", "tilt angle" | **2** | Polarization Analysis |
| "Reflection coefficient Γ", "transmission τ", "interface", "Brewster", "critical angle", "TIR" | **3** | Fresnel |
| "Wavelength λ", "phase velocity", "intrinsic impedance η", "skin depth", "loss tangent", "good conductor" | **4** | Medium Properties |
| "Transmission line", "Z_in", "VSWR", "Γ at load/input", "quarter-wave transformer" | **5** | Transmission Lines |
| "Stub matching", "single-stub tuner", "match to Z₀" | **6** | Stub Matching |
| "Poynting vector", "power density", "incident power", "H-field from E" | **7** | Poynting Vector |
| "Magnetic field from wire", "B-field", "infinite wire" | **8** | B-field (Wire) |
| "Coulomb force", "point charges" | **9** | Coulomb Force |
| "Find Z_L from VSWR", "standing wave measurement", "V_min/V_max position" | **10** | Inverse TLine |
| "Inductance", "capacitance", "solenoid", "coaxial", "parallel plate", "parallel wire" | **11** | Geometry Library |
| "Uniform wave", "non-uniform", "α parallel to β" | **12** | Wave Uniformity |

---

## Exam Problem Types → Step-by-Step

### "Find Γ_L from Γ at input" (Q13 type)
```
Menu 5 → Option 6
Enter: Z0, |Γ_in|, ∠Γ_in, length in λ
```

### "Find Z_L from reflection coefficient" (Q14 type)
```
Menu 5 → Option 5
Enter: Z0, Γ (complex)
```
*Or use Menu 5 → Option 6 which gives both Γ_L and Z_L*

### "Find wavelength in medium" (Q15 type)
```
Menu 4 → Option 1 (lossless) or Option 2 (lossy)
Enter: εr, frequency
→ Get λ
```

### "Stub matching: find d and ℓ" (Q16-Q17 type)
```
Menu 6
Enter: Z_L (real + imag), Z0, stub type, λ
→ Get d and ℓ in λ and mm
```

### "Incident power on surface" (Poynting type)
```
Menu 7 → Option 3 (scalar mode)
Enter: |E₀|, γ = α + jβ, position (x,y,z), εr (complex), area, surface normal
→ Get S_avg and Power
```

### "Polarization type and handedness"
```
Menu 2 → Option 1 (phasor) or 2 (amp/phase) or 3 (time-domain)
Enter: E-field components
→ Get type, handedness, axial ratio, tilt
```

### "Find Z_L from VSWR and V_min position"
```
Menu 10
Enter: Z0, VSWR (or |Γ| or Γ_dB), z_min or z_max
→ Get Z_L and Γ_L
```

---

## Menu Structure

```
  ╔══════════════════════════════════════════════════════════╗
  ║            ⚡ EM TOOLBOX ASSISTANT ⚡                    ║
  ║              Python Edition v2.0                         ║
  ╚══════════════════════════════════════════════════════════╝

  ┌────────────────────────────────────────┐
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
  │  10. Inverse TLine (VSWR→Z_L)          │
  │  11. Geometry Library (L, C)           │
  │  12. Wave Uniformity Analyzer          │
  │                                        │
  │  0. Exit                               │
  └────────────────────────────────────────┘
```

---

## Detailed Menu Reference

### Menu 5: Transmission Lines (8 sub-options)

| Sub | Use when... | You have | You get |
|-----|-------------|----------|---------|
| 1 | Basic analysis | Z0, Z_L, length | Z_in, Γ, VSWR |
| 2 | Find input impedance | Z0, Z_L, length | Z_in |
| 3 | Find load impedance | Z0, Z_in, length | Z_L |
| 4 | Γ from impedance | Z0, Z | Γ |
| 5 | Z from Γ | Z0, Γ | Z |
| **6** | **Γ_L from Γ_in** | Z0, Γ_in, length | **Γ_L, Z_L** |
| 7 | Quarter-wave design | Z_in, Z_L | Z0 needed |
| 8 | Electrical length | Z0, Z_in, Z_L | length in λ |

### Menu 7: Poynting Vector (3 sub-options)

| Sub | Use when... | Input format |
|-----|-------------|--------------|
| 1 | Time-domain E-field | E₀(a·cos + b·sin), β vector |
| 2 | Complex phasor E | Ex, Ey, Ez (complex), k vector |
| **3** | **Scalar/Power** | \|E\|, η (or εr), area, surface normal |

**Option 3 features:**
- Calculate |E| at position from E₀ and γ
- Handle complex εr (lossy media)
- Surface normal for tilted surfaces
- Direct power calculation

### Menu 4: Medium Properties (5 sub-options)

| Sub | Use when... |
|-----|-------------|
| 1 | Lossless dielectric (just εr) |
| 2 | Lossy medium (σ given) |
| 3 | Loss tangent given (tan δ) |
| 4 | Good conductor approximation |
| 5 | Skin depth only |

---

## Entering Values

### Numbers
```
Z0 [Ω]: 75
Length [λ]: 0.25
Frequency [Hz]: 1550e6      ← Use scientific notation
```

### Complex Numbers
```
Ex: 1+2j        ← Rectangular
Ex: 20j         ← Pure imaginary
Ex: 3-1j*4      ← Also valid
```

### Polar form (if needed)
Use the conversion: `A∠θ° = A·cos(θ) + j·A·sin(θ)`
Or enter magnitude and phase when prompted (Menu 2, Option 2)

### Vectors
Entered component by component:
```
--- E phasor components ---
Ex: 20j
Ey: 0
Ez: 0
```

### Yes/No Questions
```
Custom η? (y/n): n
Calculate power? (y/n): y
```

---

## Example Sessions

### Example 1: Stub Matching (Q16-17 type)

```
Enter choice (0-12): 6

═══════════════════════════════════════════
       SINGLE-STUB MATCHING
═══════════════════════════════════════════
ZL real [Ω]: 142
ZL imag [Ω]: 42.5
Z0 [Ω]: 75
Stub type: 1=Short, 2=Open
Choice: 1
Know the wavelength λ? (y/n): y
λ [m]: 0.1335

════════════════════════════════════════
       RESULT
════════════════════════════════════════
d = 0.1838 λ = 24.54 mm       ← Q16 answer
l = 0.1457 λ = 19.45 mm       ← Q17 answer
Alt: d=0.3754λ, l=0.3543λ
════════════════════════════════════════
```

### Example 2: Incident Power (Poynting type)

```
Enter choice (0-12): 7

═══════════════════════════════════════════
       POYNTING VECTOR & H-FIELD
═══════════════════════════════════════════
  1. Time-domain: E = E0*(a·cos + b·sin)
  2. Complex phasor E directly
  3. Scalar: |E| and η → S_avg (simple)

Enter format (1-3): 3

--- Electric field magnitude ---
  1. Enter |E| directly
  2. Calculate |E| at position (with attenuation)
Choice: 2

--- E-field at origin ---
  1. |E₀| magnitude directly
  2. Complex E₀ (e.g., j20)
Choice: 2
E₀ [V/m]: 20j
|E₀| = 20.0000 V/m

--- Propagation direction ---
  1. +z only (common case)
  2. General direction (kx, ky, kz)
Choice: 1

--- Propagation constant γ ---
  1. Enter α directly
  2. Enter γ = α + jβ
Choice: 2
α (real part): 3.0
β (imag part): 42

--- Surface position ---
  1. Enter z only
  2. Enter full (x, y, z)
Choice: 1
z [m]: 0.6

────────────────────────────────
Distance along k̂: 0.6000 m
|E(r)| = 20.0000 × 0.1653 = 3.3060 V/m
────────────────────────────────

--- Intrinsic impedance η ---
  1. Free space (377 Ω)
  2. Lossless medium (εr)
  3. Lossy medium (complex εr)
  4. Enter η directly
Choice: 3
εr (real): 3.5
εr (imag): -0.5

η = 200.00+14.21j Ω

════════════════════════════════════════
       RESULT
════════════════════════════════════════
S_avg = 27.32 mW/m²

Calculate power? (y/n): y
Area [m²]: 2

--- Surface normal ---
  1. Normal to propagation
  2. Enter (nx, ny, nz)
Choice: 2
nx: 0
ny: 0
nz: -1

P = 54.65 mW                   ← Answer
════════════════════════════════════════
```

### Example 3: Find Γ_L from Γ at input (Q13 type)

```
Enter choice (0-12): 5

═══════════════════════════════════════════
       TRANSMISSION LINES
═══════════════════════════════════════════
  1. Basic TL analysis
  2. Find input impedance
  3. Find load impedance
  4. Reflection coefficient from Z
  5. Impedance from Γ
  6. Find load from Γ at input
  7. Quarter-wave transformer
  8. Electrical length

Enter choice (1-8): 6
Z0 [Ω]: 75
|Γ_in|: 0.539
∠Γ_in [deg]: 166
Length [λ]: 0.3

════════════════════════════════════════
Γ_L = 0.4998 + j0.2019
|Γ_L| = 0.5390, ∠Γ_L = 22.00°  ← Q13 answer
Z_L = 182.84 + j104.07 Ω       ← Q14 answer
════════════════════════════════════════
```

---

## Quick Reference Card

| Problem Type | Menu | Key Inputs |
|--------------|------|------------|
| Γ_L from Γ_in | 5→6 | Z0, \|Γ\|, ∠Γ, length |
| Z_L from VSWR + position | 10 | Z0, VSWR, z_min or z_max |
| Stub matching | 6 | Z_L, Z0, stub type, λ |
| λ in medium | 4→1 | εr, frequency |
| Incident power | 7→3 | E₀, γ, position, εr, area |
| Polarization | 2 | E-field (phasor/amp-phase/time) |
| Interface Γ, τ | 3 | εr1, εr2, θ_i |
| η, β, skin depth | 4 | εr, σ, μr, frequency |

---

## Tips

### Before the Exam
- Run `python em_assistant.py` to verify it works
- Practice a few problems from each menu
- Know which menu handles which problem type

### During Use
- **Read the problem carefully** — identify keywords
- **Check units** before entering (Hz not GHz, m not mm)
- If you make a mistake, press Enter and restart
- Use Option 1 (quick defaults) when available

### Common Unit Conversions
- Frequency: 1550 MHz = `1550e6` Hz
- Length: 24.5 mm = `0.0245` m (but stub results show mm!)
- Wavelength: usually given in problem or calculated from Menu 4

---

## Files Required

```
YourFolder/
├── em_calc.py           ← Core calculation library
├── em_assistant.py      ← Interactive assistant
└── test_em_calc.py      ← Optional: verify installation
```

Run `python test_em_calc.py` to verify all functions work (should show 29/29 tests passed).

---

## Changelog (Python Edition)

**v2.0** — New features:
- Menu 10: Inverse TLine (find Z_L from VSWR + position)
- Menu 11: Geometry library (solenoid L, capacitor C)
- Menu 12: Wave uniformity analyzer (α ∥ β check)
- Menu 7 Option 3: Scalar Poynting mode with:
  - |E| calculation from E₀ and attenuation
  - Complex εr support (lossy media)
  - Arbitrary position (x, y, z)
  - Surface normal for tilted surfaces
- Analytical StubMatch solver (improved accuracy)
