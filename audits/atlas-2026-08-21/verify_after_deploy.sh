#!/usr/bin/env bash
# Post-deploy verification for the Atlas "Option A" prune.
# Run AFTER merging seo/option-a-prune to main and letting Render finish deploying.
#   bash audits/atlas-2026-08-21/verify_after_deploy.sh
# Exits non-zero if any check fails.

set -uo pipefail
BASE="${ATLAS_BASE:-https://atlas.magicheidi.ch}"
fail=0

code() { curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$BASE$1"; }
redir() { curl -s -o /dev/null -w '%{redirect_url}' --max-time 20 "$BASE$1"; }
robots() { curl -sL --max-time 20 "$BASE$1" | grep -oE 'name="robots" content="[^"]*"' | head -1; }

check() { # check <label> <actual> <expected>
  if [ "$2" = "$3" ]; then
    printf '  \033[32mPASS\033[0m  %-52s %s\n' "$1" "$2"
  else
    printf '  \033[31mFAIL\033[0m  %-52s got %s, want %s\n' "$1" "$2" "$3"; fail=1
  fi
}

echo
echo "=== 1. Locale cut: only /fr/ survives ==============================="
check "/de/"                                   "$(code /de/)"  410
check "/it/"                                   "$(code /it/)"  410
check "/en/"                                   "$(code /en/)"  410
check "/de/firma/apco-technologies-s-a-che107430655" \
                                               "$(code /de/firma/apco-technologies-s-a-che107430655)" 410
check "/fr/ still 200"                         "$(code /fr/)"  200
r=$(redir /); case "$r" in *"/fr/"*) printf '  \033[32mPASS\033[0m  %-52s %s\n' "/ redirects to /fr/" "$r";;
  *) printf '  \033[31mFAIL\033[0m  %-52s got %s\n' "/ redirects to /fr/" "${r:-<none>}"; fail=1;; esac

echo
echo "=== 2. Majority-language facet retired; others untouched ============"
check "francophone facet gone"                 "$(code /fr/lausanne/menuisier/francophone/)" 410
check "anglophone facet still live"            "$(code /fr/lausanne/menuisier/anglophone/)"  200
check "parent listing still live"              "$(code /fr/lausanne/menuisier/)"             200
a=$(robots /fr/lausanne/menuisier/anglophone/)
check "anglophone noindexed" "${a:-none}" 'name="robots" content="noindex,follow"'
p=$(robots /fr/lausanne/menuisier/)
check "parent NOT noindexed" "${p:-none}" "none"

echo
echo "=== 3. Business pages live but noindexed ==========================="
check "business page 200"                      "$(code /fr/entreprise/tabac-28-gallo-che460285251)" 200
b=$(robots /fr/entreprise/tabac-28-gallo-che460285251)
check "business noindex,follow" "${b:-none}" 'name="robots" content="noindex,follow"'
# 410 (not 404) on purpose: Search Console then reports the previously submitted
# business sitemap as permanently gone rather than merely unreadable.
check "biz sitemap retired"                    "$(code /sitemap-biz-fr.xml)" 410

echo
echo "=== 4/5. Tag hygiene: aliases 301, place-name tags retired ========="
r=$(redir /fr/lausanne/prestation/painting/)
case "$r" in *peinture*) printf '  \033[32mPASS\033[0m  %-52s %s\n' "painting -> peinture 301" "$r";;
  *) printf '  \033[31mFAIL\033[0m  %-52s got %s\n' "painting -> peinture 301" "${r:-<none>}"; fail=1;; esac
c=$(code "/fr/lausanne/prestation/gen%C3%A8ve/")
case "$c" in 410|404|301) printf '  \033[32mPASS\033[0m  %-52s %s\n' "place-name tag retired" "$c";;
  *) printf '  \033[31mFAIL\033[0m  %-52s got %s, want 410/404/301\n' "place-name tag retired" "$c"; fail=1;; esac
check "tag facet preserved" "$(code /fr/lausanne/decorateur-interieur/interior-architecture/)" 200

echo
echo "=== 6. Sitemaps ===================================================="
idx=$(curl -sL --max-time 20 "$BASE/sitemap.xml")
n_children=$(printf '%s' "$idx" | grep -c '<loc>')
n_nonfr=$(printf '%s' "$idx" | grep -cE 'sitemap-(pages|biz)-(de|it|en)\.xml')
n_biz=$(printf '%s' "$idx" | grep -c 'sitemap-biz')
check "sitemap index children"                 "$n_children" 1
check "no de/it/en sitemaps"                   "$n_nonfr"    0
check "no biz sitemap"                         "$n_biz"      0

pages=$(curl -sL --max-time 60 "$BASE/sitemap-pages-fr.xml")
total=$(printf '%s' "$pages" | grep -c '<loc>')
franco=$(printf '%s' "$pages" | grep -c 'francophone')
# grep -P is unavailable on macOS/BSD grep, so count non-ASCII locs in python instead
nonascii=$(printf '%s' "$pages" | python3 -c "
import sys,re
locs=re.findall(r'<loc>(.*?)</loc>', sys.stdin.read(), re.S)
print(sum(1 for l in locs if any(ord(c)>127 for c in l)))")
spaces=$(printf '%s' "$pages" | python3 -c "
import sys,re
locs=re.findall(r'<loc>(.*?)</loc>', sys.stdin.read(), re.S)
print(sum(1 for l in locs if ' ' in l or '%20' in l))")
alias_hits=$(printf '%s' "$pages" | grep -cE '/(painting|cleaning|accounting|carpentry|catering|moving|plumbing|roofing|hair-salon|hairdresser)/')
canton_tags=$(printf '%s' "$pages" | grep -cE '/canton-[a-z-]+/prestation/')

printf '  %-54s %s\n' "URLs in sitemap-pages-fr.xml (was 15,929)" "$total"
# NOT expected to be 0. Only facets returning the ENTIRE parent listing are
# retired; where francophone is a genuine subset the page is differentiated and
# stays (e.g. /fr/visp/restaurant/francophone/ is 6 of 9 — Visp is German-speaking
# Valais). The duplicate case is asserted directly in section 2 above.
printf '  %-54s %s\n' "francophone facets kept (genuine subsets)" "$franco"
check "no non-ASCII in URLs"                   "$nonascii"   0
check "no spaces in URLs"                      "$spaces"     0
check "no aliased EN tag slugs"                "$alias_hits" 0
if [ "$canton_tags" -gt 0 ]; then
  printf '  \033[32mPASS\033[0m  %-52s %s\n' "canton-level tag pages now included" "$canton_tags"
else
  printf '  \033[31mFAIL\033[0m  %-52s 0 (expected >0)\n' "canton-level tag pages now included"; fail=1
fi

echo
echo "=== 7. Highest-value page must survive ============================="
check "canton isolation page (168 impr)" "$(code /fr/canton-de-neuchatel/prestation/isolation/)" 200

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED — see FAIL lines above"
fi
echo
echo "Next: resubmit https://atlas.magicheidi.ch/sitemap.xml in Search Console,"
echo "then re-measure on 2026-09-15 (impressions per indexed page + category avg position)."
exit $fail
