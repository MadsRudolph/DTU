%Denne funktion beregner impulsresponsen udfra hvilken type filter er
%spurgt om med fourier transformation metoden.

%Forfatter: Bjørn Bjarnson

function h = FIR_fourier(type, n, omega_H, omega_L)
    if nargin < 4
        omega_L = 0; % Default value for low cutoff frequency
    end
        if type == "LP"
            h = (omega_H/pi)*sinc((n*omega_H)/pi);
            h((length(h)+1)/2) = omega_H/pi;
        elseif type == "HP"
            h = -(omega_H/pi)*sinc((n*omega_H)/pi);
            h((length(h)+1)/2) = (pi-omega_H)/pi;
        elseif type == "BP"
            h = (omega_H/pi)*sinc(n*omega_H/pi)-(omega_L/pi)*sinc(n*omega_L/pi);
            h((length(h)+1)/2) = (omega_H-omega_L)/pi;
        elseif type == "BS"
            h = -(omega_H/pi)*sinc(n*omega_H/pi) + (omega_L/pi)*sinc(n*omega_L/pi);
            h((length(h)+1)/2) = (pi-omega_H+omega_L)/pi;
        else
            h = 0;
        end
end