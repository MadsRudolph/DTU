%% Simscape multibody model og Regbot in balance
% initial setup with motor velocity controller 
% this is intended as simulation base for balance control.
%
close all
% Num_post=1
% Den_post=1
% Num_inte=1
% Den_inte=1
% Num_Lead=1
% Den_Lead=1
% kp=1
% kp_vel=1
% Num_filt=1
% Den_filt=1
% Num_inte_vel=1
% Den_inte_vel=1
% Num_Lead_vel=1
% Den_Lead_vel=1

clear

%% Simulink model name
model='regbot__Start_mg';

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
[~,feqpeak]=getPeakGain(Gtv)
tau_ip=1/feqpeak
Gi_post=tf([tau_ip,1],[tau_ip,0])
[Num_post,Den_post]=tfdata(Gi_post,'v')

Gtv_post=minreal(-Gi_post*Gtv)

nyquist(Gtv_post)
margin(Gtv_post)

%% Plots til raporten
Without_post=-Gtv;
With_post=Gtv_post;

figure(1)
xline(8.8,'-r');
legend
hold on


bode(Gtv)
bode(Gtv_post)
hold off

figure(2)
hold on
legend
nyquist(Gtv)
nyquist(Gtv_post)
hold off


%% Tilt controller
%design af PID 
w = logspace ( - 2 , 3 , 5000) ;  %frequency from 10ˆ -2 t i l 10ˆ2 rad/...
[mag phase ]=bode (Gtv_post ,w) ;
%Vi vælger alpha og Ni til nogle værider og en ønsket phase margin
alpha=0.03;
%0.01 0.04 0.03
Ni=6;
%6 6 6
%Ønsket phase margin
Ym=80;
%80 90 80


%Udregning af phaser for Pi og lead
Phi_i=-atand(1/Ni)
Phi_d=asind((1-alpha)/(1+alpha))
%phase for Gtv_post findes en ny Wc
Phi_G=-180+Ym-Phi_i-Phi_d
%64.7 med en ym= 60 og NI = 3
n = find ( phase > Phi_G , 1 , 'last') ; 
Wc=w(n)

%Tidskonstanter for I og D led
Tau_i1=Ni/Wc
Tau_d1=1/(Wc*sqrt(alpha))
%Overføringsfunktion for Pi og Lead
Cpi=minreal(tf([Tau_i1,1],[Tau_i1,0]))
[Num_inte,Den_inte]=tfdata(Cpi,'v')
CD=minreal(tf([Tau_d1,1],[alpha*Tau_d1,1]))
[Num_Lead,Den_Lead]=tfdata(CD,'v')

%Finder gain for Kp ud fra den nye Wc 
[magc , phasec] = bode (Gtv_post*Cpi*CD, Wc) ; 
Kp=1/magc


%open loop
Gtvol=minreal(Kp*Cpi*Gtv_post)

figure(1)
margin(Gtvol)
%closed loop
Gtvcl=minreal(Gtvol/(1+Gtvol*CD))
figure(2)
margin(Gtvcl)
figure(3)
step(Gtvcl)
stepinfo(Gtvcl)




% figure(1)
% bode(Gtv_post*Cpi*CD)
% figure(2)
% bode(0.1*tf([3.3],[1,5,2.1,1]))

% [Num_test,Den_test] = tfdata(Gtv_post*Cpi*CD,'v');
% syms s
% sys_syms=poly2sym(Num_test,s)/poly2sym(Den_test,s);
% ess = limit(1/(1+sys_syms),s,0)

%% Simulink model name
model='regbot__with_tilt_mg';

%% Velocity controller
% Estimate transfer function for base system using LINEARIZE
% Motor volatge to wheel velocity (wv)
load_system(model);
open_system(model);
% define points in model
ios2(1) = linio(strcat(model,'/tilt_ref1'),1,'openinput');
ios2(2) = linio(strcat(model, '/wheel_vel_filter'),1,'openoutput');
% attach to model
setlinio(model,ios2);
% Use the snapshot time(s) 0 seconds
op2 = [0];
% Linearize the model
sys2 = linearize(model,ios2,op2);
% get transfer function
[num2,den2] = ss2tf(sys2.A, sys2.B, sys2.C, sys2.D);
GVC = minreal(tf(num2, den2))
figure(1)
margin(GVC)
figure(2)
nyquist(GVC)
%% Filter
[~,Wfilter_peak]=getPeakGain(GVC,0.01,[10,100])
   
[MagPeak, PhasePeak]=bode(GVC,0)
GainPeak=db2mag(MagPeak)
%10
Wfilter_peak=10;
Tau_filter=1/Wfilter_peak

Vel_filter=minreal((tf([1],[Tau_filter,1]))^1)


