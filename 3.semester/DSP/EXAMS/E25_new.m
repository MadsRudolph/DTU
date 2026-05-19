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



%%
% *Svar 1-1:* TODO

%% 1-2  Overføringsfunktion H(z) og ROC
% - Opskriv H(z) på faktoriseret form ud fra poler/nulpunkter.
% - Brug H(1) = 1 til at bestemme forstærkningskonstanten.
% - Udvid til polynomieform (b, a). Angiv ROC for det kausale system.



%%
% *Svar 1-2:* TODO

%% 1-3  Stabilitetsanalyse
% - Er systemet stabilt? Argumentér ud fra polernes placering ift.
%   enhedscirklen (kausalt + stabilt <=> alle poler |p| < 1).



%%
% *Svar 1-3:* TODO

%% 1-4  Z-transformation af signal
% Signal:  x1[n] = (sqrt(2)/2)^n * sin(pi/4 * n) * u[n]
% Given formel:
%   Z{ a^n sin(w0 n) u[n] } = a z^-1 sin(w0)
%                             ---------------------------------
%                             1 - 2 a z^-1 cos(w0) + a^2 z^-2 ,  |z| > |a|
% - Identificér a og w0, opskriv X1(z), angiv ROC.



%%
% *Svar 1-4:* TODO

%% 1-5  Udgangens Z-transformation Y1(z)
% - Y1(z) = H(z) * X1(z).  Opskriv produktet (og reducér hvis muligt).



%%
% *Svar 1-5:* TODO

%% 1-6  Udgangssignal y1[n]
% - Find y1[n] ved invers Z-transformation (delbrøksopspaltning).



%%
% *Svar 1-6:* TODO

%% 1-7  Minimumfase- og all-pass-dekomposition
% - Dekomponér H(z) = H_min(z) * H_ap(z).
% - Flyt nulpunkt(er) uden for enhedscirklen via all-pass-sektion.
% - Verificér: |H_ap(e^jw)| = 1 (0 dB) for alle w.



%%
% *Svar 1-7:* TODO

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

t2 = 0:Ts2:(Nfft2-1)*Ts2;        % fuld diskret tidsvektor, N=2^14 samples (Ts2 findes allerede)
XA_sampled = A1*cos(2*pi*F1*t2) + A2c*cos(2*pi*F2*t2) + A3*cos(2*pi*F3*t2);

figure
stem(t2, XA_sampled, '.');
xlim([0 0.05]);                  % vis kun 0..0.05 s -- signalet findes for hele N
xlabel('Time [s]'); ylabel('Amplitude [a.u.]'); grid on
%%
% *Svar 2-3:* Maksimale signalfrekvens er 800Hz da Fs=1600Hz

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



%%
% *Svar 3-4:* TODO

%% 3-5  Redesign med As = 40 dB
% - Vælg nyt vindue der opfylder 40 dB (se appendix). Ny orden N.
% - Genberegn h[n] med det nye vindue.



%%
% *Svar 3-5:* TODO

%% 3-6  Verifikation af redesignet filter
% - Plot |H| i dB; verificér >= 40 dB dæmpning ved Fstop.
% - Sammenlign overgangsbåndsbredde med 20 dB-designet (trade-off).



%%
% *Svar 3-6:* TODO

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
