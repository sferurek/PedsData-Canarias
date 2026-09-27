import csv
import pathlib
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]


class RoutingBenchmarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "data/curated/routing_test_cases.csv").open(encoding="utf-8") as handle:
            cls.cases = list(csv.DictReader(handle))
        with (ROOT / "data/curated/routing_benchmark_results.csv").open(encoding="utf-8") as handle:
            cls.results = list(csv.DictReader(handle))

    def test_five_cases_cover_each_of_exactly_seven_islands(self):
        counts = Counter(row["island_id"] for row in self.cases)
        self.assertEqual(len(counts), 7)
        self.assertEqual(set(counts.values()), {5})

    def test_each_engine_routes_four_cases_per_island(self):
        islands = {row["island_id"] for row in self.cases}
        for engine in ("osrm", "valhalla"):
            rows = [row for row in self.results
                    if row["engine"] == engine and row["route_status"] == "routed"]
            self.assertEqual(Counter(row["island_id"] for row in rows),
                             Counter({island: 4 for island in islands}))

    def test_non_routes_have_no_numeric_values(self):
        for row in self.results:
            if row["route_status"] != "routed":
                self.assertEqual(row["duration_seconds"], "")
                self.assertEqual(row["distance_metres"], "")

    def test_guarded_cases_never_reach_an_engine(self):
        guarded = [row for row in self.results
                   if row["case_type"] == "no_route" and row["engine"] in ("osrm", "valhalla")]
        self.assertEqual(len(guarded), 14)
        self.assertTrue(all(row["request_sent"] == "false" for row in guarded))

    def test_la_graciosa_is_an_unknown_time_transfer(self):
        cases = [row for row in self.cases if row["case_id"] == "lanzarote-no_route"]
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0]["origin_component"], "la-graciosa")
        self.assertEqual(cases[0]["expected_status"], "requires_interisland_transfer")

    def test_routed_cases_stay_on_one_road_component(self):
        for row in self.cases:
            if row["expected_status"] == "routed":
                self.assertEqual(row["origin_component"], row["destination_component"])

    def test_openrouteservice_is_not_faked_without_a_key(self):
        rows = [row for row in self.results if row["engine"] == "openrouteservice"]
        self.assertEqual(len(rows), 35)
        self.assertTrue(all(row["route_status"] == "not_evaluated" for row in rows))
        self.assertTrue(all(row["error"] == "api_key_required" for row in rows))


if __name__ == "__main__":
    unittest.main()
