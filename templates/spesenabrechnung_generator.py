"""Generate Spesenabrechnung_Vorlage_Schweiz.xlsx / .pdf for /spesenabrechnung-vorlage-schweiz.

Excel: expense rows with MWST split formulas (brutto -> MWST -> netto), category and
payment dropdowns, Kilometerentschädigung block, totals and reimbursement amount.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from openpyxl import Workbook  # noqa: E402

from template_common import (CHF_FMT, DATE_FMT, GREY, INPUT_FILL, LIGHT, NAVY, NUM_FMT, PCT_FMT, Pdf,  # noqa: E402
                             xl_cell, xl_header_row, xl_print_setup, xl_save, xl_validation, xl_widths)

TITLE = "Spesenabrechnung Vorlage Schweiz"
SUBJECT = "Schweizer Spesenabrechnung mit MWST-Aufteilung, Kategorien, Kilometerentschädigung und Auszahlungsbetrag"
FIRST, LAST = 10, 39
CATS = ["ÖV / Zug", "Auto / Parken", "Verpflegung", "Übernachtung", "Büromaterial", "Software / Tools", "Telefon / Internet", "Kundengeschenk", "Weiterbildung", "Sonstiges"]


def build_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "Spesenabrechnung"
    xl_widths(ws, {"A": 12, "B": 16, "C": 20, "D": 30, "E": 18, "F": 14, "G": 10, "H": 13, "I": 14, "J": 16, "K": 8, "L": 20})
    xl_cell(ws, "A1", "SPESENABRECHNUNG", bold=True, size=14)
    for r, (label, fmt) in enumerate([("Firma", None), ("Name der einreichenden Person", None), ("Abrechnungsperiode", None), ("Projekt / Kostenstelle (optional)", None)], start=2):
        xl_cell(ws, f"A{r}", label, bold=True)
        ws.merge_cells(f"C{r}:E{r}")
        xl_cell(ws, f"C{r}", fill=INPUT_FILL, fmt=fmt)
    for r, (label, fmt) in enumerate([("Einreichungsdatum", DATE_FMT), ("IBAN für Rückerstattung", None), ("Freigabe durch", None), ("Freigabedatum", DATE_FMT)], start=2):
        xl_cell(ws, f"G{r}", label, bold=True)
        ws.merge_cells(f"I{r}:J{r}")
        xl_cell(ws, f"I{r}", fill=INPUT_FILL, fmt=fmt)
    xl_cell(ws, "A7", "Gelb = Eingabe, grau = Formel. Betrag immer inkl. MWST eintragen (wie auf dem Beleg); Netto und MWST werden herausgerechnet.", size=8, italic=True, color=GREY)

    headers = ["Datum", "Kategorie", "Anbieter / Lieferant", "Geschäftszweck", "Projekt / Kunde", "Betrag inkl. MWST", "MWST-Satz", "MWST-Betrag", "Betrag exkl. MWST", "Bezahlt mit", "Beleg", "Notiz"]
    xl_header_row(ws, 9, headers, height=32)
    for r in range(FIRST, LAST + 1):
        xl_cell(ws, f"A{r}", border=True, fill=INPUT_FILL, fmt=DATE_FMT)
        for col in "BCDEJKL":
            xl_cell(ws, f"{col}{r}", border=True, fill=INPUT_FILL)
        xl_cell(ws, f"F{r}", border=True, fill=INPUT_FILL, fmt=NUM_FMT)
        xl_cell(ws, f"G{r}", border=True, fill=INPUT_FILL, fmt=PCT_FMT, align="center")
        xl_cell(ws, f"H{r}", f'=IF(OR(F{r}="",G{r}=""),"",ROUND(F{r}*G{r}/(1+G{r}),2))', border=True, fill=LIGHT, fmt=NUM_FMT)
        xl_cell(ws, f"I{r}", f'=IF(F{r}="","",F{r}-N(H{r}))', border=True, fill=LIGHT, fmt=NUM_FMT)
    # example row
    ws["A10"].value = None
    xl_validation(ws, f"B{FIRST}:B{LAST}", CATS)
    xl_validation(ws, f"G{FIRST}:G{LAST}", ["0%", "2.6%", "3.8%", "8.1%"], prompt="Satz gemäss Beleg. Leer lassen = kein Vorsteuerabzug.")
    xl_validation(ws, f"J{FIRST}:J{LAST}", ["Privat bezahlt", "Geschäftskarte", "Geschäftskonto", "Bar aus Kasse"], prompt="«Privat bezahlt» wird unten zur Rückerstattung addiert.")
    xl_validation(ws, f"K{FIRST}:K{LAST}", ["Ja", "Nein"])

    t = LAST + 2
    xl_cell(ws, f"E{t}", "Total Spesen", bold=True, align="right")
    xl_cell(ws, f"F{t}", f"=SUM(F{FIRST}:F{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"H{t}", f"=SUM(H{FIRST}:H{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"I{t}", f"=SUM(I{FIRST}:I{LAST})", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)

    k = t + 2
    xl_cell(ws, f"A{k}", "KILOMETERENTSCHÄDIGUNG (Privatfahrzeug)", bold=True, size=11)
    xl_cell(ws, f"A{k + 1}", "Gefahrene Kilometer", bold=True)
    xl_cell(ws, f"C{k + 1}", fill=INPUT_FILL, fmt="0", border=True)
    xl_cell(ws, f"A{k + 2}", "Ansatz pro km CHF", bold=True)
    xl_cell(ws, f"C{k + 2}", 0.70, fill=INPUT_FILL, fmt=NUM_FMT, border=True)
    xl_cell(ws, f"D{k + 2}", "CHF 0.70/km ist der übliche Ansatz gemäss Muster-Spesenreglement der Schweizerischen Steuerkonferenz; eigenes Reglement geht vor.", size=8, italic=True, color=GREY)
    xl_cell(ws, f"A{k + 3}", "Kilometerentschädigung CHF", bold=True)
    xl_cell(ws, f"C{k + 3}", f"=ROUND(N(C{k + 1})*N(C{k + 2}),2)", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)

    s = k + 5
    xl_cell(ws, f"E{s}", "Total Spesen inkl. MWST", bold=True, align="right")
    xl_cell(ws, f"F{s}", f"=F{t}", fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"E{s + 1}", "+ Kilometerentschädigung", bold=True, align="right")
    xl_cell(ws, f"F{s + 1}", f"=C{k + 3}", fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"E{s + 2}", "Gesamttotal Spesen", bold=True, align="right")
    xl_cell(ws, f"F{s + 2}", f"=F{s}+F{s + 1}", bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"E{s + 3}", "davon privat bezahlt (Rückerstattung)", bold=True, align="right")
    xl_cell(ws, f"F{s + 3}", f'=SUMIF(J{FIRST}:J{LAST},"Privat bezahlt",F{FIRST}:F{LAST})+F{s + 1}', bold=True, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"E{s + 4}", "Auszuzahlender Betrag", bold=True, size=12, align="right")
    xl_cell(ws, f"F{s + 4}", f"=F{s + 3}", bold=True, size=12, fmt=CHF_FMT, fill=LIGHT, border=True)
    xl_cell(ws, f"G{s + 3}", "Kilometerentschädigung wird als privat bezahlt behandelt.", size=8, italic=True, color=GREY)

    u = s + 6
    xl_cell(ws, f"A{u}", "Unterschrift einreichende Person:", bold=True)
    ws.merge_cells(f"C{u}:E{u}")
    xl_cell(ws, f"C{u}", fill=INPUT_FILL)
    xl_cell(ws, f"G{u}", "Unterschrift Freigabe:", bold=True)
    ws.merge_cells(f"I{u}:J{u}")
    xl_cell(ws, f"I{u}", fill=INPUT_FILL)
    ws.row_dimensions[u].height = 22
    xl_cell(ws, f"A{u + 2}", "Belege 10 Jahre aufbewahren (Art. 958f OR). Vorsteuerabzug nur mit MWST-konformem Beleg und bei effektiver Abrechnungsmethode.", size=8, italic=True, color=GREY)
    ws.freeze_panes = "A10"
    xl_print_setup(ws, landscape_mode=True, print_area=f"A1:L{u + 2}", title_rows="9:9")

    an = wb.create_sheet("Anleitung")
    xl_widths(an, {"A": 110})
    lines = [
        ("So füllst du die Spesenabrechnung aus", True),
        ("1. Kopf ausfüllen: Firma, Name, Abrechnungsperiode (z. B. September 2026), IBAN für die Rückerstattung.", False),
        ("2. Pro Beleg eine Zeile: Datum, Kategorie (Dropdown), Anbieter, Geschäftszweck (warum geschäftlich?), Betrag inkl. MWST wie auf dem Beleg.", False),
        ("3. MWST-Satz nur eintragen, wenn der Beleg die MWST ausweist und du vorsteuerabzugsberechtigt bist. MWST und Netto werden automatisch berechnet.", False),
        ("4. «Bezahlt mit»: Nur «Privat bezahlt» wird unten zum Auszahlungsbetrag addiert. Geschäftskarte/Geschäftskonto sind bereits bezahlt.", False),
        ("5. Kilometer mit dem Privatfahrzeug unten erfassen – Ansatz gemäss deinem Spesenreglement (Standard CHF 0.70/km).", False),
        ("6. Belege nummerieren, digital ablegen (Foto/Scan reicht) und 10 Jahre aufbewahren.", False),
        ("7. Unterschreiben, freigeben lassen, auszahlen. Für Selbständige ohne Angestellte dient die Tabelle als Spesenlog für die Buchhaltung.", False),
        ("", False),
        ("Vorlage von Magic Heidi · magicheidi.ch · Stand: September 2026", False),
    ]
    for i, (text, bold) in enumerate(lines, start=1):
        xl_cell(an, f"A{i}", text, bold=bold, size=12 if bold else 10, wrap=True)
    return xl_save(wb, "Spesenabrechnung_Vorlage_Schweiz.xlsx", TITLE, SUBJECT)


def build_pdf():
    pdf = Pdf("Spesenabrechnung_Vorlage_Schweiz.pdf", TITLE, SUBJECT, landscape_mode=True)
    m = 15
    y = 18
    pdf.text(m, y, "Spesenabrechnung", size=15, bold=True, color=NAVY)
    pdf.text(282, y, "Periode: ____________________", size=9, align="right")
    y += 9
    pdf.field(m, y, "Firma:", 70)
    pdf.field(120, y, "Name:", 70)
    pdf.field(215, y, "Einreichungsdatum:", 35)
    y += 8
    pdf.field(m, y, "IBAN für Rückerstattung:", 60)
    pdf.field(120, y, "Projekt / Kostenstelle:", 55)
    pdf.field(215, y, "Freigabe durch:", 42)
    y += 9
    cols = [18, 26, 34, 52, 30, 22, 14, 20, 22, 22, 7]
    y = pdf.table(m, y, cols, ["Datum", "Kategorie", "Anbieter", "Geschäftszweck", "Projekt / Kunde", "Betrag inkl.", "MWST %", "MWST CHF", "Betrag exkl.", "Bezahlt mit", "Beleg"],
                  14, row_h=6.6, right_cols=(5, 6, 7, 8), size=8, header_h=7.5)
    y += 3
    pdf.text(m, y, "Betrag inkl. MWST wie auf dem Beleg. MWST = Betrag × Satz ÷ (1 + Satz). Belege nummerieren und 10 Jahre aufbewahren.", size=7.5, color=GREY)
    y += 7
    pdf.text(m, y, "Kilometerentschädigung: ________ km × CHF ______ /km (Standard 0.70) = CHF ____________", size=9)
    for i, label in enumerate(["Total Spesen inkl. MWST:", "davon MWST:", "+ Kilometerentschädigung:", "Auszuzahlender Betrag (privat bezahlt):"]):
        pdf.text(235, y + i * 6.5, label, size=8.5, bold=(i == 3), align="right")
        pdf.rule(240, y + i * 6.5 + 1, 282, y + i * 6.5 + 1, width=0.4)
    y += 6.5 * 3 + 10
    pdf.field(m, y, "Unterschrift einreichende Person:", 60)
    pdf.field(150, y, "Unterschrift Freigabe / Datum:", 60)
    return pdf.save()


if __name__ == "__main__":
    for p in (build_xlsx(), build_pdf()):
        print(p, p.stat().st_size, "bytes")
