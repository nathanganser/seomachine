#!/usr/bin/env python3
"""AI search visibility audit via SE Ranking (ChatGPT, Perplexity, Gemini,
Google AI Overview / AI Mode).

Pulls per-engine brand/link presence + the actual prompts where the domain or
brand shows up in LLM answers. Optional share-of-voice leaderboard vs
competitors (7,500 credits — off by default).

Outputs audits/ai-visibility-<date>/:
  raw/*.json + summary.md

Credits (defaults): discover-brand 100 + 800/engine time-series
+ 200/prompt (prompts pulled for the first engine only, 2 × --prompts-limit)
≈ 6,500 for 3 engines. --with-leaderboard adds 7,500.

Usage:
  python3 seranking_ai_visibility.py
  python3 seranking_ai_visibility.py --engines chatgpt,perplexity,ai-overview,gemini
  python3 seranking_ai_visibility.py --with-leaderboard
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient, save_json

REPO = Path(__file__).parent
CONFIG = REPO / "config" / "competitors.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="magicheidi.ch")
    ap.add_argument("--brand", default="Magic Heidi")
    ap.add_argument("--engines", default="chatgpt,perplexity,ai-overview")
    ap.add_argument("--prompts-limit", type=int, default=10,
                    help="prompts per pull, 200 credits each (default 10)")
    ap.add_argument("--prompts-engines", default=None,
                    help="engines to pull prompts for (default: first of --engines)")
    ap.add_argument("--with-leaderboard", action="store_true",
                    help="share-of-voice leaderboard vs competitors — 7,500 credits")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()

    engines = [e.strip() for e in args.engines.split(",") if e.strip()]
    prompt_engines = ([e.strip() for e in args.prompts_engines.split(",")]
                      if args.prompts_engines else engines[:1])
    out = REPO / "audits" / f"ai-visibility-{args.date}"
    raw = out / "raw"
    client = SERankingClient()

    print("== discover brand ==")
    brands = client.ai_discover_brand(args.domain)
    save_json(brands, raw / "discover_brand.json")

    overview = {}
    for engine in engines:
        print(f"== {engine} time-series ==")
        try:
            res = client.ai_timeseries(args.domain, engine)
            save_json(res, raw / f"timeseries_{engine}.json")
            overview[engine] = res.get("summary", {})
        except (RuntimeError, ValueError) as e:
            print(f"  !! {engine} failed: {e}")

    prompts = {}
    for engine in prompt_engines:
        print(f"== {engine} prompts ==")
        try:
            pt = client.ai_prompts_by_target(args.domain, engine, limit=args.prompts_limit)
            save_json(pt, raw / f"prompts_by_target_{engine}.json")
            pb = client.ai_prompts_by_brand(args.brand, engine, limit=args.prompts_limit)
            save_json(pb, raw / f"prompts_by_brand_{engine}.json")
            prompts[engine] = {"target": pt, "brand": pb}
        except RuntimeError as e:
            print(f"  !! prompts {engine} failed: {e}")

    leaderboard = None
    if args.with_leaderboard:
        cfg = json.load(open(CONFIG))
        comps = cfg.get("seranking_competitors") or cfg.get("direct_competitors", [])
        print(f"== leaderboard vs {comps} (7,500 credits) ==")
        leaderboard = client.ai_leaderboard(args.domain, comps, engines,
                                            brand=args.brand, confirm_cost=True)
        save_json(leaderboard, raw / "leaderboard.json")

    # ---- summary
    lines = [f"# AI search visibility — {args.brand} ({args.domain}) — {args.date}", "",
             f"Discovered brand names: {json.dumps(brands, ensure_ascii=False)}", "",
             "## Per-engine presence", "",
             "| Engine | Brand presence | Link presence | Avg position | AI opportunity traffic |",
             "|---|---:|---:|---:|---:|"]
    for engine, s in overview.items():
        def cur(key):
            v = (s.get(key) or {}).get("current")
            return v if v is not None else "–"
        lines.append(f"| {engine} | {cur('brand_presence')} | {cur('link_presence')} | "
                     f"{cur('average_position')} | {cur('ai_opportunity_traffic')} |")

    for engine, p in prompts.items():
        for kind, res in (("domain cited", p["target"]), ("brand mentioned", p["brand"])):
            rows = res.get("prompts", res.get("items", res if isinstance(res, list) else []))
            lines += ["", f"## {engine}: prompts where {kind} ({len(rows)} shown)", ""]
            for r in rows:
                if isinstance(r, dict):
                    lines.append(f"- {r.get('prompt') or r.get('text') or json.dumps(r)[:120]}"
                                 + (f" (vol {r['volume']})" if r.get("volume") else ""))
                else:
                    lines.append(f"- {r}")

    if leaderboard is not None:
        lines += ["", "## Share-of-voice leaderboard", "",
                  "```json", json.dumps(leaderboard, indent=2, ensure_ascii=False)[:4000], "```"]

    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out / 'summary.md'}")
    print(f"[credits] estimated spend: {client.credit_report()['total_est_credits']:,}")


if __name__ == "__main__":
    main()
