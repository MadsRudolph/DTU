%==========================================================================
%
%   Technical University of Denmark
%
%   62743 Digital Signal Processing
%
%   Template for manually sketching spectra
%   The script can be adapted to become a function
%
%   Lars Søgaard Rishøj + Anders T. Clausen
%
%   2023
%
%==========================================================================

clear all
close all
clc

%==========================================================================
%
%   Plot to sketch spectrum of signal
%
%==========================================================================

%% Generate empty plot with no arrows

% USER-DEFINED AXIS INFORMATION
xmax = 20;                              % Set maximum for x-axis
xstep = 1;                              % Set steps for x-axis
ymax = 6;                               % Set maximum for y-axis
ystep = 0.5;                            % Set steps for y-axis

% Define vectors - do not change
xaxis = [-xmax:xstep:xmax];
yaxis = zeros(size(xaxis));
yindex = [0:ystep:ymax];

% Generate plot - do not change
figure(1)
plot(xaxis,yaxis,'w')                   % Plot graph with no content
set(gca,'FontSize',15,'Fontname', 'Arial','linewidth',2)
xlabel('Frequency (set unit in correct Hz)')
ylabel('Amplitude (A.U.)')
set(gca,'XTick',xaxis);
set(gca,'YTick',yindex);
pbaspect([3,1,1])
ylim([-0.5 ymax])
grid on
hold on

%% Generate arrows
% Copy arrow block for each addditional arrow needed in plot 

% Arrow block 1 - discrete spectral component 1
    x_pos = -10;                        % set x-axis position
    y_start = 0;                        % set y-axis start
    y_end = 3;                          % set y-axis end
    anArrow = annotation('arrow');
    anArrow.Parent = gca;
    anArrow.X = [x_pos,x_pos];
    anArrow.Y = [y_start ,y_end];
    anArrow.Color = 'red';              % set colour of arrow
    anArrow.LineWidth = 4;
    anArrow.HeadLength = 15;
    anArrow.HeadWidth = 15;
    anArrow.HeadStyle = 'plain';
    

% Arrow block 2 - discrete spectral component 2
    x_pos = 15;                        % set x-axis position
    y_start = 0;                        % set y-axis start
    y_end = 1.5;                        % set y-axis end
    anArrow = annotation('arrow');
    anArrow.Parent = gca;
    anArrow.X = [x_pos,x_pos];
    anArrow.Y = [y_start ,y_end];
    anArrow.Color = 'blue';             % set colour of arrow
    anArrow.LineWidth = 4;
    anArrow.HeadLength = 15;
    anArrow.HeadWidth = 15;
    anArrow.HeadStyle = 'plain';


