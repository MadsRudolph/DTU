---
course: "34655"
course-name: "Integrated Analog Electronics 2"
type: quiz
tags: [IAE2, quiz]
---
# Quiz 10 - A/D Converter Architectures

> [!info] Related Notes
> - [[Lecture 10 - A_D Converter Architectures]]

---

## Question 1 (1 point)

> [!question] The number of comparators required for an $N$-bit flash A/D converter is
> - [ ] $N$
> - [x] **$2^N$**
> - [ ] $N^2$

> [!success] Answer: $2^N$

> [!note]- Explanation
> A flash converter compares the input to $2^N - 1$ reference levels in parallel using a resistor-ladder reference and one comparator per level. The comparator count therefore scales as $\propto 2^N$ (often stated as $2^N$ or $2^N - 1$ depending on whether the top reference is included).
>
> | $N$ | Comparators ($2^N - 1$) |
> |-----|--------------------------|
> | 4   | 15                       |
> | 8   | 255                      |
> | 10  | 1023                     |
>
> This exponential growth is the main drawback of flash converters — area, power, and input capacitance double for every additional bit.

---

## Question 2 (1 point)

> [!question] The main feature of the flash A/D converter is:
> - [x] **It is fast**
> - [ ] It is a low-power convert
> - [ ] It is suitable for high resolution converters

> [!success] Answer: It is fast

> [!note]- Explanation
> A flash converter performs the entire conversion in **one clock cycle** because all comparator decisions happen in parallel and a thermometer-to-binary encoder generates the output code immediately. This makes it the fastest A/D architecture (used in oscilloscopes, RF front-ends).
>
> The other options are wrong:
> - **Low power?** No — $2^N$ comparators each burn static current, so flash is the most power-hungry architecture.
> - **High resolution?** No — comparator count, area, and offset matching get untenable above ~8 bits. High resolution is the domain of SAR, pipelined, and Σ-Δ converters.

---

## Question 3 (1 point)

> [!question] The number of clock cycles required for converting an input sample in an $N$-bit pipelined A/D converter is
> - [x] **$N$**
> - [ ] $2^N$
> - [ ] $N^2$

> [!success] Answer: $N$

> [!note]- Explanation
> A pipelined converter chains $N$ identical 1-bit stages (or $N/k$ stages of $k$ bits). Each stage resolves part of the result and passes the residue to the next stage. A given sample must pass through all $N$ stages → **latency = $N$ clock cycles**.
>
> ```
> Sample → [Stage 1] → [Stage 2] → ... → [Stage N] → output
>            1 clk        1 clk            1 clk
> ```
>
> Don't confuse latency (cycles per sample) with throughput (see Q4).

---

## Question 4 (1 point)

> [!question] For an $N$-bit pipelined A/D converter new input samples can be entered for
> - [x] **every clock cycle**
> - [ ] every second clock cycle
> - [ ] every $N^\text{th}$ clock cycle

> [!success] Answer: every clock cycle

> [!note]- Explanation
> While each sample takes $N$ cycles to traverse the pipeline (latency), all $N$ stages operate **simultaneously** on different samples. As soon as Stage 1 finishes one sample it accepts a new one — so the throughput is **one sample per clock cycle**.
>
> | Time → | clk 1 | clk 2 | clk 3 | clk 4 |
> |--------|-------|-------|-------|-------|
> | Stage 1| s₁    | s₂    | s₃    | s₄    |
> | Stage 2|       | s₁    | s₂    | s₃    |
> | Stage 3|       |       | s₁    | s₂    |
> | Stage 4|       |       |       | s₁    |
>
> > [!tip] Pipelining trade-off
> > High throughput, but $N$-cycle latency — unusable when the loop must close on the converted value within one cycle (e.g. some control loops).

---

## Question 5 (1 point)

> [!question] The number of clock cycles required for converting an input sample in an $N$-bit algorithmic A/D converter is
> - [x] **$N$**
> - [ ] $2^N$
> - [ ] $N^2$

> [!success] Answer: $N$

> [!note]- Explanation
> An **algorithmic** (cyclic / recirculating) converter uses **one** 1-bit stage that feeds its residue back into its own input. The same hardware is reused $N$ times to resolve $N$ bits → **$N$ clock cycles per sample**.
>
> ```
>            ┌────── residue ──────┐
>            ↓                      │
> sample → [Stage] → bit_i ─────────┘
>            ↑
>            └─ S/H holds the sample for N cycles
> ```
>
> Same conversion time as a pipeline, but with a fraction of the area — at the cost of throughput (see Q6).

---

## Question 6 (1 point)

> [!question] For an $N$-bit algorithmic A/D converter new input samples can be entered for
> - [ ] every clock cycle
> - [ ] every second clock cycle
> - [x] **every $N^\text{th}$ clock cycle**

> [!success] Answer: every $N^\text{th}$ clock cycle

> [!note]- Explanation
> Because the single stage is busy recirculating the current sample for $N$ cycles, no new sample may enter until the conversion is complete. Throughput = $f_s / N$ → **a new sample only every $N^\text{th}$ cycle**.
>
> > [!summary] Pipelined vs. Algorithmic
> > | | Latency | Throughput | Area |
> > |---|---------|------------|------|
> > | **Pipelined** | $N$ cycles | 1 sample/cycle | $N$ stages |
> > | **Algorithmic** | $N$ cycles | 1 sample / $N$ cycles | 1 stage |
> >
> > Same speed per sample — pipelined trades area for throughput.

---

## Question 7 (1 point)

