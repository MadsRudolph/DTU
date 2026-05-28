function omega_c = bandwidth2crossover_frequency(omega_BW,zeta)
% Returns open-loop crossover frequency given closed-loop bandwidth
% omega_BW must be positive
    omega_c = omega_BW*sqrt(-2*zeta^2 + sqrt(1 + 4*zeta^4))/...
              sqrt(-2*zeta^2 + 1 + sqrt(2 - 4*zeta + 4*zeta^4));
end