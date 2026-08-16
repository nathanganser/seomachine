# SE Ranking Snapshot Comparison — magicheidi.ch (CH database)

**Snapshot date:** 2026-08-16 · **Baseline:** 2026-08-01 (`audits/seranking-2026-08-01/raw/`) · **Trend anchor:** June 2026 (from 12-month history series)

Raw data: `audits/seranking-2026-08-16/raw/` (overview, history, 10k keyword rows, backlinks summary + authority).

Subscription note: status shows **"expired"** (period ended 2026-08-16 10:54), but the API still served data. `units_left` read 3,022,000 both before and after the pull — the counter did not decrement (likely stale on an expired plan).

## 1. Keywords, buckets, traffic

| Metric | June 2026 | Aug 1 2026 | Aug 16 2026 | Δ vs Aug 1 | Δ vs June |
|---|---:|---:|---:|---:|---:|
| Total CH keywords | 7,860 | 9,028 | 9,537 | +509 | +1,677 |
| Top 1–5 | 1,274 | 1,532 | 1,542 | +10 | +268 |
| Top 6–10 | 992 | 1,232 | 1,342 | +110 | +350 |
| Top 11–20 | 1,581 | 1,772 | 1,961 | +189 | +380 |
| Top 21–50 | 3,565 | 4,465 | 4,583 | +118 | +1,018 |
| Top 51–100 | 3,320 | 2,658 | 3,199 | +541 | −121 |
| Est. traffic (traffic_sum) | 2,931 | 3,600 | 4,537 | **+937 (+26%)** | +1,606 (+55%) |
| Traffic value (price_sum) | CHF 2,336 | CHF 2,036 | CHF 3,203 | +CHF 1,167 (+57%) | +CHF 867 |

