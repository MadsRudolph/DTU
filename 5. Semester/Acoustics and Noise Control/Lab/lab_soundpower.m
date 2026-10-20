%% 34840 Lab exercise — part C: sound power of the vacuum cleaner
% LW = Lp - 14 dB + 10 log10(V/1 m^3) - 10 log10(T/1 s)   (guide p. 5, course text 3.2.6)
% Fill in psq1..psq3 from MeasPres() and T from part B (diffusers-only room).
% The example numbers below are PLACEHOLDERS so the script runs; replace them.

fc = [125 250 500 1000 2000 4000];        % octave centre frequencies [Hz]
V  = 4.38*3.13*3.29;                       % room volume [m^3]

%% Measured mean-square pressures in octave bands [Pa^2]  (placeholders)
psq1 = [0.010 0.020 0.030 0.030 0.020 0.010];
psq2 = [0.012 0.018 0.028 0.032 0.021 0.011];
psq3 = [0.009 0.021 0.031 0.029 0.019 0.009];

%% Reverberation time per band, diffusers only [s]  (placeholders; use T20 where SNR is low)
T = [6 5 4 3.5 3 2.5];

%% Spatial average of p^2 first, then the level:  Lp = 10 log10(<p^2>/p0^2)
psq = (psq1 + psq2 + psq3)/3
Lp = 10*log10(psq/(20e-6)^2)

%% Sound power level per band
LW = Lp - 14 + 10*log10(V/1) - 10*log10(T/1)

%% A-weighting at the octave centres (course text table 1.3.2)
Aw = [-16.1 -8.6 -3.2 0 1.2 1.0];
LWA_band = LW + Aw

%% Total A-weighted sound power  LWA = 10 log10( sum 10^(LWA_i/10) )
LWA = 10*log10(sum(10.^(LWA_band/10)))

%% Same for the unweighted total, for comparison
LW_total = 10*log10(sum(10.^(LW/10)))
