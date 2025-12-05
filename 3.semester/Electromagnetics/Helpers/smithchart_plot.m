function smithchart_plot(varargin)
% SMITHCHART_PLOT - Plot points on a Smith Chart
%
% =========================================================================
% USAGE:
% =========================================================================
%
%   smithchart_plot(Z0, ZL)              % Plot load impedance
%   smithchart_plot(Z0, ZL, 'label')     % With custom label
%   smithchart_plot('Gamma', Gamma)      % Plot reflection coefficient directly
%   smithchart_plot('Gamma', Gamma, 'label')
%
% =========================================================================
% EXAMPLES:
% =========================================================================
%
%   % Plot a load on 75 Ohm line
%   smithchart_plot(75, 15 - 1j*37.5)
%
%   % Plot multiple points
%   smithchart_plot(50, 100)
%   hold on
%   smithchart_plot(50, 25 - 1j*25, 'Z_L')
%
%   % Plot Gamma directly
%   smithchart_plot('Gamma', 0.5*exp(1j*pi/4))
%
% =========================================================================

    if nargin == 0
        % Demo mode - show example
        demo_smith_chart();
        return;
    end

    % Parse inputs
    if ischar(varargin{1}) || isstring(varargin{1})
        mode = lower(string(varargin{1}));
        if mode == "gamma"
            Gamma = varargin{2};
            if nargin >= 3
                label = varargin{3};
            else
                label = '';
            end
            
            % Calculate normalized impedance from Gamma
            zL = (1 + Gamma) / (1 - Gamma);
            
            % Print info
            fprintf('\n=== Smith Chart Point (from Gamma) ===\n');
            fprintf('  Gamma = %.4f %+.4fj\n', real(Gamma), imag(Gamma));
            fprintf('  |Gamma| = %.4f, angle = %.2f deg\n', abs(Gamma), rad2deg(angle(Gamma)));
            fprintf('  zL (normalized) = %.4f %+.4fj\n', real(zL), imag(zL));
            fprintf('======================================\n\n');
            
            plot_on_smith(Gamma, label, zL);
        else
            error('Unknown mode. Use smithchart_plot(Z0, ZL) or smithchart_plot(''Gamma'', Gamma)');
        end
    else
        % Impedance mode: smithchart_plot(Z0, ZL, [label])
        Z0 = varargin{1};
        ZL = varargin{2};
        if nargin >= 3
            label = varargin{3};
        else
            label = '';
        end
        
        % Calculate normalized impedance and Gamma
        zL = ZL / Z0;
        Gamma = (zL - 1) / (zL + 1);
        
        % Print info
        fprintf('\n=== Smith Chart Point ===\n');
        fprintf('  Z0 = %.2f Ohm\n', Z0);
        fprintf('  ZL = %.4f %+.4fj Ohm\n', real(ZL), imag(ZL));
        fprintf('  zL (normalized) = %.4f %+.4fj\n', real(zL), imag(zL));
        fprintf('  Gamma = %.4f %+.4fj\n', real(Gamma), imag(Gamma));
        fprintf('  |Gamma| = %.4f, angle = %.2f deg\n', abs(Gamma), rad2deg(angle(Gamma)));
        fprintf('=========================\n\n');
        
        plot_on_smith(Gamma, label, zL);
    end
end

function plot_on_smith(Gamma, label, zL)
    if nargin < 3
        zL = (1 + Gamma) / (1 - Gamma);
    end
    
    % Check if smithplot exists (requires RF Toolbox)
    if exist('smithplot', 'file') || exist('smithplot', 'builtin')
        % Use MATLAB's built-in smithplot
        h = smithplot;
        hold on;
        
        % Plot the point - small red outline circle
        plot(real(Gamma), imag(Gamma), 'ro', 'MarkerSize', 8, 'LineWidth', 1.5);
        
        % Add label if provided
        if ~isempty(label)
            text(real(Gamma) + 0.05, imag(Gamma) + 0.05, label, 'FontSize', 12, 'FontWeight', 'bold');
        end
        
        % Add annotation with values
        title_str = sprintf('z_L = %.3f %+.3fj', real(zL), imag(zL));
        title(title_str, 'FontSize', 14);
        
    else
        % Fallback: draw our own Smith chart
        draw_smith_chart_manual();
        hold on;
        
        % Plot the point - small red outline circle
        plot(real(Gamma), imag(Gamma), 'ro', 'MarkerSize', 8, 'LineWidth', 1.5);
        
        % Add label
        if ~isempty(label)
            text(real(Gamma) + 0.05, imag(Gamma) + 0.05, label, 'FontSize', 12, 'FontWeight', 'bold');
        else
            text(real(Gamma) + 0.05, imag(Gamma) + 0.05, ...
                sprintf('z_L = %.2f%+.2fj', real(zL), imag(zL)), 'FontSize', 10);
        end
        
        title('Smith Chart', 'FontSize', 14);
    end
    
    hold off;
