"""Generate Opg 10 submission PDF for course 62711.

Renders the five WaveDrom timing diagrams via `npx wavedrom-cli` (Node)
and embeds the resulting SVGs into a reportlab PDF that mirrors the
opg5_submission.pdf layout.
"""

import os
import shutil
import subprocess
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image,
)
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── Fonts ────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('Consolas-Bold', 'C:/Windows/Fonts/consolab.ttf'))
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold',
                   italic='Arial-Italic', boldItalic='Arial-BoldItalic')
registerFontFamily('Consolas', normal='Consolas', bold='Consolas-Bold')

OUTPUT = r"C:\Users\Mads2\DTU\Obsidian\Courses\62711 Digital Systems Design\Exercises\Work\opg10_submission.pdf"
TMP_DIR = tempfile.mkdtemp(prefix='opg10_wd_')

# ── WaveDrom specs (identical to those embedded in the .md file) ────────
WAVE_A = """
{signal: [
  {name: 'clk',             wave: 'p..'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=..', data: ['0x45']},
    {name: 'MW',            wave: '010'},
    {name: 'Data_In[15:0]', wave: 'x=x', data: ['0x00AA']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: '=.=', data: ['0x0000', '0x00AA']},
    {name: 'Data_OutR[15:0]', wave: '=..', data: ['0x0000']},
    {name: 'MMR',             wave: '0..'},
    {name: 'MUX MR out',      wave: '=.=', data: ['0x0000', '0x00AA']},
  ],
  {},
  ['I/O (idle)',
    {name: 'D_Word[15:0]', wave: '=..', data: ['0x0000']},
    {name: 'LD[7:0]',      wave: '=..', data: ['0x00']},
    {name: 'SW[7:0]',      wave: '=..', data: ['0x00']},
    {name: 'BTN[5:1]',     wave: '=..', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
"""

WAVE_B = """
{signal: [
  {name: 'clk',             wave: 'p.'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=.', data: ['0xF8']},
    {name: 'MW',            wave: '10'},
    {name: 'Data_In[15:0]', wave: '=x', data: ['0x0055']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: 'xx'},
    {name: 'Data_OutR[15:0]', wave: '==', data: ['0x0000', '0x0055']},
    {name: 'MMR',             wave: '1.'},
    {name: 'MUX MR out',      wave: '==', data: ['0x0000', '0x0055']},
  ],
  {},
  ['Port register / I/O',
    {name: 'MR0 (internal)',  wave: '==', data: ['0x00', '0x55']},
    {name: 'D_Word[15:0]',    wave: '==', data: ['0x0000', '0x0055']},
    {name: 'LD[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'SW[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'BTN[5:1]',        wave: '=.', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
"""

WAVE_C = """
{signal: [
  {name: 'clk',             wave: 'p.'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=.', data: ['0xFC']},
    {name: 'MW',            wave: '10'},
    {name: 'Data_In[15:0]', wave: '=x', data: ['0x00CC']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: 'xx'},
    {name: 'Data_OutR[15:0]', wave: '=.', data: ['0x0000']},
    {name: 'MMR',             wave: '1.'},
    {name: 'MUX MR out',      wave: '=.', data: ['0x0000']},
  ],
  {},
  ['Port register / I/O',
    {name: 'MR4 (read-only)', wave: '=.', data: ['0x00 (write ignored)']},
    {name: 'D_Word[15:0]',    wave: '=.', data: ['0x0000']},
    {name: 'LD[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'SW[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'BTN[5:1]',        wave: '=.', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
"""

WAVE_D = """
{signal: [
  {name: 'clk',             wave: 'p...'},
  {},
  ['User input',
    {name: 'SW[7:0]',       wave: '=...', data: ['0xA5']},
    {name: 'BTNL',          wave: '10..'},
    {name: 'BTN others',    wave: '0...'},
  ],
  {},
  ['CPU bus',
    {name: 'Address[7:0]',  wave: 'x.=.', data: ['0xFC']},
    {name: 'MW',            wave: '0.10'},
    {name: 'Data_In[15:0]', wave: 'x.=x', data: ['0x00CC']},
  ],
  {},
  ['Memory output',
    {name: 'MR4 (internal)',  wave: '==..', data: ['0x00', '0xA5']},
    {name: 'Data_OutR[15:0]', wave: 'x.=.', data: ['0x00A5']},
    {name: 'MMR',             wave: '0.1.'},
    {name: 'MUX MR out',      wave: 'x.=.', data: ['0x00A5']},
  ],
  {},
  ['I/O',
    {name: 'D_Word[15:0]', wave: '=...', data: ['0x0000']},
    {name: 'LD[7:0]',      wave: '=...', data: ['0x00']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
"""

