%% 34840 - Week 1: Fundamental concepts and plane waves (1 September 2026)
% Student starter: replace NaN placeholders with your own expressions.
% Run setup first, then use Run Section (Ctrl+Enter) for each problem.
% Source: course Exercises/34840-Problems 1.pdf; supplied solutions linked in note.
% Convention: exp(1i*omega*t). All amplitudes are PEAK, not RMS.
% No additional toolboxes required.
clear; clc; close all;
c_air = 343;           % m/s, at 20 deg C
rho_air = 1.204;       % kg/m^3, rho*c approximately 413 Pa*s/m
p0 = 101.3e3;          % Pa, ambient static pressure
 gamma_air = 1.401;    % specific heat ratio, as in supplied solutions
R_air = 287;           % J/(kg*K), specific gas constant
show_reference_answers = false; % Enable after attempting the problems.

%% Problem 1 - Harmonic travelling plane wave
P1 = 1;               % Pa peak, choose zero phase at observation point
f1 = 1000;            % Hz
omega1 = NaN;         % TODO: angular frequency [rad/s]
lambda1 = NaN;        % TODO 1.1: wavelength [m]
k1 = NaN;             % TODO 1.1: wavenumber [rad/m]
Z0 = NaN;             % TODO: characteristic impedance [Pa*s/m]
U1 = NaN;             % TODO 1.2: complex particle velocity [m/s]
Xi1 = NaN;            % TODO 1.2: complex particle displacement [m]
if all(isfinite([omega1,lambda1,k1,Z0,U1,Xi1]))
    fprintf('P1.1: wavelength %.4f cm; wavenumber %.4f rad/m\n',100*lambda1,k1);
    fprintf('P1.2: velocity %.4f mm/s; displacement %.4f micrometres\n', ...
        1000*abs(U1),1e6*abs(Xi1));
    % Optional illustration: compare phases at a fixed point over two cycles.
    t1 = linspace(0,2/f1,501);
    figure('Name','Problem 1 - phase relationships');
    plot(1000*t1,real(P1*exp(1i*omega1*t1))/abs(P1), ...
         1000*t1,real(U1*exp(1i*omega1*t1))/abs(U1),'--', ...
         1000*t1,real(Xi1*exp(1i*omega1*t1))/abs(Xi1),':','LineWidth',1.5);
    grid on; xlabel('Time [ms]'); ylabel('Normalized instantaneous value');
    legend('Pressure','Velocity','Displacement','Location','best');
else
    fprintf('P1: fill wave quantities, velocity and displacement.\n');
end

%% Problem 2 - Coherent addition of two identical loudspeakers
% Equal distances: common propagation phase can be absorbed into reference.
% 2.1, 2.2, 2.3, 2.4 correspond to the entries below, in that order.
p_each = 0.5;         % Pa peak, per loudspeaker acting alone
lag_deg = [0 90 180 179];
lag_rad = NaN(size(lag_deg)); % TODO: convert degrees to radians
P_first = p_each*ones(size(lag_deg));
P_second = NaN(size(lag_deg)); % TODO: second-channel phasors (negative phase for lag)
P_total = NaN(size(lag_deg));  % TODO: sum complex pressures
P_amplitude = NaN(size(lag_deg)); % TODO: magnitude AFTER addition [Pa]
if all(isfinite([P_second,P_total,P_amplitude]))
    disp(table(lag_deg(:),P_amplitude(:),1000*P_amplitude(:), ...
        'VariableNames',{'PhaseLag_deg','Amplitude_Pa','Amplitude_mPa'}));
    figure('Name','Problem 2 - phasor addition');
    for q = 1:numel(lag_deg)
        subplot(2,2,q);
        plot([0 real(P_first(q))],[0 imag(P_first(q))],'-o', ...
             [0 real(P_second(q))],[0 imag(P_second(q))],'-s', ...
             [0 real(P_total(q))],[0 imag(P_total(q))],'-x','LineWidth',1.5);
        axis equal; xlim([-0.6 1.1]); ylim([-0.6 0.6]); grid on;
        xlabel('Real [Pa]'); ylabel('Imaginary [Pa]');
        title(sprintf('Phase lag %g deg',lag_deg(q)));
        legend('P_1','P_2','P_1 + P_2','Location','best');
    end
    % At 180 degrees, round-off can leave a tiny nonzero residual.
else
    fprintf('P2: construct and add the phasors for all four phase lags.\n');
end
% Optional continuous sweep: show the sharp cancellation near 180 degrees.
lag_sweep_deg = linspace(0,360,721);
P_sweep = NaN(size(lag_sweep_deg)); % TODO: complex sum over the phase sweep
if all(isfinite(P_sweep))
    figure('Name','Problem 2 - amplitude versus phase');
    plot(lag_sweep_deg,abs(P_sweep),'LineWidth',1.5); grid on;
    xlabel('Phase lag [deg]'); ylabel('Total pressure amplitude [Pa]');
end

%% Problem 3 - Adiabatic volume change in an ear-canal cavity
fractional_volume_percent = 0.002; % percent, NOT the dimensionless fraction
fractional_volume_amplitude = NaN; % TODO: convert percentage to fraction
P3_amplitude = NaN;                % TODO 3.1: pressure amplitude [Pa]
% Explain the signed pressure-volume relation in your exercise note.
if isfinite(P3_amplitude)
    fprintf('P3.1: pressure amplitude %.5g Pa\n',P3_amplitude);
else
    fprintf('P3: convert percent to fraction and apply adiabatic compression.\n');
end

%% Problem 4 - Seasonal organ-pipe tuning
T_winter_C = 15; T_summer_C = 32; % deg C
f_summer = 110;                  % Hz, fundamental at summer temperature
T_winter_K = NaN;                % TODO: absolute temperature [K]
T_summer_K = NaN;                % TODO: absolute temperature [K]
c_ratio = NaN;                   % TODO 4.1: c_summer/c_winter
f_winter = NaN;                  % TODO 4.2: fundamental in winter [Hz]
% Assume fixed pipe length and unchanged gas composition; neglect end corrections.
if all(isfinite([c_ratio,f_winter]))
    fprintf('P4.1: c_summer/c_winter = %.6f\n',c_ratio);
    fprintf('P4.2: winter fundamental = %.4f Hz\n',f_winter);
else
    fprintf('P4: use kelvin temperatures, sound-speed ratio and fixed pipe length.\n');
end
% Optional: tuning across the full temperature interval.
T_plot_C = linspace(T_winter_C,T_summer_C,101);
f_plot = NaN(size(T_plot_C)); % TODO: frequency curve relative to summer tuning
if all(isfinite(f_plot))
    figure('Name','Problem 4 - temperature and tuning');
    plot(T_plot_C,f_plot,'LineWidth',1.5); grid on;
    xlabel('Air temperature [deg C]'); ylabel('Fundamental frequency [Hz]');
end

%% Optional reference answers - from the supplied Week 1 problem sheet
if show_reference_answers
    fprintf('\nReference answers from 34840-Problems 1.pdf:\n');
    fprintf('P1.1: 34.3 cm; 18.3 rad/m\n');
    fprintf('P1.2: 2.42 mm/s; 0.385 micrometres\n');
    fprintf('P2.1-2.4: 1 Pa; 0.71 Pa; 0 Pa; 8.7 mPa\n');
    fprintf('P3.1: 2.84 Pa\n');
    fprintf('P4.1: 1.029; P4.2: 106.9 Hz\n');
end
