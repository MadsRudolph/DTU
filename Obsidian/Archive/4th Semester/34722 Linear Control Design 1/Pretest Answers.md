---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise]
---
# Pretest - 34722 Linear Control Design 1

> [!example] Related Materials
> - Lecture notes: [[Lesson 2 - Block Diagrams and Control Concepts]]
> - MATLAB basics: [[Day 1 - MATLAB Exercise]]

---

## Math

### Question 1
**Given:** $G = \frac{a/b}{c/d}$

**Correct Answer: a)** $G = \frac{ad}{bc}$

**Explanation:**
$$G = \frac{a/b}{c/d} = \frac{a}{b} \cdot \frac{d}{c} = \frac{ad}{bc}$$

When dividing fractions, we multiply by the reciprocal of the denominator.

---

### Question 2
**Given:** $G = \frac{20}{s^2 + 9s + 20}$

**Correct Answer: b)** $G = \frac{1}{0.05s^2 + 0.45s + 1}$

**Explanation:**
Divide both numerator and denominator by 20:
$$G = \frac{20/20}{(s^2 + 9s + 20)/20} = \frac{1}{0.05s^2 + 0.45s + 1}$$

This is the normalized form where the DC gain (constant term in denominator) is 1.

---

### Question 3
**Given:** $G = \frac{\frac{1}{Cs} + R_2}{R_1 s + Ls^2 + \frac{1}{C} + R_2 s}$

**Correct Answer: e)** $G = \frac{R_2 Cs + 1}{s(LCs^2 + (R_1 + R_2)Cs + 1)}$

**Explanation:**
1. Numerator: $\frac{1}{Cs} + R_2 = \frac{1 + R_2 Cs}{Cs}$

2. Denominator: $Ls^2 + (R_1 + R_2)s + \frac{1}{C}$

3. Combined:
$$G = \frac{(1 + R_2 Cs)/Cs}{Ls^2 + (R_1 + R_2)s + 1/C} = \frac{R_2 Cs + 1}{s(LCs^2 + (R_1 + R_2)Cs + 1)}$$

---

### Question 4
**Given:** $V = 3 + j4$ where $j = \sqrt{-1}$

**Correct Answer: c)** $V = 5\angle 53.1°$

**Explanation:**
- Magnitude: $|V| = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5$
- Phase angle: $\theta = \arctan\left(\frac{4}{3}\right) = 53.13°$

This is a 3-4-5 right triangle.

---

## Physics

### Question 5
**Newton's Second Law:** $F(t) = M \cdot a(t)$

**Correct Answers:**
- ✓ Force in Newton = mass in kg × acceleration in m/s²
- ✓ The force of gravity F for a 2 kg iron block is 19.6 N when g = 9.8 m/s²
- ✓ The velocity v for a body at time t is: $v(t) = \frac{1}{M}\int_0^t F(\tau)d\tau + v(t_0)$

**Wrong statement:**
- ✗ $v = \frac{1}{2M}Ft^2$ — This is incorrect. For constant force: $a = F/M$, so $v = at = \frac{F}{M}t$ (linear in t, not quadratic)

**Explanation:**
- F = ma is the definition of Newton's second law
- F = mg = 2 × 9.8 = 19.6 N ✓
- Since a = F/M, integrating gives velocity: $v(t) = \int a \, dt = \frac{1}{M}\int F \, dt$ ✓

---

### Question 6
**Newton's 2nd Law for Rotation**

**Correct Answers:**
- ✓ **a)** $\tau = I\dot{\omega}$ — This is the rotational equivalent of F = ma
- ✓ **c)** Motor with 24 Nm torque, 2 pivots at 2m radius, 3 kg each block → 1 rad/s after 1 second

**Explanation for c):**
- Moment of inertia: $I = 2 \times m \times r^2 = 2 \times 3 \times 2^2 = 24$ kg·m²
- Angular acceleration: $\dot{\omega} = \frac{\tau}{I} = \frac{24}{24} = 1$ rad/s²
- After 1 second: $\omega = \dot{\omega} \cdot t = 1 \times 1 = 1$ rad/s ✓

