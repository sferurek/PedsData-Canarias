#!/usr/bin/env python3
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
 with (ROOT/'data/curated'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def number(v):return None if v=='' else float(v)
hosp=[{**r,'value':number(r['value']),'numerator':number(r['numerator']),'denominator':number(r['denominator'])} for r in read('pediatric_hospital_indicators.csv')]
peri=[{**r,'value':number(r['value']),'numerator':number(r['numerator']),'denominator':number(r['denominator'])} for r in read('perinatal_indicators.csv') if r['reference_period']=='2024']
mort=[{**r,'value':number(r['value']),'suppressed':r['suppressed']=='true'} for r in read('pediatric_mortality.csv') if r['cause_group_code']=='_T']
survey=[{**r,'value':number(r['value'])} for r in read('child_health_survey_indicators.csv')]
emergency=[{**r,'value':number(r['value']),'numerator':number(r['numerator']),'denominator':number(r['denominator'])} for r in read('pediatric_emergency_activity.csv')]
islands=['el-hierro','la-gomera','la-palma','tenerife','gran-canaria','fuerteventura','lanzarote']
summary={}
for island in islands:
 p={r['indicator_id']:r['value'] for r in peri if r['geography_id']==island}
 total_age=[r for r in mort if r['geography_id']==island]
 death=None if any(r['suppressed'] for r in total_age) else sum(r['value'] or 0 for r in total_age)
 summary[island]={'births_2024':p.get('births'),'preterm_births_2024':p.get('preterm_births'),'preterm_rate_2024':p.get('preterm_rate'),'pediatric_deaths_2020_2024':death,'mortality_status':'PARTIAL' if death is None else 'MULTIYEAR_AGGREGATE','emergency_status':'PARTIAL' if island=='gran-canaria' else 'NOT_AVAILABLE'}
payload={'metadata':{'version':'RC3','hospital_period':'2020–2024','perinatal_period':'2024','mortality_period':'2020–2024','survey_period':'2021'},'hospitalization':hosp,'perinatal':peri,'mortality':mort,'survey':survey,'emergency':emergency,'island_summary':summary}
out=ROOT/'apps/web/src/data/clinical.json';out.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
