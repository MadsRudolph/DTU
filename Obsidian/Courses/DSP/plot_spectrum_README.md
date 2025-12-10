# plot_spectrum.m - Exam Quick Reference

**Purpose:** Plot frequency spectra with beautiful arrows 
**For:** DTU 62743 Digital Signal Processing Exam  
**Usage:** Copy-paste patterns below at exam

---

## 🚀 Quick Start (Most Common)

### Pattern 1: Simple Baseband Spectrum
```matlab
% Just show frequencies in baseband
freqs = [1500, -1500, 3800, -3800];
amps = [1.5, 1.5, 1.0, 1.0];

plot_spectrum(freqs, amps);
```

### Pattern 2: With Custom Colors
```matlab
% Blue = no aliasing, Red = aliased
freqs = [1500, -1500, 3800, -3800];
amps = [1.5, 1.5, 1.0, 1.0];
colors = {'b', 'b', 'r', 'r'};

plot_spectrum(freqs, amps, 'Colors', colors);
```

### Pattern 3: Full Range with Replicas
```matlab
% Show spectral copies (sampling replicas)
freqs = [];
amps = [];
colors = {};

for k = -1:1  % 3 replicas
    freqs = [freqs, F1 + k*Fs, -F1 + k*Fs];
    amps = [amps, A1/2, A1/2];
    colors = [colors, 'b', 'b'];
end

plot_spectrum(freqs, amps, 'Colors', colors, 'XRange', [-10000, 10000]);
```

---

## 📋 Complete Exam Examples

### Example 1: F25 Problem 3 - Aliasing Spectrum

**Given:**
- $x(t) = 3\cos(2\pi \cdot 1500t) + 2\cos(2\pi \cdot 4200t)$
- $F_s = 8000$ Hz

**Code:**
```matlab
%% Problem 3-1: Aliasing Spectrum

F1 = 1500;  A1 = 3;
F2 = 4200;  A2 = 2;
Fs = 8000;

% Calculate aliased frequency
F2_alias = Fs - F2;  % = 3800 Hz

% Build spectrum with replicas
freqs = [];
amps = [];
colors = {};

for k = -1:1
    % F1 (blue - no aliasing)
    freqs = [freqs, F1 + k*Fs, -F1 + k*Fs];
    amps = [amps, A1/2, A1/2];
    colors = [colors, 'b', 'b'];
    
    % F2 (red - aliased)
    freqs = [freqs, F2_alias + k*Fs, -F2_alias + k*Fs];
    amps = [amps, A2/2, A2/2];
    colors = [colors, 'r', 'r'];
end

% Plot
plot_spectrum(freqs, amps, ...
              'Colors', colors, ...
              'XRange', [-10000, 10000], ...
              'Title', 'Sampled Signal Spectrum (Fs = 8000 Hz)');

% Add Nyquist lines
hold on;
xline([Fs/2, -Fs/2], '--y', 'LineWidth', 2);
hold off;
```

**What you see:**
- Blue arrows at ±1500, ±6500, ±9500 Hz (F1 and replicas)
- Red arrows at ±3800, ±4200 Hz (F2 aliased + replicas)
- Yellow dashed lines at ±4000 Hz (Nyquist)

---

### Example 2: AM Modulation Spectrum

**Given:**
- Carrier: $f_c = 5000$ Hz
- Message: $f_m = 500$ Hz
- Modulation creates sidebands at $f_c \pm f_m$

**Code:**
```matlab
fc = 5000;
fm = 500;

% Carrier + sidebands
freqs = [fc, -fc, fc+fm, -(fc+fm), fc-fm, -(fc-fm)];
amps = [1, 1, 0.5, 0.5, 0.5, 0.5];

plot_spectrum(freqs, amps, 'Title', 'AM Spectrum');
```

---

### Example 3: Aliasing Analysis (Multiple Components)

