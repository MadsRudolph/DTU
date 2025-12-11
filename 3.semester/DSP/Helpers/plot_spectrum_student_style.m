function fig = plot_spectrum(frequencies, amplitudes, varargin)
% frequency spectrum plotter
% made for exam - shows frequency components with colored arrows
% call like: plot_spectrum([1500 -1500], [1.5 1.5])

% reshape to row vectors
frequencies = frequencies(:)';
amplitudes = amplitudes(:)';

% check sizes match
if length(frequencies) ~= length(amplitudes)
    error('frequencies and amplitudes must have same length');
end

% setup parser
p = inputParser;
addRequired(p, 'frequencies');
addRequired(p, 'amplitudes');
addParameter(p, 'XRange', []);
addParameter(p, 'YMax', []);
addParameter(p, 'XStep', []);
addParameter(p, 'YStep', 0.5);
addParameter(p, 'XLabel', 'Frequency (Hz)');
addParameter(p, 'YLabel', 'Amplitude (A.U.)');
addParameter(p, 'Colors', 'auto');
addParameter(p, 'LineWidth', 3);
addParameter(p, 'Title', '');
addParameter(p, 'FigNum', []);
addParameter(p, 'MaxXLabels', 11);
addParameter(p, 'MaxYLabels', 8);
addParameter(p, 'Fs', []); % sampling freq
addParameter(p, 'LegendLabels', {}); % legend text

parse(p, frequencies, amplitudes, varargin{:});

% extract values
freqs = p.Results.frequencies(:);
amps = p.Results.amplitudes(:);
xrange = p.Results.XRange;
y_max = p.Results.YMax;
x_step = p.Results.XStep;
y_step = p.Results.YStep;
x_label = p.Results.XLabel;
y_label = p.Results.YLabel;
colors_input = p.Results.Colors;
line_width = p.Results.LineWidth;
title_text = p.Results.Title;
fig_number = p.Results.FigNum;
max_xlabels = p.Results.MaxXLabels;
max_ylabels = p.Results.MaxYLabels;
fs_val = p.Results.Fs;
legend_labels = p.Results.LegendLabels;

% generate title if Fs given
if isempty(title_text) && ~isempty(fs_val)
    title_text = sprintf('Sampled Spectrum (Fs = %.1f Hz, Nyquist = %.1f Hz)', fs_val, fs_val/2);
end

% color handling
if ischar(colors_input) || isstring(colors_input)
    colors_input = char(colors_input);
    if strcmp(colors_input, 'auto')
        % auto mode: cyan for odd indices, red for even
        colors = cell(length(freqs), 1);
        for i = 1:length(freqs)
            if mod(i, 2) == 1
                colors{i} = [0 1 1]; % cyan
            else
                colors{i} = [1 0 0]; % red  
            end
        end
    else
        % same color for all
        colors = cell(length(freqs), 1);
        for i = 1:length(freqs)
            colors{i} = colors_input;
        end
    end
elseif iscell(colors_input)
    colors = colors_input;
    % repeat if not enough
    while length(colors) < length(freqs)
        colors = [colors; colors];
    end
    colors = colors(1:length(freqs));
else
    % default cyan
    colors = cell(length(freqs), 1);
    for i = 1:length(freqs)
        colors{i} = 'c';
    end
end

% convert color letters to RGB values
for i = 1:length(colors)
    if ischar(colors{i}) || isstring(colors{i})
        c = char(colors{i});
        if strcmp(c, 'c')
            colors{i} = [0 1 1];
        elseif strcmp(c, 'r')
            colors{i} = [1 0 0];
        elseif strcmp(c, 'b')
            colors{i} = [0 0 1];
        elseif strcmp(c, 'g')
            colors{i} = [0 1 0];
        elseif strcmp(c, 'y')
            colors{i} = [1 1 0];
        elseif strcmp(c, 'm')
            colors{i} = [1 0 1];
        elseif strcmp(c, 'w')
            colors{i} = [1 1 1];
        end
    end
