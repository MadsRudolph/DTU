> 🔗 [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]] · [[Formulas/Week 2 – Tuesday]]  
> **Quick refs (DSP):** [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]]

# FIR vs IIR Filters

> [!summary] **Overview**  
> **Concept:** FIR (Finite Impulse Response) and IIR (Infinite Impulse Response) filters are both discrete-time LTI systems.  
> They differ mainly by **feedback**, **stability**, and **phase response**.

---

## Comparison Table

| Property                | **FIR Filter**                                    | **IIR Filter**                                                |
| ----------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| **Impulse Response**    | Finite — becomes zero after M samples             | Infinite — decays but never reaches zero                      |
| **Feedback**            | None → only input samples used                    | Has feedback → depends on past outputs                        |
| **Difference Equation** | $y[n]=b_0x[n]+b_1x[n-1]+\dots+b_Mx[n-M]$          | $y[n]=b_0x[n]+\dots+b_Mx[n-M]-a_1y[n-1]-\dots-a_Ny[n-N]$      |
| **Stability**           | Always stable (if coefficients finite)            | May be unstable (depends on poles inside unit circle)         |
| **Phase Response**      | Can be made linear                                | Typically nonlinear                                           |
| **Computation**         | More coefficients, no recursion                   | Efficient recursion, fewer coefficients                       |
| **Design Origin**       | Designed directly from desired frequency response | Derived from analog prototypes (Butterworth, Chebyshev, etc.) |
| **Applications**        | Audio, data communications (linear phase)         | Control systems, real-time filters (sharp cutoff)             |

---

## Example 1 — FIR Filter (Moving Average)

> [!summary] **Concept:** FIR filters have finite impulse responses and no feedback.  
> Example: 3-point moving average filter.
>
> **Equation**  
> $$
> y[n]=\tfrac{1}{3}\big(x[n]+x[n-1]+x[n-2]\big)
> $$
> **Impulse response:** $h[n]=\tfrac{1}{3}[1,1,1]$— finite length → FIR.

> [!code]- MATLAB Example
> ```matlab
> % FIR example: 3-point moving average
> n = 0:10;
> h = (1/3)*[1 1 1];
> stem(n(1:length(h)), h, 'filled');
> title('FIR Impulse Response');
> xlabel('n'); ylabel('h[n]');
> grid on;
> ```

---

## Example 2 — IIR Filter (Recursive System)

> [!summary] **Concept:** IIR filters use feedback, producing an infinite-duration response.  
> Example system:  
> $$
> y[n]-a\,y[n-1]=x[n]
> $$
> $$
> For (a=\tfrac{1}{2}):  
> $$
> $$
> h[n]=\left(\tfrac{1}{2}\right)^n u[n]
> $$  
> Infinite but decaying → **IIR** and stable since \(|a|<1\).

> [!code]- MATLAB Example
> ```matlab
> % IIR example: Recursive system y[n] - a*y[n-1] = x[n]
> n = 0:20;
> a = 0.5;
> h = a.^n;         % Impulse response h[n] = (a^n)u[n]
> stem(n, h, 'filled');
> title('IIR Impulse Response (a=0.5)');
> xlabel('n'); ylabel('h[n]');
> grid on;
> ```

---

## Summary
- **FIR** → finite response, always stable, easy to design for linear phase.  
- **IIR** → feedback structure, infinite response, efficient but may be unstable.  
- **Choice:**  
  - Use **FIR** when phase linearity matters (e.g., audio).  
  - Use **IIR** when computational efficiency is critical.

---

🔗 **References**  
- [[Week 2 – Tuesday]]: LTI systems and impulse response  
- [[Week 2 – Thursday]]: DTFT and filter frequency response  

---

**See also:** [[MOC – DSP]]

Recent in same folder
```dataview
LIST FROM "Courses/DSP"
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.mtime desc
LIMIT 5
```
