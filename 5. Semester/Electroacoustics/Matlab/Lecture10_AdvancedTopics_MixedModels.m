%% Lecture 10 - Advanced topics: mixed models and metamaterials, worked
% 34870 Electroacoustics | 26 October 2026 (FL)
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it.
% There is no problem sheet for this lecture. The three "problems" are the
% examples the deck works through, recomputed so the slide plots can be
% checked number by number:
%
% # the lumped ear-drum impedance of slide 2,
% # the five-layer wall of slides 4-9, by lumped elements (LEM), mixed
%   LEM + transfer matrices (TMM) and full TMM,
% # the two 1-D metamaterial dispersion relations of slide 18.
%
% Slide readings (no numbers are printed on the slides, only plots) are
% written next to each result as "slide:".

%% 1 - Ear-drum acoustic impedance (slide 2)
% Two series R-L-C branches in parallel (acoustic impedance analogy, units
% Pa s/m^3). Each branch is a resonance of the drum.
%
% $$Z_i = R_i + j\omega L_i + \frac{1}{j\omega C_i}, \qquad Z_{ED} = \frac{Z_1 Z_2}{Z_1 + Z_2}$$
R1 = 50.6e6; C1 = 1.9e-12; L1 = 9400;
R2 = 31.1e6; C2 = 2.1e-12; L2 = 983.8;
%%
% Branch resonances: $f_i = \frac{1}{2\pi\sqrt{L_i C_i}}$
% (slide: the two dips of |Z| at about 1.2 and 3.5 kHz)
f1 = 1/(2*pi*sqrt(L1*C1))
f2 = 1/(2*pi*sqrt(L2*C2))
%%
% Quality factors: $Q_i = \frac{1}{R_i}\sqrt{L_i/C_i}$ (low Q = broad, well-damped dips)
Q1 = sqrt(L1/C1)/R1
Q2 = sqrt(L2/C2)/R2
%%
% Low frequencies: both branches are compliance-controlled, the compliances
% add, $Z_{ED} \approx \frac{1}{j\omega(C_1 + C_2)}$. As an air volume:
% $V_{eq} = (C_1 + C_2)\rho c^2$
rho = 1.2; c = 343;
V_eq_cm3 = (C1 + C2)*rho*c^2*1e6
%%
% |Z| at 20 Hz (slide: about 2*10^9 at the left edge)
Z = @(f) 1./(1./(R1 + 1j*2*pi*f*L1 + 1./(1j*2*pi*f*C1)) + 1./(R2 + 1j*2*pi*f*L2 + 1./(1j*2*pi*f*C2)));
absZ_20Hz = abs(Z(20))
%%
f = logspace(log10(20), log10(20e3), 2000);
figure
yyaxis left, loglog(f, abs(Z(f))), ylabel('|Z| [Pa s/m^3]')
yyaxis right, semilogx(f, angle(Z(f))*180/pi), ylabel('phase [deg]')
grid on, xlabel('f [Hz]'), title('Lumped ear-drum impedance (slide 2)')

