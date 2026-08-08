---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: quiz
tags: [IAE2, quiz]
---
# Quiz 9 - Data Converter Fundamentals

> [!info] Related Notes
> - [[Lecture 9 - Data Converter Fundamentals]]

---

## Question 1 (1 point)

> [!question] For an ideal 4-bits D/A converter with the input code [1011] and a reference voltage of 8 V the output voltage is
> - [x] **5.5 V**
> - [ ] 6.0 V
> - [ ] 6.5 V

> [!success] Answer: 5.5 V

> [!note]- Explanation
> The output voltage of an ideal D/A converter is:
>
> $$V_\text{out} = \frac{b_3 \cdot 2^3 + b_2 \cdot 2^2 + b_1 \cdot 2^1 + b_0 \cdot 2^0}{2^N} \cdot V_\text{REF}$$
>
> For input code [1011]:
>
> $$V_\text{out} = \frac{8 + 0 + 2 + 1}{16} \times 8 = \frac{11}{16} \times 8 = 5.5 \text{ V}$$
>
> | Bit | Weight | Value |
> |-----|--------|-------|
> | $b_3 = 1$ | $2^3 = 8$ | 8 |
> | $b_2 = 0$ | $2^2 = 4$ | 0 |
> | $b_1 = 1$ | $2^1 = 2$ | 2 |
> | $b_0 = 1$ | $2^0 = 1$ | 1 |
> | **Total** | | **11** |
>
> See: [[Lecture 9 - Data Converter Fundamentals#Digital-to-Analog (D/A) Conversion]]

---

## Question 2 (1 point)

> [!question] For an ideal 8-bits D/A converter with $V_\text{LSB} = 0.01$ V the maximum output voltage is
> - [ ] 0.08 V
> - [x] **2.55 V**
> - [ ] 2.56 V

> [!success] Answer: 2.55 V

> [!note]- Explanation
> The maximum output voltage of a D/A converter occurs when all bits are set to 1:
>
> $$V_\text{out,max} = (2^N - 1) \cdot V_\text{LSB}$$
>
> For an 8-bit converter:
>
> $$V_\text{out,max} = (2^8 - 1) \times 0.01 = 255 \times 0.01 = 2.55 \text{ V}$$
>
> > [!tip] Common Mistake
> > The maximum is $2^N - 1$ steps, **not** $2^N$. The full-scale voltage $V_\text{REF} = 2^N \cdot V_\text{LSB} = 2.56$ V is never actually reached.
>
> See: [[Lecture 9 - Data Converter Fundamentals#Digital-to-Analog (D/A) Conversion]]

---

## Question 3 (1 point)

> [!question] For an ideal 3-bits A/D converter with a reference voltage of 8 V an analog input of 3.2 V generates an output code
> - [ ] [010]
> - [x] **[011]**
> - [ ] [100]

> [!success] Answer: [011]

> [!note]- Explanation
> First find $V_\text{LSB}$:
>
> $$V_\text{LSB} = \frac{V_\text{REF}}{2^N} = \frac{8}{2^3} = 1 \text{ V}$$
>
> Then quantize the input:
>
> $$\text{Code} = \left\lfloor \frac{V_\text{in}}{V_\text{LSB}} \right\rfloor = \left\lfloor \frac{3.2}{1} \right\rfloor = 3$$
>
> Converting 3 to binary: $3 = 0 \cdot 2^2 + 1 \cdot 2^1 + 1 \cdot 2^0 = [011]$
>
> See: [[Lecture 9 - Data Converter Fundamentals#Analog-to-Digital (A/D) Conversion]]

---

## Question 4 (1 point)

> [!question] In an A/D converter with $N$ bits the voltage $V_\text{LSB}$ is equal to
> - [ ] $V_\text{LSB} = \dfrac{V_\text{REF}}{N}$
> - [x] **$V_\text{LSB} = \dfrac{V_\text{REF}}{2^N}$**
> - [ ] $V_\text{LSB} = \dfrac{V_\text{REF}}{N^2}$

> [!success] Answer: $V_\text{LSB} = \dfrac{V_\text{REF}}{2^N}$

> [!note]- Explanation
> The LSB voltage represents the smallest voltage step the converter can resolve. An $N$-bit converter divides the reference range into $2^N$ equal levels:
>
> $$V_\text{LSB} = \frac{V_\text{REF}}{2^N}$$
>
> | $N$ (bits) | Levels $2^N$ | $V_\text{LSB}$ (for $V_\text{REF} = 8$ V) |
> |-----------|-------------|------------------------------------------|
> | 3 | 8 | 1.000 V |
> | 8 | 256 | 31.25 mV |
> | 16 | 65536 | 122 $\mu$V |
>
> See: [[Lecture 9 - Data Converter Fundamentals#Analog-to-Digital (A/D) Conversion]]

---

## Question 5 (1 point)

> [!question] With a stochastic signal applied to the input of an A/D converter the quantization noise power (voltage) at the output is given by
> - [x] **$V_{Q,\text{rms}} = \dfrac{V_\text{LSB}}{\sqrt{12}}$**
> - [ ] $V_{Q,\text{rms}} = V_\text{LSB}\sqrt{12}$
> - [ ] $V_{Q,\text{rms}} = \dfrac{V_\text{REF}}{\sqrt{12}}$

> [!success] Answer: $V_{Q,\text{rms}} = \dfrac{V_\text{LSB}}{\sqrt{12}}$

> [!note]- Explanation
> For a stochastic (random) input signal, the quantization error is uniformly distributed over $[-V_\text{LSB}/2, +V_\text{LSB}/2]$. The RMS value of a uniform distribution with width $\Delta$ is:
>
> $$V_{Q,\text{rms}} = \frac{\Delta}{\sqrt{12}} = \frac{V_\text{LSB}}{\sqrt{12}}$$
>
> This comes from the variance of a uniform distribution:
>
> $$\sigma^2 = \frac{\Delta^2}{12} \implies \sigma = \frac{\Delta}{\sqrt{12}}$$
>
> See: [[Lecture 9 - Data Converter Fundamentals#Quantization Noise — Time Domain]]

---

## Question 6 (1 point)

> [!question] For a Nyquist A/D converter with a sampling frequency of 10 MHz the maximum frequency of the input signal is limited to
> - [ ] 10 MHz
> - [x] **5 MHz**
> - [ ] 2.5 MHz

> [!success] Answer: 5 MHz

> [!note]- Explanation
> The **Nyquist-Shannon sampling theorem** states that to avoid aliasing, the input signal frequency must be less than half the sampling frequency:
>
> $$f_\text{max} = \frac{f_s}{2} = \frac{10 \text{ MHz}}{2} = 5 \text{ MHz}$$
>
> This limit $f_s / 2$ is called the **Nyquist frequency**.
>
> > [!warning] Aliasing
> > If the input frequency exceeds $f_s/2$, the signal is **aliased** — it appears as a lower-frequency signal in the digital output, corrupting the data.
>
> See: [[Lecture 9 - Data Converter Fundamentals#Quantization Noise — Frequency Domain]]

---

## Question 7 (1 point)

> [!question] In an audio system with a 16-bit A/D converter the signal to quantization noise ratio is approximately
> - [ ] 80 dB
> - [ ] 90 dB
> - [x] **96 dB**

> [!success] Answer: 96 dB

> [!note]- Explanation
> The signal-to-quantization-noise ratio (SQNR) for an $N$-bit converter with a full-scale sinusoidal input is:
>
> $$\text{SQNR} = 6.02N + 1.76 \text{ dB}$$
>
> For $N = 16$:
>
> $$\text{SQNR} = 6.02 \times 16 + 1.76 = 96.32 + 1.76 = 98.08 \text{ dB}$$
>
> The commonly quoted approximation is **$\approx 6N$ dB per bit**, giving $6 \times 16 = 96$ dB.
>
> > [!tip] Rule of Thumb
> > Each additional bit adds approximately **6 dB** of dynamic range.
>
> See: [[Lecture 9 - Data Converter Fundamentals#Signal-to-Quantization Noise Ratio (SQNR)]]

---

## Question 8 (1 point)

> [!question] For a 3-bits D/A converter with $V_\text{LSB} = 0.5$ V the measured output values (in volts) are {0.010, 0.480, 1.015, 1.506, 1.997, 2.500, 3.002, 3.497}. The absolute accuracy measured in LSB is
> - [ ] 0.02 LSB
> - [x] **0.04 LSB**
> - [ ] 0.10 LSB

> [!success] Answer: 0.04 LSB

> [!note]- Explanation
> Compare measured values to ideal values and find the maximum absolute error:
>
> | Code | Ideal (V) | Measured (V) | Error (V) | Error (LSB) |
> |------|-----------|-------------|-----------|-------------|
> | 000 | 0.000 | 0.010 | 0.010 | 0.020 |
> | 001 | 0.500 | 0.480 | 0.020 | 0.040 |
> | 010 | 1.000 | 1.015 | 0.015 | 0.030 |
> | 011 | 1.500 | 1.506 | 0.006 | 0.012 |
> | 100 | 2.000 | 1.997 | 0.003 | 0.006 |
> | 101 | 2.500 | 2.500 | 0.000 | 0.000 |
> | 110 | 3.000 | 3.002 | 0.002 | 0.004 |
> | 111 | 3.500 | 3.497 | 0.003 | 0.006 |
>
> The **maximum error** is 0.020 V at code 001, which in LSB is:
>
> $$\text{Accuracy} = \frac{0.020}{V_\text{LSB}} = \frac{0.020}{0.5} = 0.04 \text{ LSB}$$
>
> See: [[Lecture 9 - Data Converter Fundamentals#Definitions: Resolution vs. Accuracy]]

---

## Question 9 (1 point)

> [!question] For a 3-bits D/A converter with an absolute accuracy of 0.25 LSB the effective number of bits is
> - [x] **3 bits**
> - [ ] 4 bits
> - [ ] 5 bits

> [!success] Answer: 3 bits

> [!note]- Explanation
> The **effective number of bits (ENOB)** is the resolution at which the converter is accurate to within $\pm 0.5$ LSB. A converter with absolute accuracy of 0.25 LSB is well within the $\pm 0.5$ LSB threshold, meaning it uses its full resolution effectively.
>
> Since 0.25 LSB < 0.5 LSB, the 3-bit converter achieves its full rated resolution:
>
> $$\text{ENOB} = 3 \text{ bits}$$
>
> > [!tip] When ENOB < N
> > If the absolute accuracy were > 0.5 LSB, the effective resolution would be less than $N$ bits, since the errors would exceed the smallest quantization step.
>
> See: [[Lecture 9 - Data Converter Fundamentals#Definitions: Resolution vs. Accuracy]]

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Key Concept |
> |---|--------|-------------|
> | 1 | 5.5 V | D/A output: $\sum b_i 2^i / 2^N \cdot V_\text{REF}$ |
> | 2 | 2.55 V | Max output: $(2^N - 1) \cdot V_\text{LSB}$ |
> | 3 | [011] | A/D quantization: $\lfloor V_\text{in} / V_\text{LSB} \rfloor$ |
> | 4 | $V_\text{REF} / 2^N$ | LSB voltage definition |
> | 5 | $V_\text{LSB} / \sqrt{12}$ | Quantization noise (uniform distribution) |
> | 6 | 5 MHz | Nyquist: $f_\text{max} = f_s / 2$ |
> | 7 | 96 dB | SQNR $\approx 6N$ dB |
> | 8 | 0.04 LSB | Max error / $V_\text{LSB}$ |
> | 9 | 3 bits | ENOB: accuracy < 0.5 LSB $\Rightarrow$ full resolution |

---

## Key Concepts

> [!abstract] Data Converter Fundamentals Reference
> | Concept | Formula |
> |---------|---------|
> | LSB voltage | $V_\text{LSB} = V_\text{REF} / 2^N$ |
> | D/A output | $V_\text{out} = D \cdot V_\text{LSB}$ where $D$ is decimal code |
> | Max D/A output | $(2^N - 1) \cdot V_\text{LSB}$ |
> | A/D quantization | $D = \lfloor V_\text{in} / V_\text{LSB} \rfloor$ |
> | Quantization noise | $V_{Q,\text{rms}} = V_\text{LSB} / \sqrt{12}$ |
> | Nyquist frequency | $f_\text{max} = f_s / 2$ |
> | SQNR | $6.02N + 1.76$ dB $\approx 6N$ dB |
> | Absolute accuracy | Max $\|V_\text{measured} - V_\text{ideal}\| / V_\text{LSB}$ |
> | ENOB | Full $N$ bits if accuracy < 0.5 LSB |

---

> [!nav]
> [[Quiz 3 - Fabrication and Layout|← Quiz 3]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
