# SEO Audit — atlas.magicheidi.ch

**Date:** 2026-08-21
**Window:** 2026-07-22 (launch) → 2026-08-18 (last complete GSC day)
**Sources:** Google Search Console (`sc-domain:magicheidi.ch`, page-filtered to the atlas subdomain), DataForSEO live SERP (CH/fr), direct crawl of sitemaps + rendered HTML.

> **Corrections applied 2026-08-21 (post-review).** Two findings in the first draft were overstated and have been rewritten below; the deeper verification happened while scoping the fix.
> - §3.4 claimed **18,136 exact duplicate facet URLs**. Wrong. The 4,534 depth-3 non-`prestation` URLs per locale are **2,806 language facets + 1,728 tag facets**. Minority-language facets are already `noindex` via the existing `MIN_TAG_INDEXABLE = 5` rule, and tag facets carry real traffic. The genuine defect is only the **majority-language facet (~1,639 `francophone` URLs)**, which returns its parent's exact result set yet stays indexable.
> - §3.5 framed the issue as **"two competing URL patterns"**. Wrong. `city/trade/` is category-scoped and `city/prestation/tag/` is tag-scoped — a legitimate distinction, and categories are a clean curated list of 74. The real defect is that the **tag vocabulary is unvalidated free-form LLM output** (17,377 distinct tags in the DB).
>
> The implementation spec at `OPTION_A_SPEC.md` (scratchpad) supersedes the original wording of Option A steps 2, 4 and 5.

**Source availability note:** SE Ranking returned `403 License expired` on both the MCP server and the repo's prepaid Data API key — the Data API is now dead too, not just the Project API (this contradicts the 2026-08-16 note in `CLAUDE.md`, which should be updated). Ahrefs Site Explorer and the free DR endpoint both returned `Insufficient plan`. So there is **no third-party backlink or authority data** in this audit; GSC and live SERP scraping carried it.

---

## Verdict

Atlas is a well-built machine pointed at a market that does not exist, in languages nobody searches in, competing against Google using Google's own data.

The engineering is genuinely good: server-rendered HTML, correct canonicals, complete hreflang, valid `LocalBusiness` / `ItemList` / `BreadcrumbList` / `AggregateRating` JSON-LD, 80–150 ms TTFB, clean robots.txt. **None of that is the problem.** The problem is that 250,220 URLs were published against Romandie-only data, translated into three languages with no corresponding demand, and aimed at queries where Google answers with its own local pack.

Twenty-eight days after launch: **94 clicks.**

---

## 1. The traffic curve

| Date | Impressions | Clicks | Avg position |
|---|---|---|---|
| 2026-07-22 (launch) | 13 | 1 | 8.7 |
| 2026-07-24 (peak) | 1,956 | 31 | 19.3 |
| 2026-08-01 | 836 | 4 | 47.2 |
| 2026-08-18 (latest) | 141 | 0 | 31.4 |

Impressions peaked at 1,956/day on day 3 and settled at **~100–140/day, a 93% decline from peak**. This is the classic programmatic-SEO shape: Google crawls a big new sitemap, samples the pages in live SERPs, measures how users respond, and withdraws them. The withdrawal completed around 2026-08-03 and the floor has held for two weeks.

**28-day totals:** 12,761 impressions, 94 clicks, **0.74% CTR**. Atlas is 1.38% of the domain's impressions and 1.64% of its clicks.

---

## 2. Index coverage: 1.51%

| | URLs published | URLs with ≥1 impression | Coverage |
|---|---|---|---|
| Business detail pages | 186,504 | 2,276 | 1.22% |
| Category / list pages | 63,716 | 1,509 | 2.37% |
| **Total** | **250,220** | **3,785** | **1.51%** |

98.5% of the site has never been shown to a single searcher. Publishing a quarter-million URLs on a subdomain with no backlinks and no internal links from the main site means Google will never allocate the crawl budget to evaluate most of them — and the thin pages it did evaluate lowered its willingness to crawl the rest.

---

## 3. The five root causes

### 3.1 The data is Romandie-only, but the site ships four languages

