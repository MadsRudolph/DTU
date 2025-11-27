> Quick refs: [[Under-sampling of Passband Signals]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 12 Torsdag.pdf]]  
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 12 Torsdag solutions.pdf]]  
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE12/Torsdag.mlx>)

---

# Week 12 — Under-sampling of Passband Signals (Thursday)

We look at **bandpass / under-sampling** of a double-sideband modulated cosine.

The analog signal is

$$
x_a(t) = \cos(2\pi F_\text{data} t)\cos(2\pi F_\text{carrier} t)
$$

with

- $F_\text{data} = 1~\text{kHz}$
- $F_\text{carrier} = 16~\text{kHz}$

So it’s a narrowband data signal around a high carrier.

---

## Exercise 1

### 1-A) Complex exponential representation (positive and negative frequencies)

Use the identity

$$
\cos(2\pi f t) = \frac{1}{2}\left(e^{j2\pi f t} + e^{-j2\pi f t}\right)
$$

and the product–to–sum identity

$$
\cos A\cos B=\frac{1}{2}\left[\cos(A+B)+\cos(A-B)\right].
$$

We get

$$
x_a(t) = \frac{1}{2}\cos\!\big(2\pi(F_\text{carrier}+F_\text{data})t\big)
       + \frac{1}{2}\cos\!\big(2\pi(F_\text{carrier}-F_\text{data})t\big).
$$

Numerically:

- $F_\text{carrier}+F_\text{data} = 16+1 = 17~\text{kHz}$
- $F_\text{carrier}-F_\text{data} = 16-1 = 15~\text{kHz}$

So

$$
x_a(t)=\tfrac{1}{2}\cos(2\pi\cdot 17\text{kHz}\,t)
      +\tfrac{1}{2}\cos(2\pi\cdot 15\text{kHz}\,t).
$$

In terms of **positive and negative frequencies** (complex exponentials):

$$
\begin{aligned}
x_a(t)
  &= \frac{1}{4}
     \Big(
       e^{j2\pi 17\text{kHz}\, t}
     + e^{-j2\pi 17\text{kHz}\, t}
     + e^{j2\pi 15\text{kHz}\, t}
     + e^{-j2\pi 15\text{kHz}\, t}
     \Big).
\end{aligned}
$$

So the spectrum has impulses at

- $f = \pm 15~\text{kHz}$ and $f = \pm 17~\text{kHz}$  
- with (real) amplitudes $\tfrac{1}{2}$ in the cosine representation.

---

### 1-B) Mark frequencies in the analog spectrum

On the given analog spectrum axis (in kHz):

- Mark impulses at $f = \pm 15$ kHz and $f = \pm 17$ kHz.
- These form a **bandpass** around the carrier:

  $$
  F_L = 15~\text{kHz},\qquad F_H = 17~\text{kHz}.
  $$

Amplitude is arbitrary units (A.U.), but the **relative** amplitude of the four lines is equal.

---

### 1-C) Minimum sampling frequency to avoid aliasing

The highest analog frequency present is

$$
F_\text{max} = F_H = 17~\text{kHz}.
$$

The classic sampling theorem (baseband case) requires

$$
F_s \ge 2F_\text{max} = 2\cdot 17~\text{kHz} = 34~\text{kHz}.
$$

So the **minimum sampling frequency** for standard (non-under-sampled) sampling is

$$
F_{s,\min} = 34~\text{kHz}.
$$

---

### 1-D) Integer band positioning (bandpass / under-sampling setup)

We now **assign a bandwidth**

$$
B = 4~\text{kHz}.
$$

For a bandpass signal we define band edges

$$
F_L = F_\text{carrier} - \frac{B}{2},\qquad
F_H = F_\text{carrier} + \frac{B}{2}.
$$

With $F_\text{carrier}=16~\text{kHz}$ and $B=4~\text{kHz}$:

$$
F_L = 16-2 = 14~\text{kHz},\qquad
F_H = 16+2 = 18~\text{kHz}.
$$

So the occupied band is

$$
[F_L,F_H] = [14~\text{kHz}, 18~\text{kHz}],\quad B=F_H-F_L=4~\text{kHz}.
$$

For **integer band positioning** we pick a sampling frequency

$$
F_s = 2B = 8~\text{kHz}
$$

so that the band of width $B$ folds exactly into baseband after sampling.

The carrier band is centered at

$$
F_c = 16~\text{kHz} = m F_s,
$$

so the **integer band index** is

$$
m = \frac{F_c}{F_s} = \frac{16~\text{kHz}}{8~\text{kHz}} = 2.
$$

