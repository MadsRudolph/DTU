function EM_Assistant()
% EM_ASSISTANT - Interactive electromagnetic problem solver
%
% This program guides you through solving EM problems by:
%   1. Asking what topic you need help with
%   2. Gathering relevant information through guided questions
%   3. Calculating answers using your EM toolbox scripts
%
% Simply run: EM_Assistant()
%
% Requirements: All your EM helper scripts in the MATLAB path:
%   - PlaneWaveCheck.m, Polarization.m, Fresnel.m, Medium.m
%   - TLine.m, StubMatch.m, poynting_pw.m, etc.

    clc;
    print_welcome();
    
    while true
        topic = select_topic();
        
        if topic == 0
            fprintf('\n  Goodbye and good luck on your exam! 🎓\n\n');
            break;
        end
        
        handle_topic(topic);
        
        fprintf('\n  Press Enter to continue...');
        input('', 's');
        clc;
    end
end

%% ========================================================================
%  WELCOME SCREEN
%% ========================================================================
function print_welcome()
    fprintf('\n');
    fprintf('  ╔══════════════════════════════════════════════════════════╗\n');
    fprintf('  ║                                                          ║\n');
    fprintf('  ║            ⚡ EM TOOLBOX ASSISTANT ⚡                    ║\n');
    fprintf('  ║                                                          ║\n');
    fprintf('  ║     Interactive Electromagnetic Problem Solver           ║\n');
    fprintf('  ║                                                          ║\n');
    fprintf('  ╚══════════════════════════════════════════════════════════╝\n');
    fprintf('\n');
end

%% ========================================================================
%  TOPIC SELECTION
%% ========================================================================
function topic = select_topic()
    fprintf('\n');
    fprintf('  ┌────────────────────────────────────────┐\n');
    fprintf('  │         WHAT DO YOU NEED HELP WITH?    │\n');
    fprintf('  ├────────────────────────────────────────┤\n');
    fprintf('  │  1. Plane Wave Verification            │\n');
    fprintf('  │  2. Polarization Analysis              │\n');
    fprintf('  │  3. Fresnel (Reflection/Transmission)  │\n');
    fprintf('  │  4. Medium Properties (η, β, λ, etc.)  │\n');
    fprintf('  │  5. Transmission Lines                 │\n');
    fprintf('  │  6. Stub Matching                      │\n');
    fprintf('  │  7. Poynting Vector / H-field          │\n');
    fprintf('  │  8. Magnetic Field (Infinite Wire)     │\n');
    fprintf('  │  9. Coulomb Force                      │\n');
    fprintf('  │                                        │\n');
    fprintf('  │  0. Exit                               │\n');
    fprintf('  └────────────────────────────────────────┘\n');
    fprintf('\n');
    
    topic = get_number('  Enter choice (0-9): ', 0, 9);
end

%% ========================================================================
%  TOPIC HANDLERS
%% ========================================================================
function handle_topic(topic)
    switch topic
        case 1, handle_plane_wave();
        case 2, handle_polarization();
        case 3, handle_fresnel();
        case 4, handle_medium();
        case 5, handle_tline();
        case 6, handle_stub_match();
        case 7, handle_poynting();
        case 8, handle_bfield_wire();
        case 9, handle_coulomb();
    end
end

