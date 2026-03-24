---
type: concept
aliases: [FFT, DFT, Discrete Fourier Transform, Frequency Domain, Spectral Analysis]
tags:
  - concept
  - frequency-domain
  - signal-processing
  - mathematics
courses: [62743, 34655, 34722]
---
# Fourier Transform

## Definition

The Fourier Transform decomposes a time-domain signal into its constituent frequency components, expressing how much energy exists at each frequency. The continuous Fourier Transform applies to analog signals, while the Discrete Fourier Transform (DFT) and its efficient implementation, the Fast Fourier Transform (FFT), apply to sampled digital signals. The Fourier Transform is foundational to signal processing, enabling frequency-domain analysis, filter design, spectral estimation, and understanding signal composition and noise characteristics.

---

## Key Equations

**Continuous Fourier Transform:**
$$X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} dt$$

**Inverse Fourier Transform:**
$$x(t) = \int_{-\infty}^{\infty} X(f) e^{j2\pi f t} df$$

**Discrete Fourier Transform (DFT):**
$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi k n / N}$$

**Parseval's Theorem (energy conservation):**
$$\sum_{n=0}^{N-1} |x[n]|^2 = \frac{1}{N}\sum_{k=0}^{N-1} |X[k]|^2$$

**Laplace Transform (s-domain, generalization for causal signals):**
$$X(s) = \int_0^{\infty} x(t) e^{-st} dt, \quad \text{where } s = \sigma + j\omega$$

**Sampling Theorem (Nyquist criterion):**
$$f_s \geq 2 f_{max} \text{ to avoid aliasing}$$

---

## Where It Appears

- [[62743 Digital Signal Processing (Reexam)|DSP (Archive)]] — Core tool: FFT algorithms, spectral analysis, window functions, convolution/correlation in frequency domain
- [[34655 Integrated Analog Electronics 2|IAE2]] — Frequency-domain analysis of noise spectrum, harmonic distortion, and signal integrity
- [[34722 Linear Control Design 1|LCD]] — Laplace Transform as extension of Fourier Transform; frequency response of transfer functions; Bode plot derivation
- Electromagnetics (Archive) — Frequency components of electromagnetic fields and wave propagation

---

## Related Concepts

- [[Transfer Function]] — System response in frequency domain; H(jω) is evaluated using Fourier Transform of impulse response
- [[Frequency Response]] — Fourier Transform magnitude and phase directly yield frequency response
- [[Bode Plot]] — Visual representation of the Fourier Transform (magnitude and phase) of a transfer function
- [[Noise Analysis]] — Noise spectral density (power spectral density) obtained via Fourier analysis; shaped by filter frequency response
