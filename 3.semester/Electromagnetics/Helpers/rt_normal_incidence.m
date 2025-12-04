function rt = rt_normal_incidence(eps_r1, eps_r2, mu_r1, mu_r2)
   % RT_NORMAL_INCIDENCE  Fresnel coefficients for normal incidence
   %
   %   rt = rt_normal_incidence(eps_r1, eps_r2)
   %   rt = rt_normal_incidence(eps_r1, eps_r2, mu_r1, mu_r2)
   %
   % Lossless, simple media. Returns Gamma, t, R, T and intrinsic impedances.

   if nargin < 3
       mu_r1 = 1;
   end
   if nargin < 4
       mu_r2 = 1;
   end

   eps0 = 8.854e-12;
   mu0  = 4*pi*1e-7;

   eps1 = eps0 * eps_r1;
   eps2 = eps0 * eps_r2;
   mu1  = mu0  * mu_r1;
   mu2  = mu0  * mu_r2;

   eta1 = sqrt(mu1/eps1);
   eta2 = sqrt(mu2/eps2);

   Gamma = (eta2 - eta1) / (eta2 + eta1);
   t     = 2*eta2 / (eta2 + eta1);

   % Power reflection / transmission (normal incidence, lossless)
   R = abs(Gamma)^2;
   T = 1 - R;

   rt.eps_r1 = eps_r1;
   rt.eps_r2 = eps_r2;
   rt.mu_r1  = mu_r1;
   rt.mu_r2  = mu_r2;
   rt.eta1   = eta1;
   rt.eta2   = eta2;
   rt.Gamma  = Gamma;
   rt.t      = t;
   rt.R      = R;
   rt.T      = T;
end