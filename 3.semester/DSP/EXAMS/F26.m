%% ░░░░░ 62743 DSP -- F26 REEKSAMEN -- EKSAMENSDAG: GØR DETTE FØRST ░░░░░
% =====================================================================
%  CHECKLISTE NÅR DU ÅBNER COMPUTEREN (5 min, før du læser opgaven):
%
%  [ ] 1. git pull            (i C:\Users\Mads2\DTU  -- henter alt dette)
%  [ ] 2. Åbn Obsidian-hub:   "62743 Digital Signal Processing (Reexam)"
%         -> den har navigations-chart: "min opgave ligner X -> gå hertil"
%  [ ] 3. Åbn ALLE gamle løsninger i MATLAB-editoren som opslag:
%         E25_new.m (FACIT-agtig, fuld P1+P2+P3) , F24.m , F25_new.m ,
%         F23.m , F20.m , E19/E20/E22/F21.m   (mappe: 3.semester\DSP\EXAMS)
%  [ ] 4. Kør disse 4 linjer (toolbox-tjek) -- skal IKKE fejle:
%           ver                 % "Signal Processing Toolbox" SKAL stå
%           which residuez tf2zpk zplane impz freqz   % alle skal findes
%           % (Symbolic Math Toolbox? -> så virker syms/iztrans/ztrans også)
%  [ ] 5. Læs opgaven. Find opgavetype i hub-chartet -> åbn det flow/cookbook.
%  [ ] 6. REKKEFØLGE: Opgave 3 (60m) -> Opgave 2 (70m) -> Opgave 1 (80m)
%         -> 30 min: gennemse + 'pretty F26.m' -> aflever PDF + .m
% =====================================================================
%
% Date attempted:
% Time target:    4 timer hard cap  (Q3 ~60 min, Q2 ~70 min, Q1 ~80 min, 30 min review+publish)
% Self-score:     / 100
%
% FORMAT (E25-spejlet): 3 opgaver, vægtning ~ 40 / 30 / 30.
%   Opgave 1 (~40%): LTI / Z-transformation  [SVAGT - men størst]
%   Opgave 2 (~30%): filterrealisering + sampling + FFT + filtrering  [STÆRKT]
%   Opgave 3 (~30%): FIR design (Fourier + vindue)  [STÆRKT]
%
% Arbejdsgang: skriv svar som "%%"-Svar-blokke MENS du regner.
% Til sidst: i mappen 3.semester\DSP  ->  pretty F26.m   (giver pæn PDF).
%
% NAVIGATION (Obsidian-hub har det fulde chart):
%   Opgave 1  -> [[Q1 via MATLAB cookbook]]  (kan du ikke regne i hånden:
%                hver Q1-type -> præcise MATLAB-kommandoer + dansk Svar.
%                Har en PANIK-protokol nederst.)  + [[LTI z-transform flow]]
%   Opgave 2  -> [[Filter analysis and FFT flow]]
%   Opgave 3  -> [[FIR window design flow]]
%   Facit-eksempler: [[E25 exam walkthrough]] (mest lig F26) m.fl.
%
% ⚠️ Q1-FÆLDE: hvis et delspørgsmål siger "UDEN brug af MATLAB/Maple"
%    -> så scorer en ren residuez-dump 0. Skriv den analytiske OPSTILLING
%    i hånden (tabelpar, partialbrøk-ansats, cover-up) selv hvis du ikke
%    kan regne den færdig. Ellers brug cookbooken frit.

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');
% Helpers: n_value, frequency_vec, time_vec, FIR_fourier, FIR_window, MK_values
% (signaturer: se [[DSP MATLAB helpers cheat sheet]])


%% Problem 1 -- LTI / Z-transformation   [~40 %]
% Genkend: differensligning  ELLER  "poler/nulpunkter er ..." + H(1)=1
%          ELLER  input/output-tabel.  Spørger H(z), ROC, stabil?, h[n], y[n], min-fase.
%
% --- Indtast opgavens data her (vælg den variant opgaven giver) ---
% Variant A (differensligning):
%   flyt alle y-led til venstre. y[n]=0.5y[n-1]+x[n] -> a=[1 -0.5], b=[1].
%   b = [...]; a = [1, ...];
% Variant B (poler/nulpunkter + H(1)=1):
%   b0=real(poly(zer)); a0=real(poly(pol));
%   G = Hval*polyval(a0,1)/polyval(b0,1);   % her Hval=1 (H(1)=1)
%   b = G*b0;  a = a0;
% Variant C (I/O-tabel, system er LTI -> INGEN z-transform):
%   find c1,c2 så c1*x1+c2*x2 = delta[n];  så er h = c1*y1 + c2*y2.
%   (fx x1-x2 = 2*delta -> h = 0.5*(y1 - y2);  stem(h))

