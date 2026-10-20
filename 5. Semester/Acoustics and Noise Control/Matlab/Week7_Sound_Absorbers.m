%% Lecture 7 - Sound absorbers and room acoustic design
% 34840 Fundamentals of Acoustics and Noise Control | 20 October 2026
%
% Worked learning document for 34840_Problems_soundabsorbers7.pdf. Every
% formula is first written as an equation, then calculated in one plain
% MATLAB line. Lines without a semicolon print their result.
%
% No official solutions yet: the answers are my own, DERIVED, NOT YET
% CHECKED AGAINST OFFICIAL SOLUTIONS. The sheet prints final answers, and
% they are written in the comments next to each result.
%
% Constants: rho = 1.2 kg/m^3, c = 344 m/s. Sabine: T = 0.16 V / A.

%% Constants
% $$\rho c^2 \approx 1.4\cdot10^5\ \mathrm{Pa}$$
rho = 1.2;            % air density [kg/m^3]
c = 344;              % speed of sound [m/s]
rho_c = rho*c         % characteristic impedance [Pa s/m]
rho_c2 = rho*c^2      % air "stiffness" [Pa] (slide 20 uses 1.4e5)

%% Problem 1.1 - Absorption coefficient from the reverberation room (ISO 354)
% 200 m^3 chamber, 10 m^2 sample. T = 5.2 s empty, 3.0 s with the sample.
%
% $$A = \frac{0.16\,V}{T}$$
V_ch = 200;                           % chamber volume [m^3]
S_sample = 10;                        % sample area [m^2]
A_empty = 0.16*V_ch/5.2               % 6.15 m^2
A_sample = 0.16*V_ch/3.0              % 10.67 m^2
%
% $$\alpha = \frac{0.16\,V}{S}\left(\frac{1}{T_2}-\frac{1}{T_1}\right)\quad(\alpha_{wall}\ \mathrm{neglected})$$
alpha = (A_sample - A_empty)/S_sample % 0.451 (sheet: 0.45)

%% Problem 1.2 - Area of material for T = 0.8 s with 40 students
% Lecture hall 300 m^3, T = 3.1 s now (furnished, empty).
%
% $$A_{now} = \frac{0.16\,V}{T_{now}},\qquad A_{target} = \frac{0.16\,V}{T_{target}}$$
V_hall = 300;                         % hall volume [m^3]
A_now = 0.16*V_hall/3.1               % 15.48 m^2
A_target = 0.16*V_hall/0.8            % 60.0 m^2
%
% $$A_{students} = n\,A_{person}$$
A_students = 40*0.42                  % 16.8 m^2
%
% $$S = \frac{A_{target}-A_{now}-A_{students}}{\alpha}$$
A_material = A_target - A_now - A_students   % 27.72 m^2
S_needed = A_material/alpha           % 61.4 m^2 -> round up to 62 m^2 (sheet: 62 m^2)
%
% Check: T with 62 m^2 installed should be just under 0.8 s.
T_check = 0.16*V_hall/(A_now + A_students + 62*alpha)   % 0.797 s

%% Problem 2.1 - Plywood membrane absorber
% 20 mm plywood, 600 kg/m^3, 50 mm closed cavity, stiffness neglected.
%
% $$m = \rho_{panel}\,h$$
m = 600*0.020                         % 12 kg/m^2 (mass PER UNIT AREA)
L = 0.050;                            % cavity depth [m]
%
% $$f_r = \frac{1}{2\pi}\sqrt{\frac{\rho c^2}{m L}}$$
f_membrane = 1/(2*pi)*sqrt(rho_c2/(m*L))     % 77.4 Hz (sheet: 77 Hz)
f_membrane_slide = 1/(2*pi)*sqrt(1.4e5/(m*L)) % 76.9 Hz with the slide's constant

%% Problem 2.2 - The same panel perforated: 10 mm holes on a 30 mm grid
% Each hole owns a 30 x 30 mm patch of panel.
%
% $$P = \frac{\pi d^2/4}{a^2}$$
d = 0.010;                            % hole diameter [m]
a = 0.030;                            % hole spacing [m]
P = pi*d^2/4/a^2                      % 0.0873 (8.7 %, slide 28)
%
% $$\delta = 0.8\,d,\qquad l = \text{panel thickness}$$
l = 0.020;                            % neck length = panel thickness [m]
delta = 0.8*d                         % 8 mm end correction
%
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{P}{L\,(l+\delta)}}$$
f_perf = c/(2*pi)*sqrt(P/(L*(l+delta)))      % 432 Hz (sheet: 432 Hz)
%
% Same physics check: the holes act as an air mass per unit area
% $$m_{holes} = \frac{\rho\,(l+\delta)}{P}$$
m_holes = rho*(l+delta)/P             % 0.385 kg/m^2, ~31 x lighter than 12 kg/m^2
f_check = f_membrane*sqrt(m/m_holes)  % 432 Hz again

