function result = TLine(varargin)
% TLINE - Unified Transmission Line Calculator
%
% =========================================================================
% USAGE MODES:
% =========================================================================
%
% MODE 1: Full transmission line analysis
%   result = TLine(Z0, ZL, len, freq, vp)
%   result = TLine(Z0, ZL, len, freq, vp, alpha)    % lossy line
%   result = TLine(Z0, ZL, len_lambda)              % length in wavelengths
%
% MODE 2: Impedance transformation
%   result = TLine('Zin', Z0, ZL, len_lambda)       % find input impedance
%   result = TLine('ZL', Z0, Zin, len_lambda)       % find load impedance
%
% MODE 3: Reflection coefficient
%   result = TLine('Gamma', Z0, Z)                  % Gamma from impedance
%   result = TLine('Z', Z0, Gamma)                  % impedance from Gamma
%   result = TLine('Gamma_in', Gamma_L, len_lambda) % Gamma_L → Gamma_in
%   result = TLine('Gamma_L', Gamma_in, len_lambda) % Gamma_in → Gamma_L (reverse)
%
% MODE 4: Find load from input measurement (Q13/Q14 exam type)
%   result = TLine('load', Z0, Gamma_A, len_lambda) % find Gamma_L and Z_L
%
% MODE 5: Quarter-wave transformer design
%   result = TLine('QW', Z_source, Z_load)          % design QW transformer
%
% MODE 6: Special lengths
%   result = TLine('lambda/4', Z0, ZL)              % quarter-wave
%   result = TLine('lambda/2', Z0, ZL)              % half-wave
%
% MODE 7: TL with series element at input
%   result = TLine('series_C', Z0, ZL, len_m, C, freq, vp)
%   result = TLine('series_L', Z0, ZL, len_m, L, freq, vp)
%   result = TLine('series_C', Z0, ZL, len_lambda, C, freq)  % len in λ
%
% MODE 8: TL with shunt element at input
%   result = TLine('shunt_C', Z0, ZL, len_m, C, freq, vp)
%   result = TLine('shunt_L', Z0, ZL, len_m, L, freq, vp)
%
% MODE 9: Complex circuit (multiple elements)
%   result = TLine('circuit', Z0, ZL, len_m, freq, vp, ...
%                  'series_C', C1, 'shunt_L', L1, ...)
%
% MODE 10: Stub design (realize target impedance)
%   result = TLine('stub', Z_target, Z0)           % both short & open
%   result = TLine('stub', Z_target, Z0, 'short')  % short stub only
%   result = TLine('stub', Z_target, Z0, 'open')   % open stub only
%
% =========================================================================
% OUTPUTS (struct with relevant fields):
% =========================================================================
%   result.Z_in      - Input impedance
%   result.Z_L       - Load impedance
%   result.Z_A       - Input impedance (alias)
%   result.Gamma_L   - Load reflection coefficient
%   result.Gamma_in  - Input reflection coefficient
%   result.VSWR      - Voltage Standing Wave Ratio
%   result.z_vmax    - Distance to first Vmax from load (wavelengths)
%   result.z_vmin    - Distance to first Vmin from load (wavelengths)
%   result.P_frac    - Fraction of power delivered to load
%   result.RL_dB     - Return loss in dB
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % Basic analysis: 50Ω line, 100Ω load, 0.3λ long
%   TLine(50, 100, 0.3)
%
%   % Quarter-wave transformer design
%   TLine('QW', 50, 100)
%
%   % Q13/Q14 exam: Find Gamma_L and Z_L from Gamma at input
%   % Given: Gamma_A = 0.539∠166°, Z0 = 75Ω, ℓ = 0.3λ
%   TLine('load', 75, 0.539*exp(1j*deg2rad(166)), 0.3)
%
%   % TL with series capacitor (Q11 exam)
%   c0 = 3e8;
%   TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0)
%
%   % Stub design: realize j30 Ohm with 75 Ohm short stub (Q12 exam)
%   TLine('stub', 1j*30, 75, 'short')
%
% =========================================================================

    if nargin == 0
        print_help();
        return;
    end

    % Detect mode from first argument
    if ischar(varargin{1}) || isstring(varargin{1})
        mode = lower(string(varargin{1}));
        args = varargin(2:end);
    else
        mode = "full";
        args = varargin;
    end

    % Dispatch to appropriate handler
    switch mode
        case "full"
            result = mode_full_analysis(args{:});
        case "zin"
            result = mode_impedance_transform('in', args{:});
        case "zl"
            result = mode_impedance_transform('load', args{:});
        case "gamma"
            result = mode_gamma_from_z(args{:});
        case "z"
            result = mode_z_from_gamma(args{:});
        case "gamma_in"
            result = mode_gamma_propagate(args{:});
        case "gamma_l"
            result = mode_gamma_to_load(args{:});
        case "load"
            result = mode_find_load(args{:});
        case "qw"
            result = mode_quarter_wave(args{:});
        case "lambda/4"
            result = mode_special_length(0.25, args{:});
        case "lambda/2"
            result = mode_special_length(0.5, args{:});
        case "series_c"
            result = mode_series_element('C', args{:});
        case "series_l"
            result = mode_series_element('L', args{:});
        case "shunt_c"
            result = mode_shunt_element('C', args{:});
        case "shunt_l"
            result = mode_shunt_element('L', args{:});
        case "circuit"
            result = mode_circuit(args{:});
        case "stub"
            result = mode_stub_design(args{:});
        case "short_stub"
            result = mode_stub_design('short', args{:});
        case "open_stub"
            result = mode_stub_design('open', args{:});
        otherwise
            error('Unknown mode: %s. Run TLine() for help.', mode);
    end
