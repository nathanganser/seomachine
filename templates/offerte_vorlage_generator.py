#!/usr/bin/env python3
"""Generate the Swiss Offerte / Devis / Kostenvoranschlag download templates.

Outputs (default: ../mh-landing/public/downloads/):
  Offerte_Vorlage_Schweiz.docx / .xlsx / .pdf      (German, binding offer)
  Devis_Modele_Suisse.docx / .xlsx / .pdf          (French, binding offer)
  Kostenvoranschlag_Schweiz.docx / .pdf            (German, non-binding estimate)
  Devis_estimatif_Suisse.docx / .pdf               (French, non-binding estimate)

Usage:
  venv/bin/python3 templates/offerte_vorlage_generator.py [--out DIR] [--no-validate]

Every file is re-opened after writing (python-docx / openpyxl / pypdf) and
checked for umlauts + formulas so a broken build fails loudly.
"""
import argparse
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "mh-landing", "public", "downloads"
)

ACCENT = "1F3A5F"      # dark blue header text
ACCENT_LIGHT = "E8EEF5"  # light fill for table headers
GREY = "6B7280"

# ---------------------------------------------------------------------------
# Document specifications (all copy lives here so DOCX/XLSX/PDF stay in sync)
# ---------------------------------------------------------------------------

EXAMPLE_ROWS_DE = [
    ("1", "[Leistung 1, z. B. Konzept und Beratung]", 8, "Std.", 140.00),
    ("2", "[Leistung 2, z. B. Umsetzung gemäss Beschrieb]", 1, "Pauschal", 2500.00),
    ("3", "[Material / Fremdleistungen]", 10, "Stk.", 35.00),
    ("4", "[ ]", None, "", None),
    ("5", "[ ]", None, "", None),
]
EXAMPLE_ROWS_FR = [
    ("1", "[Prestation 1, p. ex. concept et conseil]", 8, "h", 140.00),
    ("2", "[Prestation 2, p. ex. réalisation selon descriptif]", 1, "forfait", 2500.00),
    ("3", "[Matériel / prestations externes]", 10, "pce", 35.00),
    ("4", "[ ]", None, "", None),
    ("5", "[ ]", None, "", None),
]

OFFERTE_DE = dict(
    kind="offer",
    lang="de",
    file_stem="Offerte_Vorlage_Schweiz",
    doc_title="OFFERTE",
    doc_subtitle=None,
    sender_heading="Absender",
    sender_lines=[
        "[Firmenname / Name]",
        "[Strasse Nr.]",
        "[PLZ Ort]",
        "[Telefon] · [E-Mail]",
        "UID: CHE-XXX.XXX.XXX MWST",
    ],
    recipient_heading="Empfänger",
    recipient_lines=["[Kunde / Firma]", "[Ansprechperson]", "[Strasse Nr.]", "[PLZ Ort]"],
    meta=[
        ("Offerten-Nr.", "2026-001"),
        ("Datum", "[TT.MM.JJJJ]"),
        ("Gültig bis", "[TT.MM.JJJJ] (30 Tage ab Datum)"),
        ("Ansprechperson", "[Name, Telefon]"),
    ],
    subject="Offerte für [Projekt / Leistung]",
    intro="Vielen Dank für Ihre Anfrage. Gerne unterbreiten wir Ihnen folgende Offerte:",
    assumptions_heading=None,
    assumptions=[],
    columns=["Pos.", "Beschreibung", "Menge", "Einheit", "Einzelpreis CHF", "Total CHF"],
    rows=EXAMPLE_ROWS_DE,
    subtotal_label="Zwischentotal exkl. MWST",
    vat_label="MWST 8.1 %",
    total_label="Total CHF inkl. MWST",
    cap_line=None,
    vat_note="Nicht MWST-pflichtig? MWST-Zeile weglassen, UID-Zeile leer lassen und ergänzen: "
             "«Keine MWST, da nicht MWST-pflichtig (Art. 10 MWSTG).»",
    conditions_heading="Bedingungen",
    conditions=[
        ("Zahlungsbedingungen", "[30 Tage netto] oder [50 % Akonto bei Auftragserteilung, 50 % nach Abnahme]"),
        ("Lieferfrist / Ausführung", "[z. B. innert 4 Wochen nach Auftragserteilung]"),
        ("Nicht enthalten", "[Zusatzleistungen werden nach Aufwand zu CHF [Satz]/Std. verrechnet]"),
        ("Gültigkeit", "Diese Offerte ist gültig bis [Datum]. Danach behalten wir uns Preisanpassungen vor."),
    ],
    legal_note="Hinweis: Mit der Annahme dieser Offerte kommt ein verbindlicher Vertrag über die "
               "beschriebenen Leistungen zum genannten Preis zustande.",
    closing="Mit freundlichen Grüssen",
    closing_lines=["[Name, Funktion]", "[Ort, Datum]"],
    acceptance_heading="Annahme der Offerte",
    acceptance_lines=[
        "Offerte angenommen am: ______________________",
        "Ort: ______________________",
        "Unterschrift Auftraggeber: ______________________________________",
    ],
    footer="Vorlage von magicheidi.ch – Offerten in einer Minute erstellen und per Klick in QR-Rechnungen umwandeln.",
    # XLSX-only labels
    xl_sheet="Offerte",
    xl_sender=["Firma / Name", "Adresse (Strasse, Nr.)", "PLZ / Ort", "Telefon", "E-Mail", "UID / MWST-Nr."],
    xl_recipient=["Firma / Name", "Ansprechperson", "Adresse", "PLZ / Ort"],
    xl_title_formula='="Offerte Nr. "&F1',
    xl_subject_label="Betreff",
    xl_vat_rate_label="MWST-Satz",
    xl_vat_amount_label="MWST-Betrag",
    xl_vat_hint="MWST-Satz: 8.1 % Normalsatz, 2.6 % reduziert, 3.8 % Beherbergung. "
                "Nicht MWST-pflichtig? 0 % wählen und UID-Zeile leer lassen (Art. 10 MWSTG).",
)

