% This is the exercise of Matlab for students in LCD1 
% Create separate sections (“cntrl enter” to execute the section)

clear all; clc;
%% General Commands - Define Variables

% Define a variable a (one integer value) 
a = 8;
% Define a vector b of four integer values
b = [7, 3, 2, 6];
% Define a matrix A(2x4) of integers
A = [5,2, 3, 1; 6, 1, 5 0];

% Compute the row and column size of the matrix A 
size(A)
% Print the elements of first row in second and fourth column
A(1, [2,4])
% Print all the elements of the first column 
A(:, 1)
% Print all the elements of the first row, but only of columns 2 to the end 
A(1, 2:end)
% Create a time vector t from 0 to 5 sec with a time step of 0.01 sec. 
t = 0:0.01:5;

% Create a sinusoidal function u (of time t) 
u = sin(t);

%% Transfer functions
% Transfer functions are a frequency-domain representation of linear time-invariant systems. 
% https://www.mathworks.com/help/control/ug/transfer-functions.html

% Create a transfer function G = tf([num], [den]) where [num] = [bn, bn-1, …, b1, b0]
% [den]= [an, an-1, …, a1, a0] in this case define a 1st order numerator and a 2nd order denominator
G = tf([1,4] , [1,6,9]);

%% Plot Outputs

% Create figure 1 
figure(1);
% Plot the step response of G for 5 seconds 
step(G, 5)
% Create figure 2 
figure(2);
% Plot the simulated time response of the transfer function G to the input u in the time t 
lsim(G, u, t)
% Create figure 3
figure(3);
% Plot the impulse response 
impulse(G)

% Plot two equal sized vectors X, Y 
X=t; Y=X;
% Create figure 4
figure(4);
% Add labels to x and y axis 
xlabel('Time (s)'); ylabel('Input (N)');
% Add title 
title('Force Input (F(t)');
% Plot two entries Y and Y.^2 in the same graph calling one plot command 
plot(X, [Y; Y.^2])
% Add a legend
legend('First entry’, ‘Second Entry');

    % use publish command to print a pdf file
%publish('Day1_Matlab_LCD1_Solutions.m','pdf');

%% Laplace
% Compute the Laplace transform of function 1/sqrt(x). The Laplace transform is in terms of s

% Create a symbolic variable x
syms x
% Create the function f
f = 1/sqrt(x);
% Compute the Laplace transform of f
laplace(f)
pretty(laplace(f))

% Define a symbolic variable s 
syms s; % or s = sym('s');
% Use the s to define a function F that has first order at the numerator and second order function at the denominator
F = (s+1) / (s^2+6*s+9);
% Find the inverse of the Laplace function 
pretty(ilaplace(F))

%% Load and plot data from a txt file

% Read data from the log.txt file using readtable() function
data = readtable(['log.txt']); % it loads the data in a table struct
% fill the NaN entries using the fillmissing() function
data = fillmissing(data,'nearest');
% Convert data from a table to a matrix
% Create matrix t for time stamps
t = table2array(data(:,1));
% Create matrix ul for left motor voltage
ul = table2array(data(:,8));
% Create matrix ur for right motor voltage
ur = table2array(data(:,9));
% Create matrix wl for left motor velocity
wl = table2array(data(:,12));
% Create matrix wr for right motor velocity
wr = table2array(data(:,13));

% The data is visualised by using subplots
figure(5)
% Create a subplot and plot the left wheel velocity wl - remind to define axis labels and title 
subplot(2,2,1)
plot(t,wl)
xlim([0 t(end)])
xlabel('time (s)')
ylabel('angular velocity (rad/s)')
title('Left wheel velocity')

% Create a subplot and plot the right wheel velocity wr - remind to define axis labels and title 
subplot(2,2,2)
plot(t,wr)
xlim([0 t(end)])
xlabel('time (s)')
ylabel('angular velocity (rad/s)')
title('Right wheel velocity')

% Create a subplot and plot the left wheel voltage ul - remind to define axis labels and title 
subplot(2,2,3)
plot(t,ul)
xlim([0 t(end)])
xlabel('time (s)')
ylabel('voltage (V)')
title('Left wheel voltage')

% Create a subplot and plot the left wheel velocity ur - remind to define axis labels and title 
subplot(2,2,4)
plot(t,ur)
xlim([0 t(end)])
xlabel('time (s)')
ylabel('voltage (V)')
title('Right wheel voltage')

% Add a title to the whole figure
sgtitle('Left and right wheel velocity and voltage')