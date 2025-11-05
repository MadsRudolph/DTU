% ========================================================================
% File: coordinate_conversion_tool.m
%
% Purpose:
%   Unified coordinate conversion helper for Electromagnetics.
%   Converts:
%     - A point (position) between Cartesian, Cylindrical, and Spherical systems
%     - A vector (field) between bases at that point
%
%   Includes detailed comments to help you learn the math behind it.
%
% Author: Mads Rudolph
% Updated: 2025-11-05
%
% ========================================================================

function result = coordinate_conversion_tool(P, A, mode)
% ------------------------------------------------------------------------
% INPUTS:
%   P    = [x, y, z]  point in Cartesian coordinates (meters)
%   A    = [Ax, Ay, Az]  vector in Cartesian components (V/m, A/m, etc.)
%   mode = string specifying conversion type:
%       'cart2cyl'  → Cartesian → Cylindrical
%       'cart2sph'  → Cartesian → Spherical
%
% OUTPUT:
%   result = structure containing all converted coordinates and components
% ------------------------------------------------------------------------

arguments
  P (1,3) double
  A (1,3) double
  mode (1,:) char {mustBeMember(mode,{'cart2cyl','cart2sph'})}
end

% Extract Cartesian components
x = P(1); y = P(2); z = P(3);
Ax = A(1); Ay = A(2); Az = A(3);

switch mode
% ========================================================================
% === Cartesian → Cylindrical ============================================
% ========================================================================
case 'cart2cyl'
    % --- POINT CONVERSION ---
    % Cylindrical coordinates are (r, φ, z):
    %   r = radial distance from z-axis
    %   φ = azimuth angle in xy-plane (from x-axis, counterclockwise)
    %   z = same as Cartesian z
    r   = hypot(x, y);          % r = sqrt(x^2 + y^2)
    phi = atan2(y, x);          % atan2 ensures correct quadrant for φ
    phi_deg = rad2deg(phi);     % convert to degrees for readability

    % --- VECTOR CONVERSION ---
    % Cylindrical basis vectors rotate with φ:
    %   r̂  = cosφ x̂ + sinφ ŷ
    %   φ̂  = -sinφ x̂ + cosφ ŷ
    %   ẑ  = ẑ
    % So to get cylindrical components:
    c = cos(phi); s = sin(phi);
    Ar   =  Ax*c + Ay*s;        % radial component (outward from z-axis)
    Aphi = -Ax*s + Ay*c;        % tangential (azimuthal) component
    % z-component remains the same:
    Az   =  Az;

    % --- Pack results into structure ---
    result.system = 'Cylindrical';
    result.coords = [r, phi, z];
    result.phi_deg = phi_deg;
    result.vector = [Ar, Aphi, Az];
    result.labels = {'A_r', 'A_phi', 'A_z'};

% ========================================================================
% === Cartesian → Spherical =============================================
% ========================================================================
case 'cart2sph'
    % --- POINT CONVERSION ---
    % Spherical coordinates are (R, θ, φ):
    %   R = distance from origin
    %   θ = angle from z-axis (zenith angle)
    %   φ = azimuth in xy-plane (same as cylindrical)
    R = sqrt(x^2 + y^2 + z^2);
    theta = acos(z / R);
    phi = atan2(y, x);
    theta_deg = rad2deg(theta);
    phi_deg = rad2deg(phi);

    % --- VECTOR CONVERSION ---
    % Spherical basis:
    %   R̂ = sinθ cosφ x̂ + sinθ sinφ ŷ + cosθ ẑ
    %   θ̂ = cosθ cosφ x̂ + cosθ sinφ ŷ - sinθ ẑ
    %   φ̂ = -sinφ x̂ + cosφ ŷ
    % In matrix form: [A_R; A_θ; A_φ] = M * [A_x; A_y; A_z]
    A_R     =  Ax*sin(theta)*cos(phi) + Ay*sin(theta)*sin(phi) + Az*cos(theta);
    A_theta =  Ax*cos(theta)*cos(phi) + Ay*cos(theta)*sin(phi) - Az*sin(theta);
    A_phi   = -Ax*sin(phi) + Ay*cos(phi);

    % --- Pack results ---
    result.system = 'Spherical';
    result.coords = [R, theta, phi];
    result.degrees = [R, theta_deg, phi_deg];
    result.vector = [A_R, A_theta, A_phi];
    result.labels = {'A_R', 'A_theta', 'A_phi'};
end

% ========================================================================
% === Display Results (nicely formatted) ================================
% ========================================================================
fprintf('\n--- %s Conversion ---\n', result.system);
if strcmp(result.system,'Cylindrical')
    fprintf('Point (r, φ, z) = (%.3f, %.3f° , %.3f)\n', r, phi_deg, z);
    fprintf('A = %.3f r̂  %+ .3f φ̂  %+ .3f ẑ\n', Ar, Aphi, Az);
elseif strcmp(result.system,'Spherical')
    fprintf('Point (R, θ, φ) = (%.3f, %.3f° , %.3f°)\n', R, theta_deg, phi_deg);
    fprintf('A = %.3f R̂  %+ .3f θ̂  %+ .3f φ̂\n', A_R, A_theta, A_phi);
end
fprintf('------------------------------------------------------\n');

end

% ========================================================================
% Example test block (uncomment to run directly):
% ========================================================================

% Example 1 — Cartesian → Cylindrical
P = [3 -1 2];
A = [5 -4 -1];
result_cyl = coordinate_conversion_tool(P,A,'cart2cyl');
%{
% Example 2 — Cartesian → Spherical
P = [3 -1 2];
A = [5 -4 -1];
result_sph = coordinate_conversion_tool(P,A,'cart2sph');
%}