DEVIS_FR = dict(
    kind="offer",
    lang="fr",
    file_stem="Devis_Modele_Suisse",
    doc_title="DEVIS",
    doc_subtitle=None,
    sender_heading="Expéditeur",
    sender_lines=[
        "[Raison sociale / Nom]",
        "[Rue n°]",
        "[NPA Localité]",
        "[Téléphone] · [E-mail]",
        "IDE : CHE-XXX.XXX.XXX TVA",
    ],
    recipient_heading="Destinataire",
    recipient_lines=["[Client / Entreprise]", "[Personne de contact]", "[Rue n°]", "[NPA Localité]"],
    meta=[
        ("N° de devis", "2026-001"),
        ("Date", "[JJ.MM.AAAA]"),
        ("Valable jusqu'au", "[JJ.MM.AAAA] (30 jours dès la date)"),
        ("Contact", "[Nom, téléphone]"),
    ],
    subject="Devis pour [projet / prestation]",
    intro="Nous vous remercions de votre demande et avons le plaisir de vous soumettre le devis suivant :",
    assumptions_heading=None,
    assumptions=[],
    columns=["Pos.", "Désignation", "Quantité", "Unité", "Prix unitaire CHF", "Total CHF"],
    rows=EXAMPLE_ROWS_FR,
    subtotal_label="Sous-total hors TVA",
    vat_label="TVA 8.1 %",
    total_label="Total CHF TTC",
    cap_line=None,
    vat_note="Pas assujetti à la TVA ? Supprimez la ligne TVA, laissez la ligne IDE vide et ajoutez : "
             "« Sans TVA, non assujetti (art. 10 LTVA). »",
    conditions_heading="Conditions",
    conditions=[
        ("Conditions de paiement", "[30 jours net] ou [50 % d'acompte à la commande, 50 % à la réception]"),
        ("Délai d'exécution / livraison", "[p. ex. dans les 4 semaines suivant la commande]"),
        ("Non compris", "[Les prestations supplémentaires sont facturées en régie à CHF [taux]/h]"),
        ("Validité", "Ce devis est valable jusqu'au [date]. Passé ce délai, nous nous réservons le droit d'adapter les prix."),
    ],
    legal_note="Remarque : l'acceptation de ce devis vaut conclusion d'un contrat portant sur les "
               "prestations décrites au prix indiqué.",
    closing="Meilleures salutations",
    closing_lines=["[Nom, fonction]", "[Lieu, date]"],
    acceptance_heading="Acceptation du devis",
    acceptance_lines=[
        "Devis accepté le : ______________________",
        "Lieu : ______________________",
        "Signature du client : ______________________________________",
    ],
    footer="Modèle de magicheidi.ch – créez vos devis en une minute et convertissez-les en factures QR en un clic.",
    xl_sheet="Devis",
    xl_sender=["Raison sociale / Nom", "Adresse (rue, n°)", "NPA / Localité", "Téléphone", "E-mail", "IDE / N° TVA"],
    xl_recipient=["Raison sociale / Nom", "Personne de contact", "Adresse", "NPA / Localité"],
    xl_title_formula='="Devis n° "&F1',
    xl_subject_label="Objet",
    xl_vat_rate_label="Taux de TVA",
    xl_vat_amount_label="Montant TVA",
    xl_vat_hint="Taux de TVA : 8.1 % normal, 2.6 % réduit, 3.8 % hébergement. "
                "Pas assujetti ? Choisissez 0 % et laissez la ligne IDE vide (art. 10 LTVA).",
)

