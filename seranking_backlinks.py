#!/usr/bin/env python3
"""Backlink gap analysis + outreach prospect list via SE Ranking.

Pulls referring domains for us + each competitor, then builds a prospect list:
domains linking to >= --min-competitors competitors but NOT to us, sorted by
domain authority. Filters out junk TLDs/platform domains that aren't
outreach-able.

Outputs:
  outreach/backlink-prospects-<date>.csv
  outreach/backlink-gap-summary-<date>.md

Credits: per-row billing on /backlinks/refdomains — capped by --max-rows per
domain (default 2000 → worst case ~12k credits for us + 5 competitors).

Usage:
  python3 seranking_backlinks.py
  python3 seranking_backlinks.py --competitors bexio.com,klara.ch --min-competitors 1
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient, save_json

REPO = Path(__file__).parent
CONFIG = REPO / "config" / "competitors.json"

# Domains that link to everyone but can't be pitched (registrars, social,
# scrapers, app stores, big platforms).
SKIP_RE = re.compile(
    r"google\.|facebook\.|twitter\.|instagram\.|youtube\.|linkedin\.|apple\.|"
    r"microsoft\.|wikipedia\.|apps\.shopify|wordpress\.|blogspot\.|wixsite\.|"
    r"webnode\.|jimdo|github\.|medium\.com|pinterest\.|reddit\.com|tiktok\.|"
    r"amazonaws|cloudfront|sitejabber|trustpilot|capterra|getapp|g2\.com|"
    r"softwareadvice|producthunt", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="magicheidi.ch")
    ap.add_argument("--competitors", default=None,
                    help="comma-separated (default: seranking_competitors from config)")
    ap.add_argument("--min-competitors", type=int, default=2,
                    help="prospect must link to at least this many competitors (default 2)")
    ap.add_argument("--max-rows", type=int, default=2000,
                    help="refdomain rows pulled per domain (credit cap, default 2000)")
    ap.add_argument("--min-dr", type=int, default=10,
                    help="minimum domain_inlink_rank for prospects (default 10)")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()

    if args.competitors:
        competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]
    else:
        cfg = json.load(open(CONFIG))
        competitors = cfg.get("seranking_competitors") or cfg.get("direct_competitors", [])

    out_dir = REPO / "outreach"
    out_dir.mkdir(exist_ok=True)
    raw_dir = out_dir / f"backlink-raw-{args.date}"
    client = SERankingClient()

    print(f"== our refdomains ({args.domain}) ==")
    ours_rows = client.backlinks_refdomains_all(args.domain, max_rows=args.max_rows)
    save_json(ours_rows, raw_dir / "refdomains_ours.json")
    ours = {r["refdomain"].lower() for r in ours_rows}
    summary = {args.domain: client.backlinks_summary(args.domain)["summary"][0]}

    linkers = {}  # refdomain -> {competitors: set, best row}
    for comp in competitors:
        print(f"== {comp} refdomains ==")
        try:
            rows = client.backlinks_refdomains_all(comp, max_rows=args.max_rows)
            summary[comp] = client.backlinks_summary(comp)["summary"][0]
        except RuntimeError as e:
            print(f"  !! {comp} failed: {e}")
            continue
        save_json(rows, raw_dir / f"refdomains_{comp.replace('.', '_')}.json")
        for r in rows:
            dom = r["refdomain"].lower()
            if dom in ours or SKIP_RE.search(dom):
                continue
            entry = linkers.setdefault(dom, {"competitors": set(), "dr": 0, "backlinks": 0})
            entry["competitors"].add(comp)
            entry["dr"] = max(entry["dr"], r.get("domain_inlink_rank") or 0)
            entry["backlinks"] += r.get("backlinks") or 0

    prospects = [
        {"refdomain": dom, "dr": e["dr"], "n_competitors": len(e["competitors"]),
         "links_to": " | ".join(sorted(e["competitors"])), "their_backlinks": e["backlinks"]}
        for dom, e in linkers.items()
        if len(e["competitors"]) >= args.min_competitors and e["dr"] >= args.min_dr
    ]
    prospects.sort(key=lambda r: (-r["n_competitors"], -r["dr"]))

    csv_path = out_dir / f"backlink-prospects-{args.date}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["refdomain", "dr", "n_competitors",
                                          "links_to", "their_backlinks"])
        w.writeheader()
        w.writerows(prospects)
    print(f"wrote {csv_path} ({len(prospects)} prospects)")

    lines = [f"# Backlink gap summary — {args.date}", "",
             "| Domain | DR | Ref domains | Backlinks |", "|---|---:|---:|---:|"]
    for dom, s in summary.items():
        dr = s.get("domain_inlink_rank") or s.get("inlink_rank")
        lines.append(f"| {dom}{' (us)' if dom == args.domain else ''} | {dr} | "
                     f"{s['refdomains']:,} | {s['backlinks']:,} |")
    lines += ["",
              f"- Prospects (link to ≥{args.min_competitors} competitors, not us, DR≥{args.min_dr}): "
              f"**{len(prospects)}**",
              f"- Raw refdomain pulls (capped at {args.max_rows}/domain): `{raw_dir.relative_to(REPO)}/`",
              "",
              "Top 25 prospects:",
              "", "| Ref domain | DR | Links to |", "|---|---:|---|"]
    for r in prospects[:25]:
        lines.append(f"| {r['refdomain']} | {r['dr']} | {r['links_to']} |")
    md_path = out_dir / f"backlink-gap-summary-{args.date}.md"
    md_path.write_text("\n".join(lines) + "\n")
    print(f"wrote {md_path}")
    print(f"[credits] estimated spend: {client.credit_report()['total_est_credits']:,}")


if __name__ == "__main__":
    main()
