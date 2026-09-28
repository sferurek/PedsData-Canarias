#!/usr/bin/env python3
"""Pinned Phase 6 curation. No network, imputation or regional disaggregation."""
import csv, hashlib, json, re, calendar
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
ISLANDS={"El Hierro":"el-hierro","La Gomera":"la-gomera","La Palma":"la-palma","Tenerife":"tenerife","Gran Canaria":"gran-canaria","Fuerteventura":"fuerteventura","Lanzarote":"lanzarote"}
PARSER="phase6-v1"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def numeric(value,status=""):
    if status or value.strip()=="": return None
    result=float(value)
    if result<0: raise ValueError("Negative observation")
    return result
def provenance(key,sources):
    s=sources[key]
    return {k:s[k] for k in ["source_url","dataset_version","checksum","retrieved_at","license_url"]}|{"source_id":key,"parser_version":PARSER}
def activity(sources):
    out=[]
    for kind in ("consultations","distinct_persons","frequentation"):
        for r in read(ROOT/sources[kind]["path"]):
            if r["TIPO_PROFESIONAL_ATENCION_PRIMARIA_CODE"]!="PEDIATRIA_AP" or r["TERRITORIO#es"] not in ISLANDS: continue
            value=numeric(r["OBS_VALUE"],r.get("ESTADO_OBSERVACION#es",""))
            out.append(provenance(kind,sources)|{"year":int(r["TIME_PERIOD_CODE"]),"island_id":ISLANDS[r["TERRITORIO#es"]],"geography_level":"island","service":"PEDIATRIA_AP","age_group_original":"Servicio Pediatría AP; edad individual no publicada","activity_type":kind,"place":r["LUGAR_CONSULTA_CODE"],"value":value,"unit":{"consultations":"consultations","distinct_persons":"persons","frequentation":"consultations_per_assigned_person_year"}[kind],"value_status":"OBSERVED" if value is not None else "NOT_AVAILABLE","method_id":"siap_original_service_v1","reference_period":r["TIME_PERIOD_CODE"]})
    return out
def waiting(sources):
    out=[]
    for kind,col,allowed in [("outpatient","CONSULTAS_EXTERNAS",{"PEDIATRIA","CIRUGIA_PEDIATRICA"}),("surgical","SERVICIOS_QUIRURGICOS",{"CIRUGIA_PEDIATRICA"})]:
        for r in read(ROOT/sources[kind]["path"]):
            if r["TERRITORIO_CODE"]!="ES70" or r[col+"_CODE"] not in allowed or r["TIME_PERIOD_CODE"]<"2017": continue
            year,month=map(int,r["TIME_PERIOD_CODE"].split("-M"))
            value=numeric(r["OBS_VALUE"],r.get("ESTADO_OBSERVACION#es",""))
            status="MISSING" if value is None else ("ZERO_PUBLISHED" if value==0 else "OBSERVED")
            # Do not release small surgical counts or permit subtraction through bands.
            suppressed=value is not None and 0<value<5
            out.append(provenance(kind,sources)|{"reference_date":f"{year}-{month:02d}-{calendar.monthrange(year,month)[1]}","reference_period":r["TIME_PERIOD_CODE"],"specialty":r[col+"_CODE"],"specialty_label":r[col+"#es"],"wait_type":kind,"geography_level":"autonomous_community","geography_id":"canarias","pending_patients":None if suppressed else value,"value_status":"SUPPRESSED" if suppressed else status,"data_status":"ADMINISTRATIVE_STOCK","time_band":r.get("TIEMPO_ESPERA_CODE","_T"),"mean_wait_days_if_available":None,"age_group_original":"Especialidad pediátrica; edad individual no publicada","comparability_status":"ADMIT_WITH_LIMITATIONS","method_id":"waiting_regional_stock_v1"})
    # Suppress all bands in any affected cut, avoiding secondary disclosure.
    affected={(r["reference_date"],r["wait_type"],r["specialty"]) for r in out if r["value_status"]=="SUPPRESSED"}
    for r in out:
        if (r["reference_date"],r["wait_type"],r["specialty"]) in affected: r["pending_patients"]=None;r["value_status"]="SUPPRESSED"
    return out
