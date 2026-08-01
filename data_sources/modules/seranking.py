"""SE Ranking Data API client.

Base: https://api.seranking.com/v1 — auth via `Authorization: Token <key>`.
Key comes from SERANKING_API_KEY in data_sources/config/.env.

Docs: https://seranking.com/api/data/
Credit costs: domain-analysis endpoints ~100 units/call (up to 1000 rows),
site audit standard = 2 units/page, backlinks endpoints are per-row.
"""

import os
import time
import json
import requests
from pathlib import Path

API_BASE = "https://api.seranking.com/v1"
_ENV_PATH = Path(__file__).resolve().parents[1] / "config" / ".env"


def _load_key():
    key = os.environ.get("SERANKING_API_KEY")
    if key:
        return key
    if _ENV_PATH.exists():
        for line in _ENV_PATH.read_text().splitlines():
            if line.startswith("SERANKING_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("SERANKING_API_KEY not found in env or data_sources/config/.env")


class SERankingClient:
    def __init__(self, api_key=None, source="ch"):
        self.api_key = api_key or _load_key()
        self.source = source  # regional database: ch = Switzerland
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {self.api_key}"

    def _request(self, method, path, params=None, json_body=None, retries=3):
        url = f"{API_BASE}{path}"
        for attempt in range(retries):
            resp = self.session.request(method, url, params=params, json=json_body, timeout=120)
            if resp.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            if resp.status_code >= 500:
                time.sleep(3 * (attempt + 1))
                continue
            if resp.status_code >= 400:
                raise RuntimeError(f"{method} {path} -> {resp.status_code}: {resp.text[:500]}")
            return resp.json()
        raise RuntimeError(f"{method} {path} failed after {retries} retries")

    def get(self, path, **params):
        return self._request("GET", path, params=params)

    def post(self, path, body):
        return self._request("POST", path, json_body=body)

    # ---- Account ----
    def subscription(self):
        return self.get("/account/subscription")

    # ---- Domain analysis ----
    def domain_overview(self, domain, source=None):
        return self.get("/domain/overview/db", domain=domain, source=source or self.source)

    def domain_overview_worldwide(self, domain):
        return self.get("/domain/overview/worldwide", domain=domain)

    def domain_history(self, domain, source=None, **kw):
        return self.get("/domain/overview/history", domain=domain, source=source or self.source, **kw)

    def domain_keywords(self, domain, source=None, limit=1000, page=1, **filters):
        """Organic keyword rankings. Rows include keyword, position, volume, traffic, url."""
        return self.get("/domain/keywords", domain=domain, source=source or self.source,
                        limit=limit, page=page, type="organic", **filters)

    def domain_pages(self, domain, source=None, limit=1000, page=1, **kw):
        return self.get("/domain/pages", target=domain, scope="base_domain",
                        source=source or self.source, limit=limit, page=page, **kw)

    def domain_competitors(self, domain, source=None, limit=20, **kw):
        return self.get("/domain/competitors", domain=domain, source=source or self.source,
                        limit=limit, type="organic", **kw)

    def keyword_gap(self, domain, compare_domain, source=None, diff_mode="missing",
                    limit=1000, page=1, **filters):
        """Keyword overlap/gap between two domains.

        diff_mode: missing (they rank, we don't), common, all ...
        """
        return self.get("/domain/keywords/comparison", domain=domain,
                        compare=compare_domain, source=source or self.source,
                        diff_mode=diff_mode, limit=limit, page=page, **filters)

    # ---- Backlinks ----
    def backlinks_summary(self, target, mode="domain"):
        return self.get("/backlinks/summary", target=target, mode=mode)

    def backlinks_refdomains(self, target, mode="domain", limit=500, offset=0, **kw):
        return self.get("/backlinks/refdomains", target=target, mode=mode,
                        limit=limit, offset=offset, **kw)

    def backlinks_authority(self, target, mode="domain"):
        return self.get("/backlinks/authority", target=target, mode=mode)

    # ---- Site audit ----
    def audit_create_standard(self, domain, settings=None):
        body = {"domain": domain}
        if settings:
            body["settings"] = settings
        return self.post("/site-audit/audits/standard", body)

    def audit_status(self, audit_id):
        return self.get("/site-audit/audits/status", audit_id=audit_id)

    def audit_report(self, audit_id):
        return self.get("/site-audit/audits/report", audit_id=audit_id)

    def audit_issue_pages(self, audit_id, code, limit=250, offset=0):
        return self.get("/site-audit/audits/issue-pages", audit_id=audit_id, code=code,
                        limit=limit, offset=offset)

    def audit_list(self, limit=20):
        return self.get("/site-audit/audits", limit=limit)


def save_json(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"  saved {path} ({path.stat().st_size:,} bytes)")
