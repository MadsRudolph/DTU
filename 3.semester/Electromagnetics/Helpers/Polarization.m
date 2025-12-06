function result = Polarization(varargin)
% POLARIZATION - Complete polarization analysis of an EM wave
%
% =========================================================================
% USAGE MODES (pick whichever matches your problem):
% =========================================================================
%
% MODE 1: Complex Phasor (most common for exam problems)
%   result = Polarization(F)              % assumes +z propagation
%   result = Polarization(F, k_hat)       % specify propagation direction
%
%   F     - Complex phasor [3x1] or [2x1], e.g., [1; -1j; 0]
%   k_hat - Propagation direction (default: [0;0;1])
%
% MODE 2: Time-domain coefficients (u*cos + v*sin form)
%   result = Polarization(u, v, beta)
%
%   Field: F(t) = u*cos(Ï‰t - Î²Â·r) + v*sin(Ï‰t - Î²Â·r)
%   u, v  - Real coefficient vectors [3x1]
%   beta  - Phase vector [3x1] in rad/m
%
% MODE 3: Amplitude and phase (for problems giving |Ex|, |Ey|, Ï†x, Ï†y)
%   result = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg)
%   result = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg, k_hat)
%
% =========================================================================
% OUTPUT (struct):
% =========================================================================
%   result.type       - 'Linear', 'Circular', or 'Elliptical'
%   result.handedness - 'RHCP', 'LHCP', or 'N/A'
%   result.AR         - Axial ratio (1=circular, Inf=linear)
%   result.AR_dB      - Axial ratio in dB (0=circular, Inf=linear)
%   result.major      - Major semi-axis amplitude
%   result.minor      - Minor semi-axis amplitude
%   result.tilt_deg   - Tilt angle of ellipse (degrees)
%   result.F          - Complex phasor used
%   result.k_hat      - Propagation direction used
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
% % RHCP wave propagating in +z
% Polarization([1; -1j; 0])
%
% % LHCP wave propagating in +x
% Polarization([0; 1; 1j], [1;0;0])
%
% % Linear polarization (45 deg)
% Polarization([1; 1; 0])
%
% % Elliptical from amplitude/phase: Ex=10, Ey=5, phi_x=0, phi_y=90
% Polarization('ap', 10, 5, 0, 90)
%
% % Time-domain form: E = x_hat*cos(psi) + y_hat*sin(psi)
% Polarization([1;0;0], [0;1;0], [0;0;1])
%
% =========================================================================

    %% Parse input mode
    if nargin == 0
        print_help();
        return;
    end
    
    % Detect mode
    if ischar(varargin{1}) || isstring(varargin{1})
        % MODE 3: Amplitude/Phase
        [F, k_hat] = parse_amplitude_phase(varargin{2:end});
    elseif nargin >= 3 && isreal(varargin{1}) && isreal(varargin{2})
        % MODE 2: Time-domain (u, v, beta)
        [F, k_hat] = parse_time_domain(varargin{1}, varargin{2}, varargin{3});
    else
        % MODE 1: Complex phasor
        F = varargin{1};
        if nargin >= 2 && ~isempty(varargin{2})
            k_hat = varargin{2};
        else
            k_hat = [0; 0; 1];  % Default +z
        end
    end
    
    %% Prepare vectors
    F = F(:);
    k_hat = k_hat(:) / norm(k_hat);
    
    % Pad to 3D if needed
    if length(F) == 2
        F = [F; 0];
    end
    if length(k_hat) == 2
        k_hat = [k_hat; 0];
    end
    
    Fr = real(F);
    Fi = imag(F);
    
    %% Polarization Type Detection
    cross_ri = cross(Fr, Fi);
    scale = max(norm(Fr), norm(Fi));
    if scale == 0
        scale = 1;
    end
    
    % Tolerance for classification (1e-6 handles typical truncated decimals)
    tol = 1e-3;
    
    is_linear = norm(cross_ri) < tol * scale;
    
    dot_ri = dot(Fr, Fi);
    amp_equal = abs(norm(Fr) - norm(Fi)) < tol * scale;
    is_circular = ~is_linear && (abs(dot_ri) < tol * scale^2) && amp_equal;
    
    %% Handedness
    if is_linear
        handedness = "N/A";
    else
        % Handedness rule: E(t) = Fr*cos - Fi*sin = u*cos + v*sin
        % where u = Fr and v = -Fi
        % s = k_hat · (u × v) = k_hat · (Fr × (-Fi))
        % s > 0 → right-hand (RHCP), s < 0 → left-hand (LHCP)
        hand = dot(k_hat, cross(Fr, -Fi));
        if hand > 0
            handedness = "RHCP";
        else
            handedness = "LHCP";
        end
    end
    
    %% Type classification
    if is_linear
        pol_type = "Linear";
    elseif is_circular
        pol_type = "Circular";
    else
        pol_type = "Elliptical";
    end
    
    %% Axial Ratio Calculation
    % Select two dominant components
    [~, idx] = sort(abs(Fr) + abs(Fi), 'descend');
    idx = idx(1:2);
    Fr2 = Fr(idx);
    Fi2 = Fi(idx);
    
    % Tilt angle of ellipse
    num = 2 * dot(Fr2, Fi2);
    den = norm(Fi2)^2 - norm(Fr2)^2;
    phi1 = 0.5 * atan2(num, den);
    phi2 = phi1 + pi/2;
    
    % Semi-axes
    E1 = norm(Fr2 * cos(phi1) - Fi2 * sin(phi1));
    E2 = norm(Fr2 * cos(phi2) - Fi2 * sin(phi2));
    
    if E1 >= E2
        major = E1; minor = E2; tilt = phi1;
    else
        major = E2; minor = E1; tilt = phi2;
    end
    
    % Axial ratio
    if minor < 1e-12 * major
        AR = Inf;
        AR_dB = Inf;
    else
        AR = major / minor;
        AR_dB = 20 * log10(AR);
    end
    
    %% Pack results
    result.type       = pol_type;
    result.handedness = handedness;
    result.AR         = AR;
    result.AR_dB      = AR_dB;
    result.major      = major;
    result.minor      = minor;
    result.tilt       = tilt;
    result.tilt_deg   = rad2deg(tilt);
    result.F          = F;
    result.k_hat      = k_hat;
    result.Fr         = Fr;
    result.Fi         = Fi;
    
    %% Display Results
    fprintf('\n');
    fprintf('========================================\n');
    fprintf('       POLARIZATION ANALYSIS           \n');
    fprintf('========================================\n');
    fprintf('  Type:        %s\n', pol_type);
    fprintf('  Handedness:  %s\n', handedness);
    fprintf('----------------------------------------\n');
    if isinf(AR)
        fprintf('  Axial Ratio: Inf (Linear)\n');
    elseif AR < 1.001
        fprintf('  Axial Ratio: 1.000 (0.00 dB)\n');
    else
        fprintf('  Axial Ratio: %.4f (%.2f dB)\n', AR, AR_dB);
    end
    fprintf('  Major axis:  %.4f\n', major);
    fprintf('  Minor axis:  %.4f\n', minor);
    fprintf('  Tilt angle:  %.2f deg\n', rad2deg(tilt));
    fprintf('----------------------------------------\n');
    fprintf('  Phasor F:\n');
    print_phasor_component('x', F(1));
    print_phasor_component('y', F(2));
    print_phasor_component('z', F(3));
    fprintf('  k_hat = [%.2f, %.2f, %.2f]\n', k_hat(1), k_hat(2), k_hat(3));
    fprintf('========================================\n\n');
