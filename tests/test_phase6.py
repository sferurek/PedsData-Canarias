import csv,hashlib,json,unittest
from pathlib import Path
from etl.build_phase6 import numeric,ISLANDS,activity,survey
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
 with (ROOT/"data/curated"/name).open() as f:return list(csv.DictReader(f))
class Phase6Tests(unittest.TestCase):
 def test_sources_and_exports_frozen(self):
  m=json.loads((ROOT/"data/manifests/phase6_manifest.json").read_text())
  for s in m["sources"].values():self.assertEqual(hashlib.sha256((ROOT/s["path"]).read_bytes()).hexdigest(),s["checksum"])
  for p,s in m["outputs"].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),s["sha256"])
 def test_seven_islands_each_year_and_metric(self):
  r=rows("pediatric_primary_care_activity.csv")
  for k in ["consultations","distinct_persons","frequentation"]:
   selected=[x for x in r if x["activity_type"]==k and x["place"]=="_T"]
   self.assertEqual(len(selected),126)
   self.assertEqual({(x["island_id"],int(x["year"])) for x in selected},{(i,y) for i in ISLANDS.values() for y in range(2007,2025)})
 def test_null_zero_and_source_status(self):
  self.assertEqual(numeric("0"),0)
  self.assertIsNone(numeric(""))
  self.assertIsNone(numeric("5","Valor no disponible"))
  with self.assertRaises(ValueError):numeric("-1")
 def test_not_children_or_resident_denominator(self):
  r=rows("pediatric_primary_care_activity.csv")
  self.assertTrue(all("Servicio" in x["age_group_original"] for x in r))
  self.assertEqual({x["unit"] for x in r if x["activity_type"]=="frequentation"},{"consultations_per_assigned_person_year"})
 def test_waiting_stock_and_geography(self):
  r=rows("pediatric_waiting_list.csv")
  self.assertEqual({x["geography_id"] for x in r},{"canarias"})
  self.assertTrue(all(x["mean_wait_days_if_available"]=="" for x in r))
  self.assertEqual({x["reference_date"][:4] for x in r},{str(y) for y in range(2017,2026)})
  self.assertEqual({x["specialty"] for x in r},{"PEDIATRIA","CIRUGIA_PEDIATRICA"})
  self.assertTrue(all(not x["pending_patients"] or float(x["pending_patients"])==0 or float(x["pending_patients"])>=5 for x in r))
 def test_survey_universe_age_no_synthetic_ci(self):
  r=rows("adolescent_survey_indicator.csv")
  self.assertEqual(len(r),20)
  self.assertEqual({x["geography_id"] for x in r},{"canarias"})
  self.assertEqual({x["value_status"] for x in r},{"SURVEY_ESTIMATE"})
  self.assertTrue(all(x["denominator"]==x["ci_lower"]==x["ci_upper"]=="" for x in r))
  self.assertIn("17–18 años",{x["age_group_original"] for x in r})
  self.assertTrue(all("escolarizados" in x["universe"] and int(x["n_valid_published"])>=100 for x in r))
 def test_unvalidated_domains_not_admitted(self):
  a=json.loads((ROOT/"data/manifests/phase6_manifest.json").read_text())["admission"]
  for k in ["bdcap","vaccination","screening","esde_estudes","waiting_island"]:self.assertEqual(a[k],"HOLD")
 def test_reproducible_curated_values(self):
  sources=json.loads((ROOT/"data/manifests/phase6_sources.json").read_text())
  self.assertEqual([str(x["value"]) if x["value"] is not None else "" for x in activity(sources)],[x["value"] for x in rows("pediatric_primary_care_activity.csv")])
  self.assertEqual([str(x["value"]) for x in survey(sources)],[x["value"] for x in rows("adolescent_survey_indicator.csv")])