b = [];                 % tæller (z^-1 form)   <-- UDFYLD
a = [1];                % nævner (z^-1 form)   <-- UDFYLD

%% 1-1  Pol-/nulpunktsdiagram
% - Skitsér / plot pol-nulpunktsdiagrammet.

% figure; zplane(b, a); title('Pol-/nulpunktsplot')
% [zer, pol, k] = tf2zpk(b, a)        % nulpunkter, poler, gain (inkl. z=0)

%%
% *Svar 1-1:* TODO

%% 1-2  Systemfunktion H(z) og ROC
% - Opskriv H(z).  - Angiv konvergensområdet ROC(H(z)).
% Hvis poler/nulpunkter er givet:  H(z) = G * prod(1 - z_k z^-1) / prod(1 - p_k z^-1),
% og G bestemmes fra H(1) = <opgivet>  (indsæt z=1, løs for G).

% Hz = tf(b, a, -1, 'Variable','z^-1')

%%
% *Svar 1-2:* TODO  (H(z) = ... ; ROC: |z| > største |pol|, kausalt system)

%% 1-3  Stabilitet
% - Stabil eller ustabil? Begrund.
% Kausalt: stabilt hvis ALLE |pol| < 1 (inden for enhedscirklen).

% poler = roots(a)
% maxpol = max(abs(poler))

%%
% *Svar 1-3:* TODO

%% 1-4  Z-transformation af givet signal
% Brug evt. den udleverede formel for Z{a^n sin(w0 n) u[n]} e.l.
% x1[n] = ...  ->  X1(z) = ...

%%
% *Svar 1-4:* TODO  (X1(z) = ...)

%% 1-5  Y(z) = H(z) * X(z)
% - Bestem Y1(z) på en form der ikke kan forkortes.
% Pas på: pol fra X(z) der rammer nulpunkt i H(z) -> forkortes; rammer pol -> dobbeltpol.

%%
% *Svar 1-5:* TODO

%% 1-6  Outputsignal y[n]  (invers Z via partialbrøk)
% [r, p, k] = residuez(bY, aY)   % r=residuer, p=poler (fortegn bagt ind)
% h[n] = sum_i r(i) * p(i)^n * u[n]   (omskriv hver faktor til 1 - a z^-1 før a aflæses!)
% Verificér ved at lægge partialbrøkerne sammen igen.

%%
% *Svar 1-6:* TODO  (y[n] = ...)

%% 1-7  Minimum-fase / all-pass dekomposition
% H(z) = Hmp(z) * Hap(z).  For et nulpunkt z0 UDENFOR enhedscirklen (|z0|>1):
%  1) Hmp: erstat (1 - z0 z^-1) med (1 - (1/conj(z0)) z^-1)   (spejlet ind)
%  2) Hap = G * (1 - z0 z^-1) / (1 - (1/conj(z0)) z^-1)
%  3) Fastlæg G fra Hap(1)=1  -> Hmp bærer 1/G  (så Hmp*Hap = H)
%  4) Tjek: freqz(Hap) -> FLAD magnitude (kun fasen varierer)

% figure; freqz(bAp, aAp); title('All-pass H_{ap} - magnitude skal være flad')

%%
% *Svar 1-7:* TODO


%% Problem 2 -- Filterrealisering + sampling + FFT + filtrering   [~30 %]
% Genkend: blokdiagram (Direct Form I/II) ELLER givet H(z); derefter "samples med Fs",
%          "frekvensspektrum (FFT)", "filtrér signalet med filter".
%
% --- Filterkoefficienter fra blokdiagrammet ---
% feedforward gains (x-grenen)  -> b
% feedback gains (y-grenen)     -> a, med a(1)=1 og FORTEGN VENDT
%   (diagram +2.0 på y[n-1]  ->  a = [1, -2.0, ...])

Fs2 = [];               % samplingsfrekvens [Hz]   <-- UDFYLD
b2  = [];               % <-- UDFYLD
a2  = [1];              % <-- UDFYLD

