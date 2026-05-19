%% 62743 DSP -- F26 REEKSAMEN -- arbejdsfil
% Dato 20. maj 2026 | 4 timer | Mads Rudolph, s246132
% Format: 3 opgaver, vægtning ~ 40 / 30 / 30
%   Opg 1 (~40%) LTI / Z-transformation
%   Opg 2 (~30%) filterrealisering + sampling + FFT + filtrering
%   Opg 3 (~30%) FIR design (Fourier + vindue)
% Svar: skriv under hver "% *Svar N-M:*" (renderes som tekst i pretty).
% Publish til sidst: i mappen 3.semester\DSP  ->  pretty F26.m
% Navigation: Obsidian-hub + [[Q1 via MATLAB cookbook]] (kan ikke regnes i hånd).

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');


%% ════════ Opgave 1 -- LTI / Z-transformation   [~40 %] ════════


%% 1-1


%%
% *Svar 1-1:*

%% 1-2


%%
% *Svar 1-2:*

%% 1-3


%%
% *Svar 1-3:*

%% 1-4


%%
% *Svar 1-4:*

%% 1-5


%%
% *Svar 1-5:*

%% 1-6


%%
% *Svar 1-6:*

%% 1-7


%%
% *Svar 1-7:*


%% ════════ Opgave 2 -- Filterrealisering + sampling + FFT   [~30 %] ════════


%% 2-1


%%
% *Svar 2-1:*

%% 2-2


%%
% *Svar 2-2:*

%% 2-3


%%
% *Svar 2-3:*

%% 2-4


%%
% *Svar 2-4:*

%% 2-5


%%
% *Svar 2-5:*


%% ════════ Opgave 3 -- FIR design (Fourier + vindue)   [~30 %] ════════


%% 3-1


%%
% *Svar 3-1:*

%% 3-2


%%
% *Svar 3-2:*

%% 3-3


%%
% *Svar 3-3:*

%% 3-4


%%
% *Svar 3-4:*

%% 3-5


%%
% *Svar 3-5:*

%% 3-6


%%
% *Svar 3-6:*


%% --- Scratch ---



%% ════════ Appendix -- referencetabeller (IIR-prototype / FIR-vindue) ════════

%% Butterworth lavpas-prototype (3 dB, eps = 1)   [hvis IIR-BLT]
%{
Orden | Nævnerpolynomium  (tæller = 1)
  1   | s + 1
  2   | s^2 + 1.4142 s + 1
  3   | s^3 + 2 s^2 + 2 s + 1
  4   | s^4 + 2.6131 s^3 + 3.4142 s^2 + 2.6131 s + 1
  5   | s^5 + 3.2361 s^4 + 5.2361 s^3 + 5.2361 s^2 + 3.2361 s + 1
  6   | s^6 + 3.8637 s^5 + 7.4641 s^4 + 9.1416 s^3 + 7.4641 s^2 + 3.8637 s + 1

IIR-BLT pipeline: spec -> prewarp Omega=(2/Ts)tan(pi f) -> orden n
 -> prototype -> lp2lp/lp2hp/lp2bp/lp2bs -> bilinear -> freqz dB
 n = ceil( log10((10^(0.1*As)-1)/eps^2) / (2*log10(nu_s)) )
 LP: nu_s = Omega_s/Omega_p ; HP omvendt: nu_s = Omega_p/Omega_s ; BP/BS dobbelt orden.
%}
proto_den{1} = [1, 1];
proto_den{2} = [1, 1.4142, 1];
proto_den{3} = [1, 2, 2, 1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
proto_den{5} = [1, 3.2361, 5.2361, 5.2361, 3.2361, 1];
proto_den{6} = [1, 3.8637, 7.4641, 9.1416, 7.4641, 3.8637, 1];

%% FIR-vinduer   [hvis FIR Fourier-design]
%{
Vindue       | As stopbånd | Ntaps = C / dF ,  dF = |Fstop-Fpass|/Fs
Rektangulær  |   21 dB     | C = 0.9
Hanning      |   44 dB     | C = 3.1
Hamming      |   53 dB     | C = 3.3
Blackman     |   74 dB     | C = 5.5
Vælg det mindste vindue der opfylder As. Rund Ntaps OP til ulige heltal.
M = Ntaps-1 ; K = M/2 ; Fc = (Fpass+Fstop)/2 ; fc = Fc/Fs ; wc = 2*pi*fc.
Ideel (MATLAB sinc(x)=sin(pi x)/(pi x), INGEN ekstra pi):
  LP: hd = 2*fc*sinc(2*fc*(n-K))
  HP: hd = (n==K) - 2*fc*sinc(2*fc*(n-K))
h = hd .* vindue(Ntaps).'   (rektangulær = ingen multiplikation, kun trunkering)
%}
