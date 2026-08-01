#!/usr/bin/env python3
"""Analyze the pulled SE Ranking data for magicheidi.ch.

Produces CSVs + a markdown summary in audits/seranking-2026-08-01/:
  - cannibalization.csv     keyword groups splitting across >1 URL
  - locale_leaks.csv        keywords still ranking with legacy /de/ URLs
  - quick_wins.csv          positions 4-20, meaningful volume
  - striking_distance_*.csv competitor top-10 where we sit 11-30
  - gap_*.csv               competitor top-20 keywords we don't rank for at all
  - top_pages.csv           traffic distribution by page
  - summary.md              headline numbers
"""

import csv
import json
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

BASE = Path(__file__).parent / "audits" / "seranking-2026-08-01"
RAW = BASE / "raw"
COMPETITORS = ["bexio_com", "klara_ch", "banana_ch", "cashctrl_com", "abaninja_ch"]

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


def write_csv(rows, path, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: {len(rows)} rows")


def main():
    keywords = json.load(open(RAW / "keywords_ch.json"))
    pages = json.load(open(RAW / "pages_ch.json"))

    # ---- 1. Cannibalization: same normalized keyword group -> multiple URLs
    groups = defaultdict(list)
    for row in keywords:
        if row.get("position") and row["position"] <= 40 and (row.get("volume") or 0) >= 20:
            groups[norm_key(row["keyword"])].append(row)
    cann = []
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
    write_csv(cann, BASE / "cannibalization.csv",
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
    write_csv(leaks, BASE / "locale_leaks.csv", ["keyword", "position", "volume", "traffic", "url"])

    # ---- 3. Quick wins: positions 4-20, volume >= 50
    wins = [
        {"keyword": r["keyword"], "position": r["position"], "volume": r["volume"],
         "traffic": r.get("traffic") or 0, "difficulty": r.get("difficulty"),
         "intents": ",".join(r.get("intents") or []), "url": path_of(r["url"])}
        for r in keywords
        if r.get("position") and 4 <= r["position"] <= 20 and (r.get("volume") or 0) >= 50
    ]
    wins.sort(key=lambda r: -(r["volume"] / r["position"]))
    write_csv(wins, BASE / "quick_wins.csv",
              ["keyword", "position", "volume", "traffic", "difficulty", "intents", "url"])

    # ---- 4/5. Striking distance + true gap per competitor
    our_kw = {r["keyword"].lower() for r in keywords}
    for comp in COMPETITORS:
        common_f = RAW / f"common_{comp}.json"
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
            write_csv(sd, BASE / f"striking_distance_{comp}.csv",
                      ["keyword", "volume", "our_pos", "their_pos", "our_url", "their_url"])
        comp_f = RAW / f"comp_keywords_{comp}.json"
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
            write_csv(gap, BASE / f"gap_{comp}.csv",
                      ["keyword", "volume", "their_pos", "difficulty", "cpc", "intents", "their_url"])

    # ---- 6. Top pages
    tp = [
        {"url": path_of(p["url"]), "traffic": p["traffic_sum"], "traffic_pct": p["traffic_percent"],
         "keywords": p["keywords_count"], "title": (p.get("title") or "")[:80]}
        for p in pages
    ]
    tp.sort(key=lambda r: -r["traffic"])
    write_csv(tp, BASE / "top_pages.csv", ["url", "traffic", "traffic_pct", "keywords", "title"])

    # ---- 7. Summary
    overview = json.load(open(RAW / "overview_ch.json"))
    bl = json.load(open(RAW / "backlinks_summary.json"))
    auth = json.load(open(RAW / "backlinks_authority.json"))
    org = overview["organic"]
    comp_dr = {}
    for comp in COMPETITORS:
        f = RAW / f"backlinks_summary_{comp}.json"
        if f.exists():
            s = json.load(open(f))["summary"][0]
            comp_dr[comp] = (s.get("inlink_rank") or s.get("domain_inlink_rank"), s["refdomains"], s["backlinks"])
    ours = bl["summary"][0]
    lines = [
        "# SE Ranking data summary — magicheidi.ch (CH database)",
        "",
        f"- Organic keywords: {org['keywords_count']:,} (top1-5: {org['top1_5']}, top6-10: {org['top6_10']}, "
        f"top11-20: {org['top11_20']}, top21-50: {org['top21_50']}, top51-100: {org['top51_100']})",
        f"- Est. organic traffic: {org['traffic_sum']:,}/mo — value ${org['price_sum']:,.0f}",
        f"- Keywords new/lost last month: +{org['keywords_new_count']:,} / -{org['keywords_lost_count']:,}",
        f"- Backlinks: {ours['backlinks']:,} from {ours['refdomains']:,} ref domains — authority: {json.dumps(auth)}",
        "",
        "## Competitor authority",
    ]
    for comp, (dr, rd, blc) in comp_dr.items():
        lines.append(f"- {comp}: DR {dr}, {rd:,} ref domains, {blc:,} backlinks")
    lines += [
        "",
        f"- Cannibalization groups: {len(cann)}",
        f"- Legacy /de/ keywords still ranking (top 30): {len(leaks)}",
        f"- Quick wins (pos 4-20, vol>=50): {len(wins)}",
    ]
    (BASE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
