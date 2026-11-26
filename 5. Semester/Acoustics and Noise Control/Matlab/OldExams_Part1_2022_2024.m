%% Old exams 2022-2024, part 1 (problems)
% 34840 Fundamentals of Acoustics and Noise Control | exam prep, 26 November 2026
%
% Worked learning document for the part 1 problem sets of the 2022, 2023
% and 2024 written exams. Every formula is first written as an equation,
% then calculated in one plain MATLAB line. Lines without a semicolon print
% their result. The official answer is written in the comment next to it.
%
% Exam questions: _Learn/000 - Old exams/34840_Exam_20xx_part1.pdf
% Official solutions: Exercises/34840_Exam_20xx_part1_solution.pdf
% Vault note: Exam Prep/Old Exams 2022-2024 - Worked.md
%
% Constants: the exams say rho = 1.2 kg/m^3 and c = 343 m/s.
% Where the official solution differs, the comment says why.

%% Constants
rho = 1.2;            % air density [kg/m^3]
c = 343;              % speed of sound [m/s]
rho_c = rho*c         % characteristic impedance [Pa s/m] = 411.6
p_ref = 20e-6;        % reference pressure [Pa]

%% ===================== 2022 =====================

%% 2022 Problem 1 - Loudspeaker in an infinite baffle, 4 V rms at 200 Hz
% Re = 5 ohm, B = 1 T, l = 2 m, M = 10 g, K = 1500 N/m, Rt = 2.5 Ns/m, a = 6 cm.
Re = 5; Bl = 1*2; M = 0.010; K = 1500; Rt = 2.5; a = 0.06; e_rms = 4;
f = 200; w = 2*pi*f;
S = pi*a^2                                  % 0.0113 m^2
%
% $$Z_M = R_t + j\left(\omega M - \frac{K}{\omega}\right)$$
Z_M = Rt + 1j*(w*M - K/w)                   % 2.5 + 11.37j Ns/m (official: 2.5 + j11.37)
%
% $$|Q| = \frac{S\,Bl}{R_e}\,\frac{\sqrt2\,e_{rms}}{|Z_M|}\quad\text{(amplitude)}$$
Q22 = S*Bl/Re*sqrt(2)*e_rms/abs(Z_M)        % 2.20e-3 m^3/s (official: 0.0022)
%
% Is it a small source? $ka < 1$ means omnidirectional.
ka22 = w/c*a                                % 0.22 (official: 0.22)
%
% $$|p(r)| = \frac{\rho\,\omega\,|Q|}{2\pi r}\quad\text{(baffle, half space)}$$
p5 = rho*w*Q22/(2*pi*5)                     % 0.105 Pa amplitude (official: 0.106; its "3e-3" in the line is a typo, 2.2e-3 is used)
%
% $$P_a = 2\pi r^2\,\frac{|p|^2}{2\rho c}$$
P22 = 2*pi*5^2*p5^2/(2*rho_c)               % 2.12e-3 W (official: 2.1 mW; its "4*pi" in the line is a typo, the number is 2*pi)
%
% Side check: if Rt did NOT already contain the electrical damping (Bl)^2/Re:
Q22_alt = S*Bl/Re*sqrt(2)*e_rms/abs(Z_M + Bl^2/Re)   % 2.16e-3 m^3/s, only 2 % lower