**Pattern for any multi-component signal:**
```matlab
% Given: x(t) = A1*cos(2πF1*t) + A2*cos(2πF2*t) + ...

% Step 1: Identify which frequencies alias
Nyquist = Fs/2;
fprintf('F1=%d: aliasing? %s\n', F1, string(F1 > Nyquist));
fprintf('F2=%d: aliasing? %s\n', F2, string(F2 > Nyquist));

% Step 2: Calculate aliased frequencies
if F1 > Nyquist
    F1_app = Fs - F1;  % Apparent frequency
else
    F1_app = F1;
end

if F2 > Nyquist
    F2_app = Fs - F2;
else
    F2_app = F2;
end

% Step 3: Plot baseband
freqs = [F1_app, -F1_app, F2_app, -F2_app];
amps = [A1/2, A1/2, A2/2, A2/2];

plot_spectrum(freqs, amps);
```

---

## 🎨 Customization Options

### All Available Parameters

```matlab
plot_spectrum(freqs, amps, ...
              'XRange', [-10000, 10000], ...  % X-axis limits
              'YMax', 2, ...                   % Y-axis max
              'XStep', 1000, ...               % X-axis tick spacing
              'YStep', 0.5, ...                % Y-axis tick spacing
              'XLabel', 'Frequency (Hz)', ...  % X-axis label
              'YLabel', 'Amplitude', ...       % Y-axis label
              'Colors', {'b','r'}, ...         % Arrow colors
              'LineWidth', 3, ...              % Arrow thickness
              'Title', 'My Spectrum', ...      % Plot title
              'MaxXLabels', 11, ...            % Max x-tick labels
              'MaxYLabels', 8);                % Max y-tick labels
```

### Color Shortcuts

| Code | Color | Use For |
|------|-------|---------|
| `'b'` | Blue | Non-aliased components |
| `'r'` | Red | Aliased components |
| `'g'` | Green | Passband |
| `'y'` | Yellow | Markers (Nyquist, etc) |
| `'auto'` | Alternating blue/red | Auto-color |

---

## 🔧 Common Patterns

### Pattern: Show Only Positive Frequencies
```matlab
% For real signals, spectrum is symmetric
% Just show positive side
freqs = [1500, 3800];
amps = [1.5, 1.0];

plot_spectrum(freqs, amps, 'XRange', [0, 5000]);
```

### Pattern: Add Reference Lines
```matlab
plot_spectrum(freqs, amps);

hold on;
xline(Fs/2, '--r', 'Nyquist');  % Nyquist frequency
xline(1000, ':g', 'f_p');       % Passband edge
yline(0.5, '--k');              % Amplitude threshold
hold off;
```

### Pattern: Multiple Replicas Loop
```matlab
% Template for showing k replicas from -k to +k
freqs = [];
amps = [];

for k = -1:1  % Change range as needed
    % For each component
    freqs = [freqs, F1 + k*Fs, -F1 + k*Fs];
    amps = [amps, A1/2, A1/2];
end

plot_spectrum(freqs, amps, 'XRange', [-k*Fs, k*Fs]);
```

---

## ⚠️ Exam Tips & Traps

### Tip 1: Cosine Amplitudes
**For $A\cos(2\pi Ft)$, spectrum has amplitude $A/2$ at $\pm F$**
```matlab
% Signal: 3*cos(2π*1500*t)
% Spectrum: amplitude 1.5 at ±1500 Hz
amps = [3/2, 3/2];  % NOT [3, 3]!
```

### Tip 2: Aliasing Formula
**If $F > F_s/2$, aliased frequency is:**
$$F_{\text{alias}} = F_s - F \quad \text{(for first fold)}$$

```matlab
% F = 4200 Hz, Fs = 8000 Hz
F_alias = Fs - F;  % = 3800 Hz
```

### Tip 3: Symmetric Spectrum
**Real signals have symmetric spectra:**
```matlab
% Always include both +F and -F
freqs = [F, -F];  % Symmetric!
amps = [A, A];    % Same amplitude
```