end

%% ========================================================================
%  MODE HANDLERS
%% ========================================================================

function result = mode_full_analysis(Z0, ZL, len, freq, vp, alpha)
    % Full transmission line analysis
    
    if nargin < 4
        % Length given in wavelengths
        len_lambda = len;
        freq = NaN;
        vp = NaN;
        lambda = 1;
        len_m = len_lambda;  % Normalized
    else
        if nargin < 6, alpha = 0; end
        omega = 2*pi*freq;
        beta = omega/vp;
        lambda = 2*pi/beta;
        len_lambda = len/lambda;
        len_m = len;
    end
    
    if nargin < 6, alpha = 0; end
    
    beta_l = 2*pi*len_lambda;  % Electrical length in radians
    
    % Reflection coefficients
    Gamma_L = (ZL - Z0) / (ZL + Z0);
    
    if alpha == 0
        Gamma_in = Gamma_L * exp(-1j*2*beta_l);
    else
        if ~isnan(freq)
            gamma = alpha + 1j*(2*pi*freq/vp);
            Gamma_in = Gamma_L * exp(-2*gamma*len_m);
        else
            Gamma_in = Gamma_L * exp(-1j*2*beta_l);  % Approximate
        end
    end
    
    % Input impedance
    if abs(len_lambda - 0.25) < 1e-9 || abs(mod(len_lambda, 0.5) - 0.25) < 1e-9
        % Quarter-wave: Z_in = Z0^2 / ZL
        Z_in = Z0^2 / ZL;
    elseif abs(mod(len_lambda, 0.5)) < 1e-9
        % Half-wave: Z_in = ZL
        Z_in = ZL;
    else
        Z_in = Z0 * (1 + Gamma_in) / (1 - Gamma_in);
    end
    
    % Alternative formula (more numerically stable)
    % Z_in = Z0 * (ZL + 1j*Z0*tan(beta_l)) / (Z0 + 1j*ZL*tan(beta_l));
    
    % VSWR
    mag_Gamma = abs(Gamma_L);
    if mag_Gamma < 1
        VSWR = (1 + mag_Gamma) / (1 - mag_Gamma);
    else
        VSWR = Inf;
    end
    
    % Vmax/Vmin positions (from load)
    if mag_Gamma > 1e-10 && alpha == 0
        phi_L = angle(Gamma_L);
        z_vmax = mod(-phi_L/(4*pi), 0.5);      % in wavelengths
        z_vmin = mod((pi-phi_L)/(4*pi), 0.5); % in wavelengths
    else
        z_vmax = NaN;
        z_vmin = NaN;
    end
    
    % Power metrics
    P_reflected = abs(Gamma_L)^2;
    P_delivered = 1 - P_reflected;
    if mag_Gamma > 0
        RL_dB = -20*log10(mag_Gamma);  % Return loss
    else
        RL_dB = Inf;
    end
    
    % Pack results
    result.Z0 = Z0;
    result.ZL = ZL;
    result.len_lambda = len_lambda;
    result.Z_in = Z_in;
    result.Gamma_L = Gamma_L;
    result.Gamma_in = Gamma_in;
    result.VSWR = VSWR;
    result.z_vmax = z_vmax;
    result.z_vmin = z_vmin;
    result.P_reflected = P_reflected;
    result.P_delivered = P_delivered;
    result.RL_dB = RL_dB;
    
    if ~isnan(freq)
        result.freq = freq;
        result.vp = vp;
        result.lambda = lambda;
        result.len_m = len_m;
    end
    
    % Display
    print_full_results(result);
end