end

function draw_smith_chart_manual()
    % Draw a basic Smith chart without RF Toolbox
    figure('Color', 'white', 'Position', [100, 100, 600, 600]);
    axis equal;
    axis([-1.2, 1.2, -1.2, 1.2]);
    hold on;
    grid off;
    
    % Unit circle (|Gamma| = 1)
    theta = linspace(0, 2*pi, 200);
    plot(cos(theta), sin(theta), 'k-', 'LineWidth', 1.5);
    
    % Constant resistance circles
    r_values = [0, 0.2, 0.5, 1, 2, 5];
    for r = r_values
        % Center at (r/(r+1), 0), radius 1/(r+1)
        center_x = r / (r + 1);
        radius = 1 / (r + 1);
        
        % Only draw part inside unit circle
        theta = linspace(0, 2*pi, 200);
        x = center_x + radius * cos(theta);
        y = radius * sin(theta);
        
        % Clip to unit circle
        inside = (x.^2 + y.^2) <= 1.001;
        x(~inside) = NaN;
        y(~inside) = NaN;
        
        plot(x, y, 'b-', 'LineWidth', 0.5);
        
        % Label
        if r < 5
            text(center_x - radius + 0.02, 0.02, sprintf('%.1f', r), 'FontSize', 8, 'Color', 'b');
        end
    end
    
    % Constant reactance arcs
    x_values = [0.2, 0.5, 1, 2, 5];
    for x = x_values
        % Center at (1, 1/x), radius 1/x
        center_y = 1 / x;
        radius = 1 / x;
        
        % Upper half (positive reactance)
        theta = linspace(-pi, 0, 200);
        px = 1 + radius * cos(theta);
        py = center_y + radius * sin(theta);
        
        inside = (px.^2 + py.^2) <= 1.001;
        px(~inside) = NaN;
        py(~inside) = NaN;
        
        plot(px, py, 'r-', 'LineWidth', 0.5);
        
        % Lower half (negative reactance)
        py_neg = -center_y + radius * sin(-theta);
        inside = (px.^2 + py_neg.^2) <= 1.001;
        px_copy = px;
        px_copy(~inside) = NaN;
        py_neg(~inside) = NaN;
        
        plot(px_copy, py_neg, 'r-', 'LineWidth', 0.5);
    end
    
    % Real axis
    plot([-1, 1], [0, 0], 'k-', 'LineWidth', 0.5);
    
    % Labels
    xlabel('Real(\Gamma)', 'FontSize', 12);
    ylabel('Imag(\Gamma)', 'FontSize', 12);
    
    % Mark key points
    plot(-1, 0, 'ks', 'MarkerSize', 8, 'MarkerFaceColor', 'k');  % Short
    plot(1, 0, 'ks', 'MarkerSize', 8, 'MarkerFaceColor', 'k');   % Open
    plot(0, 0, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'g');   % Matched
    
    text(-1, -0.1, 'Short', 'FontSize', 8, 'HorizontalAlignment', 'center');
    text(1, -0.1, 'Open', 'FontSize', 8, 'HorizontalAlignment', 'center');
    text(0, -0.1, 'Matched', 'FontSize', 8, 'HorizontalAlignment', 'center');
end

function demo_smith_chart()
    fprintf('\nSmith Chart Demo\n');
    fprintf('================\n\n');
    
    % Example: Q10 from exam
    Z0 = 75;
    ZL = 15 - 1j*37.5;
    
    fprintf('Example: Z0 = %.0f Ohm, ZL = %.0f - j%.1f Ohm\n', Z0, real(ZL), abs(imag(ZL)));
    
    smithchart_plot(Z0, ZL, 'z_L');
end