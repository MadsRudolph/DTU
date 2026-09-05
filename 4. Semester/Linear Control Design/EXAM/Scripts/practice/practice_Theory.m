%% ========================================================================
%  practice_Theory.m  —  ØVELSE: Theoretical Exercises LCD1, 10 opgaver.
%
%  SÅDAN BRUGES DEN:
%   1. Åbn PDF'en "LCD1 Theory Exercises.pdf" (og dæk evt. P7-noten til).
%   2. Q1-Q3 + Q10 er BEVISER — skriv udledningen i kommentaren.
%      Q4-Q9 er numerik — erstat NaN med din udregning.
%   3. Kør filen (F5) — den printer DINE numeriske svar.
%   4. Ret efter ved at køre  solved/solve_Theory.m  og sammenligne.
%
%  Givne værdier er fyldt ud; selve udregningen er din. NaN = ikke løst endnu.
% =========================================================================
clear; clc; close all;
s = tf('s');
fprintf('===== ØVELSE: Theoretical Exercises — dine svar =====\n\n');

%% Q1 (BEVIS) — Lead CD=(td*s+1)/(a*td*s+1): vis wm=1/(td*sqrt(a)), phi_m.
% TODO (kommentar): sæt s=jw, skriv tan(phi(w)), dPhi/dw=0 -> wm.
%   wm = ____________   phi_m = arctan(__________) = arcsin(__________)
% (Tjek: |CD(jwm)| = 1/sqrt(a), og wm = geom. middel af zero 1/td og pol 1/(a*td).)

%% Q2 (BEVIS) — 1.-ordens LPF G=1/(tau*s+1): vis wc=wBW=1/tau, tr~2.2tau, ts~4tau.
% TODO (kommentar):
%   wBW: |G|=1/sqrt(2) ved -3 dB  ->  wBW = ______
%   wc : unity feedback af 1/(tau*s), |Gol(jwc)|=1  ->  wc = ______
%   tr : y(t)=1-e^{-t/tau}, 10->90%%  ->  tr = tau*ln(9) ~ ______
%   ts : 2%% (overdæmpet 98%%)         ->  ts = tau*ln(50) ~ ______

%% Q3 (BEVIS) — P-Lag CL=(ti*s+1)/(ti*s+1/b) ved wc=Ni/ti: vis phi_L, samt limit.
% TODO (kommentar):
%   phi_L = arctan( Ni*(1-b)/(1+b*Ni^2) )   (b>1 -> phi_L<0, lag fjerner fase)
%   lim(b->inf) phi_L = -arctan(1/Ni)   (= PI-leddet)

%% Q4 (Eksamen 2021) — poler af y'''' + 9y''' + 20y'' = 71u.
G4 = 71/(s^4 + 9*s^3 + 20*s^2);
% TODO: poler = pole(G4); (hvor mange i origo? -> systemtype + stabilitet?)
p4 = [NaN NaN NaN NaN];
fprintf('Q4: poler = %s\n', mat2str(p4,3));

%% Q5 (Eksamen 2021) — G=1224/(s^3+30s^2+257s+612), KP=2 i FEEDBACK. ess (unit step)?
G5 = 1224/(s^3 + 30*s^2 + 257*s + 612);  KP5 = 2;
% TODO: ess = 1/(1+KP*G(0));  (G(0)=dcgain(G5))
ess5 = NaN;
fprintf('Q5: ess = %g\n', ess5);

%% Q6 (Eksamen 2021) — indre/ydre løkke. eps1=0.4, eps2=0.05, G2(0)=-7.9588 dB. Find K2.
eps1 = 0.4;  eps2 = 0.05;  G2_0dB = -7.9588;
% TODO: G2_0 = 10^(G2_0dB/20);  K2 = (1-eps2)/(eps2*G2_0*(1-eps1));
K2 = NaN;
fprintf('Q6: K2 = %g\n', K2);

%% Q7 (Re-Eksamen 2021) — kaskade 4/(s+1)*2/(s+2)*...*N/(s+N), unity feedback. Gcl(0)?
% TODO: ved s=0 teleskoperer produktet -> Gol(0)=4; Gcl(0)=Gol(0)/(1+Gol(0)).
Gcl0 = NaN;
fprintf('Q7: Gcl(0) = %g\n', Gcl0);

%% Q8 (Eksamen 2022, KONCEPT) — vælg feed-forward Fd. Svar (a-e)?
% TODO (kommentar): Fd = D/G1 gjort proper med (n-2)-ordens HURTIG LPF.
%   Hvilken mulighed er proper OG hurtig (tf<=min(tk)/5)?   svar = ?

%% Q9 (Re-Eksamen 2022) — to indlejrede P-regulatorer. e(0)=0.25, G(0)=0.75. KP?
G0_9 = 0.75;  e0_9 = 0.25;
% TODO: Ge(0)=(1+KP*G0)/(1+KP*G0+KP^2*G0)=e0 -> kvadratisk i KP. Vælg positiv rod.
KP9 = NaN;
fprintf('Q9: KP = %g\n', KP9);

%% Q10 (BEVIS) — P-Lag reducerer ess med faktor beta; beta->inf => PI => ess->0.
% TODO (kommentar):
%   e_ss = 1/(1+KP*p),  e_ss,lag = 1/(1+KP*beta*p)  (fordi CL(0)=KP*beta)
%   ratio = (1+KP*beta*p)/(1+KP*p) ~ beta   naar KP*p >> 1.
%   beta->inf: CL -> KP*(ti*s+1)/(ti*s) = PI (integrator) -> type+1 -> ess->0.

fprintf('\n>> Ret efter med:  solved/solve_Theory.m  (+ læs P7 i Obsidian)\n');
