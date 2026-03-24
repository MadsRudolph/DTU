---
course: "34722"
course-name: "Linear Control Design 1"
type: quiz
tags: [LCD, quiz]
---
# Quiz 1 - Block Diagrams and Control Concepts

> [!info] Related Notes
> - [[Lesson 2 - Block Diagrams and Control Concepts]]
> - [[Day 2 - Hand-Tuning Exercise]]

---

## Question 1 (1 point)

> [!question] When applying a step change in input from 100 to 120 the output exhibits a step response changing from 1000 to 1,300.
>
> The response assessment indicates a dead time $L = T_1 = 1$ s and a time constant $\tau = T_2 - T_1 = 4$ s.
>
> Using the Ziegler-Nichols tuning method for an open-loop system, what is the recommended proportional gain $K_p$ for a P-controller?
> - [x] **0.267**

> [!success] Answer: $K_p = 0.267$

> [!note]- Explanation
> **Given:**
> - Input step: $\Delta U = 120 - 100 = 20$
> - Output step: $\Delta Y = 1300 - 1000 = 300$
> - Dead time: $L = 1$ s
> - Time constant: $\tau = 4$ s
>
> > [!abstract] Step 1: Process gain
> > $$A = \frac{\Delta Y}{\Delta U} = \frac{300}{20} = 15$$
>
> > [!abstract] Step 2: Slope $R$
> > $$R = \frac{A}{\tau} = \frac{15}{4} = 3.75$$
>
> > [!abstract] Step 3: Z-N Open-Loop P-Controller
> > $$K_p = \frac{1}{R \cdot L} = \frac{1}{3.75 \times 1} = 0.267$$
>
> > [!tip] Hint
> > It is the size of the step on the input and output that is significant — i.e., the value from before to after step.
>
> See: [[Lesson 2 - Block Diagrams and Control Concepts#8.1 Open-Loop Method]]

---

## Question 2 (1 point)

> [!question] We have a closed-loop system where the speed of a motor is regulated by a controller. The system is described by $G$ and $K$. The output $M$ is in RPM, and the reference $R$ is the desired speed.
>
> $G$ describes how many RPM the motor will run per volt of input it receives.
> $K$ is the controller's gain, which describes how many volts the controller will output per RPM difference between the desired speed and the actual speed.
>
> ```
> Ref (R) → [+]→ K → G → RPM (M)
>            [-]↑_____________|
> ```
>
> **Given:** $G = 125$ RPM/V, $K = 4$ V/RPM, $R = 2500$
>
> What will be the actual speed of the motor (in RPM) when it is controlled with these values? (assume transients have passed)
> - [x] **2495 RPM**

> [!success] Answer: $M = 2495$ RPM

> [!note]- Explanation
> **Given:**
> - Plant gain: $G = 125$ RPM/V
> - Controller gain: $K = 4$ V/RPM
> - Reference: $R = 2500$ RPM
>
> > [!abstract] Step 1: Loop gain
> > $$G \cdot K = 125 \times 4 = 500$$
>
> > [!abstract] Step 2: Closed-loop transfer function
> > $$M = \frac{G \cdot K}{1 + G \cdot K} \cdot R = \frac{500}{1 + 500} \times 2500$$
>
> > [!abstract] Step 3: Calculate
> > $$M = \frac{500}{501} \times 2500 = \frac{1\,250\,000}{501} \approx 2495 \text{ RPM}$$
>
> > [!tip] Interpretation
> > The steady-state error is $e = R - M = 2500 - 2495 = 5$ RPM. This is the inherent limitation of a P-controller — there is always a small steady-state error. Higher loop gain $GK$ reduces this error but never eliminates it entirely.
>
> See: [[Lesson 2 - Block Diagrams and Control Concepts#6.2 P-Controller]]

---

## Question 3 (1 point)

> [!question] What is a closed-loop system?
> - [x] **a) A system with a controller, where a measurement of the output is compared with the desired output, and where the difference between these is used by the controller to control the system.**
> - [ ] b) A system that is stable.
> - [ ] c) A block diagram in which at least one signal is connected to form a loop.
> - [ ] d) A block diagram describing a model of a physical system.

