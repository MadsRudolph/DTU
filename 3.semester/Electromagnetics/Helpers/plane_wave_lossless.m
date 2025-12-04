function pw = plane_wave_lossless(epsilon_r, freq, mu_r)
   % PLANE_WAVE_LOSSLESS  Basic parameters for a lossless plane wave
   %
   %   pw = plane_wave_lossless(epsilon_r, freq)
   %   pw = plane_wave_lossless(epsilon_r, freq, mu_r)
   %
   % Returns a struct with beta, wavelength, phase velocity and eta.

   if nargin < 3
       mu_r = 1;
   end

   eps0 = 8.854e-12;
   mu0  = 4*pi*1e-7;
   c0   = 1/sqrt(eps0*mu0);

   eps = eps0 * epsilon_r;
   mu  = mu0 * mu_r;

   omega = 2*pi*freq;
   beta  = omega * sqrt(mu*eps);      % rad/m
   lambda= 2*pi / beta;               % m
   up    = omega / beta;              % m/s
   eta   = sqrt(mu/eps);              % ohms
   n     = c0 / up;                   % refractive index
   k0    = omega/c0;                  % free-space wavenumber

   pw.epsilon_r      = epsilon_r;
   pw.mu_r           = mu_r;
   pw.freq           = freq;
   pw.beta           = beta;
   pw.wavelength     = lambda;
   pw.phase_velocity = up;
   pw.eta            = eta;
   pw.n              = n;
   pw.k0             = k0;

   % --- Display Results ---
   fprintf('\n========================================\n');
   fprintf('  Lossless Plane Wave @ %.2e Hz\n', freq);
   fprintf('========================================\n');
   fprintf('Properties:\n');
   fprintf('  ε_r = %.2f\n', epsilon_r);
   fprintf('  μ_r = %.2f\n', mu_r);
   fprintf('\nWave Parameters:\n');
   fprintf('  β (phase const)  = %.3e rad/m\n', beta);
   fprintf('  λ (wavelength)   = %.3e m\n', lambda);
   fprintf('  u_p (velocity)   = %.3e m/s\n', up);
   fprintf('  η (impedance)    = %.2f Ω\n', eta);
   fprintf('  n (refr. index)  = %.4f\n', n);
   fprintf('  k_0 (free space) = %.3e rad/m\n', k0);
   fprintf('========================================\n\n');
end