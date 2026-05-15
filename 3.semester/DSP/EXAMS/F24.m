%% 62743 DSP -- F24 Exam -- Working Script
% Exam PDF:     Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\62743 F24 Exam.pdf
% Solution PDF: Obsidian\Archive\3rd Semester\DSP\Exercises\Exams\62743 F24 Exam student solutions.pdf
%
% Date attempted:
% Time target:    4 hours hard cap
% Self-score:     / total marks
%
% --- Fill these in during the first 5 minutes of reading the exam ---
% P1:
% P2:
% P3:
% P4:

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 --



%% Problem 2 -- Anti-aliasing filter (analog Butterworth LP)
% Signal: xA(t) = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t)
A1 = 3;    F1 = 200;
A2 = 1.5;  F2 = 750;

%% 2-1  Minimum sampling frequency
% Nyquist: Fs >= 2*Fmax  (equivalently F <= Fs/2)
Fmax   = max(F1, F2);     % = 750 Hz
Fs_min = 2 * Fmax;        % = 1500 Hz   <-- answer to 2-1b
fprintf('2-1: Fs_min = %g Hz\n', Fs_min);

%% 2-2  Aliasing at Fs = 1000 Hz
Fs = 1000;
% a) Fs = 1000 < 1500  -> Nyquist violated, aliasing occurs.
%    F1 = 200 Hz is below Fs/2 = 500 -> safe.
%    F2 = 750 Hz is above Fs/2 = 500 -> folds.
% b) Folding formula:  F_alias = F2 - 2*(F2 - Fs/2)
F_alias = F2 - 2*(F2 - Fs/2);    % = 250 Hz
fprintf('2-2: F_alias = %g Hz\n', F_alias);

%% 2-3  Spectrum via FFT — confirms the aliasing predicted in 2-2
Fs = 1000;
N  = 1e5;

t  = time_vec(Fs, N);
xA = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);

XA = fftshift(fft(xA) / N);
f  = frequency_vec(Fs, N);

figure;
plot(f, abs(XA), 'LineWidth', 1.5);
xlabel('f·F_s  [Hz]'); ylabel('|X_A[k]|');
title('Spectrum of x_A[n], F_s = 1000 Hz'); grid on;

% (b) Discussion:
% Spectret viser to peaks i det positive frekvensområde:
%   - 200 Hz med amplitude 1.5  (= A1/2, det originale signal)
%   - 250 Hz med amplitude 0.75 (= A2/2, 750 Hz komponenten "foldet ind"
%     pga. Fs = 1000 < 2*Fmax = 1500 Hz)
% Dette bekræfter beregningen i 2-2: F_alias = 250 Hz.

%% 2-4

% Det er et 4. ordens Butterworth filter. 
% Det er et lavpasfilter.
% Pasbånds frekvensen (Engelsk: edge) er Fp = 350 Hz

%a) Opskriv filterkoefficienterne for det valgte prototype filter, se appendiks 1.

% Pick prototype (order 4 from spec)

proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
b_proto = 1;
a_proto = proto_den{4};

% (b) Transform prototype -> real LP at Fp = 350 Hz
Fp = 350;
Wp = 2*pi*Fp;
[b_AA, a_AA] = lp2lp(b_proto, a_proto, Wp);

H_AA = tf(b_AA, a_AA)

%% 2-5
% a) Plot magnituden af frekvensresponset for H_AA(s) i lineære enheder som funktion af analog frekvens F i Hz.

F = linspace(0, 2000, 4096);   % analog frequency vector [Hz]
W = 2*pi*F;                    % -> rad/s for freqs (Hz->rad/s gotcha)
H = freqs(b_AA, a_AA, W);      % use the TRANSFORMED filter, not the prototype

figure;
plot(F, abs(H), 'LineWidth', 1.5);
xlabel('F  [Hz]'); ylabel('|H_{AA}(F)|');
title('Magnitude of anti-aliasing filter |H_{AA}(F)|'); grid on;

%% Problem 3 --
% Et analogt signal fa(t) har det Fourier transformerede spektrum Fa(Omega) vist i exam-PDF.
% Spektret er en trapez der er nul udenfor |Omega| > 200 rad/s.

%% 3-1  Nyquist-tjek for fa(t)
% Signalet fa(t) samples med samplingsvinkelfrekvens Omega_s; tre kandidater:
Omega_s_a = 200;     % rad/s
Omega_s_b = 400;     % rad/s
Omega_s_c = 500;     % rad/s

% Reasoning:
% Minimum sampling er 2*Omega_max og Omega_max = 200 rad/s
% (læst af spektrumgrafen: spektret er nul for |Omega| > 200 rad/s).
% Så minimum sampling er 2*200 = 400 rad/s.
Omega_max     = 200;
Omega_s_min   = 2 * Omega_max;     % = 400 rad/s
fprintf('3-1: Omega_s_min = %g rad/s\n', Omega_s_min);

% a) Omega_s = 200 rad/s  -> NEJ, 200 < 400 -> aliasing
% b) Omega_s = 400 rad/s  -> JA, lige på grænsen (boundary case OK)
% c) Omega_s = 500 rad/s  -> JA, over 400 rad/s

%% 3-2  Samme tjek, men nu paa et andet signal ga(t)
% ga(t) er også båndbegrænset, men med Omega_max = 250 rad/s.
% Threshold = 2*250 = 500 rad/s.
Omega_max_g   = 250;
Omega_s_min_g = 2 * Omega_max_g;   % = 500 rad/s
fprintf('3-2: Omega_s_min (for g) = %g rad/s\n', Omega_s_min_g);

