# DSP Verification Pattern — General Template

**A systematic approach to checking specifications, conditions, and criteria in DSP problems**

---

## 🎯 The General Pattern

```matlab
% STEP 1: Calculate criterion/threshold
threshold = ... ;  % What you're comparing against

% STEP 2: State what you're checking
fprintf('\n=== Checking [WHAT] ===\n');
fprintf('[Criterion name]: %.2f\n\n', threshold);

% STEP 3: Loop through items to check (or check individually)
for i = 1:N
    value = ... ;  % The value to check
    
    % Display the item
    fprintf('[Item %d]: [name] = %.2f\n', i, value);
    
    % Apply criterion with clear comparison
    if value [CONDITION] threshold
        fprintf('  %.2f [OPERATOR] %.2f → [PASS MESSAGE] ✓\n\n', value, threshold);
    else
        fprintf('  %.2f [OPERATOR] %.2f → [FAIL MESSAGE] ⚠️\n\n', value, threshold);
    end
end

% STEP 4: Overall conclusion
fprintf('Conclusion: [SUMMARY]\n\n');
```

---

## 📚 Common DSP Verification Templates

### **1. ALIASING CHECK**

**Use when:** Checking if sampling frequency is sufficient

```matlab
%% Aliasing Verification Template

% Criterion
F_Nyquist = Fs/2;

fprintf('\n=== Aliasing Check ===\n');
fprintf('Nyquist frequency: %.0f Hz\n\n', F_Nyquist);

% Check each frequency component
frequencies = [F1, F2, F3];  % List of frequencies to check
names = {'F1', 'F2', 'F3'};  % Names for each

for i = 1:length(frequencies)
    F = frequencies(i);
    fprintf('Component %d: %s = %.0f Hz\n', i, names{i}, F);
    
    if F < F_Nyquist
        fprintf('  %.0f < %.0f → NO aliasing ✓\n\n', F, F_Nyquist);
    else
        fprintf('  %.0f >= %.0f → ALIASING! ⚠️\n\n', F, F_Nyquist);
    end
end
```

**Example output:**
```
=== Aliasing Check ===
Nyquist frequency: 2500 Hz

Component 1: F1 = 50 Hz
  50 < 2500 → NO aliasing ✓

Component 2: F2 = 1000 Hz
  1000 < 2500 → NO aliasing ✓
```

---

### **2. STABILITY CHECK (Poles)**

**Use when:** Verifying BIBO stability from pole locations

```matlab
%% Stability Verification Template

% Find poles
poles = roots(A);

fprintf('\n=== Stability Check ===\n');
fprintf('Criterion: All poles must satisfy |p| < 1\n\n');

% Check each pole
for i = 1:length(poles)
    p_mag = abs(poles(i));
    fprintf('Pole %d: |p%d| = %.4f\n', i, i, p_mag);
    
    if p_mag < 1
        fprintf('  %.4f < 1 → Inside unit circle ✓\n\n', p_mag);
    elseif abs(p_mag - 1) < 1e-6
        fprintf('  %.4f = 1 → On unit circle (marginal) ⚠️\n\n', p_mag);
    else
        fprintf('  %.4f > 1 → Outside unit circle ✗\n\n', p_mag);
    end
end

% Overall conclusion
if all(abs(poles) < 1)
    fprintf('✓ STABLE: All poles inside unit circle\n');
elseif any(abs(poles) > 1)
    fprintf('✗ UNSTABLE: Pole(s) outside unit circle\n');
else
    fprintf('⚠ MARGINALLY STABLE: Pole(s) on unit circle\n');
end
```

**Example output:**
```
=== Stability Check ===
Criterion: All poles must satisfy |p| < 1

Pole 1: |p1| = 0.8342
  0.8342 < 1 → Inside unit circle ✓

Pole 2: |p2| = 0.8342
  0.8342 < 1 → Inside unit circle ✓

Pole 3: |p3| = 0.3618
  0.3618 < 1 → Inside unit circle ✓

✓ STABLE: All poles inside unit circle
```

---

### **3. FREQUENCY BAND CHECK (Passband/Stopband)**

**Use when:** Checking if frequencies fall in passband or stopband

```matlab
%% Frequency Band Verification Template

% Filter specification
F_cutoff = 400;  % Hz

fprintf('\n=== Frequency Band Check ===\n');
fprintf('Filter cutoff: %.0f Hz\n\n', F_cutoff);

% Check each frequency
frequencies = [50, 1000, 2000];
names = {'F1', 'F2', 'F3'};

for i = 1:length(frequencies)
    F = frequencies(i);
    fprintf('Component %d: %s = %.0f Hz\n', i, names{i}, F);
    
    if F < F_cutoff
        fprintf('  %.0f < %.0f → PASSBAND (passes) ✓\n\n', F, F_cutoff);
    else
        fprintf('  %.0f > %.0f → STOPBAND (attenuated) ✓\n\n', F, F_cutoff);
    end
end
```