Atlas covers **French-speaking Switzerland exclusively**. Page counts by city in the German sitemap: Genf 1,551 · Lausanne 1,002 · Aigle 321 · Freiburg 283 · Karouge 278 · Neuenburg 267 · Sitten 221 · Nyon 217.

Presence check for major German- and Italian-speaking cities — **all zero**:

> Zürich 0 · Bern 0 · Basel 0 · Luzern 0 · St. Gallen 0 · Winterthur 0 · Zug 0 · Aarau 0 · Chur 0 · Schaffhausen 0 · Lugano 0

Magic Heidi's stated market split is 70% German / 20% French / 5% Italian / 5% English. Atlas inverts this completely: it has **no inventory at all** in the 70% market.

Worse, the DE, IT, and EN folders are real translations *of Romandie businesses*. `/de/genf/...` is a German-language page about a Geneva business. Nobody in Zürich searches for a Geneva locksmith in German; nobody in Geneva searches in German at all. That is **187,665 URLs (75% of the site) targeting demand that does not exist.**

GSC confirms it — the "primary" language performs worst:

| Folder | Pages with impressions | Impressions |
|---|---|---|
| `/en/` | 1,733 | 4,937 |
| `/fr/` | 1,342 | 5,867 |
| `/de/` | 416 | 1,099 |
| `/it/` | 294 | 858 |

Country split reinforces it: 5,230 impressions from Switzerland, 1,032 from **France**, and just 54 from Germany. The French folder is pulling cross-border traffic from France that will never convert to a Swiss accounting product.

### 3.2 The pages that rank can't convert; the pages that could convert don't rank

| Page type | Pages | Impressions | Clicks | Avg position |
|---|---|---|---|---|
| Business detail | 2,276 | 7,147 | 72 | **16.0** |
| Category / list | 1,509 | 5,614 | 22 | **59.0** |

Business detail pages rank *well* — but only for navigational brand queries, where the searcher wants the business itself. Every single query that produced a click was one of these:

> alpincar · boutique aux 4 vents · freedomcoffee · iswim · jean marc thiebaut · la bonne etoile vallorbe · la table du royal crissier · laurent crampon · le stop bramois — **1 click each**

These searchers want a phone number, get it from the Google local pack, and never click. Note `/fr/entreprise/tabac-28-gallo-che460285251` at **position 2.1 with 67 impressions and 0 clicks** — position 2 with zero clicks is Google telling you the page adds nothing to the SERP.

Category pages are the ones with commercial intent ("entreprise de nettoyage nyon"), and they average **position 59** — page 6.

### 3.3 Atlas competes against Google's local pack, with Google's own data

Live DataForSEO SERP checks (CH/fr), top 30:

| Query | Atlas position | Who wins organic | SERP features |
|---|---|---|---|
| entreprise de nettoyage nyon | **not in top 30** | local.ch, impec.ch, tel.search.ch | local_pack, PAA |
| menuisier lausanne | **not in top 30** | indeed, tel.search.ch, ducommun-menuisiers.ch | local_pack, PAA |
| architecte d'intérieur lausanne | **not in top 30** | scavone-design.com, atelier-chevre.com | local_pack, PAA |
| ébéniste lausanne | **not in top 30** | fredericfarine.ch, local.ch | local_pack |
| gestion de fortune lausanne | **not in top 30** | lgh-associes.ch, pictet.com | local_pack, PAA |

**Every one of these SERPs carries a local pack**, and in four of five the first organic result sits at position 4 or lower because the pack occupies the top. Atlas's content is built from Google Maps listings and Google reviews — it is a mirror of what Google already shows above the organic results for free. There is no reason for Google to rank it, and the incumbents (local.ch, tel.search.ch, starofservice.ch) have a decade of authority Atlas cannot match from a zero-link subdomain.

### 3.4 Structural duplication and taxonomy bugs

**Language-facet pages are exact duplicates.** The category tree has 4,534 `city/trade/{francophone|germanophone}` URLs per language — **18,136 total**. Compared side by side:

