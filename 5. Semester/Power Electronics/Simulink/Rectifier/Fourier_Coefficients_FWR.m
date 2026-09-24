
% The parameters of the FWR
clear
T=1/2/50;
N=23;
t=0:0.0001:0.1;
Vm=23.8;

% Fourier Series

a0=2*Vm/pi;
f=a0;

for i=1:1:N
    an(i)=4*Vm/pi*(1/(1-4*i*i));
    %plot(t,f)
    F=an(i)*cos(2*i*pi/T*t);
hold on
plot(t,F)
    f=f+an(i)*cos(2*i*pi/T*t);
end

plot(t,f)

% Fourier coefficients



V_rms_2=a0^2;
 
 for i=1:1:N
    V_rms_2=V_rms_2+1/2*an(i)^2;
 end
 
 V_rms=sqrt(V_rms_2);
double(V_rms)