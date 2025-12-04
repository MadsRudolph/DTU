% ============================================================================
% LOSSY MEDIA ANALYZER - Main Function
% ============================================================================
% Usage:
%   result = lossy_media(epsilon_r, sigma, freq)
%   result = lossy_media(epsilon_r, sigma, freq, mu_r)
%   result = lossy_media(epsilon_r, sigma, freq, mu_r, 'Name')
%
% Inputs:
%   epsilon_r : Relative permittivity (dimensionless)
%   sigma     : Conductivity (S/m)
%   freq      : Frequency (Hz)
%   mu_r      : Relative permeability (default = 1)
%   name      : Material name for display (default = 'Material')
%
% Output:
%   result    : Struct with all computed parameters
%
% Examples:
%   lossy_media(8, 0.01, 5e9)                    % Q26 example
%   lossy_media(5, 10e-12, 10e9, 1, 'Glass')     % Glass at 10 GHz
%   r = lossy_media(12, 0.3, 100e6, 1, 'Tissue') % Store result
% ============================================================================

function result = lossy_media(epsilon_r, sigma, freq, mu_r, name)
    % Handle optional arguments
    if nargin < 4
        mu_r = 1;
    end
    if nargin < 5
        name = 'Material';
    end
    
    % Constants
    eps0 = 8.854e-12;   % Permittivity of free space (F/m)
    mu0 = 4*pi*1e-7;    % Permeability of free space (H/m)
    
    % Derived parameters
    omega = 2*pi*freq;
    eps = eps0 * epsilon_r;
    mu = mu0 * mu_r;
    
    % --- Physics Calculations ---
    j = 1j;
    
    % Complex propagation constant
    gamma = sqrt(j*omega*mu*(sigma + j*omega*eps));
    alpha = real(gamma);  % Attenuation constant (Np/m)
    beta = imag(gamma);   % Phase constant (rad/m)
    
    % Wave parameters
    lambda = 2*pi/beta;          % Wavelength (m)
    up = omega/beta;             % Phase velocity (m/s)
    eta = sqrt(j*omega*mu/(sigma + j*omega*eps));  % Intrinsic impedance (Ohm)
    
    % Loss tangent
    tan_delta = sigma/(omega*eps);
    
    % Classification
    if tan_delta < 0.1
        classification = 'Low-Loss Dielectric (Good Insulator)';
    elseif tan_delta > 10
        classification = 'Good Conductor';
    else
        classification = 'Quasi-Conductor';
    end
    
    % --- Package Results ---
    result.name = name;
    result.frequency = freq;
    result.epsilon_r = epsilon_r;
    result.mu_r = mu_r;
    result.sigma = sigma;
    result.tan_delta = tan_delta;
    result.classification = classification;
    result.alpha = alpha;
    result.beta = beta;
    result.wavelength = lambda;
    result.phase_velocity = up;
    result.impedance = eta;
    result.gamma = gamma;
    
    % --- Display Results ---
    fprintf('\n========================================\n');
    fprintf('  %s @ %.2e Hz\n', name, freq);
    fprintf('========================================\n');
    fprintf('Properties:\n');
    fprintf('  ε_r = %.2f\n', epsilon_r);
    fprintf('  μ_r = %.2f\n', mu_r);
    fprintf('  σ   = %.2e S/m\n', sigma);
    fprintf('\nClassification:\n');
    fprintf('  tan(δ) = %.3e\n', tan_delta);
    fprintf('  Type   = %s\n', classification);
    fprintf('\nWave Parameters:\n');
    fprintf('  α (attenuation) = %.3e Np/m\n', alpha);
    fprintf('  β (phase const) = %.3e rad/m\n', beta);
    fprintf('  λ (wavelength)  = %.3e m\n', lambda);
    fprintf('  u_p (velocity)  = %.3e m/s\n', up);
    fprintf('  η (impedance)   = %.3f + j%.3f Ω\n', real(eta), imag(eta));
    fprintf('========================================\n\n');
end