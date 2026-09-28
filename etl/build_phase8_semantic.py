#!/usr/bin/env python3
"""Build Phase 8 semantic registries, time series, and true island geometry."""
from __future__ import annotations
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path
from typing import Any
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parents[1]
ISLANDS={"El Hierro":"el-hierro","La Gomera":"la-gomera","La Palma":"la-palma","Tenerife":"tenerife","Gran Canaria":"gran-canaria","Fuerteventura":"fuerteventura","Lanzarote":"lanzarote","Canarias":"canarias"}
LABELS={v:k for k,v in ISLANDS.items()}
SEVEN=tuple(v for v in ISLANDS.values() if v!="canarias")

def read(path):
    with (ROOT/path).open(newline="",encoding="utf-8-sig") as h:return list(csv.DictReader(h))
def write(path,payload):
    target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def point(metric,geo,period,value,unit,status,source,method,level,dimension=None):
    item={"metric_id":metric,"geography_level":level,"geography_id":geo,"period":str(period),"value":round(value,4),"unit":unit,"status":status,"source_id":source,"method_id":method}
    if dimension:item["dimension"]=dimension
    return item

def build_series():
    out=[]
    assigned=defaultdict(float)
    for r in read("docs/evidence/siap_population.csv"):
        island=ISLANDS.get(r["TERRITORIO#es"])
        if island in SEVEN and r["SEXO_CODE"]=="_T" and r["GRUPO_EDAD_CODE"] in {"Y0T4","Y5T9","Y10T14"} and r["OBS_VALUE"]:
            assigned[island,r["TIME_PERIOD_CODE"]]+=float(r["OBS_VALUE"])
    for (island,year),value in sorted(assigned.items()):
        out.append(point("child_population_assigned_0_14",island,year,value,"persons","OBSERVED","ISTAC:E54086A_000002","siap_assigned_population_sum_0_14_v1","island"))

    pediatricians={}
    for r in read("docs/evidence/siap_professionals.csv"):
        island=ISLANDS.get(r["TERRITORIO#es"])
        if island not in SEVEN or r["TIPO_PROFESIONAL_ATENCION_PRIMARIA_CODE"]!="PEDIATRIA_AP" or not r["OBS_VALUE"]:continue
        if r["MEDIDAS_CODE"]=="NUMERO_PROFESIONALES_AP":
            pediatricians[island,r["TIME_PERIOD_CODE"]]=float(r["OBS_VALUE"])
            out.append(point("pediatricians_ap",island,r["TIME_PERIOD_CODE"],float(r["OBS_VALUE"]),"professionals","OBSERVED","ISTAC:E54086A_000001","siap_pediatricians_original_v1","island"))
        elif r["MEDIDAS_CODE"]=="RATIO_PROFESIONAL":
            out.append(point("assigned_children_per_pediatrician",island,r["TIME_PERIOD_CODE"],float(r["OBS_VALUE"]),"assigned_persons/professional","DERIVED_RATE","ISTAC:E54086A_000001","siap_published_ratio_v1","island"))

    for r in read("data/curated/pediatric_primary_care_activity.csv"):
        if r["geography_level"]!="island" or r["place"]!="_T" or r["value_status"]!="OBSERVED" or not r["value"]:continue
        metric={"consultations":"pediatric_consultations","distinct_persons":"pediatric_distinct_users","frequentation":"pediatric_frequentation"}[r["activity_type"]]
        out.append(point(metric,r["island_id"],r["year"],float(r["value"]),r["unit"],r["value_status"],f"ISTAC:{r['source_id']}",r["method_id"],"island"))
        staff=pediatricians.get((r["island_id"],r["year"]))
        if r["activity_type"]=="consultations" and staff:
            out.append(point("consultations_per_pediatrician",r["island_id"],r["year"],float(r["value"])/staff,"consultations/professional","DERIVED_RATE","ISTAC:E54086A","consultations_divided_by_pediatricians_v1","island"))

    for r in read("data/curated/perinatal_indicators.csv"):
        if r["geography_level"]=="island" and r["indicator_id"] in {"births","preterm_rate"}:
            out.append(point(r["indicator_id"],r["geography_id"],r["reference_period"],float(r["value"]),r["unit"],r["value_status"],r["source_id"],r["method_id"],"island"))

    for r in read("data/curated/pediatric_waiting_list.csv"):
        if r["geography_level"]=="autonomous_community" and r["specialty"]=="PEDIATRIA" and r["time_band"]=="_T" and r["pending_patients"]:
            out.append(point("pediatric_outpatient_waiting_stock","canarias",r["reference_date"],float(r["pending_patients"]),"pending_patients",r["data_status"],"ISTAC:C00045A_000002",r["method_id"],"autonomous_community"))

    sums=defaultdict(float)
    for r in read("data/curated/pediatric_hospital_indicators.csv"):
        if r["indicator_id"]=="altas" and r["value"]:sums[r["reference_period"],r["diagnosis_group_id"]]+=float(r["value"])
    for (year,diagnosis),value in sorted(sums.items()):
        out.append(point("pediatric_hospital_discharges_selected","canarias",year,value,"discharges","OBSERVED","ISTAC:E30414A_000009","selected_diagnosis_age_sum_v1","autonomous_community",diagnosis))
    order={x:i for i,x in enumerate((*SEVEN,"canarias"))}
    return sorted(out,key=lambda r:(r["metric_id"],order.get(r["geography_id"],99),r["period"],r.get("dimension","")))

