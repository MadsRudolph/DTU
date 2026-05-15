%Denne funktion laver en tids vektor udfra samplefrekvens og mængde n

%Forfattere: Bjørn Bjarnason, Tobias Nilson, Mathias Bay

function t_v = time_vec(F_s, N)
    T_s = 1/F_s;

    t_v = (0:(N-1))*T_s;
end