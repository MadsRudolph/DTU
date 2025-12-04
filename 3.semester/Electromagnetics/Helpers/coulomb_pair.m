function [F12, F21] = coulomb_pair(q1, q2, r1, r2)
   % COULOMB_PAIR  Coulomb force between two point charges (vector form)
   %
   %   [F12, F21] = coulomb_pair(q1, q2, r1, r2)
   %
   % q1, q2 : charges [C]
   % r1, r2 : position vectors [x; y; z] in meters

   eps0 = 8.854e-12;
   k_e  = 1/(4*pi*eps0);

   R12 = r1 - r2;
   R21 = -R12;

   d12 = norm(R12);
   if d12 == 0
       error('Charges must not coincide.');
   end

   u12 = R12/d12;
   u21 = -u12;

   Fmag = k_e * q1*q2 / (d12^2);

   F12 = Fmag * u12;   % Force on q1 due to q2
   F21 = Fmag * u21;   % Force on q2 due to q1
end