WAVE_CALC = """
{signal: [
  {name: 'clk',             wave: 'p.......'},
  {},
  ['Operand input',
    {name: 'SW[7:0]',       wave: '==......', data: ['0x12', '0x34']},
    {name: 'BTNU',          wave: '10......'},
    {name: 'BTND',          wave: '010.....'},
  ],
  {},
  ['CPU bus',
    {name: 'Phase',         wave: '========', data: ['BTNU', 'BTND', 'ld A6', 'ld A7', 'add', 'st A4', 'st A5', 'done']},
    {name: 'Address[7:0]',  wave: 'xx==x==x', data: ['0xFE', '0xFD', '0xF8', '0xF9']},
    {name: 'MW',            wave: '0....1.0'},
    {name: 'Data_In[15:0]', wave: 'xxxxx==x', data: ['0x0046', '0x0012']},
    {name: 'MMR',           wave: '0.1.01.0'},
    {name: 'MUX MR out',    wave: 'x.==xxxx', data: ['0x0012', '0x0034']},
  ],
  {},
  ['Port registers',
    {name: 'MR6 (BTNU)',    wave: '==......', data: ['0x00', '0x12']},
    {name: 'MR5 (BTND)',    wave: '=.=.....', data: ['0x00', '0x34']},
    {name: 'MR0 (D_Word lo)', wave: '=.....=.', data: ['0x00', '0x46']},
    {name: 'MR1 (D_Word hi)', wave: '=......=', data: ['0x00', '0x12']},
  ],
  {},
  ['CPU registers',
    {name: 'R0', wave: '=..=....', data: ['0x00', '0x12']},
    {name: 'R1', wave: '=...=...', data: ['0x00', '0x34']},
    {name: 'R2', wave: '=....=..', data: ['0x00', '0x46']},
  ],
  {},
  {name: 'D_Word[15:0]', wave: '=.....==', data: ['0x0000', '0x0046', '0x1246']},
],
 config: {hscale: 2},
 head: {tick: 1},
 foot: {text: 'Each slot abstracts one PWF instruction (= 2 clock cycles: INF + EX0)'}}
"""


def render_wavedrom(spec, name, max_w_mm=165, max_h_mm=235):
    """Render a WaveDrom JSON5 spec to PNG via wavedrom-cli, return a
    reportlab Image scaled to fit within (max_w_mm, max_h_mm)."""
    json_path = os.path.join(TMP_DIR, f'{name}.json5')
    png_path = os.path.join(TMP_DIR, f'{name}.png')
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(spec.strip())
    subprocess.run(
        ['npx', '--yes', 'wavedrom-cli', '-i', json_path, '-p', png_path],
        check=True, shell=True, capture_output=True,
    )
    iw, ih = ImageReader(png_path).getSize()
    max_w = max_w_mm * mm
    max_h = max_h_mm * mm
    scale = min(max_w / iw, max_h / ih, 1.0)
    return Image(png_path, width=iw * scale, height=ih * scale)


# ── Document setup ──────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    topMargin=2 * cm, bottomMargin=2 * cm,
    leftMargin=2 * cm, rightMargin=2 * cm,
)

styles = getSampleStyleSheet()
for name in list(styles.byName.keys()):
    s = styles[name]
    if hasattr(s, 'fontName'):
        s.fontName = (s.fontName
                      .replace('Helvetica-BoldOblique', 'Arial-BoldItalic')
                      .replace('Helvetica-Oblique', 'Arial-Italic')
                      .replace('Helvetica-Bold', 'Arial-Bold')
                      .replace('Helvetica', 'Arial'))

