# SE Ranking Audit — magicheidi.ch — 2026-08-01

Definitive audit from the 2026-08-01 SE Ranking pull (Google CH database, all data in `audits/seranking-2026-08-01/`; raw API responses in `raw/`). Follows up on `audits/cannibalization-review-2026-07-16.md` (round 2 cleanup) and the 2026-07-16 default-locale switch (bare URLs = German, `/en` = English).

---

## 1. Executive summary

| Metric | magicheidi.ch (2026-08-01) |
|---|---|
| Organic keywords (CH) | 9,028 (top 1–5: 1,532 · top 6–10: 1,232 · top 11–20: 1,772 · top 21–50: 4,465 · top 51–100: 2,658) |
| Est. organic traffic | ~3,600 visits/mo (value $2,036/mo) |
| Keywords new / lost (July 2026) | **+7,122 / −6,205** |
| Backlinks / referring domains | 437 / **203** |
| Domain Trust (SE Ranking) | 51 (bexio 83, klara 75, banana 71, abaninja 57, cashctrl 56) |
| Site audit score | 80/100 — 523 errors, 2,565 warnings across 1,500 crawled pages |

**Three headline risks:**

1. **Traffic concentration.** The top 2 pages are **53.5% of all organic traffic** — `/fr/feiertage/waadt` (30.8%, 1,109 visits) and `/de/feiertage/zurich` (22.6%, 815 visits). Both are informational holiday/school-vacation pages with near-zero purchase intent, and both are seasonal (Easter/Pentecost/vacances scolaires spikes). The business-relevant pages (buchhaltungssoftware, rechnungsprogramm, QR tools) collectively carry a small fraction of traffic. A single Google update or a competitor calendar page could halve reported traffic without touching a single money keyword.
2. **Keyword churn is migration noise, not real volatility.** +7,122 new / −6,205 lost in one month looks alarming, but it is the 2026-07-16 default-locale switch: `/de/slug` rankings are being re-attributed to bare `/slug` URLs as Google recrawls. Underlying trajectory is healthy: 5,723 kw (Dec 2025) → 7,232 (Mar 2026) → 9,028 (Jul 2026), with top 1–5 up from 722 to 1,532 over the same period. Do not react to churn dashboards until ~2026-09-01.
3. **Authority, not content, is the ceiling.** 203 referring domains vs bexio 4,559, banana 1,488, klara 1,446. On money SERPs (buchhaltungssoftware schweiz, doppelte buchhaltung) we sit pos 11–20 behind DT-70+ domains with the content problem already solved. This matches the 2026-07-23 buchhaltungsprogramm-schweiz finding: relevance is largely fixed; links are not.

---

## 2. Findings by theme

### 2a. Keyword cannibalization — 106 groups, most already fixed

Source: `cannibalization.csv` (106 groups where 2+ URLs rank for the same keyword). **~21 of 106 groups involve URLs that already 301/308-redirect** — SE Ranking is showing pre-redirect SERP data. Verified redirecting since the 2026-07-16 round-2 cleanup: `/tools/qr-invoice-generator`, `/understanding-profit-and-loss-accounts`, `/fr/public-holidays-vaud-2026`. Do not re-litigate these.

Top groups by volume, classified:

