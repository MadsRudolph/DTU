%% ========================================================================
%  solve_F22.m  —  Linear Control Design 1, eksamen F22 (25-05-2022)
%  20 multiple-choice spørgsmål. Dette script genberegner de spørgsmål der
%  kræver udregning og udskriver svaret + det officielle facit-bogstav.
%
%  Facit-kilde: "Solutions to Exam F22 LCD1.pdf" (Papageorgiou & Tolu).
%  Konceptuelle spørgsmål (Q1,Q3,Q4,Q5,Q10,Q15,Q20) løses ved aflæsning/teori
%  og er kun noteret som kommentar — ingen MATLAB nødvendig.
%
%  Kør hele filen (F5). Hvert afsnit printer "beregnet" vs "facit".
%  Sæt MAKE_FIGS = true for at eksportere nøgleplots til Obsidian
%  (Images/exam/F22/).
% =========================================================================
clear; clc; close all;
MAKE_FIGS = false;          % true -> gem grafer til Obsidian-noten
s = tf('s');
fprintf('===== LCD1 F22 — beregnede svar =====\n\n');

% --- figur-mappe (beregnes ud fra scriptets egen placering) ---------------
here = fileparts(mfilename('fullpath'));
root = here; for k = 1:5, root = fileparts(root); end     % op til DTU-roden
figdir = fullfile(root,'Obsidian','Courses','34722 Linear Control Design 1', ...
                  'Images','exam','F22');
if MAKE_FIGS && ~exist(figdir,'dir'), mkdir(figdir); end

%% Q1 — Blokdiagram-reduktion (konceptuelt)
% Facit: svar 1.  Y/R = ABE^2(C+D) / ( (1+AB)[1+(C+D)E*H2]E + ABE(C+D)H1 ).
% Regel: A,B i serie -> gang. C,D parallelt -> plus. Flyt take-off efter E
% (H1 divideres med E). Reducer indre feedback-løkke, så ydre.

%% Q2 — RC-kredsløb, tidskonstant (konceptuelt)
% G = (1/RC)/(s+1/RC), R=50, C=160e-6 (bemærk: "160F" i opgaven er µF).
% tau = RC = 8 ms. Steady state ~ 5*tau = 40 ms. 63.2% efter 1*tau = 8 ms.
% Facit: svar 5 er FALSK (påstår 16 ms; korrekt er 8 ms).
RC = 50*160e-6;  fprintf('Q2: tau = %.0f ms, 5*tau = %.0f ms (facit: udsagn 5 falsk)\n', RC*1e3, 5*RC*1e3);

%% Q3 — 2.-ordens step-respons vs zeta (konceptuelt)
% zeta=0 -> udæmpet sinus, konstant amplitude. Facit: svar 1.

%% Q4 — Bode-identifikation (konceptuelt)
% Én reel zero i RHP + to konjugerede poler på imaginæraksen (Re=0).
% RHP-zero: +20 dB/dek men -90 grader fase (fasefald). Facit: svar 4.

%% Q5 — Bode-aflæsning -> identificér G(s) (konceptuelt)
% DC-gain ~5.9 dB ~ x2; flad til w=1, så -40 dB/dek (2 poler); fase 165->-90
% (én zero); ingen peak -> reelle poler; positive poler/zero.
% Facit: svar 5 -> G(s) = (s-2)/(1+s)^2.
G5 = (s-2)/(1+s)^2;  fprintf('Q5: DC-gain |G5(0)| = %.2f ( = %.2f dB )\n', abs(dcgain(G5)), 20*log10(abs(dcgain(G5))));

%% Q6 — Find K så PM = 40 grader,  G(s) = K/(s(s+a))
% BEMÆRK TRYKFEJL: opgaven skriver s+21, men facit K=8.4 passer kun med a=2.1.
% (kontroller: 20*log10(8.4) = 18.5 dB, som facit henviser til.)
a = 2.1;                       % polens placering der reproducerer facit
G1 = 1/(s*(s+a));              % systemet med K=1
w  = logspace(-2,3,2e5);
ph = squeeze(angle(freqresp(G1,w)))*180/pi;   % fase i grader (negativ)
wc = interp1(ph, w, -180+40);                 % w hvor fase = -140 -> PM=40
K  = 1/abs(freqresp(G1,wc));
fprintf('Q6: wc = %.3f rad/s,  K = %.3f   (facit: K = 8.4, svar 2)\n', wc, K);