styles.add(ParagraphStyle("CourseTitle", parent=styles["Title"], fontSize=14, spaceAfter=4))
styles.add(ParagraphStyle("ExTitle", parent=styles["Heading1"], fontSize=13, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("ExQuestion", parent=styles["Normal"], fontSize=9, spaceAfter=6,
                          textColor=HexColor("#333333"), italic=True))
styles.add(ParagraphStyle("SubHead", parent=styles["Heading2"], fontSize=11, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.5, leading=13))
styles.add(ParagraphStyle("CalcBody", parent=styles["Normal"], fontSize=8.5, leading=11,
                          textColor=HexColor("#444444")))
styles.add(ParagraphStyle("CellStyle", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=TA_CENTER))
styles.add(ParagraphStyle("CellLeft", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=TA_LEFT))
styles.add(ParagraphStyle("CellMono", parent=styles["Normal"], fontName="Consolas", fontSize=8, leading=11, alignment=TA_CENTER))
styles.add(ParagraphStyle("CellMonoLeft", parent=styles["Normal"], fontName="Consolas", fontSize=8, leading=11, alignment=TA_LEFT))
styles.add(ParagraphStyle("CodeBlock", parent=styles["Normal"], fontName="Consolas", fontSize=8.5,
                          leading=11, leftIndent=8, textColor=HexColor("#222222")))

LIGHT_GRAY = HexColor("#F0F0F0")
HEADER_BG = HexColor("#D9E2F3")

story = []


def make_table(headers, rows, col_widths=None, mono_cols=None, left_cols=None):
    mono_cols = mono_cols or set()
    left_cols = left_cols or set()
    hdr = [Paragraph(f"<b>{h}</b>", styles["CellStyle"]) for h in headers]
    data = [hdr]
    for row in rows:
        r = []
        for ci, cell in enumerate(row):
            if ci in mono_cols and ci in left_cols:
                r.append(Paragraph(str(cell), styles["CellMonoLeft"]))
            elif ci in mono_cols:
                r.append(Paragraph(str(cell), styles["CellMono"]))
            elif ci in left_cols:
                r.append(Paragraph(str(cell), styles["CellLeft"]))
            else:
                r.append(Paragraph(str(cell), styles["CellStyle"]))
        data.append(r)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#AAAAAA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Header ──────────────────────────────────────────────────────────────
story.append(Paragraph("Course 62711 — Design of Digital Systems, DTU", styles["CourseTitle"]))
story.append(Paragraph("Assignment 10", styles["Heading2"]))
story.append(Spacer(1, 4))
story.append(Paragraph("Grp 3 — Mads (s246132) &amp; Sigurd (s245534)", styles["Body"]))
story.append(Spacer(1, 2))
story.append(HRFlowable(width="100%", thickness=1, color=black))
story.append(Spacer(1, 6))


# ════════════════════════════════════════════
# 10.1 Timing diagrams
# ════════════════════════════════════════════
story.append(Paragraph("10.1 — Timing Diagrams for Read/Write Sequences", styles["ExTitle"]))
story.append(Paragraph(
    "Draw a timing diagram (Data_In, MW, Address, Data_OutM, Data_OutR, MMR, D_Word, "
    "LD1-8, SW1-8, BTN1-5, output of MUX MR) for each of the four sequences. "
    "Address bus = 8 bits, data bus = 16 bits. MMR = 1 ⇔ Address(7:3) = \"11111\".",
    styles["ExQuestion"],
))


# ── A ──
a_headers = ["Signal", "C1: Read 0x45", "C2: Write 0xAA", "C3: Read 0x45"]
a_rows = [
    ["Address",            "0x45",           "0x45",          "0x45"],
    ["MW",                 "0",              "<b>1</b>",      "0"],
    ["Data_In",            "XXXX",           "0x00AA",        "XXXX"],
    ["Data_OutM",          "0x0000",         "0x0000",        "<b>0x00AA</b>"],
    ["Data_OutR",          "0x0000",         "0x0000",        "0x0000"],
    ["MMR",                "0",              "0",             "0"],
    ["MUX MR out",         "0x0000",         "0x0000",        "<b>0x00AA</b>"],
    ["D_Word",             "0x0000",         "0x0000",        "0x0000"],
    ["LD1-8 / SW1-8",      "0x00 / 0x00",    "0x00 / 0x00",   "0x00 / 0x00"],
    ["BTN1-5",             "00000",          "00000",         "00000"],
]
story.extend([
    Paragraph("A — read 0x45, write 0xAA → 0x45, read 0x45", styles["SubHead"]),
    make_table(a_headers, a_rows,
        col_widths=[95, 100, 100, 100], mono_cols={1, 2, 3}, left_cols={0}),
    Spacer(1, 6),
    render_wavedrom(WAVE_A, 'wave_a', max_h_mm=110),
    Paragraph(
        "<b>Bemærk:</b> 0x45 = 01000101 → bit(7:3) = 01000, så MMR = 0 i hele sekvensen. "
        "MUX MR videresender Data_OutM. Skrivningen i C2 låses ind i RAM på den stigende klokflanke, "
        "og læsningen i C3 returnerer den nyligt skrevne værdi 0x00AA.",
        styles["CalcBody"],
    ),
    Spacer(1, 12),
])


# ── B ──
b_headers = ["Signal", "C1: Write 0x55 → 0xF8", "C2: Read 0xF8"]
b_rows = [
    ["Address",        "0xF8",                   "0xF8"],
    ["MW",             "<b>1</b>",               "0"],
    ["Data_In",        "0x00 55",                "XXXX"],
    ["Data_OutM",      "(unused, RAM idle)",     "(unused)"],
    ["Data_OutR",      "0x0000 (MR0 still old)", "<b>0x0055</b>"],
    ["MMR",            "<b>1</b>",               "<b>1</b>"],
    ["MUX MR out",     "0x0000",                 "<b>0x0055</b>"],
    ["MR0 (internal)", "0x00",                   "<b>0x55</b>"],
    ["D_Word (MR1:MR0)", "0x0000",               "<b>0x0055</b>"],
    ["LD / SW / BTN",  "0x00 / 0x00 / 00000",    "0x00 / 0x00 / 00000"],
]
story.extend([
    Paragraph("B — write 0x55 → 0xF8 (MR0), read 0xF8", styles["SubHead"]),
    make_table(b_headers, b_rows,
        col_widths=[110, 142, 142], mono_cols={1, 2}, left_cols={0}),
    Spacer(1, 6),
    render_wavedrom(WAVE_B, 'wave_b', max_h_mm=110),
    Paragraph(
        "<b>Bemærk:</b> 0xF8 = 11111000 → MMR = 1 i begge cykler. Med MW=1 og Address(2:0) = 000 "
        "låses MR0 ← Data_In(7:0) = 0x55 på den stigende klokflanke. Fra C2 og frem gælder "
        "Data_OutR = 0x00 &amp; MR0 = 0x0055, og MUX MR videresender den fordi MMR=1. "
        "D_Word = MR1 &amp; MR0 = 0x0055, så 7-segment viser \"0055\".",
        styles["CalcBody"],
    ),
    Spacer(1, 12),
])


# ── C ──
c_headers = ["Signal", "C1: Write 0xCC → 0xFC", "C2: Read 0xFC"]
c_rows = [
    ["Address",        "0xFC",                       "0xFC"],
    ["MW",             "<b>1</b>",                   "0"],
    ["Data_In",        "0x00 CC",                    "XXXX"],
    ["Data_OutM",      "(unused)",                   "(unused)"],
    ["Data_OutR",      "<b>0x0000</b> (MR4 = 0x00)", "<b>0x0000</b>"],
    ["MMR",            "<b>1</b>",                   "<b>1</b>"],
    ["MUX MR out",     "0x0000",                     "0x0000"],
    ["MR4 (read-only)", "0x00 (write ignored)",      "0x00"],
    ["D_Word",         "0x0000",                     "0x0000"],
    ["LD / SW / BTN",  "0x00 / 0x00 / 00000",        "0x00 / 0x00 / 00000"],
]
story.extend([
    Paragraph("C — write 0xCC → 0xFC (read-only, ignored), read 0xFC", styles["SubHead"]),
    make_table(c_headers, c_rows,
        col_widths=[115, 145, 134], mono_cols={1, 2}, left_cols={0}),
    Spacer(1, 6),
    render_wavedrom(WAVE_C, 'wave_c', max_h_mm=110),
    Paragraph(
        "<b>Bemærk:</b> Selvom MW=1 og MMR=1, matcher PortReg8x8's case-sætning kun Address(2:0) = "
        "000, 001, 010 (MR0–MR2). Adresse 0xFC har (2:0) = 100, så skrivningen falder ind i "
        "<i>when others =&gt; null</i>, og MR4 beholder sin initielle værdi 0x00.",
        styles["CalcBody"],
    ),
    Spacer(1, 12),
])


# ── D ──
d_headers = ["Signal", "C1: BTNL=1, SW=0xA5", "C2: settle", "C3: Write 0xCC → 0xFC", "C4: Read 0xFC"]
d_rows = [
    ["Address",         "(idle)",      "(idle)",     "0xFC",            "0xFC"],
    ["MW",              "0",           "0",          "<b>1</b>",        "0"],
    ["Data_In",         "—",           "—",          "0x00 CC",         "XXXX"],
    ["SW1-8",           "<b>0xA5</b>", "0xA5",       "0xA5",            "0xA5"],
    ["BTNL",            "<b>1</b>",    "0",          "0",               "0"],
    ["BTN others",      "0000",        "0000",       "0000",            "0000"],
    ["MR4 (internal)",  "<b>0xA5</b> (latched)", "0xA5", "0xA5 (write ignored)", "0xA5"],
    ["Data_OutR",       "—",           "—",          "0x00A5",          "<b>0x00A5</b>"],
    ["MMR",             "(addr-dep.)", "—",          "<b>1</b>",        "<b>1</b>"],
    ["MUX MR out",      "—",           "—",          "0x00A5",          "<b>0x00A5</b>"],
    ["D_Word / LD",     "0x0000 / 0x00", "0x0000 / 0x00", "0x0000 / 0x00", "0x0000 / 0x00"],
]
story.extend([
    Paragraph("D — SW=0xA5 + BTNL latches MR4=0xA5, then repeat C", styles["SubHead"]),
    make_table(d_headers, d_rows,
        col_widths=[78, 100, 60, 110, 80], mono_cols={1, 2, 3, 4}, left_cols={0}),
    Spacer(1, 6),
    render_wavedrom(WAVE_D, 'wave_d', max_h_mm=110),
    Paragraph(
        "<b>Vigtig observation:</b> de read-only-porte er ikke skrivebeskyttede — de er <i>knap-indlæste</i>. "
        "MR4 følger SW mens BTNL holdes nede; når værdien er låst ind, ignoreres efterfølgende skrivninger til 0xFC stadig, "
        "men læsninger returnerer nu den låste værdi (her 0x00A5). Det er præcis sådan PWF tager operander ind.",
        styles["CalcBody"],
    ),
])


# ════════════════════════════════════════════
# 10.2 Calculator program
# ════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("10.2 — Calculator Program (Add Two Operands)", styles["ExTitle"]))
story.append(Paragraph(
    "Operands have been loaded via SW1-8 + BTNU (MR6 / 0xFE) and SW1-8 + BTNL (MR4 / 0xFC). "
    "R6 = 0xFE, R7 = 0xFD, R4 = 0xF8, R5 = 0xF9.",
    styles["ExQuestion"],
))

story.append(Paragraph("A — RTL program for fetch and add", styles["SubHead"]))

prog_headers = ["#", "RTL micro-operation", "PWF assembly", "Hex"]
prog_rows = [
    ["1", "R0 ← M[R6]   (operand 1, MR6 / BTNU)", "ld D0 A6",     "0x2030"],
    ["2", "R1 ← M[R7]   (operand 2, MR5 / BTND)", "ld D1 A7",     "0x2078"],
    ["3", "R2 ← R0 + R1",                          "add D2 A0 B1", "0x040A"],
]
story.append(make_table(prog_headers, prog_rows,
    col_widths=[22, 230, 90, 60], mono_cols={2, 3}, left_cols={1, 2}))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>Bemærkning til R7 = 0xFD vs. BTNL:</b> Opgaveteksten siger \"BTNU og BTNL for første og anden "
    "operand\", men angiver R7 = 0xFD, som svarer til MR5 (BTND), ikke MR4 (BTNL = 0xFC). Vi følger den "
    "eksplicitte adresse (R7 = 0xFD), så den anden operand hentes fra MR5. Byt BTND ↔ BTNL i testbenchen "
    "hvis prosaen skal følges ordret — programlogikken er identisk.",
    styles["CalcBody"],
))

