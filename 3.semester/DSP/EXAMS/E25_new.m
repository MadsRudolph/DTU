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



%%
% *Svar 2-1:* TODO

%% 2-2  Pol-/nulpunktsdiagram og impulsrespons
% - Plot poler/nulpunkter (roots(B2)/roots(A2) eller zplane). Stabil?
% - Plot impulsresponsen (impz). Endelig eller uendelig?



%%
% *Svar 2-2:* TODO

%% 2-3  Sampling af analogt signal
% XA(t) = A1*cos(2*pi*F1*t) + A2c*cos(2*pi*F2*t) + A3*cos(2*pi*F3*t)
F1 = 100;   A1  = 1;
F2 = 300;   A2c = 2;
F3 = 600;   A3  = 3;
Nfft2 = 2^14;          % antal samples
% - Aliasering ved Fs = 1600 Hz?  (Nyquist vs. højeste signalfrekvens)
% - Generér og plot det samplede signal.



%%
% *Svar 2-3:* TODO

%% 2-4  Frekvensspektrum
% - Beregn FFT af det samplede signal (en-sidet, normér med N).
% - Plot |spektrum| vs. F = f*Fs [Hz].
% - Aflæs linjefrekvenser og amplituder. Stemmer med F1/F2/F3?



%%
% *Svar 2-4:* TODO

%% 2-5  Filtrering
% - Filtrér det samplede signal: y = filter(B2, A2, x).
% - FFT af det filtrerede signal; plot spektrum før/efter.
% - Dæmpning ved 100, 300, 600 Hz. Sammenlign med |H| fra 2-1.



%%
% *Svar 2-5:* TODO

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



%%
% *Svar 3-1:* TODO

%% 3-2  Impulsrespons
% Ideel HØJPAS:  h_d[n] = delta[n] - (wc/pi) * sinc(wc*n/pi)
% - Beregn h_d[n], påtryk det valgte vindue, gør filteret kausalt
%   (forskyd med M). Plot h[n].   (helpers: FIR_fourier, FIR_window)



%%
% *Svar 3-2:* TODO

%% 3-3  Frekvensrespons og verifikation
% - Plot |H| i dB vs. F = f*Fs [Hz]. Marker Fpass og Fstop.
% - Opfylder filteret stopbåndskravet (>= 20 dB ved Fstop = 1250 Hz)?



%%
% *Svar 3-3:* TODO

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
