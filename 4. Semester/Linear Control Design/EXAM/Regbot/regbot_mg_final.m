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
Gwv = minreal(tf(num, den))
bode(Gwv)
nyquist(-Gwv)
kps=30;
Gs=-kps*Gwv
bode(Gs)
nyquist(Gs)
tau_i=1/8.38
Gi=tf([tau_i,1],[tau_i,0])

nyquist(-Gi*Gwv)
bode(-Gi*Gwv)


%% 



Phi_d=6;
solve(Phi_d==asind((1-a)/(1+a)),c)
b=0.81;
asind((1-b)/(1+b))
Wc=100;
alpha=0.2;
Tau_d=1/(Wc*sqrt(alpha))

GL=tf([Tau_d,1],[alpha*Tau_d,1])
figure(1)
bode(Gi*GL*Gs)

Md=1/sqrt(b)
kp=1/(abs((-Gi*Gs))*Md)






omega_i=8.38;
tau_i=1/omega_i
Cpi=tf([tau_i,1],[tau_i,0])
figure(1)
hold on
bode(-1*Gwv)
bode(Cpi)
hold off

solve(-180+60==-183-atan(1/1)+asin((1-x)/(1+x)),x)
%% Bodeplot
h = figure(100)
bode(Gwv)
grid on
title('Transfer function from motor voltage to velocity')
saveas(h, 'motor to velocity.png');
