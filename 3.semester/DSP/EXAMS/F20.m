%% 62743 DSP -- F20 Exam -- Working Script
% Exam PDF:     Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\62743 F20 Exam.pdf
% Solution PDF: Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\62743 F20 Exam student solutions.pdf
%
% Date attempted:
% Time target:    4 hours hard cap
% Self-score:     / total marks
%
% --- Problem topics ---
% P1: LTI: diff eq -> H(z) -> poles/zeros/stability -> h[n] -> y[n] -> energy
% P2:
% P3:
% P4:

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 -- LTI system analysis
% Difference equation:
%   y[n] + 0.1 y[n-1] - 0.06 y[n-2] = x[n] + 0.2 x[n-1]

%% 1-1  Bestem H(z)
% By hand: z-transform both sides, factor, divide.

% Y(z) + 0.1 z^(-1)y(z) - 0.06 z^(-2)y(z) = X(z) + 0.2 z^(-1)x(z)

% (1 + 0.1z^(-1) - 0.06z^(-2))*Y(z) = (1 + 0.2 z^(-1))*X(z)

% H(z)= Y(z)/X(z) = 1 + 0.2 z^(-1) / 1 + 0.1z^(-1) - 0.06z^(-2)


% MATLAB coefficient vectors: element k is coefficient of z^(-k).
b = [1, 0.2];         % numerator:   1 + 0.2 z^-1
a = [1, 0.1, -0.06];  % denominator: 1 + 0.1 z^-1 - 0.06 z^-2

% Display H(z) as a discrete-time transfer function.
% Ts = -1 means unspecified sampling period.
% 'Variable','z^-1' prints it in the z^-1 form we derived.
H = tf(b, a, -1, 'Variable', 'z^-1')

%% 1-2  Poles, zeros, stability
% By hand (after multiplying top & bottom by z^2):
%   H(z) = z (z + 0.2) / ((z + 0.3)(z - 0.2))
%   Zeros: z = 0, z = -0.2
%   Poles: z = -0.3, z = 0.2

% Use tf2zpk (not plain roots) so the zero at z=0 is included.
% roots(b) alone would miss it because b is only numerator in z^-1 form.
[z_all, p_all, k_gain] = tf2zpk(b, a);
fprintf('Zeros of H(z):\n');  disp(z_all);
fprintf('Poles of H(z):\n');  disp(p_all);
fprintf('Gain k = %g\n', k_gain);

% Pole-zero plot (unit circle drawn automatically)
figure('Name', 'F20 P1-2: Pole-zero diagram');
zplane(b, a);
title('F20 P1-2: Pole-zero plot');
grid on;

% Stability: causal system stable iff every pole strictly inside unit circle
pole_mag = abs(p_all);
if all(pole_mag < 1)
    fprintf('STABLE: max |pole| = %.4f < 1\n', max(pole_mag));
else
    fprintf('UNSTABLE: max |pole| = %.4f\n', max(pole_mag));
end

%% 1-3  Impulse response h[n]



%% 1-4  Output y[n] for x[n] = (-0.2)^n u[n]   -- TODO

%% 1-5  Energy E_x and E_y   -- TODO




%% Problem 2 --



%% Problem 3 --



%% Problem 4 --



%% --- Scratch / sandbox ---

