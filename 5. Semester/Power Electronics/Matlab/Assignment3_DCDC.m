%% Assignment 3 - DC-DC converters, worked
% 62755 Power Electronics | lecture of Monday 26 October 2026 (DC converters)
%
% How to read this: every step first states the formula (from the deck
% DCConverters.pdf, slide numbers in brackets), then the MATLAB line is that
% same formula typed in, and the result appears right below it.
% The problems are Rashid's chapter 5 examples. Where the assignment changed a
% number (3.2 has E = 0 V), the book's answers will not match: compare with
% your own working, not the book.
%
% Two places where the deck's formula is wrong are marked *SLIDE ERROR*: the
% critical inductance of the boost (slide 32) and buck-boost (slide 36) drops
% a factor (1-k). Both values are printed so you can see the difference.

%% 3.1 - Step-down converter, resistive load, switch drop 2 V
% Vs = 220 V, R = 10 ohm, v_ch = 2 V, f = 1 kHz, k = 0.5. The switch drop
% simply lowers the voltage the load sees during the on-time to Vs - v_ch.
Vs = 220; R = 10; vch = 2; f = 1e3; k = 0.5;
%%
% (a) Average output voltage [slide 5]: $V_a = k(V_s - v_{ch})$
Va = k*(Vs - vch)
%%
% (b) RMS output voltage [slide 6]: $V_o = \sqrt{k}\,(V_s - v_{ch})$
Vo = sqrt(k)*(Vs - vch)
%%
% (c) Efficiency: output power over input power.
% $P_o = k (V_s-v_{ch})^2/R$, $\;P_i = k V_s (V_s - v_{ch})/R$, $\;\eta = P_o/P_i$
Po = k*(Vs - vch)^2/R
Pi = k*Vs*(Vs - vch)/R
eta = Po/Pi
%%
% (d) Effective input resistance [slide 6]: $R_i = V_s/I_a$. With a resistive
% load the load current is zero during the off-time, so the average load
% current $I_a = V_a/R$ is also the average input current ($R_i \approx R/k$)
Ia = Va/R
Ri = Vs/Ia
%%
% (e) Ripple factor of the output voltage: $RF = \sqrt{(V_o/V_a)^2 - 1}$
% (for a pure pulse train this is $\sqrt{1/k - 1}$, so 100 % at k = 0.5)
RF = sqrt((Vo/Va)^2 - 1)
%%
% (f) RMS of the fundamental of the output [Fourier series, slide 46 with
% $I_a \to V_s - v_{ch}$]: the n-th harmonic has peak amplitude
% $\frac{V}{n\pi}\sqrt{\sin^2 2n\pi k + (1-\cos 2n\pi k)^2} = \frac{2V}{n\pi}|\sin n\pi k|$
V1_peak = 2*(Vs - vch)/pi*abs(sin(pi*k))
V1_rms = V1_peak/sqrt(2)