end

%% Helper Functions

function [F, k_hat] = parse_amplitude_phase(Ex, Ey, phi_x, phi_y, varargin)
    % Convert amplitude/phase to complex phasor
    % F = Ex*exp(j*phi_x)*x_hat + Ey*exp(j*phi_y)*y_hat
    Fx = Ex * exp(1j * deg2rad(phi_x));
    Fy = Ey * exp(1j * deg2rad(phi_y));
    F = [Fx; Fy; 0];
    
    if nargin >= 5 && ~isempty(varargin{1})
        k_hat = varargin{1};
    else
        k_hat = [0; 0; 1];
    end
end

function [F, k_hat] = parse_time_domain(u, v, beta)
    % Convert u*cos + v*sin to complex phasor
    % F(t) = Re{F * e^(jwt)} where F = u - j*v
    u = u(:);
    v = v(:);
    beta = beta(:);
    
    if length(u) == 2, u = [u; 0]; end
    if length(v) == 2, v = [v; 0]; end
    
    F = u - 1j*v;  % F(t) = Re{F*e^jwt} = u*cos - v*(-sin) = u*cos + v*sin
    k_hat = beta / norm(beta);
end

function print_phasor_component(comp, val)
    if abs(val) < 1e-10
        fprintf('    F%s = 0\n', comp);
    elseif abs(imag(val)) < 1e-10
        fprintf('    F%s = %.4f\n', comp, real(val));
    elseif abs(real(val)) < 1e-10
        if imag(val) > 0
            fprintf('    F%s = j%.4f\n', comp, imag(val));
        else
            fprintf('    F%s = -j%.4f\n', comp, abs(imag(val)));
        end
    else
        if imag(val) > 0
            fprintf('    F%s = %.4f + j%.4f\n', comp, real(val), imag(val));
        else
            fprintf('    F%s = %.4f - j%.4f\n', comp, real(val), abs(imag(val)));
        end
    end
end

function print_help()
    fprintf('\n');
    fprintf('POLARIZATION - Quick Reference\n');
    fprintf('==============================\n\n');
    fprintf('Complex phasor (simplest):\n');
    fprintf('  Polarization([1; -1j; 0])           %% RHCP in +z\n');
    fprintf('  Polarization([1; 1j; 0], [0;0;1])   %% LHCP in +z\n\n');
    fprintf('Amplitude/Phase:\n');
    fprintf('  Polarization(''ap'', Ex, Ey, phi_x, phi_y)\n\n');
    fprintf('Time-domain (u*cos + v*sin):\n');
    fprintf('  Polarization(u, v, beta)\n\n');
    fprintf('Run with arguments to analyze a wave.\n\n');
end
