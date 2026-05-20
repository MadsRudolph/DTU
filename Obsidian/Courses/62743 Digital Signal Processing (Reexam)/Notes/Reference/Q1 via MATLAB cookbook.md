---
type: reference
tags: [DSP, reexam, reference, z-transform, LTI, matlab, exam-day]
aliases:
  - Q1 MATLAB cookbook
  - Q1 without the math
  - Z-transform via MATLAB
  - Q1 panic sheet
---
# Q1 via MATLAB cookbook — solve Q1 without doing the math by hand

> [!info] What this note is
> Q1 ≈ **40 %** of the exam (LTI / Z-domain). It is *meant* to be solved by hand, but the exam is all-aids with MATLAB open. This note is the **fallback**: for every Q1 sub-question type → the exact commands to type, the output to read, and the Danish `Svar` sentence to write. Computed answer + stated method = real partial credit. **A computed answer always beats a blank.**
>
> By-hand theory & the math: [[LTI z-transform flow]]. Helper signatures: [[DSP MATLAB helpers cheat sheet]]. Worked Q1: [[E25 exam walkthrough]] §P1.

> [!danger] READ THE SUB-QUESTION WORDING FIRST (verified vs course policy, NotebookLM)
> `residuez`/MATLAB for Z-transform is **accepted & encouraged when MATLAB is explicitly allowed and you include commented code** — but **some Q1 sub-parts explicitly forbid MATLAB/Maple for Z-transform operations** ("*uden brug af MATLAB/Maple*"). On such a part a residuez-only answer can score **zero, not partial credit**.
> **So:** if a sub-part forbids MATLAB → still write the analytic *setup* by hand (the table pair `1/(1−a z⁻¹) ↔ aⁿu[n]`, the PFD ansatz `A/(1−p₁z⁻¹)+…`, the cover-up step) even if you can't finish the algebra. Partial method-marks > a disallowed MATLAB dump. Use this cookbook freely on every part that *doesn't* say "uden MATLAB".

---

## ⬛ 0 — GENERAL SETUP (type this first, every time)

Everything below assumes `b` (numerator) and `a` (denominator) are coefficient
vectors in **z⁻¹, ascending**: `b = [b0 b1 b2 ...]` ⇒ `b0 + b1 z⁻¹ + b2 z⁻²…`.
This is the convention `freqz`, `filter`, `residuez`, `tf(...,'z^-1')`, `impz` all use.

```matlab
% --- if you are GIVEN b, a (or a block diagram / difference eq): type them in
b = [ ... ];          % tæller (z^-1 stigende)
a = [ ... ];          % nævner (z^-1 stigende), a(1) skal være 1

% --- if you are GIVEN zeros/poles instead:
z = [ ... ];          % nulpunkter (kan være komplekse: brug 1i)
p = [ ... ];          % poler
b = real(poly(z));    % -> koeff. (poly-output ER z^-1-vektoren, venstre->højre)
a = real(poly(p));

H = tf(b, a, 1, 'Variable','z^-1')     % skriver H(z) ud (Ts=1; -1 virker også)
```

> [!danger] The three traps that will bite you
> 1. **`zplane(z,p)` argument trap.** `zplane(z,p)` only treats them as zeros/poles if they are **COLUMN** vectors. Row vectors are read as `(b,a)` coefficients → wrong plot. Use `zplane(z(:), p(:))` for zeros/poles, or `zplane(b,a)` for coefficients. **Never `zplane(z,p)` with row vectors.**
> 2. **Difference-equation sign of `a`.** Diff eq `y[n] = 0.5·y[n-1] + x[n]` → move y over: `y[n] − 0.5·y[n-1] = x[n]` ⇒ `a = [1 -0.5]`, `b = [1]`. The `a` signs are the coefficients **as they sit on the LHS after moving all y-terms left**. A `+0.5·y[n-1]` on the right becomes `-0.5` in `a`.
> 3. **Zeros/poles at z = 0.** `roots(b)` on a z⁻¹ vector misses roots at the origin. Use `tf2zpk(b,a)` — it returns the *true* z-plane zeros/poles including those at z = 0.

---

## ⬛ 1 — Difference equation → H(z)

**Sounds like:** "Find overføringsfunktionen H(z) ud fra differensligningen."

