%% 62743 DSP -- E25 Exam -- Working Script  (reexam: genløsning af dumpet eksamen)
% Exam PDF:     Obsidian\Archive\3rd Semester\DSP\62743 E25 Exam v3.pdf
% Solution PDF: Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\Solutions\62743 E25 Exam student solutions.pdf
%               (officiel facitliste -- absolut sandhedskilde)
% Egen note:    Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\E25 Exam.md
%               (egen efterrationaliseret løsning -- kan indeholde fejl,
%                stol på solution PDF / notebooklm i stedet)
%
% Eksamensdato:   12. december 2025  (Mads, s246132)
% Vægtning:       P1 40% (Z-domæne, matematik) | P2 30% (IIR) | P3 30% (FIR)
% Date attempted:
% Time target:    4 timers hard cap
% Self-score:     / total marks
%
% Arbejdsgang: skriv svar som "%%"-Svar-blokke MENS du regner. Til sidst:
% i mappen 3.semester\DSP  ->  pretty E25_new.m   (giver pæn PDF).
% Flows: [[LTI z-transform flow]] / [[Filter analysis and FFT flow]] / [[FIR window design flow]].

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 -- Z-domæne analyse   [MATEMATIK -- 40%]
% Kausalt diskret LTI-system T med overføringsfunktion H(z).
%   Nulpunkter: z = -2,  (1+i)/2,  (1-i)/2
%   Poler:      p = 0,    1/3,      2/3
%   Bibetingelse: H(1) = 1

%% 1-1  Pol-/nulpunktsdiagram
% - Skitsér/plot pol-/nulpunktsdiagram i det komplekse z-plan.
% - Marker enhedscirklen.

z=[-2 ((1+i)/2) ((1-i)/2)];
p= [0 1/3 2/3];

figure;
zplane(z.', p.');                 % kolonnevektorer -> ægte nul-/polplacering
title('Pol-/nulpunktsdiagram for H(z)')

% Polynomieform (genbruges i 1-2..1-7). poly() -> koeff. i faldende z-potens.
b0 = real(poly(z));               % tæller, monisk (uden forstærkning endnu)
a0 = real(poly(p));               % nævner


%%
% *Svar 1-1:* 3 nulpunkter: z=-2 (UDEN for enhedscirklen) samt det
% komplekst konjugerede par (1±i)/2 (|z|=0.707, inden for cirklen).
% 3 poler: z=0, 1/3, 2/3 -- alle inden for enhedscirklen. At nulpunktet
% z=-2 ligger uden for cirklen betyder, at systemet IKKE er minimumfase
% (det udnyttes i 1-7).

%% 1-2  Overføringsfunktion H(z) og ROC
% - Opskriv H(z) på faktoriseret form ud fra poler/nulpunkter.
% - Brug H(1) = 1 til at bestemme forstærkningskonstanten.
% - Udvid til polynomieform (b, a). Angiv ROC for det kausale system.




% H(z) = G * N(z)/D(z). Bestem G så H(1) = 1  (ved z=1 er z^-1=1):
G = polyval(a0,1) / polyval(b0,1)        % forstærkning -> 4/27 ≈ 0.1481
b = G*b0;                                % endelige tællerkoefficienter
a = a0;                                  % nævnerkoefficienter

Hz1 = tf(b, a, 1, 'Variable','z^-1')     % H(z) på polynomieform (z^-1)
ROC_12 = max(abs(roots(a)))              % kausal -> ROC: |z| > 2/3

%%
% *Svar 1-2:* H(z) = G·(1+2z⁻¹)(1−½(1+i)z⁻¹)(1−½(1−i)z⁻¹) /
% [(1−⅓z⁻¹)(1−⅔z⁻¹)], hvor G = 4/27 er bestemt af betingelsen H(1)=1.
% Polynomieform er vist som Hz1 ovenfor (b = G·[1 1 -1.5 1],
% a = [1 -1 2/9 0]). Systemet er kausalt, så ROC ligger uden for den
% yderste pol: |z| > 2/3.

%% 1-3  Stabilitetsanalyse
% - Er systemet stabilt? Argumentér ud fra polernes placering ift.
%   enhedscirklen (kausalt + stabilt <=> alle poler |p| < 1).



poler = roots(a)
stabil = all(abs(poler) < 1)             % logisk 1 = stabilt

