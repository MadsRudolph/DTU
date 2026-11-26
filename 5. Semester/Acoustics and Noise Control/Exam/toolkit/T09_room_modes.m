%% T09 - Room modes of a rectangular room
% 34840 exam toolkit. Fill in the GIVEN block, run, read the printed lines.
%
% Solves: all natural frequencies below f_max (sorted, with type), which
% modes fall in a given (third-)octave band, which ones are audible at the
% centre, a room dimension from a known mode, mode count and modal
% density, Schroeder frequency.
%
% Matches: Week 6 P1 (pre-filled 5 x 4 x 3 m: 34.3, 42.9, 54.9, 57.2, 66.7,
% 68.6, 71.5, 79.3 Hz), Week 6 P2 (cube, degenerate modes), 2022 MC4
% (block C: height = 4.25 m -> answer B "4 m"; the official solution has a
% typo, 2/ly^2 instead of (2/ly)^2, and gets exactly 4 m), 2023 MC3
% (block D: 7.2 x 5.4 x 3 m, 50 Hz third octave -> (2,0,0) at 47.6 Hz),
% 2024 MC5 (block D2: 6 x 9 x 3 m, 57 Hz -> (2,0,0) at 57.2 Hz).

%% Constants
c = 343;

%% GIVEN - edit these
lx = 5;  ly = 4;  lz = 3;  % room dimensions [m]
f_max = 80;                % list modes below this [Hz]
n_max = 6;                 % highest index tried in each direction

%% Step 1 - Every mode up to n_max in each direction
% $$f_{n_x n_y n_z} = \frac c2\sqrt{\left(\frac{n_x}{l_x}\right)^2+\left(\frac{n_y}{l_y}\right)^2+\left(\frac{n_z}{l_z}\right)^2}$$
[nx, ny, nz] = ndgrid(0:n_max, 0:n_max, 0:n_max);
f_all = c/2*sqrt((nx/lx).^2 + (ny/ly).^2 + (nz/lz).^2);
keep = f_all > 0 & f_all < f_max;
[f_sorted, order] = sort(f_all(keep));
N_list = [nx(keep) ny(keep) nz(keep)];
% Columns: nx ny nz f[Hz] type(1 axial, 2 tangential, 3 oblique)
modes = [N_list(order,:), round(f_sorted*10)/10, sum(N_list(order,:) > 0, 2)]
n_modes_below = numel(f_sorted)        % 8 below 80 Hz in 5x4x3 (Week 6)

%% Step 2 - Axial modes and the lowest mode
% $$f_{1,0,0} = \frac{c}{2l_x}$$
f_100 = c/(2*lx)                       % 34.3 Hz (official)
f_010 = c/(2*ly)
f_001 = c/(2*lz)

%% Step 3 - Which modes are heard in the CENTRE / in a CORNER?
% Odd index -> cos(n pi/2) = 0 -> node in the centre. Only all-even modes
% have a maximum in the centre. EVERY mode is maximal in a corner.
centre_audible = modes(all(mod(modes(:,1:3),2) == 0, 2), :)   % (2,0,0) only (Week 6 P1.2)

%% Step 4 - Modes inside a band
% Third octave: [fc 2^{-1/6}, fc 2^{1/6}]   Octave: [fc/sqrt2, fc sqrt2]
fc_band = 50;                          % GIVEN band centre [Hz]
band = [fc_band*2^(-1/6) fc_band*2^(1/6)]   % 44.5 - 56.1 Hz
in_band = modes(modes(:,4) >= band(1) & modes(:,4) < band(2), :)

%% Step 5 - Mode count and modal density (high-f estimates)
% $$N(f) \approx \frac{4\pi V}{3}\left(\frac fc\right)^3+\frac{\pi S}{4}\left(\frac fc\right)^2+\frac{L}{8}\frac fc,\qquad \frac{dN}{df}\approx\frac{4\pi V f^2}{c^3}$$
V = lx*ly*lz
S_tot = 2*(lx*ly + lx*lz + ly*lz)
L_edges = 4*(lx + ly + lz)
N_est = 4*pi*V/3*(f_max/c)^3 + pi*S_tot/4*(f_max/c)^2 + L_edges/8*f_max/c   % 8.6 vs 8 counted
dNdf = 4*pi*V*f_max^2/c^3
% Schroeder frequency (above it: diffuse field), T in s, V in m^3:
T_room = 0.5;                          % GIVEN reverberation time [s]
f_Schroeder = 2000*sqrt(T_room/V)

%% C - A dimension from known modes (2022 MC4)
% f(0,1,0) = 10 Hz -> ly; f(0,2,1) = 45 Hz -> lz.
% $$l_y = \frac{c}{2 f_{010}},\qquad \frac{1}{l_z} = \sqrt{\left(\frac{2 f_{021}}{c}\right)^2-\left(\frac{2}{l_y}\right)^2}$$
ly_C = c/(2*10)
lz_C = 1/sqrt((2*45/c)^2 - (2/ly_C)^2)   % 4.25 m -> nearest option B) 4 m

%% D - Which mode gives the peak? (2023 MC3 and 2024 MC5)
[ax, ay, az] = ndgrid(0:3, 0:3, 0:3);
fD = c/2*sqrt((ax/7.2).^2 + (ay/5.4).^2 + (az/3).^2);
pickD = fD >= 50*2^(-1/6) & fD < 50*2^(1/6);
modes_2023 = [ax(pickD) ay(pickD) az(pickD) fD(pickD)]   % (2,0,0) at 47.6 Hz
fD2 = c/2*sqrt((ax/6).^2 + (ay/9).^2 + (az/3).^2);
pickD2 = abs(fD2 - 57) < 1.5;
modes_2024 = [ax(pickD2) ay(pickD2) az(pickD2) fD2(pickD2)]   % (2,0,0), (0,3,0), (0,0,1) all 57.2 Hz; of the options only (2,0,0)