%% ========================================================================
%  1. PLANE WAVE VERIFICATION
%% ========================================================================
function handle_plane_wave()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       PLANE WAVE VERIFICATION\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What format is your problem?\n\n');
    fprintf('    1. exp(-j(ax + by + cz)) in field expression\n');
    fprintf('       (Extract k from phase term)\n\n');
    fprintf('    2. γ = [γx; γy; γz] given separately\n');
    fprintf('       (Complex propagation vector)\n\n');
    
    format = get_number('  Enter format (1 or 2): ', 1, 2);
    
    if format == 1
        % Full mode - exp term
        fprintf('\n  --- Enter E-field phasor components ---\n');
        Ex = get_complex('  Ex (e.g., 0 or 5 or 1j*2): ');
        Ey = get_complex('  Ey: ');
        Ez = get_complex('  Ez: ');
        E = [Ex; Ey; Ez];
        
        fprintf('\n  --- Enter H-field phasor components ---\n');
        Hx = get_complex('  Hx: ');
        Hy = get_complex('  Hy: ');
        Hz = get_complex('  Hz: ');
        H = [Hx; Hy; Hz];
        
        fprintf('\n  --- Enter k from phase term exp(-j(kx*x + ky*y + kz*z)) ---\n');
        kx = get_number('  kx: ', -1e10, 1e10);
        ky = get_number('  ky: ', -1e10, 1e10);
        kz = get_number('  kz: ', -1e10, 1e10);
        k = [kx; ky; kz];
        
        fprintf('\n  Use custom η? (default is 377 Ω for free space)\n');
        custom_eta = get_yes_no('  Custom η? (y/n): ');
        
        if custom_eta
            eta = get_number('  Enter η [Ω]: ', 0, 1e6);
            fprintf('\n  Calling: PlaneWaveCheck(''full'', E, H, k, %.2f)\n', eta);
            result = PlaneWaveCheck('full', E, H, k, eta);
        else
            fprintf('\n  Calling: PlaneWaveCheck(''full'', E, H, k)\n');
            result = PlaneWaveCheck('full', E, H, k);
        end
        
    else
        % Maxwell mode - γ given
        fprintf('\n  --- Enter E₀ phasor components ---\n');
        Ex = get_complex('  E0x (e.g., 2 or 1j*5): ');
        Ey = get_complex('  E0y: ');
        Ez = get_complex('  E0z: ');
        E0 = [Ex; Ey; Ez];
        
        fprintf('\n  --- Enter H₀ phasor components ---\n');
        fprintf('  (Remember to convert mA/m to A/m if needed)\n');
        Hx = get_complex('  H0x: ');
        Hy = get_complex('  H0y: ');
        Hz = get_complex('  H0z: ');
        H0 = [Hx; Hy; Hz];
        
        fprintf('\n  --- Enter γ (complex propagation vector) ---\n');
        fprintf('  Example: γ = j3 in z → γz = 1j*3\n');
        gx = get_complex('  γx: ');
        gy = get_complex('  γy: ');
        gz = get_complex('  γz: ');
        gamma = [gx; gy; gz];
        
        fprintf('\n  Calling: PlaneWaveCheck(''maxwell'', E0, H0, gamma)\n');
        result = PlaneWaveCheck('maxwell', E0, H0, gamma);
    end
end

%% ========================================================================
%  2. POLARIZATION ANALYSIS
%% ========================================================================
function handle_polarization()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       POLARIZATION ANALYSIS\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What format is your E-field?\n\n');
    fprintf('    1. Complex phasor: E = [Ex; Ey; Ez]\n');
    fprintf('    2. Amplitude/Phase: Ex∠φx, Ey∠φy\n');
    fprintf('    3. Time-domain: u·cos + v·sin\n\n');
    
    format = get_number('  Enter format (1-3): ', 1, 3);
    
    if format == 1
        % Complex phasor
        fprintf('\n  --- Enter E-field phasor components ---\n');
        fprintf('  Examples: 1, -1j, 1+1j, 1j*2\n\n');
        Ex = get_complex('  Ex: ');
        Ey = get_complex('  Ey: ');
        Ez = get_complex('  Ez: ');
        E = [Ex; Ey; Ez];
        
        fprintf('\n  --- Enter propagation direction k̂ ---\n');
        fprintf('  Default is +z: [0; 0; 1]\n');
        use_default = get_yes_no('  Use default +z? (y/n): ');
        
        if use_default
            k_hat = [0; 0; 1];
        else
            kx = get_number('  k̂x: ', -1, 1);
            ky = get_number('  k̂y: ', -1, 1);
            kz = get_number('  k̂z: ', -1, 1);
            k_hat = [kx; ky; kz];
        end
        
        fprintf('\n  Calling: Polarization(E, k_hat)\n');
        result = Polarization(E, k_hat);
        
    elseif format == 2
        % Amplitude/Phase
        fprintf('\n  --- Enter amplitudes and phases ---\n');
        Ex = get_number('  |Ex| [V/m]: ', 0, 1e10);
        Ey = get_number('  |Ey| [V/m]: ', 0, 1e10);
        phi_x = get_number('  φx [degrees]: ', -360, 360);
        phi_y = get_number('  φy [degrees]: ', -360, 360);
        
        fprintf('\n  Calling: Polarization(''ap'', %.4f, %.4f, %.2f, %.2f)\n', Ex, Ey, phi_x, phi_y);
        result = Polarization('ap', Ex, Ey, phi_x, phi_y);
        
    else
        % Time-domain
        fprintf('\n  --- Enter u vector (cos coefficient) ---\n');
        ux = get_number('  ux: ', -1e10, 1e10);
        uy = get_number('  uy: ', -1e10, 1e10);
        uz = get_number('  uz: ', -1e10, 1e10);
        u = [ux; uy; uz];
        
        fprintf('\n  --- Enter v vector (sin coefficient) ---\n');
        vx = get_number('  vx: ', -1e10, 1e10);
        vy = get_number('  vy: ', -1e10, 1e10);
        vz = get_number('  vz: ', -1e10, 1e10);
        v = [vx; vy; vz];
        
        fprintf('\n  --- Enter β vector ---\n');
        bx = get_number('  βx: ', -1e10, 1e10);
        by = get_number('  βy: ', -1e10, 1e10);
        bz = get_number('  βz: ', -1e10, 1e10);
        beta = [bx; by; bz];
        
        fprintf('\n  Calling: Polarization(u, v, beta)\n');
        result = Polarization(u, v, beta);
    end
