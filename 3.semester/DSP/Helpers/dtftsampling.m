function [ Xk,Xw ] = dtftsampling(x )
%The m.function dtftsampling calculates the DFT Xk and the DTFT Xw of an
%arbitrary signal x and displays the magnitudes and phases of Xk and X in 2
%subplots and hereby showing that the DFT of x is the DTFT sampled at
%frequencies 2*pi*k/N for k=0,1,...,N-1, where N is the length of x.
close all
N=length(x);
k=0:N-1;
Xk=fft(x,N);
magk=abs(Xk);
phasek=angle(Xk);
figure(1)
subplot(2,1,1), stem(k,magk,'filled');
hold on
subplot(2,1,2), stem(k,phasek,'filled');
hold on
disp('Strike any key when ready')
pause
[Xw,phasew]=freqz(x,1,512,'whole')
magw=abs(Xw)
phasew=angle(Xw);
w=linspace(0,N,512);
subplot(2,1,1), plot(w,magw,'r');
subplot(2,1,2), plot(w,phasew,'r');
hold off



