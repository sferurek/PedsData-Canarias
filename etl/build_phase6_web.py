"""Create route-specific payloads after admitted CSV QA. Home does not import these."""
import csv,json,hashlib
from pathlib import Path
from build_phase6 import ISLANDS,ROOT
def read(path):
 with path.open() as f:return list(csv.DictReader(f))
def num(v):return None if v=="" else float(v)
a=read(ROOT/"data/curated/pediatric_primary_care_activity.csv")
w=read(ROOT/"data/curated/pediatric_waiting_list.csv")
h=read(ROOT/"data/curated/adolescent_survey_indicator.csv")
sources=json.loads((ROOT/"data/manifests/phase6_sources.json").read_text())
staffpath=ROOT/"docs/evidence/siap_professionals.csv"
staff={}
for r in read(staffpath):
 if r["TIPO_PROFESIONAL_ATENCION_PRIMARIA_CODE"]!="PEDIATRIA_AP" or r["TERRITORIO#es"] not in ISLANDS or int(r["TIME_PERIOD_CODE"])<2007:continue
 k=(ISLANDS[r["TERRITORIO#es"]],int(r["TIME_PERIOD_CODE"]))
 staff.setdefault(k,{})[r["MEDIDAS_CODE"]]=num(r["OBS_VALUE"])
out={"islands":[{"id":i,"name":n} for n,i in ISLANDS.items()],"sources":sources,"staff_source":{"url":"https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000001/~latest.csv","frozen_path":"docs/evidence/siap_professionals.csv","checksum":hashlib.sha256(staffpath.read_bytes()).hexdigest(),"version":"snapshot_phase0_2026-09-27"},"activity":[{"island":r["island_id"],"year":int(r["year"]),"metric":r["activity_type"],"place":r["place"],"value":num(r["value"]),"status":r["value_status"]} for r in a],"staff":[{"island":i,"year":y,"pediatricians":v.get("NUMERO_PROFESIONALES_AP"),"assigned_per_professional":v.get("RATIO_PROFESIONAL")} for (i,y),v in staff.items()],"waiting":[{"date":r["reference_date"],"specialty":r["specialty"],"label":r["specialty_label"],"kind":r["wait_type"],"band":r["time_band"],"value":num(r["pending_patients"]),"status":r["value_status"]} for r in w]}
(ROOT/"apps/web/src/data/utilization.json").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":"))+"\n")
for r in h:
 for k in ["value","n_valid_published","source_page"]:r[k]=num(r[k])
(ROOT/"apps/web/src/data/adolescence.json").write_text(json.dumps(h,ensure_ascii=False,separators=(",",":"))+"\n")
print("Route payload bytes",[(n,(ROOT/"apps/web/src/data"/n).stat().st_size) for n in ["utilization.json","adolescence.json"]])