end

%% ========================================================================
%  3. FRESNEL (REFLECTION/TRANSMISSION)
%% ========================================================================
function handle_fresnel()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       FRESNEL - REFLECTION/TRANSMISSION\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What do you need?\n\n');
    fprintf('    1. Normal incidence (θ = 0°)\n');
    fprintf('    2. Oblique incidence (θ ≠ 0°)\n');
    fprintf('    3. Transmitted angle (Snell''s law)\n');
    fprintf('    4. Brewster angle\n');
    fprintf('    5. Critical angle (TIR)\n\n');
    
    mode = get_number('  Enter choice (1-5): ', 1, 5);
    
    if mode == 1
        % Normal incidence
        fprintf('\n  --- Enter material properties ---\n');
        eps1 = get_number('  εr1 (incident medium): ', 0.1, 1000);
        eps2 = get_number('  εr2 (second medium): ', 0.1, 1000);
        
        fprintf('\n  Calling: Fresnel(%.3f, %.3f)\n', eps1, eps2);
        result = Fresnel(eps1, eps2);
        
    elseif mode == 2
        % Oblique incidence
        fprintf('\n  --- Enter material properties ---\n');
        eps1 = get_number('  εr1 (incident medium): ', 0.1, 1000);
        eps2 = get_number('  εr2 (second medium): ', 0.1, 1000);
        theta = get_number('  θi [degrees]: ', 0, 90);
        
        fprintf('\n  Which polarization?\n');
        fprintf('    1. Both TE and TM\n');
        fprintf('    2. TE only\n');
        fprintf('    3. TM only\n');
        pol_choice = get_number('  Choice: ', 1, 3);
        
        if pol_choice == 1
            fprintf('\n  Calling: Fresnel(%.3f, %.3f, %.2f)\n', eps1, eps2, theta);
            result = Fresnel(eps1, eps2, theta);
        elseif pol_choice == 2
            fprintf('\n  Calling: Fresnel(%.3f, %.3f, %.2f, ''TE'')\n', eps1, eps2, theta);
            result = Fresnel(eps1, eps2, theta, 'TE');
        else
            fprintf('\n  Calling: Fresnel(%.3f, %.3f, %.2f, ''TM'')\n', eps1, eps2, theta);
            result = Fresnel(eps1, eps2, theta, 'TM');
        end
        
    elseif mode == 3
        % Snell's law
        fprintf('\n  --- Enter refractive indices ---\n');
        n1 = get_number('  n1: ', 0.1, 100);
        n2 = get_number('  n2: ', 0.1, 100);
        theta = get_number('  θi [degrees]: ', 0, 90);
        
        fprintf('\n  Calling: Fresnel(''snell'', %.4f, %.4f, %.2f)\n', n1, n2, theta);
        result = Fresnel('snell', n1, n2, theta);
        
    elseif mode == 4
        % Brewster angle
        fprintf('\n  --- Enter material properties ---\n');
        eps1 = get_number('  εr1: ', 0.1, 1000);
        eps2 = get_number('  εr2: ', 0.1, 1000);
        
        fprintf('\n  Calling: Fresnel(''brewster'', %.3f, %.3f)\n', eps1, eps2);
        result = Fresnel('brewster', eps1, eps2);
        
    else
        % Critical angle
        fprintf('\n  --- Enter material properties ---\n');
        fprintf('  (Note: n1 must be > n2 for TIR to exist)\n\n');
        eps1 = get_number('  εr1 (denser medium): ', 0.1, 1000);
        eps2 = get_number('  εr2 (less dense): ', 0.1, 1000);
        
        fprintf('\n  Calling: Fresnel(''critical'', %.3f, %.3f)\n', eps1, eps2);
        result = Fresnel('critical', eps1, eps2);
    end