```matlab
% Eks: y[n] + 0.1 y[n-1] - 0.06 y[n-2] = x[n] + 0.2 x[n-1]
b = [1 0.2];                 % x-siden
a = [1 0.1 -0.06];           % y-siden (fortegn som de står på venstre side)
H = tf(b, a, 1, 'Variable','z^-1')
```

> [!svar] Svar-skabelon
> `% *Svar:* z-transformér begge sider (x[n-k] -> z^-k X(z)). H(z)=Y/X = `
> `% tæller/nævner som vist i H ovenfor.`

---

## ⬛ 1B — Two input/output pairs → h[n]  (linearity, NO z-transform)  ⭐ recurring Q1 opener (F24, F25)

**Sounds like:** "Systemet er LTI. x₁[n] og x₂[n] samt svarene y₁[n], y₂[n] er
givet (tabel). Bestem impulsresponsen h[n]." — *no difference equation given.*

**Trick:** find scalars `c1, c2` so that `c1·x1[n] + c2·x2[n] = δ[n]` (often the
inputs are short impulse combos, so this is just solving 2 small equations).
By **linearity** the *same* combo of the outputs is h[n]:
`h[n] = c1·y1[n] + c2·y2[n]`.

```matlab
% Eks (F24): x1=3δ[n]+2δ[n-1], x2=δ[n]+2δ[n-1]; x1-x2 = 2δ[n]  -> δ[n]=½(x1-x2)
y1 = [ ... ];  y2 = [ ... ];        % indtast tabellen, n=0..N
h  = 0.5*(y1 - y2)                  % samme linearkombination som gav δ[n]
n  = 0:numel(h)-1;
figure; stem(n, h); grid on; title('h[n] via linearitet')
```

> [!tip] How to find `c1,c2`
> Write `c1·x1 + c2·x2 = δ[n]` per sample → tiny linear system. With impulses it's
> usually obvious (subtract/scale). For δ[n−k] inputs the same logic gives a shifted δ.

> [!svar] `% *Svar:* δ[n] = c1·x1 + c2·x2 (vist). LTI-linearitet -> h[n] = c1·y1 + c2·y2 = … (se stem).`

---

## ⬛ 2 — Zeros/poles (+ gain condition) → H(z), b, a

**Sounds like:** "Systemet har nulpunkter … og poler … samt H(1)=1. Opskriv H(z)."

```matlab
z  = [-2, (1+1i)/2, (1-1i)/2];     % brug 1i, ikke i
p  = [0, 1/3, 2/3];
b0 = real(poly(z));  a0 = real(poly(p));

% Gain G så H(z1)=Hval  (her z1=1, Hval=1):
z1 = 1;  Hval = 1;
G  = Hval * polyval(a0, z1) / polyval(b0, z1)      % E25: -> 4/27 ≈ 0.1481
b  = G*b0;  a = a0;
H  = tf(b, a, 1, 'Variable','z^-1')
```

> [!svar] `% *Svar:* H(z)=G·∏(1−zₖz⁻¹)/∏(1−pₖz⁻¹), G bestemt af H(1)=1 (= 4/27). Polynomieform vist i H.`

---

## ⬛ 3 — Pole/zero plot + read them off

**Sounds like:** "Tegn pol-/nulpunktsdiagram" / "angiv poler og nulpunkter."

```matlab
figure; zplane(b, a)                    % (b,a) som RÆKKEvektorer = korrekt her
title('Pol-/nulpunktsdiagram')

[zz, pp, kk] = tf2zpk(b, a)             % SAND z-plan: fanger nul/pol ved z=0
```

> [!svar] `% *Svar:* N nulpunkter (…); M poler (…). Angiv hvilke der ligger uden for enhedscirklen (vigtigt for minimumfase, se §8).`

---

## ⬛ 4 — Stability + ROC

**Sounds like:** "Er systemet stabilt?" / "Angiv konvergensområdet (ROC)."

```matlab
poler  = roots(a)
stabil = all(abs(poler) < 1)            % 1 = stabilt (kausalt system)
ROC    = max(abs(poler))                % kausal -> ROC: |z| > denne værdi
```

