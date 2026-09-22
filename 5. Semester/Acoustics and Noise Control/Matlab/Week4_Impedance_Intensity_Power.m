%% Lecture 4 - Impedance, intensity and sound power
% 34840 Fundamentals of Acoustics and Noise Control | 22 September 2026
%
% This is a worked learning document. Read the short explanation, inspect
% the calculation, then compare the result with the interpretation below it.
% The accompanying .mlx file opens as a formatted MATLAB Live Script.
% Run the document from the top once. After that, each problem can be rerun
% with Run Section. No extra toolboxes are needed.
%
% Source: 34840 - Problems 4.pdf, including both pages and the exam examples.
% All logarithms for levels are base 10. SPL always uses RMS pressure.

%% Our constants and units
% We use SI units inside the calculations: metres, cubic metres, kilograms,
% pascals and watts. The sheet uses rounded room-temperature air constants.
% For travelling-wave calculations we use rho*c = 413 Pa s/m; for masses and
% cavity stiffness we use rho = 1.2 kg/m^3 and c = 343 m/s.
c = 343;               % speed of sound [m/s]
rho = 1.2;             % air density [kg/m^3]
z_air = 413;           % characteristic impedance [Pa s/m]
p_ref = 20e-6;         % reference RMS sound pressure [Pa]
W_ref = 1e-12;          % reference sound power [W]

%% Problem 1 - Why does a bottle have a resonance?
% The air in the neck moves like a mass. The air in the bottle compresses
% like a spring. At resonance the two reactances cancel.
%
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{S}{V l_{eff}}}$$
%
% Given: 400 ml bottle, 20 mm neck diameter, 21 mm effective neck length.
% The effective length already includes the end correction.
V = 400e-6;            % 400 ml -> m^3
neck_diameter = 20e-3; % 20 mm -> m
neck_length = 21e-3;   % effective length [m]
S = pi*(neck_diameter/2)^2;
f_bottle = c/(2*pi)*sqrt(S/(V*neck_length));
fprintf('Bottle resonance = %.1f Hz (sheet: 334 Hz)\n', f_bottle);

%% Problem 1 - See what changing the volume does
% A larger bottle is a softer spring, so it resonates at a lower frequency.
% This plot changes only the volume; the neck stays the same.
volume_ml = 100:5:1000;
frequency = c/(2*pi)*sqrt(S./(volume_ml*1e-6*neck_length));
figure('Name','Bottle volume and resonance');
plot(volume_ml,frequency,'LineWidth',1.8); hold on;
plot(400,f_bottle,'o','MarkerFaceColor',[0.15 0.55 0.5]);
grid on; xlabel('Bottle volume [ml]'); ylabel('Resonance frequency [Hz]');
title('A larger cavity lowers the resonance');

%% Problem 2 - From SPL to sound power
% Given: 82 dB SPL and 10 m^2 perpendicular to a travelling plane wave.
% First undo the logarithm to get RMS pressure. Then find intensity and
% multiply by area. Intensity is power per square metre.
%
% $$p_{rms}=p_{ref}10^{L_p/20},\quad I=\frac{p_{rms}^2}{\rho c},\quad W=IS$$
Lp = 82;               % sound pressure level [dB]
area = 10;             % perpendicular area [m^2]
p_rms = p_ref*10^(Lp/20);
intensity = p_rms^2/z_air;
W_plane = intensity*area;
fprintf('RMS pressure = %.4f Pa\n',p_rms);
fprintf('Intensity = %.4f mW/m^2\n',intensity*1000);
fprintf('Power = %.3f mW (sheet: 1.54 mW)\n',W_plane*1000);
% There is no extra factor of 1/2 because our pressure is already RMS.

%% Problem 3.1 - Water to air: pressure and energy are different
% For a normally incident plane wave, pressure transmission is
% Tp = 2*z2/(z1+z2). To find transmitted intensity, also account for the
% change of characteristic impedance.
%
% $$\tau=\frac{I_t}{I_i}=T_p^2\frac{z_1}{z_2}$$
%
% Positive attenuation means incident intensity divided by transmitted
% intensity: A = -10*log10(tau). A transmitted-minus-incident level
% difference would have the opposite sign.
z_water = 1000*1480;   % density * speed [Pa s/m]
Tp_water_air = 2*z_air/(z_water+z_air);
tau_water_air = Tp_water_air^2*z_water/z_air;
atten_water_air = -10*log10(tau_water_air);
fprintf('Transmitted pressure fraction = %.7f\n',Tp_water_air);
fprintf('Transmitted intensity = %.4f percent\n',100*tau_water_air);
fprintf('Intensity attenuation = %.2f dB (sheet: about 30 dB)\n',atten_water_air);

