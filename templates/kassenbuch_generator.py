"""Generate Kassenbuch_Vorlage_Schweiz.xlsx / .pdf / .docx for /kassenbuch-schweiz.

Excel: running balance (Saldo), MWST column (optional, rate dropdown), Belegnummer,
Einnahme/Ausgabe, year totals, Soll/Ist reconciliation and a Monatsübersicht sheet.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openpyxl import Workbook  # noqa: E402

from template_common import (CHF_FMT, DATE_FMT, GREY, INPUT_FILL, LIGHT, NAVY, NUM_FMT, PCT_FMT, Pdf,  # noqa: E402
                             docx_footer, docx_heading, docx_kv_table, docx_new, docx_note, docx_para, docx_save,
                             docx_table, docx_title, xl_cell, xl_header_row, xl_print_setup, xl_save,
                             xl_validation, xl_widths)

TITLE = "Kassenbuch Vorlage Schweiz"
SUBJECT = "Schweizer Kassenbuch-Vorlage mit laufendem Saldo, Belegnummer und optionaler MWST-Spalte"
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
FIRST, LAST = 8, 107  # data rows


def build_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Kassenbuch"
    xl_widths(ws, {"A": 12, "B": 11, "C": 42, "D": 14, "E": 14, "F": 10, "G": 14, "H": 15})
    xl_cell(ws, "A1", "KASSENBUCH", bold=True, size=14)
    for r, (label, default) in enumerate([("Firma / Name", None), ("Kasse", "Hauptkasse"), ("Jahr", 2026), ("Geführt von", None)], start=2):
        xl_cell(ws, f"A{r}", label, bold=True)
        ws.merge_cells(f"B{r}:C{r}")
        xl_cell(ws, f"B{r}", default, fill=INPUT_FILL)
    xl_cell(ws, "G2", "Anfangsbestand CHF", bold=True, align="right")
    xl_cell(ws, "H2", 0, fill=INPUT_FILL, fmt=NUM_FMT, border=True)
    xl_cell(ws, "G3", "Bargeld in der Kasse am 1. Tag der Periode", size=8, italic=True, color=GREY, align="right")

    headers = ["Datum", "Beleg-Nr.", "Text / Beschreibung (von wem / an wen, wofür)", "Einnahme CHF", "Ausgabe CHF", "MWST-Satz", "MWST-Betrag CHF", "Saldo CHF"]
    xl_header_row(ws, 7, headers, height=32)
    for r in range(FIRST, LAST + 1):
        xl_cell(ws, f"A{r}", border=True, fill=INPUT_FILL, fmt=DATE_FMT)
        xl_cell(ws, f"B{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"C{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"D{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ws, f"E{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ws, f"F{r}", border=True, fill=INPUT_FILL, fmt=PCT_FMT, align="center")
        xl_cell(ws, f"G{r}", f'=IF(F{r}="","",ROUND((N(D{r})+N(E{r}))*F{r}/(1+F{r}),2))', border=True, fill=LIGHT, fmt=NUM_FMT)
        xl_cell(ws, f"H{r}", f'=IF(AND(D{r}="",E{r}=""),"",$H$2+SUM($D${FIRST}:D{r})-SUM($E${FIRST}:E{r}))', border=True, fill=LIGHT, fmt=NUM_FMT, bold=True)
    xl_validation(ws, f"F{FIRST}:F{LAST}", ["0%", "2.6%", "3.8%", "8.1%"], prompt="Nur ausfüllen, wenn du MWST-pflichtig bist. Der Betrag gilt inkl. MWST.")

    t = LAST + 2
    xl_cell(ws, f"C{t}", "Total Periode", bold=True, align="right")
    xl_cell(ws, f"D{t}", f"=SUM(D{FIRST}:D{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"E{t}", f"=SUM(E{FIRST}:E{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"G{t}", f"=SUM(G{FIRST}:G{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"G{t + 1}", "Endbestand (Soll)", bold=True, align="right")
    xl_cell(ws, f"H{t + 1}", f"=$H$2+D{t}-E{t}", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"G{t + 2}", "Kassenbestand gezählt (Ist)", bold=True, align="right")
    xl_cell(ws, f"H{t + 2}", fill=INPUT_FILL, fmt=CHF_FMT, border=True)
    xl_cell(ws, f"G{t + 3}", "Differenz (Ist − Soll)", bold=True, align="right")
    xl_cell(ws, f"H{t + 3}", f'=IF(H{t + 2}="","",H{t + 2}-H{t + 1})', bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"A{t + 3}", "Eine Differenz sofort klären und mit Beleg dokumentieren (z. B. Beleg «Kassendifferenz»).", size=8, italic=True, color=GREY)
    xl_cell(ws, f"A{t + 5}", "Kontrolliert am / Unterschrift:", bold=True)
    ws.merge_cells(f"C{t + 5}:E{t + 5}")
    xl_cell(ws, f"C{t + 5}", fill=INPUT_FILL)
    ws.freeze_panes = "A8"
    xl_print_setup(ws, print_area=f"A1:H{t + 5}", title_rows="7:7")

    # ---- Monatsübersicht
    mo = wb.create_sheet("Monatsübersicht")
    xl_widths(mo, {"A": 14, "B": 16, "C": 16, "D": 16, "E": 22, "F": 16})
    xl_cell(mo, "A1", "MONATSÜBERSICHT", bold=True, size=14)
    xl_cell(mo, "A2", "Wird automatisch aus dem Blatt «Kassenbuch» berechnet (nach Datum).", size=9, italic=True, color=GREY)
    xl_header_row(mo, 4, ["Monat", "Einnahmen CHF", "Ausgaben CHF", "Saldo Monat CHF", "Kassenbestand Monatsende CHF", "MWST CHF"], height=32)
    rng = f"Kassenbuch!$A${FIRST}:$A${LAST}"
    for i, name in enumerate(MONTHS, start=1):
        r = 4 + i
        xl_cell(mo, f"A{r}", name, border=True, bold=True)
        xl_cell(mo, f"B{r}", f'=SUMPRODUCT(--(MONTH({rng})={i}),--({rng}<>""),Kassenbuch!$D${FIRST}:$D${LAST})', border=True, fmt=NUM_FMT)
        xl_cell(mo, f"C{r}", f'=SUMPRODUCT(--(MONTH({rng})={i}),--({rng}<>""),Kassenbuch!$E${FIRST}:$E${LAST})', border=True, fmt=NUM_FMT)
        xl_cell(mo, f"D{r}", f"=B{r}-C{r}", border=True, fmt=NUM_FMT)
        xl_cell(mo, f"E{r}", f"=Kassenbuch!$H$2+SUM($B$5:B{r})-SUM($C$5:C{r})", border=True, fmt=NUM_FMT, bold=True)
        xl_cell(mo, f"F{r}", f'=SUMPRODUCT(--(MONTH({rng})={i}),--({rng}<>""),Kassenbuch!$G${FIRST}:$G${LAST})', border=True, fmt=NUM_FMT)
    xl_cell(mo, "A17", "Total Jahr", bold=True, border=True, fill=LIGHT)
    for col in "BCDF":
        xl_cell(mo, f"{col}17", f"=SUM({col}5:{col}16)", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_cell(mo, "E17", "=E16", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_print_setup(mo, print_area="A1:F17")

    # ---- Anleitung
    an = wb.create_sheet("Anleitung")
    xl_widths(an, {"A": 110})
    lines = [
        ("So führst du das Kassenbuch", True),
        ("1. Trage im Blatt «Kassenbuch» oben den Anfangsbestand ein: das Bargeld, das am ersten Tag in der Kasse liegt.", False),
        ("2. Erfasse jede Bargeldbewegung sofort und chronologisch: Datum, Belegnummer, Text, Betrag als Einnahme ODER Ausgabe.", False),
        ("3. Die Spalte «Saldo» rechnet den laufenden Kassenbestand automatisch (Anfangsbestand + Einnahmen − Ausgaben).", False),
        ("4. MWST-Satz nur ausfüllen, wenn du MWST-pflichtig bist (Umsatz ab CHF 100'000). Der MWST-Betrag wird aus dem Bruttobetrag herausgerechnet.", False),
        ("5. Nummeriere die Belege fortlaufend (z. B. K-001) und lege sie in derselben Reihenfolge ab – 10 Jahre Aufbewahrungspflicht.", False),
        ("6. Zähle die Kasse regelmässig (täglich bei viel Bargeld, sonst monatlich) und trage den gezählten Bestand unten als «Ist» ein.", False),
        ("7. Eine Differenz nie stillschweigend korrigieren: als eigene Buchung mit Beleg «Kassendifferenz» erfassen.", False),
        ("8. Privatentnahmen und Privateinlagen ebenfalls erfassen – sie sind Bargeldbewegungen und gehören ins Kassenbuch.", False),
        ("", False),
        ("Gelbe Felder = Eingabe. Graue Felder = Formel, bitte nicht überschreiben.", False),
        ("Hinweis: Änderungen in Excel sind nicht nachvollziehbar. Speichere deshalb pro Monat eine PDF-Kopie des Kassenbuchs.", False),
        ("Vorlage von Magic Heidi · magicheidi.ch · Stand: September 2026", False),
    ]
    for i, (text, bold) in enumerate(lines, start=1):
        xl_cell(an, f"A{i}", text, bold=bold, size=12 if bold else 10, wrap=True)
    return xl_save(wb, "Kassenbuch_Vorlage_Schweiz.xlsx", TITLE, SUBJECT)


COLS = ["Datum", "Beleg-Nr.", "Text / Beschreibung", "Einnahme CHF", "Ausgabe CHF", "Saldo CHF"]
COL_W = [20, 20, 66, 22, 22, 22]


def build_pdf():
    pdf = Pdf("Kassenbuch_Vorlage_Schweiz.pdf", TITLE, SUBJECT)
    m = pdf.margin
    y = 22
    pdf.text(m, y, "Kassenbuch", size=15, bold=True, color=NAVY)
    pdf.text(190, y, "Blatt Nr. ______", size=9, align="right")
    y += 10
    pdf.field(m, y, "Firma / Name:", 60)
    pdf.field(115, y, "Kasse:", 50)
    y += 8
    pdf.field(m, y, "Monat / Jahr:", 60)
    pdf.field(115, y, "Anfangsbestand CHF:", 35)
    y += 10
    y = pdf.table(m, y, COL_W, COLS, 26, row_h=7.2, right_cols=(3, 4, 5), header_h=8)
    y += 4
    pdf.text(m, y, "Einnahmen und Ausgaben sind Bruttobeträge (inkl. MWST). Saldo = Vorzeile + Einnahme − Ausgabe.", size=8, color=GREY)
    y += 8
    for label in ["Total Einnahmen CHF:", "Total Ausgaben CHF:", "Endbestand (Soll) CHF:", "Kassenbestand gezählt (Ist) CHF:", "Differenz CHF:"]:
        pdf.text(150, y, label, size=9, bold=True, align="right")
        pdf.rule(155, y + 1, 190, y + 1, width=0.4)
        y += 7
    y += 3
    pdf.field(m, y, "Kontrolliert am:", 40)
    pdf.field(100, y, "Unterschrift:", 70)
    return pdf.save()


def build_docx():
    doc = docx_new()
    docx_title(doc, "Kassenbuch")
    docx_kv_table(doc, [
        ("Firma / Name:", "[Firma oder Name]"),
        ("Kasse:", "[Hauptkasse / Handkasse]"),
        ("Monat / Jahr:", "[MM.JJJJ]"),
        ("Anfangsbestand CHF:", "[0.00]"),
    ], widths_mm=(45, 125))
    rows = [["[TT.MM.]", "[K-001]", "[z. B. Barverkauf Kunde X / Büromaterial Migros]", "[0.00]", "", "[0.00]"]]
    rows += [["", "", "", "", "", ""] for _ in range(18)]
    docx_table(doc, COLS, rows, widths_mm=(18, 18, 74, 20, 20, 20), right_cols=(3, 4, 5), row_height_mm=7)
    docx_note(doc, "Einnahmen und Ausgaben sind Bruttobeträge (inkl. MWST). Saldo = Vorzeile + Einnahme − Ausgabe. Belege fortlaufend nummerieren und 10 Jahre aufbewahren.")
    docx_heading(doc, "Abschluss der Periode")
    docx_kv_table(doc, [
        ("Total Einnahmen CHF:", "______________"),
        ("Total Ausgaben CHF:", "______________"),
        ("Endbestand (Soll) CHF:", "______________"),
        ("Kassenbestand gezählt (Ist) CHF:", "______________"),
        ("Differenz CHF:", "______________"),
        ("Kontrolliert am / Unterschrift:", "______________________________"),
    ], widths_mm=(65, 105))
    docx_footer(doc)
    return docx_save(doc, "Kassenbuch_Vorlage_Schweiz.docx", TITLE, SUBJECT)


if __name__ == "__main__":
    for p in (build_xlsx(), build_pdf(), build_docx()):
        print(p, p.stat().st_size, "bytes")