function result = mode_impedance_transform(direction, Z0, Z, len_lambda)
    beta_l = 2*pi*len_lambda;
    
    if strcmp(direction, 'in')
        % Find Z_in given ZL
        ZL = Z;
        if abs(mod(len_lambda, 0.5) - 0.25) < 1e-9
            Z_in = Z0^2 / ZL;
        elseif abs(mod(len_lambda, 0.5)) < 1e-9
            Z_in = ZL;
        else
            Z_in = Z0 * (ZL + 1j*Z0*tan(beta_l)) / (Z0 + 1j*ZL*tan(beta_l));
        end
        result.Z_in = Z_in;
        result.ZL = ZL;
        
        fprintf('\n=== Impedance Transformation ===\n');
        fprintf('  Z0 = %.2f Ohm\n', Z0);
        fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
        fprintf('  Length = %.4f lambda\n', len_lambda);
        fprintf('  --------------------------------\n');
        fprintf('  Z_in = %.4f %+.4fj Ohm\n', real(Z_in), imag(Z_in));
        fprintf('  |Z_in| = %.4f Ohm\n', abs(Z_in));
        fprintf('  angle(Z_in) = %.2f deg\n', rad2deg(angle(Z_in)));
        fprintf('================================\n\n');
    else
        % Find ZL given Z_in
        Z_in = Z;
        if abs(mod(len_lambda, 0.5) - 0.25) < 1e-9
            ZL = Z0^2 / Z_in;
        elseif abs(mod(len_lambda, 0.5)) < 1e-9
            ZL = Z_in;
        else
            ZL = Z0 * (Z_in - 1j*Z0*tan(beta_l)) / (Z0 - 1j*Z_in*tan(beta_l));
        end
        result.ZL = ZL;
        result.Z_in = Z_in;
        
        fprintf('\n=== Impedance Transformation ===\n');
        fprintf('  Z0 = %.2f Ohm\n', Z0);
        fprintf('  Z_in = %.4f %+.4fj Ohm\n', real(Z_in), imag(Z_in));
        fprintf('  Length = %.4f lambda\n', len_lambda);
        fprintf('  --------------------------------\n');
        fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
        fprintf('================================\n\n');
    end
    
    result.Z0 = Z0;
    result.len_lambda = len_lambda;
end

function result = mode_gamma_from_z(Z0, Z)
    Gamma = (Z - Z0) / (Z + Z0);
    mag = abs(Gamma);
    ang = rad2deg(angle(Gamma));
    VSWR = (1 + mag) / (1 - mag);
    
    result.Z0 = Z0;
    result.Z = Z;
    result.Gamma = Gamma;
    result.Gamma_mag = mag;
    result.Gamma_angle = ang;
    result.VSWR = VSWR;
    
    fprintf('\n=== Reflection Coefficient ===\n');
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  Z  = %.4f %+.4fj Ohm\n', real(Z), imag(Z));
    fprintf('  ------------------------------\n');
    fprintf('  Gamma = %.4f %+.4fj\n', real(Gamma), imag(Gamma));
    fprintf('  |Gamma| = %.4f\n', mag);
    fprintf('  angle(Gamma) = %.2f deg\n', ang);
    fprintf('  VSWR = %.4f\n', VSWR);
    fprintf('==============================\n\n');
end

function result = mode_z_from_gamma(Z0, Gamma)
    Z = Z0 * (1 + Gamma) / (1 - Gamma);
    
    result.Z0 = Z0;
    result.Gamma = Gamma;
    result.Z = Z;
    
    fprintf('\n=== Impedance from Gamma ===\n');
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  Gamma = %.4f %+.4fj\n', real(Gamma), imag(Gamma));
    fprintf('  |Gamma| = %.4f, angle = %.2f deg\n', abs(Gamma), rad2deg(angle(Gamma)));
    fprintf('  ----------------------------\n');
    fprintf('  Z = %.4f %+.4fj Ohm\n', real(Z), imag(Z));
    fprintf('============================\n\n');
end

function result = mode_gamma_propagate(Gamma_L, len_lambda)
    % Propagate Gamma from load toward source
    beta_l = 2*pi*len_lambda;
    Gamma_in = Gamma_L * exp(-1j*2*beta_l);
    
    result.Gamma_L = Gamma_L;
    result.Gamma_in = Gamma_in;
    result.len_lambda = len_lambda;
    
    fprintf('\n=== Gamma Propagation (Load → Input) ===\n');
    fprintf('  Gamma_L = %.4f %+.4fj\n', real(Gamma_L), imag(Gamma_L));
    fprintf('  |Gamma_L| = %.4f, angle = %.2f deg\n', abs(Gamma_L), rad2deg(angle(Gamma_L)));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('  Phase shift = -2βℓ = %.2f deg\n', -rad2deg(2*beta_l));
    fprintf('  -----------------------------------------\n');
    fprintf('  Gamma_in = %.4f %+.4fj\n', real(Gamma_in), imag(Gamma_in));
    fprintf('  |Gamma_in| = %.4f, angle = %.2f deg\n', abs(Gamma_in), rad2deg(angle(Gamma_in)));
    fprintf('=========================================\n\n');
end

function result = mode_gamma_to_load(Gamma_in, len_lambda)
    % Propagate Gamma from input toward load (reverse direction)
    % Gamma_in = Gamma_L * exp(-j*2*beta*l)
    % Gamma_L = Gamma_in * exp(+j*2*beta*l)
    beta_l = 2*pi*len_lambda;
    Gamma_L = Gamma_in * exp(1j*2*beta_l);
    
    result.Gamma_in = Gamma_in;
    result.Gamma_L = Gamma_L;
    result.len_lambda = len_lambda;
    
    fprintf('\n=== Gamma Propagation (Input → Load) ===\n');
    fprintf('  Gamma_in = %.4f %+.4fj\n', real(Gamma_in), imag(Gamma_in));
    fprintf('  |Gamma_in| = %.4f, angle = %.2f deg\n', abs(Gamma_in), rad2deg(angle(Gamma_in)));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('  Phase shift = +2βℓ = %.2f deg\n', rad2deg(2*beta_l));
    fprintf('  -----------------------------------------\n');
    fprintf('  Gamma_L = %.4f %+.4fj\n', real(Gamma_L), imag(Gamma_L));
    fprintf('  |Gamma_L| = %.4f, angle = %.2f deg\n', abs(Gamma_L), rad2deg(angle(Gamma_L)));
    fprintf('=========================================\n\n');
