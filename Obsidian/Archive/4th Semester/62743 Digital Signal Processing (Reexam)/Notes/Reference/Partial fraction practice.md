---
type: practice
tags: [DSP, reexam, practice, partial-fractions]
---
# PFD practice -- 5 problems, graduated

> [!info] How to use this
> 1. Work each problem **on paper** first -- no peeking.
> 2. When done, click the `Solution` callout to expand and check.
> 3. If your answer matches: move on. If not: compare line by line, find the slip.
> 4. Problems get harder. Stop when you're solid -- better to nail 3 than fumble 5.
>
> Full theory: [[LTI z-transform flow#Step 3 -- Impulse response h[n] via partial fractions]]

---

## Reminder -- the method

For $\dfrac{\text{numerator}}{(\text{factor}_1)(\text{factor}_2)\ldots}$:

1. **Split** into one piece per factor: $\dfrac{A}{\text{factor}_1} + \dfrac{B}{\text{factor}_2} + \ldots$
2. **Combine** the RHS back over the common denominator.
3. **Equate numerators.**
4. **Plug in** clever values that zero one factor at a time, solve for each coefficient.

**Cover-up shortcut** (use once the full method feels natural):
Skip steps 2-3. Cover the factor you want to isolate in the original, evaluate what's left at the value that zeros that factor. Same answer, fewer lines.

---

## Problem 1 -- warmup, plain algebra

Decompose:

$$\frac{5}{(x-1)(x+4)} \;=\; \frac{A}{x-1} + \frac{B}{x+4}$$

Find A and B.

> [!tip]- Solution
>
> Combine RHS and equate numerators:
>
> $$5 \;=\; A(x+4) + B(x-1)$$
>
> **Plug in x = 1** (kills B):
>
> $$5 = A(5) + 0 \;\Rightarrow\; A = 1$$
>
> **Plug in x = -4** (kills A):
>
> $$5 = 0 + B(-5) \;\Rightarrow\; B = -1$$
>
> **Answer:**
>
> $$\frac{5}{(x-1)(x+4)} \;=\; \frac{1}{x-1} - \frac{1}{x+4}$$
>
> **Verify** (recombine): $\dfrac{(x+4) - (x-1)}{(x-1)(x+4)} = \dfrac{5}{(x-1)(x+4)}\;\checkmark$

---

## Problem 2 -- numerator with x

Decompose:

$$\frac{3x + 5}{(x+1)(x+3)} \;=\; \frac{A}{x+1} + \frac{B}{x+3}$$

> [!tip]- Solution
>
> $$3x + 5 \;=\; A(x+3) + B(x+1)$$
>
> **x = -1** (kills B): $\;3(-1)+5 = A(2) \;\Rightarrow\; 2 = 2A \;\Rightarrow\; A = 1$
>
> **x = -3** (kills A): $\;3(-3)+5 = B(-2) \;\Rightarrow\; -4 = -2B \;\Rightarrow\; B = 2$
>
> **Answer:** $\dfrac{1}{x+1} + \dfrac{2}{x+3}$

---

## Problem 3 -- first z^(-1) problem

Decompose:

$$\frac{1}{(1 - 0.5\,z^{-1})(1 - 0.25\,z^{-1})} \;=\; \frac{A}{1 - 0.5\,z^{-1}} + \frac{B}{1 - 0.25\,z^{-1}}$$

> [!tip]- Solution (full method)
>
> Equate numerators:
>
> $$1 \;=\; A(1 - 0.25\,z^{-1}) + B(1 - 0.5\,z^{-1})$$
>
> **Find A** -- plug in $z^{-1}$ that zeros (1 - 0.5 z^(-1)):
>
> $$1 - 0.5\,z^{-1} = 0 \;\Rightarrow\; z^{-1} = 2$$
>
> Plug in:
>
> $$1 \;=\; A(1 - 0.25 \cdot 2) + B(0) \;=\; A(0.5) \;\Rightarrow\; A = 2$$
>
> **Find B** -- plug in $z^{-1}$ that zeros (1 - 0.25 z^(-1)):
>
> $$1 - 0.25\,z^{-1} = 0 \;\Rightarrow\; z^{-1} = 4$$
>
> Plug in:
>
> $$1 \;=\; 0 + B(1 - 0.5 \cdot 4) \;=\; B(-1) \;\Rightarrow\; B = -1$$
>
> **Answer:** $\dfrac{2}{1 - 0.5\,z^{-1}} - \dfrac{1}{1 - 0.25\,z^{-1}}$

> [!example]- Same problem, cover-up shortcut (compare to the full method above)
>
> **A:** cover $(1 - 0.5 z^{-1})$ in the original, evaluate what's left at $z^{-1} = 2$:
>
> $$A \;=\; \left.\frac{1}{1 - 0.25\,z^{-1}}\right|_{z^{-1} = 2} \;=\; \frac{1}{1 - 0.5} \;=\; 2 \;\checkmark$$
>
> **B:** cover $(1 - 0.25 z^{-1})$, evaluate at $z^{-1} = 4$:
>
> $$B \;=\; \left.\frac{1}{1 - 0.5\,z^{-1}}\right|_{z^{-1} = 4} \;=\; \frac{1}{1 - 2} \;=\; -1 \;\checkmark$$
>
> Same answer, way less writing. But only after the full method feels natural.

---

## Problem 4 -- sign trap (factor with +)

Decompose:

$$\frac{1}{(1 + 0.5\,z^{-1})(1 - 0.5\,z^{-1})} \;=\; \frac{A}{1 + 0.5\,z^{-1}} + \frac{B}{1 - 0.5\,z^{-1}}$$

> [!warning] Watch the sign
> $(1 + 0.5 z^{-1})$ is zero at $z^{-1} = -2$ (not $+2$). The factor is $+$, so the zeroing value is negative: $z^{-1} = -\tfrac{1}{0.5} = -2$.

> [!tip]- Solution
>
> Equate numerators:
>
> $$1 \;=\; A(1 - 0.5\,z^{-1}) + B(1 + 0.5\,z^{-1})$$
>
> **A** at $z^{-1} = -2$ (kills B):
>
> $$1 \;=\; A(1 - 0.5 \cdot (-2)) \;=\; A(1 + 1) \;=\; 2A \;\Rightarrow\; A = 0.5$$
>
> **B** at $z^{-1} = 2$ (kills A):
>
> $$1 \;=\; B(1 + 0.5 \cdot 2) \;=\; 2B \;\Rightarrow\; B = 0.5$$
>
> **Answer:** $\dfrac{0.5}{1 + 0.5\,z^{-1}} + \dfrac{0.5}{1 - 0.5\,z^{-1}}$

---

## Problem 5 -- realistic DSP (numerator with z^(-1))

Decompose:

$$\frac{1 + 0.4\,z^{-1}}{(1 - 0.2\,z^{-1})(1 + 0.6\,z^{-1})} \;=\; \frac{A}{1 - 0.2\,z^{-1}} + \frac{B}{1 + 0.6\,z^{-1}}$$

> [!tip]- Solution
>
> Equate numerators:
>
> $$1 + 0.4\,z^{-1} \;=\; A(1 + 0.6\,z^{-1}) + B(1 - 0.2\,z^{-1})$$
>
> **A** at $z^{-1} = 1/0.2 = 5$ (kills B):
>
> $$1 + 0.4 \cdot 5 \;=\; A(1 + 0.6 \cdot 5) + 0$$
>
> $$3 \;=\; A \cdot 4 \;\Rightarrow\; A = 0.75$$
>
> **B** at $z^{-1} = -1/0.6 = -5/3$ (kills A):
>
> $$1 + 0.4 \cdot \left(-\tfrac{5}{3}\right) \;=\; 0 + B\left(1 - 0.2 \cdot \left(-\tfrac{5}{3}\right)\right)$$
>
> $$1 - \tfrac{2}{3} \;=\; B\left(1 + \tfrac{1}{3}\right)$$
>
> $$\tfrac{1}{3} \;=\; B \cdot \tfrac{4}{3} \;\Rightarrow\; B = \tfrac{1}{4} = 0.25$$
>
> **Answer:** $\dfrac{0.75}{1 - 0.2\,z^{-1}} + \dfrac{0.25}{1 + 0.6\,z^{-1}}$
>
> **Verify** (recombine):
>
> $$0.75(1 + 0.6\,z^{-1}) + 0.25(1 - 0.2\,z^{-1})$$
>
> $$=\; 0.75 + 0.45\,z^{-1} + 0.25 - 0.05\,z^{-1}$$
>
> $$=\; 1 + 0.4\,z^{-1} \;\checkmark$$

---

## Bonus -- bring back the inverse transform

Take your Problem 4 answer: $\dfrac{0.5}{1 + 0.5\,z^{-1}} + \dfrac{0.5}{1 - 0.5\,z^{-1}}$.

Using $\dfrac{1}{1 - a\,z^{-1}} \leftrightarrow a^{n}\,u[n]$, inverse-transform each piece.

Watch the sign: rewrite each factor as $1 - (\ldots) z^{-1}$ **before** reading off $a$.

> [!tip]- Solution
>
> | Piece | Rewrite as $1 - a z^{-1}$ | $a$ | Inverse |
> |---|---|---|---|
> | $\dfrac{0.5}{1 + 0.5 z^{-1}}$ | $\dfrac{0.5}{1 - (-0.5) z^{-1}}$ | $-0.5$ | $0.5 \cdot (-0.5)^{n} u[n]$ |
> | $\dfrac{0.5}{1 - 0.5 z^{-1}}$ | (already right) | $+0.5$ | $0.5 \cdot (0.5)^{n} u[n]$ |
>
> **Sum:** $h[n] = 0.5 \cdot (-0.5)^{n} u[n] + 0.5 \cdot (0.5)^{n} u[n]$
>
> *(Fun observation: for even n both terms are $0.5\cdot(0.5)^n$ and add. For odd n they cancel. So h[n] is nonzero only for even n.)*

---

## When you're done

Tell me:
- Which problems felt **solid** (method flowed, got the right answer)
- Which felt **wobbly** (had to think hard or got a sign wrong)
- If any answer didn't match mine, show me your work -- sign traps are the usual culprit

Once the basic mechanics feel natural, we pick F20 P1-4 back up and you'll power through it.
