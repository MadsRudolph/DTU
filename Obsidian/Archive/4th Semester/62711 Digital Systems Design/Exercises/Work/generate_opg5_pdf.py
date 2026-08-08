"""Generate Opg 5 submission PDF for course 62711."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image
)
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Arial for proper Unicode support (combining diacriticals like B̄)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('Consolas-Bold', 'C:/Windows/Fonts/consolab.ttf'))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold',
                   italic='Arial-Italic', boldItalic='Arial-BoldItalic')
registerFontFamily('Consolas', normal='Consolas', bold='Consolas-Bold')

OUTPUT = r"C:\Users\Mads2\DTU\Obsidian\Courses\62711 Digital Systems Design\Exercises\Work\opg5_submission.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    topMargin=2 * cm,
    bottomMargin=2 * cm,
    leftMargin=2 * cm,
    rightMargin=2 * cm,
)

styles = getSampleStyleSheet()
# Override all built-in styles to use Arial
for name in list(styles.byName.keys()):
    s = styles[name]
    if hasattr(s, 'fontName'):
        s.fontName = s.fontName.replace('Helvetica-BoldOblique', 'Arial-BoldItalic') \
                               .replace('Helvetica-Oblique', 'Arial-Italic') \
                               .replace('Helvetica-Bold', 'Arial-Bold') \
                               .replace('Helvetica', 'Arial')

# Custom styles
styles.add(ParagraphStyle(
    "CourseTitle", parent=styles["Title"], fontSize=14, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "ExTitle", parent=styles["Heading1"], fontSize=13, spaceBefore=14, spaceAfter=6,
))
styles.add(ParagraphStyle(
    "ExQuestion", parent=styles["Normal"], fontSize=9, spaceAfter=6,
    textColor=HexColor("#333333"), italic=True,
))
styles.add(ParagraphStyle(
    "SubHead", parent=styles["Heading2"], fontSize=11, spaceBefore=10, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "Body", parent=styles["Normal"], fontSize=9.5, leading=13,
))
styles.add(ParagraphStyle(
    "CalcBody", parent=styles["Normal"], fontSize=8.5, leading=11,
    textColor=HexColor("#444444"),
))
styles.add(ParagraphStyle(
    "CellStyle", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    "CellLeft", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    "CellMono", parent=styles["Normal"], fontName="Consolas", fontSize=8, leading=11, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    "CellMonoLeft", parent=styles["Normal"], fontName="Consolas", fontSize=8, leading=11, alignment=TA_LEFT,
))

LIGHT_GRAY = HexColor("#F0F0F0")
HEADER_BG = HexColor("#D9E2F3")

story = []

# ── Header ──
story.append(Paragraph("Course 62711 — Design of Digital Systems, DTU", styles["CourseTitle"]))
story.append(Paragraph("Assignment Lecture 5", styles["Heading2"]))
story.append(Spacer(1, 4))
story.append(Paragraph("Grp 3 — Mads (s246132) &amp; Sigurd (s245534)", styles["Body"]))
story.append(Spacer(1, 2))
story.append(HRFlowable(width="100%", thickness=1, color=black))
story.append(Spacer(1, 6))


# ── Helper to build a nice table ──
def make_table(headers, rows, col_widths=None, mono_cols=None):
    """Build a formatted Table flowable."""
    mono_cols = mono_cols or set()
    # header row
    hdr = [Paragraph(f"<b>{h}</b>", styles["CellStyle"]) for h in headers]
    data = [hdr]
    for row in rows:
        r = []
        for ci, cell in enumerate(row):
            if ci in mono_cols:
                r.append(Paragraph(str(cell), styles["CellMono"]))
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
    # Alternate row shading
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
    t.setStyle(TableStyle(style_cmds))
    return t


# ════════════════════════════════════════════
# 5.1
# ════════════════════════════════════════════
story.append(Paragraph("5.1 — Micro-operation Control Word Tables", styles["ExTitle"]))
story.append(Paragraph(
    "Complete the table symbolically and in binary for each RTL micro-operation. "
    "The control word consists of 16 bits: DA(3), AA(3), BA(3), MB(1), FS(4), MD(1), RW(1).",
    styles["ExQuestion"],
))

# Symbolic
story.append(Paragraph("Symbolic Table", styles["SubHead"]))
sym_headers = ["Micro-operation", "DA", "AA", "BA", "MB", "FS", "MD", "RW"]
sym_rows = [
    ["R1 \u2190 R2 \u2212 R3",   "R1",   "R2",   "R3",   "Register", "F = A + B\u0304 + 1", "Function", "Write"],
    ["R4 \u2190 sl R6",           "R4",   "\u2014","R6",   "Register", "F = sl B",            "Function", "Write"],
    ["R7 \u2190 R7 + 1",         "R7",   "R7",   "\u2014","\u2014",   "F = A + 1",           "Function", "Write"],
    ["R1 \u2190 R0 + 2",         "R1",   "R0",   "\u2014","Constant", "F = A + B",           "Function", "Write"],
    ["Data out \u2190 R3",        "\u2014","\u2014","R3",  "Register", "\u2014",              "\u2014",   "No Write"],
    ["R4 \u2190 Data in",         "R4",   "\u2014","\u2014","\u2014",  "\u2014",              "Data in",  "Write"],
    ["R5 \u2190 0",               "R5",   "R[X]", "R[X]", "Register", "F = A + B\u0304 + 1", "Function", "Write"],
]
story.append(make_table(sym_headers, sym_rows,
    col_widths=[85, 28, 28, 28, 48, 72, 48, 40]))
story.append(Spacer(1, 8))

# Binary
story.append(Paragraph("Binary Table", styles["SubHead"]))
bin_headers = ["Micro-operation", "DA", "AA", "BA", "MB", "FS", "MD", "RW"]
bin_rows = [
    ["R1 \u2190 R2 \u2212 R3", "001", "010", "011", "0", "0101", "0", "1"],
    ["R4 \u2190 sl R6",         "100", "XXX", "110", "0", "1110", "0", "1"],
    ["R7 \u2190 R7 + 1",       "111", "111", "XXX", "X", "0001", "0", "1"],
    ["R1 \u2190 R0 + 2",       "001", "000", "XXX", "1", "0010", "0", "1"],
    ["Data out \u2190 R3",      "XXX", "XXX", "011", "0", "XXXX", "X", "0"],
    ["R4 \u2190 Data in",       "100", "XXX", "XXX", "X", "XXXX", "1", "1"],
    ["R5 \u2190 0",             "101", "XYZ", "XYZ", "0", "0101", "0", "1"],
]
story.append(make_table(bin_headers, bin_rows,
    col_widths=[85, 28, 28, 28, 28, 38, 28, 28], mono_cols={1,2,3,4,5,6,7}))
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Noter:</b>", styles["CalcBody"]))
notes_51 = [
    "<b>R4 \u2190 sl R6:</b> Shift-left opererer p\u00e5 B-input. AA er don\u2019t-care.",
    "<b>R7 \u2190 R7 + 1:</b> Increment bruger kun A (FS=0001). BA og MB er don\u2019t-care.",
    "<b>R1 \u2190 R0 + 2:</b> Konstanten 2 via Constant_In (MB=1). BA er don\u2019t-care.",
    "<b>Data out \u2190 R3:</b> Drevet af MUX B output. Ingen registerskrivning (RW=0). Alle andre felter er don\u2019t-care.",
    "<b>R4 \u2190 Data in:</b> MD=1 sender Data_In til registeret. FS/MB/AA/BA er alle don\u2019t-care.",
    "<b>R5 \u2190 0:</b> R[X] \u2212 R[X] = 0. AA=BA=samme register (XYZ). Alternativ: XOR (FS=1010) med AA=BA.",
]
for n in notes_51:
    story.append(Paragraph(n, styles["CalcBody"]))


# ════════════════════════════════════════════
# 5.2
# ════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("5.2 — Specify 16-bit Control Words", styles["ExTitle"]))
story.append(Paragraph(
    "Give the 16-bit control word for each micro-operation. Format: DA(3) AA(3) BA(3) MB(1) FS(4) MD(1) RW(1).",
    styles["ExQuestion"],
))

cw_headers = ["", "Micro-operation", "Control Word"]
cw_rows = [
    ["a)", "R5 \u2190 0",                   "101 XYZ XYZ 0 0101 0 1"],
    ["b)", "R4 \u2190 sl R5",               "100 XXX 101 0 1110 0 1"],
    ["c)", "R7 \u2190 Data_In",             "111 XXX XXX X XXXX 1 1"],
    ["d)", "R3 \u2190 sr R3",               "011 XXX 011 0 1101 0 1"],
    ["e)", "R1 \u2190 R3 \u2212 Constant_In","001 011 XXX 1 0101 0 1"],
    ["f)", "R1 \u2190 R1 + 1",              "001 001 XXX X 0001 0 1"],
    ["g)", "R2 \u2190 R1 xor R3",           "010 001 011 0 1010 0 1"],
    ["h)", "R4 \u2190 R3 + R5",             "100 011 101 0 0010 0 1"],
]
story.append(make_table(cw_headers, cw_rows,
    col_widths=[22, 130, 160], mono_cols={2}))
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Noter:</b>", styles["CalcBody"]))
notes_52 = [
    "<b>a)</b> R5 \u2190 R[X] \u2212 R[X] = 0. AA=BA=samme register. FS=0101 (subtraktion).",
    "<b>b)</b> sl R5: BA=101, FS=1110. AA er don\u2019t-care.",
    "<b>c)</b> MD=1 v\u00e6lger Data_In. Alt andet er don\u2019t-care. RW=1.",
    "<b>d)</b> sr R3: BA=011, FS=1101. Resultat gemmes i DA=R3.",
    "<b>e)</b> FS=0101 (subtraktion). AA=R3, MB=1 v\u00e6lger Constant_In.",
    "<b>f)</b> FS=0001 (increment). AA=R1. BA/MB er don\u2019t-care.",
    "<b>g)</b> FS=1010 (XOR). AA=R1, BA=R3, MB=0.",
    "<b>h)</b> FS=0010 (addition). AA=R3, BA=R5, MB=0.",
]
for n in notes_52:
    story.append(Paragraph(n, styles["CalcBody"]))


# ════════════════════════════════════════════
# 5.3
# ════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("5.3 — Decode Control Words to Micro-operations", styles["ExTitle"]))
story.append(Paragraph(
    "Given 16-bit control words, determine the micro-operation and the register change. "
    "Initial: Rn = n, Constant = 0x06, Data_in = 0x1B.",
    styles["ExQuestion"],
))

dc_headers = ["", "Control Word", "Micro-operation", "Register Change"]
dc_rows = [
    ["a)", "101 100 101 0 1000 0 1", "F \u2190 A or B",             "R5 \u2190 R4 or R5 = 0x05"],
    ["b)", "110 010 100 0 0101 0 1", "F \u2190 A + B\u0304 + 1",    "R6 \u2190 R2 \u2212 R4 = 0xFE"],
    ["c)", "101 110 000 0 1100 0 1", "F \u2190 B",                   "R5 \u2190 R0 = 0x00"],
    ["d)", "101 000 000 0 0000 0 1", "F \u2190 A",                   "R5 \u2190 R0 = 0x00"],
    ["e)", "100 100 000 1 1101 0 1", "F \u2190 sr B",                "R4 \u2190 sr(Constant) = 0x03"],
    ["f)", "011 000 000 0 0000 1 1", "R[DA] \u2190 Data_In",         "R3 \u2190 0x1B"],
]
story.append(make_table(dc_headers, dc_rows,
    col_widths=[22, 130, 110, 140], mono_cols={1}))
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Beregninger:</b>", styles["CalcBody"]))
calcs_53 = [
    "<b>a)</b> R4 OR R5 = 0x04 OR 0x05 = 00000100 OR 00000101 = 00000101 = 0x05 (ingen effektiv \u00e6ndring).",
    "<b>b)</b> R2 \u2212 R4 = 0x02 \u2212 0x04 = 0x02 + NOT(0x04) + 1 = 0x02 + 0xFB + 1 = 0xFE (= \u22122 fortegnet).",
    "<b>c)</b> FS=1100 = MOVB (F = B). B = R0 = 0x00.",
    "<b>d)</b> FS=0000 = MOVA (F = A). A = R0 = 0x00.",
    "<b>e)</b> MB=1 s\u00e5 B = Constant = 0x06 = 00000110. sr(0x06) = 00000011 = 0x03.",
    "<b>f)</b> MD=1 omg\u00e5r funktionsenheden. R3 \u2190 Data_In = 0x1B.",
]
for c in calcs_53:
    story.append(Paragraph(c, styles["CalcBody"]))


# ════════════════════════════════════════════
# 5.4
# ════════════════════════════════════════════
story.append(Paragraph("5.4 — Program Counter Timing Diagram", styles["ExTitle"]))
story.append(Paragraph(
    "A) Find PC values for each clock cycle. Initial PC = 0x45.  "
    "B) Specify the RTL operation for each cycle.",
    styles["ExQuestion"],
))

# Embed timing diagram image if it exists
TIMING_IMG = r"C:\Users\Mads2\DTU\Obsidian\Courses\62711 Digital Systems Design\Images\timing_diagram_5_4.png"
if os.path.exists(TIMING_IMG):
    # Scale to fit page width (available width = A4 - margins = 210 - 40 = 170mm)
    from reportlab.lib.utils import ImageReader
    img_reader = ImageReader(TIMING_IMG)
    iw, ih = img_reader.getSize()
    max_w = 170 * mm
    scale = min(max_w / iw, 1.0)  # don't upscale
    story.append(Image(TIMING_IMG, width=iw * scale, height=ih * scale))
    story.append(Spacer(1, 8))

pc_headers = ["Cycle", "PS", "Offset", "Addr_In", "RTL Operation", "PC"]
pc_rows = [
    ["\u2014",  "\u2014", "\u2014",  "\u2014",  "Initial value",         "<b>0x45</b>"],
    ["1",  "00", "0xF1", "0xXX", "PC \u2190 PC",               "<b>0x45</b>"],
    ["2",  "00", "0xF1", "0xXX", "PC \u2190 PC",               "<b>0x45</b>"],
    ["3",  "01", "0x7",  "0x55", "PC \u2190 PC + 1",           "<b>0x46</b>"],
    ["4",  "01", "0x7",  "0x55", "PC \u2190 PC + 1",           "<b>0x47</b>"],
    ["5",  "01", "0x7",  "0x55", "PC \u2190 PC + 1",           "<b>0x48</b>"],
    ["6",  "01", "0x7",  "0x01", "PC \u2190 PC + 1",           "<b>0x49</b>"],
    ["7",  "10", "0xE8", "0x01", "PC \u2190 PC + Offset",      "<b>0x31</b>"],
    ["8",  "10", "0xE8", "0x01", "PC \u2190 PC + Offset",      "<b>0x19</b>"],
    ["9",  "01", "0xE8", "0xF1", "PC \u2190 PC + 1",           "<b>0x1A</b>"],
    ["10", "11", "0xE8", "0xF1", "PC \u2190 Addr_In",          "<b>0xF1</b>"],
]
story.append(make_table(pc_headers, pc_rows,
    col_widths=[32, 28, 42, 45, 110, 50]))
story.append(Spacer(1, 4))


# ════════════════════════════════════════════
# 5.5
# ════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("5.5 — Zero-Filler and Sign-Extender Outputs", styles["ExTitle"]))
story.append(Paragraph(
    "For each 16-bit instruction, find the Zero-filler and Sign-extender outputs. "
    "ZF = \"00000\" &amp; IR(2:0).  "
    "SE = \"000\"/\"111\" &amp; IR(7:6) &amp; IR(2:0) depending on IR(8).",
    styles["ExQuestion"],
))

zf_headers = ["", "Instruction (IR)", "IR(8)", "IR(7:6)", "IR(2:0)", "Zero-Filler", "Sign-Extender"]
zf_rows = [
    ["a)", "1011001010100001", "0", "10", "001", "<b>00000001</b>", "<b>00010001</b>"],
    ["b)", "1100101000010101", "0", "00", "101", "<b>00000101</b>", "<b>00000101</b>"],
    ["c)", "1011100100110001", "1", "00", "001", "<b>00000001</b>", "<b>11100001</b>"],
    ["d)", "1010000000000001", "0", "00", "001", "<b>00000001</b>", "<b>00000001</b>"],
    ["e)", "1001000101110101", "1", "01", "101", "<b>00000101</b>", "<b>11101101</b>"],
    ["f)", "0110000100000011", "1", "00", "011", "<b>00000011</b>", "<b>11100011</b>"],
]
story.append(make_table(zf_headers, zf_rows,
    col_widths=[22, 105, 32, 38, 38, 62, 68], mono_cols={1,2,3,4,5,6}))
story.append(Spacer(1, 4))

story.append(Paragraph("<b>Beregninger:</b>", styles["CalcBody"]))
story.append(Paragraph("Bit-indeksering: position 15 (MSB, yderst til venstre) ned til 0 (LSB, yderst til h\u00f8jre).", styles["CalcBody"]))
calcs_55 = [
    "<b>a)</b> IR(8)=0, IR(7:6)=10, IR(2:0)=001. ZF = 00000_001 = 0x01. SE = 000_10_001 = 0x11.",
    "<b>b)</b> IR(8)=0, IR(7:6)=00, IR(2:0)=101. ZF = 00000_101 = 0x05. SE = 000_00_101 = 0x05.",
    "<b>c)</b> IR(8)=1, IR(7:6)=00, IR(2:0)=001. ZF = 00000_001 = 0x01. SE = 111_00_001 = 0xE1.",
    "<b>d)</b> IR(8)=0, IR(7:6)=00, IR(2:0)=001. ZF = 00000_001 = 0x01. SE = 000_00_001 = 0x01.",
    "<b>e)</b> IR(8)=1, IR(7:6)=01, IR(2:0)=101. ZF = 00000_101 = 0x05. SE = 111_01_101 = 0xED.",
    "<b>f)</b> IR(8)=1, IR(7:6)=00, IR(2:0)=011. ZF = 00000_011 = 0x03. SE = 111_00_011 = 0xE3.",
]
for c in calcs_55:
    story.append(Paragraph(c, styles["CalcBody"]))


# ── Build ──
doc.build(story)
print(f"PDF saved to: {OUTPUT}")
