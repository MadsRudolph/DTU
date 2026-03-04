clear all;
clc;

data = readtable('datafile3.txt');  % Load data file
t = table2array(data(:,1)); % First column is time
u = table2array(data(:,2)); % Second column is input
y = table2array(data(:,3)); % Third column is output

T_s = t(2) - t(1);          % Calculate the Sampling time
idd = iddata(y,u,T_s);      % Put inputs and outputs to special structure
np = 3;                     % Select number of poles
nz = 1;                     % Select numbers of zeros

G = tfest(idd,np,nz);       % Identify the transfer function coefficients
figure(1);                   % Make a step response plot of G
aa = subplot(2,1,1);
plot(t,u);
grid on;
ylim([-1 2.54]);
ylabel('$u$');
bb = subplot(2,1,2);
plot(t,y);
grid on;
xlabel('$t$');
ylabel('$y$');
linkaxes([aa,bb],'x');
xlim([0 t(end)]);

figure(2);
compare(G,idd);              % Compare and plot real and simulated outputs
grid on;