% Det gør kun (c) på 500 rad/s, da 250*2 = 500 rad/s.
% (a) 200 < 500 -> aliasing
% (b) 400 < 500 -> aliasing
% (c) 500 = 500 -> JA, lige på grænsen

%% Problem 4 -- IIR båndstop Butterworth filter via BLT
% Filter design metode: Bilineær transformationsmetode (BLT) med alpha = 2/Ts.
% Filtertype: IIR båndstop Butterworth filter.

% --- Spec fra eksamen ---
Fs   = 5000;             % samplingsfrekvens [Hz]
Ts   = 1/Fs;             % sampling periode [s]

% Digitale normaliserede kantfrekvenser  f = F/Fs  (enhedsløs)
fpL  = 45.0 / Fs;        % pasbånd nedre kant
fpH  = 55.5 / Fs;        % pasbånd øvre kant
fsL  = 48.0 / Fs;        % stopbånd nedre kant
fsH  = 52.1 / Fs;        % stopbånd øvre kant

ApdB = 3;                % pasbånd dæmpning [dB]
AsdB = 20;               % stopbånd dæmpning [dB]

%% 4-1  Analog prototype Butterworth filter
% a) Udregn de analoge stopbånds- og pasbåndsvinkelfrekvenser
%    Omega_sL, Omega_sH, Omega_pL, Omega_pH  (via prewarping).
% b) Vis at prototype-ordenen n der opfylder spec er n = 3.
% c) Opskriv overføringsfunktionen for prototype-filteret med n = 3.

% (a) Prewarp digital -> analog (rad/s):  Omega = 2*Fs*tan(pi*f)

omega_pL=fpL*2*pi;

omega_pH=fpH*2*pi;

omega_sL=fsL*2*pi;

omega_sH=fsH*2*pi;



Omega_pL=(2/Ts)*tan(omega_pL/2)

Omega_pH=(2/Ts)*tan(omega_pH/2)

Omega_sL=(2/Ts)*tan(omega_sL/2)

Omega_sH=(2/Ts)*tan(omega_sH/2)


% (b) Prototype orden:

vs     = (Omega_pH - Omega_pL) / (Omega_sH - Omega_sL);
eps_sq = 10^(0.1*ApdB) - 1;                                       % epsilon^2

n = ceil( log10( (10^(0.1*AsdB) - 1) / eps_sq ) / (2*log10(vs)) )

% -> n = 3


% (c) Prototype TF for n = 3 (fra appendix):

proto_num= [1];
proto_den{3} = [1, 2, 2, 1];

H_Proto= tf(proto_num, proto_den{3})



%% 4-2  Analog båndstopfilter HBS(s)
% a) Opskriv overføringsfunktionen for det analoge båndstopfilter HBS(s).

Omega_0=sqrt(Omega_pL*Omega_pH);

W=Omega_pH-Omega_pL;


[num_bs, den_bs]=lp2bs(proto_num, proto_den{3}, Omega_0, W)


H_bs=tf(num_bs, den_bs)

% b) Plot magnituden af HBS(s) i lineære enheder som funktion af Omega.

omega_grid = 0:0.1:1000;            % rad/s, dense nok til at vise notch'en
h = freqs(num_bs, den_bs, omega_grid);

figure;
plot(omega_grid, abs(h), 'LineWidth', 1.5);
xlabel('\Omega [rad/s]'); ylabel('|H_{BS}(\Omega)|');
title('Magnitude af analogt båndstopfilter'); grid on;


%% 4-3  Digitalt båndstopfilter HBS(z) via BLT
% a) Plot amplituden af overføringsfunktionen i dB som funktion af f*Fs i Hz.

[bz, az] = bilinear(num_bs, den_bs, Fs);

[H,f] = freqz(bz, az, 4096, Fs);
figure
subplot(2,1,1)
plot(f, 20*log10(abs(H)))
title('Magnitude Response')
xlabel('f·F_s [Hz]');
ylabel('|H| [dB]');
grid on
xlim([40 60]);

% b) Aflæs dæmpningen i dB ved stopbåndets øvre og nedre kantfrekvenser.

[H,f] = freqz(bz, az, [fsL*Fs, fsH*Fs], Fs);

dB = 20*log10(abs(H));            % de to svar i dB
fprintf('F = %.1f Hz  ->  %.2f dB\n', f(1), dB(1));   % stopbånd nedre kant
fprintf('F = %.1f Hz  ->  %.2f dB\n', f(2), dB(2));   % stopbånd øvre kant

% c) Sammenlign med spec og diskutér.

% Lever op til kravet om 20dB dæmpning ved stopbånd, med lidt margin dette
% giver mening da vi udregnede n til at være 2.45 men valgte at sætte den
% til 3.


%% --- Scratch / sandbox ---

%% Appendix

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

% Prototype polynomials for quick reference:
proto_den{1} = [1, 1];
proto_den{2} = [1, 1.4142, 1];
proto_den{3} = [1, 2, 2, 1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
proto_den{5} = [1, 3.2361, 5.2361, 5.2361, 3.2361, 1];
proto_den{6} = [1, 3.8637, 7.4641, 9.1416, 7.4641, 3.8637, 1];
