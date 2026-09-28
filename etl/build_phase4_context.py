#!/usr/bin/env python3
"""Build Phase 4 social, territorial and environmental curated datasets."""
from __future__ import annotations
import csv, hashlib, json, re, unicodedata, zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from shapely.geometry import Point, shape
from xlsx_reader import iter_rows

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw'; CURATED=ROOT/'data/curated'; MANIFESTS=ROOT/'data/manifests'
RETRIEVED_AT='2026-09-28T00:00:00+00:00'
ISLAND_CODES={'ES703':'el-hierro','ES706':'la-gomera','ES707':'la-palma','ES709':'tenerife','ES705':'gran-canaria','ES704':'fuerteventura','ES708':'lanzarote'}
POLLUTANTS={'PM10','PM2,5','NO2','O3','SO2'}
AIR_ALIASES={'aguimes':'Agüimes','castillo romeral':'Castillo del Romeral','lezcano':'Pedro Lezcano','san agustin':'San Agustín','jinamar fase 3':'Jinámar fase 3','san nicolas':'San Nicolás','deposito tristan':'Depósito Tristán','garcia escamez':'García Escámez','parque la granja':'Parque de la Granja','tio pino':'Tío Pino','deposito la guancha':'Depósito La Guancha','medano':'Médano'}

