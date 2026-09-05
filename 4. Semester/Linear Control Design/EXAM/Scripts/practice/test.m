% Linearize  xdot = f(x,u)  about an operating point  ->  G(s) = dX/dU
syms w a s
f = (a*0.056*sqrt(300000-1600*w) - 0.12*w)/0.23;
A = double(subs(diff(f, w), [w a], [62.83 0.3]));
B = double(subs(diff(f, a), [w a], [62.83 0.3]));
G = B/(s - A);
disp('A ='), disp(A), disp('B ='), disp(B), pretty(G)
% Higher-order ODE? write it as xdot = f([x1;x2],u), then:
%   A = double(subs(jacobian(f,[x1 x2]), [x1 x2 u], [x10 x20 u0]));
%   B = double(subs(jacobian(f,u),        [x1 x2 u], [x10 x20 u0]));
%   G = tf(ss(A,B,[1 0],0));