# DSP Toolbox - Python Edition
## DTU 62743 Digital Signal Processing

A complete Python toolkit for solving DSP exam problems, equivalent to MATLAB.

---

## 📦 Package Contents

| File | Description |
|------|-------------|
| `dsp_calc.py` | Core calculation library (24 functions) |
| `dsp_assistant.py` | Interactive terminal-based problem solver |
| `dsp_viz.py` | Visualization tools (MATLAB ports) |
| `test_dsp_calc.py` | Test suite (24 tests) |

---

## 🚀 Quick Start

### Option 1: Interactive Assistant
```bash
python dsp_assistant.py
```
This launches a menu-driven interface where you select problem types and enter values.

### Option 2: Direct Python Import
```python
from dsp_calc import *
from dsp_viz import *

# Step → Impulse
result = StepToImpulse([2, 3, -3, -2])
print(result.h)  # [2, 1, -6, 1, 2]

# Plot pole-zero diagram
plot_pz(B=[1, -2, 1], A=[1, -0.5])

# Linear phase analysis (detects A(ω) < 0 trap!)
plot_linear_phase_analysis([2, 1, -6, 1, 2])
```

---

## 🎬 Run the Visualization Demo

See all visualization functions in action:

### Option 1: Run Directly
```bash
python dsp_viz.py
```

### Option 2: Import and Call
```python
from dsp_viz import demo
demo()
```

This runs 5 example plots:

| # | Plot | What It Shows |
|---|------|---------------|
| 1 | **Spectrum** | Arrow-style frequency components |
| 2 | **Pole-Zero** | P-Z diagram with stability indicator |
| 3 | **Linear Phase** | ⚠️ 4-panel A(ω) trap detector |
| 4 | **Frequency Response** | Magnitude (dB) + Phase |
| 5 | **Z-Surface** | 3D \|H(z)\| like MATLAB's `zpgui()` |

### Run Individual Functions
```python
from dsp_viz import plot_pz, plot_linear_phase_analysis

# Just pole-zero
plot_pz(zeros=[1, -1], poles=[0.8+0.4j, 0.8-0.4j])

# Just linear phase analysis
plot_linear_phase_analysis([2, 1, -6, 1, 2])

# Save to file instead of showing
plot_pz(zeros=[1], poles=[0.5], save_path='my_plot.png', show=False)
```

---

## 📚 Available Functions

### LTI System Analysis
- `StepToImpulse(y_step)` - Convert step response to impulse response
- `SystemFunction(B, A)` - Build H(z) from coefficients
- `PoleZeroAnalysis(B, A)` - Stability & minimum-phase check
- `InverseSystem(B, A)` - Can 1/H(z) be stable + causal?
- `CascadeDecomposition(H_total, H1)` - Find H2 = H/H1

### Frequency Response
- `LinearPhaseCheck(h)` - Symmetry trick + A(ω) positivity check
- `FrequencyResponse(B, A, omega)` - Calculate H(e^jω)

### IIR Filter Design
- `Prewarp(F, Fs)` - Bilinear transform frequency pre-warping
- `ButterworthOrder(Ap, As, Ωp, Ωs)` - Calculate filter order

### FIR Filter Design
- `IdealImpulseResponse(type, ωc, N)` - sinc-based ideal filter
- `WindowedFIR(h, window_type)` - Apply Hamming, Hanning, etc.

### Sampling
- `SamplingAnalysis(frequencies, Fs)` - Detect aliasing

### Advanced
- `MinPhaseDecomposition(B)` - H = H_min · H_ap

### Visualization (NEW!)
- `plot_spectrum(freqs, amps)` - Frequency spectrum with arrows
- `plot_pz(B, A)` - Pole-zero diagram
- `plot_frequency_response(B, A)` - Magnitude & phase
- `plot_linear_phase_analysis(h)` - **4-panel A(ω) trap detector**
- `plot_z_surface(B, A)` - 3D |H(z)| surface
- `spectrum_sampled(freqs, Fs)` - Aliasing visualization

---

## ⚠️ Exam Traps Detected

### 1. A(ω) Negativity Trap
```python
# This looks symmetric but A(ω) goes negative!
h = [2, 1, -6, 1, 2]
result = LinearPhaseCheck(h)
print(result.is_positive)  # False!
print(result.positivity_warning)  # Explains the issue
```

### 2. Highpass Butterworth Ratio
```python
# HP uses Ωp/Ωs (not Ωs/Ωp like LP!)
result = ButterworthOrder(Ap=1, As=20, Omega_p=16000, Omega_s=6627, is_highpass=True)
```

### 3. Inverse System Stability
```python
# Zeros outside UC → inverse cannot be causal+stable
result = InverseSystem([1, -2.5, 1])
print(result.can_be_both)  # False
```

---

## 🧪 Run Tests
```bash
python -m pytest test_dsp_calc.py -v
# or simply:
python test_dsp_calc.py
```

---

## 📋 Requirements
- Python 3.8+
- NumPy
- Matplotlib (for visualization)

Install:
```bash
pip install numpy matplotlib
```

---

## 📖 References
All methods follow DTU 62743 exam solutions (E19-F25).

**Citation format in code:** `[E23 Q1]`, `[F24 Q3]`, etc.

---

Good luck on your exam! 📡🎓
