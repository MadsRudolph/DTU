function fig = plot_spectrum(frequencies, amplitudes, varargin)
% Plot frequency spectrum with stems
% Made this for DSP exam - plots the frequency components
% Quick use: plot_spectrum([1500 -1500 3800 -3800], [1.5 1.5 1 1])

% make sure they're row vectors
frequencies = frequencies(:)';
amplitudes = amplitudes(:)';

if length(frequencies) ~= length(amplitudes)
    error('need same number of freqs and amps!');
end

% setup input parser (learned this from stackoverflow)
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
addParameter(p, 'Fs', []); % sampling frequency for auto title
addParameter(p, 'LegendLabels', {}); % text labels

parse(p, frequencies, amplitudes, varargin{:});

% grab all the values
freqs = p.Results.frequencies(:);
amps = p.Results.amplitudes(:);
xrange = p.Results.XRange;
ymax = p.Results.YMax;
xstep = p.Results.XStep;
ystep= p.Results.YStep;
xlbl = p.Results.XLabel;
ylbl = p.Results.YLabel;
cols = p.Results.Colors;
lw = p.Results.LineWidth;
ttl = p.Results.Title;
figN = p.Results.FigNum;
maxXlab = p.Results.MaxXLabels;
maxYlab = p.Results.MaxYLabels;
fs_value = p.Results.Fs;
leg_labels = p.Results.LegendLabels;

% auto title if Fs given
if isempty(ttl) && ~isempty(fs_value)
    ttl = sprintf('Sampled Spectrum (Fs = %.1f Hz, Nyquist = %.1f Hz)', fs_value, fs_value/2);
end

% color handling - cyan for original, red for aliased
if ischar(cols) || isstring(cols)
    cols = char(cols);
    if strcmp(cols,'auto')
        % auto color: cyan then red alternating
        colors = cell(length(freqs),1);
        for i=1:length(freqs)
            if mod(i,2)==1
                colors{i}=[0 1 1]; % cyan
            else
                colors{i}=[1 0 0]; % red
            end
        end
    else
        % single color
        colors=repmat({cols},length(freqs),1);
    end
elseif iscell(cols)
    colors=cols;
    % extend if not enough colors
    if length(colors)<length(freqs)
        colors=repmat(colors,ceil(length(freqs)/length(colors)),1);
        colors=colors(1:length(freqs));
    end
else
    colors=repmat({'c'},length(freqs),1);
end

% convert color letters to RGB
for i=1:length(colors)
    if ischar(colors{i}) || isstring(colors{i})
        c = char(colors{i});
        switch c
            case 'c', colors{i}=[0 1 1];
            case 'r', colors{i}=[1 0 0];
            case 'b', colors{i}=[0 0 1];
            case 'g', colors{i}=[0 1 0];
            case 'y', colors{i}=[1 1 0];
            case 'm', colors{i}=[1 0 1];
            case 'w', colors{i}=[1 1 1];
        end
    end
end

% figure out axis limits
if isempty(xrange)
    xmax=max(abs(freqs))*1.2;
    if xmax==0, xmax=10; end
    xrange=[-xmax,xmax];
end

if isempty(xstep)
    span=xrange(2)-xrange(1);
    xstep=span/10;
    % round to nice numbers
    if xstep>=1000
        xstep=round(xstep,-3);
    elseif xstep>=100
        xstep=round(xstep,-2);
    else
        xstep=round(xstep,1,'significant');
    end
end

if isempty(ymax)
    ymax=max(amps)*1.2;
    if ymax==0, ymax=1; end
end

% create figure
if isempty(figN)
    fig=figure('Color','k');
else
    fig=figure(figN);
    clf;
    set(fig,'Color','k');
end

xaxis=xrange(1):xstep:xrange(2);
yaxis=0:ystep:ymax;

% draw zero line (invisible but needed for axis)
plot(xaxis,zeros(size(xaxis)),'Color',[0 0 0]);

ax=gca;
ax.Color=[0 0 0];
ax.GridColor=[0.3 0.3 0.3];
ax.GridAlpha=0.6;
ax.XColor=[0.9 0.9 0.9];
ax.YColor=[0.9 0.9 0.9];
ax.LineWidth=1.5;
ax.FontSize=11;
ax.FontName='Arial';
hold on;
grid on;

xlabel(xlbl,'Color',[0.9 0.9 0.9],'FontSize',12);
ylabel(ylbl,'Color',[0.9 0.9 0.9],'FontSize',12);

ax.XTick=xaxis;
ax.YTick=yaxis;
pbaspect([3 1 1]);
ylim([-0.05,ymax]);

% don't show all tick labels if too many
nX=length(xaxis);
skipX=max(1,ceil(nX/maxXlab));
xlabels=cell(size(xaxis));
xlabels(:)={''};
for i=1:skipX:nX
    xlabels{i}=num2str(xaxis(i));
end
ax.XTickLabel=xlabels;

nY=length(yaxis);
skipY=max(1,ceil(nY/maxYlab));
ylabels=cell(size(yaxis));
ylabels(:)={''};
for i=1:skipY:nY
    ylabels{i}=num2str(yaxis(i));
end
ax.YTickLabel=ylabels;

if ~isempty(ttl)
    title(ttl,'Color',[0.9 0.9 0.9],'FontSize',13,'FontWeight','bold');
end

% draw the arrows 
for i=1:length(freqs)
    c=colors{i};
    
    arr=annotation(fig,'arrow');
    arr.Parent=ax;
    arr.X=[freqs(i) freqs(i)];
    arr.Y=[0 amps(i)];
    arr.Color=c;
    arr.LineWidth=lw;
    arr.HeadLength=10;
    arr.HeadWidth=10;
    arr.HeadStyle='plain';
end

% add legend text in corner if provided
if ~isempty(leg_labels)
    ystart=ymax*0.95;
    ystep_txt=ymax*0.08;
    xpos=xrange(1)+(xrange(2)-xrange(1))*0.05;
    
    for i=1:length(leg_labels)
        text(xpos, ystart-(i-1)*ystep_txt, leg_labels{i}, ...
            'Color',[0.9 0.9 0.9],'FontSize',10,'FontName','Courier New', ...
            'Interpreter','none','VerticalAlignment','top');
    end
end

hold off;

end
