%% Lecture 11 - Structure-borne sound and vibration isolation
% 34840 Fundamentals of Acoustics and Noise Control | 17 November 2026
%
% Worked learning document for the vibration problem set that Learn files
% under module 11: 31200_Problems_8_2022.pdf (Ohlrich, "Chapter 6",
% four problems). Official answers: 31200_Solutions_8_2022.pdf.
% NB: the sheet named "34840_Problems 11_2026.pdf" is the SOUND INSULATION
% set (Learn module 12, lecture 12) and is not worked here.
%
% Every formula is first written as an equation, then calculated in one
% plain MATLAB line. Lines without a semicolon print their result. The
% official answers are written in the comments next to each result.
%
% Constants: g = 9.81 m/s^2 (Problems 2) and 9.82 (Problem 4) reproduce
% the official solutions; the difference is in the third digit only.
% Air c = 344 m/s for the bending-wave plot (as on deck page 34).

%% Problem 1 - Two springs, two masses: natural frequencies (symbolic)
% (a) springs in parallel: $s_{eq} = s_1 + s_2 = 2s$
% (b) one spring, masses stacked: $m_{eq} = 2m$
% (c) springs in series: $s_{eq} = s_1 s_2/(s_1+s_2) = s/2$
% (d) mass between two springs (one up, one down): both act on the mass, so parallel, $2s$
%
% $$f_a = f_d = \frac{1}{2\pi}\sqrt{\frac{2s}{m}},\qquad f_b = f_c = \frac{1}{2\pi}\sqrt{\frac{s}{2m}}$$
ratio_ad_over_bc = sqrt(2)/sqrt(1/2)  % 2: (a) and (d) are an octave above (b) and (c)

%% Problem 2 - Vibration exciter on four leaf springs
s_leaf = 0.5e3;       % 0.5 N/mm = 500 N/m per leaf spring
m2 = 18e-3;           % coil + table [kg]
M2 = 200e-3;          % payload [kg]
g = 9.81;
%
% (a) four springs in parallel: $s_{eq} = 4s$, $f_a = \frac{1}{2\pi}\sqrt{4s/m}$
s_eq = 4*s_leaf                       % 2000 N/m
f_a = sqrt(s_eq/m2)/(2*pi)            % 53.05 Hz (official: 53 Hz)
%
% (b) static deflection from the payload: $\xi_{stat} = Mg/(4s)$
xi_stat = M2*g/s_eq                   % 0.981e-3 m (official: ~1e-3 m)
%
% $$f_b = \frac{1}{2\pi}\sqrt{\frac{4s}{m+M}}$$
f_b = sqrt(s_eq/(m2+M2))/(2*pi)       % 15.24 Hz (official: 15.2 Hz)
%
% Check with the static-deflection rule $f_0 \approx 0.5/\sqrt{\xi_0}$, where
% $\xi_0$ is the TOTAL deflection under (m+M):
f_b_rule = 0.5/sqrt((m2+M2)*g/s_eq)   % 15.3 Hz

%% Problem 3 - Undamped mass-spring driven by a force, F = 5 N
s3 = 23.8e3; m3 = 1.5; F3 = 5;
%
% (a) $f_0 = \frac{1}{2\pi}\sqrt{s/m}$
w0_3 = sqrt(s3/m3)                    % 125.96 rad/s (official: 126 rad/s)
f0_3 = w0_3/(2*pi)                    % 20.05 Hz (official: 20.1 Hz)
%
% (b) $\omega = 37.8$ rad/s, below resonance (Omega = 0.30):
% $$|\xi| = \frac{|F|}{s\,|1-(\omega/\omega_0)^2|},\quad |v| = \omega|\xi|,\quad |a| = \omega^2|\xi|$$
wb = 37.8;
xi_b = F3/(s3*abs(1-(wb/w0_3)^2))     % 0.2309e-3 m (official: 0.231e-3 m)
v_b = wb*xi_b                         % 8.73e-3 m/s (official: 8.7e-3 m/s)
a_b = wb^2*xi_b                       % 0.330 m/s^2 (official: 0.33 m/s^2)
%
% (c) $\omega = 378$ rad/s, above resonance (Omega = 3.0):
wc = 378;
xi_c = F3/(s3*abs(1-(wc/w0_3)^2))     % 2.624e-5 m (official: 2.62e-5 m)
v_c = wc*xi_c                         % 9.92e-3 m/s (official: 9.9e-3 m/s)
a_c = wc^2*xi_c                       % 3.75 m/s^2 (official: 3.75 m/s^2)
%
% (d) force on the foundation, undamped: $|F_f| = s|\xi|$
Ff_b = s3*xi_b                        % 5.49 N (official: 5.5 N)
Ff_c = s3*xi_c                        % 0.625 N (official: 0.62 N)
%
% Same thing as a transmissibility, $T = |F_f|/|F| = 1/|1-\Omega^2|$:
T_b_dB = 20*log10(Ff_b/F3)            % +0.82 dB (below sqrt2*f0: amplified)
T_c_dB = 20*log10(Ff_c/F3)            % -18.1 dB (above sqrt2*f0: isolated)

