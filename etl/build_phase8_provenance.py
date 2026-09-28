#!/usr/bin/env python3
"""Attach stable source records and explicit lineage to every Phase 8 metric."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def write(path,payload):
 target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def source(source_id,name,organization,domain,description,contains,universe,geography,period,frequency,fmt,license_name,version,status,acquired,url,used_in,checksum=None):
 return {"source_id":source_id,"name":name,"organization":organization,"domain":domain,"description":description,"contains":contains,"universe_age":universe,"geographic_disaggregation":geography,"available_period":period,"update_frequency":frequency,"format":fmt,"license":license_name,"version_used":version,"integration_status":status,"last_acquired_at":acquired,"official_url":url,"used_in":used_in,"checksum":checksum}
sources=[
 source("ISTAC:E54086A_000001","Profesionales de Atención Primaria","ISTAC / Servicio Canario de Salud","Atención Primaria","Serie SIAP de profesionales y ratio por profesional.","Profesionales AP, tipo profesional, territorio, año.","Servicio Pediatría AP; no edad individual.","Canarias e isla","2004–2024","Anual","CSV/API","Aviso legal ISTAC","snapshot Phase 0","integrada","2026-09-27","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000001/~latest.csv",["pediatricians_ap","assigned_children_per_pediatrician","consultations_per_pediatrician"]),
 source("ISTAC:E54086A_000002","Población asignada en Atención Primaria","ISTAC / Servicio Canario de Salud","Demografía","Población asignada por edad, sexo, territorio y año.","Población asignada SIAP por grupos quinquenales.","Todas las edades; PedsData suma 0–4, 5–9 y 10–14.","Canarias e isla","2004–2024","Anual","CSV/API","Aviso legal ISTAC","snapshot Phase 0","integrada","2026-09-27","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000002/~latest.csv",["child_population_assigned_0_14","assigned_children_per_pediatrician"]),
 source("ISTAC:E54086A_000005","Consultas de Atención Primaria","ISTAC / Servicio Canario de Salud","Atención Primaria","Actividad de consultas por servicio, lugar, territorio y año.","Consultas de Pediatría AP.","Servicio Pediatría AP; no edad individual.","Canarias e isla","2007–2024","Anual","CSV/API","Aviso legal ISTAC","1.1","integrada","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000005/1.1.csv",["pediatric_consultations","consultations_per_pediatrician"]),
 source("ISTAC:E54086A_000007","Personas distintas atendidas en AP","ISTAC / Servicio Canario de Salud","Atención Primaria","Personas distintas por servicio, lugar, territorio y año.","Usuarios distintos de Pediatría AP.","Servicio Pediatría AP; no edad individual.","Canarias e isla","2007–2024","Anual","CSV/API","Aviso legal ISTAC","1.1","integrada","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000007/1.1.csv",["pediatric_distinct_users"]),
 source("ISTAC:E54086A_000009","Frecuentación en Atención Primaria","ISTAC / Servicio Canario de Salud","Atención Primaria","Frecuentación publicada por servicio, territorio y año.","Consultas por población asignada y año.","Servicio Pediatría AP; no edad individual.","Canarias e isla","2007–2024","Anual","CSV/API","Aviso legal ISTAC","1.1","integrada","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E54086A_000009/1.1.csv",["pediatric_frequentation"]),
 source("ISTAC:E30304A_000008","Nacimientos según madurez","ISTAC","Perinatal","Nacimientos de madres residentes según madurez del parto.","Nacimientos, prematuros y denominadores.","Perinatal.","Canarias e isla","1999–2024","Anual","CSV/API","Aviso legal ISTAC","latest audited","integrada","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E30304A_000008/~latest.csv",["births","preterm_rate"]),
 source("ISTAC:C00045A_000002","Listas de espera de consultas externas","ISTAC / SCS","Atención Primaria","Stock de pacientes pendientes por especialidad en fecha de corte.","Pediatría y Cirugía Pediátrica; stock, no demora individual.","Especialidad; edad individual no publicada.","Canarias validada; categorías insulares en HOLD","2017–2025","Semestral","CSV/API","Aviso legal ISTAC","1.3","parcial","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/C00045A_000002/1.3.csv",["pediatric_outpatient_waiting_stock"]),
 source("ISTAC:E30414A_000009","Encuesta de Morbilidad Hospitalaria","ISTAC / INE","Hospitalización","Altas de residentes canarios por edad y diagnóstico principal.","Altas, estancias y estancia media.","Grupos de edad pediátricos originales.","Canarias","2020–2024","Anual","CSV/API","Aviso legal ISTAC","latest audited","integrada","2026-09-28","https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E30414A_000009/~latest.csv",["pediatric_hospital_discharges_selected"]),
 source("INE:ADRH","Atlas de Distribución de Renta de los Hogares","Instituto Nacional de Estadística","Socioeconómico","Indicadores de renta de hogares y personas.","Renta media y mediana general.","Población general; no renta infantil.","Municipio","2023","Anual","JSON/API","INE reutilización / CC BY 4.0","ADRH-2023","integrada","2026-09-28","https://www.ine.es/experimental/atlas/experimental_atlas.htm",["income_mean_per_person"]),
 source("ISTAC:GRID_2024","Malla de población de Canarias 250 m","ISTAC","Demografía","Población residente georreferenciada en malla regular.","Población 0–14 por celda.","0–14.","Malla 250 m","2024","Anual","GeoJSON","Aviso legal ISTAC","2024","integrada","2026-09-27","https://datos.canarias.es/catalogos/estadisticas/dataset/malla-de-poblacion-de-canarias",["child_density","accessibility_ap"]),
 source("ISTAC:DEGURBA_2021","Grado de urbanización DEGURBA","ISTAC","Geográfico","Clasificación oficial de celdas por grado de urbanización.","Centro urbano, agrupación urbana y rural.","Población general; PedsData intersecta población infantil.","Malla 1 km / derivación municipal","2021","No especificada","GeoJSON","Aviso legal ISTAC","2021","integrada","2026-09-28","https://datos.canarias.es/catalogos/estadisticas/dataset/grado-de-urbanizacion",["degurba","child_density"]),
 source("GOB_CAN:AIR_2025","Red Canaria de Calidad del Aire","Gobierno de Canarias","Ambiental","Observaciones medidas en estaciones de calidad del aire.","PM10, PM2,5, NO2 y otros contaminantes.","Ambiental; sin edad.","Estación","2025","Horaria/diaria","XLSX/ZIP","Condiciones Gobierno de Canarias","2025 validated extract","integrada","2026-09-28","https://www3.gobiernodecanarias.org/medioambiente/calidaddelaire/",["PM10","PM2.5","NO2"]),
 source("SCS:REGCESS_U20","Registro General de Centros Sanitarios U20","Ministerio de Sanidad / SCS","Atención Primaria","Registro oficial de centros sanitarios con oferta asistencial U20.","Centros, coordenadas y cartera declarada.","Recursos sanitarios pediátricos.","Recurso puntual; 7 islas","Catálogo 2026","Según registro","XLSX/HTML","Reutilización institucional; verificar por descarga","snapshot 2026-09-27","integrada","2026-09-27","https://regcess.mscbs.es/regcessWeb/inicioBuscarCentrosAction.do",["accessibility_ap"]),
 source("OSM:CANARY_2026_09_26","OpenStreetMap Canarias congelado","OpenStreetMap contributors","Geográfico","Snapshot congelado de la red viaria de Canarias.","Grafo viario y componentes terrestres.","No aplica.","Red viaria; 7 islas y La Graciosa separada","2026-09-26","Snapshot","PBF","ODbL 1.0","canary-islands-260926","integrada","2026-09-26","https://download.geofabrik.de/europe/spain/canary-islands.html",["accessibility_ap"]),
 source("OSRM:5.27.1","OSRM local","Project OSRM","Geográfico","Motor reproducible usado para tiempos y distancias por carretera.","Rutas sobre snapshot OSM congelado.","No aplica.","Componentes terrestres","Cálculo 2026-09-28","Por snapshot","Container/graph","BSD-2-Clause","5.27.1","integrada","2026-09-28","https://github.com/Project-OSRM/osrm-backend/releases/tag/v5.27.1",["accessibility_ap"]),
]
checksum_map={
 "ISTAC:E54086A_000005":"0918db3dab0ede536f57176f40634e5538ecf71980d3b68649ffab36e507edda",
 "ISTAC:E54086A_000007":"9e648085116b93f93f6b1b1bebe2cfb01993c4f41102fde53e6ce8e368064eca",
 "ISTAC:E54086A_000009":"cabfed254e7d144e9fd060cb8f22047ed9a56f026ee1f577beaa4022e6fbd7f4",
 "ISTAC:C00045A_000002":"14eb84d8467658ac174de5625f0e2a85d55b460bb2531397b6e27a3b7db6648e",
 "ISTAC:E30414A_000009":"fb0682109de1f708c1f623b7d3757798ad5a2ce0b08700e7cef0eb58c1030a0c",
 "ISTAC:E30304A_000008":"5eec3ff99c5550b78f5abec31493259a5f05eeac47f3d0f9627bc050c0310bba",
 "ISTAC:DEGURBA_2021":"064c675f671435b5cde9b0e9fe6ee1895518fe248a9c67bbc3db0c72349d8952",
 "GOB_CAN:AIR_2025":"dd9798ea80d49f53dd5ccabcd6b5923cfbae56ee638ecd2424b9bfbf607260f5",
 "OSM:CANARY_2026_09_26":"2c5f0f3c7b42fc68f6d1bf64679642edb86f546fe510e6f081a07a4d398379f9",
 "OSRM:5.27.1":"f0b0700b3224c76f6b62682102cbf2002936164d1de7bb28d8820af81578a37e",
}
for source_item in sources:source_item["checksum"]=checksum_map.get(source_item["source_id"],source_item["checksum"])
formulas={
 "child_population_assigned_0_14":{"expression":"Y0T4 + Y5T9 + Y10T14","inputs":[{"metric":"Población asignada 0–4","source_id":"ISTAC:E54086A_000002"},{"metric":"Población asignada 5–9","source_id":"ISTAC:E54086A_000002"},{"metric":"Población asignada 10–14","source_id":"ISTAC:E54086A_000002"}],"transformations":["Filtrar sexo total","Sumar grupos etarios originales sin interpolar"],"rounding":"entero publicado"},
 "assigned_children_per_pediatrician":{"expression":"población asignada al servicio / profesionales de Pediatría AP","inputs":[{"metric":"Población asignada","source_id":"ISTAC:E54086A_000002"},{"metric":"Pediatras AP","source_id":"ISTAC:E54086A_000001"}],"transformations":["Se conserva el ratio publicado por SIAP"],"rounding":"precisión publicada"},
 "pediatric_frequentation":{"expression":"consultas de Pediatría AP / población asignada / año","inputs":[{"metric":"Consultas","source_id":"ISTAC:E54086A_000005"},{"metric":"Población asignada","source_id":"ISTAC:E54086A_000002"}],"transformations":["Se conserva el indicador publicado"],"rounding":"2 decimales publicados"},
 "consultations_per_pediatrician":{"expression":"consultas totales de Pediatría AP / pediatras AP","inputs":[{"metric":"Consultas","source_id":"ISTAC:E54086A_000005"},{"metric":"Pediatras AP","source_id":"ISTAC:E54086A_000001"}],"transformations":["Unir por isla y año","Excluir denominadores nulos o cero"],"rounding":"4 decimales en datos; 2 en UI"},
 "preterm_rate":{"expression":"nacimientos prematuros / nacimientos × 100","inputs":[{"metric":"Nacimientos prematuros","source_id":"ISTAC:E30304A_000008"},{"metric":"Nacimientos","source_id":"ISTAC:E30304A_000008"}],"transformations":["Misma isla y año"],"rounding":"2 decimales"},
 "child_density":{"expression":"población infantil 0–14 / superficie municipal km²","inputs":[{"metric":"Población 0–14","source_id":"ISTAC:GRID_2024"},{"metric":"Superficie municipal","source_id":"ISTAC:DEGURBA_2021"}],"transformations":["Intersección espacial y agregación municipal"],"rounding":"3 decimales"},
 "degurba":{"expression":"argmax(% centro urbano, % agrupación urbana, % rural)","inputs":[{"metric":"DEGURBA por celda","source_id":"ISTAC:DEGURBA_2021"},{"metric":"Población 0–14","source_id":"ISTAC:GRID_2024"}],"transformations":["Ponderar categorías por niños","Seleccionar categoría dominante"],"rounding":"categórico"},
 "accessibility_ap":{"expression":"min(tiempo OSRM por carretera desde representative_point de celda hasta destino VERIFIED del mismo componente terrestre)","inputs":[{"metric":"Población origen 0–14","source_id":"ISTAC:GRID_2024"},{"metric":"Recurso destino pediátrico","source_id":"SCS:REGCESS_U20"},{"metric":"Red viaria","source_id":"OSM:CANARY_2026_09_26"},{"metric":"Motor de rutas","source_id":"OSRM:5.27.1"}],"transformations":["Punto representativo de celda","Preselección de destinos por isla","Matrices OSRM","La Graciosa = requires_interisland_transfer"],"rounding":"segundos internos; minutos UI a 1 decimal"},
}
metric_sources={
 "child_population_assigned_0_14":["ISTAC:E54086A_000002"],"pediatricians_ap":["ISTAC:E54086A_000001"],
 "assigned_children_per_pediatrician":["ISTAC:E54086A_000001","ISTAC:E54086A_000002"],
 "pediatric_consultations":["ISTAC:E54086A_000005"],"pediatric_distinct_users":["ISTAC:E54086A_000007"],
 "pediatric_frequentation":["ISTAC:E54086A_000009","ISTAC:E54086A_000005","ISTAC:E54086A_000002"],
 "consultations_per_pediatrician":["ISTAC:E54086A_000005","ISTAC:E54086A_000001"],
 "births":["ISTAC:E30304A_000008"],"preterm_rate":["ISTAC:E30304A_000008"],
 "pediatric_outpatient_waiting_stock":["ISTAC:C00045A_000002"],"pediatric_hospital_discharges_selected":["ISTAC:E30414A_000009"],
 "income_mean_per_person":["INE:ADRH"],"child_density":["ISTAC:GRID_2024","ISTAC:DEGURBA_2021"],"degurba":["ISTAC:DEGURBA_2021","ISTAC:GRID_2024"],
 "PM10":["GOB_CAN:AIR_2025"],"PM2.5":["GOB_CAN:AIR_2025"],"NO2":["GOB_CAN:AIR_2025"],
 "child_population_grid_0_14":["ISTAC:GRID_2024"],"verified_pediatric_facilities":["SCS:REGCESS_U20"],
 "accessibility_ap":["ISTAC:GRID_2024","SCS:REGCESS_U20","OSM:CANARY_2026_09_26","OSRM:5.27.1"],
}
catalog=load("data/semantic/metrics_catalog.json")
existing={m["metric_id"] for m in catalog["metrics"]}
catalog["metrics"].extend(m for m in load("data/semantic/phase8_base_metrics.json")["metrics"] if m["metric_id"] not in existing)
for metric in catalog["metrics"]:
 metric["source_ids"]=metric_sources[metric["metric_id"]]
 metric["formula"]=formulas.get(metric["metric_id"])
 metric["transformations"]=formulas.get(metric["metric_id"],{}).get("transformations",["Filtrado y selección sin alterar la escala publicada"])
 metric["rounding"]=formulas.get(metric["metric_id"],{}).get("rounding","precisión publicada; formato UI máximo 2 decimales")
 metric["limitations"]=[metric["description"],"No se representa por debajo de "+", ".join(metric["geography_levels"])+"."] 
 metric["visualizations"]=["series","compare","explorer"]+([ "map"] if metric["map_allowed"] else [])
 metric["lineage_version"]="phase8-v1"
 if metric["status"] in {"DERIVED_RATE","ESTIMATED"} and not metric["formula"]:raise ValueError("Derived metric without formula: "+metric["metric_id"])
 if metric["map_allowed"] and not all([metric["map_geography"],metric["classification_method"],metric["time_end"]]):raise ValueError("Map metric missing contract: "+metric["metric_id"])
registered={item["source_id"] for item in sources}
for source in sources:
 source["used_in"]=sorted(set(source["used_in"]+[metric_id for metric_id,ids in metric_sources.items() if source["source_id"] in ids]))
for metric in catalog["metrics"]:
 if not metric["source_ids"] or not set(metric["source_ids"])<=registered:raise ValueError("Unregistered source for "+metric["metric_id"])
write("data/semantic/sources_catalog.json",{"version":"phase8-v1","sources":sources})
write("data/semantic/metrics_catalog.json",catalog)
write("apps/web/src/data/sources-catalog.json",{"version":"phase8-v1","sources":sources})
write("apps/web/src/data/metrics-catalog.json",catalog)
print("Registered",len(sources),"sources and",len(catalog["metrics"]),"traceable metrics")