%% 3.2 - Step-down converter, RL load, E = 0 V
% Vs = 220 V, R = 5 ohm, L = 7.5 mH, f = 1 kHz, k = 0.5, E = 0 V.
% (Rashid example 5.2 has E = 5 V. The course script assignment52.m uses E = 0
% too, so the change is intended.)
Vs = 220; R = 5; L = 7.5e-3; f = 1e3; k = 0.5; E = 0;
T = 1/f
z = T*R/L
%%
% (a) Minimum current [slide 12]: $I_1 = \frac{V_s}{R}\frac{e^{kz}-1}{e^{z}-1} - \frac{E}{R}$
I1 = Vs/R*(exp(k*z) - 1)/(exp(z) - 1) - E/R
%%
% (b) Peak current [slide 12]: $I_2 = \frac{V_s}{R}\frac{e^{-kz}-1}{e^{-z}-1} - \frac{E}{R}$
I2 = Vs/R*(exp(-k*z) - 1)/(exp(-z) - 1) - E/R
%%
% (c) Ripple [slide 12]: $\Delta I = I_2 - I_1$. At k = 0.5 this *is* the maximum
% ripple; compare the approximation $\Delta I_{max} \approx V_s/(4fL)$
dI = I2 - I1
dI_max_approx = Vs/(4*f*L)
%%
% (d) Average load current: $I_a = (kV_s - E)/R$
Ia = (k*Vs - E)/R
%%
% (e) RMS load current, exactly, from the two exponential pieces [slides 10-11]:
%
% $i_1(t) = I_1 e^{-tR/L} + \frac{V_s - E}{R}(1-e^{-tR/L})$ for $0 \le t \le kT$
%
% $i_2(t) = I_2 e^{-tR/L} - \frac{E}{R}(1-e^{-tR/L})$ for $0 \le t \le (1-k)T$
i1 = @(t) I1*exp(-t*R/L) + (Vs - E)/R*(1 - exp(-t*R/L));
i2 = @(t) I2*exp(-t*R/L) - E/R*(1 - exp(-t*R/L));
Io = sqrt((integral(@(t) i1(t).^2, 0, k*T) + integral(@(t) i2(t).^2, 0, (1-k)*T))/T)
%%
% Check with the triangle approximation $I_o \approx \sqrt{I_a^2 + (\Delta I/2\sqrt3)^2}$
Io_approx = sqrt(Ia^2 + (dI/(2*sqrt(3)))^2)
%%
% (f) Effective input resistance: $R_i = V_s/I_s$, $I_s$ = average of $i_1$ over the period
Is = integral(i1, 0, k*T)/T
Ri = Vs/Is
%%
% (g) RMS chopper (switch) current: $I_R = \sqrt{\frac1T\int_0^{kT} i_1^2\,dt}$ ($\approx \sqrt{k}\,I_o$)
IR = sqrt(integral(@(t) i1(t).^2, 0, k*T)/T)
%%
% (h) Critical inductance [slide 13]. The current is continuous while
% $x = E/V_s \le \frac{e^{kz}-1}{e^{z}-1}$. With E = 0 the left side is 0 and
% the right side is positive for every L, so *the current is continuous for
% any L > 0: there is no critical inductance*. (With the book's E = 5 V you
% would solve the equality for z and get L from z = TR/L.)
x = E/Vs
x_limit = (exp(k*z) - 1)/(exp(z) - 1)
%%
% The book-style answer for E = 5 V, to show what (h) is after:
% solve $\frac{e^{kz}-1}{e^{z}-1} = 5/220$ for z, then $L = TR/z$
z_crit_E5 = fzero(@(zz) (exp(k*zz) - 1)/(exp(zz) - 1) - 5/220, [0.5 50]);
L_crit_E5 = T*R/z_crit_E5
%%
% Plots: load current, supply (switch) current and freewheeling-diode current
% over three periods. During kT the switch carries the load current, after it
% the diode does.
t = linspace(0, 3*T, 3000);
tau = mod(t, T);
on = tau < k*T;
iLoad = on.*i1(tau) + ~on.*i2(tau - k*T);
iSupply = on.*iLoad;
iDiode = ~on.*iLoad;
figure
subplot(3,1,1), plot(t*1e3, iLoad), grid on, ylabel('i_{load} [A]'), title('3.2 Buck, RL load, E = 0')
subplot(3,1,2), plot(t*1e3, iSupply), grid on, ylabel('i_{supply} [A]')
subplot(3,1,3), plot(t*1e3, iDiode), grid on, ylabel('i_{diode} [A]'), xlabel('t [ms]')