end

function result = mode_find_load(Z0, Gamma_in, len_lambda)
    % Given Gamma at input, find Gamma_L and Z_L
    % This solves Q13/Q14 type problems in one call
    %
    % Usage: TLine('load', Z0, Gamma_in, len_lambda)
    %
    % Gamma_in = Gamma_L * exp(-j*2*beta*l)
    % Gamma_L = Gamma_in * exp(+j*2*beta*l)
    
    beta_l = 2*pi*len_lambda;
    phase_shift = 2*beta_l;
    
    % Find Gamma_L
    Gamma_L = Gamma_in * exp(1j*phase_shift);
    
    % Find Z_L from Gamma_L
    Z_L = Z0 * (1 + Gamma_L) / (1 - Gamma_L);
    
    % VSWR (same everywhere on lossless line)
    mag_Gamma = abs(Gamma_L);  % = abs(Gamma_in)
    VSWR = (1 + mag_Gamma) / (1 - mag_Gamma);
    
    % Pack results
    result.Z0 = Z0;
    result.Gamma_in = Gamma_in;
    result.Gamma_L = Gamma_L;
    result.Z_L = Z_L;
    result.len_lambda = len_lambda;
    result.phase_shift_deg = rad2deg(phase_shift);
    result.VSWR = VSWR;
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('   FIND LOAD FROM INPUT (Q13/Q14 type)\n');
    fprintf('==========================================\n');
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  Gamma_in = %.4f %+.4fj\n', real(Gamma_in), imag(Gamma_in));
    fprintf('  |Gamma_in| = %.4f, angle = %.2f deg\n', abs(Gamma_in), rad2deg(angle(Gamma_in)));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('------------------------------------------\n');
    fprintf('  Phase shift: +2βℓ = +2·2π·%.4f = %.2f deg\n', len_lambda, rad2deg(phase_shift));
    fprintf('------------------------------------------\n');
    fprintf('  Gamma_L = Gamma_in · exp(+j·%.2f°)\n', rad2deg(phase_shift));
    fprintf('  Gamma_L = %.4f %+.4fj\n', real(Gamma_L), imag(Gamma_L));
    fprintf('  |Gamma_L| = %.4f, angle = %.2f deg\n', abs(Gamma_L), rad2deg(angle(Gamma_L)));
    fprintf('------------------------------------------\n');
    fprintf('  Z_L = Z0·(1+Gamma_L)/(1-Gamma_L)\n');
    fprintf('  Z_L = %.4f %+.4fj Ohm\n', real(Z_L), imag(Z_L));
    fprintf('  |Z_L| = %.2f Ohm, angle = %.2f deg\n', abs(Z_L), rad2deg(angle(Z_L)));
    fprintf('------------------------------------------\n');
    fprintf('  VSWR = %.4f\n', VSWR);
    fprintf('==========================================\n\n');
end

function result = mode_quarter_wave(Z_source, Z_load)
    % Design quarter-wave transformer
    if ~isreal(Z_source) || ~isreal(Z_load)
        warning('Quarter-wave transformer requires real impedances. Using magnitudes.');
        Z_source = abs(Z_source);
        Z_load = abs(Z_load);
    end
    
    Z_qw = sqrt(Z_source * Z_load);
    len = 0.25;  % wavelengths
    
    result.Z_source = Z_source;
    result.Z_load = Z_load;
    result.Z_qw = Z_qw;
    result.len_lambda = len;
    
    fprintf('\n=== Quarter-Wave Transformer Design ===\n');
    fprintf('  Source impedance: %.2f Ohm\n', Z_source);
    fprintf('  Load impedance:   %.2f Ohm\n', Z_load);
    fprintf('  --------------------------------------\n');
    fprintf('  Required Z0 = sqrt(%.2f x %.2f) = %.4f Ohm\n', Z_source, Z_load, Z_qw);
    fprintf('  Length = lambda/4\n');
    fprintf('  \n');
    fprintf('  Verification: Z_in = %.4f^2 / %.2f = %.4f Ohm\n', Z_qw, Z_load, Z_qw^2/Z_load);
    fprintf('=======================================\n\n');
end

function result = mode_special_length(len_lambda, Z0, ZL)
    beta_l = 2*pi*len_lambda;
    
    if abs(len_lambda - 0.25) < 1e-9
        Z_in = Z0^2 / ZL;
        type_str = 'lambda/4';
    else
        Z_in = ZL;  % lambda/2
        type_str = 'lambda/2';
    end
    
    Gamma_L = (ZL - Z0) / (ZL + Z0);
    
    result.Z0 = Z0;
    result.ZL = ZL;
    result.Z_in = Z_in;
    result.len_lambda = len_lambda;
    result.Gamma_L = Gamma_L;
    
    fprintf('\n=== %s Line ===\n', type_str);
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
    fprintf('  -----------------------\n');
    fprintf('  Z_in = %.4f %+.4fj Ohm\n', real(Z_in), imag(Z_in));
    fprintf('=======================\n\n');
