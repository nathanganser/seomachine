"""
DataForSEO API Integration

Fetches SERP data, competitor rankings, keyword research, and more.
"""

import os
import base64
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class DataForSEO:
    """DataForSEO API client"""

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize DataForSEO client

        Args:
            login: API login (defaults to env var)
            password: API password (defaults to env var)
        """
        self.login = login or os.getenv("DATAFORSEO_LOGIN")
        self.password = password or os.getenv("DATAFORSEO_PASSWORD")
        self.base_url = os.getenv("DATAFORSEO_BASE_URL", "https://api.dataforseo.com")

        # Configurable location/language defaults (Switzerland/German by default)
        self.default_location_code = int(
            os.getenv("DATAFORSEO_LOCATION_CODE", "2756")
        )
        self.default_language_code = os.getenv("DATAFORSEO_LANGUAGE_CODE", "de")

        if not self.login or not self.password:
            raise ValueError("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set")

        # Create auth header
        cred = f"{self.login}:{self.password}"
        encoded_cred = base64.b64encode(cred.encode("ascii")).decode("ascii")
        self.headers = {
            "Authorization": f"Basic {encoded_cred}",
            "Content-Type": "application/json",
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _post(self, endpoint: str, data: List[Dict]) -> Dict:
        """Make POST request to DataForSEO API"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _first_task(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        tasks = response.get("tasks")
        if isinstance(tasks, list) and tasks:
            first = tasks[0]
            if isinstance(first, dict):
                return first
        return None

    def _first_result(self, task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = task.get("result")
        if isinstance(result, list) and result:
            first = result[0]
            if isinstance(first, dict):
                return first
        return None

    def get_rankings(
        self,
        domain: str,
        keywords: List[str],
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get ranking positions for specific keywords

        Args:
            domain: Your domain (e.g., "magicheidi.ch")
            keywords: List of keywords to check
            location_code: DataForSEO location code (defaults to env config)
            language_code: Language code (defaults to env config)

        Returns:
            List of ranking data for each keyword
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        tasks = []
        for keyword in keywords:
            tasks.append(
                {
                    "keyword": keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "device": "desktop",
                    "os": "windows",
                }
            )

        response = self._post("/v3/serp/google/organic/live/advanced", tasks)

        results = []
        if response["status_code"] == 20000:
            for task in response.get("tasks", []):
                if task.get("status_code") == 20000:
                    keyword = task.get("data", {}).get("keyword")
                    result = self._first_result(task)
                    if not keyword or result is None:
                        continue
                    items = result.get("items", [])

                    # Find domain position
                    position = None
                    url = None
                    for i, item in enumerate(items, 1):
                        if domain in item.get("domain", ""):
                            position = i
                            url = item.get("url")
                            break

                    results.append(
                        {
                            "keyword": keyword,
                            "domain": domain,
                            "position": position,
                            "url": url,
                            "ranking": position is not None,
                            "search_volume": result.get("keyword_data", {})
                            .get("keyword_info", {})
                            .get("search_volume"),
                            "cpc": result.get("keyword_data", {})
                            .get("keyword_info", {})
                            .get("cpc"),
                        }
                    )

        return results

    def get_serp_data(
        self,
        keyword: str,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Get complete SERP data for a keyword

        Args:
            keyword: Search keyword
            location_code: DataForSEO location code (defaults to env config)
            language_code: Language code (defaults to env config)
            limit: Number of results to return

        Returns:
            Dict with SERP data including all ranking pages
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [
            {
                "keyword": keyword,
                "location_code": location_code,
                "language_code": language_code,
                "device": "desktop",
                "os": "windows",
                "depth": limit,
            }
        ]

        response = self._post("/v3/serp/google/organic/live/advanced", data)

        if response["status_code"] != 20000:
            return {"error": "API request failed"}

        task = self._first_task(response)
        if not task or task.get("status_code") != 20000:
            return {"error": "Task failed"}

        result = self._first_result(task)
        if result is None:
            return {"error": "Task returned no results"}

        # Extract organic results
        organic_results = []
        for item in result.get("items", []):
            if item["type"] == "organic":
                organic_results.append(
                    {
                        "position": item.get("rank_absolute"),
                        "url": item.get("url"),
                        "domain": item.get("domain"),
                        "title": item.get("title"),
                        "description": item.get("description"),
                        "breadcrumb": item.get("breadcrumb"),
                    }
                )

        # Extract SERP features
        features = []
        for item in result.get("items", []):
            if item["type"] != "organic":
                features.append(item["type"])

        keyword_data = result.get("keyword_data", {}).get("keyword_info", {})

        return {
            "keyword": keyword,
            "search_volume": keyword_data.get("search_volume"),
            "cpc": keyword_data.get("cpc"),
            "competition": keyword_data.get("competition"),
            "organic_results": organic_results,
            "features": list(set(features)),
            "total_results": result.get("items_count", 0),
        }

    def analyze_competitor(
        self,
        competitor_domain: str,
        keywords: List[str],
        your_domain: Optional[str] = None,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze competitor rankings vs yours

        Args:
            competitor_domain: Competitor's domain
            keywords: Keywords to compare
            your_domain: Your domain (optional)
            location_code: DataForSEO location code (defaults to env config)
            language_code: Language code (defaults to env config)

        Returns:
            Comparative ranking analysis
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        tasks = []
        for keyword in keywords:
            tasks.append(
                {
                    "keyword": keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "device": "desktop",
                }
            )

        response = self._post("/v3/serp/google/organic/live/advanced", tasks)

        comparison = []
        for i, task in enumerate(response.get("tasks", [])):
            if task.get("status_code") == 20000:
                keyword = keywords[i]
                result = self._first_result(task)
                if result is None:
                    continue
                items = result.get("items", [])

                competitor_pos = None
                your_pos = None

                for j, item in enumerate(items, 1):
                    domain = item.get("domain", "")
                    if competitor_domain in domain:
                        competitor_pos = j
                    if your_domain and your_domain in domain:
                        your_pos = j

                gap = None
                if competitor_pos and your_pos:
                    gap = your_pos - competitor_pos
                elif competitor_pos and not your_pos:
                    gap = "Not ranking"

                comparison.append(
                    {
                        "keyword": keyword,
                        "competitor_position": competitor_pos,
                        "your_position": your_pos,
                        "gap": gap,
                        "opportunity": "high"
                        if competitor_pos and not your_pos
                        else "medium"
                        if isinstance(gap, (int, float)) and gap > 10
                        else "low",
                    }
                )

        return {
            "competitor": competitor_domain,
            "your_domain": your_domain,
            "comparison": comparison,
        }

    def get_keyword_ideas(
        self,
        seed_keyword: str,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get related keyword ideas

        Args:
            seed_keyword: Starting keyword
            location_code: Location code (defaults to env config)
            language_code: Language code (defaults to env config)
            limit: Number of ideas to return

        Returns:
            List of related keywords with search volume, difficulty
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [
            {
                "keyword": seed_keyword,
                "location_code": location_code,
                "language_code": language_code,
                "include_serp_info": True,
                "limit": limit,
            }
        ]

        response = self._post("/v3/dataforseo_labs/google/related_keywords/live", data)

        if response["status_code"] != 20000:
            return []

        task = self._first_task(response)
        if not task or task.get("status_code") != 20000:
            return []

        result = self._first_result(task)
        if result is None:
            return []

        keywords = []
        for item in result.get("items", []):
            keywords.append(
                {
                    "keyword": item.get("keyword_data", {}).get("keyword"),
                    "search_volume": item.get("keyword_data", {})
                    .get("keyword_info", {})
                    .get("search_volume"),
                    "cpc": item.get("keyword_data", {})
                    .get("keyword_info", {})
                    .get("cpc"),
                    "competition": item.get("keyword_data", {})
                    .get("keyword_info", {})
                    .get("competition"),
                    "avg_position": item.get("serp_info", {}).get("se_results_count"),
                }
            )

        # Sort by search volume
        keywords.sort(key=lambda x: x["search_volume"] or 0, reverse=True)

        return keywords

    def get_questions(
        self,
        keyword: str,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get question-based queries related to keyword

        Args:
            keyword: Seed keyword
            location_code: Location code (defaults to env config)
            language_code: Language code (defaults to env config)
            limit: Number of questions to return

        Returns:
            List of question queries
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [
            {
                "keyword": keyword,
                "location_code": location_code,
                "language_code": language_code,
                "limit": limit,
            }
        ]

        response = self._post("/v3/dataforseo_labs/google/related_keywords/live", data)

        if response["status_code"] != 20000:
            return []

        task = self._first_task(response)
        if not task or task.get("status_code") != 20000:
            return []

        result = self._first_result(task)
        if result is None:
            return []

        questions = []
        for item in result.get("items", []):
            kw = item.get("keyword_data", {}).get("keyword", "")

            # Filter for questions (English, German, French)
            if any(
                kw.lower().startswith(q)
                for q in [
                    # English
                    "how",
                    "what",
                    "why",
                    "when",
                    "where",
                    "who",
                    "can",
                    "should",
                    "is",
                    "are",
                    "does",
                    # German
                    "wie",
                    "was",
                    "warum",
                    "wann",
                    "wo",
                    "wer",
                    "kann",
                    "soll",
                    "ist",
                    "welch",
                    # French
                    "comment",
                    "quoi",
                    "pourquoi",
                    "quand",
                    "où",
                    "qui",
                    "est-ce",
                    "quel",
                ]
            ):
                questions.append(
                    {
                        "question": kw,
                        "search_volume": item.get("keyword_data", {})
                        .get("keyword_info", {})
                        .get("search_volume"),
                        "cpc": item.get("keyword_data", {})
                        .get("keyword_info", {})
                        .get("cpc"),
                    }
                )

        # Sort by search volume
        questions.sort(key=lambda x: x["search_volume"] or 0, reverse=True)

        return questions

    def get_domain_metrics(
        self,
        domain: str,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get domain overview metrics

        Args:
            domain: Domain to analyze
            location_code: Location code (defaults to env config)
            language_code: Language code (defaults to env config)

        Returns:
            Dict with domain metrics
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [{"target": domain, "location_code": location_code, "language_code": language_code}]

        response = self._post("/v3/dataforseo_labs/google/domain_metrics/live", data)

        if response["status_code"] != 20000:
            return {}

        task = self._first_task(response)
        if not task or task.get("status_code") != 20000:
            return {}

        result = self._first_result(task)
        if result is None:
            return {}

        items = result.get("items", [])
        first_item = items[0] if items else {}
        metrics = first_item.get("metrics", {}) if isinstance(first_item, dict) else {}

        return {
            "domain": domain,
            "organic_keywords": metrics.get("organic", {}).get("count"),
            "organic_traffic": metrics.get("organic", {}).get("etv"),
            "domain_rank": metrics.get("organic", {}).get("rank"),
            "backlinks": metrics.get("backlinks", {}),
        }

    def get_domain_keywords(
        self,
        domain: str,
        position_max: int = 20,
        limit: int = 300,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get keywords a domain ranks for using DataForSEO Labs.

        Args:
            domain: Domain to analyze
            position_max: Maximum ranking position to include
            limit: Max number of keywords to return
            location_code: Location code (defaults to env config)
            language_code: Language code (defaults to env config)

        Returns:
            List of keyword dicts with keyword, position, search_volume, cpc, difficulty
        """
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [
            {
                "target": domain,
                "location_code": location_code,
                "language_code": language_code,
                "limit": limit,
                "filters": [
                    ["ranked_serp_element.serp_item.rank_group", "<=", position_max]
                ],
                "order_by": ["ranked_serp_element.serp_item.rank_group,asc"],
            }
        ]

        response = self._post(
            "/v3/dataforseo_labs/google/ranked_keywords/live", data
        )

        if response.get("status_code") != 20000:
            return []

        task = self._first_task(response)
        if not task or task.get("status_code") != 20000:
            return []

        result = self._first_result(task)
        if result is None:
            return []

        keywords = []
        for item in result.get("items") or []:
            kw_data = item.get("keyword_data") or {}
            ranked = item.get("ranked_serp_element") or {}
            serp_item = ranked.get("serp_item") or {}
            keyword_info = kw_data.get("keyword_info") or {}
            keyword_props = kw_data.get("keyword_properties") or {}

            keywords.append(
                {
                    "keyword": kw_data.get("keyword", ""),
                    "position": serp_item.get("rank_group", 99),
                    "search_volume": keyword_info.get("search_volume", 0),
                    "cpc": keyword_info.get("cpc", 0),
                    "difficulty": keyword_props.get("keyword_difficulty", 50),
                }
            )

        return keywords

    def check_ranking_history(
        self,
        domain: str,
        keyword: str,
        months_back: int = 3,
        location_code: Optional[int] = None,
        language_code: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get ranking history for a keyword (requires historical data)

        Args:
            domain: Your domain
            keyword: Keyword to track
            months_back: Months of history
            location_code: Location code (defaults to env config)
            language_code: Language code (defaults to env config)

        Returns:
            List of historical rankings
        """
        # Note: This requires DataForSEO's ranking tracking to be set up
        # This is a simplified version - actual implementation may vary
        location_code = location_code or self.default_location_code
        language_code = language_code or self.default_language_code

        data = [
            {
                "target": domain,
                "keyword": keyword,
                "location_code": location_code,
                "language_code": language_code,
            }
        ]

        try:
            response = self._post("/v3/serp/google/organic/ranking_history/live", data)

            if response["status_code"] == 20000:
                task = self._first_task(response)
                if task and task.get("status_code") == 20000:
                    result = self._first_result(task)
                    if result is not None:
                        return result.get("items", [])
        except:
            pass

        return []


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("data_sources/config/.env")

    dfs = DataForSEO()
    print(f"Using location: {dfs.default_location_code}, language: {dfs.default_language_code}")

    print("\nChecking rankings for Magic Heidi...")
    rankings = dfs.get_rankings(
        domain="magicheidi.ch",
        keywords=["buchhaltungssoftware", "rechnungsprogramm schweiz", "buchhaltung online"],
    )

    for rank in rankings:
        print(f"\nKeyword: {rank['keyword']}")
        print(f"Position: {rank['position'] or 'Not ranking'}")
        print(
            f"Search Volume: {rank['search_volume']:,}"
            if rank["search_volume"]
            else "Search Volume: N/A"
        )

    print("\n\nGetting SERP data for 'buchhaltungssoftware schweiz'...")
    serp = dfs.get_serp_data("buchhaltungssoftware schweiz")

    if "error" not in serp:
        print(f"Search Volume: {serp.get('search_volume') or 'N/A'}")
        print(f"SERP Features: {', '.join(serp.get('features', []))}")
        print(f"\nTop 10 Results:")
        for result in serp["organic_results"][:10]:
            print(f"{result['position']}. {result['domain']}")
            print(f"   {result['url']}")

    print("\n\nRelated questions for 'buchhaltungssoftware':")
    questions = dfs.get_questions("buchhaltungssoftware")
    for q in questions[:10]:
        print(f"- {q['question']}")
        print(
            f"  Volume: {q['search_volume']:,}"
            if q["search_volume"]
            else "  Volume: N/A"
        )