> [!question] An $N$-bit successive approximation A/D converter needs the following building block:
> - [ ] An $N$-bit counter
> - [x] **An $N$-bit D/A converter**
> - [ ] An array of $2^N$ comparators

> [!success] Answer: An $N$-bit D/A converter

> [!note]- Explanation
> A SAR (Successive Approximation Register) converter does a binary search for the input voltage. On each cycle the SAR logic toggles one bit, drives an internal **N-bit DAC**, and the comparator decides whether the trial voltage is above or below the input. The bit is kept or cleared accordingly.
>
> ```
>            ┌────── SAR logic ──────┐
> Vin ──→  comparator ←── N-bit DAC  │
>             │                       │
>             └─── decision ──────────┘
> ```
>
> The DAC is the critical analog building block — its accuracy directly limits the SAR converter's accuracy.
>
> Why the others are wrong:
> - **N-bit counter** — that's a *counter-type* (single-slope) ADC, not SAR.
> - **$2^N$ comparators** — that's a *flash* converter.
>
> A SAR converter needs $N$ clock cycles per sample (one bit per cycle).

---

## Question 8 (1 point)

> [!question] An integrating dual-slope A/D converter is suitable for use in
> - [ ] audio systems
> - [ ] video systems
> - [x] **instrumentation**

> [!success] Answer: instrumentation

> [!note]- Explanation
> Dual-slope converters are **very slow but very accurate**, and they intrinsically reject noise at frequencies that fit a whole number of cycles into the integration window (set $T_1 = k/f_\text{mains}$ to reject 50/60 Hz hum). These properties make them ideal for:
> - Digital multimeters (DMMs)
> - Weighing scales / load cells
> - Panel meters, temperature loggers
>
> Not suitable for:
> - **Audio** ($f_s \approx 44$ kHz) — needs Σ-Δ for high resolution at audio rates.
> - **Video** ($f_s$ in the MHz–GHz range) — needs flash or pipelined.

---

## Question 9 (1 point)

> [!question] The number of clock cycles needed for a conversion in a dual-slope A/D converter is
> - [ ] $N$
> - [x] **$2^{N+1}$**
> - [ ] $N^2$

> [!success] Answer: $2^{N+1}$

> [!note]- Explanation
> A dual-slope conversion has two integration phases:
>
> 1. **Run-up**: integrate the input $V_\text{in}$ for a **fixed** time $T_1 = 2^N \cdot T_\text{clk}$.
> 2. **Run-down**: integrate the reference $-V_\text{ref}$ until the integrator returns to zero, taking a variable time $T_2 \le 2^N \cdot T_\text{clk}$ that is counted in clock cycles.
>
> $$\frac{V_\text{in}}{V_\text{ref}} = \frac{T_2}{T_1} \quad\Rightarrow\quad \text{count} = 2^N \cdot \frac{V_\text{in}}{V_\text{ref}}$$
>
> Worst-case total time: $T_1 + T_{2,\max} = 2^N + 2^N = 2 \cdot 2^N = \boxed{2^{N+1}}$ clock cycles.
>
> ```
>      ↑ V
>      │      /\
>      │     /  \
>      │    /    \
>      │   /      \
>      └──────────────→ t
>          T₁    T₂
>      ←─2^N─→←≤2^N→
> ```
>
> > [!tip] Why "dual-slope" beats "single-slope"
> > In single-slope the conversion depends on the absolute values of the integrator's $RC$ and the clock frequency. In dual-slope those terms appear in both $T_1$ and $T_2$ and **cancel** in the ratio — so accuracy is set only by $V_\text{ref}$ and clock stability over the conversion.

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Architecture | Key Concept |
> |---|--------|--------------|-------------|
> | 1 | $2^N$ | Flash | One comparator per level |
> | 2 | It is fast | Flash | Single-cycle conversion |
> | 3 | $N$ | Pipelined | Latency = stages |
> | 4 | every clock cycle | Pipelined | All stages work in parallel |
> | 5 | $N$ | Algorithmic | Reuse one stage $N$ times |
> | 6 | every $N^\text{th}$ clock cycle | Algorithmic | Throughput = $f_s / N$ |
> | 7 | $N$-bit D/A converter | SAR | Binary search via internal DAC |
> | 8 | instrumentation | Dual-slope | Slow, accurate, mains rejection |
> | 9 | $2^{N+1}$ | Dual-slope | Run-up $2^N$ + worst-case run-down $2^N$ |

---

## Architecture Reference

> [!abstract] A/D Converter Comparison
> | Architecture | Cycles / sample | Throughput | Resolution | Speed | Typical use |
> |--------------|----------------|------------|-----------|-------|-------------|
> | **Flash** | 1 | $f_s$ | low (≤ 8 b) | very high | scope front-end, RF |
> | **Pipelined** | $N$ (latency) | $f_s$ | medium (10–14 b) | high | video, comms |
> | **SAR** | $N$ | $f_s / N$ | medium–high (8–18 b) | medium | sensors, MCUs |
> | **Algorithmic** | $N$ | $f_s / N$ | medium | medium | area-constrained |
> | **Dual-slope** | $\sim 2^{N+1}$ | $f_s / 2^{N+1}$ | high (16–22 b) | very low | DMMs, instrumentation |
> | **Σ-Δ** | many ($\text{OSR} \cdot$ filter) | $f_s / \text{OSR}$ | very high (16–24 b) | low–medium | audio, precision |

---

> [!nav]
> [[Quiz 9 - Data Converter Fundamentals|← Quiz 9]]
>
> [[34655 Integrated Analog Electronics 2|34655 Home]]
>
> &nbsp;