%% 3.3 - Inductance for a 10 % ripple
% R = 0.25 ohm, Vs = 550 V, E = 0, Ia = 200 A, f = 250 Hz. "Use the average
% output voltage": $V_a = I_a R = kV_s$ gives k.
Vs = 550; R = 0.25; E = 0; Ia = 200; f = 250; T = 1/f;
Va = Ia*R
k = Va/Vs
dI_spec = 0.10*Ia
%%
% Linear (L/R >> T) approximation: during the on-time the inductor sees
% $V_s - V_a$, so $\Delta I = \frac{(V_s - V_a)kT}{L}$ $\Rightarrow$ $L = \frac{(V_s-V_a)k}{f\,\Delta I}$
L = (Vs - Va)*k/(f*dI_spec)
%%
% Exact check with the ripple formula of slide 12,
% $\Delta I = \frac{V_s}{R}\frac{1-e^{-kz}+e^{-z}-e^{-(1-k)z}}{1-e^{-z}}$, solved for L:
dIexact = @(LL) Vs/R*(1 - exp(-k*T*R/LL) + exp(-T*R/LL) - exp(-(1-k)*T*R/LL))/(1 - exp(-T*R/LL));
L_exact = fzero(@(LL) dIexact(LL) - dI_spec, [1e-3 50e-3])
%%
% *The book's reading (Rashid example 5.3, same wording): "maximum" ripple
% means the worst case over k.* With $\Delta I = \frac{V_s(1-k)kT}{L}$,
% $d(\Delta I)/dk = 0$ gives k = 0.5, so $L = \frac{V_s \cdot 0.5 \cdot 0.5}{f\,\Delta I}$.
% This is the answer the book prints (27.5 mH), and it is the safe design:
% the ripple stays below 10 % of 200 A for every duty cycle.
k_worst = 0.5;
L_worst = Vs*(1 - k_worst)*k_worst/(f*dI_spec)
%%
% Exact worst-case check [slide 12]: $\Delta I_{max} = \frac{V_s}{R}\tanh\frac{R}{4fL}$ solved for L
L_worst_exact = R/(4*f*atanh(dI_spec*R/Vs))

%% 3.4 - Step-up converter, resistive load
% Vs = 10 V, f = 1 kHz, R = 5 ohm, L = 6.5 mH, E = 0, k = 0.5. Mode 1: switch
% closed, L across Vs. Mode 2: L in series with R and E through the diode.
Vs = 10; f = 1e3; R = 5; L = 6.5e-3; E = 0; k = 0.5;
T = 1/f;
z = T*R/L
%%
% [slide 17]: $I_1 = \frac{V_s k z}{R}\frac{e^{-(1-k)z}}{1-e^{-(1-k)z}} + \frac{V_s - E}{R}$,
% $\quad I_2 = \frac{V_s k z}{R}\frac{1}{1-e^{-(1-k)z}} + \frac{V_s - E}{R}$
I1 = Vs*k*z/R*exp(-(1-k)*z)/(1 - exp(-(1-k)*z)) + (Vs - E)/R
I2 = Vs*k*z/R*1/(1 - exp(-(1-k)*z)) + (Vs - E)/R
%%
% Ripple: $\Delta I = I_2 - I_1 = \frac{V_s}{L}kT$
dI = I2 - I1
dI_check = Vs/L*k*T
%%
% Plot: inductor (= load during mode 2), switch and diode currents.
% Mode 1: $i = I_1 + \frac{V_s}{L}t$; mode 2: $i = I_2 e^{-tR/L} + \frac{V_s-E}{R}(1-e^{-tR/L})$
t = linspace(0, 3*T, 3000);
tau = mod(t, T);
on = tau < k*T;
iL = on.*(I1 + Vs/L*tau) + ~on.*(I2*exp(-(tau - k*T)*R/L) + (Vs - E)/R*(1 - exp(-(tau - k*T)*R/L)));
figure
subplot(3,1,1), plot(t*1e3, iL), grid on, ylabel('i_L [A]'), title('3.4 Boost, resistive load')
subplot(3,1,2), plot(t*1e3, on.*iL), grid on, ylabel('i_{switch} [A]')
subplot(3,1,3), plot(t*1e3, ~on.*iL), grid on, ylabel('i_{diode} = i_{load} [A]'), xlabel('t [ms]')

