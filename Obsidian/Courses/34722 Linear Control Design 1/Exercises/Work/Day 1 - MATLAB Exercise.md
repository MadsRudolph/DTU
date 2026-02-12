# Day 1 - MATLAB Exercise

> [!info] Files
> - Script: [FirstEXMatlab_LCD1.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day1/FirstEXMatlab_LCD1.m)
> - Data: [log.txt](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day1/log.txt)
> - Simulink: [Lecture_1.slx](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day1/Lecture_1.slx)
> - Solutions: [Day1_Matlab_LCD1_Solutions.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day1/Solutions/Day1_Matlab_LCD1_Solutions.m) | [Simulink_exercise_Solution.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day1/Solutions/Simulink_exercise_Solution.m)

> [!example] Related Materials
> - Next exercise: [[Day 2 - Hand-Tuning Exercise]]
> - Lecture notes: [[Lesson 2 - Block Diagrams and Control Concepts]]
> - Robot GUI: [[Regbot GUI]]
> - Prerequisites: [[Pretest Answers]]


## Overview

This exercise introduces basic MATLAB operations for control systems:
- Variable and matrix manipulation
- Transfer functions and their responses
- Symbolic math (Laplace transforms)
- Reading and plotting experimental data

---

## Section 1: Definition of Variables

Basic MATLAB variable types and indexing:

```matlab
c = 5;                    % Scalar
b = [1, 2, 3, 4];         % Row vector
A = [1, 2, 3, 4;          % 2x4 Matrix
     5, 6, 7, 8];

[rows, cols] = size(A);   % Get dimensions
A(:, 1)                   % All rows, first column
A(1, 2:end)               % First row, columns 2 to end

t = 0:0.01:5;             % Time vector (start:step:end)
u = sin(2*pi*t);          % Sinusoidal input
```

---

## Section 2: Transfer Functions

Transfer functions represent LTI systems in the s-domain:

$$G(s) = \frac{s + 1}{s^2 + 2s + 1} = \frac{s + 1}{(s + 1)^2} = \frac{1}{s + 1}$$

```matlab
num = [1, 1];       % s + 1
den = [1, 2, 1];    % s^2 + 2s + 1
G = tf(num, den);
```

---

## Section 3: System Response Plots

### Step Response
Shows how the system responds to a unit step input (important for settling time, overshoot).

![[ex1_step_response.png]]

### Response to Sinusoidal Input (lsim)
Simulates system response to arbitrary input signal.

![[ex1_lsim_response.png]]

### Impulse Response
Shows the system's natural dynamics - fully characterizes an LTI system.

![[ex1_impulse_response.png]]

---

## Section 4: Basic Plotting

### Exponential Decay

![[ex1_exponential_decay.png]]

### Multiple Curves with Legend

![[ex1_y_and_y_squared.png]]

---

## Section 5: Laplace Transforms

Using the Symbolic Math Toolbox:

```matlab
syms x s;
f = 1/sqrt(x);
F_laplace = laplace(f);     % Result: sqrt(pi/s)

F = (s + 1) / (s^2 + 3*s + 2);
f_inverse = ilaplace(F);    % Result: exp(-2t)
```

> [!note] Key Results
> - $\mathcal{L}\left\{\frac{1}{\sqrt{x}}\right\} = \sqrt{\frac{\pi}{s}}$
> - $\mathcal{L}^{-1}\left\{\frac{s+1}{s^2+3s+2}\right\} = e^{-2t}$

---

## Section 6: Robot Data Analysis

Data from robot "Filippa" (log.txt):

| Column | Description |
|--------|-------------|
| 1 | Time [s] |
| 6-7 | Motor velocity ref (L/R) [m/s] |
| 8-9 | Motor voltage (L/R) [V] |
| 10-11 | Motor current (L/R) [A] |
| 12-13 | Wheel velocity (L/R) [m/s] |
| 14-17 | Pose (x, y, heading, tilt) |
| 18 | Battery voltage [V] |

```matlab
data_matrix = readmatrix('log.txt', 'CommentStyle', '%');
t_log = data_matrix(:, 1);
ul = data_matrix(:, 8);   % Left motor voltage
wl = data_matrix(:, 12);  % Left wheel velocity
```

![[ex1_robot_motor_data.png]]

---

## Key MATLAB Functions

| Function | Description |
|----------|-------------|
| `tf(num, den)` | Create transfer function |
| `step(G, t)` | Plot step response |
| `impulse(G)` | Plot impulse response |
| `lsim(G, u, t)` | Simulate response to input u |
| `readmatrix()` | Read numeric data from file |
| `subplot(r, c, i)` | Create subplot grid |
| `laplace(f)` | Laplace transform |
| `ilaplace(F)` | Inverse Laplace transform |