%% 2-1  Overføringsfunktion, magnitude, dæmpning, fase
% - Opskriv H(z).  - Plot |H| i dB vs F i Hz (0 .. Fs/2).
% - Dæmpning ved de opgivne frekvenser?  - Plot fasen.  - Lineær i pasbånd?

% Hz2 = tf(b2, a2, 1/Fs2, 'Variable','z^-1')
% F_vec = frequency_vec(Fs2, Fs2/2);
% [H,F] = freqz(b2, a2, F_vec, Fs2);
% figure; plot(F, 20*log10(abs(H))); grid on; xlabel('F [Hz]'); ylabel('|H| [dB]')
% Hk = freqz(b2, a2, [f1 f2], Fs2);  dBk = 20*log10(abs(Hk))
% figure; plot(F, unwrap(angle(H))); grid on; title('Fase')

%%
% *Svar 2-1:* TODO  (FIR/IIR?; dæmpning ved ... ; fase lineær fordi ...)

%% 2-2  Poler/nulpunkter, stabilitet, impulsrespons
% - zplane.  - Stabil?  - Plot h[n] (fx n = -10 .. 30).

% figure; zplane(b2, a2); title('Pol-/nulpunktsplot')
% poler2 = roots(a2)
% h2 = filter(b2, a2, [1 zeros(1,40)]); figure; stem(0:40, h2); title('h[n]')

%%
% *Svar 2-2:* TODO

%% 2-3  Sampling af analogt signal
% xa(t) = A1 cos(2pi F1 t) + A2 cos(2pi F2 t) + ...
% - Maks. signalfrekvens uden aliasing = Fs/2 (Nyquist).
% - Definér tidsvektor fra t=0.  - Udregn x[n].  - Plot i 0 .. <T> s.

% A1=; F1=; A2=; F2=; A3=; F3=;
% Nsamp = ;                         % fx 2^14 hvis opgivet
% t2 = (0:Nsamp-1)/Fs2;             % eller time_vec(...)
% x2 = A1*cos(2*pi*F1*t2) + A2*cos(2*pi*F2*t2);   % + A3*cos(2*pi*F3*t2);
% figure; plot(t2, x2); xlim([0 0.05]); grid on; title('Samplet signal x[n]')

%%
% *Svar 2-3:* TODO  (Nyquist = Fs/2 = ... ; aliasing? ...)

%% 2-4  Frekvensspektrum (FFT) -- KORREKT skalering
% N  = length(x2);
% Xf = fft(x2);
% P  = abs(Xf)/N;                 % normalisér med N
% P1 = P(1:floor(N/2)+1);         % enkeltsidet
% P1(2:end-1) = 2*P1(2:end-1);    % dobbelt-tæl indre bins
% f1ax = (0:floor(N/2)) * Fs2/N;  % Hz-akse
% figure; stem(f1ax, P1); xlabel('F [Hz]'); ylabel('Amplitude'); grid on
% (En ren A*cos(2pi F0 t) giver en linje af højde ~A ved F0.)

%%
% *Svar 2-4:* TODO  (frekvenser/amplituder stemmer med xa fordi ...)

%% 2-5  Filtrér signalet og aflæs dæmpning
% y2 = filter(b2, a2, x2);   % brug filteret fra 2-1
% (gentag enkeltsidet FFT på y2)
% Dæmpning ved komponent = 20*log10(A_før / A_efter)
% Kryds-tjek: skal matche |H| aflæst i 2-1 ved samme frekvens.

%%
% *Svar 2-5:* TODO


%% Problem 3 -- FIR design (Fourier + vindue)   [~30 %]
% Genkend: "Filter design metode: Fourier transform", giver Fpass/Fstop/As/Fs.
%
% --- Spec fra opgaven ---
Fs3    = [];            % samplingsfrekvens [Hz]   <-- UDFYLD
Fpass  = [];            % pasbånd kant [Hz]        <-- UDFYLD
Fstop  = [];            % stopbånd kant [Hz]       <-- UDFYLD
AsdB3  = [];            % stopbånd dæmpning [dB]   <-- UDFYLD
% Filtertype: LP / HP / BP / BS  ->