%% Problem 3.2 - Air to water: reverse the direction
% The pressure almost doubles in water, yet very little power crosses.
% Water has a much larger impedance, so its particle velocity is small.
Tp_air_water = 2*z_water/(z_air+z_water);
tau_air_water = Tp_air_water^2*z_air/z_water;
atten_air_water = -10*log10(tau_air_water);
fprintf('Transmitted pressure fraction = %.6f\n',Tp_air_water);
fprintf('Transmitted intensity = %.4f percent\n',100*tau_air_water);
fprintf('Intensity attenuation = %.2f dB\n',atten_air_water);
% Both directions give 29.52 dB intensity attenuation. Compare Week 2:
% pressure attenuation was about 65.1 dB water-to-air and -6.02 dB
% air-to-water. Squaring pressure transmission alone misses this distinction.
pressure_attenuation = 20*log10(1./[Tp_water_air Tp_air_water]);
fprintf('Pressure attenuations: water-air %.2f dB; air-water %.2f dB\n', ...
    pressure_attenuation(1),pressure_attenuation(2));

%% Problem 4.1 - Absorption from the standing-wave ratio
% Given: 85 dB maximum and 74 dB minimum in a 1 m tube of area 0.01 m^2.
% The tone is 1 kHz. The level difference gives a pressure ratio s.
% From s we obtain the magnitude of reflection R, then absorption alpha.
%
% $$s=10^{(L_{max}-L_{min})/20},\quad |R|=\frac{s-1}{s+1},\quad \alpha=1-|R|^2$$
Lmax = 85;
Lmin = 74;
tube_area = 0.01;
s = 10^((Lmax-Lmin)/20);
R = (s-1)/(s+1);
alpha = 1-R^2;
fprintf('Standing-wave ratio = %.4f\n',s);
fprintf('Reflection magnitude = %.4f\n',R);
fprintf('Absorption coefficient = %.4f (sheet: 0.69)\n',alpha);

%% Problem 4.2 - Recover the two travelling waves
% At a maximum the pressures add; at a minimum they oppose each other.
% Use RMS values consistently. Subtract reflected power from incident power.
pmax = p_ref*10^(Lmax/20);
pmin = p_ref*10^(Lmin/20);
p_incident = (pmax+pmin)/2;
p_reflected = (pmax-pmin)/2;
W_incident = tube_area*p_incident^2/z_air;
W_reflected = tube_area*p_reflected^2/z_air;
W_absorbed = W_incident-W_reflected;
LW_absorbed = 10*log10(W_absorbed/W_ref);
fprintf('Incident power = %.4f microW\n',W_incident*1e6);
fprintf('Reflected power = %.4f microW\n',W_reflected*1e6);
fprintf('Absorbed power = %.4f microW (sheet: 0.87 microW)\n',W_absorbed*1e6);
fprintf('Absorbed power level = %.2f dB (sheet: 59.4 dB)\n',LW_absorbed);
% Our 0.863 microW agrees within rounding with the sheet. As a quick check,
% W_absorbed also equals tube_area*pmax*pmin/z_air.
% Tube length and frequency determine where the extrema occur, but are not
% needed to find power once both extrema are known.

%% Problem 4 - What does the pressure pattern look like?
% We choose a pressure maximum as x = 0. The wall position and reflection
% phase cannot be recovered from the extrema levels alone.
f = 1000;
k = 2*pi*f/c;
x = linspace(0,1,1000);
p_envelope = sqrt(p_incident^2+p_reflected^2 + ...
    2*p_incident*p_reflected*cos(2*k*x));
L_envelope = 20*log10(p_envelope/p_ref);
figure('Name','Standing wave in the tube');
plot(x,L_envelope,'LineWidth',1.6); grid on;
yline(Lmax,'--','85 dB maximum'); yline(Lmin,'--','74 dB minimum');
xlabel('Distance from a pressure maximum [m]'); ylabel('Sound pressure level [dB]');
title('Pressure varies with position; net power stays constant');

%% Problem 5.1 - The loudspeaker cone and cabinet
% Given: 150 mm cone diameter, 20 g moving mass, 16 litre sealed cabinet.
% Neglect suspension stiffness and external radiation impedance.
% Convert the mechanical mass through S^2, and treat the cabinet as an
% acoustic spring. The impedances are Za_cone = 1i*omega*Ma and
% Za_box = Ka/(1i*omega), both in N s/m^5.
%
% $$M_a=M/S^2,\quad K_a=\rho c^2/V,\quad f_0=\frac{1}{2\pi}\sqrt{K_a/M_a}$$
cone_diameter = 150e-3;
cone_mass = 20e-3;
box_volume = 16e-3;
cone_area = pi*(cone_diameter/2)^2;
Ma = cone_mass/cone_area^2;
Ka = rho*c^2/box_volume;
f_box = sqrt(Ka/Ma)/(2*pi);
fprintf('Za_cone = 1i*omega*%.3f [N s/m^5]\n',Ma);
fprintf('Za_box = %.6g/(1i*omega) [N s/m^5]\n',Ka);
fprintf('Natural frequency = %.2f Hz (sheet: 59 Hz)\n',f_box);
% Below this frequency the air spring dominates; above it, the cone mass
% dominates. At resonance the two imaginary impedance terms cancel.