end

function result = mode_series_element(element_type, Z0, ZL, len, element_value, freq, vp)
% TL with series element at input
% Usage: TLine('series_C', Z0, ZL, len_m, C, freq, vp)
%        TLine('series_L', Z0, ZL, len_m, L, freq, vp)
%        TLine('series_C', Z0, ZL, len_lambda, C, freq)  % len in wavelengths

    % Determine if length is in meters or wavelengths
    if nargin >= 7
        % Length in meters, need to calculate lambda
        lambda = vp / freq;
        len_lambda = len / lambda;
        len_m = len;
    else
        % Length in wavelengths
        len_lambda = len;
        vp = NaN;
        lambda = NaN;
        len_m = NaN;
    end
    
    omega = 2*pi*freq;
    
    % Calculate TL input impedance
    beta_l = 2*pi*len_lambda;
    Z_TL = Z0 * (ZL + 1j*Z0*tan(beta_l)) / (Z0 + 1j*ZL*tan(beta_l));
    
    % Calculate element impedance
    if element_type == 'C'
        Z_element = 1 / (1j * omega * element_value);
        element_str = sprintf('%.2f pF', element_value * 1e12);
        element_name = 'Capacitor';
    else  % 'L'
        Z_element = 1j * omega * element_value;
        element_str = sprintf('%.2f nH', element_value * 1e9);
        element_name = 'Inductor';
    end
    
    % Series connection: Z_total = Z_element + Z_TL
    Z_A = Z_element + Z_TL;
    
    % Pack results
    result.Z0 = Z0;
    result.ZL = ZL;
    result.freq = freq;
    result.len_lambda = len_lambda;
    result.Z_TL = Z_TL;
    result.Z_element = Z_element;
    result.Z_A = Z_A;
    result.Z_in = Z_A;  % Alias
    
    if ~isnan(lambda)
        result.lambda = lambda;
        result.vp = vp;
        result.len_m = len_m;
    end
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('   TL + SERIES %s @ %.2e Hz\n', upper(element_name), freq);
    fprintf('==========================================\n');
    fprintf('  %s: %s\n', element_name, element_str);
    fprintf('  Z_%s = %.4f %+.4fj Ohm\n', element_type, real(Z_element), imag(Z_element));
    fprintf('------------------------------------------\n');
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('  Z_TL (TL input) = %.4f %+.4fj Ohm\n', real(Z_TL), imag(Z_TL));
    fprintf('------------------------------------------\n');
    fprintf('  Z_A = Z_%s + Z_TL\n', element_type);
    fprintf('  Z_A = %.4f %+.4fj Ohm\n', real(Z_A), imag(Z_A));
    fprintf('  |Z_A| = %.2f Ohm\n', abs(Z_A));
    fprintf('  angle(Z_A) = %.2f deg\n', rad2deg(angle(Z_A)));
    fprintf('==========================================\n\n');
end

function result = mode_shunt_element(element_type, Z0, ZL, len, element_value, freq, vp)
% TL with shunt element at input
% Usage: TLine('shunt_C', Z0, ZL, len_m, C, freq, vp)
%        TLine('shunt_L', Z0, ZL, len_m, L, freq, vp)

    % Determine if length is in meters or wavelengths
    if nargin >= 7
        % Length in meters
        lambda = vp / freq;
        len_lambda = len / lambda;
        len_m = len;
    else
        % Length in wavelengths
        len_lambda = len;
        vp = NaN;
        lambda = NaN;
        len_m = NaN;
    end
    
    omega = 2*pi*freq;
    
    % Calculate TL input impedance
    beta_l = 2*pi*len_lambda;
    Z_TL = Z0 * (ZL + 1j*Z0*tan(beta_l)) / (Z0 + 1j*ZL*tan(beta_l));
    
    % Calculate element impedance
    if element_type == 'C'
        Z_element = 1 / (1j * omega * element_value);
        Y_element = 1j * omega * element_value;
        element_str = sprintf('%.2f pF', element_value * 1e12);
        element_name = 'Capacitor';
    else  % 'L'
        Z_element = 1j * omega * element_value;
        Y_element = 1 / (1j * omega * element_value);
        element_str = sprintf('%.2f nH', element_value * 1e9);
        element_name = 'Inductor';
    end
    
    % Shunt connection: Y_total = Y_element + Y_TL
    Y_TL = 1 / Z_TL;
    Y_A = Y_element + Y_TL;
    Z_A = 1 / Y_A;
    
    % Pack results
    result.Z0 = Z0;
    result.ZL = ZL;
    result.freq = freq;
    result.len_lambda = len_lambda;
    result.Z_TL = Z_TL;
    result.Z_element = Z_element;
    result.Z_A = Z_A;
    result.Z_in = Z_A;
    
    if ~isnan(lambda)
        result.lambda = lambda;
        result.vp = vp;
        result.len_m = len_m;
    end
    
    % Display
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('   TL + SHUNT %s @ %.2e Hz\n', upper(element_name), freq);
    fprintf('==========================================\n');
    fprintf('  %s: %s\n', element_name, element_str);
    fprintf('  Z_%s = %.4f %+.4fj Ohm\n', element_type, real(Z_element), imag(Z_element));
    fprintf('------------------------------------------\n');
    fprintf('  Z0 = %.2f Ohm\n', Z0);
    fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('  Z_TL (TL input) = %.4f %+.4fj Ohm\n', real(Z_TL), imag(Z_TL));
    fprintf('------------------------------------------\n');
    fprintf('  Z_A = Z_%s || Z_TL\n', element_type);
    fprintf('  Z_A = %.4f %+.4fj Ohm\n', real(Z_A), imag(Z_A));
    fprintf('  |Z_A| = %.2f Ohm\n', abs(Z_A));
    fprintf('  angle(Z_A) = %.2f deg\n', rad2deg(angle(Z_A)));
    fprintf('==========================================\n\n');