%% 2 - The five-layer wall (slides 4-9)
% Plane wave, normal incidence. Layers in the order of the sketch on slide 4:
% drywall 1 cm, insulation 3 cm, brick 5 cm, air gap 1 cm, wood 2 cm.
% Everything is per unit area: "pressure" is the across variable, particle
% velocity the through variable, impedances are specific (Pa s/m).
rho_l = [600 200 2000 1.2 550];      % drywall, insulation, brick, air, wood [kg/m^3]
c_l   = [6000 500 3600 343 4000];    % [m/s]
l_l   = [0.01 0.03 0.05 0.01 0.02];  % [m]
rho0 = 1.2; c0 = 343;
%%
% *Lumped model (slide 5).* A stiff, heavy layer moves as one block: a series
% mass $M_i = \rho_i l_i$. A soft layer is squeezed: a shunt compliance
% $C_i = \frac{l_i}{\rho_i c_i^2}$. The far side radiates into air: $R_{out} = \rho_0 c_0$.
M1 = rho_l(1)*l_l(1)
C2 = l_l(2)/(rho_l(2)*c_l(2)^2)
M3 = rho_l(3)*l_l(3)
C4 = l_l(4)/(rho_l(4)*c_l(4)^2)
M5 = rho_l(5)*l_l(5)
Rout = rho0*c0
%%
% Each element is a two-port (ABCD) matrix, and a chain is just their product:
%
% $$\text{series } Z: \begin{pmatrix}1 & Z\\ 0 & 1\end{pmatrix}, \qquad \text{shunt } Y: \begin{pmatrix}1 & 0\\ Y & 1\end{pmatrix}, \qquad \frac{p_{out}}{p_{in}} = \frac{1}{A + B/R_{out}}$$
%
% The last formula is the transmission the slides plot: output pressure over
% the (ideal) source pressure.
%
% *Transfer matrix of a layer (slide 3, the "2-port").* A uniform layer is a
% lossless transmission line with $Z_0 = \rho c$, $k = \omega/c$:
%
% $$T_i = \begin{pmatrix}\cos k l & jZ_0\sin kl\\ \dfrac{j\sin kl}{Z_0} & \cos kl\end{pmatrix}$$
%
% (In LTspice that is the T element with $T_d = l/c$, $Z_0 = \rho c$, as on slide 6.)
ser = @(Z) [1 Z; 0 1];
shu = @(Y) [1 0; Y 1];
tml = @(w, i) [cos(w*l_l(i)/c_l(i)), 1j*rho_l(i)*c_l(i)*sin(w*l_l(i)/c_l(i)); 1j*sin(w*l_l(i)/c_l(i))/(rho_l(i)*c_l(i)), cos(w*l_l(i)/c_l(i))];
tr = @(T) 1/(T(1,1) + T(1,2)/Rout);
%%
% The three models of slides 5-6, as functions of omega:
LEM   = @(w) tr(ser(1j*w*M1)*shu(1j*w*C2)*ser(1j*w*M3)*shu(1j*w*C4)*ser(1j*w*M5));
MIXED = @(w) tr(ser(1j*w*M1)*tml(w,2)*ser(1j*w*M3)*tml(w,4)*ser(1j*w*M5));
TMM   = @(w) tr(tml(w,1)*tml(w,2)*tml(w,3)*tml(w,4)*tml(w,5));
%%
% Sweep 20 Hz - 20 kHz with 10000 points per decade, as slide 5 does
% (it reports < 0.1 s for the lumped model).
f = logspace(log10(20), log10(20e3), 30001);
w = 2*pi*f;
tic, H_LEM = arrayfun(LEM, w); t_LEM = toc
H_MIX = arrayfun(MIXED, w);
H_TMM = arrayfun(TMM, w);
dB = @(H) 20*log10(abs(H));
%%
% *Check 1: mass law at 20 Hz.* Far below every resonance the wall is one
% mass $m'' = \sum \rho_i l_i$ (the lumped model leaves out the insulation and
% air masses, 117 instead of 123 kg/m^2, hence its 0.5 dB offset), so $\frac{p_{out}}{p_{in}} \approx \frac{\rho_0 c_0}{j\omega m''}$
% (slide: about -30 dB at 20 Hz in all models)
m_total = sum(rho_l.*l_l)
massLaw_dB_20Hz = 20*log10(Rout/(2*pi*20*m_total))
LEM_dB_20Hz = dB(H_LEM(1))
TMM_dB_20Hz = dB(H_TMM(1))
%%
% *Check 2: the two lumped resonances.* Each soft layer is a spring between
% the masses on either side (mass-spring-mass):
% $f = \frac{1}{2\pi}\sqrt{\frac{1}{C}\left(\frac{1}{m_a} + \frac{1}{m_b}\right)}$.
% Air gap between (drywall + brick) and wood (slide: the peak just below 200 Hz):
f_airgap = 1/(2*pi)*sqrt(1/C4*(1/(M1 + M3) + 1/M5))
%%
% Insulation between drywall and (brick + wood) (slide: the sharp peak at about 2.5 kHz):
f_insul = 1/(2*pi)*sqrt(1/C2*(1/M1 + 1/(M3 + M5)))
%%
% The peaks the three models actually produce:
[~, iL] = findpeaks(dB(H_LEM), 'MinPeakProminence', 6);
[~, iM] = findpeaks(dB(H_MIX), 'MinPeakProminence', 6);
[~, iT] = findpeaks(dB(H_TMM), 'MinPeakProminence', 6);
peaks_LEM_Hz = f(iL)
peaks_MIXED_Hz = f(iM)
peaks_TMM_Hz = f(iT)
%%
% *Check 3: where the lumped model must fail.* The extra TMM peaks are
% thickness resonances: standing waves across a layer, at
% $f_n = \frac{n c_i}{2 l_i}$. For the insulation (slide: peaks near 8-9 kHz
% and 17 kHz that only the distributed models show):
f_insul_halfwave = (1:2)*c_l(2)/(2*l_l(2))
%%
% The lumped picture needs $l \ll \lambda$. At the insulation resonance
% the insulation is already a sizeable fraction of a wavelength:
l_over_lambda_insul = l_l(2)/(c_l(2)/f_insul)
%%
% That is also why the LEM insulation peak sits about 12 % too high: the
% lumped spring has no mass, but the insulation weighs as much as the
% drywall ($\rho_2 l_2$ = 6 kg/m^2). The classic fix for a spring with its
% own mass: add a third of it to the mass it drives.
m_insul = rho_l(2)*l_l(2)
f_insul_corrected = 1/(2*pi)*sqrt(1/C2*(1/(M1 + m_insul/3) + 1/(M3 + M5)))
%%
% The stiff layers can stay lumped masses even though the brick is not
% small compared with the wavelength at 20 kHz (0.28 lambda). What matters
% is the layer's own first thickness resonance, $c_i/(2l_i)$, which for the
% drywall, brick and wood lies far above the band:
f_first_solids_kHz = c_l([1 3 5])./(2*l_l([1 3 5]))/1e3
%%
% So only the soft insulation (and the air gap, harmlessly) needs a
% transmission line. That is exactly why the *mixed* model of slide 6
% (masses lumped, insulation and air as lines) gives the full-TMM peaks.
% Differences in dB below 2 kHz (above that a few hertz of peak shift
% gives huge but meaningless dB differences on the needle-sharp peaks):
maxdiff_MIX_TMM_below2k_dB = max(abs(dB(H_MIX(f < 2e3)) - dB(H_TMM(f < 2e3))))
maxdiff_LEM_TMM_below1k_dB = max(abs(dB(H_LEM(f < 1e3)) - dB(H_TMM(f < 1e3))))
%%
figure
semilogx(f, dB(H_LEM), f, dB(H_MIX), '--', f, dB(H_TMM), ':', 'LineWidth', 1.2)
grid on, ylim([-200 0]), xlabel('f [Hz]'), ylabel('Transmission p_{out}/p_{in} [dB]')
legend('LEM (slide 5)', 'LEM + TMM (slide 6 top)', 'full TMM (slide 6 bottom)', 'Location', 'southwest')
title('Five-layer wall: drywall | insulation | brick | air | wood')