GVC_filt=minreal(Vel_filter*GVC)
figure(1)
hold on
bode(GVC)
bode(GVC_filt)
hold off
%margin(GVC_filt)
[Num_filt,Den_filt]=tfdata(Vel_filter,'v')
% figure(2)
% nyquist(GVC_filt)
%% Vel controller
%design af PID 
w_vel = logspace ( - 2 , 3 , 5000) ;  %frequency from 10ˆ -2 t i l 10ˆ2 rad/...
[mag_vel,phase_vel ]=bode (GVC_filt ,w_vel) ;
%Vi vælger alpha og Ni til nogle værider og en ønsket phase margin
%alpha= 0.5
alpha_vel=0.5;
%Ni=3
Ni_vel=3;
%Ønsket phase margin
%Ym = 80
Ym_vel=80;
%Udregning af phaser for Pi og lead
Phi_i_vel=-atand(1/Ni_vel)

Phi_d_vel=asind((1-alpha_vel)/(1+alpha_vel))

%phase for Gtv_post findes en ny Wc
Phi_G_vel=360+Ym_vel-Phi_i_vel-180-Phi_d_vel

n_vel = find ( phase_vel > Phi_G_vel , 1 , 'last') ; 
Wc_vel=w_vel(n_vel)
%Wc_vel=20
%Tidskonstanter for I og D led
Tau_i_vel=Ni_vel/Wc_vel 
Tau_d_vel=1/(Wc_vel*sqrt(alpha_vel))
%Overføringsfunktion for Pi og Lead
Cpi_vel=tf([Tau_i_vel,1],[Tau_i_vel,0])
[Num_inte_vel,Den_inte_vel]=tfdata(Cpi_vel,'v')
CD_vel=tf([Tau_d_vel,1],[alpha_vel*Tau_d_vel,1])
[Num_Lead_vel,Den_Lead_vel]=tfdata(CD_vel,'v')
%Finder gain for Kp ud fra den nye Wc 
[magc_vel , phasec_vel] = bode (GVC*Vel_filter*Cpi_vel*CD_vel, Wc_vel) ; 
Kp_vel=1/magc_vel

%open loop
GVCol_vel=minreal(Kp_vel*Cpi_vel*GVC*Vel_filter)
pole(GVCol_vel)
zero(GVCol_vel)
figure(1)
margin(GVCol_vel)
%closed loop
GVCcl_vel=minreal(GVCol_vel/(1+GVCol_vel*CD_vel))
figure(2)
margin(GVCcl_vel)

figure(3)
step(GVCcl_vel)

%% Simulink model name
model='regbot_1mg';

%% Pos controller
% Estimate transfer function for base system using LINEARIZE
% Motor volatge to wheel velocity (wv)
load_system(model);
open_system(model);
% define points in model
ios3(1) = linio(strcat(model,'/Vref'),1,'openinput');
ios3(2) = linio(strcat(model, '/robot with balance'),3,'openoutput');
% attach to model
setlinio(model,ios3);
% Use the snapshot time(s) 0 seconds
op3 = [0];
% Linearize the model
sys3 = linearize(model,ios3,op3);
% get transfer function
[num3,den3] = ss2tf(sys3.A, sys3.B, sys3.C, sys3.D);
Gpos = minreal(tf(num3, den3))
figure(1)
margin(Gpos)
figure(2)
nyquist(Gpos)

%% Pos controller
%design af PID 
w_pos = logspace ( - 2 , 3 , 5000) ;  %frequency from 10ˆ -2 t i l 10ˆ2 rad/...
[mag_pos,phase_pos ]=bode (Gpos ,w_pos) ;
%Vi vælger alpha og Ni til nogle værider og en ønsket phase margin
%alpha= 0.5
alpha_pos=0.04;
%Ni=3
Ni_pos=0;
%Ønsket phase margin
%Ym = 80
Ym_pos=80;
%Udregning af phaser for Pi og lead
%Phi_i_pos=-atand(1/Ni_pos)

Phi_d_pos=asind((1-alpha_pos)/(1+alpha_pos))

%phase for Gtv_post findes en ny Wc
Phi_G_pos=360+Ym_pos-180-Phi_d_pos

n_pos = find ( phase_pos > Phi_G_pos , 1 , 'last') ; 
Wc_pos=w_pos(n_pos)
%Wc_vel=20
%Tidskonstanter for I og D led
%Tau_i_pos=Ni_pos/Wc_pos 
Tau_d_pos=1/(Wc_pos*sqrt(alpha_pos))
%Overføringsfunktion for Pi og Lead
% Cpi_pos=tf([Tau_i_pos,1],[Tau_i_pos,0])
% [Num_inte_pos,Den_inte_pos]=tfdata(Cpi_pos,'v')
 CD_pos=tf([Tau_d_pos,1],[alpha_pos*Tau_d_pos,1])
 [Num_Lead_pos,Den_Lead_pos]=tfdata(CD_pos,'v')
%Finder gain for Kp ud fra den nye Wc  *CD_pos
[magc_pos , phasec_pos] = bode (Gpos*CD_pos, Wc_pos) ; 
Kp_pos=1/magc_pos

%open loop
Gpos_ol=minreal(Kp_pos*Gpos*CD_pos)
% pole(Gpos_ol)
% zero(Gpos_ol)
figure(1)
margin(Gpos_ol)
%closed loop
Gpos_CL=minreal(Gpos_ol/(1+Gpos_ol))
figure(2)
margin(Gpos_CL)

figure(3)
step(Gpos_CL)