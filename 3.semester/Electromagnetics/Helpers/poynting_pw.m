function pw = poynting_pw(E0, eta, A, phi)
   % POYNTING_PW  Time-average Poynting vector and power (plane wave)
   %
   %   pw = poynting_pw(E0, eta, A, phi)
   %
   % E0  : magnitude of electric field [V/m]
   % eta : intrinsic impedance (complex allowed) [ohm]
   % A   : area [m^2]
   % phi : angle between S and surface normal [rad]

   S_mag = (abs(E0)^2) / (2*abs(eta));  % W/m^2
   P_inc = S_mag * A * cos(phi);        % W

   pw.E0        = E0;
   pw.eta       = eta;
   pw.A         = A;
   pw.phi       = phi;
   pw.S_mag     = S_mag;
   pw.P_incident= P_inc;
end