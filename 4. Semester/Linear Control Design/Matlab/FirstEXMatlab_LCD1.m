%% 34722 Linear Control Design 1 - Day 1 MATLAB Exercise
% This script introduces basic MATLAB operations for control systems:
% - Variable and matrix manipulation
% - Transfer functions and their responses
% - Symbolic math (Laplace transforms)
% - Reading and plotting experimental data
%
% Author: Mads Rudolph
% Date: February 2026

% Clear workspace, close figures, and clear command window
clear all;
close all;
clc;

%% Section 1: Definition of Variables
% This section demonstrates basic MATLAB variable types:
% - Scalars (single values)
% - Vectors (1D arrays)
% - Matrices (2D arrays)
% - Indexing and slicing operations

% Define a scalar variable c (single integer)
c = 5;

% Define a row vector b with 4 integer elements
% Vectors can be created using square brackets with comma or space separation
b = [1, 2, 3, 4];

% Define a 2x4 matrix A
% Rows are separated by semicolons, columns by commas/spaces
A = [1, 2, 3, 4;
     5, 6, 7, 8];

% The size() function returns [rows, cols] of a matrix
[rows, cols] = size(A);
fprintf('Matrix A has %d rows and %d columns\n', rows, cols);

% Matrix indexing: A(row, col) accesses specific elements
% A(1, [2,4]) selects row 1, columns 2 and 4
fprintf('A(1, [2,4]) = %d, %d\n', A(1,2), A(1,4));

% The colon operator (:) selects all elements in that dimension
% A(:, 1) means "all rows, column 1" = first column
disp('First column of A:');
disp(A(:, 1));

% 2:end means "from index 2 to the last index"
% A(1, 2:end) = first row, columns 2 through end
disp('First row, columns 2 to end:');
disp(A(1, 2:end));

% Create a time vector from 0 to 5 seconds with 0.01s steps
% Syntax: start:step:end creates evenly spaced values
t = 0:0.01:5;

% Create a sinusoidal input signal u(t) = sin(2*pi*f*t)
% With f=1 Hz, this gives a sine wave with period T=1 second
u = sin(2*pi*t);

%% Section 2: Transfer Functions
% Transfer functions represent linear time-invariant (LTI) systems
% in the frequency domain (Laplace/s-domain).
%
% General form: G(s) = (b_n*s^n + ... + b_1*s + b_0) / (a_m*s^m + ... + a_1*s + a_0)
%
% In MATLAB: G = tf([b_n, ..., b_0], [a_m, ..., a_0])
% Coefficients are ordered from highest to lowest power of s

% Example: First-order numerator, second-order denominator
% G(s) = (s + 1) / (s^2 + 2s + 1) = (s + 1) / (s + 1)^2 = 1/(s + 1)
num = [1, 1];           % Numerator: 1*s + 1 = s + 1
den = [1, 2, 1];        % Denominator: 1*s^2 + 2*s + 1 = (s+1)^2
G = tf(num, den);
disp('Transfer function G:');
disp(G);

%% Section 3: Plot Outputs
% This section demonstrates different ways to analyze system response:
% - step(): Response to unit step input (u(t) = 1 for t >= 0)
% - impulse(): Response to unit impulse (Dirac delta)
% - lsim(): Response to arbitrary input signal

% Figure 1: Step Response
% Shows how the system responds when input suddenly changes from 0 to 1
% Important for understanding settling time, overshoot, steady-state value
figure(1);
step(G, 5);             % Plot step response for 5 seconds
title('Step Response of G');
grid on;

% Figure 2: Response to sinusoidal input using lsim()
% lsim(sys, u, t) simulates the system response to input u over time t
% This shows how the system filters/modifies the sine wave
figure(2);
lsim(G, u, t);
title('Response of G to Sinusoidal Input');
xlabel('Time [s]');
ylabel('Output');
grid on;

% Figure 3: Impulse Response
% Shows the system's natural dynamics (like ringing a bell)
% The impulse response fully characterizes an LTI system
figure(3);
impulse(G);
title('Impulse Response of G');
grid on;

% Figure 4: Basic plotting with labels
% plot(X, Y) creates a 2D line plot
% Always add axis labels and title for clarity
figure(4);
X = t;
Y = exp(-t);            % Exponential decay function
plot(X, Y);
xlabel('Time [s]');
ylabel('Amplitude');
title('Exponential Decay');
grid on;

% Figure 5: Multiple curves in one plot with legend
% plot(X1, Y1, X2, Y2, ...) plots multiple curves
% legend() adds labels to distinguish the curves
figure(5);
plot(X, Y, X, Y.^2);    % .^2 is element-wise squaring
xlabel('Time [s]');
ylabel('Amplitude');
title('Y and Y^2', 'Interpreter', 'none');  % 'none' prevents LaTeX interpretation
legend('Y = e^{-t}', 'Y^2 = e^{-2t}');
grid on;