| System                    | ROC                  |     |       |     |                            |
| ------------------------- | -------------------- | --- | ----- | --- | -------------------------- |
| Kausal (eksamens-default) | `                    | z   | > max | pol | ` (uden for yderste pol)   |
| Antikausal                | `                    | z   | < min | pol | ` (inden for inderste pol) |
| Tosidet                   | ring mellem to poler |     |       |     |                            |

> [!svar] `% *Svar:* Alle poler har |p|<1 -> stabilt. Kausalt -> ROC |z|>max|pol|, som indeholder enhedscirklen (bekræfter stabilitet).`

---

## ⬛ 5 — Z-transform of a given signal x[n] → X(z)

**Sounds like:** "Bestem X(z) for signalet x[n]=…" — eksamen giver typisk formlen.

**Route A — formel udleveret (mest normalt, fx E25 1-4):** indsæt tal direkte.
```matlab
% x[n]=a^n sin(w0 n) u[n], formel: a sin(w0) z^-1 / (1 - 2a cos(w0) z^-1 + a^2 z^-2)
aa = sqrt(2)/2;  w0 = pi/4;
numX = [0, aa*sin(w0)];
denX = [1, -2*aa*cos(w0), aa^2];
X = tf(numX, denX, 1, 'Variable','z^-1')
ROCx = abs(aa)                          % |z| > a
```

**Route B — symbolsk (KUN hvis Symbolic Toolbox findes — test i aften!):**
```matlab
syms n z
X = ztrans( (sqrt(2)/2)^n * sin(pi/4*n), n, z )      % -> X(z)
X = simplify(X)
```

> [!svar] `% *Svar:* Identificér a og w0, indsæt i den udleverede formel: X(z)=… , ROC |z|>|a|.`

---

## ⬛ 6 — Inverse Z-transform → h[n] or x[n] (delbrøk)

**Sounds like:** "Find h[n] / x[n] ved invers z-transformation (delbrøksopspaltning)."

**Route A — `residuez` (robust, kun Signal Toolbox — brug denne):**
```matlab
[r, pz, kdir] = residuez(b, a)
% Tolkning:  X(z) = Σ r(i)/(1 - pz(i) z^-1) + Σ kdir(l) z^-l
%            x[n] = Σ r(i)·pz(i)^n·u[n]  (+ kdir som δ[n-l])
[h, nh] = impz(b, a, 30);               % numerisk kontrol
figure; stem(nh, h); grid on; title('h[n]')
```
Reconstruér i hånden ud fra `r`,`pz`: `x[n] = r(1)*pz(1).^n + r(2)*pz(2).^n + …` for `n≥0`.

**Forsinkelse (z⁻¹-faktor i tælleren):** hvis `X(z)=z⁻¹·W(z)`, kør `residuez` på `W`,
find `w[n]`, og svar `x[n]=w[n-1]` (skift `u[n]`→`u[n-1]`, eksponent `n`→`n-1`).

**Gentagne poler:** `residuez` håndterer det selv; `impz`+`stem` viser altid det rigtige forløb — stol på plottet hvis håndformlen driller.

**Route B — symbolsk (test i aften):**
```matlab
syms z n
xN = iztrans( (1 + 0.2/z) / (1 + 0.1/z - 0.06/z^2), z, n )
```

> [!svar] `% *Svar:* residuez giver poler pz og residues r -> x[n]=Σ r(i)·pz(i)^n·u[n]. (Plot bekræfter.)`

---

## ⬛ 7 — Output y[n] for a given input x[n]

**Sounds like:** "Bestem systemets udgang y[n] når x[n]=…" eller "Y(z)=H(z)X(z)."

```matlab
% Z-domæne: Y(z)=H(z)·X(z) -> gang rationale funktioner (conv på koeff.)
numY = conv(b, numX);
denY = conv(a, denX);
Y    = minreal(tf(numY, denY, 1, 'Variable','z^-1'))   % forkorter fælles fakt.

% Tidsdomæne (numerisk svar, altid muligt):
nx = 0:30;
x  = aa.^nx .* sin(w0*nx);             % byg x[n] selv
y  = filter(b, a, x);                  % kør systemet
figure; stem(nx, y); grid on; title('y[n]')

% y[n] lukket form: residuez på (numY,denY) -> som §6
[ry, py, ky] = residuez(numY, denY)
```

