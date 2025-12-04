function tl = tl_section(Z0, ZL, freq, len, vp, alpha)
   % TL_SECTION  Single uniform TL section helper
   %
   %   tl = tl_section(Z0, ZL, freq, len, vp)
   %   tl = tl_section(Z0, ZL, freq, len, vp, alpha)
   %
   % Computes Gamma_L, Gamma_in, Z_in, VSWR and Vmax/Vmin positions
   % (for the lossless case).

   if nargin < 6
       alpha = 0;   % lossless default
   end

   omega = 2*pi*freq;
   beta  = omega/vp;
   gamma = alpha + 1j*beta;
   lambda= 2*pi/beta;

   % Reflection coefficient at load
   Gamma_L = (ZL - Z0) / (ZL + Z0);

   % Input reflection coefficient at z = -len
   Gamma_in = Gamma_L * exp(-2*gamma*len);

   % Input impedance (general lossy formula)
   Z_in = Z0 * (ZL + Z0 * tanh(gamma*len)) ./ ...
              (Z0 + ZL * tanh(gamma*len));

   % VSWR (if |Γ_L| < 1)
   magGL = abs(Gamma_L);
   if magGL < 1
       VSWR = (1 + magGL)/(1 - magGL);
   else
       VSWR = Inf;
   end

   % Vmax/Vmin positions (only meaningful if alpha ~ 0)
   if alpha == 0 && magGL ~= 0
       % Distance from load to first Vmax / Vmin
       phiL   = angle(Gamma_L);
       z_vmax = ( -phiL )/(2*beta);
       z_vmin = ( pi - phiL )/(2*beta);

       % Normalize to 0..lambda
       z_vmax = mod(z_vmax, lambda);
       z_vmin = mod(z_vmin, lambda);
   else
       z_vmax = NaN;
       z_vmin = NaN;
   end

   tl.Z0      = Z0;
   tl.ZL      = ZL;
   tl.freq    = freq;
   tl.len     = len;
   tl.vp      = vp;
   tl.alpha   = alpha;
   tl.beta    = beta;
   tl.lambda  = lambda;
   tl.gamma   = gamma;

   tl.Gamma_L = Gamma_L;
   tl.Gamma_in= Gamma_in;
   tl.Z_in    = Z_in;
   tl.VSWR    = VSWR;
   tl.z_vmax  = z_vmax;
   tl.z_vmin  = z_vmin;
end