end

%% ========================================================================
%  4. MEDIUM PROPERTIES
%% ========================================================================
function handle_medium()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       MEDIUM PROPERTIES\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What type of medium?\n\n');
    fprintf('    1. Lossless dielectric\n');
    fprintf('    2. Lossy medium (with conductivity σ)\n');
    fprintf('    3. From loss tangent tan(δ)\n');
    fprintf('    4. Good conductor\n');
    fprintf('    5. Skin depth only\n');
    fprintf('    6. Free space\n\n');
    
    mode = get_number('  Enter choice (1-6): ', 1, 6);
    
    if mode == 1
        % Lossless
        fprintf('\n  --- Enter parameters ---\n');
        eps_r = get_number('  εr: ', 0.1, 1000);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        fprintf('\n  Calling: Medium(%.3f, %.3e)\n', eps_r, freq);
        result = Medium(eps_r, freq);
        
    elseif mode == 2
        % Lossy
        fprintf('\n  --- Enter parameters ---\n');
        eps_r = get_number('  εr: ', 0.1, 1000);
        sigma = get_number('  σ [S/m]: ', 0, 1e10);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        use_name = get_yes_no('  Give it a name? (y/n): ');
        if use_name
            name = input('  Name: ', 's');
            fprintf('\n  Calling: Medium(%.3f, %.3e, %.3e, 1, ''%s'')\n', eps_r, sigma, freq, name);
            result = Medium(eps_r, sigma, freq, 1, name);
        else
            fprintf('\n  Calling: Medium(%.3f, %.3e, %.3e)\n', eps_r, sigma, freq);
            result = Medium(eps_r, sigma, freq);
        end
        
    elseif mode == 3
        % From loss tangent
        fprintf('\n  --- Enter parameters ---\n');
        eps_r = get_number('  εr: ', 0.1, 1000);
        tan_d = get_number('  tan(δ): ', 0, 1000);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        fprintf('\n  Calling: Medium(''tand'', %.3f, %.4f, %.3e)\n', eps_r, tan_d, freq);
        result = Medium('tand', eps_r, tan_d, freq);
        
    elseif mode == 4
        % Good conductor
        fprintf('\n  --- Enter parameters ---\n');
        sigma = get_number('  σ [S/m]: ', 1, 1e10);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        fprintf('\n  Calling: Medium(''conductor'', %.3e, %.3e)\n', sigma, freq);
        result = Medium('conductor', sigma, freq);
        
    elseif mode == 5
        % Skin depth
        fprintf('\n  --- Enter parameters ---\n');
        sigma = get_number('  σ [S/m]: ', 1, 1e10);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        fprintf('\n  Calling: Medium(''skin'', %.3e, %.3e)\n', sigma, freq);
        result = Medium('skin', sigma, freq);
        
    else
        % Free space
        fprintf('\n  --- Enter frequency ---\n');
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        fprintf('\n  Calling: Medium(''free'', %.3e)\n', freq);
        result = Medium('free', freq);
    end
end