end

function result = mode_circuit(Z0, ZL, len, freq, vp, varargin)
% General circuit mode for complex configurations
% Usage: TLine('circuit', Z0, ZL, len_m, freq, vp, 'series_C', C1, 'shunt_L', L1, ...)
%
% Elements are added at the INPUT of the TL, processed left to right
% Supported elements: 'series_C', 'series_L', 'shunt_C', 'shunt_L'

    % Calculate wavelength and TL input impedance
    lambda = vp / freq;
    len_lambda = len / lambda;
    omega = 2*pi*freq;
    
    beta_l = 2*pi*len_lambda;
    Z_current = Z0 * (ZL + 1j*Z0*tan(beta_l)) / (Z0 + 1j*ZL*tan(beta_l));
    
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('      CIRCUIT ANALYSIS @ %.2e Hz\n', freq);
    fprintf('==========================================\n');
    fprintf('  Z0 = %.2f Ohm, ZL = %.4f %+.4fj Ohm\n', Z0, real(ZL), imag(ZL));
    fprintf('  Length = %.4f lambda (%.2f mm)\n', len_lambda, len*1000);
    fprintf('  Z_TL = %.4f %+.4fj Ohm\n', real(Z_current), imag(Z_current));
    fprintf('------------------------------------------\n');
    
    result.Z_TL = Z_current;
    
    % Process each element
    i = 1;
    element_num = 1;
    while i <= length(varargin)
        element_type = lower(string(varargin{i}));
        element_value = varargin{i+1};
        i = i + 2;
        
        switch element_type
            case "series_c"
                Z_elem = 1 / (1j * omega * element_value);
                Z_current = Z_elem + Z_current;
                fprintf('  + Series C (%.2f pF): Z = %.4f %+.4fj\n', ...
                    element_value*1e12, real(Z_current), imag(Z_current));
            case "series_l"
                Z_elem = 1j * omega * element_value;
                Z_current = Z_elem + Z_current;
                fprintf('  + Series L (%.2f nH): Z = %.4f %+.4fj\n', ...
                    element_value*1e9, real(Z_current), imag(Z_current));
            case "shunt_c"
                Y_elem = 1j * omega * element_value;
                Z_current = 1 / (Y_elem + 1/Z_current);
                fprintf('  + Shunt C (%.2f pF): Z = %.4f %+.4fj\n', ...
                    element_value*1e12, real(Z_current), imag(Z_current));
            case "shunt_l"
                Y_elem = 1 / (1j * omega * element_value);
                Z_current = 1 / (Y_elem + 1/Z_current);
                fprintf('  + Shunt L (%.2f nH): Z = %.4f %+.4fj\n', ...
                    element_value*1e9, real(Z_current), imag(Z_current));
            otherwise
                warning('Unknown element: %s', element_type);
        end
        
        result.(sprintf('Z_after_elem%d', element_num)) = Z_current;
        element_num = element_num + 1;
    end
    
    fprintf('------------------------------------------\n');
    fprintf('  Z_A (final) = %.4f %+.4fj Ohm\n', real(Z_current), imag(Z_current));
    fprintf('  |Z_A| = %.2f Ohm\n', abs(Z_current));
    fprintf('  angle(Z_A) = %.2f deg\n', rad2deg(angle(Z_current)));
    fprintf('==========================================\n\n');
    
    result.Z0 = Z0;
    result.ZL = ZL;
    result.freq = freq;
    result.vp = vp;
    result.lambda = lambda;
    result.len_lambda = len_lambda;
    result.Z_A = Z_current;
    result.Z_in = Z_current;
end

