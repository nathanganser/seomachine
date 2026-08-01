#!/usr/bin/env python3
"""Create (or poll) an SE Ranking standard site audit for magicheidi.ch.

Usage:
  python3 seranking_site_audit.py create          # kick off crawl, prints audit_id
  python3 seranking_site_audit.py status <id>
  python3 seranking_site_audit.py fetch <id>      # save report + top issue pages
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data_sources" / "modules"))
from seranking import SERankingClient, save_json

DOMAIN = "magicheidi.ch"
OUT_DIR = Path(__file__).parent / "audits" / "seranking-2026-08-01" / "raw"


def main():
    client = SERankingClient()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "create"

    if cmd == "create":
        res = client.audit_create_standard(DOMAIN, settings={"max_pages": 1500})
        print(json.dumps(res, indent=2))
        save_json(res, OUT_DIR / "audit_created.json")

    elif cmd == "status":
        print(json.dumps(client.audit_status(sys.argv[2]), indent=2))

    elif cmd == "fetch":
        audit_id = sys.argv[2]
        report = client.audit_report(audit_id)
        save_json(report, OUT_DIR / "audit_report.json")

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
                            "pages": client.audit_issue_pages(audit_id, code),
                        }
                    except RuntimeError as e:
                        issue_pages[code] = {"name": issue.get("name"), "error": str(e)}
        save_json(issue_pages, OUT_DIR / "audit_issue_pages.json")
        print(f"Fetched report + pages for {len(issue_pages)} issues")


if __name__ == "__main__":
    main()
