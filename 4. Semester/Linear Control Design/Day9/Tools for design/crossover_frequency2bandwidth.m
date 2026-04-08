function omega_BW = crossover_frequency2bandwidth(omega_c,zeta)
% Returns open-loop crossover frequency given closed-loop bandwidth
% omega_c must be positive
    omega_BW = omega_c*sqrt(-2*zeta^2 + 1 + sqrt(2 - 4*zeta + 4*zeta^2))/...
              sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^2));
end