**Example output:**
```
=== Frequency Band Check ===
Filter cutoff: 400 Hz

Component 1: F1 = 50 Hz
  50 < 400 → PASSBAND (passes) ✓

Component 2: F2 = 1000 Hz
  1000 > 400 → STOPBAND (attenuated) ✓
```

---

### **4. ATTENUATION SPECIFICATION CHECK**

**Use when:** Verifying if attenuation meets requirements

```matlab
%% Attenuation Verification Template

% Specifications
A_pass_max = 3;    % Max passband attenuation (dB)
A_stop_min = 30;   % Min stopband attenuation (dB)

fprintf('\n=== Attenuation Specification Check ===\n');
fprintf('Passband spec: ≤ %.1f dB\n', A_pass_max);
fprintf('Stopband spec: ≥ %.1f dB\n\n', A_stop_min);

% Check passband frequencies
passband_freqs = [100, 200, 300];
for i = 1:length(passband_freqs)
    F = passband_freqs(i);
    [H, ~] = freqz(B, A, [F], Fs);
    A_dB = -20*log10(abs(H));  % Attenuation (positive)
    
    fprintf('Passband @ %.0f Hz: %.2f dB\n', F, A_dB);
    
    if A_dB <= A_pass_max
        fprintf('  %.2f ≤ %.1f → PASSES ✓\n\n', A_dB, A_pass_max);
    else
        fprintf('  %.2f > %.1f → FAILS ✗\n\n', A_dB, A_pass_max);
    end
end

% Check stopband frequencies
stopband_freqs = [800, 1000, 1500];
for i = 1:length(stopband_freqs)
    F = stopband_freqs(i);
    [H, ~] = freqz(B, A, [F], Fs);
    A_dB = -20*log10(abs(H));
    
    fprintf('Stopband @ %.0f Hz: %.2f dB\n', F, A_dB);
    
    if A_dB >= A_stop_min
        fprintf('  %.2f ≥ %.1f → PASSES ✓\n\n', A_dB, A_stop_min);
    else
        fprintf('  %.2f < %.1f → FAILS ✗\n\n', A_dB, A_stop_min);
    end
end
```

---

### **5. CUTOFF FREQUENCY VERIFICATION**

**Use when:** Checking if measured cutoff matches specification

```matlab
%% Cutoff Frequency Verification Template

% Specification
F_cutoff_spec = 400;  % Hz
tolerance = 10;       % Hz

% Measure actual cutoff
F = linspace(0, Fs/2, 10000);
[H, F_resp] = freqz(B, A, F, Fs);
Mag_dB = 20*log10(abs(H));
idx = find(Mag_dB >= -3, 1, 'last');
F_cutoff_meas = F_resp(idx);

fprintf('\n=== Cutoff Frequency Verification ===\n');
fprintf('Specified: %.0f Hz\n', F_cutoff_spec);
fprintf('Measured:  %.2f Hz\n', F_cutoff_meas);
fprintf('Tolerance: ±%.0f Hz\n\n', tolerance);

% Check if within tolerance
error = abs(F_cutoff_meas - F_cutoff_spec);
fprintf('Error: %.2f Hz\n', error);

if error <= tolerance
    fprintf('  %.2f ≤ %.0f → WITHIN TOLERANCE ✓\n', error, tolerance);
else
    fprintf('  %.2f > %.0f → OUTSIDE TOLERANCE ✗\n', error, tolerance);
end
```

---

### **6. FILTER ORDER CHECK**

**Use when:** Verifying if calculated order meets specifications

```matlab
%% Filter Order Verification Template

% Calculate required order
n_calc = ...;  % Your calculation
n_used = ceil(n_calc);  % Round up

fprintf('\n=== Filter Order Check ===\n');
fprintf('Calculated order: %.2f\n', n_calc);
fprintf('Used order:       %d\n\n', n_used);

if n_used >= n_calc
    fprintf('  %d ≥ %.2f → ORDER SUFFICIENT ✓\n', n_used, n_calc);
else
    fprintf('  %d < %.2f → ORDER INSUFFICIENT ✗\n', n_used, n_calc);
end

% Verify specifications are met
fprintf('\nVerifying specifications with n = %d:\n', n_used);
% ... check attenuation at key frequencies
```

---

### **7. LINEAR PHASE CHECK (FIR Symmetry)**

**Use when:** Verifying FIR filter has linear phase

```matlab
%% Linear Phase Verification Template

% Check impulse response symmetry
h = B;  % Impulse response
M = length(h) - 1;

fprintf('\n=== Linear Phase Check ===\n');
fprintf('Criterion: h[n] must be symmetric (Type I/II) or antisymmetric (Type III/IV)\n\n');

% Check symmetry
is_symmetric = true;
fprintf('Checking h[n] = h[M-n]:\n');
for n = 0:floor(M/2)
    if abs(h(n+1) - h(M-n+1)) > 1e-10
        is_symmetric = false;
        fprintf('  h[%d] ≠ h[%d] ✗\n', n, M-n);
    else
        fprintf('  h[%d] = h[%d] ✓\n', n, M-n);
    end
end

if is_symmetric
    fprintf('\n✓ SYMMETRIC: Filter has linear phase\n');
else
    fprintf('\n✗ NOT SYMMETRIC: Filter does NOT have linear phase\n');
end
```

