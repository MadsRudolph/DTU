function gamma_M = overshoot2phase_margin(M_p)
% Returns phase margin in degrees given overshoot (not in percentage)
% M_p must be positive
    zeta = log(1/M_p)/sqrt(pi^2 + log(1/M_p)^2);
    gamma_M = rad2deg(atan(2*zeta/sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^4))));
end