def metric(mid,label,description,geos,start,end,unit,charts,map_geo,classification,color,compatible,source,method,status):
    return {"metric_id":mid,"label":label,"description":description,"geography_levels":geos,"time_start":start,"time_end":end,"unit":unit,"chart_types":charts,"map_allowed":map_geo is not None,"map_geography":map_geo,"classification_method":classification,"color_scale":color,"compatible_metrics":compatible,"source_id":source,"method_id":method,"status":status}

def catalog():
    temporal=["line","bar","small_multiples","heatmap","slope"]
    return [
      metric("child_population_assigned_0_14","Población asignada 0–14","Suma de los grupos originales 0–4, 5–9 y 10–14, sexo total.",["island"],2004,2024,"personas",temporal,"island","quantile","sequential_blue",["pediatricians_ap","pediatric_consultations"],"ISTAC:E54086A_000002","siap_assigned_population_sum_0_14_v1","OBSERVED"),
      metric("pediatricians_ap","Pediatras de Atención Primaria","Profesionales de Pediatría AP publicados por SIAP.",["island"],2004,2024,"profesionales",temporal,"island","equal_interval","sequential_teal",["child_population_assigned_0_14","pediatric_consultations"],"ISTAC:E54086A_000001","siap_pediatricians_original_v1","OBSERVED"),
      metric("assigned_children_per_pediatrician","Población asignada por pediatra","Ratio por profesional publicado por SIAP; no es población censal.",["island"],2004,2024,"personas asignadas/profesional",["line","bar","small_multiples","heatmap"],"island","quantile","sequential_violet",["pediatricians_ap"],"ISTAC:E54086A_000001","siap_published_ratio_v1","DERIVED_RATE"),
      metric("pediatric_consultations","Consultas de Pediatría AP","Consultas totales del servicio de Pediatría AP.",["island"],2007,2024,"consultas",temporal,"island","quantile","sequential_blue",["pediatricians_ap","child_population_assigned_0_14","pediatric_distinct_users"],"ISTAC:E54086A_000005","siap_original_service_v1","OBSERVED"),
      metric("pediatric_distinct_users","Personas distintas atendidas","Personas distintas publicadas para Pediatría AP; no equivale a consultas.",["island"],2007,2024,"personas",["line","bar","small_multiples","heatmap"],None,None,None,["pediatric_consultations"],"ISTAC:E54086A_000007","siap_original_service_v1","OBSERVED"),
      metric("pediatric_frequentation","Frecuentación pediátrica","Consultas por persona asignada y año según definición SIAP.",["island"],2007,2024,"consultas/persona asignada/año",temporal,"island","equal_interval","sequential_violet",["pediatricians_ap","pediatric_consultations"],"ISTAC:E54086A_000009","siap_original_service_v1","OBSERVED"),
      metric("consultations_per_pediatrician","Consultas por pediatra","Consultas totales divididas por profesionales del mismo año e isla.",["island"],2007,2024,"consultas/profesional",["line","bar","small_multiples","heatmap"],None,None,None,["pediatricians_ap","pediatric_consultations"],"ISTAC:E54086A","consultations_divided_by_pediatricians_v1","DERIVED_RATE"),
      metric("births","Nacimientos","Nacimientos de madres residentes.",["island"],1999,2024,"nacimientos",temporal,"island","quantile","sequential_blue",["preterm_rate"],"ISTAC:E30304A_000008","istac_birth_maturity_v1","OBSERVED"),
      metric("preterm_rate","Prematuridad","Nacimientos prematuros sobre nacimientos de madres residentes.",["island"],1999,2024,"%",temporal,"island","fixed_thresholds","sequential_violet",["births"],"ISTAC:E30304A_000008","istac_birth_maturity_v1","DERIVED_RATE"),
      metric("pediatric_outpatient_waiting_stock","Stock de espera en Pediatría","Pacientes pendientes a fecha de corte; solo regional por semántica territorial no resuelta.",["autonomous_community"],2017,2025,"pacientes pendientes",["line","bar"],None,None,None,[],"ISTAC:C00045A_000002","waiting_regional_stock_v1","ADMINISTRATIVE_STOCK"),
      metric("pediatric_hospital_discharges_selected","Altas pediátricas en diagnósticos seleccionados","Suma regional por grupos diagnósticos seleccionados y edades pediátricas originales.",["autonomous_community"],2020,2024,"altas",["line","bar"],None,None,None,[],"ISTAC:E30414A_000009","selected_diagnosis_age_sum_v1","OBSERVED"),
      metric("income_mean_per_person","Renta media por persona","Renta general municipal; no equivale a renta infantil.",["municipality"],2023,2023,"€/persona",["bar","map","table"],"municipality","quantile","sequential_blue",["child_density"],"INE:ADRH","ine_adrh_municipality_v1","COMPLETE"),
      metric("child_density","Densidad infantil","Población 0–14 por superficie municipal.",["municipality"],2024,2024,"niños/km²",["bar","map","table"],"municipality","quantile","sequential_teal",["income_mean_per_person"],"ISTAC:grid+DEGURBA","child_density_municipality_v1","ESTIMATED"),
      metric("degurba","Urbanización DEGURBA","Categoría territorial oficial dominante; capa categórica municipal.",["municipality"],2021,2021,"categoría",["map","table"],"municipality","categorical","categorical_degurba",[],"ISTAC:DEGURBA","dominant_child_degurba_v1","ESTIMATED"),
      metric("PM10","PM10 observado","Valor observado en estación; no representa homogéneamente una isla.",["station"],2025,2025,"µg/m³",["map","table"],"station","fixed_thresholds","sequential_orange",[],"GobiernoCanarias:AIR","station_observation_v1","PROVISIONAL"),
      metric("PM2.5","PM2,5 observado","Valor observado en estación; no se interpola.",["station"],2025,2025,"µg/m³",["map","table"],"station","fixed_thresholds","sequential_orange",[],"GobiernoCanarias:AIR","station_observation_v1","PROVISIONAL"),
      metric("NO2","NO₂ observado","Valor observado en estación; no se interpola.",["station"],2025,2025,"µg/m³",["map","table"],"station","fixed_thresholds","sequential_orange",[],"GobiernoCanarias:AIR","station_observation_v1","PROVISIONAL"),
      metric("accessibility_ap","Accesibilidad a Pediatría AP","Tiempo estimado por carretera al destino verificado más próximo.",["grid_250m"],2024,2024,"bandas de minutos",["map","table"],"grid_250m","fixed_thresholds","accessibility_fixed",[],"PedsData:ACCESS","osrm_accessibility_v1","VALIDATED"),
    ]