function result = mode_stub_design(varargin)
% Design a stub to realize a target impedance
% Usage: TLine('stub', Z_target, Z0)              % finds both short & open
%        TLine('stub', Z_target, Z0, 'short')     % short-circuited stub only
%        TLine('stub', Z_target, Z0, 'open')      % open-circuited stub only
%        TLine('short_stub', Z_target, Z0)        % short-circuited stub
%        TLine('open_stub', Z_target, Z0)         % open-circuited stub
%
% For SHORT stub: Z_in = j*Z0*tan(β*ℓ)
% For OPEN stub:  Z_in = -j*Z0*cot(β*ℓ)

    % Parse arguments
    if ischar(varargin{1}) || isstring(varargin{1})
        % Called as mode_stub_design('short', Z_target, Z0)
        stub_type = lower(string(varargin{1}));
        Z_target = varargin{2};
        Z0 = varargin{3};
    else
        % Called as mode_stub_design(Z_target, Z0, [type])
        Z_target = varargin{1};
        Z0 = varargin{2};
        if nargin >= 3 && ~isempty(varargin{3})
            stub_type = lower(string(varargin{3}));
        else
            stub_type = "both";
        end
    end
    
    % Check if target is purely reactive
    if abs(real(Z_target)) > 1e-6
        warning('Stub can only realize purely reactive impedances. Using imaginary part only.');
        fprintf('  Note: Real part %.4f Ohm will be ignored.\n', real(Z_target));
    end
    
    X_target = imag(Z_target);  % Target reactance
    
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('         STUB DESIGN\n');
    fprintf('==========================================\n');
    fprintf('  Target Z = j%.4f Ohm\n', X_target);
    fprintf('  Stub Z0 = %.2f Ohm\n', Z0);
    fprintf('------------------------------------------\n');
    
    result.Z_target = 1j * X_target;
    result.Z0 = Z0;
    
    % SHORT-CIRCUITED STUB
    % Z_in = j*Z0*tan(β*ℓ) = jX
    % tan(β*ℓ) = X/Z0
    if stub_type == "short" || stub_type == "both"
        tan_bl = X_target / Z0;
        beta_l = atan(tan_bl);  % Principal value in (-π/2, π/2)
        
        % Ensure positive length
        if beta_l < 0
            beta_l = beta_l + pi;  % Add π to get positive length
        end
        
        len_lambda_short = beta_l / (2*pi);
        
        % Alternative solution (add λ/2)
        len_lambda_short_alt = len_lambda_short + 0.5;
        
        result.short.len_lambda = len_lambda_short;
        result.short.len_lambda_alt = len_lambda_short_alt;
        result.short.beta_l_rad = beta_l;
        result.short.beta_l_deg = rad2deg(beta_l);
        
        % Verify
        Z_verify = 1j * Z0 * tan(2*pi*len_lambda_short);
        result.short.Z_verify = Z_verify;
        
        fprintf('  SHORT-CIRCUITED STUB:\n');
        fprintf('    tan(βℓ) = %.4f / %.2f = %.6f\n', X_target, Z0, tan_bl);
        fprintf('    βℓ = %.4f rad = %.2f°\n', beta_l, rad2deg(beta_l));
        fprintf('    ℓ = %.4f λ  (or %.4f λ)\n', len_lambda_short, len_lambda_short_alt);
        fprintf('    Verify: Z_in = j·%.2f·tan(%.4f) = j%.4f Ohm ✓\n', ...
            Z0, beta_l, imag(Z_verify));
        fprintf('------------------------------------------\n');
    end
    
    % OPEN-CIRCUITED STUB
    % Z_in = -j*Z0*cot(β*ℓ) = jX
    % cot(β*ℓ) = -X/Z0
    % tan(β*ℓ) = -Z0/X
    if stub_type == "open" || stub_type == "both"
        if abs(X_target) < 1e-10
            fprintf('  OPEN-CIRCUITED STUB:\n');
            fprintf('    Cannot realize Z = 0 with open stub\n');
            fprintf('------------------------------------------\n');
            result.open.len_lambda = NaN;
        else
            tan_bl = -Z0 / X_target;
            beta_l = atan(tan_bl);
            
            % Ensure positive length
            if beta_l < 0
                beta_l = beta_l + pi;
            end
            
            len_lambda_open = beta_l / (2*pi);
            len_lambda_open_alt = len_lambda_open + 0.5;
            
            result.open.len_lambda = len_lambda_open;
            result.open.len_lambda_alt = len_lambda_open_alt;
            result.open.beta_l_rad = beta_l;
            result.open.beta_l_deg = rad2deg(beta_l);
            
            % Verify
            Z_verify = -1j * Z0 * cot(2*pi*len_lambda_open);
            result.open.Z_verify = Z_verify;
            
            fprintf('  OPEN-CIRCUITED STUB:\n');
            fprintf('    cot(βℓ) = -%.4f / %.2f = %.6f\n', X_target, Z0, -X_target/Z0);
            fprintf('    βℓ = %.4f rad = %.2f°\n', beta_l, rad2deg(beta_l));
            fprintf('    ℓ = %.4f λ  (or %.4f λ)\n', len_lambda_open, len_lambda_open_alt);
            fprintf('    Verify: Z_in = -j·%.2f·cot(%.4f) = j%.4f Ohm ✓\n', ...
                Z0, beta_l, imag(Z_verify));
            fprintf('------------------------------------------\n');
        end
    end
    
    fprintf('==========================================\n\n');
    
    % Set primary result based on stub type
    if stub_type == "short"
        result.len_lambda = result.short.len_lambda;
    elseif stub_type == "open"
        result.len_lambda = result.open.len_lambda;
    end
