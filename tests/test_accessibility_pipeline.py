import json
from pathlib import Path
import unittest

from etl.prepare_accessibility import aggregate, load_destinations, terrestrial_component

ROOT = Path(__file__).parents[1]


class AccessibilityPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/manifests/accessibility_pipeline_benchmark.json").read_text())

    def test_all_cells_and_seven_islands_are_preserved(self):
        self.assertEqual(13277, self.manifest["n_origins"])
        self.assertEqual(7, self.manifest["island_aggregate_count"])
        self.assertEqual(13277, sum(self.manifest["routing_status_counts"].values()))

    def test_la_graciosa_is_a_separate_unknown_time_transfer(self):
        self.assertEqual("la-graciosa", terrestrial_component("lanzarote", -13.50, 29.23))
        self.assertEqual(20, self.manifest["la_graciosa_cells"])
        self.assertEqual(20, self.manifest["routing_status_counts"]["requires_interisland_transfer"])

    def test_only_verified_official_destinations_are_selected(self):
        rows = load_destinations(ROOT / "data/curated/pediatric_facilities.csv")
        self.assertEqual(158, len(rows))
        self.assertTrue(all(row["verification_status"] == "VERIFIED" for row in rows))
        self.assertTrue(all(row["geocoding_match_status"] == "official_registry_point" for row in rows))

    def test_manifest_records_reproducible_local_execution(self):
        self.assertEqual(0, self.manifest["failures"])
        self.assertEqual(0, self.manifest["public_server_requests"])
        self.assertEqual("5.27.1", self.manifest["engine_version"])
        self.assertFalse(self.manifest["zbs_aggregation_enabled"])
        self.assertEqual("staging_only", self.manifest["result_publication_status"])

    def test_aggregation_is_weighted_by_children(self):
        rows = [
            {"island_id": "x", "child_population_0_14": "1", "routing_status": "routed",
             "travel_seconds": "60"},
            {"island_id": "x", "child_population_0_14": "9", "routing_status": "routed",
             "travel_seconds": "1200"},
        ]
        result = aggregate(rows, ("island_id",))[0]
        self.assertEqual(1200.0, result["median_seconds"])
        self.assertEqual(10.0, result["pct_lt_5_min"])


if __name__ == "__main__":
    unittest.main()