def compatibility(metrics):
    pairs=[]
    for item in metrics:
        for other in item["compatible_metrics"]:
            pair=sorted([item["metric_id"],other])
            if pair not in pairs:pairs.append(pair)
    return {"version":"phase8-v1","valid_pairs":pairs,"invalid_pairs":[
      {"metrics":["PM10","pediatric_hospital_discharges_selected"],"reason":"Estación y hospitalización regional no comparten geografía para mapa directo."},
      {"metrics":["pediatric_hospital_discharges_selected","income_mean_per_person"],"reason":"La hospitalización regional no puede asignarse a municipios."},
      {"metrics":["pediatric_outpatient_waiting_stock","pediatricians_ap"],"reason":"El stock es regional y la dotación insular; la semántica territorial de espera no está resuelta."}
    ]}

def islands_geojson():
    source=json.loads((ROOT/"apps/web/public/data/municipalities.geojson").read_text(encoding="utf-8"))
    grouped=defaultdict(list)
    for feature in source["features"]:grouped[feature["properties"]["island_id"]].append(shape(feature["geometry"]))
    return {"type":"FeatureCollection","features":[{"type":"Feature","geometry":mapping(unary_union(grouped[i])),"properties":{"island_id":i,"island_name":LABELS[i]}} for i in SEVEN]}

def main():
    metrics=catalog();series=build_series();rules=compatibility(metrics)
    payload={"version":"phase8-v1","metrics":metrics};points={"version":"phase8-v1","points":series}
    write("data/semantic/metrics_catalog.json",payload);write("data/semantic/metric_compatibility.json",rules)
    write("data/semantic/geographies.json",{"version":"phase8-v1","islands":[{"id":i,"label":LABELS[i]} for i in SEVEN],"special_geographies":[{"id":"canarias","label":"Canarias","level":"autonomous_community"},{"id":"la-graciosa","label":"La Graciosa","level":"land_component","query_status":"INSUFFICIENT_DATA"}]})
    write("data/curated/metric_time_series.json",points);write("apps/web/src/data/metrics-catalog.json",payload)
    write("apps/web/src/data/metric-compatibility.json",rules);write("apps/web/src/data/metric-time-series.json",points)
    write("apps/web/public/data/islands.geojson",islands_geojson())
    inputs=["docs/evidence/siap_population.csv","docs/evidence/siap_professionals.csv","data/curated/pediatric_primary_care_activity.csv","data/curated/perinatal_indicators.csv","data/curated/pediatric_waiting_list.csv","data/curated/pediatric_hospital_indicators.csv"]
    write("data/manifests/phase8_manifest.json",{"version":"phase8-v1","inputs":[{"path":p,"sha256":sha(p)} for p in inputs],"outputs":{"time_series_points":len(series),"metrics":len(metrics),"islands":len(SEVEN)},"rules":["source geography preserved","no arbitrary SQL","one thematic fill layer at a time"]})
    print(f"Built {len(series)} temporal points across {len(metrics)} registered metrics")

if __name__=="__main__":main()
