function result = Fresnel(varargin)
% FRESNEL - Unified reflection/transmission calculator for EM waves
%
% =========================================================================
% USAGE MODES:
% =========================================================================
%
% MODE 1: Normal incidence (simplest)
%   result = Fresnel(eps_r1, eps_r2)              % Both non-magnetic
%   result = Fresnel(eps_r1, eps_r2, mu_r1, mu_r2)
%   result = Fresnel('normal', n1, n2)            % Using refractive indices
%
% MODE 2: Oblique incidence with angle
%   result = Fresnel(eps_r1, eps_r2, theta_i)           % TE and TM
%   result = Fresnel(eps_r1, eps_r2, theta_i, 'TE')     % TE only
%   result = Fresnel(eps_r1, eps_r2, theta_i, 'TM')     % TM only
%
% MODE 3: Find transmission angle (Snell's law)
%   result = Fresnel('snell', n1, n2, theta_i)
%   result = Fresnel('snell', eps_r1, eps_r2, theta_i)
%
% MODE 4: From wave vector (for oblique problems)
%   result = Fresnel('kvec', beta, eps_r2, plane)
%   % beta = [kx; ky; kz], plane = 'xy', 'xz', or 'yz'
%
% MODE 5: Brewster angle
%   result = Fresnel('brewster', eps_r1, eps_r2)
%
% MODE 6: Critical angle (total internal reflection)
%   result = Fresnel('critical', eps_r1, eps_r2)
%
% =========================================================================
% OUTPUTS (struct):
% =========================================================================
%   result.Gamma_TE   - TE reflection coefficient
%   result.Gamma_TM   - TM reflection coefficient
%   result.tau_TE     - TE transmission coefficient
%   result.tau_TM     - TM transmission coefficient
%   result.R_TE       - TE power reflectance
%   result.R_TM       - TM power reflectance
%   result.T_TE       - TE power transmittance
%   result.T_TM       - TM power transmittance
%   result.theta_i    - Incident angle (degrees)
%   result.theta_t    - Transmitted angle (degrees)
%   result.eta1, eta2 - Intrinsic impedances
%   result.n1, n2     - Refractive indices
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % Normal incidence: air to glass (eps_r = 4)
%   Fresnel(1, 4)
%
%   % Oblique incidence at 45 degrees
%   Fresnel(1, 4, 45)
%
%   % TM wave at 30 degrees
%   Fresnel(1, 2.25, 30, 'TM')
%
%   % Find Brewster angle for air-glass interface
%   Fresnel('brewster', 1, 4)
%
%   % Critical angle for glass-air (internal reflection)
%   Fresnel('critical', 4, 1)
%
%   % Snell's law: find transmission angle
%   Fresnel('snell', 1, 1.5, 30)
%
% =========================================================================

    if nargin == 0
        print_help();
        return;
    end

    % Detect mode
    if ischar(varargin{1}) || isstring(varargin{1})
        mode = lower(string(varargin{1}));
        args = varargin(2:end);
    else
        % Numeric first argument: normal or oblique incidence
        if nargin >= 3 && isnumeric(varargin{3}) && isscalar(varargin{3}) && varargin{3} <= 90
            mode = "oblique";
        else
            mode = "normal";
        end
        args = varargin;
    end

    % Dispatch
    switch mode
        case "normal"
            result = mode_normal(args{:});
        case "oblique"
            result = mode_oblique(args{:});
        case "snell"
            result = mode_snell(args{:});
        case "kvec"
            result = mode_kvec(args{:});
        case "brewster"
            result = mode_brewster(args{:});
        case "critical"
            result = mode_critical(args{:});
        otherwise
            error('Unknown mode: %s. Run Fresnel() for help.', mode);
    end
end

%% ========================================================================
%  MODE HANDLERS
%% ========================================================================

function result = mode_normal(eps_r1, eps_r2, mu_r1, mu_r2)
    if nargin < 3, mu_r1 = 1; end
    if nargin < 4, mu_r2 = 1; end
    
    % Constants
    eps0 = 8.854e-12;
    mu0 = 4*pi*1e-7;
    c0 = 1/sqrt(eps0*mu0);
    
    % Impedances
    eta1 = sqrt(mu_r1/eps_r1) * sqrt(mu0/eps0);
    eta2 = sqrt(mu_r2/eps_r2) * sqrt(mu0/eps0);
    
    % Refractive indices
    n1 = sqrt(eps_r1 * mu_r1);
    n2 = sqrt(eps_r2 * mu_r2);
    
    % Fresnel coefficients (normal incidence: TE = TM)
    Gamma = (eta2 - eta1) / (eta2 + eta1);
    tau = 2*eta2 / (eta2 + eta1);
    
    % Power coefficients
    R = abs(Gamma)^2;
    T = 1 - R;
    
    % Also compute using impedance ratio for verification
    % T = (4*eta1*eta2) / (eta1 + eta2)^2 * (eta1/eta2) -- for power
    
    % Pack results
    result.eps_r1 = eps_r1;
    result.eps_r2 = eps_r2;
    result.mu_r1 = mu_r1;
    result.mu_r2 = mu_r2;
    result.eta1 = eta1;
    result.eta2 = eta2;
    result.n1 = n1;
    result.n2 = n2;
    result.theta_i = 0;
    result.theta_t = 0;
    result.Gamma = Gamma;
    result.Gamma_TE = Gamma;
    result.Gamma_TM = Gamma;
    result.tau = tau;
    result.tau_TE = tau;
    result.tau_TM = tau;
    result.R = R;
    result.R_TE = R;
    result.R_TM = R;
    result.T = T;
    result.T_TE = T;
    result.T_TM = T;
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('     FRESNEL: NORMAL INCIDENCE           \n');
    fprintf('==========================================\n');
    fprintf('  Medium 1: eps_r = %.3f, mu_r = %.3f\n', eps_r1, mu_r1);
    fprintf('  Medium 2: eps_r = %.3f, mu_r = %.3f\n', eps_r2, mu_r2);
    fprintf('------------------------------------------\n');
    fprintf('  eta1 = %.2f Ohm\n', eta1);
    fprintf('  eta2 = %.2f Ohm\n', eta2);
    fprintf('  n1 = %.4f, n2 = %.4f\n', n1, n2);
    fprintf('------------------------------------------\n');
    fprintf('  Gamma = %.4f %+.4fj\n', real(Gamma), imag(Gamma));
    fprintf('  |Gamma| = %.4f\n', abs(Gamma));
    fprintf('  tau = %.4f\n', tau);
    fprintf('------------------------------------------\n');
    fprintf('  R (reflected power) = %.4f (%.2f%%)\n', R, R*100);
    fprintf('  T (transmitted power) = %.4f (%.2f%%)\n', T, T*100);
    fprintf('==========================================\n\n');
end

function result = mode_oblique(eps_r1, eps_r2, theta_i_deg, pol, mu_r1, mu_r2)
    if nargin < 4, pol = 'both'; end
    if nargin < 5, mu_r1 = 1; end
    if nargin < 6, mu_r2 = 1; end
    
    pol = lower(string(pol));
    
    % Constants
    eta0 = sqrt(4*pi*1e-7 / 8.854e-12);  % ~377 Ohm
    
    % Impedances and refractive indices
    eta1 = eta0 * sqrt(mu_r1/eps_r1);
    eta2 = eta0 * sqrt(mu_r2/eps_r2);
    n1 = sqrt(eps_r1 * mu_r1);
    n2 = sqrt(eps_r2 * mu_r2);
    
    % Angles
    theta_i = deg2rad(theta_i_deg);
    
    % Snell's law
    sin_theta_t = (n1/n2) * sin(theta_i);
    
    if abs(sin_theta_t) > 1
        % Total internal reflection
        result.TIR = true;
        result.theta_i = theta_i_deg;
        result.theta_t = NaN;
        result.Gamma_TE = exp(1j*2*calculate_phase_TIR(n1, n2, theta_i, 'TE'));
        result.Gamma_TM = exp(1j*2*calculate_phase_TIR(n1, n2, theta_i, 'TM'));
        result.R_TE = 1;
        result.R_TM = 1;
        result.T_TE = 0;
        result.T_TM = 0;
        
        fprintf('\n');
        fprintf('==========================================\n');
        fprintf('   TOTAL INTERNAL REFLECTION (TIR)       \n');
        fprintf('==========================================\n');
        fprintf('  theta_i = %.2f deg > theta_c\n', theta_i_deg);
        fprintf('  No transmitted wave (evanescent field)\n');
        fprintf('  |Gamma_TE| = |Gamma_TM| = 1\n');
        fprintf('==========================================\n\n');
        return;
    end
    
    theta_t = asin(sin_theta_t);
    theta_t_deg = rad2deg(theta_t);
    
    % TE (s-polarized, perpendicular)
    % Gamma_TE = (eta2*cos(theta_i) - eta1*cos(theta_t)) / (eta2*cos(theta_i) + eta1*cos(theta_t))
    Gamma_TE = (eta2*cos(theta_i) - eta1*cos(theta_t)) / (eta2*cos(theta_i) + eta1*cos(theta_t));
    tau_TE = 2*eta2*cos(theta_i) / (eta2*cos(theta_i) + eta1*cos(theta_t));
    
    % TM (p-polarized, parallel)
    % Gamma_TM = (eta2*cos(theta_t) - eta1*cos(theta_i)) / (eta2*cos(theta_t) + eta1*cos(theta_i))
    Gamma_TM = (eta2*cos(theta_t) - eta1*cos(theta_i)) / (eta2*cos(theta_t) + eta1*cos(theta_i));
    tau_TM = 2*eta2*cos(theta_i) / (eta2*cos(theta_t) + eta1*cos(theta_i));
    
    % Power coefficients
    R_TE = abs(Gamma_TE)^2;
    R_TM = abs(Gamma_TM)^2;
    T_TE = 1 - R_TE;
    T_TM = 1 - R_TM;
    
    % Pack results
    result.eps_r1 = eps_r1;
    result.eps_r2 = eps_r2;
    result.mu_r1 = mu_r1;
    result.mu_r2 = mu_r2;
    result.eta1 = eta1;
    result.eta2 = eta2;
    result.n1 = n1;
    result.n2 = n2;
    result.theta_i = theta_i_deg;
    result.theta_t = theta_t_deg;
    result.Gamma_TE = Gamma_TE;
    result.Gamma_TM = Gamma_TM;
    result.tau_TE = tau_TE;
    result.tau_TM = tau_TM;
    result.R_TE = R_TE;
    result.R_TM = R_TM;
    result.T_TE = T_TE;
    result.T_TM = T_TM;
    result.TIR = false;
    
    % Brewster check
    theta_B = atan(n2/n1);
    result.theta_Brewster = rad2deg(theta_B);
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('     FRESNEL: OBLIQUE INCIDENCE          \n');
    fprintf('==========================================\n');
    fprintf('  Medium 1: eps_r = %.3f, n = %.4f\n', eps_r1, n1);
    fprintf('  Medium 2: eps_r = %.3f, n = %.4f\n', eps_r2, n2);
    fprintf('------------------------------------------\n');
    fprintf('  theta_i = %.2f deg\n', theta_i_deg);
    fprintf('  theta_t = %.2f deg (Snell''s law)\n', theta_t_deg);
    fprintf('  theta_Brewster = %.2f deg\n', rad2deg(theta_B));
    fprintf('------------------------------------------\n');
    
    if pol == "both" || pol == "te"
        fprintf('  TE (s-pol, E perpendicular to plane):\n');
        fprintf('    Gamma_TE = %.4f %+.4fj\n', real(Gamma_TE), imag(Gamma_TE));
        fprintf('    |Gamma_TE| = %.4f\n', abs(Gamma_TE));
        fprintf('    R_TE = %.4f, T_TE = %.4f\n', R_TE, T_TE);
    end
    
    if pol == "both" || pol == "tm"
        fprintf('  TM (p-pol, E parallel to plane):\n');
        fprintf('    Gamma_TM = %.4f %+.4fj\n', real(Gamma_TM), imag(Gamma_TM));
        fprintf('    |Gamma_TM| = %.4f\n', abs(Gamma_TM));
        fprintf('    R_TM = %.4f, T_TM = %.4f\n', R_TM, T_TM);
    end
    fprintf('==========================================\n\n');
end

function result = mode_snell(n1_or_eps1, n2_or_eps2, theta_i_deg)
    % Determine if inputs are n or eps_r
    if n1_or_eps1 <= 10 && n2_or_eps2 <= 10
        % Likely refractive indices or small eps_r (both valid)
        n1 = sqrt(n1_or_eps1);  % If eps_r, convert; if n, sqrt might be wrong
        n2 = sqrt(n2_or_eps2);
        
        % Heuristic: if values are close to 1-3, treat as n directly
        if n1_or_eps1 <= 3 && n2_or_eps2 <= 3
            n1 = n1_or_eps1;
            n2 = n2_or_eps2;
        else
            n1 = sqrt(n1_or_eps1);
            n2 = sqrt(n2_or_eps2);
        end
    else
        n1 = sqrt(n1_or_eps1);
        n2 = sqrt(n2_or_eps2);
    end
    
    theta_i = deg2rad(theta_i_deg);
    sin_theta_t = (n1/n2) * sin(theta_i);
    
    result.n1 = n1;
    result.n2 = n2;
    result.theta_i = theta_i_deg;
    
    if abs(sin_theta_t) > 1
        result.theta_t = NaN;
        result.TIR = true;
        theta_c = asind(n2/n1);
        result.theta_critical = theta_c;
        
        fprintf('\n');
        fprintf('=== Snell''s Law: TOTAL INTERNAL REFLECTION ===\n');
        fprintf('  n1 = %.4f, n2 = %.4f\n', n1, n2);
        fprintf('  theta_i = %.2f deg\n', theta_i_deg);
        fprintf('  theta_c = %.2f deg (critical angle)\n', theta_c);
        fprintf('  theta_i > theta_c => TIR\n');
        fprintf('===============================================\n\n');
    else
        theta_t_deg = asind(sin_theta_t);
        result.theta_t = theta_t_deg;
        result.TIR = false;
        
        fprintf('\n');
        fprintf('=== Snell''s Law ===\n');
        fprintf('  n1 = %.4f, n2 = %.4f\n', n1, n2);
        fprintf('  theta_i = %.2f deg\n', theta_i_deg);
        fprintf('  theta_t = %.2f deg\n', theta_t_deg);
        fprintf('===================\n\n');
    end
end

function result = mode_kvec(beta, eps_r2, plane)
    % Find angles from wave vector
    beta = beta(:);
    
    switch lower(plane)
        case 'xy'
            n_hat = [0; 0; 1];
        case 'xz'
            n_hat = [0; 1; 0];
        case 'yz'
            n_hat = [1; 0; 0];
        otherwise
            error('Plane must be ''xy'', ''xz'', or ''yz''');
    end
    
    k_mag = norm(beta);
    cos_theta_i = abs(dot(beta, n_hat)) / k_mag;
    cos_theta_i = min(max(cos_theta_i, -1), 1);
    theta_i_deg = acosd(cos_theta_i);
    
    n1 = 1;  % Assume air
    n2 = sqrt(eps_r2);
    
    sin_theta_t = (n1/n2) * sind(theta_i_deg);
    
    result.beta = beta;
    result.plane = plane;
    result.theta_i = theta_i_deg;
    
    if abs(sin_theta_t) > 1
        result.theta_t = NaN;
        result.TIR = true;
        fprintf('\nTotal Internal Reflection - no transmission\n');
    else
        result.theta_t = asind(sin_theta_t);
        result.TIR = false;
    end
    
    fprintf('\n');
    fprintf('=== Wave Vector Analysis ===\n');
    fprintf('  beta = [%.3f, %.3f, %.3f]\n', beta(1), beta(2), beta(3));
    fprintf('  Interface: %s plane\n', upper(plane));
    fprintf('  theta_i = %.2f deg\n', theta_i_deg);
    if ~result.TIR
        fprintf('  theta_t = %.2f deg\n', result.theta_t);
    end
    fprintf('============================\n\n');
end

function result = mode_brewster(eps_r1, eps_r2, mu_r1, mu_r2)
    if nargin < 3, mu_r1 = 1; end
    if nargin < 4, mu_r2 = 1; end
    
    n1 = sqrt(eps_r1 * mu_r1);
    n2 = sqrt(eps_r2 * mu_r2);
    
    % Brewster angle (TM polarization, non-magnetic)
    if mu_r1 == 1 && mu_r2 == 1
        theta_B = atand(n2/n1);
    else
        % General formula
        theta_B = atand(sqrt((eps_r2*(eps_r2*mu_r1 - eps_r1*mu_r2)) / ...
                            (eps_r1*(eps_r1*mu_r2 - eps_r2*mu_r1))));
    end
    
    result.eps_r1 = eps_r1;
    result.eps_r2 = eps_r2;
    result.n1 = n1;
    result.n2 = n2;
    result.theta_Brewster = theta_B;
    
    fprintf('\n');
    fprintf('=== Brewster Angle ===\n');
    fprintf('  n1 = %.4f, n2 = %.4f\n', n1, n2);
    fprintf('  theta_B = %.4f deg\n', theta_B);
    fprintf('  At this angle: Gamma_TM = 0 (no TM reflection)\n');
    fprintf('======================\n\n');
end

function result = mode_critical(eps_r1, eps_r2, mu_r1, mu_r2)
    if nargin < 3, mu_r1 = 1; end
    if nargin < 4, mu_r2 = 1; end
    
    n1 = sqrt(eps_r1 * mu_r1);
    n2 = sqrt(eps_r2 * mu_r2);
    
    result.eps_r1 = eps_r1;
    result.eps_r2 = eps_r2;
    result.n1 = n1;
    result.n2 = n2;
    
    if n1 > n2
        theta_c = asind(n2/n1);
        result.theta_critical = theta_c;
        result.TIR_possible = true;
        
        fprintf('\n');
        fprintf('=== Critical Angle ===\n');
        fprintf('  n1 = %.4f > n2 = %.4f\n', n1, n2);
        fprintf('  theta_c = %.4f deg\n', theta_c);
        fprintf('  For theta_i > theta_c: Total Internal Reflection\n');
        fprintf('======================\n\n');
    else
        result.theta_critical = NaN;
        result.TIR_possible = false;
        
        fprintf('\n');
        fprintf('=== Critical Angle ===\n');
        fprintf('  n1 = %.4f < n2 = %.4f\n', n1, n2);
        fprintf('  No critical angle (wave goes from less to more dense)\n');
        fprintf('  TIR not possible for this direction\n');
        fprintf('======================\n\n');
    end
end

function phase = calculate_phase_TIR(n1, n2, theta_i, pol)
    % Phase shift during TIR
    cos_i = cos(theta_i);
    sin_i = sin(theta_i);
    
    x = sqrt((n1*sin_i/n2)^2 - 1);
    
    if strcmpi(pol, 'TE')
        phase = atan2(x, cos_i);
    else
        phase = atan2((n1/n2)^2 * x, cos_i);
    end
end

function print_help()
    fprintf('\n');
    fprintf('FRESNEL - Reflection/Transmission Calculator\n');
    fprintf('=============================================\n\n');
    fprintf('Normal incidence:\n');
    fprintf('  Fresnel(eps_r1, eps_r2)              %% non-magnetic\n');
    fprintf('  Fresnel(eps_r1, eps_r2, mu_r1, mu_r2)\n\n');
    fprintf('Oblique incidence:\n');
    fprintf('  Fresnel(eps_r1, eps_r2, theta_i)     %% TE and TM\n');
    fprintf('  Fresnel(eps_r1, eps_r2, theta_i, ''TE'')\n');
    fprintf('  Fresnel(eps_r1, eps_r2, theta_i, ''TM'')\n\n');
    fprintf('Snell''s law:\n');
    fprintf('  Fresnel(''snell'', n1, n2, theta_i)\n\n');
    fprintf('Special angles:\n');
    fprintf('  Fresnel(''brewster'', eps_r1, eps_r2)\n');
    fprintf('  Fresnel(''critical'', eps_r1, eps_r2)\n\n');
    fprintf('Examples:\n');
    fprintf('  Fresnel(1, 4)              %% air to glass, normal\n');
    fprintf('  Fresnel(1, 4, 45)          %% air to glass, 45 deg\n');
    fprintf('  Fresnel(''brewster'', 1, 4) %% Brewster angle\n\n');
end
