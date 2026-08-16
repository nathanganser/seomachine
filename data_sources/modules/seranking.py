"""SE Ranking Data API client.

Base: https://api.seranking.com/v1 — auth via `Authorization: Token <key>`.
Key comes from SERANKING_API_KEY in data_sources/config/.env.

Docs: https://seranking.com/api/data/
Credit costs (estimates, see CREDIT_COSTS): domain-analysis endpoints ~100
units/call (up to 1000 rows), keywords/export 100/request,
keywords similar|related|questions 10/returned row, longtail 1/row,
ai-search time-series 800, discover-brand 100, prompts 200/prompt,
leaderboard 7500 flat, site audit standard = 2 units/page,
backlinks endpoints are per-row.

Note (2026-08-16): the platform subscription is expired, so the Project API
(/projects rank tracker) returns 401 and the account units_left counter can be
stale/frozen. The Data API keeps working on prepaid credits; the client's
estimated-spend counter (credit_report) is the reliable spend signal.
"""

import os
import time
import json
import requests
from pathlib import Path

from dotenv import load_dotenv

API_BASE = "https://api.seranking.com/v1"
_ENV_PATH = Path(__file__).resolve().parents[1] / "config" / ".env"

AI_ENGINES = ("chatgpt", "perplexity", "gemini", "ai-overview", "ai-mode")

# (flat credits per call, credits per returned row) keyed by path prefix.
CREDIT_COSTS = {
    "/keywords/export": (100, 0),
    "/keywords/similar": (0, 10),
    "/keywords/related": (0, 10),
    "/keywords/questions": (0, 10),
    "/keywords/longtail": (0, 1),
    "/ai-search/overview/by-engine/time-series": (800, 0),
    "/ai-search/overview/leaderboard": (7500, 0),
    "/ai-search/discover-brand": (100, 0),
    "/ai-search/prompts-by-target": (0, 200),
    "/ai-search/prompts-by-brand": (0, 200),
    "/backlinks/refdomains": (0, 1),
    "/backlinks": (100, 0),
    "/domain": (100, 0),
    "/site-audit": (0, 0),  # standard audit bills 2/page at crawl time, not per call
    "/account": (0, 0),
}


def _load_key():
    key = os.environ.get("SERANKING_API_KEY")
    if key:
        return key
    load_dotenv(_ENV_PATH)
    key = os.environ.get("SERANKING_API_KEY")
    if key:
        return key
    raise RuntimeError("SERANKING_API_KEY not found in env or data_sources/config/.env")


def _rows(res, *keys):
    """Extract the row list from a response that may be a bare list or a dict."""
    if isinstance(res, list):
        return res
    if isinstance(res, dict):
        for k in keys + ("keywords", "data", "items", "refdomains", "prompts"):
            if isinstance(res.get(k), list):
                return res[k]
    return []


