import csv
import json
import pathlib
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]


class LocalRoutingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.osm = json.loads((ROOT / "data/manifests/osm_canarias_snapshot.json").read_text())
        cls.graph = json.loads((ROOT / "data/manifests/osrm_canarias_graph.json").read_text())
        with (ROOT / "data/curated/routing_test_cases.csv").open() as handle:
            cls.cases = {row["case_id"]: row for row in csv.DictReader(handle)}
        with (ROOT / "data/curated/local_osrm_benchmark_results.csv").open() as handle:
            cls.results = list(csv.DictReader(handle))
        with (ROOT / "data/curated/routing_reference_journeys.csv").open() as handle:
            cls.references = list(csv.DictReader(handle))

    def test_frozen_snapshot_has_expected_checksum_and_islands(self):
        self.assertEqual(
            self.osm["checksum_sha256"],
            "2c5f0f3c7b42fc68f6d1bf64679642edb86f546fe510e6f081a07a4d398379f9",
        )
        self.assertEqual(len(self.osm["islands"]), 7)
        self.assertEqual(self.osm["separate_road_components"], ["la-graciosa"])

    def test_graph_records_engine_and_snapshot(self):
        self.assertEqual(self.graph["engine"], "OSRM")
        self.assertEqual(self.graph["engine_version"], "5.27.1")
        self.assertEqual(self.graph["algorithm"], "MLD")
        self.assertEqual(self.graph["osm_checksum_sha256"], self.osm["checksum_sha256"])
        self.assertTrue(self.graph["container_image_digest"].startswith("sha256:"))

    def test_phase1_sample_is_preserved(self):
        self.assertEqual(len(self.cases), 35)
        self.assertEqual(len(self.results), 35)
        routed = [row for row in self.results if row["route_status"] == "routed"]
        self.assertEqual(len(routed), 28)
        self.assertEqual(Counter(row["island_id"] for row in routed), {
            "el-hierro": 4,
            "la-gomera": 4,
            "la-palma": 4,
            "tenerife": 4,
            "gran-canaria": 4,
            "fuerteventura": 4,
            "lanzarote": 4,
        })

    def test_guards_prevent_ferries_and_preserve_null_times(self):
        blocked = [row for row in self.results if row["route_status"] != "routed"]
        self.assertEqual(len(blocked), 7)
        for row in blocked:
            self.assertEqual(row["request_sent"], "false")
            self.assertEqual(row["duration_seconds"], "")
            self.assertEqual(row["distance_metres"], "")
        graciosa = next(row for row in blocked if row["case_id"] == "lanzarote-no_route")
        self.assertEqual(graciosa["route_status"], "requires_interisland_transfer")

    def test_role_specific_snapping_thresholds(self):
        for row in self.results:
            if row["route_status"] != "routed":
                continue
            reverse = row["case_type"] == "reverse"
            cell_snap = float(row["destination_snap_metres"] if reverse else row["origin_snap_metres"])
            facility_snap = float(row["origin_snap_metres"] if reverse else row["destination_snap_metres"])
            self.assertLessEqual(cell_snap, 150.0, row["case_id"])
            self.assertLessEqual(facility_snap, 200.0, row["case_id"])

    def test_reference_journeys_meet_qa_threshold(self):
        self.assertEqual(len(self.references), 21)
        self.assertEqual(Counter(row["island_id"] for row in self.references), {
            "el-hierro": 3,
            "la-gomera": 3,
            "la-palma": 3,
            "tenerife": 3,
            "gran-canaria": 3,
            "fuerteventura": 3,
            "lanzarote": 3,
        })
        self.assertNotIn("RED", {row["snap_status"] for row in self.references})
        self.assertNotIn("RED", {row["time_status"] for row in self.references})
        self.assertLessEqual(max(float(row["time_difference_pct"]) for row in self.references), 35.0)


if __name__ == "__main__":
    unittest.main()
