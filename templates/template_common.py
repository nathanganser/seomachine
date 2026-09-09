"""Shared helpers for the Magic Heidi download-template generators.

Styling mirrors the existing Rechnungsvorlage_Schweiz.* files in
mh-landing/public/downloads (Calibri 10 + navy 1F3A5F in Word, Arial 10 +
F2F2F2 header fill + Swiss CHF number format in Excel, Helvetica + footer in PDF).

Run any generator with the seomachine venv:
    venv/bin/python3 templates/<name>_generator.py
"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas as rl_canvas

OUT_DIR = Path("/Users/nathanganser/Documents/Development/mh-landing/public/downloads")

NAVY = "1F3A5F"
GREY = "6B6B6B"
LIGHT = "F2F2F2"
CREAM = "FAFAFA"
INPUT_FILL = "FFF9E6"  # soft yellow for cells the user fills in

FOOTER_TEXT = "Vorlage erstellt mit Magic Heidi  ·  magicheidi.ch  ·  Schweizer Rechnungen in 60 Sekunden"
FOOTER_TEXT_FR = "Modèle créé avec Magic Heidi  ·  magicheidi.ch  ·  Factures suisses en 60 secondes"

CHF_FMT = '[$-807]"CHF "#,##0.00'
NUM_FMT = "[$-807]#,##0.00"
PCT_FMT = "0.0%"
DATE_FMT = "DD.MM.YYYY"
TIME_FMT = "HH:MM"
HOURS_FMT = "0.00"


# --------------------------------------------------------------------------- DOCX
def docx_new(font_size=10):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Mm(20))
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(font_size)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    normal.paragraph_format.space_after = Pt(4)
    return doc


def docx_para(doc, text="", size=10, bold=False, color=None, align=None, space_after=None, italic=False):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
    if align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def docx_runs(doc, runs, size=10, space_after=None):
    """runs = [(text, bold), ...] on one paragraph."""
    p = doc.add_paragraph()
    for text, bold in runs:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    return p


def docx_title(doc, text, size=15):
    return docx_para(doc, text, size=size, bold=True, color=NAVY, space_after=6)


def docx_heading(doc, text, size=12):
    p = docx_para(doc, text, size=size, bold=True, color=NAVY, space_after=3)
    p.paragraph_format.space_before = Pt(8)
    return p


def docx_note(doc, text):
    return docx_para(doc, text, size=9, color=GREY, italic=True)


def _shade(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def _cell_text(cell, text, size=9, bold=False, color=None, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    if align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)


def docx_table(doc, headers, rows, widths_mm, header_fill=NAVY, font_size=9, right_cols=(), borders=True, row_height_mm=None):
    """Bordered table with a shaded header row. rows = list of lists of str."""
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid" if borders else None
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        _cell_text(c, h, size=font_size, bold=True, color="FFFFFF" if header_fill == NAVY else None,
                   align="right" if i in right_cols else None)
        _shade(c, header_fill)
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            _cell_text(t.rows[ri].cells[ci], val, size=font_size, align="right" if ci in right_cols else None)
        if row_height_mm:
            t.rows[ri].height = Mm(row_height_mm)
    _set_widths(t, widths_mm)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def _set_widths(t, widths_mm):
    for ci, w in enumerate(widths_mm):
        t.columns[ci].width = Mm(w)
    for row in t.rows:
        for ci, w in enumerate(widths_mm):
            row.cells[ci].width = Mm(w)


def docx_kv_table(doc, pairs, widths_mm=(45, 120), font_size=10, bold_keys=True):
    """Two-column label/value table without borders."""
    t = doc.add_table(rows=len(pairs), cols=2)
    t.autofit = False
    for i, (k, v) in enumerate(pairs):
        _cell_text(t.rows[i].cells[0], k, size=font_size, bold=bold_keys)
        _cell_text(t.rows[i].cells[1], v, size=font_size)
    _set_widths(t, widths_mm)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def docx_two_blocks(doc, left_lines, right_lines, widths_mm=(90, 80), font_size=10):
    """Side-by-side address blocks (left/right), no borders."""
    t = doc.add_table(rows=1, cols=2)
    t.autofit = False
    for ci, lines in enumerate((left_lines, right_lines)):
        c = t.rows[0].cells[ci]
        c.text = ""
        for li, line in enumerate(lines):
            p = c.paragraphs[0] if li == 0 else c.add_paragraph()
            text, bold = (line if isinstance(line, tuple) else (line, False))
            r = p.add_run(text)
            r.font.size = Pt(font_size)
            r.font.bold = bold
            p.paragraph_format.space_after = Pt(0)
    _set_widths(t, widths_mm)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def docx_footer(doc, text=FOOTER_TEXT):
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.text = ""
    r = p.add_run(text)
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor.from_string(GREY)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def docx_page_break(doc):
    """Page break appended to the last paragraph (avoids an extra paragraph that can spill onto a blank page)."""
    from docx.enum.text import WD_BREAK
    doc.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)


def docx_save(doc, filename, title, subject):
    doc.core_properties.author = "Magic Heidi"
    doc.core_properties.title = title
    doc.core_properties.subject = subject
    path = OUT_DIR / filename
    doc.save(path)
    return path


# --------------------------------------------------------------------------- XLSX
XL_FONT = "Arial"
XL_THIN = Side(style="thin", color="BFBFBF")
XL_BORDER = Border(left=XL_THIN, right=XL_THIN, top=XL_THIN, bottom=XL_THIN)
XL_BOTTOM = Border(bottom=Side(style="thin", color="808080"))


def xl_cell(ws, ref, value=None, bold=False, size=10, fill=None, fmt=None, align=None, border=False, color=None, italic=False, wrap=False):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = Font(name=XL_FONT, size=size, bold=bold, color=color, italic=italic)
    if fill:
        c.fill = PatternFill("solid", fgColor=fill)
    if fmt:
        c.number_format = fmt
    if align or wrap:
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if border:
        c.border = XL_BORDER
    return c


def xl_header_row(ws, row, headers, start_col=1, fill=LIGHT, height=None, wrap=True):
    from openpyxl.utils import get_column_letter
    for i, h in enumerate(headers):
        ref = f"{get_column_letter(start_col + i)}{row}"
        xl_cell(ws, ref, h, bold=True, fill=fill, border=True, align="center", wrap=wrap)
    if height:
        ws.row_dimensions[row].height = height


def xl_widths(ws, widths):
    """widths = {'A': 12, ...}"""
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def xl_print_setup(ws, landscape_mode=False, fit_height=0, print_area=None, title_rows=None):
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = "landscape" if landscape_mode else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = fit_height
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.6
    ws.page_margins.top = ws.page_margins.bottom = 0.7
    if print_area:
        ws.print_area = print_area
    if title_rows:
        ws.print_title_rows = title_rows
    ws.oddFooter.center.text = "Vorlage erstellt mit Magic Heidi · magicheidi.ch"
    ws.oddFooter.center.size = 8


def xl_validation(ws, sqref, options, prompt=None):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    if prompt:
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(sqref)
    return dv


def xl_save(wb, filename, title, subject):
    wb.properties.creator = "Magic Heidi"
    wb.properties.title = title
    wb.properties.subject = subject
    path = OUT_DIR / filename
    wb.save(path)
    return path


# --------------------------------------------------------------------------- PDF
class Pdf:
    """Thin wrapper around a reportlab canvas with mm coordinates measured from the top-left."""

    MM = 72 / 25.4

    def __init__(self, filename, title, subject, landscape_mode=False, footer=FOOTER_TEXT):
        self.path = OUT_DIR / filename
        self.size = landscape(A4) if landscape_mode else A4
        self.c = rl_canvas.Canvas(str(self.path), pagesize=self.size)
        self.c.setAuthor("Magic Heidi")
        self.c.setCreator("Magic Heidi - magicheidi.ch")
        self.c.setTitle(title)
        self.c.setSubject(subject)
        self.w_mm = self.size[0] / self.MM
        self.h_mm = self.size[1] / self.MM
        self.footer_text = footer
        self.margin = 20

    # coordinate helpers -----------------------------------------------------
    def _x(self, x_mm):
        return x_mm * self.MM

    def _y(self, y_mm):
        return self.size[1] - y_mm * self.MM

    # drawing ----------------------------------------------------------------
    def text(self, x, y, s, size=10, bold=False, color=None, align="left"):
        font = "Helvetica-Bold" if bold else "Helvetica"
        self.c.setFont(font, size)
        self.c.setFillColor(HexColor("#" + color) if color else black)
        if align == "right":
            self.c.drawRightString(self._x(x), self._y(y), s)
        elif align == "center":
            self.c.drawCentredString(self._x(x), self._y(y), s)
        else:
            self.c.drawString(self._x(x), self._y(y), s)
        self.c.setFillColor(black)

    def lines(self, x, y, items, size=10, leading=None, bold_first=False):
        """Draw a block of text lines; returns y after the block."""
        lead = leading or size * 0.5
        for i, s in enumerate(items):
            bold = bold_first and i == 0
            self.text(x, y, s, size=size, bold=bold)
            y += lead
        return y

    def rule(self, x1, y1, x2, y2, width=0.5, color=None):
        self.c.setLineWidth(width)
        self.c.setStrokeColor(HexColor("#" + color) if color else black)
        self.c.line(self._x(x1), self._y(y1), self._x(x2), self._y(y2))
        self.c.setStrokeColor(black)

    def rect(self, x, y, w, h, fill=None, stroke=True, width=0.5):
        self.c.setLineWidth(width)
        if fill:
            self.c.setFillColor(HexColor("#" + fill))
        self.c.setStrokeColor(HexColor("#BFBFBF") if stroke else white)
        self.c.rect(self._x(x), self._y(y + h), w * self.MM, h * self.MM, fill=1 if fill else 0, stroke=1 if stroke else 0)
        self.c.setFillColor(black)
        self.c.setStrokeColor(black)

    def field(self, x, y, label, width, size=9):
        """Label followed by an underline for handwriting. Returns x after the field."""
        self.text(x, y, label, size=size)
        lw = self.c.stringWidth(label, "Helvetica", size) / self.MM + 2
        self.rule(x + lw, y + 0.8, x + lw + width, y + 0.8, width=0.4)
        return x + lw + width

    def table(self, x, y, col_widths, headers, n_rows, row_h=8, header_fill=NAVY, size=9, right_cols=(), rows=None, header_h=None):
        """Draw a grid; optional rows = list of lists of strings for pre-filled content. Returns y below table."""
        hh = header_h or row_h
        total_w = sum(col_widths)
        # header
        self.rect(x, y, total_w, hh, fill=header_fill, stroke=True)
        cx = x
        for i, (h, w) in enumerate(zip(headers, col_widths)):
            if i in right_cols:
                self.text(cx + w - 2, y + hh * 0.65, h, size=size, bold=True, color="FFFFFF" if header_fill == NAVY else None, align="right")
            else:
                self.text(cx + 2, y + hh * 0.65, h, size=size, bold=True, color="FFFFFF" if header_fill == NAVY else None)
            cx += w
        y += hh
        for r in range(n_rows):
            self.rect(x, y, total_w, row_h, stroke=True)
            cx = x
            for i, w in enumerate(col_widths):
                if i > 0:
                    self.rule(cx, y, cx, y + row_h, width=0.4, color="BFBFBF")
                if rows and r < len(rows) and i < len(rows[r]) and rows[r][i]:
                    if i in right_cols:
                        self.text(cx + w - 2, y + row_h * 0.65, rows[r][i], size=size, align="right")
                    else:
                        self.text(cx + 2, y + row_h * 0.65, rows[r][i], size=size)
                cx += w
            y += row_h
        return y

    def footer(self):
        self.text(self.w_mm / 2, self.h_mm - 10, self.footer_text, size=8, color=GREY, align="center")

    def new_page(self):
        self.footer()
        self.c.showPage()

    def save(self):
        self.footer()
        self.c.save()
        return self.path
