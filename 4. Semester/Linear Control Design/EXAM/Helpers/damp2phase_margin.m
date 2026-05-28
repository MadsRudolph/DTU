function gamma_M = damp2phase_margin(zeta)
% Returns phase margin in degrees given damping ratio
%     gamma_M = rad2deg(atan(2*zeta/sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^4))));
    gamma_M = rad2deg(pi/2 - atan(sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^4))/(2*zeta)));
end