end

% calculate x range if not provided
if isempty(xrange)
    max_freq = max(abs(freqs));
    x_limit = max_freq * 1.2;
    if x_limit == 0
        x_limit = 10;
    end
    xrange = [-x_limit, x_limit];
end

% calculate x step
if isempty(x_step)
    range_size = xrange(2) - xrange(1);
    x_step = range_size / 10;
    % round to nice values
    if x_step >= 1000
        x_step = round(x_step, -3);
    elseif x_step >= 100
        x_step = round(x_step, -2);
    else
        x_step = round(x_step, 1, 'significant');
    end
end

% calculate y max
if isempty(y_max)
    y_max = max(amps) * 1.2;
    if y_max == 0
        y_max = 1;
    end
end

% create figure
if isempty(fig_number)
    fig = figure('Color', 'k');
else
    fig = figure(fig_number);
    clf;
    set(fig, 'Color', 'k');
end

% create axis vectors
x_ticks = xrange(1):x_step:xrange(2);
y_ticks = 0:y_step:y_max;

% plot invisible baseline
plot(x_ticks, zeros(size(x_ticks)), 'Color', [0 0 0]);

% setup axes
ax = gca;
ax.Color = [0 0 0];
ax.GridColor = [0.3 0.3 0.3];
ax.GridAlpha = 0.6;
ax.XColor = [0.9 0.9 0.9];
ax.YColor = [0.9 0.9 0.9];
ax.LineWidth = 1.5;
ax.FontSize = 11;
ax.FontName = 'Arial';
hold on
grid on

xlabel(x_label, 'Color', [0.9 0.9 0.9], 'FontSize', 12);
ylabel(y_label, 'Color', [0.9 0.9 0.9], 'FontSize', 12);

ax.XTick = x_ticks;
ax.YTick = y_ticks;
pbaspect([3 1 1]);
ylim([-0.05, y_max]);

% setup x tick labels - skip some if too many
n_xticks = length(x_ticks);
x_skip = max(1, ceil(n_xticks / max_xlabels));
x_tick_labels = cell(1, n_xticks);
for i = 1:n_xticks
    x_tick_labels{i} = '';
end
for i = 1:x_skip:n_xticks
    x_tick_labels{i} = num2str(x_ticks(i));
end
ax.XTickLabel = x_tick_labels;

% setup y tick labels
n_yticks = length(y_ticks);
y_skip = max(1, ceil(n_yticks / max_ylabels));
y_tick_labels = cell(1, n_yticks);
for i = 1:n_yticks
    y_tick_labels{i} = '';
end
for i = 1:y_skip:n_yticks
    y_tick_labels{i} = num2str(y_ticks(i));
end
ax.YTickLabel = y_tick_labels;

% add title
if ~isempty(title_text)
    title(title_text, 'Color', [0.9 0.9 0.9], 'FontSize', 13, 'FontWeight', 'bold');
end

% draw arrows for each frequency component
for i = 1:length(freqs)
    current_color = colors{i};
    
    % create arrow annotation
    arr = annotation(fig, 'arrow');
    arr.Parent = ax;
    arr.X = [freqs(i) freqs(i)];
    arr.Y = [0 amps(i)];
    arr.Color = current_color;
    arr.LineWidth = line_width;
    arr.HeadLength = 10;
    arr.HeadWidth = 10;
    arr.HeadStyle = 'plain';
end

% add legend text if provided
if ~isempty(legend_labels)
    y_pos = y_max * 0.95;
    y_gap = y_max * 0.08;
    x_pos = xrange(1) + (xrange(2) - xrange(1)) * 0.05;
    
    for i = 1:length(legend_labels)
        text(x_pos, y_pos - (i-1)*y_gap, legend_labels{i}, ...
            'Color', [0.9 0.9 0.9], 'FontSize', 10, 'FontName', 'Courier New', ...
            'Interpreter', 'none', 'VerticalAlignment', 'top');
    end
end

hold off

end
