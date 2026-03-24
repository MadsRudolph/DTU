function result = Medium(varargin)
% MEDIUM - Electromagnetic wave parameters in materials
%
% =========================================================================
% USAGE MODES:
% =========================================================================
%
% MODE 1: General medium (lossy or lossless)
%   result = Medium(eps_r, freq)                    % Lossless dielectric
%   result = Medium(eps_r, sigma, freq)             % Lossy (conductivity)
%   result = Medium(eps_r, sigma, freq, mu_r)       % Magnetic material
%   result = Medium(eps_r, sigma, freq, mu_r, name) % With label
%
% MODE 2: From loss tangent
%   result = Medium('tand', eps_r, tan_delta, freq)
%
% MODE 3: Good conductor approximation
%   result = Medium('conductor', sigma, freq)
%   result = Medium('conductor', sigma, freq, mu_r)
%
% MODE 4: Skin depth calculation
%   result = Medium('skin', sigma, freq)
%   result = Medium('skin', sigma, freq, mu_r)
%
% MODE 5: Free space
%   result = Medium('free', freq)
%
% =========================================================================
% OUTPUTS (struct):
% =========================================================================
%   result.eps_r        - Relative permittivity
%   result.mu_r         - Relative permeability
%   result.sigma        - Conductivity (S/m)
%   result.freq         - Frequency (Hz)
%   result.omega        - Angular frequency (rad/s)
%   result.tan_delta    - Loss tangent
%   result.classification - 'Lossless', 'Low-Loss', 'Quasi-Conductor', 'Good Conductor'
%
%   result.gamma        - Complex propagation constant
%   result.alpha        - Attenuation constant (Np/m)
%   result.beta         - Phase constant (rad/m)
%   result.lambda       - Wavelength (m)
%   result.up           - Phase velocity (m/s)
%   result.eta          - Intrinsic impedance (complex, Ohm)
%   result.n            - Refractive index
%   result.skin_depth   - Skin depth (m), if lossy
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % Lossless dielectric (glass) at 10 GHz
%   Medium(4, 10e9)
%
%   % Lossy tissue at 900 MHz
%   Medium(50, 1.5, 900e6, 1, 'Muscle Tissue')
%
%   % Seawater at 1 MHz
%   Medium(80, 4, 1e6, 1, 'Seawater')
%
%   % Copper at 1 GHz
%   Medium('conductor', 5.8e7, 1e9)
%
%   % From loss tangent
%   Medium('tand', 4, 0.02, 5e9)
%
%   % Free space
%   Medium('free', 1e9)
%
% =========================================================================
% CLASSIFICATION (based on tan_delta = sigma/(omega*eps)):
% =========================================================================
%   tan_delta < 0.01  : Lossless (approximately)
%   tan_delta < 0.1   : Low-loss dielectric
%   0.1 < tan_delta < 10 : Quasi-conductor
%   tan_delta > 10    : Good conductor
%
% =========================================================================

    if nargin == 0
        print_help();
        return;
    end

    % Physical constants
    eps0 = 8.854187817e-12;  % F/m
    mu0 = 4*pi*1e-7;         % H/m
    c0 = 1/sqrt(eps0*mu0);   % m/s

    % Detect mode
    if ischar(varargin{1}) || isstring(varargin{1})
        mode = lower(string(varargin{1}));
        args = varargin(2:end);
    else
        % Numeric input: determine if lossless or lossy
        if nargin == 2
            mode = "lossless";
        else
            mode = "lossy";
        end
        args = varargin;
    end

    % Dispatch
    switch mode
        case "lossless"
            result = mode_lossless(args{:});
        case "lossy"
            result = mode_lossy(args{:});
        case "tand"
            result = mode_from_tand(args{:});
        case "conductor"
            result = mode_conductor(args{:});
        case "skin"
            result = mode_skin_depth(args{:});
        case "free"
            result = mode_free_space(args{:});
        otherwise
            error('Unknown mode: %s. Run Medium() for help.', mode);
    end
