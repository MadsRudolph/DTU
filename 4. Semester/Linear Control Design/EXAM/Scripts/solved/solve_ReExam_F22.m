%% ========================================================================
%  solve_ReExam_F22.m  —  Linear Control Design 1, RE-eksamen (17-08-2022)
%  10 multiple-choice spørgsmål. Dette script genberegner de spørgsmål der
%  kræver udregning og udskriver svaret + det officielle facit (CORRECT n.x).
%
%  Facit-kilde: "LCD1 ReExam F22 - Questions with answers.pdf"
%  (RE-EXAM LCD1, 17 August 2022 — Papageorgiou & Tolu, svar markeret CORRECT).
%
%  Sæt MAKE_FIGS = true for at eksportere nøgleplots som PNG til Obsidian
%  (Images/exam/ReExam_F22/). Kør hele filen (F5) eller: matlab -batch solve_ReExam_F22
% =========================================================================
clear; clc; close all;
MAKE_FIGS = false;          % true -> gem grafer til Obsidian-noten
s = tf('s');
fprintf('===== LCD1 RE-eksamen F22 (17-08-2022) — beregnede svar =====\n\n');

% --- figur-mappe (beregnes ud fra scriptets egen placering) ---------------
here = fileparts(mfilename('fullpath'));
root = here; for k = 1:5, root = fileparts(root); end     % op til DTU-roden
figdir = fullfile(root,'Obsidian','Courses','34722 Linear Control Design 1', ...
                  'Images','exam','ReExam_F22');
if MAKE_FIGS && ~exist(figdir,'dir'), mkdir(figdir); end

%% Q1 — Linearisering af z = y^2 + 5xy - 3x^2 om (xb=3, yb=11). Fejl ved (4,12)?
xb = 3; yb = 11;
zb = yb^2 + 5*xb*yb - 3*xb^2;          % arbejdspunkt: 259
A1 = 5*yb - 6*xb;                      % dz/dx = 5y-6x  = 37
B1 = 2*yb + 5*xb;                      % dz/dy = 2y+5x  = 37
xn = 4; yn = 12;
z_true = yn^2 + 5*xn*yn - 3*xn^2;      % 336
z_lin  = zb + A1*(xn-xb) + B1*(yn-yb); % 333
e1 = abs(z_true - z_lin)/z_true*100;
fprintf('Q1: A=%d, B=%d, fejl = %.2f%%  -> e<1%%   (facit: svar 1)\n', A1, B1, e1);

%% Q2 — Lukket sløjfe K/s * 1/(s+2), 17%% overshoot -> dæmpet frekvens wd
% Y/R = K/(s^2+2s+K) = wn^2/(s^2+2*zeta*wn*s+wn^2).
zeta2 = 0.5;                 % slide-værdi: 17%% overshoot ~ zeta=0.5
wn2   = 1/zeta2;             % 2*zeta*wn = 2  ->  wn = 1/zeta = 2
K2    = wn2^2;              % wn^2 = K = 4
wd2   = wn2*sqrt(1-zeta2^2);
fprintf('Q2: zeta=%.2f, wn=%.0f, K=%.0f, wd = %.2f rad/s   (facit: svar 3)\n', ...
        zeta2, wn2, K2, wd2);

%% Q3 — Sammenkobling af G1..G4 (symbolsk). G3,G4 parallelt; feedback om G2; G1 i serie.
% H = G1*G2 / (1 - G2*(G3+G4)).   Facit: svar 4.

%% Q4 — Samme struktur, indsæt Gi. Er systemet stabilt?
% H = G1*G2/(1-G2*(G3+G4)). Indsæt og reducer i hånden -> (s+2)/(s^2-6s-12).
% (minreal er upålidelig her pga. (s-2)(s-7)-faktorerne, så vi bruger char.poly.)
den4 = [1 -6 -12];                  % s^2 - 6s - 12
H4   = tf([1 2], den4);             % (s+2)/(s^2-6s-12)
p4   = sort(roots(den4),'descend'); % 7.58 (RHP), -1.58 (LHP)
fprintf('Q4: poler = [%.2f, %.2f] -> RHP-pol -> USTABIL   (facit: svar 2)\n', ...
        p4(1), p4(2));

%% Q5 — Bode-identifikation. Flad fase -> fald: dobbeltpol + én zero. DC-gain?
% G(s) = (s+2)/(s+4)^2  (zero -2, dobbeltpol -4).
G5   = (s+2)/(s+4)^2;
dcdB = 20*log10(abs(dcgain(G5)));
fprintf('Q5: DC = %.4f ( = %.1f dB )   (facit: svar 3, dobbeltpol -4, zero -2)\n', ...
        dcgain(G5), dcdB);

%% Q6 — G=1/(1+tau*s), input r=1+6t. Er e_ss større for tau=5 end tau=4?
% E(s) = R(s)[1-G] = R(s)*tau*s/(1+tau*s),  R=1/s+6/s^2.
% e_ss = lim s*E = 6*tau  (rampe-leddet dominerer; step-leddet -> 0).
ess_5 = 6*5;  ess_4 = 6*4;
fprintf('Q6: e_ss(tau=5)=%d, e_ss(tau=4)=%d -> større ved tau=5   (facit: svar 1)\n', ...
        ess_5, ess_4);