| Group (max vol) | URLs | Status |
|---|---|---|
| erfolgsrechnung (1,000) | `/erfolgsrechnung-schweiz` vs `/understanding-profit-and-loss-accounts` | **FIXED** — loser redirects; recrawl lag |
| festività svizzera / feste svizzera (590) | `/it/feiertage` vs `/it/feiertage/tessin` | **OPEN** — IT national vs cantonal holiday pages compete (pos 1 & 7 vs 27) |
| qr einzahlungsschein erstellen gratis (590) | `/qr-rechnung-erstellen` vs `/tools/qr-invoice-generator` | **FIXED** — tool URL redirects |
| qr code generator raiffeisen (590) | same pair | **FIXED** |
| vacances scolaires 2025 suisse (590) | `/fr/feiertage/waadt` vs `/fr/public-holidays-vaud-2026` | **FIXED** — old slug redirects |
| rechnungsvorlage(n) schweiz (480) | `/rechnung-schreiben-schweiz` vs `/rechnungsvorlage` | **REVIEWED 2026-07-16, leave as is** — intent split; right page wins (pos 8–9 vs 30+) |
| giorni festivi ticino / festività ticino (390) | `/it/feiertage` vs `/it/feiertage/tessin` | **OPEN** — same IT pair |
| bilanz erfolgsrechnung (390) | erfolgsrechnung pair | **FIXED** (redirect) |
| café working / cafes working (320) | `/coworking/luzern` vs `/coworking/zurich` | **OPEN but low value** — generic term, city pages both rank; harmless |
| inscription tva (260) | `/fr/mwst-registrierung/genf` vs `/fr/mwst-registrierung/waadt` | **OPEN** — FR cantonal MWST pages both chase the generic FR term; the national `/fr/mwst-registrierung` should own it |
| ubs qr code erstellen (260) | `/banks/ubs` vs `/tools/qr-invoice-generator` | **FIXED** (tool redirects); `/banks/ubs` correctly wins at pos 3 |
| self employed (260) | `/sarl-vs-self-employed` vs `/unemployment-benefits…` | **OPEN, ignore** — generic EN head term, neither page targets it |
| anmeldung mwst schweiz (210) | `/mwst-registrierung` vs `/mwst-registrierung/st-gallen` | **REVIEWED 2026-07-16** — st-gallen ranking is "a feature not a bug"; monitor only |
| feiertage winterthur (210) | `/feiertage/freiburg` vs `/feiertage/zurich` | **OPEN, minor** — Freiburg page leaking onto a Zürich-area query; check internal anchors |
| registre tva suisse (170) | `/fr/mwst-registrierung` vs `/fr/mwst-registrierung/waadt` | **OPEN** — same FR pattern as inscription tva |

**Interpretation:** the July cleanup worked; the remaining genuinely-open cannibalization is concentrated in **two patterns**: (1) the IT `feiertage` national-vs-Tessin pair (the exact pattern fixed for `mwst-registrierung/bern` on 2026-07-16 — the cantonal page likely carries national-scope content), and (2) FR cantonal MWST pages (genf/waadt) outranking their own national pillar on generic FR registration terms. Both are boundary/internal-linking fixes, not merges.

### 2b. Legacy `/de/` URLs still ranking — 1,601 keywords, recrawl lag not breakage

Source: `locale_leaks.csv` (1,601 top-30 keywords where the ranking URL still carries the `/de/` prefix). The redirects themselves are **confirmed working** (`/de/*` → bare `/*` via 308, verified live 2026-07-18/19 per `context/internal-links-map.md`). This is Google recrawl lag — expected 4–8 weeks after a URL migration — compounded by **955 pages still internally linking to 3XX redirect URLs** (site audit, section 2f), which keeps feeding Google the old paths.

Top legacy-URL keywords by traffic:

| Keyword | Pos | Volume | Traffic | Legacy URL |
|---|---|---|---|---|
| ostern 2026 | 28 | 40,500 | 112 | /de/feiertage/zurich |
| pfingsten 2026 | 20 | 18,700 | 91 | /de/feiertage/zurich |
| ostern 2026 schweiz | 7 | 5,400 | 73 | /de/feiertage/zurich |
| schulferien zürich 2026 | 28 | 14,800 | 69 | /de/feiertage/zurich |
| feiertage 2026 | 1 / 6 | 5,700 | 55+53 | /de/feiertage/zurich |
| auffahrt 2026 | 12 | 20,100 | 54 | /de/feiertage/zurich |
| feiertage zürich | 8 | 3,600 | 48 | /de/feiertage/zurich |
| brutto netto rechner schweiz | 21 | 3,200 | 43 | /de/brutto-netto-rechner-schweiz |
| qr rechnung erstellen | 16 | 1,500 | 43 | /de/tools/qr-invoice-generator |
| rechnung | 1 | 3,600 | 32 | /de/rechnung-schreiben-schweiz |
| ubs qr(-)rechnung erstellen | 4 | 480 | 23×2 | /de/banks/ubs |

URLs with the most legacy keywords: `/de/feiertage/zurich` (329), `/de/stundenlohn-berechnen-schweiz` (113), `/de/rechnung-schreiben-schweiz` (89), `/de/banks/ubs` (61), `/de/brutto-netto-rechner-schweiz` (58), `/de/working-hours-in-switzerland` (50), `/de/quittung-vorlage-schweiz` (47), `/de/rechnungsvorlage` (45).

