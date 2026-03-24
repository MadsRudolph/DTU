function [r, a] = rect2pol(x)
% RECT2POL - Convert complex number to polar form (magnitude and angle)
%
% Usage:
%   [r, a] = rect2pol(x)
%
% Inputs:
%   x - Complex number (can be numeric or symbolic)
%
% Outputs:
%   r - Magnitude |x|
%   a - Angle in degrees
%
% Example:
%   [mag, ang] = rect2pol(3 + 4j)
%   % mag = 5, ang = 53.13

r_temp = abs(x);
a_temp = rad2deg(angle(x));

% Convert to numeric if symbolic
if isa(r_temp, 'sym')
    r = double(r_temp);
else
    r = r_temp;
end

if isa(a_temp, 'sym')
    a = double(a_temp);
else
    a = a_temp;
end

end