%% Q7 — G=10(s+1)/((s+0.1)(s^2+20s+100)). Settling til 99%% af steady state?
G7 = 10*(s+1)/((s+0.1)*(s^2+20*s+100));
p7 = pole(G7);                                  % -0.1, -10, -10
tau_dom = 1/min(abs(real(p7)));                 % dominerende (langsomste) pol: 1/0.1=10
ts99 = 5*tau_dom;                               % 5*tau
fprintf('Q7: dominerende tau = %.0f, 5*tau = %.0f   (facit: svar 4 -> 50)\n', ...
        tau_dom, ts99);

%% Q8 — RCL-serie (R=1, C=1uF, L=1H). V->I, step 0..10V -> vælg step-respons.
% I/V = s/(L s^2 + R s + 1/C) = (s/L)/(s^2 + (R/L)s + 1/(LC)).
% Nøgle: ZERO I ORIGO -> i(0+)=0 OG i(inf)=0 (kondensator blokerer DC) + svingninger.
% -> plot n.3 (starter i 0, stor positiv top, undersving, dør ud mod 0).
R = 1; C = 1e-6; L = 1;
IV_phys  = (s/L)/(s^2 + (R/L)*s + 1/(L*C));     % = s/(s^2 + s + 1e6)
[wn8,zeta8] = damp(IV_phys);
% BEMÆRK DISKREPANS: med R=1,L=1 bliver zeta ~ 5e-4 (ringer ~300 perioder).
% Det officielle facit OG det viste plot bruger s^2+1000s+1e6 (zeta=0.5),
% dvs. R/L=1000. MC-svaret n.3 vælges dog på FORMEN (start 0, svingning, dør
% mod 0) og er robust uanset hvilken zeta man bruger.
IV_facit = s/(s^2 + 1000*s + 1e6);              % matcher plot n.3
fprintf('Q8: zeta(R=1,L=1)=%.4f (rigorøs) vs zeta=0.5 (facit/plot)   (facit: svar 3)\n', ...
        zeta8(1));

%% Q9 — Laplace af  x'' + x' - 2x = 4,  x(0)=2, x'(0)=1.
% (s^2 X -2s -1) + (sX -2) -2X = 4/s
% (s^2+s-2)X = 4/s + 2s + 3  ->  X = (2s^2+3s+4)/(s(s-1)(s+2)).
fprintf('Q9: X(s) = (2s^2+3s+4)/(s(s-1)(s+2))   (facit: svar 1)\n');

%% Q10 — Lukket sløjfe K*G/(1+K*G*H), G=1/(s(s+0.1)), K=5, H=1, input r=5 (step).
% Åben sløjfe er type 1 -> step-fejl = 0.
G10 = 1/(s*(s+0.1));  K10 = 5;  H10 = 1;
L10 = K10*G10*H10;                              % type 1 (integrator)
Etf = minreal(1/(1+L10));                       % fejl-TF E/R = s(s+0.1)/(s^2+0.1s+5)
ess10 = 5*dcgain(Etf);                          % step-amplitude 5 * DC af fejl-TF = 0
fprintf('Q10: åben sløjfe type 1 -> e_ss = %g   (facit: svar 1 -> 0)\n', ess10);

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1:1 Q2:3 Q3:4 Q4:2 Q5:3 Q6:1 Q7:4 Q8:3 Q9:1 Q10:1\n');

%% ----------------------------- FIGURER -----------------------------------
if MAKE_FIGS
    % Q2 — step med 17%% overshoot
    f = figure('Color','w','Position',[100 100 560 360]);
    step(feedback(K2/(s*(s+2)),1)); grid on;
    title('Q2: lukket sløjfe, 17% overshoot (\zeta=0.5)');
    exportgraphics(f, fullfile(figdir,'Q2_step_overshoot.png'),'Resolution',150);

    % Q5 — Bode af (s+2)/(s+4)^2
    f = figure('Color','w','Position',[100 100 560 420]);
    bode(G5); grid on; title('Q5: G(s)=(s+2)/(s+4)^2  (DC = -18.1 dB)');
    exportgraphics(f, fullfile(figdir,'Q5_bode.png'),'Resolution',150);

    % Q7 — step der settler ~50
    f = figure('Color','w','Position',[100 100 560 360]);
    step(G7, 80); grid on; title('Q7: settling til 99% ved ~50 s (dom. pol -0.1)');
    exportgraphics(f, fullfile(figdir,'Q7_settling.png'),'Resolution',150);

    % Q8 — strøm-step-respons (facit-TF, matcher plot n.3)
    f = figure('Color','w','Position',[100 100 560 360]);
    step(10*IV_facit/s, 0.014); grid on;   % I(s)=10/(s^2+1000s+1e6)
    title('Q8: strøm i(t), step 0..10V — start 0, svinger, dør mod 0');
    exportgraphics(f, fullfile(figdir,'Q8_current_step.png'),'Resolution',150);

    fprintf('\n[figurer gemt i %s]\n', figdir);
end
