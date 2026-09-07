%% 34840 - Week 2: Reflection and spherical waves (8 September 2026)
% Student starter. Replace NaN placeholders with your own expressions.
% Run this setup first, then solve using Run Section (Ctrl+Enter).
% Sections deliberately leave the calculations to you; no Symbolic Toolbox needed.
% Source: Obsidian course folder / Exercises / 34840_Problems2.pdf
% Phasors: exp(1i*omega*t); pressure/velocity values are PEAK amplitudes.
clear; clc; close all;
c_air = 343;            % m/s, assumed room-temperature air
rho_air = 1.204;        % kg/m^3, gives rho*c = 412.972 Pa*s/m
c_water = 1480;         % m/s, given
rho_water = 1000;       % kg/m^3, assumed (not specified on sheet)
c_helium = 1000;        % m/s, given
show_reference_answers = false; % Set true AFTER attempting the problems.

%% Problem 1 - Pressure nodes measured from a rigid termination
% Given: f = 1 kHz. Find the first three distances of very low pressure.
% Derive the node condition from cos(k*d) = 0 in your notes.
f1 = 1000;             % Hz
n1 = 0:2;              % node indices
lambda1 = NaN;         % TODO: wavelength [m]
k1 = NaN;              % TODO: wavenumber [rad/m]
d_nodes = NaN(size(n1)); % TODO: node distances [m]
d = linspace(0, 0.6, 1201); % distance FROM the wall [m]
p_normalized = NaN(size(d)); % TODO: |P|/|Pi| as a function of d
if all(isfinite(d_nodes)) && all(isfinite(p_normalized))
    disp(table(n1(:), d_nodes(:), 100*d_nodes(:), ...
        'VariableNames', {'NodeIndex','Distance_m','Distance_cm'}));
    figure('Name','Problem 1'); plot(100*d,p_normalized,'LineWidth',1.5);
    hold on; plot(100*d_nodes,zeros(size(d_nodes)),'ro'); grid on;
    xlabel('Distance from rigid wall [cm]'); ylabel('|P| / |P_i|');
    title('Pressure envelope and predicted nodes');
else
    fprintf('P1: fill wavelength, wavenumber, nodes and pressure envelope.\n');
end

%% Problem 2 - Same instrument geometry, different sound speed
% Derive the frequency ratio: the resonance wavelength is fixed by geometry.
frequency_ratio = NaN;  % TODO: f_helium/f_air (dimensionless)
octave_shift = NaN;     % TODO optional: log2 of the frequency ratio
if isfinite(frequency_ratio)
    fprintf('P2: frequency factor %.4f; octave shift %.4f\n', ...
        frequency_ratio, octave_shift);
else
    fprintf('P2: fill the resonance frequency ratio.\n');
end

%% Problem 3 - Air/water interface, plane waves at normal incidence
% 3.1: incidence from air. 3.2: incidence from water.
% Start from Pi+Pr=Pt and (Pi-Pr)/Z1=Pt/Z2.
Z_air = NaN;           % TODO: characteristic impedance [Pa*s/m]
Z_water = NaN;         % TODO: characteristic impedance [Pa*s/m]
R_air_water = NaN;     % TODO 3.1: pressure reflection coefficient
R_water_air = NaN;     % TODO 3.2: pressure reflection coefficient
Tp_air_water = NaN;    % TODO: transmitted / incident pressure
Tp_water_air = NaN;    % TODO: transmitted / incident pressure
atten_air_water = NaN; % TODO 3.3: incident / transmitted pressure
atten_water_air = NaN; % TODO 3.3: incident / transmitted pressure
% Optional physical check: transmitted intensity fraction, NOT pressure ratio.
tau_air_water = NaN;   % TODO: (Z_air/Z_water)*abs(Tp_air_water)^2
tau_water_air = NaN;   % TODO: (Z_water/Z_air)*abs(Tp_water_air)^2
if all(isfinite([R_air_water,R_water_air,atten_air_water,atten_water_air]))
    Direction = {'Air to water'; 'Water to air'};
    disp(table(Direction,[R_air_water;R_water_air], ...
        [Tp_air_water;Tp_water_air],[atten_air_water;atten_water_air], ...
        'VariableNames',{'Direction','R_pressure','Pt_over_Pi','Pi_over_Pt'}));
    fprintf('Optional energy balance (each should be 1): %.6f, %.6f\n', ...
        abs(R_air_water)^2+tau_air_water,abs(R_water_air)^2+tau_water_air);
