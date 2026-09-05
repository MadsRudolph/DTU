%% ========================================================================
%  solve_Theory.m  —  Linear Control Design 1, Theoretical Exercises
%  (Papageorgiou). 10 opgaver: Q1-Q3 + Q10 er BEVISER, Q4-Q9 er eksamens-
%  numerik (Q4,Q5,Q6,Q9 har optrådt på rigtige eksamener).
%
%  Dette script VERIFICERER de numeriske resultater og de symbolske formler
%  (ved at indsætte konkrete værdier og tjekke mod den udledte formel).
%  De fulde udledninger står i Obsidian: P7 — Theory Exercises.
%
%  Facit-kilde: "LCD1 Theory Exercises.pdf" + officiel Solutions-manual.
%  Sæt MAKE_FIGS = true for at eksportere Q1/Q2-plots til Obsidian.
%  Kør: F5  eller  matlab -batch "solve_Theory"
% =========================================================================
clear; clc; close all;
MAKE_FIGS = false;          % true -> gem grafer til Obsidian-noten (P7)
s = tf('s');
fprintf('===== LCD1 Theoretical Exercises — verifikation =====\n\n');

% --- figur-mappe (beregnes ud fra scriptets egen placering) ---------------
here = fileparts(mfilename('fullpath'));
root = here; for k = 1:5, root = fileparts(root); end     % op til DTU-roden
figdir = fullfile(root,'Obsidian','Courses','34722 Linear Control Design 1', ...
                  'Images','exam','Theory');
if MAKE_FIGS && ~exist(figdir,'dir'), mkdir(figdir); end

w = logspace(-3,3,2e5);

%% Q1 — Lead: max-fase ved wm = 1/(td*sqrt(alpha)), phi_m = asin((1-a)/(1+a))
% Verificér numerisk: vælg td=1, alpha=0.1, find toppunkt for fasen.
td = 1; alpha = 0.1;
CD = (td*s+1)/(alpha*td*s+1);
phCD = squeeze(angle(freqresp(CD,w)))*180/pi;
[phi_max_num, idx] = max(phCD);
wm_num   = w(idx);
wm_form  = 1/(td*sqrt(alpha));                 % formel
phi_form = asind((1-alpha)/(1+alpha));         % formel
magAtWm  = abs(freqresp(CD,wm_form));          % skal være 1/sqrt(alpha)
fprintf('Q1: wm   numerisk=%.3f  formel 1/(td*sqrt(a))=%.3f\n', wm_num, wm_form);
fprintf('    phi_m numerisk=%.2f  formel asin((1-a)/(1+a))=%.2f deg\n', phi_max_num, phi_form);
fprintf('    |CD(jwm)|=%.3f  formel 1/sqrt(a)=%.3f  (geom. middel af zero & pol)\n', ...
        magAtWm, 1/sqrt(alpha));

%% Q2 — 1.-ordens LPF: wc = wBW = 1/tau, tr ~ 2.2*tau, ts ~ 4*tau
tau = 2;  G2 = 1/(tau*s+1);
wBW = bandwidth(G2);                            % -3 dB båndbredde
S   = stepinfo(G2);                             % tr (10-90%), ts (2%)
fprintf('\nQ2: 1/tau=%.3f  wBW=%.3f (=wc)  | tr=%.3f vs 2.2*tau=%.3f  | ts=%.3f vs 4*tau=%.3f\n', ...
        1/tau, wBW, S.RiseTime, 2.2*tau, S.SettlingTime, 4*tau);

%% Q3 — P-Lag fasebidrag ved wc=Ni/ti:  phi_L = atan(Ni*(1-b)/(1+b*Ni^2))
% b>1 (lag) -> phi_L<0 (trækker fase fra). Limit b->inf = -atan(1/Ni) (= PI).
ti = 1; Ni = 3; beta = 10;
CL = (ti*s+1)/(ti*s+1/beta);
wc3 = Ni/ti;
phi_L_num  = angle(freqresp(CL,wc3))*180/pi;
phi_L_form = atand(Ni*(1-beta)/(1+beta*Ni^2));
phi_PI     = -atand(1/Ni);                       % limit b->inf
fprintf('\nQ3: phi_L numerisk=%.2f  formel=%.2f deg (<0: lag fjerner fase)\n', ...
        phi_L_num, phi_L_form);
fprintf('    lim(b->inf) phi_L = -atan(1/Ni) = %.2f deg  (= PI-leddet)\n', phi_PI);

%% Q4 (Eksamen 2021) — poler af y'''' + 9y''' + 20y'' = 71u
% G = 71/(s^4+9s^3+20s^2) = 71/(s^2(s+4)(s+5)). Dobbeltpol i 0 -> ustabil, type-2.
G4 = 71/(s^4 + 9*s^3 + 20*s^2);
p4 = pole(G4);
fprintf('\nQ4: poler = %s  (dobbeltpol i 0 -> ustabil, type-2)\n', mat2str(sort(real(p4)),3));

%% Q5 (Eksamen 2021) — KP=2 i FEEDBACK-grenen. ess ved unit step?
% Ger = 1/(1+KP*G),  ess = Ger(0) = 1/(1+KP*G(0)).
G5 = 1224/(s^3 + 30*s^2 + 257*s + 612);
KP5 = 2;
ess5 = 1/(1 + KP5*dcgain(G5));                   % G(0)=1224/612=2 -> 1/5
fprintf('\nQ5: G(0)=%.0f,  ess = 1/(1+KP*G(0)) = %.3f  (gain i feedback: stadig 1/(1+KPG(0)))\n', ...
        dcgain(G5), ess5);