%% 3-1  Fc, wc, sharpness, vindue, Ntaps
% Fc = (Fpass + Fstop)/2;                    % kant-frekvens (midtpunkt)
% fc = Fc/Fs3;   wc = 2*pi*fc;
% dF = abs(Fstop - Fpass)/Fs3;               % normaliseret transition width
%
% Vindue vælges fra As-kravet (mindste vindue der klarer As):
%   Rektangulær 21 dB : Ntaps = 0.9 / dF
%   Hanning     44 dB : Ntaps = 3.1 / dF
%   Hamming     53 dB : Ntaps = 3.3 / dF
%   Blackman    74 dB : Ntaps = 5.5 / dF
% Rund Ntaps OP til nærmeste ulige heltal.

%%
% *Svar 3-1:* TODO  (Fc = ... ; vindue = ... ; Ntaps = ...)

%% 3-2  K, M og trunkeret kausal impulsrespons
% M = Ntaps - 1;  K = M/2;            % eller [K,M] = MK_values(...)
% n3 = 0:M;
% Ideel respons (forskudt med K):
%   LP: hd = 2*fc*sinc(2*fc*(n3-K));
%   HP: hd = (n3==K) - 2*fc*sinc(2*fc*(n3-K));
% (MATLAB sinc(x)=sin(pi x)/(pi x) -> INGEN ekstra pi)
% h3 = hd .* <vindue>(Ntaps).';      % eller FIR_fourier(...) / FIR_window(...)
% figure; stem(n3, h3); title('Trunkeret kausal h[n]'); grid on

%%
% *Svar 3-2:* TODO

%% 3-3  Overføringsfunktion + magnitude
% FIR -> nævner = 1 (kun nulpunkter, altid stabilt).
% F_vec3 = frequency_vec(Fs3, Fs3/2);
% [H3,F3] = freqz(h3, 1, F_vec3, Fs3);
% figure; plot(F3, 20*log10(abs(H3))); grid on
% xline(Fc,'--g','Fc'); xline(Fpass,'--b'); xline(Fstop,'--b'); yline(-AsdB3,'--r','As')

%%
% *Svar 3-3:* TODO  (opfylder kravet? ja/nej fordi ...)

%% 3-4  Fase
% figure; plot(F3, unwrap(angle(H3))); grid on; title('Fase')
% Lineær fordi h[n] er symmetrisk om n = K (konstant gruppeforsinkelse).

%%
% *Svar 3-4:* TODO

%% 3-5  Spec ændres (typisk: nyt As) -> nyt filter
% Nyt krav, fx AsdB3_ny = 40 -> vælg nyt vindue fra tabellen -> nyt Ntaps
% (gentag 3-1..3-2 for det nye filter)

%%
% *Svar 3-5:* TODO

%% 3-6  Nyt magnituderespons, sammenlign
% (samme plot som 3-3 for det nye filter, markér Fc/Fpass/Fstop/As, kommentér)

%%
% *Svar 3-6:* TODO


%% --- Scratch / sandbox ---



%% Appendix -- Butterworth lavpas prototype (3 dB, eps = 1)  [hvis IIR-BLT optræder]
%{
Orden n | Nævnerpolynomium
--------|------------------------------------------
   1    | s + 1
   2    | s^2 + 1.4142 s + 1
   3    | s^3 + 2 s^2 + 2 s + 1
   4    | s^4 + 2.6131 s^3 + 3.4142 s^2 + 2.6131 s + 1
   5    | s^5 + 3.2361 s^4 + 5.2361 s^3 + 5.2361 s^2 + 3.2361 s + 1
   6    | s^6 + 3.8637 s^5 + 7.4641 s^4 + 9.1416 s^3 + 7.4641 s^2 + 3.8637 s + 1
Alle har tæller = 1.

IIR-BLT pipeline (hvis det dukker op som delspørgsmål):
  spec -> prewarp Omega = (2/Ts) tan(pi f) -> orden n
  -> prototype (appendix) -> lp2lp/lp2hp/lp2bp/lp2bs -> bilinear -> freqz dB
  LP: nu_s = Omega_s/Omega_p ; HP omvendt: nu_s = Omega_p/Omega_s ; BP/BS dobbelt orden.
%}
proto_den{1} = [1, 1];
proto_den{2} = [1, 1.4142, 1];
proto_den{3} = [1, 2, 2, 1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
proto_den{5} = [1, 3.2361, 5.2361, 5.2361, 3.2361, 1];
proto_den{6} = [1, 3.8637, 7.4641, 9.1416, 7.4641, 3.8637, 1];