New/lost (overview month-over-month counters): Aug 16 snapshot shows **4,539 new / 3,569 lost / 1,325 up / 1,486 down** (vs Aug 1 snapshot's 7,122 new / 6,205 lost / 1,203 up / 674 down — July was a much noisier month, consistent with the default-locale switch).

## 2. Backlinks

| Metric | Aug 1 | Aug 16 | Δ |
|---|---:|---:|---:|
| Backlinks | 437 | 462 | +25 |
| Referring domains | 203 | 221 | +18 |
| Dofollow backlinks | 339 | 357 | +18 |
| Dofollow refdomains | 150 | 165 | +15 |
| Domain Trust (domain_inlink_rank) | 51 | **52** | +1 |
| Page Trust homepage (inlink_rank) | 7 | 7 | 0 |

## 3. Money-keyword movers (Aug 1 → Aug 16)

Families matched (substring): buchhaltungssoftware, buchhaltungsprogramm, bexio, rechnungsvorlage, rechnungsprogramm, rechnung schreiben, mwst, uid, doppelte buchhaltung, erfolgsrechnung, klara, logiciel facturation, modèle facture, buchhaltung für selbständige, einzahlungsschein. ~795 matching keyword rows per snapshot. Best position per keyword. Top ~40 by volume:

| Keyword | Vol | Aug 1 | Aug 16 | URL now | Note |
|---|---:|---:|---:|---|---|
| uid | 8,000 | – | 14 | /de/uid-nummer-schweiz | NEW |
| uid register | 8,000 | – | 9 | /uid-nummer-beantragen | NEW |
| mwst schweiz | 4,400 | – | 40 | /de/mwst-registrierung | NEW |
| uid nummer | 2,400 | – | **1** | /uid-nummer-beantragen | NEW |
| mwst rechner | 1,900 | 16 | 18 | /de/tools/vat-calculator-switzerland | |
| erfolgsrechnung | 1,000 | 26 | – | (lost from top-100/pull) | LOST |
| einzahlungsschein | 990 | – | 14 | /einzahlungsschein-erstellen | NEW |
| einzahlungsschein erstellen | 910 | 29 | 23 | /de/qr-rechnung-erstellen | +6 |
| doppelte buchhaltung | 590 | 17 | 18 | /de/doppelte-buchhaltung-schweiz | |
| uid schweiz | 590 | – | 9 | /de/uid-nummer-schweiz | NEW |
| mwst id | 590 | 37 | 16 | /de/uid-nummer-schweiz | **+21** |
| schweiz uid | 590 | – | 18 | /de/uid-nummer-schweiz | NEW |
| qr(-)einzahlungsschein erstellen gratis | 590 | 10 | 9 | /qr-rechnung-erstellen | |
| buchhaltungssoftware schweiz | 590 | 11 | 18 | /buchhaltungssoftware | **−7** |
| schweizer buchhaltungssoftware | 590 | 11 | 12 | /buchhaltungssoftware | |
| mwst-nummer | 480 | 20 | 12 | /de/uid-nummer-schweiz | +8 |
| mwst sätze | 480 | 1 | 43 | /vat-rates | **−42** |
| rechnungsvorlage schweiz | 480 | 8 | – | (lost from top-100/pull) | LOST |
| mwst nummer | 480 | 21 | 11 | /de/uid-nummer-schweiz | +10 |
| uid number | 480 | – | 9 | /uid-nummer-schweiz | NEW |
| rechnungsvorlagen schweiz | 480 | 9 | 7 | /de/rechnungsvorlage | |
| uid nr | 480 | – | **1** | /uid-nummer-beantragen | NEW |
| mwst berechnen | 390 | 15 | 23 | /de/tools/vat-calculator-switzerland | **−8** |
| erfolgsrechnung und bilanz | 390 | 26 | 19 | /de/erfolgsrechnung-schweiz | +7 |
| qr-einzahlungsschein | 390 | 46 | 7 | /einzahlungsschein-erstellen | **+39** |
| mwst berechnung | 390 | 23 | 24 | /de/tools/vat-calculator-switzerland | |
| bilanz und erfolgsrechnung | 390 | 37 | 39 | /erfolgsrechnung-schweiz | |
| qr einzahlungsschein | 390 | 43 | 29 | /de/qr-rechnung-erstellen | +14 |
| berechnung mwst | 390 | 33 | 27 | /de/tools/vat-calculator-switzerland | +6 |
| mwst-nummer schweiz | 320 | 1 | 8 | /de/uid-nummer-schweiz | **−7** |
| was ist eine uid nummer | 320 | – | 13 | /de/uid-nummer-schweiz | NEW |
| mwst nummer schweiz | 320 | 10 | **1** | /de/uid-nummer-schweiz | +9 |
| ubs einzahlungsschein erstellen | 320 | 5 | 4 | /de/banks/ubs | |
| buchhaltungssoftware | 320 | 30 | 37 | /de/buchhaltungssoftware | **−7** |
| buchhaltungsprogramm | 320 | 69 | – | (lost from top-100/pull) | LOST |
| rechnung schreiben | 320 | 1 | 6 | /de/rechnung-schreiben-schweiz | **−5** |
| uid nummer suchen schweiz | 260 | – | 6 | /de/uid-nummer-schweiz | NEW |
| bexio buchhaltung | 260 | – | 19 | /blog/bexio-tutorial-ausgaben-erstellen… | NEW |
| mwst-nummer schweiz suchen | 260 | – | 5 | /de/uid-nummer-schweiz | NEW |
| aktueller mwst satz schweiz | 260 | – | 13 | /vat-rates | NEW |
| post einzahlungsschein erstellen | 260 | 28 | – | (lost from top-100/pull) | LOST |

Additional notable movers (vol ≥ 100, |Δ| ≥ 3): mwst nummer suchen schweiz 28→6, mwst-register schweiz 23→6, mwst register schweiz 27→5, uid mwst 42→1, buchhaltungsprogramm gratis 36→20, anmeldung mwst schweiz 23→14, buchhaltungsprogramm schweiz 20→16, mwst schweiz berechnen 19→11, einzahlungsschein erstellen raiffeisen 27→15, rechnung schreiben vorlage 29→23, excel rechnungsvorlage 22→17. Regressions: modèle facture 20→33, mwst berechnen schweiz 15→20, mwst saldosteuersatz 15→21, buchhaltungsprogramme schweiz 12→18, erfolgsrechnung beispiel 11→17, dreistufige erfolgsrechnung 45→50.

The entire UID/MWST-Nummer satellite cluster (`/de/uid-nummer-schweiz`, `/uid-nummer-beantragen`, `/mwst-nummer-schweiz`) is the standout: dozens of new top-10 rankings including #1 for "uid nummer" (2,400) and "uid nr" (480), plus a huge suchen/register long-tail. This is the August traffic/value jump.

Caveat: family matching by substring means "uid" also catches unrelated keywords containing "guide"/"liquidität" in the ~795 totals; the table itself was manually sanity-checked.

## 4. Locale-leak check (/de/ URLs)

Method: keyword rows where the ranking URL contains `/de/` (rows encode full URL in `url` field; best-position row per keyword; both snapshots pulled with same 10-page × 1000 method).

| Metric | Aug 1 | Aug 16 | Δ |
|---|---:|---:|---:|
| Rows ranking with /de/ URL (any position) | 8,361 | 7,311 | **−1,050** |
| Rows ranking with /de/ URL in top-30 | 4,441 | 3,865 | **−576** |

Google is progressively swapping /de/ URLs for the bare (German-default) URLs, but ~53% of top-30 rankings still resolve to /de/. Note: the previously reported "1,601 in top-30" baseline figure was computed with a different method/filter; the numbers above use one consistent method on both raw snapshots and are the ones to track going forward.

## 5. Anomalies & caveats

- **Subscription expired today** (2026-08-16 10:54) yet API still returns data and units_left is frozen at 3,022,000. Renew before the 2026-09-01 re-measure or data access may stop.
- Both keyword pulls are **capped at 10,000 rows** (10 pages × 1,000) while total keyword counts are 9,028/9,537 — rows are keyword+URL pairs, so "LOST" money keywords may have merely fallen below the pull cutoff or out of top-100, not off Google entirely. `erfolgsrechnung` (1,000 vol, was 26), `rechnungsvorlage schweiz` (480, was 8) and `buchhaltungsprogramm` (320, was 69) deserve a manual SERP check.
- **`mwst sätze` 1 → 43** on /vat-rates is the single biggest regression and looks like a URL/locale swap casualty (the keyword now also surfaces as "aktueller mwst satz schweiz" NEW at 13 on the same page). Check which URL variant Google indexes for /vat-rates.
- **`rechnung schreiben` 1 → 6** and **`mwst-nummer schweiz` 1 → 8**: lost two #1 spots while gaining a new #1 on "mwst nummer schweiz" (unhyphenated) — likely SERP churn between /de/ and bare variants, worth watching at the 2026-09-01 re-measure.
- Position buckets sum to more than keywords_count in both snapshots (SE Ranking counts keyword-URL pairs in buckets); comparisons are consistent since the same definition applies to all three dates.
