clear all;
clc;

s = tf('s');    % Define complex variable
% Define the transfer functions
% G = (s + 2.5)/((s^2 + 1)*(s - 2.7)*(s - 2.51 - 1.5*1i)*(s - 2.51 + 1.5*1i)); % Try to play with the poles and zeros
G = (s - 1)*(s - 2.1 - 1.5*1i)*(s - 2.1 + 1.5*1i)/((s^2 + 1)*(s - 2));
G = (s - 2.5)/((s - 2.1 - 1.5*1i)*(s - 2.1 + 1.5*1i)*(s^2 + 1)*(s - 2.745));

%% Nyquist plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

t = flip(0:0.0001:10);  % Define implicit parameter for complex curves
s_real = cos(0.2*pi*t); % Real part of C_1 curve                                
s_imag = sin(0.2*pi*t); % Imaginary part of C_1 curve
s = (2 + sin(0.1*pi*t)) + s_real + 1i*(s_imag + (1.7 + sin(0.2*pi*t))); % Define C_1 curve
GG = squeeze(freqresp(G,s)); % Caclulate the frequency response of G over C_1
p = pole(G);            % Find the poles of G
z = zero(G);            % Find the zeros of G

f2 = figure('WindowStyle','normal');
aa = subplot(1,2,1);
% Plot C_1, the poles and zeros of G (if they exist)
plot(real(s),imag(s));
hold on;
if (~isempty(z))
    scatter(real(z),imag(z),54,'o','MarkerEdgeColor','b');
end
scatter(real(p),imag(p),154,'x','MarkerEdgeColor','k');
% Define gradient vectors to show direction of C_1
dsx = gradient(real(s));
dsy = gradient(imag(s));
i_q = 1:ceil(length(s)/7):length(s);
% Plot direction arrows
quiver(real(s(i_q)),imag(s(i_q)),dsx(i_q),dsy(i_q),'Autoscalefactor',0.5);
hold off;
grid on;
xlabel('$\Re(s)$');
ylabel('$\Im(s)$');
title('$s$-plane');

bb = subplot(1,2,2);
plot(real(GG),imag(GG));    % Plot C_2
hold on;
% Define gradient vectors to show direction of C_1
dx = gradient(real(GG));
dy = gradient(imag(GG));
i_q = 1:ceil(length(GG)/7):length(GG);
% Plot direction arrows
quiver(real(GG(i_q)),imag(GG(i_q)),dx(i_q),dy(i_q),'Autoscalefactor',0.75);
% Alternative arrows
% scatter(real(GG(i_q)),imag(GG(i_q)),54,'>','markerFaceColor','b','MarkerEdgeColor','b');
scatter(0,0,54,'markerFaceColor','r','MarkerEdgeColor','g');
hold off;
grid on;
xlabel('$\Re(G(s))$');
ylabel('$\Im(G(s))$');
title('$w$-plane');
zoomArea = [-0.04 0.07 -0.04 0.054];
insetPositio = [0.1 0.4 0.05 0.21];
MagInset(f2,bb,zoomArea,insetPositio,{'NW','NW';'SE','SE'});