%% 2022 Problem 2 - Two sources, octave bands
% Octave band limits: $f_c/\sqrt2 \dots f_c\sqrt2$
% 250: 177-354, 500: 354-707, 1000: 707-1414, 2000: 1414-2828 Hz.
%
% 250 Hz band: nothing in it, so -Inf dB.
%
% 500 Hz band: 400 Hz (0.1) and 600 Hz (j0.05), different frequencies, so add p^2:
% $$p_{rms}^2 = \sum \frac{|\hat p_i|^2}{2}$$
p500 = sqrt(0.1^2/2 + abs(0.05j)^2/2)       % 0.0791 Pa
L500 = 20*log10(p500/p_ref)                 % 71.9 dB (official: 71.9)
%
% 1000 Hz band: 800 (0.02), 900 (j0.03) and 1200 Hz (0.01 from #1 AND j0.01 from #2).
% Same frequency: add the complex amplitudes first.
p1200 = abs(0.01 + 0.01j)/sqrt(2)           % 0.0100 Pa rms
p1000 = sqrt(0.02^2/2 + 0.03^2/2 + p1200^2) % 0.0274 Pa
L1000 = 20*log10(p1000/p_ref)               % 62.7 dB (official: 62.73)
%
% 2000 Hz band: only 1500 Hz (j0.006). The official text says "1600 Hz", a typo.
L2000 = 20*log10(0.006/sqrt(2)/p_ref)       % 46.5 dB (official: 46.53)

%% 2022 Problem 3 - Two in-phase monopoles 4 m apart
% Cancellation where the path difference is an odd number of half wavelengths:
% $$\Delta x = (2n+1)\frac{\lambda}{2} \Rightarrow f_n = (2n+1)\,f_0$$
f_cancel = [1 3 5 7]*500                    % 500, 1500, 2500, 3500 Hz (official: (1+2n)*500 Hz)
%
% Lowest one: $\Delta x = \lambda/2$, so the point sits $\lambda/4$ from the midpoint.
% $$x_c = 2\,\mathrm m + \frac{c}{4 f_0}$$
x_c = 2 + c/(4*500)                         % 2.1715 m (official: 2.172 m)
%
% Equal pressure at x_c: $|Q_1|/x_c = |Q_2|/(4-x_c)$
Q_ratio = x_c/(4 - x_c)                     % 1.188, source 1 is the stronger one (official: 1.188)
dL = 20*log10(Q_ratio)                      % 1.49 dB
%
% Midpoint: both waves in phase, equal distance, so p1/p2 = Q1/Q2.
% $$p_{rms,1} + p_{rms,2} = p_{ref}\,10^{80/20}$$
p_mid = p_ref*10^(80/20)                    % 0.2 Pa
p2_mid = p_mid/(1 + Q_ratio)                % 0.0914 Pa (official: 0.0914)
p1_mid = Q_ratio*p2_mid                     % 0.1086 Pa
%
% Opposite directions, in phase at this point, so the cross terms vanish:
% $$I_x = \frac{p_{rms,1}^2 - p_{rms,2}^2}{\rho c}$$
I_mid = (p1_mid^2 - p2_mid^2)/rho_c         % 8.33e-6 W/m^2, towards source 2 (official: 8.333 uW/m^2)

%% ===================== 2023 =====================

%% 2023 Problem 1.1 - Tunnel, vibrating end wall, perfect absorber at 20 m
% Only a forward plane wave (R = 0): $|p| = \rho c\,|u|$
U = 1e-3;                                   % wall velocity amplitude [m/s]
p_fw = rho_c*U                              % 0.412 Pa amplitude
L_tunnel1 = 20*log10(p_fw/sqrt(2)/p_ref)    % 83.3 dB everywhere (official: 0.286 Pa, 83.1 dB: an arithmetic slip, 0.412/sqrt(2) = 0.291)

%% 2023 Problem 1.2 - Absorber soaked: water, R almost 1
R_water = (1000*1480 - rho_c)/(1000*1480 + rho_c)   % 0.9994, so take R = 1
k240 = 2*pi*240/c                           % 4.40 rad/m
%
% x = 0 at the water surface, wall at x = -20 m.
% $$p = 2p_i\cos(kx),\qquad u = \frac{2j\,p_i}{\rho c}\sin(-kx)\ \Rightarrow\ p_i = \frac{U\rho c}{2j\sin(-k\,20)}$$
p_i = U*rho_c/(2j*sin(-k240*20))            % -5.62j Pa (official: -j5.5)
p8m = abs(2*p_i*cos(-k240*12))              % 8.94 Pa amplitude at 8 m from the wall (official: 8.8 Pa)
L_tunnel2 = 20*log10(p8m/sqrt(2)/p_ref)     % 110.0 dB (official: 109.9)
%
% Warning: sin(20k) is only 0.037, the tunnel is almost exactly at a resonance.
sin20k = sin(k240*20)                       % 0.0366
% With c = 344 instead of 343 the answer drops by 19 dB:
L_tunnel2_c344 = 20*log10(abs(2*1e-3*rho*344/(2j*sin(-2*pi*240/344*20))*cos(2*pi*240/344*12))/sqrt(2)/p_ref)  % 90.9 dB

%% 2023 Problem 2.1 - Two cello strings, octave bands 125-2000 Hz
% String 1: 334 (0.1), 668 (j0.001), 1002 (0.04). String 2: 501 (0.2), 1002 (0.05), 1503 (j0.02).
% 125 Hz band (88-177 Hz): nothing, -Inf dB.
L250_c = 20*log10(0.1/sqrt(2)/p_ref)                        % 71.0 dB, 334 Hz (official: 70.9)
L500_c = 20*log10(sqrt(0.2^2 + 0.001^2)/sqrt(2)/p_ref)      % 77.0 dB, 501 + 668 Hz (official: 77)
%
% 1000 Hz band: both strings have 1002 Hz, so add complex amplitudes:
p1002 = abs(0.04 + 0.05)/sqrt(2)            % 0.0636 Pa rms
L1000_c = 20*log10(p1002/p_ref)             % 70.1 dB (official: 70.1)
L2000_c = 20*log10(0.02/sqrt(2)/p_ref)      % 57.0 dB, 1503 Hz (official: 57.0)

%% 2023 Problem 2.2 - One string 1 % flat
% Now 1002 Hz and 992 (or 1002 and 992 Hz the other way): different frequencies, add p^2.
p1000_detuned = sqrt(0.04^2 + 0.05^2)/sqrt(2)   % 0.0453 Pa (official: 0.0453; its "|0.4|" is a typo for 0.04)
L1000_detuned = 20*log10(p1000_detuned/p_ref)   % 67.1 dB, i.e. 3 dB lower (official: 67.1)
% The other bands keep their components and their levels.

%% 2023 Problem 3.1 - Monopole 2 m from a rigid wall, power at three frequencies
% $$P = \frac{\rho c\,k^2|Q|^2}{8\pi}\left(1 + \frac{\sin 2kh}{2kh}\right)$$
h = 2;
k20 = 2*pi*20/c; k200 = 2*pi*200/c; k2k = 2*pi*2000/c;
P20 = rho_c*k20^2*(3e-3)^2/(8*pi)*(1 + sin(2*k20*h)/(2*k20*h))      % 33.2e-6 W (official: 32.7 uW)
P200 = rho_c*k200^2*(4e-4)^2/(8*pi)*(1 + sin(2*k200*h)/(2*k200*h))  % 37.3e-6 W (official: 36.6 uW)
P2k = rho_c*k2k^2*(5e-5)^2/(8*pi)*(1 + sin(2*k2k*h)/(2*k2k*h))      % 55.3e-6 W (official: 54.4 uW)
% All three official values are 1.7 % low: they match rho = 1.18 instead of the stated 1.2.
P20_rho118 = 1.18*c*k20^2*(3e-3)^2/(8*pi)*(1 + sin(2*k20*h)/(2*k20*h))  % 32.7e-6 W, the official number

%% 2023 Problem 3.2 - Intensity on the line from the source to the wall, 200 Hz
% Image source 4 m from the real one. r = distance from the real source.
w200 = 2*pi*200; Qb = 4e-4;
% $$|p_1| = \frac{\rho\omega Q}{4\pi r},\qquad |p_2| = \frac{\rho\omega Q}{4\pi(4-r)}$$
p1_0 = rho*w200*Qb/(4*pi*2)                 % 0.0240 Pa at the wall (official: 0.0236, rho = 1.18 again)
p1_05 = rho*w200*Qb/(4*pi*1.5)              % 0.0320 Pa (official: 0.0315)
p2_05 = rho*w200*Qb/(4*pi*2.5)              % 0.0192 Pa (official: 0.0189)
p1_1 = rho*w200*Qb/(4*pi*1.0)               % 0.0480 Pa (official: 0.0472)
p2_1 = rho*w200*Qb/(4*pi*3.0)               % 0.0160 Pa (official: 0.0157)
%
% Official method (counter-propagating waves, cross terms dropped):
% $$I = \frac{|p_1|^2 - |p_2|^2}{2\rho c}$$
I_wall = 0                                  % 0 at the wall (official: 0)
I_05 = (p1_05^2 - p2_05^2)/(2*rho_c)        % 0.80e-6 W/m^2 (official: 0.78 uW/m^2)
I_1 = (p1_1^2 - p2_1^2)/(2*rho_c)           % 2.49e-6 W/m^2 (official: 2.45 uW/m^2)
%
% Exact: $I = \tfrac12\mathrm{Re}\{p\,u^*\}$ with the near-field velocity $(1+1/jkr)$ of each wave.
% kr is only 3.7-9 here, so the cross terms do not vanish.
k200b = w200/c;
pa05 = 1j*w200*rho*Qb/(4*pi*1.5)*exp(-1j*k200b*1.5); pb05 = 1j*w200*rho*Qb/(4*pi*2.5)*exp(-1j*k200b*2.5);
I_05_exact = 0.5*real((pa05 + pb05)*conj(pa05/rho_c*(1 + 1/(1j*k200b*1.5)) - pb05/rho_c*(1 + 1/(1j*k200b*2.5))))  % 0.69e-6 W/m^2
pa1 = 1j*w200*rho*Qb/(4*pi*1.0)*exp(-1j*k200b*1.0); pb1 = 1j*w200*rho*Qb/(4*pi*3.0)*exp(-1j*k200b*3.0);
I_1_exact = 0.5*real((pa1 + pb1)*conj(pa1/rho_c*(1 + 1/(1j*k200b*1.0)) - pb1/rho_c*(1 + 1/(1j*k200b*3.0))))       % 2.78e-6 W/m^2

%% ===================== 2024 =====================

%% 2024 Problem 1.1 - Plane wave on a porous absorber, 0.6 m in front of it
% $$R = +\sqrt{1-\alpha}\quad\text{(positive, given)}$$
R400 = sqrt(1 - 0.9999)                     % 0.01 (official: 0.01)
R630 = sqrt(1 - 0.19)                       % 0.9 (official: 0.9)
%
% x = 0 at the absorber, evaluate at x = -0.6 m:
% $$|p| = |p_i e^{-jkx} + R\,p_i e^{jkx}|$$
k400 = 2*pi*400/c; k630 = 2*pi*630/c;
p400 = abs(0.9*exp(1j*k400*0.6) + R400*0.9*exp(-1j*k400*0.6))                  % 0.893 Pa (official: 0.89)
p630 = abs((0.4+0.4j)*exp(1j*k630*0.6) + R630*(0.4+0.4j)*exp(-1j*k630*0.6))    % 0.862 Pa (official: 0.86)
% Incident 630 Hz amplitude for comparison: |0.4 + 0.4j| = 0.566 Pa.

%% 2024 Problem 1.2 - A-weighted level, both tones together
% Both 400 and 630 Hz sit in the 500 Hz octave (354-707 Hz): one band.
% A-weighting (course text Table 1.3.2): -4.8 dB at 400 Hz, -1.9 dB at 630 Hz.
% $$p_{A,rms} = \frac{|p|}{\sqrt2}\,10^{K_A/20}$$
pA400 = p400/sqrt(2)*10^(-4.8/20)           % 0.363 Pa (official: 0.36)
pA630 = p630/sqrt(2)*10^(-1.9/20)           % 0.490 Pa (official: 0.50)
LA500 = 20*log10(sqrt(pA400^2 + pA630^2)/p_ref)   % 89.7 dB(A) (official: 89.7)
L500_unweighted = 20*log10(sqrt(p400^2 + p630^2)/sqrt(2)/p_ref)   % 92.8 dB, for comparison

%% 2024 Problem 2.1 - Monopole, Q = 1e-5 m^3/s at 500 Hz
w500 = 2*pi*500; k500 = w500/c; Qm = 1e-5;
% $$|p| = \frac{\omega\rho Q}{4\pi r},\qquad |u| = \frac{|p|}{\rho c}\left|1 + \frac{1}{jkr}\right|$$
p_01 = w500*rho*Qm/(4*pi*0.1)               % 0.030 Pa (official: 30 mPa)
p_02 = w500*rho*Qm/(4*pi*0.2)               % 0.015 Pa (official: 15 mPa)
p_03 = w500*rho*Qm/(4*pi*0.3)               % 0.010 Pa (official: 10 mPa)
u_01 = p_01/rho_c*abs(1 + 1/(1j*k500*0.1))  % 108e-6 m/s (official: 108 um/s)
u_02 = p_02/rho_c*abs(1 + 1/(1j*k500*0.2))  % 41.5e-6 m/s (official: 41.5 um/s)
u_03 = p_03/rho_c*abs(1 + 1/(1j*k500*0.3))  % 25.9e-6 m/s (official: 25.9 um/s)

%% 2024 Problem 2.2 - Second monopole 0.4 m away, antiphase (a dipole)
% Positive direction: from source 1 towards source 2. r2 = 0.4 - r1.
% $$p = \frac{j\omega\rho Q}{4\pi}\left(\frac{e^{-jkr_1}}{r_1} - \frac{e^{-jkr_2}}{r_2}\right)$$
% $$u = \frac{j\omega Q}{4\pi c}\left[\left(1+\frac{1}{jkr_1}\right)\frac{e^{-jkr_1}}{r_1} + \left(1+\frac{1}{jkr_2}\right)\frac{e^{-jkr_2}}{r_2}\right]$$
p_t01 = 1j*w500*rho*Qm/(4*pi)*(exp(-1j*k500*0.1)/0.1 - exp(-1j*k500*0.3)/0.3)    % 0.0200 + 0.0275j Pa (official: 0.02 + j0.0275)
u_t01 = 1j*w500*Qm/(4*pi*c)*((1 + 1/(1j*k500*0.1))*exp(-1j*k500*0.1)/0.1 + (1 + 1/(1j*k500*0.3))*exp(-1j*k500*0.3)/0.3)  % (107.4 - 44.6j)e-6 m/s (official: same)
u_t02 = 1j*w500*Qm/(4*pi*c)*2*(1 + 1/(1j*k500*0.2))*exp(-1j*k500*0.2)/0.2          % (60.1 - 57.3j)e-6 m/s (official: same)
prms_01 = abs(p_t01)/sqrt(2)                % 0.0240 Pa at 0.1 and 0.3 m, 0 at 0.2 m (official: 24 mPa / 0 / 24 mPa)
urms_01 = abs(u_t01)/sqrt(2)                % 82.2e-6 m/s at 0.1 and 0.3 m (official: 82.2 um/s)
urms_02 = abs(u_t02)/sqrt(2)                % 58.7e-6 m/s at 0.2 m (official: 58.7 um/s)
%
% $$I = \tfrac12\,\mathrm{Re}\{p\,u^*\}$$
I_01 = 0.5*real(p_t01*conj(u_t01))          % +459e-9 W/m^2 (official: 459.3 nW/m^2)
I_03 = 0.5*real(-p_t01*conj(u_t01))         % -459e-9 W/m^2, p flips sign, u does not (official: -459.3)
% At 0.2 m p = 0, so I = 0 although u is not zero.