%% Section 4: Laplace Transforms (Symbolic Math)
% The Laplace transform converts differential equations to algebraic equations
% L{f(t)} = F(s) = integral from 0 to inf of f(t)*e^(-st) dt
%
% Requires Symbolic Math Toolbox
% syms creates symbolic variables for analytical math

% Create symbolic variables
syms x s;

% Define f(x) = 1/sqrt(x)
f = 1/sqrt(x);

% Compute Laplace transform: L{1/sqrt(t)} = sqrt(pi/s)
F_laplace = laplace(f);
disp('Laplace transform of 1/sqrt(x):');
pretty(F_laplace);      % pretty() displays in readable math format

% Define a transfer function symbolically
% F(s) = (s + 1) / (s^2 + 3s + 2) = (s + 1) / ((s+1)(s+2)) = 1/(s+2)
F = (s + 1) / (s^2 + 3*s + 2);
disp('Function F(s):');
pretty(F);

% Inverse Laplace transform: convert back to time domain
% ilaplace() finds f(t) given F(s)
f_inverse = ilaplace(F);
disp('Inverse Laplace of F:');
pretty(f_inverse);

%% Section 5: Load Data from Text File
% Real control systems generate measurement data that needs analysis
% The log.txt file contains data from robot "Filippa" with columns:
%   1     - Time [s]
%   2-5   - Mission state info
%   6-7   - Motor velocity reference [m/s] (left, right)
%   8-9   - Motor voltage [V] (left, right)
%   10-11 - Motor current [A] (left, right)
%   12-13 - Wheel velocity [m/s] (left, right)
%   14-17 - Pose (x, y, heading, tilt)
%   18    - Battery voltage [V]

% Read numeric data, skipping comment lines that start with %
data_matrix = readmatrix('log.txt', 'CommentStyle', '%');

% Handle missing data (NaN) by filling with nearest valid value
data_matrix = fillmissing(data_matrix, 'nearest');

% Extract relevant columns into named variables for clarity
t_log = data_matrix(:, 1);    % Time stamps
ul = data_matrix(:, 8);       % Left motor voltage [V]
ur = data_matrix(:, 9);       % Right motor voltage [V]
wl = data_matrix(:, 12);      % Left wheel velocity [m/s]
wr = data_matrix(:, 13);      % Right wheel velocity [m/s]

%% Section 6: Plot Experimental Data
% subplot(rows, cols, index) creates a grid of plots
% This allows comparing multiple signals in one figure

figure(6);
sgtitle('Robot Motor Data from log.txt');  % Super-title for entire figure

% Subplot 1 (top-left): Left wheel velocity
subplot(2, 2, 1);
plot(t_log, wl);
xlabel('Time [s]');
ylabel('Velocity [m/s]');
title('Left Wheel Velocity');
grid on;

% Subplot 2 (top-right): Right wheel velocity
subplot(2, 2, 2);
plot(t_log, wr);
xlabel('Time [s]');
ylabel('Velocity [m/s]');
title('Right Wheel Velocity');
grid on;

% Subplot 3 (bottom-left): Left motor voltage (input)
subplot(2, 2, 3);
plot(t_log, ul);
xlabel('Time [s]');
ylabel('Voltage [V]');
title('Left Motor Voltage');
grid on;

% Subplot 4 (bottom-right): Right motor voltage (input)
subplot(2, 2, 4);
plot(t_log, ur);
xlabel('Time [s]');
ylabel('Voltage [V]');
title('Right Motor Voltage');
grid on;

%% Section 7: Export Figures to Images
% Save all figures as PNG files for documentation
% Images are saved to the Obsidian course folder

% Define output path (absolute path)
imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Images';
if ~exist(imgDir, 'dir')
    mkdir(imgDir);
end

% Export each figure using exportgraphics (better quality than saveas)
exportgraphics(figure(1), fullfile(imgDir, 'ex1_step_response.png'), 'Resolution', 300);
exportgraphics(figure(2), fullfile(imgDir, 'ex1_lsim_response.png'), 'Resolution', 300);
exportgraphics(figure(3), fullfile(imgDir, 'ex1_impulse_response.png'), 'Resolution', 300);
exportgraphics(figure(4), fullfile(imgDir, 'ex1_exponential_decay.png'), 'Resolution', 300);
exportgraphics(figure(5), fullfile(imgDir, 'ex1_y_and_y_squared.png'), 'Resolution', 300);
exportgraphics(figure(6), fullfile(imgDir, 'ex1_robot_motor_data.png'), 'Resolution', 300);

disp('Figures exported to Images folder.');
