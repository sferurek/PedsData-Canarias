import csv
from pathlib import Path
import unittest

CATALOG = Path(__file__).parents[1] / "data/curated/pediatric_facilities.csv"
ISLANDS = {"el-hierro", "la-gomera", "la-palma", "tenerife",
           "gran-canaria", "fuerteventura", "lanzarote"}


class FacilityCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CATALOG.open(encoding="utf-8", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_exactly_seven_islands_are_always_present(self):
        self.assertEqual(ISLANDS, {row["island_id"] for row in self.rows})

    def test_official_ids_are_unique(self):
        ids = [row["official_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_coordinates_stay_inside_canaries(self):
        for row in self.rows:
            if not row["latitude"]:
                continue
            self.assertLessEqual(-18.3, float(row["longitude"]), row["name"])
            self.assertLessEqual(float(row["longitude"]), -13.3, row["name"])
            self.assertLessEqual(27.5, float(row["latitude"]), row["name"])
            self.assertLessEqual(float(row["latitude"]), 29.5, row["name"])

    def test_unverified_resources_never_feed_ap_routing(self):
        for row in self.rows:
            eligible = row["routing_eligible_pediatric_ap"] == "true"
            if eligible:
                self.assertEqual("VERIFIED", row["verification_status"])
                self.assertEqual("observed", row["pediatrics_ap"])
                self.assertTrue(row["latitude"] and row["longitude"])
            elif row["verification_status"] != "VERIFIED":
                self.assertFalse(eligible)

    def test_nicu_requires_registered_u23(self):
        for row in self.rows:
            services = row["registered_service_codes"].split("|")
            self.assertEqual(row["nicu"] == "observed", "U23" in services)

    def test_unknown_service_is_not_encoded_as_zero(self):
        allowed = {"observed", "not_available", "needs_validation", "suppressed", "no_route"}
        fields = ("pediatrics_ap", "pediatric_emergency", "pediatric_inpatient",
                  "neonatology", "nicu", "picu")
        for row in self.rows:
            for field in fields:
                self.assertIn(row[field], allowed)
                self.assertNotEqual("0", row[field])

    def test_phase2_facility_evidence_and_hospital_defaults(self):
        by_id = {row["official_id"]: row for row in self.rows}
        self.assertEqual(by_id["0538005432"]["verification_status"], "VERIFIED")
        self.assertEqual(by_id["0538005432"]["routing_eligible_pediatric_ap"], "true")
        self.assertEqual(by_id["0538005357"]["routing_eligible_pediatric_ap"], "false")
        self.assertEqual(by_id["0538002288"]["pediatric_inpatient"], "needs_validation")
        self.assertEqual(by_id["0535003934"]["pediatric_inpatient"], "needs_validation")
        for official_id in ("0535001838", "0538001821", "0538001932"):
            self.assertEqual(by_id[official_id]["picu"], "observed")


if __name__ == "__main__":
    unittest.main()
