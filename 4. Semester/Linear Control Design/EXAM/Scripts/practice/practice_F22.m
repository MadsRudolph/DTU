%% ========================================================================
%  practice_F22.m  —  ØVELSE: eksamen F22 (25-05-2022), 20 MC-spm.
%
%  SÅDAN BRUGES DEN:
%   1. Åbn PDF'en "LCD1 F22 - Questions no answers.pdf" (dæk facit til).
%   2. Udfyld hver TODO nedenfor (erstat NaN med din udregning).
%   3. Kør filen (F5) — den printer DINE svar.
%   4. Ret efter ved at køre  solved/solve_F22.m  og sammenligne.
%
%  Givne værdier er fyldt ud; selve udregningen er din. NaN = ikke løst endnu.
%  Konceptuelle spm (Q1,Q3,Q4,Q9,Q14,Q15,Q18,Q20) besvares som kommentar.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== ØVELSE: eksamen F22 — dine svar =====\n\n');

%% Q1 — Blokdiagram-reduktion (konceptuelt). Find Y/R.
% A,B i serie; C,D parallelt; E i kæden; H1,H2 feedback. Take-off efter E.
% TODO (kommentar): reducer i hånden. Hvilket svar (1-5)?
% Y/R = ____________________________      svar = ?

%% Q2 — RC-kredsløb. R=50, C=160uF. tau? 5*tau? (udsagn 5: 16 ms — sandt/falsk?)
R2 = 50;  C2 = 160e-6;
% TODO: tau = R*C; afgør om udsagn 5 (16 ms) er falsk.
tau2 = NaN;        % R*C i sekunder
fprintf('Q2: tau = %g ms,  5*tau = %g ms\n', tau2*1e3, 5*tau2*1e3);

%% Q3 — 2.-ordens step-respons vs zeta (konceptuelt). zeta=0 -> ?
% TODO (kommentar): hvilken kurveform for zeta=0?  svar (1-5) = ?

%% Q4 — Bode-identifikation (konceptuelt). +20 dB/dek men fase falder mod -90.
% TODO (kommentar): hvad fortæller fasefaldet? (RHP-zero?)  svar = ?

%% Q5 — Bode-aflæsning -> identificér G(s). DC~5.9 dB; -40 dB/dek; fase 165->-90.
% TODO: vælg kandidat-G og find DC-gain i dB.
G5   = tf(1,1);    % TODO: erstat med din kandidat, fx (s-2)/(1+s)^2
dcdB5 = NaN;       % 20*log10(|G5(0)|)
fprintf('Q5: DC = %g dB\n', dcdB5);

%% Q6 — Find K saa PM=40 grader, G(s)=K/(s(s+a)).  (NB: trykfejl s+21 -> brug a=2.1)
a6 = 2.1;
G1_6 = 1/(s*(s+a6));    % systemet med K=1
% TODO: find wc hvor fase = -140 (PM=40); K = 1/|G1(jwc)|.
K6 = NaN;
fprintf('Q6: K = %g  (facit-hint: ~8.4)\n', K6);

%% Q7 — DC-gain i dB, G(s)=12/((s+2)(s+3)).
G7 = 12/((s+2)*(s+3));
% TODO: DC = dcgain(G7); i dB = 20*log10(DC).
dcdB7 = NaN;
fprintf('Q7: DC = %g dB\n', dcdB7);

%% Q8 — ODE 5y'' + y' + 0.5y = 3u -> poler.
G8 = 3/(5*s^2 + s + 0.5);
% TODO: poler = pole(G8).
p8 = [NaN NaN];
fprintf('Q8: poler = %s\n', mat2str(p8,3));

%% Q9 — State-space x1'=-x1+x2 ; x2'=2x1-w*x2. For hvilke w er systemet stabilt?
% A = [-1 1; 2 -w]. char: s^2+(1+w)s+(w-2). Routh -> stabil for ?
% TODO (kommentar): w-grænse for stabilitet?  svar = ?
wmin9 = NaN;       % nedre grænse for w
fprintf('Q9: stabil for w > %g\n', wmin9);