---

### **8. GENERAL THRESHOLD CHECK**

**Use when:** Any threshold-based verification

```matlab
%% General Threshold Verification Template

% Define what you're checking
values = [...];      % Array of values to check
names = {...};       % Names for each value
threshold = ...;     % Threshold value
operator = '<';      % '<', '>', '<=', '>='
pass_msg = 'PASSES';
fail_msg = 'FAILS';

fprintf('\n=== [Description] Check ===\n');
fprintf('Criterion: [what] %s %.2f\n\n', operator, threshold);

for i = 1:length(values)
    val = values(i);
    fprintf('%s: %.2f\n', names{i}, val);
    
    % Apply check based on operator
    switch operator
        case '<'
            passes = val < threshold;
        case '<='
            passes = val <= threshold;
        case '>'
            passes = val > threshold;
        case '>='
            passes = val >= threshold;
    end
    
    if passes
        fprintf('  %.2f %s %.2f → %s ✓\n\n', val, operator, threshold, pass_msg);
    else
        fprintf('  %.2f %s %.2f → %s ✗\n\n', val, operator, threshold, fail_msg);
    end
end
```

---

## 🎨 Formatting Best Practices

### **Visual Indicators:**
```matlab
✓  % Pass/Success
✗  % Fail/Error  
⚠️  % Warning/Marginal
```

### **Consistent Structure:**
1. **Header:** What you're checking
2. **Criterion:** The rule/threshold
3. **Item-by-item:** Check each with clear comparison
4. **Conclusion:** Overall result

### **Clear Comparisons:**
```matlab
fprintf('  %.2f < %.2f → RESULT\n', value, threshold);
%      ^value  ^operator  ^threshold    ^what it means
```

### **Section Separators:**
```matlab
fprintf('\n=== Section Name ===\n');  % Start of section
fprintf('\n');                         % Between items
fprintf('---\n\n');                    % Between major sections
```

---

## 📋 Quick Copy-Paste Template

```matlab
%% [VERIFICATION NAME]

% Step 1: Define criterion
threshold = ...;

% Step 2: Start verification
fprintf('\n=== [What You're Checking] ===\n');
fprintf('Criterion: [description]\n\n');

% Step 3: Check each item
items = [...];
for i = 1:length(items)
    val = items(i);
    fprintf('[Item %d]: %.2f\n', i, val);
    
    if val [OPERATOR] threshold
        fprintf('  %.2f [OP] %.2f → [PASS] ✓\n\n', val, threshold);
    else
        fprintf('  %.2f [OP] %.2f → [FAIL] ✗\n\n', val, threshold);
    end
end

% Step 4: Conclusion
fprintf('[Overall conclusion]\n\n');
```

---

## 💡 Exam Strategy

**Why this pattern is powerful:**

1. **Clear documentation** - Shows your thinking process
2. **Easy to debug** - Spot errors immediately
3. **Professional** - Looks organized and systematic
4. **Time-saving** - Copy-paste and modify
5. **Error-proof** - Hard to miss a requirement

**When to use:**
- ✅ Specification checks (aliasing, attenuation, cutoff)
- ✅ Stability verification (poles, zeros)
- ✅ Multiple-item checks (frequencies, poles, filters)
- ✅ Any criterion-based verification

**Time estimate:** 30 seconds to adapt template for any check ⚡

---

## 📚 Example: Complete Problem Check

```matlab
%% Complete Verification Example: Problem 4-4 & 4-5

%--- Check 1: Aliasing ---
F_Nyquist = Fs/2;
fprintf('\n=== Check 1: Aliasing ===\n');
fprintf('Nyquist: %.0f Hz\n\n', F_Nyquist);

freqs = [50, 1000];
for i = 1:length(freqs)
    F = freqs(i);
    fprintf('F%d = %.0f Hz: ', i, F);
    if F < F_Nyquist
        fprintf('%.0f < %.0f → NO aliasing ✓\n', F, F_Nyquist);
    else
        fprintf('%.0f ≥ %.0f → ALIASING ✗\n', F, F_Nyquist);
    end
end

%--- Check 2: Filter Bands ---
F_cutoff = 400;
fprintf('\n=== Check 2: Filter Effect ===\n');
fprintf('Cutoff: %.0f Hz\n\n', F_cutoff);

for i = 1:length(freqs)
    F = freqs(i);
    fprintf('F%d = %.0f Hz: ', i, F);
    if F < F_cutoff
        fprintf('%.0f < %.0f → Passband ✓\n', F, F_cutoff);
    else
        fprintf('%.0f > %.0f → Stopband ✓\n', F, F_cutoff);
    end
end

fprintf('\n✓ All checks passed!\n');
```

---

**Master this pattern → Faster exams → Better documentation!** 🎯🚀