%% Slide 5 - Reflected SPL for 70 dB incident
% $$L_{refl} = L_{inc} + 10\log_{10}(1-\alpha)$$
L_refl_050 = 70 + 10*log10(1-0.50)    % 67.0 dB
L_refl_090 = 70 + 10*log10(1-0.90)    % 60.0 dB
L_refl_099 = 70 + 10*log10(1-0.99)    % 50.0 dB

%% Slide 15 - Cotton cloth 7 cm from the wall (lambda/4 rule)
% $$f_{\lambda/4} = \frac{c}{4d},\quad f_{\lambda/2} = \frac{c}{2d}$$
f_peak = c/(4*0.07)                   % 1229 Hz: first maximum
f_dip = c/(2*0.07)                    % 2457 Hz: cloth at a velocity node

%% Slide 25 - Helmholtz resonators in DR Studio 1 (answer hidden on the slide)
% Neck diameter 65 mm, neck length 100 mm (my reading of the drawing).
%
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{s}{V\,(l+\delta)}},\qquad s = \frac{\pi d^2}{4},\ \delta = 0.8\,d$$
s_neck = pi*0.065^2/4                 % 3.32e-3 m^2
l_eff = 0.100 + 0.8*0.065             % 0.152 m
f_DR_small = c/(2*pi)*sqrt(s_neck/(0.15*0.15*0.30*l_eff))   % 98 Hz
f_DR_large = c/(2*pi)*sqrt(s_neck/(0.20*0.20*0.40*l_eff))   % 64 Hz

%% Slide 36 - Absorption coefficient from a surface impedance
% Z_n = 500 + j1000 N s/m^3, slide uses rho c = 414.
Zn = 500 + 1j*1000;
%
% $$R = \frac{Z_n-\rho c}{Z_n+\rho c},\qquad \alpha_n = 1-|R|^2$$
R = (Zn - 414)/(Zn + 414)             % 0.5877 + 0.4511i
alpha_n = 1 - abs(R)^2                % 0.451 (slide: 0.4511)
%
% $$\zeta = Z_n/\rho c = r + jx$$
r = real(Zn/414)                      % 1.208
x = imag(Zn/414)                      % 2.415
%
% $$\alpha_r = \frac{8r}{r^2+x^2}\left[1-\frac{r}{r^2+x^2}\ln\left((r+1)^2+x^2\right)+\frac{r^2-x^2}{x(r^2+x^2)}\tan^{-1}\frac{x}{r+1}\right]$$
alpha_r = 8*r/(r^2+x^2)*(1 - r/(r^2+x^2)*log((r+1)^2+x^2) + (r^2-x^2)/(x*(r^2+x^2))*atan(x/(r+1)))   % 0.53
%
% Same thing from the Paris integral of the oblique-incidence alpha
% $$\alpha_r = \int_0^{\pi/2} \left(1-\left|\frac{\zeta\cos\theta-1}{\zeta\cos\theta+1}\right|^2\right)\sin 2\theta\,d\theta$$
alpha_paris = integral(@(th) (1 - abs((Zn/414*cos(th)-1)./(Zn/414*cos(th)+1)).^2).*sin(2*th), 0, pi/2)   % 0.53

%% Slide 38 - Standing-wave ratio to normal-incidence absorption
% $$\alpha_0 = 1-\left(\frac{n-1}{n+1}\right)^2 = \frac{4}{n+1/n+2}$$
n = 3;                                % P_max/P_min (a pressure ratio, not dB)
alpha_0 = 1 - ((n-1)/(n+1))^2         % 0.75

%% Course text Fig. 4.4.3 - All absorption in the ceiling
% $$T = \frac{0.16\,h}{\alpha}$$
T_3m = 0.16*3/0.8                     % 0.6 s
T_5m = 0.16*5/0.8                     % 1.0 s
