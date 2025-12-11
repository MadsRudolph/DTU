function fig = plot_spectrum(frequencies, amplitudes, varargin)
% spectrum plotter for exam
% plots frequency components with arrows
% usage: plot_spectrum([1500 -1500 3800 -3800], [1.5 1.5 1 1])

frequencies=frequencies(:)'; % make row vectors
amplitudes=amplitudes(:)';

if length(frequencies)~=length(amplitudes)
    error('frequencies and amplitudes must be same length');
end

% parse inputs
p=inputParser;
addRequired(p,'frequencies');
addRequired(p,'amplitudes');
addParameter(p,'XRange',[]);
addParameter(p,'YMax',[]);
addParameter(p,'XStep',[]);
addParameter(p,'YStep',0.5);
addParameter(p,'XLabel','Frequency (Hz)');
addParameter(p,'YLabel','Amplitude (A.U.)');
addParameter(p,'Colors','auto');
addParameter(p,'LineWidth',3);
addParameter(p,'Title','');
addParameter(p,'FigNum',[]);
addParameter(p,'MaxXLabels',11);
addParameter(p,'MaxYLabels',8);
addParameter(p,'Fs',[]); 
addParameter(p,'LegendLabels',{});

parse(p,frequencies,amplitudes,varargin{:});

freqs=p.Results.frequencies(:);
amps=p.Results.amplitudes(:);
xrange=p.Results.XRange;
ymax=p.Results.YMax;
xstep=p.Results.XStep;
ystep=p.Results.YStep;
xlbl=p.Results.XLabel;
ylbl=p.Results.YLabel;
cols=p.Results.Colors;
linewidth=p.Results.LineWidth;
ttl=p.Results.Title;
fignum=p.Results.FigNum;
max_x_labels=p.Results.MaxXLabels;
max_y_labels=p.Results.MaxYLabels;
Fs=p.Results.Fs;
legend_txt=p.Results.LegendLabels;

% auto title
if isempty(ttl) && ~isempty(Fs)
    ttl=sprintf('Sampled Spectrum (Fs = %.1f Hz, Nyquist = %.1f Hz)',Fs,Fs/2);
end

% handle colors - cyan for original red for aliased
if ischar(cols)||isstring(cols)
    cols=char(cols);
    if strcmp(cols,'auto')
        colors=cell(length(freqs),1);
        for idx=1:length(freqs)
            if mod(idx,2)==1
                colors{idx}=[0 1 1]; %cyan
            else
                colors{idx}=[1 0 0]; %red
            end
        end
    else
        colors=repmat({cols},length(freqs),1);
    end
elseif iscell(cols)
    colors=cols;
    if length(colors)<length(freqs)
        colors=repmat(colors,ceil(length(freqs)/length(colors)),1);
        colors=colors(1:length(freqs));
    end
else
    colors=repmat({'c'},length(freqs),1);
end

% convert single letters to rgb
for idx=1:length(colors)
    if ischar(colors{idx})||isstring(colors{idx})
        col=char(colors{idx});
        if strcmp(col,'c')
            colors{idx}=[0 1 1];
        elseif strcmp(col,'r')
            colors{idx}=[1 0 0];
        elseif strcmp(col,'b')
            colors{idx}=[0 0 1];
        elseif strcmp(col,'g')
            colors{idx}=[0 1 0];
        elseif strcmp(col,'y')
            colors{idx}=[1 1 0];
        elseif strcmp(col,'m')
            colors{idx}=[1 0 1];
        elseif strcmp(col,'w')
            colors{idx}=[1 1 1];
        end
    end
end

% calculate limits if not provided
if isempty(xrange)
    x_max=max(abs(freqs))*1.2;
    if x_max==0
        x_max=10;
    end
    xrange=[-x_max,x_max];
end

if isempty(xstep)
    span=xrange(2)-xrange(1);
    xstep=span/10;
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
    if ymax==0
        ymax=1;
    end
end

% make figure with dark background
if isempty(fignum)
    fig=figure('Color','k');
else
    fig=figure(fignum);
    clf;
    set(fig,'Color','k');
end

x_axis=xrange(1):xstep:xrange(2);
y_axis=0:ystep:ymax;

plot(x_axis,zeros(size(x_axis)),'Color',[0 0 0]); % invisible baseline

ax=gca;
ax.Color=[0 0 0];
ax.GridColor=[0.3 0.3 0.3];
ax.GridAlpha=0.6;
ax.XColor=[0.9 0.9 0.9];
ax.YColor=[0.9 0.9 0.9];
ax.LineWidth=1.5;
ax.FontSize=11;
ax.FontName='Arial';
hold on
grid on

xlabel(xlbl,'Color',[0.9 0.9 0.9],'FontSize',12);
ylabel(ylbl,'Color',[0.9 0.9 0.9],'FontSize',12);

ax.XTick=x_axis;
ax.YTick=y_axis;
pbaspect([3 1 1]);
ylim([-0.05,ymax]);

% thin out labels if too many
num_x=length(x_axis);
skip_x=max(1,ceil(num_x/max_x_labels));
x_labels=cell(size(x_axis));
for i=1:length(x_labels)
    x_labels{i}='';
end
for i=1:skip_x:num_x
    x_labels{i}=num2str(x_axis(i));
end
ax.XTickLabel=x_labels;

num_y=length(y_axis);
skip_y=max(1,ceil(num_y/max_y_labels));
y_labels=cell(size(y_axis));
for i=1:length(y_labels)
    y_labels{i}='';
end
for i=1:skip_y:num_y
    y_labels{i}=num2str(y_axis(i));
end
ax.YTickLabel=y_labels;

if ~isempty(ttl)
    title(ttl,'Color',[0.9 0.9 0.9],'FontSize',13,'FontWeight','bold');
end

% draw arrows for each frequency
for i=1:length(freqs)
    color=colors{i};
    
    arrow=annotation(fig,'arrow');
    arrow.Parent=ax;
    arrow.X=[freqs(i) freqs(i)];
    arrow.Y=[0 amps(i)];
    arrow.Color=color;
    arrow.LineWidth=linewidth;
    arrow.HeadLength=10;
    arrow.HeadWidth=10;
    arrow.HeadStyle='plain';
end

% legend text in top left corner
if ~isempty(legend_txt)
    y_start=ymax*0.95;
    y_spacing=ymax*0.08;
    x_position=xrange(1)+(xrange(2)-xrange(1))*0.05;
    
    for i=1:length(legend_txt)
        text(x_position,y_start-(i-1)*y_spacing,legend_txt{i},...
            'Color',[0.9 0.9 0.9],'FontSize',10,'FontName','Courier New',...
            'Interpreter','none','VerticalAlignment','top');
    end
end

hold off

end
