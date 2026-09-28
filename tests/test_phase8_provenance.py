import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]

class Phase8ProvenanceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.metrics=json.loads((ROOT/"data/semantic/metrics_catalog.json").read_text())["metrics"]
  cls.sources=json.loads((ROOT/"data/semantic/sources_catalog.json").read_text())["sources"]
  cls.source_ids={source["source_id"] for source in cls.sources}

 def test_every_metric_has_registered_source(self):
  for metric in self.metrics:
   self.assertTrue(metric["source_ids"],metric["metric_id"])
   self.assertTrue(set(metric["source_ids"])<=self.source_ids,metric["metric_id"])

 def test_every_derived_metric_has_formula_and_lineage(self):
  for metric in self.metrics:
   if metric["status"] in {"DERIVED_RATE","ESTIMATED"}:
    self.assertIsNotNone(metric["formula"],metric["metric_id"])
    self.assertTrue(metric["formula"]["expression"])
    self.assertTrue(metric["formula"]["inputs"])
    self.assertTrue(metric["transformations"])
    self.assertTrue(metric["rounding"])

 def test_every_map_has_geography_period_method_and_sources(self):
  for metric in self.metrics:
   if metric["map_allowed"]:
    self.assertTrue(metric["map_geography"],metric["metric_id"])
    self.assertIsNotNone(metric["time_end"])
    self.assertTrue(metric["classification_method"])
    self.assertTrue(metric["source_ids"])

 def test_official_links_are_absolute_https(self):
  for source in self.sources:
   parsed=urlparse(source["official_url"])
   self.assertEqual(parsed.scheme,"https",source["source_id"])
   self.assertTrue(parsed.netloc,source["source_id"])

 def test_accessibility_lineage_has_origin_destination_graph_and_engine(self):
  metric=next(m for m in self.metrics if m["metric_id"]=="accessibility_ap")
  self.assertEqual(set(metric["source_ids"]),{"ISTAC:GRID_2024","SCS:REGCESS_U20","OSM:CANARY_2026_09_26","OSRM:5.27.1"})
  self.assertIn("requires_interisland_transfer"," ".join(metric["transformations"]))

 def test_routes_exist(self):
  for path in ["apps/web/src/app/fuentes/page.tsx","apps/web/src/app/fuentes/[source_id]/page.tsx","apps/web/src/app/indicadores/[metric_id]/page.tsx","apps/web/src/app/trazabilidad/[metric_id]/page.tsx"]:
   self.assertTrue((ROOT/path).exists(),path)

if __name__=="__main__":unittest.main()

