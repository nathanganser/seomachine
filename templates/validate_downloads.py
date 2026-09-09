"""Re-open every generated download and sanity-check it (run with the seomachine venv)."""
import sys
from pathlib import Path

import openpyxl
from docx import Document
from pypdf import PdfReader

DL = Path("/Users/nathanganser/Documents/Development/mh-landing/public/downloads")
FILES = [
    "Lieferschein_Vorlage_Schweiz.docx", "Lieferschein_Vorlage_Schweiz.xlsx", "Lieferschein_Vorlage_Schweiz.pdf",
    "Kassenbuch_Vorlage_Schweiz.xlsx", "Kassenbuch_Vorlage_Schweiz.pdf", "Kassenbuch_Vorlage_Schweiz.docx",
    "Arbeitsrapport_Vorlage_Schweiz.xlsx", "Arbeitsrapport_Vorlage_Schweiz.docx", "Arbeitsrapport_Vorlage_Schweiz.pdf",
    "Zahlungserinnerung_Vorlage_Schweiz.docx", "Zahlungserinnerung_Vorlage_Schweiz.pdf",
    "Spesenabrechnung_Vorlage_Schweiz.xlsx", "Spesenabrechnung_Vorlage_Schweiz.pdf",
]
UML = "äöüÄÖÜ"
ok = True
for name in FILES:
    p = DL / name
    size = p.stat().st_size
    if name.endswith(".docx"):
        d = Document(p)
        text = "\n".join(x.text for x in d.paragraphs) + "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
        info = f"{len(d.paragraphs)} paras, {len(d.tables)} tables"
    elif name.endswith(".xlsx"):
        wb = openpyxl.load_workbook(p)
        formulas = sum(1 for ws in wb.worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("="))
        text = "".join(str(c.value) for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value)
        info = f"sheets={wb.sheetnames}, {formulas} formulas"
    else:
        r = PdfReader(p)
        text = "".join(pg.extract_text() for pg in r.pages)
        info = f"{len(r.pages)} pages, title={r.metadata.get('/Title')!r}"
    has_uml = any(ch in text for ch in UML)
    if not has_uml:
        ok = False
    print(f"{'OK ' if has_uml else 'FAIL'} {name:45s} {size:7d} bytes  {info}  umlauts={has_uml}")
sys.exit(0 if ok else 1)
