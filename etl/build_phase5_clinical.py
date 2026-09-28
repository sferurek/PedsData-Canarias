#!/usr/bin/env python3
"""Curate Phase 5 clinical data without changing source age or geography."""
from __future__ import annotations
import csv, hashlib, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data/raw"; OUT=ROOT/"data/curated"; REF=ROOT/"data/reference"
S={
"hospitalization":("ISTAC:E30414A_000009","istac_hospitalization_residents_2020_2024.csv","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E30414A_000009/~latest.csv"),
"perinatal":("ISTAC:E30304A_000008","istac_birth_maturity_1999_2024.csv","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E30304A_000008/~latest.csv"),
"mortality":("ISTAC:E30417A_000001","istac_mortality_causes_islands_1999_2024.csv","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E30417A_000001/~latest.csv"),
"survey":("ISTAC:C00035A_000465","istac_child_health_survey_2021_health_problems.csv","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/C00035A_000465/~latest.csv")}
ISLAND={"El Hierro":"el-hierro","La Gomera":"la-gomera","La Palma":"la-palma","Tenerife":"tenerife","Gran Canaria":"gran-canaria","Fuerteventura":"fuerteventura","Lanzarote":"lanzarote","Canarias":"canarias"}
AGES={"Y_LT1":"<1 año","Y1T4":"1–4 años","Y5T14":"5–14 años"}
DIAG=[("infectious","Enfermedades infecciosas","0100","A00","B99","Capítulo oficial agregado."),("diabetes","Diabetes","0401","E08","E13","No separa cetoacidosis."),("mental_health","Salud mental","0500","F01","F99","Capítulo agregado."),("epilepsy","Epilepsia","0603","G40","G40","Categoría oficial."),("pneumonia","Neumonía","1002","J12","J18","Categoría oficial."),("lower_respiratory","Infecciones respiratorias bajas","1003","J20","J22","Incluye bronquitis aguda y bronquiolitis; no permite aislar bronquiolitis."),("asthma","Asma","1007","J45","J45","Categoría oficial."),("appendix","Enfermedades del apéndice","1106","K35","K38","Incluye apendicitis y otras enfermedades del apéndice."),("injury","Lesiones y traumatismos","1900","S00","T98","Capítulo oficial agregado.")]
COMMON=["source_id","dataset_version","reference_period","geography_level","geography_id","age_group_original","sex","unit","value","numerator","denominator","value_status","comparability_status","method_id","source_url","publication_date","case_definition"]

def rows(name):
    with (RAW/S[name][1]).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def n(v):
    try:return float(v)
    except (TypeError,ValueError):return None
