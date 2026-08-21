# Option A implementation spec — magic-heidi-atlas

Verified against the live site 2026-08-21. **Two corrections to the original audit are folded in below** (steps 2 and 4); do not implement the audit's wording where it conflicts with this file.

Guiding constraint from the repo's CLAUDE.md: *least amount of code possible*. Flask + Jinja + raw SQL. Auto-deploys from `main`. German-speaking cantons (ZH/BE/…) are on the roadmap — so the locale cut must be a **reversible config flag**, not a demolition of the i18n system.

---

## Step 1 — Serve only `/fr/`

- Add a single config constant, e.g. `ACTIVE_LOCALES = {"fr"}` (keep `ALL_LOCALES` intact so re-enabling German is a one-line change once ZH/BE are seeded).
- Any request to `/de/…`, `/it/…`, `/en/…` → **HTTP 410 Gone** with a minimal styled page.
- Root `/` → redirect to `/fr/` (currently 302s to `/de/`).
- `sitemap.xml` index → list only the two `fr` sitemaps.
- Drop the hreflang `<link rel="alternate">` block entirely while only one locale is active (a self-referential-only cluster is pointless). Keep `x-default` off too.
- Hide the language switcher in the UI.

**Traffic given up:** 2,443 pages / 6,894 impressions / 42 clicks per 28 days — all navigational brand queries. This is intentional.

## Step 2 — Language facets (CORRECTED — much narrower than the audit said)

The audit claimed "18,136 exact duplicates." That was wrong: the 4,534 depth-3 non-prestation URLs per locale are **2,806 language facets + 1,728 tag facets**, and most language facets are already handled. Verified live:

| URL | Listings | Robots |
|---|---|---|
| `/fr/lausanne/menuisier/` | 24 | indexable |
| `/fr/lausanne/menuisier/francophone/` | **24 — identical to parent** | **indexable ← the bug** |
| `/fr/lausanne/menuisier/anglophone/` | 2 | already `noindex,follow` |
| `/fr/lausanne/menuisier/germanophone/` | 2 | already `noindex,follow` |

The existing `MIN_TAG_INDEXABLE = 5` rule already noindexes small facets. The real defect is only this: **the majority-language facet (`francophone`) in French-speaking cities returns the same set as its parent but stays indexable.** CLAUDE.md notes the *chip* is hidden when it matches every business — the *URL* was not given the same treatment.

- **Fix:** when a language facet's result set equals its parent listing's, return **410** (or at minimum `noindex` + drop from sitemap). Scope: **1,639 `francophone` URLs** in FR.
- **Do NOT touch** `anglophone` / `germanophone` / `italophone` facets — they are genuine minority-language filters, already noindexed, and are a deliberate product feature.
- **Do NOT touch** the 1,728 tag-facet URLs — they carry real impressions (`decorateur-interieur` 161, `cleaning-service` 105, `peintre` 52).

## Step 3 — Noindex business detail pages

- Add `<meta name="robots" content="noindex,follow">` to every `/fr/entreprise/…` page. Verified: they currently emit no robots meta.
- Keep them live, keep them linked from listings (the `follow` matters — listings need somewhere to point).
- Remove `sitemap-biz-fr.xml` from the sitemap index and stop generating it.
- Rationale: 749 FR business pages produced 39 clicks in 28 days, all navigational, at 0% commercial value, while consuming crawl budget for ~46,626 URLs.

## Step 4 — Tag vocabulary cleanup (CORRECTED framing)

The audit framed this as "two competing URL patterns." That is not accurate: `/{city}/{trade}/` is category-scoped and `/{city}/prestation/{tag}/` is tag-scoped — a legitimate distinction. **Do not collapse the patterns.** The actual defect is that the *tag vocabulary itself* is polluted. Verified in the FR sitemap: 979 distinct tag slugs across 4,691 URLs, containing —

- **EN/FR synonym pairs, both live and indexable** — `painting` 69 / `peinture` 43 · `cleaning` 62 / `nettoyage` 36 · `accounting` 35 / `comptabilite` 4 · `carpentry` 19 / `menuiserie` 29 · `catering` 24 / `traiteur` 3 · `moving` 13 / `demenagement` 4 · `plumbing` 11 / `plomberie` 1 · `roofing` 10 / `toiture` 2. At least **243 URLs sit on an English slug that has a French twin.**
  Two live pages both titled "entreprises de peinture à Lausanne" — that is the cannibalization.
- **Fix:** build a canonical FR tag map, merge each English tag into its French twin at the data layer, and **301** the retired slug → the French one. Keep the French slug.

## Step 5 — Place-name tags and non-ASCII slugs

