#!/usr/bin/env python3
"""Pull a full SE Ranking snapshot into a dated audits/ dir.

Pulls (Switzerland database, source=ch by default):
  - domain overview + 12-month history
  - all organic keyword rankings (paginated until exhausted — no row cap)
  - ranking pages
  - organic competitors
  - keyword overlap + competitor top-20 keywords per competitor
  - backlinks summary + authority + top referring domains (us + competitors)
  - meta.json (competitors used, units before/after, credit estimates,
    per-pull completeness flags for truncation-aware comparisons)

Usage:
  python3 seranking_pull_data.py                       # today's snapshot
  python3 seranking_pull_data.py --date 2026-09-01
  python3 seranking_pull_data.py --domain magicheidi.ch --source ch \
      --competitors bexio.com,klara.ch --skip-existing
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


def load_competitors(override):
    if override:
        return [c.strip() for c in override.split(",") if c.strip()]
    cfg = json.load(open(CONFIG))
    return cfg.get("seranking_competitors") or cfg.get("direct_competitors", [])


def units(client, label):
    try:
        left = client.units_left()
        print(f"[units] {left:,} left after {label}")
        return left
    except Exception as e:
        print(f"[units] unavailable after {label}: {e}")
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--date", default=dt.date.today().isoformat(),
                    help="snapshot date YYYY-MM-DD (default: today)")
    ap.add_argument("--out", default=None,
                    help="output raw dir (default: audits/seranking-<date>/raw)")
    ap.add_argument("--domain", default="magicheidi.ch")
    ap.add_argument("--source", default="ch")
    ap.add_argument("--competitors", default=None,
                    help="comma-separated override (default: config/competitors.json)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="skip pulls whose raw file already exists")
    args = ap.parse_args()

    out = Path(args.out) if args.out else REPO / "audits" / f"seranking-{args.date}" / "raw"
    competitors = load_competitors(args.competitors)
    client = SERankingClient(source=args.source)
    units_before = units(client, "start")
    meta = {"date": args.date, "domain": args.domain, "source": args.source,
            "competitors": competitors, "units_left_before": units_before,
            "pulls": {}}

    def fresh(path):
        return not (args.skip_existing and path.exists())

    print("== domain overview ==")
    if fresh(out / "overview_ch.json"):
        save_json(client.domain_overview(args.domain), out / "overview_ch.json")
        save_json(client.domain_history(args.domain), out / "overview_history_ch.json")

    print("== organic keywords (paginated, uncapped) ==")
    if fresh(out / "keywords_ch.json"):
        rows, complete = client.domain_keywords_all(args.domain)
        print(f"  {len(rows)} rows (complete={complete})")
        save_json(rows, out / "keywords_ch.json")
        meta["pulls"]["keywords_ch"] = {"rows": len(rows), "complete": complete}

    print("== ranking pages ==")
    if fresh(out / "pages_ch.json"):
        save_json(client.domain_pages(args.domain, limit=1000), out / "pages_ch.json")

    print("== competitors ==")
    if fresh(out / "competitors_ch.json"):
        save_json(client.domain_competitors(args.domain, limit=20), out / "competitors_ch.json")
    units(client, "domain analysis")

    print("== keyword gap vs competitors ==")
    # /domain/keywords/comparison only returns COMMON keywords (both domains in
    # top 100) — useful for "we're behind" analysis. For the true gap we pull
    # each competitor's top-20 keywords and diff against our set in the
    # analysis step.
    for comp in competitors:
        slug = comp.replace(".", "_")
        common_path = out / f"common_{slug}.json"
        if fresh(common_path):
            try:
                res = client.keyword_gap(args.domain, comp, limit=1000,
                                         order_field="volume", order_type="desc",
                                         **{"filter[volume][from]": 30})
                save_json(res, common_path)
            except RuntimeError as e:
                print(f"  !! common {comp} failed: {e}")
        comp_kw_path = out / f"comp_keywords_{slug}.json"
        if fresh(comp_kw_path):
            try:
                rows, complete = client.domain_keywords_all(
                    comp, max_pages=2,
                    order_field="volume", order_type="desc",
                    **{"filter[position][to]": 20, "filter[volume][from]": 50})
                save_json(rows, comp_kw_path)
                meta["pulls"][f"comp_keywords_{slug}"] = {"rows": len(rows), "complete": complete}
            except RuntimeError as e:
                print(f"  !! comp keywords {comp} failed: {e}")
    units(client, "keyword gap")

    print("== backlinks ==")
    if fresh(out / "backlinks_summary.json"):
        save_json(client.backlinks_summary(args.domain), out / "backlinks_summary.json")
        save_json(client.backlinks_authority(args.domain), out / "backlinks_authority.json")
    if fresh(out / "backlinks_refdomains.json"):
        try:
            save_json(client.backlinks_refdomains(args.domain, limit=300),
                      out / "backlinks_refdomains.json")
        except RuntimeError as e:
            print(f"  !! refdomains failed: {e}")
    for comp in competitors:
        path = out / f"backlinks_summary_{comp.replace('.', '_')}.json"
        if fresh(path):
            try:
                save_json(client.backlinks_summary(comp), path)
            except RuntimeError as e:
                print(f"  !! backlinks {comp} failed: {e}")
    meta["units_left_after"] = units(client, "backlinks")
    meta["credit_report"] = client.credit_report()
    save_json(meta, out / "meta.json")

    print("DONE")


if __name__ == "__main__":
    main()
