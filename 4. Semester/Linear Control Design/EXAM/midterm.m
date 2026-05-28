% clear all; clc; close all; s = tf('s');
% G = s + 0.5 / (s );  % ← CHANGE THIS
% 
% [num_c, den_c] = tfdata(G, 'v');
% p = pole(G); z = zero(G);
% fprintf('Poles: '); disp(p');
% fprintf('DC gain: %.4f\n', dcgain(G));
% if all(real(p)<0), fprintf('STABLE\n'); else, fprintf('UNSTABLE\n'); end
% 
% order = length(den_c)-1;
% if order == 2
%     wn = sqrt(den_c(3)/den_c(1));
%     zeta = den_c(2)/(2*wn*den_c(1));
%     Mp = exp(-pi*zeta/sqrt(1-zeta^2))*100;
%     fprintf('wn=%.4f, zeta=%.4f, Mp=%.2f%%\n', wn, zeta, Mp);
% end
% 
% info = stepinfo(G);
% fprintf('Rise=%.4fs, Settle=%.4fs, OS=%.2f%%\n', ...
%     info.RiseTime, info.SettlingTime, info.Overshoot);
% [Gm,Pm,Wcg,Wcp] = margin(G);
% fprintf('GM=%.2fdB, PM=%.2fdeg\n', 20*log10(Gm), Pm);
% 
% figure;
% subplot(2,2,1); step(G); grid on;
% subplot(2,2,2); impulse(G); grid on;
% subplot(2,2,[3 4]); margin(G);
s = tf('s');
G = 71 / (s^4 + 9*s^3 + 20*s^2);
pole(G)   % [0; 0; -4; -5]
zero(G)   % empty → no zeros

s = tf('s');
G = (s + 2.5) / (s^2 + 3*s + 4.5);
figure; bode(G); grid on;
figure; pzmap(G);