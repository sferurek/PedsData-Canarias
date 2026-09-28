import csv, hashlib, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def rows(name):
 with (ROOT/'data/curated'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

class Phase5ClinicalTests(unittest.TestCase):
 def test_hospitalization_preserves_real_geography_age_and_dictionary(self):
  data=rows('pediatric_hospital_indicators.csv')
  self.assertEqual({r['geography_id'] for r in data},{'canarias'})
  self.assertEqual({r['geography_level'] for r in data},{'autonomous_community'})
  self.assertEqual({r['age_group_code'] for r in data},{'Y_LT1','Y1T4','Y5T14'})
  ref={r['group_id'] for r in rows('../reference/pediatric_diagnosis_groups.csv')}
  self.assertTrue({r['diagnosis_group_id'] for r in data} <= ref)
  self.assertNotIn('15–17',{r['age_group_original'] for r in data})
 def test_perinatal_has_seven_islands_and_sound_rates(self):
  data=rows('perinatal_indicators.csv')
  latest=[r for r in data if r['reference_period']=='2024' and r['geography_level']=='island']
  self.assertEqual(len({r['geography_id'] for r in latest}),7)
  for r in latest:
   if r['indicator_id']=='preterm_rate':
    self.assertAlmostEqual(float(r['value']),100*float(r['numerator'])/float(r['denominator']),places=2)
 def test_mortality_small_numbers_are_not_disclosed(self):
  data=rows('pediatric_mortality.csv')
  self.assertEqual({r['reference_period'] for r in data},{'2020-2024'})
  self.assertEqual(len({r['geography_id'] for r in data}),7)
  for r in data:
   if r['suppressed']=='true': self.assertEqual((r['value'],r['numerator']),('',''))
   elif r['value']: self.assertTrue(float(r['value'])==0 or float(r['value'])>=5)
 def test_survey_is_never_administrative_prevalence(self):
  data=rows('child_health_survey_indicators.csv')
  self.assertEqual({r['value_status'] for r in data},{'SURVEY_ESTIMATE'})
  self.assertIn('island_group',{r['geography_level'] for r in data})
  self.assertNotIn('municipality',{r['geography_level'] for r in data})
 def test_emergency_arithmetic_and_non_comparability(self):
  data={r['indicator_id']:r for r in rows('pediatric_emergency_activity.csv')}
  self.assertEqual(float(data['admitted_from_ed']['value'])+float(data['not_admitted']['value']),float(data['pediatric_ed_visits']['value']))
  self.assertEqual({r['comparability_status'] for r in data.values()},{'PARTIALLY_COMPARABLE'})
 def test_manifest_checksums_and_domain_admission(self):
  manifest=json.loads((ROOT/'data/manifests/phase5_clinical_manifest.json').read_text())
  for rel,meta in manifest['outputs'].items():
   self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),meta['sha256'])
  quality=rows('clinical_data_quality.csv')
  self.assertGreaterEqual(sum(r['admission_status'].startswith('ADMIT') for r in quality),3)
if __name__=='__main__': unittest.main()
