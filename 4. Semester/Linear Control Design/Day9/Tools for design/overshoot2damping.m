function zeta = overshoot2damping(M_p)
% Returns damping ratio 0 < zeta < 1 for Overshoot M_p (not in percentage)
    zeta = log(1/M_p)/sqrt(pi^2 + log(1/M_p)^2);
end