- **Non-ASCII slugs: 65 distinct, 225 URLs** — e.g. `genève`, `neuchâtel`, `comptabilité`, `déménagement`, `bien-être`, `auto-école`, `châtel-saint-denis`. Slugify to ASCII (`comptabilite`, `demenagement`, `bien-etre`, `auto-ecole`) and **301** old → new.
- **Place names used as tags: `genève`, `neuchâtel`, `renens`, `suisse` (130 URLs)**, plus many more hiding in the non-ASCII list (`anières`, `bôle`, `chambésy`, `chesières`, `châtelaine`, `chêne-bourg`, `céligny`, `courtemaîche`, `delémont`…). A city name is not a service. **Remove these from the tag vocabulary and 410 the resulting URLs**, then fix the enrichment step that let place names into the tags column so they don't come back.
- Note `/fr/neuchatel/prestation/neuchâtel/` already 301s to the canton form — the redirect layer added in commit `0d4b60a` is a working precedent to follow.

---

## Acceptance tests (run against local dev, then prod after deploy)

| URL | Expected |
|---|---|
| `/` | 301/302 → `/fr/` |
| `/de/`, `/it/`, `/en/` | 410 |
| `/de/firma/apco-technologies-s-a-che107430655` | 410 |
| `/fr/` | 200 |
| `/fr/lausanne/menuisier/` | 200, indexable |
| `/fr/lausanne/menuisier/francophone/` | 410 |
| `/fr/lausanne/menuisier/anglophone/` | 200, `noindex,follow` |
| `/fr/lausanne/decorateur-interieur/interior-architecture/` | 200 (tag facet — must survive) |
| `/fr/entreprise/tabac-28-gallo-che460285251` | 200 + `noindex,follow` |
| `/fr/lausanne/prestation/painting/` | 301 → `/fr/lausanne/prestation/peinture/` |
| `/fr/lausanne/prestation/genève/` | 410 |
| `/sitemap.xml` | only `sitemap-pages-fr.xml`; no biz sitemap, no de/it/en |
| `sitemap-pages-fr.xml` | no `francophone`, no English-twin tags, no place-name tags, no non-ASCII |

**Target end state:** ~7,000 indexable French category pages (from 250,220 URLs), business pages live but noindexed.

## Deployment note

Render auto-deploys from `main`. `?v=N` in `base.html` must be bumped if `style.css` changes. Do not touch `db.py` connection handling.

---

## ADDENDUM — step 4/5 scope is larger than the audit implied

Dumping all 979 FR tag slugs shows the vocabulary is polluted well beyond EN/FR twins. Hand-curating 979 slugs is not "least code"; the recommended fix is an **allowlist** (below). Categories of junk found:

1. **Slugs containing literal spaces** (URL-encoded as `%20`) — `sole proprietorship`(20), `real estate`(11), `graphic design`(11), `passenger transport`(10), `video production`(6), `film production`(6), `vehicle rental`(6), `interior design`(5), `web design`(5), `used cars`(4), `salon de coiffure`(4), `management consulting`(4), `home care`(4), `transport de personnes`(4), `project management`(3), `chauffeur service`(3), `la chaux-de-fonds`(6). A space in a URL slug is a bug in the slugifier.
2. **Accent/ASCII duplicates of the same tag** — `renovation`(148) vs `rénovation`(22); `comptabilite`(4) vs `comptabilité`(8); also `maçonnerie`, `plâtrerie`, `déménagement`/`demenagement`.
3. **Underscore/space variants** — `sole proprietorship`(20) vs `sole_proprietorship`(6).
4. **Place names as services** — `neuchâtel`(47), `genève`(46), `suisse`(23), `wallis`(19), `renens`(14), `delémont`(10), `thônex`(8), `ecublens`(7), `la chaux-de-fonds`(6), `lavaux`(4), `val-de-travers`(4), `nendaz`(3).
5. **Review-sentiment adjectives, not services** — `friendly-service`(28), `family-run`(12), `friendly-staff`(6), `vintage`(6), `affordable`(5), `luxury`(5), `customer-service`(4), `personalized-service`(3), `authentic`(3), `professional-service`(3). These make meaningless landing pages.
6. **Many slugs for one concept** — hairdressing alone has `hair-salon`(25), `hairdresser`(19), `haircuts`(18), `coiffure`(11), `barber`(8), `haircut`(5), `salon-de-coiffure`(4), `salon de coiffure`(4).

### Recommended approach (least code, biggest reduction)

Rather than a 979-row rewrite: **curate an `INDEXABLE_TAGS` allowlist of genuine French service tags** (realistically 100–200 entries) and gate tag-page indexability on it, layered on the existing `MIN_TAG_INDEXABLE = 5` rule.

- Tag in allowlist AND >= 5 matches → indexable, in sitemap.
- Tag not in allowlist → page may still render (harmless for users) but **noindex + excluded from sitemap**.
- Add a **301 map** only for the high-traffic retired slugs → their canonical French twin (`painting`→`peinture`, `cleaning`→`nettoyage`, `renovation`→`rénovation` normalized to `renovation`, the hairdressing cluster → `coiffure`, etc.).
- Fix the slugifier so spaces and non-ASCII can never enter a slug again, and filter place names out of the tags column at enrichment time.

This is a **data-quality task with an SEO deadline**, not a routing change. If time-boxed, do steps 1–3 first (they deliver most of the index reduction on their own) and land the tag allowlist as a follow-up.
