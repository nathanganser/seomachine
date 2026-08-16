#!/usr/bin/env python3
"""Create (or poll) an SE Ranking standard site audit.

Usage:
  python3 seranking_site_audit.py create                    # kick off crawl, prints audit_id
  python3 seranking_site_audit.py status <id>
  python3 seranking_site_audit.py fetch <id>                # save report + top issue pages
Options:
  --date YYYY-MM-DD   output snapshot dir (default: today) → audits/seranking-<date>/raw
  --out DIR           explicit output dir (overrides --date)
  --domain DOMAIN     default magicheidi.ch
  --max-pages N       crawl cap for create (default 1500; billed 2 credits/page)
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient, save_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["create", "status", "fetch"])
    ap.add_argument("audit_id", nargs="?", help="audit id (for status/fetch)")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--out", default=None)
    ap.add_argument("--domain", default="magicheidi.ch")
    ap.add_argument("--max-pages", type=int, default=1500)
    args = ap.parse_args()

    out_dir = Path(args.out) if args.out else (
        Path(__file__).parent / "audits" / f"seranking-{args.date}" / "raw")
    client = SERankingClient()

    if args.cmd == "create":
        res = client.audit_create_standard(args.domain, settings={"max_pages": args.max_pages})
        print(json.dumps(res, indent=2))
        save_json(res, out_dir / "audit_created.json")

    elif args.cmd == "status":
        print(json.dumps(client.audit_status(args.audit_id), indent=2))

    elif args.cmd == "fetch":
        report = client.audit_report(args.audit_id)
        save_json(report, out_dir / "audit_report.json")

        # Pull affected pages for every non-passed issue so fixes can be targeted.
        issue_pages = {}
        for section in report.get("sections", []):
            for issue in section.get("props", {}).values():
                code = issue.get("code")
                count = issue.get("value") or 0
                if (code and isinstance(count, int) and count > 0
                        and issue.get("status") in ("error", "warning")):
                    try:
                        issue_pages[code] = {
                            "name": issue.get("name"), "status": issue["status"],
                            "count": count,
                            "pages": client.audit_issue_pages(args.audit_id, code),
                        }
                    except RuntimeError as e:
                        issue_pages[code] = {"name": issue.get("name"), "error": str(e)}
        save_json(issue_pages, out_dir / "audit_issue_pages.json")
        print(f"Fetched report + pages for {len(issue_pages)} issues")


if __name__ == "__main__":
    main()
