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
%   result = TLine('Gamma_in', Gamma_L, len_lambda) % propagate Gamma
%
% MODE 4: Quarter-wave transformer design
%   result = TLine('QW', Z_source, Z_load)          % design QW transformer
%
% MODE 5: Special lengths
%   result = TLine('lambda/4', Z0, ZL)              % quarter-wave
%   result = TLine('lambda/2', Z0, ZL)              % half-wave
%
% =========================================================================
% OUTPUTS (struct with relevant fields):
% =========================================================================
%   result.Z_in      - Input impedance
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
%   % With frequency and velocity: 50Ω, 75Ω load, 0.5m, 1GHz, 2e8 m/s
%   TLine(50, 75, 0.5, 1e9, 2e8)
%
%   % Quarter-wave transformer design
%   TLine('QW', 50, 100)
%
%   % Find Gamma from load impedance
%   TLine('Gamma', 50, 75+1j*25)
%
%   % Propagate Gamma along line
%   TLine('Gamma_in', 0.5*exp(1j*pi/4), 0.2)
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
        case "qw"
            result = mode_quarter_wave(args{:});
        case "lambda/4"
            result = mode_special_length(0.25, args{:});
        case "lambda/2"
            result = mode_special_length(0.5, args{:});
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
    
    fprintf('\n=== Gamma Propagation ===\n');
    fprintf('  Gamma_L = %.4f %+.4fj\n', real(Gamma_L), imag(Gamma_L));
    fprintf('  |Gamma_L| = %.4f, angle = %.2f deg\n', abs(Gamma_L), rad2deg(angle(Gamma_L)));
    fprintf('  Length = %.4f lambda\n', len_lambda);
    fprintf('  -------------------------\n');
    fprintf('  Gamma_in = %.4f %+.4fj\n', real(Gamma_in), imag(Gamma_in));
    fprintf('  |Gamma_in| = %.4f, angle = %.2f deg\n', abs(Gamma_in), rad2deg(angle(Gamma_in)));
    fprintf('=========================\n\n');
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
    fprintf('  TLine(''Gamma_in'', Gamma_L, len)   %% propagate Gamma\n\n');
    fprintf('Quarter-wave transformer:\n');
    fprintf('  TLine(''QW'', Z_source, Z_load)     %% design transformer\n\n');
    fprintf('Special lengths:\n');
    fprintf('  TLine(''lambda/4'', Z0, ZL)\n');
    fprintf('  TLine(''lambda/2'', Z0, ZL)\n\n');
end
