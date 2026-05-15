%% 62743 DSP -- F23 Exam -- Working Script
% Exam PDF:     Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\Exam sets\62743 F23 Exam.pdf
% Solution PDF: Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\Solutions\62743 F23 Exam student solutions.pdf
%
% Date attempted:
% Time target:    4 hours hard cap
% Self-score:     / total marks
%
% Vægtning: Q1 30% | Q2 20% | Q3 20% | Q4 30%
% Filter-first strategi: fokus på Q2 (spektrum + givet filter) og
% Q4 (FIR HP via Fourier + Blackman vindue). Q1 og Q3 er matematik -> udskudt.

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 -- LTI system: H(z), ROC, stabilitet, h[n]  [MATEMATIK - UDSKUDT]
% Differensligning (initialt i hvile):
%   y[n] - (1/2) y[n-1] = x[n] - b*x[n-2],   b > 0 reel konstant
% 1-1: H(z), poler/nulpunkter, ROC for ethvert b>0
% 1-2: stabil/ustabil for ethvert b>0
% 1-3: impulsrespons for ethvert b>0
% 1-4: for hvilken b er systemet FIR?
% 1-5: b=1, find y1[n] når x1[n] = (1/3)^n * u[n]



%% Problem 2 -- Spektrum + karakterisering af givet digitalt filter   [FILTER]
% Analogt signal:  xa(t) = A1*cos(2*pi*F1*t) * (1 + A2*cos(2*pi*F2*t))
F1 = 70;     % Hz
F2 = 100;    % Hz
A1 = 4;
A2 = 2;

%% 2-1  Spektrum af det samplede signal
% Sample med Fs = 5000 Hz, N = 1e7
Fs2 = 5000;
N2  = 1e7;
% a) Udregn og plot |spektrum| som funktion af F = f*Fs i Hz.
% b) Notér frekvensværdierne af de diskrete linjer + amplituder.




%% 2-2  Sammenlign med analytisk udtryk
% a) Omskriv xa(t) så de diskrete frekvenslinjer kan aflæses direkte
%    (hint: produkt-til-sum, cos*cos identiteten).
% b) Sammenlign analytiske amplituder med observerede fra 2-1.




%% 2-3  Karakterisér det givne digitale filter H(z)
% Givet overføringsfunktion (koefficienter aflæst fra exam):
b_filt = [0.915767, -2.747302,  2.747302, -0.915767];
a_filt = [1,        -2.824127,  2.663381, -0.838630];
% a) Plot |H| i LINEÆRE enheder som funktion af F = f*Fs i Hz.
% b) Hvilken filtertype beskriver H(z)?




%% 2-4  Dæmpning ved de diskrete frekvenslinjer fra 2-1
% a) Dæmpning i lineære enheder ved frekvenslinjerne observeret i 2-1.




%% Problem 3 -- Impulstog sampling, S(Omega), samplingsteorem  [MATEMATIK/TEGNING - UDSKUDT]
% s(t) = sum delta(t - k*Ts);  S(Omega) = (2*pi/Ts) sum delta(Omega - n*Omega_s)
% 3-1: tegn S(Omega) for Ts = pi/3
% 3-2: tegn FT af y(t)=x(t)s(t) for Ts = pi/3
% 3-3: gentag for Ts = 2*pi/3
% 3-4: sammenlign 3-2/3-3, konkludér ift. samplingsteoremet



%% Problem 4 -- FIR højpasfilter via Fourier-design + Blackman vindue  [FILTER]
% Filter design metode: Fourier transformation design.
% Filtertype: FIR HØJPAS.
% Digital normaliseret cut-off: fC = 200 Hz / Fs
% Sampling frekvens: Fs = 2000 Hz
Fs4   = 2000;
FcHz  = 200;
fC    = FcHz / Fs4;        % normaliseret cut-off frekvens

%% 4-1  Ideelt højpasfilter
% a) Udregn omega_C.
% b) Udregn og plot h_ideel[n] for n = -20 ... +20.
% c) Aflæs h_ideel ved n = 0, 3, 6, 9, 12.




%% 4-2  Trunkeret (kausalt) FIR filter
Ntaps = 23;
% a) Udregn K og M.            (hint: helper MK_values)
% b) Hvilken forsinkelse (delay) gør filteret kausalt?
% c) Udregn og plot h_HP[n] for det trunkerede filter.
% d) Hvordan er h_HP relateret til filterkoefficienterne a_n og b_n?
% e) Plot |H| i dB som funktion af F = f*Fs i Hz.
% f) Markér fC*Fs på amplitudeplottet.
% g) Angiv dæmpningen ved f*Fs = 100, 200, 300 Hz.




%% 4-3  Blackman vindue (reducér Gibbs)
% a) Udregn og plot h_W[n] efter påtrykt Blackman vindue.
% b) Angiv h_W ved n = 11, 14, 17, 20.
% c) Plot |H| i dB som funktion af F = f*Fs i Hz.
% d) Markér fC*Fs.
% e) Angiv dæmpningen ved f*Fs = 100, 200, 300 Hz.




%% --- Scratch / sandbox ---
