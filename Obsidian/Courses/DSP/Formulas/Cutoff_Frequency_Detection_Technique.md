# DSP Technique: Automatic Cutoff Frequency Detection

**The `find()` Method for Detecting Filter Cutoff Frequencies**

---

## 🎯 The Problem

You need to find where a filter's magnitude response crosses a specific threshold (e.g., -3 dB for cutoff frequency, -30 dB for stopband edge).

**Traditional approach:** Zoom in on plot, manually read value → **Inaccurate! ❌**

**Better approach:** Use MATLAB's `find()` to detect threshold crossings → **Accurate! ✅**

---

## 📐 The Technique

### **Basic Pattern:**

```matlab
% Step 1: Compute frequency response with HIGH resolution
F_vec = linspace(0, Fs/2, 10000);  % Many points = better accuracy
[H, F] = freqz(B, A, F_vec, Fs);
Mag_dB = 20*log10(abs(H));

% Step 2: Find threshold crossing
idx = find(Mag_dB >= -3, 1, 'last');  % Last point above -3 dB
F_cutoff = F(idx);

% Step 3: Mark on plot
xline(F_cutoff, '--g', sprintf('%.1f Hz', F_cutoff), 'LineWidth', 1.5);
```

---

## 🔍 How It Works

### **The `find()` Function:**

```matlab
idx = find(condition, N, direction)
```

- **`condition`**: Logical condition (e.g., `Mag_dB >= -3`)
- **`N`**: Number of matches to return (usually `1`)
- **`direction`**: `'first'` or `'last'`

### **Example:**

```matlab
Mag_dB = [-1, -2, -2.5, -3.2, -4, -5];  % Sample data

% Find last index where Mag >= -3 dB
idx = find(Mag_dB >= -3, 1, 'last');
% Returns: idx = 3 (value = -2.5, last point above -3)
```

---

## 📊 Common Use Cases

### **1. Lowpass Filter: Find -3 dB Cutoff**

```matlab
% Lowpass: Find last point in passband (last ≥ -3 dB)
idx_cutoff = find(Mag_dB >= -3, 1, 'last');
F_cutoff = F(idx_cutoff);

fprintf('Lowpass cutoff: %.2f Hz\n', F_cutoff);
```

**Why `'last'`?** You want the **end of the passband** (highest frequency still above -3 dB).

---

### **2. Highpass Filter: Find -3 dB Cutoff**

```matlab
% Highpass: Find first point in passband (first ≥ -3 dB)
idx_cutoff = find(Mag_dB >= -3, 1, 'first');
F_cutoff = F(idx_cutoff);

fprintf('Highpass cutoff: %.2f Hz\n', F_cutoff);
```

**Why `'first'`?** You want the **start of the passband** (lowest frequency above -3 dB).

---

### **3. Bandpass Filter: Find Both Cutoffs**

```matlab
% Find both edges where magnitude crosses -3 dB
idx_edges = find(Mag_dB >= -3);  % All points above -3 dB
F_lower = F(idx_edges(1));       % First point (lower cutoff)
F_upper = F(idx_edges(end));     % Last point (upper cutoff)

fprintf('Bandpass: %.2f Hz to %.2f Hz\n', F_lower, F_upper);

% Mark both on plot
xline([F_lower, F_upper], '--g', ...
      {sprintf('%.1f Hz', F_lower), sprintf('%.1f Hz', F_upper)});
```

---

### **4. Find Stopband Edge (-30 dB, -40 dB, etc.)**

```matlab
% Find where attenuation reaches -30 dB (stopband spec)
idx_stop = find(Mag_dB <= -30, 1, 'first');
F_stop = F(idx_stop);

fprintf('Stopband starts at: %.2f Hz (attenuation ≥ 30 dB)\n', F_stop);
```

**Why `<=` and `'first'`?** You want where attenuation **first becomes strong enough**.

---

## 🎨 Complete Visualization Template

```matlab
%% Complete Filter Analysis with Automatic Detection

% Filter coefficients
B = [0.0102, 0.0305, 0.0305, 0.0102];
A = [1, -2.0038, 1.4471, -0.3618];
Fs = 5000;

% High-resolution frequency response
F_vec = linspace(0, Fs/2, 10000);
[H, F] = freqz(B, A, F_vec, Fs);
Mag_dB = 20*log10(abs(H));

% Detect key frequencies
idx_3dB = find(Mag_dB >= -3, 1, 'last');
F_3dB = F(idx_3dB);

idx_30dB = find(Mag_dB <= -30, 1, 'first');
F_30dB = F(idx_30dB);

% Plot with all annotations
figure;
plot(F, Mag_dB, 'b-', 'LineWidth', 1.5); hold on; grid on;
xlabel('Frequency [Hz]'); ylabel('Magnitude [dB]');
title('Filter Magnitude Response with Automatic Detection');

% Mark thresholds
yline(-3, '--r', '-3 dB', 'LineWidth', 1.5);
yline(-30, '--', '-30 dB', 'Color', [0.5 0.5 0.5]);

% Mark detected frequencies
xline(F_3dB, '--g', sprintf('Cutoff: %.1f Hz', F_3dB), ...
      'LineWidth', 1.5, 'FontSize', 12);
xline(F_30dB, '--m', sprintf('Stopband: %.1f Hz', F_30dB));

% Mark spec (if given)
xline(400, '--k', '400 Hz (spec)', 'LineWidth', 1);

xlim([0, 1500]); ylim([-60, 5]);
hold off;

% Print results
fprintf('\n=== Detected Frequencies ===\n');
fprintf('  -3 dB cutoff:     %.2f Hz\n', F_3dB);
fprintf('  -30 dB stopband:  %.2f Hz\n', F_30dB);
fprintf('  Transition width: %.2f Hz\n', F_30dB - F_3dB);
```