else
    fprintf('P3: fill impedances, reflection and transmission in both directions.\n');
end

%% Problem 4 - Outgoing spherical wave, free field
f4 = 250;             % Hz
r_ref = 1;            % m
P_ref = 0.5;          % Pa peak; choose zero phase at reference position
r_target = 0.10;      % m, outside the assumed small source
omega4 = NaN;         % TODO: angular frequency [rad/s]
k4 = NaN;             % TODO: wavenumber [rad/m]
P_target = NaN;       % TODO 4.1: complex P(r), include relative propagation phase
U_target = NaN;       % TODO 4.2: complex outward velocity, include near-field term
Z_target = NaN;       % TODO 4.3: complex ratio P/U [Pa*s/m]
phase_rad = NaN;      % TODO: angle(Z_target) [rad]
phase_deg = NaN;      % TODO: phase in degrees
if all(isfinite([P_target,U_target,Z_target,phase_rad]))
    fprintf('P4.1: |P| = %.6g Pa\n',abs(P_target));
    fprintf('P4.2: |U| = %.6g mm/s\n',1000*abs(U_target));
    fprintf('P4.3: angle(P/U) = %.6g rad = %.6g deg\n',phase_rad,phase_deg);
else
    fprintf('P4: fill spherical pressure, velocity, impedance and phase.\n');
end
% Optional: compare spherical-wave velocity with the plane-wave approximation.
r_plot = logspace(log10(0.05),log10(10),500);
P_plot = NaN(size(r_plot)); % TODO: pressure phasor vector, use ./ and .*
U_plot = NaN(size(r_plot)); % TODO: spherical velocity phasor vector
U_plane_approx = NaN(size(r_plot)); % TODO: P_plot/(rho_air*c_air)
if all(isfinite([P_plot,U_plot,U_plane_approx]))
    figure('Name','Problem 4');
    subplot(2,1,1); loglog(r_plot,abs(P_plot),'LineWidth',1.5); grid on;
    xlabel('Radius [m]'); ylabel('|P| [Pa]');
    subplot(2,1,2); loglog(r_plot,1000*abs(U_plot), ...
        r_plot,1000*abs(U_plane_approx),'--','LineWidth',1.5); grid on;
    xlabel('Radius [m]'); ylabel('|U| [mm/s]');
    legend('Spherical wave','Plane-wave approximation','Location','best');
end

%% Problem 5 - Verify the 1D wave equation by hand, then numerically
% Given p_hat = A*exp(1i*(omega*t-k*x)). Differentiate twice in x and t.
% Write your derivatives and the required k-omega relation in the exercise note.
% The values below are arbitrary test points, not additional problem givens.
A5 = 1; f5 = 1000; omega5 = 2*pi*f5;
k5 = NaN;             % TODO: dispersion relation
x5 = linspace(0,1,101); t5 = 0.0002;
p5 = A5*exp(1i*(omega5*t5-k5*x5));
d2p_dx2 = NaN(size(x5)); % TODO: analytic second x derivative evaluated here
d2p_dt2 = NaN(size(x5)); % TODO: analytic second t derivative evaluated here
if all(isfinite([d2p_dx2,d2p_dt2]))
    residual = d2p_dx2-d2p_dt2/c_air^2;
    relative_residual = max(abs(residual))/max(max(abs(d2p_dx2)),eps);
    fprintf('P5: relative wave-equation residual = %.3g\n',relative_residual);
    % A numerical check supports your derivation; it is not a general proof.
else
    fprintf('P5: write the derivatives and fill the numerical verification.\n');
end

%% Optional reference answers - transcribed from the supplied problem sheet
% Rounding depends on the assumed air/water densities and speed of sound.
if show_reference_answers
    fprintf('\nReference answers from 34840_Problems2.pdf:\n');
    fprintf('P1: 8.6, 25.7, 42.9 cm, ...\n');
    fprintf('P2: frequency factor 2.91\n');
    fprintf('P3.1/3.2: +0.99944 / -0.99944\n');
    fprintf('P3.3: Pi/Pt = 0.5 (air-water), 1793 (water-air)\n');
    fprintf('P4: 5 Pa; 29 mm/s; +1.14 rad (+65.4 deg)\n');
end
