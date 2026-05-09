import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "data_sources" / "modules" / "dataforseo.py"
)


def load_dataforseo_module():
    spec = importlib.util.spec_from_file_location("dataforseo_under_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataForSEOResilienceTests(unittest.TestCase):
    def setUp(self) -> None:
        module = load_dataforseo_module()
        self.client = object.__new__(module.DataForSEO)
        # Methods read these attributes that __init__ would normally set.
        self.client.default_location_code = 2756
        self.client.default_language_code = "de"

    def test_get_serp_data_returns_task_error_when_result_is_missing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [{"status_code": 20000, "result": []}],
        }

        result = self.client.get_serp_data("test keyword")

        self.assertEqual(result, {"error": "Task returned no results"})

    def test_get_keyword_ideas_returns_empty_list_when_result_is_missing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [{"status_code": 20000, "result": []}],
        }

        result = self.client.get_keyword_ideas("seed keyword")

        self.assertEqual(result, [])

    def test_analyze_competitor_handles_missing_result_without_crashing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [
                {
                    "status_code": 20000,
                    "data": {"keyword": "keyword one"},
                    "result": [],
                }
            ],
        }

        result = self.client.analyze_competitor(
            "competitor.com", ["keyword one"], your_domain="example.com"
        )

        self.assertEqual(result["comparison"], [])

    def test_get_domain_keywords_returns_empty_list_when_status_not_ok(self):
        self.client._post = lambda endpoint, data: {"status_code": 40000, "tasks": []}

        result = self.client.get_domain_keywords("example.com")

        self.assertEqual(result, [])

    def test_get_domain_keywords_returns_empty_list_when_tasks_missing(self):
        self.client._post = lambda endpoint, data: {"status_code": 20000, "tasks": []}

        result = self.client.get_domain_keywords("example.com")

        self.assertEqual(result, [])

    def test_get_domain_keywords_returns_empty_list_when_result_missing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [{"status_code": 20000, "result": []}],
        }

        result = self.client.get_domain_keywords("example.com")

        self.assertEqual(result, [])

    def test_get_domain_keywords_parses_normal_response(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [
                {
                    "status_code": 20000,
                    "result": [
                        {
                            "items": [
                                {
                                    "keyword_data": {
                                        "keyword": "buchhaltung schweiz",
                                        "keyword_info": {
                                            "search_volume": 1000,
                                            "cpc": 2.5,
                                        },
                                        "keyword_properties": {
                                            "keyword_difficulty": 35,
                                        },
                                    },
                                    "ranked_serp_element": {
                                        "serp_item": {"rank_group": 4}
                                    },
                                }
                            ]
                        }
                    ],
                }
            ],
        }

        result = self.client.get_domain_keywords("example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["keyword"], "buchhaltung schweiz")
        self.assertEqual(result[0]["position"], 4)
        self.assertEqual(result[0]["search_volume"], 1000)
        self.assertEqual(result[0]["cpc"], 2.5)
        self.assertEqual(result[0]["difficulty"], 35)

    def test_get_domain_keywords_handles_missing_nested_fields(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [
                {
                    "status_code": 20000,
                    "result": [{"items": [{}]}],
                }
            ],
        }

        result = self.client.get_domain_keywords("example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["keyword"], "")
        self.assertEqual(result[0]["position"], 99)
        self.assertEqual(result[0]["search_volume"], 0)


if __name__ == "__main__":
    unittest.main()