story.append(Paragraph("B — store the result on the seven-segment display", styles["SubHead"]))

prog2_headers = ["#", "RTL micro-operation", "PWF assembly", "Hex"]
prog2_rows = [
    ["4", "M[R4] ← R2   (MR0 ← sum, D_Word low byte)", "st A4 B2", "0x4022"],
    ["5", "M[R5] ← R0   (MR1 high byte; clear with scratch reg if available)", "st A5 B0", "0x4028"],
]
story.append(make_table(prog2_headers, prog2_rows,
    col_widths=[22, 270, 90, 50], mono_cols={2, 3}, left_cols={1, 2}))
story.append(Spacer(1, 6))

story.append(Paragraph("Komplet program:", styles["Body"]))
asm_lines = [
    "; --- 62711 Calculator: R2 = R0 + R1, vises på 7-segment ---",
    "ld  D0 A6     ; R0 &lt;- M[R6] = M[0xFE] = operand 1 (BTNU/MR6)",
    "ld  D1 A7     ; R1 &lt;- M[R7] = M[0xFD] = operand 2 (BTND/MR5)",
    "add D2 A0 B1  ; R2 &lt;- R0 + R1   (8-bit sum, carry på FU C-flag)",
    "st  A4 B2     ; M[R4] = MR0 &lt;- R2  -&gt; D_Word(7:0) = sum",
    "st  A5 B0     ; M[R5] = MR1 &lt;- R0  (høj byte)",
]
for line in asm_lines:
    story.append(Paragraph(line, styles["CodeBlock"]))


