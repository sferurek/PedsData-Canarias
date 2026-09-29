import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"data/visual/island_hero_images.json"
EXPECTED={"el-hierro","la-gomera","la-palma","tenerife","gran-canaria","fuerteventura","lanzarote","la-graciosa"}
ALLOWED=("CC BY ","CC BY-SA ","CC0","Public domain")

class VisualAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads(CATALOG.read_text())

    def test_eight_territories_have_verified_licensed_images(self):
        self.assertEqual(len(self.rows),8)
        self.assertEqual({row["territory_id"] for row in self.rows},EXPECTED)
        self.assertTrue(all(row["license_validation"]=="VERIFIED" for row in self.rows))
        self.assertTrue(all(row["license"].startswith(ALLOWED) for row in self.rows))

    def test_web_catalog_is_an_exact_publication_mirror(self):
        mirror=ROOT/"apps/web/src/data/island_hero_images.json"
        self.assertEqual(CATALOG.read_bytes(),mirror.read_bytes())

    def test_sources_licenses_alt_text_and_checksums_are_complete(self):
        for row in self.rows:
            self.assertTrue(row["source_url"].startswith("https://commons.wikimedia.org/wiki/File:"))
            self.assertTrue(row["license_url"].startswith("https://creativecommons.org/"))
            self.assertTrue(row["author"].strip() and row["alt"].strip())
            path=ROOT/"apps/web/public"/row["local_path"].lstrip("/")
            self.assertTrue(path.is_file())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),row["local_sha256"])
            self.assertLess(path.stat().st_size,750_000)

if __name__=="__main__":
    unittest.main()
