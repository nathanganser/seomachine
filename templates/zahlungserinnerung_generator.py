"""Generate Zahlungserinnerung_Vorlage_Schweiz.docx / .pdf for /mahnung-vorlage-schweiz.

Friendly first reminder (Stufe 0, before the 1. Mahnung): no Verzugszins, no fee,
new 10-day deadline, invoice reference table and payment details.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from template_common import (GREY, NAVY, Pdf, docx_footer, docx_kv_table, docx_new, docx_note, docx_para,  # noqa: E402
                             docx_runs, docx_save, docx_table, docx_title, docx_two_blocks)

TITLE = "Zahlungserinnerung Vorlage Schweiz"
SUBJECT = "Freundliche Zahlungserinnerung (vor der 1. Mahnung) für Schweizer Freelancer und KMU"

BODY = [
    "Guten Tag [Vorname Nachname]",
    "Beim Abgleich meiner offenen Posten habe ich festgestellt, dass die untenstehende Rechnung noch nicht beglichen wurde. "
    "Wahrscheinlich ist sie im Alltag einfach untergegangen – das passiert den Besten.",
    "Ich bitte Sie, den offenen Betrag bis zum [TT.MM.JJJJ – z. B. in 10 Tagen] auf das unten angegebene Konto zu überweisen. "
    "Es fallen keine Mahngebühren oder Verzugszinsen an.",
    "Falls sich diese Erinnerung mit Ihrer Zahlung gekreuzt hat, betrachten Sie sie bitte als gegenstandslos. "
    "Bei Fragen zur Rechnung erreichen Sie mich jederzeit unter [Telefon / E-Mail].",
    "Herzlichen Dank und freundliche Grüsse",
]


def build_docx():
    doc = docx_new()
    docx_two_blocks(doc,
                    [("[Dein Name / Firmenname]", True), "[Strasse und Nr.]", "[PLZ Ort]", "[Telefon]  ·  [E-Mail]"],
                    ["", "", ("[Firma des Kunden]", True), "[Vorname Nachname]", "[Strasse und Nr.]", "[PLZ Ort]"])
    docx_para(doc, "[Ort], [TT.MM.JJJJ]", align="right", space_after=10)
    docx_title(doc, "Zahlungserinnerung – Rechnung Nr. [JJJJ-XXX]", size=13)
    for i, p in enumerate(BODY):
        docx_para(doc, p, space_after=6 if i else 8)
        if i == 1:
            docx_table(doc, ["Rechnung Nr.", "Rechnungsdatum", "Fällig am", "Offener Betrag"],
                       [["[JJJJ-XXX]", "[TT.MM.JJJJ]", "[TT.MM.JJJJ]", "CHF [1'250.00]"]],
                       widths_mm=(40, 40, 40, 50), right_cols=(3,), font_size=10)
    docx_para(doc, "", space_after=8)
    docx_para(doc, "[Dein Name]", space_after=10)
    docx_kv_table(doc, [("Zahlung an:", "[Dein Name / Firmenname]"), ("IBAN:", "[CHXX XXXX XXXX XXXX XXXX X]"),
                        ("Bank:", "[Name der Bank, Ort]"), ("Zahlungszweck:", "Rechnung Nr. [JJJJ-XXX]")], widths_mm=(35, 135))
    docx_note(doc, "Tipp: Eine Kopie der Originalrechnung (oder den QR-Zahlteil) beilegen, damit der Kunde direkt bezahlen kann. "
                   "Bleibt die Zahlung aus, folgt nach 10 Tagen die 1. Mahnung – Vorlage auf magicheidi.ch/mahnung-vorlage-schweiz.")
    docx_footer(doc)
    return docx_save(doc, "Zahlungserinnerung_Vorlage_Schweiz.docx", TITLE, SUBJECT)


def _wrap(pdf, text, size, max_w_mm):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if pdf.c.stringWidth(test, "Helvetica", size) / pdf.MM > max_w_mm:
            lines.append(cur)
            cur = w
        else:
            cur = test
    lines.append(cur)
    return lines


def build_pdf():
    pdf = Pdf("Zahlungserinnerung_Vorlage_Schweiz.pdf", TITLE, SUBJECT)
    m = pdf.margin
    y = 22
    y = pdf.lines(m, y, ["[Dein Name / Firmenname]", "[Strasse und Nr.]", "[PLZ Ort]", "[Telefon]  ·  [E-Mail]"], size=10, leading=5, bold_first=True)
    y += 4
    y = pdf.lines(115, y, ["[Firma des Kunden]", "[Vorname Nachname]", "[Strasse und Nr.]", "[PLZ Ort]"], size=10, leading=5, bold_first=True)
    y += 6
    pdf.text(190, y, "[Ort], [TT.MM.JJJJ]", size=10, align="right")
    y += 14
    pdf.text(m, y, "Zahlungserinnerung – Rechnung Nr. [JJJJ-XXX]", size=13, bold=True, color=NAVY)
    y += 10
    for i, p in enumerate(BODY):
        for line in _wrap(pdf, p, 10, 170):
            pdf.text(m, y, line, size=10)
            y += 5
        y += 4
        if i == 1:
            y = pdf.table(m, y, [40, 40, 40, 50], ["Rechnung Nr.", "Rechnungsdatum", "Fällig am", "Offener Betrag"], 1, row_h=8,
                          right_cols=(3,), rows=[["[JJJJ-XXX]", "[TT.MM.JJJJ]", "[TT.MM.JJJJ]", "CHF [1'250.00]"]], size=10)
            y += 6
    y += 8
    pdf.text(m, y, "[Dein Name]", size=10)
    y += 12
    for k, v in [("Zahlung an:", "[Dein Name / Firmenname]"), ("IBAN:", "[CHXX XXXX XXXX XXXX XXXX X]"), ("Bank:", "[Name der Bank, Ort]"), ("Zahlungszweck:", "Rechnung Nr. [JJJJ-XXX]")]:
        pdf.text(m, y, k, size=10, bold=True)
        pdf.text(m + 35, y, v, size=10)
        y += 5.5
    y += 6
    for line in _wrap(pdf, "Tipp: Kopie der Originalrechnung oder QR-Zahlteil beilegen. Bleibt die Zahlung aus, folgt nach 10 Tagen die 1. Mahnung – Vorlage auf magicheidi.ch/mahnung-vorlage-schweiz.", 8, 170):
        pdf.text(m, y, line, size=8, color=GREY)
        y += 4
    return pdf.save()


if __name__ == "__main__":
    for p in (build_docx(), build_pdf()):
        print(p, p.stat().st_size, "bytes")