%%
% *Svar 1-3:* Polerne er z=0, 1/3 og 2/3; alle har |p| < 1 og ligger
% dermed inden for enhedscirklen. Systemet er kausalt, og ROC (|z|>2/3)
% indeholder enhedscirklen -> systemet er STABILT (stabil = 1).

%% 1-4  Z-transformation af signal
% Signal:  x1[n] = (sqrt(2)/2)^n * sin(pi/4 * n) * u[n]
% Given formel:
%   Z{ a^n sin(w0 n) u[n] } = a z^-1 sin(w0)
%                             ---------------------------------
%                             1 - 2 a z^-1 cos(w0) + a^2 z^-2 ,  |z| > |a|
% - Identificér a og w0, opskriv X1(z), angiv ROC.



a_x  = sqrt(2)/2;                        % a i den givne formel
w0   = pi/4;                             % w0 i den givne formel
numX = [0, a_x*sin(w0)];                 % tæller:  a·sin(w0)·z⁻¹
denX = [1, -2*a_x*cos(w0), a_x^2];       % nævner:  1 − 2a·cos(w0)z⁻¹ + a²z⁻²
X1z  = tf(numX, denX, 1, 'Variable','z^-1')
ROC_x = a_x                              % ROC: |z| > a ≈ 0.707

%%
% *Svar 1-4:* x1[n] har a = √2/2 og w0 = π/4. Indsat i den udleverede
% formel fås X1(z) = 0.5·z⁻¹ / (1 − z⁻¹ + 0.5·z⁻²), med ROC: |z| > √2/2
% ≈ 0.707.

%% 1-5  Udgangens Z-transformation Y1(z)
% - Y1(z) = H(z) * X1(z).  Opskriv produktet (og reducér hvis muligt).



numY = conv(b, numX);                    % produkt af tællere
denY = conv(a, denX);                    % produkt af nævnere
Y1z  = minreal(tf(numY, denY, 1, 'Variable','z^-1'))   % forkort fælles faktorer

%%
% *Svar 1-5:* Y1(z) = H(z)·X1(z). X1's nævner (1−z⁻¹+½z⁻²) er præcis
% H's konjugerede nulpunktspar, så disse udgår (minreal forkorter dem).
% Resultat: Y1(z) = (2/27)·z⁻¹(1+2z⁻¹) / [(1−⅓z⁻¹)(1−⅔z⁻¹)].

%% 1-6  Udgangssignal y1[n]
% - Find y1[n] ved invers Z-transformation (delbrøksopspaltning).



% Y1(z) = z⁻¹ · W(z),  W(z) = (2/27)(1+2z⁻¹)/[(1−⅓z⁻¹)(1−⅔z⁻¹)]
numW = (2/27)*[1 2];
denW = conv([1 -1/3], [1 -2/3]);         % = [1 -1 2/9]
[r, pz, kdir] = residuez(numW, denW)     % delbrøk: residues r, poler pz

n  = 0:15;
y1 = filter((2/27)*[0 1 2], denW, [1 zeros(1,numel(n)-1)]);   % numerisk kontrol
figure; stem(n, y1); grid on
xlabel('n'); ylabel('y_1[n]'); title('y_1[n]')

%%
% *Svar 1-6:* residuez på W giver poler 1/3 og 2/3 med residues
% -14/27 og 16/27, dvs. w[n] = (-14/27)(1/3)^n + (16/27)(2/3)^n.
% Faktoren z⁻¹ er en forsinkelse, så y1[n] = w[n-1]:
%   y1[n] = (2/27)·( -7·(1/3)^(n-1) + 8·(2/3)^(n-1) )·u[n-1].
% (Stem-plottet bekræfter forløbet numerisk.)

%% 1-7  Minimumfase- og all-pass-dekomposition
% - Dekomponér H(z) = H_min(z) * H_ap(z).
% - Flyt nulpunkt(er) uden for enhedscirklen via all-pass-sektion.
% - Verificér: |H_ap(e^jw)| = 1 (0 dB) for alle w.



% Nulpunktet z=-2 ligger uden for enhedscirklen -> spejl ind: z0 -> 1/conj(z0)
z0   = -2;
zref = 1/conj(z0);                       % = -0.5  (inde i cirklen)