# ── Test-bench timeline ──
story.append(Spacer(1, 8))
story.append(Paragraph("Test-bench (VHDL)", styles["SubHead"]))
story.append(Paragraph(
    "Følgende test-bench instantierer Microprocessor-modulet, genererer et klok-signal, "
    "indlæser operanderne via SW + BTNU/BTND, og verificerer at summen kommer ud på D_Word.",
    styles["Body"],
))

tb_vhdl_lines = [
    "library IEEE;",
    "use IEEE.STD_LOGIC_1164.ALL;",
    "",
    "entity Calculator_tb is end Calculator_tb;",
    "",
    "architecture TB of Calculator_tb is",
    "    signal CLK    : STD_LOGIC := '0';",
    "    signal RESET  : STD_LOGIC := '1';",
    "    signal SW     : STD_LOGIC_VECTOR(7 downto 0) := (others =&gt; '0');",
    "    signal BTNC, BTNU, BTNL, BTNR, BTND : STD_LOGIC := '0';",
    "    signal LED    : STD_LOGIC_VECTOR(7 downto 0);",
    "    signal D_Word : STD_LOGIC_VECTOR(15 downto 0);",
    "    constant T : time := 10 ns;   -- klokperiode (100 MHz)",
    "begin",
    "    UUT: entity work.Microprocessor port map (",
    "        CLK=&gt;CLK, RESET=&gt;RESET, SW=&gt;SW,",
    "        BTNC=&gt;BTNC, BTNU=&gt;BTNU, BTNL=&gt;BTNL, BTNR=&gt;BTNR, BTND=&gt;BTND,",
    "        LED=&gt;LED, D_Word=&gt;D_Word);",
    "",
    "    clk_gen: process begin",
    "        CLK &lt;= '0'; wait for T/2;",
    "        CLK &lt;= '1'; wait for T/2;",
    "    end process;",
    "",
    "    stim: process begin",
    "        -- Hold reset i 2 cykler, slip derefter",
    "        RESET &lt;= '1'; wait for 2*T; RESET &lt;= '0';",
    "",
    "        -- Indlæs operand 1 = 0x12 via BTNU  -&gt; MR6 (0xFE)",
    "        SW &lt;= x\"12\"; BTNU &lt;= '1'; wait for T;",
    "        BTNU &lt;= '0';                wait for 2*T;",
    "",
    "        -- Indlæs operand 2 = 0x34 via BTND  -&gt; MR5 (0xFD)",
    "        SW &lt;= x\"34\"; BTND &lt;= '1'; wait for T;",
    "        BTND &lt;= '0';                wait for 2*T;",
    "",
    "        -- Lad CPU'en køre de 5 instruktioner",
    "        wait for 30*T;",
    "",
    "        -- Verificér resultatet på 7-segment",
    "        assert D_Word(7 downto 0) = x\"46\"",
    "            report \"Sum skal være 0x46\" severity error;",
    "",
    "        report \"Calculator_tb: FÆRDIG\" severity note;",
    "        wait;",
    "    end process;",
    "end TB;",
]
for line in tb_vhdl_lines:
    if line:
        story.append(Paragraph(line, styles["CodeBlock"]))
    else:
        story.append(Spacer(1, 3))

