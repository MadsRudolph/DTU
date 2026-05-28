%% Simscape multibody model og Regbot in balance
% initial setup with motor velocity controller 
% this is intended as simulation base for balance control.
%
close all
clear

%% Simulink model name
model='regbot_1mg';

%% parameters for REGBOT
% motor
RA = 3.3/2;    % ohm (2 motors)
JA = 1.3e-6*2; % motor inertia
LA = 6.6e-3/2; % rotor inductor (2 motors)
BA = 3e-6*2;   % rotor friction
Kemf = 0.0105; % motor constant
Km = Kemf;
% køretøj
NG = 9.69; % gear
WR = 0.03; % wheel radius
Bw = 0.155; % wheel distance
% 
% model parts used in Simulink
mmotor = 0.193;   % total mass of motor and gear [kg]
mframe = 0.32;    % total mass of frame and base print [kg]
mtopextra = 0.97 - mframe - mmotor; % extra mass on top (charger and battery) [kg]
mpdist =  0.10;   % distance to lit [m]
% disturbance position (Z)
pushDist = 0.1; % relative to motor axle [m]

%% wheel velocity controller (no balance) PI-regulator
% sample (usable) controller values
Kpwv = 15;     % Kp
tiwv = 0.05;   % Tau_i
Kffwv = 0;     % feed forward constant
startAngle = 10;  % tilt in degrees at time zero
twvlp = 0.005;    % velocity noise low pass filter time constant (recommended)

%% Estimate transfer function for base system using LINEARIZE
% Motor volatge to wheel velocity (wv)
load_system(model);
open_system(model);
% define points in model
ios(1) = linio(strcat(model,'/vel_ref'),1,'openinput');
ios(2) = linio(strcat(model, '/robot with balance'),1,'openoutput');
% attach to model
setlinio(model,ios);
% Use the snapshot time(s) 0 seconds
op = [0];
% Linearize the model
sys = linearize(model,ios,op);
% get transfer function
[num,den] = ss2tf(sys.A, sys.B, sys.C, sys.D);
Gtv = minreal(tf(num, den))
bode(-Gtv)
nyquist(-Gtv)
tau_ip=1/8.38
Gi_post=tf([tau_ip,1],[tau_ip,0])

Gtv_post=-Gi_post*Gtv

nyquist(Gtv_post)
margin(Gtv_post)

%design af PID 
%Vi vælger alpha og Ni til nogle værider og en ønsket phase margin
alpha=0.02;
Ni=6;
%Ønsket phase margin
Ym=75;
%Udregning af phaser for Pi og lead
Phi_i=-atand(1/Ni)
Phi_d=asind((1-alpha)/(1+alpha))
%phase for Gtv_post findes en ny Wc
Phi_G=Ym-Phi_i-180-Phi_d
%64.7 med en ym= 60 og NI = 3
Wc=100
%Tidskonstanter for I og D led
Tau_i1=Ni/Wc
Tau_d1=1/(Wc*sqrt(alpha))
%Overføringsfunktion for Pi og Lead
Cpi=tf([Tau_i1,1],[Tau_i1,0])
CD=tf([Tau_d1,1],[alpha*Tau_d1,1])
%Finder gain for Kp ud fra den nye Wc
[magc , phasec] = bode (Gtv_post*Cpi*CD, Wc) ; 
Kp=1/magc
%open loop
Gtvol=Kp*CD*Cpi*Gtv_post
%closed loop
Gtvcl=Gtvol/(1+Gtvol)

[magGcl , phaseGcl] = bode(Gtvcl, 8.53);

prefilt = tf([1],[0.07429075346,1])

[numpf denpf] = tfdata(prefilt, 'v');

margin(Gtvol);

margin(Gtvcl);
figure(Gtvcl);


[numPi denPi] = tfdata(Cpi, 'v');
[numGcl denGcl] = tfdata(Gtvcl, 'v');
[numD denD] = tfdata(CD, 'v');