bap = [1, -z0];                          % (1 − z0·z⁻¹)   = (1 + 2z⁻¹)
aap = [1, -zref];                        % (1 − zref·z⁻¹) = (1 + 0.5z⁻¹)
Gap = sum(aap)/sum(bap);                 % sikrer Hap(1)=1  -> 0.5
bap = Gap*bap;
Hap = tf(bap, aap, 1, 'Variable','z^-1')

[Hapw, fw] = freqz(bap, aap, 1024);      % all-pass-kontrol
figure; plot(fw/pi, 20*log10(abs(Hapw))); grid on
xlabel('\omega/\pi'); ylabel('|H_{ap}| [dB]')
title('All-pass: |H_{ap}| skal være 0 dB overalt')

Hmin = minreal(tf(b,a,1,'Variable','z^-1') / Hap)   % H_min = H / H_ap

%%
% *Svar 1-7:* H er ikke minimumfase pga. nulpunktet z=-2 (uden for
% enhedscirklen). Dekomponering H(z)=Hmin(z)·Hap(z) med all-pass
% Hap(z) = (z⁻¹+½)/(1+½z⁻¹), som flytter nulpunktet fra z=-2 til
% z=-½ inde i cirklen (Gap=½ fra Hap(1)=1). Plottet bekræfter
% |Hap|=0 dB for alle ω. Hmin (= H/Hap) har alle nulpunkter inden
% for enhedscirklen.

%% Problem 2 -- IIR-filter analyse (Direct Form II)   [FILTER -- 30%]
% Digitalt LAVPASfilter givet i Direct Form II (koefficienter aflæst fra
% blokdiagram i eksamen). Filteret har -3 dB ved 400 Hz (passer iflg. facit).
%
% ⚠️ FÆLDE (årsag til dump): feedback-tapsne -0.4860 og -0.0177 sidder
% EFTER hhv. 2. og 4. z^-1-blok i DF-II-diagrammet -> de hører til z^-2
% og z^-4, IKKE z^-1 og z^-2. Nævneren er derfor:
%   A(z) = 1 + 0.486 z^-2 + 0.0177 z^-4   (nuller indsat ved z^-1 og z^-3)
% Læs delay-positionerne i diagrammet nøje før du opskriver a.

B2  = [0.0940, 0.3759, 0.5639, 0.3759, 0.0940];   % tæller: z^0..z^-4
A2  = [1, 0, 0.4860, 0, 0.0177];                   % nævner: z^-2 og z^-4
Fs2 = 1600;            % samplingsfrekvens [Hz]
Ts2 = 1/Fs2;

%% 2-1  Overføringsfunktion og frekvensrespons  (6 delopgaver)
% - Opskriv overførselsfunktionen H(z) = B2(z)/A2(z).
% - Plot |H| i dB som funktion af F = f*Fs [Hz], 0 .. Fs/2 (freqz).
% - Dæmpning ved 400 Hz? Passer det med filterbeskrivelsen? (facit: ~3 dB, ja)
% - Dæmpning ved 600 Hz? (aflæs på plottet -- facit: ~30.6 dB)
% - Plot fasen af frekvensresponset.
% - Er fasen i pasbåndet lineær? Forventet ud fra filtertypen? (IIR -> nej)

Hz = tf(B2, A2, Ts2, 'Variable','z^-1'); %laver overførselsfunktion vha.tf
Hz %printer overførselsfunktion


[H, f] = freqz(B2, A2, 4096, Fs2);

figure
subplot(2,1,1)
hH = plot(f, 20*log10(abs(H)), 'DisplayName','|H(f)|');
hold on
x1 = xline(400,  '--g', 'DisplayName','400 Hz');
y1 = yline(-3,   '--r', 'DisplayName','-3 dB');
x2 = xline(600,  '--b', 'DisplayName','600 Hz');
y2 = yline(-30.61,'--y','DisplayName','-30.61 dB');
title('Magnitude Response')
xlabel('Hz'); ylabel('dB'); grid on
legend([hH x1 y1 x2 y2], 'Location','best')
grid on;

subplot(2,1,2)
plot(f, unwrap(angle(H)))
title('Phase Response')
xlabel('Hz'); ylabel('rad');
grid on;
hold off;


%dæmpning ved 400 og 600Hz
dB = 20*log10(abs(freqz(B2, A2, [400 600], Fs2)))   % -> -3.01 dB, -30.61 dB

