#!/usr/bin/env python3
"""Generate the Swiss Offerte / Devis / Kostenvoranschlag download templates.

Outputs (default: ../mh-landing/public/downloads/):
  Offerte_Vorlage_Schweiz.docx / .xlsx / .pdf      (German, binding offer)
  Devis_Modele_Suisse.docx / .xlsx / .pdf          (French, binding offer)
  Kostenvoranschlag_Schweiz.docx / .pdf            (German, non-binding estimate)
  Devis_estimatif_Suisse.docx / .pdf               (French, non-binding estimate)

Usage:
  venv/bin/python3 templates/offerte_vorlage_generator.py [--out DIR] [--no-validate]
  venv/bin/python3 templates/offerte_vorlage_generator.py --stems Offerte_Vorlage_Schweiz,Devis_Modele_Suisse

Presentation: branded [FIRMENNAME / LOGO] header + "Vorlage: magicheidi.ch" footer on
DOCX/PDF, and a three-sheet workbook (Anleitung / Offerte / Beispiel) whose Offerte and
Beispiel sheets carry live formulas: per line Menge x Einzelpreis, Zwischentotal,
an editable MWST rate cell (dropdown 0 / 2.6 / 3.8 / 8.1 %), MWST amount and Total CHF.

Every file is re-opened after writing (python-docx / openpyxl / pypdf) and
checked for umlauts + formulas + sheet structure so a broken build fails loudly.
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
INPUT_BLUE = "176B9B"    # text colour of editable cells
INPUT_FILL = "EAF4FB"    # fill of editable cells
FORMULA_FILL = "F0F3F5"  # fill of calculated cells
STAND = "September 2026"

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
# Filled, self-computing example used on the "Beispiel" / "Exemple" sheet.
# Mirrors the worked example on /offerte-vorlage-schweiz: 3'970.00 + 8.1 % = 4'291.57.
FILLED_ROWS_DE = [
    ("1", "Konzept und Beratung", 8, "Std.", 140.00),
    ("2", "Umsetzung gemaess Beschrieb".replace("ae", "\u00e4"), 1, "Pauschal", 2500.00),
    ("3", "Stockfotos (Lizenz)", 10, "Stk.", 35.00),
]
FILLED_ROWS_FR = [
    ("1", "Concept et conseil", 8, "h", 140.00),
    ("2", "R\u00e9alisation selon descriptif", 1, "forfait", 2500.00),
    ("3", "Photos de stock (licence)", 10, "pce", 35.00),
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
# Shared presentation + workbook copy (added when the two workstream templates
# were merged: branded header/footer from one, working formulas from the other)
# ---------------------------------------------------------------------------

LOGO_DE = "[FIRMENNAME / LOGO]"
LOGO_FR = "[RAISON SOCIALE / LOGO]"
STRIP_DE = "Vorlage: magicheidi.ch \u00b7 Stand " + STAND + " \u00b7 Platzhalter in [Klammern] vor dem Versand ersetzen"
STRIP_FR = "Mod\u00e8le : magicheidi.ch \u00b7 \u00c9tat " + STAND.replace("September", "septembre") + \
    " \u00b7 Remplacer les champs entre [crochets] avant l'envoi"

for _spec in (OFFERTE_DE, KVA_DE):
    _spec["logo_placeholder"] = LOGO_DE
    _spec["strip"] = STRIP_DE
for _spec in (DEVIS_FR, KVA_FR):
    _spec["logo_placeholder"] = LOGO_FR
    _spec["strip"] = STRIP_FR

OFFERTE_DE.update(
    xl_instructions_title="Offerte \u00b7 Excel-Vorlage",
    xl_instructions_subtitle="Kostenlos \u00b7 ohne Makros \u00b7 Betr\u00e4ge in CHF \u00b7 Stand " + STAND,
    xl_instructions_head=["Schritt", "So arbeitest du mit der Datei"],
    xl_instructions=[
        ("1 \u00b7 Kopf ausf\u00fcllen",
         "Im Blatt Offerte Absender mit UID, Empf\u00e4nger, Offerten-Nr., Datum und \u00abG\u00fcltig bis\u00bb ersetzen. "
         "Blaue Felder sind Eingaben, graue Felder enthalten Formeln \u2013 diese nicht \u00fcberschreiben."),
        ("2 \u00b7 Positionen",
         "Zeilen 19 bis 28: Beschreibung, Menge, Einheit und Einzelpreis eintragen. Das Total pro Zeile "
         "rechnet die Datei selbst (Menge \u00d7 Einzelpreis), ebenso das Zwischentotal."),
        ("3 \u00b7 MWST",
         "In Zelle F31 den Satz w\u00e4hlen: 8.1 % Normalsatz, 2.6 % reduziert, 3.8 % Beherbergung. "
         "Nicht MWST-pflichtig? 0 % w\u00e4hlen, UID-Zeile leer lassen und den Hinweis \u00abKeine MWST, da nicht "
         "MWST-pflichtig\u00bb stehen lassen."),
        ("4 \u00b7 Bedingungen",
         "Zahlungsbedingungen, Lieferfrist, nicht enthaltene Leistungen und G\u00fcltigkeit erg\u00e4nzen. "
         "L\u00e4ngere Beschreibungen als nummerierten Anhang beilegen und in der Position darauf verweisen."),
        ("5 \u00b7 Annahme und Versand",
         "Annahmefeld stehen lassen, Druckansicht kontrollieren und als PDF exportieren. Dateiname zum Beispiel "
         "Offerte-2026-014-Kundenname.pdf. Keine Platzhalter in [Klammern] mitschicken."),
        ("Beispiel und Grenzen",
         "Das Blatt Beispiel ist ein fiktives Rechenbeispiel, keine Preisempfehlung. Die Vorlage hat zehn "
         "Positionszeilen; beim Erweitern Formeln, Summenbereich F19:F28 und Druckbereich mitziehen."),
    ],
    xl_sources=[
        ("Anleitung, Word- und PDF-Variante", "https://magicheidi.ch/offerte-vorlage-schweiz"),
        ("ESTV: aktuelle MWST-S\u00e4tze", "https://www.estv.admin.ch"),
    ],
    xl_source_label="Quelle",
    xl_sheet_example="Beispiel",
    xl_example_suffix=" \u00b7 FIKTIVES BEISPIEL",
    xl_blank_subtitle="Blaue Felder ausf\u00fcllen \u00b7 graue Felder rechnen automatisch \u00b7 Betr\u00e4ge in CHF",
    xl_example_subtitle="Fiktives Rechenbeispiel \u2013 nicht versenden. Die grauen Felder zeigen, wie die Vorlage rechnet.",
    xl_example_sender=["Mia Bernasconi", "Seestrasse 22", "8002 Z\u00fcrich", "+41 79 123 45 67",
                       "mia@bernasconi.ch", "CHE-123.456.789 MWST (fiktiv)"],
    xl_example_recipient=["M\u00fcller Consulting GmbH", "Frau M. M\u00fcller", "Hauptstrasse 10", "3000 Bern"],
    xl_example_meta=["2026-012", "08.09.2026", "08.10.2026 (30 Tage ab Datum)", "Mia Bernasconi, +41 79 123 45 67"],
    xl_example_subject="Offerte f\u00fcr UX-Konzept und Umsetzung Kundenportal",
    xl_example_conditions=[
        "50 % Akonto bei Auftragserteilung, 50 % innert 30 Tagen nach Abnahme",
        "innert 4 Wochen nach Auftragserteilung",
        "Texte, Hosting und \u00c4nderungen nach Abnahme (nach Aufwand, CHF 140.00/Std.)",
        "Diese Offerte ist g\u00fcltig bis 08.10.2026.",
    ],
    xl_example_warning="FIKTIVES BEISPIEL \u2013 Namen, UID und Preise sind erfunden und keine Branchenempfehlung. "
                       "Nicht versenden und nicht bezahlen.",
    filled_rows=FILLED_ROWS_DE,
)

DEVIS_FR.update(
    xl_instructions_title="Devis \u00b7 mod\u00e8le Excel",
    xl_instructions_subtitle="Gratuit \u00b7 sans macros \u00b7 montants en CHF \u00b7 \u00e9tat septembre 2026",
    xl_instructions_head=["\u00c9tape", "Comment utiliser le fichier"],
    xl_instructions=[
        ("1 \u00b7 Remplir l'en-t\u00eate",
         "Dans la feuille Devis, remplacez l'exp\u00e9diteur avec l'IDE, le destinataire, le n\u00b0 de devis, la date "
         "et la validit\u00e9. Les cellules bleues sont \u00e0 saisir, les grises contiennent des formules \u2013 ne les \u00e9crasez pas."),
        ("2 \u00b7 Positions",
         "Lignes 19 \u00e0 28 : d\u00e9signation, quantit\u00e9, unit\u00e9 et prix unitaire. Le total par ligne "
         "(quantit\u00e9 \u00d7 prix unitaire) et le sous-total se calculent tout seuls."),
        ("3 \u00b7 TVA",
         "Dans la cellule F31, choisissez le taux : 8.1 % normal, 2.6 % r\u00e9duit, 3.8 % h\u00e9bergement. "
         "Pas assujetti ? Choisissez 0 %, laissez la ligne IDE vide et conservez la remarque \u00ab Sans TVA, non assujetti \u00bb."),
        ("4 \u00b7 Conditions",
         "Compl\u00e9tez conditions de paiement, d\u00e9lai d'ex\u00e9cution, prestations non comprises et validit\u00e9. "
         "Joignez les descriptions longues en annexe num\u00e9rot\u00e9e et renvoyez-y depuis la position."),
        ("5 \u00b7 Acceptation et envoi",
         "Conservez le champ d'acceptation, contr\u00f4lez l'aper\u00e7u avant impression et exportez en PDF. "
         "Nom de fichier par exemple Devis-2026-014-Client.pdf. N'envoyez aucun champ entre [crochets]."),
        ("Exemple et limites",
         "La feuille Exemple est un calcul fictif, pas une recommandation de prix. Le mod\u00e8le compte dix lignes ; "
         "en l'\u00e9tendant, adaptez les formules, la plage F19:F28 et la zone d'impression."),
    ],
    xl_sources=[
        ("Guide, versions Word et PDF", "https://magicheidi.ch/fr/offerte-vorlage-schweiz"),
        ("AFC : taux de TVA actuels", "https://www.estv.admin.ch"),
    ],
    xl_source_label="Source",
    xl_sheet_example="Exemple",
    xl_example_suffix=" \u00b7 EXEMPLE FICTIF",
    xl_blank_subtitle="Remplissez les cellules bleues \u00b7 les cellules grises se calculent \u00b7 montants en CHF",
    xl_example_subtitle="Calcul fictif \u2013 ne pas envoyer. Les cellules grises montrent comment le mod\u00e8le calcule.",
    xl_example_sender=["Mia Bernasconi", "Rue du Lac 22", "1003 Lausanne", "+41 79 123 45 67",
                       "mia@bernasconi.ch", "CHE-123.456.789 TVA (fictif)"],
    xl_example_recipient=["M\u00fcller Consulting S\u00e0rl", "Mme M. M\u00fcller", "Rue du Rh\u00f4ne 10", "1204 Gen\u00e8ve"],
    xl_example_meta=["2026-012", "08.09.2026", "08.10.2026 (30 jours d\u00e8s la date)", "Mia Bernasconi, +41 79 123 45 67"],
    xl_example_subject="Devis pour concept UX et r\u00e9alisation du portail client",
    xl_example_conditions=[
        "50 % d'acompte \u00e0 la commande, 50 % \u00e0 30 jours apr\u00e8s r\u00e9ception",
        "dans les 4 semaines suivant la commande",
        "textes, h\u00e9bergement et modifications apr\u00e8s r\u00e9ception (en r\u00e9gie, CHF 140.00/h)",
        "Ce devis est valable jusqu'au 08.10.2026.",
    ],
    xl_example_warning="EXEMPLE FICTIF \u2013 noms, IDE et prix sont invent\u00e9s et ne constituent pas une "
                       "recommandation de prix. Ne pas envoyer, ne pas payer.",
    filled_rows=FILLED_ROWS_FR,
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
    # Inside a table cell, reuse the empty paragraph python-docx creates instead of
    # adding a second one — otherwise every cell carries a blank line and the
    # one-page A4 layout spills onto a second page.
    paras = getattr(doc_or_cell, "paragraphs", None)
    if hasattr(doc_or_cell, "_tc") and paras and len(paras) == 1 and not paras[0].text:
        p = paras[0]
        for stale in list(p.runs):
            stale._element.getparent().remove(stale._element)
    else:
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
    section.top_margin, section.bottom_margin = Cm(1.5), Cm(1.4)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)
    style.paragraph_format.space_after = Pt(3)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.line_spacing = 1.08

    # Branded header: placeholder the user replaces with their own logo.
    head_par = section.header.paragraphs[0]
    head_par.text = ""
    head_run = head_par.add_run(spec["logo_placeholder"])
    head_run.font.size = Pt(9)
    head_run.font.color.rgb = RGBColor.from_string(GREY)

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
    _docx_par(doc, spec["subject"], size=11, bold=True, space_after=4).paragraph_format.space_before = Pt(6)
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
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

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
    _docx_par(doc, spec["vat_note"], size=8, color=GREY, italic=True, space_after=6)

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

    _docx_par(doc, spec["legal_note"], size=9, bold=True, space_after=6)

    _docx_par(doc, spec["closing"], size=10, space_after=8)
    for line in spec["closing_lines"]:
        _docx_par(doc, line, size=10, space_after=0)

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
    footer.text = spec["strip"]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in footer.runs:
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor.from_string(GREY)

    doc.save(out_path)


# ---------------------------------------------------------------------------
# XLSX (offers only — the estimate is DOCX/PDF)
# ---------------------------------------------------------------------------

# Locale-tagged so the Swiss apostrophe separator survives whatever locale the
# reader's Excel/Numbers/Sheets is set to: 1'250.00, not 1,250.00 or 1.250,00.
LCID = {"de": "807", "fr": "100C"}          # de-CH / fr-CH


def _money(spec):
    return "[$-%s]#,##0.00" % LCID[spec["lang"]]


def _money_chf(spec):
    return '[$-%s]"CHF" #,##0.00' % LCID[spec["lang"]]


def _pct(spec):
    return "[$-%s]0.0%%" % LCID[spec["lang"]]

HEAD_ROW, FIRST_ROW, LAST_ROW = 18, 19, 28
SUB_ROW, RATE_ROW, VAT_ROW, TOT_ROW = 30, 31, 32, 33
COND_ROW, LEGAL_ROW, ACC_ROW, HINT_ROW, FOOT_ROW = 36, 41, 43, 48, 49

_thin = Side(style="thin", color="BFC5CE")
_hair = Side(style="hair", color="D8E0E5")


def _xl_input(cell, fmt=None):
    cell.font = Font(name="Calibri", size=10, color=INPUT_BLUE)
    cell.fill = PatternFill("solid", fgColor=INPUT_FILL)
    cell.border = Border(top=_hair, bottom=_hair, left=_hair, right=_hair)
    if fmt:
        cell.number_format = fmt
    return cell


def _xl_formula(cell, fmt=None, big=False):
    cell.font = Font(name="Calibri", size=12 if big else 10, bold=True, color=ACCENT)
    cell.fill = PatternFill("solid", fgColor=FORMULA_FILL)
    cell.border = Border(top=_hair, bottom=_hair, left=_hair, right=_hair)
    if fmt:
        cell.number_format = fmt
    return cell


def _xl_label(cell, size=10, bold=True, color=None):
    cell.font = Font(name="Calibri", size=size, bold=bold, color=color or "000000")
    return cell


def _xl_page(ws, spec, cols="A:F"):
    ws.sheet_view.showGridLines = False
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = ws.page_margins.bottom = 0.5
    ws.oddFooter.center.text = spec["strip"].split(" · Platzhalter")[0].split(" · Remplacer")[0] + " · &P / &N"
    ws.oddFooter.center.size = 8


def build_xlsx_instructions(wb, spec):
    """Sheet 1: how to use the file, plus checked sources."""
    ws = wb.create_sheet(spec_instr_name(spec))
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 92
    ws.merge_cells("A1:B1")
    ws["A1"] = spec["xl_instructions_title"]
    ws["A1"].font = Font(name="Calibri", size=18, bold=True, color=ACCENT)
    ws.row_dimensions[1].height = 30
    ws.merge_cells("A2:B2")
    ws["A2"] = spec["xl_instructions_subtitle"]
    ws["A2"].font = Font(name="Calibri", size=10, color=GREY)
    ws.merge_cells("A3:B3")
    ws["A3"] = spec["logo_placeholder"]
    ws["A3"].font = Font(name="Calibri", size=9, italic=True, color=GREY)

    for i, label in enumerate(spec["xl_instructions_head"]):
        c = ws.cell(row=5, column=i + 1, value=label)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=ACCENT)
        c.alignment = Alignment(vertical="center")
    ws.row_dimensions[5].height = 24

    r = 6
    for label, text in spec["xl_instructions"]:
        _xl_label(ws.cell(row=r, column=1, value=label), color=ACCENT)
        ws.cell(row=r, column=1).alignment = Alignment(vertical="top")
        c = ws.cell(row=r, column=2, value=text)
        c.font = Font(name="Calibri", size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 44
        r += 1
    r += 1
    for label, url in spec["xl_sources"]:
        _xl_label(ws.cell(row=r, column=1, value=spec["xl_source_label"]), size=9, color=GREY)
        c = ws.cell(row=r, column=2, value=label)
        c.hyperlink = url
        c.font = Font(name="Calibri", size=10, color=INPUT_BLUE, underline="single")
        r += 1
    ws.cell(row=r + 1, column=1, value=spec["footer"]).font = Font(name="Calibri", size=8, italic=True, color=GREY)
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)
    _xl_page(ws, spec)
    ws.print_area = f"A1:B{r + 1}"
    return ws


def spec_instr_name(spec):
    return "Anleitung" if spec["lang"] == "de" else "Instructions"


def build_xlsx_sheet(wb, spec, filled=False):
    """Sheet 2/3: the offer form itself. Blue cells are inputs, grey cells are formulas."""
    name = spec["xl_sheet_example"] if filled else spec["xl_sheet"]
    ws = wb.create_sheet(name)
    for col, w in zip("ABCDEF", (26, 38, 10, 12, 18, 18)):
        ws.column_dimensions[col].width = w

    sender = spec["xl_example_sender"] if filled else [
        spec["sender_lines"][0], spec["sender_lines"][1], spec["sender_lines"][2],
        "[Telefon]" if spec["lang"] == "de" else "[Téléphone]",
        "[E-Mail]" if spec["lang"] == "de" else "[E-mail]",
        "CHE-XXX.XXX.XXX " + ("MWST" if spec["lang"] == "de" else "TVA"),
    ]
    recipient = spec["xl_example_recipient"] if filled else spec["recipient_lines"]
    meta_values = spec["xl_example_meta"] if filled else [v for _, v in spec["meta"]]
    subject = spec["xl_example_subject"] if filled else spec["subject"]
    conditions = spec["xl_example_conditions"] if filled else [v for _, v in spec["conditions"]]
    rows = spec["filled_rows"] if filled else []

    # Branded strip + sender / meta
    ws["A1"] = spec["logo_placeholder"]
    ws["A1"].font = Font(name="Calibri", size=9, italic=True, color=GREY)
    ws["A2"] = spec["sender_heading"].upper()
    ws["A2"].font = Font(name="Calibri", size=8, bold=True, color=GREY)
    for i, label in enumerate(spec["xl_sender"]):
        _xl_label(ws.cell(row=3 + i, column=1, value=label), size=9)
        _xl_input(ws.cell(row=3 + i, column=2, value=sender[i]))

    for i, (k, _v) in enumerate(spec["meta"]):
        _xl_label(ws.cell(row=1 + i, column=5, value=k), size=9)
        _xl_input(ws.cell(row=1 + i, column=6, value=meta_values[i]))

    ws["A9"] = spec["recipient_heading"].upper()
    ws["A9"].font = Font(name="Calibri", size=8, bold=True, color=GREY)
    for i, label in enumerate(spec["xl_recipient"]):
        _xl_label(ws.cell(row=10 + i, column=1, value=label), size=9)
        _xl_input(ws.cell(row=10 + i, column=2, value=recipient[i]))

    ws["A15"] = spec["xl_title_formula"]          # ="Offerte Nr. "&F1
    ws["A15"].font = Font(name="Calibri", size=15, bold=True, color=ACCENT)
    ws.merge_cells("A15:C15")
    ws.merge_cells("D15:F15")
    ws["D15"] = spec["xl_example_subtitle"] if filled else spec["xl_blank_subtitle"]
    ws["D15"].font = Font(name="Calibri", size=8, color=GREY)
    ws["D15"].alignment = Alignment(wrap_text=True, vertical="center", horizontal="right")
    ws.row_dimensions[15].height = 24
    _xl_label(ws.cell(row=16, column=1, value=spec["xl_subject_label"]), size=9)
    _xl_input(ws.cell(row=16, column=2, value=subject))
    ws.merge_cells("B16:F16")

    if filled:
        ws.merge_cells("A17:F17")
        ws["A17"] = spec["xl_example_warning"]
        ws["A17"].font = Font(name="Calibri", size=9, bold=True, color="B03A2E")
        ws["A17"].alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[17].height = 26

    # Positions
    for i, label in enumerate(spec["columns"]):
        c = ws.cell(row=HEAD_ROW, column=i + 1, value=label)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=ACCENT)
        c.border = Border(top=_thin, bottom=_thin, left=_thin, right=_thin)
        c.alignment = Alignment(horizontal="right" if i >= 2 else "left", vertical="center", wrap_text=True)
    ws.row_dimensions[HEAD_ROW].height = 26

    for r in range(FIRST_ROW, LAST_ROW + 1):
        _xl_formula(ws.cell(row=r, column=1, value=f'=IF(B{r}="","",ROW()-{HEAD_ROW})'))
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="right")
        _xl_input(ws.cell(row=r, column=2))
        _xl_input(ws.cell(row=r, column=3), "0.##")
        _xl_input(ws.cell(row=r, column=4))
        _xl_input(ws.cell(row=r, column=5), _money(spec))
        _xl_formula(ws.cell(row=r, column=6, value=f'=IF(OR(B{r}="",C{r}=""),"",ROUND(C{r}*E{r},2))'), _money(spec))
        ws.row_dimensions[r].height = 19
    for offset, row_spec in enumerate(rows):
        r = FIRST_ROW + offset
        ws[f"B{r}"], ws[f"C{r}"], ws[f"D{r}"], ws[f"E{r}"] = row_spec[1], row_spec[2], row_spec[3], row_spec[4]

    # Totals: subtotal, editable rate cell, VAT amount, grand total
    _xl_label(ws.cell(row=SUB_ROW, column=5, value=spec["subtotal_label"]))
    _xl_formula(ws.cell(row=SUB_ROW, column=6, value=f"=SUM(F{FIRST_ROW}:F{LAST_ROW})"), _money(spec))
    _xl_label(ws.cell(row=RATE_ROW, column=5, value=spec["xl_vat_rate_label"]))
    _xl_input(ws.cell(row=RATE_ROW, column=6, value=0.081), _pct(spec))
    _xl_label(ws.cell(row=VAT_ROW, column=5, value=spec["xl_vat_amount_label"]))
    _xl_formula(ws.cell(row=VAT_ROW, column=6, value=f"=ROUND(F{SUB_ROW}*F{RATE_ROW},2)"), _money(spec))
    _xl_label(ws.cell(row=TOT_ROW, column=5, value=spec["total_label"]))
    _xl_formula(ws.cell(row=TOT_ROW, column=6, value=f"=F{SUB_ROW}+F{VAT_ROW}"), _money_chf(spec), big=True)
    ws.cell(row=TOT_ROW, column=5).font = Font(name="Calibri", size=11, bold=True, color=ACCENT)
    ws.cell(row=TOT_ROW, column=6).border = Border(
        top=Side(style="double", color=ACCENT), bottom=Side(style="double", color=ACCENT))
    for r in (SUB_ROW, RATE_ROW, VAT_ROW, TOT_ROW):
        ws.cell(row=r, column=5).alignment = Alignment(horizontal="right")

    dv = DataValidation(type="list", formula1='"0%,2.6%,3.8%,8.1%"', allow_blank=True, showErrorMessage=False)
    dv.promptTitle = spec["xl_vat_rate_label"]
    dv.prompt = spec["xl_vat_hint"]
    dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(f"F{RATE_ROW}")

    # Conditions / legal note / acceptance
    ws.cell(row=COND_ROW - 1, column=1, value=spec["conditions_heading"].upper()).font = \
        Font(name="Calibri", size=8, bold=True, color=GREY)
    for i, (k, _v) in enumerate(spec["conditions"]):
        r = COND_ROW + i
        _xl_label(ws.cell(row=r, column=1, value=k), size=9)
        ws.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
        _xl_input(ws.cell(row=r, column=2, value=conditions[i]))
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 26

    ws.merge_cells(f"A{LEGAL_ROW}:F{LEGAL_ROW}")
    ws[f"A{LEGAL_ROW}"] = spec["legal_note"]
    ws[f"A{LEGAL_ROW}"].font = Font(name="Calibri", size=9, bold=True, color=ACCENT)
    ws[f"A{LEGAL_ROW}"].alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[LEGAL_ROW].height = 26

    ws.cell(row=ACC_ROW, column=1, value=spec["acceptance_heading"].upper()).font = \
        Font(name="Calibri", size=8, bold=True, color=GREY)
    for i, line in enumerate(spec["acceptance_lines"]):
        r = ACC_ROW + 1 + i
        _xl_label(ws.cell(row=r, column=1, value=line.split(":")[0].strip()), size=9)
        _xl_input(ws.cell(row=r, column=2))
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)

    ws.merge_cells(f"A{HINT_ROW}:F{HINT_ROW}")
    ws[f"A{HINT_ROW}"] = spec["xl_vat_hint"]
    ws[f"A{HINT_ROW}"].font = Font(name="Calibri", size=8, italic=True, color=GREY)
    ws[f"A{HINT_ROW}"].alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[HINT_ROW].height = 26
    ws.merge_cells(f"A{FOOT_ROW}:F{FOOT_ROW}")
    ws[f"A{FOOT_ROW}"] = spec["strip"]
    ws[f"A{FOOT_ROW}"].font = Font(name="Calibri", size=8, italic=True, color=GREY)

    _xl_page(ws, spec)
    ws.print_area = f"A1:F{FOOT_ROW}"
    return ws


def build_xlsx(spec, out_path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    wb.properties.creator = "Magic Heidi"
    wb.properties.title = spec["doc_title"].title() + " – magicheidi.ch"
    build_xlsx_instructions(wb, spec)
    build_xlsx_sheet(wb, spec, filled=False)
    build_xlsx_sheet(wb, spec, filled=True)
    wb.active = 1
    wb.save(out_path)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def build_pdf(spec, out_path):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=15 * mm, bottomMargin=13 * mm,
        title=spec["doc_title"].title() + " – magicheidi.ch", author="Magic Heidi",
    )
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=12)
    small = ParagraphStyle("small", parent=base, fontSize=8, leading=10, textColor=colors.HexColor("#" + GREY))
    label = ParagraphStyle("label", parent=base, fontName="Helvetica-Bold", fontSize=7.5,
                           textColor=colors.HexColor("#" + GREY))
    bold = ParagraphStyle("bold", parent=base, fontName="Helvetica-Bold")
    h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=19, leading=23,
                        textColor=colors.HexColor("#" + ACCENT), spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=11, leading=14,
                        textColor=colors.HexColor("#" + ACCENT), spaceBefore=4, spaceAfter=2)
    right = ParagraphStyle("right", parent=base, alignment=2)
    right_b = ParagraphStyle("right_b", parent=bold, alignment=2)
    italic = ParagraphStyle("italic", parent=base, fontName="Helvetica-Oblique", fontSize=8.5, leading=11)

    def _page_furniture(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#BFC5CE"))
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#" + GREY))
        canvas.drawString(18 * mm, 8 * mm, spec["strip"])
        canvas.drawRightString(A4[0] - 18 * mm, 8 * mm, str(_doc.page))
        canvas.restoreState()

    story = []
    avail_w = A4[0] - 36 * mm
    story.append(Paragraph(spec["logo_placeholder"], small))

    def block(heading, lines):
        return [Paragraph(heading.upper(), label)] + [Paragraph(l, base) for l in lines]

    hdr = Table([[block(spec["sender_heading"], spec["sender_lines"]),
                  block(spec["recipient_heading"], spec["recipient_lines"])]],
                colWidths=[avail_w / 2, avail_w / 2])
    hdr.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story += [hdr, Spacer(1, 5 * mm)]

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
              Paragraph(spec["closing"], base), Spacer(1, 5 * mm)]
    for line in spec["closing_lines"]:
        story.append(Paragraph(line, base))
    story.append(Spacer(1, 4 * mm))

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
    story.append(acc_t)

    doc.build(story, onFirstPage=_page_furniture, onLaterPages=_page_furniture)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _all_formulas(ws):
    return [c for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith("=")]


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

        # ---- DOCX -------------------------------------------------------
        d = Document(os.path.join(out_dir, stem + ".docx"))
        text = "\n".join(p.text for p in d.paragraphs) + "\n".join(
            c.text for t in d.tables for row in t.rows for c in row.cells)
        if probe not in text or spec["doc_title"] not in text or spec["acceptance_heading"] not in text:
            problems.append(f"{stem}.docx: expected text missing")
        if len(d.tables) < 4:
            problems.append(f"{stem}.docx: expected >=4 tables, got {len(d.tables)}")
        sec = d.sections[0]
        if spec["logo_placeholder"] not in "".join(p.text for p in sec.header.paragraphs):
            problems.append(f"{stem}.docx: logo placeholder missing from header")
        if "magicheidi.ch" not in "".join(p.text for p in sec.footer.paragraphs):
            problems.append(f"{stem}.docx: magicheidi.ch missing from footer")

        # ---- XLSX -------------------------------------------------------
        if spec["kind"] == "offer":
            wb = openpyxl.load_workbook(os.path.join(out_dir, stem + ".xlsx"))
            want = [spec_instr_name(spec), spec["xl_sheet"], spec["xl_sheet_example"]]
            if wb.sheetnames != want:
                problems.append(f"{stem}.xlsx: sheets {wb.sheetnames} != {want}")
            total_formulas = 0
            for sheet_name in want[1:]:
                ws = wb[sheet_name]
                total_formulas += len(_all_formulas(ws))
                checks = {
                    f"F{FIRST_ROW}": "ROUND(C%d*E%d,2)" % (FIRST_ROW, FIRST_ROW),
                    f"F{LAST_ROW}": "ROUND(C%d*E%d,2)" % (LAST_ROW, LAST_ROW),
                    f"F{SUB_ROW}": f"=SUM(F{FIRST_ROW}:F{LAST_ROW})",
                    f"F{VAT_ROW}": f"=ROUND(F{SUB_ROW}*F{RATE_ROW},2)",
                    f"F{TOT_ROW}": f"=F{SUB_ROW}+F{VAT_ROW}",
                }
                for ref, needle in checks.items():
                    v = ws[ref].value
                    if not (isinstance(v, str) and v.startswith("=") and needle.lstrip("=") in v):
                        problems.append(f"{stem}.xlsx[{sheet_name}]!{ref}: expected formula containing "
                                        f"{needle!r}, got {v!r}")
                if LCID[spec["lang"]] not in str(ws[f"F{TOT_ROW}"].number_format):
                    problems.append(f"{stem}.xlsx[{sheet_name}]: total cell lost its Swiss number "
                                    f"format ({ws[f'F{TOT_ROW}'].number_format!r})")
                if ws[f"F{RATE_ROW}"].value != 0.081:
                    problems.append(f"{stem}.xlsx[{sheet_name}]: MWST rate cell F{RATE_ROW} is "
                                    f"{ws[f'F{RATE_ROW}'].value!r}, expected 0.081")
                if not ws.data_validations.dataValidation:
                    problems.append(f"{stem}.xlsx[{sheet_name}]: MWST dropdown missing")
                joined = " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value)
                if probe not in joined:
                    problems.append(f"{stem}.xlsx[{sheet_name}]: umlaut/accent probe missing")
                if "magicheidi.ch" not in joined:
                    problems.append(f"{stem}.xlsx[{sheet_name}]: magicheidi.ch missing")
            expected = 2 * (2 * (LAST_ROW - FIRST_ROW + 1) + 4)  # pos-no + line total per row, + 4 totals/title
            if total_formulas < expected:
                problems.append(f"{stem}.xlsx: {total_formulas} formulas, expected >= {expected}")

            # the Beispiel sheet must contain inputs that make the totals add up
            ex = wb[spec["xl_sheet_example"]]
            sub = sum(ex[f"C{FIRST_ROW + i}"].value * ex[f"E{FIRST_ROW + i}"].value
                      for i in range(len(spec["filled_rows"])))
            vat = round(sub * 0.081, 2)
            if round(sub + vat, 2) != 4291.57:
                problems.append(f"{stem}.xlsx[{spec['xl_sheet_example']}]: example totals "
                                f"{sub}/{vat} do not match the worked example on the landing page")

        # ---- PDF --------------------------------------------------------
        if pypdf:
            reader = pypdf.PdfReader(os.path.join(out_dir, stem + ".pdf"))
            ptext = "".join(page.extract_text() for page in reader.pages)
            if probe not in ptext or spec["acceptance_heading"].split(" ")[0] not in ptext:
                problems.append(f"{stem}.pdf: expected text missing (umlauts?)")
            if "magicheidi.ch" not in ptext:
                problems.append(f"{stem}.pdf: magicheidi.ch strip missing")
            if spec["logo_placeholder"] not in ptext:
                problems.append(f"{stem}.pdf: logo placeholder missing")
            if len(reader.pages) > 2:
                problems.append(f"{stem}.pdf: {len(reader.pages)} pages, expected 1–2")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--stems", default="", help="comma-separated file stems to (re)build; default: all")
    ap.add_argument("--no-validate", action="store_true")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    specs = [OFFERTE_DE, DEVIS_FR, KVA_DE, KVA_FR]
    if args.stems:
        wanted = {s.strip() for s in args.stems.split(",") if s.strip()}
        unknown = wanted - {s["file_stem"] for s in specs}
        if unknown:
            sys.exit("unknown stem(s): " + ", ".join(sorted(unknown)))
        specs = [s for s in specs if s["file_stem"] in wanted]

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
        print("validation OK")
    for spec in specs:
        for ext in (".docx", ".xlsx", ".pdf"):
            path = os.path.join(out, spec["file_stem"] + ext)
            if os.path.exists(path):
                print(f"{spec['file_stem'] + ext:36s} {os.path.getsize(path):>7d} bytes")


if __name__ == "__main__":
    main()