---

### Question 7
**Spring with Hook's Law:** $F = kz$, where k = 500 N/m, g = 9.8 m/s²

**Correct Answers:**
- ✓ **2 kg iron weight** — First graph (oscillation around -0.04 m)
- ✓ **3 kg bag** — Third graph (settles to approximately -0.06 m)

**Explanation:**
At equilibrium, spring force equals weight: $kz = mg$, so $z = -\frac{mg}{k}$

- 2 kg: $z_{eq} = -\frac{2 \times 9.8}{500} = -0.0392$ m ≈ -0.04 m ✓
- 3 kg: $z_{eq} = -\frac{3 \times 9.8}{500} = -0.0588$ m ≈ -0.06 m ✓

---

## Frequency

### Question 8
**Find the dominant (resonant) frequency from the oscillation graph**

**Correct Answer: d)** 15 radians per second

**Explanation:**
From the graph, counting approximately 6 complete oscillations between t=2s and t=4s (2 second span):
$$T = \frac{2 \text{ s}}{6 \text{ cycles}} = \frac{1}{3} \text{ s}$$
$$\omega = \frac{2\pi}{T} = 6\pi \approx 18.85 \text{ rad/s}$$

The closest option is **15 rad/s**.

---

### Question 9
**What is this type of plot called?**

**Correct Answer: a)** Bode plot

**Explanation:**
A Bode plot consists of two graphs:
1. **Gain plot** — Magnitude in dB vs. frequency (log scale)
2. **Phase plot** — Phase in degrees vs. frequency (log scale)

This is a fundamental tool in control systems for analyzing frequency response.

---

### Question 10
**What type of filter does this frequency characteristic represent?**

**Correct Answer: a)** Low pass filter

**Explanation:**
Characteristics of the Bode plot:
- High gain at low frequencies
- Gain decreases as frequency increases
- Phase drops from 0° toward -180°

This is the signature of a **low pass filter** — it passes low frequencies and attenuates high frequencies.

---

### Question 11
**Given:** $u = M\cos(\omega t + \theta)$, find M (amplitude in Volts) when $\omega = 15$ rad/s

**Correct Answer: e)** 3

**Explanation:**
From the Bode plot at ω = 15 rad/s:
- The gain is approximately 10 dB
- Converting: $M = 10^{10/20} = 10^{0.5} \approx 3.16 \approx 3$

---

## MATLAB

### Question 12
**MATLAB Script Analysis:**
```matlab
1.  h = figure(100)
2.  hold off
3.  plot([0,1,1,10],[0,0,1,1],':','linewidth',2);
4.  hold on
5.  t = 0:0.1:10;
6.  y = 0.7 * sin(t-1) + 0.4;
7.  y(1:10) = 0.4;
8.  plot(t,y,'linewidth', 2);
9.  grid on
10. grid minor
11. saveas(h,'sinus_step','png');
```

**Correct Answers:**
- ✓ **First plot** (with dotted step + sine curve)
- ✓ Line 5 returns a vector with 101 elements with values from 0 through 10
- ✓ Line 7 sets the first 10 elements of the vector y to 0.4
- ✓ Without line 4, there would be only 1 curve

**Explanation:**
- **Line 3:** Plots a unit step function (dotted line) from t=1
- **Line 5:** `0:0.1:10` creates vector [0, 0.1, 0.2, ..., 10] → $(10-0)/0.1 + 1 = 101$ elements
- **Line 6:** Creates a shifted sinusoid with amplitude 0.7 and offset 0.4
- **Line 7:** `y(1:10)` accesses elements 1-10 (MATLAB is 1-indexed), sets them to 0.4
- **Line 4:** `hold on` allows multiple plots on same axes. Without it, the second `plot` command would overwrite the first, leaving only the sine curve

---

> [!nav]
> &nbsp;
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
