"""Generate Lieferschein_Vorlage_Schweiz.docx / .xlsx / .pdf for /lieferschein-schweiz."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openpyxl import Workbook  # noqa: E402

from template_common import (CHF_FMT, DATE_FMT, GREY, INPUT_FILL, LIGHT, NAVY, NUM_FMT, XL_BOTTOM, Pdf,  # noqa: E402
                             docx_footer, docx_heading, docx_kv_table, docx_new, docx_note, docx_para,
                             docx_save, docx_table, docx_title, docx_two_blocks, xl_cell, xl_header_row,
                             xl_print_setup, xl_save, xl_widths)

TITLE = "Lieferschein Vorlage Schweiz"
SUBJECT = "Schweizer Lieferschein-Vorlage zum Ausfüllen (ohne Preise, Preisspalte optional)"
N_ROWS = 8


def build_docx():
    doc = docx_new()
    docx_two_blocks(
        doc,
        [("[Dein Firmenname]", True), "[Strasse und Nr.]", "[PLZ Ort]", "[Telefon]  ·  [E-Mail]", "[UID-Nr., z. B. CHE-123.456.789 – optional]"],
        [("Lieferadresse / Empfänger", True), "[Firma des Kunden]", "[Kontaktperson]", "[Strasse und Nr.]", "[PLZ Ort]"],
    )
    docx_para(doc, "[Ort], [TT.MM.JJJJ]", align="right", space_after=2)
    docx_title(doc, "Lieferschein Nr. [LS-JJJJ-XXX]")
    docx_kv_table(doc, [
        ("Lieferdatum:", "[TT.MM.JJJJ]"),
        ("Bezug:", "[Auftrag / Offerte / Bestellung Nr. XXX vom TT.MM.JJJJ]"),
        ("Kunden-Nr.:", "[optional]"),
        ("Lieferart:", "[Post / Kurier / Abholung / eigene Zustellung]"),
    ], widths_mm=(35, 135))
    docx_para(doc, "Wir liefern Ihnen gemäss Ihrem Auftrag folgende Ware:", space_after=4)
    rows = [["1", "[Menge]", "[Stk.]", "[Artikel-Nr.]", "[Artikelbezeichnung / Beschreibung]", "[optional]"]]
    rows += [[str(i), "", "", "", "", ""] for i in range(2, N_ROWS + 1)]
    docx_table(doc, ["Pos.", "Menge", "Einheit", "Artikel-Nr.", "Artikel / Beschreibung", "Preis CHF (optional)"],
               rows, widths_mm=(11, 16, 16, 24, 75, 28), right_cols=(1, 5), row_height_mm=7)
    docx_note(doc, "Hinweis: Der Lieferschein dokumentiert nur die Lieferung. Die Rechnung mit Preisen, MWST und Zahlungsangaben folgt separat. "
                   "Die Preisspalte kannst du leer lassen oder löschen.")
    docx_heading(doc, "Bemerkungen")
    docx_para(doc, "[z. B. Teillieferung – Rest folgt am TT.MM.JJJJ / Ware bitte bei Anlieferung auf Transportschäden prüfen]", color=GREY)
    docx_heading(doc, "Empfangsbestätigung")
    docx_para(doc, "Die oben aufgeführte Ware wurde vollständig und in einwandfreiem Zustand entgegengenommen.", space_after=10)
    docx_kv_table(doc, [
        ("Ort, Datum:", "______________________________"),
        ("Name (in Blockschrift):", "______________________________"),
        ("Unterschrift Empfänger:", "______________________________"),
        ("Übergeben durch:", "______________________________"),
    ], widths_mm=(50, 120))
    docx_footer(doc)
    return docx_save(doc, "Lieferschein_Vorlage_Schweiz.docx", TITLE, SUBJECT)


def build_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Lieferschein"
    xl_widths(ws, {"A": 17, "B": 9, "C": 9, "D": 14, "E": 44, "F": 15, "G": 16})
    xl_cell(ws, "A1", "ABSENDER", bold=True, size=11)
    for r, label in enumerate(["Firma / Name", "Strasse, Nr.", "PLZ / Ort", "Telefon", "E-Mail", "UID-Nr. (optional)"], start=2):
        xl_cell(ws, f"A{r}", label)
        ws.merge_cells(f"B{r}:D{r}")
        xl_cell(ws, f"B{r}", fill=INPUT_FILL)
    xl_cell(ws, "F1", "Lieferschein-Nr.", bold=True)
    xl_cell(ws, "G1", "LS-2026-001", fill=INPUT_FILL)
    xl_cell(ws, "F2", "Datum", bold=True)
    xl_cell(ws, "G2", fill=INPUT_FILL, fmt=DATE_FMT)
    xl_cell(ws, "F3", "Lieferdatum", bold=True)
    xl_cell(ws, "G3", fill=INPUT_FILL, fmt=DATE_FMT)
    xl_cell(ws, "F4", "Bezug (Auftrag/Offerte)", bold=True)
    xl_cell(ws, "G4", fill=INPUT_FILL)
    xl_cell(ws, "F5", "Kunden-Nr.", bold=True)
    xl_cell(ws, "G5", fill=INPUT_FILL)
    xl_cell(ws, "F6", "Lieferart", bold=True)
    xl_cell(ws, "G6", fill=INPUT_FILL)

    xl_cell(ws, "A9", "LIEFERADRESSE / EMPFÄNGER", bold=True, size=11)
    for r, label in enumerate(["Firma / Name", "Kontaktperson", "Strasse, Nr.", "PLZ / Ort"], start=10):
        xl_cell(ws, f"A{r}", label)
        ws.merge_cells(f"B{r}:D{r}")
        xl_cell(ws, f"B{r}", fill=INPUT_FILL)

    xl_cell(ws, "A15", '="Lieferschein Nr. "&G1', bold=True, size=14)
    headers = ["Pos.", "Menge", "Einheit", "Artikel-Nr.", "Artikel / Beschreibung", "Preis CHF (optional)", "Total CHF (optional)"]
    xl_header_row(ws, 17, headers, height=30)
    first, last = 18, 18 + N_ROWS + 3  # 12 rows
    for r in range(first, last + 1):
        xl_cell(ws, f"A{r}", f'=IF(E{r}="","",ROW()-{first - 1})', border=True, align="center")
        xl_cell(ws, f"B{r}", border=True, fill=INPUT_FILL, fmt="0.##")
        xl_cell(ws, f"C{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"D{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"E{r}", border=True, fill=INPUT_FILL, wrap=True)
        xl_cell(ws, f"F{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ws, f"G{r}", f'=IF(OR(B{r}="",F{r}=""),"",B{r}*F{r})', border=True, fill=LIGHT, fmt=NUM_FMT)
    ws["C18"].value = "Stk."
    tot = last + 2
    xl_cell(ws, f"A{tot}", "Total Stück", bold=True)
    xl_cell(ws, f"B{tot}", f"=SUM(B{first}:B{last})", bold=True, fmt="0.##", fill=LIGHT, border=True)
    xl_cell(ws, f"E{tot}", "Warenwert (optional, ohne MWST)", bold=True, align="right")
    xl_cell(ws, f"G{tot}", f"=SUM(G{first}:G{last})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"A{tot + 1}", "Der Lieferschein ist keine Rechnung: Preise sind optional, MWST und Zahlungsangaben stehen auf der separaten Rechnung.", size=8, italic=True, color=GREY)

    bem = tot + 3
    xl_cell(ws, f"A{bem}", "BEMERKUNGEN", bold=True, size=11)
    ws.merge_cells(f"A{bem + 1}:G{bem + 2}")
    xl_cell(ws, f"A{bem + 1}", "[z. B. Teillieferung – Rest folgt am TT.MM.JJJJ]", fill=INPUT_FILL, wrap=True, color=GREY)
    ws.row_dimensions[bem + 1].height = 18
    ws.row_dimensions[bem + 2].height = 18

    emp = bem + 4
    xl_cell(ws, f"A{emp}", "EMPFANGSBESTÄTIGUNG", bold=True, size=11)
    xl_cell(ws, f"A{emp + 1}", "Die oben aufgeführte Ware wurde vollständig und in einwandfreiem Zustand entgegengenommen.")
    for i, label in enumerate(["Ort, Datum:", "Name (Blockschrift):", "Unterschrift Empfänger:", "Übergeben durch:"]):
        r = emp + 2 + i
        xl_cell(ws, f"D{r}", label, bold=True, align="right")
        ws.merge_cells(f"E{r}:G{r}")
        xl_cell(ws, f"E{r}", fill=INPUT_FILL)
        ws[f"E{r}"].border = XL_BOTTOM
        ws.row_dimensions[r].height = 20
    ws.freeze_panes = None
    xl_print_setup(ws, print_area=f"A1:G{emp + 5}")
    return xl_save(wb, "Lieferschein_Vorlage_Schweiz.xlsx", TITLE, SUBJECT)


def build_pdf():
    pdf = Pdf("Lieferschein_Vorlage_Schweiz.pdf", TITLE, SUBJECT)
    m = pdf.margin
    y = 22
    pdf.text(m, y, "ABSENDER", size=8, bold=True, color=NAVY)
    pdf.text(115, y, "LIEFERADRESSE / EMPFÄNGER", size=8, bold=True, color=NAVY)
    left = ["Dein Firmenname", "Strasse und Nr.", "PLZ Ort", "Telefon · E-Mail", "UID-Nr. (optional)"]
    right = ["Firma des Kunden", "Kontaktperson", "Strasse und Nr.", "PLZ Ort"]
    yy = y + 6
    for i in range(5):
        if i < len(left):
            pdf.text(m, yy, left[i], size=9, color=GREY)
            pdf.rule(m, yy + 1, 100, yy + 1, width=0.3, color="BFBFBF")
        if i < len(right):
            pdf.text(115, yy, right[i], size=9, color=GREY)
            pdf.rule(115, yy + 1, 190, yy + 1, width=0.3, color="BFBFBF")
        yy += 7
    y = yy + 4
    pdf.text(190, y, "Ort, Datum: ____________________", size=9, align="right")
    y += 10
    pdf.text(m, y, "Lieferschein Nr. ________________", size=15, bold=True, color=NAVY)
    y += 9
    for label in ["Lieferdatum:", "Bezug (Auftrag / Offerte / Bestellung Nr.):", "Kunden-Nr.:", "Lieferart (Post / Kurier / Abholung):"]:
        pdf.field(m, y, label, 60)
        y += 7
    y += 3
    pdf.text(m, y, "Wir liefern Ihnen gemäss Ihrem Auftrag folgende Ware:", size=10)
    y += 5
    y = pdf.table(m, y, [10, 16, 16, 24, 76, 28], ["Pos.", "Menge", "Einheit", "Artikel-Nr.", "Artikel / Beschreibung", "Preis CHF (opt.)"],
                  N_ROWS + 2, row_h=8, right_cols=(1, 5), rows=[[str(i + 1)] for i in range(N_ROWS + 2)])
    y += 4
    pdf.text(m, y, "Hinweis: Der Lieferschein dokumentiert nur die Lieferung. Die Rechnung mit Preisen, MWST und Zahlungsangaben folgt separat.", size=8, color=GREY)
    y += 9
    pdf.text(m, y, "Bemerkungen", size=11, bold=True, color=NAVY)
    y += 3
    pdf.rect(m, y, 170, 16)
    pdf.text(m + 2, y + 5, "z. B. Teillieferung – Rest folgt am ______ / Ware bei Anlieferung auf Transportschäden prüfen", size=8, color=GREY)
    y += 24
    pdf.text(m, y, "Empfangsbestätigung", size=11, bold=True, color=NAVY)
    y += 6
    pdf.text(m, y, "Die oben aufgeführte Ware wurde vollständig und in einwandfreiem Zustand entgegengenommen.", size=9)
    y += 10
    pdf.field(m, y, "Ort, Datum:", 55)
    pdf.field(110, y, "Name (Blockschrift):", 45)
    y += 11
    pdf.field(m, y, "Unterschrift Empfänger:", 45)
    pdf.field(110, y, "Übergeben durch:", 50)
    return pdf.save()


if __name__ == "__main__":
    for p in (build_docx(), build_xlsx(), build_pdf()):
        print(p, p.stat().st_size, "bytes")