**Summary 1-D**

- $B = 4~\text{kHz}$  
- $F_s = 8~\text{kHz}$  
- $F_L = 14~\text{kHz}$  
- $F_H = 18~\text{kHz}$  
- Integer band index: $m = 2$

---

### 1-E) Sketch the under-sampled spectrum

Using the **under-sampling** (bandpass) sampling frequency $F_s = 8~\text{kHz}$:

- The replicas of the analog spectrum are repeated every $F_s = 8$ kHz.
- Because the carrier is at $F_c = mF_s = 16$ kHz, the band around 16 kHz folds back to **baseband**.

Steps to sketch on the provided grid:

1. Mark $F_s/2 = 4$ kHz, $F_L=14$ kHz, $F_H=18$ kHz on the original (pre-sampling) axis.
2. Sketch the **original band** in $[14,18]$ kHz (and its negative mirror).
3. After sampling with $F_s=8$ kHz, replicate the band at $f = \pm 8,\pm 16,\dots$ kHz.
4. Observe that the replica around $f=16$ kHz **aliases to baseband**:
   - The edges $F_L = 14$ kHz and $F_H = 18$ kHz fold to $-2$ kHz and $+2$ kHz.
   - So the **aliased band** occupies $[-2,2]$ kHz.
5. Mark the **bandwidth window** $2B = 8$ kHz (from $-4$ to $+4$ kHz) that contains the aliased signal.

So the final under-sampled spectrum looks like a **baseband band-limited signal** in $[-2,2]$ kHz, with periodic repetitions every $F_s=8$ kHz.

---

### 1-F) MATLAB: oversampling case (very high $F_s$)

Now we move to MATLAB to verify the spectra numerically.

We first sample with a **very high** sampling frequency, much larger than the Nyquist limit.

The exercise suggests:

```matlab
Fdata    = 1000;       % Hz
Fcarrier = 16000;      % Hz
Fs1      = Fcarrier*100;   % very high sampling rate
Ts1      = 1/Fs1;
deltaf   = 50;         % desired frequency resolution [Hz]
N1       = Fs1/deltaf; % number of samples
time1    = 0:Ts1:(Ts1*(N1-1));
```
The sampled signal is

$$
x_1[n] = x_a(nT_{s1}), \qquad T_{s1} = \frac{1}{F_{s1}}.
$$

We expect the discrete-time spectrum to show clean lines at $\pm 15$ and $\pm 17$ kHz, matching the analog analysis from 1-A/1-B.

> [!code]- MATLAB — Exercise 1-F (high-rate sampling)
> ```matlab
> %% Exercise 1-F: High sampling rate (reference spectrum)
> Fdata    = 1000;        % Hz
> Fcarrier = 16000;       % Hz
> Fs1      = Fcarrier*100;
> Ts1      = 1/Fs1;
> deltaf   = 50;          % frequency resolution [Hz]
> N1       = round(Fs1/deltaf);
> 
> t1 = 0:Ts1:(Ts1*(N1-1));
> 
> % Continuous-time expression sampled in time
> xa1 = cos(2*pi*Fdata.*t1) .* cos(2*pi*Fcarrier.*t1);
> 
> % FFT and frequency axis
> X1    = fft(xa1);
> X1mag = abs(X1)/N1;
> f1    = (0:N1-1)*Fs1/N1;
> 
> % Shifted spectrum around 0 (optional)
> X1sh    = fftshift(X1);
> X1magsh = abs(X1sh)/N1;
> f1sh    = (-N1/2:N1/2-1)*Fs1/N1;
> 
> % Plot one-sided magnitude spectrum
> figure;
> plot(f1, X1mag, 'LineWidth', 1.0); grid on;
> xlim([0 30e3]);   % show up to 30 kHz
> xlabel('f [Hz]');
> ylabel('|X_1(f)|');
> title('Exercise 1-F: Spectrum at very high sampling rate');
> ```
Comment: The spectrum should clearly show impulses at $15$ kHz and $17$ kHz (plus their negative-frequency counterparts when you look at the two-sided version).

---

### 1-G) MATLAB: under-sampling with $F_{s2} = 2B = 8$ kHz

Now set the sampling frequency to

$$
F_{s2} = 2B = 2\cdot 4~\text{kHz} = 8~\text{kHz}.
$$

Suggested settings:

```matlab
Fdata    = 1000;
Fcarrier = 16000;
B        = 4000;
Fs2      = 2*B;       % = 8000 Hz
Ts2      = 1/Fs2;
deltaf2  = 50;        % or similar resolution
N2       = Fs2/deltaf2;
```

