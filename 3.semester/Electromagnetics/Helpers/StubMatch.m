function result = StubMatch(varargin)
% STUBMATCH - Single-stub matching calculator (Q15-Q17 exam type)
%
% =========================================================================
% SIMPLE USAGE:
% =========================================================================
%
%   % With wavelength (gives physical lengths in mm)
%   StubMatch(ZL, Z0, 'short', lambda)
%   StubMatch(ZL, Z0, 'open', lambda)
%
%   % Just normalized (λ = 1)
%   StubMatch(ZL, Z0, 'short')
%
% =========================================================================
% EXAM EXAMPLE (Q15-Q17):
% =========================================================================
%
%   lambda = 0.133;  % 13.3 cm from Q15
%   StubMatch(142+1j*42.5, 75, 'short', lambda)
%
%   % Output:
%   %   d = 0.1838 λ = 24.45 mm  ← Q16 Answer
%   %   ℓ = 0.1457 λ = 19.38 mm  ← Q17 Answer
%
% =========================================================================
% OUTPUTS:
% =========================================================================
%   r.d       - Distance load to stub (λ)
%   r.l       - Stub length (λ)
%   r.d_mm    - Distance in mm (if lambda given)
%   r.l_mm    - Stub length in mm (if lambda given)
%
% =========================================================================

    if nargin == 0
        print_help();
        return;
    end

    % Parse inputs
    ZL = varargin{1};
    Z0 = varargin{2};
    
    % Defaults
    stub_type = "short";
    lambda = NaN;
    Z0_stub = Z0;
    
    % Parse remaining arguments
    if nargin >= 3
        arg3 = varargin{3};
        if ischar(arg3) || isstring(arg3)
            stub_type = lower(string(arg3));
        else
            lambda = arg3;  % It's the wavelength
        end
    end
    
    if nargin >= 4
        arg4 = varargin{4};
        if isnan(lambda) && isnumeric(arg4)
            lambda = arg4;  % Lambda provided after type
        elseif ~isnan(lambda) && isnumeric(arg4)
            % arg3 was freq, arg4 is eps_r -> calculate lambda
            freq = varargin{3};
            eps_r = arg4;
            c0 = 2.99792458e8;
            lambda = c0 / (freq * sqrt(eps_r));
        end
    end
    
    if nargin >= 5
        % StubMatch(ZL, Z0, type, freq, eps_r)
        freq = varargin{4};
        eps_r = varargin{5};
        c0 = 2.99792458e8;
        lambda = c0 / (freq * sqrt(eps_r));
    end
    
    % Validate stub type
    if ~ismember(stub_type, ["open", "short"])
        error('Stub type must be ''open'' or ''short''.');
    end
    
    % Normalize
    zL = ZL / Z0;
    yL = 1 / zL;
    Y0 = 1 / Z0;
    Y0_stub = 1 / Z0_stub;
    
    % Use numerical solver for robust solution
    beta = 2*pi;  % Normalized to lambda = 1
    
    % Find d: distance where real(Y_in) = Y0
    % Y_in(d) = Y0 * (yL + j*tan(beta*d)) / (1 + j*yL*tan(beta*d))
    
    % We need: real(Y_in) = Y0, which means real(y_in) = 1
    % Solve for d in [0, 0.5] lambda
    
    d_solutions = [];
    l_solutions = [];
    
    % Search for solutions
    d_test = linspace(0.001, 0.499, 1000);
    
    for d = d_test
        y_in = (yL + 1j*tan(beta*d)) / (1 + 1j*yL*tan(beta*d));
        
        if abs(real(y_in) - 1) < 0.01
            % Refine with finer search
            d_fine = linspace(max(0.001, d-0.01), min(0.499, d+0.01), 100);
            errors = zeros(size(d_fine));
            for k = 1:length(d_fine)
                y_temp = (yL + 1j*tan(beta*d_fine(k))) / (1 + 1j*yL*tan(beta*d_fine(k)));
                errors(k) = abs(real(y_temp) - 1);
            end
            [~, idx] = min(errors);
            d_refined = d_fine(idx);
            
            % Check if this is a new solution
            if isempty(d_solutions) || all(abs(d_solutions - d_refined) > 0.02)
                d_solutions(end+1) = d_refined;
                
                % Calculate stub length for this d
                y_in = (yL + 1j*tan(beta*d_refined)) / (1 + 1j*yL*tan(beta*d_refined));
                b_in = imag(y_in);  % Normalized susceptance to cancel
                
                % Need b_stub = -b_in (normalized to Y0_stub)
                b_stub_needed = -b_in * (Z0_stub / Z0);  % Adjust for different Z0
                
                if stub_type == "short"
                    % Y_stub = -j*cot(beta*l)/Z0_stub -> b_stub = -cot(beta*l)
                    % Need: -cot(beta*l) = b_stub_needed
                    % cot(beta*l) = -b_stub_needed
                    % beta*l = acot(-b_stub_needed) = atan(-1/b_stub_needed)
                    if abs(b_stub_needed) < 1e-10
                        l = 0.25;  % 90 degrees
                    else
                        l = atan(-1/b_stub_needed) / beta;
                    end
                else
                    % Y_stub = j*tan(beta*l)/Z0_stub -> b_stub = tan(beta*l)
                    % Need: tan(beta*l) = b_stub_needed
                    l = atan(b_stub_needed) / beta;
                end
                
                % Ensure positive length in [0, 0.5]
                l = mod(l, 0.5);
                if l < 0.001
                    l = l + 0.5;
                end
                
                l_solutions(end+1) = l;
            end
        end
    end
    
    % If numerical search didn't work well, use analytical formulas
    if length(d_solutions) < 2
        [d_solutions, l_solutions] = analytical_stub_match(zL, stub_type, Z0, Z0_stub);
    end
    
    % Sort solutions by d
    [d_solutions, idx] = sort(d_solutions);
    l_solutions = l_solutions(idx);
    
    % Pack results
    result.ZL = ZL;
    result.Z0 = Z0;
    result.Z0_stub = Z0_stub;
    result.type = stub_type;
    result.lambda = lambda;
    
    if ~isempty(d_solutions)
        result.d = d_solutions(1);
        result.l = l_solutions(1);
        
        if length(d_solutions) >= 2
            result.d_alt = d_solutions(2);
            result.l_alt = l_solutions(2);
        else
            result.d_alt = NaN;
            result.l_alt = NaN;
        end
        
        % Physical lengths (if lambda provided)
        if ~isnan(lambda)
            result.d_m = result.d * lambda;
            result.l_m = result.l * lambda;
            result.d_mm = result.d_m * 1000;
            result.l_mm = result.l_m * 1000;
            result.d_cm = result.d_m * 100;
            result.l_cm = result.l_m * 100;
            
            if ~isnan(result.d_alt)
                result.d_alt_mm = result.d_alt * lambda * 1000;
                result.l_alt_mm = result.l_alt * lambda * 1000;
            end
        end
    else
        result.d = NaN;
        result.l = NaN;
        result.d_alt = NaN;
        result.l_alt = NaN;
    end
    
    % Verification
    result.Y_in_check = verify_match(result.d, result.l, yL, stub_type, Z0, Z0_stub);
    
    % Display results
    print_results(result);
