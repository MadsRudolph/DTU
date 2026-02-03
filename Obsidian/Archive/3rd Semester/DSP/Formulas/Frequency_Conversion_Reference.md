# DSP Frequency Conversion Quick Reference

**The Rosetta Stone of DSP Frequencies** 🗿

---

## Visual Conversion Map

```
                    ×2π (add angular)
                    ──────────────→
        F                                    Ω = 2πF
    "Physical"                          "Analog Angular"
      [Hz]          ←──────────────         [rad/s]
                         ÷2π
        ↓                                      ↓
      ÷Fs                                   ×2π÷Fs
   (normalize)                           (normalize + angular)
        ↓                                      ↓
     f = F/Fs                             ω = 2πF/Fs
   "Normalized"          ×2π           "Digital Angular"
   [unit-less]      ──────────→         [rad/sample]
```

---

## The Four Frequency Types

### 1️⃣ Physical Frequency: **F**
- **Units:** Hz (cycles per second)
- **What:** Real-world frequency you measure
- **Range:** 0 to ∞
- **Example:** "The signal is 1500 Hz"

### 2️⃣ Normalized Frequency: **f**
- **Formula:** $f = F / F_s$
- **Units:** Dimensionless (0 to 1)
- **What:** Frequency relative to sampling rate
- **Range:** 0 to 1 (Nyquist at 0.5)
- **Example:** $f = 1500/8000 = 0.1875$

### 3️⃣ Digital Angular Frequency: **ω** ⭐ MOST USED
- **Formula:** $\omega = 2\pi f = 2\pi F / F_s$
- **Units:** rad/sample (unit-less)
- **What:** Frequency for z-domain analysis
- **Range:** 0 to 2π (Nyquist at π)
- **Example:** $\omega = 2\pi \times 0.1875 = 0.375\pi$ rad/sample
- **Used for:** Z-transforms, DTFT, frequency response

### 4️⃣ Analog Angular Frequency: **Ω**
- **Formula:** $\Omega = 2\pi F$
- **Units:** rad/s
- **What:** Frequency for analog (s-domain) analysis
- **Range:** 0 to ∞
- **Example:** $\Omega = 2\pi \times 1500 = 9425$ rad/s
- **Used for:** Analog prototypes, BLT pre-warping

---

## Conversion Formulas

### From Physical F (Hz):
```
f  = F / Fs                    (normalized)
ω  = 2π·F / Fs  = 2π·f        (digital angular)
Ω  = 2π·F                     (analog angular)
```

### From Digital Angular ω:
```
f  = ω / (2π)                  (normalized)
F  = ω·Fs / (2π)              (physical)
```

### BLT Pre-warping (Special):
```
Ω = (2/Ts)·tan(ω/2)           (ω → Ω for bilinear transform)
Ω = 2·Fs·tan(ω/2)             (same, with Ts = 1/Fs)
```

---

## Key Landmarks

| Frequency | Physical F | Normalized f | Digital ω | Analog Ω |
|-----------|------------|--------------|-----------|----------|
| **DC** | 0 Hz | 0 | 0 | 0 rad/s |
| **Nyquist** | Fs/2 | 0.5 | π | π·Fs rad/s |
| **Sampling** | Fs | 1.0 | 2π | 2π·Fs rad/s |

---

## When to Use Each

| Frequency Type | Use When... |
|----------------|-------------|
| **F (Hz)** | Reading problem specs, real-world measurements |
| **f (normalized)** | Designing platform-independent filters |
| **ω (digital rad)** | Working in z-domain, DTFT, frequency response |
| **Ω (analog rad/s)** | Designing analog prototypes, BLT calculations |

---

## Common Exam Patterns

### Pattern 1: Check for Aliasing
```
Given: F = 4200 Hz, Fs = 8000 Hz
Step 1: Find Nyquist → Fs/2 = 4000 Hz
Step 2: Compare → 4200 > 4000 → ALIASING!
Step 3: Find alias → Fs - F = 3800 Hz
```

### Pattern 2: IIR Filter (BLT)
```
Given: fp = 1000 Hz, Fs = 8000 Hz
Step 1: Digital → ωp = 2π·1000/8000 = 0.25π rad/sample
Step 2: Pre-warp → Ωp = 2·8000·tan(0.25π/2) = 8000 rad/s
Step 3: Design analog filter at Ωp
Step 4: Apply BLT to get digital filter
```

### Pattern 3: FIR Filter
```
Given: fc = 0.3π rad/sample (already in ω!)
Step 1: Use ωc = 0.3π directly in design equations
```

---

## ⚠️ Common Mistakes to Avoid

❌ **DON'T:**
- Confuse ω (digital) with Ω (analog)
- Forget to specify units
- Use F (Hz) in z-domain equations
- Mix up Nyquist in different representations

✅ **DO:**
- Always convert to appropriate domain first
- Remember: ω is unit-less despite "rad" notation
- Check your frequency is in valid range for that domain
- Use ω (digital angular) for most DSP work

---

## Quick Reference Card

**For F25 Exam:**

```matlab
% Given specs in Hz
F1 = 1500;  Fs = 8000;

% Convert to digital angular (for z-domain)
omega1 = 2*pi*F1/Fs;           % 0.375π rad/sample

% Check aliasing
F_nyquist = Fs/2;               % 4000 Hz
if F1 > F_nyquist
    fprintf('ALIASING!\n');
end

% For BLT (need analog angular)
Omega1 = 2*Fs*tan(omega1/2);   % rad/s for analog prototype
```

---

**Remember:** When in doubt, work in **ω (digital angular frequency)** for z-domain DSP! 🎯

**See also:** 
- [[Week 1-4]] - Section: "DSP Frequency Representations"
- [[F25 Exam]] - Problem 2 (BLT), Problem 3 (Aliasing)
