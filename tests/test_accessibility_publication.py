import csv
import json
from pathlib import Path
import unittest

from etl.prepare_accessibility import weighted_quantile

ROOT = Path(__file__).parents[1]


def rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class AccessibilityPublicationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cells = rows("data/curated/pediatric_accessibility_2024.csv")
        cls.islands = rows("data/curated/accessibility_by_island_2024.csv")
        cls.municipalities = rows("data/curated/accessibility_by_municipality_2024.csv")
        cls.qa = json.loads((ROOT / "data/manifests/accessibility_qa.json").read_text())
        cls.manifest = json.loads(
            (ROOT / "data/manifests/accessibility_publication_manifest.json").read_text())

    def test_qa_passed_and_preserved_population(self):
        self.assertTrue(self.qa["passed"])
        self.assertEqual([], self.qa["failures"])
        self.assertEqual(13277, len(self.cells))
        self.assertEqual(13277, len({row["grid_id"] for row in self.cells}))
        self.assertEqual(255814, sum(int(row["children_0_14"]) for row in self.cells))
        self.assertEqual(158, self.qa["eligible_destination_count"])

    def test_routing_states_keep_null_distinct_from_zero(self):
        counts = {status: 0 for status in ("routed", "requires_interisland_transfer",
                                           "no_route", "not_evaluated")}
        for row in self.cells:
            counts[row["routing_status"]] += 1
            if row["routing_status"] == "routed":
                self.assertGreater(float(row["travel_seconds"]), 0)
                self.assertGreater(float(row["travel_distance_m"]), 0)
            else:
                self.assertEqual("", row["travel_seconds"])
                self.assertEqual("", row["travel_minutes"])
                self.assertEqual("", row["travel_distance_m"])
        self.assertEqual({"routed": 13256, "requires_interisland_transfer": 20,
                          "no_route": 0, "not_evaluated": 1}, counts)

    def test_la_graciosa_transfer_is_preserved(self):
        transfer = [row for row in self.cells
                    if row["routing_status"] == "requires_interisland_transfer"]
        self.assertEqual(20, len(transfer))
        self.assertEqual(91, sum(int(row["children_0_14"]) for row in transfer))
        self.assertEqual({"lanzarote"}, {row["island_id"] for row in transfer})

    def test_seven_island_denominators_reconcile(self):
        self.assertEqual(7, len(self.islands))
        expected = {"el-hierro", "la-gomera", "la-palma", "tenerife",
                    "gran-canaria", "fuerteventura", "lanzarote"}
        self.assertEqual(expected, {row["island_id"] for row in self.islands})
        for row in self.islands:
            total = int(row["population_total"])
            parts = sum(int(row[field]) for field in (
                "population_routed", "population_requires_interisland_transfer",
                "population_no_route", "population_not_evaluated"))
            self.assertEqual(total, parts)

    def test_weighted_quantile_uses_children_not_cells(self):
        self.assertEqual(20, weighted_quantile([(1, 1), (20, 9)], 0.5))
        self.assertEqual(20, weighted_quantile([(1, 1), (20, 9)], 0.9))
        self.assertIsNone(weighted_quantile([(1, 0)], 0.5))

    def test_municipal_privacy_and_no_zbs_outputs(self):
        self.assertEqual(88, len(self.municipalities))
        self.assertEqual(85, sum(row["publication_status"] == "publishable"
                                 for row in self.municipalities))
        self.assertTrue(all("zbs" not in key.lower() for key in self.municipalities[0]))
        self.assertFalse(self.manifest["zbs_aggregation_enabled"])
        self.assertFalse(self.manifest["privacy"]["cell_exact_children_visible_in_ui"])

    def test_provenance_is_complete(self):
        sources = self.manifest["sources"]
        self.assertEqual("canary-islands-260926", sources["osm"]["extract_version"])
        self.assertEqual("OSRM", sources["routing"]["engine"])
        self.assertEqual("5.27.1", sources["routing"]["version"])
        self.assertEqual("2024", self.manifest["source_period"])


if __name__ == "__main__":
    unittest.main()