%% Q6 (Eksamen 2021) — indre/ydre løkke, find K2.
% Ydre åbnet ved A: step 1/K2 giver e1(0)=eps1=0.4  -> K1G1(0)=(1-eps1)/eps1.
% Lukket indre løkke bidrager DC-gain (1-eps1) til ydre. G2 type-0, G2(0)=0.4 (=-7.9588 dB).
% eps2 = 1/(1+K2*(1-eps1)*G2(0))  -> K2 = (1-eps2)/(eps2*G2(0)*(1-eps1)).
eps1 = 0.4; eps2 = 0.05; G2_0 = 10^(-7.9588/20); % ~0.4
K2 = (1-eps2)/(eps2*G2_0*(1-eps1));
fprintf('\nQ6: G2(0)=%.3f,  K2 = (1-e2)/(e2*G2(0)*(1-e1)) = %.2f\n', G2_0, K2);

%% Q7 (Re-Eksamen 2021) — kaskade 4/(s+1)*2/(s+2)*...*N/(s+N), unity feedback.
% Ved s=0 er hvert led i/(0+i)=1, så kun ledende tæller 4 overlever: Gol(0)=4.
% Gcl(0) = Gol(0)/(1+Gol(0)) = 4/5.
Gol0 = 4;                                        % teleskoperer -> kun 4 tilbage
Gcl0 = Gol0/(1+Gol0);
fprintf('\nQ7: Gol(0)=%.0f (teleskoperer),  Gcl(0) = %.0f/%.0f = %.2f\n', ...
        Gol0, Gol0, 1+Gol0, Gcl0);

%% Q8 (Eksamen 2022) — vælg feed-forward Fd = D/G1, gjort proper med HURTIG LPF.
% Fd = D*prod(tk*s+1) / [ (s^2+2*zeta*wn*s+wn^2) * (tf*s+1)^(n-2) ],  tf <= min(tk)/5.
% Kun mulighed (d): proper OG hurtig. (a)(b)(c) forkert antal poler; (e) for langsom.
fprintf('\nQ8: Fd = D/G1 + (n-2)-ordens HURTIG LPF (tf<=min(tk)/5)  -> svar (d)\n');

%% Q9 (Re-Eksamen 2022) — to indlejrede P-regulatorer, find KP. (kvadratisk!)
% Ge = (1+KP*G)/(1+KP*G+KP^2*G).  Ved s=0: G(0)=0.75, e(0)=0.25
% -> KP^2 - 3KP - 4 = 0 -> (KP-4)(KP+1)=0 -> KP=4 (KP>0).
G0_9 = 0.75; e0_9 = 0.25;
KProots = roots([1 -3 -4]);                      % fra 0.25 = (1+0.75KP)/(1+0.75KP+0.75KP^2)
KP9 = KProots(KProots>0);
fprintf('\nQ9: KP^2-3KP-4=0 -> KP = %.0f  (positiv rod; indre løkke gør ligningen kvadratisk)\n', KP9);

%% Q10 — P-Lag reducerer ess med faktor beta; beta->inf = PI -> ess->0.
% e_ss   = 1/(1+KP*p),   e_ss,lag = 1/(1+KP*beta*p)  (CL(0)=KP*beta)
% ratio  = (1+KP*beta*p)/(1+KP*p) ~ beta  naar KP*p >> 1.
fprintf('\nQ10: e_ss/e_ss,lag ~ beta (CL(0)=KP*beta);  beta->inf => PI => ess->0\n');

fprintf('\n===== facit-oversigt =====\n');
fprintf('Q1: wm=1/(td*sqrt(a)), phi_m=asin((1-a)/(1+a)), gain 1/sqrt(a)\n');
fprintf('Q2: wc=wBW=1/tau, tr~2.2tau, ts~4tau   Q3: phi_L=atan(Ni(1-b)/(1+bNi^2))\n');
fprintf('Q4: {0,0,-4,-5}  Q5: 0.2  Q6: 79.17  Q7: 0.8  Q8: (d)  Q9: 4  Q10: faktor beta\n');

%% ----------------------------- FIGURER -----------------------------------
if MAKE_FIGS
    % Q1 — Lead-fasens toppunkt ved wm (geometrisk middel af zero & pol)
    f = figure('Color','w','Position',[100 100 560 420]);
    semilogx(w, phCD, 'LineWidth',1.4); grid on; hold on;
    xline(wm_form,'--'); yline(phi_form,'--');
    plot(wm_form, phi_form,'ro','MarkerFaceColor','r');
    xlabel('\omega [rad/s]'); ylabel('\angle C_D  [deg]');
    title(sprintf('Q1: Lead-fase, top ved \\omega_m=1/(\\tau_d\\surd\\alpha)=%.2f, \\phi_m=%.1f^\\circ', ...
          wm_form, phi_form));
    exportgraphics(f, fullfile(figdir,'Q1_lead_phase.png'),'Resolution',150);

    % Q2 — 1.-ordens Bode: -3 dB ved wBW = 1/tau
    f = figure('Color','w','Position',[100 100 560 420]);
    bode(G2); grid on;
    title(sprintf('Q2: G=1/(\\tau s+1), \\tau=%g  ->  \\omega_{BW}=\\omega_c=1/\\tau=%.2f', tau, 1/tau));
    exportgraphics(f, fullfile(figdir,'Q2_firstorder_bode.png'),'Resolution',150);

    fprintf('\n[figurer gemt i %s]\n', figdir);
end