%% Problem 4 - Instrument on a spring on a vibrating train floor
% 4.1 Base (motion) excitation, Newton on the mass:
% $$m\ddot u = s(u_f - u)\ \Rightarrow\ \frac{u}{u_f} = \frac{s}{s-\omega^2 m} = \frac{1}{1-(\omega/\omega_0)^2}$$
%
% 4.2 Want $u/u_f = -0.1$ at 25 Hz with m = 1.5 kg. Solve for s:
% $$s = \frac{-(u/u_f)\,\omega^2 m}{1-u/u_f}$$
w4 = 2*pi*25;                         % 157.1 rad/s
m4 = 1.5;
ratio4 = -0.1;
s4 = -ratio4*w4^2*m4/(1-ratio4)       % 3365 N/m (official: 3.37e3 N/m)
%
% Static deflection: $u_0 = mg/s$
u0 = m4*9.82/s4                       % 4.38e-3 m (official: 4.4e-3 m, with g = 9.82)
%
% The frequency to avoid is the resonance:
w0_4 = sqrt(s4/m4)                    % 47.4 rad/s (official: 47.4 rad/s)
f0_4 = w0_4/(2*pi)                    % 7.54 Hz (official: 7.54 Hz)
Omega4 = w4/w0_4                      % 3.32 = sqrt(11): 25 Hz sits well above sqrt2*f0
f0_rule4 = 0.5/sqrt(u0)               % 7.56 Hz, the static-deflection rule agrees

%% Transmissibility with viscous damping (deck pages 35-38)
% $$T(\Omega,\zeta) = \sqrt{\frac{1+(2\zeta\Omega)^2}{(1-\Omega^2)^2+(2\zeta\Omega)^2}},\qquad \Omega = \omega/\omega_0,\ \zeta = r/(2\sqrt{ms})$$
% Every curve passes T = 1 at Omega = sqrt(2), whatever the damping.
T_sqrt2 = sqrt((1+(2*0.3*sqrt(2))^2)/((1-2)^2+(2*0.3*sqrt(2))^2))   % 1.000 for any zeta
%
% Resonance peak, small damping: $T(1) \approx 1/(2\zeta)$
T_res_z005_dB = 20*log10(sqrt(1+0.1^2)/0.1)                          % +20.0 dB for zeta = 0.05
%
% Isolation at Omega = 10 (decade above f0): damping costs isolation
T10_z0_dB = 20*log10(1/abs(1-100))                                   % -39.9 dB
T10_z01_dB = 20*log10(sqrt((1+(2*0.1*10)^2)/(99^2+(2*0.1*10)^2)))    % -32.9 dB
T10_z05_dB = 20*log10(sqrt((1+(2*0.5*10)^2)/(99^2+(2*0.5*10)^2)))    % -19.9 dB
%
% Isolation effectiveness, rigid foundation: $10\log E_{iso} = -20\log T$
%
% Static-deflection rule: $f_0 = \frac{1}{2\pi}\sqrt{g/\xi_0} \approx 0.5/\sqrt{\xi_0}$
f0_4mm = sqrt(9.81/0.004)/(2*pi)      % 7.88 Hz
f0_10mm = sqrt(9.81/0.010)/(2*pi)     % 4.98 Hz  (course text: 4-10 mm <-> 8-5 Hz)

