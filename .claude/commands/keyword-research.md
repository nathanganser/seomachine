# Keyword Research Command

Keyword expansion and metrics from the SE Ranking Swiss database.

## Usage
`/keyword-research buchhaltungssoftware` — full ideas pull for a seed keyword
`/keyword-research logiciel facturation` — works for French/Italian seeds too (source stays `ch`)

## What This Command Does

Pulls similar, related, question, and longtail keywords for a seed — each with Swiss volume, difficulty, CPC, intent, and SERP features — then clusters the results, checks them against existing content and `context/target-keywords.md`, and recommends what to add.

## Process

1. **Pull ideas**:
```bash
python3 seranking_keyword_research.py ideas "<seed>"
```
Optional: bulk metrics for an existing keyword list:
```bash
python3 seranking_keyword_research.py metrics --config-set bofu_keywords
python3 seranking_keyword_research.py metrics --keywords "kw1,kw2"
python3 seranking_keyword_research.py metrics --file context/target-keywords.md
```

2. **Analyze**: read `research/keyword-ideas-<slug>-<date>.csv` and:
   - Cluster keywords by topic/intent (transactional vs informational vs question)
   - Check each cluster against published content and `context/target-keywords.md` — mark covered / partially covered / uncovered
   - Flag quick-win candidates (decent volume, low difficulty, commercial intent)
   - Recommend: new articles, sections to add to existing pages, and cluster placement

3. **Write** `research/keyword-research-<slug>-<date>.md` with the clustered recommendation.

## Output

- `research/keyword-ideas-<slug>-<date>.csv` — deduplicated ideas with metrics
- `research/keyword-research-<slug>-<date>.md` — clustered analysis + recommendations

## Integration

- Uncovered clusters → `/research [topic]` then `/write [topic]`
- New keywords worth tracking → add to `context/target-keywords.md` and `config/competitors.json`
- For live SERP shape of a specific keyword, use `/research-serp` (DataForSEO)

## Time & Cost

**Time:** 2-3 minutes
**API Cost:** ~3,400 SE Ranking credits per seed at defaults (100 rows × 3 idea types × 10cr + 200 longtail × 1cr + export)

## When to Run

- **Before planning a new cluster or pillar page**
- **When a seed keyword's SERP intent is unclear** — the question/longtail sets reveal it