%% Q10 — s^2+2s+2=0 -> dæmpningstype (konceptuelt).
% TODO: zeta = ? -> under/kritisk/overdæmpet?
zeta10 = NaN;
fprintf('Q10: zeta = %g\n', zeta10);

%% Q11 — Nyquist gain margin. Skæring med neg. reel akse ved -0.1639. GM i dB?
cross11 = 0.1639;
% TODO: GM = 1/cross; i dB = 20*log10(GM).
GMdB11 = NaN;
fprintf('Q11: GM = %g dB\n', GMdB11);

%% Q12 — Ustabilt system (RHP-pol). Nyquist skærer reel akse ved -0.0222. KP-grænse?
cross12 = 0.0222;
% TODO: for ustabil plante kræves KP > 1/|skæring|.
KPmin12 = NaN;
fprintf('Q12: KP-grænse = %g\n', KPmin12);

%% Q13 — Lead-bidrag i dB. CD=(0.355s+1)/(a*0.355s+1), |Gol(10j)|=1 -> wc=10.
tau_d13 = 0.355;  wc13 = 10;
% TODO: alpha = (1/(wc*tau_d))^2;  MD = 1/sqrt(alpha);  i dB.
MDdB13 = NaN;
fprintf('Q13: lead-bidrag = %g dB\n', MDdB13);

%% Q14 — Bode (lukket sløjfe) -> fejl-step-respons (konceptuelt).
% 0 dB ved lave frekv. -> e_ss=?; resonanstop -> ?
% TODO (kommentar): hvilken fejl-respons?  svar = ?

%% Q15 — 4.-ordens type-0, zero ved lavere frekvens end polerne (konceptuelt).
% TODO (kommentar): fase når? antal crossover-frekvenser?  svar = ?

%% Q16 — Steady-state error -> KP.  e_ss = 1/(1+KP*G(0)) = 0.555. G(0)=-7.9588 dB.
G0dB16 = -7.9588;  ess16 = 0.555;
% TODO: G0 = 10^(G0dB/20);  KP = (1/G0)*(1/ess - 1).
KP16 = NaN;
fprintf('Q16: KP = %g\n', KP16);

%% Q17 — PI-Lead: find alpha. phiG=-112.77, Ni=5, gammaM=75.
phiG17 = -112.77;  Ni17 = 5;  gammaM17 = 75;
% TODO: phi_i = -atand(1/Ni);  phi_m = -180+gammaM-phiG-phi_i;
%       alpha = (1-sind(phi_m))/(1+sind(phi_m)).
alpha17 = NaN;
fprintf('Q17: alpha = %g\n', alpha17);

%% Q18 — (konceptuelt, facit svar d). Besvar som kommentar.
% TODO (kommentar): svar = ?

%% Q19 — PI-Lead: find KP. G=900/((0.25s+1)(s^2+50s+3000)), gammaM=75, Ni=3.
%  NB: trykfejl alpha=0.001 i opgaven -> den officielle løsning bruger alpha=0.01.
G19 = 900/((0.25*s+1)*(s^2+50*s+3000));
Ni19 = 3;  alpha19 = 0.01;  gammaM19 = 75;
% TODO: phi_i = -atand(1/Ni);  phi_m = asind((1-alpha)/(1+alpha));
%       phiG_req = -180+gammaM-phi_i-phi_m;  find wc; tau_i=Ni/wc; tau_d=1/(wc*sqrt(alpha));
%       CPI=(tau_i*s+1)/(tau_i*s); CD=(tau_d*s+1)/(alpha*tau_d*s+1); KP=1/|G*CPI*CD(jwc)|.
KP19 = NaN;
fprintf('Q19: KP = %g  (facit-hint: ~3.4154)\n', KP19);

%% Q20 — Højere PM -> ? (konceptuelt).
% TODO (kommentar): effekt af højere fasemargin?  svar = ?

fprintf('\n>> Ret efter med:  solved/solve_F22.m\n');
