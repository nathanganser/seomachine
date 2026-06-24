"""
Vercel Web Analytics (CSV-backed)

Replaces the previous GA4 integration with manually-exported CSVs from the
Vercel Web Analytics dashboard. Exposes the same interface as the old
`GoogleAnalytics` class so existing scripts work unchanged.

Expected files (live at repo root with Vercel's default export names):
  - Top Pages - <Mon DD>, <HH_MM> - <Mon DD>, <HH_MM>.csv
  - Top Referrers - <Mon DD>, <HH_MM> - <Mon DD>, <HH_MM>.csv

Each "Top Pages" file is bucketed to the closest standard window length
(1, 7, 30, or 90 days). Trend analysis compares pageviews across windows.

Fields that Vercel does not export (bounce_rate, engagement_rate,
avg_session_duration, conversions, per-page traffic sources) are returned as
zero/empty so callers degrade gracefully.

Override the CSV location with the VERCEL_ANALYTICS_DIR env var.
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_WINDOWS: Tuple[int, ...] = (1, 7, 30, 90)
_FILENAME_PATTERN = re.compile(
    r"^Top (?P<kind>Pages|Referrers) - "
    r"(?P<start>[A-Za-z]+ \d+), \d+_\d+ - "
    r"(?P<end>[A-Za-z]+ \d+), \d+_\d+\.csv$"
)


def _default_csv_dir() -> Path:
    env = os.getenv("VERCEL_ANALYTICS_DIR")
    if env:
        return Path(env)
    # modules/ -> data_sources/ -> repo root
    return Path(__file__).resolve().parents[2]


def _parse_window_days(filename: str, mtime: float) -> Optional[int]:
    """Extract the time-window length (rounded to a standard bucket) from a
    Vercel export filename. Returns None if the filename is unrecognised."""
    match = _FILENAME_PATTERN.match(filename)
    if not match:
        return None
    anchor_year = datetime.fromtimestamp(mtime).year
    try:
        end_dt = datetime.strptime(f"{match['end']}, {anchor_year}", "%b %d, %Y")
        start_dt = datetime.strptime(f"{match['start']}, {anchor_year}", "%b %d, %Y")
    except ValueError:
        return None
    if start_dt > end_dt:
        start_dt = start_dt.replace(year=anchor_year - 1)
    span = max(1, (end_dt - start_dt).days)
    return min(_WINDOWS, key=lambda w: abs(w - span))


def _bucket_files(csv_dir: Path, kind: str) -> Dict[int, Path]:
    """Map standard window length -> most-recently-modified matching CSV."""
    best: Dict[int, Tuple[float, Path]] = {}
    for path in csv_dir.glob(f"Top {kind}*.csv"):
        mtime = path.stat().st_mtime
        window = _parse_window_days(path.name, mtime)
        if window is None:
            continue
        existing = best.get(window)
        if existing is None or mtime > existing[0]:
            best[window] = (mtime, path)
    return {window: p for window, (_, p) in best.items()}


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                rows.append({
                    "page": row["Page"],
                    "visitors": int(row["Visitors"]),
                    "total": int(row["Total"]),
                })
            except (KeyError, ValueError):
                continue
    return rows


class VercelAnalytics:
    """Vercel Web Analytics fetcher (CSV-backed).

    API-compatible with the prior `GoogleAnalytics` class. Some fields that
    GA4 exposed are not present in Vercel CSV exports and are returned as
    zero/empty values.
    """

    def __init__(self, csv_dir: Optional[str] = None):
        self.csv_dir: Path = Path(csv_dir) if csv_dir else _default_csv_dir()
        self._pages_files = _bucket_files(self.csv_dir, "Pages")
        self._referrers_files = _bucket_files(self.csv_dir, "Referrers")
        if not self._pages_files:
            raise ValueError(
                f"No 'Top Pages*.csv' exports found in {self.csv_dir}. "
                "Export them from the Vercel Web Analytics dashboard."
            )

    @property
    def available_windows(self) -> List[int]:
        return sorted(self._pages_files.keys())

    def _pages_for_window(self, days: int) -> List[Dict[str, Any]]:
        window = min(self._pages_files.keys(), key=lambda w: abs(w - days))
        return _read_csv(self._pages_files[window])

    def get_top_pages(
        self,
        days: int = 30,
        limit: int = 20,
        path_filter: Optional[str] = "/blog/",
    ) -> List[Dict[str, Any]]:
        rows = self._pages_for_window(days)
        if path_filter:
            rows = [r for r in rows if path_filter in r["page"]]
        rows.sort(key=lambda r: r["total"], reverse=True)
        return [
            {
                "path": row["page"],
                "title": row["page"],
                "pageviews": row["total"],
                "sessions": row["visitors"],
                "avg_session_duration": 0.0,
                "avg_engagement_time": 0.0,
                "bounce_rate": 0.0,
                "engagement_rate": 0.0,
            }
            for row in rows[:limit]
        ]

    def get_page_performance(
        self, url: str, days: int = 30
    ) -> Dict[str, Any]:
        pages = self.get_top_pages(days=days, limit=10_000, path_filter=None)
        for page in pages:
            if page["path"] == url:
                return page
        for page in pages:
            if url and url in page["path"]:
                return page
        return {}

    def get_page_trends(
        self, url: str, days: int = 90, granularity: str = "week"
    ) -> Dict[str, Any]:
        del granularity  # CSVs only support discrete windows, not granularity

        timeline: List[Dict[str, Any]] = []
        for window in sorted(self._pages_files.keys()):
            if window > days:
                continue
            views = 0
            for row in self._pages_for_window(window):
                if row["page"] == url:
                    views = row["total"]
                    break
            timeline.append({
                "period": f"{window}d",
                "pageviews": views,
                "sessions": 0,
                "avg_duration": 0.0,
            })

        if len(timeline) >= 2:
            # Compare per-day rate in shortest window vs widest window.
            short = timeline[0]
            wide = timeline[-1]
            short_days = int(short["period"].rstrip("d")) or 1
            wide_days = int(wide["period"].rstrip("d")) or 1
            recent_per_day = short["pageviews"] / short_days
            older_per_day = wide["pageviews"] / wide_days
            if older_per_day > 0:
                trend_percent = ((recent_per_day - older_per_day) / older_per_day) * 100
            else:
                trend_percent = 0.0
            if trend_percent > 10:
                trend_direction = "rising"
            elif trend_percent < -10:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
        else:
            trend_percent = 0.0
            trend_direction = "unknown"

        total_pageviews = timeline[-1]["pageviews"] if timeline else 0

        return {
            "url": url,
            "timeline": timeline,
            "trend_direction": trend_direction,
            "trend_percent": round(trend_percent, 2),
            "total_pageviews": total_pageviews,
        }

    def get_conversions(
        self, days: int = 30, path_filter: Optional[str] = "/blog/"
    ) -> List[Dict[str, Any]]:
        del days, path_filter
        return []

    def get_traffic_sources(
        self, url: Optional[str] = None, days: int = 30
    ) -> List[Dict[str, Any]]:
        if url is not None:
            # Per-page referrer breakdown isn't in the CSV export.
            return []
        if not self._referrers_files:
            return []
        window = min(self._referrers_files.keys(), key=lambda w: abs(w - days))
        rows = _read_csv(self._referrers_files[window])
        rows.sort(key=lambda r: r["total"], reverse=True)
        return [
            {
                "source": row["page"],
                "sessions": row["visitors"],
                "pageviews": row["total"],
                "engagement_rate": 0.0,
            }
            for row in rows
        ]

    def get_declining_pages(
        self,
        comparison_days: int = 30,
        threshold_percent: float = -20.0,
        path_filter: str = "/blog/",
    ) -> List[Dict[str, Any]]:
        windows = sorted(self._pages_files.keys())
        recent_window = min(windows, key=lambda w: abs(w - comparison_days))
        # Use the widest window strictly wider than recent_window as the prior baseline.
        wider = [w for w in windows if w > recent_window]
        if not wider:
            return []
        older_window = max(wider)

        recent = {
            p["path"]: p
            for p in self.get_top_pages(
                days=recent_window, limit=10_000, path_filter=path_filter
            )
        }
        older = {
            p["path"]: p
            for p in self.get_top_pages(
                days=older_window, limit=10_000, path_filter=path_filter
            )
        }

        prior_days = older_window - recent_window
        declining: List[Dict[str, Any]] = []
        for path, recent_page in recent.items():
            older_page = older.get(path)
            if not older_page:
                continue
            prior_views = older_page["pageviews"] - recent_page["pageviews"]
            if prior_views <= 0 or prior_days <= 0:
                continue
            recent_per_day = recent_page["pageviews"] / recent_window
            prior_per_day = prior_views / prior_days
            if prior_per_day <= 0:
                continue
            change_percent = ((recent_per_day - prior_per_day) / prior_per_day) * 100
            if change_percent < threshold_percent:
                declining.append({
                    **recent_page,
                    "previous_pageviews": prior_views,
                    "change_percent": round(change_percent, 2),
                    "priority": "high" if change_percent < -40 else "medium",
                })
        declining.sort(key=lambda x: x["change_percent"])
        return declining


if __name__ == "__main__":
    va = VercelAnalytics()
    print(f"CSV directory: {va.csv_dir}")
    print(f"Available windows: {va.available_windows} day(s)")
    print()
    print("Top 10 pages (30-day window):")
    for i, page in enumerate(va.get_top_pages(days=30, limit=10, path_filter=None), 1):
        print(f"{i:2d}. {page['pageviews']:>6,} views  {page['path']}")

    sources = va.get_traffic_sources(days=90)
    if sources:
        print("\nTop traffic sources:")
        for src in sources[:10]:
            print(f"  {src['pageviews']:>6,} views from {src['source']}")