%%
% *Svar 2-1:* Dæmpningen ved 400Hz er -3dB som stemmer overens med
% filterets spec. Dæmpningen ved 600Hz aflæses på plottet til at være
% -30.61 dB. Fasen er ikke linieært, dette stemmer overens med at filteret er
% et IIR filter

%% 2-2  Pol-/nulpunktsdiagram og impulsrespons
% - Plot poler/nulpunkter (roots(B2)/roots(A2) eller zplane). Stabil?
% - Plot impulsresponsen. Endelig eller uendelig?

nulpunkter = roots(B2)
poler      = roots(A2)

figure
zplane(B2, A2)

n   = -10:30;
imp = [zeros(1,10) 1 zeros(1,30)];   % unit impulse at n=0 (index 11)
IR  = filter(B2, A2, imp);
figure
stem(n, IR)
xlabel('Sample number, n'); ylabel('amplitude'); grid on


%%
% *Svar 2-2:* Filteret er stabilt da polerne er indenfor enhedscirklen, og
% vi kan også se at impulsresponset går mod 0.

%% 2-3  Sampling af analogt signal
% XA(t) = A1*cos(2*pi*F1*t) + A2c*cos(2*pi*F2*t) + A3*cos(2*pi*F3*t)
F1 = 100;   A1  = 1;
F2 = 300;   A2c = 2;
F3 = 600;   A3  = 3;
Nfft2 = 2^14;          % antal samples

% - Aliasering ved Fs = 1600 Hz?  (Nyquist vs. højeste signalfrekvens)
% - Generér og plot det samplede signal.

t2 = time_vec(Fs2, Nfft2);        % fuld diskret tidsvektor, N=2^14 samples (Ts2 findes allerede)
XA_sampled = A1*cos(2*pi*F1*t2) + A2c*cos(2*pi*F2*t2) + A3*cos(2*pi*F3*t2);

figure
stem(t2, XA_sampled, '.');
xlim([0 0.05]);                  % vis kun 0..0.05 s -- signalet findes for hele N
xlabel('Time [s]'); ylabel('Amplitude [a.u.]'); grid on
%%
% *Svar 2-3:* Maksimale signalfrekvens uden aliasing er Fs/2 = 800 Hz
% (Nyquist). Alle komponenter F1=100, F2=300 og F3=600 Hz ligger under
% 800 Hz, så der er ingen aliasing.

%% 2-4  Frekvensspektrum
% - Beregn FFT af det samplede signal (en-sidet, normér med N).
% - Plot |spektrum| vs. F = f*Fs [Hz].
% - Aflæs linjefrekvenser og amplituder. Stemmer med F1/F2/F3?

XA = fftshift(fft(XA_sampled) / Nfft2);
f  = frequency_vec(Fs2, Nfft2);

figure;
plot(f, abs(XA), 'LineWidth', 1.5);
xlabel('f·F_s  [Hz]'); ylabel('|X_A[k]|');
title('Spectrum of x_A[n], F_s = 1600 Hz'); grid on;


%%
% *Svar 2-4:* vi ser ingen alliasering af de 3 frekvenser F1 F2 & F3, og
% deres amplituder stemmer også overerns med dem der er givet i
% specifikationen, fx A3=3 ( vi ser F3 har en amplitude på 1.5 på hver side
% af spektret hvilket giver 3)

%% 2-5  Filtrering
% - Filtrér det samplede signal: y = filter(B2, A2, x).
% - FFT af det filtrerede signal; plot spektrum før/efter.
% - Dæmpning ved 100, 300, 600 Hz. Sammenlign med |H| fra 2-1.

xa_filt = filter(B2, A2, XA_sampled);
XA_filt = fftshift(fft(xa_filt) / Nfft2);          % samme skalering som 2-4

figure
h = plot(f, abs(XA_filt), 'LineWidth',1.5);        % fang handle til datatip
xlabel('Frequency [Hz]'); ylabel('|X|'); grid on
title('Spektrum af det filtrerede signal')
for F = [100 300 600]
    [~, idx] = min(abs(f - F));                    % nærmeste bin (f, ikke f_v)
    datatip(h, 'DataIndex', idx);
end

A600=0.0442224; % aflæst på graf

A600_in  = 1.5;                                    % oprindelig amplitude 600 Hz = A3/2
A_600_dB = 20*log10(A600 / A600_in)                % -> ca. -30.6 dB


