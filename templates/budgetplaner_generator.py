#!/usr/bin/env python3
"""
Budgetplaner Vorlage Schweiz – generator for the free budget planner downloads
linked from /budgeting-apps (DE/FR/IT/EN).

Produces, per language, an Excel workbook (3 sheets: monthly budget, yearly
overview, benchmarks/parameters, all with live formulas) and a printable A4 PDF.

Usage:
    venv/bin/python3 templates/budgetplaner_generator.py            # all languages
    venv/bin/python3 templates/budgetplaner_generator.py de fr      # subset
    venv/bin/python3 templates/budgetplaner_generator.py --out DIR  # custom output dir

Default output dir: ../mh-landing/public/downloads (relative to the seomachine repo).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

# ---------------------------------------------------------------------------
# Facts (keep in sync with mh-landing/content/*/budgeting-apps.md)
# ---------------------------------------------------------------------------
STAND = "September 2026"
TAX_RATE = 0.25          # Richtwert Steuer-Rückstellung (page: 20–25%)
AHV_RATE = 0.10          # AHV/IV/EO Selbständige, voller Satz ≈ 10% (content/de/ahv-compensation-fund.md)
MWST_RATE = 0.081        # Normalsatz 8.1%
P3A_MAX_PK = 7258        # Säule 3a 2026 mit Pensionskasse
P3A_MAX_NO_PK = 36288    # Säule 3a 2026 ohne Pensionskasse (20% des Nettoeinkommens)
P3A_RATE = 0.20

CHF_FMT = '#,##0.00'
PCT_FMT = '0.0%'

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------
L = {
    "de": {
        "file": "Budgetplaner_Vorlage_Schweiz",
        "title": "Budgetplaner Vorlage Schweiz – Monatsbudget für Selbständige",
        "pdf_title": "Budgetplaner Schweiz – Monatsbudget",
        "subtitle": "Grün hinterlegte Zellen ausfüllen, grau hinterlegte Zellen rechnen automatisch. Rote Differenz = Budget überschritten.",
        "month": "Monat", "year": "Jahr",
        "sheet_month": "Monatsbudget", "sheet_year": "Jahresübersicht", "sheet_ref": "Richtwerte",
        "headers": ["Position", "Soll Geschäft", "Soll Privat", "Soll Total",
                    "Ist Geschäft", "Ist Privat", "Ist Total", "Differenz", "Notiz"],
        "pdf_headers": ["Position", "Soll Geschäft", "Soll Privat", "Ist", "Differenz"],
        "sec_income": "Einnahmen", "sec_fix": "Fixkosten", "sec_var": "Variable Kosten",
        "sec_res": "Rückstellungen", "sec_sum": "Zusammenfassung",
        "income": ["Umsatz / Honorare (inkl. MWST, falls pflichtig)",
                   "Nebeneinkünfte / Lohn aus Anstellung",
                   "Andere Einnahmen (Zinsen, Rückerstattungen)"],
        "fix": ["Miete / Hypothek inkl. Nebenkosten",
                "Krankenkasse (KVG) & Zusatzversicherung",
                "Versicherungen (Haftpflicht, Hausrat, Betrieb)",
                "Telefon / Internet",
                "Abos & Software",
                "Mobilität (ÖV-Abo, Auto, Leasing)",
                "Weitere Fixkosten"],
        "var": ["Essen & Haushalt",
                "Freizeit & Persönliches",
                "Kleidung & Gesundheit (Selbstbehalt)",
                "Weiterbildung",
                "Büromaterial & Kleinanschaffungen",
                "Marketing & Werbung",
                "Weitere variable Kosten"],
        "res": ["Steuern (Richtwert 25% des Gewinns)",
                "AHV/IV/EO Selbständige (Richtwert ca. 10%)",
                "MWST (nur bei MWST-Pflicht ab CHF 100'000 Umsatz)",
                "Säule 3a (2026: max. CHF 7'258 mit PK, 20% bis CHF 36'288 ohne PK)",
                "Notfallreserve & Sparziele (Ziel: 3–6 Monatsausgaben)"],
        "tot_income": "Total Einnahmen", "tot_fix": "Total Fixkosten",
        "tot_var": "Total variable Kosten", "tot_res": "Total Rückstellungen",
        "base": "Geschäftsgewinn vor Steuern (Basis für Richtwerte)",
        "tot_exp": "Total Ausgaben (Fixkosten + Variable + Rückstellungen)",
        "diff": "Differenz Einnahmen - Ausgaben",
        "rate": "Sparquote (Vorsorge + Reserve + Überschuss)",
        "footer": "Gratis Budgetvorlage von Magic Heidi – magicheidi.ch/budgeting-apps – Stand: {stand}. Richtwerte: Budgetberatung Schweiz (budgetberatung.ch).",
        # Jahresübersicht
        "year_title": "Jahresübersicht – Ist-Werte pro Monat eintragen",
        "months": ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
        "year_total": "Total Jahr", "year_avg": "Ø Monat", "year_plan": "Soll / Monat",
        "year_rows": ["Einnahmen", "Fixkosten", "Variable Kosten",
                      "Steuern, AHV & MWST (Rückstellung)", "Sparen & Vorsorge (3a, Reserve)"],
        "year_exp": "Total Ausgaben", "year_diff": "Differenz", "year_rate": "Sparquote",
        # Richtwerte
        "ref_title": "Richtwerte & Parameter",
        "param_title": "Parameter (anpassbar)",
        "params": ["Steuer-Rückstellung (% des Gewinns)",
                   "AHV/IV/EO Selbständige (% des Gewinns)",
                   "MWST-Satz (0% eintragen, wenn nicht MWST-pflichtig)",
                   "Pensionskasse vorhanden?",
                   "Säule 3a Maximum mit PK (2026)",
                   "Säule 3a Maximum ohne PK (2026)",
                   "Säule 3a ohne PK (% des Nettoeinkommens)"],
        "yes": "ja", "no": "nein",
        "bench_title": "Richtwerte für die Verteilung des Nettoeinkommens (Schweiz)",
        "bench_headers": ["Kategorie", "Richtwert", "Ihr Budget (Soll)", "Ihr Anteil"],
        "bench": [("Wohnen (Miete + Nebenkosten)", "max. 25–30%"),
                  ("Steuern & Rücklagen (Selbständige)", "20–25%"),
                  ("Krankenkasse & Versicherungen", "10–15%"),
                  ("Essen & Haushalt", "10–15%"),
                  ("Mobilität", "5–10%"),
                  ("Sparen & Vorsorge", "mind. 10%"),
                  ("Freizeit & Persönliches", "Rest")],
        "bench_note": "Faustregeln für Selbständige. Detaillierte Budgetvorlagen für Familien, Lernende oder Pensionierte: budgetberatung.ch/budgetvorlagen. Massgebend für Steuern, AHV und Säule 3a ist das Nettoeinkommen gemäss Steuererklärung; die Prozentsätze hier sind Richtwerte, keine Steuerberatung.",
        "legend": "Eingabe", "legend_f": "Formel",
        "pdf_tips_title": "Faustregeln",
        "pdf_tips": ["20–25% jeder Kundenzahlung sofort für Steuern und AHV zur Seite legen.",
                     "Notfallreserve: 3 bis 6 Monatsausgaben.",
                     "Säule 3a 2026: CHF 7'258 mit Pensionskasse, ohne PK 20% des Nettoeinkommens bis CHF 36'288.",
                     "MWST-Pflicht ab CHF 100'000 Jahresumsatz (Sätze 8.1% / 2.6% / 3.8%)."],
        "pdf_year_note": "Ist-Werte pro Monat eintragen, am Jahresende summieren.",
    },
    "fr": {
        "file": "Planificateur_Budget_Suisse",
        "title": "Planificateur de budget Suisse – budget mensuel pour indépendants",
        "pdf_title": "Planificateur de budget Suisse – budget mensuel",
        "subtitle": "Remplissez les cellules vertes, les cellules grises se calculent automatiquement. Écart en rouge = budget dépassé.",
        "month": "Mois", "year": "Année",
        "sheet_month": "Budget mensuel", "sheet_year": "Vue annuelle", "sheet_ref": "Repères",
        "headers": ["Poste", "Prévu pro", "Prévu privé", "Prévu total",
                    "Réel pro", "Réel privé", "Réel total", "Écart", "Note"],
        "pdf_headers": ["Poste", "Prévu pro", "Prévu privé", "Réel", "Écart"],
        "sec_income": "Revenus", "sec_fix": "Coûts fixes", "sec_var": "Coûts variables",
        "sec_res": "Réserves", "sec_sum": "Résumé",
        "income": ["Chiffre d'affaires / honoraires (TVA incluse, si assujetti)",
                   "Revenus accessoires / salaire d'un emploi",
                   "Autres revenus (intérêts, remboursements)"],
        "fix": ["Loyer / hypothèque, charges incluses",
                "Caisse maladie (LAMal) & complémentaires",
                "Assurances (RC, ménage, entreprise)",
                "Téléphone / Internet",
                "Abonnements & logiciels",
                "Mobilité (abonnement TP, voiture, leasing)",
                "Autres coûts fixes"],
        "var": ["Alimentation & ménage",
                "Loisirs & personnel",
                "Vêtements & santé (franchise, quote-part)",
                "Formation continue",
                "Matériel de bureau & petits achats",
                "Marketing & publicité",
                "Autres coûts variables"],
        "res": ["Impôts (repère : 25% du bénéfice)",
                "AVS/AI/APG indépendants (repère : env. 10%)",
                "TVA (uniquement si assujetti, dès CHF 100'000 de CA)",
                "Pilier 3a (2026 : max. CHF 7'258 avec CP, 20% jusqu'à CHF 36'288 sans CP)",
                "Réserve d'urgence & objectifs d'épargne (cible : 3–6 mois de dépenses)"],
        "tot_income": "Total revenus", "tot_fix": "Total coûts fixes",
        "tot_var": "Total coûts variables", "tot_res": "Total réserves",
        "base": "Bénéfice avant impôts (base des repères)",
        "tot_exp": "Total dépenses (fixes + variables + réserves)",
        "diff": "Écart revenus - dépenses",
        "rate": "Taux d'épargne (prévoyance + réserve + excédent)",
        "footer": "Modèle de budget gratuit de Magic Heidi – magicheidi.ch/fr/budgeting-apps – État : {stand}. Repères : Budget-conseil Suisse (budgetberatung.ch).",
        "year_title": "Vue annuelle – saisir les valeurs réelles par mois",
        "months": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"],
        "year_total": "Total année", "year_avg": "Moy. / mois", "year_plan": "Prévu / mois",
        "year_rows": ["Revenus", "Coûts fixes", "Coûts variables",
                      "Impôts, AVS & TVA (réserve)", "Épargne & prévoyance (3a, réserve)"],
        "year_exp": "Total dépenses", "year_diff": "Écart", "year_rate": "Taux d'épargne",
        "ref_title": "Repères & paramètres",
        "param_title": "Paramètres (modifiables)",
        "params": ["Réserve d'impôts (% du bénéfice)",
                   "AVS/AI/APG indépendants (% du bénéfice)",
                   "Taux de TVA (saisir 0% si non assujetti)",
                   "Caisse de pension ?",
                   "Pilier 3a maximum avec CP (2026)",
                   "Pilier 3a maximum sans CP (2026)",
                   "Pilier 3a sans CP (% du revenu net)"],
        "yes": "oui", "no": "non",
        "bench_title": "Repères pour la répartition du revenu net (Suisse)",
        "bench_headers": ["Catégorie", "Repère", "Votre budget (prévu)", "Votre part"],
        "bench": [("Logement (loyer + charges)", "max. 25–30%"),
                  ("Impôts & réserves (indépendants)", "20–25%"),
                  ("Caisse maladie & assurances", "10–15%"),
                  ("Alimentation & ménage", "10–15%"),
                  ("Mobilité", "5–10%"),
                  ("Épargne & prévoyance", "min. 10%"),
                  ("Loisirs & personnel", "le reste")],
        "bench_note": "Règles d'or pour indépendants. Modèles de budget détaillés pour familles, apprentis ou retraités : budgetberatung.ch/budgetvorlagen. Pour les impôts, l'AVS et le pilier 3a, c'est le revenu net selon la déclaration d'impôts qui fait foi ; les pourcentages sont des repères, pas un conseil fiscal.",
        "legend": "Saisie", "legend_f": "Formule",
        "pdf_tips_title": "Règles d'or",
        "pdf_tips": ["Mettre immédiatement de côté 20–25% de chaque paiement client pour les impôts et l'AVS.",
                     "Réserve d'urgence : 3 à 6 mois de dépenses.",
                     "Pilier 3a 2026 : CHF 7'258 avec caisse de pension, sans CP 20% du revenu net jusqu'à CHF 36'288.",
                     "Assujettissement à la TVA dès CHF 100'000 de chiffre d'affaires annuel (taux 8.1% / 2.6% / 3.8%)."],
        "pdf_year_note": "Saisir les valeurs réelles par mois, additionner en fin d'année.",
    },
    "it": {
        "file": "Pianificatore_Budget_Svizzera",
        "title": "Pianificatore di budget Svizzera – budget mensile per indipendenti",
        "pdf_title": "Pianificatore di budget Svizzera – budget mensile",
        "subtitle": "Compila le celle verdi, le celle grigie si calcolano da sole. Differenza in rosso = budget superato.",
        "month": "Mese", "year": "Anno",
        "sheet_month": "Budget mensile", "sheet_year": "Panoramica annuale", "sheet_ref": "Valori di riferimento",
        "headers": ["Voce", "Previsto business", "Previsto privato", "Previsto totale",
                    "Effettivo business", "Effettivo privato", "Effettivo totale", "Differenza", "Nota"],
        "pdf_headers": ["Voce", "Previsto business", "Previsto privato", "Effettivo", "Differenza"],
        "sec_income": "Entrate", "sec_fix": "Costi fissi", "sec_var": "Costi variabili",
        "sec_res": "Accantonamenti", "sec_sum": "Riepilogo",
        "income": ["Fatturato / onorari (IVA inclusa, se assoggettato)",
                   "Entrate accessorie / salario da impiego",
                   "Altre entrate (interessi, rimborsi)"],
        "fix": ["Affitto / ipoteca, spese accessorie incluse",
                "Cassa malati (LAMal) & complementari",
                "Assicurazioni (RC, economia domestica, azienda)",
                "Telefono / Internet",
                "Abbonamenti & software",
                "Mobilità (abbonamento TP, auto, leasing)",
                "Altri costi fissi"],
        "var": ["Cibo & economia domestica",
                "Tempo libero & spese personali",
                "Abbigliamento & salute (franchigia)",
                "Formazione continua",
                "Materiale d'ufficio & piccoli acquisti",
                "Marketing & pubblicità",
                "Altri costi variabili"],
        "res": ["Imposte (riferimento: 25% dell'utile)",
                "AVS/AI/IPG indipendenti (riferimento: ca. 10%)",
                "IVA (solo se assoggettato, da CHF 100'000 di fatturato)",
                "Pilastro 3a (2026: max. CHF 7'258 con CP, 20% fino a CHF 36'288 senza CP)",
                "Riserva d'emergenza & obiettivi di risparmio (target: 3–6 mesi di spese)"],
        "tot_income": "Totale entrate", "tot_fix": "Totale costi fissi",
        "tot_var": "Totale costi variabili", "tot_res": "Totale accantonamenti",
        "base": "Utile prima delle imposte (base per i riferimenti)",
        "tot_exp": "Totale uscite (fissi + variabili + accantonamenti)",
        "diff": "Differenza entrate - uscite",
        "rate": "Tasso di risparmio (previdenza + riserva + eccedenza)",
        "footer": "Modello di budget gratuito di Magic Heidi – magicheidi.ch/it/budgeting-apps – Aggiornato: {stand}. Valori di riferimento: Budgetberatung Schweiz (budgetberatung.ch).",
        "year_title": "Panoramica annuale – inserisci i valori effettivi per mese",
        "months": ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"],
        "year_total": "Totale anno", "year_avg": "Media / mese", "year_plan": "Previsto / mese",
        "year_rows": ["Entrate", "Costi fissi", "Costi variabili",
                      "Imposte, AVS & IVA (accantonamento)", "Risparmio & previdenza (3a, riserva)"],
        "year_exp": "Totale uscite", "year_diff": "Differenza", "year_rate": "Tasso di risparmio",
        "ref_title": "Valori di riferimento & parametri",
        "param_title": "Parametri (modificabili)",
        "params": ["Accantonamento imposte (% dell'utile)",
                   "AVS/AI/IPG indipendenti (% dell'utile)",
                   "Aliquota IVA (inserire 0% se non assoggettato)",
                   "Cassa pensione?",
                   "Pilastro 3a massimo con CP (2026)",
                   "Pilastro 3a massimo senza CP (2026)",
                   "Pilastro 3a senza CP (% del reddito netto)"],
        "yes": "sì", "no": "no",
        "bench_title": "Valori di riferimento per la ripartizione del reddito netto (Svizzera)",
        "bench_headers": ["Categoria", "Riferimento", "Il tuo budget (previsto)", "La tua quota"],
        "bench": [("Abitazione (affitto + spese accessorie)", "max. 25–30%"),
                  ("Imposte & accantonamenti (indipendenti)", "20–25%"),
                  ("Cassa malati & assicurazioni", "10–15%"),
                  ("Cibo & economia domestica", "10–15%"),
                  ("Mobilità", "5–10%"),
                  ("Risparmio & previdenza", "min. 10%"),
                  ("Tempo libero & spese personali", "il resto")],
        "bench_note": "Regole pratiche per indipendenti. Modelli di budget dettagliati per famiglie, apprendisti o pensionati: budgetberatung.ch/budgetvorlagen. Per imposte, AVS e pilastro 3a fa stato il reddito netto secondo la dichiarazione d'imposta; le percentuali sono valori di riferimento, non consulenza fiscale.",
        "legend": "Inserimento", "legend_f": "Formula",
        "pdf_tips_title": "Regole pratiche",
        "pdf_tips": ["Metti subito da parte il 20–25% di ogni pagamento dei clienti per imposte e AVS.",
                     "Riserva d'emergenza: da 3 a 6 mesi di spese.",
                     "Pilastro 3a 2026: CHF 7'258 con cassa pensione, senza CP il 20% del reddito netto fino a CHF 36'288.",
                     "Assoggettamento all'IVA da CHF 100'000 di fatturato annuo (aliquote 8.1% / 2.6% / 3.8%)."],
        "pdf_year_note": "Inserisci i valori effettivi per mese e somma a fine anno.",
    },
    "en": {
        "file": "Budget_Planner_Switzerland",
        "title": "Budget Planner Switzerland – Monthly Budget for the Self-Employed",
        "pdf_title": "Budget Planner Switzerland – Monthly Budget",
        "subtitle": "Fill in the green cells; grey cells calculate automatically. Red difference = over budget.",
        "month": "Month", "year": "Year",
        "sheet_month": "Monthly Budget", "sheet_year": "Yearly Overview", "sheet_ref": "Benchmarks",
        "headers": ["Item", "Planned business", "Planned personal", "Planned total",
                    "Actual business", "Actual personal", "Actual total", "Difference", "Note"],
        "pdf_headers": ["Item", "Planned business", "Planned personal", "Actual", "Difference"],
        "sec_income": "Income", "sec_fix": "Fixed costs", "sec_var": "Variable costs",
        "sec_res": "Reserves", "sec_sum": "Summary",
        "income": ["Revenue / fees (incl. VAT if registered)",
                   "Side income / salary from employment",
                   "Other income (interest, refunds)"],
        "fix": ["Rent / mortgage incl. utilities",
                "Health insurance (KVG) & supplementary",
                "Insurance (liability, household, business)",
                "Phone / Internet",
                "Subscriptions & software",
                "Transport (public transport pass, car, leasing)",
                "Other fixed costs"],
        "var": ["Food & household",
                "Leisure & personal",
                "Clothing & health (deductible, co-pay)",
                "Training & education",
                "Office supplies & small purchases",
                "Marketing & advertising",
                "Other variable costs"],
        "res": ["Taxes (benchmark: 25% of profit)",
                "AHV/IV/EO self-employed (benchmark: approx. 10%)",
                "VAT (only if registered, from CHF 100'000 revenue)",
                "Pillar 3a (2026: max. CHF 7'258 with pension fund, 20% up to CHF 36'288 without)",
                "Emergency fund & savings goals (target: 3–6 months of expenses)"],
        "tot_income": "Total income", "tot_fix": "Total fixed costs",
        "tot_var": "Total variable costs", "tot_res": "Total reserves",
        "base": "Business profit before tax (basis for benchmarks)",
        "tot_exp": "Total expenses (fixed + variable + reserves)",
        "diff": "Difference income - expenses",
        "rate": "Savings rate (retirement + reserve + surplus)",
        "footer": "Free budget template by Magic Heidi – magicheidi.ch/en/budgeting-apps – Last updated: {stand}. Benchmarks: Budgetberatung Schweiz (budgetberatung.ch).",
        "year_title": "Yearly overview – enter actual values per month",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "year_total": "Total year", "year_avg": "Avg / month", "year_plan": "Planned / month",
        "year_rows": ["Income", "Fixed costs", "Variable costs",
                      "Taxes, AHV & VAT (reserve)", "Savings & retirement (3a, reserve)"],
        "year_exp": "Total expenses", "year_diff": "Difference", "year_rate": "Savings rate",
        "ref_title": "Benchmarks & parameters",
        "param_title": "Parameters (editable)",
        "params": ["Tax reserve (% of profit)",
                   "AHV/IV/EO self-employed (% of profit)",
                   "VAT rate (enter 0% if not VAT-registered)",
                   "Pension fund?",
                   "Pillar 3a maximum with pension fund (2026)",
                   "Pillar 3a maximum without pension fund (2026)",
                   "Pillar 3a without pension fund (% of net income)"],
        "yes": "yes", "no": "no",
        "bench_title": "Benchmarks for splitting net income (Switzerland)",
        "bench_headers": ["Category", "Benchmark", "Your budget (planned)", "Your share"],
        "bench": [("Housing (rent + utilities)", "max. 25–30%"),
                  ("Taxes & reserves (self-employed)", "20–25%"),
                  ("Health insurance & other insurance", "10–15%"),
                  ("Food & household", "10–15%"),
                  ("Transport", "5–10%"),
                  ("Savings & retirement", "min. 10%"),
                  ("Leisure & personal", "the rest")],
        "bench_note": "Rules of thumb for the self-employed. Detailed budget templates for families, apprentices or retirees: budgetberatung.ch/budgetvorlagen. Taxes, AHV and pillar 3a are based on net income per your tax return; the percentages here are benchmarks, not tax advice.",
        "legend": "Input", "legend_f": "Formula",
        "pdf_tips_title": "Rules of thumb",
        "pdf_tips": ["Set aside 20–25% of every client payment immediately for taxes and AHV.",
                     "Emergency fund: 3 to 6 months of expenses.",
                     "Pillar 3a 2026: CHF 7'258 with a pension fund; without one, 20% of net income up to CHF 36'288.",
                     "VAT registration required from CHF 100'000 annual revenue (rates 8.1% / 2.6% / 3.8%)."],
        "pdf_year_note": "Enter actual values per month and add them up at year end.",
    },
}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
GREEN = "E8F5E9"      # input
GREY = "F2F2F2"       # formula
DARK = "1F3A5F"       # headers
SECTION = "DCE6F1"
RED_FILL = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def fill(color):
    return PatternFill(start_color=color, end_color=color, fill_type="solid")


def style_cell(c, *, bold=False, color=None, fmt=None, align=None, white=False, size=None, italic=False):
    c.font = Font(bold=bold, color="FFFFFF" if white else "000000", size=size or 10, italic=italic)
    if color:
        c.fill = fill(color)
    if fmt:
        c.number_format = fmt
    if align:
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
    c.border = BORDER


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------
def build_xlsx(lang: str, out: Path) -> Path:
    t = L[lang]
    wb = Workbook()

    # ---------------- Richtwerte sheet (parameters referenced by formulas) --------
    ws_ref = wb.create_sheet(t["sheet_ref"])
    ref = f"'{t['sheet_ref']}'"

    # ---------------- Monatsbudget --------------------------------------------
    ws = wb.active
    ws.title = t["sheet_month"]
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 58
    for col in "BCDEFGH":
        ws.column_dimensions[col].width = 15
    ws.column_dimensions["I"].width = 28

    ws["A1"] = t["title"]
    ws["A1"].font = Font(bold=True, size=14, color=DARK)
    ws.merge_cells("A1:I1")
    ws["A2"] = t["subtitle"]
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.merge_cells("A2:I2")
    ws["A3"] = f"{t['month']} / {t['year']}:"
    ws["A3"].font = Font(bold=True)
    ws["A3"].alignment = Alignment(horizontal="right")
    ws["B3"].fill = fill(GREEN)
    ws["B3"].border = BORDER
    ws["C3"].fill = fill(GREEN)
    ws["C3"].border = BORDER
    ws["B3"] = t["months"][0]
    ws["C3"] = 2026
    ws["E3"] = t["legend"]
    style_cell(ws["E3"], color=GREEN, align="center")
    ws["F3"] = t["legend_f"]
    style_cell(ws["F3"], color=GREY, align="center")

    HDR = 5
    for i, h in enumerate(t["headers"], start=1):
        c = ws.cell(row=HDR, column=i, value=h)
        style_cell(c, bold=True, color=DARK, white=True, align="center")
    ws.row_dimensions[HDR].height = 30

    row = HDR + 1
    rows = {}          # name -> row number

    def section(title):
        nonlocal row
        c = ws.cell(row=row, column=1, value=title.upper())
        style_cell(c, bold=True, color=SECTION)
        for col in range(2, 10):
            style_cell(ws.cell(row=row, column=col), color=SECTION)
        row += 1

    def item(label, key, *, income=False, formula_b=None, formula_c=None):
        """One budget line. B/C/E/F are inputs (or formulas), D/G/H computed."""
        nonlocal row
        r = row
        style_cell(ws.cell(row=r, column=1, value=label))
        for col, f in ((2, formula_b), (3, formula_c)):
            c = ws.cell(row=r, column=col, value=f)
            style_cell(c, color=GREY if f else GREEN, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=4, value=f"=B{r}+C{r}"), color=GREY, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=5), color=GREEN, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=6), color=GREEN, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=7, value=f"=E{r}+F{r}"), color=GREY, fmt=CHF_FMT)
        diff = f"=G{r}-D{r}" if income else f"=D{r}-G{r}"
        style_cell(ws.cell(row=r, column=8, value=diff), color=GREY, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=9), color=GREEN)
        rows[key] = r
        row += 1
        return r

    def total(label, key, first, last, income=False):
        nonlocal row
        r = row
        style_cell(ws.cell(row=r, column=1, value=label), bold=True, color=GREY)
        for col in range(2, 8):
            L_ = get_column_letter(col)
            style_cell(ws.cell(row=r, column=col, value=f"=SUM({L_}{first}:{L_}{last})"),
                       bold=True, color=GREY, fmt=CHF_FMT)
        diff = f"=G{r}-D{r}" if income else f"=D{r}-G{r}"
        style_cell(ws.cell(row=r, column=8, value=diff), bold=True, color=GREY, fmt=CHF_FMT)
        style_cell(ws.cell(row=r, column=9), color=GREY)
        rows[key] = r
        row += 2
        return r

    # Einnahmen
    section(t["sec_income"])
    first = row
    for i, lab in enumerate(t["income"]):
        item(lab, f"inc{i}", income=True)
    total(t["tot_income"], "tot_inc", first, row - 1, income=True)

    # Fixkosten
    section(t["sec_fix"])
    first = row
    keys_fix = ["rent", "kvg", "ins", "tel", "abo", "mob", "fix_other"]
    for k, lab in zip(keys_fix, t["fix"]):
        item(lab, k)
    total(t["tot_fix"], "tot_fix", first, row - 1)

    # Variable Kosten
    section(t["sec_var"])
    first = row
    keys_var = ["food", "leisure", "cloth", "edu", "office", "mkt", "var_other"]
    for k, lab in zip(keys_var, t["var"]):
        item(lab, k)
    total(t["tot_var"], "tot_var", first, row - 1)

    # Rückstellungen – formulas reference the Richtwerte parameters and the profit base.
    # Base row (in summary) is placed later; we know its row number in advance:
    # summary block starts after reserves total + blank.
    section(t["sec_res"])
    first = row
    n_res = len(t["res"])
    res_total_row = row + n_res
    base_row = res_total_row + 2 + 1   # summary section header + 1
    P = {  # parameter cell addresses on the Richtwerte sheet
        "tax": f"{ref}!$B$4", "ahv": f"{ref}!$B$5", "mwst": f"{ref}!$B$6",
        "pk": f"{ref}!$B$7", "p3a_pk": f"{ref}!$B$8", "p3a_nopk": f"{ref}!$B$9", "p3a_rate": f"{ref}!$B$10",
    }
    inc0 = rows["inc0"]
    r_tax = item(t["res"][0], "tax", formula_b=f"=ROUND(MAX(0,$B${base_row})*{P['tax']},2)")
    r_ahv = item(t["res"][1], "ahv", formula_b=f"=ROUND(MAX(0,$B${base_row})*{P['ahv']},2)")
    r_mwst = item(t["res"][2], "mwst", formula_b=f"=ROUND(B{inc0}*{P['mwst']}/(1+{P['mwst']}),2)")
    r_3a = item(t["res"][3], "p3a",
                formula_c=f'=IF({P["pk"]}="{t["yes"]}",ROUND({P["p3a_pk"]}/12,2),ROUND(MIN(MAX(0,$B${base_row})*{P["p3a_rate"]},{P["p3a_nopk"]}/12),2))')
    r_save = item(t["res"][4], "save")
    assert row == res_total_row
    total(t["tot_res"], "tot_res", first, row - 1)

    # Zusammenfassung
    section(t["sec_sum"])
    assert row == base_row, (row, base_row)
    ti, tf, tv, tr = rows["tot_inc"], rows["tot_fix"], rows["tot_var"], rows["tot_res"]

    def sum_row(label, key, fb, fc, fd, fe, ff, fg, fh, fmt=CHF_FMT):
        nonlocal row
        r = row
        style_cell(ws.cell(row=r, column=1, value=label), bold=True, color=GREY)
        for col, f in zip(range(2, 9), (fb, fc, fd, fe, ff, fg, fh)):
            style_cell(ws.cell(row=r, column=col, value=f), bold=True, color=GREY, fmt=fmt)
        style_cell(ws.cell(row=r, column=9), color=GREY)
        rows[key] = r
        row += 1
        return r

    # Profit base: business income - VAT - business fixed - business variable (B columns)
    sum_row(t["base"], "base",
            f"=D{ti}-B{r_mwst}-B{tf}-B{tv}", None, None,
            f"=G{ti}-E{r_mwst}-E{tf}-E{tv}", None, None, None)
    r_exp = sum_row(t["tot_exp"], "tot_exp",
                    f"=B{tf}+B{tv}+B{tr}", f"=C{tf}+C{tv}+C{tr}", f"=D{tf}+D{tv}+D{tr}",
                    f"=E{tf}+E{tv}+E{tr}", f"=F{tf}+F{tv}+F{tr}", f"=G{tf}+G{tv}+G{tr}",
                    f"=D{row}-G{row}")
    r_diff = sum_row(t["diff"], "diff",
                     f"=B{ti}-B{r_exp}", f"=C{ti}-C{r_exp}", f"=D{ti}-D{r_exp}",
                     f"=E{ti}-E{r_exp}", f"=F{ti}-F{r_exp}", f"=G{ti}-G{r_exp}",
                     f"=G{row}-D{row}")
    sum_row(t["rate"], "rate",
            None, None, f"=IF(D{ti}=0,0,(D{r_3a}+D{r_save}+D{r_diff})/D{ti})",
            None, None, f"=IF(G{ti}=0,0,(G{r_3a}+G{r_save}+G{r_diff})/G{ti})",
            f"=G{row}-D{row}", fmt=PCT_FMT)
    row += 1
    ws.cell(row=row, column=1, value=t["footer"].format(stand=STAND)).font = Font(italic=True, size=8, color="777777")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)

    # Conditional formatting: negative difference = over budget
    ws.conditional_formatting.add(f"H{HDR + 1}:H{row - 2}",
                                  CellIsRule(operator="lessThan", formula=["0"], fill=RED_FILL,
                                             font=Font(color="9C0006", bold=True)))
    ws.freeze_panes = f"B{HDR + 1}"
    ws.print_title_rows = f"{HDR}:{HDR}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True

    # ---------------- Jahresübersicht ------------------------------------------
    wy = wb.create_sheet(t["sheet_year"], 1)
    wy.sheet_view.showGridLines = False
    wy["A1"] = t["year_title"]
    wy["A1"].font = Font(bold=True, size=14, color=DARK)
    wy.merge_cells("A1:P1")
    wy.column_dimensions["A"].width = 38
    for col in range(2, 17):
        wy.column_dimensions[get_column_letter(col)].width = 11
    hdr = [t["sheet_year"]] + t["months"] + [t["year_total"], t["year_avg"], t["year_plan"]]
    for i, h in enumerate(hdr, start=1):
        style_cell(wy.cell(row=3, column=i, value=h), bold=True, color=DARK, white=True, align="center")
    wy.row_dimensions[3].height = 28
    ms = f"'{t['sheet_month']}'"
    plan_refs = [f"={ms}!D{ti}", f"={ms}!D{tf}", f"={ms}!D{tv}",
                 f"={ms}!D{r_tax}+{ms}!D{r_ahv}+{ms}!D{r_mwst}", f"={ms}!D{r_3a}+{ms}!D{r_save}"]
    yr = {}
    r = 4
    for i, lab in enumerate(t["year_rows"]):
        style_cell(wy.cell(row=r, column=1, value=lab))
        for col in range(2, 14):
            style_cell(wy.cell(row=r, column=col), color=GREEN, fmt=CHF_FMT)
        style_cell(wy.cell(row=r, column=14, value=f"=SUM(B{r}:M{r})"), bold=True, color=GREY, fmt=CHF_FMT)
        style_cell(wy.cell(row=r, column=15, value=f"=N{r}/12"), color=GREY, fmt=CHF_FMT)
        style_cell(wy.cell(row=r, column=16, value=plan_refs[i]), color=GREY, fmt=CHF_FMT)
        yr[i] = r
        r += 1
    r_yexp, r_ydiff, r_yrate = r, r + 1, r + 2
    for rr, lab in ((r_yexp, t["year_exp"]), (r_ydiff, t["year_diff"]), (r_yrate, t["year_rate"])):
        style_cell(wy.cell(row=rr, column=1, value=lab), bold=True, color=GREY)
        for col in range(2, 17):
            cl = get_column_letter(col)
            if rr == r_yexp:
                f = f"={cl}{yr[1]}+{cl}{yr[2]}+{cl}{yr[3]}+{cl}{yr[4]}"
                fmt = CHF_FMT
            elif rr == r_ydiff:
                f = f"={cl}{yr[0]}-{cl}{r_yexp}"
                fmt = CHF_FMT
            else:
                f = f"=IF({cl}{yr[0]}=0,0,({cl}{yr[4]}+{cl}{r_ydiff})/{cl}{yr[0]})"
                fmt = PCT_FMT
            style_cell(wy.cell(row=rr, column=col, value=f), bold=True, color=GREY, fmt=fmt)
    wy.conditional_formatting.add(f"B{r_ydiff}:P{r_ydiff}",
                                  CellIsRule(operator="lessThan", formula=["0"], fill=RED_FILL,
                                             font=Font(color="9C0006", bold=True)))
    wy.cell(row=r_yrate + 2, column=1, value=t["footer"].format(stand=STAND)).font = Font(italic=True, size=8, color="777777")
    wy.freeze_panes = "B4"
    wy.page_setup.orientation = "landscape"
    wy.page_setup.paperSize = wy.PAPERSIZE_A4
    wy.page_setup.fitToWidth = 1
    wy.page_setup.fitToHeight = 0
    wy.sheet_properties.pageSetUpPr.fitToPage = True

    # ---------------- Richtwerte content ----------------------------------------
    ws_ref.sheet_view.showGridLines = False
    ws_ref.column_dimensions["A"].width = 52
    ws_ref.column_dimensions["B"].width = 18
    ws_ref.column_dimensions["C"].width = 20
    ws_ref.column_dimensions["D"].width = 14
    ws_ref["A1"] = t["ref_title"]
    ws_ref["A1"].font = Font(bold=True, size=14, color=DARK)
    style_cell(ws_ref["A3"], bold=True, color=DARK, white=True)
    ws_ref["A3"] = t["param_title"]
    style_cell(ws_ref["B3"], bold=True, color=DARK, white=True)
    params = [(t["params"][0], TAX_RATE, PCT_FMT), (t["params"][1], AHV_RATE, PCT_FMT),
              (t["params"][2], MWST_RATE, PCT_FMT), (t["params"][3], t["no"], None),
              (t["params"][4], P3A_MAX_PK, CHF_FMT), (t["params"][5], P3A_MAX_NO_PK, CHF_FMT),
              (t["params"][6], P3A_RATE, PCT_FMT)]
    for i, (lab, val, fmt) in enumerate(params, start=4):
        style_cell(ws_ref.cell(row=i, column=1, value=lab))
        style_cell(ws_ref.cell(row=i, column=2, value=val), color=GREEN, fmt=fmt, align="right")
    dv = DataValidation(type="list", formula1=f'"{t["yes"]},{t["no"]}"', allow_blank=False)
    ws_ref.add_data_validation(dv)
    dv.add("B7")

    br = 13
    ws_ref.cell(row=br - 1, column=1, value=t["bench_title"]).font = Font(bold=True, size=11, color=DARK)
    for i, h in enumerate(t["bench_headers"], start=1):
        style_cell(ws_ref.cell(row=br, column=i, value=h), bold=True, color=DARK, white=True, align="center")
    bench_refs = [
        f"={ms}!D{rows['rent']}",
        f"={ms}!D{r_tax}+{ms}!D{r_ahv}",
        f"={ms}!D{rows['kvg']}+{ms}!D{rows['ins']}",
        f"={ms}!D{rows['food']}",
        f"={ms}!D{rows['mob']}",
        f"={ms}!D{r_3a}+{ms}!D{r_save}",
        f"={ms}!D{rows['leisure']}",
    ]
    for i, ((cat, bench), fref) in enumerate(zip(t["bench"], bench_refs), start=br + 1):
        style_cell(ws_ref.cell(row=i, column=1, value=cat))
        style_cell(ws_ref.cell(row=i, column=2, value=bench), align="center")
        style_cell(ws_ref.cell(row=i, column=3, value=fref), color=GREY, fmt=CHF_FMT)
        style_cell(ws_ref.cell(row=i, column=4, value=f"=IF({ms}!D{ti}=0,0,C{i}/{ms}!D{ti})"),
                   color=GREY, fmt=PCT_FMT)
    note_row = br + len(t["bench"]) + 2
    ws_ref.cell(row=note_row, column=1, value=t["bench_note"]).font = Font(italic=True, size=9, color="555555")
    ws_ref.cell(row=note_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws_ref.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=4)
    ws_ref.row_dimensions[note_row].height = 60
    ws_ref.cell(row=note_row + 2, column=1, value=t["footer"].format(stand=STAND)).font = Font(italic=True, size=8, color="777777")
    ws_ref.page_setup.orientation = "portrait"
    ws_ref.page_setup.paperSize = ws_ref.PAPERSIZE_A4
    ws_ref.page_setup.fitToWidth = 1
    ws_ref.sheet_properties.pageSetUpPr.fitToPage = True

    wb.properties.title = t["title"]
    wb.properties.creator = "Magic Heidi"
    path = out / f"{t['file']}.xlsx"
    wb.save(path)
    return path


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def build_pdf(lang: str, out: Path) -> Path:
    t = L[lang]
    path = out / f"{t['file']}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm,
                            title=t["pdf_title"], author="Magic Heidi", subject=t["title"])
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=15,
                        textColor=colors.HexColor("#" + DARK), alignment=0, spaceAfter=2)
    small = ParagraphStyle("small", parent=ss["Normal"], fontName="Helvetica", fontSize=7.5,
                           textColor=colors.HexColor("#555555"), leading=9.5)
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10)
    cell = ParagraphStyle("cell", parent=body, fontSize=7.8, leading=9.5)
    cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=10,
                        textColor=colors.HexColor("#" + DARK), spaceBefore=6, spaceAfter=3)
    dark = colors.HexColor("#" + DARK)
    sec = colors.HexColor("#" + SECTION)
    grey = colors.HexColor("#" + GREY)
    line = colors.HexColor("#BFBFBF")

    story = [Paragraph(t["pdf_title"], h1)]
    story.append(Paragraph(f"{t['month']}: ____________________ &nbsp;&nbsp;&nbsp; {t['year']}: __________", body))
    story.append(Spacer(1, 4))

    data = [[Paragraph(h, ParagraphStyle("hd", parent=cellb, textColor=colors.white)) for h in t["pdf_headers"]]]
    styles = [
        ("BACKGROUND", (0, 0), (-1, 0), dark),
        ("GRID", (0, 0), (-1, -1), 0.4, line),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white]),
    ]

    def add_section(title):
        data.append([Paragraph(title.upper(), cellb), "", "", "", ""])
        i = len(data) - 1
        styles.append(("BACKGROUND", (0, i), (-1, i), sec))
        styles.append(("SPAN", (0, i), (-1, i)))

    def add_item(label):
        data.append([Paragraph(label, cell), "", "", "", ""])

    def add_total(label):
        data.append([Paragraph(label, cellb), "", "", "", ""])
        i = len(data) - 1
        styles.append(("BACKGROUND", (0, i), (-1, i), grey))

    add_section(t["sec_income"])
    for lab in t["income"]:
        add_item(lab)
    add_total(t["tot_income"])
    add_section(t["sec_fix"])
    for lab in t["fix"]:
        add_item(lab)
    add_total(t["tot_fix"])
    add_section(t["sec_var"])
    for lab in t["var"]:
        add_item(lab)
    add_total(t["tot_var"])
    add_section(t["sec_res"])
    for lab in t["res"]:
        # keep long labels on one printed line: drop the parenthetical detail
        add_item(lab.split(" (")[0] if len(lab) > 52 else lab)
    add_total(t["tot_res"])
    add_section(t["sec_sum"])
    add_total(t["tot_exp"])
    add_total(t["diff"])
    add_total(t["rate"])

    widths = [82 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm]
    tbl = Table(data, colWidths=widths, rowHeights=[8 * mm] + [6.0 * mm] * (len(data) - 1), repeatRows=1)
    tbl.setStyle(TableStyle(styles))
    story.append(tbl)
    story.append(Spacer(1, 6))

    tips = [Paragraph(t["pdf_tips_title"], h2)] + [Paragraph("• " + s, body) for s in t["pdf_tips"]]
    story.append(KeepTogether(tips))
    story.append(Spacer(1, 4))
    story.append(Paragraph(t["footer"].format(stand=STAND), small))

    # Page 2: benchmarks + yearly overview grid
    story.append(PageBreak())
    story.append(Paragraph(t["bench_title"], h1))
    bdata = [[Paragraph(t["bench_headers"][0], ParagraphStyle("hd2", parent=cellb, textColor=colors.white)),
              Paragraph(t["bench_headers"][1], ParagraphStyle("hd3", parent=cellb, textColor=colors.white)),
              Paragraph(t["bench_headers"][2], ParagraphStyle("hd4", parent=cellb, textColor=colors.white)),
              Paragraph(t["bench_headers"][3], ParagraphStyle("hd5", parent=cellb, textColor=colors.white))]]
    for cat, bench in t["bench"]:
        bdata.append([Paragraph(cat, cell), Paragraph(bench, cell), "", ""])
    btbl = Table(bdata, colWidths=[80 * mm, 30 * mm, 40 * mm, 32 * mm], rowHeights=[9 * mm] + [7 * mm] * len(t["bench"]))
    btbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), dark),
                              ("GRID", (0, 0), (-1, -1), 0.4, line),
                              ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(btbl)
    story.append(Spacer(1, 3))
    story.append(Paragraph(t["bench_note"], small))
    story.append(Spacer(1, 10))

    story.append(Paragraph(t["sheet_year"], h1))
    story.append(Paragraph(t["pdf_year_note"], small))
    story.append(Spacer(1, 4))
    ystyle = ParagraphStyle("ycell", parent=cell, fontSize=7, leading=8.5)
    ycellb = ParagraphStyle("ycellb", parent=ystyle, fontName="Helvetica-Bold")
    yhead = ParagraphStyle("yhead", parent=ycellb, textColor=colors.white, alignment=TA_CENTER)
    ydata = [[Paragraph(t["months"][0][:0] or "", yhead)] + [Paragraph(m, yhead) for m in t["months"]] + [Paragraph(t["year_total"], yhead)]]
    ylabels = t["year_rows"] + [t["year_exp"], t["year_diff"], t["year_rate"]]
    for i, lab in enumerate(ylabels):
        ydata.append([Paragraph(lab, ycellb if i >= len(t["year_rows"]) else ystyle)] + [""] * 13)
    ycols = [40 * mm] + [10.4 * mm] * 12 + [17 * mm]
    ytbl = Table(ydata, colWidths=ycols, rowHeights=[8 * mm] + [9 * mm] * len(ylabels))
    yst = [("BACKGROUND", (0, 0), (-1, 0), dark),
           ("GRID", (0, 0), (-1, -1), 0.4, line),
           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    for i in range(len(t["year_rows"]) + 1, len(ylabels) + 1):
        yst.append(("BACKGROUND", (0, i), (-1, i), grey))
    ytbl.setStyle(TableStyle(yst))
    story.append(ytbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(t["footer"].format(stand=STAND), small))

    doc.build(story)
    return path


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_xlsx(path: Path, lang: str) -> None:
    t = L[lang]
    wb = load_workbook(path)
    assert wb.sheetnames == [t["sheet_month"], t["sheet_year"], t["sheet_ref"]], wb.sheetnames
    ws = wb[t["sheet_month"]]
    formulas = [c.value for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("=")]
    assert len(formulas) > 100, len(formulas)
    # Total Einnahmen row: first total after the header
    tot = next(c for row in ws.iter_rows(min_col=1, max_col=1) for c in row if c.value == t["tot_income"])
    assert str(ws.cell(row=tot.row, column=4).value).startswith("=SUM(D"), ws.cell(row=tot.row, column=4).value
    assert ws.cell(row=tot.row, column=4).number_format == CHF_FMT
    wy = wb[t["sheet_year"]]
    assert wy["N4"].value == "=SUM(B4:M4)", wy["N4"].value
    wr = wb[t["sheet_ref"]]
    assert wr["B4"].value == TAX_RATE and wr["B8"].value == P3A_MAX_PK and wr["B9"].value == P3A_MAX_NO_PK
    assert ws.conditional_formatting, "missing conditional formatting"
    print(f"  ok  {path.name}: {len(formulas)} formulas in {t['sheet_month']}, {path.stat().st_size:,} bytes")


def validate_pdf(path: Path, lang: str) -> None:
    from pypdf import PdfReader  # optional; fall back to size check
    r = PdfReader(str(path))
    text = "".join(p.extract_text() or "" for p in r.pages)
    probe = {"de": "Säule 3a", "fr": "Réserve d'urgence", "it": "Mobilità", "en": "Pillar 3a"}[lang]
    assert probe in text, f"{probe!r} not found in PDF text"
    print(f"  ok  {path.name}: {len(r.pages)} pages, umlaut probe {probe!r} found, {path.stat().st_size:,} bytes")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(L))
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    here = Path(__file__).resolve().parent.parent
    out = Path(a.out) if a.out else here.parent / "mh-landing" / "public" / "downloads"
    out.mkdir(parents=True, exist_ok=True)
    for lang in a.langs:
        print(f"[{lang}]")
        x = build_xlsx(lang, out)
        validate_xlsx(x, lang)
        p = build_pdf(lang, out)
        try:
            validate_pdf(p, lang)
        except ImportError:
            print(f"  ok  {p.name}: {p.stat().st_size:,} bytes (pypdf not installed, text probe skipped)")


if __name__ == "__main__":
    main()
