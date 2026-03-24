function result = poynting_pw(varargin)
% POYNTING_PW - Plane wave Poynting vector and H-field calculator
%
% =========================================================================
% USAGE MODES:
% =========================================================================
%
% MODE 1: Vector phasor (Q22-Q23 exam type)
%   result = poynting_pw(E_phasor, k_hat, eta)
%   result = poynting_pw(E_phasor, beta_vec)        % eta = 377 (air)
%
% MODE 2: From time-domain coefficients (a·cos + b·sin form)
%   result = poynting_pw('time', a, b, E0, beta_vec)
%   result = poynting_pw('time', a, b, E0, beta_vec, eta)
%
% MODE 3: Simple scalar (original)
%   result = poynting_pw(E0, eta, A, phi)
%
% =========================================================================
% OUTPUTS:
% =========================================================================
%   result.E_phasor  - Electric field phasor vector
%   result.H_phasor  - Magnetic field phasor vector
%   result.k_hat     - Propagation direction unit vector
%   result.S_avg     - Time-average Poynting vector [W/m²]
%   result.S_mag     - Magnitude of Poynting vector [W/m²]
%
% =========================================================================
% EXAMPLES (Q22-Q23):
% =========================================================================
%
%   % Given E = E0*[2;1;0]*cos + E0*[0;-1;-2]*sin, β = (2,-4,2)
%   a = [2;1;0]; b = [0;-1;-2]; E0 = 10;
%   beta_vec = [2; -4; 2];
%   r = poynting_pw('time', a, b, E0, beta_vec);
%
%   % Q22 Answer: r.H_phasor (in mA/m)
%   % Q23 Answer: r.S_avg (in W/m²)
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
    elseif nargin == 4 && isscalar(varargin{1}) && isscalar(varargin{2})
        % Original scalar mode: poynting_pw(E0, eta, A, phi)
        mode = "scalar";
        args = varargin;
    else
        % Vector mode: poynting_pw(E_phasor, k_hat, [eta])
        mode = "vector";
        args = varargin;
    end

    % Dispatch
    switch mode
        case "time"
            result = mode_time_domain(args{:});
        case "vector"
            result = mode_vector_phasor(args{:});
        case "scalar"
            result = mode_scalar(args{:});
        otherwise
            error('Unknown mode. Run poynting_pw() for help.');
    end
end

%% ========================================================================
%  MODE: Time-domain coefficients (a·cos + b·sin)
%% ========================================================================
function result = mode_time_domain(a, b, E0, beta_vec, varargin)
    % E = E0*(a*cos(Φ) + b*sin(Φ))
    % Phasor: Ẽ₀ = E0*(a - j*b)
    
    eta = 377;  % Default: air
    if nargin >= 5
        eta = varargin{1};
    end
    
    % Ensure column vectors
    a = a(:);
    b = b(:);
    beta_vec = beta_vec(:);
    
    % Convert to phasor
    E_phasor = E0 * (a - 1j*b);
    
    % Propagation direction
    beta_mag = norm(beta_vec);
    k_hat = beta_vec / beta_mag;
    
    % H-field phasor: H = (1/η) * k̂ × E
    H_phasor = (1/eta) * cross(k_hat, E_phasor);
    
    % Time-average Poynting vector: S̄ = (1/2)*Re{E × H*}
    S_avg = 0.5 * real(cross(E_phasor, conj(H_phasor)));
    S_mag = norm(S_avg);
    
    % Pack results
    result.a = a;
    result.b = b;
    result.E0 = E0;
    result.E_phasor = E_phasor;
    result.H_phasor = H_phasor;
    result.beta_vec = beta_vec;
    result.beta_mag = beta_mag;
    result.k_hat = k_hat;
    result.eta = eta;
    result.S_avg = S_avg;
    result.S_mag = S_mag;
    
    % Display
    print_vector_results(result);
end

