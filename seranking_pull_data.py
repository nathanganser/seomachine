#!/usr/bin/env python3
"""Pull the full SE Ranking dataset for the magicheidi.ch audit.

Pulls (Switzerland database, source=ch):
  - domain overview + 12-month history
  - all organic keyword rankings (paginated)
  - ranking pages
  - organic competitors
  - keyword gap vs main competitors (keywords they rank top-20 for, we don't)
  - backlinks summary + authority + top referring domains (us + competitors)

Everything lands in audits/seranking-2026-08-01/raw/ as JSON.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient, save_json

DOMAIN = "magicheidi.ch"
COMPETITORS = ["bexio.com", "klara.ch", "banana.ch", "cashctrl.com", "abaninja.ch"]
OUT = Path(__file__).parent / "audits" / "seranking-2026-08-01" / "raw"


def units(client, label):
    left = client.subscription()["subscription_info"]["units_left"]
    print(f"[units] {left:,} left after {label}")
    return left


def main():
    client = SERankingClient(source="ch")
    units(client, "start")

    print("== domain overview ==")
    if not (OUT / "overview_ch.json").exists():
        save_json(client.domain_overview(DOMAIN), OUT / "overview_ch.json")
        save_json(client.domain_history(DOMAIN), OUT / "overview_history_ch.json")

    print("== organic keywords (paginated) ==")
    if not (OUT / "keywords_ch.json").exists() or len(sys.argv) > 1 and sys.argv[1] == "refresh-keywords":
        all_rows = []
        page = 1
        while True:
            res = client.domain_keywords(DOMAIN, limit=1000, page=page)
            rows = res if isinstance(res, list) else res.get("keywords", res.get("data", []))
            all_rows.extend(rows)
            print(f"  page {page}: {len(rows)} rows (total {len(all_rows)})")
            if len(rows) < 1000 or page >= 10:
                break
            page += 1
        save_json(all_rows, OUT / "keywords_ch.json")

    print("== ranking pages ==")
    save_json(client.domain_pages(DOMAIN, limit=1000), OUT / "pages_ch.json")

    print("== competitors ==")
    save_json(client.domain_competitors(DOMAIN, limit=20), OUT / "competitors_ch.json")
    units(client, "domain analysis")

    print("== keyword gap vs competitors ==")
    # /domain/keywords/comparison only returns COMMON keywords (both domains in
    # top 100) — useful for "we're behind" analysis. For the true gap we pull
    # each competitor's top-20 keywords and diff against our set in the
    # analysis step.
    for comp in COMPETITORS:
        slug = comp.replace(".", "_")
        common_path = OUT / f"common_{slug}.json"
        if not common_path.exists():
            try:
                res = client.keyword_gap(DOMAIN, comp, limit=1000,
                                         order_field="volume", order_type="desc",
                                         **{"filter[volume][from]": 30})
                save_json(res, common_path)
            except RuntimeError as e:
                print(f"  !! common {comp} failed: {e}")
        comp_kw_path = OUT / f"comp_keywords_{slug}.json"
        if not comp_kw_path.exists():
            rows = []
            try:
                for page in (1, 2):
                    res = client.domain_keywords(
                        comp, limit=1000, page=page,
                        order_field="volume", order_type="desc",
                        **{"filter[position][to]": 20, "filter[volume][from]": 50})
                    batch = res if isinstance(res, list) else res.get("keywords", [])
                    rows.extend(batch)
                    if len(batch) < 1000:
                        break
                save_json(rows, comp_kw_path)
            except RuntimeError as e:
                print(f"  !! comp keywords {comp} failed: {e}")
    units(client, "keyword gap")

    print("== backlinks ==")
    save_json(client.backlinks_summary(DOMAIN), OUT / "backlinks_summary.json")
    save_json(client.backlinks_authority(DOMAIN), OUT / "backlinks_authority.json")
    try:
        save_json(client.backlinks_refdomains(DOMAIN, limit=300), OUT / "backlinks_refdomains.json")
    except RuntimeError as e:
        print(f"  !! refdomains failed: {e}")
    for comp in COMPETITORS:
        try:
            save_json(client.backlinks_summary(comp), OUT / f"backlinks_summary_{comp.replace('.', '_')}.json")
        except RuntimeError as e:
            print(f"  !! backlinks {comp} failed: {e}")
    units(client, "backlinks")

    print("DONE")


if __name__ == "__main__":
    main()
