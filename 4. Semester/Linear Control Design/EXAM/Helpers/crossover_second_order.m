function omega_c = crossover_second_order(omega_n,zeta)
% Returns the crossover frequency of a second order system given its
% natural frequency and its damping ratio
    omega_c = omega_n*sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^4));
end