| URL | Listings | Words | First result |
|---|---|---|---|
| `/fr/lausanne/auto-ecole/` | 11 | 738 | AUTO-ECOLE ALAIN, Alain Juillerat |
| `/fr/lausanne/auto-ecole/francophone/` | 11 | 740 | AUTO-ECOLE ALAIN, Alain Juillerat |

Identical content, and the facet page **self-canonicalizes** rather than pointing at its parent. In a francophone city, "francophone driving schools" is simply all of them.

**Two competing URL patterns cannibalize each other.** `city/trade/` (6,952/lang) and `city/prestation/service/` (2,963/lang) both target "service in city."

**The service taxonomy mixes English and French slugs**, creating duplicate pairs — `painting` (41 URLs) vs `peinture` (24), `cleaning` (36) vs `nettoyage` (20), `accounting` (20) vs `comptabilite` (2). Both members of each pair are live and near-identical:

```
/fr/lausanne/prestation/painting/  → "Les 50 meilleures entreprises de peinture à Lausanne"
/fr/lausanne/prestation/peinture/  → "Les 10 entreprises de peinture à Lausanne"
```

Of 979 distinct service slugs in the French sitemap, most are English (`consulting`, `restaurant`, `coaching`, `construction`, `transport`, `takeaway`, `real-estate`, `plastering`). GSC shows the damage directly: `/fr/neuchatel/prestation/property-management/` at position 85.3, `/fr/lausanne/prestation/heating/` at 77.3.

**City names leak into the service taxonomy** — 70 nonsense URLs where a canton is treated as a service, including the self-referential `/fr/neuchatel/prestation/neuchâtel/`. These also contain **non-ASCII characters** (`neuchâtel`, `genève`), which should never appear in a URL slug.

### 3.5 Business pages are too thin to justify existing

Measured visible word counts: **84 (de) / 88 (en) / 94 (it) / 96 (fr)** for the same business; 126 for a richer example. Content is a name, category, town, star rating, phone, and a two-sentence AI description. Category pages are substantially better at 602–994 words.

So **75% of the URL footprint is ~90-word pages** whose only ranking capability is brand queries that convert at 0%. They are the primary drag on how Google assesses site quality, and they consume the crawl budget the category pages need.

### 3.6 Atlas is an orphan

`atlas.magicheidi.ch` is **not linked from magicheidi.ch anywhere** — zero mentions on the homepage or the `/de/` homepage, absent from `llms.txt`, absent from the main sitemap index. It is a subdomain, so it inherits **no authority** from the main domain, and it receives none through links either. A quarter-million pages are hanging off nothing.

---

## 4. Did Atlas hurt the main site?

Site-wide daily averages, excluding Atlas itself:

| Period | Clicks/day | Impressions/day |
|---|---|---|
| Pre-launch (6/15 – 7/21) | 225.7 | 28,742 |
| Post-launch (7/22 – 8/18) | 201.5 | 32,630 |

Main-site clicks fell 10.7% while impressions rose 13.5%. **I do not think Atlas caused this.** The prior 60-day review already attributed the click decline to summer seasonality, impressions moved the opposite way, and Atlas is on a separate subdomain. Treat it as "no evidence of harm, no evidence of benefit" — but worth re-checking in September when seasonality lifts, since a sustained divergence would change the reading.

---

## 5. Recommendations

The strategic question comes first: **should Atlas exist at all?** It currently returns 94 clicks per 28 days, none of them commercial, against a build of 250,220 pages. The honest answer is that the current shape cannot be fixed by optimization — the market, the language mix, and the SERP opposition are all wrong at once. Below are the three viable paths, in the order I'd consider them.

### Option A — Cut to the defensible core (recommended)

Keep only what has a plausible path to ranking, and make Atlas roughly 3% of its current size.

*(Steps 2, 4 and 5 restated from the corrections above.)*

