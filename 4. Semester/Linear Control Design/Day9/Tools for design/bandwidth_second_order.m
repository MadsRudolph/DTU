function omega_BW = bandwidth_second_order(omega_n,zeta)
% Returns the closed-loop bandwidth of a second order system given its
% natural frequency and its damping ratio
    omega_BW = omega_n*sqrt(-2*zeta^2 + 1 + sqrt(2 - 4*zeta + 4*zeta^4));
end