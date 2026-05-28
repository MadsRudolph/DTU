function [M_p, M_percentage] = damping2overshoot(zeta)
% Returns Overshoot M_p (not in percentage) for damping ratio 0 < zeta < 1
    if  ((zeta > 0)&&(zeta < 1))  
        M_p = exp(-pi*zeta/sqrt(1 - zeta^2));
    else
        disp('Zeta must be between zero and one');
        M_p = NaN;
    end
    if (zeta == 1)
        M_p = 0;
    end
    M_percentage = 100*M_p;
end