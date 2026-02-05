%% Lecture 1 - Power Electronics 34620
% Exercises Week 2: Signals and Waveforms

%% Exercise 1.2: Linear Regulator Efficiency
Vin = 5;        % Input voltage [V]
Vout = 1.5;     % Output voltage [V]
Iout = 15;      % Output current [A]
Rload = 0.1;    % Load resistance [Ohm]

% Efficiency calculation
eta = Vout / Vin;
fprintf('Exercise 1.2: Linear Regulator\n')
fprintf('  Efficiency: %.1f%%\n', eta*100)

% Power dissipation
Ploss = (Vin - Vout) * Iout;
fprintf('  Power loss: %.1f W\n\n', Ploss)

%% Exercise 2.1: Squarewave with Duty Cycle d
syms d V_hat positive

% Mean value
V_avg_21 = d * V_hat;

% RMS value
V_rms_21 = sqrt(d) * V_hat;

% Crest factor
xi_21 = V_hat / V_rms_21;

fprintf('Exercise 2.1: Squarewave with duty cycle d\n')
fprintf('  V_avg = d * V_hat\n')
fprintf('  V_rms = sqrt(d) * V_hat\n')
fprintf('  Crest factor = 1/sqrt(d)\n\n')

% Numerical example with d = 0.5
d_num = 0.5;
V_hat_num = 10;
fprintf('  Example (d=0.5, V_hat=10V):\n')
fprintf('    V_avg = %.2f V\n', d_num * V_hat_num)
fprintf('    V_rms = %.2f V\n', sqrt(d_num) * V_hat_num)
fprintf('    Crest factor = %.2f\n\n', 1/sqrt(d_num))

%% Exercise 2.3: DC Values
fprintf('Exercise 2.3: DC Values\n')
fprintf('  a) Triangular ripple: I_DC = I\n')
fprintf('  b) Pulse with ripple: I_DC = d * I\n\n')

%% Exercise 2.4: Halfwave Sawtooth
syms I_peak d_saw positive

% Mean value
I_avg_24 = d_saw * I_peak / 2;

% RMS value
I_rms_24 = I_peak * sqrt(d_saw/3);

fprintf('Exercise 2.4: Halfwave Sawtooth\n')
fprintf('  I_avg = d * I / 2\n')
fprintf('  I_rms = I * sqrt(d/3)\n\n')

% Numerical example
d_num = 0.6;
I_num = 5;
fprintf('  Example (d=0.6, I=5A):\n')
fprintf('    I_avg = %.2f A\n', d_num * I_num / 2)
fprintf('    I_rms = %.2f A\n\n', I_num * sqrt(d_num/3))

%% Exercise 2.5: Sine Wave
fprintf('Exercise 2.5: Sine Wave v(t) = V_hat*sin(wt)\n')
fprintf('  V_avg = 0\n')
fprintf('  V_rms = V_hat / sqrt(2)\n')
fprintf('  Crest factor = sqrt(2) = %.3f\n\n', sqrt(2))

% Numerical example
V_hat_num = 325; % 230V RMS mains
fprintf('  Example (V_hat=325V, like EU mains):\n')
fprintf('    V_rms = %.1f V\n\n', V_hat_num/sqrt(2))

%% Exercise 2.6: More Triangles (symmetric triangle wave)
fprintf('Exercise 2.6: Symmetric Triangle Wave\n')
fprintf('  V_avg = 0\n')
fprintf('  V_rms = V_hat / sqrt(3)\n')
fprintf('  Crest factor = sqrt(3) = %.3f\n\n', sqrt(3))

%% Exercise 2.7: Another Square Wave
% +V_hat for T/4, -V_hat for T/4, +V_hat for T/4, 0 for T/4
fprintf('Exercise 2.7: Square Wave (+V, -V, +V, 0)\n')

V_hat_num = 10;
V_avg_27 = V_hat_num * (1/4 - 1/4 + 1/4 + 0);
V_rms_27 = V_hat_num * sqrt(3/4);

fprintf('  V_avg = V_hat / 4\n')
fprintf('  V_rms = V_hat * sqrt(3)/2\n')
fprintf('  Example (V_hat=10V):\n')
fprintf('    V_avg = %.2f V\n', V_avg_27)
fprintf('    V_rms = %.2f V\n\n', V_rms_27)

%% Exercise 2.8: Two Triangles
fprintf('Exercise 2.8: Two Triangles per period\n')
fprintf('  V_avg = V_hat / 2\n')
fprintf('  V_rms = V_hat / sqrt(3)\n\n')

V_hat_num = 10;
fprintf('  Example (V_hat=10V):\n')
fprintf('    V_avg = %.2f V\n', V_hat_num/2)
fprintf('    V_rms = %.2f V\n\n', V_hat_num/sqrt(3))

%% Exercise 2.9: A Sawtooth
fprintf('Exercise 2.9: Sawtooth (-V_hat to +V_hat)\n')
fprintf('  V_avg = 0\n')
fprintf('  V_rms = V_hat / sqrt(3)\n\n')

%% Exercise 2.10: Two Sawteeth
fprintf('Exercise 2.10: Two Sawteeth per period\n')
fprintf('  V_avg = 0\n')
fprintf('  V_rms = V_hat / sqrt(3)\n\n')

%% Summary Table
fprintf('=== SUMMARY: Common Waveform RMS Values ===\n')
fprintf('Waveform                  | V_avg      | V_rms\n')
fprintf('--------------------------|------------|----------------\n')
fprintf('Squarewave (duty d)       | d*V_hat    | sqrt(d)*V_hat\n')
fprintf('Sine wave                 | 0          | V_hat/sqrt(2)\n')
fprintf('Triangle (symmetric)      | 0          | V_hat/sqrt(3)\n')
fprintf('Sawtooth (symmetric)      | 0          | V_hat/sqrt(3)\n')
fprintf('Halfwave sawtooth (d)     | d*I/2      | I*sqrt(d/3)\n')
