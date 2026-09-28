import csv, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/'data/curated'/name).open(encoding='utf-8',newline='') as h: return list(csv.DictReader(h))
class Phase4ContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.income=rows('socioeconomic_indicators.csv'); cls.territory=rows('territorial_context.csv'); cls.stations=rows('air_stations.csv'); cls.air=rows('air_observations.csv'); cls.weather=rows('weather_stations.csv')
    def test_income_covers_all_municipalities_with_units_and_year(self):
        self.assertEqual(88,len({r['municipality_id'] for r in self.income})); self.assertEqual(264,len(self.income))
        self.assertTrue(all(r['period_start']=='2023-01-01' and r['unit'].startswith('EUR/') for r in self.income))
        self.assertNotIn('child_poverty', {r['indicator'] for r in self.income})
    def test_territorial_context_preserves_population_and_seven_islands(self):
        self.assertEqual(88,len(self.territory)); self.assertEqual(255814,sum(int(r['children_0_14']) for r in self.territory)); self.assertEqual(7,len({r['island_id'] for r in self.territory}))
        for row in self.territory:
            total=sum(float(row[k]) for k in ('degurba_urban_centre_children_pct','degurba_urban_cluster_children_pct','degurba_rural_children_pct','degurba_unclassified_children_pct'))
            self.assertAlmostEqual(100,total,places=1); self.assertEqual('ESTIMATED',row['status'])
    def test_air_is_station_level_validated_without_interpolation(self):
        self.assertEqual(51,len(self.stations)); self.assertEqual({'PM10','PM2.5','NO2','O3','SO2'},{r['pollutant'] for r in self.air}); self.assertTrue(all(r['unit']=='µg/m³' and r['geography_level']=='station' and r['status']=='VALIDATED' for r in self.air))
        self.assertEqual(7,len({r['island_id'] for r in self.stations if r['island_id']})); self.assertTrue(all(not r['longitude'] or -18.5<float(r['longitude'])<-13 for r in self.stations))
        manifest=json.loads((ROOT/'data/manifests/phase4_context_manifest.json').read_text()); self.assertFalse(manifest['air_interpolation'])
    def test_weather_inventory_covers_seven_islands_but_observations_are_pending(self):
        self.assertEqual(7,len({r['island_id'] for r in self.weather})); self.assertGreaterEqual(len(self.weather),50)
        self.assertEqual([],rows('weather_observations.csv')); self.assertEqual([],rows('environment_events.csv'))
        manifest=json.loads((ROOT/'data/manifests/phase4_context_manifest.json').read_text()); self.assertEqual('NOT_AVAILABLE_API_KEY_REQUIRED',manifest['weather_observations_status']); self.assertIn('PROVISIONAL',manifest['calima_status'])
if __name__=='__main__': unittest.main()
