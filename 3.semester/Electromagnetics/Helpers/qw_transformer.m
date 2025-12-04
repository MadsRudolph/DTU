function qw = qw_transformer(R1, RL, freq, vp)
   % QW_TRANSFORMER  Quarter-wave transformer helper (real load)
   %
   %   qw = qw_transformer(R1, RL, freq, vp)
   %
   % Computes the required R_qw and λ/4 length, and checks the match.

   if ~isreal(R1) || ~isreal(RL)
       error('R1 and RL must be real (resistive).');
   end

   omega = 2*pi*freq;
   beta  = omega/vp;
   lambda= 2*pi/beta;

   R_qw  = sqrt(R1*RL);
   len_qw= lambda/4;

   % Check using standard λ/4 input impedance formula
   Z_in_check = R_qw^2 / RL;

   qw.R1         = R1;
   qw.RL         = RL;
   qw.freq       = freq;
   qw.vp         = vp;
   qw.lambda     = lambda;
   qw.len_qw     = len_qw;
   qw.R_qw       = R_qw;
   qw.Z_in_check = Z_in_check;
end