end

%% ========================================================================
%  MODE HANDLERS
%% ========================================================================

function result = mode_lossless(eps_r, freq, mu_r)
    if nargin < 3, mu_r = 1; end
    
    % Constants
    eps0 = 8.854187817e-12;
    mu0 = 4*pi*1e-7;
    c0 = 1/sqrt(eps0*mu0);
    
    omega = 2*pi*freq;
    eps = eps0 * eps_r;
    mu = mu0 * mu_r;
    
    % Wave parameters
    beta = omega * sqrt(mu * eps);
    lambda = 2*pi / beta;
    up = omega / beta;
    eta = sqrt(mu / eps);
    n = c0 / up;
    k0 = omega / c0;
    
    % Pack results
    result.eps_r = eps_r;
    result.mu_r = mu_r;
    result.sigma = 0;
    result.freq = freq;
    result.omega = omega;
    result.tan_delta = 0;
    result.classification = 'Lossless';
    
    result.gamma = 1j * beta;
    result.alpha = 0;
    result.beta = beta;
    result.lambda = lambda;
    result.up = up;
    result.eta = eta;
    result.n = n;
    result.k0 = k0;
    result.skin_depth = Inf;
    
    % Display
    print_results(result, 'Lossless Dielectric');
end

function result = mode_lossy(eps_r, sigma, freq, mu_r, name)
    if nargin < 4, mu_r = 1; end
    if nargin < 5, name = 'Lossy Medium'; end
    
    % Constants
    eps0 = 8.854187817e-12;
    mu0 = 4*pi*1e-7;
    c0 = 1/sqrt(eps0*mu0);
    
    omega = 2*pi*freq;
    eps = eps0 * eps_r;
    mu = mu0 * mu_r;
    
    % Loss tangent
    tan_delta = sigma / (omega * eps);
    
    % Classification
    if tan_delta < 0.01
        classification = 'Lossless (approx)';
    elseif tan_delta < 0.1
        classification = 'Low-Loss Dielectric';
    elseif tan_delta < 10
        classification = 'Quasi-Conductor';
    else
        classification = 'Good Conductor';
    end
    
    % Complex permittivity and propagation constant
    eps_c = eps - 1j*sigma/omega;  % Complex permittivity
    gamma = 1j * omega * sqrt(mu * eps_c);
    gamma = sqrt(1j*omega*mu * (sigma + 1j*omega*eps));  % Equivalent
    
    alpha = real(gamma);
    beta = imag(gamma);
    
    % Wave parameters
    if beta > 0
        lambda = 2*pi / beta;
        up = omega / beta;
    else
        lambda = Inf;
        up = Inf;
    end
    
    % Intrinsic impedance
    eta = sqrt(1j*omega*mu / (sigma + 1j*omega*eps));
    
    % Refractive index (complex)
    n = c0 * sqrt(mu * eps_c) / sqrt(mu0 * eps0);
    n_real = c0 / up;
    
    % Skin depth
    skin_depth = 1 / alpha;
    
    % Pack results
    result.name = name;
    result.eps_r = eps_r;
    result.mu_r = mu_r;
    result.sigma = sigma;
    result.freq = freq;
    result.omega = omega;
    result.tan_delta = tan_delta;
    result.classification = classification;
    
    result.gamma = gamma;
    result.alpha = alpha;
    result.beta = beta;
    result.lambda = lambda;
    result.up = up;
    result.eta = eta;
    result.n = n_real;
    result.n_complex = n;
    result.skin_depth = skin_depth;
    result.eps_complex = eps_c;
    
    % Display
    print_results(result, name);
end

function result = mode_from_tand(eps_r, tan_delta, freq, mu_r)
    if nargin < 4, mu_r = 1; end
    
    % Calculate sigma from loss tangent
    eps0 = 8.854187817e-12;
    omega = 2*pi*freq;
    eps = eps0 * eps_r;
    sigma = tan_delta * omega * eps;
    
    % Use lossy mode
    result = mode_lossy(eps_r, sigma, freq, mu_r, 'From Loss Tangent');
    result.tan_delta_input = tan_delta;