---

## ⚡ Pro Tips

### **1. Use High Resolution**

```matlab
% BAD: Low resolution (may miss exact cutoff)
F = linspace(0, Fs/2, 512);  % Only 512 points

% GOOD: High resolution (accurate detection)
F = linspace(0, Fs/2, 10000);  % 10000 points
```

### **2. Choose Correct Direction**

| Filter Type | What to Find | Use |
|-------------|--------------|-----|
| Lowpass | Passband edge | `find(Mag >= -3, 1, 'last')` |
| Highpass | Passband edge | `find(Mag >= -3, 1, 'first')` |
| Bandpass | Lower edge | `find(Mag >= -3, 1, 'first')` |
| Bandpass | Upper edge | `find(Mag >= -3, 1, 'last')` |
| Any | Stopband edge | `find(Mag <= -30, 1, 'first')` |

### **3. Verify Visually**

Always plot with markers to verify:

```matlab
% Mark the detected point with a circle
plot(F_3dB, Mag_dB(idx_3dB), 'ro', 'MarkerSize', 10, 'LineWidth', 2);
```

### **4. Handle Edge Cases**

```matlab
% Check if threshold was found
idx = find(Mag_dB >= -3, 1, 'last');
if isempty(idx)
    warning('No point found above -3 dB threshold!');
else
    F_cutoff = F(idx);
    fprintf('Cutoff: %.2f Hz\n', F_cutoff);
end
```

---

## 📝 Exam Strategy

### **When to Use This Technique:**

✅ **DO use for:**
- Finding -3 dB frequencies (cutoff)
- Finding -30 dB, -40 dB (stopband edges)
- Verifying filter specifications
- Comparing measured vs. specified

❌ **DON'T use for:**
- Peak frequencies (use `[~, idx] = max(Mag_dB)`)
- Zero crossings in phase (use `interp1`)
- Group delay calculations (different technique)

### **Exam Template:**

```matlab
%% Quick Cutoff Detection (Copy-Paste for Exam)

% Given filter B, A, Fs
F = linspace(0, Fs/2, 10000);
[H, F] = freqz(B, A, F, Fs);
Mag_dB = 20*log10(abs(H));

% Find -3 dB cutoff
idx = find(Mag_dB >= -3, 1, 'last');  % Lowpass
F_cutoff = F(idx);

% Plot
plot(F, Mag_dB); grid on;
yline(-3, '--r'); xline(F_cutoff, '--g', sprintf('%.1f Hz', F_cutoff));

fprintf('Cutoff: %.2f Hz\n', F_cutoff);
```

**Time:** ~30 seconds to write, guaranteed accurate results! ⚡

---

## 🎓 Related Techniques

### **Find Peak Frequency (Resonance):**

```matlab
[max_mag, idx_peak] = max(Mag_dB);
F_peak = F(idx_peak);
fprintf('Peak at %.2f Hz (%.2f dB)\n', F_peak, max_mag);
```

### **Find Multiple Crossings:**

```matlab
% Find ALL crossings of -3 dB
idx_all = find(abs(Mag_dB + 3) < 0.1);  % Within 0.1 dB of -3
F_crossings = F(idx_all);
```

### **Interpolate for Exact Value:**

```matlab
% For even more precision
F_interp = interp1(Mag_dB, F, -3);  % Exact -3 dB frequency
```

---

## 📚 References

**Used in these exam problems:**
- F25 Problem 4-2: Lowpass filter cutoff detection
- E23 Problem 2-4: Highpass filter verification
- F24 Problem 4-3: Bandstop filter edges
- E24 Problem 2-1: Multiple filter comparison

**Course materials:**
- Week 8-11: IIR Filter Design
- Week 12-13: FIR Filter Design
- MATLAB `freqz` documentation

---

## ✅ Summary

**The `find()` method is:**
- ✅ Fast and accurate
- ✅ Reproducible (no manual reading)
- ✅ Easy to visualize (xline markers)
- ✅ Exam-friendly (quick to implement)

**Remember:**
1. High resolution (`linspace(..., 10000)`)
2. Choose correct direction (`'first'` vs `'last'`)
3. Verify with plot markers
4. Print results for documentation

---

**Master this technique → Save time on exams → Better results!** 🎯🚀