story.append(Spacer(1, 8))
story.append(Paragraph("Simulerings-tidslinje", styles["SubHead"]))
story.append(Paragraph(
    "Med operander 0x12 (BTNU) og 0x34 (BTND) er forventet resultat: R2 = 0x46 → MR0 = 0x46 → "
    "D_Word = 0x0046 (eller 0x1246 hvis MR1 ← R0 = 0x12).",
    styles["Body"],
))

tb_headers = ["Fase", "Stimulus", "Observation", "Forventet"]
tb_rows = [
    ["T0", "reset = 1",                        "PC=0x00, alle Rn=0x00, alle MRn=0x00",      "ren tilstand"],
    ["T1", "SW=0x12, BTNU=1 (1 cyklus)",       "MR6 ← 0x12 på stigende klokflanke",          "MR6 = 0x12"],
    ["T2", "SW=0x34, BTND=1 (1 cyklus)",       "MR5 ← 0x34",                                 "MR5 = 0x34"],
    ["T3", "ld D0 A6 udføres",                  "Address=0xFE, MMR=1, MUX MR=0x0012",         "R0 = 0x12"],
    ["T4", "ld D1 A7 udføres",                  "Address=0xFD, MMR=1, MUX MR=0x0034",         "R1 = 0x34"],
    ["T5", "add D2 A0 B1",                     "Funktionsenhed FS=0010, ingen hukommelses-adgang", "R2 = 0x46"],
    ["T6", "st A4 B2",                         "Address=0xF8, MW=1, MMR=1, MR0 ← 0x46",      "D_Word = 0x0046"],
    ["T7", "st A5 B0",                         "Address=0xF9, MW=1, MR1 ← R0",               "D_Word = 0x1246"],
]
story.append(make_table(tb_headers, tb_rows,
    col_widths=[28, 130, 180, 100], mono_cols={0}, left_cols={1, 2, 3}))
story.append(Spacer(1, 8))

story.append(render_wavedrom(WAVE_CALC, 'wave_calc'))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "<b>Sådan læses diagrammet.</b> Operand-indlåsningen (T1, T2) er asynkron i forhold til CPU'en — "
    "et tryk på BTNU/BTND indlæser MRn fra kontakterne uafhængigt af programmet. Hver <code>ld</code> "
    "sender sin adresse på bussen, MMR går høj (Address ≥ 0xF8), og MUX MR ruter den nul-udvidede "
    "port-register-værdi ind i destinationsregisteret. <code>add</code> bruger kun funktionsenheden "
    "(ingen hukommelses-adgang). Hver <code>st</code> hæver MW med data på bussen, og PortReg8x8 låser "
    "den lave byte ind i MR0 / MR1. D_Word følger (MR1:MR0), og 7-segments-driveren klokker den ud.",
    styles["CalcBody"],
))


# ── Build ──
doc.build(story)

# Cleanup tmp dir
shutil.rmtree(TMP_DIR, ignore_errors=True)

print(f"PDF saved to: {OUTPUT}")