end

function result = mode_conductor(sigma, freq, mu_r)
    if nargin < 3, mu_r = 1; end
    
    % Good conductor approximation
    mu0 = 4*pi*1e-7;
    mu = mu0 * mu_r;
    omega = 2*pi*freq;
    
    % Simplified formulas for good conductor
    alpha = sqrt(pi * freq * mu * sigma);
    beta = alpha;  % Equal for good conductor
    
    skin_depth = 1 / alpha;
    lambda = 2*pi / beta;
    up = omega / beta;
    
    % Surface impedance
    eta = (1 + 1j) * sqrt(omega * mu / (2 * sigma));
    Rs = real(eta);  % Surface resistance
    
    % Pack results
    result.sigma = sigma;
    result.mu_r = mu_r;
    result.freq = freq;
    result.omega = omega;
    result.classification = 'Good Conductor';
    
    result.gamma = alpha + 1j*beta;
    result.alpha = alpha;
    result.beta = beta;
    result.lambda = lambda;
    result.up = up;
    result.eta = eta;
    result.Rs = Rs;
    result.skin_depth = skin_depth;
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('      GOOD CONDUCTOR ANALYSIS            \n');
    fprintf('==========================================\n');
    fprintf('  sigma = %.3e S/m\n', sigma);
    fprintf('  mu_r = %.2f\n', mu_r);
    fprintf('  freq = %.3e Hz\n', freq);
    fprintf('------------------------------------------\n');
    fprintf('  Skin depth delta = %.3e m\n', skin_depth);
    fprintf('  alpha = beta = %.3e Np/m (or rad/m)\n', alpha);
    fprintf('  lambda = %.3e m\n', lambda);
    fprintf('  u_p = %.3e m/s\n', up);
    fprintf('------------------------------------------\n');
    fprintf('  eta = %.4f + j%.4f Ohm\n', real(eta), imag(eta));
    fprintf('  |eta| = %.4f Ohm\n', abs(eta));
    fprintf('  R_s (surface resistance) = %.4e Ohm\n', Rs);
    fprintf('==========================================\n\n');
end

function result = mode_skin_depth(sigma, freq, mu_r)
    if nargin < 3, mu_r = 1; end
    
    mu0 = 4*pi*1e-7;
    mu = mu0 * mu_r;
    
    delta = 1 / sqrt(pi * freq * mu * sigma);
    
    result.sigma = sigma;
    result.mu_r = mu_r;
    result.freq = freq;
    result.skin_depth = delta;
    
    fprintf('\n');
    fprintf('=== Skin Depth ===\n');
    fprintf('  sigma = %.3e S/m\n', sigma);
    fprintf('  freq = %.3e Hz\n', freq);
    fprintf('  mu_r = %.2f\n', mu_r);
    fprintf('  -----------------\n');
    fprintf('  delta = %.4e m\n', delta);
    fprintf('  delta = %.4f um\n', delta*1e6);
    fprintf('  delta = %.4f mm\n', delta*1e3);
    fprintf('==================\n\n');
end

function result = mode_free_space(freq)
    eps0 = 8.854187817e-12;
    mu0 = 4*pi*1e-7;
    c0 = 1/sqrt(eps0*mu0);
    eta0 = sqrt(mu0/eps0);
    
    omega = 2*pi*freq;
    k0 = omega/c0;
    lambda0 = c0/freq;
    
    result.eps_r = 1;
    result.mu_r = 1;
    result.sigma = 0;
    result.freq = freq;
    result.omega = omega;
    result.classification = 'Free Space';
    
    result.gamma = 1j*k0;
    result.alpha = 0;
    result.beta = k0;
    result.k0 = k0;
    result.lambda = lambda0;
    result.lambda0 = lambda0;
    result.up = c0;
    result.c0 = c0;
    result.eta = eta0;
    result.eta0 = eta0;
    result.n = 1;
    
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('         FREE SPACE PARAMETERS           \n');
    fprintf('==========================================\n');
    fprintf('  freq = %.3e Hz\n', freq);
    fprintf('------------------------------------------\n');
    fprintf('  c0 = %.6e m/s\n', c0);
    fprintf('  eta0 = %.4f Ohm\n', eta0);
    fprintf('  k0 = %.4f rad/m\n', k0);
    fprintf('  lambda0 = %.4e m\n', lambda0);
    fprintf('==========================================\n\n');
