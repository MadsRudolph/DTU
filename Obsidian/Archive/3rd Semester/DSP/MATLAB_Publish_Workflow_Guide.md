# MATLAB Publish Workflow - Lessons Learned from E25 Exam

**What went wrong and how to fix it for future exams**

---

## 🚨 Problems Encountered

### Problem 1: Plots Too Small in PDF

**What happened:**
- Figures appeared tiny in published PDF
- Hard to read axis labels and values
- Overall unprofessional appearance

**Root cause:**
- Default figure size too small for PDF output
- MATLAB publish uses screen resolution, not print resolution

**Solution:**
```matlab
% At start of script (SETUP section):
set(groot, 'defaultFigurePosition', [100 100 900 600]);
% Width=900, Height=600 gives good PDF size
```

---

### Problem 2: fprintf Boxes Didn't Render

**What happened:**
```matlab
fprintf('\n╔═══════════════════════════════════════╗\n');
fprintf('║  PROBLEM 2 (XX%%)                     ║\n');
fprintf('╚═══════════════════════════════════════╝\n\n');
```

**In PDF it looked like:**
```
âââââââââââââââââââââââââââââââââââââââââ
â PROBLEM 2 (XX%)                     â
âââââââââââââââââââââââââââââââââââââââââ
```

**Root cause:**
- Unicode box-drawing characters don't render in MATLAB publish
- fprintf output goes to PDF as-is (not formatted)

**Solution - Use MATLAB's section headers instead:**
```matlab
%% ========================================================================
%% PROBLEM 2 (30%) - IIR Filter Analysis
%% ========================================================================

%%
% *Problem 2: IIR Lowpass Filter*
%
% * Sampling frequency: Fs = 1600 Hz
% * Cutoff: 400 Hz at -3 dB
```

This renders beautifully in PDF with proper headers!

---

## ✅ The RIGHT Way to Use Publish

### Structure Your Script Like This:

```matlab
%% Title and Setup
% Your name, course, etc.

clear; close all; clc;

% Set publication defaults
set(groot, 'defaultFigurePosition', [100 100 900 600]);
set(groot, 'defaultLineLineWidth', 1.5);
set(groot, 'defaultAxesFontSize', 12);

%% ========================================================================
%% PROBLEM 1 (40%) - Main Topic
%% ========================================================================

%%
% *Section Description*
%
% * Bullet point 1
% * Bullet point 2

%% Problem 1-1: Sub-problem Title

% Your code here
fprintf('Results go here\n');

% Figure
figure('Name', 'Problem 1-1');
plot(x, y);
title('Problem 1-1: My Plot');
xlabel('X axis');
ylabel('Y axis');
grid on;

%% Problem 1-2: Next Sub-problem

% More code...
```

---

## 📊 Figure Best Practices for Publish

### Do These:

```matlab
% 1. Set figure size once at start
set(groot, 'defaultFigurePosition', [100 100 900 600]);

% 2. Name your figures
figure('Name', 'Problem 2-3: Magnitude Response');

% 3. Always add labels
xlabel('Frequency [Hz]');
ylabel('Magnitude [dB]');
title('Problem 2-3: Filter Response');
legend('H(f)', 'Cutoff');

% 4. Use grid
grid on;

% 5. Set reasonable limits
xlim([0 800]);
ylim([-60 5]);

% 6. Save high-quality images
exportgraphics(gcf, 'Problem_2_3_Magnitude_Response.png', 'Resolution', 300);
```

**Why exportgraphics?**
- Creates publication-quality images (300 DPI)
- Better than screenshots or PDF export alone
- Can be inserted into reports or presentations
- Easy to share individual figures with instructors
- Professional appearance for submission

**Best practice workflow:**
```matlab
figure('Name', 'Problem 2-3');
% ... all your plotting code ...
xlabel('...'); ylabel('...'); title('...');
grid on;
exportgraphics(gcf, 'Problem_2_3_Description.png', 'Resolution', 300);
```

### Don't Do These:

