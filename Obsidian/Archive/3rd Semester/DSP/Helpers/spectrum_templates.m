function fig = spectrum_templates(type, varargin)
%SPECTRUM_TEMPLATES Quick theoretical spectrum patterns
%   spectrum_templates('AM', fc, fm)        - AM signal
%   spectrum_templates('baseband', f0)      - Symmetric baseband
%   spectrum_templates('harmonics', f0, n)  - Harmonic series
%   spectrum_templates('aliased', f0, Fs)   - Aliasing demonstration

switch lower(type)
    case 'am'
        fc = varargin{1};  % carrier frequency
        fm = varargin{2};  % modulation frequency
        
        freqs = [-(fc+fm), -(fc-fm), fc-fm, fc+fm];
        amps  = [0.25, 0.25, 0.25, 0.25];
        
        fig = plot_spectrum(freqs, amps, ...
            'XLabel', 'Frequency (kHz)', ...
            'Title', sprintf('AM: f_c = %d kHz, f_m = %d kHz', fc, fm), ...
            'Colors', {{'red'}, {'red'}, {'blue'}, {'blue'}});
    
    case 'baseband'
        f0 = varargin{1};
        
        freqs = [-f0, f0];
        amps  = [0.5, 0.5];
        
        fig = plot_spectrum(freqs, amps, ...
            'XLabel', 'Frequency (kHz)', ...
            'Title', sprintf('Baseband Signal: ±%d kHz', f0), ...
            'Colors', {{'cyan'}, {'cyan'}});
    
    case 'harmonics'
        f0 = varargin{1};
        n  = varargin{2};  % number of harmonics
        
        freqs = f0 * (1:n);
        amps  = 1 ./ (1:n);  % decreasing amplitude
        
        fig = plot_spectrum(freqs, amps, ...
            'XLabel', 'Frequency (kHz)', ...
            'Title', sprintf('%d Harmonics of f_0 = %d kHz', n, f0));
    
    case 'aliased'
        f0 = varargin{1};
        Fs = varargin{2};
        
        % Original + first two aliases
        freqs = [f0, Fs-f0, Fs+f0];
        amps  = [1, 1, 1];
        
        fig = plot_spectrum(freqs, amps, ...
            'XRange', [0, 1.5*Fs], ...
            'XLabel', 'Frequency (kHz)', ...
            'Title', sprintf('Aliasing: f_0 = %d kHz, F_s = %d kHz', f0, Fs));
        
        % Add Nyquist frequency line
        figure(fig); hold on;
        xline(Fs/2, 'r--', 'LineWidth', 2);
        text(Fs/2, 0.5, 'F_s/2', 'Color', 'r', ...
     'HorizontalAlignment','center', ...
     'VerticalAlignment','bottom');

        hold off;
    
    otherwise
        error('Unknown template type: %s', type);
end
end