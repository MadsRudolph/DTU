# DSP Exam MATLAB Template - Quick Reference (Publish Workflow)

**Optimized for MATLAB's publish-to-PDF feature**

---

## 🚀 Quick Start (2 Minutes)

### At Exam Start:
1. ✅ Open `DSP_Exam_Template_OPTIMIZED.m` in MATLAB
2. ✅ Run SETUP section (Ctrl+Enter on that section)
3. ✅ Fill in your name and s-number in header
4. ✅ Read all 3 problems

### During Exam:
1. ✅ Paste problem text into appropriate section
2. ✅ Uncomment relevant template code
3. ✅ Adapt to your problem
4. ✅ Run section-by-section (Ctrl+Enter)
5. ✅ Figures appear automatically - no export needed!

### At Exam End:
1. ✅ Verify entire script runs (press F5)
2. ✅ Click "Publish" button (top toolbar)
3. ✅ Select "pdf" format
4. ✅ Wait ~30 seconds
5. ✅ Rename PDF: `Mads_DSP_Exam_Dec2025.pdf`
6. ✅ Submit!

---

## 📄 The Publish Magic

### Key Concept: NO MANUAL EXPORT NEEDED!

**Old workflow (Obsidian/Images):**
```matlab
figure;
plot(x, y);
title('My Plot');
exportgraphics(gcf, 'Images/plot.png', 'Resolution', 300);  % Manual!
```

**New workflow (Publish):**
```matlab
figure;
plot(x, y);
title('My Plot');
% Done! Publish captures it automatically! ✨
```

### What Publish Does:

1. **Runs your entire script** → Executes all code
2. **Captures all fprintf** → Text output appears in PDF
3. **Captures all figures** → Auto-embedded as high-quality images
4. **Formats sections** → `%%` becomes PDF headers
5. **Processes markdown** → `% *text*` becomes *italic*, etc.
6. **Generates PDF** → Ready to submit!

---

## 📊 Problem Type Recognition (30 sec)

| Keywords in Problem | Type | Template # | Time |
|---------------------|------|------------|------|
| "Butterworth", "bilinear" | IIR design | Problem 2-2 | 20 min |
| "FIR", "linear phase", "windowing" | FIR design | Problem 3-2 | 15 min |
| "magnitude response", "cutoff" | Frequency analysis | Problem 2-3 | 10 min |
| "poles", "zeros", "stability" | Pole-zero | Problem 2-4 | 8 min |
| "sample", "aliasing", "Nyquist" | Sampling | Problem 3-4 | 5 min |
| "filter the signal" | Apply filter | Problem 3-5 | 5 min |
| "block diagram", "H(z)" | Structure ID | Template 6 | 10 min |

---

## ⚡ Ready-to-Use Code Snippets

### Snippet 1: IIR Butterworth with BLT
```matlab
% Specs
Ap=3; As=40; Fp=2000; Fs_band=3000; Fs=10000;

% Prewarp (CRITICAL!)
wp=2*pi*Fp/Fs; ws=2*pi*Fs_band/Fs;
T=1/Fs;
Omega_p=(2/T)*tan(wp/2);
Omega_s=(2/T)*tan(ws/2);

% Design & transform
[N,Wn]=buttord(Omega_p,Omega_s,Ap,As,'s');
[b_s,a_s]=butter(N,Wn,'s');
[b,a]=bilinear(b_s,a_s,Fs);

fprintf('Order: N = %d\n', N);
```

### Snippet 2: Auto Cutoff Detection
```matlab
% High resolution for accuracy
F_vec=linspace(0,Fs/2,10000);
[H,F]=freqz(b,a,F_vec,Fs);
Mag_dB=20*log10(abs(H));

% Find cutoff (lowpass: last point >= -3 dB)
idx=find(Mag_dB>=-3,1,'last');
F_cutoff=F(idx);

fprintf('Cutoff: %.1f Hz\n', F_cutoff);
```

### Snippet 3: Stability Check with Output
```matlab
poles_H=roots(a);

fprintf('\n═══ Stability Check ═══\n');
fprintf('Criterion: All |p| < 1\n\n');

stable=true;
for i=1:length(poles_H)
    mag=abs(poles_H(i));
    fprintf('Pole %d: |p| = %.4f', i, mag);
    if mag<1
        fprintf(' → STABLE ✓\n');
    else
        fprintf(' → UNSTABLE ✗\n');
        stable=false;
    end
end

if stable
    fprintf('\n✓ Filter is stable\n');
end
```

