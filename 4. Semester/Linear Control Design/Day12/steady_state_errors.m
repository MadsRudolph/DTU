clear all;
clc;

s = tf('s');
K_1 = 4;
K_2 = 5;
tau_1 = 0.2;
tau_m = 0.001;

G_1 = K_1/(tau_1*s + 1);
G_2 = K_2/s;
H = 1/(tau_m*s + 1);

K_P = db2mag(-15.7);
bode(G_1*G_2*H,K_P*G_1*G_2*H);

[n_1,d_1] = tfdata(G_1,'v');
[n_2,d_2] = tfdata(G_2,'v');
[n_3,d_3] = tfdata(H,'v');

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);
R = 1;
d_time = 5;

%% No disturbances
D_1 = 0;
D_2 = 0;
D_3 = 0;
D_m = 0;

out = sim('disturbances_SS_Error');

figure(1);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$y(t),r(t)$');
legend({'$y(t)$' ,'$r(t)$'},'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data - out.y.Data);
grid on;
xlabel('$t$ in sec');
ylabel('$e(t)$');
linkaxes([aa,bb],'x');

%% Only d_1
D_1 = 1;
D_2 = 0;
D_3 = 0;
D_m = 0;

out = sim('disturbances_SS_Error');

figure(2);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
plot(out.d1.Time,out.d1.Data,'--r');
hold off;
grid on;
ylabel('$y(t),r(t),d_1(t)$');
legend({'$y(t)$' ,'$r(t)$', '$d_1(t)$'},'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data - out.y.Data);
grid on;
xlabel('$t$ in sec');
ylabel('$e(t)$');
linkaxes([aa,bb],'x');

%% Only d_2
D_1 = 0;
D_2 = 1;
D_3 = 0;
D_m = 0;

out = sim('disturbances_SS_Error');

figure(3);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
plot(out.d2.Time,out.d2.Data,'--r');
hold off;
grid on;
ylabel('$y(t),r(t),d_2(t)$');
legend({'$y(t)$' ,'$r(t)$', '$d_2(t)$'},'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data - out.y.Data);
grid on;
xlabel('$t$ in sec');
ylabel('$e(t)$');
linkaxes([aa,bb],'x');

%% Only d_3
D_1 = 0;
D_2 = 0;
D_3 = 1;
D_m = 0;

out = sim('disturbances_SS_Error');

figure(4);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
plot(out.d3.Time,out.d3.Data,'--r');
hold off;
grid on;
ylabel('$y(t),r(t),d_3(t)$');
legend({'$y(t)$' ,'$r(t)$', '$d_3(t)$'},'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data - out.y.Data);
grid on;
xlabel('$t$ in sec');
ylabel('$e(t)$');
linkaxes([aa,bb],'x');

%% Only d_m
D_1 = 0;
D_2 = 0;
D_3 = 0;
D_m = 1;

out = sim('disturbances_SS_Error');

figure(5);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
plot(out.dm.Time,out.dm.Data,'--r');
hold off;
grid on;
ylabel('$y(t),r(t),d_m(t)$');
legend({'$y(t)$' ,'$r(t)$', '$d_m(t)$'},'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data - out.y.Data);
grid on;
xlabel('$t$ in sec');
ylabel('$e(t)$');
linkaxes([aa,bb],'x');
