#!/usr/bin/env python3
"""Generate QSPICE schematic for two-stage CMOS opamp (34655)."""
import os

O = b'\xab'  # open delimiter
C = b'\xbb'  # close delimiter
CRLF = b'\r\n'
HDR = b'\xff\xd8\xff\xdb'
BOM = b'\xef\xbb\xbf'  # UTF-8 BOM for SPICE directives

def L(indent, text, close=True):
    """One line: open + text + optional close."""
    b = b'  ' * indent + O + text.encode('latin-1')
    if close:
        b += C
    return b + CRLF

def CL(indent):
    """Close block."""
    return b'  ' * indent + C + CRLF

# ---------- symbol templates ----------

def nmos_symbol(ref, value):
    """NMOS symbol: D at top (100,200), G left (-200,0), S bottom (100,-200)."""
    return (
        L(2, 'symbol NMOS', False) +
        L(3, 'type: MN') +
        L(3, 'description: N-Channel MOSFET') +
        L(3, 'shorted pins: false') +
        L(3, 'line (100,200) (100,150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,-150) (100,-200) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-100,150) (-100,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-100,0) (-200,0) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,-150) (-50,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,150) (-50,150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-50,150) (-50,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'triangle (70,-150) (-25,-125) (-25,-175) 0 0 0x1000000 0x3000000 -1 -1') +
        L(3, f'text (200,200) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (200,-200) 1 7 0 0x1000000 -1 -1 "{value}"') +
        L(3, 'pin (100,200) (0,0) 1 0 0 0x0 -1 "D"') +
        L(3, 'pin (-200,0) (0,0) 1 0 0 0x0 -1 "G"') +
        L(3, 'pin (100,-200) (0,0) 1 0 0 0x0 -1 "S"') +
        CL(2)
    )

def pmos_symbol(ref, value):
    """PMOS symbol: S at top (100,200), G left (-200,0), D bottom (100,-200).
    Pin ORDER is D,G,S for correct SPICE netlist."""
    return (
        L(2, 'symbol PMOS', False) +
        L(3, 'type: MP') +
        L(3, 'description: P-Channel MOSFET') +
        L(3, 'shorted pins: false') +
        L(3, 'line (100,200) (100,150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,-150) (100,-200) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-100,150) (-100,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-100,0) (-200,0) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,-150) (-50,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (100,150) (-50,150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (-50,150) (-50,-150) 0 0 0x1000000 -1 -1') +
        # Arrow at source (top), pointing right (outward for PMOS)
        L(3, 'triangle (70,150) (-25,125) (-25,175) 0 0 0x1000000 0x3000000 -1 -1') +
        # Bubble on gate
        L(3, 'ellipse (-118,18) (-82,-18) 0 0 0 0x1000000 0x1000000 -1 -1') +
        L(3, f'text (200,200) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (200,-200) 1 7 0 0x1000000 -1 -1 "{value}"') +
        # Pin order: D first, G second, S third (SPICE netlist order)
        L(3, 'pin (100,-200) (0,0) 1 0 0 0x0 -1 "D"') +
        L(3, 'pin (-200,0) (0,0) 1 0 0 0x0 -1 "G"') +
        L(3, 'pin (100,200) (0,0) 1 0 0 0x0 -1 "S"') +
        CL(2)
    )

def vsrc_symbol(ref, value):
    """Voltage source symbol."""
    return (
        L(2, 'symbol V', False) +
        L(3, 'type: V') +
        L(3, 'description: Independent Voltage Source') +
        L(3, 'shorted pins: false') +
        L(3, 'line (0,-130) (0,-200) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,200) (0,130) 0 0 0x1000000 -1 -1') +
        L(3, 'rect (-25,77) (25,73) 0 0 0 0x1000000 0x3000000 -1 0 -1') +
        L(3, 'rect (-2,50) (2,100) 0 0 0 0x1000000 0x3000000 -1 0 -1') +
        L(3, 'rect (-25,-73) (25,-77) 0 0 0 0x1000000 0x3000000 -1 0 -1') +
        L(3, 'ellipse (-130,130) (130,-130) 0 0 0 0x1000000 0x1000000 -1 -1') +
        L(3, f'text (100,150) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (100,-150) 1 7 0 0x1000000 -1 -1 "{value}"') +
        L(3, 'pin (0,200) (0,0) 1 0 0 0x0 -1 "+"') +
        L(3, 'pin (0,-200) (0,0) 1 0 0 0x0 -1 "-"') +
        CL(2)
    )

def isrc_symbol(ref, value):
    """Current source symbol."""
    return (
        L(2, 'symbol I', False) +
        L(3, 'type: I') +
        L(3, 'description: Independent Current Source') +
        L(3, 'shorted pins: false') +
        L(3, 'line (0,-130) (0,-200) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,200) (0,130) 0 0 0x1000000 -1 -1') +
        # Arrow inside circle pointing up
        L(3, 'line (0,-60) (0,60) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,60) (-20,30) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,60) (20,30) 0 0 0x1000000 -1 -1') +
        L(3, 'ellipse (-130,130) (130,-130) 0 0 0 0x1000000 0x1000000 -1 -1') +
        L(3, f'text (100,150) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (100,-150) 1 7 0 0x1000000 -1 -1 "{value}"') +
        L(3, 'pin (0,200) (0,0) 1 0 0 0x0 -1 "+"') +
        L(3, 'pin (0,-200) (0,0) 1 0 0 0x0 -1 "-"') +
        CL(2)
    )

def res_symbol(ref, value):
    """Resistor symbol (UK box style)."""
    return (
        L(2, 'symbol R1', False) +
        L(3, 'type: R') +
        L(3, 'description: Resistor(UK Style Symbol)') +
        L(3, 'shorted pins: false') +
        L(3, 'line (0,-200) (0,-150) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,150) (0,200) 0 0 0x1000000 -1 -1') +
        L(3, 'rect (50,-150) (-50,150) 0 0 0 0x1000000 0x2000000 -1 0 -1') +
        L(3, f'text (50,150) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (50,-150) 1 7 0 0x1000000 -1 -1 "{value}"') +
        L(3, 'pin (0,-200) (0,0) 1 64 0 0x0 -1 "+"') +
        L(3, 'pin (0,200) (0,0) 1 64 0 0x0 -1 "-"') +
        CL(2)
    )

def cap_symbol(ref, value):
    """Capacitor symbol."""
    return (
        L(2, 'symbol C', False) +
        L(3, 'type: C') +
        L(3, 'description: Capacitor') +
        L(3, 'shorted pins: false') +
        L(3, 'line (0,200) (0,40) 0 0 0x1000000 -1 -1') +
        L(3, 'line (0,-40) (0,-200) 0 0 0x1000000 -1 -1') +
        L(3, 'rect (-130,-40) (130,-30) 0 0 0 0x1000000 0x3000000 -1 0 -1') +
        L(3, 'rect (-130,30) (130,40) 0 0 0 0x1000000 0x3000000 -1 0 -1') +
        L(3, f'text (180,150) 1 7 0 0x1000000 -1 -1 "{ref}"') +
        L(3, f'text (180,-150) 1 7 0 0x1000000 -1 -1 "{value}"') +
        L(3, 'pin (0,200) (0,0) 1 0 0 0x0 -1 "+"') +
        L(3, 'pin (0,-200) (0,0) 1 0 0 0x0 -1 "-"') +
        CL(2)
    )

def component(x, y, rot, sym_func, ref, value):
    """Full component block."""
    return (
        L(1, f'component ({x},{y}) {rot} 0', False) +
        sym_func(ref, value) +
        CL(1)
    )

def wire(x1, y1, x2, y2, name=""):
    """Wire element."""
    n = f' "{name}"' if name else ''
    return L(1, f'wire ({x1},{y1}) ({x2},{y2}){n}')

def net(x, y, flags, name):
    """Net label. flags: 13=GND, 14=VDD/up, 11=right, 7=right."""
    return L(1, f'net ({x},{y}) 1 {flags} 0 "{name}"')

def junction(x, y):
    return L(1, f'junction ({x},{y})')

def spice_text(x, y, text):
    """SPICE directive as text element."""
    # SPICE text needs UTF-8 BOM prefix in the string
    bom_str = '\xef\xbb\xbf'
    return L(1, f'text ({x},{y}) 1 7 0 0x1000000 -1 -1 "{bom_str}{text}"')


# ========== BUILD SCHEMATIC ==========
data = HDR
data += L(0, 'schematic', False)

# --- PMOS transistors (S at top, D at bottom) ---
# Q8: bias ref, diode-connected
data += component(-2400, 2800, 0, pmos_symbol, "MQ8", "PMOS_018 W=14u L=1u")
# Q5: tail current source
data += component(0, 2800, 0, pmos_symbol, "MQ5", "PMOS_018 W=17u L=1u")
# Q6: 2nd stage load
data += component(3200, 2800, 0, pmos_symbol, "MQ6", "PMOS_018 W=43u L=1u")
# Q1: diff pair inverting
data += component(-800, 2000, 0, pmos_symbol, "MQ1", "PMOS_018 W=24u L=1u")
# Q2: diff pair non-inverting (mirrored so gate faces right)
data += component(800, 2000, 8, pmos_symbol, "MQ2", "PMOS_018 W=24u L=1u")

# --- NMOS transistors (D at top, S at bottom) ---
# Q3: mirror ref, diode-connected
data += component(-800, 1000, 0, nmos_symbol, "MQ3", "NMOS_018 W=6.2u L=1u")
# Q4: mirror output (mirrored so gate faces right)
data += component(800, 1000, 8, nmos_symbol, "MQ4", "NMOS_018 W=6.2u L=1u")
# Q7: 2nd stage CS
data += component(3200, 1000, 0, nmos_symbol, "MQ7", "NMOS_018 W=31u L=1u")

# --- Sources ---
data += component(-3600, 2800, 0, vsrc_symbol, "Vdd", "1.8")
data += component(-2400, 2000, 0, isrc_symbol, "Ibias", "20u")
data += component(1600, 400, 0, vsrc_symbol, "Vin", "DC 0 AC 1")

# --- Compensation: Rc (horizontal, rot 6) and Cc (horizontal, rot 2) ---
# Rotation 6 (270 CCW): R pin+ at left (-200,0), pin- at right (200,0)
data += component(1800, 1600, 6, res_symbol, "Rc", "995")
# Rotation 2 (90 CCW): C pin+ at left (-200,0), pin- at right (200,0)
data += component(2400, 1600, 2, cap_symbol, "Cc", "0.8p")

# --- Feedback network ---
data += component(4200, 2200, 0, cap_symbol, "CB", "1p")
data += component(4200, 1200, 0, cap_symbol, "CA", "1p")
data += component(4600, 1600, 0, res_symbol, "R1", "1G")
data += component(5000, 2400, 0, cap_symbol, "CL", "1.5p")

# ========== WIRES ==========

# --- VDD connections ---
# Q8.S at (-2300,3000), Q5.S at (100,3000), Q6.S at (3300,3000)
# Vdd+ at (-3600,3000)
data += wire(-3600, 3000, -2300, 3000, "VDD")
data += wire(-2300, 3000, 100, 3000, "VDD")
data += wire(100, 3000, 3300, 3000, "VDD")
data += junction(-2300, 3000)
data += junction(100, 3000)

# --- GND connections via labels ---
# Q3.S (-700,800), Q4.S (700,800), Q7.S (3300,800)
# Ibias- (-2400,1800), Vdd- (-3600,2600), Vin- (1600,200)
data += wire(-700, 800, -700, 600)
data += net(-700, 600, 13, "GND")
data += wire(700, 800, 700, 600)
data += net(700, 600, 13, "GND")
data += wire(3300, 800, 3300, 600)
data += net(3300, 600, 13, "GND")
data += wire(-2400, 1800, -2400, 1600)
data += net(-2400, 1600, 13, "GND")
data += wire(-3600, 2600, -3600, 2400)
data += net(-3600, 2400, 13, "GND")
data += wire(1600, 200, 1600, 0)
data += net(1600, 0, 13, "GND")
# Feedback GND
data += wire(4200, 1000, 4200, 800)
data += net(4200, 800, 13, "GND")
data += wire(4600, 1800, 4600, 2000)
data += net(4600, 2000, 13, "GND")
data += wire(5000, 2200, 5000, 2000)
data += net(5000, 2000, 13, "GND")

# --- n_bias network ---
# Q8.D at (-2300,2600), Q8.G at (-2600,2800) -> diode
data += wire(-2600, 2800, -2600, 2600)
data += wire(-2600, 2600, -2300, 2600, "n_bias")
data += junction(-2300, 2600)
# Ibias+ at (-2400,2200) connects up to n_bias
data += wire(-2400, 2200, -2400, 2600)
data += wire(-2400, 2600, -2300, 2600, "n_bias")
data += junction(-2400, 2600)
# Q5.G at (-200,2800) label
data += wire(-200, 2800, -400, 2800)
data += net(-400, 2800, 11, "n_bias")
# Q6.G at (3000,2800) label
data += wire(3000, 2800, 2800, 2800)
data += net(2800, 2800, 11, "n_bias")
# Label on the bias node itself
data += net(-2300, 2500, 11, "n_bias")

# --- n_tail ---
# Q5.D at (100,2600) -> down to diff pair
data += wire(100, 2600, 100, 2200, "n_tail")
# Q1.S at (-700,2200), Q2.S at (700,2200): horizontal wire
data += wire(-700, 2200, 700, 2200, "n_tail")
data += junction(100, 2200)

# --- n_d1 (Q1.D to Q3.D vertical) ---
data += wire(-700, 1800, -700, 1200, "n_d1")
# Q3 diode: G at (-1000,1000) -> up and right to n_d1
data += wire(-1000, 1000, -1000, 1200)
data += wire(-1000, 1200, -700, 1200, "n_d1")
data += junction(-700, 1200)
# Q4.G label (mirrored: G at (1000,1000))
data += wire(1000, 1000, 1200, 1000)
data += net(1200, 1000, 11, "n_d1")

# --- n_d2 (Q2.D to Q4.D vertical) ---
# Q2 mirrored: D at (700,1800). Q4 mirrored: D at (700,1200)
data += wire(700, 1800, 700, 1200, "n_d2")
# Compensation: Rc+ left at (1600,1600) connects to n_d2
data += wire(700, 1600, 1600, 1600, "n_d2")
data += junction(700, 1600)
# Q7.G at (3000,1000) label
data += wire(3000, 1000, 2800, 1000)
data += net(2800, 1000, 11, "n_d2")

# --- Compensation: Rc to Cc to vout ---
# Rc- at (2000,1600) -> Cc+ at (2200,1600)
data += wire(2000, 1600, 2200, 1600, "n_comp")
# Cc- at (2600,1600) -> vout
data += wire(2600, 1600, 3300, 1600, "vout")
data += junction(3300, 1600)

# --- vout (Q6.D to Q7.D vertical) ---
data += wire(3300, 2600, 3300, 1200, "vout")
# Extend vout right to feedback network
data += wire(3300, 2400, 4200, 2400, "vout")
data += junction(3300, 2400)
data += wire(4200, 2400, 5000, 2400, "vout")
data += junction(4200, 2400)
data += wire(5000, 2400, 5000, 2600)
# CB+ at (4200,2400), CL+ at (5000,2600)

# --- n_inv ---
# Q1.G at (-1000,2000) label
data += wire(-1000, 2000, -1200, 2000)
data += net(-1200, 2000, 11, "n_inv")
# CB- at (4200,2000) -> CA+ at (4200,1400) -> R1+ at (4600,1400)
data += wire(4200, 2000, 4200, 1400, "n_inv")
data += wire(4200, 1400, 4600, 1400, "n_inv")
data += junction(4200, 1400)
# Label
data += net(4300, 1700, 11, "n_inv")

# --- vin ---
# Q2.G (mirrored) at (1000,2000) label
data += wire(1000, 2000, 1200, 2000)
data += net(1200, 2000, 11, "vin")
# Vin+ at (1600,600) label
data += wire(1600, 600, 1600, 800)
data += net(1600, 800, 14, "vin")

# ========== SPICE DIRECTIVES ==========
data += spice_text(-3600, 400,
    ".model NMOS_018 nmos (level=1 kp=270u vto=0.5 lambda=0.08 gamma=0.4 phi=0.65)")
data += spice_text(-3600, 200,
    ".model PMOS_018 pmos (level=1 kp=70u vto=-0.45 lambda=0.08 gamma=0.4 phi=0.65)")
data += spice_text(-3600, 0, ".ac dec 200 1 10G")
data += spice_text(-3600, -200, ".meas AC dc_gain find vdb(vout) at=1")
data += spice_text(-3600, -400, ".meas AC ugf when vdb(vout)=0")
data += spice_text(-3600, -600, ".meas AC phase_at_ugf find vp(vout) when vdb(vout)=0")

# ========== CLOSE SCHEMATIC ==========
data += CL(0)
data += CRLF

# Write file
outpath = os.path.join(os.path.dirname(__file__), "two_stage_opamp.qsch")
with open(outpath, 'wb') as f:
    f.write(data)
print(f"Written: {outpath} ({len(data)} bytes)")
