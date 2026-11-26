%% 34840 exam 11 Dec 2023 - part 1 (practice)
% Paper: |_Learn/000 - Old exams/34840_exam_2023_part1.pdf| (vault). Official solution: 
% |Exercises/34840_Exam_2023_part1_Solution.pdf| (it has a few slips, see the worked 
% note in Exam Prep). Try first, check after.
%
% Time yourself: part 1 is about 2 hours of the 4.
clear; close all; clc

%% Constants
rho = 1.2          % kg/m^3
c   = 343          % m/s
p0  = 20e-6;       % Pa
rhoc = rho*c       % Pa*s/m

%% Problem 1 - vibrating end wall of a tunnel
% The end wall of a long tunnel vibrates uniformly at 240 Hz with a velocity 
% amplitude of 1 mm/s. At the other end, 20 m away, is a large porous absorber 
% with absorption coefficient 1 at 240 Hz.
%
% *Q1.1* Describe the sound field the wall generates in the tunnel and calculate 
% the SPL 8 m from the vibrating wall.
%
% If stuck: toolkit T02_tube_driven_end.
f  = 240;          % Hz
U0 = 1e-3;         % m/s, velocity amplitude (peak)
L  = 20;           % m, tunnel length
x  = 8;            % m from the vibrating wall

% Working:


% Answer 1.1:

%% Q1.2 - absorber soaked in water
% The absorber is now soaked and has the acoustic properties of water.
%
% *Q1.2* Describe the new sound field and calculate the SPL 8 m from the vibrating 
% wall.
rho_w = 1000;      % kg/m^3, water
c_w   = 1480;      % m/s, water

% Working:


% Answer 1.2:

%% Problem 2 - two cello strings
% Two strings, each radiating its fundamental and the 2nd and 3rd harmonic, 
% with these pressure amplitudes:
%
% String 1: f1 = 334 Hz: 0.1 Pa, 2f1: j0.001 Pa, 3f1: 0.04 Pa
%
% String 2: f2 = 501 Hz: 0.2 Pa, 2f2: 0.05 Pa, 3f2: j0.02 Pa
%
% *Q2.1* Calculate the rms pressures in the 125, 250, 500, 1000 and 2000 Hz octave 
% bands when both strings play.
%
% If stuck: toolkit T04_octave_bands_A_weighting.
fA = 334*[1 2 3];   pA = [0.1  1j*0.001 0.04];    % string 1, Hz and Pa (peak)
fB = 501*[1 2 3];   pB = [0.2  0.05     1j*0.02]; % string 2

% Working:


% Answer 2.1: p_rms(125) = ..., p_rms(250) = ..., p_rms(500) = ..., p_rms(1000) = ..., p_rms(2000) = ... Pa

%% Q2.2 - one string out of tune
% *Q2.2* Describe what happens to the octave band pressures if one string's fundamental 
% drops by 1 %, and calculate the SPL per octave band.

% Working:


% Answer 2.2:

%% Problem 3 - monopole in front of a rigid baffle
% A monopole 2 m from a fully reflecting infinite baffle.
%
% *Q3.1* Calculate the radiated power at 20 Hz, 200 Hz and 2 kHz with volume 
% velocities 3e-3, 4e-4 and 5e-5 m^3/s respectively.
%
% If stuck: toolkit T07_two_sources_wall_dipole.
h  = 2;                    % m, source to baffle
f3 = [20 200 2000];        % Hz
Q3 = [3e-3 4e-4 5e-5];     % m^3/s

% Working:


% Answer 3.1: W = ... W at 20 Hz, ... at 200 Hz, ... at 2 kHz

%% Q3.2 - intensity on the line to the baffle
% The monopole is driven at 200 Hz with 4e-4 m^3/s. Consider the line from the 
% source perpendicular to the baffle.
%
% *Q3.2* Calculate the intensity on that line at 0 m, 0.5 m and 1 m from the baffle.
d_baffle = [0 0.5 1];      % m from the baffle

% Working:


% Answer 3.2: I = ... W/m^2 at 0, 0.5 and 1 m