%% ========================================================================
%  5. TRANSMISSION LINES
%% ========================================================================
function handle_tline()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       TRANSMISSION LINES\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What do you need?\n\n');
    fprintf('    1. Basic TL analysis (Zin, Γ, VSWR)\n');
    fprintf('    2. Find input impedance\n');
    fprintf('    3. Find load impedance\n');
    fprintf('    4. Reflection coefficient from Z\n');
    fprintf('    5. Impedance from Γ\n');
    fprintf('    6. Find load from Γ at input (Q13/Q14 type)\n');
    fprintf('    7. Quarter-wave transformer design\n');
    fprintf('    8. TL with series element\n');
    fprintf('    9. Stub design (realize impedance)\n\n');
    
    mode = get_number('  Enter choice (1-9): ', 1, 9);
    
    if mode == 1
        % Basic analysis
        fprintf('\n  --- Enter TL parameters ---\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        ZL_r = get_number('  ZL real part [Ω]: ', -10000, 10000);
        ZL_i = get_number('  ZL imag part [Ω]: ', -10000, 10000);
        ZL = ZL_r + 1j*ZL_i;
        len = get_number('  Length [wavelengths]: ', 0, 100);
        
        fprintf('\n  Calling: TLine(%.2f, %.2f%+.2fj, %.4f)\n', Z0, real(ZL), imag(ZL), len);
        result = TLine(Z0, ZL, len);
        
    elseif mode == 2
        % Find Zin
        fprintf('\n  --- Enter TL parameters ---\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        ZL_r = get_number('  ZL real part [Ω]: ', -10000, 10000);
        ZL_i = get_number('  ZL imag part [Ω]: ', -10000, 10000);
        ZL = ZL_r + 1j*ZL_i;
        len = get_number('  Length [wavelengths]: ', 0, 100);
        
        fprintf('\n  Calling: TLine(''Zin'', %.2f, %.2f%+.2fj, %.4f)\n', Z0, real(ZL), imag(ZL), len);
        result = TLine('Zin', Z0, ZL, len);
        
    elseif mode == 3
        % Find ZL
        fprintf('\n  --- Enter TL parameters ---\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        Zin_r = get_number('  Zin real part [Ω]: ', -10000, 10000);
        Zin_i = get_number('  Zin imag part [Ω]: ', -10000, 10000);
        Zin = Zin_r + 1j*Zin_i;
        len = get_number('  Length [wavelengths]: ', 0, 100);
        
        fprintf('\n  Calling: TLine(''ZL'', %.2f, %.2f%+.2fj, %.4f)\n', Z0, real(Zin), imag(Zin), len);
        result = TLine('ZL', Z0, Zin, len);
        
    elseif mode == 4
        % Gamma from Z
        fprintf('\n  --- Enter parameters ---\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        Z_r = get_number('  Z real part [Ω]: ', -10000, 10000);
        Z_i = get_number('  Z imag part [Ω]: ', -10000, 10000);
        Z = Z_r + 1j*Z_i;
        
        fprintf('\n  Calling: TLine(''Gamma'', %.2f, %.2f%+.2fj)\n', Z0, real(Z), imag(Z));
        result = TLine('Gamma', Z0, Z);
        
    elseif mode == 5
        % Z from Gamma
        fprintf('\n  --- Enter parameters ---\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        fprintf('\n  Enter Γ in polar form:\n');
        Gamma_mag = get_number('  |Γ|: ', 0, 10);
        Gamma_ang = get_number('  ∠Γ [degrees]: ', -180, 180);
        Gamma = Gamma_mag * exp(1j * deg2rad(Gamma_ang));
        
        fprintf('\n  Calling: TLine(''Z'', %.2f, %.4f∠%.2f°)\n', Z0, Gamma_mag, Gamma_ang);
        result = TLine('Z', Z0, Gamma);
        
    elseif mode == 6
        % Find load from Gamma_in (Q13/Q14)
        fprintf('\n  --- Q13/Q14 Type Problem ---\n');
        fprintf('  Given Γ at input, find Γ_L and Z_L\n\n');
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        fprintf('\n  Enter Γ_in in polar form:\n');
        Gamma_mag = get_number('  |Γ_in|: ', 0, 10);
        Gamma_ang = get_number('  ∠Γ_in [degrees]: ', -180, 180);
        Gamma_in = Gamma_mag * exp(1j * deg2rad(Gamma_ang));
        len = get_number('  Length [wavelengths]: ', 0, 100);
        
        fprintf('\n  Calling: TLine(''load'', %.2f, %.4f∠%.2f°, %.4f)\n', Z0, Gamma_mag, Gamma_ang, len);
        result = TLine('load', Z0, Gamma_in, len);
        
    elseif mode == 7
        % Quarter-wave transformer
        fprintf('\n  --- Quarter-Wave Transformer Design ---\n');
        Z_source = get_number('  Z_source [Ω]: ', 0.1, 10000);
        Z_load = get_number('  Z_load [Ω]: ', 0.1, 10000);
        
        fprintf('\n  Calling: TLine(''QW'', %.2f, %.2f)\n', Z_source, Z_load);
        result = TLine('QW', Z_source, Z_load);
        
    elseif mode == 8
        % TL with series element
        fprintf('\n  --- TL with Series Element ---\n');
        fprintf('  Element type:\n');
        fprintf('    1. Series Capacitor\n');
        fprintf('    2. Series Inductor\n');
        el_type = get_number('  Choice: ', 1, 2);
        
        Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
        ZL_r = get_number('  ZL real part [Ω]: ', -10000, 10000);
        ZL_i = get_number('  ZL imag part [Ω]: ', -10000, 10000);
        ZL = ZL_r + 1j*ZL_i;
        len = get_number('  Length [wavelengths]: ', 0, 100);
        freq = get_number('  Frequency [Hz]: ', 1, 1e15);
        
        if el_type == 1
            C = get_number('  Capacitance [F] (e.g., 1e-12): ', 0, 1);
            fprintf('\n  Calling: TLine(''series_C'', %.2f, ZL, %.4f, %.3e, %.3e)\n', Z0, len, C, freq);
            result = TLine('series_C', Z0, ZL, len, C, freq);
        else
            L = get_number('  Inductance [H] (e.g., 1e-9): ', 0, 1);
            fprintf('\n  Calling: TLine(''series_L'', %.2f, ZL, %.4f, %.3e, %.3e)\n', Z0, len, L, freq);
            result = TLine('series_L', Z0, ZL, len, L, freq);
        end
        
    else
        % Stub design
        fprintf('\n  --- Stub Design ---\n');
        fprintf('  Realize target impedance with stub\n\n');
        X_target = get_number('  Target reactance X [Ω] (jX): ', -10000, 10000);
        Z0_stub = get_number('  Stub Z0 [Ω]: ', 0.1, 10000);
        
        fprintf('\n  Stub type:\n');
        fprintf('    1. Short-circuited\n');
        fprintf('    2. Open-circuited\n');
        fprintf('    3. Show both\n');
        stub_type = get_number('  Choice: ', 1, 3);
        
        if stub_type == 1
            fprintf('\n  Calling: TLine(''stub'', j%.2f, %.2f, ''short'')\n', X_target, Z0_stub);
            result = TLine('stub', 1j*X_target, Z0_stub, 'short');
        elseif stub_type == 2
            fprintf('\n  Calling: TLine(''stub'', j%.2f, %.2f, ''open'')\n', X_target, Z0_stub);
            result = TLine('stub', 1j*X_target, Z0_stub, 'open');
        else
            fprintf('\n  Calling: TLine(''stub'', j%.2f, %.2f)\n', X_target, Z0_stub);
            result = TLine('stub', 1j*X_target, Z0_stub);
        end
    end
end

%% ========================================================================
%  6. STUB MATCHING
%% ========================================================================
function handle_stub_match()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       SINGLE-STUB MATCHING\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  --- Enter parameters ---\n');
    ZL_r = get_number('  ZL real part [Ω]: ', -10000, 10000);
    ZL_i = get_number('  ZL imag part [Ω]: ', -10000, 10000);
    ZL = ZL_r + 1j*ZL_i;
    Z0 = get_number('  Z0 [Ω]: ', 0.1, 10000);
    
    fprintf('\n  Stub type:\n');
    fprintf('    1. Short-circuited\n');
    fprintf('    2. Open-circuited\n');
    stub_type = get_number('  Choice: ', 1, 2);
    
    fprintf('\n  Do you know the wavelength λ?\n');
    has_lambda = get_yes_no('  (y/n): ');
    
    if has_lambda
        lambda = get_number('  λ [m]: ', 0, 1e10);
        if stub_type == 1
            fprintf('\n  Calling: StubMatch(%.2f%+.2fj, %.2f, ''short'', %.4f)\n', real(ZL), imag(ZL), Z0, lambda);
            result = StubMatch(ZL, Z0, 'short', lambda);
        else
            fprintf('\n  Calling: StubMatch(%.2f%+.2fj, %.2f, ''open'', %.4f)\n', real(ZL), imag(ZL), Z0, lambda);
            result = StubMatch(ZL, Z0, 'open', lambda);
        end
    else
        if stub_type == 1
            fprintf('\n  Calling: StubMatch(%.2f%+.2fj, %.2f, ''short'')\n', real(ZL), imag(ZL), Z0);
            result = StubMatch(ZL, Z0, 'short');
        else
            fprintf('\n  Calling: StubMatch(%.2f%+.2fj, %.2f, ''open'')\n', real(ZL), imag(ZL), Z0);
            result = StubMatch(ZL, Z0, 'open');
        end
    end
end

%% ========================================================================
%  7. POYNTING VECTOR / H-FIELD
%% ========================================================================
function handle_poynting()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       POYNTING VECTOR & H-FIELD\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  What format is your E-field?\n\n');
    fprintf('    1. Time-domain: E = E0*(a·cos + b·sin)\n');
    fprintf('    2. Complex phasor E directly\n\n');
    
    format = get_number('  Enter format (1-2): ', 1, 2);
    
    if format == 1
        % Time-domain
        fprintf('\n  --- Enter a vector (cos coefficient) ---\n');
        ax = get_number('  ax: ', -1e10, 1e10);
        ay = get_number('  ay: ', -1e10, 1e10);
        az = get_number('  az: ', -1e10, 1e10);
        a = [ax; ay; az];
        
        fprintf('\n  --- Enter b vector (sin coefficient) ---\n');
        bx = get_number('  bx: ', -1e10, 1e10);
        by = get_number('  by: ', -1e10, 1e10);
        bz = get_number('  bz: ', -1e10, 1e10);
        b = [bx; by; bz];
        
        E0 = get_number('  E0 amplitude [V/m]: ', 0, 1e10);
        
        fprintf('\n  --- Enter β vector ---\n');
        bx = get_number('  βx: ', -1e10, 1e10);
        by = get_number('  βy: ', -1e10, 1e10);
        bz = get_number('  βz: ', -1e10, 1e10);
        beta_vec = [bx; by; bz];
        
        fprintf('\n  Use custom η? (default is 377 Ω)\n');
        custom_eta = get_yes_no('  Custom η? (y/n): ');
        
        if custom_eta
            eta = get_number('  Enter η [Ω]: ', 0, 1e6);
            fprintf('\n  Calling: poynting_pw(''time'', a, b, %.2f, beta, %.2f)\n', E0, eta);
            result = poynting_pw('time', a, b, E0, beta_vec, eta);
        else
            fprintf('\n  Calling: poynting_pw(''time'', a, b, %.2f, beta)\n', E0);
            result = poynting_pw('time', a, b, E0, beta_vec);
        end
        
    else
        % Complex phasor
        fprintf('\n  --- Enter E phasor components ---\n');
        Ex = get_complex('  Ex: ');
        Ey = get_complex('  Ey: ');
        Ez = get_complex('  Ez: ');
        E = [Ex; Ey; Ez];
        
        fprintf('\n  --- Enter k or β vector ---\n');
        kx = get_number('  kx: ', -1e10, 1e10);
        ky = get_number('  ky: ', -1e10, 1e10);
        kz = get_number('  kz: ', -1e10, 1e10);
        k = [kx; ky; kz];
        
        fprintf('\n  Use custom η? (default is 377 Ω)\n');
        custom_eta = get_yes_no('  Custom η? (y/n): ');
        
        if custom_eta
            eta = get_number('  Enter η [Ω]: ', 0, 1e6);
            fprintf('\n  Calling: poynting_pw(E, k, %.2f)\n', eta);
            result = poynting_pw(E, k, eta);
        else
            fprintf('\n  Calling: poynting_pw(E, k)\n');
            result = poynting_pw(E, k);
        end
    end
end

%% ========================================================================
%  8. B-FIELD FROM INFINITE WIRE
%% ========================================================================
function handle_bfield_wire()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       B-FIELD FROM INFINITE WIRE\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  --- Enter parameters ---\n');
    I = get_number('  Current I [A]: ', -1e10, 1e10);
    r = get_number('  Distance r [m]: ', 1e-10, 1e10);
    
    fprintf('\n  Is the material magnetic (μr ≠ 1)?\n');
    use_mu = get_yes_no('  (y/n): ');
    
    if use_mu
        mu_r = get_number('  μr: ', 0.1, 1e6);
        fprintf('\n  Calling: B_inf_wire(%.4f, %.4e, %.2f)\n', I, r, mu_r);
        B = B_inf_wire(I, r, mu_r);
    else
        fprintf('\n  Calling: B_inf_wire(%.4f, %.4e)\n', I, r);
        B = B_inf_wire(I, r);
    end
    
    fprintf('\n  ═══════════════════════════════════════════\n');
    fprintf('       RESULT\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('  B = %.6e T\n', B);
    fprintf('  B = %.6f μT\n', B * 1e6);
    fprintf('  B = %.6f mT\n', B * 1e3);
    fprintf('  ═══════════════════════════════════════════\n');
end

%% ========================================================================
%  9. COULOMB FORCE
%% ========================================================================
function handle_coulomb()
    clc;
    fprintf('\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('       COULOMB FORCE BETWEEN CHARGES\n');
    fprintf('  ═══════════════════════════════════════════\n\n');
    
    fprintf('  --- Enter charge 1 ---\n');
    q1 = get_number('  q1 [C]: ', -1e10, 1e10);
    fprintf('  Position r1:\n');
    r1x = get_number('    x [m]: ', -1e10, 1e10);
    r1y = get_number('    y [m]: ', -1e10, 1e10);
    r1z = get_number('    z [m]: ', -1e10, 1e10);
    r1 = [r1x; r1y; r1z];
    
    fprintf('\n  --- Enter charge 2 ---\n');
    q2 = get_number('  q2 [C]: ', -1e10, 1e10);
    fprintf('  Position r2:\n');
    r2x = get_number('    x [m]: ', -1e10, 1e10);
    r2y = get_number('    y [m]: ', -1e10, 1e10);
    r2z = get_number('    z [m]: ', -1e10, 1e10);
    r2 = [r2x; r2y; r2z];
    
    fprintf('\n  Calling: coulomb_pair(%.3e, %.3e, r1, r2)\n', q1, q2);
    [F12, F21] = coulomb_pair(q1, q2, r1, r2);
    
    fprintf('\n  ═══════════════════════════════════════════\n');
    fprintf('       RESULT\n');
    fprintf('  ═══════════════════════════════════════════\n');
    fprintf('  F12 (force on q1 due to q2):\n');
    fprintf('    = [%.6e; %.6e; %.6e] N\n', F12(1), F12(2), F12(3));
    fprintf('    |F12| = %.6e N\n', norm(F12));
    fprintf('\n  F21 (force on q2 due to q1):\n');
    fprintf('    = [%.6e; %.6e; %.6e] N\n', F21(1), F21(2), F21(3));
    fprintf('    |F21| = %.6e N\n', norm(F21));
    fprintf('  ═══════════════════════════════════════════\n');
end

%% ========================================================================
%  INPUT HELPER FUNCTIONS
%% ========================================================================
function val = get_number(prompt, min_val, max_val)
    while true
        try
            val = input(prompt);
            if isempty(val)
                val = 0;
            end
            if ~isscalar(val) || ~isnumeric(val) || ~isreal(val)
                fprintf('    ⚠ Please enter a real number.\n');
                continue;
            end
            if val < min_val || val > max_val
                fprintf('    ⚠ Value must be between %.2g and %.2g.\n', min_val, max_val);
                continue;
            end
            break;
        catch
            fprintf('    ⚠ Invalid input. Please enter a number.\n');
        end
    end
end

function val = get_complex(prompt)
    while true
        try
            fprintf('%s', prompt);
            str = input('', 's');
            if isempty(str)
                val = 0;
                break;
            end
            % Replace 'j' with '1j' for MATLAB compatibility
            str = regexprep(str, '(?<![0-9])j', '1j');
            str = regexprep(str, '(\d)j', '$1*1j');
            val = eval(str);
            if ~isscalar(val) || ~isnumeric(val)
                fprintf('    ⚠ Please enter a scalar number.\n');
                continue;
            end
            break;
        catch
            fprintf('    ⚠ Invalid input. Examples: 0, 5, -1j, 1+2j, 1j*3\n');
        end
    end
end

function val = get_yes_no(prompt)
    while true
        response = input(prompt, 's');
        if isempty(response)
            val = false;
            break;
        end
        response = lower(strtrim(response));
        if strcmp(response, 'y') || strcmp(response, 'yes')
            val = true;
            break;
        elseif strcmp(response, 'n') || strcmp(response, 'no')
            val = false;
            break;
        else
            fprintf('    ⚠ Please enter y or n.\n');
        end
    end
end
