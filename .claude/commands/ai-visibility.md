# AI Visibility Command

Automated AI-search visibility audit: where Magic Heidi shows up in ChatGPT, Perplexity, Gemini, and Google AI Overview answers.

## Usage
`/ai-visibility` — chatgpt + perplexity + ai-overview presence, prompts for chatgpt
`/ai-visibility --leaderboard` — adds share-of-voice leaderboard vs competitors (7,500 credits)

## What This Command Does

Replaces the manual data-gathering half of `/research-ai-citations`: instead of running prompts by hand in ChatGPT, pulls SE Ranking's AI-search index — per-engine brand presence, link presence, average position, and the actual prompts where magicheidi.ch is cited or "Magic Heidi" is mentioned.

## Process

1. **Pull the data**:
```bash
python3 seranking_ai_visibility.py                    # defaults: 3 engines, 10 prompts
python3 seranking_ai_visibility.py --with-leaderboard # + share-of-voice vs competitors
```

2. **Analyze**: read `audits/ai-visibility-<date>/summary.md` and the raw prompt JSON, then:
   - Compare presence numbers against the previous `audits/ai-visibility-*/` run (trend)
   - Cross-reference cited prompts against `context/ai-citation-targets.md` — which target topics are we absent from?
   - Identify which of our pages get cited and which prompt themes cite competitors instead
   - Update recommendations: content to create/adjust so AI engines cite us for money prompts (comparisons, "beste buchhaltungssoftware schweiz"-type prompts)

3. **Write** the analysis into `audits/ai-visibility-<date>/analysis.md`.

## Output

- `audits/ai-visibility-<date>/raw/*.json` — time-series, prompts, discover-brand, optional leaderboard
- `audits/ai-visibility-<date>/summary.md` — per-engine presence table + prompt lists
- `audits/ai-visibility-<date>/analysis.md` — trend + gap analysis with actions

## Integration

- Keep `/research-ai-citations` for prompt-set generation and strategy; this command supplies the measurement
- Missing prompt themes → `/write` or `/rewrite` targets
- Track monthly alongside `/seranking-audit`

## Time & Cost

**Time:** 2-3 minutes
**API Cost:** ~6,500 SE Ranking credits (3 engines × 800 + discover 100 + 20 prompts × 200); `--leaderboard` adds 7,500

## When to Run

- **Monthly**, same cadence as `/seranking-audit`
- After publishing comparison/listicle content aimed at AI citation
