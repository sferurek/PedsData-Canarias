import json
import unittest
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEVEN={"el-hierro","la-gomera","la-palma","tenerife","gran-canaria","fuerteventura","lanzarote"}

class Phase8SemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/"data/semantic/metrics_catalog.json").read_text())["metrics"]
        cls.by_metric={m["metric_id"]:m for m in cls.catalog}
        cls.points=json.loads((ROOT/"data/curated/metric_time_series.json").read_text())["points"]
        cls.compat=json.loads((ROOT/"data/semantic/metric_compatibility.json").read_text())
        cls.islands=json.loads((ROOT/"apps/web/public/data/islands.geojson").read_text())

    def test_catalog_has_unique_registered_metrics(self):
        ids=[m["metric_id"] for m in self.catalog]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertGreaterEqual(len(ids),18)
        for item in self.catalog:
            for key in ("geography_levels","time_start","time_end","unit","chart_types","map_allowed","source_id","method_id"):
                self.assertIn(key,item)

    def test_siap_time_series_preserve_all_seven_islands(self):
        for metric in ("child_population_assigned_0_14","pediatricians_ap","assigned_children_per_pediatrician","pediatric_consultations","pediatric_frequentation"):
            rows=[p for p in self.points if p["metric_id"]==metric]
            self.assertEqual({p["geography_id"] for p in rows},SEVEN)
        pediatricians=[p for p in self.points if p["metric_id"]=="pediatricians_ap"]
        for island in SEVEN:
            years={p["period"] for p in pediatricians if p["geography_id"]==island}
            self.assertEqual(years,{str(y) for y in range(2004,2025)})

    def test_true_map_geography_is_declared(self):
        self.assertEqual(self.by_metric["income_mean_per_person"]["map_geography"],"municipality")
        self.assertEqual(self.by_metric["pediatricians_ap"]["map_geography"],"island")
        self.assertEqual(self.by_metric["PM10"]["map_geography"],"station")
        self.assertEqual(self.by_metric["accessibility_ap"]["map_geography"],"grid_250m")
        self.assertFalse(self.by_metric["pediatric_hospital_discharges_selected"]["map_allowed"])
        self.assertFalse(self.by_metric["pediatric_outpatient_waiting_stock"]["map_allowed"])

    def test_island_layer_is_dissolved_and_complete(self):
        features=self.islands["features"]
        self.assertEqual(len(features),7)
        self.assertEqual({f["properties"]["island_id"] for f in features},SEVEN)
        self.assertTrue(all(f["geometry"]["type"] in {"Polygon","MultiPolygon"} for f in features))

    def test_compatibility_rejects_false_cross_scale_pairs(self):
        invalid={tuple(sorted(x["metrics"])) for x in self.compat["invalid_pairs"]}
        self.assertIn(tuple(sorted(("PM10","pediatric_hospital_discharges_selected"))),invalid)
        self.assertIn(tuple(sorted(("income_mean_per_person","pediatric_hospital_discharges_selected"))),invalid)

    def test_waiting_stock_stays_regional(self):
        rows=[p for p in self.points if p["metric_id"]=="pediatric_outpatient_waiting_stock"]
        self.assertTrue(rows)
        self.assertEqual({p["geography_level"] for p in rows},{"autonomous_community"})
        self.assertEqual({p["geography_id"] for p in rows},{"canarias"})

    def test_derived_consultations_per_pediatrician_are_positive(self):
        rows=[p for p in self.points if p["metric_id"]=="consultations_per_pediatrician"]
        self.assertTrue(rows)
        self.assertTrue(all(p["value"]>0 and p["status"]=="DERIVED_RATE" for p in rows))

if __name__=="__main__":unittest.main()