%% Problem 5.2 - Internal SPL at the displacement limit
% The limit is 4 mm PEAK TO PEAK. That means only 2 mm peak displacement.
% The cone changes the cavity volume by S*x. Adiabatic compression gives
% pressure amplitude Ka*S*x_peak. Divide by sqrt(2) before calculating SPL.
x_peak_to_peak = 4e-3;
x_peak = x_peak_to_peak/2;
p_peak_box = Ka*cone_area*x_peak;
p_rms_box = p_peak_box/sqrt(2);
Lp_box = 20*log10(p_rms_box/p_ref);
fprintf('Peak displacement = %.1f mm\n',x_peak*1000);
fprintf('Peak internal pressure = %.2f Pa\n',p_peak_box);
fprintf('RMS internal pressure = %.2f Pa\n',p_rms_box);
fprintf('Internal SPL = %.2f dB (sheet: 140.9 dB)\n',Lp_box);
% This is pressure INSIDE the sealed cabinet. It is not the radiated SPL
% outside. At a prescribed displacement this ideal cavity pressure does
% not depend on frequency, while the uniform-pressure approximation holds.

%% Exam A.1 - Which intensity does the question ask for?
% A 10 cm diameter tube terminates in a sample absorbing 1 microW, which
% is 10 percent of the incident power. Net intensity is absorbed power
% divided by tube area. The incident intensity is ten times larger.
exam_area = pi*(0.10/2)^2;
exam_alpha = 0.10;
exam_W_absorbed = 1e-6;
exam_W_incident = exam_W_absorbed/exam_alpha;
exam_I_net = exam_W_absorbed/exam_area;
exam_I_incident = exam_W_incident/exam_area;
exam_I_reflected = -(1-exam_alpha)*exam_I_incident;
fprintf('Net intensity = %.7f W/m^2\n',exam_I_net);
fprintf('Incident intensity = %.7f W/m^2\n',exam_I_incident);
fprintf('Reflected intensity (signed) = %.7f W/m^2\n',exam_I_reflected);
% The signed incident and reflected intensities add to the net intensity.

%% Exam A.2 - Maximum pressure level
% Convert absorption to reflection magnitude. At a pressure maximum,
% incident and reflected pressures add constructively.
exam_R = sqrt(1-exam_alpha);
exam_p_incident = sqrt(z_air*exam_I_incident);
exam_pmax = exam_p_incident*(1+exam_R);
exam_Lmax = 20*log10(exam_pmax/p_ref);
fprintf('Maximum RMS pressure = %.4f Pa\n',exam_pmax);
fprintf('Maximum SPL = %.2f dB\n',exam_Lmax);
% Answer: about 97.0 dB. Strong reflection produces a high pressure
% maximum even though the sample absorbs only a small fraction of power.

%% Multiple choice 1 - Put third-octave energy into octave bands
% Only the listed third-octave bands contain energy. Missing bands add
% zero energy, not a 0 dB contribution. Add mean squares, never dB values.
% 125 Hz octave: 100 and 160 Hz bands (56 and 58 dB).
% 250 Hz octave: only the 250 Hz band (60 dB).
% 500 Hz octave: 400 and 630 Hz bands (62 and 64 dB).
% 1000 Hz octave: only the 1000 Hz band (66 dB).
L125 = 10*log10(10^(56/10)+10^(58/10));
L250 = 60;
L500 = 10*log10(10^(62/10)+10^(64/10));
L1000 = 66;
fprintf('Octave levels = %.2f, %.2f, %.2f, %.2f dB\n',L125,L250,L500,L1000);
% Rounded: (60, 60, 66, 66) dB. Answer c.

%% Multiple choice 2 - Distance from free-field sound level
% At 1 m the level is 64 dB. For spherical spreading pressure falls as 1/r.
%
% $$r=r_0 10^{(L_0-L)/20}$$
L_other = [70 61 44];
distances = 1*10.^((64-L_other)/20);
fprintf('Distances = %.3f, %.3f, %.3f m\n',distances);
% Answer c: 0.5 m, 1.4 m, 10 m. A 20 dB drop means ten times the distance.
% This assumes the same source with negligible reflections and air loss.

%% Multiple choice 3 - Absorption from two measured levels
% Incident SPL is 90 dB, reflected SPL is 70 dB. Because both waves are
% in the same medium, their intensity ratio is 10^((70-90)/10).
reflected_fraction = 10^((70-90)/10);
alpha_mc = 1-reflected_fraction;
fprintf('Absorption coefficient = %.2f\n',alpha_mc);
% Answer d: 0.99. The pressure reflection magnitude is 0.1, but the
% reflected power fraction is its square, 0.01.

%% The answers to remember
% * Bottle: 334 Hz.
% * Plane-wave power: 1.54 mW.
% * Water/air intensity attenuation: about 30 dB in both directions.
% * Tube: alpha = 0.686, absorbed power = 0.863 microW, power level = 59.36 dB.
% * Cabinet: 59.1 Hz resonance and 140.85 dB internal SPL.
% * Exam A: net intensity = 0.1273 mW/m^2 and maximum SPL = 97.0 dB.
% * Multiple choice: c, c, d.
