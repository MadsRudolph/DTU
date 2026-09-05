%% ========================================================================
%  solve_REExam_F21.m  —  LCD1 RE-eksamen F21 (18 August 2021)
%  20 multiple-choice spørgsmål. Genberegner de udregningstunge spørgsmål.
%  Facit-kilde: "REExam_F21 with Solutions.pdf" (Papageorgiou & Tolu).
%  Konceptuelle/symbolske (Q1,Q3,Q5,Q9,Q12,Q13,Q20) er kun noteret.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== LCD1 RE-eksamen F21 — beregnede svar =====\n\n');

%% Q1 — Linearisering af DC-motor (symbolsk, facit svar 1)
% J*w' = (k/R)(v - k*w - 1.2) - B*sqrt(w). Lineariser om w0:
% d/dw[B*sqrt(w)] = 0.5B/sqrt(w0).  =>  w(s)/v(s) = k / ( R(Js + k^2/R + 0.5B/sqrt(w0)) ).

%% Q2 — Stationær hastighed for bil:  0 = Fp*uss - 0.5*rho*A*Cd*vss^2
Fp=30; uss=40; rho=1.225; A=5; Cd=0.24;
vss = sqrt(2*Fp*uss/(rho*A*Cd));
fprintf('Q2: vss = %.2f m/s   (facit: 40.41, svar 1)\n', vss);

%% Q3 — Bode-ID (konceptuelt). 14 dB DC, fasedyk og tilbage -> komplekse zeroes
% over reelle poler. Facit: svar 1 -> G = (s^2+3s+5)/(s+1)^2.

%% Q4 — Stationær fejl, type-2 system, r = 5 + 2t + t^2/2
G4 = 5*(s+4)/(s^2*(s+1)*(s+20));
Ka = dcgain(s^2*G4);                 % parabel-fejlkonstant (de to integratorer)
fprintf('Q4: type-2 -> step/ramp ess=0; parabel ess=1/Ka=%.3f  (facit: 1, svar 1)\n', 1/Ka);

%% Q5 — Bode-ID (konceptuelt). DC 60 dB, fase fra -180 stigende -> 1 positiv pol
% + 1 negativ zero. Facit: svar 4 -> G = 100(s+10)/(s-1).

%% Q6 — State-space -> overføringsfunktion
% x1'=-x1+u, x2'=-x2+9u, y=x1+x2  =>  G = 1/(s+1) + 9/(s+1) = 10/(s+1)
A6=[-1 0;0 -1]; B6=[1;9]; C6=[1 1]; D6=0;
G6 = tf(ss(A6,B6,C6,D6));
fprintf('Q6: G(s) = '); G6  % 10/(s+1)  (facit: svar 5)

%% Q7 — Respons på u=2e^{-3t}, G=5/(s+1).  Y=10/((s+1)(s+3)) -> 5e^-t - 5e^-3t
% (PFD: residuer 5 og -5). Facit: svar 1.
[r7,p7] = residue([10],conv([1 1],[1 3]));
fprintf('Q7: residuer = [%.0f %.0f] ved poler [%.0f %.0f]  (facit: 5e^-t - 5e^-3t)\n', r7(1),r7(2),p7(1),p7(2));

%% Q8 — Step-respons, Y=4(s+50)/(s^2+30s+200)*R, R=1/s
G8 = 4*(s+50)/(s^2+30*s+200);
[r8,p8] = residue(4*[1 50], conv([1 0], [1 30 200]));
fprintf('Q8: yss = %.0f ; led: ', dcgain(G8));
for i=1:numel(r8), fprintf('%+.1f e^(%.0ft) ', r8(i), p8(i)); end
fprintf('  (facit: 1 + 0.6e^-20t - 1.6e^-10t, svar 1)\n');

%% Q9 — Blokdiagram T(s)=Y/R (symbolsk, facit svar 1):
% T = K*G1*G2*(1/s) / ( 1 + G1*G2*H1 + G1*H3 + K*G1*G2*(1/s) ).

%% Q10 — Overshoot for L=K/(s(s+sqrt(2K))). Lukket: wn=sqrt(K), zeta=sqrt(2)/2.
zeta10 = sqrt(2)/2;
Mp10 = 100*exp(-pi*zeta10/sqrt(1-zeta10^2));
fprintf('Q10: zeta=%.3f -> Mp = %.1f%%   (facit: 4.3%%, svar 1)\n', zeta10, Mp10);

