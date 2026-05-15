%Denne funktion giver vindue værdi udfra hvilket type vindue (bortset fra
%rektaguler.

%Forfatter: Bjørn Bjarnason

function w = FIR_window(type, M)
    n = 0:M;
    if type == "hanning" || type == "Hanning"
        w = 0.5-0.5*cos((2*pi*n)/M);
    elseif type == "hamming" || type == "Hamming"
        w = 0.54 - 0.46*cos((2*pi*n)/(M));
    elseif type == "blackman" || type == "Blackman"
        w = 0.42 - 0.5*cos((2*pi*n)/(M)) + 0.08*cos((4*pi*n)/(M));
    else
        error('Unsupported window type');
    end
end