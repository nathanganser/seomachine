"""Generate Arbeitsrapport_Vorlage_Schweiz.xlsx / .docx / .pdf for /arbeitsrapport-schweiz.

Excel: sheet "Stundenrapport" (daily rows, Stunden/Total formulas, KW), sheet
"Übersicht" (weekly + monthly sums) and sheet "Arbeitsrapport" (per-job report form
with Arbeitszeit, Material and Kundenunterschrift).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment  # noqa: E402

from template_common import (CHF_FMT, DATE_FMT, GREY, HOURS_FMT, INPUT_FILL, LIGHT, NAVY, NUM_FMT, TIME_FMT, Pdf,  # noqa: E402
                             docx_footer, docx_heading, docx_kv_table, docx_new, docx_note, docx_page_break, docx_para,
                             docx_save, docx_table, docx_title, docx_two_blocks, xl_cell, xl_header_row, xl_print_setup,
                             xl_save, xl_widths)

TITLE = "Arbeitsrapport & Stundenrapport Vorlage Schweiz"
SUBJECT = "Arbeitsrapport (Einsatzformular) und Stundenrapport / Zeiterfassung mit automatischen Stunden- und Total-Formeln"
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
FIRST, LAST = 8, 68


def build_xlsx():
    wb = Workbook()
    # ---- Stundenrapport (daily rows)
    ws = wb.active
    ws.title = "Stundenrapport"
    xl_widths(ws, {"A": 12, "B": 24, "C": 36, "D": 8, "E": 8, "F": 11, "G": 10, "H": 14, "I": 14, "J": 6})
    xl_cell(ws, "A1", "STUNDENRAPPORT / ZEITERFASSUNG", bold=True, size=14)
    for r, (label, default, fmt) in enumerate([("Name", None, None), ("Firma", None, None), ("Monat / Jahr", None, None), ("Std.-Satz CHF", 120, NUM_FMT)], start=2):
        xl_cell(ws, f"A{r}", label, bold=True)
        ws.merge_cells(f"B{r}:C{r}")
        xl_cell(ws, f"B{r}", default, fill=INPUT_FILL, fmt=fmt)
    xl_cell(ws, "E5", "Der Stundensatz wird pro Zeile vorgeschlagen und kann dort überschrieben werden.", size=8, italic=True, color=GREY)
    headers = ["Datum", "Kunde / Projekt", "Tätigkeit", "Von", "Bis", "Pause (Std.)", "Stunden", "Stundensatz CHF", "Total CHF", "KW"]
    xl_header_row(ws, 7, headers, height=32)
    for r in range(FIRST, LAST + 1):
        xl_cell(ws, f"A{r}", border=True, fill=INPUT_FILL, fmt=DATE_FMT)
        xl_cell(ws, f"B{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"C{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"D{r}", border=True, fill=INPUT_FILL, fmt=TIME_FMT, align="center")
        xl_cell(ws, f"E{r}", border=True, fill=INPUT_FILL, fmt=TIME_FMT, align="center")
        xl_cell(ws, f"F{r}", border=True, fill=INPUT_FILL, fmt=HOURS_FMT, align="center")
        xl_cell(ws, f"G{r}", f'=IF(OR(D{r}="",E{r}=""),"",ROUND(((E{r}-D{r})+(E{r}<D{r}))*24-N(F{r}),2))', border=True, fill=LIGHT, fmt=HOURS_FMT, bold=True)
        xl_cell(ws, f"H{r}", f'=IF(G{r}="","",$B$5)', border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ws, f"I{r}", f'=IF(G{r}="","",ROUND(G{r}*N(H{r}),2))', border=True, fill=LIGHT, fmt=NUM_FMT)
        xl_cell(ws, f"J{r}", f'=IF(A{r}="","",WEEKNUM(A{r},21))', border=True, fill=LIGHT, align="center")
    t = LAST + 2
    xl_cell(ws, f"C{t}", "Total Monat", bold=True, align="right")
    xl_cell(ws, f"G{t}", f"=SUM(G{FIRST}:G{LAST})", bold=True, fmt=HOURS_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"I{t}", f"=SUM(I{FIRST}:I{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"A{t + 1}", "Stunden = (Bis − Von) − Pause. Pause in Dezimalstunden (30 Min. = 0.5). Gelb = Eingabe, grau = Formel.", size=8, italic=True, color=GREY)
    xl_cell(ws, f"A{t + 3}", "Visum Mitarbeiter/in:", bold=True)
    ws.merge_cells(f"B{t + 3}:C{t + 3}")
    xl_cell(ws, f"B{t + 3}", fill=INPUT_FILL)
    xl_cell(ws, f"D{t + 3}", "Visum Kunde / Vorgesetzte/r:", bold=True)
    ws.merge_cells(f"H{t + 3}:I{t + 3}")
    xl_cell(ws, f"H{t + 3}", fill=INPUT_FILL)
    ws.freeze_panes = "A8"
    xl_print_setup(ws, landscape_mode=True, print_area=f"A1:J{t + 3}", title_rows="7:7")

    # ---- Übersicht (weekly + monthly)
    ov = wb.create_sheet("Übersicht")
    xl_widths(ov, {"A": 10, "B": 12, "C": 14, "D": 4, "E": 14, "F": 12, "G": 14})
    xl_cell(ov, "A1", "WOCHEN- UND MONATSÜBERSICHT", bold=True, size=14)
    xl_cell(ov, "A2", "Wird automatisch aus dem Blatt «Stundenrapport» berechnet.", size=9, italic=True, color=GREY)
    xl_header_row(ov, 4, ["KW", "Stunden", "Total CHF"])
    for kw in range(1, 54):
        r = 4 + kw
        xl_cell(ov, f"A{r}", kw, border=True, align="center")
        xl_cell(ov, f"B{r}", f"=SUMIF(Stundenrapport!$J${FIRST}:$J${LAST},A{r},Stundenrapport!$G${FIRST}:$G${LAST})", border=True, fmt=HOURS_FMT)
        xl_cell(ov, f"C{r}", f"=SUMIF(Stundenrapport!$J${FIRST}:$J${LAST},A{r},Stundenrapport!$I${FIRST}:$I${LAST})", border=True, fmt=NUM_FMT)
    xl_cell(ov, "A58", "Total", bold=True, border=True, fill=LIGHT)
    xl_cell(ov, "B58", "=SUM(B5:B57)", bold=True, border=True, fill=LIGHT, fmt=HOURS_FMT)
    xl_cell(ov, "C58", "=SUM(C5:C57)", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_header_row(ov, 4, ["Monat", "Stunden", "Total CHF"], start_col=5)
    rng = f"Stundenrapport!$A${FIRST}:$A${LAST}"
    for i, name in enumerate(MONTHS, start=1):
        r = 4 + i
        xl_cell(ov, f"E{r}", name, border=True, bold=True)
        xl_cell(ov, f"F{r}", f'=SUMPRODUCT(--(MONTH({rng})={i}),--({rng}<>""),Stundenrapport!$G${FIRST}:$G${LAST})', border=True, fmt=HOURS_FMT)
        xl_cell(ov, f"G{r}", f'=SUMPRODUCT(--(MONTH({rng})={i}),--({rng}<>""),Stundenrapport!$I${FIRST}:$I${LAST})', border=True, fmt=NUM_FMT)
    xl_cell(ov, "E17", "Total", bold=True, border=True, fill=LIGHT)
    xl_cell(ov, "F17", "=SUM(F5:F16)", bold=True, border=True, fill=LIGHT, fmt=HOURS_FMT)
    xl_cell(ov, "G17", "=SUM(G5:G16)", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_print_setup(ov, print_area="A1:G58")

    # ---- Arbeitsrapport (per-job form)
    ar = wb.create_sheet("Arbeitsrapport")
    xl_widths(ar, {"A": 19, "B": 12, "C": 14, "D": 14, "E": 16, "F": 16})
    xl_cell(ar, "A1", "ARBEITSRAPPORT", bold=True, size=14)
    xl_cell(ar, "E1", "Rapport-Nr.", bold=True)
    xl_cell(ar, "F1", "AR-2026-001", fill=INPUT_FILL)
    xl_cell(ar, "E2", "Datum", bold=True)
    xl_cell(ar, "F2", fill=INPUT_FILL, fmt=DATE_FMT)
    for r, label in enumerate(["Firma (Ausführende)", "Kunde", "Einsatzort", "Auftrag / Bezug", "Mitarbeiter/in"], start=2):
        xl_cell(ar, f"A{r}", label, bold=True)
        ws_range = f"B{r}:D{r}"
        ar.merge_cells(ws_range)
        xl_cell(ar, f"B{r}", fill=INPUT_FILL)
    xl_cell(ar, "A8", "ARBEITSZEIT", bold=True, size=11)
    xl_header_row(ar, 9, ["Von", "Bis", "Pause (Std.)", "Stunden", "Stundensatz CHF", "Total CHF"])
    for r in range(10, 14):
        xl_cell(ar, f"A{r}", border=True, fill=INPUT_FILL, fmt=TIME_FMT, align="center")
        xl_cell(ar, f"B{r}", border=True, fill=INPUT_FILL, fmt=TIME_FMT, align="center")
        xl_cell(ar, f"C{r}", border=True, fill=INPUT_FILL, fmt=HOURS_FMT, align="center")
        xl_cell(ar, f"D{r}", f'=IF(OR(A{r}="",B{r}=""),"",ROUND(((B{r}-A{r})+(B{r}<A{r}))*24-N(C{r}),2))', border=True, fill=LIGHT, fmt=HOURS_FMT)
        xl_cell(ar, f"E{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ar, f"F{r}", f'=IF(D{r}="","",ROUND(D{r}*N(E{r}),2))', border=True, fill=LIGHT, fmt=NUM_FMT)
    xl_cell(ar, "C14", "Total Arbeit", bold=True, align="right")
    xl_cell(ar, "D14", "=SUM(D10:D13)", bold=True, border=True, fill=LIGHT, fmt=HOURS_FMT)
    xl_cell(ar, "F14", "=SUM(F10:F13)", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_cell(ar, "A16", "AUSGEFÜHRTE ARBEITEN", bold=True, size=11)
    ar.merge_cells("A17:F21")
    xl_cell(ar, "A17", "[Was wurde gemacht? Besondere Vorkommnisse, offene Punkte, Folgearbeiten]", fill=INPUT_FILL, wrap=True, color=GREY)
    for r in range(17, 22):
        ar.row_dimensions[r].height = 16
    ar["A17"].alignment = Alignment(wrap_text=True, vertical="top")
    xl_cell(ar, "A23", "MATERIAL / ZUSATZPOSITIONEN", bold=True, size=11)
    xl_header_row(ar, 24, ["Menge", "Einheit", "Bezeichnung", "", "Preis CHF", "Total CHF"])
    ar.merge_cells("C24:D24")
    for r in range(25, 30):
        xl_cell(ar, f"A{r}", border=True, fill=INPUT_FILL, fmt="0.##")
        xl_cell(ar, f"B{r}", border=True, fill=INPUT_FILL)
        ar.merge_cells(f"C{r}:D{r}")
        xl_cell(ar, f"C{r}", border=True, fill=INPUT_FILL)
        xl_cell(ar, f"D{r}", border=True, fill=INPUT_FILL)
        xl_cell(ar, f"E{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ar, f"F{r}", f'=IF(OR(A{r}="",E{r}=""),"",ROUND(A{r}*E{r},2))', border=True, fill=LIGHT, fmt=NUM_FMT)
    xl_cell(ar, "E30", "Total Material", bold=True, align="right")
    xl_cell(ar, "F30", "=SUM(F25:F29)", bold=True, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_cell(ar, "E32", "Total Rapport (exkl. MWST)", bold=True, align="right")
    xl_cell(ar, "F32", "=F14+F30", bold=True, size=12, border=True, fill=LIGHT, fmt=CHF_FMT)
    xl_cell(ar, "A33", "Beträge sind Nettobeträge ohne MWST. Die MWST wird auf der Rechnung ausgewiesen.", size=8, italic=True, color=GREY)
    xl_cell(ar, "A35", "BEMERKUNGEN", bold=True, size=11)
    ar.merge_cells("A36:F37")
    xl_cell(ar, "A36", fill=INPUT_FILL, wrap=True)
    ar.row_dimensions[36].height = 16
    ar.row_dimensions[37].height = 16
    xl_cell(ar, "A39", "BESTÄTIGUNG KUNDE", bold=True, size=11)
    xl_cell(ar, "A40", "Die aufgeführten Arbeiten und Materialien wurden wie beschrieben ausgeführt bzw. geliefert.")
    for i, label in enumerate(["Name:", "Datum:", "Unterschrift Kunde:", "Unterschrift Mitarbeiter/in:"]):
        r = 41 + i
        xl_cell(ar, f"C{r}", label, bold=True, align="right")
        ar.merge_cells(f"D{r}:F{r}")
        xl_cell(ar, f"D{r}", fill=INPUT_FILL)
        ar.row_dimensions[r].height = 20
    xl_print_setup(ar, print_area="A1:F44")
    return xl_save(wb, "Arbeitsrapport_Vorlage_Schweiz.xlsx", TITLE, SUBJECT)


def build_docx():
    doc = docx_new()
    # Page 1: Arbeitsrapport
    docx_two_blocks(doc, [("[Dein Firmenname]", True), "[Strasse und Nr.]", "[PLZ Ort]", "[Telefon]  ·  [E-Mail]"],
                    [("Arbeitsrapport Nr. [AR-JJJJ-XXX]", True), "Datum: [TT.MM.JJJJ]"])
    docx_title(doc, "Arbeitsrapport")
    docx_kv_table(doc, [
        ("Kunde:", "[Firma / Name, Adresse]"),
        ("Einsatzort:", "[Adresse / Gebäude / Raum]"),
        ("Auftrag / Bezug:", "[Offerte / Auftrag Nr. XXX]"),
        ("Mitarbeiter/in:", "[Name]"),
    ], widths_mm=(35, 135))
    docx_heading(doc, "Arbeitszeit")
    docx_table(doc, ["Von", "Bis", "Pause (Std.)", "Stunden", "Stundensatz CHF", "Total CHF"],
               [["[08:00]", "[12:00]", "[0.25]", "[3.75]", "[120.00]", "[450.00]"], ["", "", "", "", "", ""], ["", "", "", "", "", ""]],
               widths_mm=(22, 22, 26, 26, 34, 40), right_cols=(3, 4, 5), row_height_mm=7)
    docx_heading(doc, "Ausgeführte Arbeiten")
    for _ in range(3):
        docx_para(doc, "________________________________________________________________________________", color=GREY, space_after=2)
    docx_heading(doc, "Material / Zusatzpositionen")
    docx_table(doc, ["Menge", "Einheit", "Bezeichnung", "Preis CHF", "Total CHF"],
               [["[1]", "[Stk.]", "[Bezeichnung]", "[0.00]", "[0.00]"]] + [["", "", "", "", ""] for _ in range(3)],
               widths_mm=(18, 20, 82, 25, 25), right_cols=(3, 4), row_height_mm=7)
    docx_kv_table(doc, [("Total Arbeit CHF:", "[0.00]"), ("Total Material CHF:", "[0.00]"), ("Total Rapport CHF (exkl. MWST):", "[0.00]")], widths_mm=(70, 100))
    docx_heading(doc, "Bemerkungen")
    docx_para(doc, "[z. B. Anlage wieder betriebsbereit. Empfohlen: Kontrollservice in 6 Monaten.]", color=GREY)
    docx_heading(doc, "Bestätigung Kunde")
    docx_para(doc, "Die aufgeführten Arbeiten und Materialien wurden wie beschrieben ausgeführt bzw. geliefert.", space_after=8)
    docx_kv_table(doc, [("Name:", "______________________________"), ("Datum:", "______________________________"),
                        ("Unterschrift Kunde:", "______________________________"), ("Unterschrift Mitarbeiter/in:", "______________________________")], widths_mm=(55, 115))
    docx_page_break(doc)
    # Page 2: Stundenrapport
    docx_title(doc, "Stundenrapport / Zeiterfassung")
    docx_kv_table(doc, [("Name:", "[Name]"), ("Firma:", "[Firma]"), ("Monat / Jahr:", "[MM.JJJJ]"), ("Stundensatz CHF:", "[120.00]")], widths_mm=(35, 135))
    rows = [["[TT.MM.]", "[Kunde / Projekt]", "[Tätigkeit]", "[08:00]", "[12:00]", "[0.25]", "[3.75]"]]
    rows += [["", "", "", "", "", "", ""] for _ in range(20)]
    docx_table(doc, ["Datum", "Kunde / Projekt", "Tätigkeit", "Von", "Bis", "Pause", "Stunden"], rows,
               widths_mm=(18, 40, 54, 15, 15, 14, 14), right_cols=(6,), row_height_mm=7)
    docx_kv_table(doc, [("Total Stunden:", "______________"), ("Total CHF (Stunden × Satz):", "______________"),
                        ("Visum Mitarbeiter/in:", "______________"), ("Visum Kunde / Vorgesetzte/r:", "______________")], widths_mm=(60, 110))
    docx_note(doc, "Stunden = (Bis − Von) − Pause. Pause in Dezimalstunden (30 Min. = 0.5). Die Excel-Version rechnet Stunden, Total sowie Wochen- und Monatssummen automatisch.")
    docx_footer(doc)
    return docx_save(doc, "Arbeitsrapport_Vorlage_Schweiz.docx", TITLE, SUBJECT)


def build_pdf():
    pdf = Pdf("Arbeitsrapport_Vorlage_Schweiz.pdf", TITLE, SUBJECT)
    m = pdf.margin
    # Page 1
    y = 22
    pdf.text(m, y, "Arbeitsrapport", size=15, bold=True, color=NAVY)
    pdf.text(190, y, "Rapport-Nr. ______________", size=9, align="right")
    y += 9
    pdf.field(m, y, "Firma (Ausführende):", 65)
    pdf.field(120, y, "Datum:", 45)
    y += 8
    pdf.field(m, y, "Kunde:", 145)
    y += 8
    pdf.field(m, y, "Einsatzort:", 140)
    y += 8
    pdf.field(m, y, "Auftrag / Bezug:", 55)
    pdf.field(110, y, "Mitarbeiter/in:", 55)
    y += 10
    pdf.text(m, y, "Arbeitszeit", size=11, bold=True, color=NAVY)
    y += 3
    y = pdf.table(m, y, [24, 24, 26, 26, 34, 36], ["Von", "Bis", "Pause (Std.)", "Stunden", "Stundensatz CHF", "Total CHF"], 3, row_h=7.5, right_cols=(3, 4, 5))
    y += 6
    pdf.text(m, y, "Ausgeführte Arbeiten", size=11, bold=True, color=NAVY)
    y += 5
    for _ in range(5):
        pdf.rule(m, y + 1, 190, y + 1, width=0.3, color="BFBFBF")
        y += 7
    y += 4
    pdf.text(m, y, "Material / Zusatzpositionen", size=11, bold=True, color=NAVY)
    y += 3
    y = pdf.table(m, y, [18, 20, 82, 25, 25], ["Menge", "Einheit", "Bezeichnung", "Preis CHF", "Total CHF"], 4, row_h=7.5, right_cols=(3, 4))
    y += 5
    for label in ["Total Arbeit CHF:", "Total Material CHF:", "Total Rapport CHF (exkl. MWST):"]:
        pdf.text(150, y, label, size=9, bold=True, align="right")
        pdf.rule(155, y + 1, 190, y + 1, width=0.4)
        y += 7
    y += 2
    pdf.text(m, y, "Bemerkungen", size=11, bold=True, color=NAVY)
    y += 3
    pdf.rect(m, y, 170, 14)
    y += 20
    pdf.text(m, y, "Bestätigung Kunde", size=11, bold=True, color=NAVY)
    y += 6
    pdf.text(m, y, "Die aufgeführten Arbeiten und Materialien wurden wie beschrieben ausgeführt bzw. geliefert.", size=9)
    y += 10
    pdf.field(m, y, "Name:", 60)
    pdf.field(110, y, "Datum:", 55)
    y += 11
    pdf.field(m, y, "Unterschrift Kunde:", 45)
    pdf.field(110, y, "Unterschrift Mitarbeiter/in:", 35)
    pdf.new_page()
    # Page 2: Stundenrapport
    y = 22
    pdf.text(m, y, "Stundenrapport / Zeiterfassung", size=15, bold=True, color=NAVY)
    y += 10
    pdf.field(m, y, "Name:", 65)
    pdf.field(115, y, "Firma:", 55)
    y += 8
    pdf.field(m, y, "Monat / Jahr:", 55)
    pdf.field(115, y, "Stundensatz CHF:", 40)
    y += 10
    y = pdf.table(m, y, [18, 40, 54, 15, 15, 14, 14], ["Datum", "Kunde / Projekt", "Tätigkeit", "Von", "Bis", "Pause", "Stunden"], 24, row_h=7.2, right_cols=(6,), header_h=8)
    y += 4
    pdf.text(m, y, "Stunden = (Bis − Von) − Pause. Pause in Dezimalstunden (30 Min. = 0.5).", size=8, color=GREY)
    y += 8
    for label in ["Total Stunden:", "Total CHF (Stunden × Satz):"]:
        pdf.text(150, y, label, size=9, bold=True, align="right")
        pdf.rule(155, y + 1, 190, y + 1, width=0.4)
        y += 7
    y += 3
    pdf.field(m, y, "Visum Mitarbeiter/in:", 45)
    pdf.field(105, y, "Visum Kunde / Vorgesetzte/r:", 40)
    return pdf.save()


if __name__ == "__main__":
    for p in (build_xlsx(), build_docx(), build_pdf()):
        print(p, p.stat().st_size, "bytes")