KVA_DE = dict(
    kind="estimate",
    lang="de",
    file_stem="Kostenvoranschlag_Schweiz",
    doc_title="KOSTENVORANSCHLAG",
    doc_subtitle="unverbindlich",
    sender_heading="Absender",
    sender_lines=OFFERTE_DE["sender_lines"],
    recipient_heading="Empfänger",
    recipient_lines=OFFERTE_DE["recipient_lines"],
    meta=[
        ("Kostenvoranschlag-Nr.", "KV-2026-001"),
        ("Datum", "[TT.MM.JJJJ]"),
        ("Gültig bis", "[TT.MM.JJJJ] (30 Tage ab Datum)"),
        ("Ansprechperson", "[Name, Telefon]"),
    ],
    subject="Kostenvoranschlag für [Projekt / Leistung]",
    intro="Gerne schätzen wir die voraussichtlichen Kosten für die unten beschriebene Leistung wie folgt:",
    assumptions_heading="Grundlagen und Annahmen",
    assumptions=[
        "[Annahme 1, z. B. Zugang zum Objekt vorhanden, Arbeiten während Bürozeiten]",
        "[Annahme 2, z. B. Materialpreise Stand Datum des Kostenvoranschlags]",
        "[Nicht enthalten: z. B. Entsorgung, Bewilligungen, Zusatzwünsche]",
    ],
    columns=["Pos.", "Beschreibung", "Menge (ca.)", "Einheit", "Einzelpreis CHF", "Total CHF (ca.)"],
    rows=EXAMPLE_ROWS_DE,
    subtotal_label="Zwischentotal (ca.) exkl. MWST",
    vat_label="MWST 8.1 %",
    total_label="Voraussichtliches Total CHF",
    cap_line="Kostendach (optional): Ohne Ihre vorherige Zustimmung wird der Betrag von CHF [Betrag] nicht überschritten.",
    vat_note=OFFERTE_DE["vat_note"],
    conditions_heading="Bedingungen",
    conditions=[
        ("Verbindlichkeit", "Dieser Kostenvoranschlag ist unverbindlich. Die Preise beruhen auf dem aktuell bekannten "
                            "Aufwand und können je nach tatsächlichem Material- und Zeitbedarf abweichen. Zeichnen sich "
                            "Mehrkosten ab, informieren wir Sie vor der Ausführung."),
        ("Abrechnung", "[nach effektivem Aufwand zu CHF [Satz]/Std.] oder [Pauschale gemäss separater Offerte]"),
        ("Zahlungsbedingungen", "[30 Tage netto nach Rechnungsstellung]"),
        ("Gültigkeit", "Diese Schätzung gilt bis [Datum]. Danach kann sie aktualisiert werden."),
    ],
    legal_note="Hinweis: Ein Kostenvoranschlag ist eine Schätzung, keine verbindliche Offerte. Für ein festes "
               "Angebot mit Fixpreis erstellen wir Ihnen auf Wunsch eine Offerte.",
    closing="Mit freundlichen Grüssen",
    closing_lines=["[Name, Funktion]", "[Ort, Datum]"],
    acceptance_heading="Freigabe zur Ausführung",
    acceptance_lines=[
        "Freigegeben am: ______________________",
        "Ort: ______________________",
        "Unterschrift Auftraggeber: ______________________________________",
    ],
    footer=OFFERTE_DE["footer"],
)