> [!tip] Genvej når x[n] er en sum af impulser (F20 P3-4-typen)
> Hvis `x[n] = Σ cₖ·δ[n−kₖ]` (få vægtede/forskudte impulser): brug LTI-superposition
> direkte — **ingen Y=H·X / PFD nødvendig**:
> `y[n] = Σ cₖ·h[n−kₖ]`  (responsen på δ[n−k] er h[n−k]).
> ```matlab
> x = zeros(1,40); x(0+1)=1; x(2+1)=1;   % fx x[n]=δ[n]+δ[n-2] (1-indeks!)
> y = filter(b, a, x);                    % = h[n] + h[n-2]
> figure; stem(0:39, y); grid on
> ```

> [!tip] Pol-kollisioner
> - X's pol = H's **nulpunkt** → de udgår (`minreal` fjerner dem; PFD krymper).
> - X's pol = H's **pol** → dobbeltpol → led af typen `n·aⁿ·u[n]` (`residuez` klarer det).

> [!svar] `% *Svar:* Y(z)=H·X, fælles faktorer forkortes (minreal). Invers z (residuez) -> y[n]=… . filter()-plottet bekræfter.`

---

## ⬛ 8 — Minimum-phase / all-pass decomposition  ⭐ (recurring: E24 Q3, E25 1-7)

**Sounds like:** "Dekomponér H(z)=H_min(z)·H_ap(z)" / "gør systemet minimumfase."

Idé: et **nulpunkt uden for** enhedscirklen (`|z0|>1`) gør H ikke-minimumfase.
Spejl det ind via en all-pass: `z0 → 1/conj(z0)` (havner inde i cirklen).

```matlab
[zz, pp, kk] = tf2zpk(b, a);
out = find(abs(zz) > 1);                % nulpunkter uden for cirklen

bap = 1; aap = 1;                       % byg all-pass som produkt af sektioner
for idx = out.'
    z0   = zz(idx);
    zref = 1/conj(z0);                  % spejlet nulpunkt (inde i cirklen)
    bap  = conv(bap, [1 -z0]);          % (1 - z0 z^-1)
    aap  = conv(aap, [1 -zref]);        % (1 - zref z^-1)
end
Gap = sum(aap)/sum(bap);                % skalér så Hap(1)=1
bap = Gap*bap;
Hap = tf(bap, aap, 1, 'Variable','z^-1')
Hmin = minreal(tf(b,a,1,'Variable','z^-1') / Hap)

% VERIFICÉR all-pass: |Hap| skal være 0 dB overalt
[Hw, fw] = freqz(bap, aap, 1024);
figure; plot(fw/pi, 20*log10(abs(Hw))); grid on
xlabel('\omega/\pi'); ylabel('|H_{ap}| [dB]'); title('All-pass: flad 0 dB')
```

E25-tjek: ét nulpunkt `z0=-2` → `zref=-0.5`, `Gap=0.5`,
`Hap=(z⁻¹+½)/(1+½z⁻¹)`, |Hap|=0 dB flad. ✓

> [!svar] `% *Svar:* Nulpunkt(er) uden for cirklen -> ikke minimumfase. H=Hmin·Hap, Hap flytter z0->1/conj(z0), |Hap|=1 (0 dB, se plot). Hmin har alle nulpunkter inde i cirklen.`

---

## ⬛ 9 — Frequency response / |H|, fase, DC, Nyquist, gruppeløb

**Sounds like:** "Skitsér frekvensresponset" / "dæmpning ved …" / "DC-forstærkning."

```matlab
[Hf, w] = freqz(b, a, 1024);            % w i rad/sample (0..π)
figure
subplot(2,1,1); plot(w/pi, 20*log10(abs(Hf))); grid on; ylabel('|H| dB')
subplot(2,1,2); plot(w/pi, unwrap(angle(Hf))); grid on
xlabel('\omega/\pi'); ylabel('fase [rad]')

DC   = sum(b)/sum(a)                     % H ved z=1  (ω=0)
Nyq  = polyval(b,-1)/polyval(a,-1)       % H ved z=-1 (ω=π)  -- se note nedenfor
gd   = grpdelay(b, a, 1024);             % gruppeløb
```
*(Nyquist-tip: for et z⁻¹-vektor er `H(z=-1)` = `sum(b.*(-1).^(0:numel(b)-1)) /
sum(a.*(-1).^(0:numel(a)-1))`. `polyval(...,-1)` er kun korrekt hvis du tænker
i samme variabel — brug fortegns-summen hvis i tvivl.)*

