function result = PlaneWaveCheck(varargin)
% PLANEWAVECHECK - Complete plane wave verification
%
% =========================================================================
% WHICH MODE SHOULD I USE? (Decision Guide)
% =========================================================================
%
%   What format is your problem?
%   │
%   ├─► γ = [j...; ...; ...] given separately    (Format A)
%   │   │
%   │   │   Example: E₀ = [2;0;0], H₀ = [0;-5.3e-3;0], γ = [0;0;j3]
%   │   │
%   │   └─► Use MAXWELL mode
%   │       PlaneWaveCheck('maxwell', E0, H0, gamma)
%   │
%   └─► exp(-j(ax + by + cz)) in field expression (Format B)
%       │
%       │   Example: E = E₀[0;j;0] exp(-j(20x+10z))
%       │
%       └─► Use FULL mode (extracts k from phase term)
%           PlaneWaveCheck('full', E, H, k, eta)
%
%   ⚠️  Basic mode is only a quick sanity check - use 'full' for exams!
%
% =========================================================================
% USAGE MODES:
% =========================================================================
%
% MODE 1: Basic orthogonality check (QUICK SANITY CHECK ONLY)
%   result = PlaneWaveCheck(E_vec, H_vec, k_vec)
%   ⚠️  This only checks orthogonality, NOT the impedance relation!
%   ⚠️  For exam problems, use 'full' mode instead.
%
% MODE 2: Full verification (FOR FORMAT B - exp term problems)
%   result = PlaneWaveCheck('full', E, H, k)           % η = 377 Ω
%   result = PlaneWaveCheck('full', E, H, k, eta)      % custom η
%   ✓ Checks: orthogonality + H = (1/η)(k̂ × E) + Poynting direction
%
% MODE 3: Maxwell verification (FOR FORMAT A - γ given explicitly)  
%   result = PlaneWaveCheck('maxwell', E0, H0, gamma)
%   ✓ Checks: Maxwell curl equations with physical ωε and ωμ
%   ✓ Catches cases where fields are orthogonal but physically impossible
%
% =========================================================================
% THE 4-STEP VERIFICATION (Formelsamling):
% =========================================================================
%
% STEP 1 - ORTHOGONALITY (all must ≈ 0):
%   • k · E = 0   (E transverse to propagation)
%   • k · H = 0   (H transverse to propagation)  ← Often forgotten!
%   • E · H = 0   (E perpendicular to H)
%
% STEP 2 - NORMALIZE k:
%   • k̂ = k / |k|
%
% STEP 3 - IMPEDANCE RELATION (required for valid plane wave!):
%   • H = (1/η)(k̂ × E)   where η₀ ≈ 377 Ω for free space
%
% STEP 4 - POYNTING DIRECTION:
%   • (E × H) · k > 0   (power flows in k direction)
%
% If ANY step fails → NOT a valid uniform plane wave
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % FORMAT B: E = 5ŷ·exp(-j(20x+10z)), H = (1/120π)ẑ·exp(-j(20x+10z))
%   % Extract: E direction = ŷ, H direction = ẑ, k = [20;0;10]
%   E = [0; 5; 0];              % 5 V/m in ŷ
%   H = [0; 0; 1/(120*pi)];     % A/m in ẑ
%   k = [20; 0; 10];            % From phase term
%   PlaneWaveCheck('full', E, H, k)
%
%   % FORMAT A: Given E₀, H₀, γ explicitly (Q1 type - NOT a plane wave)
%   E0 = [2; 0; 0];
%   H0 = [0; -5.309e-3; 0];
%   gamma = [0; 0; 1j*3];       % Note: j3 → 1j*3 in MATLAB
%   PlaneWaveCheck('maxwell', E0, H0, gamma)
%   % → ωε is NEGATIVE → NOT a plane wave!
%
%   % FORMAT A: Q2 type - IS a valid plane wave
%   E0 = [0; 1j*2; 5];
%   H0 = [0; -37.5e-3; 1j*15e-3];
%   gamma = [1j*10; 0; 0];
%   PlaneWaveCheck('maxwell', E0, H0, gamma)
%   % → ωε and ωμ both positive → IS a plane wave!
%
%   % Run demo to see all examples
%   PlaneWaveCheck()
%
% =========================================================================

    if nargin == 0
        print_help();
        run_demo();
        return;
    end

    %% ====================================================================
    %  INPUT PARSING
    %% ====================================================================
    
    % Default values
    eta = 377;          % Free space impedance (Guideline #3)
    full_mode = false;
    tol = 1e-6;         % Tolerance per Guideline #1 MATLAB tip
    
    % Parse input mode
    if ischar(varargin{1}) || isstring(varargin{1})
        mode = lower(string(varargin{1}));
        
        if mode == "full"
            % FULL MODE: Complete verification with impedance
            full_mode = true;
            E_vec = varargin{2}(:);
            H_vec = varargin{3}(:);
            k_vec = varargin{4}(:);
            if nargin >= 5
                eta = varargin{5};
            end
            
        elseif mode == "phasor"
            % PHASOR MODE: Extract directions from complex phasors
            E_phasor = varargin{2}(:);
            H_phasor = varargin{3}(:);
            k_vec = varargin{4}(:);
            E_vec = get_direction(E_phasor);
            H_vec = get_direction(H_phasor);
            
        elseif mode == "maxwell"
            % MAXWELL MODE: Full Maxwell equation verification
            % This is the most rigorous check using complex phasors
            result = mode_maxwell(varargin{2:end});
            return;  % Early return - maxwell mode handles its own output
            
        else
            error('Unknown mode: %s. Use PlaneWaveCheck() for help.', mode);
        end
        
    elseif nargin == 3
        % MODE 1: E_vec, H_vec, k_vec
        E_vec = varargin{1}(:);
        H_vec = varargin{2}(:);
        k_vec = varargin{3}(:);
        
    elseif nargin == 5
        % MODE 2: E_vec, H_vec, kx, ky, kz
        E_vec = varargin{1}(:);
        H_vec = varargin{2}(:);
        k_vec = [varargin{3}; varargin{4}; varargin{5}];
        
    else
        error('Invalid arguments. Use PlaneWaveCheck() for help.');
    end

    % Ensure 3D vectors
    if length(E_vec) == 2, E_vec = [E_vec; 0]; end
    if length(H_vec) == 2, H_vec = [H_vec; 0]; end
    if length(k_vec) == 2, k_vec = [k_vec; 0]; end

    %% ====================================================================
    %  STEP 1: ORTHOGONALITY CHECK (Guideline #1)
    %% ====================================================================
    % Check dot products with tolerance for floating-point errors
    
    % Scale tolerance by vector magnitudes
    scale = max([norm(k_vec), norm(E_vec), norm(H_vec), 1]);
    tol_scaled = tol * scale;
    
    % Calculate dot products
    k_dot_E = dot(k_vec, E_vec);
    k_dot_H = dot(k_vec, H_vec);
    E_dot_H = dot(E_vec, H_vec);
    
    % Check conditions
    cond1_pass = abs(k_dot_E) < tol_scaled;  % k · E ≈ 0
    cond2_pass = abs(k_dot_H) < tol_scaled;  % k · H ≈ 0
    cond3_pass = abs(E_dot_H) < tol_scaled;  % E · H ≈ 0
    
    orthogonality_pass = cond1_pass && cond2_pass && cond3_pass;

    %% ====================================================================
    %  STEP 2: NORMALIZE k (Guideline #2)
    %% ====================================================================
    % Must use unit vector k̂ for cross product relations
    
    k_mag = norm(k_vec);
    if k_mag > 0
        k_hat = k_vec / k_mag;  % k̂ = k / |k|
    else
        k_hat = [0; 0; 0];
        warning('k vector has zero magnitude!');
    end

    %% ====================================================================
    %  STEP 3: CROSS PRODUCT & IMPEDANCE CHECK (Guideline #3)
    %% ====================================================================
    % Verify H = (1/η)(k̂ × E)
    
    cond4_pass = true;      % Default for basic mode
    H_expected = [];
    impedance_error = NaN;
    
    if full_mode
        % Calculate expected H from E using the plane wave relation
        % H = (1/η)(k̂ × E)
        H_expected = (1/eta) * cross(k_hat, E_vec);
        
        % Calculate relative error
        H_diff = norm(H_vec - H_expected);
        H_ref = max(norm(H_vec), norm(H_expected));
        
        if H_ref > tol
            impedance_error = H_diff / H_ref;
            cond4_pass = impedance_error < 0.01;  % 1% tolerance
        else
            % Both H vectors are essentially zero
            impedance_error = 0;
            cond4_pass = true;
        end
    end

    %% ====================================================================
    %  STEP 4: RIGHT-HAND RULE / POYNTING VECTOR (Guideline #4)
    %% ====================================================================
    % Verify (E × H) points in direction of k
    
    cond5_pass = true;      % Default for basic mode
    poynting_vec = cross(E_vec, H_vec);
    poynting_dot_k = dot(poynting_vec, k_vec);
    
    if full_mode
        % E × H should point in same direction as k (positive dot product)
        % Allow small negative values due to numerical errors
        cond5_pass = poynting_dot_k > -tol_scaled;
    end

    %% ====================================================================
    %  STEP 5: (Optional) PHASOR PHASE CONSISTENCY (Guideline #5)
    %% ====================================================================
    % In lossless medium, E and H should be in phase
    % For lossy medium, phase difference relates to η
    % This is implicit in the H = (1/η)(k̂ × E) check when η is complex
    
    %% ====================================================================
    %  OVERALL RESULT
    %% ====================================================================
    
    if full_mode
        is_plane_wave = cond1_pass && cond2_pass && cond3_pass && ...
                        cond4_pass && cond5_pass;
        verification_complete = true;
    else
        % Basic mode: only orthogonality - CANNOT determine definitively!
        % Orthogonality is NECESSARY but NOT SUFFICIENT for plane wave
        is_plane_wave = [];  % Empty = UNKNOWN (cannot determine without full check)
        verification_complete = false;
    end

    %% ====================================================================
    %  PACK RESULTS
    %% ====================================================================
    
    result.is_plane_wave = is_plane_wave;
    result.full_mode = full_mode;
    result.verification_complete = verification_complete;
    result.tolerance = tol;
    
    % Input vectors
    result.E_vec = E_vec;
    result.H_vec = H_vec;
    result.k_vec = k_vec;
    
    % Step 1: Orthogonality
    result.k_dot_E = k_dot_E;
    result.k_dot_H = k_dot_H;
    result.E_dot_H = E_dot_H;
    result.cond1_pass = cond1_pass;
    result.cond2_pass = cond2_pass;
    result.cond3_pass = cond3_pass;
    result.orthogonality_pass = orthogonality_pass;
    
    % Step 2: Normalization
    result.k_hat = k_hat;
    result.k_mag = k_mag;
    
    % Step 3: Impedance relation (full mode)
    if full_mode
        result.eta = eta;
        result.H_expected = H_expected;
        result.impedance_error = impedance_error;
        result.cond4_pass = cond4_pass;
    end
    
    % Step 4: Poynting vector (full mode)
    result.poynting_vec = poynting_vec;
    result.poynting_dot_k = poynting_dot_k;
    if full_mode
        result.cond5_pass = cond5_pass;
    end

    %% ====================================================================
    %  DISPLAY RESULTS
    %% ====================================================================
    print_results(result);
end

%% ========================================================================
%  MAXWELL MODE - Full Maxwell Equation Verification
%% ========================================================================
function result = mode_maxwell(E0, H0, gamma)
% MAXWELL MODE: Verifies the full Maxwell phasor relations
%
% For a uniform plane wave in a lossless medium:
%   γ × H₀ = -jωε E₀
%   γ × E₀ = +jωμ H₀
%   γ · E₀ = 0
%   γ · H₀ = 0
%
% This mode checks that ωε and ωμ are REAL, POSITIVE, and CONSISTENT.
% This catches cases where fields are orthogonal but don't satisfy
% Maxwell's equations with physical material parameters.

    % Ensure column vectors
    E0 = E0(:);
    H0 = H0(:);
    gamma = gamma(:);
    
    % Pad to 3D if needed
    if length(E0) == 2, E0 = [E0; 0]; end
    if length(H0) == 2, H0 = [H0; 0]; end
    if length(gamma) == 2, gamma = [gamma; 0]; end
    
    % Tolerances
    tol = 1e-10;           % General tolerance for floating-point checks
    tol_consist = 1e-9;    % Tolerance for ωε/ωμ consistency
    
    %% Step 1: Transverse checks (E ⊥ γ, H ⊥ γ)
    dotEg = dot(E0, gamma);
    dotHg = dot(H0, gamma);
    trans_ok = abs(dotEg) < tol * max(norm(E0)*norm(gamma), 1) && ...
               abs(dotHg) < tol * max(norm(H0)*norm(gamma), 1);
    
    %% Step 2: Cross products (from Maxwell relations)
    % γ × H₀ = -jωε E₀
    % γ × E₀ = +jωμ H₀
    gXH = cross(gamma, H0);
    gXE = cross(gamma, E0);
    
    % Scale-invariant parallelism residuals (should be ~0 for parallel)
    par1 = norm(cross(gXH, E0)) / max(norm(gXH)*norm(E0), eps);
    par2 = norm(cross(gXE, H0)) / max(norm(gXE)*norm(H0), eps);
    parallel_ok = par1 < 1e-9 && par2 < 1e-9;
    
    %% Step 3: Recover ωε and ωμ from available components
    % γ × H₀ = -jωε E₀  →  ωε = -(γ×H₀) / (j·E₀)
    % γ × E₀ = +jωμ H₀  →  ωμ = +(γ×E₀) / (j·H₀)
    omega_eps = [];
    omega_mu = [];
    
    for k = 1:3
        if abs(E0(k)) > tol
            omega_eps(end+1) = (-gXH(k)) / (1j * E0(k));
        end
        if abs(H0(k)) > tol
            omega_mu(end+1) = (gXE(k)) / (1j * H0(k));
        end
    end
    
    %% Step 4: Physical sanity checks
    % ωε and ωμ must be REAL (imaginary part ≈ 0)
    eps_real_ok = isempty(omega_eps) || all(abs(imag(omega_eps)) < tol);
    mu_real_ok = isempty(omega_mu) || all(abs(imag(omega_mu)) < tol);
    
    % ωε and ωμ must be POSITIVE (for lossless passive media)
    eps_pos_ok = isempty(omega_eps) || all(real(omega_eps) > -tol);
    mu_pos_ok = isempty(omega_mu) || all(real(omega_mu) > -tol);
    
    % ωε and ωμ must be CONSISTENT across components
    eps_vals = real(omega_eps);
    mu_vals = real(omega_mu);
    eps_consist = isempty(eps_vals) || (max(eps_vals) - min(eps_vals) < tol_consist);
    mu_consist = isempty(mu_vals) || (max(mu_vals) - min(mu_vals) < tol_consist);
    
    %% Step 5: Combined decision
    is_plane_wave = trans_ok && parallel_ok && ...
                    eps_real_ok && eps_pos_ok && eps_consist && ...
                    mu_real_ok && mu_pos_ok && mu_consist;
    
    %% Pack results
    result.mode = 'maxwell';
    result.is_plane_wave = is_plane_wave;
    
    % Input vectors
    result.E0 = E0;
    result.H0 = H0;
    result.gamma = gamma;
    
    % Transverse checks
    result.E_dot_gamma = dotEg;
    result.H_dot_gamma = dotHg;
    result.trans_ok = trans_ok;
    
    % Cross products
    result.gamma_cross_H = gXH;
    result.gamma_cross_E = gXE;
    result.parallelism_residual_1 = par1;
    result.parallelism_residual_2 = par2;
    result.parallel_ok = parallel_ok;
    
    % ωε and ωμ values
    result.omega_eps = omega_eps;
    result.omega_mu = omega_mu;
    result.eps_real_ok = eps_real_ok;
    result.eps_pos_ok = eps_pos_ok;
    result.eps_consist = eps_consist;
    result.mu_real_ok = mu_real_ok;
    result.mu_pos_ok = mu_pos_ok;
    result.mu_consist = mu_consist;
    
    %% Display results
    print_maxwell_results(result);
end

function print_maxwell_results(r)
    fprintf('\n');
    fprintf('══════════════════════════════════════════════════════════════════\n');
    fprintf('     MAXWELL PLANE WAVE VERIFICATION (Cross-Product Method)       \n');
    fprintf('══════════════════════════════════════════════════════════════════\n');
    
    % Input vectors (handle complex display)
    fprintf('  INPUT PHASORS:\n');
    print_complex_vector('    E₀', r.E0, 'V/m');
    print_complex_vector('    H₀', r.H0, 'A/m');
    print_complex_vector('    γ ', r.gamma, 'm⁻¹');
    
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 1: TRANSVERSE CHECK (γ·E₀ = 0, γ·H₀ = 0)\n');
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('    E₀ · γ = %.3e %+.3ej', real(r.E_dot_gamma), imag(r.E_dot_gamma));
    if abs(r.E_dot_gamma) < 1e-9
        fprintf('   ✓ (≈ 0)\n');
    else
        fprintf('   ✗ (≠ 0)\n');
    end
    fprintf('    H₀ · γ = %.3e %+.3ej', real(r.H_dot_gamma), imag(r.H_dot_gamma));
    if abs(r.H_dot_gamma) < 1e-9
        fprintf('   ✓ (≈ 0)\n');
    else
        fprintf('   ✗ (≠ 0)\n');
    end
    
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 2: PARALLELISM CHECK\n');
    fprintf('  (γ × H₀) ∥ E₀  and  (γ × E₀) ∥ H₀\n');
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('    Residual 1 (γ×H₀ ∥ E₀): %.3e', r.parallelism_residual_1);
    if r.parallelism_residual_1 < 1e-9
        fprintf('   ✓ (parallel)\n');
    else
        fprintf('   ✗ (not parallel)\n');
    end
    fprintf('    Residual 2 (γ×E₀ ∥ H₀): %.3e', r.parallelism_residual_2);
    if r.parallelism_residual_2 < 1e-9
        fprintf('   ✓ (parallel)\n');
    else
        fprintf('   ✗ (not parallel)\n');
    end
    
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 3: MAXWELL RELATIONS\n');
    fprintf('  γ × H₀ = -jωε E₀   →   ωε = -(γ×H₀)/(jE₀)\n');
    fprintf('  γ × E₀ = +jωμ H₀   →   ωμ = +(γ×E₀)/(jH₀)\n');
    fprintf('──────────────────────────────────────────────────────────────────\n');
    
    % Display ωε values
    fprintf('    ωε components: ');
    if isempty(r.omega_eps)
        fprintf('(none computed)\n');
    else
        for i = 1:length(r.omega_eps)
            if i > 1, fprintf(', '); end
            fprintf('%.6g%+.2gj', real(r.omega_eps(i)), imag(r.omega_eps(i)));
        end
        fprintf('\n');
    end
    
    % Display ωμ values
    fprintf('    ωμ components: ');
    if isempty(r.omega_mu)
        fprintf('(none computed)\n');
    else
        for i = 1:length(r.omega_mu)
            if i > 1, fprintf(', '); end
            fprintf('%.6g%+.2gj', real(r.omega_mu(i)), imag(r.omega_mu(i)));
        end
        fprintf('\n');
    end
    
    fprintf('──────────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 4: PHYSICAL SANITY CHECKS\n');
    fprintf('  ωε and ωμ must be REAL, POSITIVE, and CONSISTENT\n');
    fprintf('──────────────────────────────────────────────────────────────────\n');
    
    fprintf('    ωε real?       ');
    if r.eps_real_ok, fprintf('✓ YES\n'); else, fprintf('✗ NO (has imaginary part)\n'); end
    
    fprintf('    ωε positive?   ');
    if r.eps_pos_ok, fprintf('✓ YES\n'); else, fprintf('✗ NO (negative or zero)\n'); end
    
    fprintf('    ωε consistent? ');
    if r.eps_consist, fprintf('✓ YES\n'); else, fprintf('✗ NO (different values)\n'); end
    
    fprintf('    ωμ real?       ');
    if r.mu_real_ok, fprintf('✓ YES\n'); else, fprintf('✗ NO (has imaginary part)\n'); end
    
    fprintf('    ωμ positive?   ');
    if r.mu_pos_ok, fprintf('✓ YES\n'); else, fprintf('✗ NO (negative or zero)\n'); end
    
    fprintf('    ωμ consistent? ');
    if r.mu_consist, fprintf('✓ YES\n'); else, fprintf('✗ NO (different values)\n'); end
    
    fprintf('══════════════════════════════════════════════════════════════════\n');
    
    % Final verdict
    if r.is_plane_wave
        fprintf('  ✓ RESULT: This IS a valid UNIFORM PLANE WAVE\n');
        fprintf('    Maxwell relations satisfied with physical ωε and ωμ.\n');
        if ~isempty(r.omega_eps) && ~isempty(r.omega_mu)
            fprintf('    ωε = %.6g,  ωμ = %.6g\n', mean(real(r.omega_eps)), mean(real(r.omega_mu)));
        end
    else
        fprintf('  ✗ RESULT: This is NOT a valid plane wave\n');
        fprintf('    Failed checks: ');
        reasons = {};
        if ~r.trans_ok
            reasons{end+1} = 'not transverse';
        end
        if ~r.parallel_ok
            reasons{end+1} = 'cross products not parallel';
        end
        if ~r.eps_real_ok
            reasons{end+1} = 'ωε not real';
        end
        if ~r.eps_pos_ok
            reasons{end+1} = 'ωε not positive';
        end
        if ~r.eps_consist
            reasons{end+1} = 'ωε not consistent';
        end
        if ~r.mu_real_ok
            reasons{end+1} = 'ωμ not real';
        end
        if ~r.mu_pos_ok
            reasons{end+1} = 'ωμ not positive';
        end
        if ~r.mu_consist
            reasons{end+1} = 'ωμ not consistent';
        end
        fprintf('%s\n', strjoin(reasons, ', '));
    end
    fprintf('══════════════════════════════════════════════════════════════════\n\n');
end

function print_complex_vector(name, vec, unit)
    % Print a complex vector nicely
    fprintf('%s = [', name);
    for i = 1:length(vec)
        if i > 1, fprintf('; '); end
        re = real(vec(i));
        im = imag(vec(i));
        if abs(im) < 1e-15
            fprintf('%.4g', re);
        elseif abs(re) < 1e-15
            fprintf('j%.4g', im);
        else
            fprintf('%.4g%+.4gj', re, im);
        end
    end
    fprintf('] %s\n', unit);
end

%% ========================================================================
%  HELPER FUNCTIONS
%% ========================================================================

function dir = get_direction(phasor)
    % Extract direction vector from complex phasor
    % Uses magnitude of each component
    
    phasor = phasor(:);
    mags = abs(phasor);
    
    if max(mags) < 1e-15
        dir = [0; 0; 0];
        return;
    end
    
    % Create direction from magnitudes
    dir = mags;
    dir = dir / norm(dir);
end

function print_results(r)
    fprintf('\n');
    fprintf('══════════════════════════════════════════════════════════════\n');
    fprintf('         PLANE WAVE VERIFICATION (Formelsamling Method)       \n');
    fprintf('══════════════════════════════════════════════════════════════\n');
    
    % Display input vectors
    fprintf('  INPUT VECTORS:\n');
    fprintf('    k = [%.4g, %.4g, %.4g]  (|k| = %.4g)\n', ...
        r.k_vec(1), r.k_vec(2), r.k_vec(3), r.k_mag);
    fprintf('    E = [%.4g, %.4g, %.4g]\n', r.E_vec(1), r.E_vec(2), r.E_vec(3));
    fprintf('    H = [%.4g, %.4g, %.4g]\n', r.H_vec(1), r.H_vec(2), r.H_vec(3));
    
    fprintf('──────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 1: ORTHOGONALITY CHECK (Guideline #1)\n');
    fprintf('  Tolerance: %.0e\n', r.tolerance);
    fprintf('──────────────────────────────────────────────────────────────\n');
    
    % Condition 1: k · E = 0
    fprintf('    1. k · E = %.6g', r.k_dot_E);
    if r.cond1_pass
        fprintf('   ✓ PASS (E ⊥ k)\n');
    else
        fprintf('   ✗ FAIL (E not ⊥ k)\n');
    end
    
    % Condition 2: k · H = 0
    fprintf('    2. k · H = %.6g', r.k_dot_H);
    if r.cond2_pass
        fprintf('   ✓ PASS (H ⊥ k)\n');
    else
        fprintf('   ✗ FAIL (H not ⊥ k)\n');
    end
    
    % Condition 3: E · H = 0
    fprintf('    3. E · H = %.6g', r.E_dot_H);
    if r.cond3_pass
        fprintf('   ✓ PASS (E ⊥ H)\n');
    else
        fprintf('   ✗ FAIL (E not ⊥ H)\n');
    end
    
    fprintf('──────────────────────────────────────────────────────────────\n');
    fprintf('  STEP 2: NORMALIZE k (Guideline #2)\n');
    fprintf('──────────────────────────────────────────────────────────────\n');
    fprintf('    k̂ = k/|k| = [%.4f, %.4f, %.4f]\n', ...
        r.k_hat(1), r.k_hat(2), r.k_hat(3));
    
    if r.full_mode
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('  STEP 3: IMPEDANCE RELATION (Guideline #3)\n');
        fprintf('  H = (1/η)(k̂ × E),  η = %.2f Ω\n', r.eta);
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('    Expected H = [%.4g, %.4g, %.4g]\n', ...
            r.H_expected(1), r.H_expected(2), r.H_expected(3));
        fprintf('    Actual   H = [%.4g, %.4g, %.4g]\n', ...
            r.H_vec(1), r.H_vec(2), r.H_vec(3));
        fprintf('    4. H = (1/η)(k̂ × E)');
        if r.cond4_pass
            fprintf('   ✓ PASS (error = %.2f%%)\n', r.impedance_error*100);
        else
            fprintf('   ✗ FAIL (error = %.1f%%)\n', r.impedance_error*100);
        end
        
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('  STEP 4: RIGHT-HAND RULE (Guideline #4)\n');
        fprintf('  (E × H) should point in direction of k\n');
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('    S = E × H = [%.4g, %.4g, %.4g]\n', ...
            r.poynting_vec(1), r.poynting_vec(2), r.poynting_vec(3));
        fprintf('    (E × H) · k = %.6g', r.poynting_dot_k);
        if r.cond5_pass
            fprintf('   ✓ PASS (S || k)\n');
        else
            fprintf('   ✗ FAIL (S not || k)\n');
        end
    else
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('  ⚠️  STEPS 3-4 NOT CHECKED (Basic mode)\n');
        fprintf('──────────────────────────────────────────────────────────────\n');
        fprintf('    Basic mode only checks orthogonality.\n');
        fprintf('    For exam problems, use ''full'' mode to also verify:\n');
        fprintf('      • Step 3: H = (1/η)(k̂ × E)\n');
        fprintf('      • Step 4: (E × H) · k > 0\n');
    end
    
    fprintf('══════════════════════════════════════════════════════════════\n');
    
    % Final verdict
    if r.full_mode
        % Full mode: can give definitive answer
        if r.is_plane_wave
            fprintf('  ✓ RESULT: This IS a valid UNIFORM PLANE WAVE\n');
            fprintf('    All 4 steps verified.\n');
        else
            fprintf('  ✗ RESULT: This is NOT a valid plane wave\n');
            fprintf('    Failed conditions: ');
            reasons = {};
            if ~r.cond1_pass, reasons{end+1} = 'k·E≠0'; end
            if ~r.cond2_pass, reasons{end+1} = 'k·H≠0'; end
            if ~r.cond3_pass, reasons{end+1} = 'E·H≠0'; end
            if ~r.cond4_pass, reasons{end+1} = 'H≠(1/η)(k̂×E)'; end
            if ~r.cond5_pass, reasons{end+1} = '(E×H)·k<0'; end
            fprintf('%s\n', strjoin(reasons, ', '));
        end
    else
        % Basic mode: can only rule OUT, not confirm
        if ~r.orthogonality_pass
            fprintf('  ✗ RESULT: DEFINITELY NOT a plane wave\n');
            fprintf('    Failed orthogonality: ');
            reasons = {};
            if ~r.cond1_pass, reasons{end+1} = 'k·E≠0'; end
            if ~r.cond2_pass, reasons{end+1} = 'k·H≠0'; end
            if ~r.cond3_pass, reasons{end+1} = 'E·H≠0'; end
            fprintf('%s\n', strjoin(reasons, ', '));
        else
            fprintf('  ⚠️  RESULT: CANNOT DETERMINE (verification incomplete)\n');
            fprintf('    Orthogonality OK, but impedance relation NOT checked.\n');
            fprintf('    \n');
            fprintf('    → Use PlaneWaveCheck(''full'', E, H, k) for definitive answer\n');
            fprintf('    → Or  PlaneWaveCheck(''maxwell'', E0, H0, gamma) for complex phasors\n');
        end
    end
    fprintf('══════════════════════════════════════════════════════════════\n\n');
end

function print_help()
    fprintf('\n');
    fprintf('PLANEWAVECHECK - Plane Wave Verification\n');
    fprintf('=========================================\n\n');
    fprintf('┌─────────────────────────────────────────────────────────────┐\n');
    fprintf('│              WHICH MODE SHOULD I USE?                       │\n');
    fprintf('├─────────────────────────────────────────────────────────────┤\n');
    fprintf('│                                                             │\n');
    fprintf('│  What format is your problem?                               │\n');
    fprintf('│  │                                                          │\n');
    fprintf('│  ├─► γ = [j...; ...; ...] given separately (Format A)       │\n');
    fprintf('│  │   └─► Use MAXWELL mode                                   │\n');
    fprintf('│  │       PlaneWaveCheck(''maxwell'', E0, H0, gamma)           │\n');
    fprintf('│  │                                                          │\n');
    fprintf('│  └─► exp(-j(ax+by+cz)) in field (Format B)                  │\n');
    fprintf('│      └─► Use FULL mode                                      │\n');
    fprintf('│          PlaneWaveCheck(''full'', E, H, k)                    │\n');
    fprintf('│                                                             │\n');
    fprintf('│  ⚠️  Basic mode is only a quick sanity check!               │\n');
    fprintf('└─────────────────────────────────────────────────────────────┘\n\n');
    fprintf('MODES:\n\n');
    fprintf('  ''full''    → For exp(-j...) problems (Format B)\n');
    fprintf('              Checks: orthogonality + H=(1/η)(k̂×E) + Poynting\n\n');
    fprintf('  ''maxwell'' → For γ given explicitly (Format A)\n');
    fprintf('              Checks: Maxwell curl equations, ωε/ωμ physical\n\n');
    fprintf('  (basic)   → Quick sanity check only (NOT for exams!)\n\n');
end

function run_demo()
    fprintf('═══════════════════════════════════════════════════════════════\n');
    fprintf('                    DEMO EXAMPLES                              \n');
    fprintf('═══════════════════════════════════════════════════════════════\n\n');
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 1: Basic mode (incomplete - can only rule OUT)\n');
    fprintf('  E = x̂, H = ŷ, k = 10ẑ\n');
    fprintf('  Note: Basic mode CANNOT confirm plane wave, only rule out.\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    PlaneWaveCheck([1;0;0], [0;1;0], [0;0;10]);
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 2: E24 Q18 - Invalid (H not ⊥ k)\n');
    fprintf('  E = ŷ, H = ẑ, k = 20x̂ + 10ẑ\n');
    fprintf('  k · H = 10 ≠ 0 → NOT a plane wave!\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    PlaneWaveCheck([0;1;0], [0;0;1], [20;0;10]);
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 3: Full verification - correct H magnitude\n');
    fprintf('  E = 10x̂ V/m, k = 5ẑ, η = 377Ω\n');
    fprintf('  H should be = (1/377)(ẑ × 10x̂) = 10/377 ŷ ≈ 0.0265 ŷ A/m\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    PlaneWaveCheck('full', [10;0;0], [0;10/377;0], [0;0;5], 377);
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 4: Full verification - WRONG H magnitude\n');
    fprintf('  E = 10x̂ V/m, H = 0.1ŷ A/m (should be 0.0265!)\n');
    fprintf('  Orthogonality passes, but impedance relation fails!\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    PlaneWaveCheck('full', [10;0;0], [0;0.1;0], [0;0;5], 377);
    
    fprintf('\n');
    fprintf('═══════════════════════════════════════════════════════════════\n');
    fprintf('            MAXWELL MODE EXAMPLES (Complex Phasors)            \n');
    fprintf('═══════════════════════════════════════════════════════════════\n\n');
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 5: Maxwell mode - Question 1 (NOT a plane wave)\n');
    fprintf('  E₀ = [2; 0; 0] V/m\n');
    fprintf('  H₀ = [0; -5.309; 0] mA/m\n');
    fprintf('  γ  = [0; 0; j3] m⁻¹\n');
    fprintf('  \n');
    fprintf('  Fields are orthogonal, but ωε is NEGATIVE!\n');
    fprintf('  → Cannot be a plane wave in a physical medium.\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    E0_q1 = [2; 0; 0];
    H0_q1 = [0; -5.309e-3; 0];
    gamma_q1 = [0; 0; 1j*3];
    PlaneWaveCheck('maxwell', E0_q1, H0_q1, gamma_q1);
    
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    fprintf('EXAMPLE 6: Maxwell mode - Question 2 (Valid plane wave)\n');
    fprintf('  E₀ = [0; j2; 5] V/m\n');
    fprintf('  H₀ = [0; -37.5; j15] mA/m\n');
    fprintf('  γ  = [j10; 0; 0] m⁻¹\n');
    fprintf('  \n');
    fprintf('  ωε and ωμ are both POSITIVE and CONSISTENT.\n');
    fprintf('  → This IS a valid plane wave!\n');
    fprintf('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    E0_q2 = [0; 1j*2; 5];
    H0_q2 = [0; -37.5e-3; 1j*15e-3];
    gamma_q2 = [1j*10; 0; 0];
    PlaneWaveCheck('maxwell', E0_q2, H0_q2, gamma_q2);
end