```matlab
% ❌ DON'T use close all (prevents figures from appearing in PDF)
close all;

% ✅ DO use exportgraphics AFTER plotting (creates high-quality images)
exportgraphics(gcf, 'Problem_2_3_Response.png', 'Resolution', 300);

% ❌ DON'T use tiny fonts
set(gca, 'FontSize', 8);  % Too small!

% ❌ DON'T forget to label
plot(x, y);  % No xlabel, ylabel, title - BAD!
```

**Note:** exportgraphics is GOOD! It creates high-quality images. Just use it AFTER you finish the plot.

---

## 📝 Text Formatting in Comments

MATLAB publish supports **Markdown-style formatting in comments:**

### Headers:
```matlab
%% Major Section (H1)
%%% Minor Section (H2)
```

### Formatting:
```matlab
% *bold text*
% _italic text_
% |monospace text|
```

### Lists:
```matlab
%%
% * Bullet point 1
% * Bullet point 2
%
% # Numbered item 1
% # Numbered item 2
```

### Code blocks:
```matlab
%%
%  % Indented code (4 spaces)
%  for i = 1:10
%      disp(i);
%  end
```

---

## 🎯 Recommended Template Structure

```matlab
%% DTU 62743 DSP Exam - Your Name
% Student ID: sXXXXXX
% Date: December XX, 2025

clear; close all; clc;

%% Setup
% Publication-quality defaults
set(groot, 'defaultFigurePosition', [100 100 900 600]);
set(groot, 'defaultLineLineWidth', 1.5);
set(groot, 'defaultAxesFontSize', 12);
set(groot, 'defaultAxesGridLineStyle', ':');
set(groot, 'defaultAxesGridAlpha', 0.3);

fprintf('DTU 62743 DSP Exam\n');
fprintf('Date: %s\n\n', datestr(now));

%% ========================================================================
%% PROBLEM 1 (40%%) - Z-Domain Analysis
%% ========================================================================

%%
% *Problem 1: LTI System Analysis*
%
% Given:
%
% * Zeros: -2, (1+i)/2, (1-i)/2
% * Poles: 0, 1/3, 2/3
% * Constraint: H(1) = 1

%% Problem 1-1: Pole-Zero Diagram

% Define parameters
zeros_H = [-2, (1+1i)/2, (1-1i)/2];
poles_H = [0, 1/3, 2/3];

fprintf('=== Problem 1-1 ===\n\n');
fprintf('Zeros:\n');
disp(zeros_H);

% Create figure
figure('Name', 'Problem 1-1: Pole-Zero');
zplane(poly(zeros_H), poly(poles_H));
title('Pole-Zero Diagram');
grid on;

%% Problem 1-2: Transfer Function

fprintf('=== Problem 1-2 ===\n\n');
% Your solution...

%% ========================================================================
%% PROBLEM 2 (30%%) - IIR Filter
%% ========================================================================

%%
% *Problem 2: Digital Lowpass Filter*
%
% * Sampling frequency: Fs = 1600 Hz
% * Type: Direct Form II

%% Problem 2-1: Frequency Response

% Filter coefficients
B = [0.0940, 0.3759, 0.5639, 0.3759, 0.0940];
A = [1, 0.4860, 0.0177];
Fs = 1600;

fprintf('=== Problem 2-1 ===\n\n');

% Compute frequency response
[H, F] = freqz(B, A, 10000, Fs);
Mag_dB = 20*log10(abs(H));

% Plot
figure('Name', 'Problem 2-1: Magnitude');
plot(F, Mag_dB, 'b-', 'LineWidth', 1.5);
grid on;
xlabel('Frequency [Hz]');
ylabel('Magnitude [dB]');
title('Magnitude Response');
xlim([0 Fs/2]);

%% ... Continue with other problems
```

---

## 🔧 Publishing Workflow

### Before Exam:

```matlab
% Test the publish workflow:
1. Write script with %% sections
2. Press F5 to run and check for errors
3. Click "Publish" → Select "pdf"
4. Check that PDF looks good
5. Verify all plots appear
6. Check figure sizes are readable
```

### During Exam:

```matlab
% Work incrementally:
1. Write one section
2. Press Ctrl+Enter to run just that section
3. Verify output
4. Move to next section
5. At end, press F5 to run everything
6. Publish to PDF once at the very end
```

