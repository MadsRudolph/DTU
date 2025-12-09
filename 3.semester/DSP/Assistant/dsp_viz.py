#!/usr/bin/env python3
"""
DSP Visualization Tools - Python Equivalents of DTU MATLAB Scripts
===================================================================

Exact Python ports of DTU 62743 course MATLAB visualization scripts:
- plot_spectrum.m → plot_spectrum()
- spectrum_templates.m → spectrum_AM(), spectrum_aliased(), etc.
- zpgui.m / zplane → plot_pz()
- plot_z_surface.m → plot_z_surface()
- DSP_sketch_generic_spectrum_template.m → sketch_spectrum()

Usage:
    from dsp_viz import *
    
    # Frequency spectrum with arrows
    plot_spectrum([500, -500, 1200], [2, 2, 1])
    
    # Pole-zero plot
    plot_pz(zeros=[0.5, -0.5], poles=[0.9+0.3j, 0.9-0.3j])
    
    # 3D |H(z)| surface
    plot_z_surface([1, -2, 1], [1, -0.5])
    
    # Quick templates
    spectrum_AM(fc=1000, fm=100)

Reference: DTU 62743 Digital Signal Processing Course Materials
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyArrow
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Union, Optional, Tuple, Dict
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning)

# =============================================================================
# CONFIGURATION - Match MATLAB defaults
# =============================================================================
DARK_MODE = True  # Match MATLAB black background theme
DEFAULT_FIGSIZE = (12, 5)
ARROW_LINEWIDTH = 3
ARROW_HEAD_LENGTH = 12
ARROW_HEAD_WIDTH = 10

# Color scheme matching MATLAB 'lines' colormap
MATLAB_COLORS = [
    '#0072BD',  # Blue
    '#D95319',  # Orange
    '#EDB120',  # Yellow
    '#7E2F8E',  # Purple
    '#77AC30',  # Green
    '#4DBEEE',  # Cyan
    '#A2142F',  # Red
]


def _setup_dark_axes(ax, fig=None):
    """Apply dark theme matching MATLAB style"""
    if fig is not None:
        fig.patch.set_facecolor('#0d0d0d')
    ax.set_facecolor('#0d0d0d')
    ax.tick_params(colors='#e6e6e6', labelsize=10)
    ax.xaxis.label.set_color('#e6e6e6')
    ax.yaxis.label.set_color('#e6e6e6')
    ax.title.set_color('#e6e6e6')
    for spine in ax.spines.values():
        spine.set_color('#404040')
    ax.grid(True, alpha=0.3, color='#404040')


# =============================================================================
# PLOT_SPECTRUM - Frequency spectrum with arrows
# Reference: plot_spectrum.m
# =============================================================================
def plot_spectrum(frequencies: Union[List, np.ndarray],
                  amplitudes: Union[List, np.ndarray],
                  x_range: Tuple = None,
                  y_max: float = None,
                  x_step: float = None,
                  y_step: float = 0.5,
                  x_label: str = 'Frequency (Hz)',
                  y_label: str = 'Amplitude (A.U.)',
                  colors: List = None,
                  line_width: float = ARROW_LINEWIDTH,
                  title: str = '',
                  figsize: Tuple = DEFAULT_FIGSIZE,
                  max_x_labels: int = 15,
                  max_y_labels: int = 10,
                  dark_mode: bool = DARK_MODE,
                  show: bool = True,
                  save_path: str = None):
    """
    Plot frequency spectrum with arrows for discrete components.
    
    Exact port of MATLAB plot_spectrum.m
    
    Parameters:
        frequencies: Array of frequency values
        amplitudes: Array of amplitude values
        x_range: (x_min, x_max) - Auto-calculated if None
        y_max: Maximum y value - Auto-calculated if None
        x_step: X-axis tick spacing - Auto-calculated if None
        y_step: Y-axis tick spacing (default: 0.5)
        x_label: X-axis label (default: 'Frequency (Hz)')
        y_label: Y-axis label (default: 'Amplitude (A.U.)')
        colors: List of colors for each arrow
        line_width: Arrow line width (default: 3)
        title: Plot title
        figsize: Figure size (default: (12, 5))
        max_x_labels: Maximum x-tick labels to show
        max_y_labels: Maximum y-tick labels to show
        dark_mode: Use dark background (default: True)
        show: Display plot immediately (default: True)
        save_path: Save figure to file if provided
        
    Returns:
        fig, ax: Matplotlib figure and axis objects
        
    Example:
        >>> fig, ax = plot_spectrum([500, -500, 1200, -1200], [2, 2, 1, 1])
    """
    frequencies = np.array(frequencies).flatten()
    amplitudes = np.array(amplitudes).flatten()
    
    if len(frequencies) != len(amplitudes):
        raise ValueError("Frequencies and amplitudes must have same length")
    
    # Auto-calculate limits (matching MATLAB)
    if x_range is None:
        if len(frequencies) > 0:
            x_max_val = max(abs(frequencies)) * 1.2
        else:
            x_max_val = 10
        if x_max_val == 0:
            x_max_val = 10
        x_range = (-x_max_val, x_max_val)
    
    if x_step is None:
        span = x_range[1] - x_range[0]
        x_step = span / 20
        if x_step != 0:
            x_step = round(x_step, -int(np.floor(np.log10(abs(x_step)))))
        else:
            x_step = 1
    
    if y_max is None:
        if len(amplitudes) > 0:
            y_max = max(amplitudes) * 1.2
        else:
            y_max = 1
        if y_max == 0:
            y_max = 1
    
    # Default colors
    if colors is None:
        colors = [MATLAB_COLORS[i % len(MATLAB_COLORS)] for i in range(len(frequencies))]
    elif len(colors) < len(frequencies):
        colors = (colors * (len(frequencies) // len(colors) + 1))[:len(frequencies)]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if dark_mode:
        _setup_dark_axes(ax, fig)
    
    # Create x and y tick arrays
    x_ticks = np.arange(x_range[0], x_range[1] + x_step, x_step)
    y_ticks = np.arange(0, y_max + y_step, y_step)
    
    # Draw baseline
    ax.plot([x_range[0], x_range[1]], [0, 0], 
            color='#e6e6e6' if dark_mode else 'black', lw=1)
    
    # Draw arrows (matching MATLAB annotation style)
    for i, (f, a) in enumerate(zip(frequencies, amplitudes)):
        color = colors[i]
        
        # Arrow from (f, 0) to (f, a)
        ax.annotate('', 
                    xy=(f, a), 
                    xytext=(f, 0),
                    arrowprops=dict(
                        arrowstyle='-|>',
                        color=color,
                        lw=line_width,
                        mutation_scale=15
                    ))
    
    # Set ticks and labels with thinning
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    
    # Thin x labels
    num_x = len(x_ticks)
    skip_x = max(1, int(np.ceil(num_x / max_x_labels)))
    x_labels = [f'{t:.4g}' if i % skip_x == 0 else '' 
                for i, t in enumerate(x_ticks)]
    ax.set_xticklabels(x_labels)
    
    # Thin y labels
    num_y = len(y_ticks)
    skip_y = max(1, int(np.ceil(num_y / max_y_labels)))
    y_labels = [f'{t:.4g}' if i % skip_y == 0 else '' 
                for i, t in enumerate(y_ticks)]
    ax.set_yticklabels(y_labels)
    
    # Labels and limits
    ax.set_xlim(x_range)
    ax.set_ylim(-0.05 * y_max, y_max)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold')
    
    # Aspect ratio 3:1 (matching MATLAB pbaspect([3,1,1]))
    ax.set_aspect(abs(x_range[1] - x_range[0]) / (3 * y_max))
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, ax


# =============================================================================
# SKETCH_SPECTRUM - Empty template for manual sketching
# Reference: DSP_sketch_generic_spectrum_template.m
# =============================================================================
def sketch_spectrum(x_max: float = 20,
                    x_step: float = 1,
                    y_max: float = 6,
                    y_step: float = 0.5,
                    x_label: str = 'Frequency (set unit)',
                    y_label: str = 'Amplitude (A.U.)',
                    figsize: Tuple = DEFAULT_FIGSIZE,
                    dark_mode: bool = DARK_MODE,
                    show: bool = True):
    """
    Generate empty spectrum plot for manual sketching.
    
    Exact port of DSP_sketch_generic_spectrum_template.m
    """
    return plot_spectrum([], [], 
                        x_range=(-x_max, x_max),
                        y_max=y_max,
                        x_step=x_step,
                        y_step=y_step,
                        x_label=x_label,
                        y_label=y_label,
                        figsize=figsize,
                        dark_mode=dark_mode,
                        show=show)


# =============================================================================
# SPECTRUM_TEMPLATES - Quick theoretical patterns
# Reference: spectrum_templates.m
# =============================================================================
def spectrum_AM(fc: float, fm: float,
                x_label: str = 'Frequency (kHz)',
                title: str = None,
                show: bool = True):
    """AM (Amplitude Modulation) spectrum template."""
    freqs = [-(fc+fm), -(fc-fm), fc-fm, fc+fm]
    amps = [0.25, 0.25, 0.25, 0.25]
    colors = ['red', 'red', 'blue', 'blue']
    
    if title is None:
        title = f'AM Spectrum: fc = {fc}, fm = {fm}'
    
    return plot_spectrum(freqs, amps, x_label=x_label, title=title, 
                        colors=colors, show=show)


def spectrum_baseband(f0: float,
                      x_label: str = 'Frequency (kHz)',
                      title: str = None,
                      show: bool = True):
    """Symmetric baseband signal spectrum at ±f0."""
    freqs = [-f0, f0]
    amps = [0.5, 0.5]
    colors = ['cyan', 'cyan']
    
    if title is None:
        title = f'Baseband Signal: ±{f0}'
    
    return plot_spectrum(freqs, amps, x_label=x_label, title=title,
                        colors=colors, show=show)


def spectrum_harmonics(f0: float, n: int = 5,
                       x_label: str = 'Frequency (kHz)',
                       title: str = None,
                       show: bool = True):
    """Harmonic series spectrum with decreasing amplitudes (1/n)."""
    freqs = [f0 * k for k in range(1, n + 1)]
    amps = [1.0 / k for k in range(1, n + 1)]
    
    if title is None:
        title = f'{n} Harmonics of f0 = {f0}'
    
    return plot_spectrum(freqs, amps, x_label=x_label, title=title,
                        x_range=(0, f0 * (n + 1)), show=show)


def spectrum_aliased(f0: float, Fs: float,
                     x_label: str = 'Frequency (kHz)',
                     title: str = None,
                     show: bool = True):
    """Aliasing demonstration showing original + aliases."""
    freqs = [f0, Fs - f0]
    amps = [1, 1]
    colors = ['cyan', 'red']
    
    if title is None:
        title = f'Aliasing: f0 = {f0}, Fs = {Fs} (Nyquist = {Fs/2})'
    
    fig, ax = plot_spectrum(freqs, amps, 
                           x_range=(0, Fs),
                           x_label=x_label, 
                           title=title,
                           colors=colors,
                           show=False)
    
    # Add Nyquist line
    ax.axvline(x=Fs/2, color='red', linestyle='--', linewidth=2)
    ax.text(Fs/2, 0.5, 'Fs/2', color='red', ha='center', va='bottom', fontsize=10)
    
    if show:
        plt.show()
    
    return fig, ax


def spectrum_sampled(frequencies: List, Fs: float,
                     title: str = None,
                     show: bool = True):
    """Show what happens to multiple frequency components after sampling."""
    F_nyq = Fs / 2
    
    result_freqs = []
    result_amps = []
    colors = []
    annotations = []
    
    for f in frequencies:
        if f <= F_nyq:
            f_apparent = f
            aliased = False
        else:
            f_apparent = abs(Fs - f)
            if f_apparent > F_nyq:
                f_apparent = Fs - f_apparent
            aliased = True
        
        result_freqs.extend([f_apparent, -f_apparent])
        result_amps.extend([1, 1])
        
        if aliased:
            colors.extend(['red', 'red'])
            annotations.append(f'{f:.0f} → {f_apparent:.0f} Hz (ALIASED!)')
        else:
            colors.extend(['cyan', 'cyan'])
            annotations.append(f'{f:.0f} Hz (OK)')
    
    if title is None:
        title = f'Sampled Spectrum (Fs = {Fs} Hz, Nyquist = {F_nyq} Hz)'
    
    fig, ax = plot_spectrum(result_freqs, result_amps,
                           title=title, colors=colors, show=False)
    
    annotation_text = '\n'.join(annotations)
    ax.text(0.02, 0.98, annotation_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top', color='white',
           family='monospace',
           bbox=dict(boxstyle='round', facecolor='#333333', alpha=0.8))
    
    ax.axvline(x=F_nyq, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axvline(x=-F_nyq, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    
    if show:
        plt.show()
    
    return fig, ax


# =============================================================================
# PLOT_PZ - Pole-Zero Plot with Unit Circle
# Reference: zpgui.m / zplane
# =============================================================================
def plot_pz(zeros: Union[List, np.ndarray] = None,
            poles: Union[List, np.ndarray] = None,
            B: Union[List, np.ndarray] = None,
            A: Union[List, np.ndarray] = None,
            title: str = 'Pole-Zero Plot',
            figsize: Tuple = (8, 8),
            show_annotations: bool = True,
            highlight_stability: bool = True,
            show_unit_circle: bool = True,
            dark_mode: bool = DARK_MODE,
            show: bool = True,
            save_path: str = None):
    """
    Plot pole-zero diagram with unit circle.
    
    Can provide zeros/poles directly OR B/A coefficients.
    """
    # Calculate zeros/poles from coefficients if provided
    if B is not None:
        B = np.array(B, dtype=complex)
        zeros = np.roots(B) if len(B) > 1 else np.array([])
    if A is not None:
        A = np.array(A, dtype=complex)
        poles = np.roots(A) if len(A) > 1 else np.array([])
    
    zeros = np.array(zeros if zeros is not None else [], dtype=complex)
    poles = np.array(poles if poles is not None else [], dtype=complex)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if dark_mode:
        _setup_dark_axes(ax, fig)
    
    # Draw unit circle
    if show_unit_circle:
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), 'b-', lw=2, 
                label='Unit Circle', alpha=0.8)
    
    # Draw axes
    ax.axhline(y=0, color='gray', lw=0.8, alpha=0.5)
    ax.axvline(x=0, color='gray', lw=0.8, alpha=0.5)
    
    # Plot zeros (circles)
    for z in zeros:
        magnitude = np.abs(z)
        if highlight_stability:
            if magnitude > 1.001:
                color = 'red'
            elif magnitude < 0.999:
                color = 'green'
            else:
                color = 'orange'
        else:
            color = 'blue'
        
        ax.plot(np.real(z), np.imag(z), 'o', color=color, markersize=12,
                markerfacecolor='none', markeredgewidth=2)
        
        if show_annotations:
            label = f'{z:.2f}' if np.abs(np.imag(z)) > 0.001 else f'{np.real(z):.2f}'
            ax.annotate(label, (np.real(z), np.imag(z)),
                       textcoords='offset points', xytext=(8, 5),
                       fontsize=8, color=color)
    
    # Plot poles (x marks)
    for p in poles:
        magnitude = np.abs(p)
        if highlight_stability:
            if magnitude > 1.001:
                color = 'red'
            elif magnitude < 0.999:
                color = 'green'
            else:
                color = 'orange'
        else:
            color = 'blue'
        
        ax.plot(np.real(p), np.imag(p), 'x', color=color, markersize=12,
                markeredgewidth=3)
        
        if show_annotations:
            label = f'{p:.2f}' if np.abs(np.imag(p)) > 0.001 else f'{np.real(p):.2f}'
            ax.annotate(label, (np.real(p), np.imag(p)),
                       textcoords='offset points', xytext=(8, -10),
                       fontsize=8, color=color)
    
    # Determine axis limits
    all_points = np.concatenate([zeros, poles]) if len(zeros) > 0 or len(poles) > 0 else np.array([0])
    max_extent = max(1.5, np.max(np.abs(all_points)) * 1.3)
    
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)
    ax.set_aspect('equal')
    ax.set_xlabel('Real Part', fontsize=11)
    ax.set_ylabel('Imaginary Part', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    # Legend entries
    ax.plot([], [], 'o', color='gray', markersize=10, markerfacecolor='none',
            markeredgewidth=2, label='Zeros (o)')
    ax.plot([], [], 'x', color='gray', markersize=10, markeredgewidth=2,
            label='Poles (x)')
    if highlight_stability:
        ax.plot([], [], 's', color='green', markersize=8, label='Inside UC (stable)')
        ax.plot([], [], 's', color='red', markersize=8, label='Outside UC (unstable)')
        ax.plot([], [], 's', color='orange', markersize=8, label='On UC')
    
    ax.legend(loc='upper right', fontsize=9)
    
    # Stability summary
    if len(poles) > 0:
        poles_outside = np.sum(np.abs(poles) > 1.001)
        poles_on = np.sum(np.abs(np.abs(poles) - 1) < 0.01)
        if poles_outside > 0:
            stability_text = f'⚠️ UNSTABLE ({poles_outside} pole(s) |p|>1)'
            stability_color = 'red'
        elif poles_on > 0:
            stability_text = f'⚡ MARGINALLY STABLE ({poles_on} pole(s) on UC)'
            stability_color = 'orange'
        else:
            stability_text = '✓ STABLE (all poles |p|<1)'
            stability_color = 'lime'
        ax.text(0.02, 0.02, stability_text, transform=ax.transAxes,
               fontsize=10, color=stability_color, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, ax


# =============================================================================
# PLOT_Z_SURFACE - 3D |H(z)| surface
# Reference: plot_z_surface.m by David Dorran
# =============================================================================
def plot_z_surface(B: Union[List, np.ndarray],
                   A: Union[List, np.ndarray] = None,
                   surface_limit: float = 1.5,
                   resolution: float = 0.02,
                   figsize: Tuple = (10, 8),
                   elevation: float = 30,
                   azimuth: float = -60,
                   show_unit_circle: bool = True,
                   db_limits: Tuple = (-30, 30),
                   title: str = '|H(z)| Surface',
                   dark_mode: bool = DARK_MODE,
                   show: bool = True,
                   save_path: str = None):
    """
    Plot 3D surface of |H(z)| magnitude in the z-plane.
    
    Exact port of MATLAB plot_z_surface.m by David Dorran.
    """
    B = np.array(B, dtype=complex)
    A = np.array(A if A is not None else [1], dtype=complex)
    
    # Get pole and zero positions
    zeros = np.roots(B) if len(B) > 1 else np.array([])
    poles = np.roots(A) if len(A) > 1 else np.array([])
    
    # Create z-plane grid (matching MATLAB)
    min_val = -surface_limit
    max_val = surface_limit
    
    a_vals = np.arange(min_val, max_val + resolution, resolution)
    b_vals = a_vals.copy()
    
    Re, Im = np.meshgrid(a_vals, b_vals[::-1])
    Z_grid = Re + 1j * Im
    
    # Calculate |H(z)| surface in dB (matching MATLAB algorithm)
    z_surface = np.zeros_like(Z_grid, dtype=float)
    
    # Round poles/zeros for surface calculation (matching MATLAB)
    pole_positions = np.round(poles * 10) / 10 + resolution/2 + (resolution/2)*1j
    zero_positions = np.round(zeros * 10) / 10 + resolution/2 + (resolution/2)*1j
    
    # Add zeros (numerator)
    for z in zero_positions:
        with np.errstate(divide='ignore', invalid='ignore'):
            z_surface = z_surface + 20 * np.log10(np.abs(Z_grid - z) + 1e-12)
    
    # Subtract poles (denominator)
    for p in pole_positions:
        with np.errstate(divide='ignore', invalid='ignore'):
            z_surface = z_surface - 20 * np.log10(np.abs(Z_grid - p) + 1e-12)
    
    z_surface = np.clip(z_surface, db_limits[0], db_limits[1])
    
    # Create 3D figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    if dark_mode:
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        ax.title.set_color('white')
    
    # Plot surface
    surf = ax.plot_surface(Re, Im, z_surface, cmap='viridis', 
                          edgecolor='none', alpha=0.9)
    
    # Highlight unit circle on surface
    if show_unit_circle:
        theta = np.linspace(0, 2*np.pi, 200)
        x_uc = np.cos(theta)
        y_uc = np.sin(theta)
        
        z_uc = np.zeros_like(theta)
        for i, t in enumerate(theta):
            z = np.exp(1j * t)
            num = sum(B[k] * z**(-k) for k in range(len(B)))
            den = sum(A[k] * z**(-k) for k in range(len(A)))
            if abs(den) > 1e-10:
                z_uc[i] = 20 * np.log10(np.abs(num / den) + 1e-12)
            else:
                z_uc[i] = db_limits[1]
        z_uc = np.clip(z_uc, db_limits[0], db_limits[1])
        
        ax.plot(x_uc, y_uc, z_uc, 'r-', lw=3, label='Unit Circle |H(e^jω)|')
    
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(db_limits[0], db_limits[1])
    
    ax.set_xlabel('Re(z)', fontsize=10)
    ax.set_ylabel('Im(z)', fontsize=10)
    ax.set_zlabel('Magnitude (dB)', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    ax.view_init(elev=elevation, azim=azimuth)
    
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('dB', color='white' if dark_mode else 'black')
    if dark_mode:
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, ax


# =============================================================================
# FREQUENCY RESPONSE PLOT
# =============================================================================
def plot_frequency_response(B: Union[List, np.ndarray],
                            A: Union[List, np.ndarray] = None,
                            Fs: float = None,
                            N: int = 512,
                            title: str = 'Frequency Response',
                            figsize: Tuple = (12, 8),
                            show_phase: bool = True,
                            db_range: Tuple = (-60, 10),
                            dark_mode: bool = DARK_MODE,
                            show: bool = True,
                            save_path: str = None):
    """Plot magnitude and phase response of H(z)."""
    B = np.array(B, dtype=complex)
    A = np.array(A if A is not None else [1], dtype=complex)
    
    omega = np.linspace(0, np.pi, N)
    
    H = np.zeros(N, dtype=complex)
    for i, w in enumerate(omega):
        z = np.exp(1j * w)
        num = sum(B[k] * z**(-k) for k in range(len(B)))
        den = sum(A[k] * z**(-k) for k in range(len(A)))
        H[i] = num / den if abs(den) > 1e-12 else 1e10
    
    magnitude_dB = 20 * np.log10(np.abs(H) + 1e-12)
    phase = np.unwrap(np.angle(H))
    
    if Fs is not None:
        x = omega * Fs / (2 * np.pi)
        x_label = 'Frequency (Hz)'
    else:
        x = omega / np.pi
        x_label = 'Normalized Frequency (×π rad/sample)'
    
    if show_phase:
        fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
        ax_mag, ax_phase = axes
    else:
        fig, ax_mag = plt.subplots(figsize=(figsize[0], figsize[1]//2))
        axes = [ax_mag]
    
    if dark_mode:
        _setup_dark_axes(ax_mag, fig)
        if show_phase:
            _setup_dark_axes(ax_phase)
    
    ax_mag.plot(x, magnitude_dB, 'b-', lw=2)
    ax_mag.set_ylabel('Magnitude (dB)', fontsize=11)
    ax_mag.set_ylim(db_range)
    ax_mag.set_title(title, fontsize=12, fontweight='bold')
    
    ax_mag.axhline(y=-3, color='red', linestyle='--', alpha=0.7, label='-3 dB')
    ax_mag.legend(loc='upper right')
    
    if show_phase:
        ax_phase.plot(x, phase * 180 / np.pi, 'g-', lw=2)
        ax_phase.set_ylabel('Phase (degrees)', fontsize=11)
        ax_phase.set_xlabel(x_label, fontsize=11)
    else:
        ax_mag.set_xlabel(x_label, fontsize=11)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, axes


# =============================================================================
# IMPULSE RESPONSE PLOT
# =============================================================================
def plot_impulse_response(h: Union[List, np.ndarray],
                          title: str = 'Impulse Response h[n]',
                          figsize: Tuple = (10, 4),
                          show_envelope: bool = False,
                          dark_mode: bool = DARK_MODE,
                          show: bool = True,
                          save_path: str = None):
    """Stem plot of impulse response."""
    h = np.array(h)
    n = np.arange(len(h))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if dark_mode:
        _setup_dark_axes(ax, fig)
    
    markerline, stemlines, baseline = ax.stem(n, h, basefmt='k-')
    plt.setp(stemlines, 'linewidth', 1.5, 'color', '#0072BD')
    plt.setp(markerline, 'markersize', 8, 'color', '#0072BD')
    plt.setp(baseline, 'color', 'gray', 'linewidth', 0.5)
    
    if show_envelope and len(h) > 2:
        ax.plot(n, np.abs(h), 'r--', alpha=0.5, lw=1.5, label='Envelope |h[n]|')
        ax.legend()
    
    ax.axhline(y=0, color='gray', lw=0.5)
    ax.set_xlabel('n', fontsize=11)
    ax.set_ylabel('h[n]', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    if len(h) % 2 == 1:
        center = len(h) // 2
        ax.axvline(x=center, color='orange', linestyle=':', alpha=0.5, 
                  label=f'Center (n={center})')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, ax


# =============================================================================
# LINEAR PHASE ANALYSIS PLOT
# =============================================================================
def plot_linear_phase_analysis(h: Union[List, np.ndarray],
                               figsize: Tuple = (14, 10),
                               dark_mode: bool = DARK_MODE,
                               show: bool = True,
                               save_path: str = None):
    """
    Complete linear phase analysis visualization.
    
    Shows 4 subplots:
    1. Impulse response h[n] with symmetry check
    2. A(ω) amplitude function - checks for negativity!
    3. Magnitude response |H(ω)|
    4. Phase response ∠H(ω)
    """
    h = np.array(h)
    N = len(h)
    K = (N - 1) / 2
    
    h_flipped = h[::-1]
    is_symmetric = np.allclose(h, h_flipped, atol=1e-10)
    is_antisymmetric = np.allclose(h, -h_flipped, atol=1e-10)
    
    omega = np.linspace(-np.pi, np.pi, 1000)
    
    A_omega = np.zeros_like(omega)
    if is_symmetric and N % 2 == 1:
        K_int = int(K)
        A_omega = np.full_like(omega, float(h[K_int]))
        for m in range(1, K_int + 1):
            A_omega = A_omega + 2 * h[K_int - m] * np.cos(m * omega)
    elif is_symmetric and N % 2 == 0:
        K_int = N // 2
        for m in range(K_int):
            A_omega = A_omega + 2 * h[m] * np.cos((K_int - m - 0.5) * omega)
    
    H = np.zeros_like(omega, dtype=complex)
    for i, w in enumerate(omega):
        z = np.exp(1j * w)
        H[i] = sum(h[k] * z**(-k) for k in range(len(h)))
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    if dark_mode:
        fig.patch.set_facecolor('#1a1a1a')
        for ax in axes.flat:
            _setup_dark_axes(ax)
    
    # 1. Impulse Response
    ax1 = axes[0, 0]
    n = np.arange(N)
    markerline, stemlines, baseline = ax1.stem(n, h, basefmt='k-')
    plt.setp(stemlines, 'color', '#0072BD', 'linewidth', 1.5)
    plt.setp(markerline, 'color', '#0072BD', 'markersize', 8)
    plt.setp(baseline, 'color', 'gray')
    ax1.axhline(y=0, color='gray', lw=0.5)
    ax1.set_xlabel('n')
    ax1.set_ylabel('h[n]')
    
    if is_symmetric:
        sym_text = '✓ SYMMETRIC (Type I/II)'
        sym_color = 'lime'
    elif is_antisymmetric:
        sym_text = '✓ ANTISYMMETRIC (Type III/IV)'
        sym_color = 'cyan'
    else:
        sym_text = '✗ NOT SYMMETRIC'
        sym_color = 'red'
    ax1.set_title(f'Impulse Response ({sym_text})', fontweight='bold', color=sym_color)
    
    # 2. A(ω) Amplitude Function
    ax2 = axes[0, 1]
    ax2.plot(omega/np.pi, A_omega, 'b-', lw=2)
    ax2.axhline(y=0, color='red', linestyle='--', lw=1.5)
    ax2.fill_between(omega/np.pi, A_omega, 0, where=(A_omega < 0),
                     color='red', alpha=0.3, label='A(ω) < 0 ⚠️')
    ax2.set_xlabel('ω/π')
    ax2.set_ylabel('A(ω)')
    
    A_min = np.min(A_omega)
    if A_min < -0.001:
        ax2.set_title(f'⚠️ A(ω) GOES NEGATIVE! (min = {A_min:.2f})',
                     fontweight='bold', color='red')
        ax2.legend(loc='upper right')
    else:
        ax2.set_title(f'✓ A(ω) ≥ 0 (min = {A_min:.4f})',
                     fontweight='bold', color='lime')
    
    # 3. Magnitude Response
    ax3 = axes[1, 0]
    ax3.plot(omega/np.pi, np.abs(H), 'b-', lw=2, label='|H(ω)|')
    if is_symmetric or is_antisymmetric:
        ax3.plot(omega/np.pi, np.abs(A_omega), 'r--', lw=1, alpha=0.7, label='|A(ω)|')
    ax3.set_xlabel('ω/π')
    ax3.set_ylabel('|H(ω)|')
    ax3.set_title('Magnitude Response', fontweight='bold')
    ax3.legend(loc='upper right')
    
    # 4. Phase Response
    ax4 = axes[1, 1]
    phase = np.unwrap(np.angle(H))
    ax4.plot(omega/np.pi, phase, 'g-', lw=2, label='∠H(ω) actual')
    
    if is_symmetric:
        ideal_phase = -K * omega
        ax4.plot(omega/np.pi, ideal_phase, 'r--', lw=1, alpha=0.7,
                label=f'Ideal: -{K}ω')
    
    ax4.set_xlabel('ω/π')
    ax4.set_ylabel('∠H(ω) [rad]')
    ax4.set_title('Phase Response', fontweight='bold')
    ax4.legend(loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(),
                    edgecolor='none', bbox_inches='tight')
        print(f"  Saved: {save_path}")
    
    if show:
        plt.show()
    
    return fig, axes


# =============================================================================
# DEMO FUNCTION
# =============================================================================
def demo():
    """Run demo of all visualization functions."""
    print("\n  DSP Visualization Demo")
    print("  " + "="*40)
    
    print("\n  1. Spectrum Plot...")
    plot_spectrum([500, -500, 1200, -1200], [2, 2, 1, 1],
                 title='Example Spectrum', x_label='Frequency (Hz)')
    
    print("\n  2. Pole-Zero Plot...")
    plot_pz(zeros=[1, -1], poles=[0.8+0.4j, 0.8-0.4j],
           title='Example P-Z Diagram')
    
    print("\n  3. Linear Phase Analysis (with A(ω) < 0 trap!)...")
    plot_linear_phase_analysis([2, 1, -6, 1, 2])
    
    print("\n  4. Frequency Response...")
    plot_frequency_response([1, -2, 1], [1, -0.5], title='Example |H(z)|')
    
    print("\n  5. Z-Surface...")
    plot_z_surface([1, -2, 1], [1, -0.5])
    
    print("\n  Demo complete!")


if __name__ == "__main__":
    demo()