> [!success] Answer: a)

> [!note]- Explanation
> A **closed-loop system** has three essential features:
>
> 1. **Measurement** of the output (sensor/feedback)
> 2. **Comparison** with the desired value (error = reference - output)
> 3. **Controller action** based on the error
>
> **Why not the other options?**
>
> | Option | Why incorrect |
> |--------|--------------|
> | b) Stable system | A closed-loop system can be unstable (e.g., too high $K_p$) |
> | c) Loop in block diagram | A feedback loop exists, but the definition is about the control purpose, not just topology |
> | d) Model of physical system | This describes modelling, not closed-loop control |
>
> See: [[Lesson 2 - Block Diagrams and Control Concepts#5.2 Open-Loop vs Closed-Loop]]

---

## Question 4 (1 point)

> [!question] The motor has a gear reduction ratio of 10:1 (the motor runs faster than the wheel). The motor operates at 2,400 RPM at 3.1 V and the wheel attached to the gear system has a radius of 2.4 cm.
>
> ```
> Motor voltage [V] → K → Velocity [m/s]
> ```
>
> What would be the value of the constant $K$ that relates the input voltage to the linear velocity at the circumference of the wheel? The constant $K$ should be calculated in m/s/V.
> - [x] **0.195**

> [!success] Answer: $K = 0.195$ m/s/V

> [!note]- Explanation
> **Given:**
> - Motor speed: 2400 RPM at 3.1 V
> - Gear ratio: 10:1 (motor → wheel)
> - Wheel radius: $r = 2.4$ cm $= 0.024$ m
>
> > [!abstract] Step 1: Motor speed per volt
> > $$\frac{2400 \text{ RPM}}{3.1 \text{ V}} = 774.2 \text{ RPM/V}$$
>
> > [!abstract] Step 2: Wheel speed after gear reduction
> > $$\omega_{wheel} = \frac{774.2}{10} = 77.42 \text{ RPM/V}$$
>
> > [!abstract] Step 3: Convert RPM to rad/s
> > $$\omega_{wheel} = 77.42 \times \frac{2\pi}{60} = 8.107 \text{ rad/s/V}$$
>
> > [!abstract] Step 4: Linear velocity
> > $$v = \omega \cdot r = 8.107 \times 0.024 = 0.195 \text{ m/s/V}$$
>
> > [!tip] Unit chain
> > $$K = \frac{2400}{3.1 \times 10} \times \frac{2\pi}{60} \times 0.024 = \frac{1.92\pi}{31} \approx 0.195 \text{ m/(s·V)}$$
>
> Pay attention to unit conversions: RPM → rad/s ($\times 2\pi/60$) and cm → m ($\times 0.01$).

---

## Summary

> [!tldr] Quick Answers
> | Q | Answer | Key Concept |
> |---|--------|-------------|
> | 1 | $K_p = 0.267$ | Z-N open-loop: $K_p = 1/(RL)$ |
> | 2 | 2495 RPM | Closed-loop: $M = \frac{GK}{1+GK} \cdot R$ |
> | 3 | a) | Feedback: measure, compare, correct |
> | 4 | $K = 0.195$ m/s/V | Unit conversion chain: RPM → rad/s → m/s |

---

## Key Formulas Used

> [!abstract] Formulas Reference
> | Quantity | Formula |
> |----------|---------|
> | Process gain (open-loop) | $A = \Delta Y / \Delta U$ |
> | Z-N slope | $R = A / \tau$ |
> | Z-N P-controller (open-loop) | $K_p = 1 / (R \cdot L)$ |
> | Closed-loop transfer function | $\frac{GK}{1 + GK}$ |
> | Steady-state error (P-ctrl) | $e = \frac{R}{1 + GK}$ |
> | RPM to rad/s | $\omega = \text{RPM} \times 2\pi / 60$ |
> | Linear velocity | $v = \omega \cdot r$ |

---

> [!nav]
> &nbsp;
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