Omega = logspace(-1, 1, 600);
zetas = [0.01 0.05 0.1 0.2 0.5 1.0];
fig1 = figure('Visible','off','Position',[100 100 760 470]);
theme(fig1,'light');
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(1)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(1)*Omega).^2))), 'LineWidth',1.4); hold on;
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(2)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(2)*Omega).^2))), 'LineWidth',1.4);
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(3)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(3)*Omega).^2))), 'LineWidth',1.4);
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(4)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(4)*Omega).^2))), 'LineWidth',1.4);
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(5)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(5)*Omega).^2))), 'LineWidth',1.4);
semilogx(Omega, 20*log10(sqrt((1+(2*zetas(6)*Omega).^2)./((1-Omega.^2).^2+(2*zetas(6)*Omega).^2))), 'LineWidth',1.4);
xline(sqrt(2),'k--','\surd2','LabelVerticalAlignment','bottom');
yline(0,'k:');
plot([3 3.32],[20*log10(1/8) 20*log10(1/10)],'ko','MarkerFaceColor','k');
text(3.6,-17,'P3(c), P4','FontSize',9);
hold off; grid on;
ylim([-40 40]); xlim([0.1 10]);
xlabel('\Omega = f / f_0'); ylabel('20 log_{10} T  [dB]');
title('Force (or motion) transmissibility of a mass-spring-damper');
legend('\zeta = 0.01','\zeta = 0.05','\zeta = 0.1','\zeta = 0.2','\zeta = 0.5','\zeta = 1','Location','southwest');
outdir = fullfile(getenv('HOME'),'DTU','Obsidian','Courses','34840 Fundamentals of Acoustics and Noise Control','Images','Lecture11');
if ~exist(outdir,'dir'); mkdir(outdir); end
exportgraphics(fig1, fullfile(outdir,'transmissibility.png'), 'Resolution', 150);

%% Bending waves and the critical (coincidence) frequency (deck pages 30-34)
% $$c_B = \sqrt{\omega}\,\sqrt[4]{B/m'} \approx \sqrt{1.8\,c_L\,h\,f}$$
% Bending waves are dispersive: c_B grows as sqrt(f). Where c_B = c (air),
% the plate radiates (and transmits) efficiently: the critical frequency
% $$f_c = \frac{c^2}{1.8\,c_L\,h}$$
% Course text Table 6.3.1: glass c_L1 = 5151 m/s, dense concrete c_L2 = 3360 m/s.
c_air = 344;
fc_glass4mm = c_air^2/(1.8*5151*0.004)        % 3190 Hz
fc_concrete100 = c_air^2/(1.8*3360*0.100)     % 196 Hz
fc_concrete200 = c_air^2/(1.8*3360*0.200)     % 98 Hz
%
% Upper limit for the thin-plate formula: bending wavelength > 6h,
% $c_B/f = 6h \Rightarrow f = 1.8\,c_L/(36\,h)$
f_upper_concrete100 = 1.8*3360/(36*0.100)     % 1680 Hz (lambda_B = 6h)

f = logspace(log10(50), log10(5000), 300);
fig2 = figure('Visible','off','Position',[100 100 760 470]);
theme(fig2,'light');
loglog(f, sqrt(1.8*3360*0.200*f),'LineWidth',1.4); hold on;
loglog(f, sqrt(1.8*3360*0.100*f),'LineWidth',1.4);
loglog(f, sqrt(1.8*3360*0.050*f),'LineWidth',1.4);
loglog(f, sqrt(1.8*5151*0.010*f),'--','LineWidth',1.4);
loglog(f, sqrt(1.8*5151*0.004*f),'--','LineWidth',1.4);
yline(c_air,'r-','air, c = 344 m/s','LineWidth',1.6,'LabelHorizontalAlignment','left');
hold off; grid on;
xlim([50 5000]); ylim([20 2000]);
xlabel('Frequency [Hz]'); ylabel('Bending wave speed c_B [m/s]');
title('Bending wave speed in plates; crossing the air line = critical frequency');
legend('concrete 200 mm','concrete 100 mm','concrete 50 mm','glass 10 mm','glass 4 mm','Location','southeast');
exportgraphics(fig2, fullfile(outdir,'bending_wave_speed.png'), 'Resolution', 150);
