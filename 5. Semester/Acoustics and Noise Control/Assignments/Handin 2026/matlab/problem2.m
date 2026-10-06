%% 34840 hand-in 2026 - Problem 2 (music festival)
% Mads Rudolph, s246132
clear; clc; close all;

c = 343;          % speed of sound in air [m/s]
p_ref = 20e-6;    % reference pressure [Pa]

%% Q2.1 Leq 24h for stage 2
% 6 shows of 1 hour, nothing the rest of the day
T = 24;           % [h]
t = 6;            % [h]
L2 = 60;          % [dB]

Leq2 = 10*log10(t/T*10^(L2/10))

%% Q2.2 Leq 24h for the whole festival
% the stages are incoherent so the energies add
L1 = 58;
L3 = 54;

Leq_total = 10*log10(t/T*(10^(L1/10) + 10^(L2/10) + 10^(L3/10)))

%% Q2.3 subwoofers at 20 Hz
f = 20;
k = 2*pi*f/c
lambda = c/f

% positions [m], origin at the centre of the stage
xL = -10; yL = 0;      % left sub
xR = 10;  yR = 0;      % right sub
xF = 0;   yF = 13;     % front of house
x = [-20 -10 0 10 20]; % audience positions
y = 19;

% each sub gives 80 dB at FOH -> find the source strength A (p = A/r)
rF = sqrt((xF-xL)^2 + (yF-yL)^2)
pF = p_ref*10^(80/20)
A = pF*rF

% distances to the audience positions
rL = sqrt((x-xL).^2 + (y-yL)^2)
rR = sqrt((x-xR).^2 + (y-yR)^2)

% level from each sub on its own
L_left = 80 + 20*log10(rF./rL)
L_right = 80 + 20*log10(rF./rR)

% path difference and phase difference
dr = abs(rL - rR)
dphi = k*dr*180/pi       % [deg]

% same signal in both subs -> add the complex pressures
p = A*exp(-1j*k*rL)./rL + A*exp(-1j*k*rR)./rR;
Lp = 20*log10(abs(p)/p_ref)

% without interference (energy sum) for comparison
Lp_energy = 10*log10(10.^(L_left/10) + 10.^(L_right/10))

%% plot along the audience line
xx = -30:0.1:30;
r1 = sqrt((xx-xL).^2 + y^2);
r2 = sqrt((xx-xR).^2 + y^2);
Lline = 20*log10(abs(A*exp(-1j*k*r1)./r1 + A*exp(-1j*k*r2)./r2)/p_ref);
Lline_energy = 20*log10(sqrt((A./r1).^2 + (A./r2).^2)/p_ref);

figure; theme(gcf, 'light');
plot(xx, Lline, 'LineWidth', 1.5); hold on
plot(xx, Lline_energy, '--');
plot(x, Lp, 'ko', 'MarkerFaceColor', 'k');
grid on; ylim([55 90]);
xlabel('x [m] (y = 19 m)'); ylabel('SPL [dB]');
legend('Coherent sum', 'Energy sum', 'Audience positions', 'Location', 'south');
exportgraphics(gcf, '../figures/spl_audience_line.pdf');

%% map of the sound field in front of the stage
[X, Y] = meshgrid(-30:0.25:30, 0.5:0.25:30);
R1 = sqrt((X-xL).^2 + (Y-yL).^2);
R2 = sqrt((X-xR).^2 + (Y-yR).^2);
Lmap = 20*log10(abs(A*exp(-1j*k*R1)./R1 + A*exp(-1j*k*R2)./R2)/p_ref);

figure; theme(gcf, 'light');
imagesc(X(1,:), Y(:,1), Lmap); axis xy equal tight; hold on
clim([60 95]); colorbar;
plot([xL xR], [yL yR], 'ks', 'MarkerFaceColor', 'k');
plot(xF, yF, 'k^', 'MarkerFaceColor', 'w');
plot(x, y*ones(1,5), 'ko', 'MarkerFaceColor', 'w');
xlabel('x [m]'); ylabel('y [m]'); title('SPL [dB] at 20 Hz');
exportgraphics(gcf, '../figures/spl_map.pdf', 'Resolution', 200);
