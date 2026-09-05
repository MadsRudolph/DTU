%% ========================================================================
%  solve_S20.m  —  Linear Control Design 1, eksamen S20 (forår 2020)
%  11 multiple-choice spørgsmål. Genberegner de udregningstunge spørgsmål
%  og udskriver svaret + det officielle facit.
%
%  Facit-kilde: "Exam - Spring 2020 (S20) Solution.pdf" (slide-løsning,
%  DTU Electrical Engineering, 31300/31301). Stjernen i PDF'en = korrekt svar.
%  Konceptuelle/symbolske (Q3,Q4,Q6,Q8) er kun noteret som kommentar.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== LCD1 S20 — beregnede svar =====\n\n');

%% Q1 — Skateboard-motor: bestem friktion B i arbejdspunktet
% Stationært: I0*Kt = B*w0,  og  w0 = xdot0*G/r.
% => B = I0*Kt / (xdot0*G/r).
Kt=0.035; I0=8.5; xdot0=3; G=3.2; r=0.05;
B1 = I0*Kt / (xdot0*G/r);
fprintf('Q1: B = %.4f   (facit: 0.0016, svar 3)\n', B1);

%% Q2 — Dampmaskine: lineariser J*w'+B*w = a*K*sqrt(P-H*w) om 600 RPM
w0   = 600*2*pi/60;                 % = 62.83 rad/s
K=0.056; B=0.12; P=3e5; H=1600; J=0.23;
root = sqrt(P - H*w0);
a0   = B*w0/(K*root);               % stationær ventilposition
num  = K*root;                      % tæller i lineariseret G
dterm= 0.5*K*a0*H/root;             % ekstra dæmpningsled fra linearisering
G2   = num/(J*s + B + dterm);       % ω(s)/a(s)
fprintf('Q2: a0=%.3f, G(s) = %.1f/(s+%.3f)  (facit: 109/(s+0.65), svar 4)\n', ...
        a0, dcgain(G2)*(B+dterm)/J, (B+dterm)/J);

%% Q3 — Blokdiagram (symbolsk). Øvre gren A parallelt med nedre loop 1/(s+B).
% G = A + s/(s+B) = ((1+A)s + AB)/(s+B).  Facit: svar 2.

%% Q4 — Step-respons med spring ved t=0 (initialværdi 0.4, slutværdi 0.8).
% Initialværdi != 0 kræver en zero i tælleren (lige grad i tæller/nævner):
% G = (b1*s + b0)/(s + a0).  Facit: svar 3.

%% Q5 — 2.-ordens, wn=10, DC-gain 200/100=2, peak 2.9 -> Mp=(2.9-2)/2=0.45.
Mp5 = (2.9 - 2)/2;
zeta5 = sqrt(log(1/Mp5)^2 / (pi^2 + log(1/Mp5)^2));
fprintf('Q5: Mp=%.2f -> zeta=%.3f   (facit: zeta=0.2, svar 2)\n', Mp5, zeta5);

%% Q6 — Bode-ID (konceptuelt). Amplitude op ved zero, ned ved pol.
% Zero (laveste) ~10 rad/s -> s=-10; første pol ~50 -> s=-50; slutfase -90
% kræver én pol mere ~1000 -> s=-1000.  Facit: Poler s=-50,-1000 ; Zero s=-10.

%% Q7 — Bredbånd (BW) for lukket sløjfe, aflæst hvor |G| krydser 0 dB
% (kurven starter ~+3 dB, så 0 dB-krydsningen er BW).  Facit: BW = 22 rad/s.

%% Q8 — Step-respons: 1.-ordens (T~1 ms -> brud 1000 rad/s) + hurtig dæmpet
% svingning med periode T'=1.2 ms -> wn = 2*pi/T'.  Vælg Bode med resonanstop der.
T8 = 1.2e-3; wn8 = 2*pi/T8;
fprintf('Q8: wn = %.0f rad/s (resonanstop)  (facit: Bode m. peak ~5236 rad/s)\n', wn8);

%% Q9 — P-design (design 1). PM=60 deg -> wc~25 rad/s, |G(25)|~23 dB.
% KP = -23 dB i lineær skala.
KdB9 = 23;
KP9  = 10^(-KdB9/20);
fprintf('Q9: KP = %.4f   (facit: 0.06, svar 1)\n', KP9);

%% Q10 — Lead-design (design 2). wc=10, alpha=0.1. tau_d = 1/(wc*sqrt(alpha)).
% Lead-zero ved wz = 1/tau_d.
wc10=10; alpha10=0.1;
tau_d10 = 1/(wc10*sqrt(alpha10));
wz10    = 1/tau_d10;
fprintf('Q10: tau_d=%.3f s -> wz = %.2f rad/s   (facit: 3.2, svar 2)\n', tau_d10, wz10);

%% Q11 — P-Lead (design 2). |Cd(wc)|=1/sqrt(alpha) (her 10 dB).
% |G(wc)|=-14 dB aflæst -> |G*Cd| = -14+10 = -4 dB -> KP = +4 dB.
G11 = tf(28880,[1 7.04 1460 5788 5776]);
alpha11=0.1; wc11=10;
td11 = 1/(wc11*sqrt(alpha11));
Cd11 = (td11*s+1)/(alpha11*td11*s+1);
KP11 = 1/abs(freqresp(G11*Cd11, wc11));
fprintf('Q11: KP = %.3f   (facit: 1.5, svar 1)\n', KP11);

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1:3  Q2:4  Q3:2  Q4:3  Q5:zeta=0.2  Q6:poler -50,-1000/zero -10\n');
fprintf('Q7:BW=22  Q8:peak~5236  Q9:KP=0.06  Q10:wz=3.2  Q11:KP=1.5\n');
