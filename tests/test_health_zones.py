import csv
import json
from pathlib import Path
import unittest
from shapely.geometry import shape

ROOT = Path(__file__).parents[1]
ISLANDS = {"el-hierro", "la-gomera", "la-palma", "tenerife",
           "gran-canaria", "fuerteventura", "lanzarote"}


class HealthZoneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.historical = json.loads((ROOT / "data/curated/health_zones.geojson").read_text())
        cls.qa = json.loads((ROOT / "data/curated/health_zones_qa.json").read_text())
        path = ROOT / "data/curated/health_zones_current_catalog.csv"
        with path.open(encoding="utf-8") as handle:
            cls.current = list(csv.DictReader(handle))

    def test_seven_islands_are_present_in_both_versions(self):
        historical = {f["properties"]["island_id"] for f in self.historical["features"]}
        current = {row["island_id"] for row in self.current}
        self.assertEqual(ISLANDS, historical)
        self.assertEqual(ISLANDS, current)

    def test_historical_geometry_is_valid_but_never_routeable(self):
        for feature in self.historical["features"]:
            self.assertTrue(shape(feature["geometry"]).is_valid)
            self.assertFalse(feature["properties"]["routing_eligible"])
            self.assertEqual("NEEDS_VALIDATION", feature["properties"]["verification_status"])

    def test_current_catalog_has_no_fabricated_codes_or_geometry(self):
        for row in self.current:
            self.assertEqual("", row["health_zone_id"])
            self.assertEqual("", row["official_code"])
            self.assertEqual("not_available", row["geometry_status"])
            self.assertEqual("false", row["routing_eligible"])

    def test_qa_records_no_silent_geometry_repair_or_overlap(self):
        self.assertFalse(self.qa["make_valid_applied"])
        self.assertEqual(0, self.qa["duplicate_source_code_count"])
        for result in self.qa["islands"].values():
            self.assertEqual([], result["overlap_pairs_gt_1m2"])

    def test_fuerteventura_versions_remain_distinct(self):
        result = self.qa["islands"]["fuerteventura"]
        self.assertEqual(5, result["historical_2017_count"])
        self.assertEqual(6, result["current_ap_catalog_2026_count"])
        self.assertEqual(6, result["siap_2024_count"])


if __name__ == "__main__":
    unittest.main()