%% ========================================================================
%  MODE: Vector phasor input
%% ========================================================================
function result = mode_vector_phasor(E_phasor, beta_or_k, varargin)
    eta = 377;  % Default: air
    
    E_phasor = E_phasor(:);
    beta_or_k = beta_or_k(:);
    
    % Check if it's beta_vec or k_hat
    if abs(norm(beta_or_k) - 1) < 0.01
        k_hat = beta_or_k;
        beta_mag = NaN;
    else
        beta_mag = norm(beta_or_k);
        k_hat = beta_or_k / beta_mag;
    end
    
    if nargin >= 3
        eta = varargin{1};
    end
    
    % H-field phasor
    H_phasor = (1/eta) * cross(k_hat, E_phasor);
    
    % Time-average Poynting vector
    S_avg = 0.5 * real(cross(E_phasor, conj(H_phasor)));
    S_mag = norm(S_avg);
    
    % Pack results
    result.E_phasor = E_phasor;
    result.H_phasor = H_phasor;
    result.k_hat = k_hat;
    result.beta_mag = beta_mag;
    result.eta = eta;
    result.S_avg = S_avg;
    result.S_mag = S_mag;
    
    % Display
    print_vector_results(result);
end

%% ========================================================================
%  MODE: Original scalar mode
%% ========================================================================
function result = mode_scalar(E0, eta, A, phi)
    S_mag = (abs(E0)^2) / (2*abs(eta));
    P_inc = S_mag * A * cos(phi);
    
    result.E0 = E0;
    result.eta = eta;
    result.A = A;
    result.phi = phi;
    result.S_mag = S_mag;
    result.P_incident = P_inc;
    
    fprintf('\n=== Poynting Vector (Scalar) ===\n');
    fprintf('  |E₀| = %.4f V/m\n', abs(E0));
    fprintf('  η = %.2f Ω\n', abs(eta));
    fprintf('  |S̄| = |E₀|²/(2η) = %.4f W/m²\n', S_mag);
    fprintf('  P_incident = %.4f W\n', P_inc);
    fprintf('================================\n\n');
end

%% ========================================================================
%  DISPLAY
%% ========================================================================
function print_vector_results(r)
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('   PLANE WAVE: H-FIELD & POYNTING (Q22-Q23)\n');
    fprintf('==========================================\n');
    
    % E-field phasor
    fprintf('  Ẽ₀ = [%.1f%+.1fj; %.1f%+.1fj; %.1f%+.1fj] V/m\n', ...
        real(r.E_phasor(1)), imag(r.E_phasor(1)), ...
        real(r.E_phasor(2)), imag(r.E_phasor(2)), ...
        real(r.E_phasor(3)), imag(r.E_phasor(3)));
    
    fprintf('  k̂ = [%.4f, %.4f, %.4f]\n', r.k_hat(1), r.k_hat(2), r.k_hat(3));
    fprintf('  η = %.0f Ω\n', r.eta);
    
    fprintf('------------------------------------------\n');
    
    % H-field phasor (Q22)
    fprintf('  Q22: H̃₀ = (1/η)·k̂ × Ẽ₀\n');
    fprintf('  H̃₀ = [%.2f%+.2fj; %.2f%+.2fj; %.2f%+.2fj] mA/m\n', ...
        real(r.H_phasor(1))*1e3, imag(r.H_phasor(1))*1e3, ...
        real(r.H_phasor(2))*1e3, imag(r.H_phasor(2))*1e3, ...
        real(r.H_phasor(3))*1e3, imag(r.H_phasor(3))*1e3);
    
    fprintf('------------------------------------------\n');
    
    % Poynting vector (Q23)
    fprintf('  Q23: S̄ = ½·Re{Ẽ × H̃*}\n');
    fprintf('  S̄ = [%.3f; %.3f; %.3f] W/m²\n', r.S_avg(1), r.S_avg(2), r.S_avg(3));
    fprintf('  |S̄| = %.3f W/m²\n', r.S_mag);
    
    fprintf('==========================================\n\n');
end

function print_help()
    fprintf('\n');
    fprintf('POYNTING_PW - Plane Wave H-field & Poynting Vector\n');
    fprintf('==================================================\n\n');
    fprintf('For Q22-Q23 type problems:\n\n');
    fprintf('  %% Given: E = E0*(a*cos + b*sin), β vector\n');
    fprintf('  a = [2;1;0]; b = [0;-1;-2]; E0 = 10;\n');
    fprintf('  beta_vec = [2; -4; 2];\n');
    fprintf('  r = poynting_pw(''time'', a, b, E0, beta_vec);\n\n');
    fprintf('  %% Results:\n');
    fprintf('  %%   r.H_phasor → Q22 answer (mA/m)\n');
    fprintf('  %%   r.S_avg    → Q23 answer (W/m²)\n\n');
end