KVA_FR = dict(
    kind="estimate",
    lang="fr",
    file_stem="Devis_estimatif_Suisse",
    doc_title="DEVIS ESTIMATIF",
    doc_subtitle="sans engagement",
    sender_heading="Expéditeur",
    sender_lines=DEVIS_FR["sender_lines"],
    recipient_heading="Destinataire",
    recipient_lines=DEVIS_FR["recipient_lines"],
    meta=[
        ("N° d'estimation", "EST-2026-001"),
        ("Date", "[JJ.MM.AAAA]"),
        ("Valable jusqu'au", "[JJ.MM.AAAA] (30 jours dès la date)"),
        ("Contact", "[Nom, téléphone]"),
    ],
    subject="Estimation des coûts pour [projet / prestation]",
    intro="Nous estimons les coûts prévisibles de la prestation décrite ci-dessous comme suit :",
    assumptions_heading="Bases et hypothèses",
    assumptions=[
        "[Hypothèse 1, p. ex. accès au site garanti, travaux pendant les heures de bureau]",
        "[Hypothèse 2, p. ex. prix des matériaux à la date de l'estimation]",
        "[Non compris : p. ex. élimination, autorisations, demandes supplémentaires]",
    ],
    columns=["Pos.", "Désignation", "Quantité (env.)", "Unité", "Prix unitaire CHF", "Total CHF (env.)"],
    rows=EXAMPLE_ROWS_FR,
    subtotal_label="Sous-total (env.) hors TVA",
    vat_label="TVA 8.1 %",
    total_label="Total prévisible CHF",
    cap_line="Plafond de coûts (optionnel) : sans votre accord préalable, le montant de CHF [montant] ne sera pas dépassé.",
    vat_note=DEVIS_FR["vat_note"],
    conditions_heading="Conditions",
    conditions=[
        ("Engagement", "Ce devis estimatif est donné sans engagement. Les prix reposent sur l'ampleur des travaux "
                       "connue à ce jour et peuvent varier selon le matériel et le temps effectivement nécessaires. "
                       "Si des coûts supplémentaires se dessinent, nous vous en informons avant l'exécution."),
        ("Facturation", "[en régie à CHF [taux]/h] ou [forfait selon devis séparé]"),
        ("Conditions de paiement", "[30 jours net dès facturation]"),
        ("Validité", "Cette estimation est valable jusqu'au [date]. Elle peut ensuite être actualisée."),
    ],
    legal_note="Remarque : une estimation n'est pas un devis ferme. Pour une offre à prix fixe, nous vous "
               "établissons volontiers un devis contraignant.",
    closing="Meilleures salutations",
    closing_lines=["[Nom, fonction]", "[Lieu, date]"],
    acceptance_heading="Bon pour exécution",
    acceptance_lines=[
        "Approuvé le : ______________________",
        "Lieu : ______________________",
        "Signature du client : ______________________________________",
    ],
    footer=DEVIS_FR["footer"],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def chf(value):
    """Swiss number formatting: 1'234.50"""
    if value is None:
        return ""
    s = f"{value:,.2f}"
    return s.replace(",", "'")


def compute_totals(rows):
    subtotal = sum((r[2] or 0) * (r[4] or 0) for r in rows)
    vat = round(subtotal * 0.081, 2)
    return subtotal, vat, round(subtotal + vat, 2)


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

def _docx_shade(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def _docx_no_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tbl_pr.append(borders)


def _docx_par(doc_or_cell, text="", size=10, bold=False, color=None, align=None, space_after=2, italic=False):
    p = doc_or_cell.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    if align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p


def _docx_set_widths(table, widths_cm):
    for row in table.rows:
        for idx, w in enumerate(widths_cm):
            row.cells[idx].width = Cm(w)


def build_docx(spec, out_path):
    doc = Document()
    section = doc.sections[0]
    section.page_height, section.page_width = Cm(29.7), Cm(21.0)
    section.left_margin = section.right_margin = Cm(2.0)
    section.top_margin, section.bottom_margin = Cm(1.8), Cm(1.5)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)

    # Header: sender (left) / recipient (right)
    hdr = doc.add_table(rows=1, cols=2)
    _docx_no_borders(hdr)
    left, right = hdr.rows[0].cells
    left.paragraphs[0].text = ""
    _docx_par(left, spec["sender_heading"].upper(), size=8, bold=True, color=GREY)
    for line in spec["sender_lines"]:
        _docx_par(left, line, size=10, space_after=0)
    right.paragraphs[0].text = ""
    _docx_par(right, spec["recipient_heading"].upper(), size=8, bold=True, color=GREY)
    for line in spec["recipient_lines"]:
        _docx_par(right, line, size=10, space_after=0)
    _docx_set_widths(hdr, [8.5, 8.5])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Title
    title = spec["doc_title"] + (f"  ({spec['doc_subtitle']})" if spec["doc_subtitle"] else "")
    _docx_par(doc, title, size=20, bold=True, color=ACCENT, space_after=4)

    # Meta block
    meta = doc.add_table(rows=len(spec["meta"]), cols=2)
    _docx_no_borders(meta)
    for i, (k, v) in enumerate(spec["meta"]):
        meta.rows[i].cells[0].paragraphs[0].text = ""
        meta.rows[i].cells[1].paragraphs[0].text = ""
        _docx_par(meta.rows[i].cells[0], k, size=10, bold=True, space_after=0)
        _docx_par(meta.rows[i].cells[1], v, size=10, space_after=0)
    _docx_set_widths(meta, [5.0, 12.0])

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    _docx_par(doc, spec["subject"], size=11, bold=True, space_after=4)
    _docx_par(doc, spec["intro"], size=10, space_after=6)

    if spec["assumptions"]:
        _docx_par(doc, spec["assumptions_heading"], size=10, bold=True, space_after=2)
        for a in spec["assumptions"]:
            p = doc.add_paragraph(a, style="List Bullet")
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.size = Pt(10)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # Positions table
    cols = spec["columns"]
    tbl = doc.add_table(rows=1, cols=len(cols))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cols):
        cell = tbl.rows[0].cells[i]
        cell.paragraphs[0].text = ""
        _docx_par(cell, c, size=9, bold=True, space_after=0, align="right" if i >= 2 else None)
        _docx_shade(cell, ACCENT_LIGHT)
    for r in spec["rows"]:
        pos, desc, qty, unit, price = r
        line_total = (qty or 0) * (price or 0) if qty is not None else None
        vals = [pos, desc, "" if qty is None else (str(int(qty)) if float(qty).is_integer() else str(qty)),
                unit, chf(price), chf(line_total)]
        cells = tbl.add_row().cells
        for i, v in enumerate(vals):
            cells[i].paragraphs[0].text = ""
            _docx_par(cells[i], v, size=9, space_after=0, align="right" if i >= 2 else None)
    _docx_set_widths(tbl, [1.2, 6.8, 1.6, 2.4, 2.5, 2.5])

    # Totals
    subtotal, vat, total = compute_totals(spec["rows"])
    tot = doc.add_table(rows=3, cols=2)
    _docx_no_borders(tot)
    tot.alignment = WD_TABLE_ALIGNMENT.RIGHT
    for i, (label, val, bold) in enumerate([
        (spec["subtotal_label"], chf(subtotal), False),
        (spec["vat_label"], chf(vat), False),
        (spec["total_label"], "CHF " + chf(total), True),
    ]):
        tot.rows[i].cells[0].paragraphs[0].text = ""
        tot.rows[i].cells[1].paragraphs[0].text = ""
        _docx_par(tot.rows[i].cells[0], label, size=10, bold=bold, space_after=0, align="right")
        _docx_par(tot.rows[i].cells[1], val, size=10, bold=bold, space_after=0, align="right")
    _docx_set_widths(tot, [6.5, 3.5])

    if spec["cap_line"]:
        _docx_par(doc, spec["cap_line"], size=9, italic=True, space_after=2)
    _docx_par(doc, spec["vat_note"], size=8, color=GREY, italic=True, space_after=8)

    # Conditions
    _docx_par(doc, spec["conditions_heading"], size=11, bold=True, color=ACCENT, space_after=3)
    cond = doc.add_table(rows=len(spec["conditions"]), cols=2)
    _docx_no_borders(cond)
    for i, (k, v) in enumerate(spec["conditions"]):
        cond.rows[i].cells[0].paragraphs[0].text = ""
        cond.rows[i].cells[1].paragraphs[0].text = ""
        _docx_par(cond.rows[i].cells[0], k, size=9.5, bold=True, space_after=2)
        _docx_par(cond.rows[i].cells[1], v, size=9.5, space_after=2)
    _docx_set_widths(cond, [4.5, 12.5])

    _docx_par(doc, spec["legal_note"], size=9, bold=True, space_after=8)

    _docx_par(doc, spec["closing"], size=10, space_after=14)
    for line in spec["closing_lines"]:
        _docx_par(doc, line, size=10, space_after=0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Acceptance block (boxed)
    box = doc.add_table(rows=1, cols=1)
    box.style = "Table Grid"
    cell = box.rows[0].cells[0]
    cell.paragraphs[0].text = ""
    _docx_shade(cell, "F7F9FB")
    _docx_par(cell, spec["acceptance_heading"], size=10, bold=True, color=ACCENT, space_after=4)
    for line in spec["acceptance_lines"]:
        _docx_par(cell, line, size=10, space_after=6)
    _docx_set_widths(box, [17.0])

    # Footer
    footer = section.footer.paragraphs[0]
    footer.text = spec["footer"]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in footer.runs:
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor.from_string(GREY)

    doc.save(out_path)


# ---------------------------------------------------------------------------
# XLSX (offers only — the estimate is DOCX/PDF)
# ---------------------------------------------------------------------------

def build_xlsx(spec, out_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = spec["xl_sheet"]

    bold = Font(bold=True)
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor=ACCENT)
    section_font = Font(bold=True, size=9, color=GREY)
    thin = Side(style="thin", color="BFC5CE")
    border = Border(top=thin, bottom=thin, left=thin, right=thin)
    money = "#,##0.00"

    for col, w in zip("ABCDEF", (14, 40, 10, 11, 18, 16)):
        ws.column_dimensions[col].width = w

    # Sender / meta
    ws["A1"] = spec["sender_heading"].upper()
    ws["A1"].font = section_font
    for i, label in enumerate(spec["xl_sender"], start=2):
        ws[f"A{i}"] = label
        ws[f"A{i}"].font = bold
    ws["B2"], ws["B3"], ws["B4"], ws["B5"], ws["B6"] = spec["sender_lines"][0], spec["sender_lines"][1], \
        spec["sender_lines"][2], "[Telefon]" if spec["lang"] == "de" else "[Téléphone]", "[E-Mail]" if spec["lang"] == "de" else "[E-mail]"
    ws["B7"] = "CHE-XXX.XXX.XXX " + ("MWST" if spec["lang"] == "de" else "TVA")

    for i, (k, v) in enumerate(spec["meta"], start=1):
        ws[f"E{i}"] = k
        ws[f"E{i}"].font = bold
        ws[f"F{i}"] = v

    ws["A9"] = spec["recipient_heading"].upper()
    ws["A9"].font = section_font
    for i, label in enumerate(spec["xl_recipient"], start=10):
        ws[f"A{i}"] = label
        ws[f"A{i}"].font = bold
        ws[f"B{i}"] = spec["recipient_lines"][i - 10]

    ws["A15"] = spec["xl_title_formula"]
    ws["A15"].font = Font(bold=True, size=14, color=ACCENT)
    ws["A16"] = spec["xl_subject_label"]
    ws["A16"].font = bold
    ws["B16"] = spec["subject"]

    # Positions header row 18
    HEAD = 18
    FIRST, LAST = 19, 28
    for i, c in enumerate(spec["columns"]):
        cell = ws.cell(row=HEAD, column=i + 1, value=c)
        cell.font = head_font
        cell.fill = head_fill
        cell.border = border
        cell.alignment = Alignment(horizontal="right" if i >= 2 else "left", vertical="center")
    for r in range(FIRST, LAST + 1):
        ws[f"A{r}"] = f'=IF(B{r}="","",ROW()-{HEAD})'
        ws[f"F{r}"] = f'=IF(C{r}="","",ROUND(C{r}*E{r},2))'
        for col in "ABCDEF":
            ws[f"{col}{r}"].border = border
        ws[f"C{r}"].number_format = "0.##"
        ws[f"E{r}"].number_format = money
        ws[f"F{r}"].number_format = money
        ws[f"A{r}"].alignment = Alignment(horizontal="right")
    for offset, r in enumerate(spec["rows"][:3]):
        row = FIRST + offset
        ws[f"B{row}"] = r[1]
        ws[f"C{row}"] = r[2]
        ws[f"D{row}"] = r[3]
        ws[f"E{row}"] = r[4]

    # Totals
    ws["E30"] = spec["subtotal_label"]
    ws["F30"] = f"=SUM(F{FIRST}:F{LAST})"
    ws["E31"] = spec["xl_vat_rate_label"]
    ws["F31"] = 0.081
    ws["F31"].number_format = "0.0%"
    ws["E32"] = spec["xl_vat_amount_label"]
    ws["F32"] = "=ROUND(F30*F31,2)"
    ws["E33"] = spec["total_label"]
    ws["F33"] = "=F30+F32"
    for r in (30, 32, 33):
        ws[f"F{r}"].number_format = money
    for r in (30, 31, 32, 33):
        ws[f"E{r}"].font = bold
        ws[f"E{r}"].alignment = Alignment(horizontal="right")
    ws["E33"].font = Font(bold=True, size=12)
    ws["F33"].font = Font(bold=True, size=12)
    ws["F33"].border = Border(top=Side(style="double", color=ACCENT), bottom=Side(style="double", color=ACCENT))

    dv = DataValidation(type="list", formula1='"0%,2.6%,3.8%,8.1%"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("F31")

    # Conditions
    ws["A35"] = spec["conditions_heading"].upper()
    ws["A35"].font = section_font
    for i, (k, v) in enumerate(spec["conditions"], start=36):
        ws[f"A{i}"] = k
        ws[f"A{i}"].font = bold
        ws[f"B{i}"] = v
        ws[f"B{i}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(f"B{i}:F{i}")
    ws["A41"] = spec["legal_note"]
    ws["A41"].font = Font(bold=True, size=9)
    ws.merge_cells("A41:F41")
    ws["A41"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[41].height = 28

    ws["A43"] = spec["acceptance_heading"].upper()
    ws["A43"].font = section_font
    acc_labels = spec["acceptance_lines"]
    for i, line in enumerate(acc_labels, start=44):
        ws[f"A{i}"] = line.split(":")[0].strip()
        ws[f"A{i}"].font = bold
        ws[f"B{i}"].border = Border(bottom=thin)
        ws.merge_cells(f"B{i}:D{i}")

    ws["A48"] = spec["xl_vat_hint"]
    ws["A48"].font = Font(italic=True, size=8, color=GREY)
    ws.merge_cells("A48:F48")
    ws["A48"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[48].height = 26
    ws["A49"] = spec["footer"]
    ws["A49"].font = Font(italic=True, size=8, color=GREY)
    ws.merge_cells("A49:F49")

    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.5

    wb.save(out_path)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def build_pdf(spec, out_path):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title=spec["doc_title"].title() + " – magicheidi.ch", author="Magic Heidi",
    )
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=12.5)
    small = ParagraphStyle("small", parent=base, fontSize=8, leading=10, textColor=colors.HexColor("#" + GREY))
    label = ParagraphStyle("label", parent=base, fontName="Helvetica-Bold", fontSize=7.5,
                           textColor=colors.HexColor("#" + GREY))
    bold = ParagraphStyle("bold", parent=base, fontName="Helvetica-Bold")
    h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=19, leading=23,
                        textColor=colors.HexColor("#" + ACCENT), spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=11, leading=14,
                        textColor=colors.HexColor("#" + ACCENT), spaceBefore=6, spaceAfter=3)
    right = ParagraphStyle("right", parent=base, alignment=2)
    right_b = ParagraphStyle("right_b", parent=bold, alignment=2)
    italic = ParagraphStyle("italic", parent=base, fontName="Helvetica-Oblique", fontSize=8.5, leading=11)

    story = []
    avail_w = A4[0] - 36 * mm

    def block(heading, lines):
        return [Paragraph(heading.upper(), label)] + [Paragraph(l, base) for l in lines]

    hdr = Table([[block(spec["sender_heading"], spec["sender_lines"]),
                  block(spec["recipient_heading"], spec["recipient_lines"])]],
                colWidths=[avail_w / 2, avail_w / 2])
    hdr.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story += [hdr, Spacer(1, 8 * mm)]

    title = spec["doc_title"] + (f"  <font size=11 color='#{GREY}'>({spec['doc_subtitle']})</font>" if spec["doc_subtitle"] else "")
    story.append(Paragraph(title, h1))

    meta = Table([[Paragraph(k, bold), Paragraph(v, base)] for k, v in spec["meta"]],
                 colWidths=[45 * mm, avail_w - 45 * mm])
    meta.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    story += [meta, Spacer(1, 4 * mm), Paragraph(spec["subject"], bold), Spacer(1, 1.5 * mm),
              Paragraph(spec["intro"], base), Spacer(1, 3 * mm)]

    if spec["assumptions"]:
        story.append(Paragraph(spec["assumptions_heading"], bold))
        for a in spec["assumptions"]:
            story.append(Paragraph("• " + a, base))
        story.append(Spacer(1, 3 * mm))

    # Positions
    data = [[Paragraph(c, ParagraphStyle("hc", parent=bold, fontSize=8.5, alignment=2 if i >= 2 else 0))
             for i, c in enumerate(spec["columns"])]]
    for r in spec["rows"]:
        pos, desc, qty, unit, price = r
        line_total = (qty or 0) * (price or 0) if qty is not None else None
        qty_s = "" if qty is None else (str(int(qty)) if float(qty).is_integer() else str(qty))
        vals = [pos, desc, qty_s, unit, chf(price), chf(line_total)]
        data.append([Paragraph(v, right if i >= 2 else base) for i, v in enumerate(vals)])
    widths = [11 * mm, 69 * mm, 14 * mm, 23 * mm, 28 * mm, 28 * mm]
    scale = avail_w / sum(widths)
    widths = [w * scale for w in widths]
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#" + ACCENT_LIGHT)),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFC5CE")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(tbl)

    subtotal, vat, total = compute_totals(spec["rows"])
    tot = Table([
        [Paragraph(spec["subtotal_label"], right), Paragraph(chf(subtotal), right)],
        [Paragraph(spec["vat_label"], right), Paragraph(chf(vat), right)],
        [Paragraph(spec["total_label"], right_b), Paragraph("CHF " + chf(total), right_b)],
    ], colWidths=[avail_w - 60 * mm - 28 * mm * scale, 28 * mm * scale], hAlign="RIGHT")
    tot.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (1, 2), (1, 2), 1, colors.HexColor("#" + ACCENT)),
    ]))
    story += [tot, Spacer(1, 2 * mm)]
    if spec["cap_line"]:
        story.append(Paragraph(spec["cap_line"], italic))
    story += [Paragraph(spec["vat_note"], small), Spacer(1, 3 * mm)]

    story.append(Paragraph(spec["conditions_heading"], h2))
    cond = Table([[Paragraph(k, bold), Paragraph(v, base)] for k, v in spec["conditions"]],
                 colWidths=[42 * mm, avail_w - 42 * mm])
    cond.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    story += [cond, Spacer(1, 3 * mm), Paragraph(spec["legal_note"], bold), Spacer(1, 5 * mm),
              Paragraph(spec["closing"], base), Spacer(1, 8 * mm)]
    for line in spec["closing_lines"]:
        story.append(Paragraph(line, base))
    story.append(Spacer(1, 6 * mm))

    acc = [[Paragraph(spec["acceptance_heading"], ParagraphStyle("ah", parent=bold, textColor=colors.HexColor("#" + ACCENT)))]]
    for line in spec["acceptance_lines"]:
        acc.append([Paragraph(line, base)])
    acc_t = Table(acc, colWidths=[avail_w])
    acc_t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#BFC5CE")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F9FB")),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [acc_t, Spacer(1, 4 * mm), Paragraph(spec["footer"], small)]

    doc.build(story)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(out_dir, specs):
    problems = []
    try:
        import pypdf
    except ImportError:
        pypdf = None
        problems.append("pypdf not installed – PDF text check skipped (pip install pypdf)")

    for spec in specs:
        stem = spec["file_stem"]
        probe = "Gültig" if spec["lang"] == "de" else "Téléphone"

        d = Document(os.path.join(out_dir, stem + ".docx"))
        text = "\n".join(p.text for p in d.paragraphs) + "\n".join(
            c.text for t in d.tables for row in t.rows for c in row.cells)
        if probe not in text or spec["doc_title"] not in text or spec["acceptance_heading"] not in text:
            problems.append(f"{stem}.docx: expected text missing")
        if len(d.tables) < 4:
            problems.append(f"{stem}.docx: expected >=4 tables, got {len(d.tables)}")

        if spec["kind"] == "offer":
            wb = openpyxl.load_workbook(os.path.join(out_dir, stem + ".xlsx"))
            ws = wb.active
            formulas = [ws["F19"].value, ws["F30"].value, ws["F32"].value, ws["F33"].value]
            if not all(isinstance(f, str) and f.startswith("=") for f in formulas):
                problems.append(f"{stem}.xlsx: formulas missing {formulas}")
            if not ws.data_validations.dataValidation:
                problems.append(f"{stem}.xlsx: MWST dropdown missing")
            if probe not in " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value):
                problems.append(f"{stem}.xlsx: umlaut/accent probe missing")

        if pypdf:
            reader = pypdf.PdfReader(os.path.join(out_dir, stem + ".pdf"))
            ptext = "".join(page.extract_text() for page in reader.pages)
            if probe not in ptext or spec["acceptance_heading"].split(" ")[0] not in ptext:
                problems.append(f"{stem}.pdf: expected text missing (umlauts?)")
            if len(reader.pages) > 2:
                problems.append(f"{stem}.pdf: {len(reader.pages)} pages, expected 1–2")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--no-validate", action="store_true")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    specs = [OFFERTE_DE, DEVIS_FR, KVA_DE, KVA_FR]
    for spec in specs:
        stem = spec["file_stem"]
        build_docx(spec, os.path.join(out, stem + ".docx"))
        build_pdf(spec, os.path.join(out, stem + ".pdf"))
        if spec["kind"] == "offer":
            build_xlsx(spec, os.path.join(out, stem + ".xlsx"))
        print("built", stem)

    if not args.no_validate:
        problems = validate(out, specs)
        for p in problems:
            print("PROBLEM:", p)
        if any(not p.startswith("pypdf") for p in problems):
            sys.exit(1)
    for f in sorted(os.listdir(out)):
        if f.split("_")[0] in ("Offerte", "Devis", "Kostenvoranschlag"):
            print(f"{f:36s} {os.path.getsize(os.path.join(out, f)):>7d} bytes")


if __name__ == "__main__":
    main()
