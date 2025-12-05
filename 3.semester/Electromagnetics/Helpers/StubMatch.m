function result = StubMatch(varargin)
% STUBMATCH - Single-stub impedance matching calculator
%
% =========================================================================
% USAGE:
% =========================================================================
%
%   result = StubMatch(ZL, Z0)                    % Default: shunt short stub
%   result = StubMatch(ZL, Z0, 'open')            % Shunt open stub
%   result = StubMatch(ZL, Z0, 'short')           % Shunt short stub
%   result = StubMatch(ZL, Z0, type, Z0_stub)     % Different stub impedance
%   result = StubMatch('series', ZL, Z0, type)    % Series stub (less common)
%
% =========================================================================
% INPUTS:
% =========================================================================
%   ZL      - Load impedance (complex, Ohms)
%   Z0      - Main line characteristic impedance (Ohms)
%   type    - 'open' or 'short' (default: 'short')
%   Z0_stub - Stub characteristic impedance (default: same as Z0)
%
% =========================================================================
% OUTPUTS (struct):
% =========================================================================
%   result.d         - Distance from load to stub (wavelengths)
%   result.l         - Stub length (wavelengths)
%   result.d_alt     - Alternative distance solution
%   result.l_alt     - Alternative stub length
%   result.type      - Stub type used
%   result.Z0        - Line impedance
%   result.Z0_stub   - Stub impedance
%   result.ZL        - Load impedance
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % Match 100+j50 Ohm load to 50 Ohm line with short-circuit stub
%   StubMatch(100+1j*50, 50, 'short')
%
%   % Match with open-circuit stub
%   StubMatch(100+1j*50, 50, 'open')
%
%   % Different stub impedance
%   StubMatch(75+1j*25, 50, 'short', 75)
%
% =========================================================================
% THEORY:
% =========================================================================
%   Single-stub matching works by:
%   1. Moving distance d from load until real(Y) = Y0 = 1/Z0
%   2. Adding a stub of length l to cancel the imaginary part of Y
%
%   Short stub: Y_stub = -j * cot(beta*l) / Z0_stub
%   Open stub:  Y_stub = j * tan(beta*l) / Z0_stub
%
% =========================================================================

    if nargin == 0
        print_help();
        return;
    end

    % Parse inputs
    if ischar(varargin{1}) || isstring(varargin{1})
        if strcmpi(varargin{1}, 'series')
            error('Series stub matching not yet implemented. Use shunt stub.');
        end
        args = varargin(2:end);
    else
        args = varargin;
    end
    
    ZL = args{1};
    Z0 = args{2};
    
    if length(args) >= 3
        stub_type = lower(string(args{3}));
    else
        stub_type = "short";
    end
    
    if length(args) >= 4
        Z0_stub = args{4};
    else
        Z0_stub = Z0;
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
    fprintf('      SINGLE-STUB MATCHING DESIGN        \n');
    fprintf('==========================================\n');
    fprintf('  Load: ZL = %.4f %+.4fj Ohm\n', real(r.ZL), imag(r.ZL));
    fprintf('  Line: Z0 = %.2f Ohm\n', r.Z0);
    fprintf('  Stub: Z0 = %.2f Ohm (%s)\n', r.Z0_stub, upper(r.type));
    fprintf('------------------------------------------\n');
    fprintf('  SOLUTION 1:\n');
    fprintf('    d (load to stub) = %.4f lambda\n', r.d);
    fprintf('    l (stub length)  = %.4f lambda\n', r.l);
    
    if ~isnan(r.d_alt)
        fprintf('------------------------------------------\n');
        fprintf('  SOLUTION 2 (alternative):\n');
        fprintf('    d (load to stub) = %.4f lambda\n', r.d_alt);
        fprintf('    l (stub length)  = %.4f lambda\n', r.l_alt);
    end
    
    fprintf('------------------------------------------\n');
    % Verification
    y_check = r.Y_in_check * r.Z0;  % Normalized
    fprintf('  Verification: y_total = %.4f %+.4fj\n', real(y_check), imag(y_check));
    if abs(y_check - 1) < 0.01
        fprintf('  Status: MATCHED (y ≈ 1)\n');
    else
        fprintf('  Status: Check solution\n');
    end
    fprintf('==========================================\n\n');
    
    % Visual diagram
    fprintf('  Circuit Diagram:\n');
    fprintf('  \n');
    if r.type == "short"
        fprintf('       d          l\n');
        fprintf('  [ZL]----+----[===|    (short)\n');
        fprintf('          |    stub\n');
        fprintf('       to source\n');
    else
        fprintf('       d          l\n');
        fprintf('  [ZL]----+----[===o    (open)\n');
        fprintf('          |    stub\n');
        fprintf('       to source\n');
    end
    fprintf('\n');
end

function print_help()
    fprintf('\n');
    fprintf('STUBMATCH - Single-Stub Matching Calculator\n');
    fprintf('============================================\n\n');
    fprintf('Basic usage:\n');
    fprintf('  StubMatch(ZL, Z0)               %% Short stub (default)\n');
    fprintf('  StubMatch(ZL, Z0, ''open'')       %% Open stub\n');
    fprintf('  StubMatch(ZL, Z0, ''short'')      %% Short stub\n\n');
    fprintf('With different stub impedance:\n');
    fprintf('  StubMatch(ZL, Z0, ''short'', Z0_stub)\n\n');
    fprintf('Example:\n');
    fprintf('  StubMatch(100+1j*50, 50, ''short'')\n\n');
    fprintf('Output includes both solutions (d, l) and (d_alt, l_alt)\n\n');
end