def normalize(value):
    value=''.join(c for c in unicodedata.normalize('NFKD',value) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+',' ',value.casefold()).strip()
def slug(value): return normalize(value).replace(' ','-')
def checksum(path):
    d=hashlib.sha256()
    with path.open('rb') as h:
        for b in iter(lambda:h.read(1024*1024),b''): d.update(b)
    return d.hexdigest()
def write_csv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(rows)
def municipalities():
    doc=json.loads((RAW/'municipios_desde2007_generalizada_20170101.geojson').read_text())
    return [{'municipality_id':f['properties']['geocode'],'municipality_name':f['properties']['etiqueta'],'island_id':ISLAND_CODES[f['properties']['gcd_isla']],'geometry':shape(f['geometry']),'area_km2':float(f['properties']['ign_sup'])/100} for f in doc['features']]
def municipality_for_point(point,records): return next((r for r in records if r['geometry'].covers(point)),None)

def income_rows(records):
    official={normalize(r['municipality_name']):r for r in records}
    aliases={'palmas de gran canaria las':'las palmas de gran canaria','aldea de san nicolas la':'la aldea de san nicolas','oliva la':'la oliva','rosario el':'el rosario','llanos de aridane los':'los llanos de aridane','sauzal el':'el sauzal','tanque el':'el tanque'}
    indicators={'Renta neta media por persona':('net_income_mean_per_person','EUR/persona'),'Renta neta media por hogar':('net_income_mean_per_household','EUR/hogar'),'Mediana de la renta por unidad de consumo':('net_income_median_per_consumption_unit','EUR/unidad_consumo')}
    output=[]
    for path in [RAW/'ine_adrh_2023_las_palmas.json',RAW/'ine_adrh_2023_santa_cruz_tenerife.json']:
        for series in json.loads(path.read_text()):
            name=series['Nombre'].strip()
            if ' sección ' in name or ' distrito ' in name or '. Dato base. ' not in name: continue
            place,measure=name.split('. Dato base. ',1); measure=measure.rstrip('. ')
            if measure not in indicators or not series.get('Data'): continue
            place_key=normalize(place); parts=[item.strip() for item in place.split(',')]; place_key=normalize(parts[1]+' '+parts[0]) if len(parts)==2 else place_key; municipality=official.get(aliases.get(place_key,place_key))
            if not municipality: raise ValueError(f'INE municipality did not match: {place}')
            indicator,unit=indicators[measure]
            output.append({'municipality_id':municipality['municipality_id'],'municipality_name':municipality['municipality_name'],'island_id':municipality['island_id'],'indicator':indicator,'period_start':'2023-01-01','period_end':'2023-12-31','value':series['Data'][0]['Valor'],'unit':unit,'status':'COMPLETE','geography_level':'municipality','source_id':'ine-adrh','dataset_version':'ADRH-2023','retrieved_at':RETRIEVED_AT})
    return sorted(output,key=lambda r:(r['municipality_id'],r['indicator']))

def territorial_rows(records):
    grid=json.loads((RAW/'child_population_grid_2024.geojson').read_text()); deg=json.loads((RAW/'istac_degurba_1km_2021.geojson').read_text())
    zones=[(f['properties']['cod_degurba_l1'],shape(f['geometry'])) for f in deg['features']]
    grouped=defaultdict(lambda:{'children':0,'cells':0,'classes':defaultdict(int)})
    for feature in grid['features']:
        p=feature['properties']; children=int(float(p['poblacion_00a14'] or 0))
        if children<=0: continue
        point=shape(feature['geometry']).representative_point(); degree=next((code for code,poly in zones if poly.covers(point)),'NOT_AVAILABLE')
        g=grouped[str(p['municipio'])]; g['children']+=children; g['cells']+=1; g['classes'][degree]+=children
    rows=[]
    for m in records:
        g=grouped[m['municipality_id']]; total=g['children']; c=g['classes']
        rows.append({'municipality_id':m['municipality_id'],'municipality_name':m['municipality_name'],'island_id':m['island_id'],'period_start':'2024-01-01','period_end':'2024-12-31','children_0_14':total,'area_km2':round(m['area_km2'],4),'child_density_per_km2':round(total/m['area_km2'],3),'populated_child_cells':g['cells'],'children_per_populated_cell':round(total/g['cells'],3),'degurba_urban_centre_children_pct':round(100*c['CENTROS_URBANOS_NIVEL_1']/total,2),'degurba_urban_cluster_children_pct':round(100*c['AGRUPACIONES_URBANAS']/total,2),'degurba_rural_children_pct':round(100*c['CELDAS_RURALES']/total,2),'degurba_unclassified_children_pct':round(100*c['NOT_AVAILABLE']/total,2),'status':'ESTIMATED','geography_level':'municipality','source_id':'istac-grid-degurba','dataset_version':'grid-2024+degurba-2021','retrieved_at':RETRIEVED_AT})
    return rows

def pdf_coordinate_lines(path):
    text='\n'.join(p.extract_text() or '' for p in PdfReader(path).pages); pattern=re.compile(r'(\d+)°\s*(\d+)\'([\d.]+)"N\s+(\d+)°\s*(\d+)\'([\d.]+)"O')
    result={}
    for line in map(str.strip,text.splitlines()):
        match=pattern.search(line)
        if match:
            a,b,c,d,e,f=map(float,match.groups()); result[normalize(line[:match.start()].strip())]=(a+b/60+c/3600,-(d+e/60+f/3600))
    return result
def station_coordinate(name,lines):
    target=normalize(AIR_ALIASES.get(normalize(name),name)); matches=[(k,v) for k,v in lines.items() if k.startswith(target+' ') or k==target or (' '+target+' ') in (' '+k+' ')]
    return min(matches,key=lambda x:len(x[0]))[1] if matches else None
def excel_date(serial): return (datetime(1899,12,30)+timedelta(days=float(serial))).date().isoformat()

def air_rows(records):
    workbook=RAW/'canarias_air_quality_2025'/'Datos diarios_2025.xlsx'; lines=pdf_coordinate_lines(RAW/'canarias_air_station_summary_2024.pdf')
    with zipfile.ZipFile(workbook) as archive:
        root=ET.fromstring(archive.read('xl/workbook.xml')); ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
        sheets=[s.attrib['name'] for s in root.findall(f'.//{ns}sheet')]
    stations=[]; observations=[]
    for sheet in sheets:
        rows=iter_rows(workbook,sheet); headers=next(rows); coords=station_coordinate(sheet,lines)
        municipality=municipality_for_point(Point(coords[1],coords[0]),records) if coords else None
        island=municipality['island_id'] if municipality else ('gran-canaria' if sheet=='Observatorio Temisas' else 'tenerife' if sheet=='Hacienda' else '')
        station_id='air-'+slug(sheet); pollutants=[x.replace('PM2,5','PM2.5') for x in headers if x in POLLUTANTS]
        stations.append({'station_id':station_id,'name':sheet,'island_id':island,'municipality_id':municipality['municipality_id'] if municipality else '','municipality_name':municipality['municipality_name'] if municipality else '','latitude':coords[0] if coords else '','longitude':coords[1] if coords else '','station_type':'monitoring_station','pollutants':'|'.join(pollutants),'status':'VALIDATED' if coords else 'PARTIAL','source_id':'canarias-air-network','dataset_version':'validated-daily-2025','period_start':'2025-01-01','period_end':'2025-12-31','retrieved_at':RETRIEVED_AT})
        for values in rows:
            rec=dict(zip(headers,values+['']*(len(headers)-len(values))))
            if not rec.get('fecha'): continue
            date=excel_date(rec['fecha'])
            for pollutant in headers:
                if pollutant in POLLUTANTS and rec.get(pollutant,'')!='':
                    observations.append({'station_id':station_id,'island_id':island,'municipality_id':municipality['municipality_id'] if municipality else '','pollutant':pollutant.replace('PM2,5','PM2.5'),'period_start':date,'period_end':date,'value':rec[pollutant],'unit':'µg/m³','status':'VALIDATED','geography_level':'station','source_id':'canarias-air-network','dataset_version':'validated-daily-2025','retrieved_at':RETRIEVED_AT})
    return stations,observations

def weather_stations(records):
    rows=[]
    with (RAW/'sitcan_weather_stations.csv').open(encoding='latin-1',newline='') as h:
        for s in csv.DictReader(h):
            match=re.match(r'POINT\(([-\d.]+) ([-\d.]+)\)',s['location_coordinates'])
            if not match: continue
            lon,lat=map(float,match.groups()); m=municipality_for_point(Point(lon,lat),records)
            if not m: continue
            rows.append({'station_id':'weather-'+s['thing_id'],'official_id':s['thing_id'],'name':s['thing_name'],'description':s['location_description'],'island_id':m['island_id'],'municipality_id':m['municipality_id'],'latitude':lat,'longitude':lon,'period_start':s['date_from'][:10],'period_end':s['date_to'][:10] if s['date_to'] else '','status':'COMPLETE','source_id':'sitcan-sicom','dataset_version':'stations-2026-09-27','retrieved_at':RETRIEVED_AT})
    return rows

def main():
    records=municipalities(); income=income_rows(records); territory=territorial_rows(records); air_stations,air_obs=air_rows(records); weather=weather_stations(records)
    write_csv(CURATED/'socioeconomic_indicators.csv',income,list(income[0])); write_csv(CURATED/'territorial_context.csv',territory,list(territory[0])); write_csv(CURATED/'air_stations.csv',air_stations,list(air_stations[0])); write_csv(CURATED/'air_observations.csv',air_obs,list(air_obs[0])); write_csv(CURATED/'weather_stations.csv',weather,list(weather[0]))
    write_csv(CURATED/'weather_observations.csv',[],['station_id','variable','period_start','period_end','value','unit','status','geography_level','source_id','dataset_version','retrieved_at']); write_csv(CURATED/'environment_events.csv',[],['event_id','event_type','period_start','period_end','geography_level','geography_id','status','source_id','dataset_version','retrieved_at'])
    sources={'income_las_palmas':RAW/'ine_adrh_2023_las_palmas.json','income_santa_cruz':RAW/'ine_adrh_2023_santa_cruz_tenerife.json','degurba':RAW/'istac_degurba_1km_2021.geojson','air_daily':RAW/'canarias_air_quality_2025'/'Datos diarios_2025.xlsx','air_coordinates':RAW/'canarias_air_station_summary_2024.pdf','weather_stations':RAW/'sitcan_weather_stations.csv'}
    manifest={'created_at':datetime.now(timezone.utc).isoformat(),'parser_version':'phase4-v1','causality_claimed':False,'air_interpolation':False,'weather_observations_status':'NOT_AVAILABLE_API_KEY_REQUIRED','calima_status':'PROVISIONAL_SOURCE_NOT_PUBLISHED_AS_CONFIRMED_EVENT','sources':{k:{'path':str(p.relative_to(ROOT)),'checksum_sha256':checksum(p)} for k,p in sources.items()},'outputs':{'socioeconomic_rows':len(income),'territorial_rows':len(territory),'air_stations':len(air_stations),'air_observations':len(air_obs),'weather_stations':len(weather)}}
    MANIFESTS.mkdir(exist_ok=True); (MANIFESTS/'phase4_context_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(manifest['outputs'],indent=2))
if __name__=='__main__': main()
