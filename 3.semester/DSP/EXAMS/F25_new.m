%% 62743 DSP -- F25 Exam -- Working Script
% Exam PDF:     Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\Exam sets\62743 F25 Exam.pdf
% Solution PDF: Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\Solutions\62743 F25 Exam student solutions.pdf
%
% Date attempted:
% Time target:    4 hours hard cap
% Self-score:     / total marks
%
% Filter-first strategi: fokus paa Q2 (IIR HP via BLT) og Q4 (filter
% realisering + anvendelse). Q1 og Q3-3 er matematik -> udskudt.

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 -- LTI system, H(z), mag/phase, cascade  [MATEMATIK - UDSKUDT]
% (filter-first strategi: tages senere)



%% Problem 2 -- IIR højpas Butterworth filter via BLT   [FILTER]
% Filter design metode: BLT med alpha = 2/Ts.
% Filtertype: IIR HØJPAS Butterworth.

% --- Spec fra eksamen ---
Fs2  = 4000;             % samplingsfrekvens [Hz]
Ts2  = 1/Fs2;
fs   = 450  / Fs2;       % digital normaliseret STOPbånd kant (HP: stop < pas)
fp   = 1000 / Fs2;       % digital normaliseret PASbånd kant
AsdB = 30;               % stopbånd dæmpning [dB]
ApdB = 3;                % pasbånd dæmpning [dB]

%% 2-1  Analog prototype Butterworth filter
% - Udregn epsilon.
% - Udregn de analoge stop-/pasbånds vinkelfrekvenser Omega_s og Omega_p (prewarp).
% - Bestem minimum orden n.
% - Opskriv prototype TF for den fundne orden (se appendix).

eps_sq = 10^(0.1*ApdB) - 1;     % epsilon^2 fra pasbåndsdæmpning Ap
e=sqrt(eps_sq);                 % epsilon (~1 når Ap = 3 dB)
fprintf('2-1: e = %g \n', e);


omega_s=fs*2*pi;                  % digital vinkelfrekvens (rad/sample)
Omega_s=(2/Ts2)*tan(omega_s/2)    % prewarp -> analog stopbånd (rad/s)

omega_p=fp*2*pi;                  % digital vinkelfrekvens (rad/sample)
Omega_p=(2/Ts2)*tan(omega_p/2)    % prewarp -> analog pasbånd (rad/s)


vs     = Omega_p/Omega_s;     % HØJPAS: ratio Op/Os (lavpas ville være Os/Op)

% Butterworth minimum orden (ceil = rund altid OP for at opfylde spec)
n = ceil( log10( (10^(0.1*AsdB) - 1) / eps_sq ) / (2*log10(vs)) )


% Prototype Butterworth TF af orden n (slås op i appendix)
proto_num= [1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];   % orden n = 4

H_Proto= tf(proto_num, proto_den{4})             % analog prototype H(s)

%% 2-2  Analogt højpasfilter HHP(s)
% - Hvilken transformation? (LP-prototype -> HP)
% - Opskriv HHP(s).
% - Plot |HHP(s)| i dB som funktion af vinkelfrekvens.
% - Opfylder filteret de analoge krav?

% LP-prototype -> højpas: s -> Omega_p/s (cutoff = pasbåndskant)
[b_HP,a_HP] = lp2hp(proto_num, proto_den{4}, Omega_p);

HHP = tf(b_HP, a_HP)     % analog højpas overføringsfunktion H_HP(s)



% 1024 punkter; MATLAB auto-vælger Omega-området ud fra poler/nulpunkter
[H_analog,wout] = freqs(b_HP, a_HP, 1024);

figure;
plot(wout, 20*log10(abs(H_analog)), 'LineWidth', 2);
xlabel('\Omega [rad/s]'); ylabel('|H(\Omega)|  [dB]');
title('Analogt højpasfilter H_{HP}(s)'); grid on;

% Eksakt dB ved de to kravspunkter (stopbånd Om_s, pasbånd Om_p)
H_chk = freqs(b_HP, a_HP, [Omega_s, Omega_p]);
fprintf('Om_s=%.0f -> %.2f dB\n', Omega_s, 20*log10(abs(H_chk(1))));
fprintf('Om_p=%.0f -> %.2f dB\n', Omega_p, 20*log10(abs(H_chk(2))));


