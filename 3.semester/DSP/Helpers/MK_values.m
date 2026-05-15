%Denne funktion returnere M og K værdier, baseret på N_taps

%Forfatter: Bjørn Bjarnason

function [M_values, K_values] = MK_values(N_taps)
    syms K M
    M_values = double(solve(N_taps == M + 1, M));
    K_values = double(solve(N_taps == 2*K + 1, K));
end