import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(name):
    with (ROOT / "data/curated" / name).open() as handle:
        return list(csv.DictReader(handle))


class Phase6BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source_path = ROOT / "data/manifests/phase6b_sources.json"
        manifest_path = ROOT / "data/manifests/phase6b_manifest.json"
        cls.sources = json.loads(source_path.read_text())
        cls.manifest = json.loads(manifest_path.read_text())

    def test_frozen_sources_and_outputs(self):
        for source in self.sources.values():
            path = ROOT / source["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source["checksum"])
        for name, output in self.manifest["outputs"].items():
            path = ROOT / name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), output["sha256"])

    def test_admission_boundaries(self):
        admission = self.manifest["admission"]
        admitted = ["bdcap_morbidity", "metabolic_screening", "esde", "estudes"]
        held = ["sivamin", "hearing_screening", "waiting_island", "hospital_enrichment"]
        self.assertTrue(all(admission[key] == "ADMIT_WITH_LIMITATIONS" for key in admitted))
        self.assertTrue(all(admission[key] == "HOLD" for key in held))

    def test_bdcap_is_regional_weighted_and_pediatric(self):
        data = rows("bdcap_pediatric_indicators.csv")
        self.assertEqual(len(data), 14)
        self.assertEqual({row["reference_period"] for row in data}, {str(y) for y in range(2011, 2025)})
        self.assertEqual({row["geography_id"] for row in data}, {"canarias"})
        self.assertEqual({row["age_group_original"] for row in data}, {"00-14 años"})
        self.assertEqual({row["value_status"] for row in data}, {"WEIGHTED_SAMPLE"})
        self.assertTrue(all(row["denominator"] == "" for row in data))

    def test_metabolic_is_process_not_prevalence(self):
        data = rows("neonatal_screening_indicators.csv")
        self.assertEqual(len(data), 12)
        self.assertEqual({row["geography_id"] for row in data}, {"canarias"})
        self.assertEqual({row["reference_period"] for row in data}, {"2024"})
        self.assertNotIn("prevalence", {row["indicator_id"] for row in data})
        participation = next(row for row in data if row["indicator_id"] == "participation")
        self.assertEqual((participation["numerator"], participation["denominator"]), ("11536", "11671"))

    def test_surveys_remain_separate_and_regional(self):
        data = rows("adolescent_survey_indicators_phase6b.csv")
        self.assertEqual(len(data), 27)
        self.assertEqual({row["survey_id"] for row in data}, {"esde_2023", "estudes_2023"})
        self.assertEqual({row["geography_id"] for row in data}, {"canarias"})
        esde = [row for row in data if row["survey_id"] == "esde_2023"]
        estudes = [row for row in data if row["survey_id"] == "estudes_2023"]
        self.assertEqual({row["age_group_original"] for row in esde}, {"1-14 años"})
        self.assertEqual({row["age_group_original"] for row in estudes}, {"14-18 años"})
        self.assertTrue(all(row["value_status"] == "SURVEY_ESTIMATE" for row in data))
        self.assertTrue(all(row["sample_size"] == "2488" for row in estudes))
