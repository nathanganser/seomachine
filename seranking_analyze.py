#!/usr/bin/env python3
"""Analyze a pulled SE Ranking snapshot.

Produces CSVs + a markdown summary in audits/seranking-<date>/:
  - cannibalization.csv     keyword groups splitting across >1 URL
  - locale_leaks.csv        keywords still ranking with legacy /de/ URLs
  - quick_wins.csv          positions 4-20, meaningful volume
  - striking_distance_*.csv competitor top-10 where we sit 11-30
  - gap_*.csv               competitor top-20 keywords we don't rank for at all
  - top_pages.csv           traffic distribution by page
  - summary.md              headline numbers

Sections whose raw file is missing are skipped (partial snapshots are fine).

Usage:
  python3 seranking_analyze.py --date 2026-09-01   (default: latest snapshot)
"""

import argparse
import csv
import json
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

REPO = Path(__file__).parent

STOPWORDS = set("""der die das den dem des ein eine einer eines einem und oder mit für fur von zu zum zur im in am auf an bei als was ist wie wo wann warum wer man
the a an of for to and or with in on at is how what when la le les l un une des du de d en et pour sur que qui est comment ou
di il lo la i gli le un una e o con per da su che come dove""".split())


def norm_key(keyword):
    tokens = [t for t in re.findall(r"\w+", keyword.lower()) if t not in STOPWORDS]
    return " ".join(sorted(tokens))


def path_of(url):
    return urlparse(url).path or "/"


def canonical_path(url):
    """Legacy /de/ URLs 301 to bare paths (German is default locale) — treat as same page."""
    p = path_of(url)
    return p[3:] or "/" if p.startswith("/de/") else p


BRAND_RE = re.compile(r"bexio|klara|clara\b|banana|cashctrl|abaninja|abacus|swiss21|smallinvoice|zervant|atlanto|accounto", re.I)


def latest_snapshot_date():
    dirs = sorted(REPO.glob("audits/seranking-????-??-??"))
    if not dirs:
        raise SystemExit("no audits/seranking-YYYY-MM-DD snapshot found")
    return dirs[-1].name.replace("seranking-", "")


def competitor_slugs(raw):
    meta_f = raw / "meta.json"
    if meta_f.exists():
        comps = json.load(open(meta_f)).get("competitors")
        if comps:
            return [c.replace(".", "_") for c in comps]
    return sorted(f.stem.replace("comp_keywords_", "")
                  for f in raw.glob("comp_keywords_*.json"))