%%
% *Svar 2-2:* Filteret opfylder netop kravene: ved stopbåndskanten er
% dæmpningen ≈ 34.6 dB (krav ≥ 30 dB), og ved pasbåndskanten ≈ 3.0 dB
% (krav 3 dB).


%% 2-3  Digitalt højpasfilter HHP(z) via BLT
% - Opskriv s<->z relationen (BLT).
% - Udregn HHP(z).

% s=2/Ts*z-1/z+1

[bz, az]= bilinear(b_HP, a_HP, Fs2);

HHP_z= tf(bz, az, Ts2)

%% 2-4  Undersøg det designede digitale filter
% - Plot |HHP| i dB som funktion af F = f*Fs i Hz.
% - Aflæs/beregn dæmpningen ved 450 Hz og 1000 Hz.
% - Sammenlign med kravspec.

% 4096 punkter, Fs2 som 4. arg => f returneres i Hz
[h,f] = freqz(bz, az, 4096, Fs2);

figure
plot(f, 20*log10(abs(h)), 'LineWidth', 1.5)
title('Digitalt højpasfilter H_{HP}(z) - magnituderespons')
xlabel('F = f·F_s [Hz]');
ylabel('|H_{HP}| [dB]');
grid on;

% Dæmpning ved kravspunkterne: stopbånd 450 Hz, pasbånd 1000 Hz
H_chk2 = freqz(bz, az, [450, 1000], Fs2);
dB2 = 20*log10(abs(H_chk2));
fprintf('F = 450 Hz  (stopbånd) -> %.2f dB\n', dB2(1));
fprintf('F = 1000 Hz (pasbånd)  -> %.2f dB\n', dB2(2));

%%
% *Svar 2-4:* BLT bevarer responsen ved de prewarpede kanter, så de
% digitale tal matcher de analoge fra 2-2 (≈ -34.6 dB @ 450 Hz,
% ≈ -3.0 dB @ 1000 Hz). Kravene (≥ 30 dB dæmpning i stopbånd @ 450 Hz,
% ~3 dB i pasbånd @ 1000 Hz) er dermed opfyldt.



%% Problem 3 -- Sampling (3-1/3-2) + ROC/stabilitet (3-3, MATEMATIK-UDSKUDT)
% Signal: x(t) = 3*cos(2*pi*1500*t) + 2*cos(2*pi*4200*t),  Fs = 8000 Hz

Fs3 = 8000;
% 3-1: Skitsér amplitudespektret -10 kHz .. 10 kHz
% 3-2: Aliasering i -4 kHz .. 4 kHz? Ved hvilken frekvens?




%% Problem 4 -- Digitalt LP filter: realisering + anvendelse   [FILTER]
% Filteret har 3 dB dæmpning ved 400 Hz. Designet med Fs = 5000 Hz.
% Realisering (fra blokdiagram i exam):
%   feedforward gains:  0.0102, 0.0305, 0.0305, 0.0102   (x[n..n-3])
%   feedback gains:     2.0038, -1.4471, 0.3618          (y[n-1..n-3])

Fs4 = 5000;
Ts4= 1/Fs4;

b=[0.0102, 0.0305, 0.0305, 0.0102];
a=[1, -2.0038, 1.4471, -0.3618];

%% 4-1  Filterform, FIR/IIR, transferfunktion H(z)
% - Navngiv den digitale filterform.
% - FIR eller IIR? Argumentér.
% - Opskriv H(z) (byg b og a fra blokdiagrammets koefficienter).

Hz = tf(b, a, Ts4, 'Variable','z^-1');
Hz                                      % vis H(z) i output

%%
% *Svar 4-1:* Det er et *Direct Form I*-filter. Det er et *IIR*-filter,
% fordi y[n] afhænger af tidligere udgange y[n-1..n-3] (feedback, a ≠ [1])
% → uendelig impulsrespons. Overføringsfunktionen H(z) ses ovenfor.