### Tip 4: Check Your Range
**Make sure all arrows are visible:**
```matlab
% If you have frequencies at ±9500 Hz
plot_spectrum(freqs, amps, 'XRange', [-10000, 10000]);  % Good
plot_spectrum(freqs, amps, 'XRange', [-5000, 5000]);    % Bad! Cut off
```

---

## 🐛 Troubleshooting

### Problem: Arrows Not Showing
**Solution:** Check that frequencies are within XRange
```matlab
% Debug: Print what you're plotting
fprintf('Frequencies: '); disp(freqs);
fprintf('Amplitudes: '); disp(amps);
fprintf('Range: %.0f to %.0f Hz\n', min(freqs), max(freqs));
```

### Problem: Too Many/Few Labels
**Solution:** Adjust MaxXLabels
```matlab
plot_spectrum(freqs, amps, 'MaxXLabels', 15);  % More labels
plot_spectrum(freqs, amps, 'MaxXLabels', 7);   % Fewer labels
```

### Problem: Colors Not Working
**Solution:** Colors must be cell array
```matlab
% Wrong:
colors = ['b', 'r', 'b', 'r'];  ❌

% Right:
colors = {'b', 'r', 'b', 'r'};  ✓
```

### Problem: Need to Add More Components
**Solution:** Concatenate arrays
```matlab
% Start with F1
freqs = [F1, -F1];
amps = [A1/2, A1/2];

% Add F2
freqs = [freqs, F2, -F2];
amps = [amps, A2/2, A2/2];

% Add F3
freqs = [freqs, F3, -F3];
amps = [amps, A3/2, A3/2];
```

---

## 📝 Exam Checklist

**Before plotting:**
- [ ] Identify all frequency components
- [ ] Check which components alias ($F > F_s/2$?)
- [ ] Calculate aliased frequencies ($F_{\text{alias}} = F_s - F$)
- [ ] Remember: amplitude = $A/2$ for each spike
- [ ] Include negative frequencies (symmetric!)

**For the plot:**
- [ ] Build `freqs` array (all components)
- [ ] Build `amps` array (amplitudes)
- [ ] Build `colors` cell array if needed
- [ ] Set XRange to show all components
- [ ] Call `plot_spectrum(freqs, amps, ...)`
- [ ] Add reference lines (Nyquist, etc) if needed

**After plotting:**
- [ ] Check all arrows are visible
- [ ] Verify Nyquist lines at correct positions
- [ ] Label axes clearly
- [ ] Title describes what's shown

---

## 🎓 Exam-Ready Template

**Copy-paste this at exam and fill in the blanks:**

```matlab
%% Aliasing Spectrum Template

% Given parameters
F1 = ___;  A1 = ___;
F2 = ___;  A2 = ___;
Fs = ___;

% Calculate aliased frequencies
Nyquist = Fs/2;
if F1 > Nyquist
    F1_app = Fs - F1;
else
    F1_app = F1;
end

if F2 > Nyquist
    F2_app = Fs - F2;
else
    F2_app = F2;
end

% Build spectrum (choose baseband OR full replicas)

% Option A: Baseband only (simple)
freqs = [F1_app, -F1_app, F2_app, -F2_app];
amps = [A1/2, A1/2, A2/2, A2/2];

% Option B: Full replicas (complete)
freqs = [];
amps = [];
for k = -1:1
    freqs = [freqs, F1_app + k*Fs, -F1_app + k*Fs];
    amps = [amps, A1/2, A1/2];
    freqs = [freqs, F2_app + k*Fs, -F2_app + k*Fs];
    amps = [amps, A2/2, A2/2];
end

% Plot
plot_spectrum(freqs, amps, 'XRange', [-10000, 10000]);

% Add Nyquist
hold on;
xline([Nyquist, -Nyquist], '--y', 'LineWidth', 2);
hold off;
```

---

## 📚 See Also

- [[F25 Exam]] - Problem 3 complete solution
- [[Week 5-7]] - Sampling & aliasing formulas
- [[DSP-Bible]] - General MATLAB tips

---

**Last Updated:** December 2025  
**For:** DTU 62743 F25 Exam