end

%% ========================================================================
%  DISPLAY FUNCTIONS
%% ========================================================================

function print_full_results(r)
    fprintf('\n');
    fprintf('==========================================\n');
    fprintf('      TRANSMISSION LINE ANALYSIS         \n');
    fprintf('==========================================\n');
    fprintf('  Z0 = %.2f Ohm\n', r.Z0);
    fprintf('  ZL = %.4f %+.4fj Ohm\n', real(r.ZL), imag(r.ZL));
    fprintf('  Length = %.4f lambda\n', r.len_lambda);
    fprintf('------------------------------------------\n');
    fprintf('  Z_in = %.4f %+.4fj Ohm\n', real(r.Z_in), imag(r.Z_in));
    fprintf('  |Z_in| = %.4f Ohm\n', abs(r.Z_in));
    fprintf('------------------------------------------\n');
    fprintf('  Gamma_L = %.4f %+.4fj\n', real(r.Gamma_L), imag(r.Gamma_L));
    fprintf('  |Gamma_L| = %.4f, angle = %.2f deg\n', abs(r.Gamma_L), rad2deg(angle(r.Gamma_L)));
    fprintf('  Gamma_in = %.4f %+.4fj\n', real(r.Gamma_in), imag(r.Gamma_in));
    fprintf('------------------------------------------\n');
    fprintf('  VSWR = %.4f\n', r.VSWR);
    fprintf('  Return Loss = %.2f dB\n', r.RL_dB);
    fprintf('  Power delivered = %.2f%%\n', r.P_delivered*100);
    fprintf('------------------------------------------\n');
    if ~isnan(r.z_vmax)
        fprintf('  First V_max at %.4f lambda from load\n', r.z_vmax);
        fprintf('  First V_min at %.4f lambda from load\n', r.z_vmin);
    end
    fprintf('==========================================\n\n');
end

function print_help()
    fprintf('\n');
    fprintf('TLINE - Transmission Line Calculator\n');
    fprintf('====================================\n\n');
    fprintf('Basic analysis:\n');
    fprintf('  TLine(Z0, ZL, len_lambda)         %% length in wavelengths\n');
    fprintf('  TLine(Z0, ZL, len, freq, vp)      %% length in meters\n\n');
    fprintf('Impedance transformation:\n');
    fprintf('  TLine(''Zin'', Z0, ZL, len_lambda)  %% find input impedance\n');
    fprintf('  TLine(''ZL'', Z0, Zin, len_lambda)  %% find load impedance\n\n');
    fprintf('Reflection coefficient:\n');
    fprintf('  TLine(''Gamma'', Z0, Z)             %% Gamma from impedance\n');
    fprintf('  TLine(''Z'', Z0, Gamma)             %% impedance from Gamma\n');
    fprintf('  TLine(''Gamma_in'', Gamma_L, len)   %% Gamma_L -> Gamma_in\n');
    fprintf('  TLine(''Gamma_L'', Gamma_in, len)   %% Gamma_in -> Gamma_L (reverse)\n\n');
    fprintf('Find load from input (Q13/Q14 exam type):\n');
    fprintf('  TLine(''load'', Z0, Gamma_A, len)   %% find Gamma_L AND Z_L\n');
    fprintf('  Example: TLine(''load'', 75, 0.539*exp(1j*deg2rad(166)), 0.3)\n\n');
    fprintf('Quarter-wave transformer:\n');
    fprintf('  TLine(''QW'', Z_source, Z_load)     %% design transformer\n\n');
    fprintf('Special lengths:\n');
    fprintf('  TLine(''lambda/4'', Z0, ZL)\n');
    fprintf('  TLine(''lambda/2'', Z0, ZL)\n\n');
    fprintf('TL + Series element:\n');
    fprintf('  TLine(''series_C'', Z0, ZL, len_m, C, freq, vp)\n');
    fprintf('  TLine(''series_L'', Z0, ZL, len_m, L, freq, vp)\n\n');
    fprintf('TL + Shunt element:\n');
    fprintf('  TLine(''shunt_C'', Z0, ZL, len_m, C, freq, vp)\n');
    fprintf('  TLine(''shunt_L'', Z0, ZL, len_m, L, freq, vp)\n\n');
    fprintf('Stub design (realize target impedance):\n');
    fprintf('  TLine(''stub'', Z_target, Z0)        %% both short & open\n');
    fprintf('  TLine(''stub'', 1j*30, 75, ''short'') %% Q12: short stub for j30\n\n');
    fprintf('Complex circuit:\n');
    fprintf('  TLine(''circuit'', Z0, ZL, len_m, freq, vp, ...\n');
    fprintf('        ''series_C'', C, ''shunt_L'', L, ...)\n\n');
end