end

%% ========================================================================
%  DISPLAY FUNCTION
%% ========================================================================

function print_results(r, title)
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('  %s @ %.2e Hz\n', upper(title), r.freq);
    fprintf('==========================================\n');
    fprintf('  Properties:\n');
    fprintf('    eps_r = %.4f\n', r.eps_r);
    fprintf('    mu_r  = %.4f\n', r.mu_r);
    if r.sigma > 0
        fprintf('    sigma = %.3e S/m\n', r.sigma);
    end
    fprintf('------------------------------------------\n');
    fprintf('  Classification:\n');
    fprintf('    tan(delta) = %.3e\n', r.tan_delta);
    fprintf('    Type: %s\n', r.classification);
    fprintf('------------------------------------------\n');
    fprintf('  Wave Parameters:\n');
    fprintf('    alpha = %.4e Np/m\n', r.alpha);
    fprintf('    beta  = %.4e rad/m\n', r.beta);
    fprintf('    lambda = %.4e m\n', r.lambda);
    fprintf('    u_p = %.4e m/s\n', r.up);
    fprintf('    n = %.4f\n', r.n);
    fprintf('------------------------------------------\n');
    fprintf('  Intrinsic Impedance:\n');
    fprintf('    eta = %.4f %+.4fj Ohm\n', real(r.eta), imag(r.eta));
    fprintf('    |eta| = %.4f Ohm\n', abs(r.eta));
    fprintf('    angle(eta) = %.2f deg\n', rad2deg(angle(r.eta)));
    if r.alpha > 0
        fprintf('------------------------------------------\n');
        fprintf('  Attenuation:\n');
        fprintf('    Skin depth = %.4e m\n', r.skin_depth);
        fprintf('    Loss @ 1m = %.2f dB\n', 20*log10(exp(1))*r.alpha);
    end
    fprintf('==========================================\n\n');
end

function print_help()
    fprintf('\n');
    fprintf('MEDIUM - EM Wave Parameters Calculator\n');
    fprintf('======================================\n\n');
    fprintf('Lossless dielectric:\n');
    fprintf('  Medium(eps_r, freq)\n');
    fprintf('  Medium(eps_r, freq, mu_r)\n\n');
    fprintf('Lossy medium:\n');
    fprintf('  Medium(eps_r, sigma, freq)\n');
    fprintf('  Medium(eps_r, sigma, freq, mu_r)\n');
    fprintf('  Medium(eps_r, sigma, freq, mu_r, ''Name'')\n\n');
    fprintf('From loss tangent:\n');
    fprintf('  Medium(''tand'', eps_r, tan_delta, freq)\n\n');
    fprintf('Good conductor:\n');
    fprintf('  Medium(''conductor'', sigma, freq)\n\n');
    fprintf('Skin depth only:\n');
    fprintf('  Medium(''skin'', sigma, freq)\n\n');
    fprintf('Free space:\n');
    fprintf('  Medium(''free'', freq)\n\n');
    fprintf('Examples:\n');
    fprintf('  Medium(4, 10e9)                   %% Glass at 10 GHz\n');
    fprintf('  Medium(80, 4, 1e6, 1, ''Seawater'') %% Seawater at 1 MHz\n');
    fprintf('  Medium(''conductor'', 5.8e7, 1e9)  %% Copper at 1 GHz\n');
    fprintf('  Medium(''free'', 2.4e9)            %% Free space at 2.4 GHz\n\n');
end