class SERankingClient:
    def __init__(self, api_key=None, source="ch"):
        self.api_key = api_key or _load_key()
        self.source = source  # regional database: ch = Switzerland
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {self.api_key}"
        self.calls = []  # (path, est_credits) per successful request

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
            data = resp.json()
            self.calls.append((path, self._estimate_credits(path, data)))
            return data
        raise RuntimeError(f"{method} {path} failed after {retries} retries")

    @staticmethod
    def _estimate_credits(path, data):
        for prefix, (flat, per_row) in CREDIT_COSTS.items():
            if path.startswith(prefix):
                return flat + per_row * (len(_rows(data)) if per_row else 0)
        return 100  # unknown endpoint: assume a standard-cost call

    def credit_report(self):
        by_path = {}
        for path, est in self.calls:
            agg = by_path.setdefault(path, {"calls": 0, "est_credits": 0})
            agg["calls"] += 1
            agg["est_credits"] += est
        return {
            "total_calls": len(self.calls),
            "total_est_credits": sum(est for _, est in self.calls),
            "by_path": by_path,
        }

    def get(self, path, **params):
        return self._request("GET", path, params=params)

    def post(self, path, body):
        return self._request("POST", path, json_body=body)

    def paginate(self, path, limit=1000, max_pages=None, row_keys=(), **params):
        """Page through a page/limit endpoint until a short page.

        Returns (rows, complete) — complete is False only when max_pages cut
        the pull short, so downstream comparisons can tell truncation from
        genuinely-absent keywords.
        """
        rows, page = [], 1
        while True:
            res = self.get(path, limit=limit, page=page, **params)
            batch = _rows(res, *row_keys)
            rows.extend(batch)
            if len(batch) < limit:
                return rows, True
            if max_pages and page >= max_pages:
                return rows, False
            page += 1

    # ---- Account ----
    def subscription(self):
        return self.get("/account/subscription")

    def units_left(self):
        return self.subscription()["subscription_info"]["units_left"]

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

    def domain_keywords_all(self, domain, source=None, max_pages=None, **filters):
        """All organic keyword rows, paginated until exhausted. Returns (rows, complete)."""
        return self.paginate("/domain/keywords", domain=domain,
                             source=source or self.source, type="organic",
                             max_pages=max_pages, **filters)

    def domain_pages(self, domain, source=None, limit=1000, page=1, **kw):
        return self.get("/domain/pages", target=domain, scope="base_domain",
                        source=source or self.source, limit=limit, page=page, **kw)

    def domain_pages_all(self, domain, source=None, max_pages=None, **kw):
        return self.paginate("/domain/pages", target=domain, scope="base_domain",
                             source=source or self.source, row_keys=("pages",),
                             max_pages=max_pages, **kw)

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

    def keyword_gap_all(self, domain, compare_domain, source=None, diff_mode="missing",
                        max_pages=None, **filters):
        return self.paginate("/domain/keywords/comparison", domain=domain,
                             compare=compare_domain, source=source or self.source,
                             diff_mode=diff_mode, max_pages=max_pages, **filters)

    # ---- Keyword research ----
    def keywords_export(self, keywords, source=None, **kw):
        """Bulk metrics (volume, cpc, difficulty, competition, intents, 12-mo
        history_trend) for up to 5000 keywords per request; chunks automatically.
        100 credits per request."""
        out = []
        keywords = list(keywords)
        for i in range(0, len(keywords), 5000):
            res = self.post(f"/keywords/export?source={source or self.source}",
                            {"keywords": keywords[i:i + 5000], **kw})
            out.extend(res if isinstance(res, list) else _rows(res))
        return out

    def keywords_similar(self, keyword, source=None, limit=100, **filters):
        """Similar keywords — 10 credits per returned row."""
        return self.get("/keywords/similar", keyword=keyword,
                        source=source or self.source, limit=limit, **filters)

    def keywords_related(self, keyword, source=None, limit=100, **filters):
        """Related keywords — 10 credits per returned row."""
        return self.get("/keywords/related", keyword=keyword,
                        source=source or self.source, limit=limit, **filters)

    def keywords_questions(self, keyword, source=None, limit=100, **filters):
        """Question keywords — 10 credits per returned row."""
        return self.get("/keywords/questions", keyword=keyword,
                        source=source or self.source, limit=limit, **filters)

    def keywords_longtail(self, keyword, source=None, limit=200, **filters):
        """Longtail keyword ideas — 1 credit per returned row."""
        return self.get("/keywords/longtail", keyword=keyword,
                        source=source or self.source, limit=limit, **filters)

    # ---- AI search ----
    def ai_timeseries(self, target, engine, source=None, **kw):
        """Brand/link presence + avg position in one LLM engine. 800 credits."""
        if engine not in AI_ENGINES:
            raise ValueError(f"engine must be one of {AI_ENGINES}")
        return self.get("/ai-search/overview/by-engine/time-series",
                        engine=engine, target=target, source=source or self.source, **kw)

    def ai_discover_brand(self, target, source=None, scope="base_domain"):
        """Brand names associated with a domain. 100 credits."""
        return self.get("/ai-search/discover-brand", target=target,
                        source=source or self.source, scope=scope)

    def ai_prompts_by_target(self, target, engine, source=None, scope="base_domain",
                             limit=25, **kw):
        """Prompts where the target appears in LLM answers. 200 credits/prompt."""
        return self.get("/ai-search/prompts-by-target", target=target, engine=engine,
                        source=source or self.source, scope=scope, limit=limit, **kw)

    def ai_prompts_by_brand(self, brand, engine, source=None, limit=25, **kw):
        """Prompts mentioning the brand. 200 credits/prompt."""
        return self.get("/ai-search/prompts-by-brand", brand=brand, engine=engine,
                        source=source or self.source, limit=limit, **kw)

    def ai_leaderboard(self, target, competitors, engines, source=None, brand=None,
                       confirm_cost=False):
        """Share-of-voice leaderboard vs up to 10 competitors. 7500 credits flat —
        requires confirm_cost=True to run."""
        if not confirm_cost:
            raise RuntimeError("ai_leaderboard costs 7500 credits — pass confirm_cost=True to run")
        primary = {"target": target}
        if brand:
            primary["brand"] = brand
        return self.post("/ai-search/overview/leaderboard", {
            "primary": primary,
            "competitors": [{"target": c} for c in competitors][:10],
            "source": source or self.source,
            "engines": list(engines),
        })

    # ---- Backlinks ----
    def backlinks_summary(self, target, mode="domain"):
        return self.get("/backlinks/summary", target=target, mode=mode)

    def backlinks_refdomains(self, target, mode="domain", limit=500, offset=0, **kw):
        return self.get("/backlinks/refdomains", target=target, mode=mode,
                        limit=limit, offset=offset, **kw)

    def backlinks_refdomains_all(self, target, mode="domain", limit=500,
                                 max_rows=3000, **kw):
        """Referring domains, offset-paginated. Per-row billing — max_rows caps spend."""
        rows, offset = [], 0
        while True:
            res = self.backlinks_refdomains(target, mode=mode, limit=limit,
                                            offset=offset, **kw)
            batch = _rows(res)
            rows.extend(batch)
            if len(batch) < limit or len(rows) >= max_rows:
                return rows
            offset += limit

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
