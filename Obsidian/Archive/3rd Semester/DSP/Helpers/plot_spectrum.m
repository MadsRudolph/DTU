function fig = plot_spectrum(frequencies, amplitudes, varargin)
%PLOT_SPECTRUM Plot frequency spectrum - MATCHES PYTHON VERSION
%
%   EXAM QUICK MODE:
%   >> plot_spectrum([1500 -1500 3800 -3800], [1.5 1.5 1 1])
%
%   With legend labels:
%   >> plot_spectrum(freqs, amps, 'LegendLabels', {'1500 Hz (OK)', '4200 → 3800 Hz (ALIASED!)'})

%% Quick input validation
frequencies = frequencies(:)';
amplitudes = amplitudes(:)';

if numel(frequencies) ~= numel(amplitudes)
    error('Frequencies and amplitudes must have the same length');
end

%% Parse inputs with EXAM-FRIENDLY defaults
p = inputParser;
addRequired(p, 'frequencies', @isnumeric);
addRequired(p, 'amplitudes',  @isnumeric);
addParameter(p, 'XRange',    [], @isnumeric);
addParameter(p, 'YMax',      [], @isnumeric);
addParameter(p, 'XStep',     [], @isnumeric);
addParameter(p, 'YStep',     0.5, @isnumeric);
addParameter(p, 'XLabel',    'Frequency (Hz)', @ischar);
addParameter(p, 'YLabel',    'Amplitude (A.U.)', @ischar);
addParameter(p, 'Colors',    'auto');  % 'auto', 'c', 'r', or cell array
addParameter(p, 'LineWidth', 3, @isnumeric);
addParameter(p, 'Title',     '', @ischar);
addParameter(p, 'FigNum',    [], @isnumeric);
addParameter(p, 'MaxXLabels', 11, @isnumeric);
addParameter(p, 'MaxYLabels', 8, @isnumeric);
addParameter(p, 'Fs',        [], @isnumeric);  % NEW: For auto title
addParameter(p, 'LegendLabels', {}, @iscell);  % NEW: Legend text

parse(p, frequencies, amplitudes, varargin{:});

freqs       = p.Results.frequencies(:);
amps        = p.Results.amplitudes(:);
xrange      = p.Results.XRange;
ymax        = p.Results.YMax;
xstep       = p.Results.XStep;
ystep       = p.Results.YStep;
xlabel_text = p.Results.XLabel;
ylabel_text = p.Results.YLabel;
colors_in   = p.Results.Colors;
linewidth   = p.Results.LineWidth;
title_text  = p.Results.Title;
fignum      = p.Results.FigNum;
maxXLabels  = p.Results.MaxXLabels;
maxYLabels  = p.Results.MaxYLabels;
Fs_val      = p.Results.Fs;
legend_labels = p.Results.LegendLabels;

%% Auto-generate title if Fs provided
if isempty(title_text) && ~isempty(Fs_val)
    title_text = sprintf('Sampled Spectrum (Fs = %.1f Hz, Nyquist = %.1f Hz)', ...
                         Fs_val, Fs_val/2);
end

%% Smart color handling - PYTHON STYLE
if ischar(colors_in) || isstring(colors_in)
    colors_in = char(colors_in);
    if strcmp(colors_in, 'auto')
        % Auto: Cyan for non-aliased, Red for aliased
        colors = cell(numel(freqs), 1);
        for i = 1:numel(freqs)
            if mod(i, 2) == 1
                colors{i} = [0 1 1];  % Cyan
            else
                colors{i} = [1 0 0];  % Red
            end
        end
    else
        % Single color for all
        colors = repmat({colors_in}, numel(freqs), 1);
    end
elseif iscell(colors_in)
    colors = colors_in;
    % Extend if needed
    if numel(colors) < numel(freqs)
        colors = repmat(colors, ceil(numel(freqs)/numel(colors)), 1);
        colors = colors(1:numel(freqs));
    end
else
    colors = repmat({'c'}, numel(freqs), 1);  % Default cyan
end

