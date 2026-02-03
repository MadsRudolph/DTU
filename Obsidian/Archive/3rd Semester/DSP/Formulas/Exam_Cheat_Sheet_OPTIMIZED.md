# DSP Exam Cheat Sheet - Publish Workflow Edition

**DTU 62743 - December 12, 2025 - 4 hours - 3 problems**

**📄 SUBMISSION: Use MATLAB Publish → PDF (all figures auto-included!)**

---

## 🎯 Exam Day Workflow

```
1. Open template → 2. Run SETUP → 3. Solve problems → 
4. Press F5 (verify) → 5. Publish to PDF → 6. Submit!
```

**NO manual export needed - publish captures everything!** ✨

---

## ⚡ MATLAB Quick Commands

### Filter Design
```matlab
% Butterworth IIR
[N,Wn]=buttord(Ωp,Ωs,Ap,As,'s'); [b,a]=butter(N,Wn,'s');
[b,a]=bilinear(b_s,a_s,Fs);  % BLT

% FIR Windowing
b=fir1(N, fc/(Fs/2), 'low', hamming(N+1)); a=1;
```

### Analysis
```matlab
% Frequency response (Hz)
[H,F]=freqz(b,a,10000,Fs); Mag_dB=20*log10(abs(H));

% Poles/Zeros
p=roots(a); z=roots(b); zplane(b,a);

% Cutoff (lowpass)
idx=find(Mag_dB>=-3,1,'last'); F_cut=F(idx);

% Stability
if all(abs(p)<1), disp('STABLE'); end

% Filter signal
y=filter(b,a,x);
```

---

## 🎯 Problem Type Recognition (30 sec)

| Keywords | Type | Action |
|----------|------|--------|
| "Butterworth", "BLT" | IIR design | Prewarp→Design→BLT |
| "FIR", "linear phase" | FIR design | fir1 or symmetric |
| "Block diagram" | Structure | Count delays, identify |
| "Sample", "aliasing" | Sampling | F < Fs/2? |
| "Stability" | Pole check | \|p\| < 1? |

---

## 📐 Critical Formulas

### Bilinear Transform
```
Prewarping: Ω = (2/T)tan(ω/2)  where T=1/Fs
Digital→Analog, then use bilinear()
```

### Linear Phase FIR
```
Symmetric: b[k] = b[M-k]
Phase: φ(ω) = -ω(M/2)  (linear!)
Factor: H(e^jω) = e^(-jω M/2) × [Real amplitude]
```

### Stability
```
IIR stable ⟺ All |poles| < 1
FIR always stable (no feedback)
```

### Aliasing
```
No aliasing ⟺ All F_signal < F_Nyquist = Fs/2
```

---

## ✅ Verification Patterns (Copy-Paste)

### Pattern 1: Stability
```matlab
fprintf('\n=== Stability ===\n');
for i=1:length(p)
    mag=abs(p(i));
    if mag<1, fprintf('Pole %d: %.4f ✓\n',i,mag);
    else fprintf('Pole %d: %.4f ✗ UNSTABLE\n',i,mag); end
end
```

### Pattern 2: Aliasing
```matlab
fprintf('\n=== Aliasing ===\n');
F_Nyq=Fs/2;
for i=1:length(freqs)
    if freqs(i)<F_Nyq, fprintf('F%d: %.0f Hz ✓\n',i,freqs(i));
    else fprintf('F%d: %.0f Hz ✗ ALIAS\n',i,freqs(i)); end
end
```

---

## 📊 Common Plot Templates

### Magnitude + Phase
```matlab
[H,F]=freqz(b,a,1024,Fs);
subplot(2,1,1); plot(F,20*log10(abs(H))); ylabel('Mag [dB]');
subplot(2,1,2); plot(F,unwrap(angle(H))*180/pi); ylabel('Phase');
```

### Overlay (Input vs Filtered)
```matlab
plot(t,x,'b'); hold on; plot(t,y,'r'); hold off;
legend('Input','Filtered');
```

### Publishing
```matlab
% When done:
% 1. Run entire script: Home → Run → Run
% 2. Publish to PDF: Home → Publish → PDF
% All figures auto-included!
```

---

## 🔍 Structure Identification (1 min)

```
No feedback?           → FIR
Two delay chains?      → IIR Direct Form I
One shared delay chain → IIR Direct Form II

Direct Form I delays: M + N
Direct Form II delays: max(M,N)
```

---

## ⏱️ Time Budget (4 hours)

| Problem | Time | Priority |
|---------|------|----------|
| Read all | 10 min | Do first |
| Problem 1 | 70 min | 33% |
| Problem 2 | 70 min | 33% |
| Problem 3 | 70 min | 33% |
| Review | 20 min | Final check |

**Within each problem:**
- Easy points first (aliasing, stability checks)
- Plots as you go (don't save for end)
- Verify immediately (don't accumulate errors)

---

## 🚨 Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forget prewarp | Ω=(2/T)tan(ω/2) ALWAYS |
| Wrong norm | fir1: fc/(Fs/2) |
| No stability | Check \|roots(a)\|<1 |
| No units | Add [Hz], [dB], etc |
| Plots unlabeled | xlabel, ylabel, title |

---

## 💡 Easy Points (Grab These!)

1. **Aliasing check** (2 min): F < Fs/2?
2. **Stability** (3 min): |p| < 1?
3. **Cutoff detection** (5 min): Use find()
4. **Pole-zero plot** (5 min): zplane(b,a)

**Total: 15 min = ~15 points**

---

## 🎓 DTU-Specific

**Notation:**
- Ω (Omega): Analog [rad/s]
- ω (omega): Digital [rad/sample]

**Methods:**
- Step→Impulse: h[n]=y_step[n]-y_step[n-1]
- Linear phase: Factor out e^(-jω M/2)
- BLT: ALWAYS prewarp first

**Red flags:**
- Feedback → IIR (check stability!)
- Denominator ≠ 1 → IIR
- Two chains → Direct Form I

---

## 📋 Final Checklist

Before submit:
- [ ] All plots labeled (xlabel, ylabel, title)
- [ ] All results stated clearly (fprintf)
- [ ] Units included
- [ ] Stability checked (IIR)
- [ ] Code runs (Run All)
- [ ] Published to PDF
- [ ] PDF saved with your name

---

**You're ready! Stay calm, work systematically, verify as you go.** 🚀

**Good luck, Mads!** 💪🎯