def write(path,data,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(data)
def base():return dict.fromkeys(COMMON,"")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def hospitalization():
    lookup={x[2]:(x[0],x[1]) for x in DIAG};out=[];sid,_,url=S["hospitalization"]
    for r in rows("hospitalization"):
        if r["SEXO_CODE"]!="_T" or r["GRUPO_EDAD_CODE"] not in AGES or r["DIAGNOSTICO_PRINCIPAL_CODE"] not in lookup:continue
        value=n(r["OBS_VALUE"]);measure=r["MEDIDAS_CODE"]
        if value is None:continue
        gid,gname=lookup[r["DIAGNOSTICO_PRINCIPAL_CODE"]];unit={"ALTAS":"discharges","ESTANCIA":"days","ESTANCIA_MEDIA":"days"}.get(measure,measure.lower())
        out.append({**base(),"indicator_id":measure.lower(),"diagnosis_group_id":gid,"diagnosis_group_name":gname,"source_diagnosis_code":r["DIAGNOSTICO_PRINCIPAL_CODE"],"source_id":sid,"dataset_version":"latest_audited_2026-09-28","reference_period":r["TIME_PERIOD_CODE"],"geography_level":"autonomous_community","geography_id":"canarias","age_group_original":r["GRUPO_EDAD#es"],"age_group_code":r["GRUPO_EDAD_CODE"],"sex":"total","unit":unit,"value":f"{value:g}","numerator":f"{value:g}" if measure!="ESTANCIA_MEDIA" else "","value_status":"OBSERVED","comparability_status":"ADMIT_WITH_LIMITATIONS","method_id":"emh_resident_pediatric_v1","source_url":url,"publication_date":"2026-09-24","case_definition":"Residentes canarios dados de alta en cualquier hospital nacional; diagnóstico principal y edad originales."})
    return out

def perinatal():
    sid,_,url=S["perinatal"];g=defaultdict(dict);out=[]
    for r in rows("perinatal"):
        value=n(r["OBS_VALUE"])
        if r["TERRITORIO#es"] in ISLAND and value is not None:g[(r["TIME_PERIOD_CODE"],r["TERRITORIO#es"])][r["MATURIDAD_CODE"]]=value
    for (year,territory),v in sorted(g.items()):
        total,pre=v.get("_T"),v.get("PREMATURO")
        if total is None or pre is None:continue
        common={"source_id":sid,"dataset_version":"latest_audited_2026-09-28","reference_period":year,"geography_level":"autonomous_community" if territory=="Canarias" else "island","geography_id":ISLAND[territory],"age_group_original":"Perinatal — nacimientos","sex":"total","comparability_status":"ADMIT","method_id":"istac_birth_maturity_v1","source_url":url,"publication_date":"2026-09-24","case_definition":"Nacimientos de madres residentes según maturidad del parto."}
        out += [{**base(),**common,"indicator_id":"births","unit":"births","value":f"{total:g}","numerator":f"{total:g}","value_status":"OBSERVED"},{**base(),**common,"indicator_id":"preterm_births","unit":"births","value":f"{pre:g}","numerator":f"{pre:g}","value_status":"OBSERVED"},{**base(),**common,"indicator_id":"preterm_rate","unit":"percent","value":f"{100*pre/total:.2f}" if total else "","numerator":f"{pre:g}","denominator":f"{total:g}","value_status":"DERIVED_RATE"}]
    return out

def mortality():
    sid,_,url=S["mortality"];years={str(y) for y in range(2020,2025)};causes={"_T","I","II","X","XVI","XVII","XX"};g=defaultdict(float);labels={};out=[]
    for r in rows("mortality"):
        terr=r["LUGAR_RESIDENCIA#es"];age=r["GRUPO_EDAD_CODE"];cause=r["CAUSA_BASICA_DEFUNCION_CODE"];value=n(r["OBS_VALUE"])
        if terr not in ISLAND or terr=="Canarias" or r["TIME_PERIOD_CODE"] not in years or r["SEXO_CODE"]!="_T" or age not in AGES or cause not in causes or value is None:continue
        g[(terr,age,cause)]+=value;labels[cause]=r["CAUSA_BASICA_DEFUNCION#es"]
    for (terr,age,cause),count in sorted(g.items()):
        suppressed=0<count<5
        out.append({**base(),"indicator_id":"deaths","cause_group_code":cause,"cause_group_name":labels[cause],"window_start":"2020","window_end":"2024","suppressed":str(suppressed).lower(),"source_id":sid,"dataset_version":"latest_audited_2026-09-28","reference_period":"2020-2024","geography_level":"island","geography_id":ISLAND[terr],"age_group_original":AGES[age],"age_group_code":age,"sex":"total","unit":"deaths","value":"" if suppressed else f"{count:g}","numerator":"" if suppressed else f"{count:g}","value_status":"MULTIYEAR_AGGREGATE","comparability_status":"ADMIT_WITH_LIMITATIONS","method_id":"mortality_5y_small_numbers_v1","source_url":url,"publication_date":"2026-09-24","case_definition":"Defunciones de residentes; grandes grupos CIE-10; ventana fija de cinco años."})
    return out

def survey():
    sid,_,url=S["survey"];out=[]
    for r in rows("survey"):
        value=n(r["OBS_VALUE"]);territory=r["TERRITORIO#es"]
        if r["PADECIDO_ALGUNA_VEZ_CODE"]!="1" or r["MEDIDAS_CODE"]!="POBLACION_PORCENTAJE" or value is None:continue
        level="autonomous_community" if territory=="Canarias" else ("island" if territory in ("Gran Canaria","Tenerife") else "island_group")
        out.append({**base(),"indicator_id":r["PROBLEMAS_SALUD_CODE"].lower(),"indicator_name":r["PROBLEMAS_SALUD#es"],"source_id":sid,"dataset_version":"latest_audited_2026-09-28","reference_period":"2021","geography_level":level,"geography_id":ISLAND.get(territory,territory.lower().replace(" ","-").replace(",","")),"geography_label":territory,"age_group_original":"Población menor de 16 años","sex":"total","unit":"percent","value":f"{value:g}","value_status":"SURVEY_ESTIMATE","comparability_status":"ADMIT_WITH_LIMITATIONS","method_id":"esc2021_published_estimate_v1","source_url":url,"publication_date":"2023-03-16","case_definition":"Problema de salud padecido alguna vez, ESC 2021."})
    return out

def emergency():
    url="https://www3.gobiernodecanarias.org/sanidad/scs/scs/as/gc/30/memorias/24/pages/Datos_Asistenciales_Especialidades.html"
    common={"source_id":"SCS:CHUIMI_MEMORIA_2024","dataset_version":"2024","reference_period":"2024","geography_level":"hospital","geography_id":"chuimi","hospital_name":"Complejo Hospitalario Universitario Insular-Materno Infantil","island_id":"gran-canaria","age_group_original":"Pediátrica; límite etario no publicado en la tabla","sex":"total","comparability_status":"PARTIALLY_COMPARABLE","method_id":"chuimi_emergency_memory_v1","source_url":url,"publication_date":"2025","case_definition":"Urgencias pediátricas según memoria institucional."}
    vals=[("pediatric_ed_visits","visits",45002,"OBSERVED"),("admitted_from_ed","visits",1973,"OBSERVED"),("not_admitted","visits",43029,"OBSERVED"),("admission_rate","percent",round(1973/45002*100,2),"DERIVED_RATE")]
    return [{**base(),**common,"indicator_id":i,"unit":u,"value":str(v),"numerator":"1973" if i=="admission_rate" else str(v),"denominator":"45002" if i=="admission_rate" else "","value_status":s} for i,u,v,s in vals]

def main():
    missing=[str(RAW/x[1]) for x in S.values() if not (RAW/x[1]).exists()]
    if missing:raise SystemExit("Missing audited inputs: "+", ".join(missing))
    ref=[{"group_id":a,"group_name":b,"coding_system":"CIE-10 / agrupación EMH","source_group_code":c,"code_start":d,"code_end":e,"include":f"{d}-{e}" if d!=e else d,"exclude":"","clinical_notes":f,"version":"phase5-v1"} for a,b,c,d,e,f in DIAG]
    write(REF/"pediatric_diagnosis_groups.csv",ref,list(ref[0]))
    sets=[("pediatric_hospital_indicators.csv",hospitalization(),COMMON+["indicator_id","diagnosis_group_id","diagnosis_group_name","source_diagnosis_code","age_group_code"]),("perinatal_indicators.csv",perinatal(),COMMON+["indicator_id"]),("pediatric_mortality.csv",mortality(),COMMON+["indicator_id","cause_group_code","cause_group_name","window_start","window_end","suppressed","age_group_code"]),("child_health_survey_indicators.csv",survey(),COMMON+["indicator_id","indicator_name","geography_label"]),("pediatric_emergency_activity.csv",emergency(),COMMON+["indicator_id","hospital_name","island_id"])]
    files=[]
    for name,data,fields in sets:
        p=OUT/name;write(p,data,fields);files.append(p)
    quality=[{"domain":"hospitalization","admission_status":"ADMIT_WITH_LIMITATIONS","geography":"Canarias","period":"2020-2024","limitation":"Edad × diagnóstico solo para Canarias."},{"domain":"perinatal","admission_status":"ADMIT","geography":"Canarias/isla","period":"1999-2024","limitation":"Residencia materna."},{"domain":"emergency","admission_status":"ADMIT_WITH_LIMITATIONS","geography":"hospital","period":"2024","limitation":"Solo CHUIMI; no comparar hospitales."},{"domain":"mortality","admission_status":"ADMIT_WITH_LIMITATIONS","geography":"isla","period":"2020-2024","limitation":"Ventana quinquenal; 1-4 suprimidos."},{"domain":"survey","admission_status":"ADMIT_WITH_LIMITATIONS","geography":"Canarias/isla/grupo de islas","period":"2021","limitation":"Estimación; n/error no publicados por celda."}]
    qp=OUT/"clinical_data_quality.csv";write(qp,quality,list(quality[0]));files += [qp,REF/"pediatric_diagnosis_groups.csv"]
    manifest={"generated_at":datetime.now(timezone.utc).isoformat(),"pipeline":"etl/build_phase5_clinical.py","sources":{k:{"source_id":v[0],"url":v[2],"sha256":sha(RAW/v[1])} for k,v in S.items()},"outputs":{str(p.relative_to(ROOT)):{"sha256":sha(p),"rows":sum(1 for _ in p.open())-1} for p in files},"rules":{"islands":7,"mortality_window":"2020-2024","small_number_suppression":"1-4","hospital_geography":"Canarias only","survey_status":"SURVEY_ESTIMATE"}}
    mp=ROOT/"data/manifests/phase5_clinical_manifest.json";mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__":main()