### Common Mistakes:

```matlab
❌ Using close all       → Figures won't appear in PDF
❌ Using fprintf boxes   → Renders as garbage
❌ Not naming figures    → Hard to track in PDF
❌ Tiny figure sizes     → Unreadable in PDF
❌ No labels on plots    → Unprofessional
❌ Publishing mid-exam   → Wastes time
✅ Using exportgraphics  → GOOD! Creates high-res images
```

---

## 📊 Figure Size Guidelines

### Default (Too Small):
```matlab
% Default MATLAB figure
figure;  % Usually 560×420 pixels
```

**In PDF:** Tiny, hard to read

### Better (Readable):
```matlab
% Set at start of script
set(groot, 'defaultFigurePosition', [100 100 900 600]);
```

**In PDF:** Good size, readable

### Specific Figure Override:
```matlab
% For one particularly important figure
figure('Position', [100 100 1200 800]);
```

**In PDF:** Large and detailed

---

## ✅ Checklist Before Publishing

### Code Quality:
- [ ] Script runs without errors (F5)
- [ ] All variables are defined
- [ ] No undefined functions
- [ ] Consistent variable naming

### Figures:
- [ ] All figures have titles
- [ ] All axes have labels
- [ ] Grid is turned on
- [ ] Legends where appropriate
- [ ] Reasonable axis limits set

### Structure:
- [ ] Uses %% for major sections
- [ ] Uses %%% or comments for subsections
- [ ] fprintf for key results
- [ ] Clear problem numbering

### Formatting:
- [ ] No fprintf ASCII boxes
- [ ] No close all commands
- [ ] No exportgraphics calls
- [ ] Figure sizes set properly

---

## 🎯 Quick Reference

### Section Headers (Renders in PDF):
```matlab
%% Main Section
%%% Subsection
```

### Text Formatting in Comments:
```matlab
% *bold*
% _italic_
% |code|
% * bullet
% # numbered
```

### Figure Basics:
```matlab
figure('Name', 'Problem X-Y');
% ... plot code ...
xlabel('X'); ylabel('Y'); title('Title');
grid on;
exportgraphics(gcf, 'Problem_X_Y_Description.png', 'Resolution', 300);
```

### Results Output:
```matlab
fprintf('Key result: %.2f\n', value);
```

---

## 🚀 Pro Tips

1. **Set defaults once, forget about them:**
   ```matlab
   set(groot, 'defaultFigurePosition', [100 100 900 600]);
   set(groot, 'defaultLineLineWidth', 1.5);
   set(groot, 'defaultAxesFontSize', 12);
   ```

2. **Use named figures for organization:**
   ```matlab
   figure('Name', 'Problem 2-3: Spectrum');
   ```

3. **Write incrementally, publish once:**
   - Work section by section with Ctrl+Enter
   - Only publish at the very end
   - Saves time, catches errors early

4. **Test publish before exam:**
   - Practice with a mock exam
   - Verify PDF looks professional
   - Check all plots appear correctly

5. **Keep it simple:**
   - Don't over-format with ASCII art
   - Let MATLAB's publish do the work
   - Focus on correct results, not fancy formatting

---

## 🎓 Summary

### What Went Wrong in E25:
- Plots too small (no figure size set)
- fprintf boxes didn't render (Unicode issue)
- Not using %% section headers properly

### What to Do Next Time:
- Set figure defaults at start
- Use %% for section headers
- No ASCII art or Unicode boxes
- Test publish workflow beforehand
- **Use exportgraphics for high-quality images**

### Key Insight:
**MATLAB publish is powerful when you work WITH it, not against it.**

Use:
- ✅ %% headers
- ✅ Markdown formatting in comments
- ✅ Named figures with proper labels
- ✅ Default figure size settings
- ✅ exportgraphics for high-resolution output

Don't use:
- ❌ fprintf for structure/headers
- ❌ ASCII art boxes
- ❌ Tiny figures
- ❌ close all

---

**Follow these guidelines and your published PDFs will look professional and be easy to grade!** 📄✨