%% Convert color codes to RGB
for i = 1:numel(colors)
    if ischar(colors{i}) || isstring(colors{i})
        col = char(colors{i});
        switch col
            case 'c'
                colors{i} = [0 1 1];  % Cyan
            case 'r'
                colors{i} = [1 0 0];  % Red
            case 'b'
                colors{i} = [0 0 1];  % Blue
            case 'g'
                colors{i} = [0 1 0];  % Green
            case 'y'
                colors{i} = [1 1 0];  % Yellow
            case 'm'
                colors{i} = [1 0 1];  % Magenta
            case 'w'
                colors{i} = [1 1 1];  % White
        end
    end
end

%% Auto-calculate smart limits
if isempty(xrange)
    xmax = max(abs(freqs)) * 1.2;
    if xmax == 0, xmax = 10; end
    xrange = [-xmax, xmax];
end

if isempty(xstep)
    span  = xrange(2) - xrange(1);
    xstep = span / 10;
    if xstep >= 1000
        xstep = round(xstep, -3);
    elseif xstep >= 100
        xstep = round(xstep, -2);
    else
        xstep = round(xstep, 1, 'significant');
    end
end

if isempty(ymax)
    ymax = max(amps) * 1.2;
    if ymax == 0, ymax = 1; end
end

%% Figure setup - PYTHON DARK THEME
if isempty(fignum)
    fig = figure('Color', 'k');
else
    fig = figure(fignum);
    clf;
    set(fig, 'Color', 'k');
end

xaxis  = xrange(1):xstep:xrange(2);
yindex = 0:ystep:ymax;

plot(xaxis, zeros(size(xaxis)), 'Color', [0 0 0]);

ax = gca;
ax.Color        = 'k';
ax.GridColor    = [0.3 0.3 0.3];
ax.GridAlpha    = 0.6;
ax.XColor       = [0.9 0.9 0.9];
ax.YColor       = [0.9 0.9 0.9];
ax.LineWidth    = 1.5;
ax.FontSize     = 11;
ax.FontName     = 'Arial';
hold(ax, 'on');
grid(ax, 'on');

xlabel(xlabel_text, 'Color', [0.9 0.9 0.9], 'FontSize', 12);
ylabel(ylabel_text, 'Color', [0.9 0.9 0.9], 'FontSize', 12);

%% Set ticks
ax.XTick = xaxis;
ax.YTick = yindex;
pbaspect([3 1 1]);
ylim([-0.05, ymax]);

% Thin X labels
numX = numel(xaxis);
skipX = max(1, ceil(numX / maxXLabels));
xlab = repmat({''}, size(xaxis));
xlab(1:skipX:end) = arrayfun(@num2str, xaxis(1:skipX:end), 'UniformOutput', false);
ax.XTickLabel = xlab;

% Thin Y labels
numY = numel(yindex);
skipY = max(1, ceil(numY / maxYLabels));
ylab = repmat({''}, size(yindex));
ylab(1:skipY:end) = arrayfun(@num2str, yindex(1:skipY:end), 'UniformOutput', false);
ax.YTickLabel = ylab;

if ~isempty(title_text)
    title(title_text, 'Color', [0.9 0.9 0.9], 'FontSize', 13, 'FontWeight', 'bold');
end

%% Draw arrows
for i = 1:numel(freqs)
    col = colors{i};
    
    anArrow = annotation(fig, 'arrow');
    anArrow.Parent      = ax;
    anArrow.X           = [freqs(i) freqs(i)];
    anArrow.Y           = [0 amps(i)];
    anArrow.Color       = col;
    anArrow.LineWidth   = linewidth;
    anArrow.HeadLength  = 10;
    anArrow.HeadWidth   = 10;
    anArrow.HeadStyle   = 'plain';
end

%% Add legend text in top-left corner (PYTHON STYLE)
if ~isempty(legend_labels)
    y_start = ymax * 0.95;
    y_step = ymax * 0.08;
    x_pos = xrange(1) + (xrange(2) - xrange(1)) * 0.05;
    
    for i = 1:numel(legend_labels)
        text(x_pos, y_start - (i-1)*y_step, legend_labels{i}, ...
             'Color', [0.9 0.9 0.9], ...
             'FontSize', 10, ...
             'FontName', 'Courier New', ...
             'Interpreter', 'none', ...
             'VerticalAlignment', 'top');
    end
end

hold(ax, 'off');

end