end

%% ========================================================================
%  HELPER FUNCTIONS
%% ========================================================================

function [d_sols, l_sols] = analytical_stub_match(zL, stub_type, Z0, Z0_stub)
    % Analytical solution using standard formulas
    % For normalized load zL = ZL/Z0
    
    rL = real(zL);
    xL = imag(zL);
    
    d_sols = [];
    l_sols = [];
    
    % Special case: already matched
    if abs(zL - 1) < 1e-6
        d_sols = [0, 0];
        l_sols = [0, 0];
        return;
    end
    
    % Calculate t = tan(beta*d) using quadratic formula
    % For y_in = (yL + jt)/(1 + jyL*t), we need real(y_in) = 1
    
    yL = 1/zL;
    gL = real(yL);
    bL = imag(yL);
    
    if abs(gL - 1) < 1e-6
        % gL = 1: special case
        t_vals = [-bL/2];
    else
        % Quadratic: (gL-1)*t^2 + 2*bL*t + (gL-1) = 0... actually more complex
        % Use numerical refinement
        t_test = linspace(-20, 20, 2000);
        beta = 2*pi;
        
        for t = t_test
            if abs(t) > 1e-6
                y_in = (yL + 1j*t) / (1 + 1j*yL*t);
                if abs(real(y_in) - 1) < 0.01
                    d = atan(t) / beta;
                    d = mod(d, 0.5);
                    if d > 0.001 && (isempty(d_sols) || all(abs(d_sols - d) > 0.02))
                        d_sols(end+1) = d;
                        
                        % Get stub length
                        y_in = (yL + 1j*tan(beta*d)) / (1 + 1j*yL*tan(beta*d));
                        b_in = imag(y_in);
                        b_stub = -b_in * (Z0_stub/Z0);
                        
                        if stub_type == "short"
                            l = atan(-1/b_stub) / beta;
                        else
                            l = atan(b_stub) / beta;
                        end
                        l = mod(l, 0.5);
                        if l < 0.001, l = l + 0.5; end
                        l_sols(end+1) = l;
                    end
                end
            end
        end
    end