%%
% *Svar 2-5:* Efter filtrering aflæses amplituderne til ca. 0.50 ved 100 Hz,
% 0.98  ved 300 Hz og 0.044 ved 600 Hz. Dæmpningen ved 600 Hz er
% 20*log10(0.044/1.5) ≈ -30.6 dB. Dette stemmer overens med dæmpningen
% fundet fra |H| i 2-1 (≈ -30.61 dB ved 600 Hz).

%% Problem 3 -- FIR højpasfilter via vindue (Fourier-metode)  [FILTER -- 30%]
% FIR HØJPAS designet med vinduesmetoden (Fourier-transform-design).

Fpass3 = 1750;         % pasbånds-kant [Hz]
Fstop3 = 1250;         % stopbånds-kant [Hz]
AsdB3  = 20;           % stopbåndsdæmpning [dB]
Fs3    = 5000;         % samplingsfrekvens [Hz]

%% 3-1  Vinduesvalg og ordenberegning
% - Vis at cut-off er midtpunktet:  Fc = (Fpass+Fstop)/2 = 1500 Hz.
% - Normaliseret digital cut-off:   f_c = Fc/Fs  ->  wc = 2*pi*f_c.
% - Overgangsbånd dF = |Fpass-Fstop| og normaliseret dF/Fs.
% - Vælg vindue der lige opfylder As = 20 dB (se appendix-tabel).
% - Beregn antal taps N  (helper: MK_values).

Fc=(Fpass3+Fstop3)/2

f_c = Fc/Fs3;
wc= 2*pi*f_c

F_sharpnes = abs(Fstop3-Fpass3)/Fs3

n_taps = ceil(0.9/F_sharpnes)



%%
% *Svar 3-1:* Fc er udregnet ovenfor, wc bestemt til 1.8850. Fsharpnes
% bestemt til 0.1. For at opfylde stopbåndsdæmpningen på 20 dB vælges et
% Rectangulært vindue. Ntaps udregnet til 9

%% 3-2  Impulsrespons
% Ideel HØJPAS:  h_d[n] = delta[n] - (wc/pi) * sinc(wc*n/pi)
% - Beregn h_d[n], påtryk det valgte vindue, gør filteret kausalt
%   (forskyd med M). Plot h[n].   (helpers: FIR_fourier, FIR_window)

M_values = n_taps - 1        
K_values = M_values / 2

      
n3=-K_values:K_values;

h=FIR_fourier("HP",n3,wc);

figure;
stem(0:M_values, h);
title('Impulsrespons');
grid on;


%%
% *Svar 3-2:* M = 8, K = 4. Ideelt højpas via Fourier-metoden,
% h[n] = -(wc/pi)*sinc(wc*n/pi) med midtersample (pi-wc)/pi. Rektangulært
% vindue -> kun trunkering (ingen vindues-multiplikation). Filteret gøres
% kausalt ved at forskyde K=4 samples, så n går 0..M (symmetrisk -> lineær fase).

%% 3-3  Frekvensrespons og verifikation
Hz3 = tf(h, 1, 1/Fs3, 'Variable','z^-1')      % overførselsfunktion (h = impulsrespons fra 3-2)

[H3, f3] = freqz(h, 1, 1024, Fs3);            % NB: ny variabel H3, overskriv ikke h

figure
hLine = plot(f3, 20*log10(abs(H3)), 'LineWidth',1.5);   % fang handle
title('Magnitude Response'); xlabel('F = f·F_s [Hz]'); ylabel('|H| [dB]')
xline(Fc,'--g','F_c'); xline(Fpass3,'--g','F_{pass}'); xline(Fstop3,'--g','F_{stop}');
yline(-AsdB3,'--k','-20 dB'); grid on

for F = [1250 1750]
    [~, idx] = min(abs(f3 - F));
    datatip(hLine, 'DataIndex', idx);
end

%%
% *Svar 3-3:* Ved F_stop = 1250 Hz aflæses dæmpningen på datatip til
% ca. -20 dB (>= 20 dB krav netop opfyldt), og pasbåndet F >= 1750 Hz
% ligger nær 0 dB. Filteret opfylder dermed stopbåndskravet.

%% 3-4  Faserespons og linearitet
% - Plot fasen. Er den lineær i pasbåndet?
% - Argumentér ud fra impulsresponsens symmetri (Type I/II FIR).