### Snippet 4: Magnitude Response Plot
```matlab
figure('Name', 'Problem 2-3');
F_vec=linspace(0,Fs/2,10000);
[H,F]=freqz(b,a,F_vec,Fs);
Mag_dB=20*log10(abs(H));

plot(F,Mag_dB,'b','LineWidth',1.5);
hold on;
xline(F_cutoff,'--g',sprintf('%.1f Hz',F_cutoff));
yline(-3,'--r','-3 dB');
hold off;

xlabel('Frequency [Hz]');
ylabel('Magnitude [dB]');
title('Filter Magnitude Response');
grid on;
xlim([0 Fs/2]);
legend('H(f)','Measured','−3 dB','Location','best');
% Auto-captured by publish!
```

### Snippet 5: Overlay Plot (Input vs Filtered)
```matlab
figure('Name', 'Problem 3-5');
plot(t,x,'b','LineWidth',1.5);
hold on;
plot(t,y,'r','LineWidth',1.5);
hold off;

xlabel('Time [s]');
ylabel('Amplitude');
title('Input vs Filtered Output');
legend('Input','Filtered');
grid on;
xlim([0 0.05]);
% Auto-captured by publish!
```

### Snippet 6: Aliasing Verification
```matlab
F_Nyq=Fs/2;
frequencies=[F1,F2];

fprintf('\n═══ Aliasing Check ═══\n');
fprintf('Nyquist: %.0f Hz\n\n', F_Nyq);

for i=1:length(frequencies)
    F=frequencies(i);
    fprintf('F%d = %.0f Hz: ',i,F);
    if F<F_Nyq
        fprintf('%.0f < %.0f → OK ✓\n',F,F_Nyq);
    else
        fprintf('%.0f >= %.0f → ALIAS ⚠️\n',F,F_Nyq);
    end
end
```

---

## 🎯 Exam Time Strategy (4 hours)

| Activity | Time | Tips |
|----------|------|------|
| **Read all 3 problems** | 10 min | Identify types, estimate difficulty |
| **Problem 1** | 70 min | Start with easiest sub-parts |
| **Problem 2** | 70 min | Use templates, verify as you go |
| **Problem 3** | 70 min | Run incrementally, check results |
| **Review & Publish** | 20 min | Test F5, then publish to PDF |

### Within Each Problem (70 min):

```
Read carefully        →  5 min
Identify templates    →  2 min
Code solution        → 35 min  (Use templates!)
Verify results       →  8 min  (Run verification patterns)
Make plots           → 10 min  (Will auto-capture)
Document/comment     → 10 min
```

---

## 💡 Pro Tips for Beautiful PDFs

### ✅ DO These:

1. **Use descriptive figure names:**
   ```matlab
   figure('Name', 'Problem 2-3: Magnitude Response');
   ```

2. **Label everything:**
   ```matlab
   xlabel('Frequency [Hz]');
   ylabel('Magnitude [dB]');
   title('Problem 2-3: Filter Magnitude Response');
   legend('H(f)', 'Cutoff', '-3 dB', 'Location', 'best');
   ```

3. **Use fprintf for results:**
   ```matlab
   fprintf('\n📊 Result 2-3:\n');
   fprintf('  Cutoff: %.1f Hz\n', F_cutoff);
   fprintf('  Order: N = %d\n', N);
   ```

4. **Use section headers:**
   ```matlab
   %% Problem 2-3: Magnitude Response
   % *Task:* Plot and find cutoff frequency
   ```

5. **Keep figures open:**
   ```matlab
   % DON'T use "close all" in problem sections!
   % Publish needs figures open to capture them
   ```

### ❌ DON'T Do These:

1. ❌ Leave plots unlabeled
2. ❌ Forget to uncomment working code
3. ❌ Use `close all` (closes figures before capture)
4. ❌ Have syntax errors (prevents publish)
5. ❌ Forget to run entire script before publishing

---

## 🔧 Template Structure

### Main Sections (Already in Template):