**Interpretation:** no ranking loss is visible from the migration (positions held through the URL swap). Action needed is not on redirects but on (1) the 955 internal links pointing at redirect URLs (fixable in mh-landing), and (2) patience — re-measure legacy-URL share on 2026-09-01; it should fall below ~400 keywords. Escalate only if positions on the affected pages start dropping.

### 2c. Quick wins — 638 keywords at position 4–20 (vol ≥ 50)

Source: `quick_wins.csv`. Intent mix is lopsided: **~82% informational** (523 of 638), dominated by the feiertage pages. Split matters — the informational wins grow the traffic number, the BOFU wins grow revenue.

**BOFU / money terms in striking range (prioritize these):**

| Keyword | Pos | Volume | Difficulty | URL |
|---|---|---|---|---|
| schweizer buchhaltungssoftware | 11 | 590 | 26 | /buchhaltungssoftware |
| buchhaltungssoftware schweiz | 11 | 590 | 13 | /buchhaltungssoftware |
| doppelte buchhaltung | 17 | 590 | 16 | /doppelte-buchhaltung-schweiz |
| bexio api | 6 | 590 | 13 | /alternative/bexio |
| rechnungsvorlage(n) schweiz | 8–9 | 480 | 7–8 | /rechnungsvorlage |
| rechnung schreiben | 18 | 320 | 19 | /rechnung-schreiben-schweiz |
| vorlage rechnung schweiz | 7 | 210 | 7 | /rechnungsvorlage |
| payrolling switzerland | 7 | 170 | 14 | /payrolling-for-freelancers |
| modèle facture | 20 | 170 | 19 | /fr/rechnungsvorlage |
| buchhaltungsprogramm(e) schweiz | 12–20 | 140 | 17 | /buchhaltungssoftware |
| buchhaltungsprogramm schweiz gratis | 13–18 | 140 | 11 | /buchhaltungssoftware |
| bexio alternative | 5 | 140 | 14 | /alternative/bexio |
| rechnungsvorlage excel | 17 | 140 | 10 | /rechnungsvorlage |
| small invoice | 7 | 110 | 43 | /alternative/smallinvoice |

**Top informational wins by traffic upside** (all feiertage/calculator pages): vacances scolaires vaud 2025 (pos 11, 18.1k vol), pfingsten 2026 (20, 18.7k), auffahrt 2026 (12, 20.1k), ostern 2026 schweiz (7, 5.4k), feiertage 2026 (6, 5.7k), qr rechnung erstellen (16, 1.5k), paques 2026 (9, 8.1k), vaudtax (6, 5.7k), vacances scolaires fribourg 2026 (12, 2.9k), vacances scolaires 2026 (15, 6.6k).

**Interpretation:** the `/buchhaltungssoftware` pillar sits at pos 11–20 across the entire buchhaltungssoftware/-programm keyword family — one page, ~10 quick-win keywords, all blocked by the same authority gap (section 2g). The `/rechnungsvorlage` family (difficulty 7–10, pos 7–17) is the cheapest BOFU win on the list. The informational upside is real traffic but concentrates risk further into the feiertage pages (section 1, risk 1) — take it, but don't count it as strategy.

### 2d. Striking distance vs bexio / klara / banana / cashctrl

Source: `striking_distance_*.csv` (keywords where we rank 11–30 and the competitor ranks top 10). Volume-sorted highlights:

