clear all 
close all
clc

% define frequencies
F1=10;              % Frequency 1, [Hz]
F2=10.2;            % Frequency 2, [Hz]

% define time and frequency arrays accroding to FFT
Fs=1000;            % Sampling frequency
Ts=1/Fs;            % Sampling time
t=0:Ts:2-Ts;        % time vector, 2 seconds duration, [s]
N=length(t);        % Number of elements
DeltaF=Fs/N;            % Frequency resolution
f=(-N/2:N/2-1)*DeltaF;  % Frequency vector [Hz]

% Define signals in time
x1=cos(2*pi*F1*t);  %time domain signal1
x2=cos(2*pi*F2*t);  %time domain signal2

% Find frequency spectra
X1 = fftshift(fft(x1));  %FFT + order frequencies by using fftshift
X2 = fftshift(fft(x2));  %FFT + order frequencies by using fftshift

font_str = 15;

% plot signal 1, time and frequency
figure(1)
subplot(2,1,1); plot(t,x1,'-');hold on; % plot the signal
title(['x[n]=cos(2 \pi ' num2str(F1) ' t)']); xlabel('Time [s]'); ylabel('x[n]');
set(gca,'fontsize',font_str)
subplot(2,1,2); stem(f,abs(X1)/N); %x-axis represent frequencies
title('X[k]'); xlabel('Frequency [Hz]'); ylabel('|X(k)|');
set(gca,'fontsize',font_str)
xlim([-20 20])

% plot signal 2, time and frequency
figure(2)
subplot(2,1,1); plot(t,x2,'-r');hold on; % plot the signal
set(gca,'fontsize',font_str)
title(['x[n]=cos(2 \pi ' num2str(F2) ' t)']); xlabel('Time [s]'); ylabel('x[n]');
subplot(2,1,2); stem(f,abs(X2)/N,'r'); %x-axis represent frequencies
title('X[k]'); xlabel('Frequency [Hz]'); ylabel('|X(k)|');
set(gca,'fontsize',font_str)
xlim([-20 20])


%% Power of signals

% power of the frequnecy spectra (nearly preserved)
P1 = sum(abs(X1).^2);
P2 = sum(abs(X2).^2);

Error_rel = (P1-P2)/P1*100

%% Plot signals periodically

figure(3)
subplot(2,1,1); plot(t,x1,t+2,x1,t+4,x1);hold on; 
title(['x[n]=cos(2 \pi ' num2str(F1) ' t)']); xlabel('n'); ylabel('x[n]');
subplot(2,1,2); plot(t,x2,t+2,x2,t+4,x2); 
title(['x[n]=cos(2 \pi ' num2str(F2) ' t)']);  xlabel('n'); ylabel('x[n]');