%% Q7 — DC-gain i dB,  G(s) = 12/((s+2)(s+3))
G7 = 12/((s+2)*(s+3));
fprintf('Q7: DC = %.0f ( = %.0f dB )   (facit: 6 dB, svar 3)\n', dcgain(G7), 20*log10(dcgain(G7)));

%% Q8 — ODE 5y'' + y' + 0.5y = 3u -> poler
G8 = 3/(5*s^2 + s + 0.5);
fprintf('Q8: poler = '); disp(pole(G8).');   % -0.1 +/- 0.3j  (facit: svar 2)

%% Q9 — State-space, find w så poler i LHP (konceptuelt/symbolsk)
% x1' = -x1 + x2 ; x2' = 2x1 - w*x2.  A = [-1 1; 2 -w].
% char.lign: s^2 + (1+w)s + (w-2) = 0. Routh: stabil for w>2.  Facit: svar 4.
for wtest = [1.5 2 3]
    A = [-1 1; 2 -wtest];
    fprintf('Q9: w=%.1f -> max(real(eig)) = %+.3f\n', wtest, max(real(eig(A))));
end  % kun w=3 giver alle poler i LHP

%% Q10 — s^2+2s+2=0 -> dæmpningstype (konceptuelt)
% wn=sqrt(2), 2*zeta*wn=2 -> zeta=1/sqrt(2)=0.707 < 1 -> underdæmpet. Facit: svar 3.
fprintf('Q10: zeta = %.3f  -> underdæmpet (facit svar 3)\n', 2/(2*sqrt(2)));

%% Q11 — Nyquist gain margin. Skæring med negativ reel akse ved -0.1639.
GM   = 1/0.1639;
GMdB = 20*log10(GM);
fprintf('Q11: KM = %.2f ( = %.2f dB )   (facit: 15.71 dB, svar b)\n', GM, GMdB);

%% Q12 — Ustabilt system (pol i RHP), Nyquist skærer reel akse ved -0.0222.
% For CCW-encirkling af (-1,0) kræves KP > 1/0.0222 ~ 45.  Facit: KP=50 (svar b).
fprintf('Q12: KP-grænse = %.1f  (facit: KP=50 > 45, svar b)\n', 1/0.0222);

%% Q13 — Lead-bidrag i dB. CD=(0.355s+1)/(a*0.355s+1), |Gol(10j)|=1 -> wc=10.
tau_d = 0.355;  wc13 = 10;
alpha13 = (1/(wc13*tau_d))^2;            % tau_d = 1/(wc*sqrt(alpha))
MD = 1/sqrt(alpha13);
fprintf('Q13: alpha = %.4f,  MD = %.3f ( = %.2f dB )  (facit: 11 dB, svar c)\n', alpha13, MD, 20*log10(MD));

%% Q14 — Bode (lukket sløjfe) -> fejl-step-respons (konceptuelt)
% 0 dB ved lave frekvenser -> e_ss = 0; resonanstop -> komplekse poler -> svingninger.
% Facit: svar e (dæmpede svingninger mod 0).

%% Q15 — 4.-ordens type-0, zero ved lavere frekvens end polerne (konceptuelt)
% 3 flere poler end zeroes -> fase når -270; zero før poler -> magnitude op så ned
% -> kan give to crossover-frekvenser.  Facit: svar d.

%% Q16 — Steady-state error -> KP.  e_ss = 1/(1+KP*G(0)) = 0.555.
% Fra Bode: G(0) = -7.9588 dB ~ 0.4.
G0   = 10^(-7.9588/20);
KP16 = (1/G0)*(1/0.555 - 1);
fprintf('Q16: G(0)=%.3f,  KP = %.2f   (facit: KP=2, svar b)\n', G0, KP16);

%% Q17 — PI-Lead: find alpha. phiG=-112.77, Ni=5, wc=6.4, gammaM=75.
phiG = -112.77;  Ni = 5;  gammaM = 75;
phi_i = -atand(1/Ni);                          % PI-bidrag (grader)
phi_m = -180 + gammaM - phiG - phi_i;          % nødvendigt Lead-bidrag
alpha17 = (1 - sind(phi_m))/(1 + sind(phi_m));
fprintf('Q17: phi_m = %.2f deg,  alpha = %.4f   (facit: 0.5, svar e)\n', phi_m, alpha17);

%% Q19 — PI-Lead: find KP.  G=900/((0.25s+1)(s^2+50s+3000)), gammaM=75, Ni=3.
% TRYKFEJL: opgaven skriver alpha=0.001, men den officielle løsning REGNER med
% alpha=0.01 (bekræftet: tau_d=0.1983=1/(50.42*sqrt(0.01)) og phi_m=78.58 deg
% =asin((1-0.01)/(1+0.01))). Med alpha=0.001 fås KP~1.2; facit 3.4154 kræver 0.01.
G19   = 900/((0.25*s+1)*(s^2+50*s+3000));
Ni19  = 3;  alpha19 = 0.01;  gammaM19 = 75;   % 0.01, ikke 0.001 (se note ovenfor)
phi_i19 = -atand(1/Ni19);
phi_m19 =  asind((1-alpha19)/(1+alpha19));
phiG_req = -180 + gammaM19 - phi_i19 - phi_m19;     % krævet fase fra G
phG19 = squeeze(angle(freqresp(G19,w)))*180/pi;
wc19  = interp1(phG19, w, phiG_req);               % ny crossover
tau_i = Ni19/wc19;   tau_d19 = 1/(wc19*sqrt(alpha19));
CPI   = (tau_i*s+1)/(tau_i*s);
CD    = (tau_d19*s+1)/(alpha19*tau_d19*s+1);
KP19  = 1/abs(freqresp(G19*CPI*CD, wc19));
fprintf('Q19: wc = %.3f rad/s,  KP = %.4f   (facit: 3.4154, svar a)\n', wc19, KP19);

%% Q20 — Konceptuelt. Højere PM -> færre svingninger + mere robusthed. Facit: svar a.

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1:1 Q2:5 Q3:1 Q4:4 Q5:5 Q6:2 Q7:3 Q8:2 Q9:4 Q10:3\n');
fprintf('Q11:b Q12:b Q13:c Q14:e Q15:d Q16:b Q17:e Q18:d Q19:a Q20:a\n');

%% ----------------------------- FIGURER -----------------------------------
if MAKE_FIGS
    % Q5 — Bode med RHP-zero: magnitude op (+20 dB/dek) men fase FALDER (-90)
    f = figure('Color','w','Position',[100 100 560 420]);
    bode(G5); grid on; title('Q5: G(s)=(s-2)/(1+s)^2  — RHP-zero (fase falder)');
    exportgraphics(f, fullfile(figdir,'Q5_bode_RHPzero.png'),'Resolution',150);

    % Q6 — åben sløjfe K*G1 med PM ~ 40 grader
    f = figure('Color','w','Position',[100 100 560 420]);
    margin(K*G1); grid on; title('Q6: K=8.4 giver PM \approx 40^\circ');
    exportgraphics(f, fullfile(figdir,'Q6_margin_PM40.png'),'Resolution',150);

    % Q19 — kompenseret åben sløjfe (PI-Lead), tjek crossover + PM
    f = figure('Color','w','Position',[100 100 560 420]);
    margin(KP19*G19*CPI*CD); grid on;
    title('Q19: PI-Lead kompenseret \omega_c og PM (K_P=3.42)');
    exportgraphics(f, fullfile(figdir,'Q19_PIlead_margin.png'),'Resolution',150);

    fprintf('\n[figurer gemt i %s]\n', figdir);
end
