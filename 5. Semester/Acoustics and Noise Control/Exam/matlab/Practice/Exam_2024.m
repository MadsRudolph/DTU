%% 34840 exam 12 Dec 2024 - part 1 (practice)
% Paper: |_Learn/000 - Old exams/34840_Exam_2024_part1.pdf| (vault). Official solution: 
% |Exercises/34840_Exam_2024_part1_solution.pdf|. Try first, check after.
%
% Time yourself: part 1 is about 2 hours of the 4.
clear; close all; clc

%% Constants
rho = 1.2          % kg/m^3
c   = 343          % m/s
p0  = 20e-6;       % Pa
rhoc = rho*c       % Pa*s/m

%% Problem 1 - plane wave on a porous absorber
% A plane wave hits a porous absorber; two frequencies are presented one at a 
% time. The absorber always gives a positive reflection coefficient.
%
% *Q1.1* Calculate the sound pressure amplitude at each frequency 0.6 m from 
% the absorber.
%
% If stuck: toolkit T01_plane_wave_reflection.
f     = [400 630];           % Hz
alpha = [0.9999 0.19];       % absorption coefficient
pi_   = [0.9  0.4+0.4j];     % Pa, incident amplitude
d     = 0.6;                 % m from the absorber

% Working:


% Answer 1.1: |p| = ... Pa at 400 Hz, ... Pa at 630 Hz

%% Q1.2 - A-weighted octave band levels
% *Q1.2* Calculate the A-weighted SPL in the relevant octave bands when both 
% frequencies play at once, 0.6 m from the absorber.
%
% If stuck: toolkit T04_octave_bands_A_weighting.

% Working:


% Answer 1.2:

%% Problem 2 - monopole near field
% A monopole driven with volume velocity 1e-5 m^3/s at 500 Hz.
%
% *Q2.1* Calculate the pressure and particle velocity amplitudes at r = 0.1, 
% 0.2 and 0.3 m.
%
% If stuck: toolkit T06_monopole_nearfield_power.
Q = 1e-5;          % m^3/s
f2 = 500;          % Hz
r  = [0.1 0.2 0.3];% m

% Working:


% Answer 2.1: |p| = ..., |u| = ...

%% Q2.2 - two monopoles in antiphase
% A second monopole 0.4 m away, same frequency and volume velocity, in antiphase.
%
% *Q2.2* Calculate the total rms pressure, total rms particle velocity and the 
% intensity on the line between them at 0.1, 0.2 and 0.3 m from the first monopole.
%
% If stuck: toolkit T07_two_sources_wall_dipole.
D  = 0.4;          % m between the sources
x  = [0.1 0.2 0.3];% m from monopole 1

% Working:


% Answer 2.2:
