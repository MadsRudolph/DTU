%% 34722 Linear Control Design 1 - Day 1 MATLAB Exercise
% Clear workspace
clear all;
close all;
clc;

%% Definition of variables
% Define a variable c (one integer value)
c = 5;

% Define a vector b of 4 integer values
b = [1, 2, 3, 4];

% Define a matrix A(2x4) of integers
A = [1, 2, 3, 4;
     5, 6, 7, 8];

% Compute the row and column size of the matrix A
[rows, cols] = size(A);
fprintf('Matrix A has %d rows and %d columns\n', rows, cols);

% Print the elements of first row in second and fourth column
fprintf('A(1, [2,4]) = %d, %d\n', A(1,2), A(1,4));

% Print all the elements of the first column
disp('First column of A:');
disp(A(:, 1));

% Print all the elements of the first row, but only of columns 2 to end
disp('First row, columns 2 to end:');
disp(A(1, 2:end));

% Create a time vector t from 0 to 5 sec with a time step of 0.01 sec
t = 0:0.01:5;

% Create a sinusoidal function u (of time t)
u = sin(2*pi*t);  % 1 Hz sine wave

%% Transfer functions
% Create a transfer function G = tf([num], [den])
% Example: 1st order numerator, 2nd order denominator
% G(s) = (s + 1) / (s^2 + 2s + 1)
num = [1, 1];           % s + 1
den = [1, 2, 1];        % s^2 + 2s + 1
G = tf(num, den);
disp('Transfer function G:');
disp(G);

%% Plot Outputs
% Figure 1: Step response of G for 5 seconds
figure(1);
step(G, 5);
title('Step Response of G');
grid on;

% Figure 2: Simulated time response to input u using lsim
figure(2);
lsim(G, u, t);
title('Response of G to Sinusoidal Input');
xlabel('Time [s]');
ylabel('Output');
grid on;

% Figure 3: Impulse response of G
figure(3);
impulse(G);
title('Impulse Response of G');
grid on;

% Figure 4: Plot two equal-sized vectors X, Y with labels and title
figure(4);
X = t;
Y = exp(-t);
plot(X, Y);
xlabel('Time [s]');
ylabel('Amplitude');
title('Exponential Decay');
grid on;

% Plot two entries Y and Y.^2 in the same graph with legend
figure(5);
plot(X, Y, X, Y.^2);
xlabel('Time [s]');
ylabel('Amplitude');
title('Y and Y^2', 'Interpreter', 'none');
legend('Y = e^{-t}', 'Y^2 = e^{-2t}');
grid on;

%% Laplace
% Compute the Laplace transform of 1/sqrt(x)
syms x s;

% Create the function f
f = 1/sqrt(x);

% Compute the Laplace transform of f
F_laplace = laplace(f);
disp('Laplace transform of 1/sqrt(x):');
pretty(F_laplace);

% Define a function F with 1st order numerator and 2nd order denominator
% F(s) = (s + 1) / (s^2 + 3s + 2)
F = (s + 1) / (s^2 + 3*s + 2);
disp('Function F(s):');
pretty(F);

% Find the inverse Laplace transform
f_inverse = ilaplace(F);
disp('Inverse Laplace of F:');
pretty(f_inverse);

%% Load data from a txt file
% Read data from the log.txt file using readmatrix (skips % comment lines)
data_matrix = readmatrix('log.txt', 'CommentStyle', '%');

% Fill NaN entries with nearest values
data_matrix = fillmissing(data_matrix, 'nearest');

% From the log.txt header:
%  1    time
%  8  9 Motor voltage [V] left, right
% 12 13 Wheel velocity [m/s] left, right

% Create matrix t_log for time stamps (column 1)
t_log = data_matrix(:, 1);

% Create matrix ul for left motor voltage (column 8)
ul = data_matrix(:, 8);

% Create matrix ur for right motor voltage (column 9)
ur = data_matrix(:, 9);

% Create matrix wl for left motor velocity (column 12)
wl = data_matrix(:, 12);

% Create matrix wr for right motor velocity (column 13)
wr = data_matrix(:, 13);

%% Plot data
% Create a figure with subplots
figure(6);
sgtitle('Robot Motor Data from log.txt');

% Subplot 1: Left wheel velocity
subplot(2, 2, 1);
plot(t_log, wl);
xlabel('Time [s]');
ylabel('Velocity [m/s]');
title('Left Wheel Velocity');
grid on;

% Subplot 2: Right wheel velocity
subplot(2, 2, 2);
plot(t_log, wr);
xlabel('Time [s]');
ylabel('Velocity [m/s]');
title('Right Wheel Velocity');
grid on;

% Subplot 3: Left motor voltage
subplot(2, 2, 3);
plot(t_log, ul);
xlabel('Time [s]');
ylabel('Voltage [V]');
title('Left Motor Voltage');
grid on;

% Subplot 4: Right motor voltage
subplot(2, 2, 4);
plot(t_log, ur);
xlabel('Time [s]');
ylabel('Voltage [V]');
title('Right Motor Voltage');
grid on;
