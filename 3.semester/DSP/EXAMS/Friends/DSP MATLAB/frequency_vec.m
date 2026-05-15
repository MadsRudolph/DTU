%Denne funktion laver en frekvens vektor baseret på sample frekvens og
%mængde n

%Forfattere: Bjørn Bjarnason, Tobias Nilson, Mathias Bay

function f_v = frequency_vec(F_s, N)
    T_s = 1/F_s;

    f_v = -F_s/2:(1/(N*T_s)):F_s/2-(1/(N*T_s));
end