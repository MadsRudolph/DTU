%Denne funktion beregner epsilon og nu værdier udfra amplituderne, og
%baseret på n værdien, returnere prototype koeffiecienterne for det type
%filter der er spurgt om

%forfattere: Bjørn Bjarnason, Tobias Nilson, Mathias Bay

function [bd, ad] = n_value(A_sdB, A_pdB, nu, filter_type)
    
    if filter_type == "butter" || filter_type == "butterworth" || filter_type == "Butter" || filter_type == "Butterworth"
        e = (10^(0.1*A_pdB))-1;

        n = ceil((log10(((10^(0.1*A_sdB))-1)/e))/(2*log10(nu)));
           
        fprintf("e = %f\nn = %f", ceil(e), n);
        
        bd = 1;
        if n == 1
            ad = [1 1];

        elseif n == 2
            ad = [1 1.4142 1];

        elseif n == 3
            ad = [1 2 2 1];

        elseif n == 4
            ad = [1 2.6131 3.4142 2.6131 1];

        elseif n == 5
            ad = [1 3.2361 5.2361 5.2361 3.2361 1];

        elseif n == 6
            ad = [1 3.8637 7.4641 9.1416 7.4641 3.8637 1];

        else
            ad = [1 zeros(1, n-1) 1];
        end
    end

    if (filter_type == "cheb") || (filter_type == "chebyshev") || (filter_type == "Cheb") || (filter_type == "Chebyshev")
        e = (10^(0.1*A_pdB))-1;

        n = ceil((acosh(sqrt((10^(0.1*A_sdB))-1)/e))/(acosh(nu)));

        fprintf("e = %f\nn = %f", ceil(e), n);

        
        if n == 1
            bd = 1.0024;
            ad = [1 1.0024];

        elseif n == 2
            bd = 0.5012;
            ad = [1 0.6449 0.7079];

        elseif n == 3
            bd = 0.2506;
            ad = [1 0.5972 0.9283 0.2506];

        elseif n == 4
            bd = 0.1253;
            ad = [1 0.5816 0.9283 0.2506];

        elseif n == 5
            bd = 0.0626;
            ad = [1 0.5745 1.4150 0.5489 0.4080 0.0626];
            
        elseif n == 6
            bd = 0.0313;
            ad = [1 0.5707 1.6628 0.6906 0.6991 0.1634 0.0442];

        else
            bd = zeros(1);
            ad = zeros(1);
        end
    end
    
end