figure;
phaseX = rad2deg(unwrap(angle(H3)));
plot(f3, phaseX);
xlabel('Frequency [Hz]');
ylabel('Phase [degrees]');
title('Phase Response');
grid on;
xline(Fc, '--g', 'F_c'); 
xline(Fpass3, '--g', 'F_{pass}'); 
xline(Fstop3, '--g', 'F_{stop}');

%%
% *Svar 3-4:* Filteret har lineær fase i pasbåndet (ses på phase-response-
% plottet). Det er forventet: impulsresponset h[n] er symmetrisk om n=K=4,
% og med M=8 (lige) er det et Type-I lineær-fase FIR-filter. Faseforløbet
% er en ret linje med konstant grupperløb = K = 4 samples. π-springene i
% plottet er fortegnsskift hvor |H| -> 0, ikke ulinearitet.

%% 3-5  Redesign med As = 40 dB
% - Vælg nyt vindue der opfylder 40 dB (se appendix). Ny orden N.
% - Genberegn h[n] med det nye vindue.

Asdb_new = 40;

n_taps_han = ceil(3.1/F_sharpnes)

M = n_taps_han - 1        
K = M / 2

n=-K:K;

w = FIR_window("hanning", M);          % M = 30, length M+1 = 31
h_new = FIR_fourier("HP", n, wc) .* w; % ideel respons * Hann-vindue

figure;
stem(0:M, h_new);
title('New Impulse Response with 40 dB Stopband Attenuation');
grid on;


%%
% *Svar 3-5:* Et Hanning-vindue vælges, da det giver ca. 44 dB
% stopbåndsdæmpning og dermed opfylder 40 dB-kravet. Nyt antal taps
% N = 3.1/ΔF = 31 (M = 30, K = 15). Den ideelle FIR_fourier-respons
% multipliceres med Hann-vinduet (FIR_window); en rektangulær ville
% her IKKE nå 40 dB uanset antal taps.

%% 3-6  Verifikation af redesignet filter
% - Plot |H| i dB; verificér >= 40 dB dæmpning ved Fstop.
% - Sammenlign overgangsbåndsbredde med 20 dB-designet (trade-off).


Hz = tf(h_new, 1, 1/Fs3, 'Variable','z^-1')      % overførselsfunktion

[H, f] = freqz(h_new, 1, 1024, Fs3);            

figure
hLine = plot(f, 20*log10(abs(H)), 'LineWidth',1.5);   % fang handle (f fra freqz ovenfor)
title('Magnitude Response'); xlabel('F = f·F_s [Hz]'); ylabel('|H| [dB]')
xline(Fc,'--g','F_c'); xline(Fpass3,'--g','F_{pass}'); xline(Fstop3,'--g','F_{stop}');
yline(-Asdb_new,'--k','-40 dB'); grid on

for F = [1250 1750]
    [~, idx] = min(abs(f - F));
    datatip(hLine, 'DataIndex', idx);
end


%%
% *Svar 3-6:* Ved båndkanten Fstop = 1250 Hz aflæses ca. -39 dB, men
% stopbåndets sidelober ligger ca. -44 dB, så filteret opfylder 40 dB-
% kravet i stopbåndet. Trade-off vs. 20 dB-designet (rektangulær, N=9):
% den kraftigere dæmpning koster et meget bredere overgangsbånd / langt
% flere taps (N: 9 -> 31).

%% --- Scratch / sandbox ---



%% Appendix -- FIR vinduer (referencetabel)
%{
Vindue        | Stopbåndsdæmp. As | Ntaps-formel (dF = |Fstop-Fpass|/Fs)
--------------|-------------------|-------------------------------------
Rektangulær   |  21 dB            | Ntaps = 0.9 / dF
Hann          |  44 dB            | Ntaps = 3.1 / dF
Hamming       |  53 dB            | Ntaps = 3.3 / dF
Blackman      |  74 dB            | Ntaps = 5.5 / dF

Tommelfinger: vælg det MINDSTE vindue hvis As stadig opfyldes
(smallere overgangsbånd for given orden). Rund Ntaps OP til ulige
heltal (Type-I lineær fase). M = Ntaps-1, K = M/2.
Cut-off = midtpunkt af overgangsbåndet: f_c = Fc/Fs, wc = 2*pi*f_c.
(verificeret mod E25-facit + notebooklm)
%}