%% Q11 — Statisk forstærkning af lukket sløjfe. Gol(0)=4 (de øvrige led -> 1).
Gol0 = 4;
fprintf('Q11: Gcl(0) = %.2f   (facit: 0.8, svar b)\n', Gol0/(1+Gol0));

%% Q12 — RHP-pol, Nyquist 1x CCW om (-1,0) -> lukket sløjfe STABIL (N=-P). Facit: d.

%% Q13 — Konceptuelt: højere PM -> færre svingninger + robusthed. Facit: e.

%% Q14 — KP-stabilt interval. G=25/(s^3+s^2+10s). GM = 1/7.9588... aflæst.
% Ved fase=-180 (w=3.162) er |G|=7.9588 dB=2.512 -> GM=1/2.512=0.398.
% Stabil for 0<KP<GM. Facit: KP=0.25 (svar e).
G14 = 25/(s^3+s^2+10*s);
[Gm14,~,~,~] = margin(G14);
fprintf('Q14: gain margin GM = %.3f -> stabil for KP<GM  (facit: KP=0.25, svar e)\n', Gm14);

%% Q15 — PI-Lead, find MD (lead-amplitude). phiG=-167.842, gammaM=50, wc=15, Ni=3.
phiG=-167.842; gammaM=50; Ni=3;
phi_d = -180 + gammaM - phiG + atand(1/Ni);   % nødvendigt lead-fasebidrag
alpha15 = (1 - sind(phi_d))/(1 + sind(phi_d));
MD15 = 1/sqrt(alpha15);
fprintf('Q15: phi_d=%.2f deg, alpha=%.4f, MD=%.2f   (facit: 3.3, svar a)\n', phi_d, alpha15, MD15);

%% Q16 — Ustabil (RHP-pol), Nyquist skærer reel akse ved -0.0247.
% Marginal stabilitet ved K=1/0.0247=40.5; stabil for KP>K. Facit: KP=45 (svar a).
fprintf('Q16: K_marginal = %.1f -> stabil for KP>K  (facit: KP=45, svar a)\n', 1/0.0247);

%% Q17 — PI-Lead: hvor mange gange mindre er omega_i end wc? phiG=-151.064, gammaM=75, alpha=0.01.
% (Bode-aflæsning ved wc=25.04: fase = -151.064 deg.)
phiG17=-151.064; gammaM17=75; alpha17=0.01;
phi_lead = asind((1-alpha17)/(1+alpha17));
atan_term = 180 - gammaM17 + phiG17 + phi_lead;   % = arctan(1/Ni) i grader
Ni17 = 1/tand(atan_term);
fprintf('Q17: Ni = wc/wi = %.2f   (facit: 1.57, svar c)\n', Ni17);

%% Q18 — Pre-filter tau_f mod resonanstop. wp=0.7707, Mp=11.0827 dB.
wp=0.770715; Mp_dB=11.0827; Mp18=10^(Mp_dB/20);
tau_f = (1/wp)*sqrt(Mp18^2 - 1);
fprintf('Q18: Mp=%.3f, tau_f = %.2f s   (facit: 4.46, svar c)\n', Mp18, tau_f);

%% Q19 — Følsomhed af statisk fejl mod forstyrrelse + KP.
% G=(13.5s+27)/(s^2+0.4s+27) -> G(0)=1. Gyr(0)=-3.52 dB=0.6667 -> KP=2.
% Gyd(0)=-15.563 dB=0.1667 -> e(0)=-Gyd(0)=-0.1667.
G19=(13.5*s+27)/(s^2+0.4*s+27); G0_19=dcgain(G19);
Gyr0=10^(-3.52183/20); KP19=Gyr0/(1-Gyr0*G0_19);
e0_19=-10^(-15.563/20);
fprintf('Q19: G(0)=%.2f, KP=%.2f, e(0)=%.4f   (facit: KP=2, e(0)=-0.1667, svar d)\n', G0_19, KP19, e0_19);

%% Q20 — Filtreret feed-forward F=Gfilt/G; god cancellering op til wf=1/0.08=125 rad/s
% -> Gyr~0 dB og Ger meget negativ op til ~100 rad/s. Facit: figuren med bredest 0 dB.

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1:1 Q2:1 Q3:1 Q4:1 Q5:4 Q6:5 Q7:1 Q8:1 Q9:1 Q10:1\n');
fprintf('Q11:b Q12:d Q13:e Q14:e Q15:a Q16:a Q17:c Q18:c Q19:d Q20:b\n');
