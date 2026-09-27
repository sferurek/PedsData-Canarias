import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PostGISSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "sql").glob("[0-9][0-9][0-9]_*.sql"))
        )

    def test_required_tables_are_declared(self):
        tables = ("island", "municipality", "health_area", "health_zone",
                  "child_population_grid", "pediatric_facility", "pediatric_resource",
                  "source", "dataset_version", "coverage_status", "routing_snapshot",
                  "accessibility_result")
        for table in tables:
            self.assertIn(f"CREATE TABLE {table}", self.sql)

    def test_seven_islands_are_seeded(self):
        seed = (ROOT / "sql/004_seed_islands.sql").read_text(encoding="utf-8")
        self.assertEqual(seed.count("('"), 7)

    def test_non_routes_cannot_have_numeric_times(self):
        self.assertIn("route_status <> 'routed' AND travel_seconds IS NULL", self.sql)
        self.assertIn("travel_seconds IS NULL OR travel_seconds > 0", self.sql)

    def test_unverified_facilities_cannot_be_routed(self):
        self.assertIn("verification_status = 'VERIFIED' AND location IS NOT NULL", self.sql)

    def test_provenance_fields_are_present(self):
        for field in ("source_id", "source_url", "retrieved_at",
                      "reference_period_start", "reference_period_end",
                      "parser_version", "checksum_sha256"):
            self.assertIn(field, self.sql)


if __name__ == "__main__":
    unittest.main()