%% 3.5 - Buck regulator design
% Vs = 12 V, Va = 5 V, R = 500 ohm, dVc = 20 mV, f = 25 kHz, dI = 0.8 A.
Vs = 12; Va = 5; R = 500; dVc = 20e-3; f = 25e3; dI = 0.8;
%%
% (a) [slide 28]: $k = V_a/V_s$
k = Va/Vs
%%
% (b) [slide 28]: $\Delta I = \frac{V_a(V_s-V_a)}{fLV_s}$ $\Rightarrow$ $L = \frac{V_a(V_s-V_a)}{f\,\Delta I\,V_s}$
L = Va*(Vs - Va)/(f*dI*Vs)
%%
% (c) [slide 29]: $\Delta V_c = \frac{\Delta I}{8fC}$ $\Rightarrow$ $C = \frac{\Delta I}{8f\Delta V_c}$
C = dI/(8*f*dVc)
%%
% (d) [slide 29]: $L_c = \frac{(1-k)R}{2f}$, $\quad C_c = \frac{1-k}{16 L f^2}$ (with the L from (b))
Lc = (1-k)*R/(2*f)
Cc = (1-k)/(16*L*f^2)

%% 3.6 - Boost regulator
% Vs = 5 V, Va = 15 V, Ia = 0.5 A, f = 25 kHz, L = 150 uH, C = 220 uF.
Vs = 5; Va = 15; Ia = 0.5; f = 25e3; L = 150e-6; C = 220e-6;
R = Va/Ia
%%
% (a) [slide 31]: $V_a = \frac{V_s}{1-k}$ $\Rightarrow$ $k = 1 - V_s/V_a$
k = 1 - Vs/Va
%%
% (b) [slide 32]: $\Delta I = \frac{V_s k}{fL}$
dI = Vs*k/(f*L)
%%
% (c) Peak inductor current: average $I_s = \frac{I_a}{1-k}$ plus half the ripple
Is = Ia/(1 - k)
I2 = Is + dI/2
%%
% (d) [slide 32]: $\Delta V_c = \frac{I_a k}{fC}$
dVc = Ia*k/(f*C)
%%
% (e) Critical values. Set $\Delta I = 2I_L = 2I_s$ with $I_s = \frac{V_s}{(1-k)^2R}$:
% $\frac{kV_s}{fL} = \frac{2V_s}{(1-k)^2R}$ $\Rightarrow$ $L_c = \frac{k(1-k)^2R}{2f}$.
% *SLIDE ERROR*: slide 32 prints $L_c = k(1-k)R/(2f)$, one factor (1-k) short
% of its own previous line.
Lc = k*(1 - k)^2*R/(2*f)
Lc_slide = k*(1 - k)*R/(2*f)
%%
% Capacitor [slide 32]: $\Delta V_c = 2V_a$ $\Rightarrow$ $C_c = \frac{k}{2fR}$
Cc = k/(2*f*R)

%% 3.7 - Buck-boost regulator
% Vs = 12 V, k = 0.25, f = 25 kHz, L = 150 uH, C = 220 uF, Ia = 1.25 A.
Vs = 12; k = 0.25; f = 25e3; L = 150e-6; C = 220e-6; Ia = 1.25;
%%
% (a) [slide 34]: $V_a = -\frac{V_s k}{1-k}$
Va = -Vs*k/(1 - k)
R = abs(Va)/Ia
%%
% (b) [slide 35]: $\Delta V_c = \frac{I_a k}{fC}$
dVc = Ia*k/(f*C)
%%
% (c) [slide 35]: $\Delta I = \frac{V_s k}{fL}$
dI = Vs*k/(f*L)
%%
% (d) Peak transistor current = peak inductor current. [slide 35]:
% $I_L = I_s + I_a = \frac{I_a}{1-k}$, then $I_p = I_L + \Delta I/2$
IL = Ia/(1 - k)
Ip = IL + dI/2
%%
% (e) Critical values. $\Delta I = 2I_L$ with $I_L = \frac{I_a}{1-k} = \frac{kV_s}{(1-k)^2R}$:
% $\frac{kV_s}{fL} = \frac{2kV_s}{(1-k)^2R}$ $\Rightarrow$ $L_c = \frac{(1-k)^2R}{2f}$.
% *SLIDE ERROR*: slide 36 writes $2I_L = \frac{2kV_s}{(1-k)R}$ and so
% $L_c = \frac{(1-k)R}{2f}$, again one factor (1-k) short.
Lc = (1 - k)^2*R/(2*f)
Lc_slide = (1 - k)*R/(2*f)
%%
% Capacitor [slide 36]: $\Delta V_c = 2|V_a|$ $\Rightarrow$ $C_c = \frac{k}{2fR}$
Cc = k/(2*f*R)

