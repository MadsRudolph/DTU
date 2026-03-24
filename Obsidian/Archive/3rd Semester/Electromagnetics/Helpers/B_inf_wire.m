function B = B_inf_wire(I, r, mu_r)
   % B_INF_WIRE  B-field magnitude around an infinitely long wire
   %
   %   B = B_inf_wire(I, r)
   %   B = B_inf_wire(I, r, mu_r)
   %
   % I    : current [A]
   % r    : radial distance from wire [m]
   % mu_r : relative permeability (default 1)

   if nargin < 3
       mu_r = 1;
   end

   mu0 = 4*pi*1e-7;
   mu  = mu0 * mu_r;

   if any(r <= 0)
       error('Distance r must be positive.');
   end

   B = mu * I ./ (2*pi*r);
end