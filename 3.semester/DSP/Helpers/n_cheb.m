function n_cheb(A_sdB, A_pdB, nu)
    e = (10^(0.1*A_pdB))-1;

    n = (acosh(sqrt((10^(0.1*A_sdB))-1)/e))/(acosh(nu));

    fprintf("e = %f\nn = %f", ceil(e), ceil(n));
end