%% 3.8 - Buck converter with filter Le-Ce and an R-L load
% Vs = 110 V, Va = 60 V, Ia = 20 A, f = 20 kHz. Ripple (peak-to-peak): load
% voltage 2.5 %, load current 5 %, filter-inductor Le current 10 %.
Vs = 110; Va = 60; Ia = 20; f = 20e3;
k = Va/Vs
R = Va/Ia
dVc = 0.025*Va
dIo = 0.05*Ia
dILe = 0.10*Ia
%%
% (a) Le from the buck ripple formula [slide 28]: $L_e = \frac{V_a(V_s-V_a)}{f\,\Delta I_{Le}\,V_s}$
Le = Va*(Vs - Va)/(f*dILe*Vs)
%%
% Ce from [slide 29]: $C_e = \frac{\Delta I_{Le}}{8f\Delta V_c}$
Ce = dILe/(8*f*dVc)
%%
% Load inductance L. The load (R + L in series) sits across Ce, so its ripple
% current is the capacitor ripple voltage divided by the load impedance at the
% switching frequency: $\Delta I_o = \frac{\Delta V_c}{\sqrt{R^2 + (2\pi f L)^2}}$.
% Even with L = 0 this gives $\Delta V_c/R$:
dIo_with_L0 = dVc/R
%%
% *Note*: that is 0.5 A = 2.5 % of Ia, already inside the 5 % spec, so the
% equation has no positive solution for L: **any L >= 0 meets the spec**. If
% the group needs a number, state this and pick a small L (the plot below uses
% L = 0.5 mH, which brings the load ripple down to about 24 mA). Ask Ashraf
% which reading of "5 % load current" he intends.
L = 0.5e-3
dIo_with_L = dVc/sqrt(R^2 + (2*pi*f*L)^2)
%%
% (b) Verify with a switching simulation: state x = [i_Le; v_c; i_o].
% $L_e\,di_{Le}/dt = s(t)V_s - v_c$ (the diode clamps the switch node at 0
% while $i_{Le} > 0$), $C_e\,dv_c/dt = i_{Le} - i_o$, $L\,di_o/dt = v_c - R i_o$.
T = 1/f;
s = @(t) double(mod(t, T) < k*T);
rhs = @(t, x) [(s(t)*Vs - x(2))/Le; (x(1) - x(3))/Ce; (x(2) - R*x(3))/L];
opts = odeset('MaxStep', T/200, 'RelTol', 1e-7, 'AbsTol', 1e-9);
[tt, xx] = ode45(rhs, [0 200*T], [Ia; Va; Ia], opts);
last = tt > 190*T;
dILe_sim = max(xx(last,1)) - min(xx(last,1))
dVc_sim = max(xx(last,2)) - min(xx(last,2))
Va_sim = mean(xx(last,2))
dIo_sim = max(xx(last,3)) - min(xx(last,3))
figure
subplot(2,1,1), plot(tt(last)*1e3, xx(last,2)), grid on, ylabel('v_c [V]'), title('3.8 Buck with L_e-C_e filter')
subplot(2,1,2), plot(tt(last)*1e3, xx(last,3)), grid on, ylabel('i_L (load) [A]'), xlabel('t [ms]')
%%
% (c) Fourier coefficients of the input (chopper) current, a pulse train of
% height Ia and width kT [slide 46]:
%
% $i_h(t) = kI_a + \sum_n \frac{I_a}{n\pi}\left[\sin 2n\pi k\,\cos 2n\pi ft + (1-\cos 2n\pi k)\sin 2n\pi ft\right]$
%
% so the n-th harmonic has peak $\frac{2I_a}{n\pi}|\sin n\pi k|$.
n = (1:7)';
I_dc = k*Ia
In_peak = 2*Ia./(n*pi).*abs(sin(n*pi*k));
In_rms = In_peak/sqrt(2);
table(n, n*f/1e3, In_peak, In_rms, 'VariableNames', {'n', 'f_kHz', 'peak_A', 'rms_A'})