%% 3 - Metamaterials in 1-D (slide 18)
% *(a) Mass-spring line (Bragg scattering).* Masses m spaced l, tension T:
%
% $$\ddot y_n = \omega_0^2(y_{n+1} - 2y_n + y_{n-1}), \quad \omega_0^2 = \frac{T}{ml}
% \;\Rightarrow\; \omega(k) = 2\omega_0\left|\sin\frac{kl}{2}\right|$$
%
% Phase and group velocity:
% $c(k) = \frac{\omega}{k} = \frac{2\omega_0}{k}\sin\frac{kl}{2}$, $\quad c_g(k) = \frac{\partial\omega}{\partial k} = \omega_0 l\cos\frac{kl}{2}$
%
% At the zone edge $kl = \pi$ the frequency tops out at $2\omega_0$ and the
% group velocity is zero: a standing wave, nothing travels. Above $2\omega_0$
% there is no real k at all: a stop band. In units of $\omega_0$ and l:
kl = linspace(0, 4*pi, 801);
w_bragg = 2*abs(sin(kl/2));
w_max = max(w_bragg)
cg_at_edge = cos(pi/2)
%%
% *(b) Local resonators.* Each main mass m (spring k) carries a resonator
% $m_R$ on a spring $k_R$:
%
% $$0 = 2(1 - \cos kd) - \left(\frac{\omega}{\omega_0}\right)^2\left(1 + \frac{m_R/m}{1 - \omega^2/\omega_R^2}\right), \qquad \omega_0^2 = \frac{k}{m}, \;\omega_R^2 = \frac{k_R}{m_R}$$
%
% With $a = 2(1-\cos kd)$, $\mu = m_R/m$ and $W = (\omega/\omega_0)^2$,
% $\Omega_R = \omega_R/\omega_0$, multiplying out gives a quadratic in W:
%
% $$\frac{W^2}{\Omega_R^2} - W\left(1 + \mu + \frac{a}{\Omega_R^2}\right) + a = 0$$
%
% The slide gives no numbers, so this uses an illustrative resonator:
% $\mu = 1$, $\Omega_R = 0.5$.
mu = 1; OmR = 0.5;
a = 2*(1 - cos(kl));
p = 1 + mu + a/OmR^2;
W_low  = (p - sqrt(p.^2 - 4*a/OmR^2))*OmR^2/2;
W_high = (p + sqrt(p.^2 - 4*a/OmR^2))*OmR^2/2;
%%
% Gap edges: the acoustic (lower) branch peaks at $kd = \pi$, the optical
% (upper) branch starts at k = 0 where $W = (1+\mu)\Omega_R^2$:
gap_lower = sqrt(max(W_low))
gap_upper = OmR*sqrt(1 + mu)
%%
% The gap opens *around the resonator frequency* $\omega_R$, far below the
% Bragg limit $2\omega_0$: that is the point of local resonance, sub-wavelength
% stop bands. A heavier resonator (bigger mu) widens the gap.
figure
subplot(1,2,1), plot(kl/pi, w_bragg), grid on, xlabel('kl/\pi'), ylabel('\omega/\omega_0'), title('Mass-spring line')
subplot(1,2,2), plot(kl/pi, sqrt(W_low), kl/pi, sqrt(W_high)), grid on, xlabel('kd/\pi'), ylabel('\omega/\omega_0')
yline(gap_lower, ':'), yline(gap_upper, ':'), title('With local resonators (\mu = 1, \omega_R = 0.5\omega_0)')