HBSC=[
 ("breakfast_weekdays","Desayuna cinco días entre semana",25,5,6,1293,51.5),
 ("sleep_weekdays","Duerme cinco horas o menos entre semana",34,0,6,1281,10.2),
 ("physical_activity","Actividad física: siete días en la última semana",49,7,8,1876,19.8),
 ("perceived_health","Salud percibida excelente",128,3,4,1259,25.4)]
def survey(sources):
    pdf=PdfReader(ROOT/sources["hbsc"]["path"]);out=[]
    for indicator,label,page,index,categories,expected_n,expected_value in HBSC:
        text=pdf.pages[page-1].extract_text()
        patterns=[("11–18","Total\\s+"),("11–12","11-12 años\\s+"),("13–14","13-14 años\\s+"),("15–16","15-16 años\\s+"),("17–18","17-18 años\\s+")]
        for age,prefix in patterns:
            match=re.search(prefix+r"(\d+)\s+"+r"\s+".join([r"(\d+,\d+)%"]*categories),text)
            if not match: raise ValueError(f"Missing HBSC row {indicator}/{age}")
            n=int(match[1]);value=float(match[index+2].replace(",","."))
            if age=="11–18" and (n!=expected_n or value!=expected_value): raise ValueError("HBSC transcription drift")
            if n<100: raise ValueError("Small HBSC stratum")
            out.append(provenance("hbsc",sources)|{"indicator_id":indicator,"indicator_label":label,"value":value,"unit":"percent","reference_period":"2022","geography_level":"autonomous_community","geography_id":"canarias","age_group_original":age+" años","universe":"Adolescentes escolarizados; 17–18 solo quienes permanecen en educación","n_valid_published":n,"denominator":None,"ci_lower":None,"ci_upper":None,"weighting":"Pesos muestrales de la estimación publicada; N redondeado","value_status":"SURVEY_ESTIMATE","comparability_status":"ADMIT_WITH_LIMITATIONS","method_id":"hbsc2022_published_weighted_v1","source_page":page,"publication_date":"2025 (cita); NIPO 133-26-004-4","last_update":None})
    return out
def write(name,rows):
    path=ROOT/"data/curated"/name
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
    return path
def main():
    sources=json.loads((ROOT/"data/manifests/phase6_sources.json").read_text())
    for s in sources.values():
        if sha(ROOT/s["path"])!=s["checksum"]: raise ValueError("Frozen source checksum mismatch")
    a,w,h=activity(sources),waiting(sources),survey(sources)
    for kind in ("consultations","distinct_persons","frequentation"):
        totals=[r for r in a if r["activity_type"]==kind and r["place"]=="_T"]
        assert len(totals)==126
        assert {(r["island_id"],r["year"]) for r in totals}=={(i,y) for i in ISLANDS.values() for y in range(2007,2025)}
    assert len({(r["year"],r["island_id"],r["activity_type"],r["place"]) for r in a})==len(a)
    paths=[write("pediatric_primary_care_activity.csv",a),write("pediatric_waiting_list.csv",w),write("adolescent_survey_indicator.csv",h)]
    manifest={"parser_version":PARSER,"sources":sources,"admission":{"siap":"ADMIT_WITH_LIMITATIONS","waiting_regional":"ADMIT_WITH_LIMITATIONS","waiting_island":"HOLD","hbsc":"ADMIT_WITH_LIMITATIONS","bdcap":"HOLD","vaccination":"HOLD","screening":"HOLD","esde_estudes":"HOLD","hospital_enrichment":"HOLD","early_intervention":"RESEARCH_ONLY"},"outputs":{str(p.relative_to(ROOT)):{"sha256":sha(p),"rows":len(read(p))} for p in paths}}
    (ROOT/"data/manifests/phase6_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({p.name:len(read(p)) for p in paths}))
if __name__=="__main__": main()
