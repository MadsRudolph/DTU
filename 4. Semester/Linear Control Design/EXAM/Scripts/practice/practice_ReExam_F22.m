%% ========================================================================
%  practice_ReExam_F22.m  —  ØVELSE: RE-eksamen F22 (17-08-2022), 10 MC-spm.
%
%  SÅDAN BRUGES DEN:
%   1. Åbn PDF'en "LCD1 ReExam F22 - Questions with answers.pdf" (dæk facit til).
%   2. Udfyld hver TODO nedenfor (erstat NaN med din udregning).
%   3. Kør filen (F5) — den printer DINE svar.
%   4. Ret efter ved at køre  solved/solve_ReExam_F22.m  og sammenligne.
%
%  Givne værdier er fyldt ud; selve udregningen er din. NaN = ikke løst endnu.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== ØVELSE: RE-eksamen F22 — dine svar =====\n\n');

%% Q1 — Lineariser z = y^2 + 5xy - 3x^2 om (xb=3, yb=11). Fejl i %% ved (4,12)?
xb = 3; yb = 11; xn = 4; yn = 12;
% TODO: A = dz/dx, B = dz/dy i arbejdspunktet; byg lineær model; fejl i %%.
A1 = NaN;        % dz/dx ved (xb,yb)
B1 = NaN;        % dz/dy ved (xb,yb)
e1 = NaN;        % |z_true - z_lin| / z_true * 100
fprintf('Q1: A=%g B=%g  fejl = %g %%\n', A1, B1, e1);

%% Q2 — Lukket sløjfe K/s * 1/(s+2), 17%% overshoot. Find dæmpet frekvens wd.
% TODO: zeta fra overshoot (slide: 17%% -> ?); wn fra 2*zeta*wn=2; wd=wn*sqrt(1-zeta^2).
zeta2 = NaN;
wn2   = NaN;
wd2   = NaN;
fprintf('Q2: zeta=%g wn=%g  wd = %g rad/s\n', zeta2, wn2, wd2);

%% Q3 — Symbolsk: H(s) fra u til y (G3,G4 parallelt; feedback om G2; G1 i serie).
% TODO (kommentar): skriv den reducerede H(s). Hvilket svar (1-5)?
% H = ____________________________      svar = ?

%% Q4 — Indsæt G1=1/(s-2), G2=(s-2)/(s-7), G3=2/(s+2), G4=-1/(s+2). Stabilt?
G1 = 1/(s-2);  G2 = (s-2)/(s-7);  G3 = 2/(s+2);  G4 = -1/(s+2);
% TODO: byg H, find polerne, afgør stabilitet (RHP-pol?).
p4 = [NaN NaN];   % polerne i H(s)
fprintf('Q4: poler = [%g %g]\n', p4(1), p4(2));

%% Q5 — Bode: flad fase der så falder mod -90. Identificér poler/zeroes + DC-gain.
% TODO: hvilken polstruktur? (kommentar) og DC-gain i dB for din kandidat-G.
G5   = tf(1,1);   % TODO: erstat med din kandidat, fx (s+2)/(s+4)^2
dcdB = NaN;       % 20*log10(|G5(0)|)
fprintf('Q5: DC = %g dB\n', dcdB);

%% Q6 — G=1/(1+tau*s), input r=1+6t. e_ss for tau=5 vs tau=4?
% TODO: udled e_ss som funktion af tau (final value theorem), indsæt 5 og 4.
ess_5 = NaN;
ess_4 = NaN;
fprintf('Q6: e_ss(5)=%g  e_ss(4)=%g\n', ess_5, ess_4);

%% Q7 — G=10(s+1)/((s+0.1)(s^2+20s+100)). Settling til 99%%?
G7 = 10*(s+1)/((s+0.1)*(s^2+20*s+100));
% TODO: find dominerende (langsomste) pol -> tau; settling = 5*tau.
tau_dom = NaN;
ts99    = NaN;
fprintf('Q7: tau_dom=%g  5*tau = %g\n', tau_dom, ts99);

%% Q8 — RCL-serie (R=1, C=1uF, L=1H). Step 0..10V -> vælg strøm-step-respons.
% TODO (kommentar): skriv I/V. Hvilke 2 træk afgør plottet?
%   - i(0+) = ?   (initialværdisætning)     - i(inf) = ?  (slutværdi)
% svar (plot 1-4) = ?

%% Q9 — Laplace af x'' + x' - 2x = 4, x(0)=2, x'(0)=1.
% TODO (kommentar): transformér med begyndelsesbetingelser, isolér X(s).
% X(s) = ____________________________      svar = ?

%% Q10 — K*G/(1+K*G*H), G=1/(s(s+0.1)), K=5, H=1, input r=5 (step). e_ss?
G10 = 1/(s*(s+0.1));  K10 = 5;  H10 = 1;
% TODO: systemtype for åben sløjfe -> step-fejl?
ess10 = NaN;
fprintf('Q10: e_ss = %g\n', ess10);

fprintf('\n>> Ret efter med:  solved/solve_ReExam_F22.m\n');
