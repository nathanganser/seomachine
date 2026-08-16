#!/usr/bin/env python3
"""Keyword research via the SE Ranking Swiss database.

Subcommands:
  ideas <seed>     similar + related + questions + longtail for a seed keyword
                   → research/keyword-ideas-<slug>-<date>.csv
  metrics          bulk volume/difficulty/cpc/intents/12-mo trend
                   → research/keyword-metrics-<date>.csv
                   Keywords come from --keywords a,b,c | --file <txt/md> |
                   --config-set bofu_keywords (a list key in config/competitors.json)

Language: source stays "ch" (Switzerland) for all languages; the seed's
language determines what comes back (German seed → German ideas).

Credits: ideas ≈ 10/row for similar+related+questions (default 3×100 rows)
+ 1/row longtail (default 200) + 100 export ≈ 3,400/seed at defaults.
metrics = 100 credits per 5000 keywords.

Usage:
  python3 seranking_keyword_research.py ideas "buchhaltungssoftware"
  python3 seranking_keyword_research.py ideas "logiciel facturation" --limit 50
  python3 seranking_keyword_research.py metrics --config-set bofu_keywords
  python3 seranking_keyword_research.py metrics --keywords "mwst schweiz,uid nummer"
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient

REPO = Path(__file__).parent
CONFIG = REPO / "config" / "competitors.json"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50]


def extract_keywords_from_file(path):
    """Plain text: one keyword per line. Markdown (e.g. context/target-keywords.md):
    `* **Keyword**: X` entries and numbered bold list items."""
    text = Path(path).read_text()
    if path.endswith(".md"):
        kws = re.findall(r"\*\s*\*\*Keyword\*\*:\s*(.+)", text)
        kws += re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", text, re.M)
        return [k.strip() for k in kws if k.strip()]
    return [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]


def write_csv(rows, path, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def kw_row(r, kind=""):
    if isinstance(r, str):  # longtail returns bare keyword strings
        return {"keyword": r, "kind": kind}
    return {"keyword": r.get("keyword"), "kind": kind, "volume": r.get("volume"),
            "difficulty": r.get("difficulty"), "cpc": r.get("cpc"),
            "competition": r.get("competition"),
            "intents": ",".join(r.get("intents") or []),
            "serp_features": ",".join(r.get("serp_features") or [])}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ideas = sub.add_parser("ideas")
    p_ideas.add_argument("seed")
    p_ideas.add_argument("--limit", type=int, default=100,
                         help="rows per similar/related/questions call (10 credits/row)")
    p_ideas.add_argument("--longtail-limit", type=int, default=200)
    p_ideas.add_argument("--source", default="ch")

    p_metrics = sub.add_parser("metrics")
    p_metrics.add_argument("--keywords", default=None, help="comma-separated")
    p_metrics.add_argument("--file", default=None, help="txt (one/line) or md file")
    p_metrics.add_argument("--config-set", default=None,
                           help="list key in config/competitors.json, e.g. bofu_keywords")
    p_metrics.add_argument("--source", default="ch")

    args = ap.parse_args()
    date = dt.date.today().isoformat()
    client = SERankingClient(source=args.source)
    out_dir = REPO / "research"

    if args.cmd == "ideas":
        rows = []
        for kind, method, limit in [("similar", client.keywords_similar, args.limit),
                                    ("related", client.keywords_related, args.limit),
                                    ("question", client.keywords_questions, args.limit),
                                    ("longtail", client.keywords_longtail, args.longtail_limit)]:
            try:
                res = method(args.seed, limit=limit)
                batch = res.get("keywords", res) if isinstance(res, dict) else res
                rows += [kw_row(r, kind) for r in batch]
                print(f"  {kind}: {len(batch)} rows")
            except RuntimeError as e:
                print(f"  !! {kind} failed: {e}")
        seen = set()
        deduped = []
        for r in rows:  # keep first occurrence (similar > related > question > longtail)
            k = (r["keyword"] or "").lower()
            if k and k not in seen:
                seen.add(k)
                deduped.append(r)
        deduped.sort(key=lambda r: -(r.get("volume") or 0))
        write_csv(deduped, out_dir / f"keyword-ideas-{slugify(args.seed)}-{date}.csv",
                  ["keyword", "kind", "volume", "difficulty", "cpc", "competition",
                   "intents", "serp_features"])

    elif args.cmd == "metrics":
        if args.keywords:
            kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        elif args.file:
            kws = extract_keywords_from_file(args.file)
        elif args.config_set:
            kws = json.load(open(CONFIG))[args.config_set]
        else:
            raise SystemExit("need --keywords, --file, or --config-set")
        kws = list(dict.fromkeys(kws))
        print(f"fetching metrics for {len(kws)} keywords")
        res = client.keywords_export(kws)
        rows = []
        for r in res:
            row = kw_row(r)
            trend = r.get("history_trend") or {}
            if trend:
                months = sorted(trend)
                row["trend_12mo"] = " ".join(str(trend[m]) for m in months)
                if len(months) >= 2 and trend[months[0]]:
                    row["trend_change_pct"] = round(
                        100 * (trend[months[-1]] - trend[months[0]]) / trend[months[0]])
            row["found"] = r.get("is_data_found")
            rows.append(row)
        rows.sort(key=lambda r: -(r.get("volume") or 0))
        write_csv(rows, out_dir / f"keyword-metrics-{date}.csv",
                  ["keyword", "volume", "difficulty", "cpc", "competition", "intents",
                   "trend_change_pct", "trend_12mo", "found"])

    print(f"[credits] estimated spend: {client.credit_report()['total_est_credits']:,}")


if __name__ == "__main__":
    main()
