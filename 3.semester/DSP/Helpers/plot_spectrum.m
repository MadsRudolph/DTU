function fig = plot_spectrum(frequencies, amplitudes, varargin)
%PLOT_SPECTRUM Plot frequency spectrum with arrows for discrete components
%
%   fig = PLOT_SPECTRUM(frequencies, amplitudes) creates a spectrum plot
%   with arrows at specified frequencies and amplitudes.
%
%   Optional Name-Value Pairs (added):
%       'MaxXLabels' - Maximum number of x-axis labels (default: 15)
%       'MaxYLabels' - Maximum number of y-axis labels (default: 10)

%% Parse inputs
p = inputParser;
addRequired(p, 'frequencies', @isnumeric);
addRequired(p, 'amplitudes',  @isnumeric);
addParameter(p, 'XRange',    [], @isnumeric);
addParameter(p, 'YMax',      [], @isnumeric);
addParameter(p, 'XStep',     [], @isnumeric);
addParameter(p, 'YStep',     0.5, @isnumeric);
addParameter(p, 'XLabel',    'Frequency (Hz)', @ischar);
addParameter(p, 'YLabel',    'Amplitude (A.U.)', @ischar);
addParameter(p, 'Colors',    {}, @iscell);
addParameter(p, 'LineWidth', 2, @isnumeric);
addParameter(p, 'Title',     '', @ischar);
addParameter(p, 'FigNum',    [], @isnumeric);
addParameter(p, 'MaxXLabels', 15, @isnumeric);   % NEW
addParameter(p, 'MaxYLabels', 10, @isnumeric);   % NEW

parse(p, frequencies, amplitudes, varargin{:});

freqs       = p.Results.frequencies(:);
amps        = p.Results.amplitudes(:);
xrange      = p.Results.XRange;
ymax        = p.Results.YMax;
xstep       = p.Results.XStep;
ystep       = p.Results.YStep;
xlabel_text = p.Results.XLabel;
ylabel_text = p.Results.YLabel;
colors      = p.Results.Colors;
linewidth   = p.Results.LineWidth;
title_text  = p.Results.Title;
fignum      = p.Results.FigNum;
maxXLabels  = p.Results.MaxXLabels;   % NEW
maxYLabels  = p.Results.MaxYLabels;   % NEW

if numel(freqs) ~= numel(amps)
    error('Frequencies and amplitudes must have the same length');
end

%% Auto limits
if isempty(xrange)
    xmax = max(abs(freqs)) * 1.2;
    if xmax == 0, xmax = 10; end
    xrange = [-xmax, xmax];
end

if isempty(xstep)
    span  = xrange(2) - xrange(1);
    xstep = span / 20;
    xstep = round(xstep, 1, 'significant');
end

if isempty(ymax)
    ymax = max(amps) * 1.2;
    if ymax == 0, ymax = 1; end
end

% Colors
if isempty(colors)
    color_map = lines(numel(freqs));
    colors = cell(numel(freqs),1);
    for i = 1:numel(freqs)
        colors{i} = color_map(i,:);
    end
elseif numel(colors) < numel(freqs)
    colors = repmat(colors, ceil(numel(freqs)/numel(colors)), 1);
    colors = colors(1:numel(freqs));
end

%% Figure setup (black theme kept)
if isempty(fignum)
    fig = figure;
else
    fig = figure(fignum);
end
clf;

set(fig, 'Color', 'k');  % black figure background

xaxis  = xrange(1):xstep:xrange(2);
yindex = 0:ystep:ymax;

plot(xaxis, zeros(size(xaxis)), 'Color',[0 0 0]);  % dummy

ax = gca;
ax.Color        = 'k';
ax.GridColor    = [0.3 0.3 0.3];
ax.GridAlpha    = 0.6;
ax.XColor       = [0.9 0.9 0.9];
ax.YColor       = [0.9 0.9 0.9];
ax.LineWidth    = 1.5;
ax.FontSize     = 12;
ax.FontName     = 'Arial';
hold(ax,'on');
grid(ax,'on');

xlabel(xlabel_text, 'Color', [0.9 0.9 0.9]);
ylabel(ylabel_text, 'Color', [0.9 0.9 0.9]);

% ----- Ticks + label thinning -----
ax.XTick = xaxis;
ax.YTick = yindex;
pbaspect([3 1 1]);
ylim([-0.05, ymax]);

% X labels: show at most maxXLabels
numX = numel(xaxis);
skipX = max(1, ceil(numX / maxXLabels));
xlab = repmat({''}, size(xaxis));
xlab(1:skipX:end) = arrayfun(@num2str, xaxis(1:skipX:end), ...
                             'UniformOutput', false);
ax.XTickLabel = xlab;

% Y labels: show at most maxYLabels
numY = numel(yindex);
skipY = max(1, ceil(numY / maxYLabels));
ylab = repmat({''}, size(yindex));
ylab(1:skipY:end) = arrayfun(@num2str, yindex(1:skipY:end), ...
                             'UniformOutput', false);
ax.YTickLabel = ylab;

if ~isempty(title_text)
    title(title_text, 'Color', [0.9 0.9 0.9]);
end

%% Arrows
for i = 1:numel(freqs)
    anArrow = annotation(fig,'arrow');
    anArrow.Parent      = ax;
    anArrow.X           = [freqs(i) freqs(i)];
    anArrow.Y           = [0 amps(i)];
    if iscell(colors{i})
        anArrow.Color = colors{i}{1};
    elseif ischar(colors{i})
        anArrow.Color = colors{i};
    else
        anArrow.Color = colors{i};
    end
    anArrow.LineWidth   = linewidth;
    anArrow.HeadLength  = 8;
    anArrow.HeadWidth   = 8;
    anArrow.HeadStyle   = 'plain';
end

hold(ax,'off');
end