```
%% SETUP
   → Run first! Sets defaults, clears workspace

%% PROBLEM 1 (XX%)
   %% Problem 1-1: [Title]
   %% Problem 1-2: [Title]
   ...

%% PROBLEM 2 (XX%)
   %% Problem 2-1: [Title]
   %% Problem 2-2: IIR Filter Design
      → Complete BLT template ready
   %% Problem 2-3: Magnitude Response
      → Cutoff detection ready
   %% Problem 2-4: Stability Check
      → Verification pattern ready
   ...

%% PROBLEM 3 (XX%)
   %% Problem 3-1: [Title]
   %% Problem 3-2: FIR Design
      → Windowing template ready
   %% Problem 3-3: Linear Phase Check
      → Symmetry verification ready
   %% Problem 3-4: Aliasing Check
      → Verification pattern ready
   %% Problem 3-5: Filtering
      → Overlay plot template ready
   ...

%% UTILITY TEMPLATES
   → 7 copy-paste templates for common tasks
```

---

## ⚠️ Common Issues & Fixes

### Issue 1: "Publish failed - error in code"
**Solution:** Run entire script (F5) first to find error

### Issue 2: "Figures don't appear in PDF"
**Solution:** Don't use `close all`, keep figures open

### Issue 3: "PDF has wrong formatting"
**Solution:** Use `%%` for sections, `% *text*` for emphasis

### Issue 4: "Published PDF is huge"
**Solution:** Normal! High-quality figures are large, it's OK

### Issue 5: "Can't find published PDF"
**Solution:** Same folder as .m file, named `html/[filename].pdf`

---

## 📋 Pre-Submit Checklist

**Before clicking "Publish":**

- [ ] Run entire script (F5) - no errors?
- [ ] All fprintf output shows important results?
- [ ] All plots have xlabel, ylabel, title, legend?
- [ ] All problems attempted?
- [ ] Stability checked (if IIR)?
- [ ] Aliasing checked (if sampling)?
- [ ] Units included in results?
- [ ] Name and s-number in header?

**After publishing:**

- [ ] PDF generated successfully?
- [ ] All figures appear in PDF?
- [ ] All text output visible?
- [ ] PDF is readable?
- [ ] Renamed to: `Mads_DSP_Exam_Dec2025.pdf`?

---

## 🎓 DTU-Specific Reminders

### Critical Formulas:

**BLT Prewarping (DON'T FORGET!):**
```matlab
Ω = (2/T) * tan(ω/2)  where T = 1/Fs
```

**Linear Phase (Symmetric FIR):**
```matlab
Factor out: e^(-jω M/2)
Check: h[k] = h[M-k]
```

**Stability:**
```matlab
IIR stable ⟺ all |poles| < 1
```

**Aliasing:**
```matlab
No alias ⟺ all F_signal < F_Nyquist = Fs/2
```

### Notation:
- **Ω** (capital omega) = Analog frequency [rad/s]
- **ω** (lowercase omega) = Digital frequency [rad/sample]

---

## ⚡ Speed Tips

**Fastest way to solve each problem type:**

1. **IIR Design (20 min):**
   - Copy Problem 2-2 template
   - Fill in specs
   - Run → Done

2. **Cutoff Detection (5 min):**
   - Copy snippet 2
   - Run → Get result

3. **Stability (5 min):**
   - Copy snippet 3
   - Run → Verified

4. **Aliasing (3 min):**
   - Copy snippet 6
   - Run → Checked

**Total time saved: ~30 minutes per exam!**

---

## 🚀 You're Ready!

**Tomorrow:**
1. Stay calm 😌
2. Use templates 🔧
3. Run incrementally ▶️
4. Verify results ✅
5. Publish at end 📄
6. Submit! 🎯

**Good luck, Mads!** 💪🚀

---

## Quick Command Reference

```matlab
% Filter design
[N,Wn]=buttord(Ωp,Ωs,Ap,As,'s'); [b,a]=butter(N,Wn,'s');
b=fir1(N,fc/(Fs/2),'low',hamming(N+1));

% Analysis
[H,F]=freqz(b,a,10000,Fs);
p=roots(a); z=roots(b);
zplane(b,a);

% Filtering
y=filter(b,a,x);

% BLT
[b,a]=bilinear(b_s,a_s,Fs);

% Display
H_sys=tf(b,a,1/Fs,'Variable','z^-1');
```