def write_csv(rows, path, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: {len(rows)} rows")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="snapshot date (default: latest)")
    args = ap.parse_args()
    date = args.date or latest_snapshot_date()
    base = REPO / "audits" / f"seranking-{date}"
    raw = base / "raw"
    if not raw.exists():
        raise SystemExit(f"{raw} does not exist — run seranking_pull_data.py --date {date} first")
    competitors = competitor_slugs(raw)
    print(f"snapshot: {date}  competitors: {competitors}")

    cann, leaks, wins = [], [], []
    keywords = json.load(open(raw / "keywords_ch.json")) if (raw / "keywords_ch.json").exists() else None
    if keywords is None:
        print("  !! keywords_ch.json missing — skipping keyword sections")
    else:
        # ---- 1. Cannibalization: same normalized keyword group -> multiple URLs
        groups = defaultdict(list)
        for row in keywords:
            if row.get("position") and row["position"] <= 40 and (row.get("volume") or 0) >= 20:
                groups[norm_key(row["keyword"])].append(row)
        for key, rows in groups.items():
            urls = {canonical_path(r["url"]) for r in rows}
            if len(urls) > 1:
                vol = max(r["volume"] for r in rows)
                best = min(r["position"] for r in rows)
                cann.append({
                    "group": key,
                    "keywords": " | ".join(sorted({r["keyword"] for r in rows})[:6]),
                    "urls": " | ".join(sorted(urls)),
                    "n_urls": len(urls),
                    "max_volume": vol,
                    "best_position": best,
                    "positions": " | ".join(str(r["position"]) for r in rows[:8]),
                })
        cann.sort(key=lambda r: -r["max_volume"])
        write_csv(cann, base / "cannibalization.csv",
                  ["group", "keywords", "urls", "n_urls", "max_volume", "best_position", "positions"])

        # ---- 2. Locale leaks: legacy /de/ URLs still ranking (bare URLs are German now)
        leaks = [
            {"keyword": r["keyword"], "position": r["position"], "volume": r.get("volume") or 0,
             "traffic": r.get("traffic") or 0, "url": path_of(r["url"])}
            for r in keywords
            if path_of(r["url"]).startswith("/de/") and r.get("position") and r["position"] <= 30
            and (r.get("volume") or 0) >= 20
        ]
        leaks.sort(key=lambda r: -r["traffic"])
        write_csv(leaks, base / "locale_leaks.csv", ["keyword", "position", "volume", "traffic", "url"])

        # ---- 3. Quick wins: positions 4-20, volume >= 50
        wins = [
            {"keyword": r["keyword"], "position": r["position"], "volume": r["volume"],
             "traffic": r.get("traffic") or 0, "difficulty": r.get("difficulty"),
             "intents": ",".join(r.get("intents") or []), "url": path_of(r["url"])}
            for r in keywords
            if r.get("position") and 4 <= r["position"] <= 20 and (r.get("volume") or 0) >= 50
        ]
        wins.sort(key=lambda r: -(r["volume"] / r["position"]))
        write_csv(wins, base / "quick_wins.csv",
                  ["keyword", "position", "volume", "traffic", "difficulty", "intents", "url"])

        # ---- 4/5. Striking distance + true gap per competitor
        our_kw = {r["keyword"].lower() for r in keywords}
        for comp in competitors:
            common_f = raw / f"common_{comp}.json"
            if common_f.exists():
                common = json.load(open(common_f))
                sd = [
                    {"keyword": r["keyword"], "volume": r["volume"], "our_pos": r["position"],
                     "their_pos": r["compare_position"], "our_url": path_of(r["url"]),
                     "their_url": r.get("compare_url", "")}
                    for r in common
                    if r.get("compare_position") and r["compare_position"] <= 10
                    and r.get("position") and 11 <= r["position"] <= 30
                ]
                sd.sort(key=lambda r: -r["volume"])
                write_csv(sd, base / f"striking_distance_{comp}.csv",
                          ["keyword", "volume", "our_pos", "their_pos", "our_url", "their_url"])
            comp_f = raw / f"comp_keywords_{comp}.json"
            if comp_f.exists():
                comp_rows = json.load(open(comp_f))
                best = {}
                for r in comp_rows:
                    k = r["keyword"].lower()
                    if k in our_kw or (r.get("volume") or 0) < 50 or BRAND_RE.search(k):
                        continue
                    if k not in best or r["position"] < best[k]["position"]:
                        best[k] = r
                gap = [
                    {"keyword": r["keyword"], "volume": r["volume"], "their_pos": r["position"],
                     "difficulty": r.get("difficulty"), "cpc": r.get("cpc"),
                     "intents": ",".join(r.get("intents") or []),
                     "their_url": r.get("url", "")}
                    for r in best.values()
                ]
                gap.sort(key=lambda r: -r["volume"])
                write_csv(gap, base / f"gap_{comp}.csv",
                          ["keyword", "volume", "their_pos", "difficulty", "cpc", "intents", "their_url"])

    # ---- 6. Top pages
    if (raw / "pages_ch.json").exists():
        pages = json.load(open(raw / "pages_ch.json"))
        tp = [
            {"url": path_of(p["url"]), "traffic": p["traffic_sum"], "traffic_pct": p["traffic_percent"],
             "keywords": p["keywords_count"], "title": (p.get("title") or "")[:80]}
            for p in pages
        ]
        tp.sort(key=lambda r: -r["traffic"])
        write_csv(tp, base / "top_pages.csv", ["url", "traffic", "traffic_pct", "keywords", "title"])
    else:
        print("  !! pages_ch.json missing — skipping top_pages")

    # ---- 7. Summary
    if not (raw / "overview_ch.json").exists():
        print("  !! overview_ch.json missing — skipping summary")
        return
    overview = json.load(open(raw / "overview_ch.json"))
    if isinstance(overview, list):
        overview = overview[0]
    org = overview["organic"]
    lines = [
        f"# SE Ranking data summary — snapshot {date} (CH database)",
        "",
        f"- Organic keywords: {org['keywords_count']:,} (top1-5: {org.get('top1_5')}, top6-10: {org.get('top6_10')}, "
        f"top11-20: {org.get('top11_20')}, top21-50: {org.get('top21_50')}, top51-100: {org.get('top51_100')})",
        f"- Est. organic traffic: {org['traffic_sum']:,}/mo — value ${org['price_sum']:,.0f}",
    ]
    if org.get("keywords_new_count") is not None:
        lines.append(f"- Keywords new/lost last month: +{org['keywords_new_count']:,} / -{org['keywords_lost_count']:,}")
    if (raw / "backlinks_summary.json").exists():
        bl = json.load(open(raw / "backlinks_summary.json"))
        ours = bl["summary"][0]
        auth = {}
        if (raw / "backlinks_authority.json").exists():
            auth = json.load(open(raw / "backlinks_authority.json"))
        lines.append(f"- Backlinks: {ours['backlinks']:,} from {ours['refdomains']:,} ref domains — authority: {json.dumps(auth)}")
    comp_lines = []
    for comp in competitors:
        f = raw / f"backlinks_summary_{comp}.json"
        if f.exists():
            s = json.load(open(f))["summary"][0]
            dr = s.get("inlink_rank") or s.get("domain_inlink_rank")
            comp_lines.append(f"- {comp}: DR {dr}, {s['refdomains']:,} ref domains, {s['backlinks']:,} backlinks")
    if comp_lines:
        lines += ["", "## Competitor authority"] + comp_lines
    if keywords is not None:
        lines += [
            "",
            f"- Cannibalization groups: {len(cann)}",
            f"- Legacy /de/ keywords still ranking (top 30): {len(leaks)}",
            f"- Quick wins (pos 4-20, vol>=50): {len(wins)}",
        ]
    (base / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
