#!/usr/bin/env python3
"""Enrich RC1 web assets with validated Phase 4 contextual layers."""
import csv,json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; WEB=ROOT/'apps/web'; PUBLIC=WEB/'public/data'; PROFILES=WEB/'src/data/profiles.json'
def rows(name):
    with (ROOT/'data/curated'/name).open(encoding='utf-8',newline='') as h:return list(csv.DictReader(h))
def weighted(items):
    den=sum(w for _,w in items); return round(sum(v*w for v,w in items)/den,2) if den else None
def main():
    profiles=json.loads(PROFILES.read_text()); income=rows('socioeconomic_indicators.csv'); territory=rows('territorial_context.csv'); stations=rows('air_stations.csv'); observations=rows('air_observations.csv'); weather=rows('weather_stations.csv')
    income_lookup={(r['municipality_id'],r['indicator']):float(r['value']) for r in income}; territory_lookup={r['municipality_id']:r for r in territory}
    for m in profiles['municipalities']:
        t=territory_lookup[m['municipality_id']]; m.update(income_mean_per_person_2023=income_lookup[(m['municipality_id'],'net_income_mean_per_person')],income_mean_per_household_2023=income_lookup[(m['municipality_id'],'net_income_mean_per_household')],income_median_per_consumption_unit_2023=income_lookup[(m['municipality_id'],'net_income_median_per_consumption_unit')],child_density_per_km2=float(t['child_density_per_km2']),rural_children_pct=float(t['degurba_rural_children_pct']),territorial_status=t['status'])
    municipalities_by_island=defaultdict(list)
    for m in profiles['municipalities']: municipalities_by_island[m['island_id']].append(m)
    air_counts=defaultdict(int); weather_counts=defaultdict(int)
    for s in stations: air_counts[s['island_id']]+=1
    for s in weather: weather_counts[s['island_id']]+=1
    for island in profiles['islands']:
        ms=municipalities_by_island[island['island_id']]; weights=[(m['income_mean_per_person_2023'],int(m.get('children_0_14') or 0)) for m in ms if m.get('children_0_14')]
        total_area=sum(float(territory_lookup[m['municipality_id']]['area_km2']) for m in ms); total_children=sum(int(territory_lookup[m['municipality_id']]['children_0_14']) for m in ms)
        rural=weighted([(float(territory_lookup[m['municipality_id']]['degurba_rural_children_pct']),int(territory_lookup[m['municipality_id']]['children_0_14'])) for m in ms])
        island.update(income_mean_per_person_2023=weighted(weights),child_density_per_km2=round(total_children/total_area,2),rural_children_pct=rural,air_station_count=air_counts[island['island_id']],weather_station_count=weather_counts[island['island_id']])
    latest={}
    for o in observations:
        key=(o['station_id'],o['pollutant']); current=latest.get(key)
        if current is None or o['period_start']>current['period_start']: latest[key]=o
    features=[]
    for station in stations:
        if not station['longitude'] or not station['latitude']: continue
        props={'station_id':station['station_id'],'name':station['name'],'island_id':station['island_id'],'municipality_id':station['municipality_id'],'status':station['status'],'source':'Red Canaria de Calidad del Aire','period':'2025'}
        for pollutant in ('PM10','PM2.5','NO2','O3','SO2'):
            observation=latest.get((station['station_id'],pollutant)); props[pollutant]=float(observation['value']) if observation else None; props[pollutant+'_date']=observation['period_start'] if observation else None
        features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[float(station['longitude']),float(station['latitude'])]},'properties':props})
    (PUBLIC/'air-stations.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False,separators=(',',':')))
    weather_features=[{'type':'Feature','geometry':{'type':'Point','coordinates':[float(s['longitude']),float(s['latitude'])]},'properties':{'station_id':s['station_id'],'name':s['name'],'island_id':s['island_id'],'municipality_id':s['municipality_id'],'status':'PENDING_OBSERVATIONS','source':'SITCAN SICOM'}} for s in weather]
    (PUBLIC/'weather-stations.geojson').write_text(json.dumps({'type':'FeatureCollection','features':weather_features},ensure_ascii=False,separators=(',',':')))
    municipalities=json.loads((PUBLIC/'municipalities.geojson').read_text())
    context={m['municipality_id']:m for m in profiles['municipalities']}
    for feature in municipalities['features']:
        item=context[feature['properties']['municipality_id']]
        for key in ('income_mean_per_person_2023','income_mean_per_household_2023','income_median_per_consumption_unit_2023','child_density_per_km2','rural_children_pct','territorial_status'): feature['properties'][key]=item[key]
    (PUBLIC/'municipalities.geojson').write_text(json.dumps(municipalities,ensure_ascii=False,separators=(',',':')))
    profiles['metadata'].update(status='RC2',income_period=2023,air_period=2025,territorial_period='2021/2024',weather_status='PENDING OBSERVATIONS',calima_status='PENDING VALIDATION')
    PROFILES.write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'air_map_stations':len(features),'weather_stations':len(weather_features),'municipal_profiles':len(profiles['municipalities']),'island_profiles':len(profiles['islands'])},indent=2))
if __name__=='__main__':main()