%% 4-2  Magnituderespons
% - Plot |H| i dB som funktion af F = f*Fs i Hz.
% - Aflæs pasbåndsfrekvensen (3 dB punktet). Stemmer med 400 Hz?

F_vec = frequency_vec(Fs4, 1000);
[h,f]=freqz(b,a,F_vec,Fs4);

figure
plot(f, 20*log10(abs(h)))
title('Magnitude Response')
xlabel('f·F_s [Hz]');
ylabel('|H| [dB]');
xlim([0 1000]);
yline(-3, '--r', '-3dB');
xline(400, '--g', '400 Hz');
grid on

%%
% *Svar 4-2:* Magnitudeplottet skærer -3 dB-linjen ved ≈ 400 Hz, hvilket
% stemmer med opgavens krav om 3 dB dæmpning ved 400 Hz.

%% 4-3  Poler og nulpunkter
% - Find og plot poler/nulpunkter.
% - Stabil eller ej?

nuller = roots(b)
poler  = roots(a)

figure
zplane(b, a)
title('Pol-/nulpunktsplot')

%%
% *Svar 4-3:* Alle poler ligger inden for enhedscirklen (største
% polradius < 1), se de viste poler og pol-/nulpunktsplottet ovenfor
% → filteret er *stabilt*.

%% 4-4  Sampling af analogt signal
% xa(t) = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t)
A1 = 5;   F1 = 50;
A2 = 3;   F2 = 1000;
% - Aliasering ved Fs = 5000 Hz?
% - Plot det samplede signal, t = 0 .. 0.05 s.

t4 = 0:1/Fs4:0.05;

xa_sampled = A1*cos(2*pi*F1*t4) + A2*cos(2*pi*F2*t4);

figure
plot(t4, xa_sampled);
grid on;
hold off;

%%
% *Svar 4-4:* Nyquist-frekvensen er Fs/2 = 2500 Hz. Den højeste
% signalfrekvens F2 = 1000 Hz < 2500 Hz, så der sker *ingen aliasing*
% ved Fs = 5000 Hz.

%% 4-5  Filtrér det samplede signal
% - Hvad forventes filteret at gøre ved de to frekvenskomponenter?
% - Filtrér med filter(b, a, x), plot t = 0 .. 0.05 s.
% - Kommentér forskellen før/efter.

xa_filt = filter(b, a, xa_sampled);

figure
plot(t4, xa_sampled, t4, xa_filt, 'LineWidth', 1.2)
legend('Før (rå)','Efter (filtreret)'); grid on
xlabel('t [s]'); ylabel('amplitude')
title('xa[n] før og efter LP-filtrering')

%%
% *Svar 4-5:* Filteret er et lavpasfilter med 3 dB ved 400 Hz, så vi
% forventer at 50 Hz-komponenten passerer næsten uændret, mens
% 1000 Hz-komponenten dæmpes kraftigt. Det ses tydeligt: efter
% filtrering er den hurtige 1000 Hz-svingning næsten væk, og signalet
% følger den glatte 50 Hz-komponent.


%% --- Scratch / sandbox ---

%% Appendix -- Butterworth lowpass prototype (3 dB, eps = 1)

%{
Order n | Denominator polynomial
--------|------------------------------------------
   1    | s + 1
   2    | s^2 + 1.4142s + 1
   3    | s^3 + 2s^2 + 2s + 1
   4    | s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1
   5    | s^5 + 3.2361s^4 + 5.2361s^3 + 5.2361s^2 + 3.2361s + 1
   6    | s^6 + 3.8637s^5 + 7.4641s^4 + 9.1416s^3 + 7.4641s^2 + 3.8637s + 1
All have numerator = 1
%}

proto_den{1} = [1, 1];
proto_den{2} = [1, 1.4142, 1];
proto_den{3} = [1, 2, 2, 1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
proto_den{5} = [1, 3.2361, 5.2361, 5.2361, 3.2361, 1];
proto_den{6} = [1, 3.8637, 7.4641, 9.1416, 7.4641, 3.8637, 1];