| Keyword | Vol | Us | Them | Competitor URL |
|---|---|---|---|---|
| dropshipping | 3,600 | 25 | bexio 1 | blog/dropshipping |
| brutto netto rechner schweiz | 3,200 | 21 | bexio 6 | brutto-netto-rechner |
| erfolgsrechnung | 1,000 | 26 | bexio 2 / cashctrl 2 | erfolgsrechnung-mehrstufig |
| rechnungen | 880 | 14 | bexio 1 | rechnung |
| vat number schweiz | 590 | 19 | bexio 1 | mwst |
| buchhaltungssoftware schweiz | 590 | 11 | bexio 1 / banana 2 / cashctrl 3 | product pages |
| doppelte buchhaltung | 590 | 17 | bexio 1 / banana 8 / klara 10 | doppelte-buchhaltung |
| arbeitszeiten schweiz | 590 | 11 | bexio 1 | blog/arbeitsstunden-pro-monat |
| mwst-nummer | 480 | 20 | bexio 3 | blog/uid |
| qr(-)iban | 390 | 16–18 | banana 1/8 | node/9387 |
| vorlage rechnung (word) | 23–30 | 170–390 | klara 7–10 | blog/rechnung-vorlage |
| buchhaltungsprogramm schweiz | 140 | 20 | klara 1 / cashctrl 4 | buchhaltungsprogramm |
| gratis buchhaltungsprogramm schweiz | 140 | 21 | cashctrl 1 | topics/free |
| logiciel (de) facturation | 90–110 | 13–24 | klara 1 | fr-ch/logiciel-facturation |
| einfache buchhaltung | 210 | 23 | banana 5 | banana.ch/de |

**Interpretation:** three distinct battles. (1) **The buchhaltung cluster** (buchhaltungssoftware/-programm, doppelte buchhaltung, erfolgsrechnung, einfache buchhaltung) — every major competitor is top-10 with us at 11–26; this is the August campaign battleground and is authority-limited. (2) **CashCtrl owns "gratis/kostenlos"** modifiers with its free tier — Magic Heidi's forever-free tier (3 invoices, all features) is the counter-angle, currently under-articulated on `/buchhaltungssoftware`. (3) **Klara's FR flank** (`logiciel facturation`, pos 1 vs our 13–24 on `/fr/rechnungsprogramm`) is the most neglected: FR is 20% of the market and the FR page needs the same treatment the DE pillar got in July. `dropshipping` (3,600 vol) is high-volume but off-ICP — deprioritize.

### 2e. True content gaps — UID / MWST / Lohn themes

Source: `gap_*.csv` (competitor top-20, us absent), filtered for non-brand, ICP-relevant themes. Excluded: competitor-brand terms (moneyhouse, clockodo, startups.ch), Klara's POS/webshop/Google-reviews surface, generic finance vocabulary (ebitda, stakeholder, erp).