> [!svar] `% *Svar:* aflæs |H| på datatip ved de spurgte frekvenser; fase ulineær for IIR (lineær kun for symmetrisk FIR).`

---

## ⬛ 10 — Convolution / system interconnection

**Sounds like:** "y[n]=x[n]*h[n]" / "to systemer i serie/parallel."

```matlab
y = conv(x, h);                          % foldning i tid
% Serie:    Htot = H1*H2  -> b=conv(b1,b2);  a=conv(a1,a2)
% Parallel: Htot = H1+H2  -> tf-add eller fælles nævner
Hs = minreal(tf(b1,a1,1,'Variable','z^-1') * tf(b2,a2,1,'Variable','z^-1'))
```

> [!tip] "Vis at kaskaden er FIR" (F24/F25 Q1-afslutning)
> To FIR-systemer i serie: `btot = conv(b1, b2); atot = 1`. Resultatet er FIR
> netop fordi nævneren er `1` (ingen poler ≠ 0 → endelig impulsrespons).
> `htot = conv(h1, h2)` giver impulsresponsen direkte; `stem` den og påpeg at
> den har endelig længde `= len(h1)+len(h2)-1`.

---

## ⬛ 11 — Energy / Parseval (sjælden — droppet i nyere sæt, men billig)

```matlab
[h, ~] = impz(b, a, 5000);  Eh = sum(abs(h).^2)        % numerisk energi
% x[n]=a^n u[n], |a|<1:  Ex = 1/(1-abs(a)^2)  (lukket form)
```

---

## 🟥 PANIC PROTOCOL — totally lost, just bank partial credit

Type these in order. **Every line is a defensible sub-answer**, even with zero hand-math:

```matlab
b = [ ... ];  a = [ ... ];                       % 1. opskriv koeff. (eller poly(z)/poly(p))
H = tf(b,a,1,'Variable','z^-1')                  % 2. H(z)            (§1/§2)
figure; zplane(b,a); title('pol/nul')            % 3. diagram         (§3)
[zz,pp,kk] = tf2zpk(b,a)                          % 4. nul/poler m. z=0 (§3)
stabil = all(abs(pp)<1), ROC = max(abs(pp))      % 5. stabilitet+ROC  (§4)
[h,nh] = impz(b,a,40); figure; stem(nh,h)        % 6. h[n] numerisk   (§6)
[r,pz,kd] = residuez(b,a)                         % 7. h[n] lukket form (§6)
[Hf,w] = freqz(b,a,1024);                        % 8. frekvensrespons (§9)
   figure; plot(w/pi,20*log10(abs(Hf))); grid on
y = filter(b,a,x);                               % 9. svar på input x  (§7)
```

Write a one-line Danish `% *Svar:*` after each `%%` saying *what you did and read*
(e.g. `% *Svar:* poler aflæst til … alle |p|<1 -> stabilt`). Method-in-words +
computed number = partial credit even when it's "not how they wanted it."

---

## ⚠️ TEST TONIGHT (5 minutes, before you trust this in the exam)

```matlab
ver                          % står "Symbolic Math Toolbox" på listen? -> §5B/§6B virker
which residuez               % skal findes (Signal Processing Toolbox)
which tf2zpk                 % skal findes
which zplane impz freqz      % alle skal findes
% Kør hele E25_new.m's Problem 1 top->bund: ingen fejl?  -> du er klar.
```
If Symbolic Toolbox is **not** listed: ignore every Route B; `residuez`/`impz`/
`filter` cover everything anyway.

---

# Links
- [[LTI z-transform flow]] — the by-hand method & theory (read alongside)
- [[E25 exam walkthrough]] — §P1 fully worked (this cookbook reproduces it)
- [[DSP MATLAB helpers cheat sheet]] — helper signatures
- [[FIR window design flow]] — Q3 · [[Filter analysis and FFT flow]] — Q2
- [[62743 Digital Signal Processing (Reexam)]] — hub
