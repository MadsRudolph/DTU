%% REGBOT Position Controller — Plot Half K_P Results
%  Day 8 — K_P = 10.6 attempt
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% Load log
opts = detectImportOptions('log_position_half_kp.txt', 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable('log_position_half_kp.txt', opts);
data = fillmissing(data, 'nearest');

t    = table2array(data(:,1));
u_L  = table2array(data(:,8));
u_R  = table2array(data(:,9));
v_L  = table2array(data(:,10));
v_R  = table2array(data(:,11));
x    = table2array(data(:,14));
x    = x - x(1);

fprintf('Loaded %d samples, Ts = %.1f ms\n', length(t), (t(2)-t(1))*1000);

%% Plot
figure(1); clf;
aa = subplot(3,1,1);
plot(t, x);
hold on;
plot(t, 0.5*ones(size(t)), '--k');
hold off;
grid on;
ylabel('$x, x_{ref}$ in m');
legend({'$x$', '$x_{ref} = 0.5$ m'}, 'interpreter', 'latex');
title('REGBOT: $K_P = 10.6$, $N_I=3$, $\alpha=0.3$');

bb = subplot(3,1,2);
plot(t, u_L, t, u_R);
hold on;
yline(9, '--r'); yline(-9, '--r');
hold off;
grid on;
ylabel('Voltage [V]');
legend({'$u_L$', '$u_R$', '$\pm 9$ V'}, 'interpreter', 'latex');

cc = subplot(3,1,3);
plot(t, v_L, t, v_R);
grid on;
xlabel('$t$ in s');
ylabel('Velocity [m/s]');
legend({'$v_L$', '$v_R$'}, 'interpreter', 'latex');

linkaxes([aa, bb, cc], 'x');
saveas(gcf, [img_path 'day8_regbot_half_kp.png']);

%% Metrics
u_avg = (u_L + u_R) / 2;
idx_step = find(abs(u_avg) > 1, 1, 'first');
t_r = t(idx_step:end) - t(idx_step);
x_r = x(idx_step:end) - x(idx_step);
x_ref = 0.5;
x_final = x_r(end);

idx_10 = find(x_r >= 0.1*x_ref, 1);
idx_90 = find(x_r >= 0.9*x_ref, 1);
if ~isempty(idx_10) && ~isempty(idx_90)
    tr = t_r(idx_90) - t_r(idx_10);
else
    tr = NaN;
end

Mp = (max(x_r) - x_ref) / x_ref * 100;

settled = abs(x_r - x_ref) <= 0.02*x_ref;
ts = NaN;
for k = length(settled):-1:1
    if ~settled(k); ts = t_r(min(k+1, length(t_r))); break; end
end
if all(settled); ts = t_r(1); end

fprintf('\n=== REGBOT Half K_P Results ===\n');
fprintf('Final position: %.4f m\n', x_final);
fprintf('Steady-state error: %.4f m\n', abs(x_ref - x_final));
fprintf('Rise time (10-90%%): %.4f s\n', tr);
fprintf('Overshoot: %.2f %%\n', Mp);
fprintf('Settling time (2%%): %.4f s\n', ts);

%% All three attempts comparison
opts1 = detectImportOptions('log_position.txt', 'FileType', 'text');
opts1.CommentStyle = '%';
d1 = readtable('log_position.txt', opts1); d1 = fillmissing(d1,'nearest');
t1 = table2array(d1(:,1)); x1 = table2array(d1(:,14)); x1 = x1-x1(1);
ua1 = (table2array(d1(:,8))+table2array(d1(:,9)))/2;
is1 = find(abs(ua1)>1,1); t1r=t1(is1:end)-t1(is1); x1r=x1(is1:end)-x1(is1);

opts2 = detectImportOptions('log_position_conservative.txt', 'FileType', 'text');
opts2.CommentStyle = '%';
d2 = readtable('log_position_conservative.txt', opts2); d2 = fillmissing(d2,'nearest');
t2 = table2array(d2(:,1)); x2 = table2array(d2(:,14)); x2 = x2-x2(1);
ua2 = (table2array(d2(:,8))+table2array(d2(:,9)))/2;
is2 = find(abs(ua2)>1,1); t2r=t2(is2:end)-t2(is2); x2r=x2(is2:end)-x2(is2);

figure(2); clf;
plot(t_r, x_r, 'b', 'LineWidth', 2);
hold on;
plot(t2r, x2r, 'Color', [0.8 0.4 0], 'LineWidth', 1.5);
plot(t1r, x1r, 'r', 'LineWidth', 1);
plot([0 10], [0.5 0.5], '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Position [m]');
title('All REGBOT Attempts');
legend({'$K_P = 10.6$', '$K_P = 21.2$', '$K_P = 111.7$', 'Reference'}, ...
    'interpreter', 'latex', 'Location', 'southeast');
xlim([0 8]);
saveas(gcf, [img_path 'day8_regbot_all_attempts.png']);