1. **Serve only `/fr/`** — retire 187,665 URLs. 410 for `/de/`, `/it/`, `/en/`; `/` redirects to `/fr/`; suppress hreflang while one locale is active. Implement as a reversible `ACTIVE_LANGS` flag, **not** a deletion — German-speaking cantons are on the product roadmap (atlas `CLAUDE.md` "Parked / next"), so re-enabling must be a one-line change.
2. **410 the majority-language facet only** (~1,639 `francophone` URLs in FR), where the facet's result set equals its parent's. Leave `anglophone`/`germanophone`/`italophone` alone (genuine filters, already noindexed by the count rule) and leave all 1,728 tag facets alone (they carry real traffic).
3. **Noindex every business detail page** (~46,626). Keep them live and internally linked with `noindex,follow`. Drop the business sitemaps.
4. **Slug hygiene first** — cheaper than step 5 and worth more. Slugify the tag segment in `i18n.url_for_page()` (the single URL choke point), normalise before the place-name denylist so accented city names are caught, and add XML escaping to `render_urlset()`.
5. **Merge the EN/FR tag twins** via a small alias map plus 301s (`painting`→`peinture`, `cleaning`→`nettoyage`, the eight-way hairdressing cluster→`coiffure`). Do **not** hand-curate all 979 slugs; gate indexability on an allowlist of genuine French service tags and noindex the rest.
6. **Add canton-level tag pages to the sitemap** (`/{lang}/{canton}/prestation/{tag}/`). They render and are internally linked but appear in *zero* sitemaps. They're the strongest category pages on the site — canton scope means more listings and less thinness — and 36 drew impressions while sitemap-orphaned, including `/fr/canton-de-neuchatel/prestation/isolation/` at **168 impressions, the highest of any category page.** This is the one place to *add* URLs.

The deeper fix behind 4 and 5 is upstream: the v1 enrichment prompt asked for "a few free-form tags" with no language/casing/charset constraint, and the only write-time check is a type test plus a truncation to 10. The DB holds 17,377 distinct tags. Without a validation step the vocabulary will re-pollute.

This leaves roughly **7,000 French category pages** — a size Google will actually crawl and evaluate, on a subdomain that can plausibly earn links.

### Option B — Fix the market mismatch first

If Atlas is strategically important, the data problem outranks the SEO problem: **acquire German-speaking Switzerland inventory** (Zürich, Bern, Basel, Luzern, St. Gallen, Winterthur, Zug) before touching anything else. That is where 70% of Magic Heidi's market is. Do Option A's cleanup steps 2–5 regardless, but rebuild `/de/` against real German-region businesses rather than deleting it. This is the larger investment and I would not start it until the local-pack problem below has an answer.

### Option C — Accept that this SERP isn't winnable and repurpose

Every target SERP has a local pack fed by the same Google Maps data Atlas republishes. Directory pages that mirror Google's data have no differentiated value. If Atlas is to stay, it needs something Google Maps doesn't have — Magic Heidi's own angle: which businesses are sole proprietorships, VAT-registered, which legal form, UID data, industry benchmarks. That converts Atlas from "another directory" into a data asset that also feeds the main site's accounting-software funnel, which is where the actual revenue intent lives.

### Regardless of path

7. **Link Atlas from magicheidi.ch — DONE 2026-08-21.** A followed footer link (`https://atlas.magicheidi.ch/fr/`, no `nofollow`) now ships across all eight locales; verified live on production in de/en/fr/it/es/pt/sq/sr. mh-landing commit `21bf2a40`. Still worth adding to `llms.txt` and the main sitemap index. Ordering caveat: this passes equity into the current thin-page set until the prune lands, so the two should ship close together.
8. **Re-measure on 2026-09-15**, four weeks after any pruning ships, and compare against this baseline. The metric that matters is impressions per indexed page and category-page average position, not raw impressions.
9. **Update `CLAUDE.md`**: the SE Ranking Data API no longer works on prepaid credits — the whole account returns `License expired`. Every `/seranking-*` command and the 2026-09-01 re-measure are blocked until the subscription is renewed. Ahrefs is also plan-limited to GSC endpoints only.

---

## Files

- `gsc_raw.json` — full GSC pull: daily history (180d, atlas + site-wide), pages/queries/query-page/country/device for the 28-day window.
