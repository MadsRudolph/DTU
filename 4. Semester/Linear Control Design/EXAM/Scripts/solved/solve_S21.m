%% ========================================================================
%  solve_S21.m  —  Linear Control Design 1, eksamen S21 (31 maj 2021)
%  10 multiple-choice spørgsmål. Genberegner de udregningstunge spørgsmål
%  og udskriver svaret + det officielle facit (grøn "CORRECT" i PDF).
%
%  Facit-kilde: "Exam_S21.pdf" (10 questions LC1 exam 31.05.2021, m. løsninger).
%  Konceptuelle/symbolske (Q1,Q2,Q3,Q5,Q7,Q10) er kun noteret som kommentar.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== LCD1 S21 — beregnede svar =====\n\n');

%% Q1 — Blokdiagram (symbolsk). To fremadgrene (ABCD via B, samt ECD via E),
% fælles feedback BCF.  Y/U = (ABCD + ECD)/(1 + BCF).  Facit: svar 2.

%% Q2 — RLC-kredsløb -> blokdiagram. I = (Vi - Vo)*1/(R+sL), Vo = I*1/(sC).
% Dvs. fremad 1/(R+sL) så 1/(sC), enheds-feedback.  Facit: svar 1.

%% Q3 — Pol-zero-kort -> Bode. Zero ved -2.5 (reel), komplekse poler ved -1.5.
% Mag starter ~-5 dB (flad), fasefald -90.  Facit: svar 4.

%% Q4 — P-stabilt interval, P(s)=1/(s+1)^3, lukket sløjfe L=K/(s+1)^3.
% Fase=-180 ved -3*atan(w)=-180 -> atan(w)=60 -> w=tan60=sqrt(3).
% |L(jw)|=K/(sqrt(1+3))^3 = K/8 = 1 -> K=8.  Stabil for 0<K<8.  Facit: svar 3.
wbar = tand(60);
absL_at_w = 1/abs(freqresp(1/(s+1)^3, wbar));   % = 8
fprintf('Q4: w(-180)=%.3f, K_graense = %.2f -> stabil 0<K<%.0f  (facit: svar 3)\n', ...
        wbar, absL_at_w, absL_at_w);

%% Q5 — Bode-ID (konceptuelt). DC 40 dB=100; -40 dB/dek fra w=1 (2 reelle poler);
% fase ned 180 ved w=1; ved w=10 yderligere -20 dB/dek + fase op 90 -> 1 positiv pol.
% G = 100/((1+s)^2*(1-0.1s)).  Facit: svar 1 (neg. OG pos. reelle poler, ingen zeroes).

%% Q6 — Find K så PM=40. Ved wc(PM=40) er fase -140 -> aflæst w=2.28, |G|=-38.9 dB.
% K skubber kurven op til 0 dB: K = db2mag(38.9).
K6 = 10^(38.9/20);
fprintf('Q6: K = %.1f   (facit: 88, svar 5)\n', K6);

%% Q7 — To masser m1=m2=1 koblet med fjeder k=1, kraft F på m1, udgang x2.
% m1*x1'' + k(x1-x2) = F ;  m2*x2'' + k(x2-x1) = 0.
% X2/F = k/((m2 s^2+k)(m1 s^2+k) - k^2) = 1/(s^2 (s^2+2)).  Facit: svar 2.
G7 = 1/(s^2*(s^2+2));
fprintf('Q7: X2/F = 1/(s^2(s^2+2)), poler: '); disp(pole(G7).');  % facit svar 2

%% Q8 — ODE y''+2y'+y=u -> G=1/(s^2+2s+1) -> dobbeltpol s=-1.  Facit: svar 2.
G8 = 1/(s^2+2*s+1);
fprintf('Q8: poler = '); disp(pole(G8).');   % -1, -1 (facit svar 2)

%% Q9 — P-gain så overshoot <= 12% for K/(s(s+5)).
% Lukket: wn=sqrt(K), zeta=5/(2*wn)=2.5/sqrt(K).
% Mp<=0.12 -> zeta>=0.559 -> K = 6.25/zeta^2 <= 19.97.  Facit: 0<=K<=20, svar 1.
Mp9 = 0.12;
zeta9 = sqrt(log(1/Mp9)^2/(pi^2+log(1/Mp9)^2));
Kmax9 = 6.25/zeta9^2;
fprintf('Q9: zeta>=%.3f -> K <= %.2f   (facit: 0<=K<=20, svar 1)\n', zeta9, Kmax9);

%% Q10 — Magnitude-Bode (kun |G|): DC 20 dB = 10, falder til 0 dB. Ingen RHP-zeroes.
% Step-respons starter i 1 (initialværdi via b0/a... her starter ~1) og slutter i 10
% (DC-gain). Mp ingen overshoot synlig.  Facit: svar 1 (step 1 -> 10).
fprintf('Q10: DC-gain = 10 (20 dB) -> step slutter i 10  (facit: svar 1)\n');

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1:2  Q2:1  Q3:4  Q4:3  Q5:1  Q6:5  Q7:2  Q8:2  Q9:1  Q10:1\n');
