%% 34840 exam 12 Dec 2022 - part 1 (practice)
% Paper: |_Learn/000 - Old exams/34840_Exam_2022_part1.pdf| (vault). Official solution: 
% |Exercises/34840_Exam_2022_part1_solution.pdf|. Try first, check after.
%
% Time yourself: part 1 is about 2 hours of the 4.
clear; close all; clc

%% Constants
rho = 1.2          % kg/m^3
c   = 343          % m/s
p0  = 20e-6;       % Pa
rhoc = rho*c       % Pa*s/m

%% Problem 1 - loudspeaker on an infinite baffle
% A loudspeaker on an infinite baffle, driven with 4 V rms at 200 Hz.
%
% *Q1.1* Find the volume velocity of the loudspeaker, the sound pressure amplitude 
% at 5 m, and the radiated sound power.
%
% If stuck: toolkit T08_loudspeaker.
Re = 5;            % ohm, DC resistance
B  = 1;            % T
l  = 2;            % m, voice coil wire
M  = 10e-3;        % kg, moving mass
K  = 1500;         % N/m, suspension stiffness
Rt = 2.5;          % N*s/m, total damping
a  = 0.06;         % m, radius
e_rms = 4;         % V
f  = 200;          % Hz
r  = 5;            % m

% Working:


% Answer 1.1: Q = ... m^3/s,  |p| = ... Pa,  W = ... W

%% Problem 2 - two sources, octave bands
% Complex pressure amplitudes of two sources:
%
% Source 1: 0.1 Pa at 400 Hz, 0.02 Pa at 800 Hz, 0.01 Pa at 1200 Hz
%
% Source 2: j0.05 Pa at 600 Hz, j0.03 Pa at 900 Hz, j0.01 Pa at 1200 Hz, j0.006 Pa at 1500 Hz
%
% *Q2.1* Calculate the SPL in the 250, 500, 1000 and 2000 Hz octave bands with 
% both sources active.
%
% If stuck: toolkit T04_octave_bands_A_weighting.
f1 = [400 800 1200];          p1 = [0.1 0.02 0.01];           % source 1, Hz and Pa (peak)
f2 = [600 900 1200 1500];     p2 = 1j*[0.05 0.03 0.01 0.006]; % source 2

% Working:


% Answer 2.1: L(250) = ... dB, L(500) = ... dB, L(1000) = ... dB, L(2000) = ... dB

%% Problem 3 - two monopoles on a line
% Two monopoles in free space, same frequency. Only the pressure on the line 
% between them is considered.
%
% *Q3.1* Explain in words when complete cancellation can occur at some point 
% between the sources.
%
% If stuck: toolkit T07_two_sources_wall_dipole.

% Answer 3.1 (text):
%

%% Q3.2 - other cancellation frequencies
% The sources are driven in phase and give a flat pressure spectrum. At x = x_c 
% the pressure is 0 Pa at certain frequencies; the lowest is 500 Hz.
%
% *Q3.2* Determine the other frequencies where cancellation happens.
f_low = 500;       % Hz

% Working:


% Answer 3.2:

%% Q3.3 - position and level difference
% *Q3.3* Find the position of the cancellation x_c and the relative level difference 
% of the two sources. (Distances are in the figure on the paper.)

% Working:


% Answer 3.3: x_c = ... m, level difference = ... dB

%% Q3.4 - intensity at the midpoint
% If 3.3 is not answered, assume monopole 2 is 10 % louder than monopole 1.
%
% *Q3.4* Calculate the intensity at the midpoint between the sources when the SPL 
% there is 80 dB.
Lp_mid = 80;       % dB

% Working:


% Answer 3.4: I = ... W/m^2
