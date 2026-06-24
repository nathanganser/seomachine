import importlib.util
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data_sources"
    / "modules"
    / "vercel_analytics.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("vercel_analytics_under_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_csv(path: Path, rows, header="Page,Visitors,Total"):
    lines = [header] + [f'"{p}",{v},{t}' for p, v, t in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


class VercelAnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.dir = Path(self.tmpdir.name)

        # 1-day window
        _write_csv(
            self.dir / "Top Pages - Jun 3, 15_00 - Jun 4, 14_59.csv",
            [("/de/start", 10, 12), ("/de/feiertage", 50, 60)],
        )
        # 7-day window
        _write_csv(
            self.dir / "Top Pages - May 28, 14_00 - Jun 4, 14_59.csv",
            [("/de/start", 70, 80), ("/de/feiertage", 200, 240)],
        )
        # 30-day window
        _write_csv(
            self.dir / "Top Pages - May 5, 14_00 - Jun 4, 14_59.csv",
            [("/de/start", 300, 350), ("/de/feiertage", 800, 950)],
        )
        # 90-day window
        _write_csv(
            self.dir / "Top Pages - Mar 4, 13_00 - Jun 4, 14_59.csv",
            [("/de/start", 900, 1100), ("/de/feiertage", 2500, 3000)],
        )
        # Referrers
        _write_csv(
            self.dir / "Top Referrers - Mar 4, 13_00 - Jun 4, 14_59.csv",
            [("google.com", 5000, 6000), ("chatgpt.com", 200, 250)],
        )

        # Touch all files so mtime matches a recent year
        now = time.time()
        for p in self.dir.glob("*.csv"):
            os.utime(p, (now, now))

    def _ga(self):
        module = load_module()
        return module.VercelAnalytics(csv_dir=str(self.dir))

    def test_detects_all_four_windows(self):
        ga = self._ga()
        self.assertEqual(ga.available_windows, [1, 7, 30, 90])

    def test_get_top_pages_sorts_by_total(self):
        ga = self._ga()
        pages = ga.get_top_pages(days=30, limit=5, path_filter=None)
        self.assertEqual(pages[0]["path"], "/de/feiertage")
        self.assertEqual(pages[0]["pageviews"], 950)
        self.assertEqual(pages[1]["path"], "/de/start")

    def test_get_top_pages_respects_path_filter(self):
        ga = self._ga()
        pages = ga.get_top_pages(days=30, limit=5, path_filter="feiertage")
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]["path"], "/de/feiertage")

    def test_get_page_performance_exact_match(self):
        ga = self._ga()
        result = ga.get_page_performance("/de/start", days=30)
        self.assertEqual(result["pageviews"], 350)

    def test_get_page_performance_missing_returns_empty(self):
        ga = self._ga()
        self.assertEqual(ga.get_page_performance("/nope", days=30), {})

    def test_get_page_trends_detects_growth(self):
        ga = self._ga()
        # /de/feiertage: 1d=60, 90d=3000 -> per-day 60 vs 33 -> rising
        result = ga.get_page_trends("/de/feiertage", days=90)
        self.assertEqual(result["trend_direction"], "rising")
        self.assertEqual(len(result["timeline"]), 4)

    def test_get_traffic_sources_site_wide(self):
        ga = self._ga()
        sources = ga.get_traffic_sources(days=90)
        self.assertEqual(sources[0]["source"], "google.com")
        self.assertEqual(sources[0]["pageviews"], 6000)

    def test_get_traffic_sources_per_url_returns_empty(self):
        ga = self._ga()
        self.assertEqual(ga.get_traffic_sources(url="/de/start"), [])

    def test_get_conversions_returns_empty(self):
        ga = self._ga()
        self.assertEqual(ga.get_conversions(), [])

    def test_missing_csvs_raises(self):
        module = load_module()
        empty = tempfile.TemporaryDirectory()
        self.addCleanup(empty.cleanup)
        with self.assertRaises(ValueError):
            module.VercelAnalytics(csv_dir=empty.name)


if __name__ == "__main__":
    unittest.main()