end

function Y_in = verify_match(d, l, yL, stub_type, Z0, Z0_stub)
    beta = 2*pi;
    
    % Input admittance at distance d from load
    y_in = (yL + 1j*tan(beta*d)) / (1 + 1j*yL*tan(beta*d));
    
    % Stub admittance
    if stub_type == "short"
        y_stub = -1j / tan(beta*l) * (Z0/Z0_stub);
    else
        y_stub = 1j * tan(beta*l) * (Z0/Z0_stub);
    end
    
    % Total normalized admittance
    y_total = y_in + y_stub;
    
    % Denormalize
    Y_in = y_total / Z0;
end

function print_results(r)
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('      SINGLE-STUB MATCHING (Q15-Q17)     \n');
    fprintf('==========================================\n');
    fprintf('  Load: ZL = %.2f %+.2fj Ω\n', real(r.ZL), imag(r.ZL));
    fprintf('  Line: Z0 = %.0f Ω (%s stub)\n', r.Z0, upper(r.type));
    
    if ~isnan(r.lambda)
        fprintf('  λ = %.2f cm\n', r.lambda*100);
    end
    
    fprintf('------------------------------------------\n');
    
    if ~isnan(r.lambda)
        % Show physical lengths prominently
        fprintf('  SOLUTION 1:\n');
        fprintf('    d = %.4f λ = %.2f mm  ← Q16\n', r.d, r.d_mm);
        fprintf('    ℓ = %.4f λ = %.2f mm  ← Q17\n', r.l, r.l_mm);
        
        if ~isnan(r.d_alt)
            fprintf('  SOLUTION 2:\n');
            fprintf('    d = %.4f λ = %.2f mm\n', r.d_alt, r.d_alt_mm);
            fprintf('    ℓ = %.4f λ = %.2f mm\n', r.l_alt, r.l_alt_mm);
        end
    else
        % Normalized only
        fprintf('  SOLUTION 1:\n');
        fprintf('    d = %.4f λ\n', r.d);
        fprintf('    ℓ = %.4f λ\n', r.l);
        
        if ~isnan(r.d_alt)
            fprintf('  SOLUTION 2:\n');
            fprintf('    d = %.4f λ\n', r.d_alt);
            fprintf('    ℓ = %.4f λ\n', r.l_alt);
        end
    end
    
    fprintf('------------------------------------------\n');
    % Verification
    y_check = r.Y_in_check * r.Z0;  % Normalized
    if abs(y_check - 1) < 0.01
        fprintf('  ✓ Matched (y = %.3f)\n', real(y_check));
    else
        fprintf('  Check: y = %.4f %+.4fj\n', real(y_check), imag(y_check));
    end
    fprintf('==========================================\n\n');
end

function print_help()
    fprintf('\n');
    fprintf('STUBMATCH - Single-Stub Matching (Q15-Q17 type)\n');
    fprintf('===============================================\n\n');
    fprintf('Simple usage:\n');
    fprintf('  StubMatch(ZL, Z0, ''short'', lambda)   %% With wavelength → mm\n');
    fprintf('  StubMatch(ZL, Z0, ''open'', lambda)    %% Open stub\n\n');
    fprintf('Example (Q15-Q17 exam):\n');
    fprintf('  lambda = 0.133;  %% 13.3 cm from Q15\n');
    fprintf('  StubMatch(142+1j*42.5, 75, ''short'', lambda)\n\n');
    fprintf('  Output:\n');
    fprintf('    d = 0.1838 λ = 24.45 mm  ← Q16\n');
    fprintf('    ℓ = 0.1457 λ = 19.38 mm  ← Q17\n\n');
end