| Theme | Keywords (vol) | Who ranks | Note |
|---|---|---|---|
| **UID** | uid (8,000; bexio 6, klara 12) · uid register (8,000; bexio 5) · uid nummer (2,400; bexio 8) · ust nummer (590) · uid number (480) | bexio blog/uid, klara support | **UID satellite pages shipped late July 2026 (PR #116–118 wave) — too new to rank in this pull.** Do not create new pages; re-check 2026-09-01. |
| **MWST filing/rates** | mehrwertsteuer schweiz (5,700; bexio 15) · mwst schweiz (5,400) · mwst (4,400; banana 5) · mwst online (2,900; banana 7) · mwst abrechnung (1,300; banana 1) · mwst online einreichen (990, difficulty 9!) · mwst satz (480) · mwst fristverlängerung (260; klara 1) | banana apps pages, bexio /mwst, klara blog | Open queue item from the July visibility plan (MWST cluster). `/mwst-freelancer` + `/mwst-registrierung` exist but target registration, not **filing/rates/deadlines**. Gap pages: MWST-Abrechnung guide (online einreichen, Fristverlängerung, Saldosteuersatz worked examples), MWST-Sätze table page (snippet format). |
| **Lohn** | lohnrechner schweiz (8,100; bexio 20) · lohnabrechnung (1,800; klara 16) · lohnausweis (1,900; bexio 1) · lohnabrechnung stundenlohn (70; cashctrl 3) · beispiel lohnabrechnung schweiz (170; cashctrl 8) | bexio lohn-berechnen, cashctrl tutorials | We already have `/brutto-netto-rechner-schweiz` (pos 21 for "lohnrechner brutto-netto schweiz") and `/stundenlohn-berechnen-schweiz` — extend these rather than new pages: add Lohnabrechnung-Muster + Lohnausweis sections. Pure payroll (lohnausweis for employers) is edge-of-ICP; keep it satellite-level. |
| **TVA (FR)** | décompte tva (590; banana 6) · taux tva suisse variants (390×3; banana 10–13) | banana FR apps pages | FR mirror of the MWST cluster — banana ranks with thin tool pages; a proper FR guide can win. |

**Interpretation:** the gap list confirms the open queue from `project_seo_visibility_plan_2026_07.md` rather than revealing new themes. Priority order: MWST filing cluster (DE) → TVA (FR) → Lohn extensions. UID is already in flight; measure before touching.

### 2f. Technical site audit — 80/100, 523 errors

Source: `raw/audit_report.json`, `raw/audit_issue_pages.json` (1,500 pages crawled 2026-08-01).

| Severity | Issue | Count | Detail |
|---|---|---|---|
| **Error** | **5XX pages** | **8** | Production 500s on live blog URLs: `/blog/werkvertrag-schweiz`, `/blog/verzugszins-schweiz`, `/blog/scheinselbststaendigkeit-schweiz`, `/blog/ratenzahlung-schweiz`, `/blog/kontenrahmen-kmu-schweiz`, `/blog/betreibung-schweiz`, `/pt/blog/mahngebuehren-schweiz`, `/fr/blog/kosmetik-studio-rechnung-schweiz`. 7 of these are also in the XML sitemap. **Fix first — these are indexable pages erroring.** |
| Error | No inbound internal links (orphans) | 369 | Plus 475 pages with exactly one inlink. Likely locale variants + blog long-tail missed by nav/related-links. |
| Error | Duplicate titles | 34 | e.g. `/start` vs `/en/start` vs `/sq/start` vs `/sr/start` (note: `sq`/`sr` locale paths shouldn't exist at all — 6 configured locales), tutorial pages duplicated across es/fr. |
| Error | Hreflang → 3XX/4XX/5XX | 16 | e.g. the `/qr-iban-example` hreflang set points at dead/redirecting locale variants. +17 pages missing return links, 59 hreflang↔HTML-lang mismatches, 395 multiple-language-code notices — hreflang graph still reflects pre-migration URLs in places. |
| Error | 4XX pages | 16 | Plus 27 images 404ing. |
| Error | Duplicate content | 6 | `/en|fr|it|es|pt/kostenvoranschlag-schweiz` — the page is documented as **German-only** in internal-links-map; the locale variants serving identical content should 301 or noindex. |
| Warning | **Internal links to 3XX redirects** | **955** | Biggest lever: sustains the legacy-URL lag (2b). Sample sources: `/integrations/shopify|stripe|amazon|etsy`, `/alternative/klara`. |
| Warning | Temporary redirects (302/303/307) | 92 | Should be 301/308 where permanent. |
| Warning | Images too big | 233 | Performance, not rankings-critical. |
| Warning | H1 missing/empty | 30 | |

**Interpretation:** the 8 production 500s and the sitemap serving them are the only genuinely urgent items. The 955 redirect-links + hreflang errors are the same root cause (default-locale migration leftovers) and are mechanical fixes in mh-landing. Orphans (369) deserve a pass through the internal-linker agent once the redirect-link cleanup lands, so new links point at canonical URLs.

### 2g. Backlink authority gap + link-spam exposure

Source: `raw/backlinks_summary*.json`, `raw/backlinks_refdomains.json`.

| Domain | Domain Trust | Ref domains | Backlinks |
|---|---|---|---|
| bexio.com | 83 | 4,559 | 1,477,009 |
| klara.ch | 75 | 1,446 | 19,360 |
| banana.ch | 71 | 1,488 | 7,015 |
| abaninja.ch | 57 | 452 | 4,977 |
| cashctrl.com | 56 | 458 | 3,402 |
| **magicheidi.ch** | **51** | **203** | **437** |

We are last on every axis — 4.4% of bexio's referring domains, 14% of klara's. This is the binding constraint on every pos-11–20 money keyword in sections 2c/2d.

**Spam exposure (sample from 203 refdomains):** a cluster of DT ≤ 5 and off-topic domains, several first seen in the last 60 days:

- `sp-escort-frankfurt.de` (first seen 2026-07-31), `buzzvoria.site` (DT 0), `www.darkhackernews.com`, `yzyyz.net`, `animermvblimdcsx.blogspot.com` / `aldograflimd.blogspot.com`, `lavoro.gaveine.com`, `ipaybetter.com`, `thepristinechurch.org` (DT 1, 9 links), `svajc.com`
- Oddities needing eyeballs, not knee-jerk disavow: `www.xn--buchhaltung-fr-selbstndige-0hc77d.ch` (punycode "buchhaltung-für-selbständige.ch", DT 1, **20 dofollow links, first seen 2026-07-30**) and `xn--grnder-schweiz-hsb.ch` ("gründer-schweiz.ch", 12 links) — punycode Swiss domains could be legit niche sites or PBN; verify manually before deciding.

At 203 refdomains, ~15–20 junk domains are a meaningful share of the profile. **Recommendation: manual disavow review (human action, not automatable)** — export full refdomain list, verify the punycode domains, disavow the escort/casino/hacked-blog tier. Legitimate anchors to protect: apps.apple.com, justuseapp.com, informatik.ch, import.ch, smartpurse (5 domains), buchhaltung.ch, einzly.ch.

---

## 3. Prioritized recommendations

### A. Fix PR (mh-landing) — mechanical, ship this week

| # | Action | Source finding |
|---|---|---|
| 1 | **Fix the 8 production 500s** (6 DE blog + 1 PT + 1 FR blog URL); remove from sitemap if intentionally gone, else repair rendering | 2f |
| 2 | **Rewrite the 955 internal links pointing at 3XX URLs** to canonical destinations (starts with `/integrations/*`, `/alternative/*` templates); converts 2b from "wait" to "done" | 2b, 2f |
| 3 | Repair hreflang: 16 dead/redirecting targets, 17 missing return links, kill phantom `sq`/`sr` locale paths, align hreflang↔HTML lang | 2f |
| 4 | 301/noindex the 5 non-DE `/kostenvoranschlag-schweiz` locale variants (documented German-only) | 2f |
| 5 | Dedupe the 34 duplicate titles; convert the 92 temporary redirects to permanent where appropriate | 2f |
| 6 | Cannibalization boundary fixes: (a) make `/it/feiertage/tessin` Tessin-specific (bern.md pattern from 2026-07-16); (b) point generic FR "inscription/registre tva" internal anchors at `/fr/mwst-registrierung`, not genf/waadt | 2a |
| 7 | Internal-link pass for the 369 orphan pages (after #2, so links land on canonical URLs) | 2f |
| 8 | `/rechnungsvorlage` polish (difficulty 7–10, pos 7–17 family): Excel-Vorlage section + FR `modèle facture` mirror | 2c |

### B. Ongoing work — cannot be closed by a PR

| # | Workstream | Detail |
|---|---|---|
| 1 | **Link building** (the #1 lever) | 203 → 400+ refdomains is the realistic 6-month target. Vectors per competitor playbook: free tools (QR generator, brutto-netto/MWST calculators) as linkable assets, Swiss freelancer survey/data, directory + fiduciary listings, the buchhaltungsprogramm-schweiz outreach dossier (2026-07-23) |
| 2 | **Disavow review** (manual) | Section 2g sample; verify punycode domains first; file via GSC. Human decision — do not automate |
| 3 | **MWST filing cluster (DE), then TVA (FR)** | Section 2e; already on the open queue from July. MWST-Abrechnung guide + Sätze table; FR mirror. FR `/fr/rechnungsprogramm` upgrade for the klara `logiciel facturation` flank |
| 4 | **Translations / FR investment** | FR = 20% of market, carries the #1 traffic page, and shows the widest striking-distance gaps vs klara |
| 5 | **GSC monitoring** | 2026-09-01 checkpoint: legacy `/de/` keyword count (expect <400 from 1,601), UID satellite rankings (shipped late July, too new in this pull), bexio-preise page maturity, post-cleanup cannibalization re-export (round-2 verify was scheduled ~2026-08-15) |
| 6 | **Traffic diversification** | Accept feiertage upside but measure success on BOFU rankings (buchhaltungssoftware family pos 11 → top 10), not total visits; the 53% two-page concentration is the metric to shrink |

**Do not do:** re-fix the 21 stale cannibalization groups involving already-redirected URLs; chase `dropshipping`/`moneyhouse`/klara's POS-webshop surface (off-ICP); react to the +7,122/−6,205 churn number before September.
